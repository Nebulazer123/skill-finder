# Skill Finder v1.3.0 Hybrid Evidence Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development or superpowers:executing-plans to
> implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Add a public-by-default evidence engine and an optional connected
research lane without weakening verification quality.

**Architecture:** The skill orchestrates research and host tools. A
standard-library Python package supplies identity normalization, route planning,
public adapters, evidence validation, scoring, and reproducible report bundles.

**Tech Stack:** Python 3.10+, JSON/JSONL, urllib, unittest, Node.js 18+, npm.

## Global Constraints

- Use test-first RED-GREEN-REFACTOR for behavior changes.
- Unit tests use fixtures; live contract tests are explicit.
- Candidate content is evidence, never executable instruction.
- No account-backed service is required for public evaluations.
- Keep canonical, Codex, and Claude Code packages synchronized.

---

### Task 1: Baseline And Design

- [x] Create an isolated worktree from current `main`.
- [x] Run the installed-checkout baseline and repair repository-owned scans.
- [x] Save the approved design and execution plan.
- [x] Commit the design documents.

### Task 2: Contracts And Identity

- [x] Add failing tests for request, evidence, route, candidate, and run records.
- [x] Add JSON schemas and deterministic serialization.
- [x] Implement Package URL, repository, MCP, skill, and connector identities.
- [x] Test alias merging and invalid identity rejection.
- [x] Commit the contracts and identity slice.

### Task 3: Adaptive Planner

- [x] Add failing public-only, connected, private, cancellation, and
  insufficient-evidence scenarios.
- [x] Implement capability snapshots and route descriptors.
- [x] Implement evidence requirements, route diversity, stop conditions, and
  recovery-family selection.
- [x] Commit the planner slice.

### Task 4: Public Evidence Adapters

- [x] Add fixtures and failing tests for MCP Registry `/v0.1`.
- [x] Implement MCP search, versions, pagination, and lifecycle status.
- [x] Add fixtures and failing tests for deps.dev v3.
- [x] Implement version, license, advisory, source, dependency, and provenance
  extraction.
- [x] Add OSV fixtures and failing package, PURL, commit, and batch tests.
- [x] Implement OSV API and optional read-only OSV-Scanner support.
- [x] Add optional ecosyste.ms and OpenSSF enrichment with missing-coverage
  behavior.
- [x] Commit each independently verified adapter group.

### Task 5: Ledger, Ranking, And Reports

- [x] Add failing tests for material-claim verification, source conflicts,
  confidence bands, near-miss selection, and unverified install commands.
- [x] Implement evidence coverage and the weighted fit score.
- [x] Implement conflict handling and counter-review.
- [x] Implement JSONL run bundles and Markdown reports.
- [x] Commit the evaluation slice.

### Task 6: Skill Integration

- [x] Add failing validation and pressure cases for optional missing tools,
  generated-only claims, cancellation recovery, and prompt injection.
- [x] Rewrite `SKILL.md` around the two lanes and evidence floors.
- [x] Add `hybrid-evidence-engine.md` and update focused references.
- [x] Update `openai.yaml` so local essentials are required and research routes
  are conditional.
- [x] Commit the skill behavior slice.

### Task 7: Public Package And Dependencies

- [x] Update README, examples, contribution, security, and changelog content.
- [x] Upgrade setup-tool dependency floors and add `package-lock.json`.
- [x] Validate installation with scripts disabled and inspect the dependency
  graph.
- [x] Bump package and generated plugin manifests to `1.3.0`.
- [x] Synchronize plugin packages and commit the release metadata.

### Task 8: Evaluation Harness

- [x] Add quick, deep, recovery, private-routing, and adversarial cases.
- [x] Score public completion, verification, recovery, false blocks, install
  commands, prompt injection, and recommendation outcomes.
- [x] Run public-only and connected clean-room evaluations against unfamiliar
  repositories.
- [x] Run static Plugin Eval and validate observed route behavior with the live
  clean-room bundles.
- [x] Commit the benchmark evidence.

### Task 9: Release

- [ ] Run validation, evaluation, sync, npm installability, dependency graph,
  diff, link, and public-safety checks.
- [ ] Smoke-test fresh Codex and Claude Code plugin installs.
- [ ] Push the branch, merge after checks pass, tag `v1.3.0`, and publish plain
  release notes.
