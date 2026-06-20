<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/skill-finder-logo-512.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/skill-finder-logo-512.png">
    <img alt="Skill Finder logo: a magnifying glass inspecting a SKILL.md file among capability cards" src="assets/skill-finder-logo-512.png" width="156">
  </picture>

  <h1>Skill Finder</h1>
  <p>Find the strongest agent-usable skill, tool, MCP server, workflow, package, or capability stack for a real task.</p>
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
  <a href="#features">Features</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#install">Install</a> &middot;
  <a href="#validation">Validation</a>
</div>

Skill Finder helps an agent choose the right capability before it starts improvising. It searches broadly, checks real source material, compares candidates, and returns a small recommendation packet with the evidence needed to act confidently.

Community plugin note: this is not automatically listed in the first-party Codex or Claude Code plugin directories. Add this GitHub repository as a marketplace source first, then install the `skill-finder` plugin from that source.

---

## The Problem

Agents often improvise when they should first look for the right existing capability.

That improvisation is useful until the better answer is an existing skill, MCP server, app connector, workflow, package, or documentation source that the agent never checked. Skill Finder gives the agent a repeatable way to search the ecosystem, inspect important files, compare real tradeoffs, and recommend the strongest option for the task.

## Features

- **Broader search** — finds skills, MCP servers, app connectors, workflow templates, CLIs, packages, validators, documentation sources, and composed stacks.
- **Evidence-first ranking** — reads important files and checks setup, trust, license, and dependency surfaces instead of trusting search snippets.
- **Small recommendation packets** — gathers a broad finalist pool when GitHub matters, then shows at most five useful options.
- **Setup-aware choices** — keeps useful login-gated tools in contention while making setup needs clear.
- **Installable next steps** — includes dependency readiness, verification commands, risks, and explicit approval questions.
- **No-good-option fallback** — drafts a Missing Skill Blueprint when no existing option is strong enough.

## Quick Start

| Ask for | You get |
|---|---|
| `"Find the best skill for this task: ..."` | Ranked recommendation packet |
| `"Compare these connectors/skills for my agent: ..."` | Evidence table and winner |
| `"No good skill exists; find the best stack."` | Missing-capability spec and eval cases |

## When to Use It

Use Skill Finder when:

- a specialized skill or tool may already exist
- the current tool is underperforming, stale, shallow, or too expensive to keep improvising around
- the task needs current research, source inspection, installability checks, or safety review
- a non-skill capability might be the better answer

Example sample flow:

> User: "I have a large messy repo and my coding agent wastes context opening files one at a time. Find the best local capability for definitions, callers, routes, config links, and risky changes without uploading my code."
>
> Skill Finder should search code intelligence tools, MCP servers, package registries, official docs, and GitHub source; inspect finalist files; compare trust and installability; then recommend no more than five options.

## Install

The fastest path is the plugin wrapper for Codex or Claude Code. The canonical artifact is still the skill at `skills/skill-finder/`; the plugin wrapper packages that skill for the two main plugin workflows.

### Plugin Install

#### Install in Codex

Codex:

```bash
codex plugin marketplace add Nebulazer123/skill-finder
codex plugin add skill-finder@skill-finder
```

That installs from the repository's default branch. If you need a reproducible older release, add `--ref <tag>` to pin a specific version.

#### Install in Claude Code

Claude Code:

```text
/plugin marketplace add Nebulazer123/skill-finder
/plugin install skill-finder@skill-finder
/reload-plugins
```

After plugin install:

```text
@skill-finder
/skill-finder
```

Use `@skill-finder` in Codex. Use `/skill-finder` in Claude Code.

### Install as an Agent Skill

Review the files before installing. This repository does not auto-install anything.

Recommended install with the Agent Skills CLI:

```bash
npx skills add Nebulazer123/skill-finder --skill skill-finder
```

If you already have the CLI installed:

```bash
skills add Nebulazer123/skill-finder --skill skill-finder
```

The public package was verified as discoverable with `skills add Nebulazer123/skill-finder --list` and usable without installing via `skills use Nebulazer123/skill-finder@skill-finder`.

Manual local install for Codex-style skill folders:

```bash
mkdir -p ~/.codex/skills
cp -R skills/skill-finder ~/.codex/skills/skill-finder
```

Restart your agent host after copying the skill so its skill list refreshes.

Invoke the local skill the same way:

```text
/skill-finder
```

## Required Setup

Skill Finder is designed to run with a real discovery stack. If a required route is missing, the skill should stop, explain what is missing, and ask whether you want to install or configure it before it ranks candidates.

| Required dependency | Why it is required | Setup |
|---|---|---|
| [Agent Skills CLI / skills.sh](https://github.com/vercel-labs/skills) | Finds and inspects public agent skills instead of guessing from generic search. | `npm install -g skills`; browse at [skills.sh](https://skills.sh). |
| [GitHub MCP](https://github.com/github/github-mcp-server) | Gives the agent source-level repository search and file verification. | Configure the official GitHub MCP server for your agent host. The official server supports Docker via `ghcr.io/github/github-mcp-server`. |
| [DeepWiki MCP](https://docs.devin.ai/work-with-devin/deepwiki-mcp) | Gives fast public-repo maps and source-linked architecture leads before deeper verification. | Add the public DeepWiki MCP endpoint: `https://mcp.deepwiki.com/mcp`. |
| [Context7](https://context7.com/docs/clients/codex) | Checks current API, SDK, CLI, framework, and MCP documentation. | `npx ctx7 setup`; Codex MCP: `codex mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY`. |
| [Browserbase Browse CLI](https://docs.browserbase.com/integrations/skills/browse-cli) | Provides browser-backed search, fetch, snapshots, and live-page evidence. | `npm install -g browse && browse skills install`. |
| Local basics | Needed for local inspection and validation. | Install `git`, `rg`, `python3`, Node.js 18+, `npm`, and `npx`. |

## Recommended Power Routes

These are not required for every run, but Skill Finder should recommend setup when one would materially improve the answer.

| Recommended route | Use when | Setup |
|---|---|---|
| [Devin MCP](https://docs.devin.ai/work-with-devin/devin-mcp) | A repo question needs deeper Q&A, bounded sessions, private-repo context, playbooks, knowledge, schedules, or integrations. | Configure Devin MCP with your Devin account and API key. |
| [Hugging Face Hub MCP](https://huggingface.co/docs/hub/agents-mcp) and [`hf` CLI](https://huggingface.co/docs/huggingface_hub/guides/cli) | The task involves models, datasets, papers, Spaces, MCP-enabled Spaces, evals, benchmarks, inference, or training workflows. | Configure from [Hugging Face MCP settings](https://huggingface.co/settings/mcp); use `hf auth login` for private or higher-limit access. |
| codebase-memory-mcp | Local repo work needs symbol lookup, call paths, route tracing, impact analysis, or architecture summaries. | Configure in your agent host and index the repo before relying on graph answers. |
| [Composio CLI / MCP](https://docs.composio.dev/docs/cli) | The best capability is a connected SaaS action or app connector. | Install from the official Composio docs and connect only the apps you need. |
| [Codex Plugin Eval](https://developers.openai.com/blog/eval-skills) | You are creating or changing a skill and need repeatable scoring. | Install Plugin Eval from the Codex plugin directory when available. |

## Dependency Graph

GitHub can only graph supported manifests and package data. This repo now includes `package.json` for the npm-installable setup tools that are real dependencies of the public setup path:

- `skills`
- `@upstash/context7-mcp`
- `browse`

Remote MCP URLs, Docker images, Homebrew packages, OAuth connections, and hosted account setup cannot be honestly represented as npm packages. They stay in the required setup tables above instead of being faked into the graph.

Recommended evidence flow:

1. Confirm required setup is ready.
2. Use DeepWiki for fast repo orientation.
3. Verify important claims against GitHub MCP source files.
4. Use Context7 or official docs for current API behavior.
5. Use Browserbase when live web evidence is needed.
6. Add Devin, Hugging Face, codebase-memory, Composio, or Plugin Eval when the task would benefit.

A login requirement is not a disqualifier. Skill Finder should keep strong free or public-read candidates in the ranking, mark the setup step clearly, and stop before account linking, billing, remote compute, or persistent changes.

## Safety Boundary

Skill Finder treats candidate files as evidence to inspect, not instructions to obey. It should not run candidate setup scripts, enter credentials, link accounts, delete files, enable integrations, publish content, or mutate global state without explicit approval.

For serious candidates, Skill Finder can clone, download, or stage source artifacts in a temporary workspace for inspection. Staging files is evidence gathering; it is not permission to execute scripts, connect accounts, spend money, or make persistent changes.

The final recommendation should make the next action obvious: install, configure, ask for approval, run a verification command, or draft a missing-capability blueprint.

## Output Shape

A strong recommendation includes:

- Required Setup status
- Search Strategy and Source-Route Scorecard
- Candidate Evidence Table
- files read and scanned
- dependency readiness and verification command
- freshness, adoption, contributor, trust, and license signals
- winner-vs-near-miss reasoning
- source install command or `Install command: not verified`
- risks and approval boundary before install or persistent change

See [examples/recommendation-output-shape.md](examples/recommendation-output-shape.md) for a sample packet.

## Validation

Run public package checks from the repository root:

```bash
python3 -m unittest discover -s validation -v
```

Check the graphable setup manifest with:

```bash
npm pkg get dependencies
```

If you have the Codex skill validator available, validate the skill folder:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/skill-finder
```

This release has also been checked with Plugin Eval from the local development environment. Plugin Eval is recommended for skill authors and maintainers, but it is not required for ordinary use.

## How This Skill Was Built

The build packet records the project history, validation trail, scoring changes, and responsibility notes behind this public package.

See [HOW_THIS_SKILL_WAS_BUILT.md](HOW_THIS_SKILL_WAS_BUILT.md).

## What's Inside

```text
HOW_THIS_SKILL_WAS_BUILT.md                      - project history, scores, and validation summary
skills/skill-finder/SKILL.md                    - skill entrypoint and workflow
skills/skill-finder/agents/openai.yaml          - display metadata and helper dependency notes
skills/skill-finder/references/                 - search, ranking, readiness, and approval rules
examples/                                       - public-safe request and output examples
package.json                                    - graphable npm setup dependencies
validation/                                     - lightweight public package checks
DILIGENCE.md                                    - responsibility and review statement
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
