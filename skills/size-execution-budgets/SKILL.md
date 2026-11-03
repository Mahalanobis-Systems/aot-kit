---
name: size-execution-budgets
description: "AOT optimization 7.b.iii (Tier 2, Reliability): Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts. Placeholder. Use when an agent shows: runs ending at the turn cap or deadline while still producing new information in their last turns (a run that ends at the cap after repeating itself is 7.b.i's signal, not this one); commands killed by a timeout that finish when re-run with a longer one; a command that never returns until the run's deadline; a command launched with a time limit longer than the time left; runs that stop on their own far below a cap that was raised."
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

Set turn caps, deadlines and command timeouts from what your successful runs actually used, show the agent how much budget is left, and never run a command without a timeout. This is one of three changes that bound a run: this one lets productive runs finish and keeps the rest from running long, 7.b.i stops runs that have stalled, and 9.b.i makes sure a run that hits the limit still returns its best answer, so raise a cap only together with 7.b.i. On 100 SWE-bench Verified tasks, a turn cap at the 75th percentile of each model's uncapped runs, with a turns-left reminder, cut cost by 24% to 68% for a -5 to +2 point change in solve rate, and in another study showing the agent its remaining calls lifted a 50-call run from 36.8% to 55.4% resolved. The limits: a higher cap buys little where runs stop on their own or stall (raising four local computer-use models from 15 to 100 steps left average success at 24.44% and 24.91% while prompt tokens rose 5.50x), and a deadline stated only in the prompt was not kept (161% of a 15-minute budget used on average).

## When it applies

- **In the code:** caps, deadlines and command timeouts at framework defaults, unchanged since the agent was built; a shell with no default command timeout; a deadline stated only in the prompt, with no clock or remaining-budget signal in context
- **In traces:** runs ending at the turn cap or deadline while still producing new information in their last turns (a run that ends at the cap after repeating itself is 7.b.i's signal, not this one); commands killed by a timeout that finish when re-run with a longer one; a command that never returns until the run's deadline; a command launched with a time limit longer than the time left; runs that stop on their own far below a cap that was raised
- **In eval results:** limit-ended outcomes (turn cap, deadline, command timeout) on cases where the run was still progressing; success and cost at two cap settings on the same cases

## How (outline)

1. Start from the limits as they are: from traces, or one uncapped run on a sample of cases, take the distribution of turns, tool calls, wall-clock and command durations, split into runs that succeeded and runs that failed, and count the runs that end at each limit (turn cap, deadline, command timeout).
2. Find the runs that ended at a limit while still progressing (new tool results, new files or a changing answer in their last turns); only those can be saved by a higher cap. Runs that end at the cap after repeating themselves are 7.b.i's, and a higher cap only makes them longer: raising four local computer-use models from 15 to 100 steps left average OSWorld success at 24.44% and 24.91% while steps per task rose 4.08x and prompt tokens 5.50x, with failures moving from cap stalls to premature false successes. Put 7.b.i in place before raising any cap.
3. Set the turn or tool-call cap from that distribution, not a framework default: on 100 SWE-bench Verified tasks, a cap at the 75th percentile of each model's uncapped turn counts cut cost by 24% to 68% with solve rates moving -5 to +2 points against no cap, while a 25th-percentile cap lost 13 to 37 points. To save more, start lower and grant one extension to runs that have not finished: a 50th-percentile cap with one extension to the 75th matched the fixed 75th-percentile cap within 2 points at 12% to 24% lower cost.
4. Tell the agent its remaining budget every turn (turns or calls used and left, time left), not only in the first prompt: under a 50-call cap on SWE-bench Verified, a used-and-remaining block after each tool result lifted resolved tasks from 36.8% to 55.4% at about the same calls and cost, and on a retail support benchmark a 10-call cap with the block beat a 50-call cap without it (pass^4 27.2% against 26.3%) with fewer calls.
5. Give every command a timeout and return a timeout to the agent as a result it can act on: a shell with no default timeout left 34 runs blocked in a final command that never returned, while a 300 s limit turned the same hang into an error the model diagnosed and fixed. Set each timeout above the longest command that finished in successful runs, and lower it where hung commands eat the run.
6. Enforce wall-clock deadlines in the harness, not only in the prompt: with the budget stated only in the prompt, runs used 161% of a 15-minute budget on average and 15% finished on time; harness hooks that add the time remaining to each tool result brought time used to 99.7% of the budget, and also clamping each command's timeout to the time left gave 74% of runs on time and 90% valid submissions (78% prompt-only), since the commonest overrun was a command launched with a limit longer than the time remaining. Do not expect a longer deadline alone to raise quality: in that study it did not.
7. Re-run the cases that ended at a limit, then the full set, at the old and new limits on the same cases and model, and compare success, limit-ended outcomes by kind, turns, tool calls, tokens, cost and wall-clock per case, and how the failures shift.

## How to measure

- **before-after** (Tier 2): the same cases and model at the current and the new limits, first the cases that ended at a limit, then the full set, with a remaining-budget signal (turns or calls left, time left) as its own arm; report success, limit-ended outcomes by kind (turn cap, deadline, command timeout), turns, tool calls, tokens, cost and wall-clock per case, and the failure mix, since a higher cap can turn cap stalls into premature false successes
- **monitor**: in production traces: share of runs ending at each limit and whether they were still producing new results in their last turns; turns, tool calls and wall-clock per run against each cap, split by success; commands killed by a timeout and whether a re-run with a longer one finished; commands run with no timeout or with a timeout longer than the time left; time used against the deadline

## Expected impact

- **Quality:** mixed, medium: caps below what runs need cost the most: a 25th-percentile turn cap lost 13 to 37 points of solve rate and a 50-call cap held SWE-bench Verified to 36.8% against 63.0% at 70 calls, while a 75th-percentile cap with a turns-left reminder moved solve rates by -5 to +2 points against no cap (Gao, Oct 2025; Liu, Nov 2025); showing the remaining budget each turn lifted the 50-call result to 55.4% (Liu, Nov 2025); raising caps that runs rarely reach added little (BrowseComp 10.5% at 30 calls, 12.6% at 100; OSWorld 24.44% at 15 steps, 24.91% at 100) (Liu, Nov 2025; Lee, Jul 2026); a shell with no default timeout left 34 runs blocked in a command that never returned (Li, Oct 2026)
- **Cost:** mixed, large: a turn cap at the 75th percentile of uncapped runs cut cost by 24% to 68%, and starting at the 50th percentile with one extension saved 12% to 24% more within 2 points of solve rate (Gao, Oct 2025); a remaining-budget signal at a 10-call cap matched a 100-call cap on BrowseComp at 31.3% lower cost (Liu, Nov 2025); raising a cap costs more: 15 to 100 steps raised steps per task 4.08x and prompt tokens 5.50x for no gain (Lee, Jul 2026), and 50 to 70 calls raised SWE-bench Verified cost per task from 18.50 to 21.59 cents (Liu, Nov 2025)
- **Performance:** mixed, medium: a deadline stated only in the prompt ran to 161% of a 15-minute budget (mean 1,453 s); harness clocks brought it to 99.7% (897 s) and clamping command timeouts to the time left to 847 s (Wang, Oct 2026); a hung command with no timeout ran to the 40-minute deadline where a 300 s command timeout let the same task finish in 11 minutes (Li, Oct 2026); higher caps lengthen runs (steps per task 4.08x from 15 to 100 steps) (Lee, Jul 2026)

## Evidence (summary)

- repo figure_04 (2026-02): MAX_TURNS raised 63 times, lowered 14; MAX_STEPS raised 26, lowered 5. The most-edited constants in the corpus.
- repo figure_01 (2026-02): Turn-budget edits in 11 to 18 of 20 runs per benchmark.
- paper Table 10 (2026-02): Knight 40 max turns vs Pawn 20.
- repo figure_04 (2026-02): SOFT_DEADLINE_SEC 2 up / 3 down, COMMAND_TIMEOUT_SEC 1 up / 4 down, RESEARCH_DEADLINE_SEC 0 up / 2 down. Direction is mixed, unlike turn budgets.
- Aaron Wang, Neelabh Madan, Vlad Sobal, Matthew Trager, Michael Kleinman, Elman Mansimov, Wei Xia, Stefano Soatto (AWS), "On the Clock… (2026-10-07): MLE-Bench Lite at a 15-minute budget (Table 2): prompt only, 15% of runs on budget, mean 1,453 s, 78% valid submissions, quality 49.4 percentile; with clocks, 62%, 897 s, 88%, 42.1; with clocks and command timeouts clamped to the time…
- …and 4 more sources in `library/entries/size-execution-budgets.yaml`.

## Caveats

The measured studies are few and narrow: the turn-cap study ran one agent on 100 SWE-bench Verified tasks once per setting with prompt caching off, its no-reminder comparison re-scores uncapped runs rather than running them, and its abstract's extra 12% to 24% saving from extensions is 5.95% to 24.30% in its tables; the deadline study used one 27B open model on five MLE-Bench Lite competitions, and its text says quality held (47.5 to 47.0) where its table shows 49.4 against 42.1. Whether a higher cap pays depends on whether runs reach it: with 100 calls allowed, a web-search agent used 14.24 searches on average and 0.8% of its questions needed more than 50, while a 50-call cap held SWE-bench Verified to 36.8% against 63.0% at 70 calls; for local computer-use models a higher step cap bought cost and turned cap stalls into premature false successes rather than passes. The remaining-budget gains come from the authors who propose the signal, a longer deadline did not by itself raise quality in the one study that tested it, and VeRO's counts (turn caps raised 63 times, lowered 14) show what optimizers changed, not what it did; client retries for transient errors are 2.b.i, and in-model thinking budgets are 1.b.i, not budgets in this sense.

## Related

- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)

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
