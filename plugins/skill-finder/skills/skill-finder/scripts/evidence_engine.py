#!/usr/bin/env python3
"""Inspect capabilities, plan routes, and write Skill Finder run bundles."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

from skill_finder_engine import ENGINE_VERSION, SCHEMA_VERSION
from skill_finder_engine.models import EvaluationRequest
from skill_finder_engine.planner import (
    CapabilitySnapshot,
    RouteDescriptor,
    plan_routes,
)
from skill_finder_engine.reporting import RecommendationReport, write_run_bundle


SKILL_ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = SKILL_ROOT / "config" / "routes.json"
LOCAL_ESSENTIALS = ("python3", "git", "rg")


def load_routes() -> list[RouteDescriptor]:
    payload = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    return [
        RouteDescriptor(
            route_id=item["route_id"],
            lane=item["lane"],
            family=item["family"],
            executor=item["executor"],
            evidence_types=tuple(item["evidence_types"]),
            requires_account=bool(item.get("requires_account", False)),
            accepts_private=bool(item.get("accepts_private", False)),
            accepts_secret=bool(item.get("accepts_secret", False)),
            cost_class=item.get("cost_class", "free"),
            priority=int(item.get("priority", 100)),
        )
        for item in payload["routes"]
    ]


def doctor() -> dict:
    found = {name: shutil.which(name) or "" for name in LOCAL_ESSENTIALS}
    return {
        "engine_version": ENGINE_VERSION,
        "local_essentials": found,
        "required_missing": [name for name, path in found.items() if not path],
        "connected_routes": "conditional",
    }


def run_plan(args: argparse.Namespace) -> dict:
    request = EvaluationRequest(
        goal=args.goal,
        depth=args.depth,
        target_host=args.host,
        data_classification=args.data_classification,
        required_route_families=tuple(args.require_family or []),
        excluded_route_families=tuple(args.exclude_family or []),
        local_only=args.local_only,
    )
    available = {item for item in args.available.split(",") if item}
    authorized = {item for item in args.authorized.split(",") if item}
    plan = plan_routes(
        request,
        load_routes(),
        CapabilitySnapshot(available_routes=available, authorized_routes=authorized),
    )
    return {
        "selected_route_ids": list(plan.selected_route_ids),
        "meets_route_floor": plan.meets_route_floor,
        "setup_blocks": plan.setup_blocks,
        "unresolved_requirements": list(plan.unresolved_requirements),
    }


def run_render(args: argparse.Namespace) -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    report = RecommendationReport(
        recommendation=args.recommendation,
        install_command=args.install_command,
        install_command_verified=args.install_verified,
        confidence_rationale=args.confidence_rationale,
        near_miss=args.near_miss,
        unresolved_lines=tuple(args.unresolved or []),
    ).render()
    task_digest = hashlib.sha256(args.recommendation.encode("utf-8")).hexdigest()
    write_run_bundle(
        Path(args.output),
        run={
            "engine_version": ENGINE_VERSION,
            "schema_version": SCHEMA_VERSION,
            "task_digest": task_digest,
            "selected_routes": [],
            "checked_at": now.isoformat().replace("+00:00", "Z"),
            "confidence": 0,
        },
        capabilities=doctor(),
        attempts=[],
        records=[],
        candidates=[],
        report=report,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("--goal", required=True)
    plan_parser.add_argument("--depth", choices=("quick", "deep"), default="quick")
    plan_parser.add_argument("--host", default="codex")
    plan_parser.add_argument(
        "--data-classification",
        choices=("public", "private", "secret"),
        default="public",
    )
    plan_parser.add_argument("--available", default="local-source")
    plan_parser.add_argument("--authorized", default="")
    plan_parser.add_argument("--require-family", action="append")
    plan_parser.add_argument("--exclude-family", action="append")
    plan_parser.add_argument("--local-only", action="store_true")

    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("--output", required=True)
    render_parser.add_argument("--recommendation", required=True)
    render_parser.add_argument("--install-command", default="")
    render_parser.add_argument("--install-verified", action="store_true")
    render_parser.add_argument("--confidence-rationale", default="")
    render_parser.add_argument("--near-miss", default="")
    render_parser.add_argument("--unresolved", action="append")
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        payload = doctor()
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if not payload["required_missing"] else 1
    if args.command == "plan":
        print(json.dumps(run_plan(args), indent=2, sort_keys=True))
        return 0
    if args.command == "render":
        run_render(args)
        print(f"Wrote run bundle to {args.output}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
