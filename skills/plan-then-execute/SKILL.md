---
name: plan-then-execute
description: "AOT optimization 6.c.ii (Tier 4, Restructuring): Plan-then-execute. Placeholder. Use when an agent shows: Executed calls equal the planned calls plus read-only lookups; no new write call after data ingestion; each write argument traces to the request or a trusted record, not to tool output."
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

Have the agent fix its tool calls (an ordered list or a dependency graph) from the trusted request before it reads any tool output, and let a controller execute only those calls, so injected text cannot add an action. On AgentDojo this cut attack success below 1% (0.69% against 13.16% undefended for a tool-graph design; 0.52% against 15.62% for another plan-first design in an independent test), but a strict plan cost 15 to 43 points of benign utility; letting read-only lookups be added during execution recovered it in one study. It pays only where the request alone fixes the actions: on a benchmark where every task needs data-dependent planning, plan-first defenses kept 0 to 30% utility against 53% undefended on GPT-4o, while undefended Claude Sonnet 4.5 already held attack success at 0.87%. Injected data can still pick the arguments and branches of planned calls (89.5% attack success against a plan-first computer-use agent), so also bound each planned call's parameters and destinations.

## When it applies

- **In the code:** A plan (tool calls with their dependencies) is generated from the request before any untrusted data is read; a controller executes only planned calls plus read-only lookups; write-call arguments and destinations are bounded before execution; raw tool output and error messages never go back to the planner.
- **In traces:** Executed calls equal the planned calls plus read-only lookups; no new write call after data ingestion; each write argument traces to the request or a trusted record, not to tool output.
- **In eval results:** Injection suite attack success, benign utility and utility under attack, on tasks that include data-dependent ones; tokens and latency per task.
- **Probes:** Injected data that tries to add a tool call, change the arguments of a planned call, or steer a planned branch.

## How (outline)

1. Start from the baseline: your current tool loop (7.d.iii) and, as the cheapest plan-first variant, a tool filter that only fixes the tool set from the request (in an independent GPT-4o test it kept 70.10% of AgentDojo tasks against 80.41% undefended, at 4.59% average attack success against 23.69%). Run both on an injection suite that includes tasks whose actions depend on what the agent reads: AgentDojo has only 6 of 97, and on a benchmark built from such tasks undefended Claude Sonnet 4.5 already held attack success at 0.87%.
2. Sort your tasks by whether the request alone fixes the actions. Where the next write depends on what is read (act on the to-do list in this file), do not force a fixed plan: plan-first defenses kept 0 to 30% utility on such tasks against 53.33% undefended (GPT-4o); contain the input (10.c.i) and gate the action (10.b.i) instead.
3. Give a planner only the user request, the tool descriptions and trusted context, and have it emit a dependency graph: each node a tool call, each argument a literal or marked as filled from a named earlier node's output. Pin the tool descriptions it reads, since they are planner input too. Spend on the planner rather than the executor: an o4-mini planner over a GPT-4o-mini executor raised utility under attack from 57.07% to 64.39% for $7.99 against $6.73, planning being about 20% of tokens (1.b.i).
4. Execute the graph in dependency order with a controller that rejects any call not in the plan, except read-only (query) tools added after reading results; the executor fills only the pending arguments. A strict graph cost 15.5 points of benign utility (52.58% against 68.04%); read-only expansion brought it to 64.95%. Never return raw tool output or error messages to the planner to re-plan: in one study an error message and an email that reached the planner each put an attacker's call into the plan.
5. Bound what each planned write may do before execution, in code: recipients, accounts and amounts from the request or a trusted record (ask the user when there is none), allowed hosts and endpoints, and per-branch conditions. Without this, injected data set the recipient of a planned send_money in one test and steered branches at 89.5% success against a plan-first computer-use agent; per-branch constraints took that to 0% at 97% of benign utility. Where an injected instruction targets a write tool the plan already uses, answer it with a simulated call so the executor fills the real one from the request (attack success 4.77% to 0.64% in one study).
6. Measure paired against the baseline, same suite and model: benign utility, utility under attack, attack success, tokens and latency per task (one design used 2.4x the input tokens and 1.9x the time, another 0.54x the tokens and 2.7x the time); add adaptive attacks that reuse planned tools with attacker arguments, craft values that meet branch conditions and reach the planner through errors; in production, monitor rejected calls and write arguments taken from tool output.

## How to measure

- **experiment** (Tier 4): paired runs, plan-first against the current loop and a tool filter, same model, on an injection suite that includes data-dependent tasks and helpful third-party instructions (AgentDojo or ASB plus AgentDyn-style tasks; WASP or STEER-Bench for browser agents): benign utility, utility under attack, attack success, tokens and latency per task; add adaptive attacks that reuse planned tools with attacker arguments, craft values that meet branch conditions and reach the planner through error messages
- **monitor**: calls the controller rejected as unplanned, read-only expansions per task, tasks abandoned because the plan did not fit, and write arguments whose values came from tool output rather than the request or a trusted record

## Expected impact

- **Quality:** mixed, large: benign utility about even for a tool graph with read-only expansion (67.01% against 68.04%) and higher under attack (58.77% against 54.30%) (An, Aug 2025); 37.11% against 80.41% for a strict plan-first design (Ji, Nov 2025); 0 to 30% against 53.33% on data-dependent tasks (Li, Feb 2026); Sonnet-5 in both roles 38.8% against 51.0% with ReAct, but a gpt-5 planner lifted a small executor from 23.5% to 36.8% (Zingrillo, Oct 2026)
- **Cost:** mixed, medium: 2.4x the input tokens for a tool-graph design (An, Aug 2025); 0.54x the tokens for a strict plan-first design and 0.65x for a tool filter, from fewer turns (Ji, Nov 2025); $0.627 against $0.291 per task with Sonnet-5 in both roles, $0.332 with a gpt-5 planner over a locally served executor (Zingrillo, Oct 2026)
- **Performance:** degrades, medium: 13.88 s against 7.13 s per task (An, Aug 2025); 2.7x the wall-clock time for a strict plan-first design (13.36 against 4.98), while a tool filter was slightly faster (4.28) (Ji, Nov 2025)
- **Security:** improves, large: attack success below 1% on static benchmarks: 0.69% against 13.16% on AgentDojo (An, Aug 2025); 0.52% against 15.62% on AgentDojo and 0.00% against 31.04% on ASB (Ji, Nov 2025). Not against argument or branch steering: 89.5% against a plan-first computer-use agent until each branch's parameters were bounded (0%) (Zingrillo, Oct 2026); an adaptive attack reusing planned tools raised one design 3.9x, to 1.91% (Ji, Nov 2025)
- **Governance:** improves, large (unmeasured): The plan is a record of what the agent may do, reviewable before it runs; no source here measures it.
- **Brand:** improves, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", https://arxiv.org/abs/2506.08837 (2025-06-10): The pattern means "a prompt injection cannot force the LLM into executing a tool that is not part of the defined plan," though injected data can still change the inputs to planned calls. Not benchmarked.
- Zingrillo, Foerster, Shumailov, Zhao, Mullins, "Securing Computer-Use Agents Against Branch Steering Attacks"… (2026-10-02): STEER-Bench, cell-weighted attack success on the 74 cells generic agents can run: 94.4% for ReAct and 89.5% for the vanilla dual-LLM plan-first baseline; 0% for COBRA on all 199 cells, which keeps 97% of the baseline's benign utility (4…
- Li, Wen, Shi, Zhang, Vorobeychik, Xiao, "AgentDyn: Are Your Agent Security Defenses Deployable in Real-World Dynamic Environments?"… (2026-02-03): Only 6 of 97 AgentDojo tasks require dynamic planning. AgentDyn, GPT-4o, benign utility / utility under attack / attack success: undefended 53.33 / 55.52 / 37.80; Tool Filter 8.33 / 4.91 / 4.22; CaMeL 0.00 / 0.00 / 0.00; DRIFT 30.00 /…
- Ji, Wang, Li, Ma, Gao, Wu, Yan, Tian, Wang, "Taxonomy, Evaluation and Exploitation of IPI-Centric LLM Agent Defense Frameworks"… (2025-11-19): GPT-4o, average attack success: IsolateGPT 0.52% on AgentDojo (undefended 15.62%), 0.00% on ASB (31.04%) and InjecAgent (2.66%); Tool Filter 4.59% overall (undefended 23.69%). AgentDojo without attack: utility 37.11% for IsolateGPT, 70.10%…
- …and 1 more sources in `library/entries/plan-then-execute.yaml`.

## Caveats

Most attack-success numbers here come from static template attacks: the one independent adaptive test raised a plan-first design 3.9x (to 1.91%) by reusing planned tools with attacker arguments, and an email that reached the planner's context put an attacker's tool into the plan in a case study. Utility depends on how plannable the tasks are: AgentDojo has 6 data-dependent tasks in 97, and on a benchmark where all tasks are, plan-first defenses lost most of their utility; that benchmark shares authors with one of the defenses it tests, and the 89.5% branch-steering figure is on its authors' own benchmark. A fixed plan does not stop injections in the user prompt (Beurer-Kellner, Jun 2025) or in tool descriptions the planner reads, and frontier models already resist template attacks without a defense (0.87% for undefended Claude Sonnet 4.5), so the guarantee matters most against attackers stronger than today's benchmarks.

## Related

- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
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
