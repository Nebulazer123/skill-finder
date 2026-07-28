"""Different-family recovery selection for failed material routes."""

from __future__ import annotations

from collections.abc import Iterable

from .route_models import RouteDescriptor


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
