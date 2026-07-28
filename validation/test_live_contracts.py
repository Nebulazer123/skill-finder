"""Opt-in, read-only live contracts for public evidence services."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT / "skills" / "skill-finder" / "scripts"
sys.path.insert(0, str(ENGINE_ROOT))

from skill_finder_engine.adapters.base import request_json  # noqa: E402
from skill_finder_engine.adapters.deps_dev import parse_version_response  # noqa: E402
from skill_finder_engine.adapters.ecosystems import (  # noqa: E402
    ATTRIBUTION,
    parse_enrichment,
)
from skill_finder_engine.adapters.mcp_registry import (  # noqa: E402
    parse_search_response,
    search_url,
)
from skill_finder_engine.adapters.osv import build_query  # noqa: E402


LIVE = os.environ.get("SKILL_FINDER_LIVE_TESTS") == "1"


@unittest.skipUnless(LIVE, "set SKILL_FINDER_LIVE_TESTS=1 to run live contracts")
class PublicServiceLiveContracts(unittest.TestCase):
    def test_mcp_registry_search_contract(self):
        payload = request_json(search_url("filesystem", limit=5))
        page = parse_search_response(payload)
        self.assertTrue(page.items)
        self.assertTrue(all(item.candidate_id.startswith("mcp:") for item in page.items))

    def test_deps_dev_version_contract(self):
        payload = request_json(
            "https://api.deps.dev/v3/systems/npm/packages/browse/versions/0.9.5"
        )
        candidate = parse_version_response("npm", "browse", "0.9.5", payload)
        self.assertEqual(candidate.candidate_id, "pkg:npm/browse@0.9.5")
        self.assertTrue(candidate.published_at)

    def test_osv_query_contract(self):
        payload = request_json(
            "https://api.osv.dev/v1/query",
            method="POST",
            payload=build_query(purl="pkg:npm/browse@0.9.5"),
        )
        self.assertIsInstance(payload.get("vulns", []), list)

    def test_ecosystems_repository_contract(self):
        repository = quote("modelcontextprotocol/registry", safe="")
        payload = request_json(
            "https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/"
            f"{repository}"
        )
        enrichment = parse_enrichment(payload)
        self.assertTrue(enrichment.available)
        self.assertEqual(enrichment.attribution, ATTRIBUTION)


if __name__ == "__main__":
    unittest.main()
