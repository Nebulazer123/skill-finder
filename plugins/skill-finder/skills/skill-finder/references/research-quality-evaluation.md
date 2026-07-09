# Research-Quality Evaluation

Use this reference only for a Deep Evaluation. It strengthens a recommendation when the choice is costly, complex, uncertain, source-heavy, or explicitly framed as research. It does not turn a simple skill lookup into a long report.

## Choose The Depth

| Depth | Use when | Required output |
| --- | --- | --- |
| Quick Evaluation | A low-risk, straightforward discovery or single-candidate check. | Normal recommendation packet with basic source checks. |
| Deep Evaluation | Multiple plausible candidates; repository or API tracing; no-good-skill work; costly/complex setup; or an explicit research request. | Normal packet plus the Evidence Ledger, Recovery Log, Counter-Review, Unresolved Research Lines, readiness, and confidence rationale. |

Use Deep Evaluation automatically when any trigger in the table applies. Do not require more credentials, services, or remote calls merely because the deeper format is selected; record missing routes and use the available verified evidence.

## Evidence Ledger

Record every source that materially affects a Deep Evaluation. Keep discovery signals separate from verification.

| Claim or question | Source URL or artifact | Source type | Accessibility | Date checked | Evidence role | Strength | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Short claim | Link, local path, commit, or command output | official, source, test, package, docs, release, community, or other | public, user-provided, or unavailable | YYYY-MM-DD | lead evidence or verification evidence | high, medium, or low | confirmed, partial, rejected, or open |

- **lead evidence** finds likely files, candidates, routes, or questions. It can shape the search but cannot alone settle a material recommendation claim.
- **verification evidence** comes from the candidate source, GitHub source files, a checked local clone, tests, official documentation, package metadata, release notes, or another direct primary artifact.
- Use the current date as the date checked. Include publication/release dates too when freshness matters.
- Mark a source `partial` when it is useful but thin, stale, ambiguous, or incomplete. Do not silently upgrade it.

## Generated Repository Maps

DeepWiki and Devin are strong orientation routes for architecture, source paths, likely extension points, and hard follow-up questions. Treat their generated summaries and answers as lead evidence.

Before a generated-repository claim affects a winner, install recommendation, callable API statement, security conclusion, or source-path trace, verify it with GitHub MCP, a fetched or checked local source artifact, tests, manifests, official documentation, or a release note. If verification is unavailable, label the statement as an unverified lead and do not use it as the deciding proof.

## Freshness And Source Mix

- Check current API, CLI, MCP, and setup claims against official docs, Context7, source, or current releases.
- Flag time-sensitive sources that are older than the relevant product horizon. A source may remain useful, but the confidence rationale must explain the age.
- Prefer a mix of independent evidence for the winner. Do not let one README, generated wiki, marketplace page, or search result carry the conclusion alone when stronger sources are available.
- Keep user-provided private material out of a public report. It can guide the task, but it is not independent verification of the user's own facts.

## Recovery Log

When a route fails, is weak, is cancelled, or gives thin evidence, record it and recover through a materially different route. A route failure is a research signal, not a reason to discard the line of inquiry.

| Attempt | Status | What it showed | Recovery | Result |
| --- | --- | --- | --- | --- |
| Route/tool and query | worked, weak, unavailable, cancelled, or partial | useful finding or exact limitation | different source route attempted next | confirmed, partial, or unresolved |

Examples of materially different recovery: DeepWiki or Devin to GitHub source; GitHub search to a fresh local clone; Context7 retry to official docs; graph trace to `rg` plus source inspection; browser search to fetched documentation. Preserve the missing line if every route stays unavailable.

## Counter-Review

Before finalizing, test the recommendation against the strongest credible alternative. The Counter-Review must identify at least three findings across these checks:

1. What would make the winner wrong or unsuitable?
2. Which material claims rely on only lead evidence or a single source?
3. Which sources are stale, thin, or not primary?
4. Which near-miss could win under a different privacy, cost, host, or setup constraint?
5. What research line remains unverified?

Address critical findings in the recommendation. Preserve lower-severity uncertainty in Unresolved Research Lines rather than hiding it.

## Deep Evaluation Output

Use this order after the normal recommendation sections:

```markdown
## Evaluation Depth

Deep Evaluation: [why this task met the trigger]

## Evidence Ledger

| Claim or question | Source URL or artifact | Source type | Accessibility | Date checked | Evidence role | Strength | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Recovery Log

| Attempt | Status | What it showed | Recovery | Result |
| --- | --- | --- | --- | --- |

## Counter-Review

- Finding: [alternative, weak claim, stale source, or missing verification]
- Finding: ...
- Finding: ...

## Unresolved Research Lines

- [What was not verified, why it matters, and the next strongest route.]

## Setup And Install Readiness

- [Required setup, command/source, and any pending user action.]

## Confidence Rationale

[Confidence level and the evidence coverage, freshness, source quality, and remaining gaps behind it.]
```

The final recommendation must say which evidence made the winner win, what would change the decision, and whether another option is better for a different constraint.
