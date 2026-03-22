from __future__ import annotations

from typing import Any


class ContractViolationError(ValueError):
    pass


# Starter 8 roles + extension-ready keys.
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "director": ("project_brief", "priority_policy"),
    "planner": ("tasks",),
    "researcher": ("research_note", "source_list", "confidence_note"),
    "architect": ("architecture_plan",),
    "builder": ("artifact",),
    "critic": ("verdict", "scores", "reasons", "repair_instructions"),
    "qa": ("verdict", "notes"),
    "memory_curator": ("updates",),
}

ALLOWED_VERDICTS: dict[str, set[str]] = {
    "critic": {"pass", "repair", "fail"},
    "qa": {"pass", "fail"},
}


def validate_agent_response(role: str, payload: dict[str, Any]) -> None:
    required = REQUIRED_FIELDS.get(role, ())
    missing = [key for key in required if key not in payload]
    if missing:
        raise ContractViolationError(f"{role} missing required fields: {missing}")

    if role in ALLOWED_VERDICTS:
        verdict = payload.get("verdict")
        if verdict not in ALLOWED_VERDICTS[role]:
            raise ContractViolationError(
                f"{role} verdict must be one of {sorted(ALLOWED_VERDICTS[role])}, got={verdict!r}"
            )

    if role == "planner":
        tasks = payload.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            raise ContractViolationError("planner response must contain non-empty tasks list")
        for key in ("task_id", "title", "description"):
            if key not in tasks[0]:
                raise ContractViolationError(f"planner first task missing {key}")

    if role == "critic":
        if not isinstance(payload.get("scores"), dict):
            raise ContractViolationError("critic scores must be object")
        if not isinstance(payload.get("reasons"), list):
            raise ContractViolationError("critic reasons must be list")
        if not isinstance(payload.get("repair_instructions"), list):
            raise ContractViolationError("critic repair_instructions must be list")

    if role == "qa":
        if not isinstance(payload.get("notes"), list):
            raise ContractViolationError("qa notes must be list")
