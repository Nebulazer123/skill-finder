"""Decision, validation, and report-bundle tests."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENGINE_SCRIPTS = ROOT / "skills" / "skill-finder" / "scripts"
sys.path.insert(0, str(ENGINE_SCRIPTS))


def evidence(
    candidate_id: str,
    claim: str,
    *,
    material: bool = True,
    role: str = "verification",
    family: str = "official_source",
    status: str = "verified",
):
    from skill_finder_engine.models import EvidenceRecord

    return EvidenceRecord(
        candidate_id=candidate_id,
        claim=claim,
        material=material,
        source_uri=f"https://example.com/{family}/{claim.replace(' ', '-')}",
        source_type="source_code" if family == "source" else "official_doc",
        evidence_role=role,
        route_id=family,
        source_family=family,
        checked_at=datetime(2026, 7, 28, tzinfo=timezone.utc),
        strength="high" if role == "verification" else "medium",
        status=status,
    )


class LedgerTests(unittest.TestCase):
    def test_generated_summary_cannot_be_sole_material_proof(self):
        from skill_finder_engine.ledger import EvidenceLedger

        ledger = EvidenceLedger(
            [
                evidence(
                    "repo:one",
                    "supports tracing",
                    role="lead",
                    family="generated_map",
                )
            ]
        )
        result = ledger.validate_material_claims("repo:one")
        self.assertFalse(result.valid)
        self.assertIn("supports tracing", result.unverified_claims)

    def test_conflicting_material_claims_are_preserved(self):
        from skill_finder_engine.ledger import EvidenceLedger

        ledger = EvidenceLedger(
            [
                evidence("pkg:npm/example@1.0.0", "license is MIT"),
                evidence(
                    "pkg:npm/example@1.0.0",
                    "license is GPL-3.0",
                    role="contradiction",
                    family="registry",
                    status="contradicted",
                ),
            ]
        )
        conflicts = ledger.conflicts("pkg:npm/example@1.0.0")
        self.assertEqual(len(conflicts), 1)
        self.assertIn("license", conflicts[0].topic)

    def test_alias_merging_keeps_one_candidate(self):
        from skill_finder_engine.ledger import CandidateIndex

        index = CandidateIndex()
        first = index.add(
            "pkg:npm/%40example/server@1.0.0",
            aliases={"mcp:io.github.example/server@1.0.0"},
        )
        second = index.add(
            "mcp:io.github.example/server@1.0.0",
            aliases={"github.com/example/server"},
        )
        self.assertEqual(first.candidate_id, second.candidate_id)
        self.assertEqual(len(index.candidates), 1)
        self.assertIn("github.com/example/server", first.aliases)


class ScoringTests(unittest.TestCase):
    def test_fit_coverage_and_confidence_are_separate(self):
        from skill_finder_engine.scoring import CandidateScore, score_candidate

        result = score_candidate(
            CandidateScore(
                task_fit=1.0,
                capability_completeness=0.8,
                tests_verification=0.8,
                freshness=1.0,
                trust_supply_chain=0.5,
                host_installability=1.0,
                privacy_cost=1.0,
                adoption_adjacent=0.6,
            ),
            supported_weight=80,
            primary_verified=True,
            source_family_count=2,
            unresolved_material_conflict=False,
        )
        self.assertEqual(result.fit_score, 87.0)
        self.assertEqual(result.evidence_coverage, 80.0)
        self.assertGreater(result.confidence, 60.0)

    def test_unresolved_conflict_caps_confidence(self):
        from skill_finder_engine.scoring import CandidateScore, score_candidate

        result = score_candidate(
            CandidateScore.full(),
            supported_weight=100,
            primary_verified=True,
            source_family_count=3,
            unresolved_material_conflict=True,
        )
        self.assertLessEqual(result.confidence, 55.0)


class ReportingTests(unittest.TestCase):
    def test_unverified_install_command_is_not_rendered_as_actionable(self):
        from skill_finder_engine.reporting import RecommendationReport

        report = RecommendationReport(
            recommendation="Example",
            install_command="npm install example",
            install_command_verified=False,
        ).render()
        self.assertIn("Install command: not verified", report)
        self.assertNotIn("`npm install example`", report)

    def test_deep_run_writes_complete_bundle(self):
        from skill_finder_engine.reporting import write_run_bundle

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_run_bundle(
                output,
                run={"engine_version": "1.3.0", "schema_version": "1.0"},
                capabilities={"available_routes": ["local-source"]},
                attempts=[{"route_id": "local-source", "status": "worked"}],
                records=[
                    evidence("repo:one", "implements tracing").to_dict()
                ],
                candidates=[{"candidate_id": "repo:one", "fit_score": 90}],
                report="# Recommendation\n\nUse repo one.\n",
            )
            expected = {
                "run.json",
                "capabilities.json",
                "route-attempts.jsonl",
                "evidence.jsonl",
                "candidates.json",
                "report.md",
            }
            self.assertEqual({path.name for path in output.iterdir()}, expected)
            record = json.loads(
                (output / "evidence.jsonl").read_text().splitlines()[0]
            )
            self.assertEqual(record["candidate_id"], "repo:one")


if __name__ == "__main__":
    unittest.main()
