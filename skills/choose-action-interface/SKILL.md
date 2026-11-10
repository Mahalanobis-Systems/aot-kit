---
name: choose-action-interface
description: "AOT optimization 2.a.iii (Tier 3, Tuning): Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task. Placeholder. Use when an agent shows: bash-only runs emitting tools that do not exist; typed-tool runs re-patching the same file; malformed shell commands and broken edits per run (a weak coding model averaged 3.11 environment errors per bash-only trajectory against 0.35-0.54 for stronger ones); code errors in routine operations (reading a file, searching); import-error or command-not-found spans at the start of runs; calculations done in the model's own text; independent commands serialized; long chains of single tool calls that pass large intermediate results through the model; calls outside the assigned interface."
---

<!-- Generated from library/entries/choose-action-interface.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task

> **Placeholder.** Generated from `library/entries/choose-action-interface.yaml` (entry 2.a.iii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.a.iii |
| Earlier id | T61 |
| Tier | 3 (Tuning): it changes the agent's tools within the existing design |
| Categories | Tools: Refactoring; Models: Benchmarking workloads |
| Change | tool / api (restructure) |
| Also covers | CodeAct |

## What it is

Choose the agent's action interface per model and task: typed tools, a shell, or code that calls tools. Weaker models do better with typed tools (read, write, edit, grep, a narrow calculator): a general code interpreter made a weak agent write boilerplate and fail until it was replaced with typed functions, and structured data gets a typed query tool whatever the model (SQL scored 100% against 52.7% for bash at a seventh of the tokens; SQL plus bash also reached 100%). Strong models on shell-heavy or general office work get bash (on enterprise digital-worker tasks bash-only beat typed tools by 21.8-24.5 points with fewer tokens, and typed tools on top of bash added nothing), and work that chains many calls or processes bulk data gets code that calls the tools, because intermediate results never pass through the model: it matched or beat JSON calling for 11 of 14 models on BFCL v4, beat one-at-a-time calls on a many-call benchmark for all ten models tested and for small open models from 4B parameters up, but not at 2B or below, and a narrow calculator did as well as full code execution on math. The best choice is specific to the model and task (two frontier coding agents' pass rates moved under 3 points across interfaces while cost moved by up to 24.6%, and the same actions offered as typed calls or as command text moved small models' scores by up to 36.6 points in either direction), so start minimal, add tools per observed failure, provision packages, interpreter state and concurrent commands for code and shell, sandbox it (10.a.i), and decide by a paired eval per model.

## When it applies

- **In the code:** the interface in use (typed tools, code interpreter, bash), the model it serves, and whether the environment has the packages and fixtures the tasks need
- **In traces:** bash-only runs emitting tools that do not exist; typed-tool runs re-patching the same file; malformed shell commands and broken edits per run (a weak coding model averaged 3.11 environment errors per bash-only trajectory against 0.35-0.54 for stronger ones); code errors in routine operations (reading a file, searching); import-error or command-not-found spans at the start of runs; calculations done in the model's own text; independent commands serialized; long chains of single tool calls that pass large intermediate results through the model; calls outside the assigned interface
- **In eval results:** success, consistency over repeated runs (pass^k), cost and steps by model under each interface

## How (outline)

1. Start from the baseline: the current interface and model. Log per task success, consistency over repeated runs (pass^k), cost, steps, wall-clock time, errors by kind (tools that do not exist, malformed commands, broken edits, import or command-not-found errors) and which tools were actually called. Enforce the interface in configuration where you can and audit the calls: in one study a restriction set only in the prompt still let 7 and 4 explicit edit-tool calls through in 110 runs, and could not rule out the same edits made through bash.
2. Probe each model on 20 or more representative cases under each candidate interface (typed tools only, bash only, typed tools plus bash, code that calls the tools), with the same prompt and budget and several repeats. Do not assume the direction: the same actions offered as typed calls or as command text moved small models' scores by up to 36.6 points, and typed calls won in only 8 of 18 model-environment pairs. Signs that a model needs typed tools: frequent environment errors under bash (3.11 per trajectory for a weak coding model against 0.35-0.54 for stronger ones; typed tools cut its malformed commands from 0.96 to 0.01 per trajectory), bash-only runs that end after emitting tools that do not exist (66% of one weak model's runs), or a model of 2B parameters or fewer, where code that calls tools scored slightly below typed calls.
3. Pick the interface per task type. Structured data: a typed query tool (SQL 100% against 52.7% for bash), with bash beside it if the agent should check its own answers. Shell-heavy coding or office work with a strong model: bash (typed tools on top of bash gave no gain on enterprise tasks and raised input tokens 20% for two strong coding models). Many dependent calls, loops, filters, joins or bulk data: code that calls the tools as typed functions and returns only the result (GPT-5.4 went from 18.6% to 71.5% on one many-call benchmark; 37% fewer tokens in Anthropic's test). Repository edits: measure before dropping native edit tools (code-only cost 14.4% more with Claude Code, not significant, with 39.9% more output tokens, but 19.9% less with Codex). Where success ties, as it did for two frontier coding agents (pass rates within 3 points across default tools, bash only and code only), choose on cost (code-only cost 24.6% less on computation tasks with Claude Code).
4. Start minimal (bash, read, write, edit, grep, or one code-execution tool) and add a tool only when a trace shows a failure it would have prevented.
5. Provision code and shell: install the packages and fixtures the tasks expect; keep interpreter state between code calls (persistent cells raised pass rate in all eight matched comparisons by 0.6-5.7 points, several within run-to-run variation, and cut follow-up API calls from about 27-30 to 4-8); let the code load tool schemas on demand rather than all up front (most of the token savings in that study); allow concurrent commands; and sandbox it (10.a.i).
6. Measure: a paired eval per model and task type, interface A against B with the same model, prompt and budget and several repeats, comparing success and pass^k, cost, steps, wall-clock time and the share of calls made through the assigned interface; re-run it when the model changes.

## How to measure

- **experiment** (Tier 3): paired eval per model and task type, interface A against B (typed tools, bash, typed tools plus bash, code that calls the tools) with the same model, prompt and budget and several repeats: success and pass^k, cost, steps, wall-clock time, environment errors per run and the share of calls made through the assigned interface; where success ties, keep the cheaper interface
- **monitor**: per run in production: interface and model, success, cost, steps, wall-clock time, errors by kind (nonexistent tools, malformed commands, broken edits, import or command-not-found errors), calls outside the assigned interface and sandbox violations; re-run the paired eval when the model changes

## Expected impact

- **Quality:** mixed, large: typed tools +15.0 points on SWE tasks for a weak model and bash-only +3.6 for a strong one (Fan, Sep 2026); typed tools on bash raised a weak model's pass^9 from 0.020 to 0.094 (Xu, Aug 2026); typed functions in place of an interpreter took GAIA from 0.07 to 0.24 (VeRO, Feb 2026); bash beat typed tools by 21.8-24.5 points on enterprise tasks (Mak, Sep 2026); code that calls tools beat one-at-a-time calls for all ten models on a many-call benchmark (GPT-5.4 18.6% to 71.5%) but not at 2B parameters or fewer (Mao, Nov 2026); the same actions as typed calls or command text differed by up to 36.6 points in either direction (Shi, Oct 2026); two frontier coding agents moved under 3 points across interfaces (Yang, Jul 2026)
- **Cost:** improves, large: bash-only cut cost 53% for a bash-capable model (Fan, Sep 2026) and used 19-72% fewer tokens than typed tools on enterprise tasks (Mak, Sep 2026); calling tools from code cut tokens 37% (Wu, Nov 2025), and code-only cut cost 24.6% on computation tasks with Claude and 19.9% on repository edits with Codex (Yang, Jul 2026); the wrong choice costs more: bash used 7x the tokens of a SQL tool on structured data (Goyal, Jan 2026), typed tools on top of bash raised input tokens 20% for two strong models (Xu, Aug 2026), and code-only cost 14.4% more (not significant) on repository edits with Claude (Yang, Jul 2026)
- **Performance:** mixed, medium: calling tools from code finished chained calls faster for 13 of 14 models (0.32 to 0.96 of the JSON time; GPT-5 2.8x slower) (Patel, Aug 2026), Vercel's bash-and-SQL agent went from 274.8 s to 77.4 s (Qu, Dec 2025) and code actions cut mean steps from 77 to 46, 65 to 47 and 80 to 55 (Xu, Aug 2026); but code that calls tools against one-at-a-time calls cut wall time per task for two of four models (Gemini 3.1 Pro 117.8 to 44.6 s) and raised it for two (GPT-5.4 mini 14.0 to 19.1 s) (Mao, Nov 2026), and bash against typed tools was faster in one of four model-benchmark pairs (5.1 to 3.0 minutes) and slower in three (Mak, Sep 2026)
- **Security:** degrades, large (unmeasured): a shell or code interpreter lets the agent run anything its sandbox allows, where typed tools and code limited to a typed catalog expose only listed operations; no source here measures attack rates by interface, so how much it degrades depends on the sandbox and network policy (10.a.i)
- **Governance:** degrades, medium (unmeasured): named typed tools are easier to allowlist and audit than free shell or code; one study recommends code limited to a typed catalog where policy requires a fixed set of actions (Mak, Sep 2026), and a restriction set only in the prompt still let a few edit-tool calls through (7 and 4 in 110 runs) (Yang, Jul 2026)

## Evidence (summary)

- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): T4/128k, planning on. Nemotron-3 30B: typed tools +15.0 pts SWE (25.2 vs 10.2) and +10.1 TB. 66% of its bash-only TB runs end after emitting tools that don't exist (trajectory 71->15 turns). 120B: tools +1.6 SWE / +4.5 TB and shorter runs…
- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Claude Opus 4.5, 5 representative queries, old vs new: avg time 274.8s -> 77.4s ("3.5x faster"); success 4/5 -> 5/5; avg tokens ~102k -> ~61k ("37% fewer"); avg steps ~12 -> ~7 ("42% fewer"). Worst case: old "724 seconds, 100 steps, and…
- Andrew Qu (Vercel), "We removed 80% of our agent's tools", https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools (2025-12-22): Part of the bundled v1 -> v2 change (5 queries, Opus 4.5, numbers above). "We were constraining reasoning because we didn't trust the model to reason. With Opus 4.5, that constraint became a liability." Both code samples show instructions…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): "Mini-SWE-Agent's single-tool design reports 74%+ on SWE-Bench with essentially no tool infrastructure (self-reported)"; the paper says it is not comparable head-to-head with Codex's 69.1% (different models, runs, sandboxing).
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Rec 17 quoting [18]: "a common error we've observed is tools that merely wrap existing software functionality or API endpoints." Consolidate instead.
- …and 22 more sources in `library/entries/choose-action-interface.yaml`.

## Caveats

Much of the evidence is bundled, small or self-reported: the harness study changed tools together with prompts, file-state tracking and diagnostics; Vercel's 80%-fewer-tools result also removed prompts and context and covers 5 queries; mini-SWE-agent's 74% is self-reported, Cloudflare's 1,000-token figure is calculated rather than tested and Block's 30% is one author's test; and the largest code-execution gains (GPT-5.4 18.6% to 71.5%) come from the authors' own many-call benchmark, with gains of 0.7 to 11.1 points on independent MCP benchmarks. The best interface depends on the model and the task, so a result for one model does not transfer: the same actions as typed calls or as command text differed by up to 36.6 points in either direction across six models and three environments, code that calls tools scored slightly below typed calls at 2B parameters or fewer, and two frontier coding agents' pass rates moved under 3 points across interfaces while cost moved by up to 24.6%. VeRO flags the narrow calculator tool on MATH as intuitively helpful but its test gain (0.86 to 0.88) as within noise, with a MATH baseline of 0.87 near the target model's ceiling.

## Related

- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)
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
