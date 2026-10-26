---
name: samples-before-verification
description: "AOT optimization 9.c.ii (Tier 3, Tuning): Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays. Placeholder. Use when an agent shows: answer disagreement across repeated runs of the same question."
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

Running several independent attempts and picking by majority vote or a judge raised accuracy (Genie 73.8% to 81.4% with 8 runs, at up to 2.1x cost). Before adding a generative verifier on top, compare it with the vote at equal compute: it needs 4-64x the compute to match, and pays only on hard, medium-difficulty problems from weak-to-medium generators. If you do verify, an ensemble of diverse weak verifiers weighted by estimated accuracy beat one strong verifier (87.7% against 72.2%).

## When it applies

- **In the code:** a single attempt per question; or a generative verifier or best-of-N step with no comparison against a plain vote
- **In traces:** answer disagreement across repeated runs of the same question
- **In eval results:** accuracy of vote against verifier at equal compute, split by difficulty

## How (outline)

1. Measure variance across repeated runs on the same questions; if low, stop here.
2. Add N parallel attempts with a vote or aggregator; paired eval at matched compute. At a fixed thinking budget, parallel traces with a majority vote beat forcing one trace to think longer.
3. Only then try a verifier, at the same compute, on the hard slice.

## How to measure

- **experiment** (Tier 3): paired eval, N attempts against one, and vote against verifier, at matched compute

## Expected impact

- **Quality:** improves, medium: Genie +7.6 points with 8 parallel runs (May 2026); verifier over vote: gains only on hard problems (2025)
- **Cost:** degrades, large: 0.23x to 2.13x cost; verifier ensembles far more
- **Performance:** degrades, small

## Evidence (summary)

- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Llama-3.1-8B GenRM-FT on MATH: GenRM needs 8x the compute of SC to match it, and 128x to beat SC's best by 3.8%; SC plateaus around 128 solutions. Qwen-2.5-7B GenRM-FT: SC peaks with 64x less compute; GenRM +5.4% at 512x. Llama-3.3-70B…
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Llama-3.1-8B GenRM-FT (32 verifications) vs SC: up to 30% relative improvement on MATH level 5 vs much less on level 1. AIME24 (trained on MATH): GenRM almost doubles SC's performance but needs 256x more compute; SC reaches its peak with…
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Fitted power laws on MATH: Llama-3.1-8B GenRM-FT S_opt ~ C^0.57, V_opt ~ C^0.39; Qwen-2.5-7B GenRM-FT S_opt ~ C^0.75, V_opt ~ C^0.32; Llama-3.3-70B GenRM-Base S_opt ~ C^0.69, V_opt ~ C^0.43. Up to 128 solutions x 128 verifications sampled.
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): Analytical upper bound assuming constant verifier accuracy (Llama-3-8B GenRM-FT, MATH): tokens per verification 2048 -> compute to match SC 8x, to beat 128x; 1024 -> 4x/64x; 512 -> 2x/32x; 256 -> 1x/16x. The authors note keeping accuracy…
- Singhi et al., "When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning"… (2025-04-01): "In most cases, at least 32 verifications are needed to achieve good results" (Llama-3.1-8B, MATH).
- …and 31 more sources in `library/entries/samples-before-verification.yaml`.

## Related

- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)

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
