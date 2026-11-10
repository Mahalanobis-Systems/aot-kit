---
name: choose-retriever
description: "AOT optimization 8.a.i (Tier 3, Tuning): Choose the retriever by corpus size and question type. Placeholder. Use when an agent shows: repeated searches that fail to narrow; grep commands that time out or return thousands of matches; documents found but never read in full; failure rows labeled missed-read on multi-hop questions."
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

Match the retriever to the corpus: let the agent grep and read the raw files while the corpus is bounded, and put a retriever in front of grep once it grows. On about 100K long web documents, grep and file reads beat an 8B embedding retriever (80.0% against 69.0%) at 29% lower cost, but grep over the whole corpus fell to 37.5% and 32% of questions at 400K documents in two studies, while an agent that pulled retrieved candidates into a working folder and grepped there held 80 to 70 of 100 from 100K to 10M documents at a fraction of the time and cost. The index behind it matters less than older baselines suggested: dense beat default, shallow BM25, but BM25 tuned for long documents and retrieved 1,000 deep matched the dense agent, and on code, embedding search nearly doubled an 8B model's localization over grep but added 3.7 points at 32B. Use a knowledge-graph retriever only for multi-hop and synthesis questions, routed per query; keep chunk retrieval for single-fact lookup, return source text with any graph triplets, and avoid global community-summary search for detail questions.

## When it applies

- **In the code:** the retriever in use and the corpus size; a single retrieval path for all question types; grep over the full corpus with no retriever in front past a few hundred thousand long documents; BM25 at default parameters returning only the top few results on long documents
- **In traces:** repeated searches that fail to narrow; grep commands that time out or return thousands of matches; documents found but never read in full; failure rows labeled missed-read on multi-hop questions
- **In eval results:** retrieval recall (surfaced and read) and answer accuracy split by corpus size and question type

## How (outline)

1. Start from the baseline: record the retriever the agent uses today, the corpus size in documents and average document length, how often it changes, and a sample of real questions labeled single-fact lookup, multi-hop or multi-constraint, synthesis, or code localization; run the current agent on that sample and keep its accuracy, tool calls, wall time and cost.
2. For a bounded corpus (up to about 100K long documents, or single documents of a few hundred thousand tokens), store one file per document in a folder and give the agent grep (ripgrep) plus line-ranged file reads instead of an embedding retriever or the whole corpus in context. On about 100K web documents this scored 80.0% against 69.0% for an 8B embedding retriever at 29% lower cost, and with a small model 61% against 45% (embeddings) and 32% (BM25); a coding agent with no retriever scored 88.5% against 72.5% for an embedding-search agent, one file per document beat one JSON file (89.0 against 83.0 on 100 questions), and on 385K to 536K-token documents it beat GPT-5 reading the text in 200K-token windows by 11.3 and 12.5 points (on 188K-token documents the two tied, 61.5 against 61.0). Allowing piped shell commands raised accuracy from 61% to 73% but cost 2.9 times as much per question.
3. As the corpus grows into the hundreds of thousands of long documents, stop running grep over all of it: expose a retriever as a tool that pulls a few hundred ranked candidates into a working folder, show a short ranked preview, and let the agent grep and read across that folder. Grep alone fell from 67 to 32 and 29 of 100 questions at 100K, 400K and 800K documents as tool errors rose from 1.6% to 54.7%, while the pulled workspace held 80 to 70 of 100 from 100K to 10M documents at $4.03 to $5.17 per 100 questions; on all 830 questions it scored 71.2% against 62.9% at 146 s against 3,139 s and $34.91 against $88.13. Keep cross-document grep inside the workspace: blocking it dropped accuracy from 82 to 40 of 100. Corpora of short passages tolerate grep further: over 21M Wikipedia passages grep-based agents still averaged 83.0 in one study, and in another a coding agent with no retriever beat BM25 RAG on Natural Questions (56.0 against 47.0 exact match).
4. Choose and tune the index behind that tool, and test before adding one beside grep. A dense embedder beat default BM25 returning the top 5 (gpt-5: 55.9% to 70.1%), and bigger embedders found more evidence (0.6B to 8B: recall@100 26.5 to 47.7), but BM25 tuned for long documents (k1 25, b 1 against the default 0.9, 0.4) and retrieved 1,000 deep behind a paged, cached ranking reached 74.6% with gpt-5 against 73.0% for the published dense agent (a different harness) and 83.1% with gpt-5.5; inside the same workspace dense led BM25 by 82 to 80 of 100. Adding a retriever to an agent that already greps did not reliably help (88.5% with none, 84.0% with embeddings, 78.5% with BM25 in one study), and the agent grepped less when it had one.
5. For coding agents, start with grep, glob and file reads, and add embedding search or a code graph where the model is small or the repository large. Semantic search beside grep raised offline accuracy 12.5% on average (6.5 to 23.5% by model) and code retention 2.6% on 1,000+ file repositories in one vendor's tests; on SWE-bench Verified localization, embedding search nearly doubled grep-only function accuracy for an 8B open model (16.7% to 30.3%) but added 3.7 points at 32B (32.0% to 35.7%), where the model called it in a third of episodes. Graph tools helped mainly by looking up named functions and expanding one hop. Keep any code index fresh: none of eleven open coding-agent harnesses studied uses embeddings for code retrieval, and the study's authors point to embeddings going stale as code changes.
6. Add a knowledge-graph retriever only for multi-hop and synthesis questions, routed per query, and keep chunk retrieval for single-fact lookup (plain RAG led on single-hop NQ, F1 64.78 against 63.01 for the best graph method). Return source text with any triplets (F1 50.27 against 34.28 for triplets alone) and avoid global community-summary search for detail questions (null-query accuracy 19.27 against 96.01). Routing gained 1.1% over the best single path and concatenating both 6.4% on one benchmark, while graph construction took 5,560 to 7,702 s against 135 s for chunk RAG. A builder trained with RL to reorganize documents into a linked workspace beat embedding and reranker retrieval for small answering agents (0.75 against 0.44 at best), but the same builder untrained scored 0.28, below GraphRAG's 0.36.
7. Measure with a paired eval, retriever A against B, on the agent's own corpus and question sample, same model and judge, split by question type and by corpus size (pad the corpus with unrelated documents at 2, 4 and 8 times to see where grep breaks): answer accuracy, evidence localization and gold-document recall (surfaced and actually read), tool calls, tool errors and timeouts, wall time and cost per question, and index build and refresh time.

## How to measure

- **experiment** (Tier 3): paired eval, retriever A against B, on the agent's own corpus and question sample with the same model and judge, split by question type and by corpus size (pad with unrelated documents at 2, 4 and 8 times): accuracy, evidence localization and gold-document recall (surfaced and read), tool calls, tool errors and timeouts, wall time and cost per question
- **production-test** (Tier 4): when a new index is introduced (embeddings, a graph, a retriever in front of grep): A/B on live traffic with the same metrics plus index build and refresh time and answers that cite stale content
- **monitor**: per question in production traces: search-tool timeouts and errors, grep calls that return thousands of matches or fail to narrow, documents found but never read, and tool calls and wall time per question as the corpus grows

## Expected impact

- **Quality:** improves, large: grep and file reads 80.0% against 69.0% for an 8B embedding retriever at ~100K documents (Li, May 2026), and a coding agent with no retriever 88.5% against 72.5% for an embedding-search agent (Cao, Mar 2026); past 400K documents a retriever-steered workspace held 70-80 of 100 where grep alone fell to 29-32 (Lu, Jun 2026); tuned BM25 at depth 1,000 matched the published dense agent, 74.6% against 73.0% (Hsu, May 2026); Cursor +12.5% from semantic search plus grep (Nov 2025), and embedding search nearly doubled an 8B model's code localization (16.7% to 30.3%) but added 3.7 points at 32B (Bellam, Oct 2026); GraphRAG routing +1.1%, concatenating both +6.4% (Han, Feb 2025)
- **Cost:** improves, medium: grep 29% cheaper at ~100K documents (Li, May 2026); a retriever-steered workspace $34.91 against $88.13 for grep over the full corpus on 830 questions (Lu, Jun 2026); a tuned-BM25 agent $94.9 against $360.7 for the published dense agent with gpt-5, in a cache-friendly harness (Hsu, May 2026); open bash 2.9 times read plus grep per question (Li, May 2026); a graph index costs to build
- **Performance:** mixed, large: the wrong choice costs an order of magnitude in latency both ways: grep over the full corpus doubled latency from 100K to 200K documents (Li, May 2026) and averaged 3,139 s per question against 146 s with a retriever-steered workspace, with 54.7% tool errors at 800K documents (Lu, Jun 2026); graph construction took 5,560-7,702 s against 135 s for chunk RAG and KG-GraphRAG retrieval 14,434 s against 1,724 s (Han, Feb 2025)

## Evidence (summary)

- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): BrowseComp-Plus (830 q, 100,195 docs, avg 5,179 words), same Sonnet 4.6 backbone: Qwen3-Embedding-8B retrieval agent 69.0% -> DCI-Agent-CC 80.0% (+11.0), cost $1,440 -> $1,016 (-29.4%); beats best retrieval baseline GPT-5 + Qwen3-Embed-8B…
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): BrowseComp-Plus 100-q subset, GPT-5.4 nano, L4 context policy: read+grep 61% acc, 19 tool calls, $0.0355/q vs Qwen3-Embedding-8B retrieval 45%, 18 calls, $0.0498/q vs BM25 32%, 19 calls, $0.0527/q.
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): BrowseComp-Plus 100-q subset, GPT-5.4 nano: open bash 73% vs read+grep 61% (+12), but 35 vs 19 tool calls and $0.1021 vs $0.0355 per q. Lite bash usage (3,168 commands): rg | head 56.2%, rg | rg 20.6%, wc 7.8%, single rg 6.3%, ls 4.3%…
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): DCI-Agent-CC, BrowseComp-Plus 100-q subset, corpus padded with FineWeb distractors: 100K -> 200K docs: tool calls 38.5 -> 86.9, latency and cost more than doubled, accuracy -13.6 points. At 400K docs: accuracy 37.5%, 122.4 calls on…
- Li et al., "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"… (2026-05-03): DCI-Agent-Lite, GPT-5.4 nano, BrowseComp-Plus 100-q subset. L0 none: 72% acc, $0.0716/q, 2,226 s. L1 truncate 50K: 75%, fastest (1,820 s), highest retained gold coverage 31.3. L2 truncate 20K: 69% (worst), cheapest $0.0590. L3 truncate 20K…
- …and 25 more sources in `library/entries/choose-retriever.yaml`.

## Caveats

Almost all the corpus-size evidence comes from one benchmark (BrowseComp-Plus: hard multi-constraint questions over 100,195 long web pages, padded with random web pages to scale), mostly on 100-question subsets in single runs, and the two scaling studies share an author, so the crossover may sit elsewhere for paraphrase-heavy, multilingual or private corpora; short passages tolerated grep at 21M documents. BM25 against dense is confounded by the harness: the tuned-BM25 result compares a new agent with published dense runs, inside one harness dense still led slightly (82 against 80 of 100), and one study found that adding either retriever beside grep lowered accuracy on 200 questions (88.5% to 84.0% and 78.5%), though embeddings edged ahead on a 100-question rerun (90.0 against 89.0). The code evidence is a vendor's own benchmark and one study of 0.6B to 32B open models scored on localization only with a 0.6B embedder, so the gain for frontier coding models is untested outside the vendor's claim. The graph results come from two 2025 papers with small routing gains, and the long-context comparison gave the full-context model only a random 100K-token sample on corpus tasks, so it does not test reading a whole corpus in context.

## Related

- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)

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
