---
name: track-task-progress
description: "AOT optimization 7.b.iv (Tier 3, Tuning): Track explicit progress: a task list with a status per item, re-injected each turn. Placeholder. Use when an agent shows: runs ending with no edit, output or answer file, or at a timeout, and short aimless trajectories (models that stop early); long post-edit verification loops (stronger models); list updates a large share of all actions; no update for many turns; items marked done with no evidence, or still open when the agent stops; failure rows labeled goal-drift or state-tracking-failure."
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

Give the agent one tool that holds a task list (a status per item, one item in progress), require the list on the first turn of non-trivial tasks, and show the current list every turn instead of keeping old copies in history. It pays mainly for models that would otherwise stop early or drop work: in controlled studies it added 11.6 points on SWE tasks for a 30B model and kept an open 120B model working through long browser workflows (0.18 lower, to about zero, without it), while strong models gained little (0.77 to 1.36 points on repository generation) or traded about 2 points of success for about 30% lower cost on SWE tasks. Writing a list is not enough on its own: a TODO list the model wrote once at the start moved workspace pass rate between -3.90 and +1.66 points across three models, while a record kept by the harness, with done marks checked against what the agent read and a finish check of open items, gained 3.10 to 15.49 points (in the one model ablated, the gain disappeared without the harness's own capture of reads and its checks). Updates cost tokens and actions (21.10% more prompt tokens for one model; maybe a third of actions in some tasks, by one vendor's account), so measure per model and re-run after a model change.

## When it applies

- **In the code:** no task list or todo mechanism in the harness, or a list the model writes once in its reply that the harness never shows again
- **In traces:** runs ending with no edit, output or answer file, or at a timeout, and short aimless trajectories (models that stop early); long post-edit verification loops (stronger models); list updates a large share of all actions; no update for many turns; items marked done with no evidence, or still open when the agent stops; failure rows labeled goal-drift or state-tracking-failure
- **In eval results:** success and answer rate (runs ending with the required output), turns and tokens, by trajectory length, per model and task type
- **Probes:** Long tasks whose output needs many separate items found at different steps or in different files

## How (outline)

1. Start from the baseline: run your eval set per model with no list and record success, cost, tokens, turns, runs that end without the required output (no edit, no answer file) or at a timeout, and items the task asks for that are missing from the output. Expect the list to matter where runs end early or drop items: without a plan, a 30B coding model ended 68.6% of SWE runs without an edit (27.8% with one) at a median of 5 turns (40 with one); an open 120B model's browser workflows fell from a median of 176.5 to 63 turns; and a plain workspace agent left about one in five numeric values it had been shown (19.8%) out of its deliverable. Report the answer rate next to the score: at similar scores, a 35B model without a plan left 47 of 96 tool-task episodes without the required output against 24 with one, and timed out twice as often (44 against 22).
2. Add one task-list tool whose every call re-sends the complete list (each item with its text and a status: pending, in_progress or completed; exactly one in_progress), and have the harness validate each call (item format, allowed statuses, a length cap such as 10 items, consistency) and return a clear error when it fails. Require it on non-trivial tasks: a system instruction to make the first action a list for any task of about three or more steps (skip a single trivial step or a purely informational request), a reminder each turn until a list exists, and an instruction to mark an item completed as soon as it is actually done, not in batches.
3. Keep only the latest list in the harness and show it fresh before every model call, never as a copy in history: one study appended it to the end of the model input as a reminder block, another appended a one-line status of open items to each tool result. No source compares the end of the context with a block after the system prompt or a file; appending at the end leaves the cached prefix unchanged (3.b.i). If the list has not been updated for several turns, inject a reminder to update it.
4. Keep updates cheap and count them: the list costs actions and tokens. In one coding study it raised prompt tokens 21.10% for one model and 3.51% for another; Manus's co-founder recalled that maybe a third of actions in some of its tasks went to updating a todo file, and Manus moved planning to a separate planner agent. Log list updates as a share of all actions; if the share is large, ask for updates only when an item changes status, or move planning to a planner.
5. Keep the list honest: a done mark should rest on evidence the harness can check, not on the model's say-so. Have the agent cite what completes an item (a passing test, a written file, an excerpt it read) and refuse a done that cites nothing relevant; let the harness record what it can observe itself (files read, files listed but never opened) instead of asking the model to write it down; and before the agent stops, return the items still open (9.b.iii). In one workspace study a TODO list the model wrote at the start moved pass rate between -3.90 and +1.66 points across three models, while a harness-kept record of requirements, reads and unopened files, with evidence-checked done marks and a finish check, gained 3.10 to 15.49 points; removing the evidence check or the finish check each cost 1.84 points, and without the harness's own record of reads (and the review and evidence check built on it) the pass rate fell to 41.36, level with the plain agent's 41.63.
6. Measure per model and task type, with several runs per arm, with and without the list: success and answer rate, cost, tokens, turns, timeouts, list updates as a share of actions, items marked done without evidence and items still open at the finish. Expect the sign to depend on the model: the list added 11.6 points on SWE tasks for a 30B model that otherwise stopped early, 0.77 to 1.36 points for two strong models on repository generation, and no clear score change for a 35B model on clinical tasks, and it cost strong coding models 2.0 and 0.4 points of success while cutting their SWE cost about 30% by trimming post-edit verification. Re-run it when the model changes.

## How to measure

- **experiment** (Tier 3): paired eval with and without the task list, separately for each model and task type you run, several runs per arm: success and answer rate, cost, tokens, turns, timeouts, list updates as a share of actions, items marked done without evidence and items still open at the finish; re-run after a model change
- **monitor**: per model in production: share of non-trivial runs that create a list, list updates as a share of actions, turns since the last update, items marked done without evidence or still open when the agent stops, and runs ending without the required output

## Expected impact

- **Quality:** mixed, medium: a 30B model +11.6 points on SWE tasks and +4.5 on Terminal-Bench, no consistent gain at 120B, strong models -2.0 and -0.4 (Fan, Sep 2026); +1.36 and +0.77 points on repository generation for two strong models (Hu, Sep 2026); without it an open 120B model lost 0.18 on long browser workflows, while a 35B model kept its scores but left twice as many tool-task episodes without the required output (Wang, Oct 2026); a TODO list written once at the start moved workspace pass rate -3.90 to +1.66 points, a harness-kept record +3.10 to +15.49 (Baek, Oct 2026)
- **Cost:** mixed, medium: strong models about 30% and 32% cheaper on SWE tasks (fewer post-edit turns), while the 30B model's cost per task rose from $0.02 to $0.09 on SWE tasks and 75% on Terminal-Bench because it now works the task (Fan, Sep 2026); prompt tokens +21.10% and +3.51% (Hu, Sep 2026); about five times the tokens on browser workflows for the model it kept working (Wang, Oct 2026); maybe a third of actions spent updating a todo file in some production tasks, by the vendor's recollection (Ji, Oct 2025)
- **Performance:** mixed, medium: follows turns: median SWE turns 108 to 74 and 68 to 53 for strong models, 5 to 40 for the 30B model (Fan, Sep 2026); steps -1.86% and -1.07% (Hu, Sep 2026); median browser-workflow turns 63 without the plan, 176.5 with it (Wang, Oct 2026)

## Evidence (summary)

- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Protocol: a system instruction requires update_plan as the first action on any non-trivial task (about 3+ steps), a first-turn reminder repeats this until a plan exists, each call re-sends the complete list with exactly one task…
- Jinheon Baek, Soyeong Jeong, Yumin Choi, Dongsu Han, Sung Ju Hwang, "RunningTab: Direct Workspace Interaction with Environment-Side Tabs"… (2026-10-07): Workspace-Bench rubric pass rate, DCI / TODO / Self-Tracking / RunningTab: GPT-5.4 nano 41.63 / 41.67 / 42.93 / 44.73; DeepSeek V4 Flash 53.28 / 54.94 / 53.56 / 59.99; Gemini 3.8 Flash 31.42 / 27.52 / 26.87 / 46.91. TheAgentCompany score…
- Ziqing Wang, Lili Zhao, Kaize Ding, "MedicalHarness: A Controlled Evaluation of LLMs and Agent Harnesses on Medical Tasks"… (2026-10-05): Paired change in outcome without planning (95% bootstrap CI): GPT-OSS-120B MedWeb -0.18 [-0.29, -0.08] from 0.18 (process -0.19), median turns on 60 paired episodes 176.5 to 63, tokens x0.2; GPT-OSS-120B MedTool -0.02 [-0.04, +0.01]…
- Haichuan Hu, Quanjun Zhang, Shengcheng Yu, Zhifei Chen, Tianyu Luo, Chunrong Fang, Zhenyu Chen, Liang Xiao, "Beyond the Model: Demystifying… (2026-09-26): ProgramBench score +1.36 points from 42.88 (Qwen3.7-Max) and +0.77 from 45.14 (DeepSeek-V4-Pro): "Explicit planning yields small gains for both ... but planning alone is insufficient to substantially improve repository generation." Per…
- Yichao "Peak" Ji (Manus) with Lance Martin (LangChain), "Context Engineering for AI Agents with LangChain and Manus" (webinar)… (2025-10-14): Ji, recalling Manus logs from around March or April 2025: in some tasks "maybe" one-third of actions were updates to the todo list, which "wastes a lot of" tokens; Manus now has a separate planner agent, called as a tool, manage the plan…

## Caveats

The evidence is small: four controlled studies on coding, clinical tool and browser, and workspace tasks, two of them with one run per setting; none tests a frontier closed model with and without the list, and none compares where in the context the list is shown. The effect follows whether a model would otherwise stop early, not size alone: the list kept a 30B coding model and an open 120B browser agent working, left a 35B model's scores unchanged (though without it the model left the required output missing twice as often), and on strong coding models mostly cut post-edit verification, trading a little success for cost. Agents do not use or honor a list reliably: one small model stated its requirements before the finish check in only 56.9% of attempts, a TODO list written at the start hurt one of three models, and a harness-kept requirement list with a finish check but without the harness's record of reads did no better than the plain agent (41.36 against 41.63). Updating the list costs actions and tokens (maybe a third of actions in some Manus tasks, by its co-founder's recollection), and keeping the plan in a file only matters when work outlives one context window (4.b.iii).

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:inject-runtime-context` (3.a.iii, Dynamic context injection)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)
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
