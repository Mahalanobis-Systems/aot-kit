---
name: fail-soft-tools
description: "AOT optimization 2.b.i (Tier 2, Reliability): Make tool calls and tool results fail soft, and retry transient failures. Placeholder. Use when an agent shows: runs ending in an unhandled exception (AttributeError, parse or fetch errors) rather than an answer; tool spans returning empty or garbled text; failure rows labeled tool-recovery-failure or observation-failure; requests failing on rate limits or transient server errors with no retry, or with retries exhausted; failure rows labeled service-failure or recovery-failure-external; runs ended by the harness rather than the model (a repeat detector after malformed calls, a provider stream error, the output cap); three or more consecutive calls to a tool that keeps failing; a write retried after a timeout and committed twice."
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

Keep a failed call from ending the run: validate tool calls and model responses, return tool errors to the agent as results, and retry only failures that are transient and safe to repeat. Concretely, guard the parser against calls in an unexpected shape (a string where a dict is expected, a missing required argument), catch errors inside tools (bad file format, failed fetch, extraction failure) and return a usable message instead of raising, replace custom extraction code (HTML, tables) with a standard parser, and retry rate limits, timeouts and server errors with backoff and a bounded count, returning exhaustion to the loop as a result. The harness often decides the outcome: under injected faults, tool-call faults that tool error handling caught cost under 5 points while unchecked truncated arguments cost one pipeline 52.63 points, and in real benchmark runs a repeat detector that ended runs after repeated malformed calls, with no final message to the model, ended 55 runs, only one of which scored above zero. The limits: fixing crashes rarely turned them into passes (3 and 1 of 11 in one study), a tool fix can break the agent outright, 91.3% of failures mined from MCP server issues were permanent so retrying them only burns tokens, and blindly retrying a write whose reply was lost duplicated it in 53.33% of trials, so retry writes only with server-side idempotency or after checking whether the first call landed.

## When it applies

- **In the code:** parsing that assumes a fixed call shape; model responses used without checking finish_reason, empty content or tool-call arguments against the schema; tool bodies with no try/except; custom HTML or table extraction code; retry wrappers that retry every error, including permanent ones and writes without an idempotency key the server honors
- **In traces:** runs ending in an unhandled exception (AttributeError, parse or fetch errors) rather than an answer; tool spans returning empty or garbled text; failure rows labeled tool-recovery-failure or observation-failure; requests failing on rate limits or transient server errors with no retry, or with retries exhausted; failure rows labeled service-failure or recovery-failure-external; runs ended by the harness rather than the model (a repeat detector after malformed calls, a provider stream error, the output cap); three or more consecutive calls to a tool that keeps failing; a write retried after a timeout and committed twice
- **In eval results:** crash outcomes as a share of failures; request-failure outcomes
- **Probes:** Faults at the tool and model-API boundaries: malformed calls, errors, timeouts, empty and truncated responses, permanent failures, and lost replies on writes.

## How (outline)

1. Start from the harness as it is: from traces, list unhandled exceptions by tool and by parser, and runs the harness ended rather than the model (a repeat detector after malformed calls, a provider stream error, the output cap); then inject faults at the tool and model-API boundaries (explicit errors, timeouts, rate limits, empty and truncated responses, malformed arguments) for a baseline, since in two fault-injection studies robustness varied with the agent system more than with the model.
2. Validate every call and response before using it: add type guards where calls and results are built (a tool call emitted as a string rather than a dict crashed one agent), check each model response's finish_reason, emptiness and tool-call arguments against the tool's schema, and return the validation error as the tool result (its wording is 7.b.ii). Empty or truncated responses arrive as successful calls and bypass error handling: tool-call faults that error handling caught cost under 5 points of pass@1, while a pipeline that passed truncated arguments on unchecked lost 52.63 points. When the same malformed call repeats, warn the model before a repeat detector (7.b.i) ends the run: a detector that ended runs after repeated malformed edit calls, with no final message, ended 55 runs and one scored above zero, while the same model repaired such failures in other harnesses.
3. Wrap each tool body; on error return a short result marked as an error that the model can act on (what the error says is 7.b.ii).
4. Replace hand-written HTML or table extraction with a library parser.
5. Retry in the harness only what is transient: rate limits, timeouts, server errors and dropped streams from the model provider or a read-only tool, with backoff and a bounded count (provider stream errors cut off turns in 25 of one model's 62 runs in one harness, all scored as failures). Resume a turn cut off by the output cap instead of ending the run: one harness resumed 100 such runs and 48 went on to score above zero. Return permanent errors at once, marked as not retryable: 91.3% of failures mined from MCP server issues were permanent, and in the traces examined, agents left to decide never told permanent from transient failures and retried a failing tool up to 12 times in a row. When the count runs out, return that to the loop as a result.
6. For tools with side effects, retry automatically only if the call failed before it was sent, the server honors an idempotency key, or a check shows the first call did not land; gate irreversible writes with 10.b.i. Blind retries (up to 3, with exponential backoff) of writes whose reply was lost duplicated them in 53.33% of trials; client-side keys helped only on endpoints that deduplicate; server-side idempotency on every endpoint gave 97.24% recovery with no duplicates, and checking before retrying raised recovery from 43.13% to 75.00% on four composite workflows.
7. Re-run the errored cases first (a tool fix can crash the agent outright), then the full set, then paired runs with the same injected faults: task success, runs ended by the harness, recovery per fault type, retries per failure, duplicate side effects, and LLM calls and tokens per task.

## How to measure

- **experiment** (Tier 2): paired runs on the same tasks and model, the harness as is against the change, with faults injected at the tool and model-API boundaries at fixed steps: explicit errors, timeouts, rate limits, empty and truncated responses, malformed or schema-violating arguments, permanent as well as transient failures (most real MCP failures are permanent), and lost replies on write calls; report task success, runs ended by the harness rather than the model, recovery per fault type, retries per failure, duplicate external effects, and LLM calls and tokens per task; re-run the errored cases first, since a tool fix can crash the agent
- **monitor**: in production traces: unhandled-exception and crash outcomes; runs ended by the harness (repeat detector, provider stream error, output cap); schema-validation failures of tool calls per model and provider; request failures and retries per request by error class, and retry exhaustion; consecutive calls to a failing tool; writes committed twice (same idempotency key or same arguments)

## Expected impact

- **Quality:** improves, medium: tool-call faults caught by tool error handling cost under 5 points of pass@1, while a pipeline that passed truncated arguments on unchecked lost 52.63 points (Tan, Aug 2026); a repeat detector ending runs on malformed calls ended 55 runs, one scoring above zero, and resuming output-capped turns let 48 of 100 runs go on to score (Li, Oct 2026); after lost replies on writes, server-side idempotency gave 97.24% recovery against 33.20%, and verify-before-retry 75.00% against 43.13% (Sah, Oct 2026); limits: VeRO removed all 11 parser crashes in 2 of 3 runs but only 3 and 1 became passes, and a table-extraction fix crashed one agent (validation 0.10) until a standard parser took it to 0.86 (VeRO, Feb 2026); calibrated MCP faults still cut task-completion score from 8.08 to 3.23 with errors returned to the model (Iannillo, Oct 2026)
- **Cost:** degrades, small: no extra calls when nothing fails; under injected faults, retries raised AutoGen's LLM calls per task from 1.72 to 7.3 (4.24x) while a pipeline that failed early used fewer (0.71x) (Tan, Aug 2026); agents retried a failing MCP tool three or more times in a row in 38 runs, the costliest of these runs reaching 52 tool calls and 107,849 tokens (Iannillo, Oct 2026)
- **Performance:** none
- **Governance:** mixed, medium: blind retries (up to 3, with exponential backoff) of writes whose reply was lost duplicated the external effect in 53.33% of trials, 65.62% with Gemini 3.8 Flash and 51.25% with GLM-5.2; server-side idempotency took duplicates to 0.00%, and retries of calls that failed before dispatch caused none in 3,028 capable trials (Sah, Oct 2026)

## Evidence (summary)

- paper Figure 14 (2026-02): "Robust file/Wikipedia tools" flat (0.24 to 0.22); the follow-up "fix Wikipedia tool file errors" 0.22 to 0.26.
- paper Figure 15 (2026-02): A Wikipedia table-extraction fix crashed the agent (validation to 0.10) before being replaced by T18.
- paper §A.4, Table 16 (2026-02): Eliminated all 11 baseline AttributeError crashes in two of three runs; only 3 and 1 of those samples became passes, the rest failed differently.
- paper §5.4 (2026-02): Found independently by the Tools-B=89 and Filesystem-B=178 runs. Tools-B=178 guarded three result builders but not the parser and left the crash intact, yet had the best pass rate.
- paper Figure 15 (2026-02): Validation 0.10 to 0.86 and test 0.58 to 0.86; the best SimpleQA result in Table 2 (0.86 max).
- …and 4 more sources in `library/entries/fail-soft-tools.yaml`.

## Caveats

Fail-soft handling is necessary but not sufficient: in VeRO removing all 11 crashes turned only 3 and 1 of them into passes, a tool fix crashed one agent outright, and even with errors returned to the model, calibrated MCP faults cut task-completion scores by 60% (Iannillo, Oct 2026). Retries help only where failures are transient and the call is safe to repeat: 91.3% of failures mined from MCP issue threads were permanent (a stress profile, since issues over-represent reproducible bugs), agents retried permanent failures on their own, and blind retries of writes duplicated them in 53.33% of trials in a benchmark with mocked APIs and one fault per run; no study here tests marking errors as not retryable. The fault-injection studies are small or synthetic (about 4.6 triggered tasks per fault configuration in one, two gpt-oss models on an easy benchmark in another, 12 workflow clusters with verify-before-retry tested post hoc in a third), and harness comparisons bundle error handling with tools, prompts and limits, so measure the effect in your own agent.

## Related

- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)

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
