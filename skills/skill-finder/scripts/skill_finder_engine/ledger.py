"""Candidate aliasing, evidence validation, and conflict preservation."""

from __future__ import annotations

from dataclasses import dataclass

from .candidates import Candidate, CandidateIndex
from .conflicts import EvidenceConflict, find_conflicts
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


@dataclass(frozen=True)
class MaterialValidation:
    valid: bool
    unverified_claims: tuple[str, ...]


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
        return find_conflicts(self.records, candidate_id)
