---
name: evaluator-optimizer-loop
description: "AOT optimization 7.c.iii (Tier 4, Restructuring): Evaluator-optimizer loop. Placeholder. Use when an agent shows: Rounds per item; evaluator score per round next to an independent check; veto rate and recovery after a veto; items whose evaluator score rose while the independent check fell; revisions that rewrote parts that had passed."
---

<!-- Generated from library/entries/evaluator-optimizer-loop.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Evaluator-optimizer loop

> **Placeholder.** Generated from `library/entries/evaluator-optimizer-loop.yaml` (entry 7.c.iii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.iii |
| Earlier id | P17 (Workflow Patterns, from the master cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a generate-evaluate loop to the workflow |
| Categories | Orchestration: Scaling compute |
| Change | workflow / reflection |

## What it is

A separate evaluator (an LLM judge with written criteria, a different model, or an agent that tests the running app) scores the generator's output and returns specific findings; the generator revises until the output passes or a round cap is hit. It pays when the task is beyond what the generator does reliably in one pass and the evaluator is more reliable than the generator: a production diff judge vetoed about a quarter of coding-agent sessions, and half of those recovered. It fails when the judge is weak or shares the generator's blind spots: judge loops left table extraction worse than the first output and raised essay scores while human scores fell. Most of the gain comes in the first two to four rounds, at roughly twice the tokens of one call.

## When it applies

- **In the code:** A generate, evaluate, revise loop: a separate evaluator call, model or tool-using agent scores the output against written criteria and returns feedback, with a pass threshold and a round cap. Flag an evaluator that shares the generator's dialogue history, one weaker than the generator, no cap, or a loop that returns the last version instead of the best.
- **In traces:** Rounds per item; evaluator score per round next to an independent check; veto rate and recovery after a veto; items whose evaluator score rose while the independent check fell; revisions that rewrote parts that had passed.
- **In eval results:** Quality per round on a grader the loop never sees; share of items that end worse than their first output; evaluator agreement with human or gold labels.
- **Judge:** The evaluator is a judge; a meta-judge checks its agreement with humans.
- **Probes:** Items with a clear rubric and a known defect.

## How (outline)

1. Start from the single pass, tuned with the same effort, and from best-of-N at equal tokens; add the loop only where outputs often fall short and no compiler, test or execution check can judge them (if one exists, feed its verdict back instead, 9.a.i).
2. Write the evaluator's criteria as a few gradable items, each with a hard pass threshold, and calibrate it with a few scored examples; where possible let it check by acting (drive the app with Playwright, compare the diff with the original request). The same criteria in the generator's prompt also steer the first draft.
3. Make the evaluator separate and skeptical: its own call and context, not the generator's dialogue history; a model at least as capable as the generator; tune its prompt by reading its logs against your own verdicts until it stops approving problems it found. Check it on labeled good and bad outputs and planted-defect probes before wiring it in. A judge from another model family does not remove favoritism (judges favor any model whose mistakes resemble theirs), and content-free answers such as ':' or 'Thought process:' can pass it, so include them among the probes.
4. Return findings the generator can act on (failing criterion or checklist item, where, expected against actual; told which checklist items failed, Gemini 2.5 Pro went from 29.5 to 94.7, against -2.5 to +2.6 with no feedback) and tell it to keep what already passed; unconstrained regeneration breaks parts that were right.
5. Stop on pass or after a low cap (most gains came in the first 2 to 4 rounds); raise the cap only if the per-round curve keeps rising. Return the best version rather than the last, and stop early when the score stalls or drops.
6. Measure against a check the loop never sees (a human-labeled sample or a deterministic metric), per round: quality, share of items that end worse than their first output, evaluator agreement with the audit, tokens and latency.

## How to measure

- **experiment** (Tier 4): paired eval of the loop against the single pass and against best-of-N at equal tokens, per model, graded by a check the loop never sees (human-labeled sample or deterministic metric): quality per round, share of items ending worse than their first output, tokens, latency
- **monitor**: rounds per item, first-pass rate, veto rate and recovery rate after a veto, cap-hit rate; on a regularly audited sample, evaluator verdicts against human labels and drift between evaluator scores and the audit

## Expected impact

- **Quality:** mixed, medium: gains where the generator falls short and the critic is reliable: CodeContests 7.88 to 16.24 with a trained critic over five rounds, 12.48 with GPT-4o as critic (Xie, Feb 2025); Self-Refine +4.6 and +1.9 points over a tuned single call, -0.3 on chess (Leins, Aug 2026); losses where the judge is weak: table extraction 0.792 to 0.772 TEDS after 8 rounds (Kim, Jul 2026), essay judge scores rose while human scores fell (Pan, Jul 2024)
- **Cost:** degrades, medium: an evaluator call plus a revision per round: Self-Refine took 1.82 to 2.13 times the tokens of a tuned single call (Leins, Aug 2026); in one app build the QA rounds cost $3.24, $3.09 and $4.06 of $124.70, and the rebuilds they triggered $36.89 and $5.88 (Rajasekaran, Mar 2026)
- **Performance:** degrades, large: serial rounds; an evaluator that clicks through the running app took 6.8 to 9.6 minutes per round, and a 5 to 15 round design loop ran up to four hours (Rajasekaran, Mar 2026)
- **Security:** none (unmeasured)
- **Governance:** improves, small (unmeasured): Criteria are explicit.
- **Brand:** improves, medium (unmeasured): Polished output.

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Anthropic (Erik Schluntz, Barry Zhang), "Building effective agents", https://www.anthropic.com/engineering/building-effective-agents (2024-12-19): "one LLM call generates a response while another provides evaluation and feedback in a loop"; "particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value."
- Prithvi Rajasekaran (Anthropic), "Harness design for long-running application development"… (2026-03-24): "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work". Out of the box the evaluator would "identify legitimate issues, then talk itself into deciding they…
- Max Charas, Marc Bruggmann (Spotify), "Background Coding Agents: Predictable Results Through Strong Feedback Loops (Honk, Part 3)"… (2025-12-09): "out of thousands of agent sessions, the judge vetoes about a quarter of them. When that happens, the agent is able to course correct half the time." The most common trigger is "the agent going outside the instructions outlined in the…
- Zhihui Xie, Jie Chen, Liyu Chen, Weichao Mao, Jingjing Xu, Lingpeng Kong, "Teaching Language Models to Critique via Reinforcement… (2025-02-05): Qwen2.5-Coder generator, Pass@1 averaged over CodeContests, LiveCodeBench and MBPP+: zero-shot 38.75; after five critique rounds 38.30 with its own critique, 39.98 with GPT-4o, 42.77 with the trained critic. CodeContests 7.88 to 12.48…
- …and 10 more sources in `library/entries/evaluator-optimizer-loop.yaml`.

## Caveats

Most studies are small or single-run (one app per harness, 150 Bash questions, 23 essays), and the largest critic gain came from a critic trained for its generator, which is closer to 7.c.ii; prompted critics, GPT-4o included, helped less and over five rounds cut MBPP+ from 77.83 to 74.60. On outputs with no deterministic check the evaluator's own error decides the sign: judges tied, inflated scores and were gamed when they shared the generator's blind spots or context. Gains shrink as generators improve: Anthropic found the evaluator unnecessary overhead for tasks within the newer model's reach, and in one study the loop helped only the weakest of six generators. The 2 to 4 round finding comes from a setup where ground truth decided which answers got feedback, so it describes a best case.

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)

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
