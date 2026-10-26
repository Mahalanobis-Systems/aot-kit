---
name: external-verifier-feedback
description: "AOT optimization 9.a.i (Tier 2, Reliability): Feed back a sound external verifier's verdict; never the model's own critique. Placeholder. Use when an agent shows: errors a compiler, test or schema check would catch reaching the final answer; SQL errors and hallucinated table names; answers changed after a critique turn with no new external information; failure rows labeled tool-feedback-neglect or satisficing."
---

<!-- Generated from library/entries/external-verifier-feedback.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Feed back a sound external verifier's verdict; never the model's own critique

> **Placeholder.** Generated from `library/entries/external-verifier-feedback.yaml` (entry 9.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.a.i |
| Earlier id | T43 |
| Tier | 2 (Reliability): error recovery: catches outputs the check can reject |
| Categories | Verification: Checking externally |
| Change | workflow / reflection (add) |
| Also covers | Rich feedback loops |

## What it is

Run a check the model cannot fool on its output (compiler, tests, schema validation, execution, EXPLAIN on generated SQL, a solver) and feed the verdict back; a pass/fail verdict is enough, and resampling until the check accepts works about as well as detailed feedback. Repair generated SQL from execution errors and check for hallucinated tables; run it read-only with timeouts. Do not add a step where the model critiques or re-checks its own answer with no external signal: it lowered accuracy in every study, and a multi-step self-verification tool that helped on GAIA (+5.75%) cost 17.8 points on SimpleQA.

## When it applies

- **In the code:** no step runs the build, tests, linter, schema check or execution on the output before it is returned; a critique or reflect step where the same model reviews its own answer with no tool output or environment state in the loop
- **In traces:** errors a compiler, test or schema check would catch reaching the final answer; SQL errors and hallucinated table names; answers changed after a critique turn with no new external information; failure rows labeled tool-feedback-neglect or satisficing
- **In eval results:** failures a deterministic check would have flagged; accuracy before and after any critique step

## How (outline)

1. Identify the sound check the task admits (build, tests, schema, execution).
2. Run it on each output before returning; feed pass/fail back and let the agent retry, or resample until it passes.
3. If no sound check exists, do not substitute a model critique; use 9.b.iii or 9.b.ii instead.
4. Measure the check-failure rate and end quality.

## How to measure

- **before-after** (Tier 2): rate of outputs failing the check, same cases
- **experiment** (Tier 3): paired eval of end quality

## Expected impact

- **Quality:** improves, large: external verifier: Blocksworld 40% to 87% (2024); SQL compilation 66% to 96% (LinkedIn, 2025); model-only critique: negative in every study, e.g. GPT-3.5 75.8 to 38.1
- **Cost:** degrades, small
- **Performance:** degrades, small

## Evidence (summary)

- Stechly et al., "On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks"… (2024-02-12): Table 1, LLM+Sound Critique (best of binary / first-error / all-error feedback) vs standard prompting: Game of 24 38% vs 5%; Graph Coloring 38% vs 16%; Blocksworld 87% vs 40%; Mystery Blocksworld 10% vs 4%. Monotone improvement with more…
- Stechly et al., "On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks"… (2024-02-12): Table 1, binary / first-error / all-errors: Game of 24 36% / 38% / n.a.; Graph Coloring 38% / 37% / 34%; Blocksworld 60% / 87% / 83%; Mystery Blocksworld 10% / 8% / 6%. Blocksworld is the exception where first-error feedback helped (60 ->…
- Stechly et al., "On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks"… (2024-02-12): Table 1, sampling k=15 / k=25: Game of 24 28% / 42%; Graph Coloring 40% / 44%; Blocksworld 68% / 72%; Mystery Blocksworld 9% / 14% (standard prompting 5/16/40/4%).
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", https://arxiv.org/abs/2310.01798 (2023-10-03): Recommendation citing Self-Debug, CRITIC and trained verifiers; not tested in this paper.
- Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs"… (2024-06-03): Survey conclusion (2): prior studies "widely agree" self-correction improves responses when reliable external tools or knowledge exist; code-interpreter feedback counted as fair because it cannot easily improve the initial generation.
- …and 26 more sources in `library/entries/external-verifier-feedback.yaml`.

## Caveats

The paper's example of a gain that does not transfer across evaluation sets.

## Related

- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:verify-citations` (9.a.ii, Verify citations claim by claim for factual support)
- `aot-kit:no-self-written-tests` (9.c.i, Don't prompt agents to write their own tests; suppress it for test-heavy models)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)

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
