---
name: react-loop
description: "AOT optimization 7.d.iii (Tier 4, Restructuring): ReAct loop. Placeholder. Use when an agent shows: Thought before each action; observations used in the next thought; loops that ignore results; final messages that contradict the executed actions."
---

<!-- Generated from library/entries/react-loop.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# ReAct loop

> **Placeholder.** Generated from `library/entries/react-loop.yaml` (entry 7.d.iii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.d.iii |
| Earlier id | P04 (Prompting Strategies, from the master cookbook) |
| Tier (proposed) | 4 (Restructuring): it changes the control loop |
| Categories | Orchestration: Shaping the loop |
| Change | workflow / control_flow |

## What it is

Run the agent as a loop: the model reasons, calls a tool, reads the result and picks the next step, until it answers or hits a cap. It pays where the agent has to find its own path and recover from wrong steps: with the same lightweight models, each model's best loop harness resolved 51 to 63 of 100 SWE-bench tasks against 17 to 39 for a fixed repair pipeline (the loops used 4.3 to 87.8 million tokens per resolved task against 0.1 to 0.2 million), and on goal-only Google Maps tasks generic loops that kept the full history beat a fixed-step loop by 9 to 28 points. Where the lookups or steps are known in advance it buys little: a one-decision pipeline matched a tool loop on banking cases (90.5% against 88.8% correct), a fixed-step loop matched generic ones on stepwise tests at 2.6 to 10.7 times lower cost, and on web tasks with a trusted API, compiling a program before reading any page beat ReAct by 11.1 points and kept injected content from steering its steps, at 2.0 to 4.4 times the cost. On current models use native tool calling, carry the model's reasoning across tool calls, bound the whole feedback path, keep the per-step preamble small, and test per model and harness: with the model fixed, cost per task differed up to 3x across production harnesses, and for lightweight models success differed 28 to 44 points across harnesses.

## When it applies

- **In the code:** A loop that alternates model call and tool dispatch, feeds results back, and has a max-iteration guard; check that the guard bounds the whole feedback path (retries, handoffs), not just the outer loop.
- **In traces:** Thought before each action; observations used in the next thought; loops that ignore results; final messages that contradict the executed actions.
- **In eval results:** Success on tool-use tasks, scored from the executed actions; steps per task; tool error rate; success after a wrong tool call; tokens per resolved task.
- **Judge:** Do thoughts inform the next action or are they boilerplate.
- **Probes:** Tasks needing two to four dependent tool calls, each in a prescribed-step version and a goal-only version.

## How (outline)

1. Start from the cheapest design that could work and make the loop beat it. If every lookup can be run in advance, a pipeline that gathers them and asks for one decision may match it (90.5% against 88.8% correct on banking cases); if the steps are prescribed, a tight fixed-step loop may match a generic one (same success on stepwise GUI tests at 2.6 to 10.7 times lower cost). Use the generic loop where the agent must pick its next step from what it finds or recover from wrong steps; where it reads untrusted content and a trusted API covers the actions, also test compiling the plan before any content is read (6.c.i, 6.c.ii).
2. Use the provider's native tool calling, not a text Thought/Action/Observation template.
3. Loop: call the model, run every tool call it returns, append each result to the history (errors included, as observations), and call again; stop on a final answer or an explicit finish tool. Keep the accumulated history rather than rebuilding a compact prompt each step: on goal-only Google Maps tasks, runs with a wrong tool call still succeeded 78% to 83% of the time in generic loops that kept it, against 24% to 53% in a fixed-step loop that rebuilt its prompt from a step log.
4. Let the model reason before each action (interleaved or adaptive thinking; a think tool on models without it), and pass its reasoning back unchanged across tool calls.
5. Cap steps, cost and wall time on the whole feedback path, retries and handoffs included; count a cap hit as a failure (7.b.iii sizes the caps, 7.b.i catches stalls).
6. Keep the per-step preamble (system prompt and tool schemas) small: it and the growing history are re-sent every step, and with the model fixed, cost per task differed up to 3x across production harnesses, set by the preamble (16k tokens to under a thousand) times the step count.
7. Paired eval against the step 1 baseline, per model and harness and separately for prescribed and goal-only tasks, several runs per arm: success scored from the executed actions, not the final message (in one banking study, across five harnesses, 26.1% of violations came with a message denying the executed action), steps, cost and tokens per task, latency, cap-hit rate, and success after a wrong tool call.

## How to measure

- **experiment** (Tier 4): paired eval of the loop against the cheapest design that could work (one call, a precomputed pipeline, a fixed-step loop, or a compiled plan where untrusted content is read), per model and harness and separately for prescribed and goal-only tasks, several runs per arm: success scored from the executed actions, steps, cost and tokens per task, latency, cap-hit rate, and success after a wrong tool call; use the full task pool, since 45 tasks catch a 12.9-point gap only half the time
- **monitor**: steps per task, cap-hit rate, tool error rate, preamble tokens per call, cost and tokens per resolved task, and final messages that contradict the action log

## Expected impact

- **Quality:** improves, large: tasks that need several dependent calls or recovery from wrong steps: each model's best loop harness 51 to 63 of 100 SWE-bench tasks against 17 to 39 for a fixed repair pipeline (Zhao, Oct 2026); EHR-SQL 45.9 to 72.2 over a single shot, BIRD 78.5 to 79.1 (Lu, Aug 2026); goal-only Google Maps tasks +9 to +28 points for loops keeping the full history (Khoee, Oct 2026). No gain over a one-decision pipeline when lookups can be precomputed (88.8% against 90.5%, Huyut, Nov 2026); a compiled plan beat ReAct by 11.1 points on web tasks with a trusted API (Chow, Nov 2026)
- **Cost:** degrades, large: one model call per step, each re-sending the preamble and the growing history: 4.3 to 87.8 million tokens per resolved SWE-bench task in loop harnesses against 0.1 to 0.2 million for a fixed pipeline (Zhao, Oct 2026); generic loops 1.9 to 10.7 times the cost per task of a compact fixed-step loop (Khoee, Oct 2026); up to 3x across harnesses with the model fixed (Liu and Han, Oct 2026); but ReAct cost 2.0 to 4.4 times less than a compiled plan (Chow, Nov 2026)
- **Performance:** mixed, medium: serial calls, one per step: median 23 to 169 model calls per SWE-bench run in loop harnesses against 4 for a fixed pipeline (Zhao, Oct 2026); yet faster than heavier designs: 60 to 87 s per web task against 327 s for a compiled plan (Chow, Nov 2026), up to 8x faster than elaborate text-to-SQL pipelines (Lu, Aug 2026), and generic loops 3 to 57 s faster per task than a fixed-step loop that observed the screen every step (Khoee, Oct 2026)
- **Security:** degrades, medium: every tool result feeds the next action: injected page content steered a ReAct web agent's intermediate steps in a mean 16.2% (with the site's API) to 25.5% (browser only) of attacks, up to 52.8% for one model and site, though it reached the attacker's goal in only one of 12 model-site cells (5.6%); a compiled plan 0% (Chow, Nov 2026)
- **Governance:** mixed, medium: each action is a tool call in the trace, and the trace, not the transcript, is the record to audit: in one banking study, across five harnesses, 26.1% of rule violations came with a customer message denying the action just executed (Huyut, Nov 2026); with a vendor-maintained loop the team controls less of what the model receives and must keep its own run records (Khoee, Oct 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", https://arxiv.org/abs/2210.03629 (2022-10-06): ALFWorld success 71 (best of 6) against 45 for acting only and 37 for BUTLER; WebShop success 40.0 against 30.1 (acting only), 29.1 (IL) and 28.7 (IL+RL). HotpotQA EM 27.4 against 29.4 for chain-of-thought, 35.1 when ReAct falls back to…
- Verma, Bhambri, Kambhampati, "On the Brittle Foundations of ReAct Prompting for Agentic Large Language Models"… (2024-05-22): Reasoning given once before acting, instead of interleaved, beat base ReAct for GPT-3.5-Instruct (44.7 to 61.9) and GPT-4 (23.3 to 43.3), not for Claude-Opus (56.6 to 50). Performance is "minimally influenced by the 'interleaving reasoning…
- Yao, Shinn, Razavi, Narasimhan, "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"… (2024-06-17): "natively supported function calling consistently outperforms text-formatted agent methods with the state-of-the-art models. For text-formatted agent methods, adding reasoning traces still consistently helps." A "think" function added to…
- Trivedi et al., "AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents"… (2024-07-26): Task goal completion, normal / challenge test sets: GPT-4o ReAct 48.8 / 30.2 against plan-then-execute 44.6 / 19.7; GPT-4-Turbo ReAct 26.8 / 17.5 against 32.7 / 11.0. GPT-4o cost about $0.7 per example with ReAct and $1.33 with…
- …and 10 more sources in `library/entries/react-loop.yaml`.

## Caveats

The 2022 gains came from few-shot text prompting on PaLM-540B, and a 2024 study found the interleaved reasoning in that template mattered little next to the choice of examples. The newer comparisons are single studies with limits: the pipeline that matched the loop on banking cases ran four open models with reasoning off, the fixed pipeline the loops beat on SWE-bench ran without its own test validation and with one run per pairing, and the compiled plan that beat ReAct needs a trusted API per site, ran its compiler inside coding-agent harnesses at high or medium reasoning effort while ReAct called the models directly, and cost 2.0 to 4.4 times more. Harness and reasoning effects depend on the model: two of three production harnesses were within 5 points on 447 tasks while the third trailed by up to 9.2, six harnesses spread 28 to 44 points on lightweight models, and switching thinking off cost one harness 11 points and moved two others by less than the noise. Every tool result feeds the next action, so untrusted content can steer the loop: contain it (10.c.i) or commit to a plan before reading it (6.c.i, 6.c.ii), and compare harnesses only on large task pools.

## Related

- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)
- `aot-kit:prompt-chaining-with-gates` (7.a.ii, Prompt chaining with gate checks)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)

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
