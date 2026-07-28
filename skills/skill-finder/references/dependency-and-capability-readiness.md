# Dependency And Capability Readiness

Readiness is task-specific. The local essentials are `python3`, `git`, and
`rg`. Other tools are route capabilities, not universal prerequisites.

## Readiness Ledger

Record each relevant route as required-for-this-task, optional, connected,
installed, missing, unauthorized, staged/downloaded, or unavailable. Include
the verification command, source-backed install command, setup state, staging
path, cleanup status, cost, data classification, and notes.

Missing optional routes do not block a run. They reduce evidence coverage,
trigger recovery, or become an unresolved research line. Pause for setup only
when the current task's evidence floor cannot be reached without a specific
missing route.

## Local Essentials

- `python3` runs the evidence engine and validation.
- `git` inspects repository identity, revisions, and history.
- `rg` performs exhaustive local source and non-code searches.

Node.js, `npm`, and `npx` are required only when the selected candidate,
registry, or setup path uses them.

## Conditional Routes

- **Repository work:** GitHub source, a staged clone, codebase-memory-mcp, or
  Sourcegraph. Codebase-memory is high-value for symbols and call paths, but
  direct files and `rg` remain source authority and recovery.
- **Current API documentation:** Context7 or official docs. Retry alternate
  names and docs hosts; thin Context7 output is partial evidence, not failure.
- **Repository orientation:** DeepWiki or Devin can find architecture and
  source paths. They are lead evidence and never sole proof.
- **Browser evidence:** Browserbase Browse CLI or another browser route when
  static docs and source are insufficient.
- **Skill catalogs:** skills.sh/`npx skills` and skills.md public listings.
- **ML work:** Hugging Face MCP/CLI for models, datasets, Spaces, papers, and
  evals.
- **Connected apps:** Composio or the host's connector when account data or app
  actions are central to the task.
- **Supply chain:** MCP Registry, deps.dev, OSV, optional OSV-Scanner, OpenSSF,
  and ecosyste.ms.

Account-backed routes remain eligible, but select them only when available,
authorized for the input, and materially useful. Private material must stay
within routes already authorized for that source.

## Stale Or Failed Routes

Repair or update that route first when the active policy permits safe helper
setup, then rerun a harmless check. If it exposes a Skill Finder documentation,
package, engine, or plugin mismatch, create a `Nebulazer123/skill-finder` issue
with `gh issue create`, or prepare an issue draft. If the failure is unrelated
to Skill Finder, fix the task route and do not file a Skill Finder issue.

After a failed or cancelled material route, try a different source family.
Examples: DeepWiki to GitHub source, GitHub search to a local clone, Context7 to
official docs, or a graph trace to `rg` plus source inspection. Preserve the
missing line when recovery cannot verify it.

## Setup Commands

The repository tracks real npm-installable setup tools in `package.json`:
`skills`, `@upstash/context7-mcp`, `browse`, and
`codebase-memory-mcp`. These packages make the dependency graph honest; their
presence does not make every route mandatory for every run.

Useful source-backed setup examples include:

```bash
npm install -g codebase-memory-mcp
codebase-memory-mcp install
```

For skills.md use `bun install -g @hasna/skills` and
`skills setup agents`. Do not confuse its `skills` executable with skills.sh;
use `npx skills` for skills.sh commands. Check public listings with
`skills list --json`; quote premium work with `skills quote` before asking for
approval.

For any command not verified from a current source, write
`Install command: not verified`. Never guess.
