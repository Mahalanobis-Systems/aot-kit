---
name: contain-untrusted-input
description: "AOT optimization 10.c.i (Tier 2, Reliability): Contain sensitive data and untrusted input. Placeholder. Use when an agent shows: sensitive fields in model inputs or logs; injected instructions followed; benign tool outputs blocked by a detector; failure rows labeled indirect-prompt-injection."
---

<!-- Generated from library/entries/contain-untrusted-input.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Contain sensitive data and untrusted input

> **Placeholder.** Generated from `library/entries/contain-untrusted-input.yaml` (entry 10.c.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 10.c.i |
| Earlier id | T70 |
| Tier | 2 (Reliability): safety containment |
| Categories | Safety: Containing data |
| Change | tool / transformation (add) |
| Also covers | Dual LLM (privileged / quarantined); Context minimization |

## What it is

Treat everything the agent reads from tools, the web, repository files and skills as data, not instructions, and keep personal data out of the model's context. Tokenize PII in the client, wrap untrusted results in source-labeled delimiters, scan context files, skills and tool outputs for injection, and state which source wins a conflict. These are cheap layers against opportunistic attacks, not a boundary: in one study an adaptive attacker reached 99% attack success against delimiter-based spotlighting on Gemini 2.5 Pro and 90 to 94% against three injection detectors, and in another none of 14 open-weight models reliably kept even two declared priority tiers in order. Choose a detector on your agent's own tool outputs at a low false-positive rate (on AgentDojo, PIGuard, which caught 95.1% of injections on BIPIA, caught 2.1% at 1% false positives, while two agent-oriented detectors caught 73.8 and 82.2%), scan repository docs first (GPT-5.4 followed an injection in a README or TODO file 2.6 times as often as in code or data files), and put consequential actions behind containment that does not depend on spotting the attack (6.c.i, 6.c.ii, 10.a.i).

## When it applies

- **In the code:** PII or untrusted content passed to the model unmarked; context files, skills or tool outputs loaded without an injection scan; a detector chosen by its public benchmark score; no instruction-precedence statement, or one never tested for where it holds
- **In traces:** sensitive fields in model inputs or logs; injected instructions followed; benign tool outputs blocked by a detector; failure rows labeled indirect-prompt-injection
- **In eval results:** injection attack success under static and adaptive attacks, with utility with and without attack; detector false-positive rate on the agent's own tool outputs and detection at 1% false positives; data-leak safety evals
- **Probes:** whether injected instructions in untrusted surfaces are followed, and whether the declared precedence holds

## How (outline)

1. Start from a baseline: list every place personal data and untrusted text enter the context (tool and MCP results, web pages, email, repository docs such as README and TODO files, context files such as AGENTS.md, skills, tool descriptions, memory), then measure the current agent: plant a canary instruction at the start, middle and end of each surface and record attack success, how failed attacks fail, and task success with and without the attack. Weight the surfaces by risk: in one study with a fixed payload, GPT-5.4 followed it in 86% of runs that read it from a README against 19% from a code file (reconnaissance goal), 2.6 times as often on average in README or TODO files as in code or data files, and placing it at the end of the content was most effective in all three domains tested. Do not read a low attack rate as refusal: 66.8% of GPT-5.4's and 81.3% of GPT-4o's failed injections were ignored, not flagged.
2. Keep sensitive data out of the model: tokenize PII in the client or MCP layer so the model handles placeholders while real values flow from tool to tool (Anthropic's design, unmeasured), and drop untrusted segments from the context once the step that needed them is done.
3. Mark untrusted content: wrap tool, web and repository-derived text in delimiters that name its source, and defang lookalike closing tags inside it (as the Hermes and OpenHands harnesses do). Expect little from this alone: in one AgentDojo study, spotlighting moved static attack success from 30% to 28% on Gemini 2.5 Pro and from 35% to 28% on Llama 3.3 70B; utility held on Gemini 2.5 Pro (74.23% to 75.26%) but fell from 56.70% to 39.18% on Llama 3.3 70B, so measure utility on your model.
4. State a precedence order (operator policy, then user, then repository configuration, with tool and external content as data), then test where it holds on your model instead of assuming the system message protects it. In one study of 14 open-weight models, the data ruled out that any model kept even two declared priority tiers in order in 95% of replies; the first of two conflicting lines in one message won 72.42 to 94.66% of decided replies; and in tool and file-write tasks a policy sent first in the system message won less often than the same text sent first as a labeled user message in every model-mode, by 6.41 to 48.75 points. Probe conflicts across messages and placements (sending the policy after the competing line raised its wins by 19.79 to 48.22 points on Qwen 3, though recency also favors injected lines), and log dropped instructions in the harness: at most 2.92% of replies mentioned the conflict.
5. Scan context files, skills and tool outputs, and block or quarantine on a match (Hermes blocks a matching context file wholesale and tiers skills as builtin, trusted or community). Choose the detector on your own data, not its published scores: replay the agent's benign tool outputs to count false positives as blocked tasks, and measure detection at a fixed 1% false-positive rate on injected copies. On AgentDojo tool outputs, two agent-oriented detectors caught 73.8 and 82.2% of injections at 1% false positives and Prompt Guard 2 caught 60.9 to 69.4%, while PIGuard, which caught 95.1% on BIPIA, caught 2.1%; ProtectAI v2 and PIGuard flagged 30.1% and 29.5% of benign tool outputs, enough to stop 69.1% and 59.8% of tasks. Strip markup before scanning (PIGuard's false positives on README chunks fell from 24.6% to 5.6%).
6. Assume an adaptive attacker gets through these layers, and contain the consequences with controls that do not depend on recognizing the injection (6.c.i, 6.c.ii, 10.a.i, 10.b.i). In one study, a search attack of up to 800 queries reached 99% attack success against spotlighting and 95% against prompt sandwiching on Gemini 2.5 Pro, 90 to 94% against the Protect AI, PromptGuard and Model Armor detectors and 71% against PIGuard, and 96% against the trained MetaSecAlign 70B (5% under the static attack); GPT-5 Mini held best (47% with spotlighting).
7. Measure with paired runs on the same tasks, each layer on and off: attack success under static and adaptive attacks (an attacker that sees the defense and gets a few hundred queries; most searches in that study plateaued after 100 to 200), utility with and without attack, episodes that stayed safe but left the user's task undone, detector false positives on the agent's own tool outputs and detection at 1% false positives, added latency per screened output, and sensitive fields found in model inputs and logs.

## How to measure

- **experiment** (Tier 2): paired runs on the same tasks with each layer (PII tokenization, delimiters, the precedence statement and its placement, the detector) on and off: attack success under static and adaptive attacks, with canaries at the start, middle and end of each untrusted surface (repository docs first); utility with and without attack; episodes safe but with the user's task undone; the detector's false-positive rate on the agent's own benign tool outputs (as blocked tasks) and its detection at 1% false positives; added latency per screened output; sensitive fields in model inputs and logs
- **monitor**: in production traces: detector flag rate on tool outputs and tasks stopped by a flag (sample flagged outputs for review), canary or known-payload hits, actions taken after reading flagged content, sensitive fields in model inputs and logs, and conflicts in which a lower-precedence instruction won

## Expected impact

- **Quality:** mixed, medium: delimiters left AgentDojo utility unchanged on Gemini 2.5 Pro (74.23% to 75.26%) and GPT-5 Mini (72.16% to 76.29%) but cut it from 56.70% to 39.18% on Llama 3.3 70B, and with Gemini 2.5 Pro utility fell to 39.18% under the Protect AI or PIGuard detector (Nasr, Oct 2025); detectors that over-flag stop tasks: ProtectAI v2 and PIGuard flagged about 30% of benign tool outputs, stopping 69.1% and 59.8% of tasks, while Prompt Guard 2 flagged 0.0 to 0.6% (Liu, Oct 2026)
- **Cost:** degrades, small (unmeasured): a detector call per screened output (68M to 1.5B parameters, or a 7 to 8B judge, in one study (Liu, Oct 2026)) and delimiter tokens on every untrusted result; tokenizing PII and purging used segments can shrink the context; no source priced any of it
- **Performance:** degrades, small (unmeasured): one classifier or judge pass per screened tool output before the agent can act on it; no source timed it
- **Security:** improves, small: against static attacks only: spotlighting cut AgentDojo attack success from 30% to 28% (Gemini 2.5 Pro) and 35% to 28% (Llama 3.3 70B), and an adaptive search raised it to 99% on both (Nasr, Oct 2025); the best detectors caught 73.8 to 82.2% of static AgentDojo injections at 1% false positives (Liu, Oct 2026), but adaptive attacks reached 71 to 94% against four detectors with Gemini 2.5 Pro (Nasr, Oct 2025); declared precedence is not followed reliably (no open model kept two tiers in order in 95% of replies; Laddha, Oct 2026); PII tokenization is unmeasured
- **Governance:** improves, medium (unmeasured): keeps personal data out of model inputs and logs when values flow tool to tool through the client (Anthropic, Nov 2025, unmeasured); models mentioned an instruction conflict in at most 2.92% of replies (Laddha, Oct 2026), so the audit trail of what was dropped or flagged must come from the harness

## Evidence (summary)

- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "The real email addresses, phone numbers, and names flow from Google Sheets to Salesforce, but never through the model. This prevents the agent from accidentally logging or processing sensitive data. You can also use this to define…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Mistral Vibe "a formal instruction-hierarchy contract: seven precedence levels ... prompt-injection defense expressed as a ranking rather than prohibitions"; "Critical instructions—not overridable" and "Overridable defaults" sections.
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "untrusted tool results wrapped in <untrusted_tool_result> delimiters with lookalike defanging"; OpenHands "repository-derived context is wrapped in <UNTRUSTED_CONTENT> markers".
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "every context file is scanned for prompt-injection patterns and blocked wholesale on a match"; "builtin/trusted/community trust tiers and quarantine"; Pi trust-gates repo config but "context files load regardless—a documented…
- Chengquan Guo et al., "Where You Inject Matters: The Trust Region Effect in LLM Agents", https://arxiv.org/abs/2610.38867 (2026-10-28): Table 2a (GPT-5.4, coding): conditional ASR for the reconnaissance goal 86% in README, 61% in TODO, 19% in a code file, 30% in a data file; SQL injection 79 / 59 / 11 / 28%; §4.2: 2.6 times as often on average in a README or TODO file as…
- …and 3 more sources in `library/entries/contain-untrusted-input.yaml`.

## Caveats

No source tests these practices together, and PII tokenization has no measured leak or utility result. The measured numbers come from benchmarks with synthetic tool outputs and mostly static attacks, so detection rates are upper bounds and detector rankings barely transferred between benchmarks (Kendall tau 0.01 to 0.31); in one study adaptive attacks exceeded 80% on most pairs of model and defense, GPT-5 Mini holding best at 47 to 81%. The precedence results come from 14 open-weight models on short benign conflicts, not hosted frontier models or adversarial payloads, and the placement result from one fixed payload, mainly with GPT-5.4, counted only when the payload was read. Defenses also cost utility: detectors that over-flag stop most tasks, and spotlighting cut Llama 3.3 70B's AgentDojo utility from 56.70% to 39.18%.

## Related

- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:surface-unreadable-information` (8.a.ii, Surface information the source holds but the agent cannot read)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:inject-runtime-context` (3.a.iii, Dynamic context injection)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
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
