---
name: multi-agent-for-breadth
description: "AOT optimization 6.b.iii (Tier 4, Restructuring): Use multi-agent orchestration only for breadth-first, independent sub-tasks. Placeholder. Use when an agent shows: sub-agents duplicating work or making conflicting decisions; failure rows labeled delegation-failure-subagent or communication-failure-subagent; token use per task far above a single agent's."
---

<!-- Generated from library/entries/multi-agent-for-breadth.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Use multi-agent orchestration only for breadth-first, independent sub-tasks

> **Placeholder.** Generated from `library/entries/multi-agent-for-breadth.yaml` (entry 6.b.iii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 6.b.iii |
| Earlier id | T64 |
| Tier | 4 (Restructuring): a multi-agent topology is a restructuring; only a production test shows its behavior on live traffic |
| Categories | Topologies: Parallelizing; Context: Isolating subtasks |
| Change | workflow / orchestration (restructure) |
| Also covers | Parallelization by sectioning or voting; Orchestrator-workers |

## What it is

Spawn parallel sub-agents when the work splits into independent, breadth-first parts with little shared context; expect about 15x the tokens of a chat and up to 90% less wall-clock. Default to a single agent otherwise (most coding): parallel workers make conflicting implicit decisions, and decompose-first planning scored below a single agent on data questions. When delegating, share full traces, give each sub-agent an objective, output format, tools and boundaries, have it write outputs to storage and return references, and re-verify what it reports.

## When it applies

- **In the code:** a multi-agent design whose sub-tasks share context or depend on each other; or a single agent on a breadth-first task with many independent parts
- **In traces:** sub-agents duplicating work or making conflicting decisions; failure rows labeled delegation-failure-subagent or communication-failure-subagent; token use per task far above a single agent's
- **In eval results:** single-agent against multi-agent on the same tasks

## How (outline)

1. Check the task shape: independent parts, little shared context.
2. If so, prototype a lead plus 3-5 parallel sub-agents with the delegation rules above.
3. Production A/B against the single agent on cost, latency and quality.

## How to measure

- **production-test** (Tier 4): A/B, single agent against multi-agent

## Expected impact

- **Quality:** mixed, large: +90.2% on breadth-first research (Jun 2025); below a single agent when sub-tasks depend on each other (GATE, Jun 2026)
- **Cost:** degrades, large: about 15x the tokens of chat
- **Performance:** improves, large: up to 90% less time with parallelism

## Evidence (summary)

- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval" (n not given; "excel especially for breadth-first queries"). Cost…
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): Short instructions like "research the semiconductor shortage" led subagents to misinterpret or duplicate ("one subagent explored the 2021 automotive chip crisis while 2 others duplicated work investigating current 2025 supply chains").…
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): Together with parallel tool calls in subagents: "These changes cut research time by up to 90% for complex queries". Joint figure for both changes.
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): Joint figure with parallel subagent spawning: "cut research time by up to 90% for complex queries".
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): Currently synchronous: "the lead agent can't steer subagents, subagents can't coordinate, and the entire system can be blocked while waiting for a single subagent". Async "adds challenges in result coordination, state consistency, and…
- …and 17 more sources in `library/entries/multi-agent-for-breadth.yaml`.

## Related

- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)

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
