---
name: tune-search-tool
description: "AOT optimization 8.b.i (Tier 2, Reliability): Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality. Placeholder. Use when an agent shows: many page fetches per question; queries returning zero results followed by the same query or by giving up; results from the wrong product, version or date; failure rows labeled missed-read."
---

<!-- Generated from library/entries/tune-search-tool.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality

> **Placeholder.** Generated from `library/entries/tune-search-tool.yaml` (entry 8.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 8.b.i |
| Earlier id | T34 |
| Tier | 2 (Reliability): retries recover failed searches |
| Categories | Retrieval: Querying precisely; Retrieval: Ranking results |
| Change | tool / search (tune) |

## What it is

Make the search tool return what the model needs to choose what to open (a snippet per result, not just titles; five or more results; a full-document reader beside truncated search), retry failed searches, and reformulate when a query returns little (start broad, then narrow; use the corpus's own terms) rather than retrying it verbatim. Expose the source's metadata as filter parameters (date, product, version, source) where the corpus has it. Drop results from sources that leak the answer or are untrustworthy. Expanding one question into many queries up front has not helped.

## When it applies

- **In the code:** a search tool returning titles or URLs only; a fixed small result count; no retry; no filter parameters over a corpus with metadata; results passed to the model unfiltered
- **In traces:** many page fetches per question; queries returning zero results followed by the same query or by giving up; results from the wrong product, version or date; failure rows labeled missed-read
- **In eval results:** retrieval recall below answer accuracy needs; failures where the answer was in an unfetched result

## How (outline)

1. From traces, count fetches per question, empty-result queries, and repeats of the same query.
2. Change one parameter at a time (snippets, result count, retries, filters).
3. Paired eval scored on retrieval recall and answer accuracy.

## How to measure

- **before-after** (Tier 2): failed-search rate
- **experiment** (Tier 3): paired eval on retrieval recall and answer accuracy

## Expected impact

- **Quality:** mixed, medium: snippets: SimpleQA train +0.15 but validation -0.06; source filtering +3.3% on FACTS; retries and result count unmeasured; up-front query expansion: no gain (LinkedIn, 2025)
- **Cost:** mixed, small

## Evidence (summary)

- repo figure_01: 9/20 runs, and almost none elsewhere; the only benchmark with a retrieval corpus.
- paper Figure 15: Train 0.74 to 0.89, validation 0.80 (down from 0.86 best).
- blog tricks table (Tool-Centric template): +3.3%.
- paper Table 10: Knight "Enhanced (5+ results, retry logic)" vs Pawn "Basic (3 results, no retries)".
- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07-18): Appendix A.5 negative result, gpt-4o: "the query planner lowered recall and quality metrics"; produced overly nested queries even after instructing it to minimize tasks with few-shot examples. Hypothesis: unnecessary for gpt-4o, possibly…
- …and 3 more sources in `library/entries/tune-search-tool.yaml`.

## Related

- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:verify-citations` (9.a.ii, Verify citations claim by claim for factual support)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)

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
