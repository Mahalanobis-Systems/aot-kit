---
name: track-task-progress
description: "AOT optimization 7.b.iv (Tier 3, Tuning): Track explicit progress: a task list with a status per item, re-injected each turn. Placeholder. Use when an agent shows: runs ending with no edit or output, and short aimless trajectories (weaker models); long post-edit loops (stronger models); failure rows labeled goal-drift or state-tracking-failure."
---

<!-- Generated from library/entries/track-task-progress.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Track explicit progress: a task list with a status per item, re-injected each turn

> **Placeholder.** Generated from `library/entries/track-task-progress.yaml` (entry 7.b.iv). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 7.b.iv |
| Earlier id | T62 |
| Tier | 3 (Tuning): it changes what the model sees each turn |
| Categories | Orchestration: Bounding execution |
| Change | workflow / planning (add) |
| Also covers | Attention recitation |

## What it is

Give the agent a task-list tool (each item with a status, one in progress at a time), ask for the list on the first turn of non-trivial tasks, and re-inject the current list after the system prompt each turn instead of keeping old copies in history. The effect depends on the model: the one controlled study found a large success gain for a weaker model, none for a mid-size one, and a small success loss with a large cost saving for strong ones, whose removed turns were mostly post-edit verification.

## When it applies

- **In the code:** no task list or todo mechanism in the harness
- **In traces:** runs ending with no edit or output, and short aimless trajectories (weaker models); long post-edit loops (stronger models); failure rows labeled goal-drift or state-tracking-failure
- **In eval results:** success by trajectory length, per model

## How (outline)

1. Add the task-list tool and the first-turn requirement.
2. Inject the current list after the system prompt each turn; strip old copies from history.
3. Paired eval per model you run: success, cost and turns. Re-run it when the model changes.

## How to measure

- **experiment** (Tier 3): paired eval with and without the task list, separately for each model in use

## Expected impact

- **Quality:** mixed, medium: weaker model +11.6 points on SWE tasks and +4.5 on TerminalBench (a 30B model); no consistent gain at 120B; strong models about -2 points (Fan, Sep 2026)
- **Cost:** mixed, medium: strong models about 30% cheaper (fewer post-edit turns); the weaker model up to 75% dearer, because it now works the task instead of stopping early
- **Performance:** mixed: follows turns: fewer for strong models, more for the weaker one

## Evidence (summary)

- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): T4/128k, full tools. Nemotron-3 30B: planning +11.6 pp SWE and +4.5 pp TB at higher cost (TB cost +75%). Without planning its median SWE trajectory is 5 turns (vs 40), and 68.6% of runs end without an edit (vs 27.8%). Nemotron-3 120B: no…

## Caveats

Model strength decides the sign. On weaker models the list keeps the agent working the task; on strong models it mainly trades a little success for a lot of cost, by cutting verification turns. Measure it per model, and again after a model upgrade. Keeping the plan in a file only matters when work outlives one context window; that is 4.b.iii.

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)

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
