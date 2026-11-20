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

Have the same model critique and revise its own output for a few rounds (Self-Refine), or write a short lesson after a failed attempt and carry it into the next try (Reflexion). It pays when the critique has something to stand on, such as a failing test, an error, an environment reward or a checkable constraint (Reflexion on hard Rust problems went from 0.60 to 0.68 with its tests and fell to 0.52 without them, and revision broke at most 2.1% of right answers on checkable SAT constraints against up to 13.25% on long open reasoning, where one study still found significant gains on BBEH Non-Choice for all five models), or when it judges form rather than correctness. Asked only to re-check whether an answer is right, models break right answers as well as fix wrong ones: one revision pass lowered accuracy in 20 of 28 BoolQ settings, every RefineBench model (GPT-5 and o1 included) moved by -2.5 to +2.6 points over five turns (o1 18.5 to 18.3), a fresh-context self-review by four frontier models caught slips on questions they could solve but barely improved error detection on hard ones, where 47% to 77% of their errors were, and models rated their own failing code as more correct when judging it in the conversation that produced it. Lessons carried across retries depend on the model: plain retries beat Reflexion on HumanEval at lower cost, and against fresh retries at six trials Reflexion added 16 points on WebShop for GPT-5.4 nano and nothing reliable for GLM-4.7-FlashX (-4, within noise), at 2.1 to 3.6 times the tokens.

## When it applies

- **In the code:** A step where the same model critiques its own output and a step that revises it (a reflect, critique or "double-check your answer" call), or verbal reflections stored between attempts, with a round cap. Flag a loop that re-checks correctness with no test, error, environment signal or explicit checklist in the critique, no cap, one that always returns the last revision, an outer reflect step on a reasoning model with thinking on, a critique or approval asked as a follow-up turn in the conversation that produced the output instead of in a new context, and agent retries that replay stored reflections with no fresh-retry baseline.
- **In traces:** Rounds per item; share of rounds whose critique changes the answer; on items with ground truth, right-to-wrong and wrong-to-right flips per round; whether the critique cites a test, error or requirement or only restates the answer; tokens per round.
- **In eval results:** Accuracy per round against the single pass and against retries or best-of-N at equal tokens; share of initially right answers the loop breaks; for agents, success within the same number of trials against fresh retries; the critique's error detection on the model's own outputs, split into easy and hard items (on fixed examples it looked better: AUROC 0.99 against 0.89 to 0.92 on its own patches).
- **Judge:** Rate critiques for specificity.
- **Probes:** Correct outputs mixed with outputs carrying one detectable defect.

## How (outline)

1. Start from the baselines on your own items: the single pass with the model's own thinking on or a higher effort (1.b.i), and retries or best-of-N at the same tokens (9.c.ii); for agents, fresh retries with no memory at the same number of trials. Plain retries against HumanEval's example tests scored 92.0% for $2.51 where Reflexion scored 87.8% for $3.90.
2. Add the loop only where the critique has a signal to work from (a failing test, a compiler or runtime error, an environment reward, a constraint the model can check such as a formula, required fields or a length limit) or where it judges form (tone, format, coverage of required items) rather than correctness. If the check is sound, feed its verdict back instead (9.a.i); if the critic needs written criteria and its own context, use 7.c.iii. Do not add an outer "check your answer" step on a reasoning model with thinking on. A self-review mostly catches slips and answers that contradict their own written work: 13 of the 14 MATH-500 errors GPT-5.6 Sol flagged on review had a solution that disagreed with its answer, while on hard questions (those a reference model missed, 47% to 77% of each model's errors) review changed error-detection AUROC by -0.027 to +0.038.
3. Run the critique in a new context with the output pasted into a user turn, not as a follow-up in the conversation that produced it: rating their own SWE-bench patches in the same turn or a follow-up turn, models separated failing from passing patches at AUROC 0.89 to 0.92 against 0.99 in a new context, and a larger reasoning budget did not reduce the bias in one model's code-risk ratings. Put the signal or the checklist into the critique prompt: the error, the failing test, the list of requirements (given the full checklist, Gemini 2.5 Pro scored 44.5 points above open self-refinement, which gained 1.8 over five turns). On a non-reasoning model, try appending "Wait" after its own output before the critique: 14 such models fixed injected errors in their own output 64.5% less often than the same errors in the user's message, and appending "Wait" cut that gap by 89.3%. Use a neutral instruction that keeps the answer unless something contradicts it; on BoolQ every refinement prompt lowered mean accuracy, and more forceful ones added more harmful flips than helpful ones.
4. Cap rounds at one to three and stop when the check passes or the critique finds nothing to fix; Self-Refine capped at four, with most of the gain in the first iterations.
5. Keep the first answer unless the revision is better by the metric: accept it only when the check passes or the score rises, otherwise return the original. A trained gate took Qwen2.5-7B on BoolQ to 86.02% where always revising gave 72.32%, though the author flags the gate's gains as unverified. Do not gate on the model's own confidence for hard items: on questions a reference model missed, four frontier models' confidence ranked right answers above wrong ones at AUROC 0.49 to 0.63.
6. When attempts repeat (agent episodes, test-driven retries), store each failure's short verbal reflection and give the last few to the next attempt (Reflexion kept 1 to 3), and keep it only if it beats fresh retries at the same number of trials on your model. In 2023 it took GPT-3 to 130 of 134 ALFWorld tasks while the retry-only agent stopped improving after six trials; on current models with thinking off it added 16 points on WebShop for GPT-5.4 nano (39 to 55) and 6 for DeepSeek-V4-Flash (45 to 51) but moved GLM-4.7-FlashX by -4 (50 to 46, within noise), at 2.1 to 3.6 times the tokens; in a separate GPT-4o-mini sweep, showing the stored reflections on only three of four retries did better than always showing them on ALFWorld (81.3% against 76.1%, not significant) and worse on HotPotQA (45% against 49%). If attempts run in parallel, give each new attempt summaries of several earlier attempts rather than only its own: on 100 SWE-bench Verified tasks a rollout's own summary added about 1 point (Claude-4.5-Sonnet 69.87 to 70.87, Gemini-3.1-Pro 72.69 to 73.75), four random summaries 4.25 to 5.19 and four picked by a tournament 6.56 to 8.19 (see 9.c.ii).
7. Measure on held-out items with ground truth the loop never sees: accuracy per round against both baselines at matched tokens, the share of right answers turned wrong and of wrong ones fixed per round (one untrained model turned 15.8% of MATH problems from right to wrong), the critique's error detection on the model's own outputs split into easy and hard items, and tokens, calls and latency per item; for agents, success within the same number of trials against fresh retries; re-run on every model upgrade.

## How to measure

- **experiment** (Tier 3): paired eval on held-out items with ground truth the loop never sees: the loop against the single pass with thinking on and against retries or best-of-N at matched tokens, per model, and for agents against fresh retries at the same number of trials; accuracy per round, share of right answers turned wrong and of wrong answers fixed per round, the critique's error detection on the model's own outputs split into easy and hard items, tokens, calls and latency
- **monitor**: rounds per item, share of rounds that change the answer, gate acceptance rate, check-pass rate after each round, cap-hit rate; for agents, trials to first success and calls per task; on a regularly audited sample, right-to-wrong flips

## Expected impact

- **Quality:** mixed, medium: gains where a signal or checkable constraint exists: hard Rust problems 0.60 to 0.68 with self-written tests, 0.52 without (Shinn, Mar 2023); SAT 34.62% to 64.96% on Mistral Large with at most 2.1% of right answers broken (Stav, Jun 2026); constrained generation 15.0 to 45.0 on GPT-4 (Madaan, Mar 2023). Mixed on re-checks of correctness: significant gains on BBEH Non-Choice for all five models and on HLE for two, with up to 13.25% of right answers turned wrong (Stav, Jun 2026); MATH 52.8% to 51.8% with Self-Refine (Kumar, Sep 2024); lower accuracy in 20 of 28 BoolQ settings (Zhang, Sep 2026); -2.5 to +2.6 points over five turns for every RefineBench model (Lee, Nov 2025); over 90% of in-thinking reflections confirmatory in reasoning models (Kang, Oct 2025); fresh-context self-review changed error-detection AUROC on hard questions by -0.027 to +0.038 for four frontier models (Han, Sep 2026); own patches rated in the producing conversation at AUROC 0.89 to 0.92 against 0.99 in a new context (Khullar, Mar 2026). Lessons across retries: Reflexion 87.8% against plain retry 92.0% on HumanEval (Kapoor, Jul 2024); against fresh retries at six trials +16 (GPT-5.4 nano), +6 (DeepSeek-V4-Flash) and -4 (GLM-4.7-FlashX, within noise) points on WebShop (Bai, Sep 2026); a summary of the agent's own previous attempt +1.00 and +1.06 pass@1 on SWE-bench Verified against +4.25 to +8.19 from summaries of four parallel attempts (Kim, Apr 2026)
- **Cost:** degrades, medium: at least one critique and one revision call per round: Reflexion cost $3.90 on HumanEval against $1.93 for one GPT-4 call and $2.51 for plain retry (Kapoor, Jul 2024); over six WebShop trials Reflexion used 78,506 to 120,545 tokens per task against 21,703 to 46,880 for fresh retries, 2.1 to 3.6 times (Bai, Sep 2026); inside reasoning models, reflections after the first answer took 16.8% to 47.8% of tokens for 1.4 to 3.5 points (Kang, Oct 2025)
- **Performance:** degrades, medium: each round is a serial critique and revision call: over six WebShop trials Reflexion made 26.0 to 33.0 model calls per task against 15.3 to 21.7 for fresh retries (Bai, Sep 2026); summaries of four selected earlier attempts shortened later ones from 41.23 to 14.31 agent steps for Claude-4.5-Opus on SWE-bench Verified (Kim, Apr 2026); no source here measures wall-clock time
- **Security:** degrades, small: when a self-review is used as an approval or safety gate: rating patches in the same or a follow-up turn, models approved patches that followed a prompt injection 5 times more often in one setting than when the same patches came in a new context, and rated risky computer-use actions they had just taken as safer (Khullar, Mar 2026)
- **Governance:** none (unmeasured)
- **Brand:** improves, small (unmeasured): Polished output where the critique is about form (tone, format, required items).

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback", https://arxiv.org/abs/2303.17651 (2023-03-30): "improving by ~20% absolute on average in task performance" over one-step generation. Per task, GPT-4 base to Self-Refine: dialogue response preference 25.4 to 74.6, constrained generation 15.0 to 45.0, code optimization 27.3 to 36.0, math…
- Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao, "Reflexion: Language Agents with Verbal… (2023-03-20): ALFWorld: ReAct + Reflexion completed "130 out of 134 tasks"; the ReAct-only agent, which also reset and retried, stopped improving: "performance increase halts between trials 6 and 7". HotpotQA (CoT with the gold context, exact-match…
- Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan, "AI Agents That Matter"… (2024-07-01): Mean of 5 runs, accuracy and total cost: Reflexion (GPT-4) 87.8% and $3.90 (91.0 in its own paper); retry 92.0% and $2.51; warming 93.2% and $2.45; one GPT-4 call 89.6% and $1.93. "Reflexion and LDB cost over 50% more than the warming…
- Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi Singh, et al. (Google DeepMind), "Training Language Models to… (2024-09-19): MATH, Gemini 1.5 Flash, first to second attempt: base model 52.6% to 41.4% (-11.2; 15.8% of problems went from correct to incorrect, 4.6% the other way); Self-Refine 52.8% to 51.8% (-1.0; 4.2% vs 3.2%); SCoRe 60.0% to 64.4% (+4.4; 1.4% vs…
- …and 10 more sources in `library/entries/reflection-loop.yaml`.

## Caveats

Most of the evidence is math, code and puzzles with ground truth; the form-critique gains come from Self-Refine's 2023 GPT-3.5 and GPT-4 runs against one-step generation, not against best-of-N at equal compute, and no source here measures the loop's wall-clock latency (only calls, steps and tokens). Reflexion's signals are sometimes close to an oracle (HotpotQA graded by exact match against the gold answer), its HumanEval gain did not hold against plain retries in an independent rerun, and the one current-model test against fresh retries (three low-cost models with thinking off, 100 WebShop goals, six trials) found gains on two models and a loss on the third, while the agent-summary result is a 100-task ablation without intervals inside a paper proposing a parallel-plus-sequential method. The supporting 2026 study runs at temperature 0 against a single zero-shot answer with no sampling baseline, and the 29-model study mixes protocols across settings, its largest gain starting from an unusually low 17.44% on GSM8K. The two 2026 self-review studies measure error detection, not the accuracy of a revise loop (one at low reasoning effort, one with simple single-turn prompts), and trained self-correction (SCoRe) is the one result where same-model revision beat parallel sampling at the same number of samples, but it needs multi-turn RL on the model itself.

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:no-self-written-tests` (9.c.i, Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
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
