---
name: inversion-of-control
description: "AOT optimization 7.d.ii (Tier 4, Restructuring): Inversion of control. Placeholder. Use when an agent shows: Variety of action sequences across tasks of the same type: one sequence recurring across most tasks suggests code could own the path; widely varying sequences on a known procedure suggest constraints are being missed."
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

Give the agent the goal, the tools and the acceptance checks and let it choose the sequence of steps, instead of coding a fixed workflow; the goal, permissions, budget and evaluation stay outside the agent. It pays when the path depends on what the agent finds and the model is strong: a GPT-5.5 optimizer that composed its own process beat two prescribed pipelines in 12 of 14 comparisons at a median 34.3% of the target-interaction budget, but a medium model did better with the pipeline. Where the procedure is known and the constraints are hard, or the model is small, a coded workflow wins: 35.56% against 10.40% for same-model ReAct on TravelPlanner, and 45.3% against 6.7% for a 4B tool-calling agent on WebArena-Verified at 98.6% lower cost. Agent-decided steps also cost more per task: 2.7x to 3.6x the input tokens in one RAG comparison.

## When it applies

- **In the code:** Minimal orchestration code; the agent decides the sequence.
- **In traces:** Variety of action sequences across tasks of the same type: one sequence recurring across most tasks suggests code could own the path; widely varying sequences on a known procedure suggest constraints are being missed.
- **In eval results:** Success, constraint violations, LLM calls, tokens and latency per task for the agent loop against a fixed workflow, per model tier.
- **Judge:** Rate whether autonomy was used well.
- **Probes:** Tasks with a known procedure and hard constraints, and tasks whose next step depends on what is found.

## How (outline)

1. Start from two baselines on the same model, tools and task set: the fixed workflow you have or would write (code picks the steps, the model fills bounded nodes) and an agent loop (7.d.iii) that gets the goal, the same tools and the same acceptance checks and picks its own steps.
2. Keep the ends outside the agent in both designs: the goal, permissions, budget caps and the acceptance check or evaluator, so only the route is delegated.
3. Sort tasks by whether the path is known. Where the steps and constraints are stable (a runbook, a recurring task family, hard business rules), code the path and enforce the constraints in code: on TravelPlanner a coded workflow passed 35.56% against 10.40% for same-model ReAct, and writing the same rules into the baselines' prompts left them 12.7 to 20.2 points behind (37.20 against 17.00 to 24.50). Where the next step depends on what is found, let the agent choose: it rewrote retrieval queries better than a fixed rewrite step (NDCG@10 55.6 against 52.8).
4. Delegate the route only to a model that can carry it: a GPT-5.5 optimizer that composed its own process beat two prescribed pipelines in 12 of 14 comparisons, but with a medium model the pipeline won by 3.50 to 9.68 points and a 4B model produced no valid action; on WebArena-Verified, code-owned control held 44.7 to 45.3% while a tool-calling agent scored 30.0% on a 120B model and 12.7% and 6.7% on 20B and 4B models.
5. Mix within one task: keep fixed steps the agent does worse (a fixed reranker scored 49.5 NDCG@10 against 43.9 when the agent re-retrieved on its own), and enforce preconditions on irreversible actions in code (10.b.i); for a task family you run often, move recurring decisions out of the loop into code and keep the model for the semantic steps (76.0 to 91.8% fewer LLM calls in one study).
6. Measure paired runs on the deployed model and one cheaper tier: success, constraint violations, LLM calls, tokens and latency per task, and spread over at least three runs; agent-orchestrated RAG used 2.7x to 3.6x the input tokens and 1.4x to 1.5x the time of a fixed pipeline. Re-run the comparison when the model changes.

## How to measure

- **experiment** (Tier 4): paired runs of the agent loop against a fixed workflow on the same model, tools, task set, budget and acceptance checks, on the deployed model and one cheaper tier: success, constraint violations, LLM calls, tokens and latency per task, and spread over at least three runs; report tasks with a known procedure and tasks whose path depends on findings separately
- **monitor**: distinct action sequences per task type, steps and cost per task, constraint and policy violations caught by checks, cap-hit rate, and sequences that recur often enough to move into code

## Expected impact

- **Quality:** mixed, large: an agent-decided route wins with a strong model where the path depends on findings: 12 of 14 comparisons against prescribed pipelines with a GPT-5.5 optimizer (Xue, Aug 2026); query rewriting NDCG@10 55.6 against 52.8 for a fixed step (Ferrazzi, Jan 2026). A coded workflow wins on known procedures and with smaller models: 35.56% against 10.40% for ReAct on TravelPlanner (Qiu, Aug 2025); a medium optimizer did 3.50 to 9.68 points better with the pipeline (Xue, Aug 2026); 45.3% against 6.7% for a 4B tool-calling agent on WebArena-Verified (Li, Sep 2026)
- **Cost:** degrades, medium: more model calls per task: code-owned control cut LLM calls by 76.0 to 91.8% and deployed cost by 74.4 to 98.6% against a tool-calling agent, offline training excluded (Li, Sep 2026); agent-orchestrated RAG used 2.7x to 3.6x the input tokens of a fixed pipeline (Ferrazzi, Jan 2026). Not always: an agent-composed optimizer used a median 34.3% of a fixed pipeline's target-interaction budget (Xue, Aug 2026)
- **Performance:** degrades, medium: agent-orchestrated RAG took 1.4x to 1.5x the end-to-end time (Ferrazzi, Jan 2026); a tool-calling agent took longer per task than a code-owned harness in all six settings (Li, Sep 2026); 14.0 steps against 10.2 for a coded workflow (Qiu, Aug 2025)
- **Security:** degrades, small (unmeasured): The agent picks each next action, so text in tool output can steer the sequence; contain input (10.c.i) or fix the plan before reading it (6.c.ii).
- **Governance:** degrades, medium: rules stated only in the prompt get broken: 835 commonsense-constraint violations for ReAct against 11 for a coded workflow on 1,000 tasks (Qiu, Aug 2025); the agent's route varied more than a staged pipeline's (larger edits and more churn in all 8 paired runs), though final pass/fail agreement was at least 0.78 in 7 of 8 (Xue, Aug 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Simon Willison, "I think “agent” may finally have a widely enough agreed upon definition to be useful jargon now"… (2025-09-18): "An LLM agent runs tools in a loop to achieve a goal."
- Li et al., "Grow the Harness, Not the Context: From Strategy-Free Scaffolds to Reusable Specialist Agents", https://arxiv.org/abs/2609.26760 (2026-09-22): Against the tool-calling agent, LLM calls fell 76.0-91.8% and deployed-agent cost 74.4-98.6%, with the highest mean success in five of six settings (0.7 points behind in the sixth). WebArena-Verified success 45.3 / 44.7 / 45.3% against…
- Xue, Yang, "Rethinking Self-Evolving Agents: Do We Still Need Prescribed Optimization Pipelines?", https://arxiv.org/abs/2608.09629 (2026-08-10): With GPT-5.5 as optimizer, OEO beat SkillOpt in 7 of 8 settings and tied 1, and beat GEPA in 5 of 6 (GEPA's one lead 0.21 points), using a median 34.3% of SkillOpt's target-interaction token budget; optimizer tokens slightly exceeded…
- Ferrazzi, Cvjeticanin, Piraccini, Giannuzzi, "Is Agentic RAG worth it? An experimental comparison of RAG approaches"… (2026-01-12): Query rewriting NDCG@10 55.6 for the agent against 52.8 for the fixed pipeline on average (51.7 against 43.9 on NQ). Intent routing F1 98.8 and 99.8 against 95.7 and 96.6 on two narrow domains, but 64.6 against 87.9 on FEVER. Document…
- …and 1 more sources in `library/entries/inversion-of-control.yaml`.

## Caveats

Each study is small or tests the authors' own method: the optimizer comparison is one run per cell, the RAG comparison caps a single-tool agent at three turns, the code-harness results have confidence-interval half-widths of 7 to 13 points on 50 tasks and exclude the offline optimization cost, and the coded-workflow paper encodes the benchmark scorer's constraints and has a cross-model table whose caption and figures disagree. The winner depends on the model and the task, so a result on one model tier does not transfer: prescribed structure helped a medium model and was required for a weak one. The coded workflow's advantage narrowed on open-ended ScienceWorld tasks that need discovery, where both designs failed. The older evidence here (a pattern-library listing and a definition) is unmeasured.

## Related

- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)

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
