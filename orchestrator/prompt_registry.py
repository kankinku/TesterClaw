from __future__ import annotations

from pathlib import Path


class PromptNotFoundError(FileNotFoundError):
    pass


class PromptRegistry:
    def __init__(self, repo_root: Path) -> None:
        self.prompt_root = repo_root / "agents" / "prompts"

    def get(self, role: str) -> str:
        path = self.prompt_root / f"{role}.md"
        if not path.exists():
            raise PromptNotFoundError(f"missing prompt for role={role}: {path}")
        return path.read_text(encoding="utf-8")
