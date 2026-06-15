from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PublicPackageTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
