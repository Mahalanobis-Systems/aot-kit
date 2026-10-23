---
name: fail-soft-tools
description: "AOT optimization 2.b.i (Tier 2, Reliability): Make tool calls and tool results fail soft, and retry transient failures. Placeholder. Use when an agent shows: runs ending in an unhandled exception (AttributeError, parse or fetch errors) rather than an answer; tool spans returning empty or garbled text; failure rows labeled tool-recovery-failure or observation-failure; requests failing on rate limits or transient server errors with no retry, or with retries exhausted; failure rows labeled service-failure or recovery-failure-external."
---

<!-- Generated from library/entries/fail-soft-tools.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Make tool calls and tool results fail soft, and retry transient failures

> **Placeholder.** Generated from `library/entries/fail-soft-tools.yaml` (entry 2.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.b.i |
| Earlier id | T16 |
| Tier | 2 (Reliability): removes crashes, a hard failure |
| Categories | Tools: Avoiding misuse; Orchestration: Bounding execution |
| Change | tool / error_handling (fix) |

## What it is

Guard the tool-call parser against calls in an unexpected shape (a string where a dict is expected), catch errors inside tools (bad file format, failed fetch, extraction failure) and return a usable message instead of raising, and replace custom extraction code (HTML, tables) with a standard parser. A failed call must never crash the loop. Evaluate the errored cases first: a tool fix can break the agent outright. Retry transient failures (rate limits, timeouts and server errors from the model provider or a tool's backend) with backoff and a bounded count, and when the count runs out, return that to the loop as a result rather than ending the run.

## When it applies

- **In the code:** parsing that assumes a fixed call shape; tool bodies with no try/except; custom HTML or table extraction code
- **In traces:** runs ending in an unhandled exception (AttributeError, parse or fetch errors) rather than an answer; tool spans returning empty or garbled text; failure rows labeled tool-recovery-failure or observation-failure; requests failing on rate limits or transient server errors with no retry, or with retries exhausted; failure rows labeled service-failure or recovery-failure-external
- **In eval results:** crash outcomes as a share of failures; request-failure outcomes

## How (outline)

1. From traces, list unhandled exceptions by tool and by parser.
2. Add type guards where calls and results are built.
3. Wrap each tool body; on error return a short message the model can act on.
4. Replace hand-written HTML or table extraction with a library parser.
5. Add bounded retries with backoff for transient errors on model and tool calls.
6. Re-run the errored cases; then the full set.

## How to measure

- **before-after** (Tier 2): unhandled-exception rate, crash outcomes and request-failure rate on the same cases or load stream

## Expected impact

- **Quality:** improves, small: VeRO: removed all 11 parser crashes in 2 of 3 runs, but only 1-3 became passes; a parser switch on SimpleQA went 0.62 to 0.86 against the last working version
- **Cost:** none
- **Performance:** none

## Evidence (summary)

- paper Figure 14: "Robust file/Wikipedia tools" flat (0.24 to 0.22); the follow-up "fix Wikipedia tool file errors" 0.22 to 0.26.
- paper Figure 15: A Wikipedia table-extraction fix crashed the agent (validation to 0.10) before being replaced by T18.
- paper §A.4, Table 16: Eliminated all 11 baseline AttributeError crashes in two of three runs; only 3 and 1 of those samples became passes, the rest failed differently.
- paper §5.4: Found independently by the Tools-B=89 and Filesystem-B=178 runs. Tools-B=178 guarded three result builders but not the parser and left the crash intact, yet had the best pass rate.
- paper Figure 15: Validation 0.10 to 0.86 and test 0.58 to 0.86; the best SimpleQA result in Table 2 (0.86 max).

## Caveats

Tool fixes can break the agent outright; evaluate the errored samples first. Reliably discoverable but neither necessary nor sufficient for a pass-rate gain.

## Related

- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)

<!-- End of the generated part. Everything below is written by hand. -->

## To build

This skill is a placeholder. To make it usable on a client's agent:
- [ ] **Detect:** a check that finds where this applies, from the agent's code, its traces and
      its eval results (the signals above), and says how strongly.
- [ ] **Apply:** a step-by-step procedure for making the change in the client's repository,
      with the decisions the owner must make.
- [ ] **Measure:** the before/after recipe at this tier's evidence gate, run through
      aot-evals (`aot-evals:run` for a paired comparison).
- [ ] **Evidence:** a short, dated summary of what the change has done elsewhere, with the
      conditions under which it helped or hurt.
