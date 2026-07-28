"""Material evidence conflict grouping."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .models import EvidenceRecord


@dataclass(frozen=True)
class EvidenceConflict:
    topic: str
    claims: tuple[str, ...]
    record_ids: tuple[str, ...]


def claim_topic(claim: str) -> str:
    lowered = claim.lower()
    for topic in ("license", "version", "install", "security", "support"):
        if topic in lowered:
            return topic
    words = re.findall(r"[a-z0-9]+", lowered)
    return " ".join(words[:2]) or "claim"


def find_conflicts(
    records: list[EvidenceRecord],
    candidate_id: str,
) -> tuple[EvidenceConflict, ...]:
    grouped: dict[str, list[EvidenceRecord]] = {}
    for record in records:
        if record.candidate_id == candidate_id and record.material:
            grouped.setdefault(claim_topic(record.claim), []).append(record)
    return tuple(
        _to_conflict(topic, topic_records)
        for topic, topic_records in grouped.items()
        if _has_conflict(topic_records)
    )


def _has_conflict(records: list[EvidenceRecord]) -> bool:
    return len(records) >= 2 and any(
        record.evidence_role == "contradiction"
        or record.status == "contradicted"
        for record in records
    )


def _to_conflict(
    topic: str,
    records: list[EvidenceRecord],
) -> EvidenceConflict:
    return EvidenceConflict(
        topic=topic,
        claims=tuple(record.claim for record in records),
        record_ids=tuple(record.record_id for record in records),
    )
