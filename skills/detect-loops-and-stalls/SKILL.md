---
name: detect-loops-and-stalls
description: "AOT optimization 7.b.i (Tier 2, Reliability): Detect stalls and loops: warn, then stop early. Placeholder. Use when an agent shows: tool spans whose normalized call (name plus arguments) and result repeat an earlier span in the run; the same screen or state recurring three times with no visible change; streaks of identical failing calls; runs ending at the turn cap or deadline after such a streak; a warning followed by the same call again; failure rows labeled redundancy or state-tracking-failure (same-tool streaks with changing arguments are retries, not loops)."
---

<!-- Generated from library/entries/detect-loops-and-stalls.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Detect stalls and loops: warn, then stop early

> **Placeholder.** Generated from `library/entries/detect-loops-and-stalls.yaml` (entry 7.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 7.b.i |
| Earlier id | T05 |
| Tier | 2 (Reliability): an execution bound: runaway loops are hard failures |
| Categories | Orchestration: Bounding execution |
| Change | workflow / termination (add) |
| Also covers | Infinite-loop prevention by hashing recent calls |

## What it is

When an agent repeats the same call and gets the same result, push it to change approach after a few repeats, and end the run only after a long streak of identical failures. It pays mainly for loop-prone models: loops appeared in 5.21% of Meta's production coding-agent trajectories, where an observer that flagged them (with other misbehaviors) and injected course-correction reminders cut tokens per session 5.3%, and on OSWorld forcing a change of approach after repeated no-change actions added up to 4.24 points for Gemini 3 Flash but 0.04 for Claude Sonnet 4.6 at 100 steps, and cost 6.15 points at a 15-step budget. A prompt line or a silent refusal of exact repeats is not a substitute (with repeats refused, an agent proposed already-run calls as often as before), and repetition alone is not failure: identical repeats were rare after tool faults, retries with changed arguments were common, and blind retries were as frequent in passing coding runs as in failing ones. Treat the stop as a tested backstop, not a saving: ending stuck runs cost a small model 3.4 points of success, a rule-based abandon never fired for a frontier terminal agent, and advisory controllers raised cost 19% to 47% with no gain, so test any controller end to end against plain rules and a placebo.

## When it applies

- **In the code:** no comparison of a tool call or query against previous ones; the loop ends only at a fixed turn cap
- **In traces:** tool spans whose normalized call (name plus arguments) and result repeat an earlier span in the run; the same screen or state recurring three times with no visible change; streaks of identical failing calls; runs ending at the turn cap or deadline after such a streak; a warning followed by the same call again; failure rows labeled redundancy or state-tracking-failure (same-tool streaks with changing arguments are retries, not loops)
- **In eval results:** per model: share of runs with a loop and of steps spent in loops (5.21% of production coding trajectories in one company; 2.1% to 4.9% of steps on OSWorld), turn-cap and timeout outcomes as a share of failures, and success on runs a stop rule ended
- **Probes:** Tasks where a tool returns the same error or an unchanged result whatever the agent does, or whose goal is unattainable

## How (outline)

1. Start from the baseline: on the eval set or recorded traces, per model, measure the share of runs with a loop (the same normalized call, tool name plus arguments with whitespace and argument order normalized, returning the same result as an earlier call), the share of steps spent in loops, runs ending at the turn cap or deadline, success, tokens, turns and wall-clock. Expect loops in a minority of runs that varies by model and setup: 5.21% of a five-week sample of one company's production coding-agent trajectories (2.18% for Claude Sonnet 4.5, 3.59% for Claude Opus 4.5), 12.1% to 20.7% of failed OSWorld tasks for two current backbones, and 21.3% to 40.0% of CodeGym tasks for three Gemini models with full history (any single repeat counted), more once history is summarized (5.a.i).
2. Compare the call together with its result, not the call alone: keep a hash of each normalized call and of its result (for a GUI agent, of the screen) over a recent window, and count a repeat only when the same call returns the same result or the same state recurs with no visible change; normalize search queries the same way to catch near-duplicates. A streak of calls to one tool with changing arguments is usually a retry, not a loop: after injected tool faults, agents called the same tool three or more times in a row in 12.5% to 22.2% of trials but with identical arguments in only 0.8% to 1.8%, and on SWE-bench Verified blind retries appeared in 46.0% of passing and 44.9% of failing runs (regression loops 38.7% and 39.5%), while cyclic patterns were more common in failing runs (44.5% against 33.6%) and wasted more steps there (7.8 against 4.6 per instance).
3. On a short streak, inject a message that names the repeated call and its count and requires a different approach, and escalate if the streak continues. Published harnesses warn at two to five identical calls (one study's harness at five identical calls or five identical failures, Hermes after two identical failures; OpenCode asks the user at three). In a desktop agent that forced a different interaction mode after two identical actions with no visible change and a new strategy after the same screen recurred three times, steps spent in loops fell from 4.9% to 2.8% (Gemini 3 Flash) and from 3.2% to 2.1% (Claude Sonnet 4.6); success rose 1.82 to 4.24 points for Gemini 3 Flash at 50 and 100 steps and 0.04 to 1.44 for Sonnet 4.6, but fell 6.15 points at a 15-step budget, where the escalation steps crowded out the task. In production, 94.29% of loops flagged by an asynchronous observer did not recur after one injected course correction (judged by an LLM). Neither a prompt line nor a silent refusal changes behavior on its own: refusing an exact repeat and returning the earlier result kept repeated calls from running (5.7% of tasks ran one, 46.7% tried) but the agent proposed already-run calls as often as before (71.3% of tasks against 69.8%) and used as many tokens (24.9k against 23.9k), so keep refusal only to avoid re-running calls with side effects (2.b.i); on that small model a reminder when stuck left steps (14.85 against 15.00) and success (23.7% against 25.1%) about where they were.
4. Keep a stop rule as a backstop, not a saving: end the run at a long streak of identical failures (eight in two published harnesses, one of which ships the stop disabled) or when the task's progress signal (step 5) has been flat for K turns, and return the best answer so far with the stop reason (9.b.i). Expect it to fire rarely and to cost successes when it fires early: on a small open model under aggressive summarization, ending the run when a stuck detector fired cut steps from 15.00 to 13.08 and tokens from 23.9k to 21.6k per task but success fell from 25.1% to 21.7% (one run), and a rule to abandon after four consecutive failures past 40% of the step budget never fired in 63 runs of a Claude Sonnet 5.5 terminal agent (without a controller, 10 of 17 failures ended at a timeout or cap instead). Repetition alone does not show a task is infeasible: require separate evidence before reporting failure.
5. Define 'no progress' for the task from what the run produces, not from its length: no new file or diff, test result, retrieved fact, screen state or change to the draft answer in K turns; the tool-step count alone ranked failing coding runs at chance (AUC 0.471 to 0.528). Put the detector in place before raising a turn cap, keep the cap and deadline as the hard bound (7.b.iii), track progress items explicitly where the task allows (7.b.iv), and make every stop path, detector or cap, return an extractable answer (9.b.i).
6. Keep detection cheap and test anything smarter end to end. Hashes and counters cost nothing; an LLM check after every action does not: a loop breaker whose top tier asked an LLM judge after each action cut actions per task from 16.80 to 14.28 but raised model calls from 28.40 to at least 41.52 and tracked tokens from at least 257,618 to at least 422,074, and the production observer ran its LLM classifier asynchronously at fixed intervals so the agent never waited on it. Compare any added controller against plain rules and a placebo: on a terminal benchmark, advisory messages at small failure and repetition streaks plus verify prompts at finish raised cost per attempt 24% (rules), 19% (a cheap decision model) and 47% (a small LLM) with no detectable pass-rate change, while random advice at the same moments did not raise cost (0.98 times). Don't add a learned stop monitor yet: one trained on past runs saved 4.5% of cost per retained solve at 99.0% retention for one agent, catching 5.0% of failing runs, and nothing for another, and stopping pays only when the execution it avoids exceeds the monitor's cost plus the successes it kills.
7. Measure on the same cases and model, at the step budgets you run, with several runs per arm: no detector, warning only, warning plus stop (and a placebo reminder when testing a controller); report the share of runs with a loop and of steps spent in loops, warnings issued and whether the repeated call recurred after them, stops and cap hits by reason, success overall and on the runs the stop ended (replay them without the stop to count the successes it cut), tokens, turns and wall-clock. Re-measure when the model changes: in one production sample the newer model looped more (3.59% against 2.18%).

## How to measure

- **experiment** (Tier 2): same cases and model at each step budget you run, several runs per arm: no detector, warning only, warning plus stop, and a placebo reminder at random moments when testing a controller; report the share of runs with a loop (same normalized call and result) and of steps spent in loops, stops and cap hits by reason, success overall and on the runs the stop ended (replayed without the stop), tokens, turns and wall-clock
- **monitor**: per model in production: share of runs with a loop, warnings issued and whether the repeated call recurred in the following steps, stops by reason, cap hits, tokens per session; re-run the experiment when the model or harness changes

## Expected impact

- **Quality:** mixed, small: forcing a change of approach at short streaks added 1.82 to 4.24 points on OSWorld and 5.2 to 7.8 on WindowsAgentArena for Gemini 3 Flash and 0.04 to 1.44 for Claude Sonnet 4.6, but cost 6.15 points at a 15-step budget (Han, Apr 2026); on a small open model, ending runs when a stuck detector fired cut success from 25.1% to 21.7% and a reminder gave 23.7% (Chen, Oct 2026); advisory recover and verify messages left a frontier terminal agent at 73.0% (Vats, Oct 2026); in VeRO, adaptive termination +5.6% on FACTS, an anti-loop prompt line +0.04 on GAIA and flat on SimpleQA (VeRO, Feb 2026)
- **Cost:** mixed, small: an observer that flagged loops and other misbehaviors and injected reminders cut tokens per session 5.3% in a production A/B test (Nanda, Feb 2026); ending stuck runs cut tokens per task from 23.9k to 21.6k, while refusing repeats saved nothing (24.9k) (Chen, Oct 2026); a loop breaker with an LLM judge after each action raised tracked tokens per task from at least 257,618 to at least 422,074 (Han, Apr 2026); advisory controllers raised cost per attempt 19% to 47% (Vats, Oct 2026); a learned stop monitor saved 4.5% of cost per retained solve for one agent and nothing for another (Liang, Oct 2026)
- **Performance:** mixed, small: forced changes cut steps spent in loops from 4.9% to 2.8% and actions per task from 16.80 to 14.28, but added model calls (28.40 to at least 41.52) (Han, Apr 2026); ending stuck runs cut steps per task from 15.00 to 13.08 (Chen, Oct 2026); session execution time -4.3% (not significant) with detection run asynchronously (Nanda, Feb 2026); advisory messages lengthened runs from 13.3 to 15.6 steps (9.4 to 9.5 minutes) (Vats, Oct 2026); VeRO's template with query dedup ran about 2x faster, bundled (VeRO, Feb 2026)
- **Governance:** improves, small (unmeasured): refusing an exact repeat kept repeated calls from running (5.7% of tasks ran one against 46.7% that tried) (Chen, Oct 2026), which matters where a repeated call has side effects (2.b.i); no source measures duplicated effects for this change
- **Brand:** improves, small (unmeasured): in a production A/B test an observer that corrected loops and other misbehaviors cut engineer interventions per session 4.2% (Nanda, Feb 2026); no source isolates loops or measures how users perceive the agent

## Evidence (summary)

- paper §A.4 (2026-02): Part of the Filesystem-B=178 commit; contributed to AgentTimeoutError rising 16 to 23 as crashing tasks migrated to timeouts rather than passes.
- cookbook (master-agent-optimization-cookbook, Infinite Loop Prevention) (2026-02): Hash recent tool calls, inject a warning on repeat.
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Held fixed across all conditions. A reminder is inserted once per streak at five identical calls (same tool name, byte-identical arguments) of any status or five identical failing calls, and an identical failing streak of eight ends the…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes hashes the call signature (SHA-256), "warning after two identical failures and halting after eight—but the hard stop ships disabled"; Gemini CLI aborts on "five identical tool calls or ten identical content chunks"; OpenCode's…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI LoopDetectionService: "after thirty turns in a single prompt an LLM-based self-check runs at an adaptive interval—a two-tier design"; paper calls this a "platform-tier investment".
- …and 12 more sources in `library/entries/detect-loops-and-stalls.yaml`.

## Caveats

Most of the measured evidence is small, bundled or from single runs: the desktop study reports single point estimates with fixed, unswept thresholds and an LLM judge inside its loop breaker; the production A/B test bundles loops with other misbehaviors and judges recovery with an LLM; the stuck-stop, reminder and blocker controls ran once on one benchmark with an 8B open model under aggressive 4,096-token summarization; and VeRO's items come from bundled optimizer runs. Stopping is the least supported part: ending stuck runs lost 3.4 points on that small model, a rule-based abandon never fired for a frontier terminal agent across 63 runs, advisory controllers raised cost with no gain on 21 tasks, and a learned stop monitor saved 4.5% for one agent and nothing for another, so treat the stop as a backstop to test. Repetition is not failure: identical repeats were rare after tool faults while retries with changed arguments were common, blind retries were as frequent in passing coding runs as in failing ones, and the one fix that removed most loops in the summarization study was training on the agent's own loops (57.3% to 6.1%), not a harness rule. Gains depend on model and budget, and newer is not safer: a loop-prone model gained up to 4.24 points from forced changes where a strong one gained 0.04 at 100 steps, and in production Claude Opus 4.5 looped more often than Claude Sonnet 4.5 (3.59% against 2.18%).

## Related

- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:tune-search-tool` (8.b.i, Tune the search tool: snippets, enough results, retries, reformulation, filters, source quality)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)

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
