---
name: plan-then-execute
description: "AOT optimization 6.c.ii (Tier 4, Restructuring): Plan-then-execute. Placeholder. Use when an agent shows: Executed calls equal the planned calls; no new tool call after data ingestion."
---

<!-- Generated from library/entries/plan-then-execute.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Plan-then-execute

> **Placeholder.** Generated from `library/entries/plan-then-execute.yaml` (entry 6.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.c.ii |
| Earlier id | P48 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it fixes the plan before untrusted data is seen |
| Categories | Topologies: Separating privileges |
| Change | workflow / planning |

## What it is

Fix the tool sequence before seeing untrusted data.

## When it applies

- **In the code:** A plan is generated before untrusted data is read; the controller executes the fixed sequence.
- **In traces:** Executed calls equal the planned calls; no new tool call after data ingestion.
- **In eval results:** Injection suite pass rate; task success.
- **Probes:** Injected data that tries to add a tool call.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Controller rejects unplanned calls.
- **Examples:** Injection probes.
- **Benchmark:** Injection benchmark.
- **Production:** Plan deviation alerts.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** mixed, medium: Rigid plans cannot adapt.
- **Cost:** none
- **Performance:** improves, small
- **Security:** improves, large
- **Governance:** improves, large
- **Brand:** improves, small

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", https://arxiv.org/abs/2506.08837 (2025-06-10): The pattern means "a prompt injection cannot force the LLM into executing a tool that is not part of the defined plan," though injected data can still change the inputs to planned calls. Not benchmarked.

## Related

- `aot-kit:react-loop` (7.d.iii, ReAct loop)

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
