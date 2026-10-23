---
name: rewrite-tool-surface
description: "AOT optimization 2.a.ii (Tier 1, Hygiene): Rewrite the tool surface: names, schemas, descriptions. Placeholder. Use when an agent shows: misrouted cases per tool (false positives and false negatives); failure rows labeled incorrect-tool-selection, malformed-arguments or suboptimal-arguments; per-tool error rate and retries (Datadog tracks these per tool and server)."
---

<!-- Generated from library/entries/rewrite-tool-surface.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Rewrite the tool surface: names, schemas, descriptions

> **Placeholder.** Generated from `library/entries/rewrite-tool-surface.yaml` (entry 2.a.ii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.a.ii |
| Earlier id | T35 |
| Tier | 1 (Hygiene): when the hand-labeled set shows behavior unchanged |
| Categories | Tools: Refactoring; Tools: Avoiding misuse |
| Change | tool / api (reword) |
| Also covers | Low-friction tool input formats; Poka-yoke tool design; Tool namespacing |

## What it is

Change what the model sees of each tool without touching its implementation: a distinct name, a strict schema (enums, required fields), and a description with fixed sections (what it is for and when to use it versus sibling tools, defaults and limits, error modes, side effects), plus a usage example for complex parameters. Write for the model: distinctive terms, since search finds tools by them; error messages that say what to do next. One rewrite fed the misrouted cases matches hand-tuning; richer descriptions add steps, so slim them after. Where two tools genuinely overlap, rewording cannot separate them: consolidate instead (2.a.i).

## When it applies

- **In the code:** descriptions that do not state the tool's purpose (56% of audited MCP tools) or when to use it; duplicate or overlapping names; schemas without enums or required fields; no example for complex parameters
- **In traces:** misrouted cases per tool (false positives and false negatives); failure rows labeled incorrect-tool-selection, malformed-arguments or suboptimal-arguments; per-tool error rate and retries (Datadog tracks these per tool and server)
- **In eval results:** failures attributed to tool selection or arguments; step count per task after a description change

## How (outline)

1. From traces, collect misrouted cases per tool (called when it should not have been, and not called when it should).
2. Audit descriptions for missing purpose, missing when-to-use, and duplicate names.
3. Rewrite once with an LLM, given the misrouted cases; add a usage example for complex parameters.
4. Slim the result and check step count.
5. Replay the hand-labeled set, or run the paired eval; pairs that stay confused go to 2.a.i for consolidation.

## How to measure

- **verify-fix** (Tier 1): replay the hand-labeled set
- **experiment** (Tier 3): paired eval, old against new descriptions

## Expected impact

- **Quality:** improves, medium: +5.85 pp median success (Feb 2026); complex-parameter accuracy 72% to 90% with examples (Anthropic); a compliant description picked 72% vs 20% among equivalents
- **Cost:** mixed, medium: augmented descriptions added 67% more steps; slim variants keep most of the gain
- **Performance:** mixed, small

## Evidence (summary)

- repo figure_01: 7 to 18 of 20 runs per benchmark.
- paper Table 11: The Tool-Centric template is built around docstring guidance and parameter design.
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "an agent searching the web for context that only exists in Slack is doomed from the start" ... "Bad tool descriptions can send agents down completely wrong paths, so each tool needs a distinct purpose and a clear description."
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "This process for improving tool ergonomics resulted in a 40% decrease in task completion time for future agents using the new description, because they were able to avoid most mistakes." (no benchmark, n or model beyond "Claude 4 models")
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Every tool description in the study uses this template. Not ablated.
- …and 13 more sources in `library/entries/rewrite-tool-surface.yaml`.

## Related

- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
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
