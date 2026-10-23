---
name: inject-runtime-context
description: "AOT optimization 3.a.iii (Tier 3, Tuning): Dynamic context injection. Placeholder. Use when an agent shows: Model guesses the date or year, asks the user for information the system already has, builds queries with stale dates."
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

Put the runtime facts the model cannot know into its context each run: today's date and timezone, the working directory, OS and git state, the tools available, the user and locale. Inject them after the cached prefix, as a date rather than a timestamp, and refresh them when they change. The measured gains are on time-sensitive work: absolute dates beat relative ones, and stating the time remaining each turn raised deal closure under deadlines. On tasks that do not depend on time, the date only adds variance.

## When it applies

- **In the code:** Prompt templates contain runtime placeholders (date, time, user, locale, tool availability). Absence where tasks are time- or user-sensitive is the signal.
- **In traces:** Model guesses the date or year, asks the user for information the system already has, builds queries with stale dates.
- **In eval results:** Failures concentrated on time-sensitive or user-specific items.
- **Judge:** Flag outputs that assume stale state.
- **Probes:** Tasks whose answer depends on today's date, relative dates, locale or the current user.

## How (outline)

1. List the runtime facts your tasks depend on: date and IANA timezone, working directory, OS and shell, git status, the tools or skills available, the user and locale.
2. Inject them after the cached prefix, in a trailing block or a message in the conversation, never under a cache breakpoint; keep the date to the day, and serve time of day through a clock tool or the shell.
3. State dates as absolute values, and resolve relative dates ("last quarter") to absolute ones before the model sees them.
4. Refresh on change: resend the block when a value changes and after compaction or resume; if the run has a deadline, inject the time remaining each turn.
5. Fix the date in evals and report it; run a time-sensitive slice with and without the injection, and watch cache-read tokens.

## How to measure

- **before-after** (Tier 3): run a time-sensitive slice with and without the injected block, with the date fixed; compare cache-read tokens per call before and after
- **monitor**: questions asking the user for facts the system holds, date errors in outputs, cache-hit rate

## Expected impact

- **Quality:** mixed, medium: time-sensitive work: deal closure 0.04 to 0.32 with the time remaining stated each turn (Sehgal, Jan 2026); answers 24-35% worse with relative than with absolute dates (Wallat, 2024). On tasks that do not depend on time, the date moved scores by up to 14% with no good date to fix (Sanz-Guerrero, Sep 2026)
- **Cost:** none: if the block sits after the cached prefix; a date in the system prompt cost Claude Code cache hits until it was moved out (Feb 2026)
- **Performance:** none
- **Security:** mixed, small (unmeasured): Injected state is a small injection surface.
- **Governance:** mixed, small (unmeasured): User data in the prompt needs retention rules.
- **Brand:** improves, small (unmeasured): Fewer obviously wrong dates.

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Anthropic, "System Prompts" (release notes), https://docs.claude.com/en/release-notes/system-prompts: Claude's web and mobile apps "use a system prompt to provide up-to-date information, such as the current date, to Claude at the start of every conversation."
- Zhao, Brumbaugh, Wang, Hajishirzi, Smith, "Set the Clock: Temporal Alignment of Pretrained Language Models"… (2024-02-26): F1 on questions about 2022 rose from 17.2 to 24.4 with the year in a 5-shot prompt. The authors also note that "prompting LMs to be aligned to a more recent year could lead to more QA errors."
- Wallat, Jatowt, Anand, "Temporal Blind Spots in Large Language Models", https://arxiv.org/abs/2401.12078 (2024-01-22): Performance dropped 24-35% for text-davinci-003 and 23-30% for alpaca-7B with relative references; both models answered 2021 when asked what year it is.
- Sehgal, Guntuku, Ungar, "Real-Time Deadlines Reveal Fragile Temporal Adaptation in LLM Strategic Dialogues"… (2026-01-19): Deal closure rose from 0.04 (12/300) to 0.32 (97/300) for GPT-5.1; offers were over six times more likely to be accepted (OR = 6.38). GPT-4.1 went from 44.7% to 72.0%. "only 5 of 10 comparisons reach Bonferroni-corrected significance."
- …and 4 more sources in `library/entries/inject-runtime-context.yaml`.

## Caveats

Few studies isolate the date on agent tasks; the measured support is indirect: a stated year, absolute against relative dates, the time remaining in a negotiation. On tasks that do not depend on time the date only adds variance, and chain-of-thought amplifies it, so fix the date in evals. Some providers already add a date server-side, so check the model is not seeing two. Any per-request value placed before the cached prefix turns every call into a cache write (3.b.i).

## Related

- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)

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
