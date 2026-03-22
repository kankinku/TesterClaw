from __future__ import annotations

from time import perf_counter
from typing import Any, Callable

from orchestrator.contracts import ContractViolationError, validate_agent_response
from runtime.openclaw_runtime import OpenClawRuntime
from runtime.parsers.response_parser import ResponseParseError, parse_json_object
from runtime.policies.call_policy import CallPolicy


class AgentExecutionError(RuntimeError):
    pass


CHAIN_BREAK_PATTERNS = (
    "ignore previous",
    "ignore all previous",
    "reveal system prompt",
    "show system prompt",
    "abort",
    "shutdown",
    "stop execution",
)


def _contains_chain_break(value: Any) -> bool:
    if isinstance(value, str):
        lower = value.lower()
        return any(p in lower for p in CHAIN_BREAK_PATTERNS)
    if isinstance(value, list):
        return any(_contains_chain_break(item) for item in value)
    if isinstance(value, dict):
        return any(_contains_chain_break(v) for v in value.values())
    return False


class SecureAgentExecutor:
    """Role output contract + retry guard for external LLM integration."""

    def __init__(
        self,
        runtime: OpenClawRuntime,
        max_retries: int = 2,
        observer: Callable[[str, int, float, str], None] | None = None,
    ) -> None:
        self.runtime = runtime
        self.max_retries = max_retries
        self.observer = observer

    def run(self, role: str, prompt: str, context: dict[str, Any], system_rules: list[str]) -> dict[str, Any]:
        policy = CallPolicy(max_retries=self.max_retries)
        envelope = {
            "system_rules": system_rules,
            "task_prompt": prompt,
            "input_data": context,
            "response_format": "JSON object only",
            "policy": {
                "timeout_sec": policy.timeout_sec,
                "max_retries": policy.max_retries,
                "stop_sequences": policy.stop_sequences,
                "risk_tier": policy.risk_tier,
            },
        }

        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 2):
            t0 = perf_counter()
            status = "ok"
            try:
                response = self.runtime.run_agent(role=role, prompt=prompt, context=envelope)
                payload = parse_json_object(response)
                if _contains_chain_break(payload):
                    raise ContractViolationError(f"potential chain-break pattern detected in {role} output")
                validate_agent_response(role, payload)
                return payload
            except (ResponseParseError, TypeError, ContractViolationError) as err:
                last_error = err
                status = "error"
            finally:
                if self.observer:
                    self.observer(role, attempt, perf_counter() - t0, status)

        raise AgentExecutionError(f"{role} execution failed after retries: {last_error}")
