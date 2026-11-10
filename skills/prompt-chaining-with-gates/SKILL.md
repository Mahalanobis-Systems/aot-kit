---
name: prompt-chaining-with-gates
description: "AOT optimization 7.a.ii (Tier 4, Restructuring): Prompt chaining with gate checks. Placeholder. Use when an agent shows: Stage outputs; gate failures by category (format-only, such as valid JSON inside a markdown fence, against schema or value violations); retries per stage; the whole chain rerun when one step fails; intermediates validated only at the end of the chain."
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

Split a cleanly decomposable task into a fixed chain of model calls with a code check between steps, and rerun only the step that fails. Give each call one goal; gate with a schema check, an assertion or a run against the real system, and use an LLM check only for subjective criteria. The trade is latency and tokens for accuracy and inspectable intermediate outputs, and it pays only on tasks beyond what one call does reliably: on coding tasks a current strong model mostly solved alone, a three-call chain cost 3.2 times as much and took 3.2 times as long for no gain, while on recurring tasks a fixed program was far cheaper and more consistent than an agent loop. Where a chain beat one call, the gain came mostly from the split and its focused prompts rather than from the gate (one study, small models), and gates misfire: 37% of halts were false alarms in one study, and about half of the failures on markdown-fenced JSON in another were valid once the fence was stripped.

## When it applies

- **In the code:** A fixed sequence of model calls with checks between them rather than one prompt.
- **In traces:** Stage outputs; gate failures by category (format-only, such as valid JSON inside a markdown fence, against schema or value violations); retries per stage; the whole chain rerun when one step fails; intermediates validated only at the end of the chain.
- **In eval results:** Per-stage and end-to-end quality.
- **Judge:** Rate each stage's output.
- **Probes:** Inputs that should fail at each gate.

## How (outline)

1. Start from a single call tuned with the same effort on the same model, and for a recurring task also from the agent loop; chain only if the task splits cleanly into fixed steps and the single call fails on it. On coding tasks a current strong model mostly solved alone, a planner, coder and reviewer chain cost 3.2 times as much, took 3.2 times as long and solved no more; a cheap model in the planner and reviewer roles left it dearer, slower and 8.1 points less accurate than the single call, so to save cost choose the model per task first (1.b.i). Against an agent loop on recurring analytics tasks, a fixed program with model calls only at judgment points used about 70 times fewer input tokens and a third of the runtime, and was correct on every run.
2. Give each step one goal and a typed handoff the next step can validate against a schema, and validate it right after the call that produced it, before the next call: in one study an unvalidated intermediate failed only at final assembly, after the next call had already run.
3. Gate in code first: schema validation or assertions; where you can, run the output against the real system (execute the query) instead of asking the model whether it is valid; use an LLM check with hard thresholds only for subjective criteria. Strip format wrappers before validating and record what remains: in one study 48.0% of failures on markdown-fenced JSON validated once the fence was removed.
4. On a failure, rerun only the failed step with its previous output and the specific violation, not a generic parse error: in that study all 24 of Claude Haiku 4.5's steps that exhausted their retries ended on a length cap, and the parse error returned for their fenced attempts never named it. Cap retries (up to three further attempts completed 948 of 973 runs there), and never rerun the whole chain on a deterministic validation error (six calls per injected fault, then a silently dropped item, in another study).
5. When retries run out, stop or continue with a warning, keep outputs that already passed, and record the failure.
6. Run new gates in warn-only mode first and review each halt for false alarms.
7. Log each step's output, gate result and attempts; compare the chain with the single call (and with the agent loop where it is the alternative) on success, tokens, cost per solved task and latency, per model.

## How to measure

- **experiment** (Tier 4): paired eval of the chain against a single call tuned with the same effort (and against the agent loop for recurring tasks), per model and reasoning effort, several runs per arm: success, tokens, cost per solved task, latency
- **monitor**: per step: first-attempt gate pass rate, attempts per completed step, retry and halt rate, and failure category (format-only, schema, value range); false-alarm rate on reviewed halts; each error traced to the step that caused it

## Expected impact

- **Quality:** improves, medium: tasks beyond what one call does reliably: well-formatted JSON 37.6% to 98.8% with assertions and retry (DSPy Assertions, 2023); a fixed program 1.00 accuracy against 0.97 for a skill-guided agent loop (Sabouri, Oct 2026); none where a strong reasoning model already succeeds: -0.5 points pass@1 for a three-call chain (Zettl, Oct 2026); over a tuned single call, orchestration gained at most 4.6 points (Leins, Aug 2026); the split gave up to +0.075 F1 and the typed gate -0.003 to +0.013 (Zuppardo, Oct 2026); 37% of gate halts were false alarms in one study (Elina, Sep 2026)
- **Cost:** mixed, medium: against one call, more calls: a three-call chain 3.20 times the cost (Zettl, Oct 2026), orchestration about 2 to 4 times the tokens (Leins, Aug 2026); a fixed chain that reran downstream steps cost 1,632 tokens per retry against 904 for one prompt, and 436 when only the failed step reran (Asthana, May 2026); against an agent loop on recurring tasks, 321 input tokens per run against 23,138 (Sabouri, Oct 2026)
- **Performance:** mixed, medium: against one call, serial calls: 3.20 times the wall time for a three-call chain (Zettl, Oct 2026); with gates, one model got faster and the other markedly slower (Dhage, Aug 2026); against an agent loop on recurring tasks, 1.5 s against 4.4 s per run (Sabouri, Oct 2026)
- **Security:** improves, small (unmeasured): Gates can check policy.
- **Governance:** improves, medium (unmeasured): Checkpoints are auditable.
- **Brand:** improves, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Anthropic (Erik Schluntz, Barry Zhang), "Building effective agents", https://www.anthropic.com/engineering/building-effective-agents (2024-12-19): "You can add programmatic checks (see "gate" in the diagram below) on any intermediate steps to ensure that the process is still on track." Use it when "the task can be easily and cleanly decomposed into fixed subtasks"; "The main goal is…
- Tongshuang Wu, Michael Terry, Carrie J. Cai, "AI Chains: Transparent and Controllable Human-AI Interaction by Chaining Large Language Model… (2021-10-04): "In a 20-person user study, we found that Chaining not only improved the quality of task outcomes, but also significantly enhanced system transparency, controllability, and sense of collaboration."
- Singhvi et al., "DSPy Assertions: Computational Constraints for Self-Refining Language Model Pipelines", https://arxiv.org/abs/2312.13382 (2023-12-20): Well-formatted JSON quizzes 37.6% to 98.8% with assertions and backtracking; valid quiz questions 30.5% to 87.2% with all assertion-driven optimizations. Across four case studies, constraints passed "up to 164% more often" and responses…
- Sun et al., "Prompt Chaining or Stepwise Prompt? Refinement in Text Summarization", https://arxiv.org/abs/2406.00507 (2024-06-01): Chained refinement with GPT-4 won 77 of 100 comparisons against a one-step GPT-4 summary; the stepwise prompt won 53. The authors suggest the stepwise prompt "might produce a simulated refinement process".
- …and 10 more sources in `library/entries/prompt-chaining-with-gates.yaml`.

## Caveats

Chains cost latency and tokens: on tasks a current strong model already solved, a three-call chain cost 3.2 times as much and took 3.2 times as long for no gain, and a chain that reruns downstream steps on a failure can cost more per retry than one prompt. Gates misfire and can mislead retries: in one study 37% of halts were false alarms, enough to turn a gain into a loss; in another, a markdown fence hid the real violation from the retry message. The benefit depends on the model and shrinks as models improve: Anthropic dropped a step-by-step breakdown when a stronger model arrived, tuned single calls came within a few points of orchestration, and where a chain did win, the typed gate added at most 0.013 F1 over the split alone (7-8B models, one dataset). Several studies are small (one app, one run, one benchmark category), and the agent-loop comparison is a single preliminary study on one model.

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)

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
