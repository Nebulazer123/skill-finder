# Public Clean-Room Evaluation: bpftime

## Recommendation

Use a staged, commit-pinned source checkout as the verification route for this
repository-heavy question. DeepWiki supplied a useful map, but no material claim
depends on that generated summary.

The verified runtime path is:

`inject_by_frida` -> `bpftime_agent_main` -> registered `frida_attach_impl` ->
shared-memory uprobe handler -> `create_attach_with_ebpf_callback` ->
`bpftime_prog_exec` -> compiled JIT function or interpreter.

## Evidence

| Claim | Role | Source |
| --- | --- | --- |
| CLI injection enters `bpftime_agent_main` | Primary verification | `tools/cli/main.cpp` at commit `005635b` |
| Userspace perf-event handling creates a uprobe | Primary verification | `runtime/syscall-server/syscall_context.cpp` |
| Attach callback executes the loaded program | Primary verification | `runtime/src/attach/bpf_attach_ctx.cpp` |
| Load/execute selects JIT or interpreter | Primary verification | `runtime/src/bpftime_prog.cpp` |
| Initial architecture map | Lead only | DeepWiki |

## Recovery Log

The first local staging command included a destructive pre-clean and was rejected.
The run changed method: it created a new unique temporary directory and cloned
there without deleting anything. That recovery produced the primary evidence.

## Counter-Review

The strongest alternative was to rely on DeepWiki and direct GitHub page reads.
That would be faster, but it would not prove all cross-file runtime transitions
at one immutable revision. It would win only for a quick orientation request
where exact source tracing was not material.

## Unresolved Lines

- The trace is source-level; no eBPF program was executed in a live target.
- CUDA attachment and kernel passthrough paths were outside this question.
- The exact interpreter call immediately after the inspected excerpt remains
  outside the cited line range, although the JIT branch is directly verified.

## Confidence

**91/100.** Independent source families were used, all material claims were
verified at one commit, and the failed route recovered. Confidence is below
maximum because the program was not run end to end.

## Setup Readiness

No install action is recommended for this source-trace result. The run completed
with public routes and did not require an account-backed service.
