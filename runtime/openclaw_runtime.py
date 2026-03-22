from __future__ import annotations

from typing import Any


class OpenClawRuntime:
    """Interface for actual OpenClaw runtime integration."""

    def run_agent(self, role: str, prompt: str, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class MockRuntime(OpenClawRuntime):
    """Deterministic fallback for harness testing without external dependencies."""

    def run_agent(self, role: str, prompt: str, context: dict[str, Any]) -> dict[str, Any]:
        mission = context.get("mission", "")
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
            draft = context.get("artifact", "")
            has_metrics = "Success" in draft
            return {
                "verdict": "pass" if has_metrics else "repair",
                "scores": {
                    "goal_alignment": 5,
                    "completeness": 4 if has_metrics else 2,
                    "quality": 4,
                },
                "reasons": ["Contains mission mapping"],
                "repair_instructions": [] if has_metrics else ["Add success metrics section"],
            }
        if role == "qa":
            return {"verdict": "pass", "notes": ["Document exists and is storable"]}
        return {"message": f"No-op role: {role}", "prompt": prompt}
