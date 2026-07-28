"""Task-specific route planning for public and connected evidence lanes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .models import EvaluationRequest


@dataclass(frozen=True)
class RouteDescriptor:
    route_id: str
    lane: str
    family: str
    executor: str
    evidence_types: tuple[str, ...]
    requires_account: bool = False
    accepts_private: bool = False
    accepts_secret: bool = False
    cost_class: str = "free"
    priority: int = 100


@dataclass(frozen=True)
class CapabilitySnapshot:
    available_routes: set[str] = field(default_factory=set)
    authorized_routes: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class RoutePlan:
    selected_route_ids: tuple[str, ...]
    meets_route_floor: bool
    setup_blocks: list[str]
    unresolved_requirements: tuple[str, ...]


def _route_can_handle(
    route: RouteDescriptor,
    request: EvaluationRequest,
    snapshot: CapabilitySnapshot,
) -> bool:
    if route.route_id not in snapshot.available_routes:
        return False
    if route.family in request.excluded_route_families:
        return False
    if request.local_only and route.executor not in {"local", "filesystem"}:
        return False
    if route.requires_account and route.route_id not in snapshot.authorized_routes:
        return False
    if request.data_classification == "private" and not (
        route.accepts_private or route.executor in {"local", "filesystem"}
    ):
        return False
    if request.data_classification == "secret" and not (
        route.accepts_secret or route.executor in {"local", "filesystem"}
    ):
        return False
    return True


def plan_routes(
    request: EvaluationRequest,
    routes: Iterable[RouteDescriptor],
    snapshot: CapabilitySnapshot,
) -> RoutePlan:
    eligible = sorted(
        (
            route
            for route in routes
            if _route_can_handle(route, request, snapshot)
        ),
        key=lambda route: (route.priority, route.lane == "connected", route.route_id),
    )
    selected: list[RouteDescriptor] = []
    covered_types: set[str] = set()
    covered_families: set[str] = set()
    required_types = {"discovery", "verification"}
    if request.depth == "deep":
        required_types.add("freshness")

    for route in eligible:
        adds_required_family = route.family in request.required_route_families
        adds_evidence = bool(set(route.evidence_types) - covered_types)
        adds_diversity = request.depth == "deep" and route.family not in covered_families
        if adds_required_family or adds_evidence or adds_diversity:
            selected.append(route)
            covered_types.update(route.evidence_types)
            covered_families.add(route.family)
        if (
            required_types <= covered_types
            and set(request.required_route_families) <= covered_families
            and (request.depth == "quick" or len(covered_families) >= 2)
        ):
            break

    unresolved = sorted(
        (required_types - covered_types)
        | (set(request.required_route_families) - covered_families)
    )
    return RoutePlan(
        selected_route_ids=tuple(route.route_id for route in selected),
        meets_route_floor=not unresolved
        and (request.depth == "quick" or len(covered_families) >= 2),
        setup_blocks=[],
        unresolved_requirements=tuple(unresolved),
    )


def choose_recovery(
    failed_route_id: str,
    routes: Iterable[RouteDescriptor],
    available_routes: set[str],
    attempted_routes: set[str],
) -> RouteDescriptor | None:
    route_list = list(routes)
    failed = next(
        (route for route in route_list if route.route_id == failed_route_id),
        None,
    )
    if failed is None:
        return None
    candidates = [
        route
        for route in route_list
        if route.route_id in available_routes
        and route.route_id not in attempted_routes
        and route.family != failed.family
    ]
    return min(candidates, key=lambda route: (route.priority, route.route_id), default=None)
