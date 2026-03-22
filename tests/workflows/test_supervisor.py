import unittest
from pathlib import Path

from orchestrator.harness import AgentHarness
from orchestrator.models import GoalSpec
from runtime.openclaw_runtime import MockRuntime, OpenClawRuntime


class FailRuntime(OpenClawRuntime):
    def run_agent(self, role, prompt, context):
        if role == "director":
            return {"project_brief": "x", "priority_policy": ["a"]}
        if role == "planner":
            return {"tasks": [{"task_id": "t1", "title": "t", "description": "d"}]}
        if role == "builder":
            return {"artifact": "bad artifact"}
        if role == "critic":
            return {
                "verdict": "fail",
                "scores": {
                    "goal_alignment": 1,
                    "factuality": 1,
                    "completeness": 1,
                    "logic": 1,
                    "reproducibility": 1,
                    "quality": 1,
                },
                "reasons": ["bad"],
                "repair_instructions": [],
            }
        if role == "qa":
            return {"verdict": "pass", "notes": ["ok"]}
        if role == "memory_curator":
            return {"updates": ["none"]}
        return {"updates": ["noop"]}


class SupervisorWorkflowTests(unittest.TestCase):
    def test_demo_runtime_reaches_final_state(self):
        harness = AgentHarness(Path(".").resolve(), MockRuntime())
        result = harness.run_stage1_prd_loop(
            GoalSpec(project_id="ut-demo", mission="m", budget_limits={"max_steps": 10, "max_minutes": 1})
        )
        self.assertEqual(result["state"], "KNOWLEDGE_UPDATED")

    def test_repeated_review_fail_escalates(self):
        harness = AgentHarness(Path(".").resolve(), FailRuntime())
        result = harness.run_stage1_prd_loop(
            GoalSpec(project_id="ut-fail", mission="m", budget_limits={"max_steps": 10, "max_minutes": 1})
        )
        self.assertEqual(result["state"], "REVIEW_FAILED")
        self.assertEqual(result["escalation"], "human_required")


if __name__ == "__main__":
    unittest.main()
