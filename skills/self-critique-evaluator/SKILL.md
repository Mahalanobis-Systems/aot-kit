---
name: self-critique-evaluator
description: "AOT optimization 7.c.ii (Tier 3, Tuning): Self-critique evaluator loop. Placeholder. Use when an agent shows: Judge pass rate and score distribution per training or refresh iteration next to accuracy on an audited sample; a widening gap, scores saturating near the top of the scale, and output length rising across iterations."
---

<!-- Generated from library/entries/self-critique-evaluator.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Self-critique evaluator loop

> **Placeholder.** Generated from `library/entries/self-critique-evaluator.yaml` (entry 7.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.ii |
| Earlier id | P38 (Feedback & Iteration, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it adds a self-bootstrapped judge |
| Categories | Orchestration: Scaling compute |
| Change | workflow / reflection |

## What it is

Train or tune the system's own judge from its own outputs and synthetic judgments (contrastive pairs with one side deliberately degraded, the judge's own verdicts kept only where they match the construction label) instead of human labels, then use it to score, select or train in the loop. It pays where no sound check exists and a prompted judge is too weak or too costly: synthetic-only training lifted a 70B judge from 75.4 to 88.3 on RewardBench and another 70B judge from 48.6 to 60.0 on JudgeBench, and an agent-loop verifier evolved from ten anchored examples agreed with held-out labels 0.625 of the time against 0.55 for the bare LLM judge it contains, a gap that was not significant. The limits are the point: gains concentrate on the benchmark used for selection (human agreement on MT-Bench moved only from 77.8 to 78.9), and a policy optimized against its own reference-free judge drove the judge's pass rate from 0.72 to 0.94 while true accuracy stayed at 0.20. Keep a human-labeled set the judge never trains or selects on; the agent's downstream score cannot validate the judge.

## When it applies

- **In the code:** A pipeline that trains or prompt-tunes a judge on the system's own outputs or its own verdicts, with periodic refresh. Flag a judge from the same model or family as the generator, no human-labeled set held out from both training and selection, and a judge validated only by the agent's downstream score.
- **In traces:** Judge pass rate and score distribution per training or refresh iteration next to accuracy on an audited sample; a widening gap, scores saturating near the top of the scale, and output length rising across iterations.
- **In eval results:** Chance-corrected agreement with a locked human-labeled set; the judge's accuracy on the generator's own outputs against equal-quality outputs from other sources; results on judge benchmarks other than the one used for model selection.
- **Judge:** An outer judge kept outside every loop, from another family, given the task contract and checked against humans.
- **Probes:** Outputs built to fool the judge: content-free answers, plausible-but-wrong answers and padded answers, plus the generator's outputs paired with equal-quality outputs from other sources.

## How (outline)

1. Start from the baseline: a prompted judge from another model family with written criteria (7.c.iii), or a sound external check where one exists (9.a.i). Bootstrap your own judge only where that baseline disagrees with human labels too often or costs too much per call. First label two small human sets: one for calibration and selection, and a locked one the judge never trains or selects on (one agent-loop verifier was selected on ten anchored items and validated on locked sets of 40-48).
2. Build contrastive pairs from your own traces so the label comes from construction, not from the judge's opinion: a good output against a degraded one, such as an answer to a subtly modified instruction, a sampled answer that fails a known-answer check, or an output cut to a bare opener ('Thought process:'). Include both orderings of every pair.
3. Train the judge on the pairs (fine-tune on its own verdicts that match the label and iterate, or RL on verdict correctness), or tune a judge prompt against them. Prefer a base from another family than the generator, since self-preference rises with self-recognition, but check it: judges also favor any model whose mistakes resemble theirs. Where answers are checkable, make the judge commit its own answer before it compares (false-positive rate on wrong answers 0.719 to 0.012 in one study).
4. Gate it before use: chance-corrected agreement and true- and false-positive rates on the locked set; judge benchmarks other than the one used for selection; accuracy on the generator's outputs against equal-quality outputs from other sources; false-positive rate on adversarial probes (bare openers, punctuation, padded and plausible-but-wrong answers). Never validate it by the agent's downstream score: an always-pass verifier trained skills as well as a valid one.
5. In the loop, control length when picking preferred outputs, track the judge's pass rate against audited accuracy, and keep a human-audited sample and an outer judge outside the loop (9.c.iii).
6. Refresh on a schedule from new traces: promote a retrained judge only if it agrees better with the locked set, add outputs the old judge wrongly accepted as negatives, and discard scores that depended on the replaced judge.
7. Measure with a paired eval on the locked set against the prompted judge and against best-of-N or majority vote at equal compute (9.c.ii); report the gap between the judge's pass rate and audited accuracy at every iteration.

## How to measure

- **experiment** (Tier 3): paired eval on a locked human-labeled set the judge never trains or selects on: the bootstrapped judge against the prompted judge it would replace and against majority vote or best-of-N at equal compute; chance-corrected agreement, true- and false-positive rates, accuracy on the generator's own outputs against equal-quality outputs from other sources, false-positive rate on adversarial probes; then the loop's end quality graded on the same locked set, never by the judge
- **monitor**: per training iteration and per refresh: the judge's pass rate against accuracy on a regularly audited human sample, score saturation near the top of the scale, output length, and the judge's acceptance rate on the generator's outputs against outputs from other sources; promote a retrained judge only if it agrees better with the locked set

## Expected impact

- **Quality:** mixed, medium: gains on judge benchmarks and on what is trained against them: RewardBench 75.4 to 88.3 (Wang, Aug 2024); JudgeBench 48.6 to 60.0 for a 70B judge trained on 22K synthetic pairs, but +0.6 (70.8 to 71.4) on a Qwen3-32B thinking base, still below o3's 75.7 (Whitehouse, May 2025); AlpacaEval 2 LC win rate 25.5% to 39.4% (Wu, Jul 2024); search with a co-evolved code reviewer found a coder passing 23 of 28 held-out DeepSWE tasks against 21 of 28 with a fixed evaluator, one run (Iacob, Jun 2026). Gains that do not transfer: MT-Bench human agreement 77.8 to 78.9 (Wang, Aug 2024); a self-trained 8B judge scored 83.0 against 69.5 on RewardBench but 30.2 against 32.3 on JudgeBench (Whitehouse, May 2025); self-play against its own judge took the pass rate from 0.72 to 0.94 at 0.20 true accuracy (Zhou, Jul 2026)
- **Cost:** degrades, medium: up-front generation, training and validation, repeated at every refresh: Meta-Rewarding sampled 7 responses for each of 5,000 prompts and 11 judgments of each response per iteration, for four iterations (Wu, Jul 2024); Self-Taught Evaluators retrained a 70B judge for five iterations (Wang, Aug 2024); one co-evolution search with a learned reviewer used 587M tokens to its best coder against 429M with a fixed evaluator on DeepSWE, but 1.35 to 1.72 times fewer on Polyglot (Iacob, Jun 2026)
- **Performance:** none (unmeasured)
- **Security:** mixed, medium: a learned judge is a gate that can be gamed: content-free answers such as 'Thought process:' or ':' drew false-positive rates as high as 80%, one trained verifier 66.8% on a single blank space, and adding 20k truncated outputs as negatives brought trained judges near 0% (Zhao, Jul 2025); errors a policy learned against its own judge fooled judges of other families, and a three-family ensemble still accepted 55% of wrong answers on one seed, 65% over three seeds (Zhou, Jul 2026)
- **Governance:** degrades, medium: self-referential evaluation: the system's own score cannot show whether it improved. A collapsed always-pass verifier trained skills as well as a valid one, and rubric gaming that no in-loop signal saw was caught by an outer judge (Zhang, Oct 2026); without a held-out check a self-play judge reported 94% correct when 20% were (Zhou, Jul 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Wang et al., "Self-Taught Evaluators", https://arxiv.org/abs/2408.02666 (2024-08-05): "can improve a strong LLM (Llama3-70B-Instruct) from 75.4 to 88.3 (88.7 with majority vote) on RewardBench"; the same judge setup trained on human-labeled HelpSteer2 data reached 85.6. Agreement with human judgments on MT-Bench: 77.8 for…
- Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho, Xian Li, Sainbayar Sukhbaatar, Jing Xu, Jason Weston, "Self-Rewarding Language Models"… (2024-01-18): AlpacaEval 2.0 win rate over GPT-4 Turbo "from 9.94% in Iteration 1, to 15.38% in Iteration 2, to 20.44% in Iteration 3". Judge pairwise accuracy against held-out human rankings: 65.1% with instruction data only, 78.7% after adding the…
- Tianhao Wu, Weizhe Yuan, Olga Golovneva, Jing Xu, Yuandong Tian, Jiantao Jiao, Jason Weston, Sainbayar Sukhbaatar, "Meta-Rewarding Language… (2024-07-28): AlpacaEval 2 length-controlled win rate 25.47% (after fine-tuning on the human-derived evaluation data; 22.9% before it) to 39.4% and Arena-Hard 20.6% to 29.1% over four iterations; Self-Rewarding with the same length control reached…
- Chenxi Whitehouse, Tianlu Wang, Ping Yu, Xian Li, Jason Weston, Ilia Kulikov, Swarnadeep Saha, "J1: Incentivizing Thinking in… (2025-05-15): Position-consistent JudgeBench accuracy: Llama-3.3-70B-Instruct 48.6, J1-Llama-70B 60.0; Llama-3.1-8B-Instruct 32.3, J1-Llama-8B 42.0; Qwen3-32B 70.8, J1-Qwen-32B-MultiTask 71.4 (+0.6); o3 75.7. RewardBench for the same pairs 85.4 to 93.3…
- …and 6 more sources in `library/entries/self-critique-evaluator.yaml`.

## Caveats

Most evidence comes from instruction-following benchmarks graded by GPT-4 (AlpacaEval, Arena-Hard) or from judge benchmarks also used for model selection, and the agent-loop studies are small: 28 held-out DeepSWE tasks with one run per arm, locked sets of 40-48 items over three seeds, one model family. Gains shrink on strong reasoning bases (+0.6 on JudgeBench for a Qwen3-32B thinking model, which o3 still beat), and the largest self-play hacking appeared in a regime built to hold accuracy low; under natural chain-of-thought the gap between judge pass rate and true accuracy fell to 0.086-0.125. A judge from another family cuts self-preference but not shared blind spots: judges favor any model whose mistakes resemble theirs, and errors a policy learned against one judge fooled judges of other families. Several methods sold as label-free still used human data (Self-Rewarding's seed evaluation examples, a ten-item anchor, accepted and rejected pull requests), so treat a small human set as part of the method.

## Related

- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))

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
