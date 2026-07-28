"""Behavior tests for the Skill Finder hybrid evidence engine."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENGINE_SCRIPTS = ROOT / "skills" / "skill-finder" / "scripts"
sys.path.insert(0, str(ENGINE_SCRIPTS))


class IdentityTests(unittest.TestCase):
    def test_package_identity_uses_purl_and_normalizes_scoped_npm_name(self):
        from skill_finder_engine.identity import package_identity

        self.assertEqual(
            package_identity("npm", "@upstash/context7-mcp", "3.2.5"),
            "pkg:npm/%40upstash/context7-mcp@3.2.5",
        )

    def test_repository_identity_normalizes_github_url(self):
        from skill_finder_engine.identity import repository_identity

        self.assertEqual(
            repository_identity(
                "https://github.com/ModelContextProtocol/Registry.git",
                "ABC123",
            ),
            "github.com/modelcontextprotocol/registry@abc123",
        )

    def test_mcp_skill_and_connector_identities_are_stable(self):
        from skill_finder_engine.identity import (
            connector_identity,
            mcp_identity,
            skill_identity,
        )

        self.assertEqual(
            mcp_identity("io.github.example/server", "1.2.0"),
            "mcp:io.github.example/server@1.2.0",
        )
        self.assertEqual(
            skill_identity("skills.sh", "owner/repo", "research", "2.0.0"),
            "skill:skills.sh/owner/repo/research@2.0.0",
        )
        self.assertEqual(
            connector_identity("composio", "google-drive"),
            "connector:composio/google-drive",
        )

    def test_identity_rejects_missing_required_parts(self):
        from skill_finder_engine.identity import package_identity

        with self.assertRaisesRegex(ValueError, "package name"):
            package_identity("npm", "", "1.0.0")


class ModelTests(unittest.TestCase):
    def test_evidence_record_round_trips_deterministically(self):
        from skill_finder_engine.models import EvidenceRecord

        checked_at = datetime(2026, 7, 28, 5, 0, tzinfo=timezone.utc)
        record = EvidenceRecord(
            candidate_id="pkg:npm/browse@0.9.5",
            claim="browse 0.9.5 is the current package version",
            material=True,
            source_uri="https://api.deps.dev/v3/systems/npm/packages/browse",
            source_type="package_registry",
            evidence_role="verification",
            route_id="deps-dev",
            source_family="package_registry",
            checked_at=checked_at,
            strength="high",
            status="verified",
        )

        encoded = record.to_dict()
        self.assertEqual(encoded["checked_at"], "2026-07-28T05:00:00Z")
        self.assertTrue(encoded["record_id"].startswith("ev_"))
        self.assertEqual(EvidenceRecord.from_dict(encoded).to_dict(), encoded)
        self.assertEqual(
            json.dumps(encoded, sort_keys=True),
            json.dumps(record.to_dict(), sort_keys=True),
        )

    def test_route_attempt_records_recovery(self):
        from skill_finder_engine.models import RouteAttempt

        attempt = RouteAttempt(
            route_id="deepwiki",
            lane="public",
            executor="host_tool",
            status="failed",
            failure_category="timeout",
            recovery_route_id="github-source",
        )

        encoded = attempt.to_dict()
        self.assertEqual(encoded["status"], "failed")
        self.assertEqual(encoded["recovery_route_id"], "github-source")

    def test_invalid_model_enums_are_rejected(self):
        from skill_finder_engine.models import EvidenceRecord

        with self.assertRaisesRegex(ValueError, "evidence_role"):
            EvidenceRecord(
                candidate_id="pkg:npm/browse@0.9.5",
                claim="claim",
                material=True,
                source_uri="https://example.com",
                source_type="official_doc",
                evidence_role="guess",
                route_id="docs",
                source_family="official_docs",
                strength="high",
                status="verified",
            )


if __name__ == "__main__":
    unittest.main()
