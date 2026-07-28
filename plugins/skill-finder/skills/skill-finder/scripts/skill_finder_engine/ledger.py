"""Candidate aliasing, evidence validation, and conflict preservation."""

from __future__ import annotations

from dataclasses import dataclass, field
import re

from .models import EvidenceRecord


PRIMARY_SOURCE_TYPES = frozenset(
    {
        "source_code",
        "official_doc",
        "package_registry",
        "release",
        "test",
        "security_advisory",
    }
)


@dataclass
class Candidate:
    candidate_id: str
    aliases: set[str] = field(default_factory=set)


class CandidateIndex:
    def __init__(self) -> None:
        self.candidates: dict[str, Candidate] = {}
        self._aliases: dict[str, str] = {}

    def add(self, candidate_id: str, aliases: set[str] | None = None) -> Candidate:
        all_ids = {candidate_id, *(aliases or set())}
        canonical = next(
            (self._aliases[value] for value in all_ids if value in self._aliases),
            candidate_id,
        )
        candidate = self.candidates.get(canonical)
        if candidate is None:
            candidate = Candidate(canonical)
            self.candidates[canonical] = candidate
        candidate.aliases.update(all_ids)
        for value in all_ids:
            old_canonical = self._aliases.get(value)
            if old_canonical and old_canonical != canonical:
                old = self.candidates.pop(old_canonical)
                candidate.aliases.update(old.aliases)
            self._aliases[value] = canonical
        for value in candidate.aliases:
            self._aliases[value] = canonical
        return candidate


@dataclass(frozen=True)
class MaterialValidation:
    valid: bool
    unverified_claims: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceConflict:
    topic: str
    claims: tuple[str, ...]
    record_ids: tuple[str, ...]


def _claim_topic(claim: str) -> str:
    lowered = claim.lower()
    for topic in ("license", "version", "install", "security", "support"):
        if topic in lowered:
            return topic
    words = re.findall(r"[a-z0-9]+", lowered)
    return " ".join(words[:2]) or "claim"


class EvidenceLedger:
    def __init__(self, records: list[EvidenceRecord] | None = None) -> None:
        self.records = list(records or [])

    def add(self, record: EvidenceRecord) -> None:
        self.records.append(record)

    def validate_material_claims(self, candidate_id: str) -> MaterialValidation:
        material = [
            record
            for record in self.records
            if record.candidate_id == candidate_id and record.material
        ]
        unverified: list[str] = []
        for record in material:
            matching_proof = any(
                other.candidate_id == candidate_id
                and other.claim == record.claim
                and other.evidence_role == "verification"
                and other.status == "verified"
                and other.source_type in PRIMARY_SOURCE_TYPES
                for other in material
            )
            if not matching_proof:
                unverified.append(record.claim)
        return MaterialValidation(
            valid=bool(material) and not unverified,
            unverified_claims=tuple(dict.fromkeys(unverified)),
        )

    def conflicts(self, candidate_id: str) -> tuple[EvidenceConflict, ...]:
        grouped: dict[str, list[EvidenceRecord]] = {}
        for record in self.records:
            if record.candidate_id != candidate_id or not record.material:
                continue
            grouped.setdefault(_claim_topic(record.claim), []).append(record)
        conflicts: list[EvidenceConflict] = []
        for topic, records in grouped.items():
            if len(records) < 2:
                continue
            has_contradiction = any(
                record.evidence_role == "contradiction"
                or record.status == "contradicted"
                for record in records
            )
            if has_contradiction:
                conflicts.append(
                    EvidenceConflict(
                        topic=topic,
                        claims=tuple(record.claim for record in records),
                        record_ids=tuple(record.record_id for record in records),
                    )
                )
        return tuple(conflicts)
