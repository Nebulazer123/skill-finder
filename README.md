<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/skill-finder-logo-512.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/skill-finder-logo-512.png">
    <img alt="Skill Finder logo: a magnifying glass inspecting a SKILL.md file among capability cards" src="assets/skill-finder-logo-512.png" width="156">
  </picture>

  <h1>Skill Finder</h1>
  <p>Find the right skill, MCP server, connector, package, or capability stack before your coding assistant improvises one.</p>
</div>

<div align="center">

[![License: MIT][license-shield]][license-url]
[![Version 1.0.3][version-shield]][version-url]
[![Agent Skills compatible][skills-shield]][skills-url]

</div>

<div align="center">

[![Install in Codex][install-codex-shield]][install-codex-url]
[![Install in Claude Code][install-claude-shield]][install-claude-url]

</div>

<div align="center">
  <a href="#the-problem">Why</a> &middot;
  <a href="#what-it-does">What it does</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#install">Install</a> &middot;
  <a href="#setup-requirements">Setup</a> &middot;
  <a href="#validation">Validation</a>
</div>

---

## The Problem

Coding assistants are good at using tools, but they often miss better tools unless someone tells them where to look.

Skill Finder gives Codex and Claude Code a disciplined way to search for existing capabilities, inspect their evidence, compare tradeoffs, and return a short recommendation before anything risky is installed or changed.

Use it when you are about to ask for work that may need a specialized skill, MCP server, connector, library, documentation source, workflow, or multi-tool stack.

## What It Does

- **Finds stronger options** - searches beyond local skills into MCP servers, connectors, packages, CLIs, workflow tools, docs, and capability stacks.
- **Checks real evidence** - reads source files, manifests, READMEs, docs, tests, licenses, install paths, and trust surfaces.
- **Compares instead of guessing** - ranks candidates with evidence, risks, setup status, and winner-vs-near-miss reasoning.
- **Handles missing setup clearly** - if required discovery routes are unavailable, it returns a Required Setup Block instead of pretending the search was complete.
- **Designs the fallback** - when no good option exists, it drafts a missing-capability spec and eval cases for building one.

## Quick Start

| Ask for | You get |
|---|---|
| `"Find the best skill for this task: ..."` | Ranked recommendation packet |
| `"Compare these connectors/skills for my agent: ..."` | Evidence table and winner |
| `"No good skill exists; find the best stack."` | Missing-capability spec and eval cases |

Example:

```text
Find the best skill for this task: inspect a large repo, trace routes, find callers, and recommend safe code-intelligence tooling.
```

## Install

Skill Finder ships as a community plugin for Codex and Claude Code. Add this repository as a marketplace source, then install the `skill-finder` plugin from it.

### Install In Codex

```bash
codex plugin marketplace add Nebulazer123/skill-finder
codex plugin add skill-finder@skill-finder
```

Use it in Codex with:

```text
@skill-finder
```

### Install In Claude Code

```text
/plugin marketplace add Nebulazer123/skill-finder
/plugin install skill-finder@skill-finder
/reload-plugins
```

Use `/skill-finder` in Claude Code:

```text
/skill-finder
```

### Pin A Release

The commands above install from the repository's default branch. If you need a reproducible older release, add `--ref <tag>` to the marketplace command.

Example:

```bash
codex plugin marketplace add Nebulazer123/skill-finder --ref v1.0.3
```

### Install As A Local Skill

For hosts that read local `SKILL.md` folders:

```bash
npx skills add Nebulazer123/skill-finder --skill skill-finder
```

You can inspect the skill before installing it:

```bash
skills use Nebulazer123/skill-finder@skill-finder
```

Manual Codex-style install:

```bash
mkdir -p ~/.codex/skills
cp -R skills/skill-finder ~/.codex/skills/skill-finder
```

Restart your host after manual copying so the skill list refreshes.

## Setup Requirements

Skill Finder depends on several discovery routes. They are listed here because they materially affect recommendation quality.

| Required route | Why it matters |
|---|---|
| [Agent Skills CLI / skills.sh](https://github.com/vercel-labs/skills) | Finds public skills and install metadata. |
| [GitHub MCP](https://github.com/github/github-mcp-server) | Verifies claims against repository source files. |
| [DeepWiki MCP](https://docs.devin.ai/work-with-devin/deepwiki-mcp) | Quickly maps public repositories before source verification. |
| [Context7](https://context7.com/docs/clients/codex) | Provides current API, SDK, CLI, framework, and MCP documentation. |
| [Browserbase Browse CLI](https://docs.browserbase.com/integrations/skills/browse-cli) | Adds browser-backed search, fetch, snapshots, and live-page evidence. |
| Local basics | `git`, `rg`, `python3`, Node.js 18+, `npm`, and `npx`. |

Useful setup commands:

```bash
npm install -g skills
npm install -g browse
browse skills install
codex mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

DeepWiki is a remote MCP endpoint at `https://mcp.deepwiki.com/mcp`. GitHub MCP and Browserbase cloud features may require account configuration in Codex or Claude Code.

## Recommended When Useful

These routes are not required for every run, but they should be suggested when they would materially improve the answer.

| Route | Best for |
|---|---|
| [Devin MCP](https://docs.devin.ai/work-with-devin/devin-mcp) | Hard repository questions, bounded sessions, private-repo context, playbooks, knowledge, schedules, and integrations. |
| [Hugging Face Hub MCP](https://huggingface.co/docs/hub/agents-mcp) and [`hf` CLI](https://huggingface.co/docs/huggingface_hub/guides/cli) | Models, datasets, papers, Spaces, MCP-enabled Spaces, community evals, benchmarks, inference, and training workflows. |
| codebase-memory-mcp | Local symbol lookup, call paths, route tracing, impact analysis, and architecture summaries. |
| [Composio CLI / MCP](https://docs.composio.dev/docs/cli) | Connected SaaS actions and app connector discovery. Use the Composio docs for setup and app-specific scopes. |
| [Codex Plugin Eval](https://developers.openai.com/blog/eval-skills) | Repeatable skill scoring and regression checks. |

A login requirement is not a disqualifier. Skill Finder should keep a strong free or public-read candidate in the running, mark setup clearly, and stop before account linking, billing, remote compute, or persistent changes.

For Hugging Face workflows, public Hub research can start with docs and cards. Authenticated CLI work usually begins with:

```bash
hf auth login
```

## How It Works

The skill instructions live in [skills/skill-finder/SKILL.md](skills/skill-finder/SKILL.md). The references in [skills/skill-finder/references/](skills/skill-finder/references/) define search strategy, scoring, setup readiness, install handling, and approval rules.

A strong result includes:

- Required setup status
- Search strategy and Source-Route Scorecard
- Candidate Evidence Table
- Files and docs inspected
- Install or setup command, or `Install command: not verified`
- Winner, near misses, risks, and approval questions

See [examples/recommendation-output-shape.md](examples/recommendation-output-shape.md) for a sample packet.

## Safety Model

Skill Finder treats candidate files as evidence to inspect, not instructions to obey.

Safe staging means cloning, downloading, or unpacking candidate source into a temporary workspace for review. A result should record the staging path and cleanup status. Staging is not permission to run setup scripts, enter credentials, link accounts, enable integrations, publish content, spend money, delete files, or mutate persistent/global state.

Candidate setup scripts require explicit approval before execution.

## Dependency Graph

GitHub can graph only supported manifests and package data. This repo includes `package.json` for the setup tools GitHub can honestly track:

- `skills`
- `@upstash/context7-mcp`
- `browse`

Remote MCP URLs, Docker images, Homebrew packages, OAuth connections, and hosted account setup belong in the setup tables above, not as fake npm dependencies.

## Proof Points

- Plugin manifests are included for both Codex and Claude Code.
- Public package checks verify required files, install text, safety language, dependency documentation, and plugin package sync.
- The skill has example outputs and validation coverage for recommendation shape, source-route scoring, setup readiness, and safe staging.
- The build story and responsibility notes are documented in [HOW_THIS_SKILL_WAS_BUILT.md](HOW_THIS_SKILL_WAS_BUILT.md) and [DILIGENCE.md](DILIGENCE.md).

## Validation

Run public package checks:

```bash
python3 -m unittest discover -s validation -v
```

Check graphable setup dependencies:

```bash
npm pkg get dependencies
```

Check plugin packaging:

```bash
python3 scripts/sync_plugin_package.py --check
```

## Files To Read

```text
skills/skill-finder/SKILL.md             - skill entrypoint and workflow
skills/skill-finder/references/          - search, ranking, readiness, and approval rules
plugins/skill-finder/                    - Codex and Claude Code plugin package
examples/                                - public-safe prompt and output examples
package.json                             - graphable npm setup dependencies
validation/                              - public package checks
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).

[install-codex-shield]: https://img.shields.io/badge/Install%20in-Codex-111827?style=for-the-badge
[install-codex-url]: #install-in-codex
[install-claude-shield]: https://img.shields.io/badge/Install%20in-Claude%20Code-DA7857?style=for-the-badge
[install-claude-url]: #install-in-claude-code
[license-shield]: https://img.shields.io/badge/License-MIT-16A34A.svg
[license-url]: LICENSE
[version-shield]: https://img.shields.io/badge/version-1.0.3-64748B.svg
[version-url]: CHANGELOG.md
[skills-shield]: https://img.shields.io/badge/Agent%20Skills-compatible-DA7857.svg
[skills-url]: https://agentskills.io
