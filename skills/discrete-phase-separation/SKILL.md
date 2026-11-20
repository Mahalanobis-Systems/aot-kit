---
name: discrete-phase-separation
description: "AOT optimization 5.c.i (Tier 4, Restructuring): Discrete phase separation. Placeholder. Use when an agent shows: Phase boundaries and what crosses them; handoff size against the full history; files the implement phase re-reads that research already covered; edits made to the plan at review; research or plan files older than the code they describe."
---

<!-- Generated from library/entries/discrete-phase-separation.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Discrete phase separation

> **Placeholder.** Generated from `library/entries/discrete-phase-separation.yaml` (entry 5.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 5.c.i |
| Earlier id | P47 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it splits the work into isolated phases |
| Categories | Context: Isolating subtasks |
| Change | workflow / orchestration |

## What it is

Run research, planning and implementation as separate sessions, each starting fresh from the previous phase's written document, with a person reviewing that document before the next phase starts. It pays when the document knows more than the implementer would find alone: a stronger model's plan at the agent's first edit raised SWE-bench Verified resolution by 6.0 to 16.8 points, a fresh implementer given only that plan did as well as continuing the session (58.6% vs 58.2%), and a structured specification tied to its sources raised PaperBench scores from 24.14 to 29.87 with a third fewer tokens than letting the planner read the paper itself. The phases alone add little and the plan is a risk: GitHub Spec Kit's spec, plan and tasks stages scored 3.51 against 3.46 for implementing directly on a 1-to-5 judge scale, design documents changed how an agent structured a rebuilt library but not its held-out test pass rate (35.8% vs 33.7%), the implementer's own model as planner recovered 12 of 223 failures against 9 with no plan, a weaker planner's plans broke 14.6% of passing runs, and with incomplete instructions a read-only plan phase never raised task success. Agents' own plans name where to edit far more often than the constraints and checks a change needs, teams use the split for large new features but read the specs only partially, and no study we found tests the full split with human review against one continuous session.

## When it applies

- **In the code:** Phases with distilled handoffs rather than shared history.
- **In traces:** Phase boundaries and what crosses them; handoff size against the full history; files the implement phase re-reads that research already covered; edits made to the plan at review; research or plan files older than the code they describe.
- **In eval results:** Quality vs monolithic run.
- **Judge:** Rate each plan for coverage of target files, implementation approach, constraints and validation (against a reference plan where one exists), and each handoff for completeness.
- **Probes:** Multi-file tasks whose request leaves out requirements the repository reveals, where a design decision must precede coding.

## How (outline)

1. Start from one continuous session on your real tasks, with the harness's own compaction (see 5.a.i), and record where it goes wrong: the wrong problem solved, the fix put in the wrong place, requirements the request left out but the repository shows, rework after review. Split only the tasks that fail that way, typically large new features or multi-file changes in unfamiliar code; practitioners skip it for small fixes, bugs and one-off scripts, and 82.0% of the public specs studied describe new features. Do not assume the phases help by themselves: on 32 feature requests with one open model, running Spec Kit's spec, plan and tasks stages before coding scored 3.51 against 3.46 for implementing directly on a 1-to-5 judge scale, and its completed runs took 24.0 against 14.4 minutes.
2. Research: run a read-only session (no edit tools) that explores the code and writes a research document in fixed fields: the requirements, including those the request does not state; the relevant files with paths and line references; how the current behavior works; components and how they depend on each other; interfaces; constraints and conventions; and how each requirement will be checked, with every entry pointing to the file, line or passage it came from. In one ML-research pipeline, a structured specification built this way scored 29.87 against 24.14 on PaperBench and used 564K against 842K tokens per paper compared with the planner reading the paper directly. Tell the session to treat the request as evidence rather than the full specification and to keep exploring until it can say how each requirement will be checked: unstated requirements were the earliest failure in 24.5% to 46.0% of runs per configuration across 18 current agent and model pairs, a plan phase that stopped exploring early wrote plans covering only part of the task, and HumanLayer traced its own failed 7-hour attempt to research that did not go deep enough through the dependency tree.
3. Plan: start a fresh session from the request and the research document only, and have it write a plan file: every change file by file, the reason for each, the constraints it must respect (compatibility, boundary conditions) and the test or command that validates it. Agents' own plans covered where to edit far more often than how to constrain and verify the change (79.7% against 41.6% of a gold plan's information points for Claude Code, 65.6% against 37.1% for Codex), so check those parts first. Use your strongest model here: a stronger planner's plans raised resolution by 6.0 to 16.8 points, the implementer's own model as planner recovered 12 of 223 failures against 9 with no plan, and a weaker planner's plans broke 14.6% of passing runs. Keep detail that names classes, functions or library versions scoped to this change; it is what goes stale first.
4. Review at each boundary: first check the documents mechanically against the repository (every path named exists, every dependency is installed, the task order is feasible), then have a person read the research document and the plan before the next phase starts and correct or reject them, because a wrong line of research or plan turns into many wrong lines of code. In one study an LLM judge scored read-only discovery before each phase plus these checks after it 3.66 against 3.51 without them (the checks alone 3.57), but blinded human raters on six tasks preferred the runs without them 19 to 8 (33 ties), so confirm they help on your own reviews. Check that the review happens; most spec-driven tool users read specs only partially or handed the review to another agent.
5. Implement: start a fresh session with the request, the plan file and a structured handoff in fixed fields (files changed or to change, validation commands and results, what failed, what is still uncertain, what to verify first), and tell it to check the plan against the repository rather than trust it. Notes cost part of the raw history's gain (+4.4 to +5.0 against +6.1 points for the same model), so keep the research transcript where the implementer can read it on demand. If research and planning used little context, appending the plan to the same session is cheaper: a fresh implementer matched the continuing one (58.6% vs 58.2%) but needed 2.0 times the executor calls on failed tasks.
6. After the change merges, update or archive the research and plan files so no later session reads them as current (see 4.b.iii).
7. Measure with paired runs on the same tasks and models: one continuous session, the plan in the same session, and the phase split, with and without the boundary review; report task success, requirement coverage on tasks whose request omits requirements, runs the baseline solved that the variant broke, a structure or design score against a reference or rubric as well as tests (design documents moved a rebuilt library's modules closer to the original, module F1 0.54 to 0.63, without changing held-out tests passed, 33.7% against 35.8%), tokens and wall time per phase and human review minutes; check any LLM judge against blinded human ratings on a sample, and label each failure as research, plan, handoff or implementation.

## How to measure

- **experiment** (Tier 4): paired runs on the same tasks, model and budget: one continuous session with compaction, a plan in the same session, and the phase split with fresh contexts, each with and without the boundary review; include tasks whose instruction omits requirements that hidden tests check; report task success, requirement coverage, baseline-solved runs the variant broke, a structure or design score against a reference or rubric alongside tests, tokens and wall time per phase and review minutes; check any LLM judge against blinded human ratings on a sample; repeat with the planner on a stronger model and on the implementer's model, and again after a model upgrade
- **monitor**: per task: phases run, tokens and time per phase, handoff size, files the implement phase re-reads that research already covered, plan coverage of target files, approach, constraints and validation, edits made to the plan at review and whether a reviewer opened it, failures traced to research, plan or handoff, and research or plan files older than the code they describe

## Expected impact

- **Quality:** mixed, medium: pays when the document knows more than the implementer finds alone: a stronger model's plan at the first edit +6.0 to +16.8 points on SWE-bench Verified, a fresh implementer from that plan alone 58.6% vs 58.2% for the continuing session; the implementer's own model as planner 12 of 223 failures recovered against 9 with no plan, and a weaker planner's plans 43.4% against a 45.6% baseline with 14.6% of passing runs broken (Patel, Oct 2026); a structured specification tied to its sources 29.87 vs 24.14 on PaperBench against the planner reading the paper directly (Liu, Nov 2026); little from the phases alone: Spec Kit's spec, plan and tasks stages 3.51 vs 3.46 for direct implementation on a 1-5 judge scale, repository checks around each phase 3.66 by the judge but blinded raters preferring the runs without them 19 to 8 (Taghavi, Apr 2026); requirements and architecture documents 35.8% vs 33.7% held-out tests (not significant) but module F1 0.54 to 0.63 (Sas, Oct 2026); under incomplete instructions a read-only plan phase never raised Success@1 and cut Score@1 from 68.8 to 55.3 and 66.3 to 55.0 for two of three models (Liu, Oct 2026); agents' plans covering 24.8% to 41.6% of a gold plan's constraint and validation points against 43.8% to 79.7% for where to edit (Zhou, Aug 2026); distilled notes +4.4 to +5.0 points against +6.1 for the raw history, same model (KC, Jun 2026); one team's 35k LOC in 7 hours, anecdotal (Horthy, Aug 2025)
- **Cost:** mixed, medium: more when the next phase must re-explore: a fresh implementer from the same plan used 2.0 times the executor calls and 22% more executor tokens on failed tasks, and 519.1M against 347.4M executor tokens on 500 tasks (Patel, Oct 2026); planning itself adds tokens, one team reporting two to three times those of direct prompting, self-reported (Agarwal, Oct 2026); design documents added prompt text (4.8k vs 1.0k tokens) without changing agent steps (858 vs 869) (Sas, Oct 2026); fewer when a written document replaces repeated reading: a structured specification 564K vs 842K tokens and $7.91 vs $10.08 per paper (Liu, Nov 2026), and a same-model successor given notes 602k to 660k prompt tokens against 811k with the raw trace, its first prompt about 10k characters against 87k (KC, Jun 2026)
- **Performance:** degrades, medium: phases run in sequence and wait for review: completed runs with Spec Kit's stages took 24.0 against 14.4 minutes for direct implementation (different completed subsets, 90 and 40 minute budgets), and repository checks around each phase raised that to 37.2 minutes (Taghavi, Apr 2026); a fresh implementer needed 2.0 times the executor calls (Patel, Oct 2026); a successor working from notes took a median 53 to 55 steps against 41 with the raw trace (KC, Jun 2026); one team reported about twice the time, self-reported (Agarwal, Oct 2026); 3 of 7 hours went to research and plans (Horthy, Aug 2025); no source measures review wait time
- **Security:** none (unmeasured)
- **Governance:** mixed, medium: research and plan files are a reviewable record of intent, and reading a 200-line plan instead of 2,000 lines of code is the stated point (Horthy, Aug 2025); in practice most spec-driven tool users read specs only partially or delegated review to other agents, 98.3% of spec files with history had one author, 68.5% of inline spec comments came from bots, and specs went stale as code changed (Agarwal, Oct 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Dex Horthy (HumanLayer), "Getting AI to Work in Complex Codebases"… (2025-08-29): "We use a "research, plan, implement" workflow"; reports shipping 35k LOC to BAML in 7 hours (3 on research/plans, 4 on implementation). A 7-hour attempt to remove Hadoop dependencies from parquet-java "did not go well": "the research…
- Viral Patel, Boyin Tan, Jason Xue, Youcheng Sun, "PAUSE: Search-Free Steering of Coding Agents Before Their First Source-Code Edit"… (2026-10-21): Online with GPT-5.6 Sol as Planner, SWE-bench Verified resolution rose from 50.2% to 65.0% (SWE-agent), 37.0% to 43.0% (Pi) and 45.4% to 62.2% (OpenHands); Multilingual 28.3% to 43.0%. On 223 recorded Qwen3-coder failures: no plan…
- Kaiming Liu, Yuxuan Liu, Jinrui Ju, Minyuan Ruan, Xuanyu Lei, Peng Li, Yang Liu, "Instructions Are Evidence, Not Objectives: Measuring… (2026-10-13): Score@1 (share of five requirements passed) and Success@1 (all passed), without vs with plan mode: GPT-5.6-Luna 41.6 vs 45.9 and 3.1 vs 3.1; Kimi-K3 68.8 vs 55.3 and 21.9 vs 17.2; DeepSeek-V4.1-Flash 66.3 vs 55.0 and 25.0 vs 21.9. "the…
- Shyam Agarwal, Anmol Singhal, Andrew Macvean, Bogdan Vasilescu, Travis Breaux, "Spec-Driven Development as Prescribed and as Practiced"… (2026-10-15): Practitioners "used SDD selectively", skipping it for small tasks, bugs and one-off scripts; an estimated 82.0% of specs describe new features. "Most tool users read specs only partially or delegated their review to other agents"; 98.3% of…
- …and 5 more sources in `library/entries/discrete-phase-separation.yaml`.

## Caveats

The one controlled comparison of a spec-driven tool's phases against implementing directly found little difference (one open model, 32 features, one run each, an LLM judge, plan review auto-approved), and no study we found compares the full research, plan and implement split with human review against one continuous session on the same tasks. The other measured results cover a plan injected at the first edit, where the gain comes from a stronger planner model; a same-session plan mode under deliberately partial instructions (64 tasks, three models); mid-task handoffs between 24B to 31B open-weight models; design documents recovered from the target code for library rebuilds whose interface the agent is given (one open model); a specification ablation inside its authors' own ML-research system (20 papers, no repeated runs reported); and plan coverage read from agents' trajectories by an LLM judge. Plans can hurt: a weaker planner's plans broke passing runs, a plan written after too little exploration covered only part of the task, distilled notes kept less of the solve-rate gain than the raw history, and an LLM judge and blinded human raters disagreed on whether repository checks around each phase improved the result. The practice evidence is self-reported (practitioners could not separate the benefit from model improvements, one team reported two to three times the tokens and about twice the time, and the 35k-LOC report is one team's anecdote), and human review time remains unmeasured.

## Related

- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:initializer-maintainer-agents` (4.b.ii, Initializer-maintainer dual agent)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)

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
