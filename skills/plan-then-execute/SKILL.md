---
name: plan-then-execute
description: "AOT optimization 6.c.ii (Tier 4, Restructuring): Plan-then-execute. Placeholder. Use when an agent shows: Executed writes are a prefix of the committed writes, in order; executed calls equal the planned calls plus read-only lookups; each write argument and lookup destination traces to the request, a trusted record or a user confirmation, not to tool output."
---

<!-- Generated from library/entries/plan-then-execute.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Plan-then-execute

> **Placeholder.** Generated from `library/entries/plan-then-execute.yaml` (entry 6.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.c.ii |
| Earlier id | P48 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it fixes the plan before untrusted data is seen |
| Categories | Topologies: Separating privileges |
| Change | workflow / planning |

## What it is

Commit the agent's tool calls, writes above all, from the trusted request before it reads any tool output, and have code reject any other write and any write argument the request did not supply. On AgentDojo, plan-first designs cut attack success below 1% (0.69% against 13.16% for a tool graph; 0.52% against 15.62% in an independent test), but a strict plan cost 15 to 43 points of benign utility, and where every task needs data-dependent planning they kept 0 to 30% utility against 53% undefended (GPT-4o); one design that re-plans only within a tool whitelist kept 51% at 2% attack success in its authors' test. The plan alone does not stop injected data from choosing the values of planned calls: a tool graph let 47.92% and 67.36% of parameter-poisoning attacks through, a plan layer added nothing over input isolation against task tampering on five current models (7.0% against 6.6%), and branch steering reached 89.5% against a plan-first computer-use agent. Checking each write's recipient, amount, object and destination against values the request states let 0 of 13,935 attacks through on 15 open models of 1.7B to 35B parameters, at 29.0% utility under attack against 50.2% undefended.

## When it applies

- **In the code:** Write calls are committed from the request before any untrusted data is read, and the executor can add only read-only lookups; read and write tools are classified in code from their schemas; every authority argument of a write (recipient, account, amount, object identifier, destination) and every lookup destination is checked in code against values the request states or a trusted record, else the user is asked; raw tool output and error messages never go back to the planner.
- **In traces:** Executed writes are a prefix of the committed writes, in order; executed calls equal the planned calls plus read-only lookups; each write argument and lookup destination traces to the request, a trusted record or a user confirmation, not to tool output.
- **In eval results:** Injection suite attack success scored on write arguments, benign utility and utility under attack, on tasks that include data-dependent ones and attacks that keep the task's tools but change their values; confirmation requests, tokens and latency per task.
- **Probes:** Injected data that tries to add a tool call, change the arguments of a planned call, tamper with a value, rule or state the task reads, steer a planned branch, or send a lookup to an attacker's URL.

## How (outline)

1. Start from the baseline: your current tool loop (7.d.iii) and, as the cheapest plan-first variant, a tool filter that only fixes the tool set from the request (in an independent GPT-4o test it kept 70.10% of AgentDojo tasks against 80.41% undefended, at 4.59% average attack success against 23.69%). Run both on an injection suite that includes tasks whose actions depend on what the agent reads (AgentDojo has only 6 of 97) and attacks that keep the task's own tools but tamper with the values it needs: undefended Claude Sonnet 4.5 held template attacks to 0.87% on a data-dependent benchmark, but planted false amounts, rules or state claims still succeeded against it 11.1% of the time (11.1% to 23.2% across five current models).
2. Sort your tasks by whether the request alone fixes the actions. Where the next write depends on what is read (act on the to-do list in this file), a fixed plan fails: plan-first defenses kept 0 to 30% utility on such tasks against 53.33% undefended (GPT-4o). Either mark that step in the plan for a re-plan that may add only tools from a whitelist fixed up front, with a declared source for each write argument (one design kept 51% utility at 2% attack success there, against 53% utility and 39% attack success undefended, in its authors' GPT-4o test), or contain the input (10.c.i) and gate the action (10.b.i).
3. Give a planner only the user request, the tool descriptions and trusted context, and have it emit the calls in order or as a dependency graph: each node a tool call, each argument a literal from the request or a placeholder filled from a named earlier node's output. Pin the tool descriptions it reads, since they are planner input too, and classify each tool as read-only or write in code from its name and schema rather than leaving the security decision to the model: tool graphs written by the agent's own model admitted attacks on 13 of 15 open models (1.7B to 35B). Spend on the planner rather than the executor: an o4-mini planner over a GPT-4o-mini executor raised utility under attack from 57.07% to 64.39% for $7.99 against $6.73, planning being about 20% of tokens (1.b.i).
4. Commit the writes: execute in dependency order with a controller that rejects any write not in the plan, so the executor may add read-only lookups and fill placeholders but never add, drop or reorder a write. A strict graph cost 15.5 points of benign utility (52.58% against 68.04%) and read-only expansion brought it to 64.95%; in another study a planner allowed to append writes after reading let 53 of 7,432 attacks through, where committed writes let none. Treat the URL or destination of a lookup as a write argument: on eight open models a tool graph with read-only expansion let 69 of 168 attacks that fetch an attacker's URL succeed (85 undefended, 0 with destinations checked). Never return raw tool output or error messages to the planner to re-plan: in one study an error message and an email that reached the planner each put an attacker's call into the plan.
5. Bound in code what each planned write may do before it runs: every argument that decides whom or what it affects (recipient, account, amount, object identifier, channel, URL) must equal a value the request states or come from a trusted record named for it, else ask the user (free-text bodies such as a message are not covered). The plan alone does not do this: a tool graph let 47.92% (Qwen3.6-27B) and 67.36% (GPT-4o) of parameter-poisoning attacks through, against 93.06% and 57.64% undefended; against task tampering, in action-level audits of two of the five models (GLM-5 and Sonnet 4.5), no plan-position check blocked an attacked call and only the argument checklist blocked any (0 of 26 and 3 of 31); branch steering reached 89.5% against a plan-first computer-use agent until per-branch constraints took it to 0% at 97% of benign utility. Exact request grounding let 0 of 13,935 attacks through across 15 open models (106 of 7,432 without it, on eight of them); budget for confirmations, since values that appear only in tool output become questions to the user (8 to 12% of that design's failures, where they went unanswered). Where an injected instruction targets a write tool the plan already uses, answer it with a simulated call so the executor fills the real one from the request (attack success 4.77% to 0.64% in one study).
6. Measure paired against the baseline, same suite and model: benign utility, utility under attack, attack success scored on write arguments, confirmation requests, tokens and latency per task (a tool graph used 2.4x the input tokens and 1.9x the time, a strict plan-first design 0.54x the tokens and 2.7x the time, committed writes with request grounding 17.1k tokens per episode against 28.0k undefended, whitelisted re-planning 1.87x the time and 4.23x the tokens). Add adaptive attacks that reuse planned tools with attacker arguments, tamper with amounts, rules or state the task reads, craft values that meet branch conditions, send lookups to attacker URLs and reach the planner through errors; in production, monitor rejected calls, confirmation requests and write arguments or lookup destinations taken from tool output.

## How to measure

- **experiment** (Tier 4): paired runs, plan-first against the current loop and a tool filter, same model, on an injection suite that includes data-dependent tasks and helpful third-party instructions (AgentDojo or ASB plus AgentDyn-style tasks; WASP or STEER-Bench for browser agents) and attacks that keep the task's tools but change their values (task-tampering and parameter-poisoning cases): benign utility, utility under attack, attack success scored on write arguments, confirmation requests, tokens and latency per task; add adaptive attacks that reuse planned tools with attacker arguments, craft values that meet branch conditions, send read-only lookups to attacker URLs and reach the planner through error messages
- **monitor**: calls the controller rejected as unplanned, writes the executor tried to add, read-only expansions per task, confirmation requests for authority values found only in tool output, tasks abandoned because the plan did not fit, and write arguments or lookup destinations whose values came from tool output rather than the request or a trusted record

## Expected impact

- **Quality:** mixed, large: benign utility about even for a tool graph with read-only expansion (67.01% against 68.04%) and higher under attack (58.77% against 54.30%) (An, Aug 2025), but 40.1% against 59.4% for the same design across 15 open models (1.7B to 35B) and 55.7% against 90.7% on the strongest of them (Xu, Nov 2026); 37.11% against 80.41% for a strict plan-first design (Ji, Nov 2025); 0 to 30% against 53.33% on data-dependent tasks (Li, Feb 2026), 51% against 53% with whitelisted re-planning (Wang, May 2026); committed writes with request grounding 29.0% under attack against 50.2% (Xu, Nov 2026); adding a plan layer to input isolation cut benign completion from 98.0% to 88.9% with no security gain (Zhang, Nov 2026); Sonnet-5 in both roles 38.8% against 51.0% with ReAct, but a gpt-5 planner lifted a small executor from 23.5% to 36.8% (Zingrillo, Oct 2026)
- **Cost:** mixed, medium: 2.4x the input tokens for a tool-graph design (An, Aug 2025) and 60.5k against 28.0k tokens per episode across 15 open models (1.7B to 35B), where committed writes with request grounding used 17.1k (Xu, Nov 2026); 0.54x the tokens for a strict plan-first design and 0.65x for a tool filter, from fewer turns (Ji, Nov 2025); 4.23x for whitelisted re-planning (Wang, May 2026); $0.627 against $0.291 per task with Sonnet-5 in both roles, $0.332 with a gpt-5 planner over a locally served executor (Zingrillo, Oct 2026)
- **Performance:** degrades, medium: 13.88 s against 7.13 s per task (An, Aug 2025); 2.7x the wall-clock time for a strict plan-first design (13.36 against 4.98), while a tool filter was slightly faster (4.28) (Ji, Nov 2025); 9.93 s against 5.32 s for whitelisted re-planning (Wang, May 2026)
- **Security:** improves, large: attack success below 1% on static benchmarks: 0.69% against 13.16% on AgentDojo (An, Aug 2025); 0.52% against 15.62% on AgentDojo and 0.00% against 31.04% on ASB (Ji, Nov 2025); 0 of 13,935 with committed writes and request-grounded arguments (Xu, Nov 2026). Only with argument bounds: a tool graph let 47.92% and 67.36% of parameter-poisoning attacks through (93.06% and 57.64% undefended) (Wang, Nov 2026); a plan layer added nothing over input isolation against task tampering (7.0% against 6.6%, 17.0% undefended) (Zhang, Nov 2026); branch steering 89.5% against a plan-first computer-use agent until each branch's parameters were bounded (0%) (Zingrillo, Oct 2026); an adaptive attack reusing planned tools raised one design 3.9x, to 1.91% (Ji, Nov 2025)
- **Governance:** improves, medium: the committed plan and the allowed argument values are a record that can be checked after the fact: a trace audit re-derived them from the logged request and tool registry and found no violation in 25,452 episodes (Xu, Nov 2026); no source measures human review of plans
- **Brand:** improves, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", https://arxiv.org/abs/2506.08837 (2025-06-10): The pattern means "a prompt injection cannot force the LLM into executing a tool that is not part of the defined plan," though injected data can still change the inputs to planned calls. Not benchmarked.
- Zingrillo, Foerster, Shumailov, Zhao, Mullins, "Securing Computer-Use Agents Against Branch Steering Attacks"… (2026-10-02): STEER-Bench, cell-weighted attack success on the 74 cells generic agents can run: 94.4% for ReAct and 89.5% for the vanilla dual-LLM plan-first baseline; 0% for COBRA on all 199 cells, which keeps 97% of the baseline's benign utility (4…
- Li, Wen, Shi, Zhang, Vorobeychik, Xiao, "AgentDyn: Are Your Agent Security Defenses Deployable in Real-World Dynamic Environments?"… (2026-02-03): Only 6 of 97 AgentDojo tasks require dynamic planning. AgentDyn, GPT-4o, benign utility / utility under attack / attack success: undefended 53.33 / 55.52 / 37.80; Tool Filter 8.33 / 4.91 / 4.22; CaMeL 0.00 / 0.00 / 0.00; DRIFT 30.00 /…
- Ji, Wang, Li, Ma, Gao, Wu, Yan, Tian, Wang, "Taxonomy, Evaluation and Exploitation of IPI-Centric LLM Agent Defense Frameworks"… (2025-11-19): GPT-4o, average attack success: IsolateGPT 0.52% on AgentDojo (undefended 15.62%), 0.00% on ASB (31.04%) and InjecAgent (2.66%); Tool Filter 4.59% overall (undefended 23.69%). AgentDojo without attack: utility 37.11% for IsolateGPT, 70.10%…
- …and 5 more sources in `library/entries/plan-then-execute.yaml`.

## Caveats

The plan fixes which tools run, not what values they get: without argument bounds a tool graph let 47.92% and 67.36% of parameter-poisoning attacks through and a plan layer added nothing over input isolation against task tampering on five current models, while the bounded design's 0 of 13,935 comes from its authors' test on open models of 1.7B to 35B with thinking off and AgentDojo's tasks, at 21 points less utility under attack than undefended. Most attack numbers come from static template attacks: the one independent adaptive test raised a plan-first design 3.9x (to 1.91%) by reusing planned tools, and an email that reached the planner's context put an attacker's tool into the plan in a case study; a fixed plan also does not stop injections in the user prompt (Beurer-Kellner, Jun 2025) or in tool descriptions the planner reads. Utility depends on how plannable the tasks are: AgentDojo has 6 data-dependent tasks in 97, the benchmark built from such tasks shares authors with one of the defenses it tests, the 89.5% branch-steering figure is on its authors' own benchmark, and the re-planning design that kept utility on data-dependent tasks is its authors' GPT-4o test, which excluded 2 of 60 tasks and lets the re-planner read the observation. Frontier models resist template attacks undefended (0.87% for Claude Sonnet 4.5) but not task tampering (11.1%), and no source here compares a plan-first defense with a current frontier model running its vendor's built-in defenses.

## Related

- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)
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
