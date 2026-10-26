---
name: graph-of-thought
description: "AOT optimization 7.c.iv (Tier 4, Restructuring): Graph-of-Thought. Placeholder. Use when an agent shows: Per item: nodes and model calls, input and output tokens per node, aggregation and refine steps, scorer verdicts beside an independent check, budget-cap hits, wall-clock time. In a single-call agent, errors that grow with input size (dropped, duplicated or miscounted elements) mark where a split-and-merge graph could help."
---

<!-- Generated from library/entries/graph-of-thought.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Graph-of-Thought

> **Placeholder.** Generated from `library/entries/graph-of-thought.yaml` (entry 7.c.iv). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.iv |
| Earlier id | P33 (Reasoning & Search, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it replaces a single chain with a search |
| Categories | Orchestration: Scaling compute |
| Change | workflow / planning |

## What it is

Graph-of-Thought runs one task as a graph of model calls: split the input into parts, generate and score several candidates per part, keep the best, then merge the partial results and refine the merged answer. It paid on merge-shaped tasks that one call gets wrong as inputs grow: on sorting it made fewer errors than Tree-of-Thought at lower cost (median error about 62% lower in the original paper; 12.7 against 18.4 mistakes at 5.0 against 15.9 cents in a re-implementation), but it cost far more than one chain-of-thought call. Independent 2025-2026 comparisons are mixed: graph methods mostly beat chain-of-thought on Game of 24 and multi-hop QA but trailed it or direct answering on GPQA and step-by-step math at several times the tokens; on a six-task suite GoT ranked below tree search and had the highest share of runs both costlier and worse. No study compares GoT with self-consistency at matched tokens.

## When it applies

- **In the code:** A controller that runs a fixed or generated graph of model calls on one task: split the input, generate several candidates per part, score and keep the best, aggregate partial results and refine the merge (GoT's Generate, Score, KeepBestN, Aggregate). Flag independent nodes run one after another, every node on the strongest model, an LLM scorer where code could check, and no cap on depth, branching, nodes or tokens.
- **In traces:** Per item: nodes and model calls, input and output tokens per node, aggregation and refine steps, scorer verdicts beside an independent check, budget-cap hits, wall-clock time. In a single-call agent, errors that grow with input size (dropped, duplicated or miscounted elements) mark where a split-and-merge graph could help.
- **In eval results:** Accuracy against chain-of-thought and self-consistency at matched tokens, sliced by input size; cost and latency per correct answer.
- **Judge:** Rate whether each merge kept all information from its inputs without duplication (retention and redundancy, as in GoT's document-merging score).
- **Probes:** Tasks whose sub-results must be merged, at growing input sizes, plus a sequential control.

## How (outline)

1. Start from one chain-of-thought call and from self-consistency or best-of-N with a vote at the same total tokens (9.c.ii); add a graph only where one call fails on inputs that split into parts whose results can be merged (sorting, set intersection, keyword counting, merging documents, questions that combine several sources) and the failures grow with input size. On step-by-step math (GSM8K, MATH-500) graphs lost to a single call with GPT-4o-mini and Qwen2.5-7B, at far more tokens where counted.
2. Write the graph of operations for the task class up front, as the original framework does (a controller executes a fixed plan through a per-task prompter, parser and scorer): split the input into parts small enough that one call usually gets each right (16 elements in the paper), Generate several candidates per part (k=5), Score them and KeepBestN(1), Aggregate pairs of partial results with several attempts each, Score and keep the best again, and add a refine step on the merged result; merge level by level up to the final answer.
3. Score with code wherever the task allows (the paper's sorting and set scorers count errors); an LLM scorer is noisier, and in one benchmark replacing search strategies' heuristic evaluator with an exact one raised quality and cut run-to-run variance. Without a trustworthy score, keeping the best of k is close to a random pick.
4. Hold cost down: run independent nodes in parallel and cache repeated calls (parallel execution took GoT sorting from 259 s to 30 s per instance); trim few-shot examples in node prompts, which dominate once the task is split finely; pass compact summaries instead of whole parent contexts; route leaf subtasks to a smaller model while planning and the final merge stay on the strong one, under a token budget that caps depth, branching and node count (one router cut output tokens 79.1% against Adaptive GoT).
5. Tune k, part size and depth on a held-out set with cost capped at the untuned level (one framework cut sorting mistakes from 12.7 to 12.1 at no extra cost).
6. Measure on a paired set against chain-of-thought and self-consistency at matched input-plus-output tokens, per model and per input size, over repeated runs (the top strategy won only 77% of head-to-head runs in one benchmark): accuracy on a deterministic grader, tokens, wall-clock latency and cost per correct answer.

## How to measure

- **experiment** (Tier 4): paired eval of the graph against one chain-of-thought call and against self-consistency or best-of-N at matched input-plus-output tokens, per model and sliced by input size, over repeated runs with a deterministic grader: accuracy, tokens, wall-clock latency, cost per correct answer, and the share of runs both costlier and worse
- **monitor**: per item: nodes and model calls, input and output tokens per node, aggregation and refine steps, budget-cap hits, latency p50 and p95; on a sampled subset, scorer verdicts against an independent check

## Expected impact

- **Quality:** mixed, medium: gains on merge-shaped tasks: sorting 128 numbers, median error about 62% below ToT (Besta, Aug 2023), 12.7 against 18.4 mistakes in a re-implementation (Fricke, Feb 2026); a generalized GoT on Qwen3-30B beat CoT on multi-hop QA (MoreHopQA 73.0 vs 68.0) and Game of 24 (72.0 vs 58.0) but trailed it on GPQA (59.6 vs 63.1) (Liu, Mar 2026); GPT-4.1 Nano six-task suite 0.336 vs CoT 0.279 and CoT-SC 0.227, below ToT-BFS 0.415 (Potamitis, Dec 2025); below direct answering on MATH-500 (73.24 vs 74.96) and GSM8K (88.76 vs 90.95) with Qwen2.5-7B (Hao, May 2025); graph reasoning 82.0 vs CoT 89.5 on GSM8K under the same grader (Huang, Mar 2026)
- **Cost:** degrades, large: many calls per item: costs "much higher" than IO and CoT (Besta, Aug 2023); 9,468 output and 16,826 input tokens per GPQA question against 4,965 and 247 for CoT (Liu, Mar 2026); mean cost 0.0099 against 0.0003 for CoT and 0.0014 for CoT-SC, and the highest joint cost-quality failure rate of nine strategies, 43.3% (Potamitis, Dec 2025); cheaper than ToT: over 31% at 128 elements (Besta, Aug 2023), 5.0 against 15.9 cents (Fricke, Feb 2026)
- **Performance:** degrades, large: rounds of dependent calls: 259 s per sorting instance and 145 s per document merge run sequentially, 30 s and 32 s with parallel nodes (Fricke, Feb 2026); 22.89 to 116.03 s per question for a generalized GoT on Qwen3-30B (Liu, Mar 2026)
- **Security:** none (unmeasured)
- **Governance:** none (unmeasured)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Besta et al., "Graph of Thoughts: Solving Elaborate Problems with Large Language Models", https://arxiv.org/abs/2308.09687 (2023-08-18): "increasing the quality of sorting by 62% over ToT, while simultaneously reducing costs by >31%" (median error at 128 elements). Against the cheaper ToT variant GoT "only negligibly improves" at 32 elements and has ≈61% and ≈69% fewer…
- Maciej Besta et al., "Demystifying Chains, Trees, and Graphs of Thoughts", https://arxiv.org/abs/2401.14295 (2024-01-25): "In terms of cost-effectiveness, chain-based prompting schemes generally outperform their tree-based and graph-based counterparts", since tree and graph schemes "often involve multiple rounds of prompting"; "When it comes to the quality of…
- Tushar Pandey, Ara Ghukasyan, Oktay Goktas, Santosh Kumar Radha, "Adaptive Graph of Thoughts: Test-Time Adaptive Reasoning Unifying Chain… (2025-02-07): GPQA Diamond with shuffled options: gpt-4o-mini 37.4 (IO) to 49.5 (+32.4%, relative), CoT 38.6; gpt-4o 39.4 to 57.6 (+46.2%). Standard unshuffled GPQA Diamond: 54.6 to 55.1 (+0.9%), where CoT (49.0) and AIoT (48.0) fell below IO. HotpotQA…
- Qianyue Hao, Sibo Li, Jian Yuan, Yong Li, "RL of Thoughts: Navigating LLM Reasoning with Inference-time Reinforcement Learning"… (2025-05-20): Qwen2.5-7B-Instruct, mean of 5 runs, GoT against direct answering (DirectQA): MATH-500 73.24 vs 74.96, GSM8K 88.76 vs 90.95, GPQA 33.26 vs 31.16, StrategyQA 75.69 vs 68.53; average 67.74 vs 66.40. On average GoT ranked below rStar (70.80)…
- …and 4 more sources in `library/entries/graph-of-thought.yaml`.

## Caveats

Most gains come from hand-built graphs on synthetic merge tasks run with GPT-3.5 on 100 samples per task, or from papers proposing a successor method; in some independent comparisons graph methods trailed chain-of-thought or direct answering on GPQA and step-by-step math, and GoT ranked below tree search on a six-task suite and had the highest share of runs both costlier and worse. No source compares GoT with self-consistency or best-of-N at matched tokens, and none tests the original GoT on reasoning models. The later graph methods (Adaptive GoT, Network-of-Thought) are different designs; Adaptive GoT reports no cost figures, and an independent rerun with token counts found it worse than chain-of-thought on HotpotQA (72.0 vs 86.0) at substantially more tokens. Results vary run to run (the top strategy won only 77% of head-to-head runs in one benchmark), and only two of these sources report repeated runs.

## Related

- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)

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
