"""Repository identity normalization."""

from urllib.parse import urlparse

from .identity_common import required


def repository_identity(repository_url: str, revision: str = "") -> str:
    raw = required(repository_url, "repository URL")
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("repository URL must include a host")
    parts = _repository_parts(parsed.path)
    normalized = f"{host}/{'/'.join(parts).lower()}"
    if revision.strip():
        normalized += f"@{revision.strip().lower()}"
    return normalized


def _repository_parts(path: str) -> list[str]:
    normalized = path.strip("/")
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    parts = [part for part in normalized.split("/") if part]
    if len(parts) < 2:
        raise ValueError("repository URL must include owner and repository")
    return parts
