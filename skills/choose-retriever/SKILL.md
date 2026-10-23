---
name: choose-retriever
description: "AOT optimization 8.a.i (Tier 3, Tuning): Choose the retriever by corpus size and question type. Placeholder. Use when an agent shows: repeated searches that fail to narrow; documents found but never read in full; failure rows labeled missed-read on multi-hop questions."
---

<!-- Generated from library/entries/choose-retriever.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Choose the retriever by corpus size and question type

> **Placeholder.** Generated from `library/entries/choose-retriever.yaml` (entry 8.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 8.a.i |
| Earlier id | T57 |
| Tier | 3 (Tuning): routing between retrieval paths that exist |
| Categories | Retrieval: Expanding sources; Retrieval: Querying precisely; Orchestration: Routing |
| Change | tool / search (restructure) |

## What it is

On a bounded corpus (up to about 100K documents), grep and file reads over the raw text beat an embedding retriever: the agent narrows into documents it has found. As the corpus grows, grep degrades (37.5% at 400K); add semantic search beside it, and on large codebases semantic search plus grep beats grep alone. A dense retriever beats BM25. Use a knowledge-graph retriever only for multi-hop and synthesis questions, routed per query; keep chunk retrieval for single-fact lookup, return source text with any graph triplets, and avoid global community-summary search for detail questions.

## When it applies

- **In the code:** the retriever in use and the corpus size; a single retrieval path for all question types
- **In traces:** repeated searches that fail to narrow; documents found but never read in full; failure rows labeled missed-read on multi-hop questions
- **In eval results:** retrieval recall and answer accuracy split by corpus size and question type

## How (outline)

1. Size the corpus and classify the questions (single-fact, multi-hop).
2. Pick the retriever by the table in the summary.
3. Paired eval, retriever A against B, on the agent's own corpus, measuring evidence localization as well as document recall.

## How to measure

- **experiment** (Tier 3): paired eval, retriever A against B, split by question type
- **production-test** (Tier 4): when a new index is introduced

## Expected impact

- **Quality:** improves, large: grep 80.0% against 69.0% for an 8B embedding retriever at ~100K documents (May 2026); Cursor +12.5% from semantic search plus grep on large codebases; GraphRAG routing +1.1%, concatenating both +6.4% (Mar 2026)
- **Cost:** improves, medium: grep 29% cheaper at ~100K documents; a graph index costs to build

## Evidence (summary)

- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): BrowseComp-Plus (830 q, 100,195 docs, avg 5,179 words), same Sonnet 4.6 backbone: Qwen3-Embedding-8B retrieval agent 69.0% -> DCI-Agent-CC 80.0% (+11.0), cost $1,440 -> $1,016 (-29.4%); beats best retrieval baseline GPT-5 + Qwen3-Embed-8B…
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): BrowseComp-Plus 100-q subset, GPT-5.4 nano, L4 context policy: read+grep 61% acc, 19 tool calls, $0.0355/q vs Qwen3-Embedding-8B retrieval 45%, 18 calls, $0.0498/q vs BM25 32%, 19 calls, $0.0527/q.
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): BrowseComp-Plus 100-q subset, GPT-5.4 nano: open bash 73% vs read+grep 61% (+12), but 35 vs 19 tool calls and $0.1021 vs $0.0355 per q. Lite bash usage (3,168 commands): rg | head 56.2%, rg | rg 20.6%, wc 7.8%, single rg 6.3%, ls 4.3%…
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): DCI-Agent-CC, BrowseComp-Plus 100-q subset, corpus padded with FineWeb distractors: 100K -> 200K docs: tool calls 38.5 -> 86.9, latency and cost more than doubled, accuracy -13.6 points. At 400K docs: accuracy 37.5%, 122.4 calls on…
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): DCI-Agent-Lite, GPT-5.4 nano, BrowseComp-Plus 100-q subset. L0 none: 72% acc, $0.0716/q, 2,226 s. L1 truncate 50K: 75%, fastest (1,820 s), highest retained gold coverage 31.3. L2 truncate 20K: 69% (worst), cheapest $0.0590. L3 truncate 20K…
- …and 20 more sources in `library/entries/choose-retriever.yaml`.

## Related

- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)

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
