"""Stable public imports for canonical candidate identities."""

from .capability_ids import connector_identity, mcp_identity, skill_identity
from .package_ids import package_identity
from .repository_ids import repository_identity

__all__ = [
    "connector_identity",
    "mcp_identity",
    "package_identity",
    "repository_identity",
    "skill_identity",
]
