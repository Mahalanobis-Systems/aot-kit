---
name: evaluator-optimizer-loop
description: "AOT optimization 7.c.iii (Tier 4, Restructuring): Evaluator-optimizer loop. Placeholder. Use when an agent shows: Rounds per item and rounds to pass; evaluator score per round next to an independent check; veto rate and recovery after a veto; items whose evaluator score rose while the independent check fell; revisions that rewrote parts that had passed or ran out of budget; findings repeated on code unchanged since the first pass."
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

Have a separate, skeptical evaluator check each output against written criteria and send back specific findings, revising until it passes or a low round cap. It pays when the task is beyond what the generator does reliably in one pass and the evaluator is at least as strong and sees every requirement: a production diff judge vetoed about a quarter of coding-agent sessions and half of those recovered, and a strong grader lifted a weak writer's projects more than the writer's own grading did. On strong current models most of the gain is extra budget: given the same rounds without feedback, Opus 5.5 and GPT-6 Sol came within a point of the loop, and at equal calls best-of-four sampling matched or beat a reviewer loop in 13 of 16 code-quality comparisons. It backfires when the evaluator is weak, blind to the requirements or gamed: feedback from a judge that could not see the instructions left outputs worse than no feedback and worse each round, judge loops degraded table extraction and inflated essay scores, and attackers revised code to a reviewer's findings to get vulnerable changes approved.

## When it applies

- **In the code:** A generate, evaluate, revise loop: a separate evaluator call, model or tool-using agent scores the output against written criteria and returns feedback, with a pass threshold and a round cap. Flag an evaluator that shares the generator's dialogue history, one weaker than the generator, one not shown the request, policy or source the output must respect, feedback that is only a score, no cap, re-review that repeats posted findings, or a loop that returns the last version instead of the best.
- **In traces:** Rounds per item and rounds to pass; evaluator score per round next to an independent check; veto rate and recovery after a veto; items whose evaluator score rose while the independent check fell; revisions that rewrote parts that had passed or ran out of budget; findings repeated on code unchanged since the first pass.
- **In eval results:** Quality per round on a grader the loop never sees, against the same model given the same rounds or budget without feedback and against best-of-N at equal calls; share of items that end worse than their first output; evaluator agreement with human or gold labels, and the spread of its scores when it re-grades the same output.
- **Judge:** The evaluator is a judge; a meta-judge checks its agreement with humans.
- **Probes:** Items with a clear rubric and a known defect.

## How (outline)

1. Start from three baselines: the single pass tuned with the same effort, best-of-N at equal calls, and the same model given the same extra rounds or budget with no feedback. Add the loop only where outputs often fall short and no compiler, test or execution check can judge them (if one exists, feed its verdict back instead, 9.a.i). On strong current models the baselines take most of the gain: with seven models as writers and graders of data science projects, Opus 5.5 and GPT-6 Sol scored 94% and 93% after two rounds of feedback against 93% and 92% revising twice without it, and at four calls best-of-four ranked by a static analyzer matched or beat a coder-reviewer loop in 13 of 16 code-quality comparisons. The loop paid for weaker writers (GPT-6 Luna 78% to 87%) and where the writer had broken a rule without knowing it (Haiku 4.5, 8% to 45%, once told its data were generated, not real).
2. Write the evaluator's criteria as a few gradable items, each with a hard pass threshold, and calibrate it with a few scored examples; where possible let it check by acting (drive the app with Playwright, run the code and read the result, compare the diff with the original request). Show it everything the output must respect: the request, the system prompt or policy, and the source the output draws on. In one study, revising on reports from a judge shown only the response cut instruction constraints met from 84% to 70% in one round while a revise-only control rose to 87%, and it fell again each round; a judge that saw the request without its separately stated constraints still lost 8 points. The same criteria in the generator's prompt also steer the first draft.
3. Make the evaluator separate and skeptical: its own call and context, not the generator's dialogue history, and a model at least as capable as the generator. A stronger grader lifted a weak writer (Haiku 4.5's final projects scored 45% by other graders when Opus 5.5 graded the rounds, 36% when it graded itself), weaker graders did not improve stronger writers, and models grading their own work scored it about 9 points higher than other graders did. Tune its prompt by reading its logs against your own verdicts until it stops approving problems it found. Check it on labeled good and bad outputs and planted-defect probes before wiring it in, including defects the rubric does not name: seven graders' marks barely moved for planted errors such as tests that assert nothing or a wrong headline result. A judge from another model family does not remove favoritism (judges favor any model whose mistakes resemble theirs), and content-free answers such as ':' or 'Thought process:' can pass it, so include them among the probes.
4. Return findings the generator can act on (failing criterion or checklist item, where, expected against actual) rather than a score: told which checklist items failed, Gemini 2.5 Pro went from 29.5 to 94.7, against -2.5 to +2.6 with no feedback, and in another study a bare 1 to 5 score gained less than no report at all (+3.6 against +5.9 points). Net gain follows the precision of the findings, since false findings make the generator break what was right (acting only on a blind judge's most severe complaint cut its harm by about 60% but did not remove it); tell the generator to keep what already passed, because unconstrained regeneration breaks parts that were right.
5. Stop on pass or after a low cap, and raise the cap only if the per-round curve keeps rising on an independent check: most gain came from the first round of feedback (+13 points, then +5, with 35 of 147 runs falling in the third round), and other studies found most in the first 2 to 4 rounds. Give each revision room to finish: revisions that ran out of tool calls or time broke 24 of 99 working projects, against 2 of 115 that ended on their own. Return the best version rather than the last, and stop early when the score stalls or drops.
6. When the author is also an agent (code-review bots), make the loop converge: the two can keep each other busy indefinitely (one pull request ran more than fifty review-and-fix rounds overnight, and 59% of repeat flags were on code there since the first pass). After the first passes re-review only the new diff, never repeat a posted finding, flag a bug class once, and after three rounds ask the author to reconsider the approach; at Anthropic mean reviews to pass fell from 2.08 to 1.32 and pull requests needing five or more rounds from 8.9% to 1.5%. Where the author may be adversarial or the change is security-relevant, also re-check the whole change against the original requirement before approval: an attacker revising code to an AI reviewer's findings got exploitable changes approved in 20.8% of 159 cases within five rounds, while re-inspecting the whole diff each round caught 22 and a root-cause check 23 of the 33 that ordinary review approved.
7. Measure against a check the loop never sees (a human-labeled sample or a deterministic metric), per round and against the no-feedback and best-of-N baselines: quality, share of items that end worse than their first output, evaluator agreement with the audit, tokens and latency. Re-grade a sample several times to learn the evaluator's own noise: in one study about half of later-round score changes were within it.

## How to measure

- **experiment** (Tier 4): paired eval of the loop against the single pass, best-of-N at equal calls and the same model given the same extra rounds or budget without feedback, per model, graded by a check the loop never sees (human-labeled sample or deterministic metric): quality per round, share of items ending worse than their first output, tokens, latency; re-grade a sample several times to estimate the evaluator's own noise
- **monitor**: rounds per item and rounds to pass, first-pass rate, veto rate and recovery rate after a veto, cap-hit rate, findings repeated on unchanged code; on a regularly audited sample, evaluator verdicts against human labels and drift between evaluator scores and the audit

## Expected impact

- **Quality:** mixed, medium: gains where the generator falls short and the critic is reliable: CodeContests 7.88 to 16.24 with a trained critic over five rounds, 12.48 with GPT-4o as critic (Xie, Feb 2025); a weaker writer's projects 87% against 78% revising without feedback (Alexander, Nov 2026); little on strong generators: Opus 5.5 94% against 93% without feedback (Alexander, Nov 2026), Self-Refine +4.6 and +1.9 points over a tuned single call (Leins, Aug 2026), best-of-four matched or beat a reviewer loop in 13 of 16 code-quality cells (Kadam, Oct 2026); losses where the judge is weak or blind: constraints met 84% to 70% with a judge that could not see the instructions (Kumar, Oct 2026), table extraction 0.792 to 0.772 TEDS after 8 rounds (Kim, Jul 2026), essay judge scores rose while human scores fell (Pan, Jul 2024)
- **Cost:** degrades, medium: an evaluator call plus a revision per round: Self-Refine took 1.82 to 2.13 times the tokens of a tuned single call (Leins, Aug 2026); each revision round of a data science project cost $0.32 to $0.35 on average against $0.68 for the first submission (Alexander, Nov 2026); in one app build the QA rounds cost $3.24, $3.09 and $4.06 of $124.70, and the rebuilds they triggered $36.89 and $5.88 (Rajasekaran, Mar 2026); before a round cap, pull requests took 2.08 reviews on average to pass (Osmani, Oct 2026)
- **Performance:** degrades, large: serial rounds; an evaluator that clicks through the running app took 6.8 to 9.6 minutes per round, and a 5 to 15 round design loop ran up to four hours (Rajasekaran, Mar 2026); without a cap, an agent author and an agent reviewer ran more than fifty rounds overnight on one pull request (Osmani, Oct 2026)
- **Security:** degrades, medium: where the author may be adversarial, the evaluator's findings guide it: revising code to an AI reviewer's findings got exploitable changes approved in 20.8% (Sonnet 5 reviewer) and 15.7% (GPT-5.5) of 159 cases within five rounds, against 8.2% and 1.3% for the strongest text- or comment-based attack, and 11.9% when the reviewer gave only its verdict; a root-cause check each round caught 23 of 33 (Gong, Oct 2026)
- **Governance:** improves, small (unmeasured): Criteria are explicit.
- **Brand:** improves, medium (unmeasured): Polished output.

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Anthropic (Erik Schluntz, Barry Zhang), "Building effective agents", https://www.anthropic.com/engineering/building-effective-agents (2024-12-19): "one LLM call generates a response while another provides evaluation and feedback in a loop"; "particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value."
- Prithvi Rajasekaran (Anthropic), "Harness design for long-running application development"… (2026-03-24): "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work". Out of the box the evaluator would "identify legitimate issues, then talk itself into deciding they…
- Max Charas, Marc Bruggmann (Spotify), "Background Coding Agents: Predictable Results Through Strong Feedback Loops (Honk, Part 3)"… (2025-12-09): "out of thousands of agent sessions, the judge vetoes about a quarter of them. When that happens, the agent is able to course correct half the time." The most common trigger is "the agent going outside the instructions outlined in the…
- Zhihui Xie, Jie Chen, Liyu Chen, Weichao Mao, Jingjing Xu, Lingpeng Kong, "Teaching Language Models to Critique via Reinforcement… (2025-02-05): Qwen2.5-Coder generator, Pass@1 averaged over CodeContests, LiveCodeBench and MBPP+: zero-shot 38.75; after five critique rounds 38.30 with its own critique, 39.98 with GPT-4o, 42.77 with the trained critic. CodeContests 7.88 to 12.48…
- …and 16 more sources in `library/entries/evaluator-optimizer-loop.yaml`.

## Caveats

Most studies are small or single-run (one app per harness, 150 Bash questions, 23 essays, one single-author study of 147 runs on one assignment), and the largest critic gain came from a critic trained for its generator, which is closer to 7.c.ii; prompted critics, GPT-4o included, helped less and over five rounds cut MBPP+ from 77.83 to 74.60. On outputs with no deterministic check the evaluator's own error decides the sign: judges tied, inflated scores, missed planted errors and were gamed when they shared the generator's blind spots or context or could not see the requirements, and in one study about half of later-round score changes fell within the grader's own repeat noise. Gains shrink as generators improve: Anthropic found the evaluator unnecessary overhead for tasks within the newer model's reach, the strongest current writers came within a point of the loop when given the same rounds without feedback, and in one study the loop helped only the weakest of six generators. The code-review convergence figures are a vendor's before-and-after on its own pull requests, the blind-judge harm was measured with small open responders, and the 2 to 4 round finding comes from a setup where ground truth decided which answers got feedback, so it describes a best case.

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:no-self-written-tests` (9.c.i, Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests)
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
