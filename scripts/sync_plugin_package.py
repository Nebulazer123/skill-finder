#!/usr/bin/env python3
"""Generate and check Skill Finder plugin package files."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.2"
PLUGIN_NAME = "skill-finder"
REPOSITORY_URL = "https://github.com/Nebulazer123/skill-finder"

CANONICAL_SKILL_ROOT = ROOT / "skills" / "skill-finder"
PLUGIN_ROOT = ROOT / "plugins" / PLUGIN_NAME
PLUGIN_SKILL_ROOT = PLUGIN_ROOT / "skills" / PLUGIN_NAME
PLUGIN_ASSET_ROOT = PLUGIN_ROOT / "assets"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
LOGO_SOURCE = ROOT / "assets" / "skill-finder-logo-512.png"


CODEX_PLUGIN_MANIFEST = {
    "name": PLUGIN_NAME,
    "version": VERSION,
    "description": (
        "Find, compare, vet, and prepare agent-usable skills, tools, MCP servers, "
        "workflows, packages, documentation sources, and capability stacks."
    ),
    "author": {
        "name": "Nebulazer123",
        "url": "https://github.com/Nebulazer123",
    },
    "homepage": REPOSITORY_URL,
    "repository": REPOSITORY_URL,
    "license": "MIT",
    "keywords": [
        "agent-skills",
        "capability",
        "capability-discovery",
        "mcp",
        "tooling",
        "research",
        "evaluation",
    ],
    "skills": "./skills/",
    "interface": {
        "displayName": "Skill Finder",
        "shortDescription": "Find and vet agent capabilities",
        "longDescription": (
            "Skill Finder helps an agent search broadly, inspect source evidence, "
            "rank candidates, and recommend the strongest installable capability "
            "for a real task."
        ),
        "developerName": "Nebulazer123",
        "category": "Productivity",
        "capabilities": ["Research", "Developer Tools"],
        "websiteURL": REPOSITORY_URL,
        "defaultPrompt": [
            "Find the best skill for this task.",
            "Compare these connectors/skills for my agent.",
            "No good skill exists; find the best stack.",
        ],
        "brandColor": "#DA7857",
        "logo": "./assets/skill-finder-logo-512.png",
    },
}

CLAUDE_PLUGIN_MANIFEST = {
    "name": PLUGIN_NAME,
    "displayName": "Skill Finder",
    "version": VERSION,
    "description": (
        "Find, compare, vet, and prepare agent-usable skills, tools, MCP servers, "
        "workflows, packages, documentation sources, and capability stacks."
    ),
    "author": {
        "name": "Nebulazer123",
        "url": "https://github.com/Nebulazer123",
    },
    "homepage": REPOSITORY_URL,
    "repository": REPOSITORY_URL,
    "license": "MIT",
    "keywords": [
        "agent-skills",
        "capability",
        "capability-discovery",
        "mcp",
        "tooling",
        "research",
        "evaluation",
    ],
    "skills": "./skills/",
}

CODEX_MARKETPLACE_MANIFEST = {
    "name": PLUGIN_NAME,
    "interface": {
        "displayName": "Skill Finder",
    },
    "plugins": [
        {
            "name": PLUGIN_NAME,
            "source": {
                "source": "local",
                "path": "./plugins/skill-finder",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
    ],
}

CLAUDE_MARKETPLACE_MANIFEST = {
    "name": PLUGIN_NAME,
    "owner": {
        "name": "Nebulazer123",
    },
    "description": "Skill Finder plugin marketplace.",
    "version": VERSION,
    "plugins": [
        {
            "name": PLUGIN_NAME,
            "source": "./plugins/skill-finder",
            "displayName": "Skill Finder",
            "description": CLAUDE_PLUGIN_MANIFEST["description"],
            "version": VERSION,
            "author": CLAUDE_PLUGIN_MANIFEST["author"],
            "homepage": REPOSITORY_URL,
            "repository": REPOSITORY_URL,
            "license": "MIT",
            "category": "Productivity",
            "tags": [
                "agent-skills",
                "capability",
                "capability-discovery",
                "mcp",
                "tooling",
                "research",
            ],
        }
    ],
}


def json_bytes(data: object) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")


def expected_files() -> dict[Path, bytes]:
    files: dict[Path, bytes] = {
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json": json_bytes(CODEX_PLUGIN_MANIFEST),
        PLUGIN_ROOT / ".claude-plugin" / "plugin.json": json_bytes(CLAUDE_PLUGIN_MANIFEST),
        CODEX_MARKETPLACE: json_bytes(CODEX_MARKETPLACE_MANIFEST),
        CLAUDE_MARKETPLACE: json_bytes(CLAUDE_MARKETPLACE_MANIFEST),
    }

    for source_path in sorted(CANONICAL_SKILL_ROOT.rglob("*")):
        if source_path.is_file():
            relative = source_path.relative_to(CANONICAL_SKILL_ROOT)
            files[PLUGIN_SKILL_ROOT / relative] = source_path.read_bytes()

    files[PLUGIN_ASSET_ROOT / "skill-finder-logo-512.png"] = LOGO_SOURCE.read_bytes()
    return files


def managed_existing_files() -> set[Path]:
    files: set[Path] = set()
    if PLUGIN_ROOT.exists():
        files.update(path for path in PLUGIN_ROOT.rglob("*") if path.is_file())
    for marketplace in (CODEX_MARKETPLACE, CLAUDE_MARKETPLACE):
        if marketplace.exists():
            files.add(marketplace)
    return files


def check() -> int:
    expected = expected_files()
    existing = managed_existing_files()
    expected_paths = set(expected)
    problems: list[str] = []

    for path, expected_content in sorted(expected.items()):
        if not path.is_file():
            problems.append(f"missing: {path.relative_to(ROOT)}")
            continue
        actual_content = path.read_bytes()
        if actual_content != expected_content:
            problems.append(f"changed: {path.relative_to(ROOT)}")

    for path in sorted(existing - expected_paths):
        problems.append(f"unexpected: {path.relative_to(ROOT)}")

    if problems:
        print("Plugin package is out of sync.")
        for problem in problems:
            print(f"- {problem}")
        print("Run: python3 scripts/sync_plugin_package.py")
        return 1

    print("Plugin package is in sync.")
    return 0


def sync() -> int:
    expected = expected_files()

    if PLUGIN_ROOT.exists():
        shutil.rmtree(PLUGIN_ROOT)

    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    print("Plugin package synced.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check generated plugin files without writing changes.",
    )
    args = parser.parse_args(argv)
    if args.check:
        return check()
    return sync()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
