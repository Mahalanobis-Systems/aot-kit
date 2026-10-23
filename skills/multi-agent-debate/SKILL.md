---
name: multi-agent-debate
description: "AOT optimization 7.c.vi (Tier 4, Restructuring): Multi-agent debate. Placeholder. Use when an agent shows: Rounds; whether positions change."
---

<!-- Generated from library/entries/multi-agent-debate.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Multi-agent debate

> **Placeholder.** Generated from `library/entries/multi-agent-debate.yaml` (entry 7.c.vi). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.vi |
| Earlier id | P43 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a multi-agent topology |
| Categories | Orchestration: Scaling compute |
| Change | workflow / orchestration |

## What it is

Multi-agent debate

## When it applies

- **In the code:** Multiple agents with opposing prompts and a synthesizer.
- **In traces:** Rounds; whether positions change.
- **In eval results:** Decision quality vs single agent.
- **Judge:** Rate synthesis and whether the debate was substantive.
- **Probes:** Questions with a confirmation-bias trap.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Examples:** Trap probes.
- **Benchmark:** Decision or judgment benchmark.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium: Decisions only.
- **Cost:** degrades, large
- **Performance:** degrades, large
- **Security:** none
- **Governance:** improves, small: Recorded arguments.
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Du et al., "Improving Factuality and Reasoning in Language Models through Multiagent Debate", https://arxiv.org/abs/2305.14325 (2023-05-23): "Arithmetic: 81.8 vs 67.0 single agent; Grade School Math: 85.0 vs 77.0 (%, Table 1)"

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
