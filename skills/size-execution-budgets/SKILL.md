---
name: size-execution-budgets
description: "AOT optimization 7.b.iii (Tier 2, Reliability): Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts. Placeholder. Use when an agent shows: runs ending at the turn cap or deadline while still producing new information in their last turns (a run that ends at the cap after repeating itself is 7.b.i's signal, not this one); commands killed by a timeout that finish when re-run with a longer one."
---

<!-- Generated from library/entries/size-execution-budgets.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts

> **Placeholder.** Generated from `library/entries/size-execution-budgets.yaml` (entry 7.b.iii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 7.b.iii |
| Earlier id | T29 |
| Tier | 2 (Reliability): budgets are execution bounds |
| Categories | Orchestration: Bounding execution |
| Change | config / resource_limits (tune) |

## What it is

Set the turn or step cap, the wall-clock deadline and per-command timeouts from what runs that succeeded actually needed, not from framework defaults, so a run that is still making progress is not stopped short. This is one of three changes that bound a run, each for a different failure: this one lets productive runs finish, 7.b.i stops runs that have stalled, and 9.b.i makes sure a run that does hit the limit still returns its best answer. Raise a cap only together with 7.b.i, or a stall becomes a longer stall. Timeouts are tuned both ways: a timeout that kills commands that would have finished is too low, one that lets a hung command eat the run is too high.

## When it applies

- **In the code:** caps, deadlines and command timeouts at framework defaults, unchanged since the agent was built
- **In traces:** runs ending at the turn cap or deadline while still producing new information in their last turns (a run that ends at the cap after repeating itself is 7.b.i's signal, not this one); commands killed by a timeout that finish when re-run with a longer one
- **In eval results:** limit-ended outcomes (turn cap, deadline, command timeout) on cases where the run was still progressing

## How (outline)

1. From traces, take the distribution of turns, wall-clock and command durations on runs that succeeded.
2. Find the runs that ended at a limit while still progressing: new tool results, new files or a changing answer in their last turns.
3. Set each cap above the successful range (for example the 95th percentile) and each command timeout above the longest command that finished, with 7.b.i in place before raising a cap.
4. Re-run the truncated cases and compare limit-ended outcomes, cost and turns on the same cases.

## How to measure

- **before-after** (Tier 2): limit-ended outcomes, cost and turns on the same cases, before and after

## Expected impact

- **Cost:** mixed, medium: more turns per case when a cap is raised
- **Performance:** mixed, medium

## Evidence (summary)

- repo figure_04: MAX_TURNS raised 63 times, lowered 14; MAX_STEPS raised 26, lowered 5. The most-edited constants in the corpus.
- repo figure_01: Turn-budget edits in 11 to 18 of 20 runs per benchmark.
- paper Table 10: Knight 40 max turns vs Pawn 20.
- repo figure_04: SOFT_DEADLINE_SEC 2 up / 3 down, COMMAND_TIMEOUT_SEC 1 up / 4 down, RESEARCH_DEADLINE_SEC 0 up / 2 down. Direction is mixed, unlike turn budgets.

## Caveats

The evidence is frequency only: VeRO's optimizers raised turn caps far more often than they lowered them (MAX_TURNS 63 up, 14 down) and moved timeouts both ways, but no run measured the effect. Client retries for rate limits and transient errors are not a budget; they are in 2.b.i.

## Related

- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)

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
