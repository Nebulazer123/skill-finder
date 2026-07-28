"""Task-specific route planning for public and connected evidence lanes."""

from __future__ import annotations

from typing import Iterable

from .models import EvaluationRequest
from .recovery import choose_recovery
from .route_floor import route_floor_met, unresolved_requirements
from .route_models import CapabilitySnapshot, RouteDescriptor, RoutePlan
from .route_policy import route_can_handle
from .route_selection import select_routes


def plan_routes(
    request: EvaluationRequest,
    routes: Iterable[RouteDescriptor],
    snapshot: CapabilitySnapshot,
) -> RoutePlan:
    eligible = sorted(
        (
            route
            for route in routes
            if route_can_handle(route, request, snapshot)
        ),
        key=lambda route: (route.priority, route.lane == "connected", route.route_id),
    )
    selected, covered_types, covered_families = select_routes(eligible, request)
    unresolved = unresolved_requirements(
        request,
        covered_types,
        covered_families,
    )
    return RoutePlan(
        selected_route_ids=tuple(route.route_id for route in selected),
        meets_route_floor=route_floor_met(
            request,
            unresolved,
            covered_families,
        ),
        setup_blocks=[],
        unresolved_requirements=unresolved,
    )
