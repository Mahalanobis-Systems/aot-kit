---
name: inject-runtime-context
description: "AOT optimization 3.a.iii (Tier 3, Tuning): Dynamic context injection. Placeholder. Use when an agent shows: Model guesses the date or year, asks the user for information the system already has, builds queries with stale dates, takes a retrieved past date as today, gives a fact as it was before a known change (or names the old value first), never calls an offered clock or date tool."
---

<!-- Generated from library/entries/inject-runtime-context.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Dynamic context injection

> **Placeholder.** Generated from `library/entries/inject-runtime-context.yaml` (entry 3.a.iii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 3.a.iii |
| Earlier id | P02 (Context Engineering, from the master cookbook) |
| Tier (proposed) | 3 (Tuning): it changes what the model sees |
| Categories | Prompts: Structuring |
| Change | prompt / context |

## What it is

Tell the model the runtime facts it cannot know: today's date and timezone, the working directory, OS and git state, the tools available, the user and locale. Inject them after the cached prefix, as a date rather than a timestamp, refresh them when they change, and when an answer depends on the date, state it in the question as well. The measured gains are on time-sensitive work: absolute dates beat relative ones, stating the time remaining each turn raised deal closure under deadlines, injecting vetted package versions cut code tasks with a known vulnerability from 36.70-55.70% to 10.90-27.60% across ten models, and instructions to resolve relative dates against the injected one took one search agent from 16.0% to 30.6%. The limits: in one study, with reasoning off, a date in the system prompt, an earlier turn or a date tool left most answers about a changed fact outdated, a stated past date does not hide what a model knows, and on tasks that do not depend on time the date only adds variance.

## When it applies

- **In the code:** Prompt templates contain runtime placeholders (date, time, user, locale, tool availability). Absence where tasks are time- or user-sensitive is the signal.
- **In traces:** Model guesses the date or year, asks the user for information the system already has, builds queries with stale dates, takes a retrieved past date as today, gives a fact as it was before a known change (or names the old value first), never calls an offered clock or date tool.
- **In eval results:** Failures concentrated on time-sensitive or user-specific items.
- **Judge:** Flag outputs that assume stale state.
- **Probes:** Tasks whose answer depends on today's date, relative dates, locale or the current user.

## How (outline)

1. Start from the baseline: with the date fixed, run a slice of time-, environment- and user-sensitive tasks with no injected block, including facts that changed after the model's cutoff, and record outdated answers, stale dates in queries, questions asking the user for facts the system holds, tool calls spent discovering the environment, and cache-read tokens per call.
2. List the runtime facts your tasks depend on: date and IANA timezone, working directory, OS and shell, git status, the tools or skills available, the user and locale, and for code that names dependencies the versions to use. In one study, injecting a vetted version for each library cut tasks with a known vulnerability from 36.70-55.70% to 10.90-27.60% across ten models, where an instruction to avoid vulnerable versions moved it by -2.2 to +4.3 points.
3. Inject them after the cached prefix, in a trailing block or a message in the conversation, never under a cache breakpoint; keep the date to the day, and serve time of day through a clock tool or the shell, with an instruction to call it. Where the answer depends on the date, also state it in the request itself ("as of <date>"): in one study, with reasoning off, today's date in the system prompt left 68-100% outdated answers about a changed fact for 10 of 12 models, five of six models never called an offered date tool, and the date in an earlier turn or a tool result left 69-99% outdated, while "as of" in the question left none for seven of eight models with reasoning on.
4. State dates as absolute values, and resolve relative dates ("last quarter") to absolute ones before the model sees them; tell a search agent to resolve relative dates against the injected date before calling tools and to keep dates it retrieves apart from the current one (one agent went from 16.0% to 30.6% as these instructions were added).
5. Refresh on change: resend the block when a value changes and after compaction or resume; if the run has a deadline, inject the time remaining each turn.
6. Fix the date in evals and report it, and check the chat template and the provider for a date you did not add. Do not rely on a stated past date to hide later knowledge in backtests: GPT-5 kept 0.75 accuracy against 0.76 with the date declared, while its claims of prior knowledge fell from 39% to 1%. Run the baseline slice with and without the injection, and with the date in the system prompt against the question, and watch cache-read tokens.

## How to measure

- **before-after** (Tier 3): with the date fixed, run a time-sensitive slice (including facts that changed after the model's cutoff) with and without the injected block, and with the date in the system prompt against in the question; count outdated answers, including answers that name the old value first, and compare cache-read tokens per call before and after
- **monitor**: questions asking the user for facts the system holds, date errors and outdated answers in outputs, stale dates in search queries, calls to any clock or date tool, cache-hit rate

## Expected impact

- **Quality:** mixed, medium: time-sensitive work: deal closure 0.04 to 0.32 with the time remaining stated each turn (Sehgal, Jan 2026); answers 24-35% worse with relative than with absolute dates (Wallat, 2024); a search agent 16.0% to 30.6% with instructions to resolve dates against the injected one (Zhou, Mar 2026). Today's date in the system prompt left 68-100% outdated answers for 10 of 12 models with reasoning off, where "as of" in the question left none for seven of eight with reasoning (Phan, Nov 2026). On tasks that do not depend on time, the date moved scores by up to 14% with no good date to fix (Sanz-Guerrero, Sep 2026)
- **Cost:** none: if the block sits after the cached prefix; a date in the system prompt cost Claude Code cache hits until it was moved out (Feb 2026)
- **Performance:** none, small (unmeasured): a short block after the cached prefix; no source measures latency
- **Security:** improves, medium: for code that pins dependencies: injected vetted versions cut tasks with a known vulnerability from 36.70-55.70% to 10.90-27.60% across ten models (Wang, May 2026). Injected state is also a small injection surface (not measured)
- **Governance:** mixed, small (unmeasured): User data in the prompt needs retention rules.
- **Brand:** improves, small (unmeasured): Fewer obviously wrong dates.

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Anthropic, "System Prompts" (release notes), https://docs.claude.com/en/release-notes/system-prompts: Claude's web and mobile apps "use a system prompt to provide up-to-date information, such as the current date, to Claude at the start of every conversation."
- Zhao, Brumbaugh, Wang, Hajishirzi, Smith, "Set the Clock: Temporal Alignment of Pretrained Language Models"… (2024-02-26): F1 on questions about 2022 rose from 17.2 to 24.4 with the year in a 5-shot prompt. The authors also note that "prompting LMs to be aligned to a more recent year could lead to more QA errors."
- Wallat, Jatowt, Anand, "Temporal Blind Spots in Large Language Models", https://arxiv.org/abs/2401.12078 (2024-01-22): Performance dropped 24-35% for text-davinci-003 and 23-30% for alpaca-7B with relative references; both models answered 2021 when asked what year it is.
- Sehgal, Guntuku, Ungar, "Real-Time Deadlines Reveal Fragile Temporal Adaptation in LLM Strategic Dialogues"… (2026-01-19): Deal closure rose from 0.04 (12/300) to 0.32 (97/300) for GPT-5.1; offers were over six times more likely to be accepted (OR = 6.38). GPT-4.1 went from 44.7% to 72.0%. "only 5 of 10 comparisons reach Bonferroni-corrected significance."
- …and 8 more sources in `library/entries/inject-runtime-context.yaml`.

## Caveats

Few studies isolate the date on agent tasks, and the newest are small: the placement results are post hoc, on 80 Vietnamese addresses in single runs, and the search-agent gain is one model on 320 questions with instructions added on top of the date. Models fall back on their training prior: with reasoning off, a date in the system prompt, an earlier turn or a date tool left most answers about a changed fact outdated, having a model rewrite each question with the date inserted the old fact as a premise into 9% of them, and a declared past date changed what GPT-5 claimed to know (39% to 1%) but not its accuracy (0.76 to 0.75). On tasks that do not depend on time the date only adds variance, and chain-of-thought amplifies it, so fix the date in evals; some chat templates and providers already add a date, so check the model is not seeing two. Any per-request value placed before the cached prefix turns every call into a cache write (3.b.i).

## Related

- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)

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
