# Dependency And Capability Readiness

Capability candidate: skill, plugin, MCP server, app/connector, workflow/automation template, CLI/tool, binary, package/library, validator/test runner, docs source, Missing Skill Blueprint.

Inspect README, `SKILL.md`, references, scripts, manifests, install/setup docs, lockfiles, Dockerfiles, MCP config, CLI docs, release notes, workflow JSON, tests. Use ripgrep for dependency/setup/package-manager/secret/auth/admin/global terms. Blast-radius: hosted/private-code indexing, OAuth/account/payment, telemetry, global MCP config, OpenAPI/generated-client commands, task graphs, cache/index, CI.

Prefer source evidence: skills.sh, `npx skills`, GitHub CLI skills, package docs, Composio catalogs, n8n workflow JSON, MCP registries, `find-docs`, Context7, canonical docs.

Baseline helper readiness: verify `python3` for validation/evidence scripts, `git`/`gh` for repository inspection, `rg` for local file scans, `skills` or `npx skills` for skills.sh marketplace discovery, `node`/`npm`/`npx` for package-tool discovery, and Plugin Eval or `skill-installer` only when the run needs evaluation or install planning. Record unavailable helpers and fall back to source URLs, official docs, or manual instructions rather than assuming they exist from global agent guidance.

Helper setup boundary: installing/verifying expected helper tools is dependency preparation only when the active user/session/project policy allows safe helper setup or the user explicitly approves it. Candidate package-manager activity is different: do not run a discovered repo's setup/install scripts or package installs unless approval/sandbox scope is explicit.

Dependency readiness ledger: required, optional, installed, missing, prepared, pending admin/secret/interactive setup, verification command, install command source, notes. Hosted/enterprise adds account/OAuth/SSO/private-code indexing/payment/data-retention/admin approval. Guardrails need OpenAPI spec path, generated-client command, old/new spec, CI baseline. Use `unknown` unless proven; `none` only with evidence.

Quote source install commands; if missing, write `Install command: not verified`. Never guess.

Examples: FFmpeg, Playwright, GitHub CLI, Skills CLI (`npx skills find`, `npx skills add`, `npx skills check`, `npx skills update`), ripgrep, plugin-eval, MCP servers, Sourcegraph MCP, codebase-memory-mcp, Serena, CodeGraph, oasdiff, Nx affected, Turborepo filters, Composio/app connectors, n8n workflows.

Sandbox install/test/cleanup only when safe and approved. Prefer temp dirs, fixtures, dry runs, local-only, reversible. No real data, credentials, paid services, production systems, browser sessions, or persistent/global state unless approved. If OAuth/API key/account linking/browser login/payment/MCP auth/global mutation is needed, stop with setup link, reason, partial evidence, resume point.
