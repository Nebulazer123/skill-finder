# Dependency And Capability Readiness

Use when a finalist needs tools, packages, APIs, MCP servers, config, auth, or verification.

## Capability Candidate

A capability candidate may be a skill, plugin, MCP server, app/connector, workflow/automation template, CLI/tool, binary, package/library, validator/test runner, docs source, or Missing Skill Blueprint. State type and bundle pieces.

## Detection

Inspect README, `SKILL.md`, references, scripts, manifests, install/setup docs, lockfiles, Dockerfiles, MCP config, CLI docs, release notes, workflow JSON, tests. Use ripgrep for dependency/setup terms, package managers, FFmpeg/ripgrep/rg/gh/node/python/semgrep, and secret/auth/admin/global terms. Read key setup files; scan lockfiles, vendored/generated folders, large references.

Prefer source-specific evidence: GitHub CLI skills, `npx skills`, package docs, Composio/app connector catalogs, n8n workflow JSON, MCP registries, `find-docs`, Context7, canonical docs for current library, CLI, API, framework, cloud, app, workflow, or MCP behavior.

## Readiness

Quote install commands from candidate source, official docs, package manager output, or vendor release page. If missing, write `Install command: not verified` and name next source/file. Never treat a guessed command as evidence.

Do not run installs, browser binaries, global config changes, candidate scripts, MCP setup, app auth, workflow imports, or credential flows without user approval.

Every finalist needs dependency readiness: required, optional, installed, missing, prepared, pending admin/secret/interactive setup, verification command, install command source, notes. Use `unknown` unless proven; use `none` only with evidence.

Examples: FFmpeg, Playwright, GitHub CLI (`gh skill search/preview/install/list/update`), ripgrep (`rg --version`), plugin-eval (`plugin-eval analyze <skill-path> --format markdown`), MCP servers, Composio/app connectors, n8n workflows.
