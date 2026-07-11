# skills.md Route

skills.md is an API-based remote skill catalog. It can expose a large public registry through a CLI or MCP provider, load only the selected skill contract, and return generated artifacts, logs, and receipts. Use it as a discovery and execution route when a broader remote catalog would improve the task.

## Setup

Use the current official setup sequence:

```bash
brew install bun
bun install -g @hasna/skills
$HOME/.bun/bin/skills setup agents
$HOME/.bun/bin/skills --version
$HOME/.bun/bin/skills list --json
```

`$HOME/.bun/bin/skills setup agents` registers the provider for supported MCP hosts, including Codex and Claude Code. An account is not needed to inspect the public registry, but sign in for account-backed work:

```bash
$HOME/.bun/bin/skills auth signup
$HOME/.bun/bin/skills auth whoami
```

Use the current `$HOME/.bun/bin/skills setup agents` flow from the installed CLI documentation.

## Command Collision

Vercel's skills.sh CLI and skills.md's hosted CLI both use the executable name `skills`. They are different products.

- Use `npx skills ...` or the verified Vercel binary for skills.sh discovery and local Agent Skills package work.
- Use the skills.md installation path, commonly `$HOME/.bun/bin/skills`, for the remote registry and hosted runs.
- Never decide which provider is active from the command name alone. Check the version and record the provider in the readiness ledger.

## Discovery Workflow

1. List or search the public registry with `skills list --json` or `skills search <query>`.
2. Inspect one selected candidate with `skills info <name>` or `skills docs <name>`.
3. Record source, capability, pricing tier, account status, and any input or system requirements.
4. Treat the remote contract as candidate evidence. Inspect its trust and data-handling surface before recommending it for sensitive work.
5. Use `skills quote <name>` for premium or input-priced work before any run.
6. Ask for approval when the quote, data transfer, account access, or sensitive input makes the action consequential.
7. Run only after approval, then record the run id, receipt, exported artifact paths, and cleanup status.

## Evidence Rules

The catalog and returned Skill.md are useful discovery evidence. They do not prove that a remote skill is the best option, safe for private inputs, or equivalent to a local implementation.

- Prefer official skill metadata, docs, quote output, and receipt data for platform claims.
- Verify technical or repository claims through source files, official docs, tests, or a local clone when the recommendation depends on them.
- Keep skills.md evidence separate from skills.sh, GitHub, DeepWiki, Devin, Context7, and local source evidence.
- Record failed searches and empty results as route evidence, then recover through another source route.

## Pricing And Approval

Free public listing does not mean every run is free. Premium skills may expose fixed or input-dependent pricing. Always quote before a premium run and show:

- skill name;
- estimated or fixed price;
- input units that affect the price;
- approval state;
- run or receipt identifier after execution.

Do not run a premium or sensitive skill just to test whether it works. A public `list` or `info` check is enough for setup verification.

## Output Fields

When this route contributes to a recommendation, add these fields to the Candidate Evidence Table or Deep Evaluation packet:

| Field | Example |
| --- | --- |
| Provider | skills.md |
| Remote skill | `read-pdf` |
| Availability | public, account-required, or unavailable |
| Pricing | free, premium, or quote required |
| Evidence | registry, docs, quote, receipt, or returned artifact |
| Data surface | local file, URL, text, or account-backed input |
| Verification | command, source, test, or unresolved |
| Next action | inspect, quote, ask approval, run, or choose another route |
