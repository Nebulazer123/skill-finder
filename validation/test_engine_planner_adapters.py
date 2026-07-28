"""Planner and public-adapter contracts for the hybrid evidence engine."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENGINE_SCRIPTS = ROOT / "skills" / "skill-finder" / "scripts"
sys.path.insert(0, str(ENGINE_SCRIPTS))


class PlannerTests(unittest.TestCase):
    def setUp(self):
        from skill_finder_engine.planner import RouteDescriptor

        self.routes = [
            RouteDescriptor(
                route_id="local-source",
                lane="public",
                family="source",
                executor="local",
                evidence_types=("discovery", "verification"),
            ),
            RouteDescriptor(
                route_id="mcp-registry",
                lane="public",
                family="registry",
                executor="http",
                evidence_types=("discovery", "freshness"),
            ),
            RouteDescriptor(
                route_id="deepwiki",
                lane="public",
                family="generated_map",
                executor="host_tool",
                evidence_types=("discovery",),
            ),
            RouteDescriptor(
                route_id="sourcegraph",
                lane="connected",
                family="code_intelligence",
                executor="host_tool",
                evidence_types=("discovery", "verification"),
                requires_account=True,
                accepts_private=True,
            ),
        ]

    def test_public_plan_does_not_require_connected_routes(self):
        from skill_finder_engine.models import EvaluationRequest
        from skill_finder_engine.planner import CapabilitySnapshot, plan_routes

        request = EvaluationRequest(
            goal="Find an MCP server for package research",
            depth="deep",
            target_host="codex",
            data_classification="public",
        )
        snapshot = CapabilitySnapshot(
            available_routes={"local-source", "mcp-registry", "deepwiki"}
        )
        plan = plan_routes(request, self.routes, snapshot)

        self.assertTrue(plan.meets_route_floor)
        self.assertNotIn("sourcegraph", plan.selected_route_ids)
        self.assertEqual(plan.setup_blocks, [])

    def test_connected_route_is_selected_only_when_authorized_and_relevant(self):
        from skill_finder_engine.models import EvaluationRequest
        from skill_finder_engine.planner import CapabilitySnapshot, plan_routes

        request = EvaluationRequest(
            goal="Inspect a private repository across history",
            depth="deep",
            target_host="codex",
            data_classification="private",
            required_route_families=("code_intelligence",),
        )
        unavailable = plan_routes(
            request,
            self.routes,
            CapabilitySnapshot(available_routes={"local-source"}),
        )
        self.assertFalse(unavailable.meets_route_floor)
        self.assertIn("code_intelligence", unavailable.unresolved_requirements)

        available = plan_routes(
            request,
            self.routes,
            CapabilitySnapshot(
                available_routes={"local-source", "sourcegraph"},
                authorized_routes={"sourcegraph"},
            ),
        )
        self.assertIn("sourcegraph", available.selected_route_ids)

    def test_failure_recovery_uses_a_different_source_family(self):
        from skill_finder_engine.planner import choose_recovery

        recovery = choose_recovery(
            failed_route_id="deepwiki",
            routes=self.routes,
            available_routes={"local-source", "mcp-registry", "deepwiki"},
            attempted_routes={"deepwiki"},
        )
        self.assertIsNotNone(recovery)
        self.assertNotEqual(recovery.family, "generated_map")


class PublicAdapterTests(unittest.TestCase):
    def test_mcp_registry_parses_status_identity_and_cursor(self):
        from skill_finder_engine.adapters.mcp_registry import parse_search_response

        payload = {
            "servers": [
                {
                    "server": {
                        "name": "io.github.example/server",
                        "version": "1.2.0",
                        "repository": {
                            "url": "https://github.com/example/server",
                            "source": "github",
                        },
                        "packages": [
                            {
                                "registryType": "npm",
                                "identifier": "@example/server",
                                "version": "1.2.0",
                            }
                        ],
                    },
                    "_meta": {"io.modelcontextprotocol.registry/official": {"status": "active"}},
                }
            ],
            "metadata": {"nextCursor": "next-page", "count": 1},
            "futureField": {"ignored": True},
        }
        page = parse_search_response(payload)
        self.assertEqual(page.next_cursor, "next-page")
        self.assertEqual(page.items[0].candidate_id, "mcp:io.github.example/server@1.2.0")
        self.assertEqual(page.items[0].status, "active")
        self.assertIn("pkg:npm/%40example/server@1.2.0", page.items[0].aliases)

    def test_deps_dev_marks_source_links_unverified(self):
        from skill_finder_engine.adapters.deps_dev import parse_version_response

        candidate = parse_version_response(
            "npm",
            "browse",
            "0.9.5",
            {
                "versionKey": {"system": "NPM", "name": "browse", "version": "0.9.5"},
                "publishedAt": "2026-07-01T00:00:00Z",
                "licenses": ["MIT"],
                "advisoryKeys": [{"id": "GHSA-test"}],
                "links": [{"label": "SOURCE_REPO", "url": "https://github.com/example/browse"}],
                "slsaProvenances": [{"sourceRepository": "https://github.com/example/browse"}],
                "extra": "ignored",
            },
        )
        self.assertEqual(candidate.candidate_id, "pkg:npm/browse@0.9.5")
        self.assertEqual(candidate.licenses, ("MIT",))
        self.assertEqual(candidate.direct_advisories, ("GHSA-test",))
        self.assertFalse(candidate.source_verified)
        self.assertTrue(candidate.has_provenance)

    def test_osv_builds_purl_and_batch_queries_and_bounds_responses(self):
        from skill_finder_engine.adapters.osv import (
            MAX_RESPONSE_BYTES,
            build_batch_query,
            build_query,
            parse_response_bytes,
        )

        self.assertEqual(
            build_query(purl="pkg:npm/browse@0.9.5"),
            {"package": {"purl": "pkg:npm/browse@0.9.5"}},
        )
        self.assertEqual(
            build_query(commit="abc123"),
            {"commit": "abc123"},
        )
        batch = build_batch_query(
            [{"purl": "pkg:npm/browse@0.9.5"}, {"commit": "abc123"}]
        )
        self.assertEqual(len(batch["queries"]), 2)
        with self.assertRaisesRegex(ValueError, "response size"):
            parse_response_bytes(b"x" * (MAX_RESPONSE_BYTES + 1))
        with self.assertRaises(json.JSONDecodeError):
            parse_response_bytes(b"{")

    def test_osv_scanner_never_emits_fix(self):
        from skill_finder_engine.adapters.osv import scanner_source_command

        command = scanner_source_command("/tmp/candidate")
        self.assertEqual(command[:3], ["osv-scanner", "scan", "source"])
        self.assertNotIn("fix", command)

    def test_host_tool_emits_intent_without_secrets(self):
        from skill_finder_engine.adapters.host_tool import HostToolIntent

        intent = HostToolIntent(
            route_id="deepwiki",
            tool_name="ask_question",
            arguments={"repo": "owner/repo", "question": "Trace the route"},
        )
        encoded = intent.to_dict()
        self.assertEqual(encoded["executor"], "host_tool")
        self.assertNotIn("secret", json.dumps(encoded).lower())


if __name__ == "__main__":
    unittest.main()
