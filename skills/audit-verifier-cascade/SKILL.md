---
name: audit-verifier-cascade
description: "AOT optimization 9.c.iii (Tier 4, Restructuring): Audit a verifier-gated cascade against a gold sample the verifier never sees. Placeholder. Use when an agent shows: escalation rate against the eval's true error rate; verifier accept rate shifting after a verifier model or prompt change while the generator is unchanged."
---

<!-- Generated from library/entries/audit-verifier-cascade.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Audit a verifier-gated cascade against a gold sample the verifier never sees

> **Placeholder.** Generated from `library/entries/audit-verifier-cascade.yaml` (entry 9.c.iii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.c.iii |
| Earlier id | T48 |
| Tier | 4 (Restructuring): it governs an escalation topology, which only a production test can judge |
| Categories | Verification: Sizing verification; Topologies: Escalating |
| Change | workflow / other (add) |

## What it is

Check a verifier-gated cascade against a small human-labeled sample the verifier never sees: the verifier's own numbers can hide most of the error. In one study the error measured through the verifier stayed near 3% while true error swung 14-32%, and in a production text-to-SQL pipeline a judge nobody had checked agreed with human labels at kappa 0.04 on the cases it flagged (0.42 on a random sample). A frontier verifier cuts misses but escalates more than the true error rate, erasing the saving; never train the cheap model on verifier rejects or accepted outputs. The verifier's labels cannot replace the gold sample (when it is no more accurate than the model it checks, they can at most halve the gold labels needed), and the verifier itself drifts with silent version and prompt changes, so keep a frozen human-labeled anchor set as well.

## When it applies

- **In the code:** a cheap model whose outputs are accepted or escalated by a verifier model, with error measured only through the verifier; a verifier called by a floating model alias, or its prompt changed with no re-audit
- **In traces:** escalation rate against the eval's true error rate; verifier accept rate shifting after a verifier model or prompt change while the generator is unchanged
- **In eval results:** no gold-labeled sample drawn at random from live traffic and scored independently of the verifier, or a gold set drawn only from cases the verifier flagged

## How (outline)

1. Start from the baseline: record the cascade's error as measured through the verifier (accept and escalation rates, error on accepted items as the verifier sees it) and its cost per item, and run the single strong model on the same traffic as the comparison arm.
2. Label a rolling sample (e.g. 100 cases a week) of delivered answers by hand or by the environment, drawn at random from live traffic and stratified by the verifier's verdict (accepted, escalated) or its confidence, with each stratum's share set in proportion to its size: in one study 200 labels gave an RMSE of 2.46 points with proportional allocation against 4.56 with equal labels per stratum. Never build the gold set only from cases the verifier flagged: a production judge's agreement with humans was kappa 0.04 on such a set and 0.42 on a uniform-random one. Have two people label at least part of it and adjudicate, since gold is noisy too (pre-consensus kappa 0.87 on 200 cases in that audit, and 21.7-25.5% of one public benchmark's expert-written gold SQL were flagged as candidate errors).
3. Score the cascade's delivered answers on that sample separately from the verifier's own accept rate: true error per stratum and overall (weighted by stratum size) with a 95% interval, plus the verifier's miss rate (wrong answers it accepted) and false-reject rate. In one study the verifier-measured error stayed near 3% while gold error on 300 items swung 14-32%; in the production audit even the repaired judge's raw faithful rate (84.3%) moved to about 90.6% once reweighted with a 200-case random sample.
4. Use the verifier's labels only through a bias-corrected estimator (prediction-powered inference, or a correction by the miss and false-reject rates measured on the gold sample), and do not count on them to shrink the gold sample: when the verifier is no more accurate than the model it checks, no unbiased method can cut the gold labels needed by more than half, and in one study a sensitivity and false-positive correction needed fewer human labels than a plain random audit for only 6 of 56 model-verifier pairs on MMLU-Pro and none on MMMU-Pro.
5. Keep the gold sample out of everything it audits: no verifier prompt or threshold tuning, judge fine-tuning or student training on it, and never train the cheap model on verifier rejects or accepted outputs (naive fine-tuning on rejects collapsed the student in every tested setting).
6. Refresh and alert. Re-draw the sample after every student, verifier, prompt or schema change, since the verifier's blind spot grows as the student gets stronger, and pin the verifier to a dated model snapshot. Keep a frozen human-labeled anchor set that the current verifier re-scores on a schedule, to tell verifier drift from cascade drift: a silent judge version bump was detected in 60 of 60 runs with 200 anchors re-scored every 5th item, but in 4 of 60 with 50 anchors every 20th. Alert when true error diverges from verifier-measured error using a sequential (anytime-valid) test, not a rolling z-test re-run on every new label, which false-alarmed on 75% of drift-free streams; monitor per stratum, because one pooled monitor never detected a drift confined to one stratum.
7. Measure with an A/B of the cascade against the single strong model, both scored on the same gold sample: true error with its interval, cost per item, and escalation rate against the true error rate (a frontier verifier escalated 46% of hard MATH queries against a 39% true error rate in one study).

## How to measure

- **monitor**: true error of delivered answers on a rolling gold sample drawn at random from live traffic and stratified by verifier verdict, with its 95% interval, next to the verifier-measured error; the verifier's miss and false-reject rates on that sample; a frozen human-labeled anchor set re-scored by the verifier on a schedule, alerting with a sequential test, per stratum
- **production-test** (Tier 4): A/B of the cascade against the single strong model, both scored on the same gold sample: true error, cost per item, and escalation rate against true error rate; repeat after each student, verifier or prompt change

## Expected impact

- **Quality:** improves, medium: reveals hidden error: ~3% through the verifier against 14-32% gold (Rajput, Sep 2026); a production judge never checked against humans agreed at kappa 0.04 on flagged cases and 0.42 on a random sample, and the audit replaced it with one at 0.72 and 0.94 (Liu, Sep 2026)
- **Cost:** degrades, small: labeling the audit sample: 200 gold labels gave an RMSE of 2.46 points with proportional allocation, and verifier labels saved human labels for only 6 of 56 model-verifier pairs (Choi, Oct 2026); at most a factor-two saving when the verifier is no more accurate than the model it checks (Dorner, Oct 2024); a drift monitor with 200 human anchors ran at about 0.64 of the cost of strong-judging every item (Li, Jun 2026)
- **Performance:** none (unmeasured): the audit labels a sample off the serving path; no source measures serving latency
- **Governance:** improves, medium: an independent record of true error that can say whether the cascade or the verifier changed: a frozen human anchor set attributed a silent judge version bump in 60 of 60 runs and a stricter judge prompt in 110 of 120 (Li, Jun 2026); re-audit against fresh gold on each schema or model-snapshot change (Liu, Sep 2026)

## Evidence (summary)

- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Qwen2.5-7B student, gpt-4o-mini verifier, GSM8K corrective loop: verifier-estimated error of the delivered stream flat near 3% across rounds while gold user-facing error swung 14% to 32% (5-11x gap, 95% intervals separate from round 1…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): GSM8K, fixed gpt-4o-mini verifier: blind-spot rate beta rises from 0.12 (CI 0.08-0.17) at Qwen2.5-0.5B to 0.55 (CI 0.44-0.66) at 14B; 7B-32B plateau around 0.35-0.65. Hard MATH, fixed 7B student: beta 0.42 (CI 0.32-0.53) with gpt-4o-mini…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Hard MATH L4-5, Qwen2.5-7B student: gpt-4.1 verifier beta ~0.05 but escalation rate 0.46 (CI 0.39-0.53, n=200) against a 0.39 true error rate, i.e. frontier price on nearly half of traffic. "Low blind spot and low cost are not…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Qwen2.5-1.5B and 7B students, GSM8K corrective loop, teachers gpt-4o-mini, gpt-4o (cross-family) and Qwen2.5-32B (same-family): naive LoRA fine-tuning on rejects degraded the student in every case and cumulatively collapsed it (raw error…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Synthetic model only (rho=0.7, 20 seeds, 8 rounds): self-training user-facing error 0.296 vs corrective 0.249 (raw error 0.356 vs 0.304); frozen 0.334; oracle-in-loop 0.000. Predicted rise above q0*beta0 was not observed.
- …and 12 more sources in `library/entries/audit-verifier-cascade.yaml`.

## Caveats

The audit practice still rests mainly on one study on GSM8K and MATH (Rajput et al.) and one production text-to-SQL audit whose gold came from two of its authors (234 enriched and 200 random cases); neither compares a cascade run with an audit against one without. The label-count results come from multiple-choice benchmarks with exact answer keys (simulated audits on MMLU-Pro and MMMU-Pro; MMLU and MT-Bench for the factor-two bound) and assume clean, IID gold, while real gold is noisy (annotator kappa 0.87; 21.7-25.5% candidate errors in one expert-written benchmark) and rare failures need far larger samples. The 6-of-56 result is an idealized comparison for one correction method; prediction-powered estimators with a tuned weight are never worse than the gold labels alone, so verifier labels can still tighten an interval, just not by much. The drift-monitor results come from one author, two datasets and one model family as judge, with a strong LLM judge rather than humans scoring the main stream.

## Related

- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:verify-citations` (9.a.ii, Verify citations claim by claim for factual support)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)

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
