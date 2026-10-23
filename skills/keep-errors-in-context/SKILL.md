---
name: keep-errors-in-context
description: "AOT optimization 7.b.ii (Tier 2, Reliability): Keep errors in context. Placeholder. Use when an agent shows: Errors absent from the next model input; exact repeats of a call that already failed; runs of failed fixes of the same error; agents stopping after error text that asks for a step they cannot take; error observations thousands of lines long."
---

<!-- Generated from library/entries/keep-errors-in-context.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Keep errors in context

> **Placeholder.** Generated from `library/entries/keep-errors-in-context.yaml` (entry 7.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.b.ii |
| Earlier id | P26 (Production, from the master cookbook) |
| Tier (proposed) | 2 (Reliability): error recovery: failures stay visible to the model |
| Categories | Orchestration: Bounding execution |
| Change | workflow / state_management |

## What it is

Return every failed action to the model as an error it can read (the call, the cause, a capped trace) instead of swallowing the exception, retrying silently, returning an empty result or deleting the failed attempt, and collapse each error once it is resolved. Failures that surface as explicit errors were recovered from far more often than failures that look like valid output (37 points more on average across nine models on one benchmark), and a linter that shows its errors and rejects the bad edit raised SWE-bench Lite from 15.0% to 18.0% on one model. The limits: in 135M-1.7B models the verbatim failed call made exact repeats more likely (though deleting it was worse), a model's own unflagged mistakes in its context raise its later error rate, and on HumanEval restarting fresh after 2-3 failed fixes beat continuing; so keep the diagnosis, cap it, and don't let failures pile up.

## When it applies

- **In the code:** Exceptions swallowed or retried silently; failures returned as empty or default results; a generic "operation failed" in place of the cause; failed attempts deleted before a retry; full stack traces or test logs passed untruncated; third-party error text passed through with steps the agent cannot take (a terminal command, a config change, a web page).
- **In traces:** Errors absent from the next model input; exact repeats of a call that already failed; runs of failed fixes of the same error; agents stopping after error text that asks for a step they cannot take; error observations thousands of lines long.
- **In eval results:** Recovery rate per injected failure and repeat rate of failed calls, alongside task success.
- **Probes:** A tool that fails deterministically on first use.

## How (outline)

1. Start from the harness as it is and find every place a failure is hidden from the model: exceptions swallowed, silent retries, a failed attempt deleted before the retry, a generic "operation failed" in place of the cause, or an empty or default result returned on failure. Inject a few failures (a tool that fails on first use, a silent wrong result, a third-party error message) and record recovery and repeated failed calls.
2. Return every failed action to the model in the next turn as a tool result marked as an error: the call (tool and arguments), the error type, the cause message and the exit code. Never turn a failure into an empty or plausible-looking result; on one benchmark agents recovered from silent failures 37 points less often than from explicit ones. Keeping the loop alive when a tool raises is 2.b.i.
3. Cap what goes in: keep the exception type and message, the frames in the agent's own code and the last lines of output; write the full trace or log to a file and give the path (2.c.i); make test and lint runs print a few lines, with ERROR and the reason on one line. Write the errors you own so they name the fix, and strip sentences from third-party error text that ask for steps the agent cannot take (a terminal command, a config change, a web page); in one study a one-sentence filter prompt raised recovery on expired credentials from 45% to 82%.
4. Do not retry from a context with the failure deleted: under greedy decoding that was the harness that repeated most. If the agent re-emits a failed call verbatim (measured in small models), replace the earlier verbatim call with a short harness-written note of what failed and why, or refuse exact repeats (7.b.i); keep the diagnosis either way.
5. Drop errors once they are resolved: when a later call succeeds or the tests pass, collapse the old error observation to a one-line stub, keep only the first of a run of identical format errors, and carry only unresolved errors through compaction (5.a.i). Don't let failures pile up: after 2-3 failed fixes of the same error, restart from the original task (optionally with a one-line note of what failed) or hand off, since non-thinking models make more mistakes as their own uncorrected errors accumulate in context.
6. Measure with paired runs on the same tasks and injected failures, the harness as is against errors kept, capped and dropped once resolved, per model: task success, recovery rate per injected failure by type (the agent's own call, credentials, permissions, rate limits, silent wrong results), exact and canonical repeat rate of failed calls, runs ending in a loop, steps and tokens. Re-run after a model change: the repetition effect shrank with model size, and thinking models did not self-condition.

## How to measure

- **experiment** (Tier 2): paired runs on a fixed task set with failures injected at fixed steps (a tool that fails deterministically on first use, a silent failure that returns a plausible but wrong result, a third-party error that names a step the agent cannot take): the harness as is against failures returned as error results with capped traces and collapsed once resolved, and optionally against a harness-written note in place of the verbatim failed call; per model: task success, recovery rate per injected failure, exact and canonical repeat rate of failed calls, runs ending in a loop, steps and tokens
- **monitor**: in production traces: the share of failed tool calls whose error text reaches the next model input; exact repeats of a call that already failed; consecutive failed attempts on the same error; the size of error observations; and recovery after errors by failure type (the agent's own call against credentials, permissions and rate limits)

## Expected impact

- **Quality:** mixed, medium: recovery from silent failures 37.15 points below explicit errors, averaged over nine models (Zhu, Jun 2026); lint errors shown with the bad edit rejected 18.0% vs 15.0% on SWE-bench Lite (Yang, May 2024); in 135M-1.7B models a kept verbatim failed call raised repeat probability from 0.06 to 0.54, while deleting it raised exact repeats from 31% to 80% (Gumaan, Aug 2026); wrong answers in a model's own history lowered later accuracy in non-thinking models of every size tested (Sinha, Sep 2025); fresh starts after 2-3 failed debug attempts beat continuing, e.g. 72.56% to 82.82% (Adnan, Jun 2025); a developer-facing step in the error text cut recovery from 82% to 45% (Xu, Sep 2026)
- **Cost:** mixed, small: error text and full traces add tokens unless capped (Carlini, Feb 2026); masking old observations, errors included, cut cost per instance by more than half in most configurations against the full history (Lindenbauer, Aug 2025); fresh starts used similar or fewer tokens, e.g. 108,289 to about 89,000 (Adnan, Jun 2025); filtering 949 error messages with a prompt cost $0.09 (Xu, Sep 2026)
- **Security:** mixed, small (unmeasured): Stack traces may leak internals.
- **Governance:** improves, small (unmeasured)
- **Brand:** mixed, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yichao 'Peak' Ji (Manus), "Context Engineering for AI Agents: Lessons from Building Manus"… (2025-07-18): "one of the most effective ways to improve agent behavior is deceptively simple: leave the wrong turns in the context." No numbers.
- Akshit Sinha, Arvindh Arun, Shashwat Goel, Steffen Staab, Jonas Geiping, "The Illusion of Diminishing Returns: Measuring Long Horizon… (2025-09-11): "as we increase the rate of injected errors into the context, accuracy at turn 100 consistently degrades further." Frontier non-thinking models (Kimi-K2, DeepSeek-V3, Qwen3-235B-Instruct-2507) "remain susceptible to self-conditioning"…
- Esmail Gumaan, "Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail"… (2026-08-24): Keeping the failed call and its error made a repeat more likely for all 6 models: "Over a fixed candidate set the probability of repeating the failed call rises from 0.06 to 0.54"; "the failed call's surface form accounts for 83% of the…
- Tobias Lindenbauer, Igor Slinko, Ludwig Felder, Egor Bogomolov, Yaroslav Zharov, "The Complexity Trap: Simple Observation Masking Is as… (2025-08-29): Observation masking "halves cost relative to the Raw Agent while matching, and sometimes slightly exceeding, the solve rate of LLM-Summary" (Qwen3-Coder 480B: 53.4% raw, 54.8% masking, 53.8% summary; Gemini 2.5 Flash with thinking: 40.4%…
- …and 6 more sources in `library/entries/keep-errors-in-context.yaml`.

## Caveats

No study isolates keeping versus hiding an error on a frontier agent: the closest measurements are a bundled linter change on one model (+3 points on SWE-bench Lite), a benchmark that compares explicit with silent tool failures, and a single-author study of 135M-1.7B models in which the verbatim failed call raised repeats while deleting it was worse. Failures that accumulate hurt: wrong answers in a model's own history lowered its later accuracy in non-thinking models (not fixed by scale, absent in one thinking family), and on HumanEval restarting fresh after 2-3 failed fixes beat continuing for all six models tested. What the error says matters as much as whether it is shown: a step the agent cannot take cut recovery from 82% to 45%, and for failures in the agent's own call the wording barely mattered.

## Related

- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)

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
