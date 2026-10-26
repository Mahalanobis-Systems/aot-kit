---
name: react-loop
description: "AOT optimization 7.d.iii (Tier 4, Restructuring): ReAct loop. Placeholder. Use when an agent shows: Thought before each action; observations used in the next thought; loops that ignore results."
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

Run the agent as a loop: the model reasons, calls a tool, reads the result and picks the next step, until it answers or hits a cap. The loop is the common default for tasks that need several dependent tool calls; the 2022 text template (Thought/Action/Observation lines in a few-shot prompt) is not. On current models, use native tool calling, carry the model's reasoning across tool calls, bound the whole feedback path, and keep the per-step preamble small: with the model fixed, the harness around the loop moved cost per task by up to 3x and pass rate by less than the noise.

## When it applies

- **In the code:** A loop that alternates model call and tool dispatch, feeds results back, and has a max-iteration guard; check that the guard bounds the whole feedback path (retries, handoffs), not just the outer loop.
- **In traces:** Thought before each action; observations used in the next thought; loops that ignore results.
- **In eval results:** Success on tool-use tasks; steps per task; tool error rate.
- **Judge:** Do thoughts inform the next action or are they boilerplate.
- **Probes:** Tasks needing two to four dependent tool calls.

## How (outline)

1. Use the provider's native tool calling, not a text Thought/Action/Observation template.
2. Loop: call the model, run every tool call it returns, append each result to the history (errors included, as observations), and call again; stop on a final answer or an explicit finish tool.
3. Let the model reason before each action (interleaved or adaptive thinking; a think tool on models without it), and pass its reasoning back unchanged across tool calls.
4. Cap steps, cost and wall time on the whole feedback path, retries and handoffs included; count a cap hit as a failure (7.b.iii sizes the caps, 7.b.i catches stalls).
5. Keep the per-step preamble (system prompt and tool schemas) small; it is re-sent every step.
6. Paired eval against the current design (one call or a fixed workflow), per model: success, steps, cost per task, cap-hit rate.

## How to measure

- **experiment** (Tier 4): paired eval of the loop against the current design, per model: success, steps, cost per task, cap-hit rate; use the full task pool, since 45 tasks catch a 12.9-point gap only half the time
- **monitor**: steps per task, cap-hit rate, tool error rate, cost per task

## Expected impact

- **Quality:** improves, large: tasks that need several dependent tool calls: text-to-SQL 45.9 to 72.2 on EHR-SQL over a single shot, but 78.5 to 79.1 on BIRD (Lu, Aug 2026); ALFWorld 71 against 45 for acting without reasoning (Yao, 2022)
- **Cost:** degrades, medium: one model call per step, each re-sending the preamble and history; with the model fixed, cost per task differed by up to 3x across harnesses (Liu and Han, Oct 2026)
- **Performance:** degrades, medium: serial round trips, one per step
- **Security:** mixed, medium (unmeasured): Autonomous tool actions need scoping.
- **Governance:** mixed, medium (unmeasured): Every action must be logged to be auditable.
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", https://arxiv.org/abs/2210.03629 (2022-10-06): ALFWorld success 71 (best of 6) against 45 for acting only and 37 for BUTLER; WebShop success 40.0 against 30.1 (acting only), 29.1 (IL) and 28.7 (IL+RL). HotpotQA EM 27.4 against 29.4 for chain-of-thought, 35.1 when ReAct falls back to…
- Verma, Bhambri, Kambhampati, "On the Brittle Foundations of ReAct Prompting for Agentic Large Language Models"… (2024-05-22): Reasoning given once before acting, instead of interleaved, beat base ReAct for GPT-3.5-Instruct (44.7 to 61.9) and GPT-4 (23.3 to 43.3), not for Claude-Opus (56.6 to 50). Performance is "minimally influenced by the 'interleaving reasoning…
- Yao, Shinn, Razavi, Narasimhan, "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"… (2024-06-17): "natively supported function calling consistently outperforms text-formatted agent methods with the state-of-the-art models. For text-formatted agent methods, adding reasoning traces still consistently helps." A "think" function added to…
- Trivedi et al., "AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents"… (2024-07-26): Task goal completion, normal / challenge test sets: GPT-4o ReAct 48.8 / 30.2 against plan-then-execute 44.6 / 19.7; GPT-4-Turbo ReAct 26.8 / 17.5 against 32.7 / 11.0. GPT-4o cost about $0.7 per example with ReAct and $1.33 with…
- …and 6 more sources in `library/entries/react-loop.yaml`.

## Caveats

The 2022 gains came from few-shot text prompting on PaLM-540B, and ReAct alone trailed chain-of-thought on HotpotQA; a 2024 study found the interleaved reasoning in that template mattered little next to the choice of examples. Whether reasoning between calls helps depends on the model and harness: switching thinking off cost one harness 11 points and moved two others by less than the noise. Every tool result feeds the next action, so untrusted content can steer the loop: contain it (10.c.i) or commit to a plan before reading it (6.c.ii). Harness comparisons need large task pools.

## Related

- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)
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
