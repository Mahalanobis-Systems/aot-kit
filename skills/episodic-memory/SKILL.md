---
name: episodic-memory
description: "AOT optimization 4.c.i (Tier 4, Restructuring): Episodic memory retrieval. Placeholder. Use when an agent shows: Memories retrieved per task; relevance."
---

<!-- Generated from library/entries/episodic-memory.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Episodic memory retrieval

> **Placeholder.** Generated from `library/entries/episodic-memory.yaml` (entry 4.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.c.i |
| Earlier id | P55 (Context & Memory, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a cross-session memory architecture |
| Categories | Memory: Reusing work |
| Change | tool / memory |

## What it is

Episodic memory retrieval

## When it applies

- **In the code:** A vector store; write after each episode; top-k retrieval; TTL or decay.
- **In traces:** Memories retrieved per task; relevance.
- **In eval results:** Repeat-mistake rate over time.
- **Judge:** Rate retrieved memories for relevance.
- **Probes:** A task pair where the first teaches a lesson the second needs.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Store, retrieve, decay.
- **Examples:** Task-pair probes.
- **Production:** Repeat-mistake rate; memory size.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium
- **Cost:** degrades, small
- **Performance:** degrades, small
- **Security:** mixed, medium: Memory poisoning.
- **Governance:** mixed, medium: Retention of user data.
- **Brand:** improves, small

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning", https://arxiv.org/abs/2303.11366 (2023-03-20): "91% pass@1 accuracy on the HumanEval coding benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%"

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
