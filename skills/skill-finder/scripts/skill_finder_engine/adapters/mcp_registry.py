"""MCP Registry v0.1 response parsing."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode

from ..identity import mcp_identity, package_identity, repository_identity


BASE_URL = "https://registry.modelcontextprotocol.io/v0.1/servers"


@dataclass(frozen=True)
class RegistryCandidate:
    candidate_id: str
    name: str
    version: str
    status: str
    aliases: tuple[str, ...]
    repository_id: str = ""


@dataclass(frozen=True)
class RegistryPage:
    items: tuple[RegistryCandidate, ...]
    next_cursor: str = ""


def search_url(query: str, cursor: str = "", limit: int = 30) -> str:
    parameters = {"search": query, "limit": max(1, min(limit, 100))}
    if cursor:
        parameters["cursor"] = cursor
    return f"{BASE_URL}?{urlencode(parameters)}"


def parse_search_response(payload: dict) -> RegistryPage:
    items: list[RegistryCandidate] = []
    for wrapped in payload.get("servers", []):
        server = wrapped.get("server", wrapped)
        name = str(server.get("name", "")).strip()
        version = str(server.get("version", "")).strip()
        if not name:
            continue
        official = wrapped.get("_meta", {}).get(
            "io.modelcontextprotocol.registry/official", {}
        )
        status = str(official.get("status", server.get("status", "active")))
        aliases: list[str] = []
        for package in server.get("packages", []):
            system = str(package.get("registryType", "")).lower()
            identifier = str(package.get("identifier", ""))
            package_version = str(package.get("version", version))
            if system and identifier:
                aliases.append(
                    package_identity(system, identifier, package_version)
                )
        repository_id = ""
        repository_url = server.get("repository", {}).get("url", "")
        if repository_url:
            repository_id = repository_identity(repository_url)
            aliases.append(repository_id)
        items.append(
            RegistryCandidate(
                candidate_id=mcp_identity(name, version),
                name=name,
                version=version,
                status=status,
                aliases=tuple(dict.fromkeys(aliases)),
                repository_id=repository_id,
            )
        )
    metadata = payload.get("metadata", {})
    return RegistryPage(
        items=tuple(items),
        next_cursor=str(metadata.get("nextCursor", "")),
    )
