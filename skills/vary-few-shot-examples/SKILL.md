---
name: vary-few-shot-examples
description: "AOT optimization 3.a.ii (Tier 3, Tuning): Avoid few-shot ruts. Placeholder. Use when an agent shows: Identical or near-identical consecutive actions; repeats of a call that already failed; later outputs that copy wording or structure from earlier items; decisions that drift with position in the batch or toward the batch majority, or that differ from the same item run alone."
---

<!-- Generated from library/entries/vary-few-shot-examples.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Avoid few-shot ruts

> **Placeholder.** Generated from `library/entries/vary-few-shot-examples.yaml` (entry 3.a.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 3.a.ii |
| Earlier id | P27 (Production, from the master cookbook) |
| Tier (proposed) | 3 (Tuning): it changes what the model sees |
| Categories | Prompts: Structuring |
| Change | prompt / few_shot |

## What it is

An agent's own history, and any examples in its prompt, act as few-shot demonstrations: when the context fills with near-identical action-observation pairs (twenty similar items in a row, a retried call), the model tends to copy their surface form instead of judging the current item. The change is to break that uniformity: vary the serialization, phrasing and order of examples and of newly appended actions and observations, describe repeated or failed actions instead of replaying them verbatim, or move independent items into separate contexts (5.c.ii). The measured support is mostly for the mechanism and for diverse examples: a failed call's verbatim string accounted for 83% of small models' pull toward repeating it, batching 20 studies flipped 5.6-26.7% of one model's screening decisions against one-at-a-time runs, and diverse demonstrations beat the most similar ones by up to 23 points. No study tests Manus-style serialization noise on an agent end to end, and equivalent formats alone moved accuracy by up to 76 points, so measure the variation instead of assuming it helps.

## When it applies

- **In the code:** Every action and tool result serialized with one fixed template; harness messages with identical wording; few-shot examples that share one format and one structure or were picked as the most similar to the input; many similar items processed in one context; failed calls replayed verbatim in the history.
- **In traces:** Identical or near-identical consecutive actions; repeats of a call that already failed; later outputs that copy wording or structure from earlier items; decisions that drift with position in the batch or toward the batch majority, or that differ from the same item run alone.
- **In eval results:** Accuracy and outlier detection by position in the batch; decision flip rate against each item run alone; spread across several equivalent templates.
- **Judge:** Detect over-generalization: later outputs that carry over content or conclusions from earlier items instead of the current one.
- **Probes:** A batch of similar items with one outlier.

## How (outline)

1. Start from the baseline: run the agent with its uniform template on a batch of near-identical items (for example 20 resumes or abstracts in one context), plant an outlier late in the batch (position 15 of 20), run every item alone in a fresh context as the reference, and log accuracy and decisions by position, repeated actions and repeats of failed calls.
2. Find where uniformity enters: tool results and actions serialized with one fixed template, harness messages with identical wording, few-shot examples that share one format and one structure, many similar items in one context, and failed calls replayed verbatim.
3. Diversify the examples in the prompt: choose examples that differ in structure and cover edge cases instead of the most similar ones; if you also vary their formatting (field names, separators, layout), pin the required output format with an instruction or a schema, since examples are what the model copies the format from.
4. Vary newly appended history, deterministically: rotate two or three equivalent templates and phrasings for observations and harness messages, and the order of fields that carry no meaning, choosing the variant from the item index or a seed at append time; never rewrite earlier entries, so the context stays append-only and the prefix cache-stable (see 3.b.i).
5. Do not replay repeated or failed actions verbatim (see 7.b.ii): replace a failed call with a short runtime-generated description of what failed, or block exact repeats at the decoder (see 7.b.i); an instruction not to repeat did not reduce repeats, and deleting the failed step made them worse.
6. Where items are independent, break the repetition structurally instead: process each item or small batches in fresh contexts (5.c.ii), shuffle item order across batches, and in proposal loops reject proposals too similar to recently accepted ones; raising the temperature did not add real diversity.
7. Measure with paired runs on the same items, uniform against varied (and against per-item contexts): accuracy and outlier detection by position, decision flip rate against the single-item runs, exact-repeat rate, output-format errors, tokens and cache hit rate, over several template sets and per model, reporting the spread rather than one number.

## How to measure

- **experiment** (Tier 3): paired runs on one batch of near-identical items with an outlier planted late (position 15 of 20), each item also run alone as the reference: uniform template against varied templates, phrasing and order (and against per-item contexts); accuracy and outlier detection by position, decision flip rate against the single-item runs, exact-repeat rate of actions, output-format errors, tokens and cache hit rate; repeat over at least three template sets and report the spread, per model
- **monitor**: per batch in production: share of consecutive identical or near-identical actions, repeats of a call that already failed, decision rates by position against the first items of the batch and drift toward the batch majority; on a weekly sample, re-run items alone and track the decision flip rate

## Expected impact

- **Quality:** mixed, medium: diverse demonstrations beat the most similar ones by up to 23 points, 50.3 to 73.5, on compositional semantic parsing (Levy, Dec 2022); mixing formats across few-shot examples raised one task's worst-format accuracy from 0.139 to 0.712 but lost on three task-model pairs (Ngweta, Apr 2025); describing a failed call instead of replaying it cut exact repeats from 31% to 16% while task success went from 42% to 33%, within noise (Gumaan, Aug 2026); rejecting near-duplicate proposals and reweighting toward unused edit types raised audited faithfulness from 0.44 to 0.71 where a higher temperature added 0.02-0.03 (He, Aug 2026); equivalent formats alone moved accuracy by up to 76 points (Sclar, Oct 2023)
- **Cost:** mixed, small: replacing a verbatim call with a description cost no generated tokens (Gumaan, Aug 2026); varying entries already in the history breaks the prompt cache, which the same Manus post warns against (Ji, Jul 2025); one item per call gives up the savings that are the reason to batch (Hida, Aug 2026)
- **Performance:** none: no study reports latency; serialization changes add no generated tokens (Gumaan, Aug 2026); per-item contexts add calls that can run in parallel (see 5.c.ii)
- **Security:** none (unmeasured)
- **Governance:** none (unmeasured)
- **Brand:** mixed, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yichao 'Peak' Ji (Manus), "Context Engineering for AI Agents: Lessons from Building Manus"… (2025-07-18): Manus "introduces small amounts of structured variation in actions and observations—different serialization templates, alternate phrasing, minor noise in order or formatting." Example of drift while reviewing 20 resumes. No numbers.
- Esmail Gumaan, "Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail"… (2026-08-24): For every model "the normalised probability of repeating the failed call rises from 0.06 to 0.54", and greedy decoding repeated it token for token on 19% of items against 0% before. "The failed call's surface form accounts for 83% of the…
- Akshit Sinha, Arvindh Arun, Shashwat Goel, Steffen Staab, Jonas Geiping, "The Illusion of Diminishing Returns: Measuring Long Horizon… (2025-09-11): "as we increase the rate of injected errors into the context, accuracy at turn 100 consistently degrades further"; the authors tie this to in-context learning, since here "the model conditions on its own past behaviour, which could be…
- Gilberto Sussumu Hida, Danilo Monteiro Ribeiro, Clayton Suguio Hida, "Class Imbalance and Batch Effects in LLM-Based Screening for… (2026-08-13): For Llama, batching changed the decision on 5.6% (rsl_1) to 26.7% (rsl_4) of studies, significant by McNemar (p < 0.001) in all five reviews; for GPT-5-mini 1.3% to 14.0%, significant in four of five (mean flip rate 0.160 for Llama against…
- …and 8 more sources in `library/entries/vary-few-shot-examples.yaml`.

## Caveats

No study tests Manus-style serialization noise on an agent end to end: the measured support is for the mechanism (models copy what repeats in their context) and for diverse few-shot examples, often on small or older models (135M-1.7B for the failed-call study, Codex for the demonstration study). Variation is not free: equivalent formats moved accuracy by up to 76 points, mixing formats lost on some task-model pairs, Google advises identical formatting across examples, and a serialization fix that cut repeats did not raise task success. The effect depends on the model and task: thinking models did not self-condition on errors in their history, larger models copied a failed call less, and a batch-judging study found contrast between neighbors rather than imitation. Varying entries already in the history also breaks the append-only, cache-stable context, so vary only new entries, deterministically.

## Related

- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)

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
