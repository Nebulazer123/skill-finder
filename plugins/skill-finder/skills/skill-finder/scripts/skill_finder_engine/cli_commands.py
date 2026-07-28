"""Evidence-engine command implementations."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

from . import ENGINE_VERSION, SCHEMA_VERSION
from .models import EvaluationRequest
from .planner import CapabilitySnapshot, RouteDescriptor, plan_routes
from .reporting import RecommendationReport, write_run_bundle


SKILL_ROOT = Path(__file__).resolve().parents[2]
ROUTES_PATH = SKILL_ROOT / "config" / "routes.json"
LOCAL_ESSENTIALS = ("python3", "git", "rg")


def load_routes() -> list[RouteDescriptor]:
    payload = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    return [_route_from_dict(item) for item in payload["routes"]]


def _route_from_dict(item: dict) -> RouteDescriptor:
    return RouteDescriptor(
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


def doctor() -> dict:
    found = {name: shutil.which(name) or "" for name in LOCAL_ESSENTIALS}
    return {
        "engine_version": ENGINE_VERSION,
        "local_essentials": found,
        "required_missing": [name for name, path in found.items() if not path],
        "connected_routes": "conditional",
    }


def run_plan(args: argparse.Namespace) -> dict:
    request = _request_from_args(args)
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


def _request_from_args(args: argparse.Namespace) -> EvaluationRequest:
    return EvaluationRequest(
        goal=args.goal,
        depth=args.depth,
        target_host=args.host,
        data_classification=args.data_classification,
        required_route_families=tuple(args.require_family or []),
        excluded_route_families=tuple(args.exclude_family or []),
        local_only=args.local_only,
    )


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
    write_run_bundle(
        Path(args.output),
        run=_run_metadata(args.recommendation, now),
        capabilities=doctor(),
        attempts=[],
        records=[],
        candidates=[],
        report=report,
    )


def _run_metadata(recommendation: str, checked_at: datetime) -> dict:
    return {
        "engine_version": ENGINE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "task_digest": hashlib.sha256(recommendation.encode("utf-8")).hexdigest(),
        "selected_routes": [],
        "checked_at": checked_at.isoformat().replace("+00:00", "Z"),
        "confidence": 0,
    }
