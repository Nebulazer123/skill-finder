"""Shared constants and utilities for Skill Finder validation tests."""

from pathlib import Path
from typing import Sequence
import unittest


ROOT = Path(__file__).resolve().parents[1]

SKILL_ROOT = ROOT / "skills" / "skill-finder"

REFERENCE_PATHS = {
    "search": SKILL_ROOT / "references" / "search-and-inspection.md",
    "evaluation": SKILL_ROOT / "references" / "evaluation-and-improvement.md",
    "dependency": SKILL_ROOT / "references" / "dependency-and-capability-readiness.md",
    "install": SKILL_ROOT / "references" / "install-and-approval.md",
}

ALL_REFERENCE_FILES = tuple(REFERENCE_PATHS.values())


def read_files(*paths: Path, encoding: str = "utf-8") -> str:
    """Read and concatenate multiple files into a single string."""
    return "\n".join(
        path.read_text(encoding=encoding, errors="ignore") for path in paths
    )


def read_all_references() -> str:
    """Read and concatenate all skill reference files."""
    return read_files(*ALL_REFERENCE_FILES)


def assert_phrases_present(
    test: unittest.TestCase,
    phrases: Sequence[str],
    text: str,
    *,
    case_sensitive: bool = True,
) -> None:
    """Assert that every phrase in the sequence is found in text."""
    check_text = text if case_sensitive else text.lower()
    for phrase in phrases:
        check_phrase = phrase if case_sensitive else phrase.lower()
        test.assertIn(check_phrase, check_text)


def assert_phrases_absent(
    test: unittest.TestCase,
    phrases: Sequence[str],
    text: str,
) -> None:
    """Assert that none of the phrases appear in text."""
    for phrase in phrases:
        test.assertNotIn(phrase, text)
