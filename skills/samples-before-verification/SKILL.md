---
name: samples-before-verification
description: "AOT optimization 9.c.ii (Tier 3, Tuning): Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays. Placeholder. Use when an agent shows: answer disagreement across repeated runs of the same question; selection steps that return no usable candidate."
---

<!-- Generated from library/entries/samples-before-verification.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays

> **Placeholder.** Generated from `library/entries/samples-before-verification.yaml` (entry 9.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.c.ii |
| Earlier id | T46 |
| Tier | 3 (Tuning): extra compute within the existing design |
| Categories | Verification: Sizing verification; Orchestration: Scaling compute |
| Change | workflow / parallelization (tune) |
| Also covers | Self-consistency voting; Inference-time scaling; LLM-as-judge |

## What it is

Run several independent attempts and pick the answer by vote before paying for a verifier. A vote over 16 runs lifted search agents from 59.7% to 75.5%, 8 parallel runs lifted a data agent from 73.8% to 81.4% at up to 2.1x cost, and for code, keeping the candidate that passed the most available tests beat a same-model judge (453 against 376 of 500) at lower cost; on math a generative verifier needed 4-64x the compute to match the vote and paid only on hard, medium-difficulty problems from weak-to-medium generators. Verification pays where a vote cannot: on long-horizon tasks that deliver open-ended artifacts a ten-run vote added under a point while a verifier that checked claims against the workspace added about 4, and an ensemble of diverse weak verifiers weighted by estimated accuracy beat both the vote and the best single reward model (87.7% against 72.2% and 72.7%). Any selector is capped by what the attempts cover (a math vote stalled near 43% while coverage reached 98%), so measure coverage first.

## When it applies

- **In the code:** a single attempt per question; or a generative verifier, judge or best-of-N step with no comparison against a plain vote (or, for code, test execution) at equal cost; a verifier filter applied to a single attempt; a selection step with no fallback when it returns nothing usable
- **In traces:** answer disagreement across repeated runs of the same question; selection steps that return no usable candidate
- **In eval results:** coverage (any of N runs correct) against single-run and voted accuracy, and vote against verifier at equal compute, split by difficulty and by whether runs disagree

## How (outline)

1. Start from the baseline: run the current agent once per task on a labeled sample and record accuracy, cost and latency, then rerun each task 8 or more times to measure run-to-run disagreement and coverage (the share of tasks at least one run solves). If runs agree and coverage barely exceeds single-run accuracy, stop here: no selector can pick an answer the runs never produce. Run whole attempts in parallel only where each gets a fresh or resettable environment; where actions change shared state, drafting parallel plans and executing one lowered workflow accuracy by 4.2 to 4.6 points in one study.
2. Add N parallel whole-run attempts and submit the most common final answer, grouping equivalent answers (normalized text, equal values) before counting; compare against the single run in a paired eval at matched cost, charging every call in dollars. Expect the gain to taper: on search agents the vote reached 65.5%, 69.7%, 73.8% and 75.5% at 2, 4, 8 and 16 runs against 59.7% for one, while coverage reached 90.9%. At a fixed thinking budget, parallel traces with a majority vote beat forcing one trace to think longer.
3. Match the selection rule to the output. For code, run every candidate on the tests you have and keep the one that passes most, ties to the earliest: 453 of 500 correct against 376 for a same-model judge, at 12-49% lower API cost, and consulting the judge only on ties added cost and no accuracy (452). For short answers, vote: on identical math pools a same-model judge beat a three-way vote 186 to 182 of 292 (interval spanning zero) while the vote cost 12-21% less. Whatever the rule, fall back to the first nonempty candidate when selection returns nothing usable; this recovered 61 of 500 coding submissions at unchanged cost and turned an 8.6-point loss against one attempt into a 3.6-point gain.
4. Only then try a verifier or judge, at the same compute and on the hard slice, and keep it only if it beats the vote there. On math a generative verifier needed 4-64x the compute to match the vote. On search agents an LLM aggregator agent scored below the vote (68.9% against 75.5% at 16 runs) and other generative aggregators roughly matched a confidence-weighted vote, while a small selector trained on labeled pools added 3.1 points and, on WebQA, matched a 64-run vote with 8 runs; on GAIA a list-wise selector that compares all candidates beat the vote (63.03 against 56.8 with 4 runs, selection compute not matched). Do not filter a single attempt through a verifier (32.5% to 25.1% resolved on SWE-bench Verified); with several attempts take the top-scoring one (4.4 points above the best fixed threshold at 16 rollouts). Re-asking the same judges helps only when wrong answers do not fool most of them (nine calls instead of one: -0.3 to +0.1 points on MATH-500, +1.2 to +4.8 on GPQA). If you ensemble verifiers, weight diverse weak verifiers by estimated accuracy instead of averaging them (87.7% against 69.1% for a naive top-10 ensemble).
5. For long-horizon agents that deliver open-ended artifacts (reports, spreadsheets, patches), where a vote over whole artifacts barely helps (+0.3 and +0.8 points with ten runs on five workspace benchmarks), spend on verification against the environment: a verifier using the same model that tested disputed and agreed claims against the source files and data added 4.1 to 4.4 points at $1.44 to $3.92 per task. Its gains came where runs disagreed (6.1 points over the pool mean against 0.6 on unanimous pools), and 34% of values all ten runs agreed on were still wrong, so have it challenge the consensus too.
6. Size N and verification from a small labeled pilot rather than a fixed rule, and stop early: a pilot-calibrated plan came within 0.02-0.8 points of the best allocation in hindsight where every fixed rule lost at least 2.5 points somewhere, and stopping a task at its first accepted candidate kept success within 0.24 points while spending 5-25% less. A second model adds less than independence suggests (+1.6 points against a predicted +5) because models fail on the same problems, and fixed tests accept more wrong code from stronger generators, so rerun the pilot whenever the model changes.
7. Measure with a paired eval on the same labeled tasks at matched dollar cost: one run, N runs with a vote (or tests), and N runs with the verifier; report coverage, selection accuracy when a correct candidate exists, empty or failed selections, cost and latency, split by difficulty and by whether the runs disagree, and include a stronger model answering once (in one study it beat five cheaper models with extra samples outside programming).

## How to measure

- **experiment** (Tier 3): paired eval on the same labeled tasks at matched dollar cost with every call charged: one run, N runs with a vote (or test execution for code), and N runs with a judge or verifier; report coverage, selection accuracy when a correct candidate exists, empty selections, cost and latency, split by difficulty and by whether runs disagree, with a stronger model answering once as a reference
- **monitor**: in production traces: answer disagreement across parallel runs per task, how often selection returns no usable candidate, the share of tasks stopped at the first accepted candidate, and cost and latency per task; rerun the labeled pilot when the model, prompt or verifier changes

## Expected impact

- **Quality:** improves, medium: a 16-run vote lifted search agents from 59.7% to 75.5% and a learned selector to 78.6% (Zhou, Sep 2026); Genie +7.6 points with 8 parallel runs (Databricks, May 2026); test-based selection 453 against 376 of 500 coding cells for a same-model judge (Yang, Oct 2026); on open-ended workspace artifacts a ten-run vote added 0.3-0.8 points and a verifier checking claims against the workspace 4.1-4.4 (Zhang, Oct 2026); a verifier filter on a single SWE-bench attempt cut resolves from 32.5% to 25.1% (Iyengar, Oct 2026); verifier over vote gains only on hard problems (Singhi, Apr 2025)
- **Cost:** degrades, large: N runs cost about N single runs: 0.23x to 2.13x relative cost for 8 Genie runs (Databricks, May 2026); voting cost 12-21% less than a same-model judge on the same pools and test-based selection 12-49% less (Yang, Oct 2026); an evidence-checking verifier $1.44-$3.92 per task on top of ten runs (Zhang, Oct 2026); stopping at the first accepted candidate spent 5-25% less (Iyengar, Oct 2026); verifier ensembles far more (Saad-Falcon, Jun 2025)
- **Performance:** degrades, medium: parallel trajectories with aggregation raised Genie's average runtime from 5.5 to 9.5 min (Opus 4.6) and 3.8 to 8.2 min (GPT-5.4) (Databricks, May 2026); LLM aggregators took 12-258x the post-rollout GPU time of a small learned selector (Zhou, Sep 2026)

## Evidence (summary)

- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Llama-3.1-8B GenRM-FT on MATH: GenRM needs 8x the compute of SC to match it, and 128x to beat SC's best by 3.8%; SC plateaus around 128 solutions. Qwen-2.5-7B GenRM-FT: SC peaks with 64x less compute; GenRM +5.4% at 512x. Llama-3.3-70B…
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Llama-3.1-8B GenRM-FT (32 verifications) vs SC: up to 30% relative improvement on MATH level 5 vs much less on level 1. AIME24 (trained on MATH): GenRM almost doubles SC's performance but needs 256x more compute; SC reaches its peak with…
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Fitted power laws on MATH: Llama-3.1-8B GenRM-FT S_opt ~ C^0.57, V_opt ~ C^0.39; Qwen-2.5-7B GenRM-FT S_opt ~ C^0.75, V_opt ~ C^0.32; Llama-3.3-70B GenRM-Base S_opt ~ C^0.69, V_opt ~ C^0.43. Up to 128 solutions x 128 verifications sampled.
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Analytical upper bound assuming constant verifier accuracy (Llama-3-8B GenRM-FT, MATH): tokens per verification 2048 -> compute to match SC 8x, to beat 128x; 1024 -> 4x/64x; 512 -> 2x/32x; 256 -> 1x/16x. The authors note keeping accuracy…
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): "In most cases, at least 32 verifications are needed to achieve good results" (Llama-3.1-8B, MATH).
- …and 36 more sources in `library/entries/samples-before-verification.yaml`.

## Caveats

Most of the evidence is math, code and question answering, and the agent results come from single runs or replays of fixed candidate pools, several by the authors of the selector or verifier being tested (a learned search selector, a workspace verifier) and one a single-author reanalysis of public releases. A vote needs comparable final answers: on open-ended artifacts it barely helped and 34% of values all ten runs agreed on were wrong, and any selector is capped by coverage (a 16-run search vote reached 75.5% against 90.9% coverage). Parallel whole runs need a resettable environment, learned selectors need labeled pools (2,655 questions in one study), and fixed tests accept more wrong code from stronger generators (Spearman 0.97 across 17 models on HumanEval+), so results do not carry across models without re-measuring. In one sealed study a stronger model answering once beat five cheaper models given extra samples everywhere except programming (math 57 against 52 of 60, workflows 148 against 82 of 160).

## Related

- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:no-self-written-tests` (9.c.i, Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:test-first-fail-to-pass` (9.c.iv, Write a fail-to-pass test before the fix, and harden it against wrong fixes)

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
