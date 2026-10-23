---
name: reflection-loop
description: "AOT optimization 7.c.i (Tier 3, Tuning): Reflection loop. Placeholder. Use when an agent shows: Iterations per item; whether critiques change the output."
---

<!-- Generated from library/entries/reflection-loop.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Reflection loop

> **Placeholder.** Generated from `library/entries/reflection-loop.yaml` (entry 7.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.i |
| Earlier id | P37 (Feedback & Iteration, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it adds a refine step graded against a metric |
| Categories | Orchestration: Scaling compute |
| Change | workflow / reflection |

## What it is

Generate, grade against a metric, refine.

## When it applies

- **In the code:** A self-critique call and a threshold; refinement loop.
- **In traces:** Iterations per item; whether critiques change the output.
- **In eval results:** Gain per iteration.
- **Judge:** Rate critiques for specificity.
- **Probes:** Outputs with detectable defects.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Threshold and iteration cap.
- **Examples:** Planted-defect probes.
- **Benchmark:** Writing or reasoning benchmark.
- **Production:** Iterations per item.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium: VeRO T26: Knight's reflect tool is part of a much stronger baseline.
- **Cost:** degrades, medium
- **Performance:** degrades, medium
- **Security:** none
- **Governance:** none
- **Brand:** improves, small

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback", https://arxiv.org/abs/2303.17651 (2023-03-30): "improving by ~20% absolute on average in task performance" over one-step generation

## Related

- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)

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
