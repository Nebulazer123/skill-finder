"""Data contracts shared by route planning and recovery."""

from __future__ import annotations

from dataclasses import dataclass, field


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
