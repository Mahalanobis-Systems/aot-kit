---
name: model-and-effort-per-call-site
description: "AOT optimization 1.b.i (Tier 3, Tuning): Match the model and its effort to each call site and query class. Placeholder. Use when an agent shows: simple queries using as many steps, tokens or sub-agents as complex ones; a call site whose cost dominates with no quality reason; retries exhausted or timeouts at one site."
---

<!-- Generated from library/entries/model-and-effort-per-call-site.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Match the model and its effort to each call site and query class

> **Placeholder.** Generated from `library/entries/model-and-effort-per-call-site.yaml` (entry 1.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 1.b.i |
| Earlier id | T65 |
| Tier | 3 (Tuning): model per call site within the existing design |
| Categories | Models: Finding specialists; Models: Benchmarking workloads; Prompts: Sizing reasoning effort |
| Change | config / model_settings (tune) |
| Also covers | Chain-of-thought; Routing to specialists |

## What it is

Pick the model per role or call site rather than one model everywhere, and set its reasoning effort and sampling parameters per site; tune each role's prompt to its model (GEPA raised every model tested at lower cost). Give the agent explicit effort budgets by query class (e.g. one agent and 3-10 tool calls for simple fact-finding) so simple queries are not over-served. Upgrade the model generation before doubling token budgets. A prompt that forces stepwise reasoning is the same lever from the prompt side and hurt on GPQA; prefer the model's own effort setting.

## When it applies

- **In the code:** one model and one effort setting for every call site; no per-query-class budget
- **In traces:** simple queries using as many steps, tokens or sub-agents as complex ones; a call site whose cost dominates with no quality reason; retries exhausted or timeouts at one site
- **In eval results:** quality and cost per call site, per model; price not predicting quality across the measured configurations (in an email-triage agent we measured: Spearman 0.12)

## How (outline)

1. From traces, list call sites and their token, cost and error profile.
2. For each, run a small model grid (cheaper, specialist, effort levels) on the eval slice that exercises it. Sweep effort rather than max it, since forced extra thinking cut GSM8K accuracy from 87.3% to 70.3% (1,100 to 15,980 thinking tokens), majority-voted parallel traces beat one long trace at the same budget (+10.1%), and stopping once a candidate answer appears cut reasoning tokens by 24.5% for a 2.9-point accuracy drop.
3. Optimize each site's prompt for its model.
4. Add per-query-class budgets.
5. Paired eval per call site.

## How to measure

- **experiment** (Tier 3): paired eval per call site and per query class

## Expected impact

- **Quality:** improves, medium: Genie: 81.4% to 91.6% with a model per role (May 2026); in an email-triage agent we measured, the best recall came from gpt-5-nano at low effort
- **Cost:** improves, large: Genie 2.13x to 0.95x cost

## Evidence (summary)

- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Figure 1, internal benchmark: + Multi-LLM (GPT-5.4 + Opus 4.6) on top of parallel thinking 81.4% -> 91.6% (+10.2pp) while relative cost falls 2.13x -> 0.95x (baseline code agent = 1.00x). Bundled with GEPA-optimized prompts ("Multi-LLM…
- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Figure 6, end-to-end accuracy of the Multi-LLM agent vs relative token cost (Sonnet 4.5 baseline = 1.0), approximate reads, baseline -> GEPA-optimized table-search sub-agent: Sonnet 4.5 ~73.1% @1.00 -> ~78.2% @~0.80; GPT-5.4 ~71.8% @~0.76…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): OpenCode "nine base prompts by model-id substring"; Codex per-generation prompts delivered as server-side catalog data; Hermes "15 guidance blocks gated by model family (tool-use enforcement blocks are sent to…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Aider "per-model metadata for 350+ models"; "This data-driven approach enables support for new models without code changes"; Pi "20 per-model compat quirk flags"; OpenCode 1,400-line per-vendor transform matrix.
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Aider picks among 13 edit formats via Coder.create() from model metadata; OpenCode "GPT-family models receive a port of Codex's apply_patch DSL and lose edit/write entirely"; OpenHands "model-specific tool presets (default, gemini, gpt5…
- …and 14 more sources in `library/entries/model-and-effort-per-call-site.yaml`.

## Caveats

The model checkpoint itself is off-limits under VeRO's rules; only its call parameters move.

## Related

- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)
- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)

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
