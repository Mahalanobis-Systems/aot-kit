---
name: reflection-loop
description: "AOT optimization 7.c.i (Tier 3, Tuning): Reflection loop. Placeholder. Use when an agent shows: Rounds per item; share of rounds whose critique changes the answer; on items with ground truth, right-to-wrong and wrong-to-right flips per round; whether the critique cites a test, error or requirement or only restates the answer; tokens per round."
---

<!-- Generated from library/entries/reflection-loop.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Reflection loop

> **Placeholder.** Generated from `library/entries/reflection-loop.yaml` (entry 7.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.i |
| Earlier id | P37 (Feedback & Iteration, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it adds a refine step graded against a metric |
| Categories | Orchestration: Scaling compute |
| Change | workflow / reflection |

## What it is

The same model critiques and revises its own output for a few rounds (Self-Refine), or after a failed attempt writes a short lesson it carries into the next try (Reflexion). It pays when the critique has something to stand on, such as a failing test, an error, an environment reward or a checkable constraint (Reflexion on hard Rust problems went from 0.60 to 0.68 with its tests and fell to 0.52 without them), or when it judges form rather than correctness. Asked only to re-check whether an answer is right, models often break right ones as well as fix wrong ones: one revision pass lowered accuracy in 20 of 28 BoolQ settings across open-weight models, every RefineBench model (GPT-5 and o1 included) moved by -2.5 to +2.6 points over five turns, and plain retries against the tests beat Reflexion on HumanEval at lower cost. Revision can still help long reasoning (one study found significant gains on BBEH Non-Choice for all five models and on HLE for two), but there it turned up to 13.25% of right answers wrong against at most 2.1% on checkable SAT constraints, so gate the loop by how checkable the answer is. On reasoning models an outer loop mostly adds tokens: over five self-refinement turns on RefineBench, o1 went from 18.5 to 18.3 and DeepSeek-R1 from 8.1 to 7.9.

## When it applies

- **In the code:** A step where the same model critiques its own output and a step that revises it (a reflect, critique or "double-check your answer" call), or verbal reflections stored between attempts, with a round cap. Flag a loop that re-checks correctness with no test, error, environment signal or explicit checklist in the critique, no cap, one that always returns the last revision, and an outer reflect step on a reasoning model with thinking on.
- **In traces:** Rounds per item; share of rounds whose critique changes the answer; on items with ground truth, right-to-wrong and wrong-to-right flips per round; whether the critique cites a test, error or requirement or only restates the answer; tokens per round.
- **In eval results:** Accuracy per round against the single pass and against retries or best-of-N at equal tokens; share of initially right answers the loop breaks.
- **Judge:** Rate critiques for specificity.
- **Probes:** Correct outputs mixed with outputs carrying one detectable defect.

## How (outline)

1. Start from the baselines on your own items: the single pass with the model's own thinking on or a higher effort (1.b.i), and retries or best-of-N at the same tokens (9.c.ii). Plain retries against HumanEval's example tests scored 92.0% for $2.51 where Reflexion scored 87.8% for $3.90.
2. Add the loop only where the critique has a signal to work from (a failing test, a compiler or runtime error, an environment reward, a constraint the model can check such as a formula, required fields or a length limit) or where it judges form (tone, format, coverage of required items) rather than correctness. If the check is sound, feed its verdict back instead (9.a.i); if the critic needs written criteria and its own context, use 7.c.iii. Do not add an outer "check your answer" step on a reasoning model with thinking on.
3. Put the signal or the checklist into the critique prompt: the error, the failing test, the list of requirements (given the full checklist, Gemini 2.5 Pro scored 44.5 points above open self-refinement, which gained 1.8 over five turns). On a non-reasoning model, try appending "Wait" after its own output before the critique: 14 such models fixed injected errors in their own output 64.5% less often than the same errors in the user's message, and appending "Wait" cut that gap by 89.3%. Use a neutral instruction that keeps the answer unless something contradicts it; on BoolQ every refinement prompt lowered mean accuracy, and more forceful ones added more harmful flips than helpful ones.
4. Cap rounds at one to three and stop when the check passes or the critique finds nothing to fix; Self-Refine capped at four, with most of the gain in the first iterations.
5. Keep the first answer unless the revision is better by the metric: accept it only when the check passes or the score rises, otherwise return the original. A trained gate took Qwen2.5-7B on BoolQ to 86.02% where always revising gave 72.32%, though the author flags the gate's gains as unverified.
6. When attempts repeat (agent episodes, test-driven retries), store each failure's short verbal reflection and give the last few to the next attempt (Reflexion kept 1 to 3); that is where reflection beat plain retry: 130 of 134 ALFWorld tasks while the retry-only agent stopped improving after six trials.
7. Measure on held-out items with ground truth the loop never sees: accuracy per round against both baselines at matched tokens, the share of right answers turned wrong and of wrong ones fixed per round (one untrained model turned 15.8% of MATH problems from right to wrong), and tokens and latency per item; re-run on every model upgrade.

## How to measure

- **experiment** (Tier 3): paired eval on held-out items with ground truth the loop never sees: the loop against the single pass with thinking on and against retries or best-of-N at matched tokens, per model; accuracy per round, share of right answers turned wrong and of wrong answers fixed per round, tokens and latency
- **monitor**: rounds per item, share of rounds that change the answer, gate acceptance rate, check-pass rate after each round, cap-hit rate; on a regularly audited sample, right-to-wrong flips

## Expected impact

- **Quality:** mixed, medium: gains where a signal or checkable constraint exists: hard Rust problems 0.60 to 0.68 with self-written tests, 0.52 without (Shinn, Mar 2023); SAT 34.62% to 64.96% on Mistral Large with at most 2.1% of right answers broken (Stav, Jun 2026); constrained generation 15.0 to 45.0 on GPT-4 (Madaan, Mar 2023). Mixed on re-checks of correctness: significant gains on BBEH Non-Choice for all five models and on HLE for two, with up to 13.25% of right answers turned wrong (Stav, Jun 2026); MATH 52.8% to 51.8% with Self-Refine (Kumar, Sep 2024); lower accuracy in 20 of 28 BoolQ settings (Zhang, Sep 2026); -2.5 to +2.6 points over five turns for every RefineBench model (Lee, Nov 2025); Reflexion 87.8% against plain retry 92.0% on HumanEval (Kapoor, Jul 2024); over 90% of in-thinking reflections confirmatory in reasoning models (Kang, Oct 2025)
- **Cost:** degrades, medium: at least one critique and one revision call per round: Reflexion cost $3.90 on HumanEval against $1.93 for one GPT-4 call and $2.51 for plain retry (Kapoor, Jul 2024); inside reasoning models, reflections after the first answer took 16.8% to 47.8% of tokens for 1.4 to 3.5 points (Kang, Oct 2025)
- **Performance:** degrades, medium (unmeasured): each round is a serial critique and revision call; no source here measures the latency
- **Security:** none (unmeasured)
- **Governance:** none (unmeasured)
- **Brand:** improves, small (unmeasured): Polished output where the critique is about form (tone, format, required items).

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback", https://arxiv.org/abs/2303.17651 (2023-03-30): "improving by ~20% absolute on average in task performance" over one-step generation. Per task, GPT-4 base to Self-Refine: dialogue response preference 25.4 to 74.6, constrained generation 15.0 to 45.0, code optimization 27.3 to 36.0, math…
- Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao, "Reflexion: Language Agents with Verbal… (2023-03-20): ALFWorld: ReAct + Reflexion completed "130 out of 134 tasks"; the ReAct-only agent, which also reset and retried, stopped improving: "performance increase halts between trials 6 and 7". HotpotQA (CoT with the gold context, exact-match…
- Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan, "AI Agents That Matter"… (2024-07-01): Mean of 5 runs, accuracy and total cost: Reflexion (GPT-4) 87.8% and $3.90 (91.0 in its own paper); retry 92.0% and $2.51; warming 93.2% and $2.45; one GPT-4 call 89.6% and $1.93. "Reflexion and LDB cost over 50% more than the warming…
- Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi Singh, et al. (Google DeepMind), "Training Language Models to… (2024-09-19): MATH, Gemini 1.5 Flash, first to second attempt: base model 52.6% to 41.4% (-11.2; 15.8% of problems went from correct to incorrect, 4.6% the other way); Self-Refine 52.8% to 51.8% (-1.0; 4.2% vs 3.2%); SCoRe 60.0% to 64.4% (+4.4; 1.4% vs…
- …and 6 more sources in `library/entries/reflection-loop.yaml`.

## Caveats

Most of the evidence is math, code and puzzles with ground truth; the form-critique gains come from Self-Refine's 2023 GPT-3.5 and GPT-4 runs against one-step generation, not against best-of-N at equal compute, and no source here measures the loop's latency. Reflexion's signals are sometimes close to an oracle (HotpotQA graded by exact match against the gold answer), and its HumanEval gain did not hold against plain retries in an independent rerun. The supporting 2026 study runs at temperature 0 against a single zero-shot answer with no sampling baseline, and the 29-model study mixes protocols across settings, its largest gain starting from an unusually low 17.44% on GSM8K. Trained self-correction (SCoRe) is the one result where same-model revision beat parallel sampling at the same number of samples, but it needs multi-turn RL on the model itself.

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:no-self-written-tests` (9.c.i, Don't prompt agents to write their own tests; suppress it for test-heavy models)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)

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
