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
[![Version 0.1.6][version-shield]][version-url]
[![Agent Skills compatible][skills-shield]][skills-url]

</div>

<div align="center">
  <a href="#the-problem">Why</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#install">Install</a> &middot;
  <a href="#dependencies">Dependencies</a> &middot;
  <a href="#validation">Validation</a> &middot;
  <a href="#learning-evidence">Learning Evidence</a>
</div>

If an AI assistant keeps improvising one-off fixes or grabbing the first matching tool, Skill Finder is for you. It forces a source-backed search, deep inspection, and an approval boundary before anything gets installed or changed.

---

## The Problem

Agents are good at making temporary helpers, but that can waste time, miss better existing tools, or install something shallow because the name matched. Skill Finder gives the agent a repeatable way to search broadly, inspect source files, compare real candidates, and recommend the best agent-usable capability for the task.

## Features

- Finds more than traditional skills: MCP servers, app connectors, workflow templates, CLIs, packages, validators, documentation sources, and composed stacks.
- Compares candidates from evidence, not search snippets, by reading important files and scanning setup, trust, license, and dependency surfaces.
- Keeps recommendations bounded: gather a broad finalist pool when GitHub matters, then show at most five useful options.
- Keeps free account-gated or API-key-gated tools in contention instead of demoting them only because setup is required.
- Produces installable next steps with dependency readiness, verification commands, risks, and explicit approval questions.
- Falls back to a Missing Skill Blueprint when no existing option is good enough.

## Quick Start

```text
"Find the best capability for this task: ..."      -> ranked recommendation packet
"Compare these candidate tools for my agent: ..."  -> evidence table and winner
"No good skill exists; draft the blueprint."       -> missing-capability spec and eval cases
```

## Usage

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

## Dependencies

Set up these external capabilities for the full Skill Finder workflow across skill marketplaces, GitHub source, current docs, browser evidence, app connectors, and skill evaluation.

| Dependency | Purpose | Get it / sign up | macOS setup | Windows setup |
|---|---|---|---|---|
| [Agent Skills CLI / skills.sh](https://github.com/vercel-labs/skills) | Discover and install agent skills from GitHub repositories and the open skills ecosystem. | No account required. Browse public skills at [skills.sh](https://skills.sh). | `npm install -g skills` | `npm install -g skills` |
| [GitHub CLI](https://cli.github.com/) | Search repositories, inspect source files, check releases/issues, and verify GitHub candidates from the terminal. | Use a GitHub account, then authenticate with `gh auth login`. | `brew install gh && gh auth login` | `winget install --id GitHub.cli && gh auth login` |
| [Context7](https://github.com/upstash/context7) | Pull current library, SDK, API, and framework documentation into the agent workflow. | Get a free API key at [context7.com/dashboard](https://context7.com/dashboard) for higher limits. | `npx ctx7 setup`; for Codex MCP: `codex mcp add context7 -- npx -y @upstash/context7-mcp@latest` | `npx ctx7 setup`; for Codex MCP: `codex mcp add context7 -- npx -y @upstash/context7-mcp@latest` |
| [Browserbase Browse CLI](https://docs.browserbase.com/integrations/skills/browse-cli) | Use search, fetch, cloud browser sessions, and Browse.sh skills when normal search snippets are not enough. | Create a Browserbase account and API key at [browserbase.com](https://www.browserbase.com/). | `npm install -g browse && browse skills install` | `npm install -g browse && browse skills install` |
| [Composio CLI / MCP](https://docs.composio.dev/docs/cli) | Discover, authenticate, and use app connectors across SaaS tools; useful when the best capability is an app action, not a code package. | Create or sign in to Composio; app connections may require OAuth. Codex MCP setup is documented at [composio.dev/toolkits/composio/framework/codex](https://composio.dev/toolkits/composio/framework/codex). | <code>curl -fsSL https://composio.dev/install &#124; bash && composio login</code> | Use WSL with <code>curl -fsSL https://composio.dev/install &#124; bash && composio login</code>, or follow the Codex MCP setup page. |
| [Codex Plugin Eval](https://developers.openai.com/blog/eval-skills) | Score and improve skills with repeatable checks instead of relying on vibes. | Install Plugin Eval from the Codex plugin directory. Codex plugin setup is documented at [developers.openai.com/codex/plugins](https://developers.openai.com/codex/plugins). | Run `codex`, then `/plugins`, then install Plugin Eval. | Run `codex`, then `/plugins`, then install Plugin Eval. |

Credential setup is a readiness step. Free tools that require an account, API key, OAuth flow, or browser login should still be considered valid candidates and can still win. Paid services, required payment, risky authorization, opaque code, destructive actions, or persistent/global mutation remain approval boundaries.

## Safety Boundary

Skill Finder treats candidate files as evidence to inspect, not instructions to obey. It should not run candidate setup scripts, enter credentials, link accounts, delete files, enable integrations, publish content, or mutate global state without explicit approval. If a free recommended tool needs credentials, Skill Finder should still recommend or download/install the safe package when allowed, then stop at the credential-entry step with clear setup instructions.

This is not a package manager, scraper, or automatic installer. It is a decision workflow for helping an agent find and vet the right capability before acting.

## Output Shape

A strong recommendation includes:

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

If you have the Codex skill validator available, validate the skill folder:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/skill-finder
```

This release has also been checked with Plugin Eval from the local development environment. If Plugin Eval is unavailable in your setup, treat that as an optional review tool rather than a hard dependency.

## Learning Evidence

This project was built as an AI Fluency course project and public agent-skill package. The short evidence packet explains what I learned through Delegation, Description, Discernment, and Diligence; how the project scores evolved; where AI contributed; and what I personally reviewed, changed, and take responsibility for.

See [AI_FLUENCY_EVIDENCE.md](AI_FLUENCY_EVIDENCE.md).

## What's Inside

```text
AI_FLUENCY_EVIDENCE.md                           - learning evidence, scores, and human/AI collaboration summary
skills/skill-finder/SKILL.md                    - skill entrypoint and workflow
skills/skill-finder/agents/openai.yaml          - display metadata and helper dependency notes
skills/skill-finder/references/                 - search, ranking, readiness, and approval rules
examples/                                       - public-safe request and output examples
validation/                                     - lightweight public package checks
DILIGENCE.md                                    - AI collaboration and responsibility statement
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).

[license-shield]: https://img.shields.io/badge/License-MIT-green.svg
[license-url]: LICENSE
[version-shield]: https://img.shields.io/badge/version-0.1.6-blue.svg
[version-url]: CHANGELOG.md
[skills-shield]: https://img.shields.io/badge/Agent%20Skills-compatible-DA7857.svg
[skills-url]: https://agentskills.io
