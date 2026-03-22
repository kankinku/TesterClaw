from __future__ import annotations

from enum import Enum


class FlowState(str, Enum):
    GOAL_INGESTED = "GOAL_INGESTED"
    MISSION_LOCKED = "MISSION_LOCKED"
    PLAN_CREATED = "PLAN_CREATED"
    TASKS_CREATED = "TASKS_CREATED"
    TASKS_ASSIGNED = "TASKS_ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED_FOR_REVIEW = "SUBMITTED_FOR_REVIEW"
    REVIEW_REPAIR = "REVIEW_REPAIR"
    REVIEW_PASSED = "REVIEW_PASSED"
    REVIEW_FAILED = "REVIEW_FAILED"
    REPAIRING = "REPAIRING"
    INTEGRATING = "INTEGRATING"
    QA_REVIEW = "QA_REVIEW"
    QA_FAILED = "QA_FAILED"
    QA_PASSED = "QA_PASSED"
    FINAL_PACKAGING = "FINAL_PACKAGING"
    DELIVERED = "DELIVERED"
    RETROSPECTIVE_STORED = "RETROSPECTIVE_STORED"
    KNOWLEDGE_UPDATED = "KNOWLEDGE_UPDATED"


ALLOWED_TRANSITIONS: dict[FlowState, set[FlowState]] = {
    FlowState.GOAL_INGESTED: {FlowState.MISSION_LOCKED},
    FlowState.MISSION_LOCKED: {FlowState.PLAN_CREATED},
    FlowState.PLAN_CREATED: {FlowState.TASKS_CREATED},
    FlowState.TASKS_CREATED: {FlowState.TASKS_ASSIGNED},
    FlowState.TASKS_ASSIGNED: {FlowState.IN_PROGRESS},
    FlowState.IN_PROGRESS: {FlowState.SUBMITTED_FOR_REVIEW},
    FlowState.SUBMITTED_FOR_REVIEW: {
        FlowState.REVIEW_PASSED,
        FlowState.REVIEW_REPAIR,
        FlowState.REVIEW_FAILED,
    },
    FlowState.REVIEW_REPAIR: {FlowState.REPAIRING},
    FlowState.REPAIRING: {FlowState.IN_PROGRESS},
    FlowState.REVIEW_FAILED: {FlowState.PLAN_CREATED},
    FlowState.REVIEW_PASSED: {FlowState.INTEGRATING},
    FlowState.INTEGRATING: {FlowState.QA_REVIEW},
    FlowState.QA_REVIEW: {FlowState.QA_PASSED, FlowState.QA_FAILED},
    FlowState.QA_FAILED: {FlowState.IN_PROGRESS},
    FlowState.QA_PASSED: {FlowState.FINAL_PACKAGING},
    FlowState.FINAL_PACKAGING: {FlowState.DELIVERED},
    FlowState.DELIVERED: {FlowState.RETROSPECTIVE_STORED},
    FlowState.RETROSPECTIVE_STORED: {FlowState.KNOWLEDGE_UPDATED},
    FlowState.KNOWLEDGE_UPDATED: set(),
}


def assert_transition(current: FlowState, nxt: FlowState) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if nxt not in allowed:
        raise ValueError(f"Invalid transition: {current} -> {nxt}")
