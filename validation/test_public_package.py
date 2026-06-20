from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

BINARY_SUFFIXES = frozenset((
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".zip", ".tar", ".gz", ".bz2",
    ".pdf", ".bin", ".exe", ".dll", ".so", ".dylib",
))


def _read_text_strict(path: Path) -> str:
    """Read a text file with strict UTF-8 decoding.

    Raises FileNotFoundError with a clear message if the file is missing,
    and UnicodeDecodeError if the file contains invalid UTF-8.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Expected text file not found: {path}")
    return path.read_text(encoding="utf-8")


def _read_reference_files(*paths: Path) -> str:
    """Concatenate multiple reference files with strict decoding.

    Propagates encoding errors instead of silently dropping characters.
    """
    parts = []
    for path in paths:
        parts.append(_read_text_strict(path))
    return "\n".join(parts)


class PublicPackageTests(unittest.TestCase):
    def test_public_repo_files_exist(self):
        required_files = [
            ROOT / "README.md",
            ROOT / "AI_FLUENCY_EVIDENCE.md",
            ROOT / "LICENSE",
            ROOT / "CONTRIBUTING.md",
            ROOT / "CODE_OF_CONDUCT.md",
            ROOT / "SECURITY.md",
            ROOT / ".github" / "repo-meta.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md",
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
            ROOT / "assets" / "skill-finder-logo.png",
            ROOT / "assets" / "skill-finder-logo-512.png",
        ]
        for path in required_files:
            self.assertTrue(
                path.is_file(),
                f"Required file missing: {path.relative_to(ROOT)}",
            )

    def test_skill_files_exist(self):
        skill_root = ROOT / "skills" / "skill-finder"
        required_skill_files = [
            skill_root / "SKILL.md",
            skill_root / "agents" / "openai.yaml",
            skill_root / "references" / "search-and-inspection.md",
            skill_root / "references" / "evaluation-and-improvement.md",
            skill_root / "references" / "dependency-and-capability-readiness.md",
            skill_root / "references" / "install-and-approval.md",
        ]
        for path in required_skill_files:
            self.assertTrue(
                path.is_file(),
                f"Required skill file missing: {path.relative_to(ROOT)}",
            )

    def test_skill_contract_keeps_required_boundaries(self):
        text = _read_text_strict(ROOT / "skills" / "skill-finder" / "SKILL.md")

        self.assertIn("20+ finalists", text)
        self.assertIn("show at most five", text)
        self.assertIn("Source-Route Scorecard", text)
        self.assertIn("Candidate Evidence Table", text)
        self.assertIn("dependency readiness", text.lower())
        self.assertIn("Install command: not verified", text)
        self.assertIn("approval", text.lower())
        self.assertIn("DeepWiki/Ask Devin", text)
        self.assertIn("Context7/API docs", text)
        self.assertIn("staged/downloaded artifacts", text.lower())

    def test_readme_has_public_front_door_sections(self):
        readme = _read_text_strict(ROOT / "README.md")

        for phrase in (
            "assets/skill-finder-logo-512.png",
            "## The Problem",
            "## Features",
            "## Quick Start",
            "## Install",
            "## Dependencies",
            "## Safety Boundary",
            "## Validation",
            "## Evidence",
            "## Contributing",
            "## License",
        ):
            self.assertIn(phrase, readme, f"README.md missing section: {phrase}")

        self.assertIn("does not auto-install anything", readme)
        self.assertIn("npx skills add Nebulazer123/skill-finder --skill skill-finder", readme)
        self.assertIn("skills use Nebulazer123/skill-finder@skill-finder", readme)
        self.assertIn("Agent Skills CLI / skills.sh", readme)
        self.assertIn("GitHub CLI", readme)
        self.assertIn("DeepWiki MCP", readme)
        self.assertIn("Ask Devin", readme)
        self.assertIn("Devin MCP", readme)
        self.assertIn("/mcp", readme)
        self.assertIn("Context7", readme)
        self.assertIn("API and MCP documentation", readme)
        self.assertIn("Hugging Face Hub / `hf` CLI", readme)
        self.assertIn("Browserbase Browse CLI", readme)
        self.assertIn("Composio CLI / MCP", readme)
        self.assertIn("Codex Plugin Eval", readme)
        self.assertIn("codex mcp add context7", readme)
        self.assertIn("private repositories", readme)
        self.assertIn("playbooks", readme)
        self.assertIn("knowledge", readme)
        self.assertIn("schedules", readme)
        self.assertIn("hf auth login", readme)
        self.assertIn("https://hf.co/cli/install.sh", readme)
        self.assertIn("https://hf.co/cli/install.ps1", readme)
        self.assertIn("huggingface.co/join", readme)
        self.assertIn("settings/tokens", readme)
        self.assertIn("MCP-enabled Spaces", readme)
        self.assertIn("hosted Jobs/training", readme)
        self.assertIn("browse skills install", readme)
        self.assertIn("composio.dev/install", readme)
        self.assertIn("explicit approval", readme.lower())
        self.assertIn("credential setup is a readiness step", readme.lower())
        self.assertIn("temporary workspace", readme.lower())
        self.assertIn("staged paths and cleanup status", readme.lower())
        self.assertIn("AI_FLUENCY_EVIDENCE.md", readme)

    def test_hugging_face_route_is_documented(self):
        readme = _read_text_strict(ROOT / "README.md")
        agent_meta = _read_text_strict(
            ROOT / "skills" / "skill-finder" / "agents" / "openai.yaml"
        )
        references = _read_reference_files(
            ROOT / "skills" / "skill-finder" / "references"
            / "search-and-inspection.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "dependency-and-capability-readiness.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "install-and-approval.md",
        )

        for phrase in (
            "models",
            "datasets",
            "papers",
            "Spaces",
            "MCP-enabled Spaces",
            "community eval",
            "ML benchmark",
            "Jobs/training",
            "cost and credential approval",
        ):
            self.assertIn(phrase, readme + references)

        self.assertIn('value: "huggingface"', agent_meta)
        self.assertIn('value: "hf"', agent_meta)
        self.assertIn("HF_TOKEN", references)
        self.assertIn("billing/prepaid credits", references)
        self.assertNotIn("huggingface-" + "cli", readme + references)
        self.assertNotIn("huggingface_hub" + "[cli]", readme + references)

    def test_safe_staging_download_policy_is_documented(self):
        scanned = _read_reference_files(
            ROOT / "README.md",
            ROOT / "skills" / "skill-finder" / "SKILL.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "search-and-inspection.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "dependency-and-capability-readiness.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "evaluation-and-improvement.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "install-and-approval.md",
        ).lower()

        for phrase in (
            "safe staging",
            "temporary/sandbox",
            "staging path",
            "cleanup status",
            "staging is not permission to run setup scripts",
            "candidate setup scripts",
        ):
            self.assertIn(phrase, scanned)

    def test_learning_evidence_is_scannable(self):
        evidence = _read_text_strict(ROOT / "AI_FLUENCY_EVIDENCE.md")

        for phrase in (
            "My Role Versus AI's Role",
            "The 4D Learning Evidence",
            "Score And Evolution",
            "Material Lessons Learned",
            "Public Responsibility Boundary",
            "Maintenance Note",
            "96/100",
            "99/100",
            "98/100",
        ):
            self.assertIn(phrase, evidence)

    def test_free_credentialed_tools_are_not_disqualified(self):
        scanned = _read_reference_files(
            ROOT / "README.md",
            ROOT / "skills" / "skill-finder" / "SKILL.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "dependency-and-capability-readiness.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "evaluation-and-improvement.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "install-and-approval.md",
        ).lower()

        self.assertIn("credential requirement is not a disqualifier", scanned)
        self.assertIn("free credentialed tools stay eligible", scanned)
        self.assertIn("free account/api-key/oauth requirements should not block", scanned)
        self.assertNotIn("credential-" + "free answer", scanned)

    def test_metadata_shape(self):
        meta = _read_text_strict(ROOT / ".github" / "repo-meta.yml")
        description = []
        in_description = False
        topics = []

        for line in meta.splitlines():
            if line.startswith("description:"):
                in_description = True
                continue
            if line.startswith("topics:"):
                in_description = False
                continue
            if line.startswith("homepage:"):
                in_description = False
            if in_description and line.startswith("  "):
                description.append(line.strip())
            stripped = line.strip()
            if stripped.startswith("- "):
                topics.append(stripped[2:])

        desc_text = " ".join(description)
        self.assertGreater(
            len(desc_text), 0,
            "repo-meta.yml: description section is empty",
        )
        self.assertLessEqual(
            len(desc_text), 350,
            f"repo-meta.yml: description too long ({len(desc_text)} chars > 350)",
        )
        self.assertGreaterEqual(
            len(topics), 8,
            f"repo-meta.yml: too few topics ({len(topics)} < 8)",
        )
        self.assertLessEqual(
            len(topics), 20,
            f"repo-meta.yml: too many topics ({len(topics)} > 20)",
        )
        for topic in topics:
            self.assertRegex(
                topic, r"^[a-z0-9][a-z0-9-]*$",
                f"repo-meta.yml: invalid topic format: {topic!r}",
            )

    def test_public_docs_do_not_include_private_workspace_paths(self):
        scanned_parts = []
        unreadable_files = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.suffix == ".pyc":
                continue
            if path.suffix.lower() in BINARY_SUFFIXES:
                continue
            try:
                scanned_parts.append(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError as exc:
                unreadable_files.append((path.relative_to(ROOT), exc))

        if unreadable_files:
            details = "; ".join(
                f"{p}: {e}" for p, e in unreadable_files
            )
            self.fail(
                f"Files contain invalid UTF-8 (possible encoding "
                f"corruption or unexpected binary): {details}"
            )

        scanned = "\n".join(scanned_parts)

        forbidden = (
            "/" + "Users/",
            "corbin" + "floyd",
            "Anthropic " + "Academy",
            "Claude A.I. " + "Fluency",
            "raw " + "evidence",
            "API" + "_KEY=",
            "PASS" + "WORD=",
            "SECRET" + "_KEY=",
            "ACCESS" + "_KEY=",
            "PRIVATE" + "_KEY=",
            "BEGIN RSA PRIVATE" + " KEY",
            "BEGIN EC PRIVATE" + " KEY",
            "Bearer " + "eyJ",
        )
        for phrase in forbidden:
            self.assertNotIn(
                phrase, scanned,
                f"Private/sensitive content leaked into public docs: {phrase!r}",
            )

    def test_gitignore_covers_generated_cache_files(self):
        gitignore = _read_text_strict(ROOT / ".gitignore")
        for pattern in ("__pycache__/", "*.pyc", ".pytest_cache/"):
            self.assertIn(
                pattern, gitignore,
                f".gitignore missing required pattern: {pattern}",
            )

    def test_all_text_files_are_valid_utf8(self):
        """Verify that all text files in the repo are valid UTF-8.

        Catches encoding corruption early instead of silently ignoring
        malformed bytes at test time.
        """
        invalid_files = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.suffix.lower() in BINARY_SUFFIXES:
                continue
            if path.suffix == ".pyc":
                continue
            try:
                path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                invalid_files.append(f"{path.relative_to(ROOT)}: {exc}")

        if invalid_files:
            self.fail(
                "Text files with invalid UTF-8 encoding found:\n"
                + "\n".join(f"  - {f}" for f in invalid_files)
            )

    def test_gitignore_covers_secret_and_credential_files(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in (".env", "*.pem", "*.key", "*.p12", "*.pfx"):
            self.assertIn(pattern, gitignore)


if __name__ == "__main__":
    unittest.main()
