---
name: continuous-task-loop
description: "AOT optimization 7.d.i (Tier 4, Restructuring): Continuous autonomous task loop. Placeholder. Use when an agent shows: Iterations; commits; rate-limit events."
---

<!-- Generated from library/entries/continuous-task-loop.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Continuous autonomous task loop

> **Placeholder.** Generated from `library/entries/continuous-task-loop.yaml` (entry 7.d.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.d.i |
| Earlier id | P51 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it changes the control loop |
| Categories | Orchestration: Shaping the loop |
| Change | workflow / control_flow |

## What it is

Continuous autonomous task loop

## When it applies

- **In the code:** A loop over a task queue with fresh context, git automation, rate-limit handling and iteration limits.
- **In traces:** Iterations; commits; rate-limit events.
- **In eval results:** Throughput; defect rate of produced work.
- **Judge:** Rate produced commits.
- **Probes:** A queue with a poison task.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Iteration cap; rate-limit backoff.
- **Examples:** Poison-task probes.
- **Production:** Cost per day; revert rate.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** mixed, medium
- **Cost:** degrades, large
- **Performance:** none
- **Security:** degrades, medium: Autonomous commits.
- **Governance:** mixed, medium: Needs hard limits.
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Geoffrey Huntley, "Ralph Wiggum as a “software engineer”", https://ghuntley.com/ralph/ (2025-07-14): "In its purest form, Ralph is a Bash loop. while :; do cat PROMPT.md | claude-code ; done". Says it has defects that are "identifiable and resolvable through various styles of prompts."

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)

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
