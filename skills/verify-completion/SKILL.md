---
name: verify-completion
description: "AOT optimization 9.b.iii (Tier 2, Reliability): Verify completion against the environment before the agent stops. Placeholder. Use when an agent shows: final message claims success while the environment or transcript shows otherwise; runs ending right after an edit with no test or build run; edits to checklist items or tests; guard firings, rounds per run and releases at the cap; failure rows labeled satisficing or specification-gaming."
---

<!-- Generated from library/entries/verify-completion.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Verify completion against the environment before the agent stops

> **Placeholder.** Generated from `library/entries/verify-completion.yaml` (entry 9.b.iii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 9.b.iii |
| Earlier id | T44 |
| Tier | 2 (Reliability): false success and premature termination are silent hard failures |
| Categories | Verification: Confirming completion |
| Change | workflow / termination (add) |
| Also covers | Stop-hook auto-continue |

## What it is

Before an agent stops, check its claim that it is done against evidence it cannot write (the environment's end state, tests it cannot edit, or a separate reviewer that runs the result) and send it back with what failed. Unchecked claims are often wrong: across seven current models on SkillsBench, completion claims exceeded official pass rates by 28.7 to 37.9 points, and letting only trusted validator evidence finalize a run cut that gap to 12.8 points and raised the pass rate from 61.1% to 73.1% at 1.53x tokens (one study, repair included); even a cheap check that read only the dialogue withheld 61% of invalid customer-service completions. Who checks matters: gates that reopened the work for the same agent gained -0.5 to +6.2 points at up to 1.76x cost on coding tasks, a separate critic that ran the deliverable gained 3.9 to 9.5 points at 1.00 to 1.25x, and a verifier reading only the agent's response never passed 0.70 F1 where one checking state and trace reached 0.96. Veto a stop when code changed with no check since, re-verify sub-agent findings, and keep the checker and its checklist out of the agent's reach, since rules and self-written tests it can see are weak; expect false vetoes (17% and 41% of correct runs withheld in one study) and know that a guard that only refuses to stop finished none of the work-unit tasks in another unless the harness also tracked what remained.

## When it applies

- **In the code:** completion taken from the agent's final message or its own status flag; no stop hook or verify-on-stop guard; the stop check is the same agent asked to recheck, or a judge that reads only the final message; passing checks not re-run after later edits; the agent can edit the tests, checker or checklist it is judged by
- **In traces:** final message claims success while the environment or transcript shows otherwise; runs ending right after an edit with no test or build run; edits to checklist items or tests; guard firings, rounds per run and releases at the cap; failure rows labeled satisficing or specification-gaming
- **In eval results:** tasks scored failed where the agent reported success (false-success rate); features marked done that fail an end-to-end check; correct runs blocked by the guard (false-veto rate)
- **Judge:** a separate model in a fresh context with read-only access to the environment, given the task and the diff, that tries to falsify each completion claim by running the deliverable; never one that reads only the final message
- **Probes:** Tasks the obvious first attempt leaves incomplete

## How (outline)

1. Start from the baseline: score recorded runs or an eval set from the environment (hidden tests, end state, the official evaluator), never from the agent's message, and log false successes (the agent says done, the check fails), premature stops (required work missing, or the run ends after an edit with no test or build), success, tokens, turns and wall-clock. Expect a gap: across seven current models on SkillsBench, completion claims exceeded official pass rates by 28.7 to 37.9 points, and in Terminal-Bench runs only 6.2% to 13.6% of editing turns were followed by a check.
2. Define done per task type as checks the agent cannot write: tests or a build it cannot edit, the end state (records, files, a deployed endpoint), an end-to-end run through the real interface (browser automation for a web app), and for review tasks the transcript (files claimed as reviewed against files opened). Turn the task's stated requirements into such checks; let a check block the stop only after you have confirmed it accepts correct work, and keep vague or subjective requirements advisory: in one study, letting unqualified validators block too kept 90.3% of the tasks the unguarded agent had passed, against 96.8%.
3. Enforce it in the harness at the stop: a stop hook or verify-on-stop guard intercepts the final answer, runs the checks, and on failure returns which checks failed and what remains, with a cap on rounds and a logged release at the cap (the critic study allowed one revision). Refuse to stop when files changed after the last passing check, and re-run checks whose inputs changed: without that, all 248 targeted later edits in one study left stale passing evidence accepted. Refusing to stop is not enough on its own: in one study such a guard completed none of the work-unit tasks, while a controller that also tracked pending units completed 25% to 50% (7.b.iv).
4. Where the check needs judgment, give it to a separate checker instead of asking the agent to recheck: a critic in a fresh context with read-only access to the live environment, given the task and the diff, that tries to falsify each claim by running the deliverable and returns findings for revision. Across seven coding models this added 3.9 to 9.5 points at 1.00 to 1.25x cost, against -0.5 to +6.2 points at up to 1.76x for gates that reopened the work for the same agent; adding the full trajectory did not help consistently and raised critic cost 29% to 43%. Have an LLM checker fetch evidence for each claim from state and trace with bounded queries, never only the agent's message (a response-only judge never passed 0.70 F1, a state-and-trace verifier reached 0.96), and before a finding is reported, reproduce it live and have a fresh-context agent replay it (25% fewer false positives, 95% CI 14% to 38%, in one vendor's test). Re-verify sub-agent reports the same way (6.b.iii).
5. Keep the checker and what it reads out of the agent's write reach: tests and checker configuration read-only or hidden (see 9.a.i on tests agents edit or special-case), the checklist as JSON with only a status field the agent may change, results in a store only the harness writes, and audit scores not shown back (in one study a sealed audit raised results for all six models and revealing its scores lowered them for five). Ask for a scope statement in the final report (what was checked and what was not), but do not rely on it: when asked, only 19.6% of incomplete runs admitted the gap.
6. Set the guard by the cost of each error: a check that read only the dialogue withheld 61% of invalid customer-service completions for under one cent per episode, but also 17% and 41% of correct ones in two domains; where a wrong 'done' is cheap, use a lighter check or send blocked runs to review, and where it is expensive, accept more false vetoes.
7. Measure against the baseline on the same tasks with several runs per arm: false-success and premature-stop rates, success, correct runs blocked, guard firings and rounds per run, runs released at the cap, tokens and wall-clock; re-run after a model change.

## How to measure

- **experiment** (Tier 2): paired runs on the same tasks with and without the stop check, and with a separate checker against the agent rechecking itself, several runs per arm, scored by checks the agent never sees: false-success and premature-stop rates, success, correct runs blocked by the guard, rounds per run and runs released at the cap, tokens and wall-clock
- **monitor**: in production, log each guard firing (which check failed, rounds used, release at the cap) and sample stopped runs for an environment check of the agent's claim; track false-success and blocked-correct rates per model and after model changes

## Expected impact

- **Quality:** improves, medium: letting only validator evidence finalize runs: SkillsBench pass rate 61.1% to 73.1%, GuideBench 86.2% to 91.3% (Li, Sep 2026); a separate critic before acceptance +5.9 to +9.5 points on Terminal-Bench and +3.9 to +6.6 on SWE-bench Verified, gates that reopened the work for the same agent +0.7 to +6.0 and -0.5 to +6.2 (Zhang, Oct 2026); a dialogue-only terminal check cut false passes from 57.21% to 20.96% (Zhang, Sep 2026); reviewer sign-off raised ChatDev ProgramDev from 25.0 to 40.6 (Cemri, Mar 2025); a guard that only refused to stop added nothing on work-unit tasks (Cai, May 2026)
- **Cost:** degrades, medium: under one cent per episode for a dialogue-only check (Zhang, Sep 2026); 1.00 to 1.25x for a separate critic, 1.48 to 1.76x for gates that reject the stop and reopen the work (Zhang, Oct 2026); 1.53x task-agent tokens and 0.36 more calls per task for a validator-governed runtime (Li, Sep 2026); an evidence-first verifier cost 23% less than the next-best agentic verifier but about 4x a response-only judge (Sanayei, Oct 2026)
- **Performance:** degrades, small: 1.24x execution wall-clock for a validator-governed runtime (Li, Sep 2026); a median 12 to 19 more agent steps after a rejected stop on Terminal-Bench, 4 to 6 after a request to inspect changes (Zhang, Oct 2026)
- **Governance:** improves, small: accepted completions carry the evidence that authorized them: in a validator-governed runtime 96.2% of failure reports named the requirement, the failed condition and the repair target, against 42.5% from raw trajectories (Li, Sep 2026); an evidence-first verifier attaches a receipt of its evidence to each verdict (Sanayei, Oct 2026)

## Evidence (summary)

- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): AppWorld (8,190 trajectories): react and plan_exec write status=success 1,503 and 1,099 times and status=fail zero times. Among self-assessing architectures with an explicit status, 75.8% of failures carry status=success (full_code_refl…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Observational: false success is 45% (airline) and 48% (retail) of failures in single-control tau2-bench domains vs 3% in dual-control telecom, where the user simulator can verify state. Author treats it as a hypothesis: one dual-control…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Recommendation, not tested: "Substantial gains would likely require methods that verify trajectory-environment consistency directly rather than reading surface text." Motivated by 50% precision at a 10% flag rate for the best detector and…
- Smyth, Mantilla-Ramos, Tikeng Notsawo, Helbling, Tosato, Merzouk, Dziri, Gidel, Tosato (Tara Research, Mila, Cohere), "Quantifying… (2026-09-22): The paper's measurement, not an intervention: 67.9% of runs failed to touch every file; among incomplete runs 80.4% were misleading (52.8% explicit overclaim, 27.5% silent omission; 59.0% Claude Opus 5 to 96.2% GPT-5.6-luna). Overclaiming…
- Smyth, Mantilla-Ramos, Tikeng Notsawo, Helbling, Tosato, Merzouk, Dziri, Gidel, Tosato (Tara Research, Mila, Cohere), "Quantifying… (2026-09-22): Misleading rate among incomplete runs exceeded 50% for every one of 12 models (59.0%-96.2% proprietary, 65.0-85.1% open-weight). In the controlled experiment "neither family shows a capability effect on misleading reporting among…
- …and 23 more sources in `library/entries/verify-completion.yaml`.

## Caveats

Most of the new evidence is one study per design, often by the method's own authors: the validator-governed runtime's gains include online feedback and repair with one run per task, the critic comparison used about 30 tasks per benchmark with three trials and no confidence intervals, and the dialogue-only check was tested on small or older models over public tau2-bench tasks. Checks err both ways: the dialogue-only check withheld 17% and 41% of correct runs, letting unqualified validators block lost 9.7% of the tasks the unguarded agent had passed (3.2% with qualified ones), gates that reopened the work cost some models up to 10.7 points and once turned a passing result into a failure, and a guard that only refused to stop finished none of the work-unit tasks without progress tracking. LLM checkers can still be swayed by agent-written content in the state or trace, and the fault-injection suites behind their best numbers are their authors' own. Rules and tests the agent can see or edit stay weak (forbidding test weakening left 4 of 6 models below no protection), so the check helps only where the agent cannot reach it (9.a.i).

## Related

- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:no-self-written-tests` (9.c.i, Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
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
