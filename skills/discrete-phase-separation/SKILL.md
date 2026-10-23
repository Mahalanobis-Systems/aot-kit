---
name: discrete-phase-separation
description: "AOT optimization 5.c.i (Tier 4, Restructuring): Discrete phase separation. Placeholder. Use when an agent shows: Phase boundaries; handoff size vs full history."
---

<!-- Generated from library/entries/discrete-phase-separation.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Discrete phase separation

> **Placeholder.** Generated from `library/entries/discrete-phase-separation.yaml` (entry 5.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 5.c.i |
| Earlier id | P47 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it splits the work into isolated phases |
| Categories | Context: Isolating subtasks |
| Change | workflow / orchestration |

## What it is

Research, plan, execute; pass only distilled conclusions.

## When it applies

- **In the code:** Phases with distilled handoffs rather than shared history.
- **In traces:** Phase boundaries; handoff size vs full history.
- **In eval results:** Quality vs monolithic run.
- **Judge:** Rate handoffs for completeness.
- **Probes:** Tasks where premature implementation hurts.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Handoff schema.
- **Examples:** Design-first probes.
- **Benchmark:** Coding benchmark.
- **Production:** Rework rate.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium
- **Cost:** improves, small
- **Performance:** degrades, small
- **Security:** none
- **Governance:** improves, medium: Review at boundaries.
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Dex Horthy (HumanLayer), "Getting AI to Work in Complex Codebases"… (2025-08-29): "We use a "research, plan, implement" workflow"; reports shipping 35k LOC to BAML in 7 hours (3 on research/plans, 4 on implementation). Anecdotal, no controlled comparison.

## Related

- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)

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
