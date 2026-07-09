# Example Output Shape

```markdown
# Skill Finder Recommendation

Use the Quick Evaluation shape for simple lookups. Add the Deep Evaluation sections when the task compares several serious options, traces a repository or API, has costly or complex setup, has no clear existing capability, or explicitly asks for research.

## Problem

Summarize the capability needed and the task context.

## Search Strategy

List exact, semantic, source-specific, code/file, docs, package, MCP/app/workflow, and fallback web searches.

## Source-Route Scorecard

| Route | Why chosen | Status | Evidence count | Strength | Notes |
| --- | --- | --- | ---: | --- | --- |

## Candidate Evidence Table

| Candidate | Type | Availability | Files read | Freshness | Adoption | Trust surfaces | Score | Confidence |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |

## Recommendation

Name the winner, explain why it beats the closest alternatives, and state what evidence could change the ranking.

## Approval Needed

Ask before install, credentials, risky scripts, integration setup, deletion, publishing, or persistent/global mutation.
```

## Deep Evaluation Addendum

```markdown
## Evaluation Depth

Deep Evaluation: comparing three repository-intelligence routes before changing shared developer tooling.

## Evidence Ledger

| Claim or question | Source URL or artifact | Source type | Accessibility | Date checked | Evidence role | Strength | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| The route exposes a repository map | Official MCP docs | official | public | 2026-07-09 | verification evidence | high | confirmed |
| Likely source paths for the request flow | DeepWiki answer | docs | public | 2026-07-09 | lead evidence | medium | partial |
| The source path reaches the runtime handler | GitHub source at a pinned commit | source | public | 2026-07-09 | verification evidence | high | confirmed |

## Recovery Log

| Attempt | Status | What it showed | Recovery | Result |
| --- | --- | --- | --- | --- |
| Context7 lookup | partial | Current docs were thin | Checked official docs and source | confirmed |
| DeepWiki question | worked | Identified likely path | Verified path in GitHub source | confirmed |

## Counter-Review

- The local-first route may be better if private code cannot leave the machine.
- The generated repository map was not used as final proof; source verification was required.
- Runtime behavior remains unverified until a representative request is executed.

## Unresolved Research Lines

- Live performance and account-tier limits were not benchmarked.

## Setup And Install Readiness

- Required MCP routes are callable. The recommended local graph tool still needs installation.

## Confidence Rationale

High confidence in the source-level recommendation. Confidence is lower for runtime cost and performance because no live benchmark ran.
```
