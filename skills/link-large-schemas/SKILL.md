---
name: link-large-schemas
description: "AOT optimization 8.b.ii (Tier 3, Tuning): Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall. Placeholder. Use when an agent shows: queries against non-existent columns or the wrong tables on a large schema; prompt tokens dominated by the schema; schema prompts that overflow the window; exploration runs that end at the turn cap or spend tens of seconds linking per question."
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

When a database schema is too large to load whole, let the agent find the tables and columns each question needs by exploring it, instead of retrieving once up front. Seed it with all table names plus the top retrieved columns, give it a column index, metadata probes and trial queries, favor recall and cap the turns low. First check that the schema really is too large: in one independent comparison of eight linking methods, the whole schema gave GPT-4.1 and Gemini 2.5 Pro their best accuracy at every size tested, and linking paid off only for economy and open models on schemas of 1,000 or more columns. AutoLink reports keeping every needed column on 91.2% of Spider 2.0-Lite questions, but an independent rerun on Spider 2.0-Snow found 31.55% on the largest schemas, and exploring took 45 to 131 s of linking per question with self-hosted 14B models, against about 4 s for a single linking prompt.

## When it applies

- **In the code:** a schema too large to load whole, or over about 1,000 columns with an economy or open model, linked by a single up-front retrieval or sent whole in every prompt; a linking or exploration step in front of a schema that fits a flagship model's window, with no full-schema comparison
- **In traces:** queries against non-existent columns or the wrong tables on a large schema; prompt tokens dominated by the schema; schema prompts that overflow the window; exploration runs that end at the turn cap or spend tens of seconds linking per question
- **In eval results:** strict schema-linking recall and execution accuracy on the large-schema subset, with no full-schema or one-shot retrieval baseline

## How (outline)

1. Start from the baselines: count the schema's tokens as you would send it (names, types, descriptions, sample values) against the model's window, and run the full schema (where it fits, 5.b.i) and a one-shot column retrieval on the same questions before adding exploration. In one independent comparison, the full schema gave GPT-4.1 and Gemini 2.5 Pro their best accuracy at every schema size tested (0.37 to 0.58), no linking method beat it by more than a point under 1,000 columns for any model class, and linking (done by GPT-4.1) paid only for economy and open generators on larger schemas (0.29 against 0.19 and 0.16 at 1,000 to 2,500 columns).
2. Build a column-level vector index of the schema (1.4 s per database on one H100 in one study). If the catalog spans many databases, shortlist the database before linking columns: run over a 53-database, 102,341-column catalog with no target database given, AutoLink used 635K to 652K tokens per question, and in that study removing the database-shortlisting step lowered column recall in all six settings.
3. Seed each question with all table names plus the top retrieved columns (strict recall 79.2% with the top 5 columns, 91.2% with the top 100) rather than starting from nothing: an untrained 4B model exploring with no schema in context lost 17.0 points on BIRD against having the schema (an 8B model lost 2.0).
4. Give the agent actions to retrieve more columns with its own queries (removing this cost 6.7 to 7.6 points of strict recall, the largest ablation), to probe metadata and sample values with exploratory SQL (results capped at a few rows, with a timeout), and to test sufficiency with a minimal executable query before it writes the answer (in one pilot, making the agent commit to a verified schema first cut hallucinated tables and columns from 26.4% of failures to 2.8%).
5. Favor recall, then keep the set small: in a regression over 183,825 generated queries, column recall dominated accuracy (coefficient 3.382, against 0.096 for column precision), yet the linked set's size still cost accuracy (-0.429 per log column count). AutoLink's linked sets ran at 8.00% field precision in an independent rerun, held 9.5 to 24.9 times more columns than a hierarchical linker, and raised SQL-generation tokens (65.82K against 45.53K to 52.41K), so track the set's size next to recall.
6. Cap exploration at a few turns (strict recall 89.2% at 4 turns against 91.2% at 10, with 3.72 to 5.79 turns used) and budget for latency: AutoLink took 45 to 131 s of linking per question on BIRD-dev with self-hosted 14B models, against about 4 s for a single linking prompt. AutoLink's authors used a non-reasoning policy because a reasoning model broke the action format.
7. Measure with paired runs on your own large schemas, split by schema size, against the full schema (where it fits) and one-shot retrieval, with the production model and a cheaper one: strict linking recall (questions whose linked set holds every needed column), linked-set size, execution accuracy, tokens for linking and for generation, and wall-clock per question.

## How to measure

- **experiment** (Tier 3): paired runs on the same questions over your own large schemas, split by schema size (columns), with the production model and a cheaper one: the full schema where it fits, one-shot column retrieval, and exploration; report strict linking recall (questions whose linked set holds every needed column), linked-set size, execution accuracy, tokens for linking and for generation, and wall-clock per question
- **monitor**: in production traces: queries that reference tables or columns outside the linked set or the schema, exploration turns and runs ending at the turn cap, linked-set size, the schema's share of prompt tokens, and linking wall-clock per question

## Expected impact

- **Quality:** mixed, large: AutoLink kept every needed column on 91.2% of Spider 2.0-Lite questions against 64.0% for the best full-schema linker (Wang, Nov 2025), but an independent rerun on Spider 2.0-Snow got 73.11% overall and 31.55% on schemas of 506 or more fields, and its linked schemas gave 32.88% execution accuracy against 36.75% for a non-iterative linker (Zheng, May 2026); against sending the whole schema, linking lost for GPT-4.1 and Gemini 2.5 Pro at every size and won only for economy and open models on schemas of 1,000 or more columns (0.29 against 0.19 and 0.16 at up to 2,500) (Luoma, May 2026); an untrained 4B model exploring with no schema lost 17.0 points on BIRD, while an RL-trained one matched the full schema (64.9% against 64.8%) (Jian, Mar 2026)
- **Cost:** mixed, medium: 21.2K against 171.9K tokens per question for full-schema linkers on Spider 2.0-Lite (Wang, Nov 2025); in a rerun on Spider 2.0-Snow, 77.93K linking tokens against 240.34K and 580.80K for two other linkers, but its larger linked schemas raised generation tokens to 65.82K against 45.53K to 52.41K (Zheng, May 2026); 635K to 652K tokens per question over a 53-database catalog (Xu, Aug 2026); under 1,000 columns, LLM-based linkers used more tokens than sending the full schema (Luoma, May 2026)
- **Performance:** degrades, large: AutoLink's linking took 45 to 131 s per question on BIRD-dev with self-hosted 14B models against about 4 s for a single linking prompt, and 465 to 638 s on a 53-database Spider 2.0-Snow catalog (Xu, Aug 2026); an agentic column-by-column linker took 32 to 352 s per question and was infeasible above 2,500 columns (Luoma, May 2026); a trained 4B exploring agent took 0.6 s against 0.4 s with the schema in context (Jian, Mar 2026)

## Evidence (summary)

- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 1, DeepSeek-V3 backbone for all LLM methods. Spider 2.0-Lite SRR 91.2% at 21.2K avg tokens vs SQL-to-Schema 64.0% at 171.9K, MCS-SQL 58.9% at 168.9K, RSL-SQL 52.0% at 29.2K, LinkAlign 36.4% at 66.7K; Bird-Dev SRR 97.4% at 8.0K vs…
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Ablation Table 4 (Spider 2.0-Lite SRR, removing the @retrieve_schema action that queries this index): n=5 79.2 -> 72.4 (-6.8); n=50 88.0 -> 80.4 (-7.6); n=100 91.2 -> 84.5 (-6.7) - the largest ablation. Build cost: 222.8 s for 158 Spider…
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 4: removing @retrieve_schema costs 6.7-7.6 SRR points (see index entry). Table 7, top-m per call: m=1 SRR 89.2 (20.7K tokens), m=2 89.6 (21.0K), m=3 91.2 (21.2K). Contrasted with CHESS-style question rewriting; not directly compared.
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 4 (Spider 2.0-Lite SRR) removing @explore_schema: n=5 79.2 -> 76.8 (-2.4); n=50 88.0 -> 84.8 (-3.2); n=100 91.2 -> 88.8 (-2.4).
- Ziyang Wang, Yuanlei Zheng, Zhenbiao Cao, Xiaojin Zhang, Zhongyu Wei, Pei Fu, Zhenbo Luo, Wei Chen, Xiang Bai (HUST, Fudan, Xiaomi)… (2025-11-21): Table 4 (Spider 2.0-Lite SRR) removing @verify_schema: n=5 79.2 -> 77.2 (-2.0); n=50 88.0 -> 86.8 (-1.2); n=100 91.2 -> 89.6 (-1.6).
- …and 11 more sources in `library/entries/link-large-schemas.yaml`.

## Caveats

The case for exploration still rests mostly on AutoLink's own ablations (Spider 2.0-Lite, a DeepSeek-V3 policy), which compared it with other linkers but not with sending the full schema to the generator; in a competing team's rerun on Spider 2.0-Snow with GLM-5.1, it kept every needed field on 31.55% of questions over schemas of 506 or more fields, at 8.00% precision overall, and its linked schemas trailed a non-iterative linker downstream. Whether to link at all depends on schema size and model: in the one independent comparison against the full schema (eight linking methods, none an exploration agent like AutoLink, with GPT-4.1 doing the LLM-based linking), the full schema won for GPT-4.1 and Gemini 2.5 Pro at every size, and most of its large schemas came from 221 Spider 2 questions and Bird schemas padded with generated tables. Exploration costs time and needs a capable policy: AutoLink's latency figures come from self-hosted 14B models, an untrained 4B model exploring from no schema lost 17.0 points, and AutoLink's authors found a reasoning model a worse policy because its instruction following degraded.

## Related

- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
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
