---
name: code-then-execute
description: "AOT optimization 6.c.i (Tier 4, Restructuring): Code-then-execute (CaMeL). Placeholder. Use when an agent shows: Policy denials and user confirmations per task; privileged-model retries per task; no executed call whose arguments carry untrusted labels unless a policy allows it; no tool-derived text in another agent's instruction."
---

<!-- Generated from library/entries/code-then-execute.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Code-then-execute (CaMeL)

> **Placeholder.** Generated from `library/entries/code-then-execute.yaml` (entry 6.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.c.i |
| Earlier id | P49 (Control Flow, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it restructures the control loop for trust separation |
| Categories | Topologies: Separating privileges |
| Change | tool / code_execution |

## What it is

Have a privileged model turn the trusted request into a small program before any untrusted data is read, then run it in an interpreter that labels every value with where it came from and checks a per-tool policy before each call, so injected text can neither add actions nor send private data to the wrong place. Attack success stayed at or below 1.8% across five models even under an adaptive attack (up to 58.6% undefended), but it was the costliest defense in utility: 26.3 to 52.6% of clean tasks solved against 63.2 to 89.5% undefended in one independent test, a gap that narrowed to 5.4 to 7.2 points only with frontier models (GPT-5.5, o3). Use it where the request alone fixes the actions and a hard block on exfiltration is worth lost tasks and about 3.5x the latency; the guarantee holds only where label tracking reaches, and retries, error messages, untaken branches and agent-to-agent messages have all been shown to leak.

## When it applies

- **In the code:** The privileged model sees only the request, trusted context and tool descriptions with return schemas, and writes the task as a program; a custom interpreter labels every value with its sources and readers and propagates labels through operations, string formatting and control flow, including untaken branches; untrusted content is parsed only by a model with no tools and a typed output; each side-effecting tool has a policy on argument sources and readers; repair retries and error messages stay inside the checked boundary.
- **In traces:** Policy denials and user confirmations per task; privileged-model retries per task; no executed call whose arguments carry untrusted labels unless a policy allows it; no tool-derived text in another agent's instruction.
- **In eval results:** Static and adaptive injection suites (AgentDojo with per-tool policies, plus data-dependent tasks); benign utility and utility under attack; tokens and latency per task; share of tasks with a policy denial; excess privilege left open.
- **Probes:** Injected data that tries to add a call, set a write argument, leak a private value through a branch or a retry, or cross an agent boundary inside instruction text.

## How (outline)

1. Start from the baseline: your current tool loop (7.d.iii) and a cheaper check on where write arguments came from (argument provenance or per-task policies), same model, on an injection suite with static and adaptive attacks; frontier models already resist template attacks undefended (0.3% for Claude-Haiku-4.5, 0.0% for GPT-5.5), so static numbers alone overstate the gain. Sort tasks by whether the request alone fixes the actions: a program written before reading data cannot do "the actions specified in the email" (no model solved it), so contain those inputs (10.c.i) and gate the action (10.b.i) instead.
2. Give the privileged model only the request, trusted context and tool descriptions with full return schemas, and have it write the whole task as a program in a restricted Python subset: undocumented tool outputs caused 13 of Claude 3.5 Sonnet's 15 Travel failures, and a follow-up had to add return schemas to every tool to reach usable utility. Parse untrusted content only through a quarantined model call with no tools and a typed output schema; it can be a cheaper model (Claude 3.5 Haiku under Claude 4 Sonnet cost about 1% utility for about 12% lower cost per median task) (1.b.i).
3. Run the program in a custom interpreter that attaches sources and allowed readers to every value and propagates them through every operation, string formatting and control flow, including assignments on branches not taken: an independent audit found CaMeL's interpreter dropped labels in both places. Keep repair retries inside the checked boundary: never return raw error text derived from tool output to the privileged model (an error message put an attacker's reserve_hotel call into the rewritten program in one test), and cap retries, since each blocked-or-allowed retry leaks a bit.
4. Write a policy for each side-effecting tool on where every argument may come from and who may read what is sent (for example, send_money's recipient and amount only from the user). Without policies, a recipient the quarantined model parsed from a landlord's notice was used for a scheduled payment. Route denials to user confirmation and budget for them: CaMeL's released policies refused 41.5% of calls a task was entitled to make and let every required call through on only 37 of 92 tasks, and turning policies on cut banking utility from 66.7% to 37.5% (GPT-5.2).
5. If agents call agents, pass tool-derived values to the child agent through a separate data channel, never inside its instruction text: with CaMeL in every agent, 0.2% of attacks still got through (0.5% for GPT-4.1, from 36.1%), all by that route, and the separate channel took it to 0.0%.
6. Deploy it on strong models and on tasks the request fully specifies: clean utility was 26.3 to 52.6% against 63.2 to 89.5% undefended across five smaller models, but 77.3% against 84.5% for o3 and 82.1% against 87.5% for GPT-5.5 (no policies). If that loss is too high, a cheaper argument-provenance or policy defense kept 59.6 to 63.2% clean utility at 4.4 to 7.7% adaptive attack success on GPT-4o-mini, where CaMeL kept 26.3% at 0.0%.
7. Measure paired against the baseline, same model and suite: benign utility, utility under attack, attack success under static and adaptive attacks, tokens and latency per task (17.30 s against 4.98 s and 5,083 against 8,020 tokens with GPT-4o in one test; 2.73x the input and 2.82x the output tokens for the median task with Claude 3.5 Sonnet in the authors' test), the share of tasks with a policy denial and the excess privilege left open; in production, monitor denials, retries and tasks the program could not express.

## How to measure

- **experiment** (Tier 4): paired runs, CaMeL-style program and interpreter against the current tool loop and a cheaper argument-provenance or policy check, same model, on AgentDojo with per-tool policies plus data-dependent tasks (AgentDyn-style): benign utility, utility under attack, attack success under the static attack and an adaptive black-box optimizer (AutoDojo-style), tokens and latency per task, the share of tasks with a policy denial, and excess privilege left open (Ajar-style candidate calls); add probes for error-message injection, secret-dependent assignments on untaken branches, string interpolation of untrusted values and, in multi-agent systems, tool output written into a child agent's instructions
- **monitor**: policy denials and user confirmations per task, privileged-model retries per task and error messages that contain tool-derived text, tasks abandoned because the program could not express them, quarantined-model not-enough-information errors, and values that cross agent boundaries inside instruction text

## Expected impact

- **Quality:** degrades, large: benign utility 77.3% against 84.5% for o3 but 41.2% against 73.2% for Gemini 2.5 Pro (Debenedetti, Mar 2025); 59.79% against 80.41% with GPT-4o (Ji, Nov 2025); 26.3 to 52.6% against 63.2 to 89.5% across five smaller models, the largest cost of ten defenses on four (Ma, Jun 2026); 64.9% against 86.6% with Sonnet-5, 73.2% against 77.3% with Haiku-4.5 (Sharma, Sep 2026); policies on 37.5% against 66.7% off (GPT-5.2, banking) (Garby, Feb 2026); without policies 82.1% against 87.5% for GPT-5.5 and 20.5% against 64.3% for Gemini 2.5 Flash-Lite (Peters-Gill, Oct 2026). Tasks whose actions come from the data cannot be expressed.
- **Cost:** mixed, medium: median task 2.73x the input and 2.82x the output tokens, mean 7.24x and 6.23x, against native tool calling (Claude 3.5 Sonnet); a cheaper quarantined model cut cost about 12% for about 1% utility (Debenedetti, Mar 2025); 5,083 against 8,020 tokens per task with GPT-4o (Ji, Nov 2025)
- **Performance:** degrades, large: 17.30 s against 4.98 s per task with GPT-4o, the slowest of the GPT-4o defenses tested (Ji, Nov 2025); the authors attribute the overhead to model calls and code-repair retries, not the interpreter (Debenedetti, Mar 2025)
- **Security:** improves, large: 0 of 949 attacks succeeded with policies for o3 and Gemini 2.5 Pro, against 11 and 163 undefended (Debenedetti, Mar 2025); at most 1.8% under static and adaptive attacks across five models, against up to 58.6% undefended (Ma, Jun 2026); 1.21% against 15.62% on AgentDojo and 7.15% against 31.04% on ASB, and an attack reusing the task's tools doubled it (0.95% to 1.90%) (Ji, Nov 2025). Leaks where tracking stops: error messages (Ji, Nov 2025), untaken branches and the retry loop (Garby, Feb 2026), tool output written into another agent's instructions (0.2%, 0.0% with a separate data channel) (Peters-Gill, Oct 2026); 16 of 609 attack sinks left open against 1 for an argument-exact oracle (Sharma, Sep 2026)
- **Governance:** improves, medium: the program, per-value labels and per-tool policies are a reviewable record of what may flow where; it left less excess privilege open than a tool allowlist (0.0895 against 0.3551) but about 45 times an argument-exact oracle (0.0020), partly by refusing entitled calls (Sharma, Sep 2026); its guarantee is not formally verified: the label rules live in its Python interpreter, which missed an implicit flow (Garby, Feb 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Debenedetti et al., "Defeating Prompt Injections by Design", https://arxiv.org/abs/2503.18813 (2025-03-24): "solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo": o3 (high effort) 77.3% against 84.5% with native tool calling; other models lost more (Claude 4 Sonnet 74.2% against 86.6%, Gemini 2.5…
- Peters-Gill, Semler, Bartsch, Shumailov, Schroeder de Witt, "Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt… (2026-10-05): MultiAgentDojo, n=949 per model, attack success with no CaMeL / CaMeL in every agent / multi-CaMeL: average 12.9% / 0.2% / 0.0%; GPT-4.1 36.1% / 0.5% / 0.0%; Gemini 2.5 Pro 24.6% / 0.4% / 0.0%; GPT-5.5 0.0% in all three. Every attack that…
- Sharma, Jiang, Chen, Lin, "Ajar: Measuring Open Privilege in Agent Defenses", https://arxiv.org/abs/2609.26900 (2026-09-22): CaMeL (released implementation and its four suite policies), deciding model Sonnet-5: over-privilege leakage 0.0895 against 0.3551 for a tool-name allowlist and 0.0020 for an argument-exact oracle; 16 of 609 attack sinks left open…
- Ma, Li, Xiao, Yu, Zhang, Vorobeychik, "AutoDojo: A Generative Benchmark for Evaluating Prompt Injection Defenses in LLM Agents"… (2026-06-13): AgentDojo (banking, slack, travel), clean utility / static attack success / adaptive attack success. CaMeL: GPT-4o-mini 26.3 / 0.0 / 0.0; GPT-5.4-mini 52.6 / 1.8 / 1.8; Gemini-2.5-Flash 28.1 / 0.3 / 0.3; DeepSeek-v4-Flash 38.6 / 0.8 / 0.5…
- …and 2 more sources in `library/entries/code-then-execute.yaml`.

## Caveats

The guarantee holds only where labels are tracked and policies are written: an audit found leaks through untaken branches, the retry loop and string interpolation (Garby, Feb 2026), an error message carried an injection into the privileged model (Ji, Nov 2025), tool output written into another agent's instructions got through (Peters-Gill, Oct 2026), and untrusted data can still choose among the program's branches. Several tests ran CaMeL without its policies (Ji, Nov 2025; Peters-Gill, Oct 2026) or on one 16-task suite with wide intervals (Garby, Feb 2026), the strongest utility figure (77.3% for o3) is the authors' own, and the independent test that kept the policies found the largest utility cost of ten defenses on four of five models (Ma, Jun 2026). Tasks whose actions come from the data cannot be expressed at all, and frontier models already resist static template attacks undefended (0.3% for Claude-Haiku-4.5, 0.0% for GPT-5.5), so the case rests on adaptive attackers and on a hard block on exfiltration.

## Related

- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)

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
