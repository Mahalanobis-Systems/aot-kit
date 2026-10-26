---
name: episodic-memory
description: "AOT optimization 4.c.i (Tier 4, Restructuring): Episodic memory retrieval. Placeholder. Use when an agent shows: Memories retrieved per task, whether the agent read and followed them, and whether they applied; memory writes and their source; repeated mistakes the store should have prevented."
---

<!-- Generated from library/entries/episodic-memory.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Episodic memory retrieval

> **Placeholder.** Generated from `library/entries/episodic-memory.yaml` (entry 4.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.c.i |
| Earlier id | P55 (Context & Memory, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a cross-session memory architecture |
| Categories | Memory: Reusing work |
| Change | tool / memory |

## What it is

Log every agent session as a raw trace, distill a few verified lessons from them (user corrections, definitions, workflows that worked, mistakes) into short memory files, show the agent an index of those files at the start of each task, and let it search both. It pays where later tasks need what earlier ones learned: Databricks' data agent went from 22.3% to 68.4% on tasks built from its users' past sessions, with 31% fewer tokens. Elsewhere the gains mostly vanish: with three frontier models two memory methods moved average accuracy by -1.1 to +3.0 points over six benchmarks, a no-memory web agent given the same tokens beat ReasoningBank by 5.1 to 8.1 points, and off-the-shelf memory systems were at or below memory off on coding tasks in 11 of 12 pairings. Unverified lessons reproduce mistakes, and an agent that writes memory from what it reads can be poisoned: one crafted email planted a lasting instruction in up to 87.5% of test cases.

## When it applies

- **In the code:** Raw session traces kept across tasks or sessions; distilled memory files or a vector store of lessons; an index or retrieval step at task start; writes after each task or on user request; a consolidation, TTL or decay job.
- **In traces:** Memories retrieved per task, whether the agent read and followed them, and whether they applied; memory writes and their source; repeated mistakes the store should have prevented.
- **In eval results:** Repeat-mistake rate over time; pass rate with and without memory on a task stream, split into rescues and regressions.
- **Judge:** Rate retrieved memories for relevance.
- **Probes:** A task pair where the first teaches a lesson the second needs, an unrelated task the lesson could mislead, and untrusted content that asks to be remembered.

## How (outline)

1. Start from two baselines on the same tasks and model: no memory, and a no-memory agent that gets the memory's token budget as extra steps (7.b.iii) or reasoning effort (1.b.i). A no-memory web agent allowed 15 steps instead of 10 beat ReasoningBank by 5.1 to 8.1 points with three 2026 models, mostly at fewer total tokens, and with GPT-5.4, Gemini 3.1 Pro and Claude Opus 4.7 two memory methods moved average accuracy by -1.1 to +3.0 points. Build the evaluation stream so later tasks need what earlier ones learned (a user's corrections, metric or table definitions, repository conventions, a workflow that was costly to find): that is where memory paid, 22.3% to 68.4% on tasks built from real user sessions.
2. Log every session as an append-only raw trace (task, steps, tool results, outcome, user feedback), and keep a separate set of short distilled memory files (preferences, definitions, workflows, mistakes) under an auto-generated index file that says what each file holds. In Databricks' ablation, raw traces alone reached 35.8% (the agent searched them in only about a third of cases), distilled files with the index 66.1%, and both 68.4%.
3. Persist a distilled lesson only after a check against ground truth (tests pass, the user confirms, the outcome is verified), never on the agent's own success judgment: on one site 52.9 to 59.5% of ReasoningBank's success-labeled lessons came from tasks that had failed, stored lessons trailed raw trajectories in 7 of 9 settings, and a GPT-5.5 check before admitting each lesson raised stored-lesson memory from 38.7% to 46.0%. Where nothing can verify a lesson, synthesize guidance from the retrieved raw traces for the current task and discard it afterwards (+3.3 to +28.0 points over storing it). Write explicit user requests (“Never write scripts in the /tmp dir”) at once.
4. At session start inject the index, give the agent search and fetch tools over both stores, and retrieve only a few records (the studies used one to five). Inject a short record anchored to the files, tables or fix it concerns, not raw transcript chunks or loosely extracted facts: off-the-shelf memory systems were at or below memory off in 11 of 12 coding pairings, mostly because the record they injected buried or dropped the fix. Keep a separate store per user or domain (an unrelated passage cost 0.7 to 3.4 points) and tell the agent a memory is a hint to check against the current task, not an instruction.
5. Consolidate offline on a schedule: distill new sessions into the files, merge duplicates, split oversized files, resolve conflicts and delete stale entries (offline distillation 63.5% against 53.9% for writes made during the session, 66.1% with both).
6. Treat a memory write as a privileged action (10.c.i): only the user and verified outcomes may write; never store instructions found in email, web pages, documents or tool output; record each entry's source and show every write to the user. One crafted email made agents store and later act on a poisoned memory in 87.5% (GPT-5.4) and 71.4% (Sonnet 4.6) of held-out cases when mail was processed in the background, past input, model and trace defenses; asking the agent to report what it checked and did cut foreground success from 75.0% to 1.8% and from 48.2% to 23.2%.
7. Measure with paired runs against both baselines, memory frozen during evaluation, at least three seeds: pass rate split into tasks memory rescues and tasks it breaks (it helps where the model fails without it and can hurt where it already succeeds), tokens including memory-side calls, steps and latency (1.35x faster and 1.44x fewer tokens in Databricks' test; A-Mem cost up to 6.37x of no memory on GPT-5.4), and a poisoning probe; re-run after every model change.

## How to measure

- **experiment** (Tier 4): paired runs on a held-out stream that mixes tasks reusing what earlier ones learned (user corrections, definitions, repository conventions) with tasks that share nothing, memory frozen during evaluation and at least three seeds: memory against no memory and against a no-memory agent given the same total tokens as extra steps or effort; report pass rate split into rescues and regressions, tokens including memory-side calls, steps and latency; ablate raw traces only, distilled files only and both; add a poisoning probe (a document or email asking the agent to remember an instruction) and count writes and later effects
- **monitor**: memory writes per session by source (user, verified outcome, untrusted content) and whether the user saw them; retrievals per task and how often the agent followed a memory that did not apply; repeat-mistake rate; regressions on task types solved before memory; store size, duplicates and conflicts after each consolidation; tokens per task

## Expected impact

- **Quality:** mixed, medium: tasks built to need earlier sessions: 22.3% to 68.4% pass rate (Databricks, Oct 2026); with GPT-5.4, Gemini 3.1 Pro and Claude Opus 4.7 over six benchmarks, A-Mem and ReasoningBank moved average accuracy by -1.1 to +3.0 points (Yan, Jul 2026); a no-memory web agent given the same tokens beat ReasoningBank by 5.1 to 8.1 points (Hajimiri, Jun 2026); memory systems at or below memory off in 11 of 12 coding pairings, a test-verified record +0.0 to +4.5 (Fan, Sep 2026); stored lessons trailed raw trajectories in 7 of 9 settings and discarding them gained 3.3 to 28.0 points (Wang, Oct 2026); under a tight budget several memory methods fell below no memory, MemRL 4.7% against 30.7% (Lai, Oct 2026)
- **Cost:** mixed, medium: 1.44x fewer tokens per task than no memory (Databricks, Oct 2026); per-task cost 0.62x to 0.98x of no memory for ReasoningBank but up to 6.37x for A-Mem on GPT-5.4 (Yan, Jul 2026); ReasoningBank 82.6K tokens per task against 73.6K for a stronger no-memory agent, its module adding 16.5K to 26.1K prompt tokens (Gemini 3 Flash) (Hajimiri, Jun 2026); 9.31 against 9.48 to 10.17 LLM calls per task for designs that store lessons (Wang, Oct 2026)
- **Performance:** mixed, medium: 1.35x faster per task, and one repeated workflow from nearly six minutes to 41 seconds (Databricks, Oct 2026); steps per task down 6.6% to 23.2% with A-Mem and ReasoningBank on GPT-5.4 and Gemini 3.1 Pro (Yan, Jul 2026); tasks must run in order, so they cannot run in parallel (Hajimiri, Jun 2026)
- **Security:** degrades, large: when the agent reads untrusted content and can write memory: one crafted email made agents store and act on a poisoned memory in 87.5% (GPT-5.4) and 71.4% (Sonnet 4.6) of held-out cases in background mode, also with a Mem0 backend (85.7%), past input, model and trace defenses; handcrafted payloads scored 0.0% on both models (Zhang, Jul 2026)
- **Governance:** mixed, medium: distilled memory kept as files with an index is a reviewable record that can move between agents (Databricks, Oct 2026); writes can be hidden from the user, with 100% stealth in background mode on GPT-5.4 (Zhang, Jul 2026); the store depends on task order, so one failed task cannot be re-run in isolation (Hajimiri, Jun 2026); stored sessions retain user data
- **Brand:** improves, small (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning", https://arxiv.org/abs/2303.11366 (2023-03-20): "91% pass@1 accuracy on the HumanEval coding benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%"
- Databricks AI Research (Veronica Lyu, Wenhao Zhan, Sam Havens, et al.), "MemCurrent: Designing Persistent Memory for Production Agents"… (2026-10-20): Internal Memory Benchmark (Genie agent): pass rate 22.3% with no memory, 68.4% with MemCurrent, 78.6% with the gold memories injected, Mem0 43.9%; MemCurrent 252 s and 418K tokens per task, 1.35x faster and 1.44x fewer tokens than no…
- Ruhan Wang, Kishan Panaganti, Dongruo Zhou, "More Memory, Worse Agents: Error Reproduction and Anti-Persistence in LLM Agents"… (2026-10-19): Held-out success, equal-weight mean over nine settings: anti-persistence 59.9%, trajectory memory 53.5%, abstraction memory 49.0%, joint memory 49.3%, Reflexion 52.9%; anti-persistence +19.2 points over ReAct with no memory. Stored…
- Guannan Lai, Zi-Yang Bai, Jun-Peng Jiang, Han-Jia Ye, "Learning What to Remember: Resource-Efficient Self-Improvement for Lifelong Agents"… (2026-10-19): LifelongAgentBench success, local Qwen2.5-14B / API DeepSeek-V4-Flash: no memory 25.2/26.2 (DB), 50.2/67.2 (OS), 30.7/12.7 (KG); plain retrieval 33.0/29.4, 54.6/66.6, 11.3/31.3; TokenWorth 65.0/62.2, 59.4/73.2, 36.7/36.7. Several methods…
- …and 4 more sources in `library/entries/episodic-memory.yaml`.

## Caveats

The large gains come from benchmarks built so that memory is needed, and the biggest is Databricks' own (114 cases from its own agent, scored by an LLM judge); the independent tests that found small or negative effects used largely self-contained tasks (WebArena, SWE-style coding, 50-task benchmark streams), mostly open or mid-size models, and intervals that often cross zero, and none of them compares memory with a budget-matched baseline on tasks that depend on earlier ones. Memory makes tasks depend on their order, so they cannot run in parallel and a transient failure silently changes what later tasks see. It helps weaker models and unsolved tasks more and can break tasks a strong model already solves: where one record moved two solvers in opposite directions, the one weaker without memory gained in 61 of 64 cases. The 87.5% poisoning rate needs an attacker model trained against a copy of the agent; handcrafted payloads scored 0.0% on GPT-5.4 and Sonnet 4.6.

## Related

- `aot-kit:skill-library` (4.c.ii, Skill library evolution)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)

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
