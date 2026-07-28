"""Route-attempt and evaluation-request records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from .serialization import utc_iso


ROUTE_STATUSES = frozenset(
    {"worked", "partial", "unavailable", "failed", "cancelled", "skipped"}
)
FAILURE_CATEGORIES = frozenset(
    {
        "",
        "timeout",
        "authentication",
        "not_found",
        "schema_change",
        "weak_evidence",
        "transport",
        "cancelled",
    }
)
EVALUATION_DEPTHS = frozenset({"quick", "deep"})
DATA_CLASSIFICATIONS = frozenset({"public", "private", "secret"})


@dataclass
class RouteAttempt:
    route_id: str
    lane: str
    executor: str
    status: str
    failure_category: str = ""
    recovery_route_id: str = ""
    started_at: datetime | None = None
    ended_at: datetime | None = None
    evidence_record_ids: list[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self) -> None:
        if self.status not in ROUTE_STATUSES:
            raise ValueError(f"invalid route status: {self.status}")
        if self.failure_category not in FAILURE_CATEGORIES:
            raise ValueError(
                f"invalid failure_category: {self.failure_category}"
            )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["started_at"] = utc_iso(self.started_at)
        data["ended_at"] = utc_iso(self.ended_at)
        return data


@dataclass(frozen=True)
class EvaluationRequest:
    goal: str
    depth: str = "quick"
    target_host: str = "codex"
    data_classification: str = "public"
    task_category: str = "capability_discovery"
    local_only: bool = False
    max_cost_usd: float = 0.0
    max_minutes: int = 15
    required_route_families: tuple[str, ...] = ()
    excluded_route_families: tuple[str, ...] = ()
    output_mode: str = "recommendation"

    def __post_init__(self) -> None:
        if not self.goal.strip():
            raise ValueError("goal is required")
        if self.depth not in EVALUATION_DEPTHS:
            raise ValueError(f"invalid depth: {self.depth}")
        if self.data_classification not in DATA_CLASSIFICATIONS:
            raise ValueError(
                f"invalid data_classification: {self.data_classification}"
            )
        if self.max_cost_usd < 0 or self.max_minutes <= 0:
            raise ValueError("cost must be non-negative and time must be positive")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["required_route_families"] = list(self.required_route_families)
        data["excluded_route_families"] = list(self.excluded_route_families)
        return data
