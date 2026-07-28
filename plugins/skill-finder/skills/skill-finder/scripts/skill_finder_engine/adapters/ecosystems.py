"""Optional ecosyste.ms enrichment records."""

from __future__ import annotations

from dataclasses import dataclass


ATTRIBUTION = "Data from ecosyste.ms, licensed CC BY-SA 4.0"


@dataclass(frozen=True)
class EcosystemsEnrichment:
    available: bool
    metadata: dict
    attribution: str = ATTRIBUTION


def parse_enrichment(payload: dict | None) -> EcosystemsEnrichment:
    return EcosystemsEnrichment(
        available=payload is not None,
        metadata=payload or {},
    )
