---
name: ground-queries-in-schema
description: "AOT optimization 5.b.i (Tier 3, Tuning): Give the model the schema it queries, in context: descriptions, keys, codes, sample values. Placeholder. Use when an agent shows: queries against non-existent columns, wrong joins, guessed codes; SQL that omits a rule the context documents (a NULL wildcard read as unknown, an excluded code kept); failure rows labeled tool-hallucination (names) or domain-knowledge-deficit."
---

<!-- Generated from library/entries/ground-queries-in-schema.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Give the model the schema it queries, in context: descriptions, keys, codes, sample values

> **Placeholder.** Generated from `library/entries/ground-queries-in-schema.yaml` (entry 5.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 5.b.i |
| Earlier id | T40 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Context: Filtering input; Retrieval: Querying precisely |
| Change | prompt / context (add) |

## What it is

Tell a SQL-writing agent what its data means, not only what it is called: what each column, code and NULL means and how each metric is computed, with keys and sample values. The meaning does the work: emptying the prose from an otherwise identical context cost 26 to 36 points on hard data-agent tasks across four models in one ablation, a 4 KB semantic document added 17 to 23 points for three frontier models in a vendor study, and keys and join paths added only a few points over descriptive names in a third study. Put a short document in the prompt; when the rules run long, keep an index in the prompt and let the agent read each rule by name, since the same knowledge pasted as a 24,177-character prompt gained much less, and on a second benchmark long business documents helped less than concise rule snippets. Each result rests on one benchmark, and once the schema outgrows a modest share of the window, link it by exploration (8.b.ii).

## When it applies

- **In the code:** a SQL-writing agent with no column descriptions, code meanings, null semantics or metric definitions in its context; a long rule document pasted whole into the system prompt with no index or lookup by name; schema context reachable only through a similarity-search tool
- **In traces:** queries against non-existent columns, wrong joins, guessed codes; SQL that omits a rule the context documents (a NULL wildcard read as unknown, an excluded code kept); failure rows labeled tool-hallucination (names) or domain-knowledge-deficit
- **In eval results:** failures from wrong table, column or value, or from a documented rule not applied

## How (outline)

1. Start from the baseline: run your own questions with the bare schema (table and column names, types) and count what the full context would cost in tokens as you would send it (descriptions, code meanings, sample values, rule documents); if the schema alone takes more than a modest share of the window, use 8.b.ii instead.
2. Make every name say what it holds, then add keys: in one factorial study on corrected BIRD questions, replacing anonymous column names with abbreviated ones moved accuracy 18.5 to 42.3 points by difficulty, while adding types, primary keys, foreign keys and join paths to a names-only schema moved it 2.6 to 5.5, most on the hardest questions (models up to Gemini 2.5 Flash). Rename or describe cryptic identifiers first and name link columns plainly: with foreign keys declared, the model still joined on canonical key names.
3. Write down what no column name records: what each code means, what a NULL means (in one benchmark a NULL in a fee rule meant 'applies to all values', not 'unknown'), and how each metric is computed, as a SQL expression where you can, starting from existing manuals and data dictionaries. Most of the gain is here: emptying that prose from an otherwise identical context cost 26 to 36 points on hard DABStep tasks across four models, and BIRD's per-question hints added 16.36 points on BIRD dev for gemini-1.5-pro.
4. Add sample values for the text and code columns that questions filter on: in one study they added 1.76 points overall and 5.52 on challenging BIRD questions, for about 4,772 more tokens per request (mean plus one standard deviation).
5. Choose the delivery by length. A short document goes in the prompt: a 4 KB semantic document added 17 to 23 points for three frontier models in a vendor study, where an agentic platform holding the same knowledge did not significantly beat raw DDL. When the rules run long, keep an index of domains and metrics in the prompt and have the agent read each rule by name, from files or a lookup tool, before it writes SQL: the same knowledge pasted as a 24,177-character prompt trailed the lookups by 13.7 to 44.6 hard-task points and on one model did no better than the bare schema, and on another benchmark all eight systems tested did better with concise expert-written evidence than with the whole business document (21.4% against 15.9% for the best).
6. Keep the static part cache-friendly (3.b.i) and watch the bill: looked-up rules are billed as fresh input (on GPT-5.6, $8.87 against $3.55 of fresh input for the cached prompt, $21.32 against $14.42 in total), though fewer turns and less reasoning made lookups the cheapest per correct answer on three of four models.
7. Measure with paired runs on your own questions, with the production model and a cheaper one: bare schema against the full context and, where it runs long, prompt against index plus lookups. Report execution accuracy split by questions that need a documented rule and those that don't (the pasted manual led on the easy tasks on all four models), wrong-table, wrong-column, wrong-value and rule-not-applied failures, whether the SQL carries each documented rule, fresh and cached input tokens, turns, and cost per correct answer, over at least two runs (23.4% of verdicts flipped between two near-identical runs in one study).

## How to measure

- **experiment** (Tier 3): paired runs on the same questions with the production model and a cheaper one: bare schema, schema plus descriptions, code meanings, null semantics and metric definitions, and, where the semantics run long, the same content pasted in the prompt against an index plus lookups by name; report execution accuracy split by questions that need a documented rule and those that don't, failures by wrong table, column, value or rule not applied, fresh and cached input tokens, turns and cost per correct answer, over at least two runs
- **monitor**: in production traces: queries against non-existent columns or guessed codes, SQL that omits a documented rule (for example a NULL wildcard read as unknown), lookups per question and questions answered without one, the schema context's share of prompt tokens and its cache hit rate

## Expected impact

- **Quality:** improves, large: domain semantics fetched by lookup raised hard DABStep accuracy from 13.9-37.0% to 55.1-77.4% on four models, 26 to 36 points of it from the prose itself, while the same knowledge pasted as a 24,177-character prompt reached 22.9-50.3% (Ye, Sep 2026); a 4 KB semantic document +17.2 to +23.2 points on 99 questions, breaking 4 to 8 passing ones per model (Rumiantsau, Apr 2026); long business documents raised the best of eight systems from 6.8% to 15.9%, concise per-question evidence to 21.4% (Liao, Jun 2026); BIRD hints +16.36 and sample values +1.76 (+5.52 on challenging questions) for gemini-1.5-pro (Chung, Jan 2025); abbreviated names over anonymous ones +18.5 to +42.3, keys and join paths +2.6 to +5.5 (Su, Jun 2026)
- **Cost:** mixed, medium: a 4 KB document added 2.4K to 4.2K input tokens per query (Rumiantsau, Apr 2026) and sample values about 4,772 tokens per request, mean plus one SD (Chung, Jan 2025); caching the prefix (3.b.i) makes a static document near free in steady state (Cube's claim, unmeasured); in an agent, a 24,177-character pasted manual meant 191k input tokens per task against 91k for the bare schema on Sonnet 5, and lookups were billed as fresh input ($21.32 against $14.42 for the cached manual on GPT-5.6) but cut turns and reasoning, giving a lower cost per correct answer than the bare schema on all four models (Ye, Sep 2026)
- **Performance:** none: latency per query changed -0.9 to +1.8 s with a 4 KB document (Rumiantsau, Apr 2026); 4,772 more tokens of sample values left normalized latency unchanged, but latency grows near-linearly with context and its variance rises past 32K tokens (Chung, Jan 2025); in an agent, fetched semantics took the fewest turns per task of any arm on all four models (Ye, Sep 2026)

## Evidence (summary)

- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Same bundled 5-query result. "The semantic layer is already great documentation ... We were building tools to summarize what was already legible. Claude just needed access to read it directly." Code: sandbox.writeFiles(files) from…
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): n=99, single shot, analytical verdict. Opus 4.7 50.5% -> 67.7% (+17.2 pp, McNemar b/c 22/5, p=0.0015); Sonnet 4.6 46.5% -> 68.7% (+22.2 pp, 30/8, p=0.0005); GPT-5.4 45.5% -> 68.7% (+23.2 pp, 27/4, p<0.0001). The document also broke 4-8…
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): Reported only in passing, numbers not given. Paper §6.5: an internal experiment found "an agentic-tool-use system with equivalent underlying semantic knowledge did not outperform the schema-only baseline on this benchmark"; REPORT.md 3.5…
- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07-18): Described in §2.2.2; not ablated separately.
- Qing Ye (independent researcher), "Which Part of the Context Layer Does the Work? Separating Semantic Content from Retrieval Scaffolding in… (2026-09-06): Table 4, hard-split accuracy (GLM / DeepSeek / Sonnet 5 / GPT-5.6): bare schema 13.9 / 22.6 / 22.9 / 37.0%; hollow contract (same nine tools and instruction, prose emptied) 19.3 / 22.6 / 38.0 / 51.2%; manual pasted into a 24,177-character…
- …and 3 more sources in `library/entries/ground-queries-in-schema.yaml`.

## Caveats

Each measured gain rests on one benchmark and few runs: Cube's vendor study (99 questions on one 25-table schema), a single-author ablation on DABStep in which 294 of 332 hard tasks are fee questions, no run was repeated and the author maintains the lookup library tested, and BIRD studies with gemini-1.5-pro or models no larger than Gemini 2.5 Flash. The lookup-over-prompt result is confounded and bounded: the looked-up contract restated the manual as per-metric entries with SQL expressions and settled three points the manual left open, the pasted manual still led on easy tasks on all four models, and Cube's internal test favored the prompt for its 4 KB document. On EntSQL, concise evidence beat whole documents only when experts wrote it per question, and even then Claude Code reached 20.3% against 84.0% for experts on a 212-question sample. Past a modest share of the window, loading the whole schema costs more than it returns; that is 8.b.ii.

## Related

- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)

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
