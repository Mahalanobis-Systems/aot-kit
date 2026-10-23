---
name: bound-tool-output
description: "AOT optimization 2.c.i (Tier 3, Tuning): Bound tool output: cap it, or write it to a file the agent can read. Placeholder. Use when an agent shows: a single tool result over about 10% of the context window; context-overflow outcomes; a truncated result followed by re-running the same command."
---

<!-- Generated from library/entries/bound-tool-output.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Bound tool output: cap it, or write it to a file the agent can read

> **Placeholder.** Generated from `library/entries/bound-tool-output.yaml` (entry 2.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.c.i |
| Earlier id | T02 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Tools: Trimming results; Context: Filtering input |
| Change | tool / transformation (tune) |
| Also covers | Token-efficient tool responses |

## What it is

Cap the characters of tool output kept per call (VeRO settled near 15-20 KB on TerminalBench), or, better, write long output to a file and return its path with a short head, so the agent can read more if it needs to. When the agent runs code, filter and aggregate results inside the execution environment and return only the slice it needs.

## When it applies

- **In the code:** tool results passed to the model whole, with no cap or file offload
- **In traces:** a single tool result over about 10% of the context window; context-overflow outcomes; a truncated result followed by re-running the same command
- **In eval results:** context-overflow outcomes as a share of failures

## How (outline)

1. From traces, find the largest tool results and the share of context they take.
2. Set a cap from the distribution of results on successful cases; or switch to file offload for that tool.
3. Re-run cases that previously overflowed or truncated.

## How to measure

- **experiment** (Tier 3): paired eval at the old and new cap, or cap against file offload; count overflow failures

## Expected impact

- **Quality:** mixed, small: a cap can drop what the agent needed; file offload avoids that (Cursor, unmeasured)
- **Cost:** improves, medium: VeRO: overflow errors 13 to 1 with a lower cap
- **Performance:** improves, small

## Evidence (summary)

- paper §A.4: 30KB to 15KB (Tools-B=89), 20KB (Filesystem-B=178), 17KB (Tools-B=178, after probing 15KB on 16 samples and seeing some tasks needed more). Filesystem run cut ContextLengthExceeded from 13 to 1.
- repo figure_04 (100 runs, five benchmarks): MAX_TOOL_OUTPUT_CHARS lowered 16 times, raised 13. The only frequently-touched constant lowered more often than raised.
- Jediah Katz (Cursor), "Dynamic context discovery", https://cursor.com/blog/dynamic-context-discovery (2026-01-06): Truncation "can lead to data loss"; the file approach "has resulted in fewer unnecessary summarizations when reaching context limits." No number.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): Illustrative: a 10,000-row sheet filtered to pending orders; "The agent sees five rows instead of 10,000." Not measured.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): With direct calls "the full call transcript flows through twice. For a 2-hour sales meeting, that could mean processing an additional 50,000 tokens" (estimate). Also: "models may be more likely to make mistakes when copying data between…
- …and 2 more sources in `library/entries/bound-tool-output.yaml`.

## Caveats

Samples 16, 17 and 47 regressed under every run; output-length changes are the usual suspect.

## Related

- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)

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
