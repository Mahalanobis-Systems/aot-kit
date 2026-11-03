---
name: verify-citations
description: "AOT optimization 9.a.ii (Tier 3, Tuning): Verify citations claim by claim for factual support. Placeholder. Use when an agent shows: search-call counts far above what the question needs; cited URLs never fetched in the run (cited from snippets only); cited passages that do not contain the claim; cited URLs that return 404 with no archive snapshot."
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

Check every citation in a research agent's report against the page it cites, and fix or drop what fails before the report goes out. It pays wherever readers rely on the citations: in one 14-model study, over 94% of frontier agents' links worked and over 80% pointed to relevant pages, yet the page supported the claim only 38.9 to 76.8% of the time; in another, a URL checker in the loop cut non-resolving links from 4.9-16.0% to under 1%, and a writer that cites from extracted source facts cut misattributed claims 2.4 to 6.2 times in three systems, at 1.2 to 9.5 times the writing-stage input tokens. Cap search calls (GPT-5.4's supported share fell from 78.6% at 2 calls to 16.7% at 150) and make the writer read what it cites: two web-search agents fetched only 2% and 19% of the pages they cited. The checks have limits: cheap judges matched frontier ones but rejected 18 to 47% of supported citations, and a binary support check passes conclusions that overstate their sources, which were at least 22% of the conclusions in each of seven systems.

## When it applies

- **In the code:** a research or RAG agent that returns citations with no check of what they support, no URL check before the answer is returned, or a writer that drafts from multi-source notes or search snippets instead of the cited documents; no cap on search calls
- **In traces:** search-call counts far above what the question needs; cited URLs never fetched in the run (cited from snippets only); cited passages that do not contain the claim; cited URLs that return 404 with no archive snapshot
- **In eval results:** share of citations whose source supports the claim, scored by a judge with known false negative and false positive rates; a holistic report score with no claim-level audit
- **Probes:** whether the support check catches unsupported citations without rejecting supported ones

## How (outline)

1. Start from the baseline: run the current agent on a fixed question set and audit its reports. Parse claim-citation pairs deterministically with a Markdown parser (numbered, footnote, inline-link and range citations; a citation at the end of a passage covers the uncited sentences before it), fetch each cited page, and score each pair on three checks: the link works, the page is relevant, the page supports the claim. In one 14-model study, 12 models had over 94% working links and every frontier model over 80% relevant pages, but support ranged from 38.9% (GPT-5 Mini) to 76.8% (Claude Opus 4.5). Do not rely on a holistic report score instead: in another study a writer change cut misattributed claims 2.4 to 6.2 times while the overall RACE score moved at most 1.8 points of 100.
2. Check links in the loop, before the answer is returned: give the agent a URL tool that sends HEAD (then GET), treats 403 as blocked rather than dead, and labels a dead URL with an archive snapshot as stale and one without as likely fabricated, and have the agent replace or drop failing citations. In one study on 435 questions this cut non-resolving citation URLs from 16.0% to 0.6% (GPT-5.1), 6.1% to 0.1% (Gemini 2.5 Pro) and 4.9% to 0.8% (Claude Sonnet 4.5) in a mean 1.56 to 4.06 correction rounds. 10.3 to 20.2% of URLs stayed unknown (bot blocking, paywalls, timeouts) and need a browser fetch or a person, and gpt-5-nano called the tool but kept re-proposing flagged URLs (7.5% still not live), so check that the model acts on the verdicts.
3. Check support with a judge that sees only the claim and the fetched page text, one decision per pair, and choose and calibrate it on a human-labeled sample of your own claim-citation pairs (the studies here used 50 to 624) rather than by price. On one 624-pair benchmark, eight judges' factual-support F1 ran from 0.649 to 0.750 with overlapping confidence intervals across a 49-fold spread in cost per decision, and GPT-5-mini, among the cheapest, had the best relevance F1 (0.908). Track false negative and false positive rates, not only F1: those judges rejected about 86% to nearly all deliberately falsified claims but also 18.3 to 47.0% of supported ones, so a strict judge understates support. Compare variants under one judge: on the same ten tasks, one audit measured 12.09 to 23.80% hallucinated claims with GPT-5.5 as judge and 45.24 to 58.72% with Gemini 3.5 Flash.
4. Act on each failure rather than only reporting the share: re-cite a claim to the retrieved source that supports it (in one audit, claims citing the wrong retrieved source were 5.9 to 24.7% of claims, against 12.1 to 27.1% that no retrieved source supported), and hedge or drop what nothing supports. For conclusions drawn across several sources, also check that the claim is no stronger or broader than the cited documents allow, which a binary support check passes: in one study at least 22% of conclusions in each of seven systems were overstated this way (22 to 35% severely for Gemini Deep Research). A no-search revision pass given the supporting and qualifying quotes a checker collected raised rubric scores by 4.4 and 12.0 points, against 0.4 and 1.1 for revising without them, with a fifth to a tenth of the tokens of the full documents.
5. Make the writer read what it cites, and cap search calls when it synthesizes cited facts. Two web-search agents fetched the full page for only 19% (GPT Luna 5.6) and 2% (Claude Sonnet 5) of the documents they cited, working mostly from search snippets; giving them the full cited documents plus instructions to match each claim's strength and scope to the evidence cut overstated conclusions from 29% to 12% and from 61% to 25%, while either change alone did much less. In one two-model ablation, GPT-5.4's supported share fell from 78.6% at 2 search calls to 45.9% at 10 and 16.7% at 150 (Claude Opus 4.6: 80.0% to 57.9%), while working links and relevance stayed above 92%. Prefer primary sources: Anthropic's early research agents chose SEO content farms over academic PDFs until source-quality heuristics were added to the prompt (unmeasured).
6. If support or attribution stays low, change how the writer cites rather than adding checks: feed it single-source units that carry their citation. One writer that extracts facts from each source, assigns them to an outline drawn from the query and drafts each section with fact-level citation ids resolved at assembly cut misattributed claims from 22.31% to 3.62%, 18.94% to 5.43% and 5.92% to 2.50% in three open deep research systems and hallucinated claims 2.6 to 4.5 times, at 1.2 to 9.5 times the writing-stage input tokens and 3.8 to 5.5 points of 100 lower RACE readability (its authors' own method). Cite selectively: providers whose models cited most had lower support, and more citations per query did not mean fewer errors per citation, though both findings compare models rather than test the change.
7. Measure with paired runs on the same questions, before and after, scored by the same calibrated judge: the share of claim-citation pairs passing each check, non-resolving, likely fabricated and unknown URLs, misattributed and unsupported claims, the share of synthesized conclusions stronger than their sources, an overall report score, and tokens, page fetches, judge calls and wall-clock per report; recheck the judge's false negative and false positive rates on a fresh labeled sample.

## How to measure

- **experiment** (Tier 3): paired runs on the same questions with and without the checks (and any writer change), scored by the same calibrated judge: the share of claim-citation pairs whose link works, whose page is relevant and whose page supports the claim; non-resolving, likely fabricated and unknown URLs; misattributed and unsupported claims; the share of synthesized conclusions stronger or broader than their sources; an overall report score; and tokens, page fetches, judge calls and wall-clock per report
- **monitor**: in production traces: per report, the share of citations failing each check, likely fabricated URLs, the share of cited documents the agent actually fetched, and search calls; recheck the judge's false negative and false positive rates on a fresh human-labeled sample of claim-citation pairs

## Expected impact

- **Quality:** improves, medium: the checks find a real gap: cited pages supported 38.9 to 76.8% of frontier agents' claims (Onweller, May 2026); fixes driven by them gained: a URL checker in the loop cut non-resolving links from 4.9-16.0% to 0.1-0.8% (Rao, Apr 2026), a writer citing from extracted source facts cut misattributed claims 2.4 to 6.2 times and hallucinated claims 2.6 to 4.5 times with overall RACE within 1.8 points (Hayashi, Aug 2026), and full cited documents plus calibration instructions cut overstated conclusions from 29% to 12% and 61% to 25% (Singha Roy, Oct 2026); no study has gated reports on the support check itself
- **Cost:** mixed, medium: each claim-citation pair costs a page fetch and a judge call per check; judge cost per decision spanned 49 times across eight judges with no accuracy edge for the costliest (Leung, Jul 2026); link self-correction took a mean 1.56 to 4.06 rounds per question (Rao, Apr 2026); a claim-first writer used 1.2 to 9.5 times the writing-stage input tokens (Hayashi, Aug 2026); revising with checker-gathered evidence used 11k and 65k tokens of context against 117k and 324k for the full documents (Singha Roy, Oct 2026); capping search calls at 2 to 10 instead of 150 cuts search calls and kept support higher (Onweller, May 2026)
- **Performance:** mixed, small: link self-correction added a mean 1.56 to 4.06 correction rounds per question, up to 8 (Rao, Apr 2026); capping search calls cuts calls (Onweller, May 2026), whose checks ran 15 evaluators concurrently; no source timed the checks

## Evidence (summary)

- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Described as reproducible and scaling to thousands of cited pages; parser accuracy is not reported.
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Table 1, 14 models: Link Works 80.8-100%; Relevant 60.6-95.7%; Fact Check 24.4% (OSS-120B) to 76.8% (Claude Opus 4.5). Frontier Fact Check 38.9% (GPT-5 Mini) to 76.8%. Only the Fact Check stage separates models (53-point spread). Used as…
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): 12 of 14 models exceed 94% Link Works and all frontier models exceed 80% Relevant, yet frontier Fact Check is 39-77% (e.g. GPT-5.4: 100% link, 93.7% relevant, 47.7% fact).
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Max tool calls 2/10/30/50/70/100/150. GPT-5.4 Fact Check 78.6/45.9/43.0/38.0/35.5/37.2/16.7%; Claude Opus 4.6 80.0/74.4/69.2/61.2/61.7/58.7/57.9%. Link Works and Relevant stay above 92% throughout. Mean drop about 42 percentage points from…
- Onweller et al., "Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents"… (2026-05-07): Correlational across providers: OpenAI 100% task success, most citations (GPT-5 Mini 1,272 attributions), Fact Check 39-59%; Anthropic 83-97% success, Fact Check up to 77% (Opus 4.5) and 69% (Haiku 4.5); Gemini 45-49%. No intervention on…
- …and 7 more sources in `library/entries/verify-citations.yaml`.

## Caveats

No study has yet gated reports on the support check itself and measured the gain: the 14-model support rates come from an evaluation with an unnamed judge whose agreement with humans is not reported, and the tested fixes act on links (one study, URL validity only), on the writer (its authors' own method, at up to 9.5 times the writing-stage input tokens and lower readability) or on revision with gathered evidence (one study, two models). The judge is a weak point: on one adversarial benchmark built by the 14-model study's team, judges rejected 18 to 47% of supported citations, so measured support rates may understate true support, and in another audit absolute hallucination rates differed 2.5 to 3.9 times between two judges on the same reports, so compare variants only under one calibrated judge. A binary support check also passes conclusions that overstate their sources, and the advice to cap search calls and cite selectively rests on one two-model ablation and on comparisons across models (within one system, citing more documents did not predict more overstatement).

## Related

- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)

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
