"""Bounded standard-library HTTP helpers."""

from __future__ import annotations

import json
from urllib.request import Request, urlopen


DEFAULT_TIMEOUT_SECONDS = 15
DEFAULT_MAX_RESPONSE_BYTES = 4 * 1024 * 1024


def request_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_RESPONSE_BYTES,
) -> dict:
    body = None
    headers = {"Accept": "application/json", "User-Agent": "skill-finder/1.3.0"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(url, data=body, method=method, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("response size exceeds configured limit")
    parsed = json.loads(data)
    if not isinstance(parsed, dict):
        raise ValueError("expected a JSON object")
    return parsed
