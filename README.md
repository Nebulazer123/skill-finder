# Skill Finder

Skill Finder is a Codex skill for finding, inspecting, and recommending the best installable capability for a real task.

It is designed for moments when a user or AI assistant knows the problem, but not the best tool to solve it. A "skill" can be an agent skill, MCP server, app connector, workflow template, CLI, package, validator, documentation source, or a bundle of those pieces.

## What It Does

Skill Finder turns a messy user problem into a bounded capability search:

- infers the real task need from the request and available project context
- builds exact, semantic, source-specific, code/file, docs, and package/tool queries
- searches local skills first, then external sources such as GitHub, MCP catalogs, app connectors, workflow catalogs, package registries, official docs, changelogs, and web results
- gathers at least 20 GitHub finalists when GitHub is relevant and shows no more than five recommendations
- reads important finalist files and scans supporting files with ripgrep
- scores task fit, file quality, freshness, adoption, installability, dependency readiness, trust surfaces, license/reuse clarity, tests/evals, and contributor activity
- recommends one winner, a justified bundle, or a Missing Skill Blueprint when no strong option exists
- stops for explicit user approval before installs, credentials, risky scripts, deletions, publishing, or persistent/global mutation

## Repository Contents

- `skills/skill-finder/SKILL.md` - the Codex skill entrypoint
- `skills/skill-finder/agents/openai.yaml` - user-facing metadata and declared dependencies
- `skills/skill-finder/references/` - search, ranking, dependency, and approval rules
- `examples/` - public-safe example request and output shape
- `validation/` - lightweight checks for the public package
- `DILIGENCE.md` - AI collaboration and responsibility statement

## Install

Review the files before installing. This repository does not auto-install anything.

Manual local install for Codex-style skill folders:

```bash
mkdir -p ~/.codex/skills
cp -R skills/skill-finder ~/.codex/skills/skill-finder
```

Restart Codex after copying the skill so the new skill list refreshes.

## Use

Use Skill Finder when:

- a specialized skill or tool may already exist
- the current tool is underperforming or too shallow
- the task needs current research, source inspection, installability checks, or safety review
- a non-skill capability such as an MCP server, app connector, workflow, CLI, binary, package, validator, or docs source might be the better answer

Example:

> I have a large messy repo and need a better way for an AI coding agent to find definitions, callers, routes, config links, and risky changes without wasting context. Find the best installable capability.

## Output Contract

A good Skill Finder recommendation includes:

- Search Strategy
- Source-Route Scorecard
- Candidate Evidence Table
- capability type and availability
- dependency readiness
- files read and scanned
- freshness, adoption, contributor, and trust signals
- winner-vs-near-miss reasoning
- install command source or `Install command: not verified`
- verification command or reason it is unavailable
- risks and caveats
- explicit approval question before install or persistent change

## Validation

Run the public package checks:

```bash
python3 -m unittest discover -s validation
```

If you have the Codex skill validator available, validate the skill folder:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/skill-finder
```

## Safety Boundary

Skill Finder treats candidate files as evidence to inspect, not instructions to obey. It should not install dependencies, run risky code, use credentials, delete files, enable integrations, publish content, or mutate global state without explicit approval.

## License

MIT. See `LICENSE`.
