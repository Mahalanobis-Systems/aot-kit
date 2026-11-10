---
name: constrain-agent-reach
description: "AOT optimization 10.a.i (Tier 2, Reliability): Constrain what the agent can touch. Placeholder. Use when an agent shows: commands touching paths outside the workspace once symlinks are resolved; reads of credential files; writes to hooks, editor tasks or git config; egress to hosts outside the allowlist; requests to run a command outside the sandbox; queries returning very large result sets; out-of-memory kills; failure rows labeled unauthorized-irreversible-action."
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

Limit what the agent can reach at the operating system, not in its prompt or tool wrappers. Run the agent process and every program it starts in one OS-level sandbox (a VM, gVisor or a hardened container) with network denied by default, a path guard that resolves symlinks and checks the file it will actually act on, credentials kept outside the sandbox behind a proxy or scrubbed from the command environment, agent-written SQL read-only with timeouts and row caps, and resource limits with headroom. In one study of 74 scripted attacks on a coding agent, a tool allowlist plus a command sandbox like those deployed agents use let 56 succeed, while confining the whole agent and resolving every request let 2 succeed at the cost of 3 of 46 benign operations; a vendor reports its sandbox cut permission prompts 84% and that only environment controls could have stopped a pasted prompt that exfiltrated credentials in 24 of 25 runs. The limits: secrets still leave through allowed hosts in encoded form, seven frontier models escaped misconfigured containers in every run, and memory limits pinned at a benchmark's spec failed 5.8% of its runs.

## When it applies

- **In the code:** shell or code execution without a sandbox, or a sandbox around spawned commands only while the agent process runs unconfined; privileged containers, a mounted Docker socket or writable host mounts; path checks on the string (prefix match, or before symlinks are resolved); credentials in the agent's environment or in files it can read; an agent-reachable way to run commands outside the sandbox; open network, or allowlisted hosts that accept any account's credentials; write access where read is enough; no row cap or timeout on agent SQL; memory limits set equal to the guaranteed allocation
- **In traces:** commands touching paths outside the workspace once symlinks are resolved; reads of credential files; writes to hooks, editor tasks or git config; egress to hosts outside the allowlist; requests to run a command outside the sandbox; queries returning very large result sets; out-of-memory kills; failure rows labeled unauthorized-irreversible-action
- **In eval results:** safety evals with out-of-bounds actions (credential reads, writes outside the workspace, egress) and container-escape checks for the configuration in use
- **Probes:** Out-of-bounds probes from inside the agent's environment.

## How (outline)

1. Start from the baseline: list everything the agent and the programs it starts can reach (files it can read and write, including ~/.ssh, ~/.aws and .env; network destinations; credentials in its environment or in readable files; database roles; local sockets and daemons; and files other tools execute later, such as editor tasks, agent hooks, git config and HEAD, and virtual-environment interpreters), then run out-of-bounds probes against the current setup and record which succeed.
2. Isolate at the operating system, not in the tool wrapper: run the agent process itself and every program it starts, interpreters included, under one policy (in one study a tool allowlist plus a command sandbox that confined only spawned programs still let 56 of 74 attacks through; also confining the agent process and resolving every request to the object it acts on let 2 through). Use a VM or gVisor where the agent runs unattended or its users cannot judge shell commands, and prefer maintained primitives (hypervisors, gVisor, seccomp, bubblewrap, Seatbelt) over code you write yourself. In containers, never use privileged mode, a mounted Docker socket or writable host mounts, drop unneeded capabilities, and patch the kernel and runtime: seven frontier models escaped such misconfigured containers in every run. Remove any switch the agent can use to run a command outside the sandbox, and do not load project-local config or hooks before the user trusts the folder.
3. Deny network by default and route allowed traffic through a proxy outside the sandbox. Treat each allowlisted host as a capability grant, not a destination filter: an allowlisted API can accept uploads to an attacker's account, so at the proxy pass only requests that carry the session's own token, bind entries to host and port, and resolve host names so a name that points at an internal address is refused.
4. Bound files by object, not by name: allow writes only inside the workspace and deny reads where secrets live; resolve every path (.., symlinks, hard links, case aliases) to the file the kernel will open before checking it, and check again at use; keep the repository's own control files (.git, agent settings and hooks, editor tasks, virtual-environment interpreters) read-only or held for review; mount read-only or no-delete where the task allows.
5. Keep credentials and data access narrow: keep secrets out of the sandbox (in the host keychain, or in a broker or proxy that attaches a per-session, revocable, scoped token on the way out); where a secret must stay in a command environment, scrub variables whose names match TOKEN, SECRET, KEY, AUTH or CREDENTIAL from every other command; give agent-written SQL a read-only role with a statement timeout and a row cap (one text-to-SQL agent allowed only SELECT and WITH, a 25-second timeout and 10,000 rows).
6. Limit compute with headroom: set CPU, memory, process and time limits on generated code as a guaranteed allocation plus a separate, higher kill threshold, calibrated so task success at the two levels is within noise (on Terminal-Bench 2.0, limits pinned at the per-task spec failed 5.8% of runs on infrastructure errors; a 3x ceiling cut that to 2.1% with no significant change in score).
7. Measure: rerun the out-of-bounds probes and reach-related safety cases before and after (canary reads outside the workspace directly, through a symlink and from a spawned interpreter; writes to hooks and editor tasks; a request to a non-allowlisted host and an encoded canary sent to an allowlisted one; a write through the SQL tool; a container-escape check for your configuration), plus the task eval for completion, latency and permission prompts per task; in production, monitor sandbox denials, egress decisions, prompts and out-of-memory kills, alert on attempts to run outside the sandbox, and export these logs where isolation hides the agent from endpoint monitoring.

## How to measure

- **before-after** (Tier 2): run out-of-bounds probes and reach-related safety cases before and after the change: canary reads outside the workspace (SSH key, cloud credentials, .env) directly, through a symlink and from a spawned interpreter; writes outside the workspace and to files other tools execute (hooks, editor tasks, git config); a request to a non-allowlisted host and an encoded canary sent to an allowlisted one; a write and an unbounded query through the SQL tool; and a container-escape check for the configuration in use; count successes and escalations per category, and rerun the task eval for completion, wall-clock time and permission prompts per task
- **monitor**: per session: sandbox denials and escalations by category, egress allow and deny decisions by host, credential use through the proxy, permission prompts, out-of-memory kills and infrastructure errors; alert on attempts to run outside the sandbox and on reads of credential files; export the logs where isolation hides the agent from endpoint monitoring

## Expected impact

- **Quality:** degrades, small: where limits are too tight or confinement blocks legitimate work: memory limits pinned at the per-task spec failed 5.8% of Terminal-Bench 2.0 runs on infrastructure errors and uncapped resources scored 6 points higher, while a 3x ceiling cut errors to 2.1% with no significant score change (Segato, Feb 2026); object-bound confinement completed 43 of 46 operations and 4 of 7 workflows against 46 and 7 for an allowlist with a command sandbox, failing on subprocesses, virtual environments and commit -a (Commey, Oct 2026)
- **Cost:** degrades, small (unmeasured): mainly build and upkeep: native OS sandboxing is 'a substantial multi-thousand-line investment' where a harness builds its own, while Claude Code wraps a reusable runtime (Barbaste, Jul 2026); one confinement broker is 3,164 lines of trusted code (Commey, Oct 2026); no source measures run cost
- **Performance:** mixed, small: a brokered request added 4.0 ms and spawned programs 8.5 to 18.4 ms (Commey, Oct 2026); where an OS sandbox replaced per-action approval, permission prompts fell 84% (Anthropic, May 2026, vendor claim)
- **Security:** improves, large: against 74 scripted attacks on a coding agent, a tool allowlist let 66 succeed, the allowlist plus a command sandbox around spawned programs 56, and object-bound confinement of the whole agent 2, with 14 held for review (Commey, Oct 2026); the vendor judged environment controls the only defense against a pasted prompt that exfiltrated cloud credentials in 24 of 25 runs (Anthropic, May 2026); the bound: seven frontier models escaped misconfigured containers in every run, and Claude Mythos Preview escaped in 84% of runs across 18 tasks at a 100M-token budget (Marchand, Mar 2026, updated Aug 2026)
- **Governance:** mixed, small: an open-sourced sandbox runtime makes the boundary auditable (Anthropic, May 2026) and a broker can sign every authorization into a tamper-evident log (Commey, Oct 2026), but VM isolation kept enterprise endpoint detection from seeing inside, with only pulled log exports as a mitigation (Anthropic, May 2026)

## Evidence (summary)

- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Codex vendored Bubblewrap with "--ro-bind, --unshare-net, --unshare-user, --unshare-pid"; "Protected paths (.git, .agents, .codex) are re-marked read-only even when they sit inside a writable root"; described as "a substantial…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI "environment scrubbing of provider credentials (name-pattern regexes over TOKEN/SECRET/KEY/AUTH/CREDENTIAL, a denylist, and GitHub-token value regexes) before each command runs."
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Held fixed, not ablated: 'A workspace guard resolves each path and rejects any that escapes the project root, including through symlinks.' A read-before-write check and a permission layer that classifies each action as allow, ask or deny…
- Youngwon Lee, Jaejin Kim, Seung-won Hwang (Seoul National University), "Bootstrapping Semantic Layer from Execution for Text-to-SQL (GATE… (2026-06-04): Implementation detail, not ablated: SQL queries 'are restricted to read-only operations (SELECT / WITH only)', with data-modifying statements 'rejected before execution'; 'Each query is subject to a timeout of 25 seconds, and results are…
- Adam Jones, Conor Kelly (Anthropic), "Code execution with MCP: Building more efficient agents"… (2025-11-04): "Running agent-generated code requires a secure execution environment with appropriate sandboxing, resource limits, and monitoring. These infrastructure requirements add operational overhead and security considerations that direct tool…
- …and 4 more sources in `library/entries/constrain-agent-reach.yaml`.

## Caveats

The measured evidence is small and mostly comes from builders and vendors: the 74-attack comparison is one author's scripted suite against his own system on one small Python project, with the deployed-style sandbox modeled rather than run, and the 84% prompt reduction and the 24-of-25 exfiltration are a vendor's reports on its own products, with no attack rates with and without its sandbox. A boundary controls where data goes, not what it encodes: both attacks that beat full confinement sent an access key to an allowlisted host Base64-encoded or split in two, and a vendor's sandbox let workspace files leave through its own allowlisted API under an attacker's key. Container isolation erodes as models improve: seven frontier models escaped misconfigured containers in every run, and with a 100M-token budget Claude Mythos Preview escaped in 84% of runs across all 18 tasks, kernel and runtime exploits included, though the agents knew escape was the goal and no one was monitoring. Tight settings cost work: full confinement, which refuses process creation, finished 4 of 7 workflows, and memory limits pinned at a benchmark's spec failed 5.8% of runs on one Claude model, with uncapped resources scoring 6 points higher.

## Related

- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
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
