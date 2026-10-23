---
name: detect-loops-and-stalls
description: "AOT optimization 7.b.i (Tier 2, Reliability): Detect stalls and loops: warn, then stop early. Placeholder. Use when an agent shows: tool spans with identical name and arguments repeated 3 or more times in a run; the same query string issued twice; runs ending at the turn cap; failure rows labeled redundancy or state-tracking-failure."
---

<!-- Generated from library/entries/detect-loops-and-stalls.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Detect stalls and loops: warn, then stop early

> **Placeholder.** Generated from `library/entries/detect-loops-and-stalls.yaml` (entry 7.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 7.b.i |
| Earlier id | T05 |
| Tier | 2 (Reliability): an execution bound: runaway loops are hard failures |
| Categories | Orchestration: Bounding execution |
| Change | workflow / termination (add) |
| Also covers | Infinite-loop prevention by hashing recent calls |

## What it is

Track repeated identical actions (same tool, same arguments; same search query) and turns with no new information. Inject a warning at a small streak (about 5 identical calls), refuse exact-repeat queries, and end the run early at a longer streak (about 8 identical failures) or when progress has stalled, instead of running to the turn cap. A prompt line telling the agent not to repeat itself is a weak version of the same thing and is not a substitute.

## When it applies

- **In the code:** no comparison of a tool call or query against previous ones; the loop ends only at a fixed turn cap
- **In traces:** tool spans with identical name and arguments repeated 3 or more times in a run; the same query string issued twice; runs ending at the turn cap; failure rows labeled redundancy or state-tracking-failure
- **In eval results:** turn-cap and timeout outcomes as a share of failures

## How (outline)

1. In the loop, hash each tool call (name plus arguments) and each query; keep the last N.
2. On a streak of 5, inject a 'you are repeating; change approach' message; on 8 identical failures, stop with the best answer so far.
3. Define 'stalled' for the task (no new file, result or fact in K turns) and stop on it.
4. Measure loop and turn-cap failures before and after.

## How to measure

- **before-after** (Tier 2): loop and turn-cap failure rate on the same cases; time per case

## Expected impact

- **Quality:** improves, medium: adaptive termination +5.6% on FACTS; anti-loop prompt line GAIA +0.04, flat on SimpleQA (VeRO)
- **Cost:** improves, medium
- **Performance:** improves, medium: the template with query dedup ran about 2x faster, bundled

## Evidence (summary)

- paper §A.4: Part of the Filesystem-B=178 commit; contributed to AgentTimeoutError rising 16 to 23 as crashing tasks migrated to timeouts rather than passes.
- cookbook (master-agent-optimization-cookbook, Infinite Loop Prevention): Hash recent tool calls, inject a warning on repeat.
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Held fixed across all conditions. The reminder texts and thresholds are given.
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes hashes the call signature (SHA-256), "warning after two identical failures and halting after eight—but the hard stop ships disabled"; Gemini CLI aborts on "five identical tool calls or ten identical content chunks"; OpenCode's…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI LoopDetectionService: "after thirty turns in a single prompt an LLM-based self-check runs at an adaptive interval—a two-tier design"; paper calls this a "platform-tier investment".
- …and 5 more sources in `library/entries/detect-loops-and-stalls.yaml`.

## Related

- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)

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
