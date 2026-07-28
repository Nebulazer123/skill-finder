"""Shared canonical-identity validation."""


def required(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} is required")
    return cleaned
