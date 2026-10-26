---
name: extractable-final-answer
description: "AOT optimization 9.b.i (Tier 2, Reliability): Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit. Placeholder. Use when an agent shows: runs ending with no extractable answer; refusals returned as answers; numbers in the wrong format; runs ending at the turn cap with a correct value in context (in one image-labeling agent, 71 items returned all-unknown)."
---

<!-- Generated from library/entries/extractable-final-answer.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit

> **Placeholder.** Generated from `library/entries/extractable-final-answer.yaml` (entry 9.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.b.i |
| Earlier id | T32 |
| Tier | 2 (Reliability): graceful degradation: always return a usable answer |
| Categories | Verification: Confirming completion; Prompts: Structuring |
| Change | tool / parsing (fix) |

## What it is

State the required answer format in the prompt, and make the harness extract it robustly: strip markers, normalize numbers, detect refusals, and force a best-effort answer when the loop ends on a budget rather than returning nothing. The format reminder alone was mixed on GPQA (train up, test down); the harness side is what stops right work being lost.

## When it applies

- **In the code:** no answer-format statement; extraction that assumes a marker; no forced answer when the loop ends on a budget
- **In traces:** runs ending with no extractable answer; refusals returned as answers; numbers in the wrong format; runs ending at the turn cap with a correct value in context (in one image-labeling agent, 71 items returned all-unknown)
- **In eval results:** failures where the working was right but the submitted answer was not (instruction-grader-mismatch)

## How (outline)

1. From traces, list runs whose working was right but whose returned answer was missing, malformed or a refusal.
2. Add the format section to the prompt (3.a.iv).
3. Harden extraction and add the forced-answer path at the turn cap.
4. Measure no-answer and malformed-answer rates.

## How to measure

- **before-after** (Tier 2): no-answer, malformed-answer and refusal rates on the same cases

## Expected impact

- **Quality:** improves, medium: estimate; in an image-labeling agent we measured, a salvage turn at the limit cut all-unknown items from 71 to 1
- **Cost:** none
- **Performance:** none

## Evidence (summary)

- repo taxonomy.py role hints: Symbols such as _submit, _answer_payload, _scale_variants, _format_number, _extract_answer are common enough to get deterministic role hints.
- repo figure_01: 15/20 runs touched submission.
- paper Figure 13: Train recovered 0.54 to 0.60 in phase 2; test 0.54 (below the 0.61 baseline).
- repo figure_01: Submission-path edits in 15/20 and 18/20 runs; 2/20 on Terminal-Bench, where the verifier does not read an answer string.

## Related

- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)

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
