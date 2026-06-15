from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


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
        skill_root = ROOT / "skills" / "skill-finder"
        self.assertTrue((skill_root / "SKILL.md").is_file())
        self.assertTrue((skill_root / "agents" / "openai.yaml").is_file())
        self.assertTrue((skill_root / "references" / "search-and-inspection.md").is_file())
        self.assertTrue((skill_root / "references" / "evaluation-and-improvement.md").is_file())
        self.assertTrue((skill_root / "references" / "dependency-and-capability-readiness.md").is_file())
        self.assertTrue((skill_root / "references" / "install-and-approval.md").is_file())

    def test_skill_contract_keeps_required_boundaries(self):
        text = (ROOT / "skills" / "skill-finder" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("20+ finalists", text)
        self.assertIn("show at most five", text)
        self.assertIn("Source-Route Scorecard", text)
        self.assertIn("Candidate Evidence Table", text)
        self.assertIn("dependency readiness", text.lower())
        self.assertIn("Install command: not verified", text)
        self.assertIn("explicit approval", text.lower())
        self.assertIn("do not demote free account", text.lower())

    def test_readme_has_public_front_door_sections(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for phrase in (
            "assets/skill-finder-logo-512.png",
            "## The Problem",
            "## Features",
            "## Quick Start",
            "## Install",
            "## Safety Boundary",
            "## Validation",
            "## Learning Evidence",
            "## Contributing",
            "## License",
        ):
            self.assertIn(phrase, readme)

        self.assertIn("does not auto-install anything", readme)
        self.assertIn("explicit approval", readme.lower())
        self.assertIn("credential setup as a readiness step", readme)
        self.assertIn("AI_FLUENCY_EVIDENCE.md", readme)

    def test_learning_evidence_is_scannable(self):
        evidence = (ROOT / "AI_FLUENCY_EVIDENCE.md").read_text(encoding="utf-8")

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
        scanned = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in (
                ROOT / "README.md",
                ROOT / "skills" / "skill-finder" / "SKILL.md",
                ROOT
                / "skills"
                / "skill-finder"
                / "references"
                / "dependency-and-capability-readiness.md",
                ROOT
                / "skills"
                / "skill-finder"
                / "references"
                / "evaluation-and-improvement.md",
                ROOT
                / "skills"
                / "skill-finder"
                / "references"
                / "install-and-approval.md",
            )
        ).lower()

        self.assertIn("credential requirement is not a disqualifier", scanned)
        self.assertIn("free credentialed tools stay eligible", scanned)
        self.assertIn("free account/api-key/oauth requirements should not block", scanned)
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

        forbidden = (
            "/" + "Users/",
            "corbin" + "floyd",
            "Anthropic " + "Academy",
            "Claude A.I. " + "Fluency",
            "raw " + "evidence",
            "API" + "_KEY=",
            "PASS" + "WORD=",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, scanned)

    def test_gitignore_covers_generated_cache_files(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("__pycache__/", gitignore)
        self.assertIn("*.pyc", gitignore)
        self.assertIn(".pytest_cache/", gitignore)


if __name__ == "__main__":
    unittest.main()
