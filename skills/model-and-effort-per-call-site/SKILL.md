---
name: model-and-effort-per-call-site
description: "AOT optimization 1.b.i (Tier 3, Tuning): Match the model and its effort to each call site and query class. Placeholder. Use when an agent shows: simple queries using as many steps, tokens or sub-agents as complex ones; a call site whose cost dominates with no quality reason; trajectories that grow longer (more calls, more self-verification) at higher effort on tasks a lower setting already solves; many calls per task at effort none; retries exhausted or timeouts at one site."
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

Start each call site at a low reasoning effort and a model chosen on its own eval, instead of the top setting everywhere: on agentic coding tasks that every effort level solved, xhigh effort cost 2.5 to 5.3 times low effort, and on Terminal-Bench every one of eight models lost some tasks its lowest level had solved. Pick the model per role or call site and tune each role's prompt to its model (a model per role raised one data agent from 81.4% to 91.6% at lower cost; GEPA raised every model tested at lower cost), give explicit effort budgets by query class (e.g. one agent and 3-10 tool calls for simple fact-finding), and where an external check exists, escalate effort only after a verified failure, which matched or beat fixed top effort's success for all eight models, mostly at lower cost. Choose by measured cost and quality per task, not list price or release date: a model at a fifth of the per-token price cost only 3.2 times less per task and passed 16.4% of tasks against 27.1%, and the newer generation of each of three model families lost recall on one fraud benchmark (by up to 22.2 points), so try a newer model before doubling token budgets but benchmark it on the site's eval first. Routers that pick model or effort per query or turn often matched but did not beat the best single choice, and a prompt that forces stepwise reasoning is the same lever from the prompt side and hurt on GPQA; prefer the model's own effort setting.

## When it applies

- **In the code:** one model and one effort setting (often the top one) for every call site; no per-query-class budget; a model or version upgrade shipped without re-running the site's eval; several items packed into one call at a reasoning-heavy site
- **In traces:** simple queries using as many steps, tokens or sub-agents as complex ones; a call site whose cost dominates with no quality reason; trajectories that grow longer (more calls, more self-verification) at higher effort on tasks a lower setting already solves; many calls per task at effort none; retries exhausted or timeouts at one site
- **In eval results:** quality and cost per call site, per model; price not predicting quality across the measured configurations (in an email-triage agent we measured: Spearman 0.12)

## How (outline)

1. From traces, list call sites and their token, cost, latency and error profile; the baseline is the current model and effort at each site. Count realized cost per task (input including cache reads, reasoning and output, calls per task), not list price: in one spreadsheet-agent study Claude Haiku 4.5, at a fifth of GPT-5.6 Sol's input price, made about 41 calls per session against about 25 and cost only 3.2 times less per task while passing 16.4% against 27.1%.
2. For each site, run a small model grid (cheaper, specialist, effort levels) on the eval slice that exercises it. Sweep effort from the lowest level up rather than max it: in one eight-model sweep, on tasks every level solved, low to xhigh raised mean cost 2.51 to 5.34 times in the GPT-5.6 and Claude Sonnet 5 cases reported for Terminal-Bench and SWE-Bench Pro (up to 42 times across models and benchmarks), largely through longer trajectories (GPT-5.6-sol 14.7 to 28.4 calls), and on Terminal-Bench every model lost some tasks its lowest level had solved; xhigh cost 2.11 to 4.22 times medium on SlopCodeBench while strict passes fell for two of three models (one run each); Claude Opus 4.8 at low effort passed more multi-turn spreadsheet tasks than at high for 27 to 46% less cost. Forced extra thinking cut GSM8K accuracy from 87.3% to 70.3% (1,100 to 15,980 thinking tokens), majority-voted parallel traces beat one long trace at the same budget (+10.1%), and stopping once a candidate answer appears cut reasoning tokens by 24.5% for a 2.9-point accuracy drop. Include 'none' in the sweep but count its calls: GPT-5.6-luna made 21.5 calls at none against 5.4 at low and cost 4.58 times as much.
3. Where the site has an external correctness check (tests, a verifier), run it at the lowest effort and retry at the top effort only after a failed check. Across eight models this matched or beat fixed top effort on every benchmark, at median cost savings of 25.3% (AIME), 41.5% (GPQA) and 15.5% (corrected SWE-Bench Pro), with cheaper runs for four of eight models on Terminal-Bench (GPT-5.6-sol 83.0% to 88.6% success at 17.4% lower cost); letting the model pick its own effort from the task description did no better than random allocation.
4. Optimize each site's prompt for its model (GEPA raised every model tested as a table-search sub-agent at lower cost), and keep per-model prompt variants and metadata in a registry so a model swap does not need code changes.
5. Add per-query-class budgets (e.g. one agent and 3-10 tool calls for simple fact-finding, 2-4 sub-agents for comparisons). If a multi-turn agent routes per user turn, give the router the session history (at a matched offloading rate it raised pass rate from 25.0% to 28.3%) and switch down early rather than up late: at that study's prices a switch to a cheaper model recovered its lost prompt cache in about 1.25 calls, an upward switch never did. In long coding tasks, let the capable model start and hand the rest to the cheaper one, not the reverse: on DeepSWE, handoffs to Qwen3.8-27B at 30 to 60% of the trajectory kept accuracy within a point of the capable model at 47.9 to 82.4% lower cost, while cheap-first handoffs saved little (6.1% for GPT-5.6 Sol) or lost accuracy.
6. Re-run the site's eval before any model upgrade, under the existing prompt and decision policy: on one fraud benchmark the newer Sonnet lost 22.2 recall points and the newer GPT 20.7, although general benchmarks improved. Do not pack several items into one call at a reasoning-heavy site, since per-item reasoning shrinks with the number of items (random batches of six lost 10.5 points on GPQA-Diamond, eight-model mean).
7. Paired eval per call site and query class, with repeated runs: success, tasks gained and lost against the current setting (not only the aggregate), realized cost per task, calls per task and latency per model and effort level.

## How to measure

- **experiment** (Tier 3): paired eval per call site and per query class: each candidate model and effort level (from the lowest, including none where offered) on the same items, with repeated runs; success, tasks gained and lost against the current setting, realized cost per task (input incl. cache reads, reasoning, output), calls per task and latency; for escalation or routing policies, charge both attempts and the router calls
- **monitor**: per call site in production: cost per task, calls per trajectory, latency, escalation or routing rate and quality on sampled traffic; re-run the site's eval on every model or provider version change before switching

## Expected impact

- **Quality:** improves, medium: Genie: 81.4% to 91.6% with a model per role (May 2026); in an email-triage agent we measured, the best recall came from gpt-5-nano at low effort; escalating effort only after a failed check raised Terminal-Bench success for all eight models tested, e.g. GPT-5.6-sol 83.0% to 88.6% (Sun, Oct 2026); Opus 4.8 at low effort beat high on multi-turn spreadsheets, 31.2% vs 29.5% and 36.7% vs 32.1% (Parashar, Oct 2026); limits: newer generations lost 20.7 and 22.2 recall points on one fraud benchmark (Ma, Oct 2026), and cheap-first model handoffs lost accuracy (Li, Oct 2026)
- **Cost:** improves, large: Genie 2.13x to 0.95x cost (May 2026); on tasks every level solved, low to xhigh effort cost 2.51-5.34x on agentic benchmarks and up to 42x across all benchmarks, and escalating only after a failed check saved a median 15.5 to 41.5% against fixed top effort (Sun, Oct 2026); xhigh cost 2.11-4.22x medium on SlopCodeBench (Horthy, Oct 2026); a capable-then-cheap model handoff cut API cost 65.9% on average over 11 model pairs (Li, Oct 2026); a history-aware per-turn router saved nothing ($0.369 vs $0.365 per task) where the cheap setting alone was as good (Parashar, Oct 2026)
- **Performance:** improves, medium: low instead of max effort cut median response time per run by 20% (37.4 vs 47.0 s and 52.6 vs 65.9 s for two GPT-5.6 tiers) on routine office tasks (Xu, Aug 2026); at higher effort GPT-5.6-sol's SWE-Bench Pro trajectories grew from 14.7 to 28.4 calls (Sun, Oct 2026); step-by-step prompts made reasoning models' requests 20-80% (10-20 s) slower (Meincke, Jun 2025); escalating after a failed check adds a second full run on those tasks

## Evidence (summary)

- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Figure 1, internal benchmark: + Multi-LLM (GPT-5.4 + Opus 4.6) on top of parallel thinking 81.4% -> 91.6% (+10.2pp) while relative cost falls 2.13x -> 0.95x (baseline code agent = 1.00x). Bundled with GEPA-optimized prompts ("Multi-LLM…
- The Databricks AI Research Team, "Pushing the Frontier for Data Agents with Genie"… (2026-05-08): Figure 6, end-to-end accuracy of the Multi-LLM agent vs relative token cost (Sonnet 4.5 baseline = 1.0), approximate reads, baseline -> GEPA-optimized table-search sub-agent: Sonnet 4.5 ~73.1% @1.00 -> ~78.2% @~0.80; GPT-5.4 ~71.8% @~0.76…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): OpenCode "nine base prompts by model-id substring"; Codex per-generation prompts delivered as server-side catalog data; Hermes "15 guidance blocks gated by model family (tool-use enforcement blocks are sent to…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Aider "per-model metadata for 350+ models"; "This data-driven approach enables support for new models without code changes"; Pi "20 per-model compat quirk flags"; OpenCode 1,400-line per-vendor transform matrix.
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Aider picks among 13 edit formats via Coder.create() from model metadata; OpenCode "GPT-family models receive a port of Codex's apply_patch DSL and lose edit/write entirely"; OpenHands "model-specific tool presets (default, gemini, gpt5…
- …and 21 more sources in `library/entries/model-and-effort-per-call-site.yaml`.

## Caveats

Most effort sweeps on agentic tasks run each setting once (the eight-model sweep and the SlopCodeBench comparison), and a four-rollout check found lost lower-effort tasks at rates comparable to chance, so compare settings on repeated runs and tasks gained and lost, not one aggregate score. Effort and model do not move uniformly: higher effort raised strict passes for one of three coding models and its code had less flagged slop for another, escalating after a failed check needs a reliable external check and cost more than fixed top effort for four of eight models on Terminal-Bench, and none can cost more than low when the agent compensates with extra calls. Routing per query or turn often matched but did not beat the best single setting: a history-aware router stayed within a point of the expensive model at no cost saving, a cheap model or low effort alone matched or beat it in two of three pairs, self-chosen effort did no better than random allocation, and within-turn de-escalation trailed the fixed models on average on spreadsheets while capable-first handoffs in coding saved 65.9% on average but lost 5% or more relative accuracy in 10 of 22 settings (the authors' own method). Newer generations can regress on a narrow task (one fraud benchmark, point estimates only), and packing several items into one call cuts reasoning per item, so re-run the site's eval on every upgrade or batching change.

## Related

- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:link-large-schemas` (8.b.ii, Link large schemas by exploration: start broad, grow the linked set with probing queries, favor recall)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:tree-of-thought` (7.c.vii, Tree-of-Thought)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
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
