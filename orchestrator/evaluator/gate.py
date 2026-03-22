from __future__ import annotations

from dataclasses import dataclass

DEFAULT_AXES = (
    "goal_alignment",
    "factuality",
    "completeness",
    "logic",
    "reproducibility",
    "quality",
)


@dataclass(frozen=True)
class GateThresholds:
    pass_score: int = 40
    repair_min: int = 26
    repair_max: int = 39


@dataclass(frozen=True)
class GateResult:
    verdict: str
    total_score: int
    missing_axes: list[str]


def evaluate_scores(scores: dict[str, int], thresholds: GateThresholds | None = None) -> GateResult:
    t = thresholds or GateThresholds()
    missing = [axis for axis in DEFAULT_AXES if axis not in scores]
    total = sum(int(value) for value in scores.values())

    if total >= t.pass_score and not missing:
        return GateResult(verdict="pass", total_score=total, missing_axes=[])
    if t.repair_min <= total <= t.repair_max:
        return GateResult(verdict="repair", total_score=total, missing_axes=missing)
    return GateResult(verdict="fail", total_score=total, missing_axes=missing)
