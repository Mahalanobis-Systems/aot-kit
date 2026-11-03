---
name: extractable-final-answer
description: "AOT optimization 9.b.i (Tier 2, Reliability): Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit. Placeholder. Use when an agent shows: runs ending with no extractable answer (none, an echoed placeholder, output cut off before the answer marker, a turn cap reached); refusals or explanations returned as answers; numbers in the wrong format or wrapped in markup; runs ending at the limit with a correct value in context; parse rates that differ sharply between models on the same prompt."
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

Ask for the final answer in one marked place after the reasoning, extract it with a parser you have checked, and force an answer when a run hits its limit instead of returning nothing. It pays wherever a parser or grader reads the answer: on the same questions and model, an instructed \boxed{} answer scored 93.9% where pattern-matching free text scored 20.8%, and a JSON schema with the answer before the reasoning took GPT-4o from 95.60% to 55.34% on GSM8K. Asking for a format cost open-weight models accuracy, which a second formatting call or a thinking phase mostly recovered, while three recent closed models paid little. The limits: the forced-answer evidence is one exploratory study on small models whose output hit a token limit (no outside study here tests a final-answer turn at an agent's turn cap), the format reminder alone was mixed on GPQA in VeRO, and a lenient fallback parser flatters models that ignore the format.

## When it applies

- **In the code:** no answer-format statement, or one shown only as a bracketed placeholder or an example value the model may copy; a structured answer schema with the answer field before the reasoning; extraction that assumes a marker, or falls back to any matching letter or number anywhere in the text; string matching with no number, unit or markup normalization; no forced answer when the loop or the generation ends on a budget
- **In traces:** runs ending with no extractable answer (none, an echoed placeholder, output cut off before the answer marker, a turn cap reached); refusals or explanations returned as answers; numbers in the wrong format or wrapped in markup; runs ending at the limit with a correct value in context; parse rates that differ sharply between models on the same prompt
- **In eval results:** failures where the working was right but the submitted answer was not (instruction-grader-mismatch); a gap between strict and lenient scores, or between the deterministic scorer and a symbolic or model-based equivalence check
- **Probes:** Solved cases whose answer the harness may fail to read: output cut off at the limit, answers in equivalent forms, and each candidate answer format.

## How (outline)

1. Start from a baseline that separates wrong answers from unreadable ones: score a run as is and report the parse rate beside accuracy, then list runs with no extractable answer (none at all, a refusal, an echoed placeholder, output cut off before the answer marker, a loop that ended at its turn cap) and runs whose working holds the right value while the returned answer does not. Re-score a sample with a symbolic or model-based equivalence check: a deterministic MATH-500 scorer rejected 3.3% (free text) to 10.5% (Markdown) of responses an LLM judge accepted, with 0.1% the other way, and in another study a computer-algebra grader turned roughly 28% of string-graded MATH rows from wrong to right.
2. State the format once, in the prompt's format section (3.a.iv): one marker the harness reads (\boxed{}, 'Final answer:' or a named field), placed at the end of the response, and the allowed values by name ('one of A, B, C, D') rather than a bracketed placeholder or an example value. On identical questions and model, an instructed \boxed{} answer scored 93.9% where pattern-matching the bare question's free text scored 20.8%; an example letter from another alphabet made one model answer in that alphabet (58.2%, last place) until the prompt named the letters (83.9%, 100% parse rate), and in another study a '#### <answer>' placeholder was echoed verbatim and scored as wrong.
3. Keep the reasoning ahead of the format: let the model work in free text or a thinking phase and commit to the answer at the end, and in a JSON or XML answer put the reasoning fields before the answer field (answer-first JSON took GPT-4o from 95.60% to 55.34% on GSM8K; answer-first XML left two small models at 10.98%). If a format request still costs accuracy, as it did for every open-weight model in one study, answer freely first and convert the answer to the format in a second call: that significantly improved 42 of 72 comparisons (6.8 points on average) and significantly worsened 2, while a thinking phase significantly improved 43 and worsened 11 (thinking settings are 1.b.i). Constrained decoding guarantees the shape (format compliance 55.7% to 92.2%) but not the answer (accuracy 57.3% without it, 55.7% with it, 61.5% free-form), so apply it to the final answer after the reasoning, not to the whole response.
4. Harden extraction: strip markup, normalize numbers and units, compare by value, take the last marked answer, and record refusals, empty answers and echoed placeholders as their own outcomes rather than as wrong answers. Do not let a lenient fallback fill the gaps unseen: a leaderboard that read the marker where present and any option letter otherwise scored models that ignored the format leniently and compliant ones strictly, and fixing it moved 185 of 215 published cells; keep strict and lenient scores side by side.
5. Force an answer when the loop or the generation ends on a budget: make one more call that gives the model its work so far and asks only for the answer in the stated format (for example by appending 'Therefore, my final answer is'), constrained to the valid answers where they can be listed. In one small-model study this recovered correct answers on 63.5% of no-answer rows in one cell, against 19.2% for a full revision turn, and passed its decision rule in 6 of 8 cells; constrained re-extraction made every answer parseable. Raising the limit is not the fix (sizing it is 7.b.iii): doubling a generation cap from 8,192 to 16,384 tokens cut unparsed responses only from 15.9% to 14.0%.
6. Measure on the same cases, per model, before and after: accuracy under one stated protocol, parse rate, no-answer, refusal and malformed-answer rates, strict against lenient score, and answers that flip from right to wrong when the format changes. Format defects are model-specific: the same placeholder left 828 of one model's answers on one subject unparsed (827 of them real answers in the wrong alphabet) and cost another model 17 of 60,389 responses.

## How to measure

- **before-after** (Tier 2): same cases and model, before and after: accuracy under one stated extraction protocol, parse rate, and the rates of no answer, refusal, echoed placeholder, malformed answer and answer cut off by a limit; score strictly (the stated format) and leniently (any recognizable answer) side by side, and re-score a sample with a symbolic or model-based equivalence check; when the answer format changes, run old and new formats on the same questions for each model and count answers that flip from right to wrong
- **monitor**: in production traces: parse rate and no-answer rate per model and prompt version (an outlier parse rate for one model on one prompt is a format defect, not a model result); refusals and explanations returned as answers; how often the forced-answer path runs at the limit and how often its answers are right; the share of answers read only by a fallback parser

## Expected impact

- **Quality:** improves, medium: an instructed \boxed{} answer against pattern-matched free text: 20.8% to 93.9% on one subject and model, and fixing a lenient fallback parser moved 185 of 215 leaderboard cells (Huang, Oct 2026); reasoning-first against answer-first JSON on GSM8K: 95.60% against 55.34% for GPT-4o, 80.21% against 31.01% for Llama-3.1-8B (Kumar, Oct 2026); a second formatting call significantly improved 42 of 72 open-weight comparisons, by 6.8 points on average, and a deterministic scorer rejected 3.3% to 10.5% of responses an LLM judge accepted (Lee, Apr 2026); a forced short continuation recovered correct answers on 63.5% of no-answer rows against 19.2% for a full revision, in one cell (Chen, Aug 2026); limits: the format reminder alone was mixed on GPQA, train 0.54 to 0.60 and test 0.54 against a 0.61 baseline (VeRO, Feb 2026), Claude Sonnet 4.5 scored higher with answer-first JSON on GSM8K (96.13% against 87.79%) (Kumar, Oct 2026), and three recent closed models paid little or no format tax (Lee, Apr 2026)
- **Cost:** degrades, small: stating the format and hardening extraction add nothing per run; converting the answer to the format in a second call means two inference calls instead of one (Lee, Apr 2026); the forced answer at the limit is one short call on the runs that need it (a 32-token continuation in Chen, Aug 2026)
- **Performance:** none (unmeasured): no added latency on runs that answer in the stated format; the optional second formatting call and the forced answer each add one sequential call on the runs that use them

## Evidence (summary)

- repo taxonomy.py role hints (2026-02): Symbols such as _submit, _answer_payload, _scale_variants, _format_number, _extract_answer are common enough to get deterministic role hints.
- repo figure_01 (2026-02): 15/20 runs touched submission.
- paper Figure 13 (2026-02): Train recovered 0.54 to 0.60 in phase 2; test 0.54 (below the 0.61 baseline).
- repo figure_01 (2026-02): Submission-path edits in 15/20 and 18/20 runs; 2/20 on Terminal-Bench, where the verifier does not read an answer string.
- Liang-Hsun Huang, Min-Yi Chen, Chao-Chun Chuang, Yu-Wei Liu, Che-Yu Wu, Po-Feng Lee, "OpenTWBench (Open Taiwan Benchmark): Taiwan-Domain… (2026-10-14): Pattern-matching an option letter from the free-form output of the bare question (no system prompt), against instructing the model to end with \boxed{X} and counting unparseable responses as wrong: "On the same civics subject and the same…
- …and 3 more sources in `library/entries/extractable-final-answer.yaml`.

## Caveats

Most of the evidence comes from single-call benchmarks, not agent loops: no outside study here measures a final-answer turn at an agent's turn cap, and the forced-answer result is one exploratory probe on small models (up to 9B) whose parser fallback was added after inspecting failures, failing its rule in 2 of 8 cells. Format costs depend on the model: three recent closed models paid little or no format tax while every open-weight model tested did, Claude Sonnet 4.5 scored higher with answer-first JSON on GSM8K (96.13% against 87.79%), and a thinking phase made 11 of 72 comparisons significantly worse. The largest extraction effect (20.8% to 93.9%) is one subject and one model and changes the prompt as well as the parser, and lenient fallback parsing is not a free fix: on one leaderboard it scored models that ignored the format leniently and compliant ones strictly. In VeRO the format reminder alone was mixed on GPQA (train 0.54 to 0.60, test 0.54 against a 0.61 baseline).

## Related

- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
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
