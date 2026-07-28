"""Stable Markdown rendering and reproducible run bundles."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _jsonl_text(values: list[dict]) -> str:
    return "".join(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
        for value in values
    )


@dataclass(frozen=True)
class RecommendationReport:
    recommendation: str
    install_command: str = ""
    install_command_verified: bool = False
    confidence_rationale: str = ""
    near_miss: str = ""
    unresolved_lines: tuple[str, ...] = ()

    def render(self) -> str:
        lines = [
            "# Recommendation",
            "",
            self.recommendation,
            "",
            "## Setup Readiness",
            "",
        ]
        if self.install_command and self.install_command_verified:
            lines.extend(["Verified install command:", "", f"`{self.install_command}`"])
        else:
            lines.append("Install command: not verified")
        if self.near_miss:
            lines.extend(["", "## Counter-Review", "", self.near_miss])
        lines.extend(["", "## Unresolved Research", ""])
        if self.unresolved_lines:
            lines.extend(f"- {item}" for item in self.unresolved_lines)
        else:
            lines.append("- None.")
        if self.confidence_rationale:
            lines.extend(
                ["", "## Confidence Rationale", "", self.confidence_rationale]
            )
        return "\n".join(lines).rstrip() + "\n"


def write_run_bundle(
    output_dir: Path,
    *,
    run: dict,
    capabilities: dict,
    attempts: list[dict],
    records: list[dict],
    candidates: list[dict],
    report: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "run.json": _json_text(run),
        "capabilities.json": _json_text(capabilities),
        "route-attempts.jsonl": _jsonl_text(attempts),
        "evidence.jsonl": _jsonl_text(records),
        "candidates.json": _json_text(candidates),
        "report.md": report,
    }
    for name, content in files.items():
        (output_dir / name).write_text(content, encoding="utf-8")
