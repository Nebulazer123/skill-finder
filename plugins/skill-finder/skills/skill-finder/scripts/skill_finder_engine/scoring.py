"""Weighted candidate fit and evidence confidence scoring."""

from __future__ import annotations

from dataclasses import dataclass


WEIGHTS = {
    "task_fit": 30,
    "capability_completeness": 15,
    "tests_verification": 15,
    "freshness": 10,
    "trust_supply_chain": 10,
    "host_installability": 10,
    "privacy_cost": 5,
    "adoption_adjacent": 5,
}


@dataclass(frozen=True)
class CandidateScore:
    task_fit: float
    capability_completeness: float
    tests_verification: float
    freshness: float
    trust_supply_chain: float
    host_installability: float
    privacy_cost: float
    adoption_adjacent: float

    def __post_init__(self) -> None:
        for value in self.__dict__.values():
            if value < 0 or value > 1:
                raise ValueError("criterion values must be between 0 and 1")

    @classmethod
    def full(cls) -> "CandidateScore":
        return cls(**{key: 1.0 for key in WEIGHTS})


@dataclass(frozen=True)
class ScoreResult:
    fit_score: float
    evidence_coverage: float
    confidence: float


def score_candidate(
    score: CandidateScore,
    *,
    supported_weight: float,
    primary_verified: bool,
    source_family_count: int,
    unresolved_material_conflict: bool,
) -> ScoreResult:
    fit = round(
        sum(getattr(score, key) * weight for key, weight in WEIGHTS.items()),
        1,
    )
    coverage = round(max(0.0, min(100.0, supported_weight)), 1)
    confidence = fit * 0.45 + coverage * 0.35
    if primary_verified:
        confidence += 10
    confidence += min(source_family_count, 3) * 2.5
    if unresolved_material_conflict:
        confidence = min(confidence, 55.0)
    if not primary_verified:
        confidence = min(confidence, 49.0)
    return ScoreResult(
        fit_score=fit,
        evidence_coverage=coverage,
        confidence=round(max(0.0, min(100.0, confidence)), 1),
    )
