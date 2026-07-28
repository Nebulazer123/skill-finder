"""Evidence-floor calculation for route plans."""

from .models import EvaluationRequest


def required_evidence_types(request: EvaluationRequest) -> set[str]:
    required = {"discovery", "verification"}
    if request.depth == "deep":
        required.add("freshness")
    return required


def unresolved_requirements(
    request: EvaluationRequest,
    covered_types: set[str],
    covered_families: set[str],
) -> tuple[str, ...]:
    missing = (
        required_evidence_types(request) - covered_types
    ) | (set(request.required_route_families) - covered_families)
    return tuple(sorted(missing))


def route_floor_met(
    request: EvaluationRequest,
    unresolved: tuple[str, ...],
    covered_families: set[str],
) -> bool:
    return not unresolved and (
        request.depth == "quick" or len(covered_families) >= 2
    )
