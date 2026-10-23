---
name: code-then-execute
description: "AOT optimization 6.c.i (Tier 4, Restructuring): Code-then-execute (CaMeL). Placeholder. Use when an agent shows: Policy violations blocked."
---

<!-- Generated from library/entries/code-then-execute.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Code-then-execute (CaMeL)

> **Placeholder.** Generated from `library/entries/code-then-execute.yaml` (entry 6.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.c.i |
| Earlier id | P49 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it restructures the control loop for trust separation |
| Categories | Topologies: Separating privileges |
| Change | tool / code_execution |

## What it is

Code-then-execute (CaMeL)

## When it applies

- **In the code:** A DSL or sandbox interpreter; a taint or policy checker.
- **In traces:** Policy violations blocked.
- **In eval results:** Injection suite plus capability benchmark.
- **Probes:** Data-flow violations.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** Checker blocks each violation class.
- **Examples:** Data-flow probes.
- **Benchmark:** AgentDojo style.
- **Production:** Blocked-flow alerts.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** mixed, medium: DSL limits expressiveness.
- **Cost:** degrades, small
- **Performance:** degrades, small
- **Security:** improves, large
- **Governance:** improves, large: Formal verifiability.
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Debenedetti et al., "Defeating Prompt Injections by Design", https://arxiv.org/abs/2503.18813 (2025-03-24): "solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo"

## Related

- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)

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
