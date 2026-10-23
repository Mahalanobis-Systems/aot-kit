---
name: language-agent-tree-search
description: "AOT optimization 7.c.v (Tier 4, Restructuring): Language Agent Tree Search (LATS). Placeholder. Use when an agent shows: Tree size; rollouts per item."
---

<!-- Generated from library/entries/language-agent-tree-search.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Language Agent Tree Search (LATS)

> **Placeholder.** Generated from `library/entries/language-agent-tree-search.yaml` (entry 7.c.v). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.v |
| Earlier id | P34 (Reasoning & Search, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it replaces a single chain with a search |
| Categories | Orchestration: Scaling compute |
| Change | workflow / planning |

## What it is

MCTS with LLM reflection.

## When it applies

- **In the code:** MCTS loop with selection, expansion, simulation and backpropagation; reflection used as value.
- **In traces:** Tree size; rollouts per item.
- **In eval results:** Accuracy vs ReAct at equal budget.
- **Judge:** Rate reflections used as value estimates.
- **Probes:** Multi-step tasks with recoverable mistakes.

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **Unit:** UCB selection and backprop.
- **Examples:** Recoverable-mistake probes.
- **Benchmark:** HotpotQA or WebShop style.

## Expected impact (first-pass assessment, unmeasured)

- **Quality:** improves, medium
- **Cost:** degrades, large
- **Performance:** degrades, large
- **Security:** none
- **Governance:** none
- **Brand:** none

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Zhou et al., "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models", https://arxiv.org/abs/2310.04406 (2023-10-06): "state-of-the-art pass@1 accuracy (92.7%) for programming on HumanEval with GPT-4"; "average score of 75.9" on WebShop with GPT-3.5, "comparable to gradient-based fine-tuning"

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
