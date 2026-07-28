import json
from pathlib import Path
import subprocess
import sys
import unittest

from helpers import read_package_version


ROOT = Path(__file__).resolve().parents[1]

BINARY_SUFFIXES = frozenset((
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".zip", ".tar", ".gz", ".bz2",
    ".pdf", ".bin", ".exe", ".dll", ".so", ".dylib",
))

EXCLUDED_SCAN_PARTS = frozenset((
    ".git",
    "__pycache__",
    "node_modules",
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


def _public_package_paths() -> list[Path]:
    """Return tracked and non-ignored files that Git could publish."""
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [
        ROOT / relative
        for relative in result.stdout.decode("utf-8").split("\0")
        if relative
    ]


class PublicPackageTests(unittest.TestCase):
    def test_public_repo_files_exist(self):
        required_files = [
            ROOT / "README.md",
            ROOT / "HOW_THIS_SKILL_WAS_BUILT.md",
            ROOT / "LICENSE",
            ROOT / "CONTRIBUTING.md",
            ROOT / "CODE_OF_CONDUCT.md",
            ROOT / "SECURITY.md",
            ROOT / "package.json",
            ROOT / ".github" / "repo-meta.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md",
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
            ROOT / "assets" / "skill-finder-logo.png",
            ROOT / "assets" / "skill-finder-logo-512.png",
            ROOT / "assets" / "logos" / "agent-skills.svg",
            ROOT / "assets" / "logos" / "claude-code-color.svg",
            ROOT / "assets" / "logos" / "claude-code-text.svg",
            ROOT / "assets" / "logos" / "codex-text.svg",
            ROOT / "assets" / "logos" / "codex.webp",
            ROOT / "assets" / "logos" / "codex-cloud-color.png",
            ROOT / "assets" / "logos" / "huggingface-color.svg",
            ROOT / "assets" / "logos" / "install-codex-cloud.svg",
            ROOT / "assets" / "logos" / "install-claude-code-button.svg",
            ROOT / "assets" / "logos" / "github-invertocat-white.svg",
            ROOT / "assets" / "logos" / "deepwiki.png",
            ROOT / "assets" / "logos" / "context7.png",
            ROOT / "assets" / "logos" / "browserbase.svg",
            ROOT / "assets" / "logos" / "devin-color.svg",
            ROOT / "assets" / "logos" / "codebase-memory.png",
            ROOT / "assets" / "logos" / "composio-symbol.svg",
            ROOT / "assets" / "logos" / "plugin-eval.svg",
            ROOT / "assets" / "logos" / "mcp-registry.svg",
            ROOT / "assets" / "logos" / "deps-dev.svg",
            ROOT / "assets" / "logos" / "osv.png",
            ROOT / "assets" / "logos" / "ecosystems.ico",
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
            skill_root / "references" / "research-quality-evaluation.md",
            skill_root / "references" / "skills-md-route.md",
            skill_root / "references" / "dependency-and-capability-readiness.md",
            skill_root / "references" / "install-and-approval.md",
        ]
        for path in required_skill_files:
            self.assertTrue(
                path.is_file(),
                f"Required skill file missing: {path.relative_to(ROOT)}",
            )

    def test_plugin_package_files_exist(self):
        required_files = [
            ROOT / "plugins" / "skill-finder" / ".codex-plugin" / "plugin.json",
            ROOT / "plugins" / "skill-finder" / ".claude-plugin" / "plugin.json",
            ROOT / "plugins" / "skill-finder" / "skills" / "skill-finder" / "SKILL.md",
            ROOT / "plugins" / "skill-finder" / "skills" / "skill-finder"
            / "agents" / "openai.yaml",
            ROOT / "plugins" / "skill-finder" / "assets" / "skill-finder-logo-512.png",
            ROOT / ".agents" / "plugins" / "marketplace.json",
            ROOT / ".claude-plugin" / "marketplace.json",
            ROOT / "scripts" / "sync_plugin_package.py",
        ]
        for path in required_files:
            self.assertTrue(
                path.is_file(),
                f"Required plugin package file missing: {path.relative_to(ROOT)}",
            )

    def test_codex_plugin_manifest_shape(self):
        package_version = read_package_version()
        manifest = json.loads(
            _read_text_strict(
                ROOT / "plugins" / "skill-finder" / ".codex-plugin" / "plugin.json"
            )
        )

        self.assertEqual(manifest["name"], "skill-finder")
        self.assertEqual(manifest["version"], package_version)
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["repository"], "https://github.com/Nebulazer123/skill-finder")
        self.assertEqual(manifest["author"]["name"], "Nebulazer123")
        self.assertEqual(manifest["interface"]["displayName"], "Skill Finder")
        self.assertEqual(manifest["interface"]["category"], "Productivity")
        self.assertEqual(manifest["interface"]["logo"], "./assets/skill-finder-logo-512.png")
        self.assertEqual(
            manifest["interface"]["defaultPrompt"],
            [
                "Find the best skill for this task.",
                "Compare these connectors/skills for my agent.",
                "No good skill exists; find the best stack.",
            ],
        )
        self.assertIn("capability", manifest["keywords"])
        self.assertLessEqual(len(manifest["interface"]["defaultPrompt"]), 3)
        for prompt in manifest["interface"]["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)

    def test_claude_plugin_manifest_shape(self):
        package_version = read_package_version()
        manifest = json.loads(
            _read_text_strict(
                ROOT / "plugins" / "skill-finder" / ".claude-plugin" / "plugin.json"
            )
        )

        self.assertEqual(manifest["name"], "skill-finder")
        self.assertEqual(manifest["displayName"], "Skill Finder")
        self.assertEqual(manifest["version"], package_version)
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["repository"], "https://github.com/Nebulazer123/skill-finder")
        self.assertEqual(manifest["author"]["name"], "Nebulazer123")
        self.assertIn("capability", manifest["keywords"])

    def test_plugin_marketplaces_reference_skill_finder(self):
        package_version = read_package_version()
        codex_marketplace = json.loads(
            _read_text_strict(ROOT / ".agents" / "plugins" / "marketplace.json")
        )
        claude_marketplace = json.loads(
            _read_text_strict(ROOT / ".claude-plugin" / "marketplace.json")
        )

        self.assertEqual(codex_marketplace["name"], "skill-finder")
        self.assertEqual(codex_marketplace["interface"]["displayName"], "Skill Finder")
        self.assertEqual(len(codex_marketplace["plugins"]), 1)
        codex_entry = codex_marketplace["plugins"][0]
        self.assertEqual(codex_entry["name"], "skill-finder")
        self.assertEqual(codex_entry["source"]["source"], "local")
        self.assertEqual(codex_entry["source"]["path"], "./plugins/skill-finder")
        self.assertEqual(codex_entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(codex_entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(codex_entry["category"], "Productivity")

        self.assertEqual(claude_marketplace["name"], "skill-finder")
        self.assertEqual(claude_marketplace["owner"]["name"], "Nebulazer123")
        self.assertEqual(len(claude_marketplace["plugins"]), 1)
        claude_entry = claude_marketplace["plugins"][0]
        self.assertEqual(claude_entry["name"], "skill-finder")
        self.assertEqual(claude_entry["source"], "./plugins/skill-finder")
        self.assertEqual(claude_entry["displayName"], "Skill Finder")
        self.assertEqual(claude_entry["version"], package_version)
        self.assertEqual(claude_entry["category"], "Productivity")

    def test_package_json_tracks_npm_setup_dependencies(self):
        manifest = json.loads(_read_text_strict(ROOT / "package.json"))

        self.assertTrue(manifest["private"])
        self.assertEqual(manifest["version"], read_package_version())
        self.assertIn("npm-installable setup tools", manifest["description"])
        self.assertEqual(manifest["engines"]["node"], ">=18")

        dependencies = manifest["dependencies"]
        for package_name in (
            "skills",
            "@upstash/context7-mcp",
            "browse",
            "codebase-memory-mcp",
        ):
            self.assertIn(package_name, dependencies)
        self.assertEqual(dependencies["browse"], "^0.9.5")

        dependabot = _read_text_strict(ROOT / ".github" / "dependabot.yml")
        self.assertIn('package-ecosystem: "npm"', dependabot)

    def test_manifest_version_assertions_use_package_json_source(self):
        source = _read_text_strict(ROOT / "validation" / "test_public_package.py")
        package_version = read_package_version()

        self.assertIn("read_package_version", source)
        self.assertNotIn(
            f'["version"], "{package_version}"',
            source,
            "Manifest version assertions should compare against package.json",
        )

    def test_npm_setup_dependencies_match_public_docs(self):
        manifest = json.loads(_read_text_strict(ROOT / "package.json"))
        dependencies = manifest["dependencies"]

        npm_setup_dependencies = (
            "skills",
            "@upstash/context7-mcp",
            "browse",
            "codebase-memory-mcp",
        )
        public_setup_docs = _read_reference_files(
            ROOT / "README.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "skills" / "skill-finder" / "SKILL.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "dependency-and-capability-readiness.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "install-and-approval.md",
        )

        for package_name in npm_setup_dependencies:
            self.assertIn(package_name, dependencies)
            self.assertIn(
                package_name,
                public_setup_docs,
                f"package.json dependency missing from public setup docs: {package_name}",
            )

        non_npm_capability_routes = ("GitHub MCP", "DeepWiki MCP")
        dependency_names = {name.lower() for name in dependencies}
        for route_name in non_npm_capability_routes:
            self.assertIn(route_name, public_setup_docs)
            self.assertNotIn(
                route_name.lower(),
                dependency_names,
                f"Non-npm capability route should not be a package dependency: {route_name}",
            )

    def test_plugin_package_is_in_sync_with_canonical_skill(self):
        result = subprocess.run(
            [sys.executable, "scripts/sync_plugin_package.py", "--check"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(
            result.returncode,
            0,
            "Plugin package is out of sync:\n" + result.stdout,
        )

    def test_skill_contract_keeps_required_boundaries(self):
        text = _read_text_strict(ROOT / "skills" / "skill-finder" / "SKILL.md")

        self.assertIn("20+ finalists", text)
        self.assertIn("show at most five", text)
        self.assertIn("Source-Route Scorecard", text)
        self.assertIn("Candidate Evidence Table", text)
        self.assertIn("setup/install readiness", text.lower())
        self.assertIn("task-specific evidence floor", text)
        self.assertIn("Install command: not verified", text)
        self.assertIn("approval", text.lower())
        self.assertIn("DeepWiki", text)
        self.assertIn("Context7", text)
        self.assertIn("temporary workspace", text.lower())

    def test_stale_dependency_self_repair_and_issue_reporting_is_documented(self):
        scanned = _read_reference_files(
            ROOT / "skills" / "skill-finder" / "SKILL.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "dependency-and-capability-readiness.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "install-and-approval.md",
        )

        for phrase in (
            "repair or update that route first",
            "Nebulazer123/skill-finder",
            "gh issue create",
            "issue draft",
            "If the failure is unrelated to Skill Finder",
        ):
            self.assertIn(phrase, scanned)

    def test_deep_evaluation_research_quality_contract_is_documented(self):
        scanned = _read_reference_files(
            ROOT / "skills" / "skill-finder" / "SKILL.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "evaluation-and-improvement.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "research-quality-evaluation.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "search-and-inspection.md",
        )

        for phrase in (
            "Quick Evaluation",
            "Deep Evaluation",
            "Evidence Ledger",
            "source type",
            "accessibility",
            "date checked",
            "lead evidence",
            "verification evidence",
            "DeepWiki and Devin",
            "Counter-Review",
            "Recovery Log",
            "Unresolved Research Lines",
            "confidence rationale",
        ):
            self.assertIn(phrase.lower(), scanned.lower())

    def test_skills_md_remote_route_is_documented(self):
        scanned = _read_reference_files(
            ROOT / "README.md",
            ROOT / "skills" / "skill-finder" / "SKILL.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "skills-md-route.md",
            ROOT / "skills" / "skill-finder" / "references"
            / "dependency-and-capability-readiness.md",
            ROOT / "skills" / "skill-finder" / "agents" / "openai.yaml",
        ).lower()

        for phrase in (
            "skills.md",
            "@hasna/skills",
            "skills setup agents",
            "skills list --json",
            "skills quote",
            "premium",
            "approval",
            "skills.sh",
        ):
            self.assertIn(phrase.lower(), scanned)

        self.assertIn("do not confuse", scanned)
        self.assertNotIn("skills mcp connect", scanned)

    def test_readme_has_public_front_door_sections(self):
        readme = _read_text_strict(ROOT / "README.md")

        for phrase in (
            "assets/skill-finder-logo-512.png",
            "assets/logos/claude-code-color.svg",
            "assets/logos/agent-skills.svg",
            "assets/logos/huggingface-color.svg",
            "assets/logos/codex-cloud-color.png",
            "assets/logos/install-codex-cloud.svg",
            "assets/logos/install-claude-code-button.svg",
            "assets/logos/github-invertocat-white.svg",
            "assets/logos/deepwiki.png",
            "assets/logos/context7.png",
            "assets/logos/browserbase.svg",
            "assets/logos/devin-color.svg",
            "assets/logos/codebase-memory.png",
            "assets/logos/composio-symbol.svg",
            "assets/logos/plugin-eval.svg",
            "assets/logos/mcp-registry.svg",
            "assets/logos/deps-dev.svg",
            "assets/logos/osv.png",
            "assets/logos/ecosystems.ico",
            "## The Problem",
            "## What It Does",
            "## Quick Start",
            "## Install",
            "## Setup Requirements",
            "## Recommended When Useful",
            "## How It Works",
            "## Safety Model",
            "## Validation",
            "## Files To Read",
            "## Contributing",
            "## License",
        ):
            self.assertIn(phrase, readme, f"README.md missing section: {phrase}")

        self.assertIn(
            "Find, verify, and set up the right skill, MCP server, connector, package, or capability stack",
            readme,
        )
        self.assertIn('"Find the best skill for this task: ..."', readme)
        self.assertIn('"Compare these connectors/skills for my agent: ..."', readme)
        self.assertIn('"No good skill exists; find the best stack."', readme)
        self.assertIn("## Research-Quality Evaluation", readme)
        self.assertIn("Evidence Ledger", readme)
        self.assertIn("Counter-Review", readme)
        self.assertIn("[skills/skill-finder/SKILL.md]", readme)
        self.assertIn("Missing optional routes do not block a run", readme)
        self.assertIn("Use `@skill-finder` in Codex", readme)
        self.assertNotIn("### Install As A Local Skill", readme)
        self.assertNotIn("Manual Codex-style install", readme)
        self.assertNotIn("npx skills add Nebulazer123/skill-finder --skill skill-finder", readme)
        self.assertNotIn("skills use Nebulazer123/skill-finder@skill-finder", readme)
        self.assertNotIn("coding assistant improvises", readme)
        self.assertIn("Agent Skills CLI / skills.sh", readme)
        self.assertIn("GitHub MCP", readme)
        self.assertIn("## Setup Requirements", readme)
        self.assertIn("### Built-In Public Evidence Sources", readme)
        self.assertIn("[MCP Registry](https://registry.modelcontextprotocol.io/docs)", readme)
        self.assertIn("[deps.dev](https://docs.deps.dev/api/v3/)", readme)
        self.assertIn("[OSV](https://google.github.io/osv.dev/api/)", readme)
        self.assertIn("[ecosyste.ms](https://ecosyste.ms/api)", readme)
        self.assertIn("They add public research coverage without another install", readme)
        self.assertIn("DeepWiki MCP", readme)
        self.assertIn("Devin MCP", readme)
        self.assertIn("Context7", readme)
        self.assertIn("current API", readme)
        self.assertIn("Hugging Face Hub", readme)
        self.assertIn("Browserbase Browse CLI", readme)
        self.assertIn("[codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)", readme)
        self.assertIn("npm install -g codebase-memory-mcp", readme)
        self.assertIn("codebase-memory-mcp install", readme)
        self.assertIn("Composio CLI / MCP", readme)
        self.assertIn("Codex Plugin Eval", readme)
        self.assertIn("Install In Codex", readme)
        self.assertIn("Install In Claude Code", readme)
        self.assertIn("codex plugin marketplace add Nebulazer123/skill-finder", readme)
        self.assertIn("codex plugin add skill-finder@skill-finder", readme)
        self.assertIn("codex plugin list | grep skill-finder", readme)
        self.assertIn("claude plugin marketplace add Nebulazer123/skill-finder", readme)
        self.assertIn("claude plugin install skill-finder@skill-finder", readme)
        self.assertIn("claude plugin list | grep skill-finder", readme)
        self.assertIn("/skill-finder", readme)
        self.assertIn("Use `/skill-finder` in Claude Code", readme)
        self.assertNotIn("/skill-finder:skill-finder", readme)
        self.assertNotIn("/plugin marketplace add", readme)
        self.assertNotIn("/plugin install", readme)
        self.assertNotIn("/reload-plugins", readme)
        self.assertNotIn("### Pin A Release", readme)
        self.assertNotIn("If you need a reproducible older release", readme)
        self.assertNotIn("marketplace plugin skills are namespaced", readme)
        self.assertIn("codex mcp add github --url https://api.githubcopilot.com/mcp/", readme)
        self.assertIn("codex mcp add deepwiki --url https://mcp.deepwiki.com/mcp", readme)
        self.assertIn("codex mcp add context7", readme)
        self.assertIn("claude mcp add --transport http github https://api.githubcopilot.com/mcp/", readme)
        self.assertIn("claude mcp add --transport http deepwiki https://mcp.deepwiki.com/mcp", readme)
        self.assertIn("claude mcp add context7", readme)
        self.assertIn("browse skills install", readme)
        self.assertIn("Composio docs", readme)
        self.assertIn("package.json", readme)
        self.assertIn("npm setup metadata", readme)
        self.assertIn("@upstash/context7-mcp", readme)
        self.assertIn("Start here", readme)
        self.assertIn('<img src="assets/logos/codex-cloud-color.png"', readme)
        self.assertIn('<img src="assets/logos/claude-code-color.svg"', readme)
        self.assertIn('align="absmiddle"> Install In Codex', readme)
        self.assertIn('align="absmiddle"> Install In Claude Code', readme)
        self.assertIn('<img src="assets/logos/agent-skills.svg"', readme)
        self.assertIn('<img src="assets/logos/huggingface-color.svg"', readme)
        self.assertIn('<img src="assets/logos/install-codex-cloud.svg"', readme)
        self.assertIn('<img src="assets/logos/install-claude-code-button.svg"', readme)
        self.assertIn('<img src="assets/logos/github-invertocat-white.svg"', readme)
        self.assertIn('<img src="assets/logos/deepwiki.png"', readme)
        self.assertIn('<img src="assets/logos/context7.png"', readme)
        self.assertIn('<img src="assets/logos/browserbase.svg"', readme)
        self.assertIn('<img src="assets/logos/devin-color.svg"', readme)
        self.assertIn('<img src="assets/logos/codebase-memory.png"', readme)
        self.assertIn('<img src="assets/logos/composio-symbol.svg"', readme)
        self.assertIn('<img src="assets/logos/plugin-eval.svg"', readme)
        for logo in (
            "agent-skills.svg",
            "github-invertocat-white.svg",
            "deepwiki.png",
            "context7.png",
            "browserbase.svg",
            "codebase-memory.png",
            "devin-color.svg",
            "huggingface-color.svg",
            "composio-symbol.svg",
            "plugin-eval.svg",
            "mcp-registry.svg",
            "deps-dev.svg",
            "osv.png",
            "ecosystems.ico",
        ):
            self.assertIn(
                f'assets/logos/{logo}" alt="" width="22" height="22"',
                readme,
            )
        self.assertLess(
            readme.index("assets/logos/install-codex-cloud.svg"),
            readme.index("## The Problem"),
        )
        self.assertLess(
            readme.index("assets/logos/install-claude-code-button.svg"),
            readme.index("## The Problem"),
        )
        self.assertGreater(
            readme.index("assets/logos/agent-skills.svg"),
            readme.index("## Setup Requirements"),
        )
        for logo in (
            "assets/logos/github-invertocat-white.svg",
            "assets/logos/deepwiki.png",
            "assets/logos/context7.png",
            "assets/logos/browserbase.svg",
            "assets/logos/codebase-memory.png",
            "assets/logos/mcp-registry.svg",
            "assets/logos/deps-dev.svg",
            "assets/logos/osv.png",
            "assets/logos/ecosystems.ico",
        ):
            self.assertGreater(readme.index(logo), readme.index("## Setup Requirements"))
            self.assertLess(readme.index(logo), readme.index("## Recommended When Useful"))
        self.assertGreater(
            readme.index("assets/logos/huggingface-color.svg"),
            readme.index("## Recommended When Useful"),
        )
        for logo in (
            "assets/logos/devin-color.svg",
            "assets/logos/composio-symbol.svg",
            "assets/logos/plugin-eval.svg",
        ):
            self.assertGreater(readme.index(logo), readme.index("## Recommended When Useful"))
        install_codex = _read_text_strict(
            ROOT / "assets" / "logos" / "install-codex-cloud.svg"
        )
        install_claude = _read_text_strict(
            ROOT / "assets" / "logos" / "install-claude-code-button.svg"
        )
        self.assertIn('fill="#fff"', install_codex)
        self.assertIn('fill="#fff"', install_claude)
        self.assertIn('fill="#635BFF"', install_codex)
        self.assertIn('fill="#DA7857"', install_claude)
        self.assertIn('width="260" height="44" viewBox="0 0 260 44"', install_codex)
        self.assertIn('width="260" height="44" viewBox="0 0 260 44"', install_claude)
        self.assertIn('transform="translate(66 13) scale(.75)"', install_codex)
        self.assertIn('transform="translate(98 10) scale(1.05)"', install_codex)
        self.assertIn("M79.915 14.964", install_codex)
        self.assertNotIn("<text", install_codex)
        self.assertIn('transform="translate(86 10)"', install_claude)
        self.assertIn('transform="translate(120 10)"', install_claude)
        self.assertIn("Source review does not authorize", readme)
        self.assertIn("explicit approval", readme.lower())
        self.assertIn("temporary workspace", readme.lower())
        self.assertNotIn("## Dependency Graph", readme)
        self.assertNotIn("## Proof Points", readme)
        self.assertNotIn("Check graphable setup dependencies", readme)
        self.assertNotIn("hf auth login", readme)
        self.assertNotIn("Community plugin note", readme)
        self.assertNotIn("Skill Finder should search", readme)

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

        for phrase in ("models", "datasets", "papers", "Spaces", "evals"):
            self.assertIn(phrase, readme + references)

        self.assertIn('value: "huggingface"', agent_meta)
        self.assertIn('value: "hf"', agent_meta)
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
            "temporary",
            "staging path",
            "cleanup status",
            "staging is not permission to run setup scripts",
            "candidate setup scripts",
        ):
            self.assertIn(phrase, scanned)

    def test_build_story_is_scannable(self):
        evidence = _read_text_strict(ROOT / "HOW_THIS_SKILL_WAS_BUILT.md")

        for phrase in (
            "My Role Versus AI's Role",
            "Build Method",
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

        self.assertIn("account-backed routes remain eligible", scanned)
        self.assertIn("do not downgrade a strong free candidate", scanned)
        self.assertIn("paid/hosted compute", scanned)
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

    def test_metadata_description_matches_readme_value_proposition(self):
        description = (
            "Find, verify, and set up the right skill, MCP server, connector, "
            "package, or capability stack for a task."
        )
        meta = _read_text_strict(ROOT / ".github" / "repo-meta.yml")
        readme = _read_text_strict(ROOT / "README.md")

        self.assertIn(description, meta)
        self.assertIn(description, readme)

    def test_public_docs_do_not_include_private_workspace_paths(self):
        scanned_parts = []
        unreadable_files = []
        for path in _public_package_paths():
            if not path.is_file():
                continue
            if EXCLUDED_SCAN_PARTS.intersection(path.parts):
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
        scanned_lower = scanned.lower()

        forbidden = (
            "/" + "Users/",
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

        personal_name_parts = (
            "cor" + "bin",
            "flo" + "yd",
        )
        for phrase in personal_name_parts:
            self.assertNotIn(
                phrase,
                scanned_lower,
                "Private personal name leaked into public docs",
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
        for path in _public_package_paths():
            if not path.is_file():
                continue
            if EXCLUDED_SCAN_PARTS.intersection(path.parts):
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

    def test_hybrid_evidence_floor_replaces_all_tools_gate(self):
        skill_text = _read_text_strict(
            ROOT / "skills" / "skill-finder" / "SKILL.md"
        )
        readiness = _read_text_strict(
            ROOT / "skills" / "skill-finder" / "references"
            / "dependency-and-capability-readiness.md"
        )
        reference_text = _read_reference_files(
            *(ROOT / "skills" / "skill-finder" / "references").glob("*.md")
        )
        combined = f"{skill_text}\n{readiness}\n{reference_text}".lower()

        self.assertIn("task-specific evidence floor", combined)
        self.assertIn("public/local lane", combined)
        self.assertIn("connected lane", combined)
        self.assertIn("missing optional routes do not block", combined)
        self.assertNotIn("if any required route is missing", combined)
        self.assertNotIn("required before search", combined)
        self.assertNotIn("required setup block", combined)

    def test_engine_commands_resolve_from_loaded_skill_directory(self):
        skill_text = _read_text_strict(
            ROOT / "skills" / "skill-finder" / "SKILL.md"
        )
        self.assertIn("<skill-directory>/scripts/evidence_engine.py", skill_text)
        self.assertIn(
            "Do not assume the workspace root contains the engine",
            skill_text,
        )

    def test_generated_sources_and_route_failures_have_strict_recovery_rules(self):
        skill_text = _read_text_strict(
            ROOT / "skills" / "skill-finder" / "SKILL.md"
        ).lower()

        self.assertIn("never sole proof", skill_text)
        self.assertIn("different source family", skill_text)
        self.assertIn("prompt injection", skill_text)
        self.assertIn("unresolved research", skill_text)

    def test_engine_contract_files_are_public_and_packaged(self):
        paths = [
            ROOT / "skills" / "skill-finder" / "config" / "routes.json",
            ROOT / "skills" / "skill-finder" / "schemas" / "request.schema.json",
            ROOT / "skills" / "skill-finder" / "schemas" / "evidence.schema.json",
            ROOT / "skills" / "skill-finder" / "schemas" / "run.schema.json",
            ROOT / "skills" / "skill-finder" / "scripts" / "evidence_engine.py",
            ROOT / "skills" / "skill-finder" / "references"
            / "hybrid-evidence-engine.md",
        ]
        for path in paths:
            self.assertTrue(path.is_file(), path)


if __name__ == "__main__":
    unittest.main()
