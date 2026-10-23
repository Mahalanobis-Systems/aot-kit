---
name: link-large-schemas
description: "AOT optimization 8.b.ii (Tier 3, Tuning): Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall. Placeholder. Use when an agent shows: queries against non-existent columns or the wrong tables on a large schema; prompt tokens dominated by the schema."
---

<!-- Generated from library/entries/link-large-schemas.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall

> **Placeholder.** Generated from `library/entries/link-large-schemas.yaml` (entry 8.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 8.b.ii |
| Earlier id | T71 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Retrieval: Querying precisely |
| Change | tool / database (add) |

## What it is

When a schema is too large to load whole, link the tables and columns a question needs by exploration rather than by one up-front retrieval or by loading everything: start from all table names plus the top retrieved columns, give the agent a column-level vector index, metadata probes and trial queries to grow the linked set, favor recall over minimizing noise, and cap the exploration turns low.

## When it applies

- **In the code:** a large schema (too many tables to load whole) linked by a single up-front retrieval, or loaded whole into every prompt
- **In traces:** queries against non-existent columns or the wrong tables on a large schema; prompt tokens dominated by the schema
- **In eval results:** schema-linking recall and execution accuracy on the large-schema subset

## How (outline)

1. Build a column-level vector index of the schema.
2. Seed each question with all table names plus the top retrieved columns.
3. Give the agent actions to retrieve more columns, probe metadata and sample values with exploratory SQL (results capped at a few rows, with a timeout), and test sufficiency with a minimal executable query.
4. Cap exploration at a few turns.
5. Paired eval on schema-linking recall (share of needed columns kept), execution accuracy and tokens.

## How to measure

- **experiment** (Tier 3): paired eval on schema-linking recall, execution accuracy and tokens on large schemas

## Expected impact

- **Quality:** improves, large: AutoLink: 91.2% of needed columns kept against 64.0% for the best full-schema method on Spider 2.0-Lite (Nov 2025)
- **Cost:** improves, large: 21.2K against 171.9K tokens per question

## Evidence (summary)

- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 1, DeepSeek-V3 backbone for all LLM methods. Spider 2.0-Lite SRR 91.2% at 21.2K avg tokens vs SQL-to-Schema 64.0% at 171.9K, MCS-SQL 58.9% at 168.9K, RSL-SQL 52.0% at 29.2K, LinkAlign 36.4% at 66.7K; Bird-Dev SRR 97.4% at 8.0K vs…
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Ablation Table 4 (Spider 2.0-Lite SRR, removing the @retrieve_schema action that queries this index): n=5 79.2 -> 72.4 (-6.8); n=50 88.0 -> 80.4 (-7.6); n=100 91.2 -> 84.5 (-6.7) - the largest ablation. Build cost: 222.8 s for 158 Spider…
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 4: removing @retrieve_schema costs 6.7-7.6 SRR points (see index entry). Table 7, top-m per call: m=1 SRR 89.2 (20.7K tokens), m=2 89.6 (21.0K), m=3 91.2 (21.2K). Contrasted with CHESS-style question rewriting; not directly compared.
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 4 (Spider 2.0-Lite SRR) removing @explore_schema: n=5 79.2 -> 76.8 (-2.4); n=50 88.0 -> 84.8 (-3.2); n=100 91.2 -> 88.8 (-2.4).
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 4 (Spider 2.0-Lite SRR) removing @verify_schema: n=5 79.2 -> 77.2 (-2.0); n=50 88.0 -> 86.8 (-1.2); n=100 91.2 -> 89.6 (-1.6).
- …and 6 more sources in `library/entries/link-large-schemas.yaml`.

## Caveats

One paper (AutoLink, Nov 2025) supplies all of the evidence, on Spider 2.0 with a DeepSeek-V3 policy; the component ablations are its own. It found a reasoning model a worse policy because its instruction following degraded.

## Related

- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)

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
