"""Canonical candidate identity helpers."""

from __future__ import annotations

import re
from urllib.parse import quote, urlparse


def _required(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} is required")
    return cleaned


def package_identity(system: str, name: str, version: str = "") -> str:
    package_type = _required(system, "package system").lower()
    package_name = _required(name, "package name")
    package_version = version.strip()

    if package_type == "npm" and package_name.startswith("@"):
        scope, separator, leaf = package_name.partition("/")
        if not separator or not leaf:
            raise ValueError("scoped npm package name must include a package")
        encoded_name = f"{quote(scope, safe='')}/{quote(leaf, safe='')}"
    else:
        if package_type == "pypi":
            package_name = re.sub(r"[-_.]+", "-", package_name).lower()
        encoded_name = quote(package_name, safe="/")

    identity = f"pkg:{package_type}/{encoded_name}"
    if package_version:
        identity += f"@{quote(package_version, safe='.+~-')}"
    return identity


def repository_identity(repository_url: str, revision: str = "") -> str:
    raw = _required(repository_url, "repository URL")
    if "://" not in raw:
        raw = f"https://{raw}"
    parsed = urlparse(raw)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("repository URL must include a host")
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    parts = [part for part in path.split("/") if part]
    if len(parts) < 2:
        raise ValueError("repository URL must include owner and repository")
    normalized = f"{host}/{'/'.join(parts).lower()}"
    if revision.strip():
        normalized += f"@{revision.strip().lower()}"
    return normalized


def mcp_identity(server_name: str, version: str = "") -> str:
    identity = f"mcp:{_required(server_name, 'MCP server name')}"
    if version.strip():
        identity += f"@{version.strip()}"
    return identity


def skill_identity(
    provider: str,
    source: str,
    skill_name: str,
    version: str = "",
) -> str:
    identity = (
        f"skill:{_required(provider, 'skill provider').lower()}/"
        f"{_required(source, 'skill source').strip('/')}/"
        f"{_required(skill_name, 'skill name')}"
    )
    if version.strip():
        identity += f"@{version.strip()}"
    return identity


def connector_identity(provider: str, connector_id: str) -> str:
    return (
        f"connector:{_required(provider, 'connector provider').lower()}/"
        f"{_required(connector_id, 'connector ID')}"
    )
