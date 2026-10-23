---
name: false-success-detector
description: "AOT optimization 9.b.ii (Tier 2, Reliability): Triage false success with a cheap trained detector, not an LLM judge. Placeholder. Use when an agent shows: runs that end with a success claim; the closing message text and the tool-call sequence are the detector's inputs."
---

<!-- Generated from library/entries/false-success-detector.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Triage false success with a cheap trained detector, not an LLM judge

> **Placeholder.** Generated from `library/entries/false-success-detector.yaml` (entry 9.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.b.ii |
| Earlier id | T45 |
| Tier | 2 (Reliability): detects a silent failure mode; it does not change the agent |
| Categories | Verification: Confirming completion; Verification: Sizing verification |
| Change | tool / validation (add) |

## What it is

Train a lightweight text classifier (TF-IDF with logistic regression) on 50-100 labeled runs to flag likely false successes for review. LLM judges, including reasoning models and tuned judge prompts, peaked at AUROC 0.65 and were anti-correlated on false success against honest failure; the detector reached 0.83-0.95 and caught 72% at a 10% review budget.

## When it applies

- **In traces:** runs that end with a success claim; the closing message text and the tool-call sequence are the detector's inputs
- **In eval results:** an LLM judge currently used to decide whether a run completed; a labeled sample with a false-success rate above a few percent

## How (outline)

1. Label 50-100 runs as true success, false success or honest failure from the environment (9.b.iii).
2. Train the classifier on the run's closing text and tool sequence.
3. Route the top 10% by score to review; track catch rate against the labels.

## How to measure

- **monitor**: catch rate at a fixed review budget against a labeled sample

## Expected impact

- **Quality:** improves, medium: as a review triage signal: 72% of false successes caught at a 10% review budget, against 13% for the best judge (Jun 2026)
- **Cost:** improves, large: compared with an LLM judge
- **Performance:** improves, large: 3,300x lower latency than a judge call

## Evidence (summary)

- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Task-disjoint AUROC 0.849 (LR) / 0.825 (XGB) / 0.827 (DeBERTa-v3) on tau2-bench and 0.953 (XGB) on AppWorld API-call sequences, versus best LLM judge 0.640 and 0.537. At a 10% flag rate the detector recovers 72% of false successes [95% CI…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): tau2-bench airline<->retail LODO: TF-IDF+LR 0.693 zero-shot -> 0.736 (K=10 per class) -> 0.788 (K=50) -> 0.827 (K=100). TF-IDF+XGB degrades 0.657 -> 0.538 at K=100. Entity stripping does not help (LR 0.690, XGB 0.684).
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Detector and judge scores correlate at rho=0.41; a 75/25 weighted ensemble raises tau2-bench AUROC from 0.834 to 0.855. Author calls the gain modest.
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): tau2-bench, 295 trajectories, 5 judges (GPT-4o, Sonnet 4.5, Llama 3.3-70B, DeepSeek-R1, o3-mini) x 5 prompt conditions x 3 phrasings: no configuration exceeds AUROC 0.65 on false success vs true success (best 0.640). On false success vs…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): tau2-bench: Sonnet 4.5 blind 0.576, checklist 0.576, stepwise 0.590, tool_only 0.605, no_closing 0.640; adding the full task spec (strong-real) moves 0.640 -> 0.632 ("judges do not lack information, they fail to use it"). AppWorld: telling…
- …and 1 more sources in `library/entries/false-success-detector.yaml`.

## Related

- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)

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
