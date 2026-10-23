---
name: oracle-worker-escalation
description: "AOT optimization 6.a.i (Tier 4, Restructuring): Oracle-worker multi-model. Placeholder. Use when an agent shows: Escalation rate; oracle tokens share."
---

<!-- Generated from library/entries/oracle-worker-escalation.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Oracle-worker multi-model

> **Placeholder.** Generated from `library/entries/oracle-worker-escalation.yaml` (entry 6.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.a.i |
| Earlier id | P42 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a multi-model topology |
| Categories | Topologies: Escalating; Models: Using cheaper models |
| Change | workflow / orchestration |

## What it is

Cheap worker, expensive oracle on request.

## When it applies

- **In the code:** Two models with an escalation call from worker to oracle.
- **In traces:** Escalation rate; oracle tokens share.
- **In eval results:** Quality vs cost against single-model baselines.
- **Judge:** Whether escalations were warranted.
- **Probes:** Tasks where the worker fails.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Escalation trigger.
- **Examples:** Worker-failure probes.
- **Benchmark:** Task benchmark with cost.
- **Production:** Escalation rate; cost per task.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** mixed, medium: Depends on the escalation trigger.
- **Cost:** improves, large
- **Performance:** mixed, small
- **Security:** none
- **Governance:** improves, small
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Lingjiao Chen, Matei Zaharia, James Zou, "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance"… (2023-05-09): "FrugalGPT can match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost"

## Related

- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)

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
