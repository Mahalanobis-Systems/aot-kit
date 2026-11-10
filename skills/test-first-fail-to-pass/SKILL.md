---
name: test-first-fail-to-pass
description: "AOT optimization 9.c.iv (Tier 3, Tuning): Write a fail-to-pass test before the fix, and harden it against wrong fixes. Placeholder. Use when an agent shows: the agent's own test passing on a fix that the reference tests reject; tests that also pass on the unpatched code; runs that submit right after their own new test passes."
---

<!-- Generated from library/entries/test-first-fail-to-pass.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Write a fail-to-pass test before the fix, and harden it against wrong fixes

> **Placeholder.** Generated from `library/entries/test-first-fail-to-pass.yaml` (entry 9.c.iv). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 9.c.iv |
| Earlier id | none (added after 2026-10-19) |
| Tier (proposed) | 3 (Tuning): it changes what the agent does and what it spends, so quality and cost must be checked |
| Categories | Verification: Sizing verification |
| Change | workflow / validation (add) |

## What it is

Make a coding agent's test a real check: write it before any source edit, admit it only if it fails on the unpatched code, then harden it against plausible wrong fixes or have a separate strong model write it and hold it fixed while the agent repairs. A test written together with the fix shares the fix's mistakes and adds little (58.9% to 61.4% resolved for GPT-5-mini); written first and hardened, it reached 69.4%, at $0.84 against $0.39 per issue. Frozen tests from GPT-5.6-sol raised it from 81.5% to 85.7% on SWE-bench Verified but only 0.7 points on SWE-bench Pro, and tests from a weak test writer lowered a repair agent from 61.2% to 57.3%.

## When it applies

- **In the code:** a test step that runs after or alongside the fix, with no check that the test fails on the unpatched code
- **In traces:** the agent's own test passing on a fix that the reference tests reject; tests that also pass on the unpatched code; runs that submit right after their own new test passes
- **In eval results:** resolve rate with and without the test step at matched spend; for a separate test writer, the share of past issues where its test fails on the unpatched code and passes on the known fix

## How (outline)

1. Start from the current agent as the baseline: resolve rate, cost and steps per issue with no test, and, for each check that passed after the agent's first edit, whether it also passes when replayed on the unpatched code (46.0% did for GPT-5.6-sol in one study).
2. Have the agent write the test before any source edit, run it on the unpatched code and reject it unless it fails there. Asserting the exact expected behavior matters more than printing values. In one study with GPT-5-mini, a test written together with the fix gave 61.4% resolved against 58.9% without, at $0.56 against $0.39 per issue; joint test and fix failures ran at 1.87 times the rate expected if they were independent, and 48.2% of unresolved runs had their own test passing on a wrong fix. Dropping the test-first phase cost 7.0 points.
3. Harden the test against plausible wrong fixes: run it against a few mutated versions of the fix (symptom suppressed, incomplete fix, input-specific shortcut) and strengthen it until they fail. Injected reproduction tests that also passed wrong fixes added nothing to the fix rate (+0.0 points) while strict ones added 8.5; the full loop took GPT-5-mini from 58.9% to 69.4%, at $0.84 against $0.39 per issue.
4. Alternatively, separate and freeze: a separate run writes the test from the issue, the harness admits it only if it fails on the unpatched code, and the repair agent then edits source only, with the test held fixed. First check the test writer on past issues: its tests should fail on the unpatched code and pass on the known fix (87.8% of SWE-bench Verified issues for GPT-5.6-sol, 61.0% for Codex-5.3, 22.2% for an untrained Qwen3.5-35B-A3B). Frozen tests from GPT-5.6-sol raised a Qwen repair agent from 61.2% to 65.3%, while tests from the untrained Qwen model lowered it to 57.3%.
5. A cheaper step on its own: have the harness tell the agent when a passing check also passes on the unpatched code (a median 11.0 s per run). It cut runs closing on such checks from 23.8% to 13.6% but did not change the resolve rate.
6. Measure with paired runs against the no-test baseline at matched spend where you can, several runs per arm: resolve rate, cost and steps per issue, and the share of kept tests that fail on the unpatched code and reject mutated fixes.

## How to measure

- **experiment** (Tier 3): paired runs against the no-test baseline, at matched spend where possible, several runs per arm: resolve rate, cost and steps per issue, and the share of kept tests that fail on the unpatched code and reject mutated fixes
- **monitor**: in production traces: the share of the agent's own passing tests that also pass on the unpatched code, and fixes whose own test passes but whose review or reference tests fail

## Expected impact

- **Quality:** improves, medium: written first and hardened, GPT-5-mini 58.9% to 69.4% resolved (Tan, Jul 2026); frozen tests from GPT-5.6-sol 81.5% to 85.7% on SWE-bench Verified but +0.7 on SWE-bench Pro, and tests from a weak writer cut a repair agent from 61.2% to 57.3% (Tao, Sep 2026)
- **Cost:** degrades, medium: $0.39 per issue with no test, $0.56 with a test written alongside the fix, $0.84 written first and hardened (GPT-5-mini; Tan, Jul 2026); the frozen-test gains are not compute-matched (Tao, Sep 2026)
- **Performance:** degrades, small: the agent took more steps when told to write the test first (Cheng, Jan 2026); replaying passing checks on the unpatched code added a median 11.0 s per run (Xu, Jul 2026)
- **Governance:** improves, small: code owners reviewing Google's AI-generated fixes strongly preferred fixes with a fail-to-pass reproduction test (Cheng, Jan 2026)

## Evidence (summary)

- Yuhao Tan, Zhibang Yang, Fangkai Yang, et al. (Nanjing University, Peking University, Microsoft), "Beyond Fail-to-Pass: Iterative Hardening… (2026-07-22): Table 2 (OpenHands with GPT-5-mini, 433 issues): fix only 58.9% resolved at $0.39 per issue; fix plus test in one run 61.4% at $0.56, its test failing on the buggy code and passing on the reference fix in 72.7%; CoHarden 69.4% at $0.84…
- Leitian Tao, Baolin Peng, Haorui Wang, et al. (University of Wisconsin-Madison, Microsoft Research), "ExecCritic: Learn to Test, Test to… (2026-09-08): §5.2.1: with the untrained Qwen3.5-35B-A3B repair agent fixed, no test 61.2% resolved; tests from the same untrained model 57.3% (-3.9); tests from GPT-5.6-sol 65.3% (+4.1); oracle fail-to-pass tests 69.4%. GPT-5.6-sol with generated…
- Runxiang Cheng, Michele Tufano, José Cambronero, et al. (Google), "Dynamic Cogeneration of Bug Reproduction Test in Agentic Program… (2026-01-27): §5.1: all three cogeneration prompts "produce at least one plausible fix for a similar number of bugs compared to Fix-only" (pass@k plotted in Figure 2, not tabulated); the agent took more steps when told to prioritize the test. Table 2…
- Xiaonan Xu, Wenjing Wu (Georgia Tech, University of Colorado Boulder), "Validation Evidence in LLM Repair Agents: How Much of What Passes… (2026-07-30): Table 3: of 2,548 passing checks with evaluable replays (3,730 events in 643 runs), 1,141 were regression-only and 30 misleading, so 46.0% also passed on the unpatched code; 26.9% of the checks that failed on the unpatched code and passed…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-02-08): Exploratory only: 8 SWE-bench Verified issues appear both in encourage-prompt Fail->Success-with-new-tests and discourage-prompt Success->Fail-with-tests-removed (e.g. astropy-13236, django-11790, sympy-21612); themes summarized with…
- …and 2 more sources in `library/entries/test-first-fail-to-pass.yaml`.

## Caveats

Each measured gain comes from its authors' own method: CoHarden on 433 Python issues with one run per issue and no significance tests (with GPT-5.4 and Claude Opus 4.5 it was compared only with other test-writing methods), and ExecCritic, whose gain is not compute-matched and nearly vanished on SWE-bench Pro. A weak test writer makes results worse, so the writer must be checked first, and the quality gain costs about twice as much per issue. Apart from 120 internal bugs at Google, all results come from Python issue-resolution benchmarks.

## Related

- `aot-kit:no-self-written-tests` (9.c.i, Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)

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
