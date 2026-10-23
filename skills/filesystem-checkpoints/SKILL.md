---
name: filesystem-checkpoints
description: "AOT optimization 4.b.i (Tier 2, Reliability): Filesystem-based agent state and checkpoints. Placeholder. Use when an agent shows: Resume events; steps skipped on resume."
---

<!-- Generated from library/entries/filesystem-checkpoints.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Filesystem-based agent state and checkpoints

> **Placeholder.** Generated from `library/entries/filesystem-checkpoints.yaml` (entry 4.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.b.i |
| Earlier id | P54 (Context & Memory, from the catalog cookbook) |
| Tier (proposed) | 2 (Reliability): operational hardening: checkpoint and resume |
| Categories | Memory: Resuming |
| Change | tool / memory |

## What it is

Filesystem-based agent state and checkpoints

## When it applies

- **In the code:** Checkpoint writes with metadata; resume logic on start.
- **In traces:** Resume events; steps skipped on resume.
- **In eval results:** Recovery from injected failure.
- **Probes:** Kill mid-run and resume.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Checkpoint round-trip.
- **Examples:** Kill-and-resume probes.
- **Production:** Redo rate after failures.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, small
- **Cost:** improves, medium
- **Performance:** improves, small
- **Security:** mixed, small: State files persist.
- **Governance:** improves, medium
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Justin Young (Anthropic), "Effective harnesses for long-running agents"… (2025-11-26): The initializer sets up "an init.sh script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git commit"; later sessions "make incremental progress, then leave structured updates."

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
