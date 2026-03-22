from __future__ import annotations

import json
from typing import Any


class ResponseParseError(ValueError):
    pass


def parse_json_object(payload: Any) -> dict:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ResponseParseError(f"invalid json response: {exc}") from exc
        if not isinstance(parsed, dict):
            raise ResponseParseError("json response must be object")
        return parsed
    raise ResponseParseError(f"unsupported response type: {type(payload)!r}")
