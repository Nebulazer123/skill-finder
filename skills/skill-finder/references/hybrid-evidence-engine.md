# Hybrid Evidence Engine

The hybrid evidence engine makes Skill Finder useful with only public and local
evidence while allowing authenticated routes to improve coverage when the task
actually needs them.

## Lanes

The **public/local lane** uses installed skills, local files, `git`, `rg`, staged
clones, public GitHub, the MCP Registry, deps.dev, OSV, package registries,
official documentation, Context7, DeepWiki, skills.sh, skills.md public
listings, and other safe public sources that are available.

The **connected lane** includes private GitHub, Sourcegraph MCP, Devin sessions,
Browserbase cloud, Firecrawl, Exa, private Hugging Face repositories, Composio,
and premium skills.md execution. Select it only when it is configured,
authorized for the data, and able to add evidence the public/local lane cannot.
Never place a secret in an EvidenceRecord.

## Canonical Identity

Normalize candidates before deduplication:

| Capability | Identity |
| --- | --- |
| Package | Package URL, such as `pkg:npm/browse@0.9.5` |
| Repository | `github.com/owner/repo@commit` |
| MCP server | `mcp:<official-name>@<version>` |
| Skill | `skill:<provider>/<owner/repo>/<skill>@<version>` |
| Connector | `connector:<provider>/<stable-id>` |

Keep every alias and source-specific identifier. Merge candidates when any
canonical identifier or alias overlaps.

## Public Adapters

- **MCP Registry `/v0.1`:** discovery, pagination, versions, lifecycle status,
  repository identity, and package identity. It is not a security audit.
- **deps.dev v3:** publication date, SPDX licenses, direct advisories, source
  links, dependencies, and SLSA provenance. Treat source links as unverified
  until source inspection confirms identity.
- **OSV API v1:** package, PURL, version, commit, and batch vulnerability
  queries. Use bounded responses. When OSV-Scanner is present, only use
  read-only `osv-scanner scan source`; never invoke `fix` automatically.
- **ecosyste.ms and OpenSSF:** optional corroboration. Missing coverage is never
  negative evidence. Preserve ecosyste.ms attribution and license requirements.
- **Host tools:** emit structured call intents because Python cannot invoke MCP
  tools directly. Import the host result and route attempt into the ledger.

All adapters use bounded timeouts, pagination, response sizes, and tolerant
parsing of additive response fields. Unit tests use fixtures; live contract
tests are explicit and non-mutating.

## Evidence Rules

Discovery or generated sources may identify a candidate, file, or question.
Material claims require a primary verification source such as source code,
tests, official documentation, a package registry, a release, or a security
advisory.

Detect conflicting claims about version, license, support, installation,
repository identity, and security. Preserve unresolved conflicts and reduce
confidence. Do not turn an OpenSSF score, stars, downloads, or a generated
summary into the deciding signal.

## Run Bundles

Deep runs write:

- `run.json`: engine/schema versions, task digest, routes, date, confidence.
- `capabilities.json`: available and authorized route snapshot.
- `route-attempts.jsonl`: attempts, failures, recoveries, and evidence IDs.
- `evidence.jsonl`: provenance records.
- `candidates.json`: normalized candidates and scores.
- `report.md`: reader-facing recommendation and counter-review.

Store bundles only in a user-selected or temporary path. The engine introduces
no global research history or telemetry.
