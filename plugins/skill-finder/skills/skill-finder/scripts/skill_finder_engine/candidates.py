"""Candidate alias normalization and merging."""

from __future__ import annotations

from dataclasses import dataclass, field


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
        candidate = self.candidates.setdefault(canonical, Candidate(canonical))
        candidate.aliases.update(all_ids)
        self._merge_existing_candidates(candidate, canonical, all_ids)
        self._index_aliases(candidate, canonical)
        return candidate

    def _merge_existing_candidates(
        self,
        candidate: Candidate,
        canonical: str,
        aliases: set[str],
    ) -> None:
        for value in aliases:
            previous = self._aliases.get(value)
            if previous and previous != canonical:
                candidate.aliases.update(self.candidates.pop(previous).aliases)

    def _index_aliases(self, candidate: Candidate, canonical: str) -> None:
        for value in candidate.aliases:
            self._aliases[value] = canonical
