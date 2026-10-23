---
name: contain-untrusted-input
description: "AOT optimization 10.c.i (Tier 2, Reliability): Contain sensitive data and untrusted input. Placeholder. Use when an agent shows: sensitive fields in model inputs or logs; injected instructions followed; failure rows labeled indirect-prompt-injection."
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

Tokenize PII in the client so it never reaches the model, wrap untrusted tool and web results in taint delimiters, scan context files and skills for prompt injection, and state an explicit instruction-precedence order (user, repo, defaults, external data as data).

## When it applies

- **In the code:** PII or untrusted content passed to the model unmarked; no instruction-precedence statement
- **In traces:** sensitive fields in model inputs or logs; injected instructions followed; failure rows labeled indirect-prompt-injection
- **In eval results:** injection and data-leak safety evals

## How (outline)

1. Map where PII and untrusted text enter the prompt.
2. Add tokenization at the client and delimiters on untrusted results.
3. Add the precedence statement to the prompt.
4. Run injection and data-leak safety evals.

## How to measure

- **before-after** (Tier 2): injection and data-leak safety evals

## Expected impact

- **Quality:** none
- **Cost:** none
- **Performance:** none

## Evidence (summary)

- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "The real email addresses, phone numbers, and names flow from Google Sheets to Salesforce, but never through the model. This prevents the agent from accidentally logging or processing sensitive data. You can also use this to define…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Mistral Vibe "a formal instruction-hierarchy contract: seven precedence levels ... prompt-injection defense expressed as a ranking rather than prohibitions"; "Critical instructions—not overridable" and "Overridable defaults" sections.
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "untrusted tool results wrapped in <untrusted_tool_result> delimiters with lookalike defanging"; OpenHands "repository-derived context is wrapped in <UNTRUSTED_CONTENT> markers".
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "every context file is scanned for prompt-injection patterns and blocked wholesale on a match"; "builtin/trusted/community trust tiers and quarantine"; Pi trust-gates repo config but "context files load regardless—a documented…

## Related

- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:react-loop` (7.d.iii, ReAct loop)

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
