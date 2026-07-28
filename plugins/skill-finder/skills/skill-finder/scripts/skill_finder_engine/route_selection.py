"""Smallest-diverse-portfolio route selection."""

from collections.abc import Iterable

from .models import EvaluationRequest
from .route_floor import required_evidence_types
from .route_models import RouteDescriptor


def select_routes(
    eligible: Iterable[RouteDescriptor],
    request: EvaluationRequest,
) -> tuple[list[RouteDescriptor], set[str], set[str]]:
    selected: list[RouteDescriptor] = []
    covered_types: set[str] = set()
    covered_families: set[str] = set()
    required_types = required_evidence_types(request)
    required_families = set(request.required_route_families)

    for route in eligible:
        if _adds_value(route, request, covered_types, covered_families):
            selected.append(route)
            covered_types.update(route.evidence_types)
            covered_families.add(route.family)
        if _can_stop(
            request,
            required_types,
            required_families,
            covered_types,
            covered_families,
        ):
            break
    return selected, covered_types, covered_families


def _adds_value(
    route: RouteDescriptor,
    request: EvaluationRequest,
    covered_types: set[str],
    covered_families: set[str],
) -> bool:
    return (
        route.family in request.required_route_families
        or bool(set(route.evidence_types) - covered_types)
        or (request.depth == "deep" and route.family not in covered_families)
    )


def _can_stop(
    request: EvaluationRequest,
    required_types: set[str],
    required_families: set[str],
    covered_types: set[str],
    covered_families: set[str],
) -> bool:
    has_evidence = required_types <= covered_types
    has_families = required_families <= covered_families
    has_diversity = request.depth == "quick" or len(covered_families) >= 2
    return has_evidence and has_families and has_diversity
