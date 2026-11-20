---
name: tree-of-thought
description: "AOT optimization 7.c.vii (Tier 4, Restructuring): Tree-of-Thought. Placeholder. Use when an agent shows: Nodes expanded, depth and branching per item; pruned and backtracked branches; LLM calls, tokens and wall-clock per item; evaluator score of the chosen path next to the ground truth; share of searches that hit the budget or end without a solution."
---

<!-- Generated from library/entries/tree-of-thought.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Tree-of-Thought

> **Placeholder.** Generated from `library/entries/tree-of-thought.yaml` (entry 7.c.vii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.vii |
| Earlier id | P32 (Reasoning & Search, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it replaces a single chain with a search |
| Categories | Orchestration: Scaling compute |
| Change | workflow / planning |

## What it is

Replace one reasoning chain with a search: the model proposes several next steps, an evaluator (a rule check, a trained verifier or probe, or the model itself) scores the partial solutions, and the search keeps the best or backtracks. It pays on narrow tasks where early steps decide the outcome and partial states can be judged reliably: Game of 24 rose from 4% with CoT to 74% on GPT-4, ToT with a rule check on each step reached 81.8% against 75.6% for 8-sample self-consistency on Qwen3-8B at similar tokens, and on open-weight thinking models beam search over thinking steps scored by a hidden-state probe beat 256-sample self-consistency on all 15 model and benchmark pairs with 19.7% to 68.5% fewer tokens. Against cheaper baselines the gain often disappears: tree search needed an evaluator at least 90% accurate to beat re-ranking, PRM-guided tree search showed no significant gain over best-of-N despite higher cost, DeepSeek-V3.2 with thinking on solved 92% of Game of 24 in one call against 30% for ToT with thinking off, and on Blocksworld GPT-5 alone solved every instance it was given while Qwen3-14B needed ToT with thinking on (47 of 50, against 23 in one call) at 330k tokens per instance. Its authors put the cost at 5 to 100 times the generated tokens of CoT.

## When it applies

- **In the code:** A search controller: several candidate next steps per node, an evaluator that scores partial solutions (the model's value or vote, a trained verifier or hidden-state probe, or a rule or execution check), breadth-first or beam search keeping the best b, or depth-first with backtracking, and a node or token budget. Flag a one-prompt imitation ("imagine three experts") presented as ToT, a model self-evaluator where a rule or execution check exists, a search that only revises the last step when the checker can name the earlier decision that caused the failure, a search with no fallback answer when it ends empty, and no comparison against the same model in one call with thinking on or against self-consistency or best-of-N at equal tokens.
- **In traces:** Nodes expanded, depth and branching per item; pruned and backtracked branches; LLM calls, tokens and wall-clock per item; evaluator score of the chosen path next to the ground truth; share of searches that hit the budget or end without a solution.
- **In eval results:** Accuracy against the same model in one call with thinking on and against self-consistency or best-of-N at matched tokens, split by difficulty; evaluator ranking accuracy on labeled partial solutions; tokens and latency.
- **Judge:** The partial-solution evaluator is the judge: check its ranking accuracy against ground truth before relying on it (tree search needed at least 90% to beat re-ranking).
- **Probes:** Puzzles with dead ends.

## How (outline)

1. Start from the cheap baselines on your own items: the same model in one call with thinking on or higher effort (1.b.i), and self-consistency or best-of-N at the same token budget (9.c.ii); consider a search only for the items those miss, where an early wrong step dooms the answer and partial states can be checked, and route only those to it (a low average verifier score across samples served as the difficulty estimate). Re-check the need on every model upgrade, since stronger models gained less: best-of-N beat search at 72B, and on Blocksworld GPT-5 solved in one call every instance it was given, where Qwen3-14B solved 23 of 50 in one call with thinking on and 47 of 50 with ToT.
2. If the moves and the goal can be written down, have the model write the successor function and goal test in code and run plain BFS or DFS: that solved all 1,362 Game of 24 instances with about 2 LLM calls in total, where ToT makes about 100 calls per problem.
3. Otherwise define a thought as one checkable step (an equation, a SQL clause, a line of code, a plan action, one derived fact), propose several candidates per node and keep the best b (ToT kept b = 5), scoring partial states with the most reliable evaluator you have: a rule or execution check first (execution feedback raised discriminator accuracy by up to 30.2 points; with exact arithmetic, state-transition and test checks on each step, ToT on Qwen3-8B averaged 81.8% over five tasks against 75.6% for 8-sample self-consistency, at 7.0k against 6.5k generated tokens), then a trained verifier, then the model's own value or vote. Measure the evaluator's ranking accuracy on labeled partial solutions before wiring it in; tree search needed at least 90% to beat re-ranking.
4. Use a search that can back up: depth-first or best-first with pruning of states rated impossible, not a fixed-depth breadth-first pass (ToT's BFS won 9.47% of 5-number Countdown games against 60.00% for MCTS). When the checker can name the earlier decisions that make a state fail, jump back to the latest of them and cache the failing combination rather than revising the last step: against ToT on Qwen3-8B that raised mean success from 81.8% to 84.2% with 12.0 instead of 19.0 verifier calls. Cap nodes, tokens and wall-clock, stop on the first verified solution, and return a fallback answer when the search ends empty.
5. On an open-weight thinking model you serve yourself, search inside the reasoning trace rather than across prompts: split the thinking at paragraph breaks, score each prefix with a small probe on the model's hidden states trained on labeled traces, and at fixed intervals (every 200 tokens in one study) prune the lowest-scoring traces and branch from the best prefixes so the children share their KV cache, starting only after enough reasoning has accumulated (12,000 tokens there). With 256 traces per question this beat 256-sample self-consistency on all 15 model and benchmark pairs (HMMT-24 on Qwen3-4B-Thinking 50.8 to 65.0) with 19.7% to 68.5% fewer tokens; it needs hidden-state access, so it does not apply to API-only models.
6. Branch only where a step needs it: a cheap check before each expansion cut ToT beam-search output tokens by 78.3% and 78.9% on Qwen3-32B, at accuracy 0.97 and 0.86 against 0.98 and 0.87, but on LLaMA3-8B the cuts were 37.8% to 73.4% with accuracy drops, so re-check accuracy on your model. Run the b expansions and their evaluations in parallel, and to cut wall time expand the likely next branches before the evaluator returns and end deep straggler branches early: across four ToT and MCTS algorithms that gave average speedups of 1.8 to 3 times for depth-first and 1.2 to 1.9 times for breadth-first search, with average accuracy unchanged or slightly higher.
7. Measure on held-out items with ground truth the search never sees: accuracy against both baselines at matched tokens, split by difficulty, plus tokens, LLM and verifier calls, p50 and p95 latency, and the share of searches that end without a solution.

## How to measure

- **experiment** (Tier 4): paired eval on held-out items with ground truth the search never sees: ToT against the same model in one call with thinking on or higher effort, and against self-consistency or best-of-N at matched tokens, split by difficulty; accuracy, tokens, LLM and verifier calls, p50 and p95 latency, share of searches that end without a solution
- **monitor**: per item: nodes expanded, depth, branching and pruning, LLM and verifier calls, tokens and wall-clock, budget-hit and fallback rates; on a regularly audited sample, the evaluator's scores of partial states against a rule check or ground truth

## Expected impact

- **Quality:** mixed, medium: gains where one pass fails early and partial states can be judged: Game of 24 4% to 74% on GPT-4 (Yao, May 2023); logic proofs 72.0 to 83.1 on GPT-4o (He, Apr 2025); with a rule check per step 81.8% vs 75.6% for 8-sample self-consistency on Qwen3-8B (Song, Sep 2026); beam search over thinking steps above 256-sample self-consistency in all 15 cells, e.g. HMMT-24 50.8 to 65.0 on Qwen3-4B-Thinking (Yang, Aug 2026); Blocksworld 47 of 50 with ToT and thinking on vs 23 of 50 in one call on Qwen3-14B (Hamm, May 2026); no gain over cheaper selection when the evaluator is weak or the model strong: tree search 67.5 vs re-ranking 70.3 on Spider (Chen, Feb 2024), PRM beam search 71.8 vs best-of-8 72.7 (Cinquin, Oct 2025), best-of-N best at 72B (Liu, Feb 2025); thinking on alone 92% vs ToT with thinking off 30% on Game of 24 (Hao, Mar 2026); GPT-5 alone solved all Blocksworld instances it was given (Hamm, May 2026)
- **Cost:** degrades, large: $0.74 and 5.5k completion tokens per Game of 24 case vs $0.47 for 100 CoT samples; 5 to 100 times CoT's tokens by the authors' estimate (Yao, May 2023); about 100 LLM calls per Game of 24 problem vs about 2 in total for a coded search (Katz, Apr 2024); PRM beam search 20.2 vs 8.2 (x10^7) generated tokens for best-of-8 at the same accuracy (Cinquin, Oct 2025); ToT with thinking on 330k tokens per Blocksworld instance vs 231k with it off (Hamm, May 2026); cheaper than wide sampling when branches share prefixes: 1.6M to 4.2M tokens per question for beam search over thinking steps vs 2.3M to 8.5M for 256-sample self-consistency, 19.7% to 68.5% fewer (Yang, Aug 2026); branching only where needed cut ToT output tokens 78.3% to 78.9% on Qwen3-32B; on LLaMA3-8B cuts were 37.8% to 73.4%, with accuracy drops (Li, Sep 2025)
- **Performance:** degrades, large: serial generate-then-evaluate rounds: tree search 262.8 to 405.2 s per Bird example vs 16.4 to 24.4 s for re-ranking (Chen, Feb 2024); ToT on GPT-4o 0.30 to 2.13 min per logic problem vs 0.08 to 0.12 for CoT and 0.21 to 1.02 for o3-mini (He, Apr 2025); beam search over thinking steps 1,177 to 2,179 s per competition-math question on Qwen3-4B vs 3,338 to 5,358 s for 256-sample self-consistency on one GPU (Yang, Aug 2026); expanding likely branches before the evaluator returns gave 1.8 to 3 times average speedups for depth-first and 1.2 to 1.9 times for breadth-first ToT (Zhong, May 2026)
- **Security:** none (unmeasured)
- **Governance:** none (unmeasured)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", https://arxiv.org/abs/2305.10601 (2023-05-17): "in Game of 24, while GPT-4 with chain-of-thought prompting only solved 4% of tasks, our method achieved a success rate of 74%". Other Game of 24 results: CoT self-consistency over 100 samples 9.0%, an oracle best of 100 CoT samples 49%…
- Ziru Chen, Michael White, Raymond Mooney, Ali Payani, Yu Su, Huan Sun, "When is Tree Search Useful for LLM Planning? It Depends on the… (2024-02-16): "advanced planning methods demand discriminators with at least 90% accuracy to achieve significant improvements over re-ranking"; with oracle discriminators, tree search agents "consistently underperform the other two when the…
- Michael Katz, Harsha Kokel, Kavitha Srinivas, Shirin Sohrabi, "Thought of Search: Planning with Language Models Through The Lens of… (2024-04-18): ToT "performs ≈100 calls to the LLM" per Game of 24 problem and about 200 per crossword in the worst case. Projected over the datasets, ToT would make 102K calls on Game of 24 (1,362 problems), 5K on crosswords, 201K on BlocksWorld and…
- Charlie Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar, "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model… (2024-08-06): "with smaller generation budgets, beam search significantly outperforms best-of-N. However, as the budget is scaled up, these improvements greatly diminish, with beam search often underperforming the best-of-N baseline." On easy questions…
- …and 10 more sources in `library/entries/tree-of-thought.yaml`.

## Caveats

Most gains come from puzzles built to break left-to-right decoding (Game of 24, crosswords, Sudoku, Countdown, Blocksworld) or synthetic logic and contest math, often with a programmatic move generator or checker doing part of the work, and the headline 74% is against single-sample CoT: self-consistency over 100 samples scored 9.0%, and the 49% best-of-100 baseline is an oracle. The studies that compare against re-ranking or best-of-N with a trained or model evaluator (Chen, Snell, Liu, Cinquin) find tree search ties or trails them except on harder items with weaker models and a reliable evaluator; the two 2026 studies where search beat self-consistency used a rule check on every step (Song, one team, thinking mode not stated) or a probe trained on the model's own hidden states, which needs open weights and labeled traces (Yang, 30-problem contest sets, 256 traces and 1.6M to 4.2M tokens per question, no single-call baseline). The only ToT run with thinking on is one small Blocksworld study (Hamm: one model, 50 instances, results that swung with prompt configuration, and tables that do not match its text), and there GPT-5 alone solved every instance it was given; the closest other evidence shows thinking alone far above ToT with thinking off (Hao). Several studies are small (100 items per task in Hao and Li, 50 in Hamm, one model in Cinquin, 1,790 items in He), Katz's ToT call counts are estimates, not runs, and branching only where a check calls for it held accuracy on Qwen3-32B but cost accuracy on LLaMA3-8B (Li).

## Related

- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)

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
