from __future__ import annotations

from pathlib import Path

from orchestrator.memory_store import MemoryStore
from orchestrator.models import DecisionSpec, EvalSpec, FailureSpec, GoalSpec, TaskSpec
from orchestrator.state_machine import FlowState, assert_transition
from runtime.openclaw_runtime import OpenClawRuntime


class AgentHarness:
    def __init__(self, repo_root: Path, runtime: OpenClawRuntime) -> None:
        self.repo_root = repo_root
        self.runtime = runtime
        self.memory = MemoryStore(repo_root)

    def run_stage1_prd_loop(self, goal: GoalSpec) -> dict:
        state = FlowState.GOAL_INGESTED
        self.memory.append_state_event(goal.project_id, state.value, goal.to_dict())

        state = self._advance(goal.project_id, state, FlowState.MISSION_LOCKED, {"mission": goal.mission})
        state = self._advance(goal.project_id, state, FlowState.PLAN_CREATED, {})
        state = self._advance(goal.project_id, state, FlowState.TASKS_CREATED, {})
        state = self._advance(goal.project_id, state, FlowState.TASKS_ASSIGNED, {})
        state = self._advance(goal.project_id, state, FlowState.IN_PROGRESS, {})

        plan = self.runtime.run_agent("planner", "Create task tree", {"mission": goal.mission})
        task = TaskSpec(
            task_id=plan["tasks"][0]["task_id"],
            title=plan["tasks"][0]["title"],
            description=plan["tasks"][0]["description"],
            owner="builder",
            expected_outputs=["prd_draft.md"],
            status="IN_PROGRESS",
        )
        self.memory.write_json(f"memory/tasks/active/{task.task_id}.json", task.to_dict())

        built = self.runtime.run_agent("builder", "Generate PRD draft", {"mission": goal.mission})
        artifact_text = built["artifact"]
        draft_path = self.repo_root / "artifacts" / "drafts" / f"{goal.project_id}-prd.md"
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(artifact_text, encoding="utf-8")

        state = self._advance(goal.project_id, state, FlowState.SUBMITTED_FOR_REVIEW, {"artifact": str(draft_path)})
        critique = self.runtime.run_agent("critic", "Evaluate artifact", {"artifact": artifact_text})

        if critique["verdict"] == "repair":
            eval_report = EvalSpec(
                artifact_id=draft_path.name,
                reviewer="critic",
                verdict="repair",
                scores=critique["scores"],
                reasons=critique["reasons"],
                repair_instructions=critique["repair_instructions"],
                risk_level="medium",
            )
            self.memory.write_json(f"memory/evaluations/{goal.project_id}-critic-repair.json", eval_report.to_dict())
            state = self._advance(goal.project_id, state, FlowState.REVIEW_REPAIR, eval_report.to_dict())
            state = self._advance(goal.project_id, state, FlowState.REPAIRING, {})
            repaired_text = artifact_text + "\n\n## Success Metrics\n- Quality gate pass rate"
            draft_path.write_text(repaired_text, encoding="utf-8")
            artifact_text = repaired_text
            state = self._advance(goal.project_id, state, FlowState.IN_PROGRESS, {"repaired": True})
            state = self._advance(goal.project_id, state, FlowState.SUBMITTED_FOR_REVIEW, {})
            critique = self.runtime.run_agent("critic", "Re-evaluate artifact", {"artifact": artifact_text})

        verdict = "REVIEW_PASSED" if critique["verdict"] == "pass" else "REVIEW_FAILED"
        state = self._advance(goal.project_id, state, FlowState[verdict], critique)

        if state == FlowState.REVIEW_FAILED:
            failure = FailureSpec(
                failure_id=f"failure-{goal.project_id}",
                task_id=task.task_id,
                failure_type="critic_fail",
                observed_problem="Artifact failed critic gate",
                root_cause="Insufficient completeness",
                preventive_rule="Require mandatory sections template",
                retry_history=["attempt-1"],
            )
            self.memory.write_json(f"memory/failures/{goal.project_id}-critic-fail.json", failure.to_dict())
            raise RuntimeError("Critic gate failed; replan required")

        state = self._advance(goal.project_id, state, FlowState.INTEGRATING, {})
        state = self._advance(goal.project_id, state, FlowState.QA_REVIEW, {})
        qa = self.runtime.run_agent("qa", "Validate final artifact", {"artifact": artifact_text})
        qa_state = FlowState.QA_PASSED if qa.get("verdict") == "pass" else FlowState.QA_FAILED
        state = self._advance(goal.project_id, state, qa_state, qa)
        if state == FlowState.QA_FAILED:
            raise RuntimeError("QA failed; architect + builder re-entry required")

        final_path = self.repo_root / "artifacts" / "final" / f"{goal.project_id}-final-prd.md"
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_path.write_text(artifact_text, encoding="utf-8")

        state = self._advance(goal.project_id, state, FlowState.FINAL_PACKAGING, {"final": str(final_path)})
        state = self._advance(goal.project_id, state, FlowState.DELIVERED, {})
        state = self._advance(goal.project_id, state, FlowState.RETROSPECTIVE_STORED, {})

        decision = DecisionSpec(
            decision_id=f"decision-{goal.project_id}",
            context="Stage1 demo loop",
            chosen_option="Use stage1 PRD closed loop",
            rejected_options=["Skip critic gate"],
            reasoning_summary="Keeps traceable quality gate before expansion",
            revisit_conditions=["When moving to multi-task parallel stage"],
        )
        self.memory.write_json(f"memory/decisions/{goal.project_id}-stage1.json", decision.to_dict())
        state = self._advance(goal.project_id, state, FlowState.KNOWLEDGE_UPDATED, {})

        self.memory.write_json(f"memory/tasks/completed/{task.task_id}.json", {**task.to_dict(), "status": "DONE"})
        return {
            "project_id": goal.project_id,
            "final_artifact": str(final_path),
            "state": state.value,
        }

    def _advance(self, project_id: str, current: FlowState, nxt: FlowState, payload: dict) -> FlowState:
        assert_transition(current, nxt)
        self.memory.append_state_event(project_id, nxt.value, payload)
        return nxt
