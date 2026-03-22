from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator.harness import AgentHarness
from orchestrator.models import GoalSpec
from runtime.openclaw_runtime import MockRuntime


def _load_goal_from_file(path: Path) -> GoalSpec:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return GoalSpec(**raw)


def _demo_goal() -> GoalSpec:
    return GoalSpec(
        project_id="demo-project",
        mission="Create PRD draft for autonomous OpenClaw Stage-1 MVP",
        deliverables=["PRD 문서"],
        constraints=["문서는 한국어 중심"],
        success_criteria=["critic gate pass", "qa pass"],
        references=["docs/MISSION.md", "docs/CONSTITUTION.md"],
        budget_limits={"time_hours": 2},
        stop_conditions=["3회 fail"],
        priority_order=["goal_alignment", "quality", "speed"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Autonomous OpenClaw harness demo")
    parser.add_argument("--goal", type=Path, help="Path to GoalSpec JSON")
    parser.add_argument("--demo", action="store_true", help="Run built-in demo goal")
    args = parser.parse_args()

    if not args.goal and not args.demo:
        parser.error("Use --demo or provide --goal <file.json>")

    goal = _demo_goal() if args.demo else _load_goal_from_file(args.goal)
    repo_root = Path(__file__).resolve().parent.parent
    harness = AgentHarness(repo_root=repo_root, runtime=MockRuntime())
    result = harness.run_stage1_prd_loop(goal)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
