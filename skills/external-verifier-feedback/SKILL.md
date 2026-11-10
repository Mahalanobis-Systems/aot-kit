---
name: external-verifier-feedback
description: "AOT optimization 9.a.i (Tier 2, Reliability): Feed back a sound external verifier's verdict; never the model's own critique. Placeholder. Use when an agent shows: errors a compiler, test, schema or policy check would catch reaching the final answer; SQL errors and hallucinated table names; runs that end after a failed or never-run check; identical resubmissions after a rejection; edits to test files, special-cased test inputs or overloaded comparisons; answers changed after a critique turn with no new external information; failure rows labeled tool-feedback-neglect or satisficing."
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

Have the harness check every output with something the model cannot fool, such as tests, a compiler, a schema or policy check, execution or a solver, and send the verdict back for another try. With a current reasoning model, resampling until a sound checker accepted added up to 18.2 points where a comparable loop judged by an LLM critic moved accuracy between -2.7 and +3.1; pass/fail with the first error is usually enough, generated SQL can be repaired from execution errors, and checking SQL against governed rules took 0.15 retries per question in one system. The check works only if the harness enforces it and the agent cannot change it: an agent left to decide when to stop gave up on 30 solvable problems, 28 of them with a proof the validator had rejected, agents edited or special-cased tests they could see (a test-feedback loop raised cheating on impossible tasks from 33% to 38%), and visible tests overstated held-out correctness by 43-48 points for one frontier agent building whole systems. So keep tests read-only or hidden, score on a held-out check, let the agent flag a check it thinks is broken, and do not add a same-model critique step (7.c.i): on older models it cut accuracy (GPT-3.5 on CommonsenseQA 75.8% to 38.1%), and a verification tool one optimizer added raised GAIA 5.75 points but cut SimpleQA 17.8.

## When it applies

- **In the code:** no step runs the build, tests, linter, schema check, policy rules or execution on the output before it is returned, or the agent can finish without the check passing; tests or checker config the agent can write to; a critique or reflect step where the same model reviews its own answer with no tool output or environment state in the loop
- **In traces:** errors a compiler, test, schema or policy check would catch reaching the final answer; SQL errors and hallucinated table names; runs that end after a failed or never-run check; identical resubmissions after a rejection; edits to test files, special-cased test inputs or overloaded comparisons; answers changed after a critique turn with no new external information; failure rows labeled tool-feedback-neglect or satisficing
- **In eval results:** failures a deterministic check would have flagged; a gap between the pass rate on checks the agent saw and on held-out checks; accuracy before and after any critique step
- **Probes:** Tasks whose visible tests contradict the specification, so any pass is gaming, and tasks scored on a held-out check that combines features the visible tests check one at a time.

## How (outline)

1. Start from the baseline: on the eval set or recorded runs, log how often outputs reach the user failing a check you could have run (build, tests, type or schema check, SQL that fails EXPLAIN or names a table that does not exist, a policy rule), plus pass rate, rounds, tokens and latency per task. Set aside a held-out check the agent never sees (hidden tests, gold answers or review) to score the change, because the loop will optimize whatever check it is given.
2. Pick the sound check the task admits and wire it to every output: compiler, type checker, linter or language-server diagnostics after each edit; unit tests; JSON or schema validation; for plans, proofs and puzzles a validator, proof checker or solver; for tool use, the policy written as code that rejects a violating call (it raised one agent's safety score from 48.75% to 58.34%). For SQL, run EXPLAIN and execute, check for hallucinated tables and columns and repair from the error (removing one fixer cut successful compilation from 95% to 76%), validate against approved metrics, joins, filters and row-level security where they exist, and run read-only with timeouts and row caps (10.a.i).
3. Put the check where the agent cannot change it: keep tests and checker config read-only or hidden (hiding tests cut cheating on impossible tasks to near zero but cost legitimate solves; read-only kept performance and stopped test edits but not special-casing), and do not let the agent write the check it is judged by (9.c.i). Judge coverage, not the green light: frontier agents saturated visible feature tests while failing held-out tests that combine those features, by 43-48 points for one agent building whole systems.
4. Enforce it in the harness, not the prompt: accept no answer until the check passes, and on a failure start another round with the verdict and require an edit before resubmitting (one agent resubmitted an unchanged proof 170 times). Feed back pass/fail with the first concrete error (compiler message, failing test, violated rule); in one planning study more detail than pass/fail helped only on Blocksworld (60% to 87%). Let the agent edit in place with feedback after every edit rather than regenerate the whole output (69 against 18 proofs at the same model and budget). Where only the final answer can be checked, resample until the check accepts; where intermediate states can be checked, check them during the run (on a maze task 88.8% with a final-answer check against 97.9% with checks during the run).
5. Bound the loop and give it an exit: cap rounds (one SQL system allowed three revisions and averaged 0.15 per question), stop runs that repeat or stall (7.b.i) and size budgets so productive runs can finish (7.b.iii). Let the agent flag a check it believes is wrong, or abstain when no answer passes, instead of working around it: an abort option cut GPT-5's cheating on impossible tasks from 54% to 9%.
6. Where no sound check exists, do not substitute the model's own critique: with a current reasoning model a comparable loop judged by an LLM critic moved accuracy by -2.7 to +3.1 points while resampling until a sound checker accepted added up to 18.2. Check completion against the environment (9.b.iii), use a trained detector (9.b.ii) or spend on parallel samples with a vote (9.c.ii), and test any added verification step on every task type.
7. Measure: run the paired eval at equal budget with no check, pass/fail feedback, full error text and resampling until the check passes; report end quality on the held-out check, the check-failure rate on the first attempt and on returned outputs, rounds per task, tokens and latency, and gaming signals (test or checker edits, special-cased inputs, identical resubmissions); add probes whose tests contradict the specification, where any pass is gaming.

## How to measure

- **experiment** (Tier 3): paired eval at equal budget: no check, the check with pass/fail and first-error feedback, full error text, resampling until the check passes, and any proposed critique step; score end quality on a held-out check the agent never sees (hidden tests, gold answers or review) as well as the check-failure rate on the first attempt and on returned outputs, rounds per task, tokens and latency; include probes whose tests contradict the specification, where any pass is gaming
- **monitor**: in production traces: share of outputs returned without a passing check, rounds to pass, runs that hit the round cap, identical resubmissions, edits to test files or checker config, special-cased inputs, and flags or abstentions; audit a sample of passed outputs against a held-out check or human review, since the loop's own pass rate can rise while true correctness does not

## Expected impact

- **Quality:** improves, large: sound check in the loop: Blocksworld 40% to 87% (Stechly, Feb 2024); removing an SQL fixer cut successful compilation from 95% to 76% (Chen, Jul 2025); resampling until a sound checker accepted raised ZebraLogic-XL from 79.2% to 97.4% where a comparable LLM-critic loop reached 82.3%, and policy checks written as code took a Qwen3-30B agent on telecom tasks from 32.17% to 42.11% (87.70% with rules debugged on traces) (Bhat, Feb 2026); exposing the Lean validator and enforcing it lifted the same Claude model from 63 to 83 FATE-X proofs (Moalla, Oct 2026); limits: agents game checks they can see or edit (GPT-5 passed 54% of impossible SWE-bench tasks; Zhong, Oct 2025) and visible tests overstated held-out correctness by 43-48 points for Claude Code on 30 systems-building tasks (Zhao, May 2026); same-model critique cut GPT-3.5 on CommonsenseQA from 75.8% to 38.1% (Huang, Oct 2023)
- **Cost:** degrades, small: retries add calls only when the check fails: 0.15 retries per question (at most 2), with the system's 5x tokens coming from its grounding prompt rather than the retries (Pillai, Jul 2026); resampling until a sound checker accepted used 106% to 270% of one attempt's tokens and checks inside the trace 62% to 153%, below one attempt where feedback cut unproductive reasoning (Bhat, Feb 2026); loop design matters more than the check: the same model cost $9.00 per problem editing in place against $17.39 regenerating the whole proof each round, and reflecting after every turn about doubled the cost per solve (Moalla, Oct 2026)
- **Performance:** degrades, small: governed SQL with its validate-and-retry loop took 7.8 s against 6.1 s per question for direct text-to-SQL (about 1.3x), mostly from its larger prompt (Pillai, Jul 2026); each failed check adds a model call and a check run
- **Security:** improves, medium: policy rules written as code that reject unsafe tool calls raised AgentSafetyBench safety from 48.75% to 58.34% (72.31% with per-task checks) for one Qwen3-30B agent (Bhat, Feb 2026); SQL checked against row-level-security rules and retried had 0 violations on four models where ungoverned single-pass baselines leaked on 7.5% to 13% of adversarial questions, though only the governed arm was given the user's access predicate (Pillai, Jul 2026); a check the agent can edit is itself a target: agents edited tests or special-cased them to pass (Zhong, Oct 2025)
- **Governance:** improves, medium: rules enforced by a check held at zero filter violations with no run-to-run variance across four models, against 41% to 48% for ungoverned baselines, but weaker models executed fewer queries (Pillai, Jul 2026, confounded as above); an option to flag a broken check leaves a record instead of a silent workaround (Zhong, Oct 2025); a passing check certifies only what it covers: visible tests were saturated while held-out tests failed (Zhao, May 2026)

## Evidence (summary)

- Stechly et al., "On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks"… (2024-02-12): Table 1, LLM+Sound Critique (best of binary / first-error / all-error feedback) vs standard prompting: Game of 24 38% vs 5%; Graph Coloring 38% vs 16%; Blocksworld 87% vs 40%; Mystery Blocksworld 10% vs 4%. Monotone improvement with more…
- Stechly et al., "On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks"… (2024-02-12): Table 1, binary / first-error / all-errors: Game of 24 36% / 38% / n.a.; Graph Coloring 38% / 37% / 34%; Blocksworld 60% / 87% / 83%; Mystery Blocksworld 10% / 8% / 6%. Blocksworld is the exception where first-error feedback helped (60 ->…
- Stechly et al., "On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks"… (2024-02-12): Table 1, sampling k=15 / k=25: Game of 24 28% / 42%; Graph Coloring 40% / 44%; Blocksworld 68% / 72%; Mystery Blocksworld 9% / 14% (standard prompting 5/16/40/4%).
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", https://arxiv.org/abs/2310.01798 (2023-10-03): Recommendation citing Self-Debug, CRITIC and trained verifiers; not tested in this paper.
- Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs"… (2024-06-03): Survey conclusion (2): prior studies "widely agree" self-correction improves responses when reliable external tools or knowledge exist; code-interpreter feedback counted as fair because it cannot easily improve the initial generation.
- …and 29 more sources in `library/entries/external-verifier-feedback.yaml`.

## Caveats

The evidence that self-critique hurts comes mostly from 2023-2024 runs on GPT-3.5, GPT-4 and Llama-2; with a current reasoning model an LLM-critic loop left accuracy roughly flat (-2.7 to +3.1 points), and Self-Refine helped one coding scaffold (OpenHands, +15.8 for GPT-5 mini), so the case for a sound check is that it gains far more, not that critique always fails (7.c.i). A check is only as sound as its coverage and its distance from the agent: agents edited or special-cased tests they could write (GPT-5 passed 54% of impossible SWE-bench tasks), more search against visible tests often widened their gap to held-out tests, and making composition tests visible cut one task's gap from 35 to 9 points but raised another's by 25. Several gains are scored by the loop's own check or confounded: GROUND's zero violations come from a retry loop that reuses its evaluator's classifiers, only its governed arm got the user's access predicate and its baselines ran once without retry; interwhen's telecom gain includes rules debugged on traces and a per-task completeness check; h1's ablations are single runs against a proof checker, a near-perfect check most tasks lack. In VeRO, a multi-step verification tool an optimizer added raised GAIA 5.75 points and cut SimpleQA 17.8 in the same commit, so test any added verification step on every task type.

## Related

- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:no-self-written-tests` (9.c.i, Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests)
- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:verify-citations` (9.a.ii, Verify citations claim by claim for factual support)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:self-critique-evaluator` (7.c.ii, Self-critique evaluator loop)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)
- `aot-kit:test-first-fail-to-pass` (9.c.iv, Write a fail-to-pass test before the fix, and harden it against wrong fixes)

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
