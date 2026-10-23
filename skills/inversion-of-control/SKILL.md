---
name: inversion-of-control
description: "AOT optimization 7.d.ii (Tier 4, Restructuring): Inversion of control. Placeholder. Use when an agent shows: Variety of action sequences across tasks."
---

<!-- Generated from library/entries/inversion-of-control.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Inversion of control

> **Placeholder.** Generated from `library/entries/inversion-of-control.yaml` (entry 7.d.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.d.ii |
| Earlier id | P50 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it changes who owns the control flow |
| Categories | Orchestration: Shaping the loop |
| Change | workflow / control_flow |

## What it is

Goal plus tools; humans supply guardrails at the ends.

## When it applies

- **In the code:** Minimal orchestration code; the agent decides the sequence.
- **In traces:** Variety of action sequences across tasks.
- **In eval results:** Quality on open-ended tasks.
- **Judge:** Rate whether autonomy was used well.
- **Probes:** Open-ended tasks.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Examples:** Open-ended probes.
- **Benchmark:** Agentic benchmark.
- **Production:** Cost per task; outcome quality.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** mixed, medium: VeRO: Knight did best with the least prescriptive template.
- **Cost:** degrades, medium
- **Performance:** degrades, medium
- **Security:** degrades, small
- **Governance:** degrades, medium: Less predictable.
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Simon Willison, "I think “agent” may finally have a widely enough agreed upon definition to be useful jargon now"… (2025-09-18): "An LLM agent runs tools in a loop to achieve a goal."

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
