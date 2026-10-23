---
name: surface-unreadable-information
description: "AOT optimization 8.a.ii (Tier 3, Tuning): Surface information the source holds but the agent cannot read. Placeholder. Use when an agent shows: failed opens of PDF, Excel, Word or ZIP files; the set of tables and columns queried, compared with the catalog, joined to failures; failure rows labeled domain-knowledge-deficit or missed-read."
---

<!-- Generated from library/entries/surface-unreadable-information.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Surface information the source holds but the agent cannot read

> **Placeholder.** Generated from `library/entries/surface-unreadable-information.yaml` (entry 8.a.ii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 8.a.ii |
| Earlier id | T39 |
| Tier | 3 (Tuning): it changes what the model can reach and sees |
| Categories | Retrieval: Expanding sources |
| Change | tool / database (add) |

## What it is

Find information a connected source holds that the agent never reads, and expose it. At file level: a reader that drops a format (PDF, Excel, Word, ZIP) or a channel (cell colors, formatting, comments). At warehouse level: tables and columns never queried, found by comparing what the agent queried against the source's catalog and joining that to failed cases; then add them to the schema context. An index over existing metadata raised table discovery sharply. The runtime alternative, a catalog-search tool the agent calls, did not beat giving the schema up front.

## When it applies

- **In the code:** a file tool limited to plain-text formats; a spreadsheet reader that drops formatting; the source catalog lists tables or columns the agent's prompts and tools never reference
- **In traces:** failed opens of PDF, Excel, Word or ZIP files; the set of tables and columns queried, compared with the catalog, joined to failures; failure rows labeled domain-knowledge-deficit or missed-read
- **In eval results:** failures where the answer existed in an unread part of the source

## How (outline)

1. List the source's contents (formats, catalog).
2. Diff against what the agent's tools can read and what its queries touched.
3. Join the gap to failed or insufficient-evidence cases.
4. Extend the reader, or add the missing tables to the schema context (5.b.i).
5. Paired eval on the cases that failed for lack of data.

## How to measure

- **experiment** (Tier 3): paired eval on the questions that failed for lack of data

## Expected impact

- **Quality:** improves, medium: Excel colors +4.9% on FACTS; Genie metadata index raised table-discovery Recall@10 from 0.075 to 0.450 (May 2026); PDF reading flat on GAIA

## Evidence (summary)

- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07-18): Table 2, internal 133-question benchmark, gpt-4o: all knowledge-graph components vs schemas only (A.1): score (% 4+) 48% vs 9%, table recall 78% vs 45%, column recall 56% vs 24%, compile 96% vs 88%. Paper: "Most of the improvement is from…
- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Figure 4, internal table-discovery benchmark, Recall@10 with vs without semantic context by max steps: 2 steps 0.450 vs 0.075; 4 steps 0.623 vs 0.219; 8 steps 0.724 vs 0.342; 16 steps 0.774 vs 0.466. Prose: "improve table search…
- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Described only: "It uses multiple search indices in parallel together with rich metadata signals to efficiently discover most relevant assets for a user query." Not ablated separately from the index itself.
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): Reported only in passing (Section 6.5; REPORT.md 3.5): "did not significantly outperform raw-DDL Claude on this benchmark"; numbers not given in the paper. 25-table schema, so everything fit in context; the authors flag 1,000+ table…
- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Same bundled 5-query result. "The semantic layer is already great documentation ... We were building tools to summarize what was already legible. Claude just needed access to read it directly." Code: sandbox.writeFiles(files) from…
- …and 6 more sources in `library/entries/surface-unreadable-information.yaml`.

## Caveats

The only evidence is one row of the blog's tricks table (checked against the table image, 2026-09-23). It is about background colors alone, not formatting in general, and it credits a FACTS gain to GAIA questions without saying how the two relate. Read it as one instance of 8.a.ii, not as a general spreadsheet technique.

## Related

- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
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
