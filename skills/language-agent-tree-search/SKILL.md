---
name: language-agent-tree-search
description: "AOT optimization 7.c.v (Tier 4, Restructuring): Language Agent Tree Search (LATS). Placeholder. Use when an agent shows: Nodes expanded and LLM calls per item; tokens and wall time per item; restore or replay time, its share of wall time and failed snapshots; the critic's value of intermediate states against the outcomes of continuations from them; value of the chosen trajectory against its actual outcome; destructive actions executed during exploration."
---

<!-- Generated from library/entries/language-agent-tree-search.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Language Agent Tree Search (LATS)

> **Placeholder.** Generated from `library/entries/language-agent-tree-search.yaml` (entry 7.c.v). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.v |
| Earlier id | P34 (Reasoning & Search, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it replaces a single chain with a search |
| Categories | Orchestration: Scaling compute |
| Change | workflow / planning |

## What it is

Run the agent as a Monte Carlo tree search over its own actions: sample several next actions, execute each, score the new states with the model, reflect on failed endings, and back the scores up the tree until a branch succeeds or the budget runs out. It is only as good as its value signal, and it needs an environment whose states can be restored and kept free of irreversible side effects: against a single ReAct run it raised success on web, coding and incident-diagnosis tasks (VisualWebArena 18.9% to 26.4%, SWE-bench Lite +23% relative across five models, root-cause accuracy 39.8% to 91.3%, though those baselines got about a quarter of the tokens), but on Terminal-Bench 2.1 with GPT-5.6 Luna, where model critics ranked early states barely better than chance, MCTS moved success only from 63.4% to 64.0% at 3.81 times the cost, while checking only claimed-final states in a forked sandbox reached 72.4% at 2.2 times. At matched spend the results split: retries beat LATS on HumanEval (92.0% at $2.51 against 88.0% at $134.50) and no search policy beat best-of-N significantly on MLE-bench, while tree search beat re-ranking whole runs on VisualWebArena (32.0% against 30%), MCTS beat best-of-N on OSWorld with GPT-5-mini (64.27% against 54.29%, with more samples and about 3.6 times the wall time per solved task), and a value-guided tree beat majority voting at equal tool-call and token budgets on multi-hop QA, where an unguided tree lost. It cost 3.8 to 14.1 times the tokens or dollars of a single run in most studies (over 50 times simple retries on HumanEval) and 7.6 to about 10 times the wall time.

## When it applies

- **In the code:** A search loop over agent actions: UCT or best-first selection, expansion of several sampled actions executed in the environment, a model-scored value (often with self-consistency), reflections on failed endings, backpropagation, and a way to restore earlier states (reset and replay, a commit per node, snapshots). Flag search over actions with side effects and no restore path or destructive-action gate, search guided by a critic of intermediate states whose ranking accuracy was never measured, and search with no simpler baseline at a matched budget.
- **In traces:** Nodes expanded and LLM calls per item; tokens and wall time per item; restore or replay time, its share of wall time and failed snapshots; the critic's value of intermediate states against the outcomes of continuations from them; value of the chosen trajectory against its actual outcome; destructive actions executed during exploration.
- **In eval results:** Success against ReAct with retries, best-of-N with a vote or judge, and a completion check in a forked sandbox, at equal tokens and wall time, per model and task difficulty.
- **Judge:** Rate reflections used as value estimates.
- **Probes:** Multi-step tasks with recoverable mistakes.

## How (outline)

1. Start from the cheap baselines on the same model and tasks: the ReAct loop (7.d.iii) with retries on failed checks, best-of-N whole runs picked by a vote, a judge or a test (9.c.ii), and a completion check in a forked sandbox (step 4), each given the tokens and wall time the search would get; add search only where a gap remains. Read-only diagnosis (searching over hypotheses with tools that only list, search and compare logs and metrics) suits it best, since every branch is safe to explore.
2. Make every node restorable before searching: checkpoint filesystem and process state together (rolling back only the filesystem leaves the process with stale state), preferably with incremental copy-on-write snapshots: on SWE-bench MCTS trajectories, restoring by replaying the recorded actions took 27.7 s on average and other coupled snapshot methods 0.8 to 3.4 s, against 1.86 ms for an incremental sandbox, and state management took 23% to 48% of search time on a VM-snapshot runtime against 1% to 2%. Check that a restored state matches the original and count failed snapshots. Stock Docker checkpointing does not preserve background processes reliably and replays can diverge; where states cannot be restored, use one-step lookahead (sample K actions, a critic picks one) plus selection among whole runs, or simulate candidate actions with an LLM world model instead of executing them.
3. Validate each proposed action before running it, before adding any search: that alone raised WebArena-lite success from 47.74% to 53.55%, most of the gain, while adding naive tree search lowered it to 51.61% until destructive actions were handled. Keep exploration off irreversible actions: flag likely destructive actions before execution (form submits, Enter, buttons that are not navigation) and confirm after (POST, PUT, DELETE or PATCH requests), defer them until the search commits, drop the states they make unreachable, and on live systems restrict expansion to non-destructive actions or gate them (10.b.i).
4. Measure the value signal before building on it: score states at several depths and compare the scores with the outcomes of a few continuations from each state. Never expand without one: at the same budget an unguided tree scored 0.215 exact match against 0.268 for majority voting, and a value-guided one 0.309. On terminal tasks, critics ordered states a quarter of the way in correctly 49% to 56% of the time (chance is 50%) and MCTS on them added nothing; there, spend the critic on claimed-final states instead: give it execute access to disposable forks of the candidate and the initial state, and on rejection resume the actor from the candidate with the findings (63.4% to 72.4% at 2.2 times the cost; restarting from scratch scored 66.3% at 1.6 times the cost of resuming), capped at about three claims (9.b.iii).
5. Build the search: select by UCT, expand 3 to 5 deduplicated sampled actions and execute each, and score the new states with the model after it sees the observation, judging siblings jointly rather than one at a time (64.27% against 57.96% on OSWorld) plus self-consistency over several samples with state-specific value prompts; where a sound signal such as tests or the environment's reward exists, use it (9.a.i). Write a reflection on each failed ending and feed it to later expansions, and backpropagate, backing up the maximum value where one success is enough (a mean backup fell to 45.42%).
6. Bound, parallelize and check the pick: cap iterations or nodes per task and search time per state, shift from exploring to exploiting as the budget runs out (budget-aware selection raised exact match from 0.309 to 0.388), expand siblings and environments concurrently with prefix caching on (4.4 and 2.1 times faster on OSWorld), and on reasoning models choose the effort setting that leaves room for enough nodes in the time budget (maximum effort completed 18.5 search nodes per run against 62.8 at medium, 1.b.i). Choose the final answer with a checked selector: the value function picked the resolving patch 73% of the time and a separate discriminator 84%, so compare the selector's choice with outcomes.
7. Measure against step 1 at matched tokens and wall time, per model and task difficulty: success, tokens, LLM calls, wall time, restore time and failed restores, the critic's ranking accuracy at intermediate states, and destructive actions executed during exploration; re-check after a model upgrade, since the gain flipped with backbone capability and a completion critic stopped helping significantly with stronger actors.

## How to measure

- **experiment** (Tier 4): before building the search, the critic's pairwise accuracy on states at several depths against the outcomes of a few continuations from each; then a paired eval of the tree search against ReAct with retries, best-of-N with a vote or judge, and a completion check in a forked sandbox, at matched tokens and wall time, same model and value signal, split by task difficulty and per model and reasoning-effort setting: success, tokens, LLM calls, wall time, destructive actions executed during exploration
- **monitor**: nodes expanded and budget-hit rate per task; tokens, LLM calls and p50/p95 wall time; state restore or replay time, its share of wall time, failed snapshots and replay divergence; agreement between the chosen trajectory's value and its actual outcome; critic false accepts and false rejects at claimed-final states; destructive actions flagged, blocked and executed

## Expected impact

- **Quality:** mixed, medium: gains over a single ReAct run: VisualWebArena 18.9% to 26.4% (Koh, Jul 2024), SWE-bench Lite +23% relative across five models (Antoniades, Oct 2024), root-cause accuracy 39.8% to 91.3% (Naakka, May 2026); at matched spend simpler methods matched or won: HumanEval 88.0% against 92.0% for retries (Kapoor, Jul 2024), GAIA best-of-N 63.03 against beam search 56.97 and tree search 55.76 at equal sampling width (Zhu, Jun 2025), no search policy significantly better than best-of-N (Brilliantov, Sep 2026), Terminal-Bench 2.1 MCTS 64.0% against 63.4% without search while a completion check in a forked sandbox reached 72.4% (Xu, Oct 2026); search won: VisualWebArena 32.0% against 30% for re-ranking at about equal compute (Koh, Jul 2024), MCTS beat best-of-N at equal trajectory count on 3 of 4 backbones (Chen, Feb 2025), OSWorld 64.27% against 54.29% for best-of-N with N=3 (Tang, Feb 2026), a value-guided tree 0.338 exact match at 5 tool calls against 0.334 for majority voting at 20 (Li, Mar 2026)
- **Cost:** degrades, large: LATS cost $134.50 against $2.51 for retries on HumanEval (Kapoor, Jul 2024); SWE-Search $576.00 against $40.86 with GPT-4o and about 5x on four other models (Antoniades, Oct 2024); MCTS agents used 7.2x to 10.1x ReAct's tokens (Yu, Oct 2024); LATS averaged 71.0 LLM calls per request (Kim, Jun 2025); 156K against 41K tokens per investigation (Naakka, May 2026); MCTS cost 3.81x no search on Terminal-Bench 2.1, the critic 31.3% of it (Xu, Oct 2026)
- **Performance:** degrades, large: tree search took 749.2 to 972.1 s per VisualWebArena task against 68.3 to 87.7 s for a reactive agent (Gu, Nov 2024); 9.1 against 1.2 minutes per root-cause investigation (Naakka, May 2026); 1116.5 against 313.37 s per solved OSWorld task (Tang, Feb 2026); some LATS tasks ran over 2 hours (Kapoor, Jul 2024); restoring by replay took 27.7 s per restore, and state management took 23% to 48% of MCTS time on a VM-snapshot sandbox against 1% to 2% with incremental checkpoints (Dong, May 2026); expanding 16 children in parallel instead of 1 cut LATS latency by 196.3 s on average (Kim, Jun 2025)
- **Security:** degrades, medium: exploratory branches execute real actions; irreversible ones (placing an order, submitting a form) cannot be backtracked, so search outside a sandbox needs a non-destructive action space or gating (Koh, Jul 2024; Gu, Nov 2024); a conservative pre-execution check flagged actions of which about 37% were truly destructive (Dihan, Dec 2025); sandbox forks do not isolate writes to external databases or shared services (Xu, Oct 2026)
- **Governance:** none (unmeasured)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Zhou et al., "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models", https://arxiv.org/abs/2310.04406 (2023-10-06): "state-of-the-art pass@1 accuracy (92.7%) for programming on HumanEval with GPT-4"; "average score of 75.9" on WebShop with GPT-3.5, "comparable to gradient-based fine-tuning"
- Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan, "AI Agents That Matter"… (2024-07-01): Mean of five runs: LATS (GPT-4) 88.0% at $134.50 total; Retry (GPT-4) 92.0% at $2.51; Warming (GPT-4) 93.2% at $2.45; GPT-4 alone 89.6% at $1.93; LATS (GPT-3.5) 80.4% at $9.49. "Reflexion and LDB cost over 50% more than the warming…
- Jing Yu Koh, Stephen McAleer, Daniel Fried, Ruslan Salakhutdinov, "Tree Search for Language Model Agents", https://arxiv.org/abs/2407.01476 (2024-07-01): GPT-4o agent: VisualWebArena 18.9% to 26.4% ("39.7% relative"), WebArena 15.0% to 19.2%; Llama-3-70B: VWA 7.6% to 16.7%, WA 7.6% to 10.1%. On 200 VWA tasks: no search 24.5%, budget c=5 32.0%, c=20 37.0%; re-ranking "starts to plateau…
- Antonis Antoniades, Albert Örwall, Kexun Zhang, Yuxi Xie, Anirudh Goyal, William Wang, "SWE-Search: Enhancing Software Agents with Monte… (2024-10-26): SWE-bench Lite resolve rate, without and with search: GPT-4o 25.7% to 31.0%, GPT-4o-mini 13.0% to 17.0%, Qwen-2.5-72B 18.0% to 24.7%, DeepSeek-V2.5 16.3% to 21.0%, Llama-3.1-70B 13.6% to 17.7%; "a 23% relative improvement". API cost…
- …and 13 more sources in `library/entries/language-agent-tree-search.yaml`.

## Caveats

Most gains are measured against a single ReAct run; where spend was matched, retries beat LATS on HumanEval, best-of-N led on GAIA (matched on samples, not tokens), no search policy beat best-of-N significantly on MLE-bench and MCTS added 0.6 points (not significant) on Terminal-Bench 2.1, while tree search beat re-ranking on VisualWebArena, MCTS beat best-of-N on three of four backbones with a trained reward model, a value-guided tree beat voting at small budgets with 20B to 30B open models (one study, no confidence intervals), and MCTS beat best-of-N on OSWorld in a comparison that gave the search 5 children and 20 iterations against N=3 with no token counts, so not at equal compute despite the paper's claim. The value signal is the bottleneck: a ground-truth reward reached 43.5% against 37.0% with GPT-4o's estimate, terminal-task critics ordered states a quarter of the way in correctly 49% to 56% of the time (chance 50%), an unguided tree fell below voting (0.215 against 0.268 exact match), naive tree search lowered WebArena-lite success from 54.84% to 51.61% until destructive-action handling was added, and SWE-Search's value function picked the resolving patch 73% of the time. Search needs states that can be restored: live websites and stock Docker checkpointing do not reliably provide them, incremental sandboxes now restore in 1.86 ms but that study measured overhead, not success, and the one production study fell from 91.3% on its benchmark to 65.1% on 37 incidents. Gains shrink as models get stronger: the Terminal-Bench MCTS arm used a light configuration (at most two children, a snapshot every five turns), a completion critic gained nothing significant with GPT-6 Astra or Claude Opus 5.5 actors on 15 hard tasks, and on MLE-bench maximum reasoning effort starved the search of nodes.

## Related

- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)

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
