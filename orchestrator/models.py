from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class GoalSpec:
    project_id: str
    mission: str
    deliverables: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    budget_limits: dict[str, Any] = field(default_factory=dict)
    stop_conditions: list[str] = field(default_factory=list)
    priority_order: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TaskSpec:
    task_id: str
    title: str
    description: str
    owner: str
    depends_on: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    expected_outputs: list[str] = field(default_factory=list)
    status: str = "PENDING"
    retry_count: int = 0
    priority: int = 3
    evaluation_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvalSpec:
    artifact_id: str
    reviewer: str
    verdict: str
    scores: dict[str, int]
    reasons: list[str]
    repair_instructions: list[str]
    risk_level: str
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DecisionSpec:
    decision_id: str
    context: str
    chosen_option: str
    rejected_options: list[str]
    reasoning_summary: str
    revisit_conditions: list[str]
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class FailureSpec:
    failure_id: str
    task_id: str
    failure_type: str
    observed_problem: str
    root_cause: str
    preventive_rule: str
    retry_history: list[str]
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
