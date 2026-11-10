---
name: bound-tool-output
description: "AOT optimization 2.c.i (Tier 3, Tuning): Bound tool output: cap it, or write it to a file the agent can read. Placeholder. Use when an agent shows: a single tool result over about 10% of the context window; context-overflow outcomes; a truncated result followed by re-running the same command; cut results that no longer parse (broken JSON); fields or records the tool produced that never reached the model; with file offload, answers given without the agent reading the tool's output."
---

<!-- Generated from library/entries/bound-tool-output.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Bound tool output: cap it, or write it to a file the agent can read

> **Placeholder.** Generated from `library/entries/bound-tool-output.yaml` (entry 2.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.c.i |
| Earlier id | T02 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Tools: Trimming results; Context: Filtering input |
| Change | tool / transformation (tune) |
| Also covers | Token-efficient tool responses |

## What it is

Keep big tool results from flooding the context: return what fits whole, cut larger ones by whole lines or records and say so, and put the rest in a file the agent can read. A bounded view helps: a 100-line file window resolved 18.0% of SWE-bench Lite against 12.7% for whole files (GPT-4 Turbo, 2024), and code run over a large JSON result beat reading it on filtering and aggregation questions for all 15 models in one study. How you bound matters as much as whether: a cut by character position broke every structured result it cut and cost 28% to 43% more tool calls, and file-only delivery cost GPT-5.1 11.3 points but Claude Opus 4.6 and Sonnet 4.6 nothing detectable, while inlining what fits or naming the authoritative output won back 4.6 to 8.0 points, so test the delivery for each model.

## When it applies

- **In the code:** tool results passed to the model whole, with no cap or file offload; a cap that slices serialized output at a fixed character position (keeping the front, or cutting the middle) instead of by whole lines or records; framework truncation defaults left as shipped; a cut result that does not say it was cut or how to get the rest; offloaded output with nothing telling the agent which output is authoritative
- **In traces:** a single tool result over about 10% of the context window; context-overflow outcomes; a truncated result followed by re-running the same command; cut results that no longer parse (broken JSON); fields or records the tool produced that never reached the model; with file offload, answers given without the agent reading the tool's output
- **In eval results:** context-overflow outcomes as a share of failures; task success, tool calls and tokens per task with results inline against offloaded, per model
- **Probes:** Tool results larger than the cap, structured (long JSON lists) and unstructured (logs), with the needed record or line near the end.

## How (outline)

1. Start from the harness as it is: from traces, list each tool's result sizes (median, 95th percentile, largest) and their share of the context, the results that were cut or overflowed, and commands re-run after a cut; log what each tool produced next to what the model received, because a run log shows only what was delivered (one harness cut a third of its 11,189 tool results while its largest prompt used 5.75% of the window).
2. Return results that fit whole, and set the cap from result sizes on successful cases, not a framework default (in one survey, langchain-core kept the first 500 characters of a tool output and smolagents deleted the middle of any observation over 20,000 characters); VeRO's optimizers moved a 30 KB cap to 15-20 KB, and one that probed 15 KB found some tasks needed more output and settled on 17 KB.
3. Above the cap, cut by structure, not by character position: keep whole lines, rows or records, keep structured output parseable (trim long lists rather than the end of the text), and say in the result that it was cut, how much was dropped and how to get the rest (a page, a line range, a narrower query). A prefix slice at 6,000 characters broke every JSON result it cut and delivered one field in 4.7% of calls against 99.3% for its neighbor, while a row-aware cut broke none. For file reads, return a window with paging: a 100-line viewer resolved 18.0% of SWE-bench Lite against 14.3% at 30 lines and 12.7% for the whole file.
4. For output too long to inline, write it to a file and return the path with a short preview (Cursor's agent reads the tail first; for JSON, the schema and one element of each list), and when the agent can also write output files of its own, say which output is authoritative: under file-only delivery two GPT models skipped the tool's report in 53% and 60% of trajectories and answered from their own higher-precision files; a three-sentence instruction naming the report as authoritative raised accuracy 6.3 to 7.9 points for three GPT models, an instruction to round correctly did not help, and inlining reports that fit (offloading only the rest) recovered 4.6 and 8.0 points for two of them.
5. When the agent can run code, have it filter and aggregate the full result there and return only the slice it needs (Anthropic's example: five rows of a 10,000-row sheet): in one study, code run over large JSON responses beat reading them on filtering and aggregation questions for all 15 models, reading won single-value lookups for 10 of 15, and giving the code a reduced response (one element per list) beat giving it only the schema.
6. Re-run the cases that overflowed or were cut, then run paired comparisons for each model you serve (old against new cap, position cut against whole-record cut, inline against offload): task success, tool calls and tokens per task, overflow outcomes, and the share of produced fields and records that reached the model; on the same tasks, file-only delivery cost GPT-5.1 11.3 points and Claude Opus 4.6 and Sonnet 4.6 nothing detectable, and a bad cut showed up first as 28% to 43% more tool calls, not as wrong answers.

## How to measure

- **experiment** (Tier 3): paired runs on the same tasks for each model you serve, cases that overflowed or were cut first: the current delivery against the change (the old against the new cap; a cut by character position against a cut by whole lines or records; inline-if-it-fits against file-only offload, with and without naming the authoritative output); report task success, tool calls and tokens per task, context-overflow outcomes, cut results that no longer parse, and the share of produced fields and records that reached the model
- **monitor**: in production traces: result size per tool (median, 95th percentile, largest) against the cap; results cut and how much each lost; cut results that fail to parse; context-overflow outcomes; a command re-run right after a cut; for offloaded outputs, whether the agent read the file before answering

## Expected impact

- **Quality:** mixed, medium: a 100-line file window resolved 18.0% of SWE-bench Lite against 12.7% for whole files and 14.3% at 30 lines (Yang, May 2024); code over large JSON responses beat reading them on filtering and aggregation for all 15 models but lost single-value lookups for 10 of 15, and exact-match accuracy fell 7% (GPT-4o) to 91% (Mistral-large) as responses grew from 10K to 80K tokens (Kate, Oct 2025); file-only delivery cost GPT-5.1 11.3 and GPT-5.2 7.9 points and Claude Opus 4.6, Sonnet 4.6 and GPT-5.4 nothing detectable, and inlining what fits or naming the authoritative output won back 4.6 to 8.0 points (Zhang, Oct 2026); a cut by character position delivered one field in 4.7% of calls, left answers unchanged where the agent had a second route (15/15 against 14/15) and got 0 of 5 right against 3 of 6 on a production trace (Sehgal, Oct 2026); in VeRO the run that cut context-overflow errors from 13 to 1 moved those tasks into timeouts (16 to 23) with passes unchanged (VeRO, Feb 2026)
- **Cost:** improves, small: file delivery cut mean input tokens per item from 60.9k to 52.8k (GPT-5.1), 65.7k to 61.8k (GPT-5.2) and 64.3k to 55.7k (GPT-5.4) (Zhang, Oct 2026); a cut by character position used 5% to 14% more input tokens than a whole-record cut because the agent made more calls (Sehgal, Oct 2026); passing data between tools in code rather than through context avoids about 50,000 tokens in Anthropic's example (estimate, Nov 2025)
- **Performance:** mixed, small: file delivery took 9.1 against 7.2 steps for two GPT models (Zhang, Oct 2026); a cut by character position raised median tool calls per run from 53 to 68 and 76 (Sehgal, Oct 2026); running conditionals in code saves waiting for the model to evaluate them (Anthropic, Nov 2025, unmeasured)

## Evidence (summary)

- paper §A.4 (2026-02): 30KB to 15KB (Tools-B=89), 20KB (Filesystem-B=178), 17KB (Tools-B=178, after probing 15KB on 16 samples and seeing some tasks needed more). Filesystem run cut ContextLengthExceeded from 13 to 1.
- repo figure_04 (100 runs, five benchmarks) (2026-02): MAX_TOOL_OUTPUT_CHARS lowered 16 times, raised 13. The only frequently-touched constant lowered more often than raised.
- Jediah Katz (Cursor), "Dynamic context discovery", https://cursor.com/blog/dynamic-context-discovery (2026-01-06): Truncation "can lead to data loss"; the file approach "has resulted in fewer unnecessary summarizations when reaching context limits." No number.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): Illustrative: a 10,000-row sheet filtered to pending orders; "The agent sees five rows instead of 10,000." Not measured.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): With direct calls "the full call transcript flows through twice. For a 2-hour sales meeting, that could mean processing an additional 50,000 tokens" (estimate). Also: "models may be more likely to make mistakes when copying data between…
- …and 7 more sources in `library/entries/bound-tool-output.yaml`.

## Caveats

How a result is bounded decides whether bounding helps: a cut by character position silently dropped whole fields and broke every structured result it cut, with the cost showing first as extra tool calls rather than wrong answers (one harness, one unnamed model, 15 runs per arm), and file-only delivery cost two GPT models 7.9 and 11.3 points (the smaller loss not significant after correction) but two Claude models nothing detectable on one simulator benchmark, because the GPT models answered from their own files instead of the tool's report. In VeRO's TerminalBench-2 runs every cap change came bundled with other edits: the run that cut context-overflow errors from 13 to 1 moved those tasks into timeouts (16 to 23) with passes unchanged at 27 of 89, and three tasks that passed before regressed in all three runs, which the authors put down to the output-length and prompt changes optimizers tend to make. The file-window and search-cap results used GPT-4 Turbo in 2024 and the code-over-JSON results come from single-turn question answering rather than an agent loop, so measure on your own agent and models.

## Related

- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)

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
