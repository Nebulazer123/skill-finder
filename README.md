<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/skill-finder-logo-512.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/skill-finder-logo-512.png">
    <img alt="Skill Finder logo: a magnifying glass inspecting a SKILL.md file among capability cards" src="assets/skill-finder-logo-512.png" width="156">
  </picture>

  <h1>Skill Finder</h1>
  <p>Find, verify, and set up the right skill, MCP server, connector, package, or capability stack for a task.</p>
</div>

<div align="center">

[![License: MIT][license-shield]][license-url]
[![Version 1.3.0][version-shield]][version-url]
[![Agent Skills compatible][skills-shield]][skills-url]

</div>

<div align="center">

<a href="#install-in-codex"><img src="assets/logos/install-codex-cloud.svg" alt="Install in Codex" height="44"></a>
&nbsp;
<a href="#install-in-claude-code"><img src="assets/logos/install-claude-code-button.svg" alt="Install in Claude Code" height="44"></a>

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

The first plausible tool is often not the best one for the job. It may be stale, unsupported in your host, unsafe to install, or simply a poor fit for the task.

Skill Finder helps Codex and Claude Code search for existing capabilities, verify the important claims, compare tradeoffs, and recommend a clear next step before work begins.

Use it before work that may need a specialized skill, MCP server, connector, library, documentation source, workflow, or multi-tool stack. It is a research and selection tool, not a package manager or task executor.

## What It Does

- **Finds stronger options** - searches beyond local skills into MCP servers, connectors, packages, CLIs, workflow tools, docs, and capability stacks.
- **Shows the proof** - grounds the recommendation in source files, docs, tests, licenses, install paths, and trust signals.
- **Compares instead of guessing** - ranks candidates with evidence, risks, setup status, and winner-versus-near-miss reasoning.
- **Explains complex choices** - adds freshness checks, recovery history, and a review of the strongest alternative when the decision deserves deeper research.
- **Works without account-backed tools** - starts with public and local evidence, then uses connected services only when they add something the task needs.
- **Keeps missing research visible** - recovers from failed routes through another source or clearly names what could not be verified.
- **Designs the fallback** - drafts a missing-capability spec and eval cases when no good option exists.

## Quick Start

Start with `@skill-finder` in Codex or `/skill-finder` in Claude Code, then ask for one of these outcomes:

| Ask for | You get |
|---|---|
| `"Find the best skill for this task: ..."` | Ranked recommendation packet |
| `"Compare these connectors/skills for my agent: ..."` | Evidence table and winner |
| `"Research the best capability stack for this task: ..."` | Deep evaluation with evidence ledger and counter-review |
| `"No good skill exists; find the best stack."` | Missing-capability spec and eval cases |

Example prompt:

```text
Find the best skill for this task: inspect a large repo, trace routes, find callers, and recommend safe code-intelligence tooling.
```

## Install

**Start here:** Skill Finder ships as a community plugin for Codex and Claude Code. Add this repository as a marketplace source, then install the `skill-finder` plugin from it.

### <img src="assets/logos/codex-cloud-color.png" alt="" width="24" height="24" align="absmiddle"> Install In Codex

Copy and paste this into your terminal:

```bash
codex plugin marketplace add Nebulazer123/skill-finder
codex plugin add skill-finder@skill-finder
codex plugin list | grep skill-finder
```

Use `@skill-finder` in Codex:

```text
@skill-finder
```

### <img src="assets/logos/claude-code-color.svg" alt="" width="24" height="24" align="absmiddle"> Install In Claude Code

Copy and paste this into your terminal:

```bash
claude plugin marketplace add Nebulazer123/skill-finder
claude plugin install skill-finder@skill-finder
claude plugin list | grep skill-finder
```

Use `/skill-finder` in Claude Code:

```text
/skill-finder
```

## Setup Requirements

Start with `python3`, `git`, and `rg`. Everything else is a task-specific research route. Missing optional routes do not block a run: Skill Finder uses another source family, reports lower coverage, or offers setup when the missing route would materially improve the result.

| Route | Use it when | Setup note |
|---|---|---|
| <img src="assets/logos/agent-skills.svg" alt="" width="22" height="22"> [Agent Skills CLI / skills.sh](https://github.com/vercel-labs/skills) | Finds public skills and install metadata. | `npm install -g skills` |
| <img src="assets/logos/github-invertocat-white.svg" alt="" width="22" height="22"> [GitHub MCP](https://github.com/github/github-mcp-server) | Verifies claims against repository source files. | Remote endpoint: `https://api.githubcopilot.com/mcp/`; configure auth in your host. |
| <img src="assets/logos/deepwiki.png" alt="" width="22" height="22"> [DeepWiki MCP](https://docs.devin.ai/work-with-devin/deepwiki-mcp) | Quickly maps public repositories before source verification. | Remote endpoint: `https://mcp.deepwiki.com/mcp` |
| <img src="assets/logos/context7.png" alt="" width="22" height="22"> [Context7](https://context7.com/docs/clients/codex) | Provides current API, SDK, CLI, framework, and MCP documentation. | Use `@upstash/context7-mcp`; API key recommended. |
| <img src="assets/logos/browserbase.svg" alt="" width="22" height="22"> [Browserbase Browse CLI](https://docs.browserbase.com/integrations/skills/browse-cli) | Adds browser-backed search, fetch, snapshots, and live-page evidence. | `npm install -g browse` and `browse skills install` |
| <img src="assets/logos/codebase-memory.png" alt="" width="22" height="22"> [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | Adds local code graph indexing, symbol lookup, call paths, route tracing, and impact analysis. | `npm install -g codebase-memory-mcp` and `codebase-memory-mcp install` |
| Local essentials | Run the evidence engine, inspect repositories, and search source or documentation. | Install `python3`, `git`, and `rg` with your system package manager. |

### Built-In Public Evidence Sources

These routes ship with the evidence engine. They add public research coverage without another install, account, or API key.

| Source | What it adds | Setup note |
|---|---|---|
| <img src="assets/logos/mcp-registry.svg" alt="" width="22" height="22"> [MCP Registry](https://registry.modelcontextprotocol.io/docs) | Searches public MCP servers and checks current versions, lifecycle status, and repository or package identity. | Built in; public API. |
| <img src="assets/logos/deps-dev.svg" alt="" width="22" height="22"> [deps.dev](https://docs.deps.dev/api/v3/) | Cross-checks package identity, release information, licenses, dependencies, advisories, and provenance. | Built in; public API. |
| <img src="assets/logos/osv.png" alt="" width="22" height="22"> [OSV](https://google.github.io/osv.dev/api/) | Checks known vulnerabilities by package, version, PURL, or commit. | Built in; public API. |
| <img src="assets/logos/ecosystems.ico" alt="" width="22" height="22"> [ecosyste.ms](https://ecosyste.ms/api) | Adds optional public package and repository corroboration. | Built in; public API; preserve source attribution. |

Codex setup commands:

```bash
npm install -g skills
npm install -g browse
npm install -g codebase-memory-mcp
browse skills install
codebase-memory-mcp install
codex mcp add github --url https://api.githubcopilot.com/mcp/
codex mcp add deepwiki --url https://mcp.deepwiki.com/mcp
codex mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

Claude Code setup commands:

```bash
npm install -g skills
npm install -g browse
npm install -g codebase-memory-mcp
browse skills install
codebase-memory-mcp install
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
claude mcp add --transport http deepwiki https://mcp.deepwiki.com/mcp
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

These commands prepare the broadest public route stack, but they are not prerequisites for every evaluation. Node.js, `npm`, and `npx` are needed only for JavaScript-based routes. Connected features may require account configuration in Codex or Claude Code.

The package-backed setup routes are kept in [`package.json`](package.json). It is the source of truth for the supported `skills`, Context7, Browse, and codebase-memory versions.

## Recommended When Useful

These routes are selected only when available, authorized for the task data, and able to add evidence the public/local lane cannot provide.

| Route | Best for |
|---|---|
| <img src="assets/logos/devin-color.svg" alt="" width="22" height="22"> [Devin MCP](https://docs.devin.ai/work-with-devin/devin-mcp) | Hard repository questions, bounded sessions, private-repo context, playbooks, knowledge, schedules, and integrations. |
| <img src="assets/logos/huggingface-color.svg" alt="" width="22" height="22"> [Hugging Face Hub MCP](https://huggingface.co/docs/hub/agents-mcp) and [`hf` CLI](https://huggingface.co/docs/huggingface_hub/guides/cli) | Models, datasets, papers, Spaces, MCP-enabled Spaces, community evals, benchmarks, inference, and training workflows. |
| <img src="assets/logos/composio-symbol.svg" alt="" width="22" height="22"> [Composio CLI / MCP](https://docs.composio.dev/docs/cli) | Connected SaaS actions and app connector discovery. Use the Composio docs for setup and app-specific scopes. |
| <img src="assets/logos/plugin-eval.svg" alt="" width="22" height="22"> [Codex Plugin Eval](https://developers.openai.com/blog/eval-skills) | Repeatable skill scoring and regression checks. |
| [skills.md](https://skills.md/) CLI/MCP | Broad remote skill catalog; load one selected contract at a time and quote premium work before running. |

### Optional skills.md setup

skills.md is a separate remote catalog from skills.sh. Both expose a `skills` command, so use the full path below when you mean skills.md:

```bash
brew install bun
bun install -g @hasna/skills
$HOME/.bun/bin/skills setup agents
$HOME/.bun/bin/skills --version
$HOME/.bun/bin/skills list --json
```

Use `$HOME/.bun/bin/skills auth signup` for private or account-backed work. Inspect with `$HOME/.bun/bin/skills info <name>` and request a quote with `$HOME/.bun/bin/skills quote <name>` before any premium run. For skills.sh discovery, use `npx skills ...`; do not rely on whichever `skills` executable appears first on `PATH`.

## How It Works

The skill instructions live in [skills/skill-finder/SKILL.md](skills/skill-finder/SKILL.md). A standard-library Python engine normalizes candidate identity, plans routes, validates evidence, separates fit from confidence, and writes reproducible Deep Evaluation bundles. Codex or Claude Code still performs the actual tool calls.

A strong result includes:

- Public/local or connected lane and capability status
- Search strategy and Source-Route Scorecard
- Candidate Evidence Table
- Files and docs inspected
- Install or setup command, or `Install command: not verified`
- Winner, near misses, risks, and approval questions

See [examples/recommendation-output-shape.md](examples/recommendation-output-shape.md) for a sample packet.

## Research-Quality Evaluation

Straightforward lookups stay quick. Skill Finder switches to a deeper evaluation for multi-option comparisons, repository or API tracing, costly or complex setup, missing-capability work, and explicit research requests.

The deep path records an **Evidence Ledger** with source type, accessibility, date checked, evidence role, and strength. DeepWiki and Devin are used to find the right questions and source paths; important claims are then verified against source files, tests, official docs, package metadata, or releases.

Before recommending a winner, it includes a **Recovery Log**, a **Counter-Review** of the strongest alternative and weak evidence, unresolved research lines, setup readiness, and a confidence rationale. This keeps research depth visible without slowing down ordinary searches.

A Deep Evaluation can also write `run.json`, `capabilities.json`, `route-attempts.jsonl`, `evidence.jsonl`, `candidates.json`, and `report.md`, so a later run can be compared without relying on chat history.

## Safety Model

Skill Finder treats candidate files as evidence to inspect, not instructions to obey.

When source inspection is useful, Skill Finder stages candidate source in a temporary workspace and records the staging path and cleanup status.

Source review does not authorize setup scripts, credentials, account linking, integrations, publishing, paid actions, file deletion, or persistent/global state changes.

Candidate setup scripts require explicit approval before execution.

## Validation

Run public package checks:

```bash
python3 -m unittest discover -s skills/skill-finder/tests -v
python3 -m unittest discover -s validation -v
```

Run the behavioral evaluation harness:

```bash
python3 -m unittest discover -s evaluation -v
```

Check plugin packaging and npm dependency integrity:

```bash
python3 scripts/sync_plugin_package.py --check
npm ci --ignore-scripts
npm ls --all
```

## Files To Read

```text
skills/skill-finder/SKILL.md             - skill entrypoint and workflow
skills/skill-finder/references/          - search, research-quality evaluation, ranking, readiness, and approval rules
plugins/skill-finder/                    - Codex and Claude Code plugin package
examples/                                - public-safe prompt and output examples
package.json                             - npm setup metadata
validation/                              - public package checks
evaluation/                              - public, recovery, private-routing, and adversarial cases
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).

[license-shield]: https://img.shields.io/badge/License-MIT-16A34A.svg
[license-url]: LICENSE
[version-shield]: https://img.shields.io/badge/version-1.3.0-64748B.svg
[version-url]: CHANGELOG.md
[skills-shield]: https://img.shields.io/badge/Agent%20Skills-compatible-DA7857.svg
[skills-url]: https://agentskills.io
