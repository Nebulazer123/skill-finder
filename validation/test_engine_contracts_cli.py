"""Schema, route configuration, and CLI smoke tests."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "skill-finder"
CLI = SKILL_ROOT / "scripts" / "evidence_engine.py"


class SchemaTests(unittest.TestCase):
    def test_contract_schemas_are_versioned_and_strict_at_top_level(self):
        for name in ("request", "evidence", "run"):
            path = SKILL_ROOT / "schemas" / f"{name}.schema.json"
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema["type"], "object")
            self.assertFalse(schema["additionalProperties"])
            self.assertTrue(schema["required"])

    def test_routes_have_unique_ids_and_both_lanes(self):
        routes = json.loads(
            (SKILL_ROOT / "config" / "routes.json").read_text(encoding="utf-8")
        )["routes"]
        ids = [route["route_id"] for route in routes]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("public", {route["lane"] for route in routes})
        self.assertIn("connected", {route["lane"] for route in routes})
        for route in routes:
            self.assertIn("family", route)
            self.assertIn("evidence_types", route)


class CliTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *arguments],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_doctor_reports_local_essentials_without_requiring_accounts(self):
        result = self.run_cli("doctor", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("python3", payload["local_essentials"])
        self.assertNotIn("sourcegraph", payload["required_missing"])

    def test_plan_emits_public_route_plan(self):
        result = self.run_cli(
            "plan",
            "--goal",
            "Find an MCP server",
            "--depth",
            "deep",
            "--available",
            "local-source,mcp-registry,osv",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["meets_route_floor"])
        self.assertNotIn("sourcegraph", payload["selected_route_ids"])

    def test_render_writes_the_six_file_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(
                "render",
                "--output",
                directory,
                "--recommendation",
                "Use the verified candidate.",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                len(list(Path(directory).iterdir())),
                6,
            )


if __name__ == "__main__":
    unittest.main()
