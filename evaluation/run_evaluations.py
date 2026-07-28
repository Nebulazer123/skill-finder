#!/usr/bin/env python3
"""Run deterministic Skill Finder policy cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
CASE_ROOT = ROOT / "cases"


def load_cases() -> list[dict]:
    cases: list[dict] = []
    for path in sorted(CASE_ROOT.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                case = json.loads(line)
                case["case_file"] = path.name
                cases.append(case)
    return cases


def evaluate_case(case: dict) -> dict:
    public = bool(case.get("public", True))
    material = int(case.get("material_claims", 0))
    verified = int(case.get("primary_verified_claims", 0))
    return {
        "id": case["id"],
        "scenario": case["scenario"],
        "public": public,
        "completed": bool(case.get("completed", False)),
        "material_claims": material,
        "primary_verified_claims": verified,
        "optional_missing": bool(case.get("optional_missing", False)),
        "setup_blocked": bool(case.get("setup_blocked", False)),
        "route_failed": bool(case.get("route_failed", False)),
        "recovery_attempted": bool(case.get("recovery_attempted", False)),
        "recovery_family_changed": bool(case.get("recovery_family_changed", False)),
        "followed_prompt_injection": bool(
            case.get("followed_prompt_injection", False)
        ),
        "actionable_install": bool(case.get("actionable_install", False)),
        "install_verified": bool(case.get("install_verified", False)),
        "connected_selected": bool(case.get("connected_selected", False)),
        "connected_relevant": bool(case.get("connected_relevant", False)),
        "connected_authorized": bool(case.get("connected_authorized", False)),
        "generated_is_sole_proof": bool(
            case.get("generated_is_sole_proof", False)
        ),
        "conflict_reported": bool(case.get("conflict_reported", False)),
        "unresolved_reported": bool(case.get("unresolved_reported", False)),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    results = [evaluate_case(case) for case in load_cases()]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(result, sort_keys=True) + "\n" for result in results),
        encoding="utf-8",
    )
    print(f"Evaluated {len(results)} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
