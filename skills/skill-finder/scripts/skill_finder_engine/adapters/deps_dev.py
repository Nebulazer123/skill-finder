"""deps.dev v3 response parsing."""

from __future__ import annotations

from dataclasses import dataclass

from ..identity import package_identity


@dataclass(frozen=True)
class DepsDevCandidate:
    candidate_id: str
    published_at: str
    licenses: tuple[str, ...]
    direct_advisories: tuple[str, ...]
    source_links: tuple[str, ...]
    source_verified: bool
    has_provenance: bool


def parse_version_response(
    system: str,
    name: str,
    version: str,
    payload: dict,
) -> DepsDevCandidate:
    links = tuple(
        str(link.get("url", ""))
        for link in payload.get("links", [])
        if link.get("url")
    )
    advisories = tuple(
        str(item.get("id", ""))
        for item in payload.get("advisoryKeys", [])
        if item.get("id")
    )
    return DepsDevCandidate(
        candidate_id=package_identity(system, name, version),
        published_at=str(payload.get("publishedAt", "")),
        licenses=tuple(str(item) for item in payload.get("licenses", [])),
        direct_advisories=advisories,
        source_links=links,
        source_verified=False,
        has_provenance=bool(payload.get("slsaProvenances")),
    )
