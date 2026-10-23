---
name: ground-queries-in-schema
description: "AOT optimization 5.b.i (Tier 3, Tuning): Give the model the schema it queries, in context: descriptions, keys, codes, sample values. Placeholder. Use when an agent shows: queries against non-existent columns, wrong joins, guessed enum codes; failure rows labeled tool-hallucination (names) or domain-knowledge-deficit."
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

When the model writes SQL or structured filters, put the schema it is querying in its context: table and column descriptions, key relationships, what enum codes and nulls mean, sample values. Give it directly, in the prompt or as files it reads, rather than behind a search tool. This holds while the schema fits in a modest share of the window; past that, link it by exploration (8.b.ii). Making the schema context good (names, descriptions, examples) is data-side work.

## When it applies

- **In the code:** a SQL-writing agent with no table and column descriptions, keys or allowed values in its context; schema context reachable only through a search tool
- **In traces:** queries against non-existent columns, wrong joins, guessed enum codes; failure rows labeled tool-hallucination (names) or domain-knowledge-deficit
- **In eval results:** failures from wrong table, column or value

## How (outline)

1. Count the schema's tokens with descriptions and sample values; if it takes more than a modest share of the window, use 8.b.ii instead.
2. Write or generate the missing descriptions: column meanings, keys, enum codes, null semantics.
3. Put the schema in the prompt, or mount it as files, instead of a retrieval tool.
4. Paired eval on execution accuracy and wrong-table, wrong-column and wrong-value failures.

## How to measure

- **experiment** (Tier 3): paired eval with and without the schema context, on execution accuracy

## Expected impact

- **Quality:** improves, large: Cube: +17 to +23 points from a semantic-context document on 99 questions (Apr 2026)
- **Cost:** degrades, small: the schema costs prompt tokens on every call; caching the prefix (3.b.i) recovers most of it
- **Performance:** none

## Evidence (summary)

- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Same bundled 5-query result. "The semantic layer is already great documentation ... We were building tools to summarize what was already legible. Claude just needed access to read it directly." Code: sandbox.writeFiles(files) from…
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): n=99, single shot, analytical verdict. Opus 4.7 50.5% -> 67.7% (+17.2 pp, McNemar b/c 22/5, p=0.0015); Sonnet 4.6 46.5% -> 68.7% (+22.2 pp, 30/8, p=0.0005); GPT-5.4 45.5% -> 68.7% (+23.2 pp, 27/4, p<0.0001). The document also broke 4-8…
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): Reported only in passing (Section 6.5; REPORT.md 3.5): "did not significantly outperform raw-DDL Claude on this benchmark"; numbers not given in the paper. 25-table schema, so everything fit in context; the authors flag 1,000+ table…
- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07-18): Described in §2.2.2; not ablated separately.

## Caveats

The measured gain comes from a semantic-layer vendor's study (Cube) on one 25-table schema. Past a modest share of the window, loading the whole schema costs more than it returns; that is 8.b.ii.

## Related

- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
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
