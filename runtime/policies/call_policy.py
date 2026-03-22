from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CallPolicy:
    timeout_sec: int = 90
    max_retries: int = 2
    stop_sequences: tuple[str, ...] = field(default_factory=lambda: ("\n```", "</END>"))
    risk_tier: str = "normal"
