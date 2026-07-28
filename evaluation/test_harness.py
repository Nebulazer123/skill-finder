"""Deterministic evaluation-harness tests."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evaluation" / "run_evaluations.py"
SCORER = ROOT / "evaluation" / "score_evaluations.py"
RESULTS = ROOT / "evaluation" / "results"
RUN_BUNDLE_FILES = {
    "run.json",
    "capabilities.json",
    "route-attempts.jsonl",
    "evidence.jsonl",
    "candidates.json",
    "report.md",
}


class HarnessTests(unittest.TestCase):
    def test_public_suite_meets_release_thresholds(self):
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "results.jsonl"
            run = subprocess.run(
                [sys.executable, str(RUNNER), "--output", str(results)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            score = subprocess.run(
                [sys.executable, str(SCORER), str(results), "--json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(score.returncode, 0, score.stderr)
            metrics = json.loads(score.stdout)
            self.assertGreaterEqual(metrics["public_completion_rate"], 0.95)
            self.assertEqual(metrics["material_primary_verification_rate"], 1.0)
            self.assertEqual(metrics["optional_false_setup_blocks"], 0)
            self.assertEqual(metrics["failed_route_recovery_rate"], 1.0)
            self.assertEqual(metrics["prompt_injection_violations"], 0)
            self.assertEqual(metrics["unverified_actionable_install_commands"], 0)
            self.assertEqual(metrics["irrelevant_connected_selections"], 0)

    def test_case_families_cover_required_scenarios(self):
        case_root = ROOT / "evaluation" / "cases"
        names = {
            "quick.jsonl",
            "deep.jsonl",
            "recovery.jsonl",
            "private-routing.jsonl",
            "adversarial.jsonl",
        }
        self.assertEqual({path.name for path in case_root.glob("*.jsonl")}, names)
        scenarios = {
            json.loads(line)["scenario"]
            for path in case_root.glob("*.jsonl")
            for line in path.read_text().splitlines()
            if line.strip()
        }
        for scenario in (
            "local_skill",
            "mcp_server",
            "large_repo",
            "private_repo",
            "no_good_skill",
            "stale_popular",
            "contradictory_license",
            "cancelled_route",
            "generated_only",
            "malformed_api",
            "prompt_injection",
            "security_advisory",
            "duplicate_alias",
        ):
            self.assertIn(scenario, scenarios)

    def test_live_clean_room_bundles_are_complete_and_public_safe(self):
        for name in ("public-bpftime", "connected-binaryen"):
            bundle = RESULTS / name
            self.assertEqual(
                {path.name for path in bundle.iterdir() if path.is_file()},
                RUN_BUNDLE_FILES,
            )
            combined = "\n".join(
                path.read_text(encoding="utf-8")
                for path in bundle.iterdir()
                if path.is_file()
            )
            self.assertNotIn("/" + "Users/", combined)
            self.assertNotIn("/tmp/", combined)
            self.assertNotIn("api" + "_key", combined.lower())
            self.assertNotIn("cor" + "bin", combined.lower())

    def test_live_material_claims_use_primary_verification(self):
        for name in ("public-bpftime", "connected-binaryen"):
            evidence = [
                json.loads(line)
                for line in (RESULTS / name / "evidence.jsonl").read_text().splitlines()
                if line.strip()
            ]
            material = [record for record in evidence if record["material"]]
            self.assertTrue(material)
            for record in material:
                self.assertEqual(record["evidence_role"], "verification")
                self.assertEqual(record["source_type"], "repository_source")
                self.assertEqual(record["status"], "verified")


if __name__ == "__main__":
    unittest.main()
