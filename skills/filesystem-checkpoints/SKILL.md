---
name: filesystem-checkpoints
description: "AOT optimization 4.b.i (Tier 2, Reliability): Filesystem-based agent state and checkpoints. Placeholder. Use when an agent shows: Resume and rollback events; steps re-executed after a resume; an external effect issued twice for one step; checkpoint latency exposed on the critical path; rollbacks per run and what followed them."
---

<!-- Generated from library/entries/filesystem-checkpoints.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Filesystem-based agent state and checkpoints

> **Placeholder.** Generated from `library/entries/filesystem-checkpoints.yaml` (entry 4.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.b.i |
| Earlier id | P54 (Context & Memory, from the catalog cookbook) |
| Tier (proposed) | 2 (Reliability): operational hardening: checkpoint and resume |
| Categories | Memory: Resuming |
| Change | tool / memory |

## What it is

Save the agent's state at each step boundary (the conversation, the workspace files, process state when it matters, and a ledger of external side effects) so a crashed or stuck run resumes or rolls back instead of starting over. With one crash injected per task, restoring all of that recovered every task within 1.9% of fault-free time, while resuming from the conversation alone recovered 8 to 13% of Terminal-Bench tasks and restarting cost up to 1.67x the time; in one study, letting the agent roll back workspace and conversation together, with a note on what failed, raised success on long engineering tasks from 62.2% to 87.8%. The risks are side effects and partial restores: widely used framework checkpointers re-ran completed steps after a real crash, restores that bring back some state but not the rest let approvals and validations carry over to the wrong action, and rewinding the conversation without the files did worse than not rewinding.

## When it applies

- **In the code:** What a checkpoint covers (transcript only, workspace files, sandbox processes, a ledger of external effects) and when it is written; whether resume serves recorded tool results or re-executes them; whether conversation and workspace can be restored from different points; whether a parked step or approval is claimed atomically before it runs; resume logic on start.
- **In traces:** Resume and rollback events; steps re-executed after a resume; an external effect issued twice for one step; checkpoint latency exposed on the critical path; rollbacks per run and what followed them.
- **In eval results:** Recovery from injected crashes (a real kill, not only an exception) on tasks the agent already solves, against restart and transcript-only resume: recovery correctness, redo time and tokens, duplicate effects in an external ledger.
- **Probes:** Kill mid-run and resume.

## How (outline)

1. Start from the baseline: restart the run from scratch on a crash, and resume from the conversation history alone (what most framework checkpointers and hosted agents restore). On 100 solved tasks per setup with one injected crash each, restart recovered every task but added up to 1.52x (Terminal-Bench) and 1.67x (SWE-bench) to completion time, and conversation-only resume recovered 8 to 13% of Terminal-Bench tasks and 9% of SWE-bench tasks (Wu, Apr 2026).
2. Checkpoint what the next step depends on, not only the transcript: at each turn boundary (after tool results, before the next model call) record the conversation and the workspace together, for example a commit per step in a bare git repository kept outside the project's own history, with secrets excluded and caches dropped (Zhuang, Aug 2026), and add a process or sandbox snapshot when the task leaves services running or packages installed: conversation plus files recovered 100% on SWE-bench but only 28 to 42% on Terminal-Bench, where processes matter (Wu, Apr 2026). Always restore conversation and workspace from the same point: inconsistent restored state appeared only in the two tools that let files and conversation be restored separately, and a workspace rollback that kept the agent's passing malware scan released the uncleaned repository (Wu, Aug 2026).
3. Size checkpoints to what changed: skip turns with no net file or process change (up to 87% of turns), take file snapshots (about 20 to 100 ms) where only files changed and process snapshots (700 to 1,000 ms) only where processes changed, and run them during the next model call; that kept a crashed run within 1.9% of fault-free time, while a full checkpoint every turn was 3.78x slower at 96 sandboxes per host, worse than restarting (Wu, Apr 2026).
4. Treat external side effects (payments, messages, deploys, approvals) as the hard part: record each call and its result in a durable ledger keyed by the step, outside the checkpoint, and on resume return the recorded result instead of calling again. Test this with a real kill, not a raised exception: LangGraph 1.2.9 re-ran a completed step whose result was durably written after a SIGKILL, CrewAI 1.15.2's checkpoint restore re-ran a completed effect while its state looked correct, and an embedded DBOS engine ran each step's effect once (Khan, Aug 2026). Ordering the effect and the checkpoint write does not close the gap: with a failure between them, execute-then-commit repeated or skipped the effect in 90 of 96 workflows and commit-then-execute in 93 (Wu, Aug 2026); use idempotency keys or a transactional effect record (2.b.i).
5. Make resumes single-shot and re-check what a restore carries forward: claim a parked step or approval in the shared store with a compare-and-swap before running it (when 2 to 16 processes resumed one parked approval, every racer fired the gated effect in 36 of 40 cells) (Khan, Aug 2026). After any restore, re-validate approvals, checks and external bindings (the active account or mailbox, recipients) against the live world, and store concrete values (timestamps, object IDs, versions) rather than references such as "now" or "current state": rollback re-ran a test mail-forwarding rule on a live mailbox and paid an invoice twice under one approval (Wu, Aug 2026); gate irreversible actions (10.b.i).
6. Use checkpoints for rollback, not only crash recovery: give the agent a rewind tool that restores workspace and conversation to an earlier step and adds a short note on what failed. On 82 long engineering tasks with GPT-5.4 this raised success from 62.2% (continue) and 78.0% (restart with notes) to 87.8%, and recovered 30% of 50 stuck runs against 8%; rewinding the conversation without the workspace scored 43.9%, below not rewinding (Zhuang, Aug 2026). External effects are not rewound, so keep steps 4 and 5; for branching search over snapshots see 7.c.v.
7. Measure with crash-injection runs on tasks the agent already solves: one fail-stop per task at a random step, recovered by restart, transcript-only resume and your checkpoints, scoring recovery correctness, redo time and tokens, duplicate effects counted in a ledger the agent cannot see, and checkpoint latency exposed in fault-free runs; for rollback, compare runs with and without the rewind tool at a fixed token budget.

## How to measure

- **experiment** (Tier 2): crash-injection runs on tasks the agent already solves: one fail-stop per task at a random step (SIGKILL of the agent process or sandbox, not a raised exception), recovered by restart, transcript-only resume, transcript plus files, and the full checkpoint; score recovery correctness, redo time and tokens, duplicate external effects counted in a ledger the agent cannot see, and exposed checkpoint latency in fault-free runs; add probes that kill right after each durable write and between an effect and its checkpoint, resume one parked approval from two processes, and roll back after a validation; for rollback, paired runs with and without a rewind tool on long tasks at a fixed token budget (success, tokens, rewinds per run)
- **monitor**: resume and rollback events per run, steps re-executed per resume, external effects issued more than once per step key, approvals consumed more than once, checkpoint latency exposed on the critical path, checkpoint size and retention, and task outcomes after each rewind

## Expected impact

- **Quality:** improves, medium: after one injected crash, restoring files and processes recovered 100% of solved tasks against 28 to 42% for conversation plus files and 8 to 13% for conversation only on Terminal-Bench (Wu, Apr 2026); a rewind tool restoring workspace and conversation raised success from 62.2% (continue) and 78.0% (restart with notes) to 87.8% on 82 long tasks with GPT-5.4, and from 78.7% to 83.1% on Terminal-Bench 2.0, but rewinding the conversation without the workspace scored 43.9% (Zhuang, Aug 2026); framework checkpointers re-ran completed steps after a crash (Khan, Aug 2026)
- **Cost:** improves, medium: a crash with no checkpoint re-runs prior work: restart added up to 1.52x to 1.67x completion time against within 1.9% with checkpoints, and forking from a checkpoint instead of re-running a shared prefix cut RL rollout tokens 40.0 to 64.2% (Wu, Apr 2026); the rollback study reports no token cost and set no budget (Zhuang, Aug 2026)
- **Performance:** mixed, medium: checkpointing only turns with net changes and overlapping snapshots with the model call kept a crashed run within 1.9% of fault-free time, with p95 exposed delay of 0.44% at 64 sandboxes per host; a full file-and-process checkpoint every turn was 3.06x and 3.78x slower at 64 and 96 sandboxes, worse than restarting (up to 1.52x); process snapshots took 0.7 to 1.0 s against 20 to 100 ms for file snapshots (Wu, Apr 2026)
- **Security:** mixed, medium: restores combine state from different points: incomplete internal state in 67.2% of 1,735 executions across five frameworks, and attacks that kept a passing malware scan for an uncleaned repository, re-ran a mail-forwarding rule on a live mailbox and paid twice under one approval (Wu, Aug 2026); 2 to 16 processes resuming one parked approval each fired its effect (Khan, Aug 2026); rollback also restores a known-good state after a destructive action, such as overwritten test fixtures (Zhuang, Aug 2026)
- **Governance:** mixed, medium: per-step commits and checkpoints give a reviewable history and an undo (Young, Nov 2025; Zhuang, Aug 2026), but framework records can misstate what happened: CrewAI's restore re-ran an effect while its state looked correct, and LangGraph persisted schema-invalid state silently and served a second, different approval the first answer's branch (Khan, Aug 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Justin Young (Anthropic), "Effective harnesses for long-running agents"… (2025-11-26): The initializer sets up "an init.sh script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git commit"; later sessions "make incremental progress, then leave structured updates." Committing progress to…
- Guanlong Wu, Dahui Li, Ke Jiang, Jianyu Niu, Cong Wang, Yinqian Zhang, "Safe to Resume? Breaking Execution Continuity of Agent Execution… (2026-08-29): Across 1,735 framework-task executions (one random recovery point each): incomplete internal state coverage in 1,166 (67.2%), inconsistent checkpoint state in 489, external state mismatch in 198, divergent nondeterministic replay in 1,174…
- Yu Zhuang, Kefei Chen, Yitong Duan, Shuxin Zheng, Jian Li, Xu-Yao Zhang, "AgentRewind: Recoverable Execution for Long-Horizon LLM Agents"… (2026-08-14): MettleBench (82 tasks), GPT-5.4 with mini-SWE-agent, success / checklist progress: continue 62.2% / 81.4%, restart with experiences 78.0% / 88.8%, safety review 34.1% / 54.4%, AgentRewind 87.8% / 94.3%; GPT-5.4 mini success: 33.7%, 43.1%…
- Sajjad Khan, "Resume Means Resume: A Machine-Checked Conformance Contract for Checkpoint, Interrupt, and Resume Semantics in Workflow… (2026-08-04): LangGraph 1.2.9 (in-memory, SQLite and PostgreSQL savers): after a SIGKILL following a durable write, resume re-executed the completed task (effect count 1 before, 2 after), and killing after each of five persistence writes re-executed…
- …and 1 more sources in `library/entries/filesystem-checkpoints.yaml`.

## Caveats

The quality gains come from the authors' own systems: rollback was tested on the authors' own 82-task benchmark with one model family, no token or step limit and no cost reported, and 74.7% of task-strategy-model triples agreed across three runs (Zhuang, Aug 2026); the crash-recovery comparison replays recorded traces of tasks the agents had already solved (Wu, Apr 2026). A restored run is not a replay: with a live model, conversation plus files recovered 34% against 48% under replay because the agent's corrective actions perturbed the run (Wu, Apr 2026), and widely used framework checkpointers differ in what they re-execute, so a framework's exactly-once claim has to be tested with real kills (Khan, Aug 2026). Checkpoints cannot undo external effects and ordering the effect and the checkpoint write does not fix that (90 and 93 of 96 workflows still repeated or skipped the effect); the security study's prevalence counts come from its own model-built detection pipeline (98.7% precision on manual inspection) at one recovery point per run (Wu, Aug 2026).

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
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
