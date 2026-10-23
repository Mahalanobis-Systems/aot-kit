---
name: audit-verifier-cascade
description: "AOT optimization 9.c.iii (Tier 4, Restructuring): Audit a verifier-gated cascade against a gold sample the verifier never sees. Placeholder. Use when an agent shows: escalation rate against the eval's true error rate."
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

When a cheap model's outputs are accepted or escalated by a verifier, measure true error on a small gold-labeled sample outside the verifier: metrics measured through the verifier showed about 3% error while true error was 14-32%. A frontier verifier cuts misses but escalates more than the true error rate, erasing the saving. Never train the cheap model on verifier rejects or accepted outputs.

## When it applies

- **In the code:** a cheap model whose outputs are accepted or escalated by a verifier model, with error measured only through the verifier
- **In traces:** escalation rate against the eval's true error rate
- **In eval results:** no gold-labeled sample scored independently of the verifier

## How (outline)

1. Label a rolling sample (e.g. 100 cases a week) by hand or by the environment.
2. Score the cascade's delivered answers on it, separately from the verifier's own accept rate.
3. Alert when true error diverges from verifier-measured error.

## How to measure

- **monitor**: true error on a rolling gold-labeled sample
- **production-test** (Tier 4): A/B of the cascade against the single strong model

## Expected impact

- **Quality:** improves, medium: reveals hidden error: ~3% through the verifier against 14-32% true (Sep 2026)
- **Cost:** degrades, small: labeling the audit sample
- **Performance:** none

## Evidence (summary)

- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Qwen2.5-7B student, gpt-4o-mini verifier, GSM8K corrective loop: verifier-estimated error of the delivered stream flat near 3% across rounds while gold user-facing error swung 14% to 32% (5-11x gap, 95% intervals separate from round 1…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): GSM8K, fixed gpt-4o-mini verifier: blind-spot rate beta rises from 0.12 (CI 0.08-0.17) at Qwen2.5-0.5B to 0.55 (CI 0.44-0.66) at 14B; 7B-32B plateau around 0.35-0.65. Hard MATH, fixed 7B student: beta 0.42 (CI 0.32-0.53) with gpt-4o-mini…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Hard MATH L4-5, Qwen2.5-7B student: gpt-4.1 verifier beta ~0.05 but escalation rate 0.46 (CI 0.39-0.53, n=200) against a 0.39 true error rate, i.e. frontier price on nearly half of traffic. "Low blind spot and low cost are not…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Qwen2.5-1.5B and 7B students, GSM8K corrective loop, teachers gpt-4o-mini, gpt-4o (cross-family) and Qwen2.5-32B (same-family): naive LoRA fine-tuning on rejects degraded the student in every case and cumulatively collapsed it (raw error…
- Rajput et al., "Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades"… (2026-09-01): Synthetic model only (rho=0.7, 20 seeds, 8 rounds): self-training user-facing error 0.296 vs corrective 0.249 (raw error 0.356 vs 0.304); frozen 0.334; oracle-in-loop 0.000. Predicted rise above q0*beta0 was not observed.
- …and 8 more sources in `library/entries/audit-verifier-cascade.yaml`.

## Related

- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
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
