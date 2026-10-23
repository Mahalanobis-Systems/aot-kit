---
name: prompt-chaining-with-gates
description: "AOT optimization 7.a.ii (Tier 4, Restructuring): Prompt chaining with gate checks. Placeholder. Use when an agent shows: Stage outputs; gate failures; retries per stage; the whole chain rerun when one step fails."
---

<!-- Generated from library/entries/prompt-chaining-with-gates.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Prompt chaining with gate checks

> **Placeholder.** Generated from `library/entries/prompt-chaining-with-gates.yaml` (entry 7.a.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.a.ii |
| Earlier id | P13 (Workflow Patterns, from the master cookbook) |
| Tier (proposed) | 4 (Restructuring): it decomposes one call into a gated chain |
| Categories | Orchestration: Routing |
| Change | workflow / orchestration |

## What it is

Split a task that decomposes cleanly into fixed steps into a chain of model calls, one goal per call, with a gate between steps: a schema check, an assertion, or a run against the real system, and an LLM check only for subjective criteria. On a gate failure, rerun only the failed step with its output and the error. The trade is latency and tokens for accuracy and inspectable intermediate outputs; it pays on tasks beyond what one call does reliably, and less as models improve.

## When it applies

- **In the code:** A fixed sequence of model calls with checks between them rather than one prompt.
- **In traces:** Stage outputs; gate failures; retries per stage; the whole chain rerun when one step fails.
- **In eval results:** Per-stage and end-to-end quality.
- **Judge:** Rate each stage's output.
- **Probes:** Inputs that should fail at each gate.

## How (outline)

1. Start from a single call tuned with the same effort; chain only if the task splits cleanly into fixed steps.
2. Give each step one goal and a handoff the next step can validate against a schema.
3. Gate in code first: schema validation or assertions; where you can, run the output against the real system (execute the query) instead of asking the model whether it is valid; use an LLM check with hard thresholds only for subjective criteria.
4. On a failure, rerun only the failed step with its previous output and the error message; cap retries, then stop or continue with a warning; keep outputs that already passed.
5. Run new gates in warn-only mode first and review each halt for false alarms.
6. Log each step's output and gate result; compare the chain with the single call on success, tokens and latency, per model.

## How to measure

- **experiment** (Tier 4): paired eval of the chain against a single call tuned with the same effort, per model: success, tokens, latency
- **monitor**: gate failure and retry rate per step; false-alarm rate on reviewed halts; each error traced to the step that caused it

## Expected impact

- **Quality:** improves, medium: tasks beyond what one call does reliably: well-formatted JSON 37.6% to 98.8% with assertions and retry (DSPy Assertions, 2023); over a tuned single call, orchestration gained at most 4.6 points (Leins, Aug 2026); 37% of gate halts were false alarms in one study (Elina, Sep 2026)
- **Cost:** degrades, medium: more calls: orchestration took about 2 to 4 times the tokens of a single call (Leins, Aug 2026); a fixed chain that reran downstream steps cost 1,632 tokens per retry against 904 for one prompt, and 436 when only the failed step reran (Asthana, May 2026)
- **Performance:** degrades, medium: serial calls; with gates, one model got faster and the other markedly slower (Dhage, Aug 2026)
- **Security:** improves, small (unmeasured): Gates can check policy.
- **Governance:** improves, medium (unmeasured): Checkpoints are auditable.
- **Brand:** improves, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Anthropic (Erik Schluntz, Barry Zhang), "Building effective agents", https://www.anthropic.com/engineering/building-effective-agents (2024-12-19): "You can add programmatic checks (see "gate" in the diagram below) on any intermediate steps to ensure that the process is still on track." Use it when "the task can be easily and cleanly decomposed into fixed subtasks"; "The main goal is…
- Tongshuang Wu, Michael Terry, Carrie J. Cai, "AI Chains: Transparent and Controllable Human-AI Interaction by Chaining Large Language Model… (2021-10-04): "In a 20-person user study, we found that Chaining not only improved the quality of task outcomes, but also significantly enhanced system transparency, controllability, and sense of collaboration."
- Singhvi et al., "DSPy Assertions: Computational Constraints for Self-Refining Language Model Pipelines", https://arxiv.org/abs/2312.13382 (2023-12-20): Well-formatted JSON quizzes 37.6% to 98.8% with assertions and backtracking; valid quiz questions 30.5% to 87.2% with all assertion-driven optimizations. Across four case studies, constraints passed "up to 164% more often" and responses…
- Sun et al., "Prompt Chaining or Stepwise Prompt? Refinement in Text Summarization", https://arxiv.org/abs/2406.00507 (2024-06-01): Chained refinement with GPT-4 won 77 of 100 comparisons against a one-step GPT-4 summary; the stepwise prompt won 53. The authors suggest the stepwise prompt "might produce a simulated refinement process".
- …and 6 more sources in `library/entries/prompt-chaining-with-gates.yaml`.

## Caveats

Chains cost latency and tokens, and a fixed chain that reruns downstream steps on a failure can cost more per retry than one prompt; rerun only the failed step. Gates misfire: in one study 37% of halts were false alarms, enough to turn a gain into a loss. The benefit depends on the model and shrinks as models improve: Anthropic dropped a step-by-step breakdown when a stronger model arrived, and tuned single calls came within a few points of orchestration. Several studies are small (one app, one run).

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)

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
