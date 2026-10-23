---
name: self-discover-reasoning
description: "AOT optimization 3.c.i (Tier 3, Tuning): Self-Discover reasoning structures. Placeholder. Use when an agent shows: Plan structure per task; modules chosen."
---

<!-- Generated from library/entries/self-discover-reasoning.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Self-Discover reasoning structures

> **Placeholder.** Generated from `library/entries/self-discover-reasoning.yaml` (entry 3.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 3.c.i |
| Earlier id | P35 (Reasoning & Search, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it changes the reasoning prompt |
| Categories | Prompts: Sizing reasoning effort |
| Change | prompt / instructions |

## What it is

Self-Discover reasoning structures

## When it applies

- **In the code:** A module-selection step before solving; a composed reasoning plan.
- **In traces:** Plan structure per task; modules chosen.
- **In eval results:** Accuracy on hard, heterogeneous reasoning.
- **Judge:** Rate whether the chosen structure fits the task.
- **Probes:** A mix of task types needing different reasoning.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Examples:** Mixed-type probes.
- **Benchmark:** BigBench-Hard style.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium: Catalog cites up to 32 percent over fixed CoT.
- **Cost:** degrades, small: One extra planning call.
- **Performance:** degrades, small
- **Security:** none
- **Governance:** none
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Zhou et al., "Self-Discover: Large Language Models Self-Compose Reasoning Structures", https://arxiv.org/abs/2402.03620 (2024-02-06): Improves GPT-4 and PaLM 2 "by as much as 32% compared to Chain of Thought"; beats CoT-Self-Consistency "by more than 20%, while requiring 10-40x fewer inference compute"

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
