---
name: graph-of-thought
description: "AOT optimization 7.c.iv (Tier 4, Restructuring): Graph-of-Thought. Placeholder. Use when an agent shows: Graph size; aggregation steps."
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

Graph-of-Thought

## When it applies

- **In the code:** Graph of thoughts with aggregation and refinement edges.
- **In traces:** Graph size; aggregation steps.
- **In eval results:** Accuracy on tasks with interdependent steps; cost.
- **Judge:** Rate aggregation quality.
- **Probes:** Tasks needing merged partial results.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Graph operations terminate.
- **Examples:** Merge probes.
- **Benchmark:** Sorting or set-operation benchmarks.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium: Narrow task class.
- **Cost:** degrades, large
- **Performance:** degrades, large
- **Security:** none
- **Governance:** none
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Besta et al., "Graph of Thoughts: Solving Elaborate Problems with Large Language Models", https://arxiv.org/abs/2308.09687 (2023-08-18): "increasing the quality of sorting by 62% over ToT, while simultaneously reducing costs by >31%"

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
