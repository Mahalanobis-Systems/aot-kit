---
name: risky-action-policy
description: "AOT optimization 10.b.i (Tier 2, Reliability): Gate irreversible actions: allow, ask or deny by side effect. Placeholder. Use when an agent shows: irreversible actions taken without a policy or human check; failure rows labeled unauthorized-irreversible-action or over-initiative."
---

<!-- Generated from library/entries/risky-action-policy.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Gate irreversible actions: allow, ask or deny by side effect

> **Placeholder.** Generated from `library/entries/risky-action-policy.yaml` (entry 10.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 10.b.i |
| Earlier id | T69 |
| Tier | 2 (Reliability): safety containment |
| Categories | Safety: Gating risky actions |
| Change | tool / validation (add) |
| Also covers | Human-in-the-loop approval gates; Spectrum of control |

## What it is

Classify every action the agent can take by its side effect (read, reversible write, irreversible or externally visible: sending email, issuing a refund, deleting a record, posting publicly, pushing code) and gate by class: allow, ask a human or a policy, or deny. Where the environment already stages changes before they reach the world, gate only what escapes the stage. Coding agents can run on auto-approve because the development process contains their changes (a branch, PR review and CI stand between the agent and production). Most other agents (marketing, support, CRM, finance) have no such stage, so the gate has to sit at the action, or the harness has to build one: drafts, pending changes, batched approval. Keep a deny floor that auto-approve cannot switch off, and write the policy as code with tested examples.

## When it applies

- **In the code:** tools with irreversible or externally visible effects (send, pay, delete, publish, push) with no gate and no staging step; one approval setting for every tool; a deny list that auto-approve disables
- **In traces:** irreversible actions taken without a policy or human check; failure rows labeled unauthorized-irreversible-action or over-initiative
- **In eval results:** safety cases built from the agent's own irreversible actions, including prompt-injected requests for them

## How (outline)

1. List the agent's actions and mark each one's side effect: read, reversible write, irreversible or externally visible.
2. For each irreversible action, find where review can happen: an existing stage (branch and PR, draft, staging environment) or none.
3. Where there is no stage, add one (draft and approve, pending changes, batch approval) or an ask gate on the action; deny what should never run unattended, in a floor auto-approve cannot lift.
4. Write the policy as code with tested examples.
5. Run safety evals built from irreversible actions; monitor approved, denied and escalated actions in production, including how often humans approve without changes.

## How to measure

- **before-after** (Tier 2): safety evals on risky-action prompts
- **monitor**: denied and approved risky actions in production

## Expected impact

- **Quality:** none
- **Cost:** none
- **Performance:** degrades, small: approval waits; staging and batching keep them small

## Evidence (summary)

- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Pi "steer() queue injects messages after the current turn's tool calls, while followUp() drains only when the agent would otherwise stop"; Hermes "mid-turn user steering is spliced into the last tool result behind an anti-injection marker."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Mistral Vibe "a plan file under a dedicated plans directory is the profile's only writable target, and an exit_plan_mode tool emits a PlanReviewRequestedEvent"; "all four provider-native systems now ship a read-only planning mode."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI ApprovalMode enum (four modes); Mistral Vibe four-layer permission hierarchy; Rec 9: "matches how a human developer triages risk."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Codex execpolicy "rules may carry inline match/not_match examples that are validated at parse time—executable test cases inside the policy file"; Rec 11: "Policies-as-code survive refactors and are auditable independently of the loop."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "twelve-pattern hardline floor ... that survives --yolo—the YOLO environment variable is frozen at module import precisely so a prompt-injected skill cannot flip it"; 47 dangerous patterns "matched on deobfuscated variants".
- …and 4 more sources in `library/entries/risky-action-policy.yaml`.

## Caveats

Every source comes from coding-agent harnesses (a source-code study of 11 of them, and one controlled study that held the policy fixed), and none measures the gate's effect. The shell examples (rm -rf, sudo, git push, command parsing) are one case of the general rule. Asking too often has a cost of its own: approvals slow the agent, and humans who are asked constantly start approving without reading, so stage and batch where you can rather than prompt per action.

## Related

- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)
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
