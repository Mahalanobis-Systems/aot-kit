---
name: self-critique-evaluator
description: "AOT optimization 7.c.ii (Tier 3, Tuning): Self-critique evaluator loop. Placeholder. Use when an agent shows: Judge agreement over time."
---

<!-- Generated from library/entries/self-critique-evaluator.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Self-critique evaluator loop

> **Placeholder.** Generated from `library/entries/self-critique-evaluator.yaml` (entry 7.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.ii |
| Earlier id | P38 (Feedback & Iteration, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it adds a self-bootstrapped judge |
| Categories | Orchestration: Scaling compute |
| Change | workflow / reflection |

## What it is

Bootstrap a judge from its own traces; collusion risk.

## When it applies

- **In the code:** A pipeline that fine-tunes a judge on its own traces; periodic refresh.
- **In traces:** Judge agreement over time.
- **In eval results:** Human agreement; collusion tests between generator and evaluator.
- **Judge:** Meta-judge.
- **Probes:** Outputs built to fool the evaluator.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Examples:** Adversarial probes.
- **Benchmark:** Judge-agreement benchmark.
- **Production:** Drift in agreement.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium
- **Cost:** degrades, medium: Training cost up front.
- **Performance:** none
- **Security:** mixed, small
- **Governance:** mixed, medium: Self-referential evaluation.
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Wang et al., "Self-Taught Evaluators", https://arxiv.org/abs/2408.02666 (2024-08-05): "can improve a strong LLM (Llama3-70B-Instruct) from 75.4 to 88.3 (88.7 with majority vote) on RewardBench"

## Related

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
