---
name: skill-library
description: "AOT optimization 4.c.ii (Tier 4, Restructuring): Skill library evolution. Placeholder. Use when an agent shows: Skill reuse rate; skills authored per session."
---

<!-- Generated from library/entries/skill-library.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Skill library evolution

> **Placeholder.** Generated from `library/entries/skill-library.yaml` (entry 4.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.c.ii |
| Earlier id | P58 (Learning, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a reusable skill memory |
| Categories | Memory: Reusing work |
| Change | tool / memory |

## What it is

Persist working code as reusable, lazily loaded skills.

## When it applies

- **In the code:** A skills directory; a load_skills tool; lazy MCP binding.
- **In traces:** Skill reuse rate; skills authored per session.
- **In eval results:** Time to solve repeated task families.
- **Judge:** Review self-authored skills.
- **Probes:** Repeated task families.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Skill loading.
- **Examples:** Task-family probes.
- **Production:** Reuse rate.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium
- **Cost:** improves, medium: Catalog cites 91 percent token reduction with lazy MCP.
- **Performance:** improves, small
- **Security:** degrades, small: Self-authored code.
- **Governance:** mixed, medium: Needs review of skills.
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Wang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models", https://arxiv.org/abs/2305.16291 (2023-05-25): "obtains 3.3x more unique items, travels 2.3x longer distances, and unlocks key tech tree milestones up to 15.3x faster than prior SOTA"

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
