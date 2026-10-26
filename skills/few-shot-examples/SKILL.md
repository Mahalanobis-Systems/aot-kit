---
name: few-shot-examples
description: "AOT optimization 3.a.i (Tier 3, Tuning): Add worked examples to the prompt (few-shot), or curated example queries for data agents. Placeholder. Use when an agent shows: Outputs that miss the expected shape or metric definition; repeated queries for the same custom metric; retrieved examples with low similarity to the question, or answers that copy a retrieved pattern that does not fit."
---

<!-- Generated from library/entries/few-shot-examples.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Add worked examples to the prompt (few-shot), or curated example queries for data agents

> **Placeholder.** Generated from `library/entries/few-shot-examples.yaml` (entry 3.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 3.a.i |
| Earlier id | T11 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Prompts: Structuring |
| Change | prompt / few_shot (add) |

## What it is

Put a few solved examples of the task in the prompt (the input and the exact output wanted), or give a data agent commented example queries for its custom metrics and an index of past queries it retrieves per question. The clear gains are on knowledge the model cannot infer, mostly in data agents: one Genie space went from 54% to 77% on 13 questions, removing LinkedIn's example-query index cut correct answers from 49% to 24%, and retrieving past queries raised one text-to-SQL pipeline from 54.27% to 60.95%. On strong and reasoning models examples mostly fix the output format rather than the reasoning: Qwen2.5-72B scored 95.83% zero-shot against 95.75% with eight examples on GSM8K once the answer extractor was fixed, and five examples moved o1-preview by -2.2 to +1.2 points across six medical benchmarks. Start from a zero-shot baseline, add a few examples only where a paired eval shows a gain, and keep fixed examples in the cached prefix with retrieved ones after it.

## When it applies

- **In the code:** A prompt with no worked examples on a task with a fixed output shape; a data agent with no example queries for its custom metrics; examples kept on a reasoning or strong model with no zero-shot comparison; examples retrieved per request placed before static prompt content, so the cached prefix changes on every call.
- **In traces:** Outputs that miss the expected shape or metric definition; repeated queries for the same custom metric; retrieved examples with low similarity to the question, or answers that copy a retrieved pattern that does not fit.
- **In eval results:** Failures that cluster on custom metrics, business logic or an output format the examples would show; no paired zero-shot baseline for the examples in use.

## How (outline)

1. Start from the baseline: the same model zero-shot, with a plain instruction, an explicit output format and a robust answer extractor (9.b.i), on held-out cases. Examples often look like a gain only because they fix the format: Qwen2.5-72B went from 91.58% zero-shot to 95.75% with eight examples on GSM8K, but scored 95.83% zero-shot once the extractor read the boxed answer. On a reasoning model begin with no examples: five examples moved o1-preview by -2.2 to +1.2 points across six medical benchmarks, while a tailored prompt and ensembling helped.
2. Add examples only where failures cluster on what the instruction and schema cannot carry: a custom metric, business logic, a join path, a value convention, an exact output shape. For a data agent, write one example query per custom metric with comments that explain the logic (54% to 77% on 13 questions in one Genie space), and build an example-query index from queries in code, wikis and the query log, each with a description embedded for retrieval and refreshed as needed (removing such an index cut correct answers from 49% to 24%). With dozens of metrics, define them once in a view or semantic layer instead (7.a.i): in the same Genie space a view holding the definitions also scored 100%.
3. Make each example the full input and the full desired output, in exactly the target format: in the math study the format benefit fell as more of each example was masked, while the reasoning content was largely ignored (in most settings, replacing half of the example tokens with noise barely changed accuracy). Include worked reasoning only for small or older models, which did gain from it (LLaMA3.2-1B, LLaMA2-7B, Qwen-7B); for strong models even reasoning written by DeepSeek-R1 rarely beat zero-shot. Vary the examples' form so the model does not copy one pattern (3.a.ii).
4. Use a few examples, retrieved per question when the pool is large: on underspecified text-to-SQL, retrieving past queries from the same database raised execution accuracy from 54.27% to 60.95% (67.34% with the right ones), peaking at four examples (61.31%, against 58.36% with one), which the authors attribute to noise from over-retrieval. Retrieve broadly, then filter and rerank for precision: whole-question similarity alone reached 59.15%, retrieval precision was 35.53%, and in one failure the model copied a retrieved pattern that did not fit.
5. Keep the prefix cacheable (3.b.i): put fixed examples in the static part of the prompt and append retrieved ones after it, next to the question. In many-shot prompts the edge of similarity selection fades as examples are added, and caching a large fixed set while adding 20 retrieved examples per query matched similarity-only selection at an estimated half the cost at 50 examples and a tenth at 200. Retrieval is not always better: on a tool-selection benchmark, similarity-retrieved examples did not beat zero-shot while random ones did.
6. Keep the pool curated, as the tested setups did: final, successful queries only, filtered by execution count and certification. If the examples come from the agent's own past runs, that is episodic memory (4.c.i): verify them before reuse. Do not add examples where the problem calls for validation (one of VeRO's anti-patterns).
7. Measure with paired runs on held-out cases (never the example pool): zero-shot, fixed examples and retrieved examples, per model and again after each model change; report accuracy, output-format errors, input tokens, cache hit rate and latency (retrieval with LLM reranking took about 6 s per question in one test).

## How to measure

- **experiment** (Tier 3): paired runs on held-out cases, never the example pool: zero-shot with an explicit output format and a robust extractor, against fixed examples and against examples retrieved per query (1 to 5), per model and again after each model change; report accuracy (for data agents, sliced by questions on custom metrics or business logic), output-format errors, input tokens, cache hit rate and latency, over several runs
- **monitor**: per request: which examples were retrieved and their similarity, whether the answer followed a retrieved pattern, output-format errors, input tokens and cache hit rate; weekly: failed questions with no relevant example (gaps in the index) and examples that no longer run after schema or metric changes

## Expected impact

- **Quality:** mixed, medium: data agents asked about custom metrics or underspecified business logic: 54% to 77% on 13 questions (Databricks, Feb 2026), 49% to 24% without the example-query index (Chen, Jul 2025), 54.27% to 60.95% with retrieved past queries and 61.31% at four examples (Zhou, Aug 2026); strong models on math: 95.75% with eight examples against 95.83% zero-shot once the extractor was fixed (Cheng, Jun 2025), MATH train 0.81 to 0.83 with validation flat (VeRO, Feb 2026); o1-preview -2.2 to +1.2 points across six medical benchmarks (Nori, Nov 2024)
- **Cost:** degrades, small: more input tokens per call; examples retrieved per query change the prompt and defeat prefix caching, while caching a large fixed set and adding 20 retrieved examples cut estimated attention cost about 2x at 50 examples and 10x at 200 against similarity-only selection (Golchin, Jul 2025); few-shot o1-preview used more tokens than a tailored prompt for lower accuracy (Nori, Nov 2024); indexing a query log took about 5.2 s of LLM time per query (Zhou, Aug 2026)
- **Performance:** degrades, small: fixed examples add only input tokens; retrieving and reranking examples per question with an LLM added about 6 s per question with serial API calls (Zhou, Aug 2026)

## Evidence (summary)

- paper Figure 12: Adding few-shot maths examples: train 0.81 to 0.83, validation flat at 0.87.
- Databricks, "How to Build Production-Ready Genie Spaces and Build Trust Along the Way"… (2026-02-06): Adding example SQL queries for custom metrics such as CTR (comments in the SQL recommended) raised benchmark accuracy from 54% to 77% on 13 questions, "the largest single accuracy improvement thus far". Text instructions then reached 100%…
- Albert Chen, Manas Bundele, Gaurav Ahlawat, et al. (LinkedIn), "Text-to-SQL for Enterprise Data Analytics", https://arxiv.org/abs/2507.14372 (2025-07-18): Removing the example-query index (human-authored queries from code repos and wikis, filtered by execution count and certification) cut answers rated correct or close to correct from 49% to 24%, and table recall from 76% to 60%.
- Yunfan Zhou, Qiming Shi, Yizhou Yang, Di Weng, Yingcai Wu, "BIRD-History: A Benchmark for History-Driven Text-to-SQL with Fine-Grained… (2026-08-29): OpenSearch-SQL execution accuracy: 54.27% with no retrieval, 59.15% with its own similarity retrieval, 60.95% with the authors' retriever, 67.34% with the gold examples. DAIL-SQL rose from 40.78% to 51.33%, N-rep from 54.49% to 57.79%…
- Shahriar Golchin, Yanfei Chen, Rujun Han, Manan Gandhi, Tianli Yu, Swaroop Mishra, Mihai Surdeanu, Rishabh Agarwal, Chen-Yu Lee, Tomas… (2025-07-22): "the influence of selection criteria (e.g., similarity) on performance diminishes as the number of demonstrations increases substantially"; on TREC similarity selection barely changed past 50 examples. "Both of our selection strategies…
- …and 2 more sources in `library/entries/few-shot-examples.yaml`.

## Caveats

The large gains are from data agents asked about custom metrics or underspecified logic, on small or purpose-built sets: 13 questions in one Genie space, 133 questions scored by an LLM judge in one run at LinkedIn, and a benchmark built so that past queries are needed, run with one model. On strong instruction-tuned and reasoning models examples mostly align the format and can hurt: eight examples tied zero-shot on math for Qwen2.5-72B, few-shot prompts collapsed on LSAT and CommonsenseQA in the same study's appendix, and five examples lowered o1-preview on four of six medical benchmarks, though neither study tests a 2026 model. Retrieved examples are not reliably better than fixed ones (they did not beat zero-shot on a tool-selection benchmark, and low-precision retrieval misled the model), and the caching savings are estimated from attention complexity, not measured bills. No source here measures examples for multi-step agent tool calling, and VeRO lists adding examples where the problem calls for validation as an anti-pattern.

## Related

- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)

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
