---
name: multi-agent-for-breadth
description: "AOT optimization 6.b.iii (Tier 4, Restructuring): Use multi-agent orchestration only for breadth-first, independent sub-tasks. Placeholder. Use when an agent shows: sub-agents duplicating work or making conflicting decisions; merge conflicts, overwritten or redone work, parts that pass their own tests but fail together; runs ending on budget exhaustion; turns and tokens per task far above a single agent's; failure rows labeled delegation-failure-subagent or communication-failure-subagent."
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

Fan work out to parallel sub-agents only when it splits into independent parts, and check that one agent given the same budget doesn't do as well. In a matched-budget study across six benchmarks, multi-agent setups gained 80.8% on decomposable financial analysis but lost 39-70% on sequential planning and 2-15% on SWE-bench Verified (mean change -0.3%), a role-split customer-service team lost to one agent in 12 of 13 settings, and teams cost more (about 15x a chat's tokens in one vendor's research system; 1.7-4.3x one agent's cost on coding tasks) without always being faster (up to 90% less research time, but 1.2-2.5x longer for a coordinated coding team). For code, split only with a lead that sees every requirement and with explicit ownership and isolation: two parallel agents with conflicting requirements passed jointly 16% of the time against 62% for one agent holding both, while a manager that split a repository by its dependencies, gave each worker its own git worktree and merged through tests gained about 6 points for Claude Sonnet 4.5. When delegating, give each sub-agent an objective, output format, tools, boundaries and the files it owns, have it write outputs to storage and return references, and re-verify what it reports.

## When it applies

- **In the code:** a multi-agent design whose sub-tasks share context or depend on each other, or whose planner lacks the tools or context its workers hold; parallel coding workers sharing one working tree or without stated file and interface ownership; or a single agent on a breadth-first task with many independent parts
- **In traces:** sub-agents duplicating work or making conflicting decisions; merge conflicts, overwritten or redone work, parts that pass their own tests but fail together; runs ending on budget exhaustion; turns and tokens per task far above a single agent's; failure rows labeled delegation-failure-subagent or communication-failure-subagent
- **In eval results:** single agent against the team on the same tasks at the same token or cost budget, split by task shape (independent breadth vs sequential), with wall-clock and conflict rate
- **Probes:** Paired tasks at the same budget: one that splits into independent parts and one whose steps depend on each other

## How (outline)

1. Start from one agent and check the task shape before splitting. Split only when the work has many parts that are independent (no part needs another's result or must follow another's decisions), share little context and can be checked separately: breadth-first research, one item per entity or file, independent reviews, code modules with clear interfaces. Keep one agent for sequential work, conversations with a single user and tasks it already does well: at a matched budget, multi-agent setups gained 80.8% on decomposable financial analysis but lost 39-70% on sequential planning and 2-15% on SWE-bench Verified, with gains shrinking once the single agent passed about 45%; a role-split customer-service team lost in 12 of 13 settings, including the two where that 45% rule predicted a gain; and decomposing a text-to-SQL question before looking at the data scored below a single agent. Run the single agent first at the budget the team would get, and treat a threshold from a paper as a hint, not a rule.
2. Let one lead that sees the whole task make the split, and give each sub-agent an objective, an output format, its tools and boundaries, and the context it needs (the relevant trace, not a one-line task: vague tasks led research sub-agents to duplicate work). For code, split along the dependency graph: group files with strong or circular dependencies under one worker, list for each task the files it owns and the interfaces it consumes and produces, mark shared files (package init files, configs) off-limits, and settle shared conventions before workers start. Parallel coding agents that each saw only their own requirement passed jointly 16% of the time against 62% for one agent holding both; when agents agreed on an owner for the contested code, conflicts fell from 67% to 18% of runs (61% pass against 29%).
3. Isolate writers and integrate through checks. Give each coding worker its own branch and git worktree, merge into the main branch only after the worker's relevant tests pass, and have the worker that caused a merge conflict resolve it: on paper reproduction, one shared workspace with files assigned by instruction scored 55.5% (single agent 57.2%), separate worktrees 63.3%. Prefer read-only sub-agents (search, review, investigation) wherever the task allows; they cannot make conflicting edits.
4. Have sub-agents write outputs (code, reports, data) to storage and return references, and have the lead check each report against the artifact before building on it (the stop-time check is 9.b.iii). Making delegation required raised the share of planted issues that reviews reported (49.9% to 69.6%) but did not make their coverage claims honest: 50.3% of incomplete delegating reviews still explicitly overclaimed.
5. Cap the number of workers and the team's total budget, and log spend per worker. Start with a few workers (one research system runs 3-5 in parallel; one harness defaults to three concurrent children at depth 1): going from 4 to 8 coding workers lowered the pass rate, turns grew from 7.2 for one agent to 27.7 for an orchestrated team, and under a token ceiling 74% of one team's loss came from runs that exhausted the budget.
6. Measure the team against one agent at the same token or cost budget (and, where you can, one agent running the same plan-and-review steps in one context), with several runs per arm on your own task mix split by task shape: success, tokens and cost, wall-clock, conflict and rework rate (merge conflicts, overwritten or redone work, parts that pass alone but fail together) and sub-agent reports later found wrong. Do not assume parallel means faster: parallel sub-agents with parallel tool calls cut research time by up to 90%, but a coordinated coding team ran 1.2-2.5x longer than one agent because its merges were sequential and test-gated. Do not run one agent first and fall back to the team after it fails: in one study that nearly added the two runtimes and costs.

## How to measure

- **production-test** (Tier 4): A/B the team against one agent at the same token or cost budget (and one agent running the same plan-and-review steps where feasible), several runs per arm, split by task shape (independent breadth vs sequential): success, tokens and cost, wall-clock, conflict and rework rate (merge conflicts, overwritten or redone work, parts that pass alone but fail together) and sub-agent reports later found wrong
- **monitor**: per production run: workers spawned, tokens per worker and in total against the team ceiling, runs ending on budget exhaustion, wall-clock, merge conflicts and redone work, duplicated sub-tasks, and lead corrections of sub-agent reports; re-run the A/B after a model change

## Expected impact

- **Quality:** mixed, large: +90.2% on breadth-first research, not compute-matched (Hadfield, Jun 2025); at a matched budget an orchestrated team +80.8% on decomposable financial analysis, -39% to -70% on sequential planning, -2% to -15% on SWE-bench Verified, mean -0.3% over six benchmarks (Kim, Dec 2025); a role-split customer-service team worse in 12 of 13 settings, weighted mean -28 points, under a matched token ledger (Yang, Oct 2026); a worktree-isolated coding team +6.0 and +6.1 points for Claude Sonnet 4.5 (Geng, Mar 2026); parallel coding agents with conflicting requirements 16% joint pass against 62% for one agent, a lead delegating to sub-agents 58% (Mediratta, Oct 2026); decomposition-first text-to-SQL below a single agent (GATE, Jun 2026)
- **Cost:** degrades, large: about 15x the tokens of a chat (Hadfield, Jun 2025); 21.5 successes per 1,000 tokens for an orchestrated team against 67.7 for one agent (Kim, Dec 2025); 1.7x to 4.3x one agent's cost on coding tasks (Geng, Mar 2026); 1.4x to 3.1x the dollars per setting, level with one agent only at 5.5x its tokens without a ceiling (Yang, Oct 2026); 1.18x to 1.58x one agent's tokens for a lead delegating to sub-agents (Mediratta, Oct 2026)
- **Performance:** mixed, large: up to 90% less research time with parallel sub-agents and parallel tool calls (Hadfield, Jun 2025); 25% less wall-clock on one coding build, three-run means, against a workflow that dispatched sub-agents one at a time (Wogu, Oct 2026); a worktree-isolated coding team took 1.2x to 2.5x one agent's runtime because merges are sequential and test-gated (Geng, Mar 2026)

## Evidence (summary)

- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval" (n not given; "excel especially for breadth-first queries"). Cost…
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): Short instructions like "research the semiconductor shortage" led subagents to misinterpret or duplicate ("one subagent explored the 2021 automotive chip crisis while 2 others duplicated work investigating current 2025 supply chains").…
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "the lead agent spins up 3-5 subagents in parallel rather than serially"; together with parallel tool calls in subagents: "These changes cut research time by up to 90% for complex queries". Joint figure for both changes.
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): Joint figure with parallel subagent spawning: "cut research time by up to 90% for complex queries".
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): Currently synchronous: "the lead agent can't steer subagents, subagents can't coordinate, and the entire system can be blocked while waiting for a single subagent". Async "adds challenges in result coordination, state consistency, and…
- …and 23 more sources in `library/entries/multi-agent-for-breadth.yaml`.

## Caveats

Most gains are not compute-matched: the +90.2% research result came at about 15x a chat's tokens, and the same vendor found token usage alone explained 80% of the variance on a browsing eval; at a matched budget the gain held mainly on decomposable tasks, in one study whose coding cells had 20 tasks (intervals of about 20 points) and whose 45% capability rule did not transfer to customer-service conversations. That contradicting study's team planned without seeing the tool schemas (a deviation its authors label), and the coding evidence comes from purpose-built benchmarks (conflicting requirements from separate principals; 16 library repositories and a set of papers, one run each) and one practitioner's own plugin on one project, so effect sizes will differ on your tasks. Speed gains need the parts to run truly in parallel: sequential, test-gated merges made a coordinated coding team slower than one agent, and the 25% faster coding build was measured against a workflow that dispatched sub-agents one at a time, not against a single agent.

## Related

- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:verify-citations` (9.a.ii, Verify citations claim by claim for factual support)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)

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
