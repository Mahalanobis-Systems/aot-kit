---
name: tune-search-tool
description: "AOT optimization 8.b.i (Tier 2, Reliability): Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality. Placeholder. Use when an agent shows: many page fetches per question, or the same page fetched again; queries returning zero or irrelevant results followed by the same query, by giving up or by an answer anyway; near-identical consecutive queries; answers given without opening any result, or wrong answers whose answer text was visible in a returned snippet or page; results from the wrong product, version or date; results from dataset hosts or pages containing the eval question; failure rows labeled missed-read."
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

Make the search tool show the agent enough to choose what to open, give it a reader that keeps the pages it opens, and have the tool say plainly when it found nothing. Return a snippet and source metadata per result and five or more results, retry failed searches and reformulate thin ones (start broad, then narrow; use the corpus's own terms) rather than repeating them, expose the source's metadata as filters, and drop sources that leak the answer or are untrustworthy; expanding one question into many queries up front has not helped. In single studies, a reader that saves fetched pages to a workspace the agent can grep beat snippets alone by 8.5 to 17 points on BrowseComp across three models, a plain "no reliable results" message raised abstention on unanswerable questions from 23% to 97% for two Qwen3 models, and blocking the site where search agents found benchmark answers cut their accuracy on those questions by about 15%. The limits: Claude Sonnet 5.5 and Opus 5.5 ignored the no-result message, three commercial search APIs gave the same accuracy while solving different questions, and the effects of result count and retries are unmeasured.

## When it applies

- **In the code:** a search tool returning titles or URLs only; a fixed small result count; no page reader beside search, or a reader that injects one fixed reading of the page that cannot be queried again; a tool that always returns its top-k even when nothing matches; no retry; no filter parameters over a corpus with metadata; results passed to the model unfiltered, including from hosts of eval datasets
- **In traces:** many page fetches per question, or the same page fetched again; queries returning zero or irrelevant results followed by the same query, by giving up or by an answer anyway; near-identical consecutive queries; answers given without opening any result, or wrong answers whose answer text was visible in a returned snippet or page; results from the wrong product, version or date; results from dataset hosts or pages containing the eval question; failure rows labeled missed-read
- **In eval results:** retrieval recall below what answer accuracy needs; failures where the answer was in an unfetched result; wrong rather than unknown answers on questions the corpus cannot answer
- **Probes:** Questions whose answer-bearing documents have been removed from the index, and, for evals with web search, questions whose answers are published online.

## How (outline)

1. Start from the search tool as it is: from traces, count per question the searches, page opens, near-identical repeated queries, and searches that returned nothing useful together with what followed (the same query, a reformulation, giving up, or an answer anyway); count answers given without opening any result and wrong answers whose answer text was visible in a returned snippet or page (53 to 57 of 100 questions in one comparison of three search APIs, by string match); and measure the tokens search results take per question.
2. Return results the agent can choose from: a title, URL, source and date metadata and a snippet per result, not just titles or URLs, and enough results to choose among (VeRO's stronger agent used five or more results with retries, its weaker one three without; no study here isolates the count). Snippet size trades page opens for tokens: under the same agent, the search API with the richest snippets (a median 7,810 tokens of results per question, against 2,704 for the leanest) showed answer-bearing snippets on 30 of 100 questions against 16 and opened pages on 65% of questions against 81%, at the same accuracy; in VeRO, adding snippets raised SimpleQA training accuracy but not validation.
3. Put a page reader beside search, and keep what it fetches: a fetch tool that saves the full page to a per-question workspace and returns only its path and size, with grep and bounded line reads across every saved page, beat a snippets-only agent (BrowseComp 44.5, 52.5 and 70.5% against 27.5, 37.5 and 62.0% on three models), a visit tool returning a goal-focused summary made at fetch time (37.5, 48.0 and 64.0%) and a one-page-at-a-time browser (42.0, 50.5 and 66.0%), and it searched less than the snippets-only agent (58 to 67 searches per question against 70 to 101); confining grep to one page at a time cost 5 points on one model. If you keep a visit tool that returns one reading of the page, a summary beat a goal-focused chunk on every model. How much of a page each read returns is 2.c.i.
4. Make a failed search visible: when nothing reliable matches, return a short message instead of the usual top-k irrelevant passages, saying so and what to do next (for example "No reliable results were found for this query. The index may not contain the information needed.", then try a different query or answer unknown). In one study this raised abstention on unanswerable questions from 23% to 97% for Qwen3-8B and Qwen3-32B and from 28% to 57% for Claude Haiku 4.5 (80.7% with the "what to do next" sentence), cutting wrong answers almost one for one, while a warning placed above the usual passages barely helped. Claude Sonnet 5.5 and Opus 5.5 ignored the message and answered from memory but followed a system-prompt instruction to answer unknown without evidence (abstention +16 points), so state it in the system prompt too. The tool needs a miss detector: a score-based one held to 5% false refusals delivered only part of the gain, and every false refusal on an answerable question costs that answer.
5. Retry a search that errored (transient failures, per 2.b.i), and when a query returns little, reformulate rather than repeat it: prompt the agent to start with short, broad queries and then narrow (Anthropic's research agents defaulted to overly long, specific queries that returned few results; unmeasured), and let it write its own targeted queries in the corpus's terms (removing an agent-written schema-retrieval action cost 6.7 to 7.6 points of schema recall in one study; large schemas are 8.b.ii). Do not expand the question into many queries up front: a query planner lowered recall, and its sub-tasks used as query expansion did not raise table recall (gpt-4o).
6. Filter sources: expose the corpus's metadata (date, domain, product, version, source) as filter parameters, and drop results from untrustworthy sources or sources that leak the answer (source filtering gained 3.3% on FACTS in VeRO). In evals with web search, block hosts of the eval's own data and check retrieved text for the eval's questions: search agents found HLE, SimpleQA and GPQA items with their answers on HuggingFace for 0.99% to 4.15% of questions, and blocking HuggingFace cut accuracy on those questions by about 15%; a URL blocklist alone is not enough, since other sites also carry the questions.
7. Change one thing at a time and run paired evals on the same questions and model, scoring answer accuracy, whether an answer-bearing result was returned, opened and used, searches and page opens per question, tokens per question, and wrong rather than unknown answers on questions the corpus cannot answer; when comparing search APIs, compare solved questions one by one, since three providers at 25 to 26 of 100 solved different questions (44 of 100 solved by at least one).

## How to measure

- **experiment** (Tier 3): paired runs on the same questions and model, the current search tool against one change at a time (a snippet and metadata per result, result count, a page reader that keeps fetched pages, an explicit no-result message, retries and reformulation prompts, source filters); report answer accuracy, whether an answer-bearing result was returned, opened and used, searches and page opens per question, tokens per question, and abstention against wrong answers on questions whose documents were removed from the index; when comparing search APIs, compare solved questions one by one, not only accuracy
- **monitor**: in production traces: searches returning nothing useful and what followed (the same query, a reformulation, giving up or answering anyway); near-identical consecutive queries; answers given without opening any result; tokens of search results per question; pages fetched more than once; results from the wrong product, version or date; false refusals if the tool can refuse; in evals with web search, results from hosts of the eval's data and retrieved text that contains the eval's questions

## Expected impact

- **Quality:** mixed, medium: a reader that keeps fetched pages queryable: BrowseComp 44.5, 52.5 and 70.5% against 27.5, 37.5 and 62.0% with snippets only and 37.5, 48.0 and 64.0% with a page summary made at fetch time (Liu, Aug 2026); a no-result message cut wrong answers on unanswerable questions from 64.5% to 10.5% for three models that obeyed it, but moved Sonnet 5.5 and Opus 5.5 abstention only from 1.4% to 3.2% (Chandradevan, Oct 2026); three search APIs: 25, 25 and 26 of 100 correct (Selvam, Jul 2026); snippets: SimpleQA train +0.15 but validation -0.06; source filtering +3.3% on FACTS (VeRO, Feb 2026); up-front query expansion: no gain (Chen, Jul 2025); retries and result count unmeasured
- **Cost:** mixed, small: a page reader cut searches per BrowseComp question (70 to 101 with snippets only, 58 to 67 with a workspace reader) but adds fetch, grep and read calls (Liu, Aug 2026); richer snippets meant fewer page opens (65% of questions against 81%) for more result text (a median 7,810 against 2,704 tokens per question), with no significant difference in total tokens (54,156 to 59,627 per question) (Selvam, Jul 2026); a no-result message left searches mostly unchanged but tripled them for one model on one dataset (1.38 to 4.12 per question) (Chandradevan, Oct 2026)
- **Governance:** improves, small: in evals with web search, agents found benchmark items with their answers on HuggingFace for 0.99% to 4.15% of questions and blocking it cut accuracy on those questions by about 15%, so source filters keep scores honest; a URL blocklist alone misses other sites (Han, Aug 2025)

## Evidence (summary)

- repo figure_01 (2026-02): 9/20 runs, and almost none elsewhere; the only benchmark with a retrieval corpus.
- paper Figure 15 (2026-02): Train 0.74 to 0.89, validation 0.80 (down from 0.86 best).
- blog tricks table (Tool-Centric template) (2026-02): +3.3%.
- paper Table 10 (2026-02): Knight "Enhanced (5+ results, retry logic)" vs Pawn "Basic (3 results, no retries)".
- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07-18): Appendix A.5 negative result, gpt-4o: "the query planner lowered recall and quality metrics"; produced overly nested queries even after instructing it to minimize tasks with few-shot examples. Hypothesis: unnecessary for gpt-4o, possibly…
- …and 7 more sources in `library/entries/tune-search-tool.yaml`.

## Caveats

The reader and no-result results come from one study each: the workspace reader on a 200-question BrowseComp sample with three models, reporting the best of three runs, and the no-result message on 557 Wikipedia questions with a BM25 index, where an oracle decided when to refuse; a realistic score-based detector at a 5% false-refusal budget recovered only part of the gain, and false refusals cost answers (1% to 23% of answerable episodes for budgeted detectors). The strongest models respond differently: Claude Sonnet 5.5 and Opus 5.5 ignored a refusal in the tool result and answered from memory but followed a system-prompt instruction (+16 points of abstention), and in VeRO snippets helped on SimpleQA's training split but not validation. Result count and retries rest only on VeRO's description of a stronger agent (five or more results with retries, against three without, alongside other differences), and the one search-API comparison is 100 questions with one model and one run per provider, where equal accuracy hid different solved questions (44 of 100 solved by at least one). The contamination result is on Perplexity's Sonar agents, its URL-based detector misses leaks from other sites, and up-front query expansion was tested only on table retrieval with gpt-4o.

## Related

- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:verify-citations` (9.a.ii, Verify citations claim by claim for factual support)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)

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
