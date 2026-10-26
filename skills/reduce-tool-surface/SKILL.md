---
name: reduce-tool-surface
description: "AOT optimization 2.a.i (Tier 1, Hygiene): Reduce the tool surface: remove and consolidate tools, then defer the rest behind search. Placeholder. Use when an agent shows: tools never called across the eval runs; tool-use coverage below the eval's needs (share of needing cases where the right tool was loaded and chosen; GitHub measured 69% for a static list); calls to a tool where none was needed; failure rows labeled incorrect-tool-selection concentrated on one pair of tools."
---

<!-- Generated from library/entries/reduce-tool-surface.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Reduce the tool surface: remove and consolidate tools, then defer the rest behind search

> **Placeholder.** Generated from `library/entries/reduce-tool-surface.yaml` (entry 2.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.a.i |
| Earlier id | T60 |
| Tier | 1 (Hygiene): removing tools that are never called, verified unchanged on the hand-labeled set |
| Categories | Tools: Refactoring; Context: Filtering input |
| Change | tool / api (restructure) |
| Also covers | Consolidate tools into higher-level operations; Progressive tool discovery |

## What it is

Offer the agent only the tools the task needs. First remove tools no task uses; then consolidate tools with overlapping scopes (read and write tools with a method parameter, tools grouped around jobs), because rewording cannot separate tools that genuinely overlap. Then keep a small core always loaded and defer the rest: names and one-line purposes in the prompt, full definitions loaded on demand through tool search, per-server files or expandable groups. Defer once definitions exceed about 10k tokens or 10 tools; keep deferred groups under about 10 tools each. Every tool offered has a cost even when not called: one irrelevant tool cut accuracy from 98.2% to 63.5%. Deferral costs extra calls (2-3x) and time (about 50%), so consolidate first.

## When it applies

- **In the code:** more than about 10 tools, or more than about 10k tokens of tool definitions, in every prompt; duplicate or near-duplicate tool names or descriptions (73% of audited MCP servers have repeated names); tools the agent's credentials cannot use
- **In traces:** tools never called across the eval runs; tool-use coverage below the eval's needs (share of needing cases where the right tool was loaded and chosen; GitHub measured 69% for a static list); calls to a tool where none was needed; failure rows labeled incorrect-tool-selection concentrated on one pair of tools
- **In eval results:** accuracy falling as tools are added (an ablation over catalog size); paired eval, current tool set against a reduced one

## How (outline)

1. From traces over the eval set, list each tool's call count and the cases where it was needed.
2. Remove tools with no calls and no needing case.
3. Find overlapping pairs (similar names or descriptions, or cases routed to the wrong one of the pair) and merge them; a method parameter often replaces several tools.
4. If what remains exceeds about 10 tools or 10k tokens, keep a core loaded and defer the rest behind search or expandable groups.
5. Run the paired eval, old set against new, and compare coverage, success, calls and latency.

## How to measure

- **verify-fix** (Tier 1): replay the hand-labeled set after removing unused tools
- **experiment** (Tier 3): paired eval, old tool set against new: success, coverage, calls, latency

## Expected impact

- **Quality:** improves, medium: GitHub +2-5 points on SWE-bench with 40 to 13 tools (Nov 2025); Anthropic tool search 49% to 74% (Opus 4); one irrelevant tool cost 34.7 points on questions answerable without tools (Sep 2026)
- **Cost:** improves, large: definitions -85% (Anthropic); -46.9% tokens (Cursor A/B); deferral alone raises call count
- **Performance:** mixed, medium: consolidation faster (GitHub -400 ms); deferral about 50% slower with 2-3x calls (Speakeasy)

## Evidence (summary)

- Jediah Katz (Cursor), "Dynamic context discovery", https://cursor.com/blog/dynamic-context-discovery (2026-01-06): "In an A/B test, we found that in runs that called an MCP tool, this strategy reduced total agent tokens by 46.9% (statistically significant, with high variance based on the number of MCPs installed)." No n, model or quality metric given.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "This lets the agent load only the definitions it needs for the current task. This reduces the token usage from 150,000 tokens to 2,000 tokens, a time and cost saving of 98.7%." (single Google Drive to Salesforce example; model not…
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "Including a detail level parameter in the search_tools tool that allows the agent to select the level of detail required ... also helps the agent conserve context and find tools efficiently."
- Drew Breunig, "How Long Contexts Fail / How to Fix Your Context"… (2025-06-22): RAG-MCP (Gan & Sun), DeepSeek-v3: selection "becomes critical when you have more than 30 tools"; "Beyond 100 tools, the model was virtually guaranteed to fail"; RAG-selecting under 30 tools gave "as much as 3x better tool selection…
- Xiaofang Yang, Lijun Li, Heng Zhou, Tong Zhu, Xiaoye Qu, Yuchen Fan, et al. (Shanghai AI Lab et al.), "Toward Efficient Agents: A Survey of… (2026-01-20): TinyAgent (DeBERTa-v3 small multi-label selector, >50% threshold) 'reduces nearly half of the prompt size'. The other methods give no numbers. Trade-off: aggressive selection 'may filter out necessary tools'.
- …and 27 more sources in `library/entries/reduce-tool-surface.yaml`.

## Related

- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)

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
