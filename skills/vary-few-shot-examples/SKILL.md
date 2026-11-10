---
name: vary-few-shot-examples
description: "AOT optimization 3.a.ii (Tier 3, Tuning): Avoid few-shot ruts. Placeholder. Use when an agent shows: Identical or near-identical consecutive actions; repeats of a call that already failed; later outputs that copy wording or structure from earlier items; decisions that drift with position in the batch or toward the batch majority, or that differ from the same item run alone or in another random batch; few strategy switches after a run of unproductive steps."
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

Keep the model from copying its own context: when it fills with near-identical steps or items, vary how new entries are written, label or describe repeats instead of replaying them, and give independent items their own context. An agent's own history and its prompt examples act as few-shot demonstrations: in one study agents attended more to their own earlier responses as context grew, and periodically clearing old rounds beat keeping the full history on eight agent tasks (68.9% against 54.4% for Qwen3-8B, 71.1% against 64.6% for GPT-4o-mini). Separating items pays most when many similar ones would share a context: grading 25 per prompt changed 11-22% of decisions between random batches, and a majority vote over nine orders of each batch still left 52-60% of those flips; for prompt examples, diverse demonstrations beat the most similar ones by up to 23 points. Changes to how history is written help only a little on current agents and have limits: labeling each observation as the outcome of the action before it raised success from 46.39% to 48.25% and cut repeats from 36.91% to 32.23% across five models, keeping only the last three steps cost the same models 10.4 points, seven current search agents (including Opus 5 and GPT-5.6 Sol) still switched strategy 3.6-17.4 points less after a dead-end history than after a neutral one of the same length, and no study tests Manus-style serialization noise end to end, so measure the variation instead of assuming it helps.

## When it applies

- **In the code:** Every action and tool result serialized with one fixed template; harness messages with identical wording; few-shot examples that share one format and one structure or were picked as the most similar to the input; many similar items processed in one context; failed calls replayed verbatim in the history.
- **In traces:** Identical or near-identical consecutive actions; repeats of a call that already failed; later outputs that copy wording or structure from earlier items; decisions that drift with position in the batch or toward the batch majority, or that differ from the same item run alone or in another random batch; few strategy switches after a run of unproductive steps.
- **In eval results:** Accuracy and outlier detection by position in the batch; decision flip rate against each item run alone and between two random batch arrangements, next to a renamed-keys baseline (accuracy can hold while decisions flip); spread across several equivalent templates.
- **Judge:** Detect over-generalization: later outputs that carry over content or conclusions from earlier items instead of the current one.
- **Probes:** A batch of similar items with one outlier; a history of repeated unproductive steps.

## How (outline)

1. Start from the baseline: run the agent with its uniform template on a batch of near-identical items (for example 20 resumes or abstracts in one context), plant an outlier late in the batch (position 15 of 20), run every item alone in a fresh context as the reference, and log accuracy and decisions by position, repeated actions and repeats of failed calls; for batched grading, also run the same items in a second random arrangement and with renamed item keys, since accuracy can hold (AUROC moved -0.033 to +0.010) while 11-22% of decisions change with the batch.
2. Find where uniformity enters: tool results and actions serialized with one fixed template, harness messages with identical wording, few-shot examples that share one format and one structure, many similar items in one context, failed calls replayed verbatim, and long runs of unproductive steps that all follow one strategy.
3. Diversify the examples in the prompt: choose examples that differ in structure and cover edge cases instead of the most similar ones; if you also vary their formatting (field names, separators, layout), pin the required output format with an instruction or a schema, since examples are what the model copies the format from.
4. Vary and label newly appended history, deterministically: rotate two or three equivalent templates and phrasings for observations and harness messages, and the order of fields that carry no meaning, choosing the variant from the item index or a seed at append time; label each observation as the outcome of the action that produced it ("Outcome of <action>: ..."), which raised success from 46.39% to 48.25% and cut third repeats from 36.91% to 32.23% across five current models; never rewrite or reorder earlier entries (shuffling past actions cost 2.55 points), so the context stays append-only and the prefix cache-stable (see 3.b.i).
5. Do not replay repeated or failed actions verbatim (see 7.b.ii): replace a failed call with a short runtime-generated description of what failed, or block exact repeats at the decoder (see 7.b.i); on small models an instruction not to repeat did not reduce repeats and deleting the failed step made them worse, while on five current models a short caution that earlier steps may be wrong, incomplete or stale and that "Repetition is not evidence of correctness" raised success from 46.39% to 48.60%. Do not have the agent write its own lessons into the history as the fix: those notes cut repeats the most (to 21.38%) but lowered success (45.01%).
6. Where items are independent, break the repetition structurally: give each ambiguous item its own context, with all shared instructions first so they are served from the prompt cache (see 5.c.ii); shuffling is not a substitute, since a majority vote over nine orders of a batch left 52-60% of the flips and batches of five still differed from single-item grading on 9-16% of decisions; if you must batch, shuffle items across batches and report agreement with single-item runs. In long sessions on tasks whose state is in the current observation, try clearing old rounds periodically (for example back to the last round once the history reaches 12 rounds) instead of keeping all of it or sliding a window, which cannot reuse the cache, and compare it with full history first: on ALFWorld, ScienceWorld, WebShop and AppWorld, keeping only the last three steps cost five current models 10.4 points (see 5.a.i). In proposal loops, reject proposals too similar to recently accepted ones; raising the temperature did not add real diversity.
7. Measure with paired runs on the same items, uniform against varied and labeled history (and against per-item contexts): accuracy and outlier detection by position, decision flip rate against the single-item runs and between two random batch arrangements next to a renamed-keys baseline, exact-repeat rate, strategy switches after a planted run of unproductive steps against a neutral history of the same length, task success, output-format errors, tokens and cache hit rate, over several template sets and per model, reporting the spread rather than one number.

## How to measure

- **experiment** (Tier 3): paired runs on one batch of near-identical items with an outlier planted late (position 15 of 20), each item also run alone as the reference and the batch also run in a second random arrangement with renamed item keys as the noise baseline: uniform template against varied templates, phrasing and order, against outcome-labeled history, and against per-item contexts; accuracy and outlier detection by position, decision flip rate against the single-item runs and between arrangements, exact-repeat rate of actions, task success, output-format errors, tokens and cache hit rate; for agents, also prefill a run of unproductive steps in one strategy and compare strategy switching against a neutral history of the same shape and length; repeat over at least three template sets and report the spread, per model
- **monitor**: per batch in production: share of consecutive identical or near-identical actions, repeats of a call that already failed, strategy switches after unproductive steps, decision rates by position against the first items of the batch and drift toward the batch majority; on a weekly sample, re-run items alone and in a second random batch and track the decision flip rate

## Expected impact

- **Quality:** mixed, medium: diverse demonstrations beat the most similar ones by up to 23 points, 50.3 to 73.5 (Levy, Dec 2022); mixing formats across few-shot examples raised one task's worst-format accuracy from 0.139 to 0.712 but lost on three task-model pairs (Ngweta, Apr 2025); clearing old rounds periodically beat the full history by 6.5-14.5 points on eight agent tasks (Wan, Feb 2026), but keeping only the last three steps cost five current models 10.4 points, labeling observations as action outcomes raised success from 46.39% to 48.25%, and self-written lesson notes cut repeats to 21.38% while success fell to 45.01% (Liu, Oct 2026); describing a failed call instead of replaying it cut exact repeats from 31% to 16% while task success went from 42% to 33%, within noise (Gumaan, Aug 2026); one item per prompt avoids the 11-22% of decisions that changed with the batch, of which a vote over nine orders left 52-60% (Xie, Oct 2026); rejecting near-duplicate proposals and reweighting toward unused edit types raised audited faithfulness from 0.44 to 0.71 where a higher temperature added 0.02-0.03 (He, Aug 2026); equivalent formats alone moved accuracy by up to 76 points (Sclar, Oct 2023)
- **Cost:** mixed, small: replacing a verbatim call with a description cost no generated tokens (Gumaan, Aug 2026); varying entries already in the history breaks the prompt cache, which the same Manus post warns against (Ji, Jul 2025); one item per call gives up the savings that are the reason to batch (Hida, Aug 2026), but with the shared instructions first and cache reads billed at 0.1 of the input price or less it adds at most that fraction of the shared prefix per item over a cached batch, while voting over three to nine orders of a batch costs three to nine times as much (Xie, Oct 2026); clearing old rounds keeps a cacheable prefix within each cycle, unlike a sliding window (Wan, Feb 2026)
- **Performance:** mixed, small: clearing old rounds periodically ran prefill 2-7x faster than a sliding window, which cannot reuse the cache (Wan, Feb 2026); serialization changes add no generated tokens (Gumaan, Aug 2026); voting over orders multiplies calls three to nine times (Xie, Oct 2026); per-item contexts add calls that can run in parallel (see 5.c.ii)
- **Security:** none (unmeasured)
- **Governance:** improves, small: a verdict made in its own context depends only on its item and can be reproduced: in batches of 25, 11-22% of moderation and grading decisions changed with which items shared the prompt, and one model flagged 58% of comments targeting a race when graded alone against 35% in batches (point estimates; Xie, Oct 2026); batching changed 5.6-26.7% of one model's screening decisions for systematic reviews (Hida, Aug 2026)
- **Brand:** mixed, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yichao 'Peak' Ji (Manus), "Context Engineering for AI Agents: Lessons from Building Manus"… (2025-07-18): Manus "introduces small amounts of structured variation in actions and observations—different serialization templates, alternate phrasing, minor noise in order or formatting." Example of drift while reviewing 20 resumes. No numbers.
- Esmail Gumaan, "Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail"… (2026-08-24): For every model "the normalised probability of repeating the failed call rises from 0.06 to 0.54", and greedy decoding repeated it token for token on 19% of items against 0% before. "The failed call's surface form accounts for 83% of the…
- Akshit Sinha, Arvindh Arun, Shashwat Goel, Steffen Staab, Jonas Geiping, "The Illusion of Diminishing Returns: Measuring Long Horizon… (2025-09-11): "as we increase the rate of injected errors into the context, accuracy at turn 100 consistently degrades further"; the authors tie this to in-context learning, since here "the model conditions on its own past behaviour, which could be…
- Gilberto Sussumu Hida, Danilo Monteiro Ribeiro, Clayton Suguio Hida, "Class Imbalance and Batch Effects in LLM-Based Screening for… (2026-08-13): For Llama, batching changed the decision on 5.6% (rsl_1) to 26.7% (rsl_4) of studies, significant by McNemar (p < 0.001) in all five reviews; for GPT-5-mini 1.3% to 14.0%, significant in four of five (mean flip rate 0.160 for Llama against…
- …and 12 more sources in `library/entries/vary-few-shot-examples.yaml`.

## Caveats

No study tests Manus-style serialization noise on an agent end to end: the history changes tested on current agents moved success by about two points (outcome labels 46.39% to 48.25%, a caution reminder 48.60%, one run each), cutting repeats did not reliably raise success (self-written lesson notes, a description of the failed call), and clearing old history helped 8B models and GPT-4o-mini on mostly text games and puzzles, with settings tuned per method, while keeping only the last three steps cost five current models 10.4 points. Stronger models are less affected but not immune: GPT-5.6-Sol repeated a twice-repeated action 8.70% of the time (46 histories) against 51.36% for Qwen3-8B, thinking models did not self-condition on errors in their history, larger models copied a failed call less, and seven current search agents including Opus 5 still switched strategy 3.6-17.4 points less after a dead-end history; the batch-grading study used open-weight models up to 32B, and on easy items batching changed only 2.9-3.9% of decisions. Variation is not free: equivalent formats moved accuracy by up to 76 points, mixing formats lost on some task-model pairs, Google advises identical formatting across examples, a batch-judging study found contrast between neighbors rather than imitation, and varying entries already in the history breaks the append-only, cache-stable context, so vary only new entries, deterministically.

## Related

- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
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
