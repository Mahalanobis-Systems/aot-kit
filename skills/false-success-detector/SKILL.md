---
name: false-success-detector
description: "AOT optimization 9.b.ii (Tier 2, Reliability): Triage false success with a cheap trained detector, not an LLM judge. Placeholder. Use when an agent shows: runs that end with a success claim; the closing message, the tool-call sequence and whether any state-changing call succeeded are the detector's inputs; read-only call sequences that end in a completion claim."
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

To catch agent runs that claim success but failed, rank finished runs with a small model trained on your own labeled runs and send the top of the ranking to human review, instead of asking an LLM judge that reads the agent's own claim. In one study on tau2-bench customer-service runs, no LLM judge exceeded AUROC 0.65 and judges took confident closing messages as proof, while TF-IDF classifiers trained on a corpus with 616 labeled false successes reached 0.83 to 0.85 on unseen tasks and caught 72% of false successes when flagging 10% of runs (half the flags were false alarms); in a second study, a 4B judge fine-tuned on about 2,600 labeled tau2-bench runs told failed from successful runs better than two 2026 frontier judges (AUROC 0.899 against 0.794 and 0.847), at about 1% of the strongest one's inference cost. It pays where the trajectory itself shows the failure and labels exist: each new domain needs 50 to 100 more labeled examples per class, precision falls as false successes get rarer, and on web and computer-use runs a frontier judge (AUROC 0.929) and an engineered verifier that checks every screenshot (1 to 8% of failed runs accepted) did as well or better.

## When it applies

- **In the code:** completion decided by the agent's own status field, or by an LLM judge whose prompt includes the agent's final message or self-report
- **In traces:** runs that end with a success claim; the closing message, the tool-call sequence and whether any state-changing call succeeded are the detector's inputs; read-only call sequences that end in a completion claim
- **In eval results:** on a labeled sample split by task, false successes above a few percent of runs that claim success; a completion judge whose AUROC is close to that of step count or transcript length, or whose verdicts change when the agent's report is removed

## How (outline)

1. Start from the baseline: how runs are marked complete today (the agent's own status, an LLM judge, or nothing) and a labeled sample of finished runs. Label each run from the environment's end state, never from the agent's words (9.b.iii), as true success, false success (the agent claims success, the state shows failure) or honest failure (the agent says it failed or hands off), and triage only the runs that claim success. Report the false-success share (in one study 45 to 48% of failures in single-control tau2-bench domains, 3% in a domain where the simulated user could check state, and 75.8% among AppWorld agents that write an explicit status), and score the current judge and a content-blind baseline on the same runs: step count alone separated failed from successful tau-bench runs at AUROC 0.716 in one study.
2. Check that the trajectory records the evidence a reviewer would use (tool results, state-changing calls and what they returned). Where the outcome is decided by something the trajectory never shows, such as hidden tests, judges trained on the runs reached only AUROC 0.53 to 0.65 on code repair in one study, and nothing could be decided automatically.
3. Train the detector on the labeled runs, split by task so no task is in both training and test: unigram and bigram TF-IDF features (up to 30,000) of the closing message and trajectory text, or of the sequence of API calls (method plus endpoint), with class-balanced logistic regression. In one study this reached AUROC 0.849 on unseen tau2-bench tasks from a corpus of 616 labeled false successes and 8,146 successes, and a fine-tuned 184M-parameter DeBERTa did no better (0.827). With a few thousand labels, a small fine-tuned judge is the stronger option: a 4B model prompted to treat the agent's claims as no evidence and scored by its probability of answering SUCCESS rather than FAIL reached AUROC 0.899 after fine-tuning on about 2,600 labeled tau2-bench runs (0.903 after a further RL stage). For an open-weight agent with no failure labels yet, a reference fitted on a few tens of verified successful runs can rank runs by their distance from it (AUROC 0.787 from the agent's own activations in one tau-bench study, against 0.551 for text embeddings).
4. Recalibrate for each new domain and agent version. Zero-shot transfer between tau2-bench airline and retail fell to AUROC 0.69; adding 50 to 100 labeled false successes and honest failures per class from the new domain raised logistic regression from 0.693 to 0.788 to 0.827, while XGBoost fell from 0.657 to 0.538; runs from an earlier benchmark generation transferred at 0.68 to 0.73. Refit a label-free reference when the agent changes: in one study a stale reference fell from 0.818 to 0.793 after the agent's sampling changed, and refitting restored 0.814.
5. If an LLM judge stays in the loop (as a second opinion or in an ensemble), keep the agent's own success claims out of its input and have it check the trace: in one GUI-agent study, withholding the agent's report raised a judge's recall of false successes by 13.3 and 43.4 points for two models, and in the tau2-bench study the best judge condition was the one with the closing message removed (0.640). A 75/25 blend of detector and judge scores raised AUROC from 0.834 to 0.855 there.
6. Flag the top r% of runs by score for human review, with r set by review capacity, and never fail a flagged run automatically. Precision depends on how rare false successes are: 50% at a 10% flag rate (72% caught) on test data where about 7% of runs were false successes (616 of 8,762), and, in another study, an implied 0.25 when 5% of runs fail and 0.06 when 1% do. To let part of the queue be decided without review, certify the threshold with a task-level bootstrap (resample tasks, not runs): a certificate that treated runs as independent claimed 98% automation while its realized error exceeded the budget in 17.5% of task resamples, and under the task-level certificate the fine-tuned 4B judge could auto-reject 29.7% of tau2-bench runs with at most 10% error.
7. Measure on a fresh labeled sample split by task, against the current judge and the step-count baseline on the same runs: AUROC, recall and precision at the chosen flag rate, and the false-success share, since recall at a fixed flag rate depends on it (in the tau2-bench study the detector's 72% and the judge's 13% came from sets where about 7% and nearly half of the runs were false successes). Relabel a random sample each period to catch drift.

## How to measure

- **experiment** (Tier 2): on a labeled sample of finished runs split by task (labels from environment state), score the detector, the current judge with and without the agent's report, and a step-count baseline on the same runs: AUROC, recall and precision at the chosen flag rate, and the false-success share among runs that claim success
- **monitor**: in production: flag rate, reviewer-confirmed precision of flagged runs, and recall on a random sample labeled from environment state each period; refit the detector when recall drops after an agent, model or domain change

## Expected impact

- **Quality:** improves, medium: as a review triage signal on customer-service and tool-use runs: AUROC 0.834 against 0.640 for the best transcript-reading judge on the same tau2-bench set, and 72% of false successes caught at a 10% flag rate with 50% precision (Advani, Jun 2026); a fine-tuned 4B judge told failed from successful tau2-bench runs at AUROC 0.899 to 0.903 against 0.794 and 0.847 for two frontier judges (Gan, Sep 2026); on web and GUI runs LLM verifiers did as well or better: a frontier judge at 0.929 against 0.922 (Gan, Sep 2026), 1 to 8% of failed runs accepted by a verifier that checks every screenshot (Rosset, Apr 2026), and F1 0.75 to 0.81 for an auditor kept blind to the agent's report (Zhu, Oct 2026)
- **Cost:** improves, large: a TF-IDF detector needs one CPU inference per run and no GPU, against an API call per judge decision (Advani, Jun 2026); a fine-tuned 4B judge needs one forward pass, about 1% of the inference cost of the strongest frontier judge (about 1,000 reasoning tokens per run), and its certified auto-decisions saved about 30 reviewer-hours per 1,000 tau2-bench runs at 6 minutes per review (Gan, Sep 2026); LLM verifiers that worked on GUI runs took 6 calls on a median 22K-token trace (Zhu, Oct 2026) to about 65 calls per run (Rosset, Apr 2026); offset by labels: hundreds per domain (616 false successes on tau2-bench), about 2,600 runs to fine-tune the 4B judge, and 50 to 100 per class for each new domain
- **Performance:** improves, large: 1.19 ms per run on CPU against about 4,000 ms per judge call, about 3,300 times faster (Advani, Jun 2026); label-free scoring 0.35 to 1.14 ms per run on one CPU core (Naagarajan, Oct 2026); a batched 4B judge about 10 runs per second on one GPU (Gan, Sep 2026); it runs on finished runs, so it adds no latency to the agent

## Evidence (summary)

- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Task-disjoint AUROC for false success against true success on tau2-bench: 0.849 (LR) / 0.825 (XGB) / 0.827 (DeBERTa-v3), against 0.640 for the best LLM judge; on the judges' own tau2-bench set the detector scored 0.834 (Figure 7). On…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): tau2-bench airline<->retail LODO: TF-IDF+LR 0.693 zero-shot -> 0.736 (K=10 per class) -> 0.788 (K=50) -> 0.827 (K=100). TF-IDF+XGB degrades 0.657 -> 0.538 at K=100. Entity stripping does not help (LR 0.690, XGB 0.684).
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Detector and judge scores correlate at rho=0.41; a 75/25 weighted ensemble raises tau2-bench AUROC from 0.834 to 0.855. Author calls the gain modest.
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): tau2-bench, 295 trajectories, 5 judges (GPT-4o, Sonnet 4.5, Llama 3.3-70B, DeepSeek-R1, o3-mini) x 5 prompt conditions x 3 phrasings: no configuration exceeds AUROC 0.65 on false success vs true success (best 0.640). On false success vs…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): tau2-bench: Sonnet 4.5 blind 0.576, checklist 0.576, stepwise 0.590, tool_only 0.605, no_closing 0.640; adding the full task spec (strong-real) moves 0.640 -> 0.632 ("judges do not lack information, they fail to use it"). AppWorld: telling…
- …and 5 more sources in `library/entries/false-success-detector.yaml`.

## Caveats

The detector's evidence for the triage task itself comes from one single-author workshop study on tau2-bench, whose false-success labels are regular expressions on the closing message the detector also reads (91.5% agreement with a human on 200 runs); its AppWorld result separates false successes from honest failures rather than from true successes, and its headline 72% against 13% compares recall on sets where about 7% and nearly half of the runs were false successes (AUROC on the same set, 0.834 against 0.640, is the fair comparison). Detectors learn domain vocabulary (AUROC 0.69 across tau2-bench domains without new labels), were flipped by confident rewrites of honest-failure closings in 20% of cases, and lose precision as false successes get rarer (an implied 0.25 when 5% of runs fail in another study, where step count alone reached 0.716), so they rank runs for review and do not decide them. Better-built judges narrow or reverse the gap: 2026 frontier judges reached AUROC 0.79 to 0.85 at telling failed from successful tau2-bench runs and 0.93 on web runs, withholding the agent's report raised a GUI judge's recall of false successes by 13 to 43 points, and Microsoft's own verifier accepted 1 to 8% of failed computer-use runs at about 65 model calls per run; where the outcome is decided by evidence the trajectory never shows (hidden tests), trained judges did little better than chance.

## Related

- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
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
