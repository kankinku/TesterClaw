from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.runtime_dir = root / "runtime"
        self.runtime_dir.mkdir(exist_ok=True)
        self.db_path = self.runtime_dir / "state.db"
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS state_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    payload TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    attempt INTEGER NOT NULL,
                    latency_sec REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def append_state_event(self, project_id: str, state: str, payload: dict[str, Any]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO state_events (project_id, state, payload) VALUES (?, ?, ?)",
                (project_id, state, json.dumps(payload, ensure_ascii=False)),
            )

    def record_agent_run(self, role: str, attempt: int, latency_sec: float, status: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO agent_runs (role, attempt, latency_sec, status) VALUES (?, ?, ?, ?)",
                (role, attempt, latency_sec, status),
            )

    def write_json(self, relative_path: str, data: dict[str, Any]) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def read_json(self, relative_path: str) -> dict[str, Any] | None:
        path = self.root / relative_path
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _recent_json(self, relative_dir: str, limit: int) -> list[dict[str, Any]]:
        base = self.root / relative_dir
        if not base.exists():
            return []
        files = [p for p in base.glob("*.json") if p.is_file()]
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        output: list[dict[str, Any]] = []
        for path in files[:limit]:
            output.append(json.loads(path.read_text(encoding="utf-8")))
        return output

    def get_execution_context(self, project_id: str, task_id: str | None = None) -> dict[str, Any]:
        """Retrieval layer for agent invocation context.

        Priority:
          1) policy rules
          2) active task
          3) recent decisions
          4) knowledge summaries
          5) recent failures
        """
        active_task = self.read_json(f"memory/tasks/active/{task_id}.json") if task_id else None
        return {
            "project_id": project_id,
            "policy_rules": self._load_policy_rules(),
            "active_task": active_task,
            "recent_decisions": self._recent_json("memory/decisions", limit=3),
            "knowledge_summaries": self._recent_json("memory/knowledge/summaries", limit=3),
            "recent_failures": self._recent_json("memory/failures", limit=5),
        }

    def _load_policy_rules(self) -> list[str]:
        policy_path = self.root / "docs" / "CONSTITUTION.md"
        if not policy_path.exists():
            return []
        rules: list[str] = []
        for line in policy_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and stripped[0].isdigit() and "." in stripped:
                rules.append(stripped)
        return rules
