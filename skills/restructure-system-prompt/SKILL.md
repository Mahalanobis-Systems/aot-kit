---
name: restructure-system-prompt
description: "AOT optimization 3.a.iv (Tier 3, Tuning): Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need. Placeholder. Use when an agent shows: failure rows labeled instruction-following-failure or instruction-grader-mismatch where the requirement was never in the prompt; prompt tokens the largest share of input per step; context-overflow outcomes."
---

<!-- Generated from library/entries/restructure-system-prompt.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need

> **Placeholder.** Generated from `library/entries/restructure-system-prompt.yaml` (entry 3.a.iv). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 3.a.iv |
| Earlier id | T04 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Prompts: Structuring |
| Change | prompt / system_prompt (restructure) |
| Also covers | System prompt altitude and sectioned structure |

## What it is

Rewrite the system prompt so that each requirement the task has (constraints, the answer format, the completion check, how to work efficiently, the domain procedure) is stated once, up front, in a named section, and remove instructions the model does not need. Adding structure and removing bulk are the same edit seen from two sides: what stays is what the eval shows the model needs. A domain procedure section is worth adding only when failures cluster on a step an expert would take; write it from those failures, from a domain expert, or by searching prompt variants against the eval (GEPA).

## When it applies

- **In the code:** system prompt with no named sections; requirements repeated, contradictory, or absent (no answer format, no completion criteria); prompt plus tool descriptions over about a quarter of the context window
- **In traces:** failure rows labeled instruction-following-failure or instruction-grader-mismatch where the requirement was never in the prompt; prompt tokens the largest share of input per step; context-overflow outcomes
- **In eval results:** an ablation that removes a section and shows no loss (cut it), or failures that cluster on one step of the task procedure (add it)

## How (outline)

1. List the requirements the task actually has, from the task spec and from failures.
2. Put each in one named section; put the answer format and completion check in their own sections.
3. Cut everything else, and shorten tool descriptions and checklists with it (the TerminalBench run cut the prompt from 7 lines to 3).
4. Add a domain procedure only if failures cluster on a step; derive it from those failures or an expert, or generate and test variants with GEPA.
5. Run the paired eval on development and held-out cases; keep only sections that earn their place.

## How to measure

- **experiment** (Tier 3): paired eval, old against restructured prompt, checked on held-out cases; count context-overflow failures too

## Expected impact

- **Quality:** mixed, small: adds: MAST +4.7 to +5.0 points on GSM-Plus (2025), VeRO MATH validation +0.10 with train -0.07; cuts: TerminalBench +6.8 points where the prompt crowded out context, GPQA train -0.04 where the prompt carried procedure
- **Cost:** improves, small: fewer prompt tokens
- **Performance:** improves, small

## Evidence (summary)

- paper §A.4: 8 lines to 23 lines in Filesystem-B=178. Net-zero pass rate (6 new passes, 6 regressions) although the run had the largest crash reduction (46.1% to 30.3%).
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", https://arxiv.org/abs/2310.01798 (2023-10-03): Table 8, CommonGen-Hard concept coverage, gpt-3.5-turbo-0613: Madaan et al. reported standard 44.0 -> self-correct 67.0 (7 calls); replication 53.0 -> 61.1; adding "Write a reasonable paragraph that includes *ALL* of the above concepts"…
- Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs"… (2024-06-03): Self-Refine used wrong few-shot labels or mismatched instructions only for initial generation (Tables 9-10); detoxification studies often do not ask for harmless output initially.
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", https://arxiv.org/abs/2503.13657 (2025-03-17): Table 5, GSM-Plus (200 sampled problems, 6 repetitions): GPT-4 84.75±1.94 -> 89.75±1.44; GPT-4o 84.25±1.86 -> 89.00±1.38 (Wilcoxon p=0.03 vs baseline for both).
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", https://arxiv.org/abs/2503.13657 (2025-03-17): Proposed tactic (App. L.2 is the example; measured forms are the ChatDev/AG2 entries above). Such tactics "often prove inconsistent".
- …and 6 more sources in `library/entries/restructure-system-prompt.yaml`.

## Caveats

Intermediate 20-task subset showed 45% and misled the optimizer; full evaluation regressed previously-passing tasks. 12 new passes against 6 regressions; the same run left 11 AttributeError crashes in place. Helps when the prompt was crowding out task context; hurts on reasoning tasks where the prompt carried procedure.

## Related

- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)

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
