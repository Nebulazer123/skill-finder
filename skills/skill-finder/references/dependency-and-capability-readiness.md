# Dependency And Capability Readiness

Capability candidates include skills, plugins, MCP servers, app connectors, workflows, CLIs/tools, binaries, packages, validators, docs sources, bundles, and Missing Skill Blueprints.

Inspect README, `SKILL.md`, references, scripts, manifests, setup docs, lockfiles, Dockerfiles, MCP config, release notes, workflow JSON, and tests. Use ripgrep for dependency, setup, package-manager, secret, auth, admin, and global-state terms.

Prefer source evidence from skills.sh/Skills CLI, GitHub/source repos, package docs, app/workflow catalogs, MCP registries, `find-docs`, Context7, and official docs.

Verify only helpers needed for the run: `python3`, `git`/`gh`, `rg`, `skills`/`npx skills`, `node`/`npm`/`npx`, Plugin Eval, or `skill-installer`. Record unavailable helpers and use source URLs, official docs, or manual fallback; do not assume private global setup.

Helper prep and candidate setup are different. Expected helper preparation is allowed only when policy or the user allows it. Do not run a discovered repo's setup scripts or package installs unless approval/sandbox scope is explicit.

Dependency readiness ledger: required, optional, installed, missing, prepared, pending admin/secret/interactive setup, verification command, install command source, notes. Hosted/enterprise adds account/OAuth/SSO/private-code indexing/payment/data-retention/admin approval. Use `unknown` unless proven; `none` only with evidence.

Credential readiness passes only when the needed value is present and non-empty in the command environment or authenticated config, then verified by a harmless official command. Do not treat `launchctl getenv`, `printenv`, keychain lookup, or CLI auth exit code as proof by itself. Check status or value length without printing secrets. If credentials exist for the user but not the agent shell, classify as `credential available to user / not exported to agent` and give the exact non-secret setup command.

Credential requirement is not a disqualifier. If a candidate is free but needs an account, API key, OAuth flow, or browser login, keep it eligible and mark the setup step. Download or install the safe package when allowed; stop only at the point of entering secrets, linking accounts, granting scopes, or accepting paid/risky terms.

Browserbase: local `browse` needs no credential; cloud search/fetch/sessions require non-empty `BROWSERBASE_API_KEY` and harmless verification such as `browse cloud projects list`. If credentials live outside the agent shell, verify length without printing secrets and use command-scoped exports. If only local mode works, rank Browserbase as local browser inspection, not verified cloud search/fetch.

Quote source install commands; if missing, write `Install command: not verified`. Never guess.

Sandbox install/test/cleanup only when safe and approved. Prefer temp dirs, fixtures, dry runs, local-only, and reversible actions. No real data, credentials, paid services, production systems, browser sessions, or persistent/global state unless approved. If OAuth/API key/account linking/browser login/payment/MCP auth/global mutation is needed, stop with setup link, reason, partial evidence, and resume point.
