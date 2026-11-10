---
name: reduce-tool-surface
description: "AOT optimization 2.a.i (Tier 1, Hygiene): Reduce the tool surface: remove and consolidate tools, then defer the rest behind search. Placeholder. Use when an agent shows: tools never called across the eval runs; tool-use coverage below the eval's needs (share of needing cases where the right tool was loaded and chosen; GitHub measured 69% for a static list); calls to a tool where none was needed; failure rows labeled incorrect-tool-selection concentrated on one pair of tools; first responses cut off at the output cap on long tool lists; three or more tool searches per task, or needed tools that search never returned."
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

Give an agent only the tools its tasks need, and put the rest behind tool search once the catalog is large. Remove tools no task uses, then merge overlapping ones into a few task-level tools (rewording cannot separate tools that genuinely overlap), but not into one catch-all tool: four task-level tools beat both 8-10 single-purpose tools and a single tool for small local models. Every listed tool costs tokens on every turn and costs some models accuracy: a related but unnecessary tool cut six models' pooled answer rate on questions they could answer unaided from 98.2% to 63.5% (two were unaffected), and growing the list from 8 to 128 tools cost 12.3 to 17.5 points across 21 current model configurations, mostly in those where the longer list used up a tight output cap (their 43.7-point loss fell to 2.7 once the cap was raised sixteenfold). Deferral pays at scale with a capable model (12.6k against 233.3k tokens per turn with 1,500 extra tools, success held level, fewer successful tool-injection attacks), but a weaker model lost 14.9 to 27.8 points driving discovery, search is slower and dearer on small catalogs (break-even about 25-28 tools in one vendor's cost model) and when the agent searches three or more times, and under prompt caching token savings overstate the bill (17.2% fewer input tokens, 5.5% lower bill), so consolidate first and measure per model.

## When it applies

- **In the code:** more than about 10 tools, or more than about 10k tokens of tool definitions, in every prompt; an MCP client or gateway that sends every connected server's tools on every request; duplicate or near-duplicate tool names or descriptions (73% of audited MCP servers have repeated names); tools the agent's credentials cannot use; a whole server collapsed into one catch-all tool
- **In traces:** tools never called across the eval runs; tool-use coverage below the eval's needs (share of needing cases where the right tool was loaded and chosen; GitHub measured 69% for a static list); calls to a tool where none was needed; failure rows labeled incorrect-tool-selection concentrated on one pair of tools; first responses cut off at the output cap on long tool lists; three or more tool searches per task, or needed tools that search never returned
- **In eval results:** accuracy falling as tools are added (an ablation over catalog size, with unrelated and with near-duplicate tools); paired eval, current tool set against a reduced one; completeness of tool search on labeled multi-tool requests

## How (outline)

1. Start from the baseline, per model: from traces over the eval set, list each tool's call count, the cases where it was needed, wrong-tool calls, tokens of tool definitions per request, searches per task, latency, billed cost with prompt caching on, and responses cut off at the output cap before any call.
2. Remove tools with no calls and no needing case, and tools the agent's credentials cannot use. Do not leave a tool in tasks it does not serve: a related but unnecessary tool cut six models' pooled answer rate on questions they could answer unaided from 98.2% to 63.5% (two models were unaffected); where it must stay, a one-sentence note on its scope raised the answer rate by up to 45.6 points in that study (2.b.ii).
3. Consolidate: find overlapping pairs (similar names or descriptions, or cases routed to the wrong one of the pair) and merge them; rewording cannot separate tools whose scopes genuinely overlap (2.a.ii). Group by task class, with an action or method parameter for closely related operations, but do not collapse a server into one catch-all tool: across nine small local models, four task-level tools completed 0.49 of tasks against 0.42 for 8-10 single-purpose tools, 0.42 for one read and one write tool, and 0.36 for a single tool, with which 28.2% of runs called no tool.
4. If what remains is still large, keep a small core of frequently used tools loaded and defer the rest behind tool search, per-server files or expandable groups of under about 10 tools each. Thresholds differ: Anthropic recommends deferral from 10 tools or 10k tokens of definitions; one vendor's cost model puts the break-even against a static list at about 25-28 tools; in one benchmark GPT-5.4 lost 0.5 points with 1,000 unrelated tools listed (87.2% to 86.7%) and 3.9 at 1,500, while tool search held level. First check that the model can drive discovery: with GPT-5.1, gateways that exposed tools through discovery scored 14.9 to 27.8 points below flat lists on the same tasks, while with GPT-5.4 they matched (85.1% against 87.2%).
5. Check search on your own requests: build probes from real multi-step tasks, label the full set of tools each needs (including the tools that produce the IDs later calls consume), and score completeness (every needed tool returned), not recall. At 2,048 registered tools a flat lexical retriever returned the needed tools in 19.4% of its shortlists against 77.8% for a router that picked the server first; one vendor's ranker covered every needed tool on the first search in 304 of 327 sessions, most misses coming from how the agent split the task. Count searches per task: against a 100-tool list one search cut session input a median 28.2%, while three or more raised it 32.3% to 43.8%.
6. Keep the prompt cache intact: keep the loaded core and the order of definitions fixed, and add discovered tools by appending (deferred loading, a tool-addition block) rather than rebuilding the list mid-session (3.b.ii, 3.b.i). Judge cost in dollars with caching on: with 85% to 87% of input served from cache, 17.2% fewer input tokens became a 5.5% lower bill (an interval that includes zero).
7. Measure with a paired eval per model, old tool set against new (and flat list against search where deferring), several runs per arm: success, search completeness, wrong-tool calls, calls and searches per task, tokens, billed cost, latency, and responses truncated at the output cap. Give reasoning models enough output budget for the tool list before blaming the tools: with a 1,024-token cap, going from 8 to 128 tools cost six truncation-heavy configurations 43.7 points, against 2.7 at 16,384. Where MCP servers come from third parties, add tool-injection probes: in one benchmark, gateways that exposed tools through discovery held tool-injection attack success at about 16% against 40.6% to 51.5% for flat lists with GPT-5.1, and about 31% against 45.1% to 53.9% with GPT-5.4; with GPT-5.1 discovery also cost up to 5.5 points of task success.

## How to measure

- **verify-fix** (Tier 1): replay the hand-labeled set after removing unused tools
- **experiment** (Tier 3): paired eval per model, old tool set against new and flat list against tool search where deferring, several runs per arm: success, completeness of what search returns on labeled multi-tool probes, wrong-tool calls, calls and searches per task, tokens, billed cost with caching on, latency, and responses cut off at the output cap
- **monitor**: per model in production: tools loaded per request and their tokens, searches per task, needed tools that search did not return (calls to unloaded tools, failed lookups), tools never called over a window, cache read share and billed cost per task

## Expected impact

- **Quality:** improves, medium: GitHub +2-5 points on SWE-bench with 40 to 13 tools (Nov 2025); Anthropic tool search 49% to 74% (Opus 4, Nov 2025); 8 to 128 listed tools -12.3 points across 21 configurations, -43.7 to -2.7 in truncation-heavy ones once the output cap was raised sixteenfold, 0.0 for Claude Opus 5.5 and GPT-6.1 Sol (Xu, Oct 2026); flat lists -3.9 to -10.0 points at 1,500 extra tools while tool search held level, but tool search 14.9-27.8 points below flat lists with GPT-5.1 (Zheng, Oct 2026); four task-level tools 0.49 task completion against 0.42 for 8-10 tools and 0.36 for one tool on small local models (Paschalides, Sep 2026); a related unnecessary tool cut the pooled answer rate from 98.2% to 63.5% (Paturi, Sep 2026)
- **Cost:** improves, medium: tool-definition tokens -85% (Anthropic, Nov 2025); agent tokens -46.9% in an A/B (Cursor, Jan 2026); 12.6k against 233.3k tokens per turn with 1,500 extra tools (Zheng, Oct 2026); against a 100-tool list, input -17.2% but bill only -5.5% under prompt caching with Codex (-39.6% and -21.8% with Claude Code, which also offloaded large results), while short lookups over 8-37 tools used 22.0% more input and three or more searches 32.3-43.8% more (Partee, Oct 2026, vendor's own system)
- **Performance:** mixed, medium: consolidation faster (GitHub -400 ms response time, Nov 2025); tool search slower with no extra tools (30.1 s against 20.8 s per task) and faster at 1,500 (38.7 s against 64.1 s), crossing between 500 and 1,000 (Zheng, Oct 2026); dynamic toolsets 2-3x calls and about 50% slower (Speakeasy, Nov 2025)
- **Security:** improves, medium: gateways exposing tools through discovery: tool-injection attack success about 16% against 40.6-51.5% for flat lists (GPT-5.1) and about 31% against 45.1-53.9% (GPT-5.4), no difference for injection through returned content or the user prompt, and a spread across discovery designs (about 20-41%) as wide as the gap (Zheng, Oct 2026; one benchmark, single run)

## Evidence (summary)

- Jediah Katz (Cursor), "Dynamic context discovery", https://cursor.com/blog/dynamic-context-discovery (2026-01-06): "In an A/B test, we found that in runs that called an MCP tool, this strategy reduced total agent tokens by 46.9% (statistically significant, with high variance based on the number of MCPs installed)." No n, model or quality metric given.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "This lets the agent load only the definitions it needs for the current task. This reduces the token usage from 150,000 tokens to 2,000 tokens, a time and cost saving of 98.7%." (single Google Drive to Salesforce example; model not…
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "Including a detail level parameter in the search_tools tool that allows the agent to select the level of detail required ... also helps the agent conserve context and find tools efficiently."
- Drew Breunig, "How Long Contexts Fail / How to Fix Your Context"… (2025-06-22): RAG-MCP (Gan & Sun), DeepSeek-v3: selection "becomes critical when you have more than 30 tools"; "Beyond 100 tools, the model was virtually guaranteed to fail"; RAG-selecting under 30 tools gave "as much as 3x better tool selection…
- Xiaofang Yang, Lijun Li, Heng Zhou, Tong Zhu, Xiaoye Qu, Yuchen Fan, et al. (Shanghai AI Lab et al.), "Toward Efficient Agents: A Survey of… (2026-01-20): TinyAgent (DeBERTa-v3 small multi-label selector, >50% threshold) 'reduces nearly half of the prompt size'. The other methods give no numbers. Trade-off: aggressive selection 'may filter out necessary tools'.
- …and 31 more sources in `library/entries/reduce-tool-surface.yaml`.

## Caveats

Most numbers come from one study each, often on synthetic tasks or mock servers with single runs (the menu-size and gateway benchmarks), small local models (the granularity study) or older models (the unnecessary-tool study), and many are vendors measuring their own products (Anthropic, GitHub, Cursor, Speakeasy, Arcade). How much an extra tool costs depends on the model, its output budget and how close the tool is to the needed ones: 1,500 unrelated tools cost GPT-5.4 3.9 points, 120 near-duplicate tools cost Claude Opus 5.5 and GPT-6.1 Sol 0.0 points, and a related unnecessary tool left two of six models unaffected while cutting another's answer rate by 76 points. Deferral has failure modes of its own: weaker models fail to drive discovery, retrievers miss needed tools (a flat lexical retriever had them in 19.4% of its shortlists at 2,048 tools), each search re-sends the conversation, and token savings shrink in dollars under caching. Exposing tools through discovery lowered tool-injection attack success in one benchmark, but the spread between discovery designs (about 20% to 41%) was as wide as the gap to flat lists, and it did nothing against injection through what tools return.

## Related

- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
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
