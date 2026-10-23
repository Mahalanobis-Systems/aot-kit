---
name: few-shot-examples
description: "AOT optimization 3.a.i (Tier 3, Tuning): Add worked examples to the prompt (few-shot), or curated example queries for data agents. Placeholder. Use when an agent shows: outputs that miss the expected shape or metric definition; repeated queries for the same custom metric."
---

<!-- Generated from library/entries/few-shot-examples.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Add worked examples to the prompt (few-shot), or curated example queries for data agents

> **Placeholder.** Generated from `library/entries/few-shot-examples.yaml` (entry 3.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 3.a.i |
| Earlier id | T11 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Prompts: Structuring |
| Change | prompt / few_shot (add) |

## What it is

Add solved examples of the task to the prompt. For data agents the examples are curated example queries (commented SQL for custom metrics, an example-query index). Vary their form so the model reasons about the case instead of copying the examples' pattern, and don't add examples where the problem calls for validation.

## When it applies

- **In the code:** a prompt with no worked examples on a task with a fixed output shape; a data agent with no example queries for its metrics
- **In traces:** outputs that miss the expected shape or metric definition; repeated queries for the same custom metric
- **In eval results:** failures that cluster on custom metrics or an output format the examples would show

## How (outline)

To be written: the entry names the change but not the steps.

## How to measure

- **experiment** (Tier 3): paired eval with and without the examples, on held-out cases

## Expected impact

- **Quality:** mixed, medium: weak in VeRO (MATH train 0.81 to 0.83, validation flat); strong for data agents (Genie 54% to 77%)
- **Cost:** degrades, small: more prompt tokens
- **Performance:** none

## Evidence (summary)

- paper Figure 12: Adding few-shot maths examples: train 0.81 to 0.83, validation flat at 0.87.
- Databricks, "How to Build Production-Ready Genie Spaces and Build Trust Along the Way"… (2026-02): 54% to 77% on 13 questions.
- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07): 49% to 24%.

## Caveats

Vary the examples (3.a.ii, avoid few-shot ruts). Don't add examples where the problem calls for validation, one of VeRO's anti-patterns.

## Related

- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)

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
