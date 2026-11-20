---
name: initializer-maintainer-agents
description: "AOT optimization 4.b.ii (Tier 4, Restructuring): Initializer-maintainer dual agent. Placeholder. Use when an agent shows: Session handoffs; progress file updates; whether each session starts by reading state and running the smoke test from a clean install; items removed or reworded in the feature list; agent commits that loosen tests or CI checks; sessions declaring the project done with items failing; builds that work in the session's environment but fail a clean install; a first-session plan never revised after tests expose new defects."
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

Have the first session of a long build write a failing end-to-end test list, an init script and a progress file, and have every later session re-test what passed, build and verify one item, and commit. It pays when the model would otherwise under-scope, one-shot or stop early, and when items count as done only on a check the builder cannot write: a planning call before one development pass raised a game-building score from 49.58 to 59.71, Anthropic kept its planner on Opus 4.6 at $0.46 of a $124.70 run, and a harness that kept the requirement list outside fresh one-subtask sessions and closed items only on a read-only audit raised WeaveBench pass rate from 51.8% to 80.7% over one session with the same model. Freezing the plan and letting agents edit their own checks are the weak parts: a plan frozen after the first loop scored 63.39 against 71.52 when each loop replanned from test results, Cursor dropped its one-time planner as too rigid, and in an agent factory whose agents filed 95% of new issues, 7 of their 40 CI changes loosened checks. Strong models narrow the need, and no study compares the split with one agent keeping the same state files (4.b.iii): one Codex session ran about 25 hours, and one conversation with compaction delivered fully working full-stack products in 64.7% of builds with GPT-6.1 Sol.

## When it applies

- **In the code:** Two entry points; a progress file and feature list; bootstrap and per-session flows.
- **In traces:** Session handoffs; progress file updates; whether each session starts by reading state and running the smoke test from a clean install; items removed or reworded in the feature list; agent commits that loosen tests or CI checks; sessions declaring the project done with items failing; builds that work in the session's environment but fail a clean install; a first-session plan never revised after tests expose new defects.
- **In eval results:** Multi-session completion rate.
- **Probes:** A multi-session project.

## How (outline)

1. Start from one agent with one prompt that keeps the 4.b.iii state files (spec, plan, progress log, git history) in one continuous session with compaction, and log what goes wrong across a multi-session build: it starts building before it specs and under-scopes, tries to one-shot and runs out of context mid-feature, declares the job done early, or breaks features that had passed. A strong model may need nothing more: one Codex session with a spec, a milestone plan it wrote first, a runbook and a status file ran about 25 hours, and one conversation with compaction built full-stack products over 9 to 18 feature requests, fully working in 64.7% of builds with GPT-6.1 Sol and 48.5% with Opus 5.5. Early stops are the failure to look for: 26% of single-session program rebuilds submitted failing work with over 90% of their budget left.
2. If it under-scopes, one-shots or skips requirements, give the first session a setup-only prompt on the same harness, tools and system prompt (in Anthropic's version the first user prompt is the only difference), chosen by the harness when no feature list exists yet. It expands the spec into a JSON list of end-to-end tests ordered by priority, each with steps and all failing (over 200 for Anthropic's claude.ai clone), with a test for every stated requirement, since agents skip what no test checks: in one benchmark missed requirements were mostly those the visible tests left unclear, and withholding the visible tests often cut complex rebuilds from 95% or more of held-out tests passed to below 50%. It also writes an init script that installs from a clean environment, starts the app and runs a smoke test, a progress file and a first git commit. Keep it at product level rather than implementation detail, since spec errors cascade downstream; ask for a concrete number of items ("20-100 tasks", not "many"); and review the spec itself, since a weak one set Cursor's first browser on an architecture that could not grow into a full browser.
3. Give every later session a maintainer prompt with a fixed contract: read the progress file, the list and the git log; run the init script from a clean install (fresh container, empty database) and re-test one or two core passing items, marking any regression failing and fixing it first; take the highest-priority failing item and only that; verify it end to end as a user would (browser automation for a web app); change only that item's status; commit, update the progress file and leave a merge-ready state. The clean install matters: in one benchmark's reference runs every build that failed all of its test plans used a database table before creating it, which only a clean install exposes.
4. Let the plan move with the evidence instead of freezing it: allow each session, or a planning step at its start that cannot edit code, to append items for defects and requirements the build exposes and to re-prioritize, never to delete or weaken an item. In one study a plan frozen after the first loop scored 63.39 against 71.52 when it was revised each loop from test results. Keep the tests and CI checks that judge the items out of the agents' unreviewed reach: in an agent factory where agents filed 95% of 704 new issues, they also wrote 40 of 58 CI-workflow changes, 7 of which loosened checks, and at least 5.6% of issues marked fixed were wrong fixes.
5. Keep each role narrow and mark an item passing only on evidence the maintainer cannot write (7.c.iii, 9.b.iii): a harness whose manager kept the requirement list without touching the environment, gave a fresh executor one subtask per round and closed items only on a read-only auditor's evidence raised WeaveBench pass rate from 51.8% to 80.7% and Terminal-Bench 2.1 from 69.7% to 77.2% over one Claude Code session with the same model. Do not give one agent planning, coding, review, merging and the completion decision at once; Cursor's agent that held all of them stalled and claimed premature completion.
6. Measure with paired runs on the same specs and model at matched sessions and tokens: one agent with the 4.b.iii files, setup plus maintainer, and setup plus a maintainer that may append items; score with an end-to-end suite the agents never see, run on a clean install (features passing, spec features never built, regressions reopened), plus tokens, the planning and checking roles' shares (a manager used 2.0% to 8.1% and an auditor 19.4% to 38.1% of tokens in one study) and wall time, and count the edits agents make to tests or checks; re-run after a model upgrade, since Anthropic dropped context resets for Opus 4.5 and sprints for Opus 4.6 but kept the planner, and one-conversation builds went from 3.1% to 53.1% fully working across three releases of one model family.

## How to measure

- **experiment** (Tier 4): paired runs on the same specs and model at matched sessions and tokens: one agent with the 4.b.iii state files in one continuous session with compaction; a setup-only first session plus maintainer sessions; the same with the maintainer allowed to append items from test results; score with an end-to-end suite the agents never see, run on a clean install (features passing, spec features never built, regressions reopened), plus total tokens, the planning and checking roles' shares and wall time; several runs per spec, per model, and again after an upgrade
- **monitor**: per session: whether it read the progress file, list and git log and ran the init script and smoke test from a clean install before new work; regressions found at session start; items marked passing that fail the hidden suite; items removed or reworded in the list (should be zero); items added from test findings; edits agents make to tests or CI checks, and whether each was reviewed; sessions per item; sessions that declare the project done with items still failing

## Expected impact

- **Quality:** improves, medium: multi-session builds where the model under-scopes, one-shots or stops early: a separate planning call before one development pass 49.58 to 59.71 on 45 game builds; a plan frozen after the first loop and built in fresh sessions 63.39 against 58.24 for one session continued for the same three passes, and 71.52 when each loop replanned from test results (Yan, Sep 2026); a requirement list kept outside fresh one-subtask sessions, with items closed only on a read-only audit, 51.8% to 80.7% on WeaveBench and 69.7% to 77.2% on Terminal-Bench 2.1 against one Claude Code session with the same model (Ma, Aug 2026); without its planner Opus 4.6 under-scoped (Rajasekaran, Mar 2026); one-time up-front planning was too rigid to readjust and was removed (Lin, Feb 2026); the baseline is strong on current models: one conversation with compaction delivered fully working products in 64.7% of builds with GPT-6.1 Sol (Furman, Nov 2026), and single compacted sessions rebuilt a 16,000-line toolkit in 14 hours but submitted failing work with over 90% of budget left in 26% of runs (Adamczewski, Jun 2026); no study against one agent keeping the same state files
- **Cost:** mixed, medium: the setup and planning roles are a small share: planner $0.46 of $124.70 (Rajasekaran, Mar 2026); a manager 2.0% to 8.1% of tokens, but with its auditor (19.4% to 38.1%) the loop used 2.3 times the single session's tokens on WeaveBench and 3.6 times the output tokens on OSWorld, 24% fewer on Terminal-Bench, and fewer for Opus 4.7 (11.1M against 16.5M per game task) but more for Qwen 3.7-Plus (34.3M against 10.7M) (Ma, Aug 2026); a planning call before one pass 2.88M against 2.59M tokens per task; three fresh-session loops 8.41M (frozen plan 7.56M) against 6.33M for three passes of one continued session, but 3.77 against 2.32 points per extra million tokens, and rebuilding from scratch each loop instead of continuing raised tokens to 11.12M (Yan, Sep 2026); planner, sprints and evaluator together cost $200 against $9 for a solo run (Rajasekaran, Mar 2026)
- **Performance:** degrades, small (unmeasured): the setup session adds minutes, not hours: planner 4.7 min of a 3 hr 50 min run (Rajasekaran, Mar 2026); Anthropic's quickstart warns the first session takes 10-20+ minutes and each coding session 5-15 (Young, Nov 2025); every later session re-reads state and re-runs a smoke test before new work; no source compares wall time with one agent
- **Security:** none (unmeasured)
- **Governance:** mixed, medium: a commit, progress-log entry and issue record per session make the work reviewable: a 70-loop build kept 81 issues on record, 17 of them reopened after later changes broke verified behavior (Yan, Sep 2026); in an agent factory a second person approved 534 of 541 merged PRs, but agents filed 95% of new issues and wrote 40 of 58 CI-workflow PRs, 7 of which loosened checks, and at least 5.6% of issues marked fixed were wrong fixes, so the record is only as trustworthy as checks the agents cannot change unreviewed (Jiang, Oct 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Justin Young (Anthropic), "Effective harnesses for long-running agents"… (2025-11-26): "an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session." The two are one harness: "We…
- Haoyang Yan, Min-Le Su, Hangfan Zhang, Zhanhao Li, Chen Zhang, Shao Zhang, Yang Chen, Lei Bai, Shuyue Hu (Shanghai AI Laboratory)… (2026-09-01): GameCraft-Bench Overall, Codex with GPT-5.5 (high), 45 tasks: one pass 49.58 (2.59M tokens per task); after the first loop 59.71 (2.88M); one session continued for two and three passes 54.99 (4.56M) and 58.24 (6.33M); HoH after two and…
- Prithvi Rajasekaran (Anthropic), "Harness design for long-running application development"… (2026-03-24): The planner survived the ablation: "Without the planner, the generator under-scoped: given the raw prompt, it would start building without first speccing its work, and end up creating a less feature-rich application than the planner did."…
- Derrick Choi (OpenAI), "Run long horizon tasks with Codex", https://developers.openai.com/blog/run-long-horizon-tasks-with-codex (2026-02-23): "Codex ran for about 25 hours uninterrupted, used about 13M tokens, and generated about 30k lines of code." "The most important technique was durable project memory. I wrote the spec, plan, constraints, and status in markdown files that…
- …and 5 more sources in `library/entries/initializer-maintainer-agents.yaml`.

## Caveats

No study isolates the split as Anthropic built it, two first prompts on one harness, against one agent keeping the same state files (4.b.iii), and none tests an append-only list; the two controlled comparisons come from their authors' own frameworks, bundle per-round planning and an independent tester or auditor with the fresh sessions, and neither matches tokens, one matching passes and the other nothing (45 game builds with one run each; WeaveBench, OSWorld and Terminal-Bench tasks rather than app builds, with the OSWorld baselines on a different tool set). The vendor accounts (Anthropic, Cursor, OpenAI) are single builds judged by their authors, and the factory observations come from two deployments of two to three weeks at one company. The advice conflicts on freezing the plan: Anthropic forbids editing the test list, while a frozen first plan lost 8.13 points to per-loop replanning and Cursor dropped up-front planning as too rigid, yet agents allowed to change their own CI loosened checks. The need and the cost shift with the model and task: Anthropic dropped resets for Opus 4.5 and sprints for Opus 4.6 but kept the planner, one Codex session ran about 25 hours, one-conversation full-stack builds went from 3.1% to 53.1% fully working across three releases of one model family, and one round-based loop used 24% fewer tokens than a single session on one benchmark and 2.3 times as many on another.

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
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
