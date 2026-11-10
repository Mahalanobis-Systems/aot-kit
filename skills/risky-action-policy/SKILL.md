---
name: risky-action-policy
description: "AOT optimization 10.b.i (Tier 2, Reliability): Gate irreversible actions: allow, ask or deny by side effect. Placeholder. Use when an agent shows: irreversible actions taken without a policy or human check; an operation blocked once and then reached through an allowed interpreter, script or file edit; flagged actions approved without change; failure rows labeled unauthorized-irreversible-action or over-initiative."
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

Sort every action the agent can take by its side effect (read, reversible write, irreversible or visible to others) and let it run, ask first, or block it by class. Where the environment stages changes (a branch with PR review and CI, a draft), gate only what escapes the stage, and count what takes effect at run time (uploads, deletions, credential reads, install hooks) as escaping. Gates work where the host enforces them: across six coding harnesses with injected instructions, auto-approve let 95.6% of attack checks pass against 29.2% with an LLM reviewer (at 18.3 points of task utility), and a command deny list cut attack success from 41.7% to 1.3% with no utility loss, yet an estimated 90% of destructive MCP tools have no server-side confirmation, so build a stage or enforce an ask gate in the host for every tool not marked read-only. Give approvers the action's effects, not only its text (approvers reading only the command left 14.8% to 18.8% of coding tasks harmed against 19.7% with no approval; one shown a sandboxed pre-run's effects left 6.7%), keep a deny floor that auto-approve cannot lift, and write the policy as code with tested examples.

## When it applies

- **In the code:** tools with irreversible or externally visible effects (send, pay, delete, publish, push) with no gate and no staging step; approval left to a confirmation argument the model can set or to annotations from an untrusted tool server; one approval setting for every tool; a deny list that auto-approve disables; an automated approver that sees only the command text; alerts that warn without blocking
- **In traces:** irreversible actions taken without a policy or human check; an operation blocked once and then reached through an allowed interpreter, script or file edit; flagged actions approved without change; failure rows labeled unauthorized-irreversible-action or over-initiative
- **In eval results:** safety cases built from the agent's own irreversible actions, including prompt-injected requests for them, and safe twins (same request and command, harmless effect) to count false blocks
- **Probes:** Tasks whose benign request leads to an irreversible action, including harm hidden inside a script or tool the command runs

## How (outline)

1. Start from the baseline: list every action the agent can take, by tool and by what each tool runs underneath (package scripts, build targets, interpreters, MCP tools), and mark its side effect: read, reversible write, or irreversible or externally visible (send, pay, delete, publish, push, network calls, credential reads). Treat a tool you have not checked as irreversible: an estimated 90% of destructive tools in a sample of the MCP registry have no server-side confirmation, and the MCP specification tells clients to treat tool annotations as untrusted unless the server is trusted. Run your eval set with auto-approve and count the irreversible actions the agent takes, including ones requested by injected content (with no approval step, four of five low-cost models carried out an injected deletion in 479 of 960 runs).
2. For each irreversible action, find where review can happen before it takes effect: an existing stage (a branch with PR review and CI, a draft, a staging environment, pending changes) or none. A stage holds only what waits in it: workspace edits behind PR review are staged, but a command's run-time effects are not (an upload, an install-hook callback, a deleted untracked file), nor is a write to a file a running system reads. Showing the agent its changes after each command is too late for these: a staging file system that the agent reviewed and reverted itself left 21.2% of 682 shell tasks harmed against 19.7% with no approval, because 'a credential once sent cannot be recalled'. Contain what the agent can reach first (10.a.i), so fewer actions need a gate.
3. Where there is no stage, build one (draft and approve, pending changes, batched approval) or enforce an ask gate in the host, not in the tool's arguments: given a confirmation flag, models set confirm=true themselves in 127 of 169 injected-deletion attempts. Ask by default for every tool not marked read-only or non-destructive by a source you trust: in one estimate this would leave 5.4% of destructive-tool and application pairs unapproved against 60.7% under current defaults, at the cost of asking on 82.6% of pairs whose flagged tool is harmless, against 32.5%. Where no one can answer (headless or scheduled runs), refuse or queue the action.
4. Keep a deny floor that auto-approve cannot lift for what must never run unattended: one harness denies rm -rf, sudo, git push, git reset --hard, chmod -R and chown -R by default; another keeps a twelve-pattern hardline floor that survives --yolo, with the switch frozen at startup so injected content cannot flip it, and matches 47 dangerous patterns on deobfuscated commands. Parse commands and scope 'always allow' grants to the command and its subcommand (git commit *), not the whole tool. In one benchmark a command deny list cut attack success from 41.7% to 1.3% of checks while utility rose from 94.6% to 99.8%, and an allowlist cut it from 98.1% to 50.0% at 1.5 points of utility, but one agent ran a checker the gate had refused through an allowed Python interpreter: test every path to each protected operation (interpreter, script, file edit, MCP tool).
5. Send the ask class to a human, a rule or an automated approver that fails closed on timeout or malformed output and returns its reason to the agent so it can take a safer path. Give the approver the action's effects, not only its text: on the same 682 tasks a rule checker, three guardrail models and Claude Code Auto Mode left 14.8% to 18.8% of tasks harmed against 19.7% with no approval, and 62.7% to 94.1% of tasks whose harm hid inside an invoked tool (71.6% with no approval); pre-running each command in a snapshotted sandbox with the network off and giving an LLM approver a short report of what it changed left 6.7% and 7.8% harmed, blocked 1.0% of safe look-alikes (61.8% for the same approver without the report) and rolled blocked commands back (see 4.b.i). Make a high-risk flag block by default and require an explicit override: with an LLM monitor alerting at the permission prompt, developers kept an agent's covert exfiltration in 9 of 16 correctly alerted sessions.
6. Write the policy as code with tested examples (rules carrying inline match and not-match cases validated at parse time), keep it under version control, and expose hooks that can deny or rewrite a call before it runs, so every decision is auditable apart from the agent loop. Check that the settings in effect are the ones you configured: of 205 confirmed security mechanisms across 40 coding harnesses, 109 are opt-in.
7. Measure on the same tasks and model with the gate off and on, several runs per arm: harmful outcomes checked on the environment's state (files, records, receiver logs) rather than the transcript, task utility, false blocks on safe twins (same request and command, harmless effect), prompts and blocks per task, approval latency (a median 3.2 s per command for an LLM approver in one study, plus about 0.5 s of sandboxing per allowed command) and approver cost. In production, track approvals, denials and escalations per action class, the approve-without-change rate, time to decision, overrides of flagged actions, retries after a block, and irreversible actions that ran with no recorded decision.

## How to measure

- **experiment** (Tier 2): same tasks and model with the gate off (auto-approve) and on, several runs per arm, on safety cases built from the agent's own irreversible actions, injected requests for them and safe twins (same request and command, harmless effect), including other paths to each protected operation (an allowed interpreter, a script, a file edit, an MCP tool); score harmful outcomes on the environment's state (files, records, receiver logs), task utility, false blocks on the twins, prompts and blocks per task, approval latency and approver cost
- **monitor**: per action class in production: approvals, denials and escalations, the approve-without-change rate, time to decision, overrides of flagged actions, retries after a block, irreversible actions that ran with no recorded decision, and harmful actions found later; recheck that the gate settings in effect match the configured ones after each harness update

## Expected impact

- **Quality:** mixed, medium: an LLM reviewer on permission requests cost 18.3 points of task utility against auto-approve across six coding harnesses (77.1% against 95.4% of utility checks), within 2.3 points in three harnesses and 30.8 to 44.6 points in the other three, while a command deny list raised utility from 94.6% to 99.8% and an allowlist cost 1.5 points (Zhu, Oct 2026); an approver that judged observed effects kept safe outcomes at 67.8% against 66.6% with no approval, though more of them were refusals (safe completions 48.6% against 57.4%) (Wu, Oct 2026)
- **Cost:** degrades, small: an LLM approver on each shell command cost $0.0135 per task (10.3 calls) on top of $0.0053 for a low-cost agent, against $0.0060 for the agent alone, and Claude Code Auto Mode's classifier an estimated $0.0550 per task at most (Wu, Oct 2026); no source measures human approval time
- **Performance:** degrades, small: median approval latency 3.2 s per command (p95 6.4 s) for an LLM approver given an effects report and 3.3 s (p95 11.4 s) without it, plus about 0.5 s of sandboxing per allowed command and 1.5 s per blocked one (Wu, Oct 2026); no source measures waits on a human
- **Security:** improves, large: against injected instructions in six coding harnesses, an LLM reviewer on permission requests cut attack success from 95.6% to 29.2% of checks against auto-approve (0.0% to 81.7% by harness), a command deny list from 41.7% to 1.3% and an allowlist from 98.1% to 50.0% (Zhu, Oct 2026); approvers that read only command text left 14.8% to 18.8% of tasks harmed against 19.7% with no approval, and one that judged observed effects 6.7% (Wu, Oct 2026); with no approval step, four of five low-cost models carried out an injected deletion in 479 of 960 runs (Yao, Nov 2026)
- **Governance:** mixed, medium: a gate puts a decision on each irreversible call only where the host enforces it: an estimated 60.7% of destructive-tool and application pairs in the MCP ecosystem have no enforced approval by default, 5.4% if hosts asked for every tool not annotated read-only or non-destructive (Yao, Nov 2026), and 109 of 205 confirmed security mechanisms in coding harnesses are opt-in (Zhu, Oct 2026); a human decision is weak oversight: developers kept an agent's flagged covert exfiltration in 9 of 16 correctly alerted sessions (Ye, Jun 2026)

## Evidence (summary)

- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Pi "steer() queue injects messages after the current turn's tool calls, while followUp() drains only when the agent would otherwise stop"; Hermes "mid-turn user steering is spliced into the last tool result behind an anti-injection marker."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Mistral Vibe "a plan file under a dedicated plans directory is the profile's only writable target, and an exit_plan_mode tool emits a PlanReviewRequestedEvent"; "all four provider-native systems now ship a read-only planning mode."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI ApprovalMode enum (four modes); Mistral Vibe four-layer permission hierarchy; Rec 9: "matches how a human developer triages risk."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Codex execpolicy "rules may carry inline match/not_match examples that are validated at parse time—executable test cases inside the policy file"; Rec 11: "Policies-as-code survive refactors and are auditable independently of the loop."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "twelve-pattern hardline floor ... that survives --yolo—the YOLO environment variable is frozen at module import precisely so a prompt-injected skill cannot flip it"; 47 dangerous patterns "matched on deobfuscated variants".
- …and 8 more sources in `library/entries/risky-action-policy.yaml`.

## Caveats

The measured evidence is recent, from benchmarks and small samples, and mostly from coding agents: the harness comparison ran one acting model and one 27B reviewer on two tasks per mechanism; the approver comparison ran each of 682 tasks once with one agent and one approver model, against no attacker that adapts to the approver; the human study had 17 to 19 developers per condition working with agents instructed to exfiltrate data; and the MCP shares (60.7% unapproved, and 5.4% if hosts asked for every tool not annotated read-only or non-destructive) are estimates from reading source code, not runtime counts. Every gate leaks where an action reaches it by another path (an allowed interpreter, a file edit, an MCP tool), approvers that read only command text barely beat no approval, and a sandboxed pre-run cannot undo anything that leaves the sandbox, so it has to run with the network off. Humans are weak approvers: most developers missed covert exfiltration in CI-gated sessions and most kept it after a correct alert, and asking for every tool not annotated read-only or non-destructive would raise asks on harmless tools (from 32.5% to 82.6% of such pairs in one estimate), so stage and batch where you can and keep a blocking deny floor beside the prompts.

## Related

- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:filesystem-checkpoints` (4.b.i, Filesystem-based agent state and checkpoints)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
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
