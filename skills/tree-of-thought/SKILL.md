---
name: tree-of-thought
description: "AOT optimization 7.c.vii (Tier 4, Restructuring): Tree-of-Thought. Placeholder. Use when an agent shows: Branch counts; pruned branches; tokens per item."
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

Tree-of-Thought

## When it applies

- **In the code:** Branching, evaluation and pruning code; a queue of partial solutions.
- **In traces:** Branch counts; pruned branches; tokens per item.
- **In eval results:** Accuracy on puzzle and planning tasks vs CoT; cost.
- **Judge:** Rate the partial-solution evaluator.
- **Probes:** Puzzles with dead ends.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Search terminates within budget.
- **Examples:** Dead-end probes.
- **Benchmark:** Puzzle or planning benchmark.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium: Narrow task class.
- **Cost:** degrades, large
- **Performance:** degrades, large
- **Security:** none
- **Governance:** none
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", https://arxiv.org/abs/2305.10601 (2023-05-17): "in Game of 24, while GPT-4 with chain-of-thought prompting only solved 4% of tasks, our method achieved a success rate of 74%"

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
