---
name: no-self-written-tests
description: "AOT optimization 9.c.i (Tier 3, Tuning): Don't prompt agents to write their own tests; suppress it for test-heavy models. Placeholder. Use when an agent shows: test files written with print statements and no assertions; test writing and running over about 20% of tokens."
---

<!-- Generated from library/entries/no-self-written-tests.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Don't prompt agents to write their own tests; suppress it for test-heavy models

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

Agent-written tests are mostly print probes and do not change resolve rate. Prompting for them added 20% output tokens for no gain; suppressing them for models that write many saved 33-49% of input tokens for a non-significant loss. Keep test writing for bugs with explicit repro conditions, and make those tests assertion-based.

## When it applies

- **In the code:** a prompt that tells the agent to write tests
- **In traces:** test files written with print statements and no assertions; test writing and running over about 20% of tokens
- **In eval results:** resolve rate unchanged between runs with and without agent tests

## How (outline)

1. From traces, measure the share of tokens spent writing and running tests, and whether they contain assertions.
2. Remove any instruction to write tests; for test-heavy models add an instruction not to, except for bugs with a stated repro.
3. Paired eval on resolve rate and tokens.

## How to measure

- **experiment** (Tier 3): paired eval with and without the instruction

## Expected impact

- **Quality:** none: -1.8 to -2.6 points, not significant (Apr 2026)
- **Cost:** improves, medium: -33 to -49% input tokens
- **Performance:** improves, small

## Evidence (summary)

- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-04-09): Encourage prompt: GPT-5.2 flips No test -> Has test on 322/500 tasks (64.4%) with net 0 change in resolved (359 -> 359, McNemar p=1.000) while API calls +5.5%, input tokens +9.0%, output tokens +19.8% (all Wilcoxon p<0.001). Gemini 3 Pro…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-04-09): Discourage prompt, SWE-bench Verified: Kimi K2 Thinking resolved 317 -> 304 (-2.6pp, McNemar p=0.228), API calls -35.4%, input tokens -49.0%, output tokens -43.1%; DeepSeek v3.2 Reasoner resolved 300 -> 291 (-1.8pp, p=0.435), API calls…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-04-09): Recommendation from the discussion, untested. Motivating data: value-revealing prints outnumber assertions for every model (e.g. Claude Opus 4.5 25.00 prints vs 5.16 assertions per resolved task; MiniMax M2 34.06 vs 7.37); 69.7-77.5% of…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-04-09): Recommendation, untested: "the goal should not be to simply make agents write more tests, but to make testing more targeted and budget-aware ... generating one minimal regression test, strengthening a weak oracle ..., or running only the…
- Chen et al., "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (2026-04-09): Recommendation, untested. Motivated by unresolved tasks running tests more (ExecCount 6.52 vs 4.89, ExecPerTest 1.70 vs 1.46, Mann-Whitney significant) and interventions moving cost far more than outcomes.
- …and 1 more sources in `library/entries/no-self-written-tests.yaml`.

## Related

- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
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
