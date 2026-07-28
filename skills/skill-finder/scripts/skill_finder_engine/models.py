"""Serializable evidence-engine records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any


EVIDENCE_ROLES = frozenset(
    {"lead", "corroboration", "verification", "contradiction"}
)
EVIDENCE_STRENGTHS = frozenset({"low", "medium", "high"})
EVIDENCE_STATUSES = frozenset(
    {"verified", "unverified", "contradicted", "stale", "unavailable"}
)
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


def _utc_iso(value: datetime | None) -> str:
    if value is None:
        return ""
    normalized = value.astimezone(timezone.utc)
    return normalized.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_datetime(value: str | datetime | None) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(encoded).hexdigest()[:16]}"


@dataclass
class EvidenceRecord:
    candidate_id: str
    claim: str
    material: bool
    source_uri: str
    source_type: str
    evidence_role: str
    route_id: str
    source_family: str
    strength: str
    status: str
    checked_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    source_updated_at: datetime | None = None
    artifact_digest: str = ""
    accessibility: str = "public"
    account_state: str = "not_required"
    notes: str = ""
    record_id: str = ""

    def __post_init__(self) -> None:
        if self.evidence_role not in EVIDENCE_ROLES:
            raise ValueError(f"invalid evidence_role: {self.evidence_role}")
        if self.strength not in EVIDENCE_STRENGTHS:
            raise ValueError(f"invalid strength: {self.strength}")
        if self.status not in EVIDENCE_STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        if not self.candidate_id or not self.claim or not self.source_uri:
            raise ValueError("candidate_id, claim, and source_uri are required")
        if not self.record_id:
            self.record_id = _stable_id("ev", self._identity_payload())

    def _identity_payload(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "claim": self.claim,
            "source_uri": self.source_uri,
            "route_id": self.route_id,
            "checked_at": _utc_iso(self.checked_at),
        }

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["checked_at"] = _utc_iso(self.checked_at)
        data["source_updated_at"] = _utc_iso(self.source_updated_at)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceRecord":
        values = dict(data)
        values["checked_at"] = _parse_datetime(values.get("checked_at"))
        values["source_updated_at"] = _parse_datetime(
            values.get("source_updated_at")
        )
        return cls(**values)


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
        data["started_at"] = _utc_iso(self.started_at)
        data["ended_at"] = _utc_iso(self.ended_at)
        return data
