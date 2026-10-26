---
name: self-discover-reasoning
description: "AOT optimization 3.c.i (Tier 3, Tuning): Self-Discover reasoning structures. Placeholder. Use when an agent shows: Structure id and version per call and the task type it was discovered for; modules selected; whether the output fills every key or rephrases or skips them; tokens and latency per call against plain CoT."
---

<!-- Generated from library/entries/self-discover-reasoning.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Self-Discover reasoning structures

> **Placeholder.** Generated from `library/entries/self-discover-reasoning.yaml` (entry 3.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 3.c.i |
| Earlier id | P35 (Reasoning & Search, from the catalog cookbook) |
| Tier (proposed) | 3 (Tuning): it changes the reasoning prompt |
| Categories | Prompts: Sizing reasoning effort |
| Change | prompt / instructions |

## What it is

Self-Discover has the model compose a reasoning structure once per task type (select useful modules from 39 seed heuristics, adapt them to the task, write them as a step-by-step plan), then follow that cached structure on every instance, so each instance costs one call. On non-reasoning models it beat CoT (GPT-4 on BBH 75% to 81%, on T4D 52% to 85%) and, in a third-party run, 5-sample self-consistency at under half the cost; but it trailed CoT on Claude 3 Sonnet and on multistep arithmetic, and trailed zero-shot prompting on long-form essays. On reasoning models with thinking on, the evidence is thin and leans negative: no study runs the original method, a plan-first prompt changed mean accuracy over 10 benchmarks by at most 0.51 points, and Anthropic advises general instructions over hand-written step-by-step plans.

## When it applies

- **In the code:** A module-selection or planning step before solving, or a reasoning structure (key-value or numbered steps) per task type in the prompt. Flag a structure regenerated for every instance where one cached per task type would do, JSON structures where a natural-language plan would do, a structure stacked on a reasoning model with thinking on that was never compared against thinking alone, and no CoT or self-consistency baseline.
- **In traces:** Structure id and version per call and the task type it was discovered for; modules selected; whether the output fills every key or rephrases or skips them; tokens and latency per call against plain CoT.
- **In eval results:** Accuracy per task type against CoT, the model's own thinking at matched tokens and self-consistency at matched cost; computation-heavy split from knowledge-heavy, short answers from long-form.
- **Judge:** Before caching, check each discovered structure: would following it solve labeled examples of the task? (12.5% of MATH structures were wrong in the original study.)
- **Probes:** A mix of task types needing different reasoning.

## How (outline)

1. Start from the cheap baselines on your own labeled items: plain CoT for a non-reasoning model, the model's own thinking at a chosen effort setting for a reasoning model (1.b.i), and self-consistency at the same token budget (9.c.ii). Expect little on reasoning models with thinking on (a plan-first prompt moved mean accuracy by 0.51 points or less; an induced task strategy moved o3-mini by -1.42 to +3.20); the clearest gains were on non-reasoning and smaller models, on task types the baselines get wrong.
2. Group traffic into task types that are solved the same way, and pick a handful of unlabeled examples for each (the follow-up studies used 3 to 10).
3. Run discovery offline, once per task type, with the strongest model you have: SELECT the useful modules from the paper's 39 seed modules, ADAPT each to the task, and IMPLEMENT them as a step-by-step plan, showing one human-written plan for another task as the format example; that is 3 calls per task type. Small models wrote poor structures, while structures from a stronger model transferred (GPT-4's raised Llama2-70B on disambiguation QA from 42% with CoT to 52%). Also try letting the model write its own task-specific modules instead of picking from the 39 seeds: in a rival team's rerun (Auto-Evolve), that reached 65.4% on BBH for Claude 2.0 against 58.7% for Self-Discover and 53.7% for direct prompting.
4. Check each structure before caching it: would following it solve a few labeled examples? In the original study 12.5% of MATH structures were wrong, and an instance that follows a wrong structure fails.
5. Cache the structure as a versioned block in that task type's prompt, in the stable prefix (3.b.i; the rest of the system prompt is 3.a.iv), followed by the instance and the paper's instruction to fill in each step by reasoning about the task, not to rephrase the keys, so each instance costs one call; keep the final answer extractable (9.b.i). On Claude with thinking on, give the structure as worked examples (problem, method, answer) rather than asking for it as visible output, and test it against thinking alone. Prefer a natural-language plan to JSON (it won on every benchmark, e.g. 75.50% vs 63.50% on MATH, in a per-question study with no CoT baseline), and leave out task types where the structure lost to the baseline, such as multistep arithmetic (70 vs 92 for CoT on GPT-4) and long-form rubric-graded answers (46.32 vs 57.35 zero-shot).
6. Measure on held-out labeled items per task type: accuracy against CoT, the model's own thinking at matched tokens and self-consistency at matched cost, plus tokens, cost and p50 and p95 latency per item. Rediscover and re-test the structures when the model changes: the gain over CoT disappeared on a stronger model (Claude 3 Sonnet 67.7 vs 68.3).

## How to measure

- **experiment** (Tier 3): paired eval per task type on held-out labeled items: the cached structure against CoT, against the model's own thinking or a higher effort setting at matched tokens (1.b.i), and against self-consistency at matched cost (9.c.ii); accuracy split by task type (computation-heavy vs knowledge-heavy, short answer vs long-form), tokens, cost and p50 and p95 latency per item; repeat on every model change
- **monitor**: per call: which structure was used (task type, version, discovering model), whether the output fills every key or rephrases or skips them, answer-extraction failures, tokens and latency; accuracy by task type on a regularly labeled sample, and the share of traffic that matches no task type with a structure

## Expected impact

- **Quality:** mixed, medium: non-reasoning models: BBH 75% to 81% and T4D 52% to 85% over CoT on GPT-4 (Zhou, Feb 2024); BBH 91.0 vs 86.0 for CoT and 89.6 for self-consistency on DeepSeek-V3 (Fan, Apr 2026); below CoT on Claude 3 Sonnet, 67.7 vs 68.3 (Aswani, Oct 2024), and on GPT-4 multistep arithmetic, 70 vs 92 (Zhou, Feb 2024); below zero-shot on long-form CFA essays, 46.32 vs 57.35 (Shetty, Jun 2025); JSON plans 63.50 vs 75.50 for natural-language plans on MATH, per question (Gunasekara, Jul 2025); reasoning models: a plan-first prompt within 0.51 pp of direct prompting (Preet, May 2026), an induced task strategy -1.42 to +3.20 on o3-mini (Chen, May 2026), a hand-written structure 74.3 to 83.3 for o1 on obfuscated Mystery Blocksworld, while o1-mini fell 19.1 to 16.83 (Goh, Feb 2026)
- **Cost:** degrades, medium: 3 task-level calls per task type, then one call per instance with longer input and output (Zhou, Feb 2024); 2.7x zero-shot cost per multiple-choice task ($0.686 vs $0.255) against 6.7x for 3-sample self-consistency ($1.701) (Shetty, Jun 2025); normalized cost 5.0 vs 2.5 for CoT and 12.0 for 5-sample self-consistency on DeepSeek-V3 (Fan, Apr 2026)
- **Performance:** degrades, medium: one call per instance after offline discovery, but longer outputs: 14.9 s vs 6.0 s zero-shot per multiple-choice task and 25.27 s vs 15.18 s per essay, against 37.9 s for 3-sample self-consistency (Shetty, Jun 2025); a step-by-step prompt made reasoning models 20-80% slower (Meincke, Jun 2025)
- **Security:** none (unmeasured)
- **Governance:** none (unmeasured)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Zhou et al., "Self-Discover: Large Language Models Self-Compose Reasoning Structures", https://arxiv.org/abs/2402.03620 (2024-02-06): Table 1, CoT -> Self-Discover (plan-and-solve in brackets): BBH PaLM 2-L 60% -> 67% (61%), GPT-4 75% -> 81% (73%); T4D 40% -> 69% (42%), 52% -> 85% (53%); MATH 42% -> 50.5% (49%), 71% -> 73% (70%). The abstract's "by as much as 32%…
- Krishna Aswani, Huilin Lu, Pranav Patankar, Priya Dhalwani, Iris Tan, Jayant Ganeshmohan, Simon Lacasse, "Auto-Evolve: Enhancing Large… (2024-10-08): BBH average over 23 tasks (Table 1), direct / CoT / Self-Discover / Auto-Evolve: Claude 2.0 53.7% / 55.0% / 58.7% / 65.4%; Claude 3 Sonnet 68.6% / 68.3% / 67.7% / 71.6%; Mistral Large 61.9% / 67.3% / 72.7% / 75.4%. GPT-4, gain over direct…
- Pranam Shetty, Abhisek Upadhayaya, Parth Mitesh Shah, Srikanth Jagabathula, Shilpi Nayak, Anna Joo Fee, "Advanced Financial Reasoning at… (2025-06-29): Means across models (Tables 3-4), multiple choice: accuracy zero-shot 61.8%, Self-Discover 68.6%, CoT-SC N=3 69.1%, N=5 69.6%; cost per task $0.255, $0.686, $1.701, $2.840; latency 6.0, 14.9, 37.9, 63.1 s. Essays (LLM-graded): 57.35…
- Sachith Gunasekara, Yasiru Ratnayake (Surge Global), "Effects of structure on reasoning in instance-level Self-Discover"… (2025-07-04): Table 1, LLaMA-3.1-405B / Mistral-Large: task-level Self-Discover BBH 86.59 / 82.04, T4D 100.00 / 96.63; instance-level JSON (0-shot) BBH 85.05 / 83.14, T4D 73.23 / 76.06, MATH 63.50 / 67.50; instance-level natural language (0-shot) BBH…
- …and 6 more sources in `library/entries/self-discover-reasoning.yaml`.

## Caveats

The original's compute advantage counts inference calls on two BBH tasks, not tokens, and its authors note longer inputs and outputs; the headline 32% is one task (T4D), and on MATH it built a structure per instance. Most follow-ups are small or come from papers proposing a rival method (Auto-Evolve, SABA): the CFA study's Self-Discover is a one-prompt, per-question imitation scored on 60 multiple-choice questions with no single-sample CoT arm, the instance-level replication had no CoT baseline, and Strategy-Induct sampled 25 questions per task. The reasoning-model evidence comes mostly from neighboring prompts (CoT, plan-and-solve, induced instructions, a hand-written TMK structure) rather than Self-Discover itself, and it disagrees: no gain on multiple-choice benchmarks, a gain on one obfuscated planning task, where o1-mini nonetheless fell from 19.1% to 16.83% on the Mystery variant. Per-question strategy prompts broke a reasoning model's answer format (o3-mini on Shift Cipher, 24.64 vs 98.40 for CoT), which favors one cached strategy per task type.

## Related

- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)

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
