---
name: rewrite-tool-surface
description: "AOT optimization 2.a.ii (Tier 1, Hygiene): Rewrite the tool surface: names, schemas, descriptions. Placeholder. Use when an agent shows: misrouted cases per tool (false positives and false negatives); failure rows labeled incorrect-tool-selection, malformed-arguments or suboptimal-arguments; per-tool error rate and retries (Datadog tracks these per tool and server); tool calls and cost per task; a higher-privilege tool called before the standard ones were tried."
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

Rewrite each tool's name, parameters and description for the model, starting from the calls it gets wrong. Give each tool a distinct name, a strict schema whose parameter names say what the request supplies, and a description with fixed sections (what it is for and when to use it versus sibling tools, defaults and limits, error modes and what to do next, side effects), plus an example for complex parameters: in one study parameter names and structure swayed five models' choice between equivalent tools far more than tool names did, examples raised complex-parameter accuracy from 72% to 90% in Anthropic's testing, and one LLM rewrite fed the misrouted cases matched hand-tuning. Task-level gains are often small: trace-driven description edits cut tool calls 24-33% and cost 18-38% on three production servers but raised the pass rate on only one, description-only rewrites did not significantly lift a customer-service benchmark (one cut a domain from 29.5% to 25.6%), and with informative names, stripping descriptions moved success at most 4 points on nine open models, so slim the result and keep only what a paired test per model confirms. Where a failure needs a lookup or a result the tool does not provide, change the tool itself; where two tools genuinely overlap, rewording cannot separate them: consolidate instead (2.a.i).

## When it applies

- **In the code:** descriptions that do not state the tool's purpose (56% of audited MCP tools) or when to use it; duplicate or overlapping names; schemas without types, enums, required fields or parameter descriptions; parameter names that signal a different input from what requests supply (an id where users give an email address) and parameters grouped into one object; no statement of side effects or privilege; no example for complex parameters
- **In traces:** misrouted cases per tool (false positives and false negatives); failure rows labeled incorrect-tool-selection, malformed-arguments or suboptimal-arguments; per-tool error rate and retries (Datadog tracks these per tool and server); tool calls and cost per task; a higher-privilege tool called before the standard ones were tried
- **In eval results:** failures attributed to tool selection or arguments, separated from failures where the tool had returned what was needed; step count, tool calls and cost per task after a description change; wrong-tool rate under varied tool order
- **Probes:** Requests that should route to each tool, phrased in users' terms, boundary cases between similar tools, and inputs in the forms users give (an email address, an owner/repo path).

## How (outline)

1. Start from the baseline: from traces or the eval set, collect per tool the misrouted cases (called when it should not have been, not called when it should), malformed or wrong arguments, tool errors and retries, and calls, tokens and cost per task. Label which failures a description could fix: in one study most failures on a customer-service domain were reasoning errors made after the tools had returned what was needed, and failures that needed a lookup or a result the tools did not provide were fixed by changing the tool, which a description cannot do; tool pairs whose scopes genuinely overlap go to 2.a.i.
2. Audit names, schemas and descriptions: missing purpose (56% of audited MCP tools) or when-to-use against sibling tools, repeated names (73% in an audit of 10,831 MCP servers), parameters without a type, enum, required flag or description, parameters grouped into one object, and parameter names that signal a different input from what requests supply (renaming a send-email tool's 'to' to 'recipient_id' cut its selection to 1-10% across five models, while 'receiver' kept it at 35-51%).
3. Fix the schema: separate top-level parameters named for what the request supplies (models chose them over one grouped object in 93-100% of trials), a description for each parameter, types, enums and required fields, and the provider's strict or constrained tool calling where offered (in one study forcing a schema-valid first call added nothing on the native schema and 29 points on a merged one). On tools other agents already call, keep names and parameter contracts and change only descriptions, as one production study did.
4. Write each description in fixed sections: what it is for and when to use it versus siblings, defaults and limits, error modes and what to do next, and side effects with a privilege level (read, write or administer), in the distinctive terms tool search matches on; add a usage example for complex parameters (72% to 90% accuracy in Anthropic's testing). In one benchmark a privilege class and cost appended to each description cut premature use of a higher-privilege tool by 3.3 to 19.3 points on seven of eight models, mostly by delaying it; with a least-privilege instruction in the prompt as well (2.b.ii) safe completion rose on seven of eight (18.8% to 51.1% at best), and neither replaces enforcement (10.a.i, 10.b.i).
5. Rewrite once from the misrouted cases with an LLM, or with a coding agent that reads the traces and the tool code: one rewrite matched hand-tuning (79.2% against 79.4% F1), and on a customer-service benchmark only a coding agent that read past traces and could also change tool code raised reward significantly (Telecom 29.5% to 36.8%), while description-only edits, a single-shot rewrite of the tool file and the DRAFT, ToolObserver and GEPA optimizers did not, and DRAFT's rewrite cut it to 25.6%.
6. Slim the result: richer descriptions add steps and tokens (augmented MCP descriptions added 67.46% more execution steps; description-only toolsets cost 1.9 to 2.9 times as much per run in one benchmark), so drop sections the paired eval shows the model does not need; with informative names, stripping descriptions moved success at most 4 points on nine open models but cost 0.23 on BFCL, whose tools rely on them.
7. Measure: replay the hand-labeled set, then run a paired eval per model, old against new, on at least about 100 target tasks (about 100 queries ranked schema variants nearly as the full set did, Spearman 0.81, against 0.52-0.57 for query-free probes), several trials per task with a paired test (one study used 30 per held-out task, and an unchanged toolset rerun scored 0.92 points lower), and tool order varied (with only names differing, four of five models picked the first-listed tool in 79-96% of trials); report wrong-tool rate, argument and tool errors, pass rate overall and on previously passing tasks, and calls, tokens and cost per task, and re-run when the model changes. Pairs that stay confused go to 2.a.i.

## How to measure

- **verify-fix** (Tier 1): replay the hand-labeled misrouted cases against the rewritten names, schemas and descriptions
- **experiment** (Tier 3): paired eval per model, old against new surface, on at least about 100 target tasks with several trials per task and a paired test, a rerun of the unchanged surface as a noise check, and tool order varied: wrong-tool rate, argument and tool errors, pass rate overall and on previously passing tasks, and calls, tokens and cost per task
- **monitor**: per tool and server in production traces: misrouted and unused calls, argument and validation errors, tool errors and retries, and calls and cost per task; re-run the paired eval when the model or toolset changes

## Expected impact

- **Quality:** improves, medium: examples raised complex-parameter accuracy from 72% to 90% (Anthropic, Nov 2025); augmented MCP descriptions +5.85 pp median success, with 16.67% of cases worse (Hasan, Feb 2026); a compliant description was picked 72% vs 20% among equivalents (Wang, Feb 2026), and a parameter renamed 'recipient_id' cut a tool's selection to 1-10% (Li, Oct 2026); one rewrite matched hand-tuning, 79.2% vs 79.4% F1 (Zhou, Jun 2026); description edits raised held-out pass@1 from 49.3% to 51.4% on TerminalBench-2 and the pass rate on one of three production servers (54.5% to 72.7%, 11 tasks), while description-only rewrites left tau2-bench reward unchanged and DRAFT's cut Telecom from 29.5% to 25.6% (Ravichandran, Oct 2026); with informative names, stripping descriptions moved success at most 4 points on nine open models (Liu, Sep 2026)
- **Cost:** mixed, medium: augmented descriptions added 67.46% more execution steps, and slim variants keep most of the gain (Hasan, Feb 2026); trace-driven description edits cut tool calls 24-33%, tool errors 33-49% and session cost 18-38% on three production MCP servers for a one-time $1.34-$7.68 each, while on tau2-bench description-only toolsets cost 1.9 to 2.9 times as much per run and a rerun of an unchanged toolset cost 13% more (Ravichandran, Oct 2026)
- **Performance:** mixed, small: a tool-testing agent's description rewrite cut task completion time 40% (Anthropic, Jun 2025); augmented descriptions added 67.46% more execution steps (Hasan, Feb 2026); description edits cut tool calls 24-33% on three production servers (Ravichandran, Oct 2026)
- **Security:** improves, small: a privilege class and cost appended to each tool description cut premature use of a higher-privilege tool by 3.3 to 19.3 points on seven of eight models (Claude Sonnet 4.6 unchanged at 1.5%), mostly by delaying it; with a least-privilege instruction too, safe completion rose on seven of eight (18.8% to 51.1% at best), and a neutral note of the same format raised escalation on two models (Parkinson, Oct 2026); nothing is enforced, so it complements enforcement (10.a.i, 10.b.i)

## Evidence (summary)

- repo figure_01 (2026-02): 7 to 18 of 20 runs per benchmark.
- paper Table 11 (2026-02): The Tool-Centric template is built around docstring guidance and parameter design.
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "an agent searching the web for context that only exists in Slack is doomed from the start" ... "Bad tool descriptions can send agents down completely wrong paths, so each tool needs a distinct purpose and a clear description."
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "This process for improving tool ergonomics resulted in a 40% decrease in task completion time for future agents using the new description, because they were able to avoid most mistakes." (no benchmark, n or model beyond "Claude 4 models")
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Every tool description in the study uses this template. Not ablated.
- …and 17 more sources in `library/entries/rewrite-tool-surface.yaml`.

## Caveats

Most of the controlled evidence is narrow: the parameter-name and privilege results come from single-turn selection without execution (five tasks, thinking off or minimal) and from 544 simulated scenarios with nothing enforced, and the production result is three servers with 5 to 11 held-out tasks, one run each, judged by an LLM, where content scores fell on two. On a curated customer-service benchmark, description-only rewrites (the optimizer's own, DRAFT, ToolObserver and GEPA) did not significantly raise reward, the one significant gain needed changes to tool code and did not hold when averaged over five agent models, and a rerun of an unchanged toolset scored 0.92 points lower and cost 13% more, so small differences are noise. Effects are model-specific: the same equivalent schema matched native success for one model and collapsed another, names and descriptions were largely redundant when names were informative, and a privilege note mostly delayed risky calls while a neutral note of the same format raised them on two models, so every added line needs its own paired test. Several sources are unmeasured practice (Arcade, Block, Datadog, Fan et al., VeRO's tool-centric template), and the example gain (72% to 90%) is Anthropic's internal testing with no benchmark or n given.

## Related

- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
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
