---
name: bound-tool-output
description: "AOT optimization 2.c.i (Tier 3, Tuning): Bound tool output: cap it, or write it to a file the agent can read. Placeholder. Use when an agent shows: a single tool result over about 10% of the context window; context-overflow outcomes; a truncated result followed by re-running the same command, or by no narrowed follow-up at all; no requests for later pages although results were cut; cut results that no longer parse (broken JSON); fields or records the tool produced that never reached the model; answers that report a capped count as the total; with file offload, answers given without the agent reading the tool's output."
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

Cap big tool results by whole lines or records and say plainly what was cut, because agents rarely ask for the rest and neither they nor their verifiers notice a cut that is not marked. It pays where results overflow, not as a general cost lever: with no cap, one broad search can end a run (a harness that inlined every output aborted 65 of 100 BrowseComp-Plus tasks for GPT-5.6 Sol), while in public coding-agent traces the median tool result was 118 to 286 tokens and result size explained 4% of the variation in cost. How you bound matters as much as whether: a cut by character position broke every structured result it cut and cost 28% to 43% more tool calls, a capped list that did not say so led three current models to overclaim in 62% of answers (0% when it gave the true total), and file-only delivery cost GPT-5.1 11.3 points but Claude Opus 4.6 and Sonnet 4.6 nothing detectable, so inline what fits, offload the rest to a file the agent can read, and test the delivery for each model.

## When it applies

- **In the code:** tool results passed to the model whole, with no cap or file offload; a cap that slices serialized output at a fixed character position (keeping the front, or cutting the middle) instead of by whole lines or records; framework truncation defaults left as shipped; a cut result that does not say it was cut, the true total or how to narrow the request, or a capped list or bounded scan whose output reads as complete ("Found 20 document(s)" when more matched, "searched the full text" after a scan limit); offloaded output with nothing telling the agent which output is authoritative
- **In traces:** a single tool result over about 10% of the context window; context-overflow outcomes; a truncated result followed by re-running the same command, or by no narrowed follow-up at all; no requests for later pages although results were cut; cut results that no longer parse (broken JSON); fields or records the tool produced that never reached the model; answers that report a capped count as the total; with file offload, answers given without the agent reading the tool's output
- **In eval results:** context-overflow outcomes as a share of failures; task success, tool calls and tokens per task with results inline against offloaded, per model
- **Probes:** Tool results larger than the cap, structured (long JSON lists) and unstructured (logs), with the needed record or line near the end.

## How (outline)

1. Start from the harness as it is: from traces, list each tool's result sizes (median, 95th percentile, largest) and their share of the context, the results that were cut or overflowed, and commands re-run after a cut; log what each tool produced next to what the model received, because a run log shows only what was delivered (one harness cut a third of its 11,189 tool results while its largest prompt used 5.75% of the window). Expect the cap to matter at the tail, not the median: in 600 public coding-agent trajectories the median observation was 118 to 286 tokens and the 99th percentile 4,274 to 6,208, and observation size explained 4% of the variation in cost against 84% for turn count, so bound output to keep runs alive and evidence intact rather than to cut the bill.
2. Never run without a cap: a seed harness that appended every output whole aborted 65 of 100 BrowseComp-Plus tasks on context overflow with GPT-5.6 Sol, and each of four current models, editing its own harness, added output truncation in its first round. Return results that fit whole, and set the cap from result sizes on successful cases, not a framework default (in one survey, langchain-core kept the first 500 characters of a tool output and smolagents deleted the middle of any observation over 20,000 characters); VeRO's optimizers moved a 30 KB cap to 15-20 KB, and one that probed 15 KB found some tasks needed more output and settled on 17 KB.
3. Above the cap, cut by structure, not by character position: keep whole lines, rows or records, keep structured output parseable (trim long lists rather than the end of the text); a prefix slice at 6,000 characters broke every JSON result it cut and delivered one field in 4.7% of calls against 99.3% for its neighbor, while a row-aware cut broke none. Say in the result that it was cut, the true total and how to narrow the request (a line range, a filter, a more specific query): a capped search that opened "Found 20 document(s)" when 4,772 matched led three current models to overclaim in 62% of answers, against 0% when it said "Showing the first 20 of 4772", and verifiers accepted a false answer 30 of 30 times without the notice and 0 of 30 with it; in public coding-agent traces, 76.9% of actions after a cut with recovery guidance narrowed the query, against 44.0% after a bare marker. Do not count on paging: in one MCP middleware's logs agents never asked for a second chunk, so put the records most likely needed in the first one (whether the needed item was in the chunk mattered; its rank within it did not). For file reads, return a window the agent can move: a 100-line viewer resolved 18.0% of SWE-bench Lite against 14.3% at 30 lines and 12.7% for the whole file.
4. For output too long to inline, write it to a file and return the path with a short preview (Claude Code does this, and Cursor's agent reads the tail first; for JSON, the schema and one element of each list), and when the agent can also write output files of its own, say which output is authoritative: under file-only delivery two GPT models skipped the tool's report in 53% and 60% of trajectories and answered from their own higher-precision files; a three-sentence instruction naming the report as authoritative raised accuracy 6.3 to 7.9 points for three GPT models, an instruction to round correctly did not help, and inlining reports that fit (offloading only the rest) recovered 4.6 and 8.0 points for two of them.
5. When the agent can run code, have it filter and aggregate the full result there and return only the slice it needs (Anthropic's example: five rows of a 10,000-row sheet): in one study, code run over large JSON responses beat reading them on filtering and aggregation questions for all 15 models, reading won single-value lookups for 10 of 15, and giving the code a reduced response (one element per list) beat giving it only the schema. Treat a model-written summary of a large output as a quality bet, not a cost one: re-scoring 600 trajectories, summarizing large observations with a cheaper model saved no more than cutting them (within 0.17 points), and both saved 11% to 19% only when nearly every observation was reduced.
6. Re-run the cases that overflowed or were cut, then run paired comparisons for each model you serve (old against new cap, position cut against whole-record cut, a cut with and without a notice of the true total, inline against offload): task success, tool calls and tokens per task, overflow outcomes, the share of produced fields and records that reached the model, and whether the agent's answer (and a reviewer given only the delivered output) treats a cut result as complete; on the same tasks, file-only delivery cost GPT-5.1 11.3 points and Claude Opus 4.6 and Sonnet 4.6 nothing detectable, and a bad cut showed up first as 28% to 43% more tool calls, not as wrong answers.

## How to measure

- **experiment** (Tier 3): paired runs on the same tasks for each model you serve, cases that overflowed or were cut first: the current delivery against the change (no cap against a cap; the old against the new cap; a cut by character position against a cut by whole lines or records; a cut with and without a notice of the true total and how to narrow the request; inline-if-it-fits against file-only offload, with and without naming the authoritative output); report task success, tool calls and tokens per task (priced with cache reads), context-overflow outcomes, cut results that no longer parse, the share of produced fields and records that reached the model, and answers that treat a cut result as complete, including when a reviewer sees only the delivered output
- **monitor**: in production traces: result size per tool (median, 95th percentile, largest) against the cap; results cut and how much each lost; cut results that fail to parse or that do not say they were cut; context-overflow outcomes; what follows a cut (a narrowed query, the same command re-run, a request for the next page, or nothing); for offloaded outputs, whether the agent read the file before answering

## Expected impact

- **Quality:** mixed, medium: with no cap a seed harness aborted 65 of 100 BrowseComp-Plus tasks on context overflow for GPT-5.6 Sol, and the self-evolved harness that added truncation (with time limits, compaction and review) answered 57 of them, 34% to 90% overall (Xu, Sep 2026); a capped result that did not say so led Claude Sonnet 5, GPT-5.6 Sol and Gemini 3.1 Pro to overclaim in 62% (result totals), 100% (search scope) and 100% (estimates) of answers, against 0%, 8% and 20% with a notice (Jeffries, Oct 2026); a 100-line file window resolved 18.0% of SWE-bench Lite against 12.7% for whole files and 14.3% at 30 lines (Yang, May 2024); code over large JSON responses beat reading them on filtering and aggregation for all 15 models but lost single-value lookups for 10 of 15 (Kate, Oct 2025); file-only delivery cost GPT-5.1 11.3 and GPT-5.2 7.9 points and Claude Opus 4.6, Sonnet 4.6 and GPT-5.4 nothing detectable, and inlining what fits or naming the authoritative output won back 4.6 to 8.0 points (Zhang, Oct 2026); a cut by character position delivered one field in 4.7% of calls, left answers unchanged where the agent had a second route (15/15 against 14/15) and got 0 of 5 right against 3 of 6 on a production trace (Sehgal, Oct 2026); raising how often the needed file came first in a capped list from 50% to 70%-72% of test tasks moved file-localization accuracy by -2.8 to +2.2 points across five models (Petrova, Jun 2026); in VeRO the run that cut context-overflow errors from 13 to 1 moved those tasks into timeouts (16 to 23) with passes unchanged (VeRO, Feb 2026)
- **Cost:** mixed, small: file delivery cut mean input tokens per item from 60.9k to 52.8k (GPT-5.1), 65.7k to 61.8k (GPT-5.2) and 64.3k to 55.7k (GPT-5.4) (Zhang, Oct 2026); a cut by character position used 5% to 14% more input tokens than a whole-record cut because the agent made more calls (Sehgal, Oct 2026); in 600 re-scored coding-agent trajectories (two open models) observation size explained 4% of the variation in cost against 84% for turn count, cutting or summarizing large observations saved 11% to 19% only when nearly every observation was reduced and fell toward zero, negative in two of four cells, when only large ones were (Kumar, Oct 2026); passing data between tools in code rather than through context avoids about 50,000 tokens in Anthropic's example (estimate, Nov 2025)
- **Performance:** mixed, small: file delivery took 9.1 against 7.2 steps for two GPT models (Zhang, Oct 2026); a cut by character position raised median tool calls per run from 53 to 68 and 76 (Sehgal, Oct 2026); running conditionals in code saves waiting for the model to evaluate them (Anthropic, Nov 2025, unmeasured)
- **Governance:** improves, small: a cut the output does not mention cannot be caught downstream: given the same false answer, three verifiers accepted it 30 of 30 times in each of three families when the tool output omitted its cap or scan limit and 0 of 30 when it stated them, and an audit prompt run with Codex and Claude Code found unmarked cuts in two open-source agents (a search tool that truncated matched lines at 500 characters without a marker) (Jeffries, Oct 2026); a run log shows only what the model received, so logging what each tool produced beside it exposed fields that reached the model in 4.7% of calls (Sehgal, Oct 2026); single-turn tests on one production archive

## Evidence (summary)

- paper §A.4 (2026-02): 30KB to 15KB (Tools-B=89), 20KB (Filesystem-B=178), 17KB (Tools-B=178, after probing 15KB on 16 samples and seeing some tasks needed more). Filesystem run cut ContextLengthExceeded from 13 to 1.
- repo figure_04 (100 runs, five benchmarks) (2026-02): MAX_TOOL_OUTPUT_CHARS lowered 16 times, raised 13. The only frequently-touched constant lowered more often than raised.
- Jediah Katz (Cursor), "Dynamic context discovery", https://cursor.com/blog/dynamic-context-discovery (2026-01-06): Truncation "can lead to data loss"; the file approach "has resulted in fewer unnecessary summarizations when reaching context limits." No number.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): Illustrative: a 10,000-row sheet filtered to pending orders; "The agent sees five rows instead of 10,000." Not measured.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): With direct calls "the full call transcript flows through twice. For a 2-hour sales meeting, that could mean processing an additional 50,000 tokens" (estimate). Also: "models may be more likely to make mistakes when copying data between…
- …and 11 more sources in `library/entries/bound-tool-output.yaml`.

## Caveats

Most of the evidence on how to bound is narrow: the position-cut result is one harness and one unnamed model (15 runs per arm), file-only delivery cost two GPT models 7.9 and 11.3 points (the smaller loss not significant after correction) but two Claude models nothing detectable on one simulator benchmark, the cut-notice results are single-turn tests (one tool output, one answer) on one production archive with notice wording that also carried instructions, and the file-window and code-over-JSON results come from GPT-4 Turbo in 2024 and single-turn question answering. The current-model case for having a cap at all is bundled: the self-evolved harness that took GPT-5.6 Sol from 34% to 90% on BrowseComp-Plus also added time limits, compaction and review, and in VeRO's TerminalBench-2 runs the commit that cut context-overflow errors from 13 to 1 moved those tasks into timeouts (16 to 23) with passes unchanged at 27 of 89. The cost bound comes from re-scoring public trajectories of two open models with simulated caching, and the finding that agents never page from one middleware's logs, published by its builders without a count of the responses covered. No controlled study yet varies cap size, truncation style or file offload on current frontier coding agents at matched compute, and none measures security.

## Related

- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
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
