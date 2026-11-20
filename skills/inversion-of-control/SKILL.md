---
name: inversion-of-control
description: "AOT optimization 7.d.ii (Tier 4, Restructuring): Inversion of control. Placeholder. Use when an agent shows: Variety of action sequences across tasks of the same type: one sequence recurring across most tasks suggests code could own the path; widely varying sequences on a known procedure suggest constraints are being missed; on a long run, items batched or skipped, decisions made without reading the data, or an early stop after the first few dozen items suggest the procedure needs enforcing in code."
---

<!-- Generated from library/entries/inversion-of-control.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Inversion of control

> **Placeholder.** Generated from `library/entries/inversion-of-control.yaml` (entry 7.d.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.d.ii |
| Earlier id | P50 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it changes who owns the control flow |
| Categories | Orchestration: Shaping the loop |
| Change | workflow / control_flow |

## What it is

Let the agent pick its own steps toward a goal, with the tools and acceptance checks, instead of coding a fixed workflow; the goal, permissions, budget and checks stay outside it. It pays where the next step depends on what the agent finds and the model is strong: on 90 microservice incidents, harnesses that left every model call to the model ranked the root cause first in 65 to 77% of cases against 16 to 53% for agents with hand-crafted procedures, and a GPT-5.5 optimizer that composed its own process beat prescribed pipelines in 12 of 14 comparisons (a medium model did better with the pipeline). Where the procedure is known, code should own it: a state machine that enforced a 200-account procedure gave Claude Haiku 4.5 139.2 faithful and correct decisions against 48.4 for the best prompted baseline, a coded workflow passed 35.56% of TravelPlanner against 10.40% for ReAct, and compiling an agent's logged runs into code kept 93.8% completion against 96.8% on 79 production procedures at 24% lower cost. Agent-chosen routes also cost more than a workflow that calls the model only for bounded steps (2.7x to 3.6x the input tokens in one RAG comparison) and can be steered: fake error messages redirected an agent orchestrator to run an attacker's code in 83 to 100% of trials until its permitted route was fixed before untrusted data was read.

## When it applies

- **In the code:** Minimal orchestration code; the agent decides the sequence.
- **In traces:** Variety of action sequences across tasks of the same type: one sequence recurring across most tasks suggests code could own the path; widely varying sequences on a known procedure suggest constraints are being missed; on a long run, items batched or skipped, decisions made without reading the data, or an early stop after the first few dozen items suggest the procedure needs enforcing in code.
- **In eval results:** Success, procedure and constraint violations (per window across long runs), hand-offs and early stops, LLM calls, tokens and latency per task for the agent loop against a fixed or enforced workflow, per model tier.
- **Judge:** Rate whether autonomy was used well.
- **Probes:** Tasks with a known procedure and hard constraints, run long enough to show drift; tasks whose next step depends on what is found; tool output that fakes an error and proposes a different next step.

## How (outline)

1. Start from two baselines on the same model, tools and task set: the fixed workflow you have or would write (code picks the steps, the model fills bounded nodes) and an agent loop (7.d.iii) that gets the goal, the same tools and the same acceptance checks and picks its own steps. Add the cheapest arm, one model call over evidence that code assembles: on 90 microservice incidents it ranked the root cause first in 65.3% of cases, ahead of every agent with a hand-crafted procedure (53.3% at best), while agent loops that chose what to read reached 72.8% and 77.2%.
2. Keep the ends outside the agent in both designs: the goal, permissions, budget caps and the acceptance check or evaluator, so only the route is delegated. Where the agent reads untrusted content, also fix which next steps are allowed before it reads any: fake error messages in tool output redirected an agent orchestrator to run an attacker's code in 83 to 100% of trials, least privilege still let 67 to 80% through because the attack used the task's own agents, and an LLM alignment check in its default setup let 87 to 100% of rephrased attacks through; a graph of permitted agent calls generated from the request before any data was read, with up to three rules per edge, blocked all of them at 2.5x the time per task, with benign success equal or higher on the attacked coding tasks (97% against 93% on single-answer coding) and 62% against 65% in a separate AgentDojo Slack test (6.c.ii, 10.c.i).
3. Sort tasks by whether the path is known. Where the next step depends on what is found (diagnosis, open lookups), let the model choose what to read and compute: incident agents whose programs fixed at least 10% and up to all of their model calls ranked the root cause first in 16 to 53% of cases against 65 to 77% for harnesses that fixed none, and in a case study the matched procedure never read the log that held the answer; an agent also rewrote retrieval queries better than a fixed rewrite step (NDCG@10 55.6 against 52.8). Where the steps and constraints are stable (a runbook, an SOP, hard business rules), code the path and enforce the constraints in code: on TravelPlanner a coded workflow passed 35.56% against 10.40% for same-model ReAct, and writing the same rules into the baselines' prompts left them 12.7 to 20.2 points behind (37.20 against 17.00 to 24.50).
4. For a known procedure over a long unattended run, keep its state in code and enforce it at three points: admit only the tools the current state permits, check exit conditions before each transition, and refuse to end the turn until the work is done. Restating the procedure or auto-resuming the agent only moved the drift to another shortcut (batching items, stopping early, deciding without looking at the data); with all three gates Claude Haiku 4.5 made 139.2 faithful and correct decisions on a 200-account batch against 48.4 for the best prompted baseline, while the stop gate alone scored 5.7 and the other two gates alone 104.0. Close every route (one the gates left open was used in 3 of 8 sessions) and keep checks no stricter than the policy: over-strict checks cut tau2-bench retail successes from 15 to 9 of 30 while telecom rose from 13 to 30 of 40. The gain tracks how much the plain agent drifts (12.9 decisions for a model that mostly held the procedure, 1 task in 100 on easy SWE-bench tasks at 23% more median time), so measure drift first.
5. Delegate the route only to a model that can carry it, and upgrade the model before raising its effort: a GPT-5.5 optimizer that composed its own process beat two prescribed pipelines in 12 of 14 comparisons, but with a medium model the pipeline won by 3.50 to 9.68 points and a 4B model produced no valid action; on WebArena-Verified code-owned control held 44.7 to 45.3% while a tool-calling agent scored 30.0% on a 120B model and 12.7% and 6.7% on 20B and 4B models. In the incident study a stronger model raised first-rank accuracy 14.4 to 17.8 points with fewer calls and cut cases solved in only some of three passes from 32 to 36% to 7 to 8%, while more reasoning effort added 2.2 to 4.4 points at 1.5 to 4 times the wall time.
6. Mix within one task and move recurring decisions into code: keep fixed steps the agent does worse (a fixed reranker scored 49.5 NDCG@10 against 43.9 when the agent re-retrieved on its own), enforce preconditions on irreversible actions in code (10.b.i), and for a procedure you run often, compile logged agent runs, including the reason the agent wrote for each call, into a workflow in which code picks every step: on 79 production procedures this kept 93.8% completion against 96.8% for the agent at 24% lower cost per task, and on tau2-bench telecom 75.8% against 80.6% at 1.3 s against 170 s per task; the written reasons added 8.8 and 6.2 points over tool calls alone. Another study learned recurring control as code from failure traces and made 76.0 to 91.8% fewer LLM calls.
7. Measure paired runs on the deployed model and one cheaper tier: success, procedure and constraint violations per window of a long run, hand-offs and early stops, LLM calls, tokens and latency per task, and spread over at least three runs (three passes of one agent on a mid-tier model scored 62%, 69% and 76%); agent-orchestrated RAG used 2.7x to 3.6x the input tokens and 1.4x to 1.5x the time of a fixed pipeline. Check tool outcomes, not completion flags: a production agent's web-tool calls succeeded 27.3% of the time (86.6% for the compiled workflow), yet some of its runs with no successful call were marked complete. Re-run the comparison when the model changes.

## How to measure

- **experiment** (Tier 4): paired runs of the agent loop against a fixed or enforced workflow and one call over code-assembled evidence, on the same model, tools, task set, budget and acceptance checks, on the deployed model and one cheaper tier: success, procedure and constraint violations per window across long runs, hand-offs and early stops, LLM calls, tokens and latency per task, and spread over at least three runs; report tasks with a known procedure and tasks whose path depends on findings separately, score tool outcomes rather than completion flags, and add tool output that fakes an error and proposes a different next step
- **monitor**: distinct action sequences per task type, steps and cost per task, procedure and policy violations caught by checks, compliance late in long runs against early, hand-offs and early stops, cap-hit rate, route transitions blocked by the permitted-call graph, and sequences that recur often enough to compile into code

## Expected impact

- **Quality:** mixed, large: an agent-decided route wins with a strong model where the path depends on findings: harnesses that prescribed none of the model's calls ranked the root cause first in 65 to 77% of 90 incidents against 16 to 53% for hand-crafted procedure agents (Bi, Oct 2026); 12 of 14 comparisons against prescribed pipelines with a GPT-5.5 optimizer (Xue, Aug 2026); query rewriting NDCG@10 55.6 against 52.8 for a fixed step (Ferrazzi, Jan 2026). Code-owned control wins on known procedures and with smaller models: 139.2 against 48.4 faithful and correct decisions on a 200-account procedure with an enforced state machine (Sun, Nov 2026); 35.56% against 10.40% for ReAct on TravelPlanner (Qiu, Aug 2025); a medium optimizer did 3.50 to 9.68 points better with the pipeline (Xue, Aug 2026); 45.3% against 6.7% for a 4B tool-calling agent on WebArena-Verified (Li, Sep 2026). Compiling an agent's runs into code cost 3 to 5 points (93.8% against 96.8% completion, 75.8% against 80.6% on tau2-bench telecom) (Hou, Nov 2026)
- **Cost:** mixed, medium: more than a workflow that calls the model only for bounded steps: compiled workflows cut cost per task 24% on 79 production procedures and planning calls from 12.1 per tau2-bench run to none (Hou, Nov 2026); code-owned control cut LLM calls 76.0 to 91.8% and deployed cost 74.4 to 98.6%, offline training excluded (Li, Sep 2026); agent-orchestrated RAG used 2.7x to 3.6x the input tokens (Ferrazzi, Jan 2026). Not more than elaborate multi-call pipelines: among usable incident runs every cost-Pareto run used a simple harness, from under one cent to about 26 cents per case (Bi, Oct 2026); an agent-composed optimizer used a median 34.3% of a pipeline's target-interaction budget (Xue, Aug 2026); and enforcing a procedure cost 3.5x the free agent's session, which had skipped work (Sun, Nov 2026)
- **Performance:** degrades, medium: choosing the next step took 37 to 43% of execution time for production agents with three to five tools; compiled workflows ran tau2-bench tasks in 1.3 s against 170 s and cut median production time from 68 s to 37 s, though mean time rose from 153 s to 163 s as more slow web calls succeeded (Hou, Nov 2026); agent-orchestrated RAG took 1.4x to 1.5x the time (Ferrazzi, Jan 2026); a tool-calling agent took longer per task than a code-owned harness in all six settings (Li, Sep 2026); 14.0 steps against 10.2 for a coded workflow (Qiu, Aug 2025). Enforcing or bounding the route adds time too: 23% more median time on easy SWE-bench tasks (Sun, Nov 2026), 2.5x per task for a permitted-call graph (Jha, Oct 2025)
- **Security:** degrades, medium: the agent picks each next step, so text in tool output can steer the route: fake error messages redirected an agent orchestrator to run an attacker's code in 83 to 100% of trials and to copy an outside address on an email in 67 to 89%; least privilege did not help where the attack used the task's own agents (67 to 89%), while a graph of permitted calls fixed from the request before any data was read blocked all of them (Jha, Oct 2025; o4-mini and GPT-4o, 16 tasks). Contain input (10.c.i) or fix the plan before reading it (6.c.ii)
- **Governance:** degrades, medium: rules stated only in the prompt get broken, and restating them does not fix it: plain and prompted agents decided 11.9% to 48.6% of their accounts by a stated procedure against 94.8% when a state machine enforced it, and a customer-service agent ended 24 of its 27 failures by handing the customer to a human (Sun, Nov 2026); 835 commonsense-constraint violations for ReAct against 11 for a coded workflow on 1,000 tasks (Qiu, Aug 2025); the agent's route varied more than a staged pipeline's (larger edits and more churn in all 8 paired runs), though final pass/fail agreement was at least 0.78 in 7 of 8 (Xue, Aug 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Simon Willison, "I think “agent” may finally have a widely enough agreed upon definition to be useful jargon now"… (2025-09-18): "An LLM agent runs tools in a loop to achieve a goal."
- Li et al., "Grow the Harness, Not the Context: From Strategy-Free Scaffolds to Reusable Specialist Agents", https://arxiv.org/abs/2609.26760 (2026-09-22): Against the tool-calling agent, LLM calls fell 76.0-91.8% and deployed-agent cost 74.4-98.6%, with the highest mean success in five of six settings (0.7 points behind in the sixth). WebArena-Verified success 45.3 / 44.7 / 45.3% against…
- Xue, Yang, "Rethinking Self-Evolving Agents: Do We Still Need Prescribed Optimization Pipelines?", https://arxiv.org/abs/2608.09629 (2026-08-10): With GPT-5.5 as optimizer, OEO beat SkillOpt in 7 of 8 settings and tied 1, and beat GEPA in 5 of 6 (GEPA's one lead 0.21 points), using a median 34.3% of SkillOpt's target-interaction token budget; optimizer tokens slightly exceeded…
- Ferrazzi, Cvjeticanin, Piraccini, Giannuzzi, "Is Agentic RAG worth it? An experimental comparison of RAG approaches"… (2026-01-12): Query rewriting NDCG@10 55.6 for the agent against 52.8 for the fixed pipeline on average (51.7 against 43.9 on NQ). Intent routing F1 98.8 and 99.8 against 95.7 and 96.6 on two narrow domains, but 64.6 against 87.9 on FEVER. Document…
- …and 5 more sources in `library/entries/inversion-of-control.yaml`.

## Caveats

Each study is small or tests the authors' own method: one optimization run per cell, a single-tool RAG agent capped at three turns, code-harness results with confidence-interval half-widths of 7 to 13 points that exclude offline cost, a coded workflow that encodes the scorer's constraints (with a cross-model table whose caption and figures disagree), a state machine tested on one procedure (three seeds on Sonnet 4.6, where its pre-registered prediction against the resumed baseline failed), a compiled workflow whose public test covers one tau2-bench domain of 40 tasks without a simulated user, and an injection study of 16 tasks on o4-mini and GPT-4o with the authors' own attacks. The winner depends on model tier and task: prescribed structure helped a medium model and was required for a weak one, enforcement gained little where the plain agent already held the procedure, the coded workflow's lead narrowed on ScienceWorld tasks that need discovery, and in the incident study one call over rule-selected evidence also beat every hand-crafted agent, so part of that gain comes from not fixing the investigation rather than from the loop. No study compares an agent-chosen route with a coded workflow at matched cost on the top frontier models (the incident study stopped below them) in real business workflows; the production comparison used a Sonnet 4.0 agent and the platform's own completion flags, which counted some runs with no successful tool call as complete. The older evidence here (a pattern-library listing and a definition) is unmeasured.

## Related

- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
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
