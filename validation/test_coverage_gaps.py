"""Tests for modules with zero or minimal coverage in the existing test suite.

Covers: openai.yaml agent config, CHANGELOG.md, CONTRIBUTING.md content,
SECURITY.md content, DILIGENCE.md, CODE_OF_CONDUCT.md, examples directory,
reference files individual content, SKILL.md workflow and output contract,
cross-file consistency, markdown structure, and LICENSE content.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "skill-finder"
REFS = SKILL_ROOT / "references"


class AgentConfigTests(unittest.TestCase):
    """openai.yaml had near-zero coverage: only two values were checked."""

    def setUp(self):
        self.text = (SKILL_ROOT / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )

    def test_interface_display_name(self):
        self.assertIn('display_name: "Skill Finder"', self.text)

    def test_interface_short_description(self):
        self.assertIn("short_description:", self.text)
        self.assertIn("Find, vet, and prepare skills", self.text)

    def test_interface_default_prompt_references_skill(self):
        self.assertIn("default_prompt:", self.text)
        self.assertIn("$skill-finder", self.text)

    def test_dependencies_section_exists(self):
        self.assertIn("dependencies:", self.text)
        self.assertIn("tools:", self.text)

    def test_all_expected_tool_types_present(self):
        self.assertIn('type: "mcp"', self.text)
        self.assertIn('type: "binary"', self.text)

    def test_mcp_dependencies_listed(self):
        for mcp_name in ("github", "context7", "codebase-memory-mcp", "huggingface"):
            self.assertIn(
                f'value: "{mcp_name}"',
                self.text,
                f"MCP dependency {mcp_name!r} missing",
            )

    def test_binary_dependencies_listed(self):
        for binary in (
            "rg",
            "skills",
            "gh",
            "browse",
            "codebase-memory-mcp",
            "hf",
            "composio",
            "python3",
            "node",
            "npm",
            "npx",
        ):
            self.assertIn(
                f'value: "{binary}"',
                self.text,
                f"Binary dependency {binary!r} missing",
            )

    def test_node_runtime_dependencies_listed(self):
        for binary in ("node", "npm", "npx"):
            with self.subTest(binary=binary):
                self.assertIn(
                    f'value: "{binary}"',
                    self.text,
                    f"Node runtime dependency {binary!r} missing",
                )
        self.assertIn("Node.js 18+", self.text)

    def test_every_tool_has_description(self):
        entries = self.text.split("- type:")
        for entry in entries[1:]:
            self.assertIn(
                "description:",
                entry,
                "Tool entry missing description field",
            )

    def test_tool_count_minimum(self):
        self.assertGreaterEqual(
            self.text.count("- type:"),
            9,
            "Expected at least 9 tool dependency entries",
        )


class PluginPackagingTests(unittest.TestCase):
    """Plugin wrapper and marketplace files need direct coverage."""

    def test_sync_script_exists(self):
        script = ROOT / "scripts" / "sync_plugin_package.py"
        self.assertTrue(script.is_file())
        text = script.read_text(encoding="utf-8")
        self.assertIn("__pycache__", text)
        self.assertIn(".plugin-eval", text)
        self.assertIn('path.suffix == ".pyc"', text)
        text = script.read_text(encoding="utf-8")
        self.assertIn("CODEX_PLUGIN_MANIFEST", text)
        self.assertIn("CLAUDE_PLUGIN_MANIFEST", text)
        self.assertIn("CODEX_MARKETPLACE_MANIFEST", text)
        self.assertIn("CLAUDE_MARKETPLACE_MANIFEST", text)

    def test_codex_manifest_mentions_skills_directory(self):
        text = (
            ROOT / "plugins" / "skill-finder" / ".codex-plugin" / "plugin.json"
        ).read_text(encoding="utf-8")
        self.assertIn('"skills": "./skills/"', text)
        self.assertIn('"name": "skill-finder"', text)

    def test_claude_manifest_mentions_skills_directory(self):
        text = (
            ROOT / "plugins" / "skill-finder" / ".claude-plugin" / "plugin.json"
        ).read_text(encoding="utf-8")
        self.assertIn('"skills": "./skills/"', text)
        self.assertIn('"name": "skill-finder"', text)

    def test_marketplaces_are_documented_in_readme(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Install In Codex", readme)
        self.assertIn("Install In Claude Code", readme)
        self.assertIn("community plugin for Codex and Claude Code", readme)

    def test_install_approval_script_references_exist(self):
        docs = [
            REFS / "install-and-approval.md",
            ROOT / "plugins" / "skill-finder" / "skills" / "skill-finder"
            / "references" / "install-and-approval.md",
        ]
        for path in docs:
            text = path.read_text(encoding="utf-8")
            for match in re.findall(r"`(scripts/[^`\s]+\.py)`", text):
                with self.subTest(file=path.relative_to(ROOT), script=match):
                    self.assertTrue(
                        (ROOT / match).is_file(),
                        f"{path.relative_to(ROOT)} references missing script {match}",
                    )


class ChangelogTests(unittest.TestCase):
    """CHANGELOG.md had zero coverage."""

    def setUp(self):
        self.text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    def test_has_changelog_heading(self):
        self.assertIn("# Changelog", self.text)

    def test_has_version_entries(self):
        versions = re.findall(r"^## (\d+\.\d+\.\d+)", self.text, re.MULTILINE)
        self.assertGreaterEqual(len(versions), 1, "No version entries found")

    def test_versions_are_semver_and_dated(self):
        entries = re.findall(
            r"^## (\d+\.\d+\.\d+) - (\d{4}-\d{2}-\d{2})", self.text, re.MULTILINE
        )
        self.assertGreaterEqual(len(entries), 1, "No dated semver entries found")

    def test_latest_version_matches_readme_badge(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        versions = re.findall(r"^## (\d+\.\d+\.\d+)", self.text, re.MULTILINE)
        latest = versions[0]
        self.assertIn(latest, readme, "Latest changelog version not in README badge")

    def test_entries_are_newest_first(self):
        versions = re.findall(r"^## (\d+\.\d+\.\d+)", self.text, re.MULTILINE)
        tuples = [tuple(int(x) for x in v.split(".")) for v in versions]
        self.assertEqual(tuples, sorted(tuples, reverse=True))

    def test_initial_release_documented(self):
        self.assertIn("0.1.0", self.text)
        self.assertIn("Initial public release", self.text)


class ContributingContentTests(unittest.TestCase):
    """CONTRIBUTING.md had only file-existence coverage."""

    def setUp(self):
        self.text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    def test_has_development_flow_section(self):
        self.assertIn("## Development Flow", self.text)

    def test_documents_test_command(self):
        self.assertIn(
            "python3 -m unittest discover -s skills/skill-finder/tests -v",
            self.text,
        )
        self.assertIn("python3 -m unittest discover -s validation -v", self.text)
        self.assertIn("python3 -m unittest discover -s evaluation -v", self.text)
        self.assertIn("python3 scripts/sync_plugin_package.py --check", self.text)
        self.assertIn("npm ci --ignore-scripts", self.text)
        self.assertIn("npm ls --all", self.text)

    def test_has_contribution_guidelines_section(self):
        self.assertIn("## Contribution Guidelines", self.text)

    def test_warns_against_private_paths(self):
        self.assertIn("private paths", self.text.lower())

    def test_preserves_approval_boundary(self):
        self.assertIn("explicit approval", self.text.lower())

    def test_has_issue_reporting_section(self):
        self.assertIn("## Useful Issue Reports", self.text)


class ValidationCommandParityTests(unittest.TestCase):
    """Public validation command surfaces should not drift apart."""

    REQUIRED_COMMANDS = (
        "python3 -m unittest discover -s skills/skill-finder/tests -v",
        "python3 -m unittest discover -s validation -v",
        "python3 -m unittest discover -s evaluation -v",
        "python3 scripts/sync_plugin_package.py --check",
        "npm ci --ignore-scripts",
        "npm ls --all",
    )

    def test_required_commands_match_docs_pr_template_and_ci(self):
        surfaces = {
            "README.md": ROOT / "README.md",
            "CONTRIBUTING.md": ROOT / "CONTRIBUTING.md",
            ".github/PULL_REQUEST_TEMPLATE.md": ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
            ".github/workflows/validate.yml": ROOT / ".github" / "workflows" / "validate.yml",
        }

        for label, path in surfaces.items():
            text = path.read_text(encoding="utf-8")
            for command in self.REQUIRED_COMMANDS:
                with self.subTest(surface=label, command=command):
                    self.assertIn(command, text)

    def test_package_json_exposes_validation_scripts(self):
        package_json = (ROOT / "package.json").read_text(encoding="utf-8")
        self.assertIn(
            '"test": "python3 -m unittest discover -s skills/skill-finder/tests -v && '
            'python3 -m unittest discover -s validation -v && '
            'python3 -m unittest discover -s evaluation -v"',
            package_json,
        )
        self.assertIn(
            '"check:plugin-package": "python3 scripts/sync_plugin_package.py --check"',
            package_json,
        )

    def test_ci_provisions_declared_local_essentials(self):
        workflow = (
            ROOT / ".github" / "workflows" / "validate.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("apt-get install -y ripgrep", workflow)


class SecurityContentTests(unittest.TestCase):
    """SECURITY.md had only file-existence coverage."""

    def setUp(self):
        self.text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")

    def test_has_reporting_section(self):
        self.assertIn("## Reporting a Vulnerability", self.text)

    def test_has_supported_versions_section(self):
        self.assertIn("## Supported Versions", self.text)

    def test_has_scope_section(self):
        self.assertIn("## Scope", self.text)

    def test_scope_covers_key_risks(self):
        for risk in (
            "expose secrets",
            "run candidate scripts without approval",
            "install or mutate global state without approval",
            "recommend unsafe commands as verified",
        ):
            self.assertIn(risk, self.text)

    def test_has_safety_notes_section(self):
        self.assertIn("## Safety Notes", self.text)

    def test_has_handling_section(self):
        self.assertIn("## Handling", self.text)

    def test_warns_against_credential_exposure(self):
        self.assertIn("credentials", self.text.lower())


class DiligenceTests(unittest.TestCase):
    """DILIGENCE.md had zero coverage."""

    def setUp(self):
        self.text = (ROOT / "DILIGENCE.md").read_text(encoding="utf-8")

    def test_has_heading(self):
        self.assertIn("# Diligence Statement", self.text)

    def test_discloses_ai_collaboration(self):
        self.assertIn("collaborated with AI", self.text)

    def test_describes_human_review(self):
        self.assertIn("reviewed and directed the work", self.text)
        self.assertIn("take responsibility", self.text)

    def test_links_to_build_story_file(self):
        self.assertIn("HOW_THIS_SKILL_WAS_BUILT.md", self.text)

    def test_excludes_private_material_note(self):
        self.assertIn("private planning notes", self.text.lower())
        self.assertIn("excluded from the public package", self.text.lower())


class CodeOfConductContentTests(unittest.TestCase):
    """CODE_OF_CONDUCT.md had only file-existence coverage."""

    def setUp(self):
        self.text = (ROOT / "CODE_OF_CONDUCT.md").read_text(encoding="utf-8")

    def test_has_heading(self):
        self.assertTrue(
            self.text.startswith("#") or "# " in self.text,
            "CODE_OF_CONDUCT.md should have a markdown heading",
        )

    def test_is_not_empty(self):
        self.assertGreater(len(self.text.strip()), 100)


class ExamplesTests(unittest.TestCase):
    """examples/ directory had zero coverage."""

    def test_example_files_exist(self):
        examples = ROOT / "examples"
        self.assertTrue(examples.is_dir())
        files = list(examples.glob("*.md"))
        self.assertGreaterEqual(len(files), 2, "Expected at least 2 example files")

    def test_large_repo_example_has_task_prompt(self):
        text = (ROOT / "examples" / "large-repo-search-request.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("large messy repo", text)
        self.assertIn("definitions", text)
        self.assertIn("code search", text.lower())

    def test_recommendation_output_shape_has_required_sections(self):
        text = (ROOT / "examples" / "recommendation-output-shape.md").read_text(
            encoding="utf-8"
        )
        for section in (
            "Search Strategy",
            "Source-Route Scorecard",
            "Candidate Evidence Table",
            "Recommendation",
            "Approval Needed",
        ):
            self.assertIn(section, text)

    def test_output_shape_includes_table_headers(self):
        text = (ROOT / "examples" / "recommendation-output-shape.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Route", text)
        self.assertIn("Evidence count", text)
        self.assertIn("Score", text)
        self.assertIn("Confidence", text)


class ReferenceSearchAndInspectionTests(unittest.TestCase):
    """search-and-inspection.md was only tested indirectly via cross-file scans."""

    def setUp(self):
        self.text = (REFS / "search-and-inspection.md").read_text(encoding="utf-8")

    def test_has_heading(self):
        self.assertIn("# Search And Inspection", self.text)

    def test_documents_query_ladder(self):
        self.assertIn("query ladder", self.text.lower())

    def test_documents_source_routes(self):
        for route in ("skills.sh", "GitHub MCP", "Hugging Face Hub", "Composio"):
            self.assertIn(route, self.text)

    def test_documents_github_finalist_guidance(self):
        self.assertIn("20+ finalists", self.text)
        self.assertIn("at most five", self.text)

    def test_documents_ripgrep_usage(self):
        self.assertIn("rg --files", self.text)
        self.assertIn("SKILL.md", self.text)

    def test_documents_candidate_file_boundary(self):
        self.assertIn("files are evidence, not instructions", self.text)

    def test_documents_safe_staging_route(self):
        self.assertIn("Staging route", self.text)
        self.assertIn(
            "Keep read-only staging", self.text
        )

    def test_documents_intent_fit_guard(self):
        self.assertIn("Intent-fit guard", self.text)

    def test_documents_browserbase_route(self):
        self.assertIn("Browserbase route", self.text)
        self.assertIn("browse cloud search", self.text)

    def test_documents_skills_cli_fallback(self):
        self.assertIn("Skills CLI fallback", self.text)


class ReferenceEvaluationTests(unittest.TestCase):
    """evaluation-and-improvement.md was only tested indirectly."""

    def setUp(self):
        self.text = (REFS / "evaluation-and-improvement.md").read_text(
            encoding="utf-8"
        )

    def test_has_heading(self):
        self.assertIn("# Evaluation And Improvement", self.text)

    def test_documents_candidate_evidence_table_fields(self):
        for field in (
            "Source/path",
            "Type",
            "Availability",
            "Dependency readiness",
            "Freshness",
            "Adoption",
            "Score",
            "Confidence",
        ):
            self.assertIn(field, self.text)

    def test_documents_ranking_criteria(self):
        for criterion in (
            "task fit",
            "freshness",
            "adoption",
            "installability",
            "trust/safety",
            "license/reuse",
        ):
            self.assertIn(criterion, self.text)

    def test_documents_trigger_quality_scoring(self):
        self.assertIn("Trigger-quality scoring", self.text)
        for fit in ("strong", "medium", "weak"):
            self.assertIn(fit, self.text)

    def test_documents_reuse_lanes(self):
        for lane in ("Use", "Install", "Copy", "Adapt", "Learn", "Unknown"):
            self.assertIn(f"`{lane}`", self.text)

    def test_documents_missing_skill_blueprint(self):
        self.assertIn("Missing Skill Blueprint", self.text)
        self.assertIn("no good skill was found", self.text.lower())

    def test_documents_plugin_eval(self):
        self.assertIn("Plugin Eval", self.text)
        self.assertIn("plugin-eval analyze", self.text)

    def test_documents_acceptance_rubric(self):
        self.assertIn("Recommendation Acceptance Rubric", self.text)

    def test_documents_hugging_face_scoring(self):
        self.assertIn("Hugging Face scoring", self.text)
        self.assertIn("model or dataset fit", self.text)


class ReferenceDependencyReadinessTests(unittest.TestCase):
    """dependency-and-capability-readiness.md was only tested indirectly."""

    def setUp(self):
        self.text = (REFS / "dependency-and-capability-readiness.md").read_text(
            encoding="utf-8"
        )

    def test_has_heading(self):
        self.assertIn("# Dependency And Capability Readiness", self.text)

    def test_documents_capability_types(self):
        for cap_type in (
            "skill",
            "MCP",
            "connector",
            "CLI",
            "package",
        ):
            self.assertIn(cap_type, self.text)

    def test_documents_baseline_helper_readiness(self):
        self.assertIn("Local Essentials", self.text)
        for helper in ("python3", "git", "rg", "npm", "npx"):
            self.assertIn(f"`{helper}`", self.text)
        self.assertIn("task-specific", self.text)

    def test_documents_dependency_readiness_ledger(self):
        self.assertIn("Readiness Ledger", self.text)
        for field in ("required-for-this-task", "optional", "installed", "missing", "staged/downloaded"):
            self.assertIn(field, self.text)

    def test_documents_credential_readiness(self):
        self.assertIn("Account-backed routes remain eligible", self.text)
        self.assertIn("authorized", self.text)

    def test_documents_hugging_face_readiness(self):
        self.assertIn("Hugging Face MCP/CLI", self.text)
        self.assertIn("models, datasets, Spaces", self.text)

    def test_documents_browserbase_readiness(self):
        self.assertIn("Browserbase Browse CLI", self.text)
        self.assertIn("static docs and source are insufficient", self.text)

    def test_documents_sandbox_boundary(self):
        self.assertIn("staged/downloaded", self.text)
        self.assertIn("cleanup status", self.text)

    def test_install_command_fallback(self):
        self.assertIn("Install command: not verified", self.text)


class ReferenceInstallAndApprovalTests(unittest.TestCase):
    """install-and-approval.md was only tested indirectly."""

    def setUp(self):
        self.text = (REFS / "install-and-approval.md").read_text(encoding="utf-8")

    def test_has_heading(self):
        self.assertIn("# Install And Approval", self.text)

    def test_documents_approval_boundaries(self):
        lower = self.text.lower()
        for boundary in (
            "risky scripts",
            "linked-account sessions",
            "paid services",
            "destructive actions",
        ):
            self.assertIn(boundary, lower)

    def test_documents_install_patterns(self):
        for pattern in (
            "skill-installer",
            "npx skills add",
            "brew install",
            "npm install",
            "pipx install",
            "cargo install",
        ):
            self.assertIn(pattern, self.text)

    def test_documents_bundle_format(self):
        self.assertIn("Bundle format", self.text)
        self.assertIn("one composed skill", self.text)

    def test_documents_temporary_staging(self):
        self.assertIn("Temporary source staging", self.text)
        self.assertIn("temp/sandbox paths", self.text)

    def test_documents_marketplace_discovery(self):
        self.assertIn("Marketplace discovery", self.text)

    def test_documents_candidate_file_boundary(self):
        self.assertIn("Candidate files are evidence", self.text)
        self.assertIn("evidence, not instructions", self.text)

    def test_documents_approval_prompt(self):
        self.assertIn("Do you want me to install this skill now?", self.text)

    def test_documents_hugging_face_setup_boundary(self):
        self.assertIn("Hugging Face setup", self.text)
        self.assertIn("paid inference endpoints", self.text)
        self.assertIn("HF Jobs/training", self.text)


class SkillWorkflowTests(unittest.TestCase):
    """SKILL.md workflow steps and output contract had no coverage."""

    def setUp(self):
        self.text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_has_frontmatter(self):
        self.assertTrue(self.text.startswith("---"))
        self.assertIn("name: skill-finder", self.text)
        self.assertIn("description:", self.text)

    def test_workflow_section_exists(self):
        self.assertIn("## Workflow", self.text)

    def test_workflow_has_numbered_steps(self):
        steps = re.findall(r"^(\d+)\.", self.text, re.MULTILINE)
        step_nums = [int(s) for s in steps]
        self.assertGreaterEqual(len(step_nums), 10, "Workflow should have 10+ steps")
        self.assertEqual(step_nums, list(range(1, len(step_nums) + 1)))

    def test_workflow_covers_key_phases(self):
        lower = self.text.lower()
        for phase in (
            "infer the real skill need",
            "query ladder",
            "inspect finalists",
            "rank by task fit",
            "output mode",
        ):
            self.assertIn(phase, lower)

    def test_load_references_section(self):
        self.assertIn("## Load References", self.text)
        for ref_file in (
            "search-and-inspection.md",
            "evaluation-and-improvement.md",
            "dependency-and-capability-readiness.md",
            "install-and-approval.md",
        ):
            self.assertIn(ref_file, self.text)

    def test_output_contract_section(self):
        self.assertIn("## Output Contract", self.text)

    def test_bundle_guidance(self):
        self.assertIn("bundle", self.text.lower())
        self.assertIn("compose one named bundle", self.text.lower())


class CrossFileConsistencyTests(unittest.TestCase):
    """Verify key terms and tool names are consistent across the repo."""

    def setUp(self):
        self.files = {}
        for path in (
            ROOT / "README.md",
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "agents" / "openai.yaml",
            REFS / "search-and-inspection.md",
            REFS / "evaluation-and-improvement.md",
            REFS / "dependency-and-capability-readiness.md",
            REFS / "install-and-approval.md",
        ):
            self.files[path.name] = path.read_text(encoding="utf-8")
        self.all_text = "\n".join(self.files.values())

    def test_skill_name_consistent(self):
        for name, content in self.files.items():
            if name == "openai.yaml":
                self.assertIn("Skill Finder", content)
            elif name in ("SKILL.md", "README.md"):
                self.assertIn("Skill Finder", content)

    def test_approval_boundary_mentioned_in_skill_and_refs(self):
        for name in ("SKILL.md", "install-and-approval.md"):
            self.assertIn(
                "approval",
                self.files[name].lower(),
                f"Approval concept missing from {name}",
            )
        self.assertIn("review", self.files["evaluation-and-improvement.md"].lower())

    def test_candidate_evidence_table_mentioned_in_skill_and_eval(self):
        for name in ("SKILL.md", "evaluation-and-improvement.md"):
            self.assertIn(
                "Candidate Evidence Table",
                self.files[name],
                f"Candidate Evidence Table missing from {name}",
            )

    def test_source_route_scorecard_in_readme_and_example(self):
        readme = self.files["README.md"]
        example = (ROOT / "examples" / "recommendation-output-shape.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Source-Route Scorecard", readme)
        self.assertIn("Source-Route Scorecard", example)

    def test_install_command_not_verified_across_files(self):
        for name in ("SKILL.md", "dependency-and-capability-readiness.md",
                      "install-and-approval.md", "evaluation-and-improvement.md"):
            self.assertIn(
                "Install command: not verified",
                self.files[name],
                f"'Install command: not verified' missing from {name}",
            )

    def test_twenty_plus_finalists_in_skill_and_search_ref(self):
        for name in ("SKILL.md", "search-and-inspection.md"):
            self.assertIn(
                "20+",
                self.files[name],
                f"'20+' finalist guidance missing from {name}",
            )

    def test_at_most_five_in_skill_and_search_ref(self):
        for name in ("SKILL.md", "search-and-inspection.md"):
            self.assertIn(
                "at most five",
                self.files[name],
                f"'at most five' guidance missing from {name}",
            )


class MarkdownStructureTests(unittest.TestCase):
    """Validate heading structure and internal references."""

    def test_readme_headings_are_well_formed(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        headings = re.findall(r"^(#{1,6}) (.+)$", readme, re.MULTILINE)
        self.assertGreater(len(headings), 5)
        for level, title in headings:
            self.assertGreater(len(title.strip()), 0, "Empty heading found")

    def test_readme_internal_links_resolve(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", readme)
        for text, target in md_links:
            if target.startswith("http"):
                continue
            target_path = target.split("#")[0]
            if not target_path:
                continue
            self.assertTrue(
                (ROOT / target_path).exists(),
                f"Broken internal link: [{text}]({target})",
            )

    def test_reference_files_each_have_heading(self):
        for ref_file in REFS.glob("*.md"):
            text = ref_file.read_text(encoding="utf-8")
            self.assertTrue(
                text.startswith("#") or "\n# " in text,
                f"{ref_file.name} missing a top-level heading",
            )

    def test_no_duplicate_h2_headings_in_readme(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        h2s = re.findall(r"^## (.+)$", readme, re.MULTILINE)
        self.assertEqual(len(h2s), len(set(h2s)), f"Duplicate H2s: {h2s}")


class LicenseContentTests(unittest.TestCase):
    """LICENSE file existence was tested but content was not."""

    def setUp(self):
        self.text = (ROOT / "LICENSE").read_text(encoding="utf-8")

    def test_is_mit_license(self):
        self.assertIn("MIT License", self.text)

    def test_has_permission_clause(self):
        self.assertIn("Permission is hereby granted", self.text)

    def test_has_warranty_disclaimer(self):
        self.assertIn("WITHOUT WARRANTY", self.text.upper())


if __name__ == "__main__":
    unittest.main()
