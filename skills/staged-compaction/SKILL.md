---
name: staged-compaction
description: "AOT optimization 5.a.i (Tier 2, Reliability): Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary. Placeholder. Use when an agent shows: context-overflow outcomes; peak context over about 85% of the window; summaries that drop file changes or decisions; failure rows labeled context-rationale-erosion."
---

<!-- Generated from library/entries/staged-compaction.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary

> **Placeholder.** Generated from `library/entries/staged-compaction.yaml` (entry 5.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 5.a.i |
| Earlier id | T31 |
| Tier | 2 (Reliability): stops runs dying on context overflow, a hard failure |
| Categories | Context: Compacting |
| Change | workflow / state_management (tune) |
| Also covers | Context compaction |

## What it is

Manage the history before it overflows. Past a soft threshold (about 60% of the window) replace old tool outputs with short stubs; only past a hard threshold (about 85%) summarize the oldest turns into a summary with fixed sections (goal, files touched, done, pending, errors, next step) that is updated incrementally, not regenerated. Keep the recent tail verbatim. The value is large at small windows and near zero at 128k; compaction alone does not carry multi-window work (see 4.b.iii for state kept in files).

## When it applies

- **In the code:** no compaction, or compaction that summarizes the whole history at once; a context window under about 64k
- **In traces:** context-overflow outcomes; peak context over about 85% of the window; summaries that drop file changes or decisions; failure rows labeled context-rationale-erosion
- **In eval results:** failures concentrated in the longest trajectories

## How (outline)

1. Measure peak context against the window on the longest runs.
2. Implement the two thresholds and the fixed-section summary.
3. Evaluate with post-compaction probes (recall, artifacts, next step) and tokens per task, not compression ratio.

## How to measure

- **before-after** (Tier 2): context-overflow rate on the same cases
- **experiment** (Tier 3): paired eval, tokens per task, post-compaction probes

## Expected impact

- **Quality:** improves, large: +35.7 points at 32k, +2.7 at 128k (Fan, Sep 2026); staged elision matches other strategies on success
- **Cost:** improves, medium: staged elision lowest cost in 7 of 8 panels, e.g. $1.45 against $2.57

## Evidence (summary)

- repo figure_04: MAX_HISTORY_CHARS lowered twice, never raised.
- repo figure_01: Context-management edits in 6 to 10 of 20 runs per benchmark.
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Managed tiers (T1-T4) vs no management (T0), averaged over 4 models (Nemotron-3 30B/120B/550B, Mistral-Medium-3.5-128B): the gap is 35.7, 15.9, 5.5 and 2.7 pp on SWE-Bench Verified (n=500) and 9.5, 7.5, 4.8 and 2.8 pp on Terminal-Bench 2.1…
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): T2 (elision+recall) vs T1 (elision) over 32 model-benchmark-window comparisons: 15 wins, 14 losses, 3 ties. Mean -0.36 pp (+0.40 SWE, -1.12 TB). 36 of 64 T2/T4 settings never call recall_event and the median rate is zero. Use is…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Claude Code "AUTOCOMPACT_BUFFER_TOKENS = 13 000"; post-compact restores "up to 5 files (POST_COMPACT_TOKEN_BUDGET = 50 000)"; Gemini "fires when history exceeds 50% ... preserves the most recent 30%"; Mistral Vibe envelope "re-injects…
- …and 14 more sources in `library/entries/staged-compaction.yaml`.

## Related

- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
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
