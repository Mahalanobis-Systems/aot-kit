---
name: continuous-task-loop
description: "AOT optimization 7.d.i (Tier 4, Restructuring): Continuous autonomous task loop. Placeholder. Use when an agent shows: Iterations; commits; rate-limit events; iterations with no tool calls; tokens since the last test or score gain; the same item claimed or built twice; previously passing tests broken; completion claims while hidden tests fail."
---

<!-- Generated from library/entries/continuous-task-loop.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Continuous autonomous task loop

> **Placeholder.** Generated from `library/entries/continuous-task-loop.yaml` (entry 7.d.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.d.i |
| Earlier id | P51 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it changes the control loop |
| Categories | Orchestration: Shaping the loop |
| Change | workflow / control_flow |

## What it is

Run the coding agent from a shell or harness loop that starts a fresh headless session every iteration with the same short prompt; each session reads the plan, progress notes and git history, does one item, runs its tests, commits and exits, until an iteration cap, a budget or a stop rule ends the run. It pays on long backlogs with a near-perfect automatic check: 16 such loops on Opus 4.6 built a 100,000-line C compiler that builds Linux 6.9 over nearly 2,000 sessions for just under $20,000, though new features kept breaking existing ones and the author had to add a CI gate. In one controlled study, a harness that rebuilt a fresh context for every invocation and assigned each next experiment reached the strongest baseline's kernel result with 93.1% fewer tokens, while a framework that resumed long-running sessions kept spending until 1B tokens though its last improvement came at 231M. No study compares a plain loop with one long session on the same backlog, and fresh contexts do not stop drift: across fresh-container iterations code erosion rose in 77% of agent trajectories.

## When it applies

- **In the code:** A shell or harness loop that starts a headless agent each iteration with the same prompt file over a plan, task list or progress file, committing per iteration; whether it resumes the previous session (a stop hook or resume flag) or starts a fresh one; iteration, budget and time caps; permission prompts turned off outside a container.
- **In traces:** Iterations; commits; rate-limit events; iterations with no tool calls; tokens since the last test or score gain; the same item claimed or built twice; previously passing tests broken; completion claims while hidden tests fail.
- **In eval results:** Throughput; defect rate of produced work.
- **Judge:** Rate produced commits.
- **Probes:** A queue with a poison task.

## How (outline)

1. Start from the baseline: the same backlog run as one long agent session with the harness's own compaction, or an operator re-prompting it, and log where it stops: it waits for input, declares the job done early, or fills its context. Use the loop only for a long list of checkable items with an automatic check you trust, since the agent "will solve the wrong problem" unless the verifier is "nearly perfect" (Carlini, Feb 2026); tests, type checkers and builds are the loop's back pressure (Huntley, Jul 2025).
2. Start a new headless process every iteration with the same short prompt file, inside a container that holds only the repository, and log each iteration to its own file: while true; do claude --dangerously-skip-permissions -p "$(cat AGENT_PROMPT.md)" &> agent_logs/agent_$(git rev-parse --short=6 HEAD).log; done (Carlini, Feb 2026). Do not resume the previous session: the official Claude Code plugin re-feeds the prompt inside one session through a stop hook (Anthropic, Nov 2025), and in a framework that resumed each agent's own session after restarts, agents that had declared their work optimal kept repeating that decision, with 98% of the last 1,500 sessions making no tool calls (Zhang, Oct 2026).
3. Keep state in the repository, not the conversation, and load the same files every iteration: the spec, a plan or fix list, a progress file and README the agent updates, and the git log (see 4.b.iii). Ask for one item per iteration and have the agent search the code before implementing, since a wrong "not implemented" conclusion produces duplicate implementations (Huntley, Jul 2025). Letting the agent pick "the next most obvious" problem works while failing tests are independent (Carlini, Feb 2026); in one controlled study a stateless planner that assigned each next experiment from a harness-built summary beat independent worker choices in all four checkpoint comparisons (Zhang, Oct 2026). For parallel loops, claim an item by pushing a lock file through git so a second claim fails (Carlini, Feb 2026); posted notes did not stop two agents from building the same feature twice (Zhang, Oct 2026).
4. Gate every commit: a CI run so new commits can't break existing tests (added once the agents began breaking existing functionality with each new feature), a --fast mode that runs a 1% or 10% sample of the tests, deterministic per agent, for checks inside an iteration, short test output with details in log files (see 7.b.ii), and a known-good oracle to split a monolithic target (GCC compiled most of the kernel so agents could fix different files) (Carlini, Feb 2026). Schedule cleanup as well: across fresh-container iterations structural erosion rose in 77% of trajectories and verbosity in 75.5%, and quality prompts lowered the level but not the rate of decline (Orlanski, Mar 2026); Carlini gave one agent the job of coalescing duplicate code.
5. Bound and stop the run: always set an iteration cap (the plugin's default is unlimited), a token or dollar budget and a time limit per iteration; stop when the list is done and a check the agent does not control passes, or when several iterations add no passing test or score gain, not on the agent's own completion phrase (the plugin's exact-match phrase cannot express "blocked") (see 7.b.i, 7.b.iii, 9.b.iii). Budget for scale: 16 loops used 2 billion input and 140 million output tokens, just under $20,000, over two weeks (Carlini, Feb 2026).
6. Measure: run the baseline and the loop on the same backlog, model and dollar budget; score with an end-to-end suite the agents never see plus complexity and duplication of the final code, read at several budget points (one harness trailed on all four software tasks at 25% of the budget and led on all four at 100%, Zhang, Oct 2026); per iteration, log tokens, dollars, commits, tests gained and broken, iterations with no tool calls and tokens since the last improvement.

## How to measure

- **experiment** (Tier 4): paired runs on the same backlog, model and dollar budget: one long session with compaction (or resumed sessions), the fresh-process loop with state files, and the loop with a CI gate, assigned next items and a stop-on-no-progress rule; score with an end-to-end suite the agents never see plus cyclomatic complexity and duplicated code of the final tree, read at 25%, 50% and 100% of the budget; report dollars per accepted commit, regressions introduced and human hours needed to finish
- **monitor**: per iteration: tokens and dollars, wall time, tool calls (zero means idle), commits, tests gained and broken, CI rejections, items claimed or built twice, rate-limit waits, tokens since the last improvement, complexity and duplication trend, and completion claims checked against the hidden suite

## Expected impact

- **Quality:** mixed, medium: long backlogs with a near-perfect check: 16 loops built a 100,000-line C compiler that builds Linux 6.9 on x86, ARM and RISC-V and passes 99% of most compiler test suites, but its output is less efficient than GCC with all optimizations disabled and new features frequently broke existing ones (Carlini, Feb 2026); a fresh-context harness had the best final result on every task, 1112.0 against 1275.7 kernel cycles for the strongest baseline (Zhang, Oct 2026); across fresh-container iterations erosion rose in 77% of trajectories and core pass rate fell from 64.6% to 35.5% (Orlanski, Mar 2026); no study against one long session on the same backlog
- **Cost:** degrades, large: nearly 2,000 sessions, 2 billion input and 140 million output tokens, just under $20,000 (Carlini, Feb 2026); a framework resuming long sessions kept spending until 1B tokens after its last improvement at 231M, while a fresh-context harness reached the strongest baseline's kernel result with 67.9M against 986.3M tokens and its planner used under 0.6% of tokens (Zhang, Oct 2026); mean cost per iteration grew 2.2x from first to last checkpoint (Orlanski, Mar 2026)
- **Performance:** mixed, small (unmeasured): unattended runs of hours to weeks (two weeks for the compiler) replace operator turns, but each fresh session spends significant time re-orienting on a large project and agents will spend hours running tests without a sampled fast mode (Carlini, Feb 2026); going from 1 to 15 parallel workers cut elapsed time 6.6 to 7.3x (Zhang, Oct 2026); no source compares wall time with one long session
- **Security:** degrades, medium: loops run with permission prompts off (--dangerously-skip-permissions) and push their own commits; Carlini says to run it "in a container, not your actual machine" and saw an agent run pkill -9 bash and end its own loop (Carlini, Feb 2026); one harness ran workers as unprivileged processes under Landlock filesystem limits with restricted network (Zhang, Oct 2026)
- **Governance:** mixed, medium: each iteration leaves a commit, a log named by commit and lock files in git history (Carlini, Feb 2026), but no one reviews each commit and the agent's own "done" is weak: "it is easy to see tests pass and assume the job is done, when this is rarely the case" (Carlini, Feb 2026); the vendor plugin stops on an exact completion phrase and has no iteration cap by default (Anthropic, Nov 2025)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Geoffrey Huntley, "Ralph Wiggum as a “software engineer”", https://ghuntley.com/ralph/ (2025-07-14): "In its purest form, Ralph is a Bash loop. while :; do cat PROMPT.md | claude-code ; done". Says it has defects that are "identifiable and resolvable through various styles of prompts." Each loop loads the same plan and specifications, and…
- Qizheng Zhang, Changxiu Ji, Isaac Sun, Yuetai Li, Shubhangi Upasani, Sherry Ruan, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Yoonho Lee… (2026-10-06): Best full-budget result on every task. Anthropic kernel task with Codex (three runs): 1112.0 ± 8.9 cycles against 1275.7 ± 133.9 for the strongest baseline, whose final result it matched at 67.9M against 986.3M tokens (93.1% fewer); with…
- Gabriel Orlanski, Devjeet Roy, Alexander Yun, Changho Shin, Alex Gu, Albert Ge, Dyah Adila, Nicholas Roberts, Frederic Sala, Aws… (2026-03-25): No agent solved any problem end to end; best strict checkpoint solve rate 14.8% (GPT 5.5). Structural erosion rose in 77% of trajectories (53% of human repositories) and verbosity in 75.5%; agent code was 2.3x more verbose and 2.0x more…
- Nicholas Carlini (Anthropic), "Building a C compiler with a team of parallel Claudes"… (2026-02-05): "Over nearly 2,000 Claude Code sessions across two weeks, Opus 4.6 consumed 2 billion input tokens and generated 140 million output tokens, a total cost just under $20,000." The 100,000-line compiler builds a bootable Linux 6.9 on x86, ARM…
- …and 1 more sources in `library/entries/continuous-task-loop.yaml`.

## Caveats

No study compares a plain fresh-process loop with one long session, or an operator re-prompting, on the same backlog, model and budget: the largest account is one build judged by its author on the vendor's own model, and the one controlled comparison is an automated-research harness whose gain mixes fresh contexts with planner-assigned work and harness summaries, with three runs on one task and one run elsewhere. Fresh contexts do not stop drift: across fresh-container iterations code erosion rose in 77% of agent trajectories (against 53% of human repositories) and quality prompts lowered the level but not the rate, on a benchmark with a two-hour limit per run. The vendor's own plugin loops inside one session rather than restarting, and no source measures that design against a fresh process. What the loop can finish depends on the model: earlier Opus 4 models "were barely capable of producing a functional compiler" and Opus 4.5 could not compile real large projects.

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:verify-completion` (9.b.iii, Verify completion against the environment before the agent stops)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
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
