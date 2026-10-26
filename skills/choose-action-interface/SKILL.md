---
name: choose-action-interface
description: "AOT optimization 2.a.iii (Tier 3, Tuning): Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task. Placeholder. Use when an agent shows: bash-only runs emitting tools that do not exist; typed-tool runs re-patching the same file; code errors in routine operations (reading a file, searching); import-error or command-not-found spans at the start of runs; calculations done in the model's own text; independent commands serialized."
---

<!-- Generated from library/entries/choose-action-interface.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task

> **Placeholder.** Generated from `library/entries/choose-action-interface.yaml` (entry 2.a.iii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.a.iii |
| Earlier id | T61 |
| Tier | 3 (Tuning): it changes the agent's tools within the existing design |
| Categories | Tools: Refactoring; Models: Benchmarking workloads |
| Change | tool / api (restructure) |
| Also covers | CodeAct |

## What it is

Decide the action interface deliberately, by model and by task, and provision what it needs. The rule the evidence supports: (1) weaker models get typed tools (read, write, edit, grep, a narrow calculator); a general code interpreter made a weak agent write boilerplate and fail until it was replaced with typed functions. (2) Structured data gets a typed query tool, whatever the model: SQL scored 100% against 52.7% for bash at a seventh of the tokens, and SQL plus bash also reached 100%. (3) Strong models on shell-heavy or general office work get bash: on enterprise digital-worker tasks bash-only beat typed tools by 21.8-24.5 points with fewer tokens, and typed tools on top of bash added nothing. (4) Work that chains many calls or processes bulk data gets code execution, because intermediate results never pass through the model; calling tools from code matched or beat JSON calling for 11 of 14 models on BFCL v4, and a narrow calculator did as well as full code execution on maths. Whichever you choose: start minimal and add tools per observed failure; for code or shell, provision the packages and fixtures the agent expects, allow concurrent commands, and sandbox it (10.a.i).

## When it applies

- **In the code:** the interface in use (typed tools, code interpreter, bash), the model it serves, and whether the environment has the packages and fixtures the tasks need
- **In traces:** bash-only runs emitting tools that do not exist; typed-tool runs re-patching the same file; code errors in routine operations (reading a file, searching); import-error or command-not-found spans at the start of runs; calculations done in the model's own text; independent commands serialized
- **In eval results:** success and cost by model under each interface

## How (outline)

1. Classify the model's shell and coding ability from a probe run (typed tools against bash-only on 20 cases).
2. Pick the interface by the table in the summary; for code execution, install the packages the tasks need and set up fixtures.
3. Add tools only when a trace shows a failure a tool would have prevented.
4. Paired eval per model: success, cost, steps.

## How to measure

- **experiment** (Tier 3): paired eval per model, interface A against B: success, cost, steps

## Expected impact

- **Quality:** mixed, large: typed tools +15.0 points for a weak model; bash-only +3.6 for a strong one (Fan, Sep 2026); typed functions in place of an interpreter took GAIA from 0.07 to 0.24 (VeRO)
- **Cost:** improves, large: bash-only -53% cost for a bash-capable model; chaining tools in code 150k to 2k tokens in one example

## Evidence (summary)

- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): T4/128k, planning on. Nemotron-3 30B: typed tools +15.0 pts SWE (25.2 vs 10.2) and +10.1 TB. 66% of its bash-only TB runs end after emitting tools that don't exist (trajectory 71->15 turns). 120B: tools +1.6 SWE / +4.5 TB and shorter runs…
- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Claude Opus 4.5, 5 representative queries, old vs new: avg time 274.8s -> 77.4s ("3.5x faster"); success 4/5 -> 5/5; avg tokens ~102k -> ~61k ("37% fewer"); avg steps ~12 -> ~7 ("42% fewer"). Worst case: old "724 seconds, 100 steps, and…
- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Part of the bundled v1 -> v2 change (5 queries, Opus 4.5, numbers above). "We were constraining reasoning because we didn't trust the model to reason. With Opus 4.5, that constraint became a liability." Both code samples show instructions…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): "Mini-SWE-Agent's single-tool design reports 74%+ on SWE-Bench with essentially no tool infrastructure (self-reported)"; the paper says it is not comparable head-to-head with Codex's 69.1% (different models, runs, sandboxing).
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Rec 17 quoting [18]: "a common error we've observed is tools that merely wrap existing software functionality or API endpoints." Consolidate instead.
- …and 17 more sources in `library/entries/choose-action-interface.yaml`.

## Caveats

The paper flags this as intuitively helpful but the test gain is within noise; MATH baseline 0.87 is near the target model's ceiling.

## Related

- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)
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
