from pathlib import Path
import unittest

from helpers import (
    ROOT,
    SKILL_ROOT,
    REFERENCE_PATHS,
    read_files,
    read_all_references,
    assert_phrases_present,
    assert_phrases_absent,
)


class PublicPackageTests(unittest.TestCase):
    def test_public_repo_files_exist(self):
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertTrue((ROOT / "AI_FLUENCY_EVIDENCE.md").is_file())
        self.assertTrue((ROOT / "LICENSE").is_file())
        self.assertTrue((ROOT / "CONTRIBUTING.md").is_file())
        self.assertTrue((ROOT / "CODE_OF_CONDUCT.md").is_file())
        self.assertTrue((ROOT / "SECURITY.md").is_file())
        self.assertTrue((ROOT / ".github" / "repo-meta.yml").is_file())
        self.assertTrue(
            (ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").is_file()
        )
        self.assertTrue(
            (ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").is_file()
        )
        self.assertTrue((ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").is_file())
        self.assertTrue((ROOT / "assets" / "skill-finder-logo.png").is_file())
        self.assertTrue((ROOT / "assets" / "skill-finder-logo-512.png").is_file())

    def test_skill_files_exist(self):
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertTrue((SKILL_ROOT / "agents" / "openai.yaml").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "search-and-inspection.md").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "evaluation-and-improvement.md").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "dependency-and-capability-readiness.md").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "install-and-approval.md").is_file())

    def test_skill_contract_keeps_required_boundaries(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("20+ finalists", text)
        self.assertIn("show at most five", text)
        self.assertIn("Source-Route Scorecard", text)
        self.assertIn("Candidate Evidence Table", text)
        self.assertIn("dependency readiness", text.lower())
        self.assertIn("Install command: not verified", text)
        self.assertIn("explicit approval", text.lower())
        self.assertIn("do not demote free account", text.lower())
        self.assertIn("staged/downloaded artifacts", text.lower())

    def test_readme_has_public_front_door_sections(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        assert_phrases_present(self, (
            "assets/skill-finder-logo-512.png",
            "## The Problem",
            "## Features",
            "## Quick Start",
            "## Install",
            "## Dependencies",
            "## Safety Boundary",
            "## Validation",
            "## Learning Evidence",
            "## Contributing",
            "## License",
        ), readme)

        assert_phrases_present(self, (
            "does not auto-install anything",
            "npx skills add Nebulazer123/skill-finder --skill skill-finder",
            "skills use Nebulazer123/skill-finder@skill-finder",
            "Agent Skills CLI / skills.sh",
            "GitHub CLI",
            "Context7",
            "Hugging Face Hub / `hf` CLI",
            "Browserbase Browse CLI",
            "Composio CLI / MCP",
            "Codex Plugin Eval",
            "codex mcp add context7",
            "hf auth login",
            "https://hf.co/cli/install.sh",
            "https://hf.co/cli/install.ps1",
            "huggingface.co/join",
            "settings/tokens",
            "MCP-enabled Spaces",
            "hosted Jobs/training",
            "browse skills install",
            "composio.dev/install",
            "AI_FLUENCY_EVIDENCE.md",
        ), readme)

        assert_phrases_present(self, (
            "explicit approval",
            "credential setup is a readiness step",
            "temporary workspace",
            "staged paths and cleanup status",
        ), readme, case_sensitive=False)

    def test_hugging_face_route_is_documented(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agent_meta = (SKILL_ROOT / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        references = read_files(
            REFERENCE_PATHS["search"],
            REFERENCE_PATHS["dependency"],
            REFERENCE_PATHS["install"],
        )

        assert_phrases_present(self, (
            "models",
            "datasets",
            "papers",
            "Spaces",
            "MCP-enabled Spaces",
            "community eval",
            "ML benchmark",
            "Jobs/training",
            "cost and credential approval",
        ), readme + references)

        self.assertIn('value: "huggingface"', agent_meta)
        self.assertIn('value: "hf"', agent_meta)
        self.assertIn("HF_TOKEN", references)
        self.assertIn("billing/prepaid credits", references)
        self.assertNotIn("huggingface-" + "cli", readme + references)
        self.assertNotIn("huggingface_hub" + "[cli]", readme + references)

    def test_safe_staging_download_policy_is_documented(self):
        scanned = read_files(
            ROOT / "README.md",
            SKILL_ROOT / "SKILL.md",
            *REFERENCE_PATHS.values(),
        ).lower()

        assert_phrases_present(self, (
            "safe staging",
            "temporary/sandbox",
            "staging path",
            "cleanup status",
            "staging is not permission to run setup scripts",
            "do not run candidate scripts",
        ), scanned)

    def test_learning_evidence_is_scannable(self):
        evidence = (ROOT / "AI_FLUENCY_EVIDENCE.md").read_text(encoding="utf-8")

        assert_phrases_present(self, (
            "My Role Versus AI's Role",
            "The 4D Learning Evidence",
            "Score And Evolution",
            "Material Lessons Learned",
            "Public Responsibility Boundary",
            "Maintenance Note",
            "96/100",
            "99/100",
            "98/100",
        ), evidence)

    def test_free_credentialed_tools_are_not_disqualified(self):
        scanned = read_files(
            ROOT / "README.md",
            SKILL_ROOT / "SKILL.md",
            REFERENCE_PATHS["dependency"],
            REFERENCE_PATHS["evaluation"],
            REFERENCE_PATHS["install"],
        ).lower()

        assert_phrases_present(self, (
            "credential requirement is not a disqualifier",
            "free credentialed tools stay eligible",
            "free account/api-key/oauth requirements should not block",
        ), scanned)

        self.assertNotIn("credential-" + "free answer", scanned)

    def test_metadata_shape(self):
        meta = (ROOT / ".github" / "repo-meta.yml").read_text(encoding="utf-8")
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

        self.assertLessEqual(len(" ".join(description)), 350)
        self.assertGreaterEqual(len(topics), 8)
        self.assertLessEqual(len(topics), 20)
        for topic in topics:
            self.assertRegex(topic, r"^[a-z0-9][a-z0-9-]*$")

    def test_public_docs_do_not_include_private_workspace_paths(self):
        scanned = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        )

        assert_phrases_absent(self, (
            "/" + "Users/",
            "corbin" + "floyd",
            "Anthropic " + "Academy",
            "Claude A.I. " + "Fluency",
            "raw " + "evidence",
            "API" + "_KEY=",
            "PASS" + "WORD=",
        ), scanned)

    def test_gitignore_covers_generated_cache_files(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("__pycache__/", gitignore)
        self.assertIn("*.pyc", gitignore)
        self.assertIn(".pytest_cache/", gitignore)


if __name__ == "__main__":
    unittest.main()
