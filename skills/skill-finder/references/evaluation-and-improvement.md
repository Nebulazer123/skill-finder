# Evaluation And Improvement

Use for local, suspicious, high-stakes, or closely ranked candidates.

## Candidate Evidence Table

| Candidate | Source/path | README/source summary | Type | Availability | Dependency readiness | Files read | Tests/evals found | Freshness | Adoption | Contributor signal | Trust surfaces | Reuse lane | Score | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use `unknown` instead of guessing. Explain missing type, dependency readiness, install command source, or verification command. Use README/docs/marketplace/canonical evidence. For GitHub, score 20+ finalists when possible; show at most five.

## Score And Confidence

Finalist evidence: README/source summary, files read/scanned, install command/source, dependencies, trust surfaces, tests/evals, freshness, adoption, license/reuse, docs/changelog, verification command, confidence notes.

Trigger-quality scoring: fit `strong|medium|weak`; risk `overtrigger|undertrigger|overlap|unclear|low`. Reuse lane: `Use`, `Install`, `Copy`, `Adapt`, `Learn`, `Unknown`; inspect license before Copy/Adapt.

Score: relevance, Codex fit, triggers, file quality, freshness, adoption, tests/evals, install/dependency readiness, verification, usefulness, trust/safety, license/reuse, adjacent value, plugin-eval/sandbox evidence, low-weight contributor activity. Popularity/contributors never outrank file evidence, freshness, installability, dependency readiness, trigger fit, or trust. Prefer one answer; bundle only with distinct roles and verification.

For large-repo search compare exact/lexical, path, regex, AST, symbol/LSP, semantic/vector, hybrid, RAG/indexing, graph/path tracing, hosted search.

Winner packet: why it beats near-misses, what would change the recommendation, missing evidence, one-vs-bundle decision, approval needed. Bundle packet: roles, install order, approvals, dependencies/conflicts, verification, one end-to-end test, fallback, rollback.

Install command rule: quote source commands. If missing, write `Install command: not verified` and name next source/file. Every finalist needs required/optional/installed/missing/prepared/pending dependencies, verification command, install source, notes. Use `not applicable` for docs-only or Missing Skill Blueprint.

## Evals And Rubric

For local skills run `plugin-eval analyze <skill-path> --format markdown`. If findings appear, use `plugin-eval:improve-skill`, then rerun plugin-eval and tests.

Pressure tests: browser automation, web performance, PR/code review, MCP/app/n8n setup, FFmpeg/ripgrep/gh lookup, dependency conflicts, skill authoring, create-new-skill fallback, installed-skill interference, stale-popular vs fresh-small, prompt injection, buried monorepos, misleading README vs weak `SKILL.md`. Record prompt, result, pass/fail; no packet is partial/fail.

Record eval-loop rounds and scores. If a synthetic hard/boundary scenario scores 100/100 on first pass, treat it as weak; add harder decoys, tighter bounds, deeper inspection, or realistic failure pressure, then rerun.

Recommendation Acceptance Rubric:

- Minimum evidence: source URL, path, install command or unavailable reason, dependency readiness, verification command or reason, full reads/scans, Candidate Evidence Table, actual capability.
- Ranking confidence: downgrade missing install docs, undocumented dependencies, weak files, poor triggers, unclear license/reuse, stale maintenance, unresolved safety, no verification command, unplanned bundle.
- Human review gate: ask explicit approval before installs, global changes, risky scripts, credentials, integrations, or deleting non-temporary files.
- No good skill fallback: say no good skill was found, list searched sources/missing evidence, and include a Missing Skill Blueprint.

Missing Skill Blueprint: name, trigger description, should/should-not-trigger examples, workflow, references, scripts/tools/dependencies, trust surfaces, eval cases, install/use surface, confidence, open questions.

Observed usage scope: plugin-eval observed usage measures the full Codex session, not only active skill tokens. Use static budget for size; use observed usage, task outcome scorecard, and human review for usefulness. Coverage map: maintain `evidence/skill-finder-coverage-map.md`.
