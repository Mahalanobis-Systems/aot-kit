---
name: semantic-layer-routing
description: "AOT optimization 7.a.i (Tier 3, Tuning): Route metric questions through a deterministic semantic layer; fall back to text-to-SQL. Placeholder. Use when an agent shows: wrong numbers on questions whose metric the layer defines; failure rows labeled reasoning-failure on metric questions."
---

<!-- Generated from library/entries/semantic-layer-routing.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Route metric questions through a deterministic semantic layer; fall back to text-to-SQL

> **Placeholder.** Generated from `library/entries/semantic-layer-routing.yaml` (entry 7.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 7.a.i |
| Earlier id | T54 |
| Tier | 3 (Tuning): routing within a single agent |
| Categories | Orchestration: Routing; Retrieval: Querying precisely |
| Change | workflow / control_flow (add) |

## What it is

Where a semantic layer exists, have the agent answer metric questions by choosing metrics and dimensions that the layer compiles to SQL, and write SQL only when the layer cannot answer. The layer fails with an explicit error rather than a plausible wrong answer. Higher reasoning effort or a bigger model did not close the gap; the layer did.

## When it applies

- **In the code:** a data agent that writes SQL directly although a semantic or metrics layer exists
- **In traces:** wrong numbers on questions whose metric the layer defines; failure rows labeled reasoning-failure on metric questions
- **In eval results:** accuracy on metric questions, split by whether the layer defines them

## How (outline)

1. Confirm a semantic layer covers the metrics the agent is asked about.
2. Add a first path that maps the question to metrics and dimensions; fall back to SQL on a layer error.
3. Paired eval on metric questions, tracking explicit errors against wrong answers.

## How to measure

- **experiment** (Tier 3): paired eval on metric questions

## Expected impact

- **Quality:** improves, large: dbt: 98.2% against 90.0% (Sonnet 4.6), 100% against 84.1% (GPT-5.3 Codex), 11 questions x 20 runs (Apr 2026)

## Evidence (summary)

- Jason Ganz, Benoit Perigaud (dbt Labs), "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update"… (2026-04-07): On questions the Semantic Layer can reach (not too many entity hops), 11-question ACME set x 20 runs: SL 100.0% for both Sonnet 4.6 and GPT-5.3 Codex vs text-to-SQL 62.5% (Sonnet 4.6) and 51.2% (GPT-5.3 Codex) on raw tables; 2023 GPT-4 was…
- Jason Ganz, Benoit Perigaud (dbt Labs), "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update"… (2026-04-07): Recommendation derived from the benchmark above; the routing policy itself was not evaluated. Packaged as a dbt agent skill for answering natural-language questions.
- Jason Ganz, Benoit Perigaud (dbt Labs), "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update"… (2026-04-07): Sweep on SL-answerable questions (Opus 4.6, Sonnet 4.6, GPT-5.3 Codex, GPT-5.2; Anthropic low..max, OpenAI none..xhigh): most configurations hit 95-100% SL accuracy regardless of effort; Sonnet 4.6 100.0% at low/medium/max vs Opus 4.6…
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): Pairwise McNemar, n=99: within the with-document cluster all p >= 0.79 (67.7-68.7%); within the DDL-only cluster all p >= 0.42 (45.5-50.5%); all nine cross-cluster comparisons p < 0.01. Sonnet 4.6 plus the document used ~28% fewer input…

## Caveats

Applies only where a semantic layer already covers the metrics being asked about; building one is data-side work and a separate change. Both studies come from semantic-layer vendors (dbt Labs, Cube), and the question sets are small (11 questions x 20 runs; 99 questions). The routing policy itself, layer first and SQL as fallback, was recommended by dbt but not evaluated.

## Related

- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)

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
