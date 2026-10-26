---
name: parallel-read-only-tools
description: "AOT optimization 6.b.i (Tier 3, Tuning): Parallel tool execution for read-only calls. Placeholder. Use when an agent shows: Average tool calls per tool-calling turn near 1 on tasks with independent lookups (parallelism unused); overlapping spans for calls that touch the same resource; calls that failed because a prerequisite in the same batch had not run."
---

<!-- Generated from library/entries/parallel-read-only-tools.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Parallel tool execution for read-only calls

> **Placeholder.** Generated from `library/entries/parallel-read-only-tools.yaml` (entry 6.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.b.i |
| Earlier id | P52 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it changes execution order and latency |
| Categories | Topologies: Parallelizing |
| Change | workflow / parallelization |

## What it is

Let the model put several independent read-only tool calls (searches, fetches, file reads) in one turn and have the harness run them at once, while calls that write, share state or need another call's result run one at a time in the order the model emitted them. It pays where a task has many slow, independent lookups: told to make three parallel search or scrape calls per turn, GPT-5 scored 68% against 66% on 100 BrowseComp tasks in half the turns, at 35.9% lower cost and 40.6% less time, and native parallel calls ran 1.61x to 2.76x faster than one call per step on parallel search questions. The gain shrinks where tool work is fast or sequential (1.04x on SWE-bench Lite, 1.40x once the harness declared each tool's reads and writes and kept decoding during calls), wider is not better (five or eight calls per turn scored 60% and 63%), and batching calls that depend on each other costs accuracy (GLM-4.5 completed 63.1% of compound tasks when parallelizing against 71.8% sequentially).

## When it applies

- **In the code:** Each tool marked read-only (safe to run together) or as having side effects, shared state or ordering needs, with unknown tools defaulting to serial; read-only calls in a batch dispatched concurrently; the rest run in model-emitted order; all results returned in one message before any text; a parallel-calls instruction in the prompt.
- **In traces:** Average tool calls per tool-calling turn near 1 on tasks with independent lookups (parallelism unused); overlapping spans for calls that touch the same resource; calls that failed because a prerequisite in the same batch had not run.
- **In eval results:** Accuracy, turns, cost and p95 latency with parallel calls off and on, on tasks with and without dependent calls; race-condition failures.
- **Probes:** Batches that mix reads and writes to the same resource, or hold a call that needs another call's output.

## How (outline)

1. Start from the baseline: the same agent, model and tasks with parallel calls off (disable_parallel_tool_use in Claude's tool_choice, or your provider's equivalent), and with them on but executed one at a time; record accuracy, turns, tokens, cost and p50/p95 wall-clock per task, and the average number of tool calls per tool-calling turn. Expect the gain to track how much slow, independent lookup work a task has: native parallel batches ran 1.61x to 2.76x faster than ReAct on 2-way and 8-way parallel search questions (gpt-3.5-turbo), but running a model's same-turn batches concurrently instead of one by one gave 1.04x on SWE-bench Lite (GPT-5.6 Sol).
2. Classify every tool by what it reads and writes. Search, fetch, grep, glob, file reads and other lookups can run together; anything with side effects, shared state (a shell session, a browser, a working directory) or an ordering requirement cannot. Default unknown tools to serial, and classify shell commands per command (one harness locked the whole repository for python, pytest and any command its rules did not match). Declaring a read set and a write set per tool lets the harness run non-conflicting calls together while conflicting ones keep the model's order.
3. Dispatch each batch in the harness, not the model: the provider APIs leave execution order, partial failure and races to you. Run the safe calls concurrently, run the rest in the order the model emitted them, and when a call fails cancel only the calls that depend on it. Return one result per call, all in the next message and before any text (results sent as separate messages teach Claude to stop batching), with is_error and a short reason for any call not run or that failed because its prerequisite had not completed; the model reissues it next turn.
4. Prompt for it, at a modest width: "whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially" plus "Only batch tool calls that are independent of each other." With GPT-5 on 100 BrowseComp tasks at a 100-turn limit, three to four search or scrape calls per turn scored 68% against 66% for one, in 23.8 against 45.7 turns, while five and eight scored 60% and 63%; a wide-then-narrow schedule (3, then 2, then 1 per turn) reached 74%, and letting the model choose reached 72%. Open-weight models gained little (DeepSeek-V3.2 38% to 39%), so measure before relying on it.
5. Keep dependent steps sequential: where later calls need earlier results, parallel scheduling cost GLM-4.5 8.7 points of task completion (63.1% against 71.8% sequential), and QwQ-32B put dependent calls in one batch and completed 29.36%. Leave those workflows serial, or plan them as an explicit dependency graph (the LLMCompiler planner ran 1.40x to 3.74x faster than ReAct).
6. Where tools are slow, also let decoding continue while calls run: returning placeholders (futures) and filling in results at turn boundaries gave 1.40x on SWE-bench Lite and 1.26x on BFCL web search with no significant accuracy change, and with no read/write declarations it still helped by overlapping decoding with serialized calls.
7. Measure paired against the baseline on tasks with and without dependent calls: accuracy, turns, cost and p95 latency per task, average calls per tool-calling turn, calls returned as is_error because a prerequisite had not run, and probes that put a read and a write to the same resource in one batch.

## How to measure

- **experiment** (Tier 3): paired runs on the same tasks and model with parallel calls off, on but executed one at a time, and on and concurrent, including tasks whose calls depend on each other: accuracy, turns, tokens and cost per task, p50/p95 wall-clock, and average tool calls per tool-calling turn; sweep the calls-per-turn instruction (1, 3, 5) and a wide-then-narrow schedule; add probes that put a read and a write to the same resource, or a call that needs another call's output, in one batch
- **monitor**: average tool calls per tool-calling turn, the share of batches that mix read-only and side-effecting calls, calls returned as is_error because a prerequisite had not run, turns per task, and p95 tool wall-clock per turn

## Expected impact

- **Quality:** mixed, medium: 68% against 66% in half the turns at three parallel calls per turn on 100 BrowseComp tasks, 60% and 63% at five and eight, 38% to 39% for DeepSeek-V3.2 (Lin, Feb 2026); 63.1% against 71.8% forced sequential for GLM-4.5 on compound tasks with dependencies, 29.36% for QwQ-32B, which batched dependent calls (Xu, Nov 2025); 79.3% against 79.0% on SWE-bench Lite, no significant change (Feng, May 2026); native parallel calls 77.00% against 72.47% on Movie Recommendation and 87.32% against 89.09% on ParallelQA for ReAct (Kim, Dec 2023). A tool with side effects classified read-only can race; no source measures that.
- **Cost:** improves, medium: $65.7 against $102.5 per 100 BrowseComp tasks (35.9% less) for three parallel calls per turn (Lin, Feb 2026); native parallel calls 1.81x to 3.33x cheaper than ReAct (Kim, Dec 2023); sequential scheduling raised DeepSeek-R1 from 11.6k to 12.6k tokens per task (Xu, Nov 2025)
- **Performance:** improves, medium: 904.2 s against 1,522.6 s per task (40.6% less) (Lin, Feb 2026); native parallel calls 1.61x to 2.76x faster than ReAct on parallel search questions (Kim, Dec 2023); 1.04x on SWE-bench Lite for concurrent batches alone, 1.40x with read/write declarations and decoding during calls (Feng, May 2026); 361.6 s against 423.6 s sequential for DeepSeek-R1 (Xu, Nov 2025)
- **Security:** mixed, small (unmeasured): No source measures it: a call with side effects classified read-only can run alongside, or ahead of, a check it should follow.
- **Governance:** none (unmeasured)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Kim et al., "An LLM Compiler for Parallel Function Calling", https://arxiv.org/abs/2312.04511 (2023-12-07): "latency speedup of up to 3.7x, cost savings of up to 6.7x, and accuracy improvement of up to ~9% compared to ReAct": the best cases, 3.74x and 6.73x on Movie Recommendation with gpt-3.5-turbo and +8.55 points on ParallelQA with LLaMA-2…
- Feng, Mao, Dutta, Gonzalez, "Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs"… (2026-05-14): SWE-bench Lite (n=300, GPT-5.6 Sol, real tool latency), resolve rate and speedup over SWE-agent: baseline 79.0%; same-turn batches run concurrently 79.0%, 1.04x; AsyncFC 79.3%, 1.40x. BFCL v3 multi-turn (n=150, GPT-4o, 5 s injected delay)…
- Lin, Liew, Savarese, Li (Salesforce AI Research), "W&D:Scaling Parallel Tool Calling for Efficient Deep Research Agents"… (2026-02-07): BrowseComp, first 100 tasks, GPT-5 medium effort, accuracy (turns) at a 100-turn limit: 1 call 66% (45.7), 2 calls 68% (27.1), 3 calls 68% (23.8), 5 calls 60% (19.9), 8 calls 63% (15.2); at a 10-turn limit 44% for 1 call against 56% for 8.…
- Xu, Huang, Liu, Yu, Deng, "TPS-Bench: Evaluating AI Agents' Tool Planning & Scheduling Abilities in Compounding Tasks"… (2025-11-03): Forced sequential against default parallel scheduling: GLM-4.5 task completion 71.8% against 63.1%; DeepSeek-R1 12.6k against 11.6k tokens and 423.6 s against 361.6 s; "Serial scheduling can effectively help the model reduce errors caused…
- …and 1 more sources in `library/entries/parallel-read-only-tools.yaml`.

## Caveats

The current-model accuracy and cost result rests on one study's first 100 BrowseComp tasks, where 68% against 66% is two tasks, and its headline 62.2% compares a full-set run with GPT-5 medium against the score OpenAI reported for GPT-5 high in a different harness, not a single-call run (Lin, Feb 2026). The speedup depends on the workload: concurrent batches alone gave 1.04x on SWE-bench Lite, the 1.40x also needs futures and per-tool read/write declarations, and the same paper's May 2026 version reported 1.44x with a 3.3-point lower resolve rate on GPT-5.2, not significant (Feng, May 2026). The loss on dependent calls comes from an LLM-judged benchmark whose same-model ablation gives numbers for two of four models (Xu, Nov 2025), the largest speedups are with gpt-3.5-turbo against ReAct (Kim, Dec 2023), and no source measures races or security effects of a misclassified tool.

## Related

- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)

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
