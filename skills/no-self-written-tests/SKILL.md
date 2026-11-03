---
name: no-self-written-tests
description: "AOT optimization 9.c.i (Tier 3, Tuning): Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests. Placeholder. Use when an agent shows: test files written with print statements and no assertions; test writing and running over about 20% of tokens; passing checks that also pass when replayed on the unpatched code; runs that submit right after their own new test passes."
---

<!-- Generated from library/entries/no-self-written-tests.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests

> **Placeholder.** Generated from `library/entries/no-self-written-tests.yaml` (entry 9.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.c.i |
| Earlier id | T51 |
| Tier | 3 (Tuning): it changes what the agent does, so quality must be checked |
| Categories | Verification: Sizing verification |
| Change | prompt / instructions (remove) |

## What it is

Telling a coding agent to write its own tests mostly buys cost, not fixes, so drop the instruction and tell test-heavy models not to. In one prompt study on SWE-bench Verified, asking GPT-5.2 for tests added 19.8% output tokens and resolved the same 359 of 500 tasks, and telling two test-heavy models not to write tests cut input tokens 33 to 49% for a non-significant loss of 1.8 to 2.6 points. The checks agents run for themselves are weak: in another study 46.0% of the passing checks one agent ran also passed on the unpatched code. Keep a test the patch must ship with. A test written before the fix, shown to fail and hardened against wrong fixes is a different change, with its own gains and costs.

## When it applies

- **In the code:** a prompt or scaffold default (such as a reproduce-the-issue step) that tells the agent to write tests or scripts as a self-check
- **In traces:** test files written with print statements and no assertions; test writing and running over about 20% of tokens; passing checks that also pass when replayed on the unpatched code; runs that submit right after their own new test passes
- **In eval results:** resolve rate unchanged between runs with and without agent tests

## How (outline)

1. Start from the current agent's traces as the baseline: measure the share of API calls and tokens spent writing tests and, separately, running them; whether new test files hold assertions or only print values; and, for each check that passed after the agent's first edit, whether it also passes when replayed on the unpatched code. In one study of GPT-5.6-sol on 110 tasks, 46.0% of replayable passing checks also passed on the unpatched code, and 23.8% of runs submitted with no other kind of passing evidence.
2. Remove instructions that ask for tests or reproduction scripts, including testing cues in the scaffold's default prompt.
3. For models that write tests in most tasks (four of six models in one study did so in 83.0% to 98.6% of tasks), add an instruction not to write new test files or scripts: on SWE-bench Verified this cut input tokens 49.0% and 32.9% and API calls 35.4% and 24.5% for Kimi K2 Thinking and DeepSeek v3.2 Reasoner, for a non-significant loss of 2.6 and 1.8 points. Don't add a test request to a model that rarely writes tests: GPT-5.2 then wrote tests on 322 more of 500 tasks, used 19.8% more output tokens and resolved the same 359.
4. Keep a test where it is part of the deliverable rather than a self-check: if reviewers expect a fix to ship with a fail-to-pass test, ask for it in the patch. Code owners reviewing Google's AI-generated fixes strongly preferred that, and asking Gemini 2.5 Pro for a fix plus a reproduction test gave plausible fixes for a similar number of bugs as asking for the fix alone.
5. Measure with paired runs on the same tasks, with and without the instruction, and several runs per arm, because single runs move many tasks both ways (83.2% of tasks kept their outcome in one study while net changes were at most 13 of 500): resolve rate with an exact McNemar test, input and output tokens, API calls and wall-clock per task.

## How to measure

- **experiment** (Tier 3): paired runs on the same tasks with and without the test instruction, several runs per arm: resolve rate with an exact McNemar test, input and output tokens, API calls and wall-clock per task
- **monitor**: in production traces: the share of tokens and API calls spent writing and running tests, logged separately; new test files with prints and no assertions; the share of passing checks that also pass when replayed on the unpatched code; runs that submit right after their own new test passes

## Expected impact

- **Quality:** none, small: prompting for or against agent tests changed resolve rate by 0 to 2.6 points on SWE-bench Verified, none significant (Chen, Feb 2026)
- **Cost:** improves, medium: told not to write tests, two test-heavy models used 32.9% and 49.0% fewer input tokens and 14.0% and 43.1% fewer output tokens; asked to, GPT-5.2 used 9.0% more input and 19.8% more output tokens (Chen, Feb 2026)
- **Performance:** improves, small: API calls fell 24.5% and 35.4% when test-heavy models were told not to write tests and rose 5.5% when GPT-5.2 was asked to (Chen, Feb 2026); no study timed the change itself
- **Governance:** degrades, small: if suppression also drops the test a fix should ship with: code owners reviewing Google's AI-generated fixes strongly preferred fixes with a fail-to-pass reproduction test, and 39% of human-written null-pointer fixes there changed a test (Cheng, Jan 2026); keep such tests in the patch

## Evidence (summary)

- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-02-08): Encourage prompt: GPT-5.2 flips No test -> Has test on 322/500 tasks (64.4%) with net 0 change in resolved (359 -> 359, McNemar p=1.000) while API calls +5.5%, input tokens +9.0%, output tokens +19.8% (all Wilcoxon p<0.001). Gemini 3 Pro…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-02-08): Discourage prompt, SWE-bench Verified: Kimi K2 Thinking resolved 317 -> 304 (-2.6pp, McNemar p=0.228), API calls -35.4%, input tokens -49.0%, output tokens -43.1%; DeepSeek v3.2 Reasoner resolved 300 -> 291 (-1.8pp, p=0.435), API calls…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-02-08): Recommendation from the discussion, untested. Motivating data: value-revealing prints outnumber assertions for every model (e.g. Claude Opus 4.5 25.00 prints vs 5.16 assertions per resolved task; MiniMax M2 34.06 vs 7.37); 69.7-77.5% of…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-02-08): Recommendation, untested: "the goal should not be to simply make agents write more tests, but to make testing more targeted and budget-aware ... generating one minimal regression test, strengthening a weak oracle ..., or running only the…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-02-08): Recommendation, untested. Motivated by unresolved tasks running tests more (ExecCount 6.52 vs 4.89, ExecPerTest 1.70 vs 1.46, Mann-Whitney significant) and interventions moving cost far more than outcomes.
- …and 3 more sources in `library/entries/no-self-written-tests.yaml`.

## Caveats

The case for dropping tests rests on one prompt study (mini-SWE-agent on SWE-bench Verified, one run per arm, two models per direction, counting only files named like tests), and the share of weak checks comes from one model family on 110 tasks. It covers ad-hoc self-checks only: in 2026 studies, tests made into real checks (written before the fix, shown to fail on the unpatched code, then hardened against wrong fixes or written by a separate strong model and frozen) raised resolve rate, at about twice the cost per issue. Apart from 120 internal bugs at Google, all results come from Python issue-resolution benchmarks.

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)

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
