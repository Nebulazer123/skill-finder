# AI Fluency Evidence

This file explains how Skill Finder was created as an AI-assisted project and what I learned while building it. It is written for a reviewer who wants to quickly understand the human intent, the AI collaboration, the evaluation process, and the responsibility boundaries behind the public release.

## Project Summary

Skill Finder is a reusable agent skill for people who use AI agents regularly and need a better way to find current third-party skills, tools, MCP servers, workflows, packages, documentation sources, or capability stacks.

The problem I wanted to solve was practical: when an AI agent needs a capability, it can waste time improvising temporary instructions or grabbing the first matching search result. Skill Finder makes the agent search more broadly, inspect real evidence, compare candidates, and recommend the strongest option before anything risky is installed or changed.

## What I Built

- A public Skill Finder package under `skills/skill-finder/`.
- A reader-first public `README.md`.
- A public diligence statement in `DILIGENCE.md`.
- Public-safe examples and validation checks.
- A selected AI-assisted logo image for the README.
- Safety and approval rules for installs, credentials, paid services, risky scripts, destructive actions, publishing, and persistent/global mutation.

## My Role Versus AI's Role

| Area | My human role | AI/tool role |
| --- | --- | --- |
| Project choice | Chose the Skill Finder idea because it matched a real workflow problem I kept running into. | Helped turn the idea into a concrete project shape. |
| Goal definition | Explained what success should look like: find the best capability, not just a keyword match. | Helped organize that into workflow rules, output requirements, and evaluation criteria. |
| Delegation | Decided which parts should be autonomous and which parts require human approval. | Took on scalable work such as research, inspection, drafting, testing, and iteration. |
| Description | Gave detailed context about what I wanted, why it mattered, how deep the search should go, and how the agent should behave. | Converted that direction into skill instructions, README language, references, and tests. |
| Discernment | Judged whether recommendations were actually useful, whether tests were hard enough, and whether outputs matched the intended use. | Produced candidates, evidence summaries, eval results, and improvement suggestions. |
| Diligence | Chose what to disclose, what to exclude, and what I personally take responsibility for. | Helped draft the diligence language and public-safe packaging. |
| Final decisions | Approved the public direction, selected the logo, corrected boundaries, and decided what belongs in the release. | Assisted with implementation, validation, and documentation. |

The project is not simply "AI made a skill." I used AI as a collaborator, but I shaped the requirements, challenged weak outputs, changed the ranking logic, rejected or refined assumptions, and kept final responsibility for what is published.

## The 4D Learning Evidence

### Delegation

I learned to separate what AI can do well from what I still need to own.

- **Problem Awareness:** I started from a real pain point: needing better skills/tools without wasting time and tokens on temporary one-off solutions.
- **Platform Awareness:** I expanded the search space beyond local skills into GitHub, skill catalogs, MCP servers, apps/connectors, workflows, CLIs, packages, documentation sources, and evaluation tools.
- **Task Delegation:** I delegated research, source discovery, file inspection, candidate comparison, stress-test creation, and draft writing to AI while keeping human approval for installs, credentials, risky actions, publication, and final trust.

### Description

I learned that good prompting is not just telling AI the final answer format. It is giving the full context of what I want, why I want it, who it is for, how deep it should go, and how the assistant should collaborate.

- **Product Description:** I defined the expected output: source-backed recommendations, no more than five visible top options, evidence tables, install commands, dependency readiness, freshness/adoption signals, risks, and approval boundaries.
- **Process Description:** I described the search process: infer the real need, use exact and semantic search, inspect important files, check docs and source links, compare candidates, run evals, and refine weak spots.
- **Performance Description:** I wanted the AI to act both as a teacher and a builder: conversational during course work, autonomous during backend work, and strict about asking before risky actions.

### Discernment

I learned that judging AI output means judging the result, the method, and the collaboration behavior.

- **Product Discernment:** I checked whether a recommendation actually solved the problem, not just whether it had the right name or popularity.
- **Process Discernment:** I pushed the workflow to inspect real files, compare sources, use current documentation, test beyond obvious cases, and avoid shallow search.
- **Performance Discernment:** I corrected the collaboration when it became redundant, missed context, mixed global/project instructions, or treated easy tests as enough.

The biggest Discernment upgrade was using hard eval loops. I wanted tests that could fail first, expose weaknesses, and then guide real improvements.

### Diligence

I learned that transparency about AI use is useful, not embarrassing. It helps a reader understand my intent, where AI contributed, where I reviewed the work, and where future users should still apply judgment.

- **Creation Diligence:** I used AI systems and tools intentionally, including Claude, Codex, Skill Finder itself, Plugin Eval, skill-creator, skill-installer, Superpowers, Context7, Browserbase, Composio, GitHub CLI, and image generation for the logo.
- **Transparency Diligence:** I disclosed that AI helped with planning, drafting, implementation support, search strategy, testing, iteration, documentation, validation, and visual asset creation.
- **Deployment Diligence:** I tested the project through repeated iteration, real workflows, stress tests, cross-model comparison, public package checks, and review against the intended purpose before sharing it.

## Score And Evolution

| Phase | Focus | Score | What changed |
| --- | --- | ---: | --- |
| Phase 1 | Project planning and Delegation | 96/100 | The rough idea became a reusable project with a clear problem, value, major tasks, and human/AI responsibility split. |
| Phase 3 | Description and Discernment execution | 96/100 | The project expanded from finding "skills" into finding agent-usable capabilities: skills, tools, MCPs, apps, workflows, packages, docs, and stacks. |
| Phase 3 strict eval addendum | Hard Description-Discernment loop | 99/100 | Blind evals and failure-driven refinement made the project more trustworthy. The workflow learned to inspect more broadly, stop cleanly, and justify recommendations. |
| Phase 4 | Diligence statement | 98/100 | The public release gained clearer responsibility boundaries, AI-use disclosure, privacy limits, and maintenance awareness. |

Phase 2 was skipped as a separate exercise because the project became a build-focused path, but its Discernment concepts were practiced heavily inside the ranking, testing, eval, and review loops.

## Material Lessons Learned

- Clear Description includes context, intent, audience, depth, constraints, and collaboration style.
- Delegation works best when AI owns scalable research and inspection, while the human owns trust, approval, and final judgment.
- Discernment is stronger when tests are hard enough to break the system and reveal useful failure modes.
- Passing an easy test is not the same as being reliable.
- It is valid to ask AI to create stress tests or search strategies, then judge whether the output is good enough.
- Transparency about AI use can help reviewers understand the human purpose and the review process.
- Public/open-source work creates a stronger responsibility: the repo should be clear, maintainable, public-safe, and honest about what it does and does not guarantee.

## Public Responsibility Boundary

I back this project as a thoroughly researched and tested skill, but Skill Finder does not guarantee perfect recommendations. It is a decision workflow that improves an agent's ability to search, inspect, compare, and recommend.

Users should still review:

- candidate source files and documentation;
- install commands and setup scripts;
- licenses and reuse obligations;
- account, API key, OAuth, or browser-login requirements;
- paid-service boundaries;
- security, privacy, and trust implications;
- whether a recommended tool fits their actual task.

Skill Finder should not silently enter credentials, link accounts, run risky scripts, delete files, publish content, or mutate persistent/global state without explicit approval.

## Review Path

For a fast review, read these files in order:

1. `README.md` — what Skill Finder is and how to use it.
2. `DILIGENCE.md` — AI collaboration disclosure and responsibility statement.
3. `skills/skill-finder/SKILL.md` — the actual skill workflow.
4. `skills/skill-finder/references/` — search, ranking, readiness, approval, and evaluation rules.
5. `examples/recommendation-output-shape.md` — what a good output packet should look like.
6. `validation/test_public_package.py` — public package checks.

## Maintenance Note

Public users can help improve Skill Finder by opening issues for:

- stale or broken install commands;
- missing or outdated source routes;
- weak or biased recommendation behavior;
- risky candidate setup behavior;
- unclear approval boundaries;
- better evaluation scenarios.

Those reports should include the task prompt, sources searched if known, candidates returned, what seemed wrong, and any safer or stronger alternative.
