---
name: initializer-maintainer-agents
description: "AOT optimization 4.b.ii (Tier 4, Restructuring): Initializer-maintainer dual agent. Placeholder. Use when an agent shows: Session handoffs; progress file updates; whether each session starts by reading state and running the smoke test; items removed or reworded in the feature list; sessions declaring the project done with items failing; a first-session plan never revised after tests expose new defects."
---

<!-- Generated from library/entries/initializer-maintainer-agents.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Initializer-maintainer dual agent

> **Placeholder.** Generated from `library/entries/initializer-maintainer-agents.yaml` (entry 4.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.b.ii |
| Earlier id | P46 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it splits the work across two agents |
| Categories | Memory: Resuming |
| Change | workflow / orchestration |

## What it is

Give the first session of a multi-session build a setup-only prompt (expand the spec into a JSON list of end-to-end tests, all failing, and write an init script, a progress file and a first commit) and every later session a maintainer prompt that reads that state, re-tests what passed, builds one failing item, verifies it end to end and commits. A separate up-front spec step pays when the model would otherwise start building and under-scope, and it is cheap: Anthropic kept its planner on Opus 4.6 for that reason at $0.46 of a $124.70 run, and in one controlled study a planning call before a single development pass raised a game-building score from 49.58 to 59.71. Freezing that first plan is the weak part: in the same study a plan written once and built over three fresh sessions scored 63.39, above 58.24 for one session continued for three passes but below 71.52 when each session replanned from test results, and Cursor dropped its one-time planner as too rigid. No study compares the split with one agent keeping the same state files (4.b.iii), Anthropic's two "agents" differ only in their first prompt, and strong models narrow the need: one Codex session ran about 25 hours on spec, plan and status files.

## When it applies

- **In the code:** Two entry points; a progress file and feature list; bootstrap and per-session flows.
- **In traces:** Session handoffs; progress file updates; whether each session starts by reading state and running the smoke test; items removed or reworded in the feature list; sessions declaring the project done with items failing; a first-session plan never revised after tests expose new defects.
- **In eval results:** Multi-session completion rate.
- **Probes:** A multi-session project.

## How (outline)

1. Start from one agent with one prompt that keeps the 4.b.iii state files (spec, plan, progress log, git history) in one continuous session with compaction, and log what goes wrong across a multi-session build: it starts building before it specs and under-scopes, tries to one-shot and runs out of context mid-feature, declares the job done early, or breaks features that had passed. A strong model may need nothing more: one Codex session with a spec, a milestone plan it wrote first, a runbook and a status file ran about 25 hours.
2. If it under-scopes or one-shots, give the first session a setup-only prompt on the same harness, tools and system prompt (in Anthropic's version the first user prompt is the only difference), chosen by the harness when no feature list exists yet. It expands the spec into a JSON list of end-to-end tests ordered by priority, each with steps and all failing (over 200 for Anthropic's claude.ai clone), and writes an init script that installs, starts the app and runs a smoke test, a progress file and a first git commit. Keep it at product level rather than implementation detail, since spec errors cascade downstream; ask for a concrete number of items ("20-100 tasks", not "many"); and review the spec itself, since a weak one set Cursor's first browser on an architecture that could not grow into a full browser.
3. Give every later session a maintainer prompt with a fixed contract: read the progress file, the list and the git log; run the init script and re-test one or two core passing items, marking any regression failing and fixing it first; take the highest-priority failing item and only that; verify it end to end as a user would (browser automation for a web app); change only that item's status; commit, update the progress file and leave a merge-ready state.
4. Let the plan move with the evidence instead of freezing it: allow each session, or a planning step at its start that cannot edit code, to append items for defects and requirements the build exposes and to re-prioritize, never to delete or weaken an item. In one study a plan frozen after the first loop scored 63.39 against 71.52 when it was revised each loop from test results.
5. Keep each role narrow: check each session's work outside the maintainer's own pass flags (7.c.iii, 9.b.iii), and do not give one agent planning, coding, review, merging and the completion decision at once; Cursor's agent that held all of them stalled and claimed premature completion.
6. Measure with paired runs on the same specs and model at matched sessions and tokens: one agent with the 4.b.iii files, setup plus maintainer, and setup plus a maintainer that may append items; score with an end-to-end suite the agents never see (features passing, spec features never built, regressions reopened), plus tokens, the setup session's share and wall time; re-run after a model upgrade, since Anthropic dropped context resets for Opus 4.5 and sprints for Opus 4.6 but kept the planner.

## How to measure

- **experiment** (Tier 4): paired runs on the same specs and model at matched sessions and tokens: one agent with the 4.b.iii state files in one continuous session; a setup-only first session plus maintainer sessions; the same with the maintainer allowed to append items from test results; score with an end-to-end suite the agents never see (features passing, spec features never built, regressions reopened), plus total tokens, the setup session's share and wall time; per model, and again after an upgrade
- **monitor**: per session: whether it read the progress file, list and git log and ran the smoke test before new work; regressions found at session start; items marked passing that fail the hidden suite; items removed or reworded in the list (should be zero); items added from test findings; sessions per item; sessions that declare the project done with items still failing

## Expected impact

- **Quality:** improves, medium: multi-session builds where the model under-scopes or one-shots: a separate planning call before one development pass 49.58 to 59.71 on 45 game builds; a plan frozen after the first loop and built in fresh sessions 63.39 against 58.24 for one session continued for the same three passes, and 71.52 when each loop replanned from test results (Yan, Sep 2026); without its planner Opus 4.6 under-scoped (Rajasekaran, Mar 2026); one-time up-front planning was too rigid to readjust and was removed (Lin, Feb 2026); no study against one agent keeping the same state files
- **Cost:** mixed, small: the setup session is a small share: planner $0.46 of $124.70 (Rajasekaran, Mar 2026); a planning call before one pass 2.88M against 2.59M tokens per task; three fresh-session loops 8.41M (frozen plan 7.56M) against 6.33M for three passes of one continued session, but 3.77 against 2.32 points per extra million tokens, and rebuilding from scratch each loop instead of continuing raised tokens to 11.12M (Yan, Sep 2026); planner, sprints and evaluator together cost $200 against $9 for a solo run (Rajasekaran, Mar 2026)
- **Performance:** degrades, small (unmeasured): the setup session adds minutes, not hours: planner 4.7 min of a 3 hr 50 min run (Rajasekaran, Mar 2026); Anthropic's quickstart warns the first session takes 10-20+ minutes and each coding session 5-15 (Young, Nov 2025); every later session re-reads state and re-runs a smoke test before new work; no source compares wall time with one agent
- **Security:** none (unmeasured)
- **Governance:** improves, medium (unmeasured): a commit and progress-log entry per session and an issue record make each session's work reviewable; a 70-loop build kept 81 issues on record, 17 of them reopened after later changes broke verified behavior (Yan, Sep 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Justin Young (Anthropic), "Effective harnesses for long-running agents"… (2025-11-26): "an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session." The two are one harness: "We…
- Haoyang Yan, Min-Le Su, Hangfan Zhang, Zhanhao Li, Chen Zhang, Shao Zhang, Yang Chen, Lei Bai, Shuyue Hu (Shanghai AI Laboratory)… (2026-09-01): GameCraft-Bench Overall, Codex with GPT-5.5 (high), 45 tasks: one pass 49.58 (2.59M tokens per task); after the first loop 59.71 (2.88M); one session continued for two and three passes 54.99 (4.56M) and 58.24 (6.33M); HoH after two and…
- Prithvi Rajasekaran (Anthropic), "Harness design for long-running application development"… (2026-03-24): The planner survived the ablation: "Without the planner, the generator under-scoped: given the raw prompt, it would start building without first speccing its work, and end up creating a less feature-rich application than the planner did."…
- Derrick Choi (OpenAI), "Run long horizon tasks with Codex", https://developers.openai.com/blog/run-long-horizon-tasks-with-codex (2026-02-23): "Codex ran for about 25 hours uninterrupted, used about 13M tokens, and generated about 30k lines of code." "The most important technique was durable project memory. I wrote the spec, plan, constraints, and status in markdown files that…
- …and 1 more sources in `library/entries/initializer-maintainer-agents.yaml`.

## Caveats

No study isolates the split as Anthropic built it, two first prompts on one harness, against one agent keeping the same state files (4.b.iii); the one controlled comparison is one framework, one model setup and 45 game-building tasks with one run each, and its roles add an independent tester and per-loop planning. The vendor accounts (Anthropic, Cursor, OpenAI) are single builds judged by their authors, mostly on the vendors' own models, with no quality numbers. The advice conflicts on freezing the plan: Anthropic forbids editing the test list, while a frozen first plan lost 8.13 points to per-loop replanning and Cursor dropped up-front planning as too rigid; an append-only list sits between them and is untested. The need shifts with the model: Anthropic dropped resets for Opus 4.5 and sprints for Opus 4.6 but kept the planner, and one Codex session ran about 25 hours without a separate setup role.

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)
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
