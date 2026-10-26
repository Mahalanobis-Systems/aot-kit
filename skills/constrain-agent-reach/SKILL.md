---
name: constrain-agent-reach
description: "AOT optimization 10.a.i (Tier 2, Reliability): Constrain what the agent can touch. Placeholder. Use when an agent shows: commands touching paths outside the workspace; queries returning very large result sets; failure rows labeled unauthorized-irreversible-action."
---

<!-- Generated from library/entries/constrain-agent-reach.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Constrain what the agent can touch

> **Placeholder.** Generated from `library/entries/constrain-agent-reach.yaml` (entry 10.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 10.a.i |
| Earlier id | T68 |
| Tier | 2 (Reliability): safety containment |
| Categories | Safety: Sandboxing |
| Change | config / environment (add) |
| Also covers | Tool capability compartmentalization |

## What it is

Run the agent in an OS-level sandbox with a workspace path guard that resolves symlinks, scrub credentials from the command environment, run agent-written SQL read-only with timeouts and row caps, and set resource limits on generated code.

## When it applies

- **In the code:** shell or code execution without a sandbox; credentials in the agent's environment; write access where read is enough; no row cap or timeout on agent SQL
- **In traces:** commands touching paths outside the workspace; queries returning very large result sets; failure rows labeled unauthorized-irreversible-action
- **In eval results:** safety evals with out-of-bounds actions

## How (outline)

1. List what the agent can reach (paths, credentials, databases, network).
2. Remove write access and credentials it does not need; add the path guard and limits.
3. Run the safety evals before and after.

## How to measure

- **before-after** (Tier 2): safety evals and out-of-bounds action attempts

## Expected impact

- **Quality:** none
- **Cost:** degrades, small
- **Performance:** degrades, small

## Evidence (summary)

- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Codex vendored Bubblewrap with "--ro-bind, --unshare-net, --unshare-user, --unshare-pid"; "Protected paths (.git, .agents, .codex) are re-marked read-only even when they sit inside a writable root"; described as "a substantial…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI "environment scrubbing of provider credentials (name-pattern regexes over TOKEN/SECRET/KEY/AUTH/CREDENTIAL, a denylist, and GitHub-token value regexes) before each command runs."
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Held fixed, not ablated. The deny and allow lists are given in the bash tool description.
- Youngwon Lee, Jaejin Kim, Seung-won Hwang (Seoul National University), "Bootstrapping Semantic Layer from Execution for Text-to-SQL (GATE… (2026-06-04): Implementation detail (Appendix B.2), not ablated.
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "Running agent-generated code requires a secure execution environment with appropriate sandboxing, resource limits, and monitoring. These infrastructure requirements add operational overhead and security considerations that direct tool…

## Related

- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)

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
