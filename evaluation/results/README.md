# Live Clean-Room Results

These bundles exercise the v1.3.0 evidence engine against unfamiliar repositories.
They are checked-in release evidence, not reusable facts about the repositories.

- `public-bpftime/` uses only public and local routes.
- `connected-binaryen/` uses Browserbase for hosted discovery, then recovers to
  an independently staged source checkout for primary verification.

Every bundle contains the six files emitted by a Deep Evaluation. Source claims
are pinned to the commit inspected on the date recorded in `run.json`.
