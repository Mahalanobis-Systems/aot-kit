---
name: initializer-maintainer-agents
description: "AOT optimization 4.b.ii (Tier 4, Restructuring): Initializer-maintainer dual agent. Placeholder. Use when an agent shows: Session handoffs; progress file updates."
---

<!-- Generated from library/entries/initializer-maintainer-agents.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Initializer-maintainer dual agent

> **Placeholder.** Generated from `library/entries/initializer-maintainer-agents.yaml` (entry 4.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.b.ii |
| Earlier id | P46 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it splits the work across two agents |
| Categories | Memory: Resuming |
| Change | workflow / orchestration |

## What it is

Initializer-maintainer dual agent

## When it applies

- **In the code:** Two entry points; a progress file and feature list; bootstrap and per-session flows.
- **In traces:** Session handoffs; progress file updates.
- **In eval results:** Multi-session completion rate.
- **Probes:** A multi-session project.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Progress file schema.
- **Examples:** Multi-session probes.
- **Production:** Sessions per feature.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium: Long projects only.
- **Cost:** improves, small
- **Performance:** none
- **Security:** none
- **Governance:** improves, medium
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Justin Young (Anthropic), "Effective harnesses for long-running agents"… (2025-11-26): "an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session."

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
