from __future__ import annotations

from typing import Any


class OpenClawRuntime:
    """Interface for actual OpenClaw runtime integration."""

    def run_agent(self, role: str, prompt: str, context: dict[str, Any]) -> dict[str, Any] | str:
        raise NotImplementedError


class MockRuntime(OpenClawRuntime):
    """Deterministic fallback for harness testing without external dependencies."""

    def run_agent(self, role: str, prompt: str, context: dict[str, Any]) -> dict[str, Any] | str:
        input_data = context.get("input_data", {})
        goal = input_data.get("goal", {})
        mission = goal.get("mission", "")

        if role == "director":
            return {
                "project_brief": f"Mission locked: {mission}",
                "priority_policy": ["goal_alignment", "quality", "safety"],
            }

        if role == "planner":
            return {
                "tasks": [
                    {
                        "task_id": "task-1",
                        "title": "Draft PRD",
                        "description": "Create a first PRD draft from goals and constraints.",
                    }
                ]
            }

        if role == "builder":
            return {
                "artifact": f"PRD Draft for mission: {mission}\n\n- Scope\n- Constraints\n- Success Metrics"
            }

        if role == "critic":
            draft = input_data.get("artifact", "")
            has_metrics = "Success" in draft
            if "bad" in draft.lower():
                verdict = "fail"
            else:
                verdict = "pass" if has_metrics else "repair"
            return {
                "verdict": verdict,
                "scores": {
                    "goal_alignment": 5,
                    "factuality": 4,
                    "completeness": 5 if has_metrics else 2,
                    "logic": 4,
                    "reproducibility": 4,
                    "quality": 4,
                    "originality": 3,
                    "usefulness": 4,
                    "clarity": 4,
                    "market_value": 3,
                    "differentiation": 3,
                },
                "reasons": ["Contains mission mapping"],
                "repair_instructions": [] if has_metrics else ["Add success metrics section"],
            }

        if role == "qa":
            return {"verdict": "pass", "notes": ["Document exists and is storable"]}

        if role == "memory_curator":
            return {"updates": ["No-op in mock runtime"]}

        return {"updates": [f"No-op role: {role}"], "notes": [prompt]}
