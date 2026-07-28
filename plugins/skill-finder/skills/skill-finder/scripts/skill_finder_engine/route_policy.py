"""Eligibility checks for public/local and connected routes."""

from __future__ import annotations

from .models import EvaluationRequest
from .route_models import CapabilitySnapshot, RouteDescriptor


def route_can_handle(
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
    if request.data_classification == "private":
        return route.accepts_private or route.executor in {"local", "filesystem"}
    if request.data_classification == "secret":
        return route.accepts_secret or route.executor in {"local", "filesystem"}
    return True
