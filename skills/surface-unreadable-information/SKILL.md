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

Find what your agent's sources hold but its readers never pass on, and expose it: file formats and channels a converter drops (font color, highlight, comments, footnotes, PDF or spreadsheet content) and, in a warehouse, tables, joins and past queries the agent never reads. It pays where the answer sits in the dropped part: on 76 real policy documents, recovering the requirements authors had colored or highlighted scored micro F1 0.690 with a parser that kept those cues, against 0.150 with docling and 0.075 with plain text, and in industry reports a metadata index raised table-discovery Recall@10 from 0.075 to 0.450 and a knowledge graph over metadata raised scores from 9% to 48%. Expose the channel that holds the evidence, not everything: OCR text added 13 to 16 points for a small page-image reader on text evidence but extracted text was neutral to harmful on charts, PDF reading left one GAIA agent flat, and loaders widened for coverage also passed on content Office hides, which LLM file services then reported as fact in 48% to 76% of trials.

## When it applies

- **In the code:** a file tool limited to plain-text formats; a converter that drops font color and highlight, comments, footnotes, headers and footers or document properties; a broad converter that emits hidden sheets, rows or off-page text with no provenance tag; the source catalog lists tables or columns the agent's prompts and tools never reference
- **In traces:** failed opens of PDF, Excel, Word or ZIP files; the set of tables and columns queried, compared with the catalog, joined to failures; failure rows labeled domain-knowledge-deficit or missed-read
- **In eval results:** failures where the answer existed in an unread part of the source; evals that score recall but not false positives on unflagged items, or pool text and chart evidence into one number

## How (outline)

1. Start from the baseline: run the current agent on questions whose answers live in each part of the source, and record what its readers emit per file type and which tables and columns its queries touch. List the source's contents: file formats and, inside each, the channels (font color, highlight, comments, footnotes, headers and footers, document properties, tracked changes, hidden sheets, images and charts); for a warehouse, the catalog and the query history.
2. Diff what the readers emit against the source, format by format and channel by channel, and diff the tables and columns queried against the catalog. In one study, docling and plain-text extraction dropped color and highlight, and headers, footers, footnotes and document properties were unreachable from a body-only walk of a Word file; adding those four raised the authors' parser on the Word file-fidelity track of Microsoft's Office Comprehension Benchmark from 0.853 to 0.959.
3. Join the gap to failed or insufficient-evidence cases, and check how often the channel carries meaning: 32.8% of 6,462 policy documents carried deliberate color or highlight (10.3% on an obligation), and those two cues carried the whole effect (+0.302 and +0.262 macro F1 when removed one at a time), while bold, italic, monospace and strikethrough each moved it by at most 0.003.
4. Extend the reader for the channels that carry answers, in code where possible, and label what a cue means rather than passing the raw value: typed tags (critical warning, warning, deprecated) added +0.085 macro F1 over identical raw color markers (p = 0.049; positive on five of six models, significant on three). At warehouse level, add the missing tables to the schema context (5.b.i), and mine the query history into per-table cards (join recipes, filters, example SQL): in one retailer's warehouse, replacing handcrafted documentation with cards distilled from past queries raised table-selection recall from 0.714 to 0.805 and AST similarity from 0.490 to 0.550 (Claude Sonnet 4.6).
5. Match the representation to where the evidence lives: for a 2B page-image reader, adding OCR text raised strict accuracy by 13 to 16 points on text evidence (about double with the PDF text layer, which helped all six open 2B to 8B readers tested), but extracted text was neutral to harmful on charts and figures (-0.046) and trailed where retrieval had missed gold pages (-0.061, p = 0.099), so add it for text evidence behind retrieval that works.
6. Bound what you expose: a loader widened for coverage also reads what the application hides (hidden sheets, rows and columns, vanished text, off-page text boxes, alt text, stale caches); markitdown and Apache Tika exposed 17 and 16 of 21 such mechanisms, and LLM file services reported a planted hidden fact in 48% to 76% of trials. Tag text from channels the author's application does not show with its provenance so the model can discount it (10.c.i).
7. Measure with paired runs, current reader against extended reader on the same model: the cases that failed for lack of data plus questions whose answer lives only in each channel, stratified by evidence modality and retrieval recall; score precision and false positives as well as recall (a converter that dropped the cues raised the false-positive rate on unflagged requirements from 0.011 to 0.043), and track tokens per document (the cue-preserving form cost about twice plain text).

## How to measure

- **experiment** (Tier 3): paired eval, current reader against extended reader on the same model: the questions that failed for lack of data, plus questions whose answer lives only in one channel (color or highlight, comment, footnote, header, hidden sheet, chart, an unqueried table); score recall, precision and false positives on unflagged items, stratified by evidence modality and retrieval recall, and record tokens per document
- **monitor**: per format and channel, the share of files whose loader output lacks content present in the file (failed opens, cues detected in the file but absent from the output) or includes text from views the application hides, and the share of catalog tables and columns never queried, each joined to failure labels; ingestion assertions that every detected cue maps to an emitted span

## Expected impact

- **Quality:** improves, large: Where the answer sits in the dropped channel: author-flagged requirements recovered at micro F1 0.690 with color and highlight kept, against 0.150 (docling) and 0.075 (plain text), across six models (Zhao, Oct 2026); OCR text added 13 to 16 points for a 2B page-image reader on text evidence (Xia, Oct 2026); a metadata index raised table-discovery Recall@10 from 0.075 to 0.450 (Databricks, May 2026, vendor) and a metadata knowledge graph raised score from 9% to 48% (Chen, Jul 2025); query-history cards raised AST similarity 0.490 to 0.550 (Gwimm, Aug 2026). Flat or worse where it is not: extracted text -0.046 on chart and figure questions and +0.004 pooled on MMLongBench-Doc (Xia, Oct 2026); PDF reading flat on GAIA (VeRO, Feb 2026); on BEAVER, cards plus raw SQL 9.00% against 6.33%, p = 0.12 (Gwimm, Aug 2026).
- **Cost:** degrades, medium: Keeping formatting cues cost roughly twice plain-text tokens per document; parsing ran in code with no LLM calls (Zhao, Oct 2026). Genie's 0.23x relative cost covers its whole harness, not this change (Databricks, May 2026).
- **Security:** degrades, medium: When a loader is widened for coverage: broad converters (markitdown, Apache Tika) emitted 17 and 16 of 21 constructions Office does not show, four native-ingestion LLM APIs reported a planted hidden fact in 48% to 76% of trials, and 17.5% of 4,263 ordinary files carried at least one such construction (Liu, Aug 2026). Provenance tags on text from hidden channels are the authors' suggested defense, untested.

## Evidence (summary)

- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07-18): Table 2, internal 133-question benchmark, gpt-4o: all knowledge-graph components vs schemas only (A.1): score (% 4+) 48% vs 9%, table recall 78% vs 45%, column recall 56% vs 24%, compile 96% vs 88%. Paper: "Most of the improvement is from…
- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Figure 4, internal table-discovery benchmark, Recall@10 with vs without semantic context by max steps: 2 steps 0.450 vs 0.075; 4 steps 0.623 vs 0.219; 8 steps 0.724 vs 0.342; 16 steps 0.774 vs 0.466. Prose: "improve table search…
- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Described only: "It uses multiple search indices in parallel together with rich metadata signals to efficiently discover most relevant assets for a user query." Not ablated separately from the index itself.
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): Reported only in passing (Section 6.5; REPORT.md 3.5): "did not significantly outperform raw-DDL Claude on this benchmark"; numbers not given in the paper. 25-table schema, so everything fit in context; the authors flag 1,000+ table…
- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Same bundled 5-query result. "The semantic layer is already great documentation ... We were building tools to summarize what was already legible. Claude just needed access to read it directly." Code: sandbox.writeFiles(files) from…
- …and 10 more sources in `library/entries/surface-unreadable-information.yaml`.

## Caveats

The file-level evidence rests on one study per claim with the authors' own benchmarks: the color and highlight result comes from a task built so the answer is the cue (a text-only classifier reached AUC 0.664), with the authors' own parser and labels not yet checked by humans, and typed cue labels helped on only three of six models. Exposing a channel helps only where the evidence lives in it: extracted text was neutral to harmful on charts and figures and pooled to +0.004 on MMLongBench-Doc, measured with open 2B to 8B readers only, and VeRO's PDF reading left GAIA flat. The warehouse half rests on in-house and vendor reports (LinkedIn, Databricks, Amazon); the only public-benchmark check was directional (9.00% against 6.33%, p = 0.12, with cards alone tying raw historical SQL), and VeRO's +4.9% FACTS row credits GAIA's cell colors without saying how the two relate. Widening a loader also widens what a document can plant: hidden-view content reached LLM answers in 48% to 76% of trials on a constructed test set.

## Related

- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)

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
