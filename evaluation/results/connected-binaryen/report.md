# Connected Clean-Room Evaluation: Binaryen

## Recommendation

Use connected browser research to locate likely implementation anchors, then
verify the route in a commit-pinned source checkout. Browserbase improved initial
discovery but did not replace source evidence.

The verified transformation path is:

`wasm-opt` option parsing -> `OptimizationOptions::runPasses` ->
`PassRunner::add` -> `PassRunner::run` -> module/function pass execution ->
validation -> `ModuleWriter` -> binary serialization.

## Evidence

| Claim | Role | Source |
| --- | --- | --- |
| Hosted search identified likely files | Lead only | Browserbase Cloud Search |
| Options build and flush the pass pipeline | Primary verification | `src/tools/optimization-options.h` at commit `55dff6b` |
| Pass registry creates and runs requested passes | Primary verification | `src/passes/pass.cpp` |
| The transformed module is emitted | Primary verification | `src/tools/wasm-opt.cpp` and `src/wasm/wasm-binary.cpp` |

## Recovery Log

Browserbase Cloud Search worked. Fetching a complete GitHub source page returned
an oversized response that was truncated by the host, so the run did not treat
it as proof. It recovered through a different source family: a fresh shallow
clone and direct source inspection.

Devin was not exposed as a callable route in this host. It was skipped and did
not block the public-source verification path.

## Counter-Review

The strongest alternative was a fully public run using GitHub search or a direct
clone from the start. It would win when hosted discovery is unavailable, cost is
restricted, or the likely source files are already known. The connected route
won narrowly here because it found the relevant files quickly; the final
technical confidence still comes from source.

## Unresolved Lines

- The trace covers the normal `wasm-opt` pass and output path, not every fuzzing,
  convergence, or exception-translation branch.
- No local Binaryen build or live `.wasm` transformation was executed.
- Devin-specific repository Q&A remains untested in this host.

## Confidence

**92/100.** Connected discovery and immutable source verification agreed, the
oversized result recovered through another family, and all material claims have
primary evidence. Confidence is below maximum because runtime execution was not
part of this source-level test.

## Setup Readiness

Browserbase was selected only because it was configured and relevant to hosted
discovery. The same task remains completable without it. No new install command
is recommended by this evaluation.
