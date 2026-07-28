"""Deterministic datetime and identifier serialization helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from typing import Any


def utc_iso(value: datetime | None) -> str:
    if value is None:
        return ""
    normalized = value.astimezone(timezone.utc)
    return normalized.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_datetime(value: str | datetime | None) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def stable_id(prefix: str, payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(encoded).hexdigest()[:16]}"
