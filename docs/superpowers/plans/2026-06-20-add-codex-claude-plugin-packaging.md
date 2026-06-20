# Add Codex And Claude Plugin Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add installable Codex and Claude Code plugin packaging around the existing Skill Finder skill without replacing the canonical skill.

**Architecture:** Keep `skills/skill-finder/` as the single source of truth. Generate one dual-manifest plugin wrapper at `plugins/skill-finder/` with both `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`, plus repo marketplace files for Codex and Claude. Add a deterministic sync/check script so plugin-packaged skill files cannot drift from the canonical skill.

**Tech Stack:** Python stdlib, JSON manifests, Codex plugin marketplace, Claude Code plugin marketplace, existing `unittest` validation suite.

---

## Research Notes

- Codex docs: skills are the workflow authoring format, and plugins are the installable distribution unit for reusable skills and apps in Codex: https://developers.openai.com/codex/skills
- Codex plugin docs: plugins can bundle skills, apps, and MCP servers: https://developers.openai.com/codex/plugins
- Codex build docs: plugin folders require `.codex-plugin/plugin.json`; repo marketplaces live at `$REPO_ROOT/.agents/plugins/marketplace.json`; `codex plugin marketplace add owner/repo` is supported: https://developers.openai.com/codex/plugins/build
- Claude Code skills docs: Claude Code supports Agent Skills and direct `/skill-name` invocation: https://code.claude.com/docs/en/skills
- Claude Code plugin docs: plugins can contain skills, agents, hooks, MCP servers, LSP servers, and monitors: https://code.claude.com/docs/en/plugins
- Claude Code marketplace docs: marketplace files live at `.claude-plugin/marketplace.json`, and users install with `/plugin marketplace add ...` then `/plugin install plugin@marketplace`: https://code.claude.com/docs/en/plugin-marketplaces
- Claude Code plugin reference: `.claude-plugin/plugin.json` is the Claude manifest; if present, `name` is the only required field; plugin skills are namespaced as `/plugin-name:skill-name`: https://code.claude.com/docs/en/plugins-reference

## File Structure

- Create: `plugins/skill-finder/.codex-plugin/plugin.json`
  Codex plugin manifest generated from source metadata.
- Create: `plugins/skill-finder/.claude-plugin/plugin.json`
  Claude Code plugin manifest generated from source metadata.
- Create: `plugins/skill-finder/skills/skill-finder/`
  Generated copy of canonical `skills/skill-finder/` for plugin distribution.
- Create: `plugins/skill-finder/assets/skill-finder-logo-512.png`
  Plugin logo copied from `assets/skill-finder-logo-512.png`.
- Create: `.agents/plugins/marketplace.json`
  Codex repo marketplace.
- Create: `.claude-plugin/marketplace.json`
  Claude Code repo marketplace.
- Create: `scripts/sync_plugin_package.py`
  Deterministic generator and drift checker for plugin package files.
- Modify: `validation/test_public_package.py`
  Add plugin packaging, manifest, marketplace, and sync tests.
- Modify: `README.md`
  Add plugin install options for Codex and Claude while preserving skill install instructions.
- Modify: `CHANGELOG.md`
  Add a v1.0.1 entry describing plugin packaging.
- Optional local verification only: run Codex and Claude CLI plugin commands if installed and if the session is allowed to mutate local plugin/marketplace state.

## Task 1: Add Failing Plugin Package Tests

**Files:**
- Modify: `validation/test_public_package.py`
- Test: `validation/test_public_package.py`

- [ ] **Step 1: Add JSON import**

At the top of `validation/test_public_package.py`, change:

```python
from pathlib import Path
import unittest
```

to:

```python
import json
from pathlib import Path
import subprocess
import sys
import unittest
```

- [ ] **Step 2: Add plugin file existence checks**

Inside `PublicPackageTests`, after `test_skill_files_exist`, add:

```python
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
```

- [ ] **Step 3: Add Codex plugin manifest shape test**

After `test_plugin_package_files_exist`, add:

```python
    def test_codex_plugin_manifest_shape(self):
        manifest = json.loads(
            _read_text_strict(
                ROOT / "plugins" / "skill-finder" / ".codex-plugin" / "plugin.json"
            )
        )

        self.assertEqual(manifest["name"], "skill-finder")
        self.assertEqual(manifest["version"], "1.0.1")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["repository"], "https://github.com/Nebulazer123/skill-finder")
        self.assertEqual(manifest["author"]["name"], "Nebulazer123")
        self.assertEqual(manifest["interface"]["displayName"], "Skill Finder")
        self.assertEqual(manifest["interface"]["category"], "Productivity")
        self.assertEqual(manifest["interface"]["logo"], "./assets/skill-finder-logo-512.png")
        self.assertIn("capability", manifest["keywords"])
        self.assertLessEqual(len(manifest["interface"]["defaultPrompt"]), 3)
        for prompt in manifest["interface"]["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)
```

- [ ] **Step 4: Add Claude plugin manifest shape test**

After `test_codex_plugin_manifest_shape`, add:

```python
    def test_claude_plugin_manifest_shape(self):
        manifest = json.loads(
            _read_text_strict(
                ROOT / "plugins" / "skill-finder" / ".claude-plugin" / "plugin.json"
            )
        )

        self.assertEqual(manifest["name"], "skill-finder")
        self.assertEqual(manifest["displayName"], "Skill Finder")
        self.assertEqual(manifest["version"], "1.0.1")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["repository"], "https://github.com/Nebulazer123/skill-finder")
        self.assertEqual(manifest["author"]["name"], "Nebulazer123")
        self.assertIn("capability", manifest["keywords"])
```

- [ ] **Step 5: Add marketplace tests**

After `test_claude_plugin_manifest_shape`, add:

```python
    def test_plugin_marketplaces_reference_skill_finder(self):
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
        self.assertEqual(claude_entry["version"], "1.0.1")
        self.assertEqual(claude_entry["category"], "Productivity")
```

- [ ] **Step 6: Add plugin sync check test**

After `test_plugin_marketplaces_reference_skill_finder`, add:

```python
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
```

- [ ] **Step 7: Run test to verify it fails**

Run:

```bash
python3 -m unittest validation.test_public_package.PublicPackageTests.test_plugin_package_files_exist -v
```

Expected: FAIL with a message containing `Required plugin package file missing`.

- [ ] **Step 8: Commit failing tests**

```bash
git add validation/test_public_package.py
git commit -m "test: cover plugin packaging"
```

## Task 2: Add Deterministic Plugin Sync Script

**Files:**
- Create: `scripts/sync_plugin_package.py`
- Generated by script: `plugins/skill-finder/**`
- Generated by script: `.agents/plugins/marketplace.json`
- Generated by script: `.claude-plugin/marketplace.json`
- Test: `validation/test_public_package.py`

- [ ] **Step 1: Create the sync script**

Create `scripts/sync_plugin_package.py` with this exact content:

```python
#!/usr/bin/env python3
"""Generate and check Skill Finder plugin package files."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.1"
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
```

- [ ] **Step 2: Generate plugin package files**

Run:

```bash
python3 scripts/sync_plugin_package.py
```

Expected:

```text
Plugin package synced.
```

- [ ] **Step 3: Verify drift check passes**

Run:

```bash
python3 scripts/sync_plugin_package.py --check
```

Expected:

```text
Plugin package is in sync.
```

- [ ] **Step 4: Run plugin package tests**

Run:

```bash
python3 -m unittest validation.test_public_package.PublicPackageTests.test_plugin_package_files_exist validation.test_public_package.PublicPackageTests.test_codex_plugin_manifest_shape validation.test_public_package.PublicPackageTests.test_claude_plugin_manifest_shape validation.test_public_package.PublicPackageTests.test_plugin_marketplaces_reference_skill_finder validation.test_public_package.PublicPackageTests.test_plugin_package_is_in_sync_with_canonical_skill -v
```

Expected: all five tests PASS.

- [ ] **Step 5: Validate Codex plugin manifest with local validator**

Run:

```bash
python3 <skill-creator-root>/../plugin-creator/scripts/validate_plugin.py plugins/skill-finder
```

Expected: validation succeeds with no errors.

- [ ] **Step 6: Commit generated package and sync script**

```bash
git add scripts/sync_plugin_package.py plugins/skill-finder .agents/plugins/marketplace.json .claude-plugin/marketplace.json
git commit -m "feat: add dual plugin package"
```

## Task 3: Update Public Install Documentation

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Test: `validation/test_public_package.py`

- [ ] **Step 1: Add plugin install copy to README**

In `README.md`, under the existing `## Install` section and after the manual local skill install block, add:

```markdown
### Plugin Install

The canonical artifact is still the skill at `skills/skill-finder/`. The plugin wrapper packages that skill for Codex and Claude Code plugin workflows.

Codex:

```bash
codex plugin marketplace add Nebulazer123/skill-finder --ref v1.0.1
codex plugin add skill-finder@skill-finder
```

Claude Code:

```text
/plugin marketplace add Nebulazer123/skill-finder
/plugin install skill-finder@skill-finder
/reload-plugins
```

After install, invoke the packaged skill as:

```text
@skill-finder
/skill-finder:skill-finder
```
```

- [ ] **Step 2: Add README assertions**

In `validation/test_public_package.py`, inside `test_readme_has_public_front_door_sections`, after the existing marketplace/source assertions, add:

```python
        self.assertIn("### Plugin Install", readme)
        self.assertIn("codex plugin marketplace add Nebulazer123/skill-finder --ref v1.0.1", readme)
        self.assertIn("codex plugin add skill-finder@skill-finder", readme)
        self.assertIn("/plugin marketplace add Nebulazer123/skill-finder", readme)
        self.assertIn("/plugin install skill-finder@skill-finder", readme)
        self.assertIn("/skill-finder:skill-finder", readme)
```

- [ ] **Step 3: Add changelog entry**

At the top of `CHANGELOG.md`, after `# Changelog`, add:

```markdown
## 1.0.1 - 2026-06-20

- Added Codex and Claude Code plugin packaging while keeping `skills/skill-finder/` as the canonical skill source.
- Added repo marketplace files for Codex and Claude plugin installation.
- Added a deterministic sync/check script and validation coverage so packaged plugin skills cannot drift from the canonical skill.

```

- [ ] **Step 4: Run documentation tests**

Run:

```bash
python3 -m unittest validation.test_public_package.PublicPackageTests.test_readme_has_public_front_door_sections validation.test_coverage_gaps.ChangelogTests -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit docs**

```bash
git add README.md CHANGELOG.md validation/test_public_package.py
git commit -m "docs: document plugin installs"
```

## Task 4: Add Full Validation Coverage For Plugin Packaging

**Files:**
- Modify: `validation/test_coverage_gaps.py`
- Test: `validation/test_coverage_gaps.py`

- [ ] **Step 1: Add plugin packaging coverage class**

In `validation/test_coverage_gaps.py`, after `AgentConfigTests`, add:

```python
class PluginPackagingTests(unittest.TestCase):
    """Plugin wrapper and marketplace files need direct coverage."""

    def test_sync_script_exists(self):
        script = ROOT / "scripts" / "sync_plugin_package.py"
        self.assertTrue(script.is_file())
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
        self.assertIn("Codex:", readme)
        self.assertIn("Claude Code:", readme)
        self.assertIn("plugin wrapper packages that skill", readme)
```

- [ ] **Step 2: Run coverage gap tests**

Run:

```bash
python3 -m unittest validation.test_coverage_gaps.PluginPackagingTests -v
```

Expected: all tests PASS.

- [ ] **Step 3: Commit coverage tests**

```bash
git add validation/test_coverage_gaps.py
git commit -m "test: cover plugin package docs"
```

## Task 5: Run Full Validation And Optional CLI Smoke Tests

**Files:**
- No new files
- Test: full validation suite
- Optional manual smoke: Codex CLI and Claude Code CLI

- [ ] **Step 1: Run public package validation**

Run from repository root:

```bash
python3 -m unittest discover -s validation -v
```

Expected: all public package tests PASS.

- [ ] **Step 2: Run workspace tests**

Run from the workspace root that contains the shared `tests/` directory:

```bash
python3 -m unittest discover -s tests
```

Expected: all workspace tests PASS.

- [ ] **Step 3: Run sync check**

Run from `public-release`:

```bash
python3 scripts/sync_plugin_package.py --check
```

Expected:

```text
Plugin package is in sync.
```

- [ ] **Step 4: Run Codex plugin validator**

Run:

```bash
python3 <skill-creator-root>/../plugin-creator/scripts/validate_plugin.py plugins/skill-finder
```

Expected: validation succeeds with no errors.

- [ ] **Step 5: Run Claude plugin validator when Claude Code is installed**

Run:

```bash
command -v claude >/dev/null && claude plugin validate plugins/skill-finder --strict
```

Expected when `claude` exists: validation succeeds with no errors. Expected when `claude` is missing: command exits without running validation.

- [ ] **Step 6: Optional Codex install smoke after local-state approval**

Only run this step when the current session is allowed to add local Codex marketplaces/plugins:

```bash
codex plugin marketplace add . --json
codex plugin add skill-finder@skill-finder --json
codex plugin list --available --json
```

Expected: `skill-finder` is visible in the `skill-finder` marketplace and can be installed.

- [ ] **Step 7: Optional Claude install smoke after local-state approval**

Only run this step when the current session is allowed to add local Claude marketplaces/plugins:

```text
/plugin marketplace add .
/plugin install skill-finder@skill-finder
/reload-plugins
/skill-finder:skill-finder Find the best skill for repo-intelligence work.
```

Expected: Claude loads the packaged skill under `/skill-finder:skill-finder`.

- [ ] **Step 8: Commit final verification note only if files changed**

If Step 1-5 caused no file changes, do not commit. If a validator auto-formatted files, review the diff and commit:

```bash
git add <changed-files>
git commit -m "chore: finalize plugin packaging validation"
```

## Task 6: Release The Plugin Packaging Update

**Files:**
- No new files unless version tags require release note edits

- [ ] **Step 1: Confirm working tree is clean**

Run:

```bash
git status -sb
```

Expected:

```text
## main...origin/main
```

- [ ] **Step 2: Push main**

Run:

```bash
git push origin main
```

Expected: main branch pushes successfully.

- [ ] **Step 3: Tag v1.0.1**

Run:

```bash
git tag -a v1.0.1 -m "Skill Finder v1.0.1"
git push origin v1.0.1
```

Expected: `v1.0.1` is visible on the remote.

- [ ] **Step 4: Move short v1 tag to latest v1 release**

Run:

```bash
git tag -f -a v1 -m "Skill Finder v1"
git push --force origin v1
```

Expected: `v1` points at the same commit as `v1.0.1`.

- [ ] **Step 5: Final remote audit**

Run:

```bash
git status -sb
git ls-remote --tags origin 'v1*'
gh pr list --state open --json number,title,url --limit 20
gh issue list --state open --json number,title,url --limit 20
```

Expected:

```text
## main...origin/main
```

Expected tag output includes `refs/tags/v1` and `refs/tags/v1.0.1`. Expected PR and issue JSON outputs are `[]` unless new unrelated work was opened after this plan was written.

## Self-Review

**Spec coverage:** This plan covers Codex plugin packaging, Claude Code plugin packaging, marketplace install surfaces, docs, tests, sync enforcement, validation, and release tagging.

**Placeholder scan:** The plan contains no `TBD`, `TODO`, `implement later`, or vague "add tests" steps. Each code or manifest change includes concrete content.

**Type consistency:** The plugin name is consistently `skill-finder`, the packaged skill path is consistently `plugins/skill-finder/skills/skill-finder/`, the version is consistently `1.0.1`, and the marketplace name is consistently `skill-finder`.

**Execution choice:** Plan complete and saved to `docs/superpowers/plans/2026-06-20-add-codex-claude-plugin-packaging.md`. Two execution options:

**1. Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
