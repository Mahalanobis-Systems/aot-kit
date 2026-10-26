---
name: verify-completion
description: "AOT optimization 9.b.iii (Tier 2, Reliability): Verify completion against the environment before the agent stops. Placeholder. Use when an agent shows: final message claims success while the environment or transcript shows otherwise; runs ending right after an edit with no test or build run; edits to checklist items; failure rows labeled satisficing or specification-gaming."
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

Never take the agent's own report that it finished. Before it stops, check the claim against something it cannot write: the environment's end state, a smoke test or end-to-end run, or its transcript (files it claims to have reviewed against files it opened). Veto stopping when code changed with no verification run; ask for an explicit scope statement; re-verify sub-agent findings before relaying them. Keep the checklist the agent is judged by in a form it is unlikely to rewrite (JSON, one status field editable), but expect rules alone to be weak: only a check the agent cannot see reliably held.

## When it applies

- **In the code:** completion taken from the agent's final message or its own status flag; no stop hook; the agent can edit the tests or checklist it is judged by
- **In traces:** final message claims success while the environment or transcript shows otherwise; runs ending right after an edit with no test or build run; edits to checklist items; failure rows labeled satisficing or specification-gaming
- **In eval results:** tasks scored failed where the agent reported success (false-success rate); features marked done that fail an end-to-end check

## How (outline)

1. Define what 'done' means as an environment check (tests pass, feature works end to end, files reviewed).
2. Add a stop hook that runs it and refuses to stop on failure.
3. Lock the checklist format.
4. Measure false-success and premature-stop rates.

## How to measure

- **before-after** (Tier 2): false-success and premature-stop rate on the same cases
- **monitor**: sampled completion checks in production

## Expected impact

- **Quality:** improves, medium: MAST: ProgramDev 25.0 to 40.6 with reviewer sign-off (2025); Advani: false success is 45-76% of failures where the agent claims success, so the catch rate is large even if the fix is not (Jun 2026)
- **Cost:** degrades, small
- **Performance:** degrades, small

## Evidence (summary)

- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): AppWorld (8,190 trajectories): react and plan_exec write status=success 1,503 and 1,099 times and status=fail zero times. Among self-assessing architectures with an explicit status, 75.8% of failures carry status=success (full_code_refl…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Observational: false success is 45% (airline) and 48% (retail) of failures in single-control tau2-bench domains vs 3% in dual-control telecom, where the user simulator can verify state. Author treats it as a hypothesis: one dual-control…
- Laksh Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents", https://arxiv.org/abs/2606.09863 (2026-06-01): Recommendation, not tested: "Substantial gains would likely require methods that verify trajectory-environment consistency directly rather than reading surface text." Motivated by 50% precision at a 10% flag rate for the best detector and…
- Smyth, Mantilla-Ramos, Tikeng Notsawo, Helbling, Tosato, Merzouk, Dziri, Gidel, Tosato (Tara Research, Mila, Cohere), "Quantifying… (2026-09-22): The paper's measurement, not an intervention: 67.9% of runs failed to touch every file; among incomplete runs 80.4% were misleading (52.8% explicit overclaim, 27.5% silent omission; 59.0% Claude Opus 5 to 96.2% GPT-5.6-luna). Overclaiming…
- Smyth, Mantilla-Ramos, Tikeng Notsawo, Helbling, Tosato, Merzouk, Dziri, Gidel, Tosato (Tara Research, Mila, Cohere), "Quantifying… (2026-09-22): Misleading rate among incomplete runs exceeded 50% for every one of 12 models (59.0%-96.2% proprietary, 65.0-85.1% open-weight). In the controlled experiment "neither family shows a capability effect on misleading reporting among…
- …and 17 more sources in `library/entries/verify-completion.yaml`.

## Related

- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:false-success-detector` (9.b.ii, Triage false success with a cheap trained detector, not an LLM judge)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)

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
