---
name: semantic-layer-routing
description: "AOT optimization 7.a.i (Tier 3, Tuning): Route metric questions through a deterministic semantic layer; fall back to text-to-SQL. Placeholder. Use when an agent shows: wrong numbers on questions whose metric the layer defines; failure rows labeled reasoning-failure on metric questions; with a layer in place, answers written in raw SQL for questions the layer covers, and layer metrics or views that no answer uses."
---

<!-- Generated from library/entries/semantic-layer-routing.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Route metric questions through a deterministic semantic layer; fall back to text-to-SQL

> **Placeholder.** Generated from `library/entries/semantic-layer-routing.yaml` (entry 7.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 7.a.i |
| Earlier id | T54 |
| Tier | 3 (Tuning): routing within a single agent |
| Categories | Orchestration: Routing; Retrieval: Querying precisely |
| Change | workflow / control_flow (add) |

## What it is

Have a data agent answer metric questions by picking metrics and dimensions that a semantic layer compiles into SQL, and write SQL itself only when the layer can't answer. On questions the layer models, this beat direct text-to-SQL in dbt's benchmark (98.2% against 90.0% for Claude Sonnet 4.6, 100% against 84.1% for GPT-5.3 Codex) and in an independent paired test on the same insurance data (all three runs right on 37 of 38 questions against 21, with one refusal and no wrong-but-executed result in 114 runs against 29 wrong runs), and more reasoning effort did not close the gap. The margin is smaller with 2026 models (text-to-SQL 78.2% to 90.9% against 80.0% to 100% for the layer in dbt's August rerun, where GPT-5.6 Luna did better writing SQL), the layer path usually cost more per query, and in one vendor test on rule-heavy questions a compiled layer lost to SQL written from tuned documentation, with the agent in its best run bypassing the layer for most answers. Serve the layer as a compiler or lookup tools, not as definitions pasted into the prompt: in two 2026 studies a pasted layer left strong agents no better or worse. The evidence is small and comes mostly from the people who built the layer or system they test.

## When it applies

- **In the code:** a data agent that writes SQL directly although a semantic or metrics layer exists
- **In traces:** wrong numbers on questions whose metric the layer defines; failure rows labeled reasoning-failure on metric questions; with a layer in place, answers written in raw SQL for questions the layer covers, and layer metrics or views that no answer uses
- **In eval results:** accuracy on metric questions split by whether the layer defines them, with wrong-but-executed answers counted apart from refusals, over several runs per question

## How (outline)

1. Start from the baseline: run your current agent writing SQL with full schema context (5.b.i) on real metric questions with checked answers, several runs per question, and record accuracy, answers that executed but were wrong, refusals, and cost and latency per question. In one paired test, direct SQL was right on all three runs for 21 of 38 questions and returned a wrong result that still executed on 29 of 114 runs. Expect raw SQL to be weakest on real warehouses: on BEAVER's private enterprise warehouses the best end-to-end method reached 11.4%, and experts rated 53% of answers from LinkedIn's production SQL assistant good.
2. Measure coverage before routing: mark which questions the layer can answer with one query. dbt's layer could not answer 3 of its 11 benchmark questions (too many entity hops) until an LLM added 3 dbt models; in Baidu's deployment a compiled query representation over generated views expressed and executed 95.3% of user queries. Close gaps in the layer first where they are cheap: on one small database, model-generated views took 29 to 116 s against 28,689 s for three analysts writing them by hand, at similar accuracy (80.42% against 78.06%). Compile first the metrics your production model fails to derive: in one independent ablation, views compiled from a data contract were right on all 176 tasks they covered, while agents writing SQL from the same definitions fell short by 39.2, 37.3, 26.1 and 5.1 points from the weakest model to the strongest.
3. On the layer path, let the model only choose: metrics, dimensions, filters and grain from the layer's catalog, or from question-specific options a lookup tool returns, while the layer resolves joins and compiles the SQL; the model writes no joins or aggregations there. Ask for a single layer query or an explicit cannot-answer (dbt's benchmark prompt asks for one semantic-layer query or CANNOT_ANSWER).
4. Make the fallback explicit and logged: on a refusal or compile error, retry once with the reason (in one study 10 of 114 runs retried and 9 then produced SQL); where the model writes the query itself, check it against the layer's definitions and abstain after a few failed repairs (with GPT-4 this raised accuracy from 54.2% to 72.55% with 8% of answers "I don't know"); then fall back to text-to-SQL with the schema in context for exploratory questions, or to a person for numbers that go into reports (Baidu sends the 4.7% of queries its pipeline fails on to experts). Label every answer with the path it took.
5. Check that the layer's definitions match what users mean, and grow the layer from the fallback log: a compiled view fixes one interpretation, and in one test a view that ranked by an average where the questions meant a sum scored 0 of 19 (11 of 19 after falling back to SQL, 19 of 19 for SQL written from documentation). Add the metrics, joins or views that recurring fallbacks and misses need, and keep test questions the layer was not built against.
6. Budget for the catalog: with every metric and dimension in the prompt, the layer path cost $0.0416 against $0.0128 per query for Claude Sonnet 4.6 in dbt's benchmark, and a Malloy layer used 2.52 times the median prompt tokens of SQL with documentation. Return only the options or views relevant to the question through lookup tools, and keep the fixed part of the prompt cacheable (3.b.i). Don't paste the whole layer as text: a static layer in the prompt lowered GPT-5.6-sol by 2.3 and Claude Sonnet 5 by 11.9 points on DDR-Bench while the same knowledge served through tools gained, and in a seven-model study strong agents given a descriptive layer stopped checking the data (68% to 31% on those runs) and cost 1.1 to 1.9 times as much.
7. Measure with paired runs on the same questions, with your production model and a cheaper one (in dbt's August runs GPT-5.6 Luna scored 87.3% to 90.9% with SQL against 80.0% to 87.3% through the layer): accuracy per path, wrong-but-executed answers against refusals, the share of answers that bypassed or fell back from the layer, run-to-run spread, and cost and latency per question.

## How to measure

- **experiment** (Tier 3): paired runs on the same metric questions with checked answers, several runs each, with the production model and a cheaper one: text-to-SQL with full schema context, the layer path alone, and layer first with fallback; report accuracy per path, wrong-but-executed answers against refusals, the share of answers that fell back or bypassed the layer, run-to-run spread, and cost and latency per question
- **monitor**: in production: the share of answers by path (layer, SQL fallback, person), refusals and compile errors by reason, questions that fall back repeatedly (candidates to add to the layer), layer metrics and views no answer uses, and tokens and latency per query by path

## Expected impact

- **Quality:** improves, large: on questions the layer models: 98.2% against 90.0% (Claude Sonnet 4.6) and 100% against 84.1% (GPT-5.3 Codex), 11 questions x 20 runs (dbt, Apr 2026); all three runs right on 37 of 38 questions against 21, with 0 of 114 runs wrong but executed against 29 (Ai, Aug 2026); 71.4% against 62.8% on BIRD-dev with a compiled query representation (Lian, Jun 2026); narrower with 2026 models, 80.0% to 100% against 78.2% to 90.9%, and lower than SQL at every effort for GPT-5.6 Luna (dbt, Aug 2026); 70.4% against 99.8% when one model answered rule-heavy questions through a model-authored Malloy layer instead of SQL with documentation tuned on the same benchmark (Matson, Aug 2026); on DABStep, views compiled from a data contract were right on all 176 tasks they covered, where agents writing SQL from the same definitions fell 5.1 to 39.2 points short, the gap shrinking with model strength (Ye, Sep 2026); a layer pasted into the prompt as description lowered or left unchanged accuracy for agents that already inspect the data (Sourati, Oct 2026)
- **Cost:** degrades, medium: per query, $0.0416 against $0.0128 (Claude Sonnet 4.6) and $0.0172 against $0.0068 (GPT-5.3 Codex) with the whole metric catalog in the prompt (dbt, Aug 2026); 2.52 times the median prompt tokens and $11.81 against $8.58 for a run of 419 questions through a Malloy layer (Matson, Aug 2026); 6,112,623 against 5,185,149 prompt tokens on BIRD-dev (Lian, Jun 2026); building the layer is extra: three analysts took 28,689 s to write views for one small database, against 29 to 116 s for a model (Lian, Jun 2026); a descriptive layer in every prompt cut tool calls 22 to 30% but raised cost 1.1 to 1.9 times (Sourati, Oct 2026)
- **Performance:** mixed, small: mean latency per query 2.22 s against 2.63 s (Claude Sonnet 4.6), 1.85 s against 2.74 s (GPT-5.3 Codex) and 3.80 s against 9.88 s (GPT-5.6 Sol, high), but 9.05 s against 5.77 s for GPT-5.6 Luna (medium) (dbt, Aug 2026); 8.91 s against 9.43 s per question (Lian, Jun 2026); the Malloy layer was slower, not quantified (Matson, Aug 2026)
- **Governance:** improves, medium: for a fixed plan and layer the compiled SQL is the same every time, so a metric is computed one way for every user, and the planner cannot name a table, join or SQL fragment (Ai, Aug 2026); on the questions it could answer, the layer path scored the same on all 20 runs for three models, where text-to-SQL for two GPT models varied by 12.5 points between best and worst run, though on the modeled schema GPT-5.2 still varied by 18.2 points through the layer (dbt, Aug 2026); the benefit covers only answers that go through the layer: the best Malloy run answered 56.6% of questions in raw SQL (Matson, Aug 2026)

## Evidence (summary)

- Jason Ganz, Benoit Perigaud (dbt Labs), "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update"… (2026-04-07): On questions the Semantic Layer can reach (not too many entity hops), 11-question ACME set x 20 runs: SL 100.0% for both Sonnet 4.6 and GPT-5.3 Codex vs text-to-SQL 62.5% (Sonnet 4.6) and 51.2% (GPT-5.3 Codex) on raw tables; 2023 GPT-4 was…
- Jason Ganz, Benoit Perigaud (dbt Labs), "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update"… (2026-04-07): Recommendation derived from the benchmark above; the routing policy itself was not evaluated: "check if the Semantic Layer can answer first. If not, check if a minor modeling change would close the gap. Otherwise, fall back to text-to-SQL…
- Jason Ganz, Benoit Perigaud (dbt Labs), "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update"… (2026-04-07): Sweep on SL-answerable questions (Opus 4.6, Sonnet 4.6, GPT-5.3 Codex, GPT-5.2; Anthropic low..max, OpenAI none..xhigh): most configurations hit 95-100% SL accuracy regardless of effort; Sonnet 4.6 100.0% at low/medium/max vs Opus 4.6…
- Michael Rumiantsau, Ivan Fokeev (Cube), "Semantic Layers for Reliable LLM-Powered Data Analytics: A Paired Benchmark of Accuracy and… (2026-04-28): Pairwise McNemar, n=99: within the with-document cluster all p >= 0.79 (67.7-68.7%); within the DDL-only cluster all p >= 0.42 (45.5-50.5%); all nine cross-cluster comparisons p < 0.01. Sonnet 4.6 plus the document used ~28% fewer input…
- Jacob Matson, Alex Monahan (MotherDuck), "AI Writes the Semantic Layer", https://motherduck.com/blog/AI-writes-the-semantic-layer/ (2026-08-20): Post: the Malloy layer "consumed 2.5x more tokens, was less accurate (95% vs. 100%), and slower"; "The ability to compile and validate Malloy improved accuracy substantially"; "The semantic layer did not provide the expected retrieval…
- …and 11 more sources in `library/entries/semantic-layer-routing.yaml`.

## Caveats

The case for the layer path rests on small question sets from one insurance dataset (dbt's 11 questions, a vendor benchmark; an independent author's 38, whose compiler was built while inspecting those questions and whose layer arm also got semantics the SQL arm lacked) and on systems evaluated by their builders, with Baidu's ablation also swapping the model. The routing policy itself (layer first, SQL as fallback) is still not tested against either path alone; the closest numbers are Baidu's 95.3% of production queries handled by its compiled representation, with the rest sent to experts, and a vendor test in which the agent took the SQL route for 56.6% of answers. Against it: in dbt's August 2026 rerun the margin narrowed and GPT-5.6 Luna did better with SQL, and on DABStep's fee-rule questions a model-authored Malloy layer lost to SQL written from documentation by 29.4 points with the model fixed, though that documentation had been tuned on the same benchmark. Cube's paired study, often cited for semantic layers, tested a document in the prompt rather than a layer that compiles queries (see 5.b.i). Independent 2026 work splits the effect: the semantic content does most of the work (Ye, on DABStep with one run per model, found it lifted hard-task accuracy by 34 to 46 points) and compiling it adds most for weaker models; layers given as descriptions in the prompt helped agents that give up early but made thorough agents stop checking the data (Sourati, seven models, 1,514 tasks). The ontology results that first made the case (data.world, 16.7% against 54.2% with GPT-4) gave the SQL arm no business context.

## Related

- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)

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
