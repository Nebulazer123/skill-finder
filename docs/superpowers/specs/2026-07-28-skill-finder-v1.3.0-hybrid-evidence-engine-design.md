# Skill Finder v1.3.0 Hybrid Evidence Engine

## Goal

Skill Finder should complete useful public research without requiring accounts
while using connected services when they materially improve the result. Missing
optional routes reduce evidence coverage or trigger recovery; they do not block
unrelated work.

## Architecture

The skill remains responsible for research judgment and host tool calls. A
Python standard-library engine adds canonical identity, route planning,
evidence validation, scoring, and reproducible output.

The public lane uses local source, the MCP Registry, deps.dev, OSV, and optional
ecosyste.ms or OpenSSF enrichment. The connected lane represents host-managed
tools such as Devin, Sourcegraph, authenticated GitHub, Browserbase, Firecrawl,
Hugging Face, Composio, and premium skills.md runs.

Host-managed tools are not invoked from Python. The engine emits structured call
intents and imports returned evidence into the same ledger used by public HTTP
adapters.

## Evidence Model

Candidates receive canonical identities before deduplication:

- Package candidates use Package URLs.
- Repositories use normalized host, owner, repository, and immutable revision.
- MCP servers use the registry server name and version.
- Skills use provider, source, skill name, and version.
- Connectors use provider and stable connector identifier.

Evidence records keep the exact claim, materiality, source, retrieval time,
source role, route, strength, verification state, and optional artifact digest.
Route attempts preserve failures, cancellations, and recovery paths.

Fit score, evidence coverage, and confidence remain separate. Generated
summaries are leads and cannot independently verify material winner claims.

## Evidence Floors

Quick Evaluation requires one credible discovery source, one primary
verification source, and verified setup syntax when an action is recommended.

Deep Evaluation requires two source families, primary verification for every
material winner claim, freshness checks for current claims, recovery after
material route failures, a credible alternative winner, unresolved research
lines, and a confidence rationale.

Repository-heavy work also requires direct source inspection through GitHub, a
staged clone, codebase-memory, or Sourcegraph.

## Route Policy

The engine classifies the task, reads a capability snapshot, selects the
smallest diverse route portfolio that can meet the evidence floor, and stops
when further research cannot change the decision. A failed material route
recovers through a different source family.

Private data is only routed through local tools or services already authorized
for that source. Secrets are never placed in requests, evidence records, or
reports.

## Ranking

The default fit score weights task fit at 30, capability completeness at 15,
tests and verification at 15, freshness at 10, trust at 10, host compatibility
at 10, privacy and cost alignment at 5, and adoption at 5.

High confidence requires current primary verification, independent
corroboration, and no unresolved material contradiction. Popularity,
OpenSSF aggregate scores, or generated summaries cannot determine the winner
alone.

## Outputs

A Deep Evaluation produces `run.json`, `capabilities.json`,
`route-attempts.jsonl`, `evidence.jsonl`, `candidates.json`, and `report.md`.
The run manifest includes schema and engine versions, task digest, selected
routes, checked dates, and confidence.

## Release Gate

The public benchmark completion rate must reach 95 percent. Material-claim
verification, optional-route nonblocking behavior, recovery disclosure, install
command verification, prompt-injection resistance, package synchronization,
and public-safety scans must all pass before v1.3.0 is tagged.
