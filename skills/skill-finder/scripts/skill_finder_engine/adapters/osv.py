"""OSV API v1 query helpers and safe scanner invocation."""

from __future__ import annotations

import json


MAX_RESPONSE_BYTES = 32 * 1024 * 1024
MAX_BATCH_QUERIES = 1000


def build_query(
    *,
    purl: str = "",
    system: str = "",
    name: str = "",
    version: str = "",
    commit: str = "",
) -> dict:
    if commit:
        return {"commit": commit}
    package: dict[str, str] = {}
    if purl:
        package["purl"] = purl
    else:
        if not system or not name:
            raise ValueError("purl or package system and name are required")
        package.update({"ecosystem": system, "name": name})
    query = {"package": package}
    if version:
        query["version"] = version
    return query


def build_batch_query(queries: list[dict[str, str]]) -> dict:
    if not queries or len(queries) > MAX_BATCH_QUERIES:
        raise ValueError("batch must contain 1 to 1000 queries")
    return {"queries": [build_query(**query) for query in queries]}


def parse_response_bytes(data: bytes) -> dict:
    if len(data) > MAX_RESPONSE_BYTES:
        raise ValueError("response size exceeds OSV limit")
    parsed = json.loads(data)
    if not isinstance(parsed, dict):
        raise ValueError("expected a JSON object")
    return parsed


def scanner_source_command(path: str) -> list[str]:
    if not path:
        raise ValueError("source path is required")
    return ["osv-scanner", "scan", "source", "--format", "json", path]
