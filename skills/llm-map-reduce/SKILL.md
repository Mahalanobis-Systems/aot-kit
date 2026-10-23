---
name: llm-map-reduce
description: "AOT optimization 6.b.ii (Tier 4, Restructuring): LLM map-reduce. Placeholder. Use when an agent shows: Per-chunk outputs conform to schema."
---

<!-- Generated from library/entries/llm-map-reduce.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# LLM map-reduce

> **Placeholder.** Generated from `library/entries/llm-map-reduce.yaml` (entry 6.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.b.ii |
| Earlier id | P45 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it decomposes the task across parallel calls |
| Categories | Topologies: Parallelizing |
| Change | workflow / parallelization |

## What it is

LLM map-reduce

## When it applies

- **In the code:** Chunking, a sandboxed model per chunk with a constrained output schema, a deterministic reducer.
- **In traces:** Per-chunk outputs conform to schema.
- **In eval results:** Injection containment; recall vs monolithic.
- **Probes:** One injected chunk among clean chunks.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Schema enforcement per chunk; reducer.
- **Examples:** Injected-chunk probes.
- **Benchmark:** Long-document QA.
- **Production:** Schema violation rate.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** mixed, small: Constrained outputs lose nuance.
- **Cost:** degrades, medium
- **Performance:** improves, medium: Parallel map.
- **Security:** improves, large
- **Governance:** improves, medium
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", https://arxiv.org/abs/2506.08837 (2025-06-10): Proposed as a design pattern with "provable resistance to prompt injection"; analyzed for trade-offs and case studies, not benchmarked.

## Related

- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
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
