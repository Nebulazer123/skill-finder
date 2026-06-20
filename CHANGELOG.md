# Changelog

## 1.0.3 - 2026-06-20

- Made Agent Skills, GitHub MCP, DeepWiki MCP, Context7, Browserbase Browse CLI, and local inspection basics required setup for real Skill Finder runs.
- Added a Required Setup Block behavior so the skill pauses and asks before installing or configuring missing required routes.
- Marked Devin, Hugging Face, codebase-memory-mcp, Composio, and Plugin Eval as recommended power routes when they would materially improve a task.
- Added `package.json` for graphable npm setup dependencies: `skills`, `@upstash/context7-mcp`, and `browse`.
- Refocused the README for first-time reviewers with clearer problem framing, setup requirements, proof points, and validation steps.
- Changed the README install blocks to copy-paste terminal commands for both Codex and Claude Code.
- Removed the README pin-release section to keep first-time install guidance simple.
- Expanded README setup guidance for GitHub MCP, DeepWiki, Context7, Browserbase, and local helpers.
- Removed README-only dependency graph and proof-point sections to keep the page focused on use.
- Added logo-marked install buttons, a clearer install lead, present-tense safety wording, and npm setup metadata wording.
- Replaced the top install badge row with supplied white Codex and Claude Code wordmark buttons, while keeping Agent Skills and Hugging Face logos only in their relevant setup sections.
- Added route-specific GitHub, DeepWiki, Context7, Browserbase, Devin, and Composio logos only in their matching setup/recommendation rows.
- Added the Plugin Eval logo and normalized all setup/recommendation row logos to the same rendered size.
- Added npm Dependabot tracking and removed an internal implementation-plan document from the public package.

## 1.0.2 - 2026-06-20

- Changed the Codex plugin install command to use the repository's default branch instead of pinning `--ref v1.0.1`.
- Refreshed the README and Codex plugin prompt examples around skills, connectors, and best-stack fallback.
- Added GitHub Actions Dependabot tracking for the repository's real graphable dependencies.

## 1.0.1 - 2026-06-20

- Added Codex and Claude Code plugin packaging while keeping `skills/skill-finder/` as the canonical skill source.
- Added repo marketplace files for Codex and Claude plugin installation.
- Added a deterministic sync/check script and validation coverage so packaged plugin skills cannot drift from the canonical skill.

## 1.0.0 - 2026-06-20

- Promoted the public package to v1 after merging the open Devin branches and clearing open PRs/issues.
- Removed course-specific README framing so the front door reads like a standalone public skill package.
- Kept the evidence packet linked with neutral project-history wording instead of personal or course-context language.
- Renamed the evidence link and artifact to "How This Skill Was Built" for cleaner public framing.
- Reworked the README dependency and safety sections into public-facing guidance instead of internal routing notes.

## 0.1.9 - 2026-06-20

- Merged Devin branch cleanup for stricter public-package validation and clearer test failure messages.
- Added GitHub Actions validation so the public package test suite runs on pushes and pull requests.
- Added secret-file `.gitignore` coverage and stronger public-package scans for private paths and credential-shaped strings.
- Added broad validation coverage across README, references, examples, metadata, license, and skill workflow docs.
- Updated stale branch tests to match the current DeepWiki, Devin, Context7, and setup-readiness wording.

## 0.1.8 - 2026-06-19

- Added DeepWiki and Ask Devin as a stronger repo-intelligence lane for public repo maps, hard source questions, and second-pass uncertainty checks.
- Added Context7 recovery: retry alternate names, docs-host IDs, and CLI/MCP routes before calling docs unavailable.
- Added thin-doc handling so Context7 can count as partial evidence while source files and official docs carry the detailed trace.
- Added clean-room repo eval evidence from harder repos, including `eunomia-bpf/bpftime`.
- Refreshed public README wording for credentialed free tools so setup is a readiness step, not a reason to discard a useful candidate.

## 0.1.7 - 2026-06-16

- Added Hugging Face as a source/dependency route for ML models, datasets, papers, Spaces, evals, benchmark material, and hosted workflows that require explicit setup review.
- Added a safe temporary staging rule so strong candidates can be downloaded, cloned, fetched, or staged for direct inspection when reasonable, while execution, credentials, paid compute, and persistent mutation remain approval boundaries.
- Added public validation coverage for Hugging Face routing and staging-vs-execution boundaries.

## 0.1.6 - 2026-06-16

- Added a public Dependencies section with the full external source-route stack: Agent Skills CLI, GitHub CLI, Context7, Browserbase Browse CLI, Composio CLI/MCP, and Codex Plugin Eval.
- Added purpose, setup/sign-up links, and macOS/Windows setup guidance for each external capability.
- Moved free credentialed-tool guidance below the dependency table so account/API/OAuth setup is treated as readiness work, not a disqualifier.

## 0.1.5 - 2026-06-15

- Added the verified Agent Skills CLI install path: `npx skills add Nebulazer123/skill-finder --skill skill-finder`.
- Documented that the package is discoverable with `skills add Nebulazer123/skill-finder --list` and usable with `skills use Nebulazer123/skill-finder@skill-finder`.

## 0.1.4 - 2026-06-15

- Added the final public README logo image and removed unused placeholder logo assets.
- Added `HOW_THIS_SKILL_WAS_BUILT.md` so reviewers can scan the project history, evidence trail, scoring changes, and responsibility notes.
- Linked the learning evidence from the README and diligence statement.
- Added public contribution guidance for stale source routes, broken install commands, risky candidate behavior, unclear approval boundaries, and stronger eval scenarios.

## 0.1.3 - 2026-06-15

- Clarified that free tools requiring accounts, API keys, OAuth, or browser login remain valid candidates.
- Changed credential requirements from a ranking demotion to a readiness/setup step.
- Preserved approval boundaries for entering secrets, linking accounts, paid services, risky scripts, and persistent/global mutation.

## 0.1.2 - 2026-06-15

- Reworked the README into a public-facing GitHub front door for first-time readers.
- Added logo assets, contributing guidance, security policy, code of conduct, issue templates, PR template, and repository metadata draft.
- Added universal Browserbase routing, credential-readiness, Skills CLI mismatch, and intent-fit guardrails to the public skill package.
- Removed generated validation cache files from the public package.

## 0.1.1 - 2026-06-15

- Added portable helper-tool readiness guidance for the Skills CLI, GitHub CLI, ripgrep, Python, and package-tool discovery.
- Clarified that expected helper setup and candidate package-manager activity have different approval boundaries.
- Clarified that final recommendations should be usable by an AI agent in the target host.
- Made bundle recommendations default to one composed skill artifact unless the user explicitly asks for separate sibling installs.
- Removed portfolio-specific/design-biased routing from the public skill package.

## 0.1.0 - 2026-06-15

- Initial public release of Skill Finder.
- Added bounded source-route search, 20+ GitHub finalist guidance, max-five visible recommendations, deep file inspection, dependency readiness, approval gates, and eval-loop pressure-test guidance.
- Added public examples, validation checks, and a diligence statement.
