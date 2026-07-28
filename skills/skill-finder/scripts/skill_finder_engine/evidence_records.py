"""Serializable evidence records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from .serialization import parse_datetime, stable_id, utc_iso


EVIDENCE_ROLES = frozenset(
    {"lead", "corroboration", "verification", "contradiction"}
)
EVIDENCE_STRENGTHS = frozenset({"low", "medium", "high"})
EVIDENCE_STATUSES = frozenset(
    {"verified", "unverified", "contradicted", "stale", "unavailable"}
)


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
            self.record_id = stable_id("ev", self._identity_payload())

    def _identity_payload(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "claim": self.claim,
            "source_uri": self.source_uri,
            "route_id": self.route_id,
            "checked_at": utc_iso(self.checked_at),
        }

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["checked_at"] = utc_iso(self.checked_at)
        data["source_updated_at"] = utc_iso(self.source_updated_at)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceRecord":
        values = dict(data)
        values["checked_at"] = parse_datetime(values.get("checked_at"))
        values["source_updated_at"] = parse_datetime(
            values.get("source_updated_at")
        )
        return cls(**values)
