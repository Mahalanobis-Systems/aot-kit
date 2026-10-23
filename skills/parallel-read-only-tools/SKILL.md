---
name: parallel-read-only-tools
description: "AOT optimization 6.b.i (Tier 3, Tuning): Parallel tool execution for read-only calls. Placeholder. Use when an agent shows: Overlapping tool spans; ordering violations."
---

<!-- Generated from library/entries/parallel-read-only-tools.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Parallel tool execution for read-only calls

> **Placeholder.** Generated from `library/entries/parallel-read-only-tools.yaml` (entry 6.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.b.i |
| Earlier id | P52 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it changes execution order and latency |
| Categories | Topologies: Parallelizing |
| Change | workflow / parallelization |

## What it is

Parallel tool execution for read-only calls

## When it applies

- **In the code:** Tools classified read-only or mutating; concurrent dispatch for read-only batches.
- **In traces:** Overlapping tool spans; ordering violations.
- **In eval results:** Latency; race-condition failures.
- **Probes:** Batches mixing reads and writes.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Mutating calls serialized; read-only concurrent.
- **Examples:** Mixed-batch probes.
- **Production:** p95 latency; race errors.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** mixed, small: Races if misclassified. VeRO T36: shell concurrency was only ever raised.
- **Cost:** none
- **Performance:** improves, large
- **Security:** mixed, small
- **Governance:** none
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Kim et al., "An LLM Compiler for Parallel Function Calling", https://arxiv.org/abs/2312.04511 (2023-12-07): "latency speedup of up to 3.7x, cost savings of up to 6.7x, and accuracy improvement of up to ~9% compared to ReAct"

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
