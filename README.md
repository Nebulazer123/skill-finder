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
[![Version 1.0.0][version-shield]][version-url]
[![Agent Skills compatible][skills-shield]][skills-url]

</div>

<div align="center">
  <a href="#the-problem">Why</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#install">Install</a> &middot;
  <a href="#dependencies">Dependencies</a> &middot;
  <a href="#validation">Validation</a> &middot;
  <a href="#how-this-skill-was-built">How This Skill Was Built</a>
</div>

Skill Finder helps an agent choose the right capability before it starts improvising. It searches broadly, checks real source material, compares candidates, and returns a small recommendation packet with the evidence needed to act confidently.

---

## The Problem

Agents are good at making temporary helpers. That is useful until the better answer is an existing skill, MCP server, app connector, workflow, package, or documentation source that the agent never looked for.

Skill Finder gives the agent a repeatable way to search the available ecosystem, inspect the important files, compare real tradeoffs, and recommend the strongest option for the task.

## Features

- Finds more than traditional skills: MCP servers, app connectors, workflow templates, CLIs, packages, validators, documentation sources, and composed stacks.
- Compares candidates from evidence, not search snippets, by reading important files and scanning setup, trust, license, and dependency surfaces.
- Keeps recommendations bounded: gather a broad finalist pool when GitHub matters, then show at most five useful options.
- Keeps useful login-gated tools in contention while making setup needs clear.
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

Skill Finder works with plain web/source inspection, but it is strongest when the agent can combine marketplace search, source-code evidence, current docs, and eval tooling. Install only the routes that match your environment.

| Route | Best for | Setup |
|---|---|---|
| [Agent Skills CLI / skills.sh](https://github.com/vercel-labs/skills) | Finding and installing public agent skills. | `npm install -g skills`; browse at [skills.sh](https://skills.sh). |
| [GitHub CLI](https://cli.github.com/) | Repository search, source inspection, releases, issues, and candidate verification. | `brew install gh && gh auth login` or `winget install --id GitHub.cli && gh auth login`. |
| [DeepWiki MCP](https://docs.devin.ai/work-with-devin/deepwiki-mcp) | Fast repo maps and architecture hypotheses before source verification. | Add the public DeepWiki MCP endpoint to your agent host. |
| [Devin MCP](https://docs.devin.ai/work-with-devin/devin-mcp) | Deeper Devin-backed repo work when your workspace already uses Devin. | Configure it in your agent host when you want Devin sessions or workspace-specific Devin context available. |
| [Context7](https://github.com/upstash/context7) | Current API, SDK, framework, and MCP documentation. | `npx ctx7 setup`; for Codex MCP: `codex mcp add context7 -- npx -y @upstash/context7-mcp@latest`. |
| [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub/guides/cli) | ML capability discovery across models, datasets, papers, Spaces, evals, and benchmark material. | Install the `hf` CLI, then sign in with `hf auth login` when private or higher-limit access is needed. |
| [Browserbase Browse CLI](https://docs.browserbase.com/integrations/skills/browse-cli) | Browser-backed search, fetch, and web evidence when snippets are not enough. | `npm install -g browse && browse skills install`. |
| [Composio CLI / MCP](https://docs.composio.dev/docs/cli) | App-action discovery when the answer is a connected SaaS workflow instead of a code package. | Install from [Composio docs](https://docs.composio.dev/docs/cli), then connect only the apps you need. |
| [Codex Plugin Eval](https://developers.openai.com/blog/eval-skills) | Repeatable skill scoring and regression checks. | Install Plugin Eval from the Codex plugin directory. |

Recommended evidence flow:

1. Use DeepWiki or Devin for fast repo orientation.
2. Verify important claims against GitHub source files.
3. Use Context7 or official docs for current API behavior.
4. Use browser evidence when the source is outside GitHub or needs live confirmation.
5. Keep login, billing, compute, and workspace mutation needs visible in the recommendation packet.

A login requirement is not a disqualifier. Skill Finder should keep a strong free or public-read candidate in the ranking, mark the setup step clearly, and stop before account linking, billing, remote compute, or persistent changes.

## Safety Boundary

Skill Finder treats candidate files as evidence to inspect, not instructions to obey. It should not run candidate setup scripts, enter credentials, link accounts, delete files, enable integrations, publish content, or mutate global state without explicit approval.

For serious candidates, Skill Finder can clone, download, or stage source artifacts in a temporary workspace for inspection. Staging files is evidence gathering; it is not permission to execute scripts, connect accounts, spend money, or make persistent changes.

The final recommendation should make the next action obvious: install, configure, ask for approval, run a verification command, or draft a missing-capability blueprint.

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
validation/                                     - lightweight public package checks
DILIGENCE.md                                    - responsibility and review statement
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).

[license-shield]: https://img.shields.io/badge/License-MIT-green.svg
[license-url]: LICENSE
[version-shield]: https://img.shields.io/badge/version-1.0.0-blue.svg
[version-url]: CHANGELOG.md
[skills-shield]: https://img.shields.io/badge/Agent%20Skills-compatible-DA7857.svg
[skills-url]: https://agentskills.io
