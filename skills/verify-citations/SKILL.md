---
name: verify-citations
description: "AOT optimization 9.a.ii (Tier 3, Tuning): Verify citations claim by claim for factual support. Placeholder. Use when an agent shows: search-call counts far above what the question needs; cited passages that do not contain the claim."
---

<!-- Generated from library/entries/verify-citations.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Verify citations claim by claim for factual support

> **Placeholder.** Generated from `library/entries/verify-citations.yaml` (entry 9.a.ii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.a.ii |
| Earlier id | T50 |
| Tier | 3 (Tuning): it changes what the agent returns |
| Categories | Verification: Checking externally; Retrieval: Ranking results |
| Change | tool / validation (add) |

## What it is

Extract claim-citation pairs deterministically, then check each: the link resolves, the source is relevant, and the source actually supports the claim. Frontier agents pass the first two over 80-94% of the time and the third only 39-77%. Cap search calls when synthesizing cited facts and cite selectively: going from 2 to 150 calls cut supported citations from 78.6% to 16.7%. Prefer primary sources over content farms.

## When it applies

- **In the code:** a research or RAG agent that returns citations with no check of what they support; no cap on search calls
- **In traces:** search-call counts far above what the question needs; cited passages that do not contain the claim
- **In eval results:** share of citations that factually support their claim

## How (outline)

1. Parse the report's claims and citations with a Markdown parser.
2. For each: fetch, check relevance, check support with a judge that sees only the claim and the passage.
3. Report the supported share; cap search calls in the agent.

## How to measure

- **experiment** (Tier 3): paired eval scored on factual citation support

## Expected impact

- **Quality:** improves, medium: factual support 39-77% before checking (May 2026)
- **Cost:** improves, medium: fewer search calls

## Evidence (summary)

- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Described as reproducible and scaling to thousands of cited pages; parser accuracy is not reported.
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Table 1, 14 models: Link Works 80.8-100%; Relevant 60.6-95.7%; Fact Check 24.4% (OSS-120B) to 76.8% (Claude Opus 4.5). Frontier Fact Check 38.9% (GPT-5 Mini) to 76.8%. Only the Fact Check stage separates models (53-point spread). Used as…
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): 12 of 14 models exceed 94% Link Works and all frontier models exceed 80% Relevant, yet frontier Fact Check is 39-77% (e.g. GPT-5.4: 100% link, 93.7% relevant, 47.7% fact).
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Max tool calls 2/10/30/50/70/100/150. GPT-5.4 Fact Check 78.6/45.9/43.0/38.0/35.5/37.2/16.7%; Claude Opus 4.6 80.0/74.4/69.2/61.2/61.7/58.7/57.9%. Link Works and Relevant stay above 92% throughout. Mean relative drop ~42%; steepest step…
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Correlational across providers: OpenAI 100% task success, most citations (GPT-5 Mini 1,272 attributions), Fact Check 39-59%; Anthropic 83-97% success, Fact Check up to 77% (Opus 4.5) and 69% (Haiku 4.5); Gemini 45-49%. No intervention on…
- …and 3 more sources in `library/entries/verify-citations.yaml`.

## Related

- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)

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
