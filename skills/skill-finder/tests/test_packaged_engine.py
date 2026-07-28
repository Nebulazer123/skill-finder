"""Smoke tests that ship with the evidence engine package."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from skill_finder_engine.identity import package_identity  # noqa: E402
from skill_finder_engine.models import EvaluationRequest  # noqa: E402
from skill_finder_engine.planner import (  # noqa: E402
    CapabilitySnapshot,
    RouteDescriptor,
    plan_routes,
)


class PackagedEngineSmokeTests(unittest.TestCase):
    def test_package_identity_is_stable(self):
        self.assertEqual(
            package_identity("npm", "browse", "0.9.5"),
            "pkg:npm/browse@0.9.5",
        )

    def test_public_route_can_meet_quick_floor(self):
        request = EvaluationRequest(
            goal="Find a package",
            depth="quick",
            target_host="codex",
            data_classification="public",
        )
        route = RouteDescriptor(
            route_id="local-source",
            lane="public",
            family="source",
            executor="local",
            evidence_types=("discovery", "verification"),
        )
        plan = plan_routes(
            request,
            [route],
            CapabilitySnapshot(available_routes={"local-source"}),
        )
        self.assertTrue(plan.meets_route_floor)


if __name__ == "__main__":
    unittest.main()
