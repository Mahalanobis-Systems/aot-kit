---
name: multi-window-task-state
description: "AOT optimization 4.b.iii (Tier 4, Restructuring): Keep plan, progress and results in files when work outlives one context window. Placeholder. Use when an agent shows: Context resets followed by re-exploration or redone steps; notes written but never read back; entries that vanish from the state between windows; completed actions repeated after a reset despite a completion record; user constraints or decisions violated after compaction; work declared done after a reset; state files older than the code they describe."
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

Keep a long task's plan, progress, decisions and large results in files, and start every new context window by reading them back. In measured studies, mostly of deep-research, coding and autoresearch agents, state kept outside the history beat a growing or compacted one: Anthropic's memory tool plus context editing gained 39% on agentic search against 29% for context editing alone, a checkpoint of progress and verified facts plus a self-chosen reset took Claude Sonnet 4 from 22.7% to 30.7% on 150 BrowseComp questions with the same tools, and fresh contexts over the same workspace beat one compacted session at equal compute (0.55 against 0.45 normalized score). Form matters: a structured handoff beat a narrative summary of the same length (52.1% against 42.8% of tasks fully completed, GPT-5.4), and state updated by code answered access questions at 0.80 where a ledger the model rewrote itself fell to chance. The limits: the full history still beat a compact handoff where it fit, a strong reasoning model needed explicit state only for long histories, a 7B model lost accuracy with the extra tools, and stale, wrong or unread notes misled agents, so enforce read-back, let code apply updates, measure per model, and within one window use a re-injected task list (7.b.iv) instead.

## When it applies

- **In the code:** A plan or todo file, a progress log, a decisions and open-items file, and for coding a structured test list and an init script, kept outside the context window, plus a start-of-window step that reads them back.
- **In traces:** Context resets followed by re-exploration or redone steps; notes written but never read back; entries that vanish from the state between windows; completed actions repeated after a reset despite a completion record; user constraints or decisions violated after compaction; work declared done after a reset; state files older than the code they describe.
- **In eval results:** Completion rate and redone work on tasks longer than one window, with a reset forced midway, against carrying the full history where it fits.
- **Probes:** Tasks longer than one context window.

## How (outline)

1. Start from the harness as it is (compaction or truncation only) on tasks that really run past one window or carry a long history, and log what breaks after each reset: work redone, decisions or user constraints lost, work declared done too early. Where the full history still fits, keep it as the baseline to beat: in one study it beat a compact handoff (57.9% against 52.1% of tasks fully completed with GPT-5.4), and a 120B reasoning model read a 256-event log almost as well as the extracted state (0.95 against 0.99).
2. In the first window, before real work, have the agent create the state files: a structured list of features or tests (JSON, every item failing, with an instruction that items are never removed or rewritten, only marked passing), a progress log, a decisions and open-items file that also holds the user's constraints, and for coding an init script that starts the app and runs a smoke test; commit them to git. Keep the handoff structured (facts, commitments, completed actions, remaining work), not a narrative: at the same length it fully completed 52.1% of tasks against 42.8% (GPT-5.4). Record next to each verified fact where it came from (file, URL, test), since a fact corrupted before a reset was never caught afterward.
3. Write large intermediate results (sources, query results, documents, logs) to files and keep only the path and a one-line note in context.
4. Start every later window with a fixed resume step written into the prompt: read the progress log, the decisions file, the test list and the git log, run the init script and the smoke test, then take one open item. Do not leave reading optional; agents write notes they never read.
5. Update at fixed points: when an item passes an end-to-end check, mark it, append to the log and commit; before a reset, write the handoff. Have code, not the model, apply changes to structured state: keep one keyed entry per item or constraint that the model may update but not drop, and retire an entry only by an explicit rule (done, superseded). A ledger the model rewrote itself dropped entries it judged inactive and fell to chance (0.50), against 0.80 when the model only parsed each event and code applied it. Keep free-text files describing the present and delete stale ones, because agents follow a written file over the code.
6. Keep harness-side safety nets instead of relying on model-written notes alone: keep compaction or the harness's own state capture, re-append the constraint list after every compaction, and choose a fresh window or compaction per model. Where you reset, do it at task boundaries or on a fixed schedule rather than waiting for a stall: fresh contexts over the same workspace beat one compacted session at equal compute (0.55 against 0.45 normalized, better on 6 of 11 tasks), and a plateau trigger did not fire before the budget ran out in 15 of 25 runs. Check weaker models first: a checkpoint-and-reset prompt gained 4.8 to 8.0 points with Claude Sonnet 4 but cost a 7B model 3.9 points.
7. Measure with paired runs that force a reset midway, with and without the files and the resume step, and against the full history where it fits: completion, steps redone, completed actions repeated, constraint violations after the reset, tokens and wall time, per model and with several runs; add a copy that corrupts one state entry before the reset; re-run after a model change.

## How to measure

- **experiment** (Tier 4): paired runs on tasks longer than one window, forcing a reset (or capping the window) midway: the harness as is against the same harness with state files and a fixed resume step, and against carrying the full history where it still fits; completion, steps redone and completed actions repeated after the reset, constraint violations after the reset, tokens and wall time, per model with several runs; add a copy in which one state entry is corrupted before the reset; re-run after a model change
- **monitor**: per reset: whether the first actions read the state files, steps redone, completed actions repeated, items marked done that fail their test, entries that vanish from the state between windows, state files older than the code or plan they describe, and the share of tokens spent writing notes

## Expected impact

- **Quality:** improves, medium: tasks past one window or with long histories: memory tool plus context editing +39% against +29% (Anthropic, Sep 2025); checkpoint plus reset 22.7% to 30.7% on BrowseComp with Claude Sonnet 4, but 17.5 to 13.6 on GAIA for a 7B model (Zhu, Oct 2026); fresh contexts over the same workspace 0.55 against 0.45 for one compacted session at equal compute (Cai, Oct 2026); a report rewritten into each rebuilt context +12.7 (o3) and +19.2 (DeepSeek-V3.1) points on BrowseComp over ReAct (Chen, Nov 2025); structured handoff 52.1% against 42.8% for a narrative summary, full history 57.9% (Li, Oct 2026); code-applied state 0.80 against 0.50 for a model-kept ledger, and only +0.04 for a 120B reasoning reader at 256 events (Guo, Nov 2026); without todo, checklist and log files 52.76 to 48.69 RACE on 10 queries (Zhu, Feb 2026); model-written notes alone degraded Devin (Cognition, Sep 2025); a stale convention file cut better-form decisions from 33% with no file to 0% (Mohammadi, Aug 2026)
- **Cost:** improves, medium: where the state replaces a growing history: 314K against 1,078K input tokens per GAIA trajectory at about the same accuracy (20.4% against 19.4%), peak context 14.3K against 30.6K, for an 8B model (Zhu, Oct 2026); 1.3k against 28.1k tokens per decision on a 1,024-event log, though building the state costs one parser call per event (Guo, Nov 2026); 61% and 22% fewer tokens on tau3-Bench Airline and Retail (Li, Sep 2026); file I/O under 0.03% of wall time (Zhu, Feb 2026); resets add token overhead (Rajasekaran, Mar 2026) and an agent sometimes spent more tokens writing summaries than solving the problem (Cognition, Sep 2025), both unmeasured
- **Performance:** mixed, small: 21.8 against 45.3 model calls per GAIA trajectory with checkpoints and resets for an 8B model (Zhu, Oct 2026); with a state-recovery memory, minutes per DeepSWE task rose from 42.0 to 54.2 under one harness and fell from 103.8 to 75.3 under another (Xu, Oct 2026); resets add latency (Rajasekaran, Mar 2026)
- **Security:** none (unmeasured)
- **Governance:** improves, medium: constraints and permissions kept outside the summary: a constraint registry appended after compaction raised compliance by 39.5 to 42.6 points, and after compaction an agent deleted emails without approval in 30 of 100 sessions against none before (Wang, Jul 2026); permission state applied by code answered whether a service may act at 0.80 to 0.89 against 0.64 to 0.73 for the same readers reading the full log with a reasoning trace, while a ledger the model kept itself dropped components and fell to chance (Guo, Nov 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- Lance Martin, "Agent Design Patterns", https://rlancemartin.github.io/2026/01/09/agent_design/ (2026-01-09): "Some agents write a plan to a file and read it back into context periodically to reinforce objectives and / or verify its work."
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan."
- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Justin Young (Anthropic), "Effective harnesses for long-running agents"… (2025-11-26): "The key insight here was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the claude-progress.txt file alongside the git history."
- Anthropic, "Managing context on the Claude Developer Platform", https://www.anthropic.com/news/context-management (2025-09-29): "combining the memory tool with context editing improved performance by 39% over baseline. Context editing alone delivered a 29% improvement." The 84% token reduction in the same post is for context editing alone, on a 100-turn web search…
- …and 15 more sources in `library/entries/multi-window-task-state.yaml`.

## Caveats

Most measured gains come from systems built around their authors' own memory design, often on one model and small or synthetic samples (one ablation used 10 queries and the BrowseComp check 150 questions on one backbone, and the structured-handoff and state-tracking results come from synthetic tasks), and no controlled study isolates a plain progress file under a forced reset. Model-written state is not free memory: Cognition found notes incomplete, Vending-Bench agents wrote notes they never read, a model rewriting its own state ledger dropped entries until it answered at chance, a stale written standard led agents to the worse form on every contested decision, and a fact corrupted before a reset was never caught, so let code apply updates, keep each fact's source and enforce read-back. The need depends on the model and the history: Anthropic needed resets for Sonnet 4.5 but not Opus 4.5, a 120B reasoning reader gained 0.04 from explicit state at 256 events and 0.12 at 1,024, a checkpoint-and-reset prompt cost a 7B model 3.9 points, and the full history beat a compact handoff where it fit, so measure per model and again after an upgrade. The fresh-context result comes from optimization tasks with a scored objective, where it won on 6 of 11 tasks, and under a stricter status check structured handoffs scored below recent transcripts for five of six receivers.

## Related

- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)

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
