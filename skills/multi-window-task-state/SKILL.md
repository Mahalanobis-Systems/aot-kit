---
name: multi-window-task-state
description: "AOT optimization 4.b.iii (Tier 4, Restructuring): Keep plan, progress and results in files when work outlives one context window. Placeholder. Use when an agent shows: Context resets followed by re-exploration or redone steps; notes written but never read back; user constraints or decisions violated after compaction; work declared done after a reset; state files older than the code they describe."
---

<!-- Generated from library/entries/multi-window-task-state.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Keep plan, progress and results in files when work outlives one context window

> **Placeholder.** Generated from `library/entries/multi-window-task-state.yaml` (entry 4.b.iii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.b.iii |
| Earlier id | P21 (Long-Horizon, from the master cookbook) |
| Tier (proposed) | 4 (Restructuring): it moves task state outside the context window |
| Categories | Memory: Resuming; Memory: Externalizing state |
| Change | workflow / state_management |
| Also covers | Structured note-taking; File system as external memory; Proactive state externalization |

## What it is

When a task spans context resets (compaction, a truncation limit, a new session), have the agent keep what the next window needs in files and read them back at the start of each window: the plan and a progress list, decisions and open items, intermediate results too large to hold in context, and for coding a structured test list and an init script. In measured studies, mostly of deep-research and long-horizon coding agents, state kept outside the history beat a growing or compacted one: Anthropic's memory tool plus context editing gained 39% on agentic search against 29% for context editing alone. The limits: model-written notes were incomplete or never read back, a stale file misled agents more than no file, and a stronger model needed resets less. Within one window this adds nothing a re-injected task list (7.b.iv) doesn't.

## When it applies

- **In the code:** A plan or todo file, a progress log, a decisions and open-items file, and for coding a structured test list and an init script, kept outside the context window, plus a start-of-window step that reads them back.
- **In traces:** Context resets followed by re-exploration or redone steps; notes written but never read back; user constraints or decisions violated after compaction; work declared done after a reset; state files older than the code they describe.
- **In eval results:** Completion rate and redone work on tasks longer than one window, with a reset forced midway.
- **Probes:** Tasks longer than one context window.

## How (outline)

1. Start from the harness as it is (compaction or truncation only) on tasks that really run past one window, and log what breaks after each reset: work redone, decisions or user constraints lost, work declared done too early.
2. In the first window, before real work, have the agent create the state files: a structured list of features or tests (JSON, every item failing, with an instruction that items are never removed or rewritten, only marked passing), a free-text progress log, a decisions and open-items file that also holds the user's constraints, and for coding an init script that starts the app and runs a smoke test; commit them to git.
3. Write large intermediate results (sources, query results, documents, logs) to files and keep only the path and a one-line note in context.
4. Start every later window with a fixed resume step written into the prompt: read the progress log, the decisions file, the test list and the git log, run the init script and the smoke test, then take one open item. Do not leave reading optional; agents write notes they never read.
5. Update at fixed points: when an item passes an end-to-end check, mark it, append to the log and commit; before a reset, write the handoff. Rewrite the files in place so they describe the present and delete stale entries, because agents follow a written file over the code.
6. Keep harness-side safety nets instead of relying on model-written notes alone: keep compaction or the harness's own state capture, re-append the constraint list after every compaction, and choose a fresh window or compaction per model.
7. Measure with paired runs that force a reset midway, with and without the files and the resume step: completion, steps redone, constraint violations after the reset, tokens and wall time, per model; re-run after a model change.

## How to measure

- **experiment** (Tier 4): paired runs on tasks longer than one window, forcing a reset (or capping the window) midway: the harness as is against the same harness with state files and a fixed resume step; completion, steps redone after the reset, constraint violations after the reset, tokens and wall time, per model; re-run after a model change
- **monitor**: per reset: whether the first actions read the state files, steps redone, items marked done that fail their test, state files older than the code or plan they describe, and the share of tokens spent writing notes

## Expected impact

- **Quality:** improves, medium: tasks past one window: memory tool plus context editing +39% against +29% for context editing alone (Anthropic, Sep 2025); a report rewritten into each rebuilt context +12.7 (o3) and +19.2 (DeepSeek-V3.1) points on BrowseComp over ReAct (Chen, Nov 2025); without todo, checklist and log files 52.76 to 48.69 RACE on 10 queries (Zhu, Feb 2026); model-written notes alone degraded Devin (Cognition, Sep 2025); a stale convention file cut better-form decisions from 33% with no file to 0% (Mohammadi, Aug 2026)
- **Cost:** mixed, small: file I/O under 0.03% of wall time (Zhu, Feb 2026); resets add token overhead (Rajasekaran, Mar 2026); an agent sometimes spent more tokens writing summaries than solving the problem (Cognition, Sep 2025); no study reports tokens for the files alone
- **Performance:** mixed, small: with a state-recovery memory, minutes per DeepSWE task rose from 42.0 to 54.2 under one harness and fell from 103.8 to 75.3 under another (Xu, Oct 2026); resets add latency (Rajasekaran, Mar 2026)
- **Security:** none (unmeasured)
- **Governance:** improves, small (unmeasured)
- **Brand:** none (unmeasured)

## Evidence (summary)

- Lance Martin, "Agent Design Patterns", https://rlancemartin.github.io/2026/01/09/agent_design/ (2026-01-09): "Some agents write a plan to a file and read it back into context periodically to reinforce objectives and / or verify its work."
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan."
- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Justin Young (Anthropic), "Effective harnesses for long-running agents"… (2025-11-26): "The key insight here was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the claude-progress.txt file alongside the git history."
- Anthropic, "Managing context on the Claude Developer Platform", https://www.anthropic.com/news/context-management (2025-09-29): "combining the memory tool with context editing improved performance by 39% over baseline. Context editing alone delivered a 29% improvement." The 84% token reduction in the same post is for context editing alone, on a 100-turn web search…
- …and 10 more sources in `library/entries/multi-window-task-state.yaml`.

## Caveats

Most measured gains come from deep-research and long-horizon coding systems built around their authors' own memory design, often on one model and small samples (one ablation used 10 queries, another does not state its run count), and no controlled study isolates a plain progress file under a forced reset. Model-written notes are not free memory: Cognition found them incomplete, Vending-Bench agents wrote notes they never read, and a stale written standard led agents to the worse form on every contested decision, so read-back and upkeep must be enforced. The need depends on the model: Anthropic needed resets with handoff files for Sonnet 4.5 but dropped them for Opus 4.5, so measure per model and again after an upgrade.

## Related

- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)

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
