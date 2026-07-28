"""Structured intents for tools that only the host can invoke."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class HostToolIntent:
    route_id: str
    tool_name: str
    arguments: dict[str, Any]
    executor: str = "host_tool"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
