---
name: tool-use-guidance
description: "AOT optimization 2.b.ii (Tier 3, Tuning): Tell the agent when to use each tool, in context it always sees. Placeholder. Use when an agent shows: tool spans: a tool called on under about 5% of cases where its trigger condition held (e.g. a docs skill never invoked in 56% of runs); bash spans where a dedicated tool exists; failure rows labeled incorrect-tool-selection."
---

<!-- Generated from library/entries/tool-use-guidance.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Tell the agent when to use each tool, in context it always sees

> **Placeholder.** Generated from `library/entries/tool-use-guidance.yaml` (entry 2.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 2.b.ii |
| Earlier id | T09 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Tools: Avoiding misuse |
| Change | prompt / instructions (add) |
| Also covers | Tool docstrings with use / do-not-use guidance and examples |

## What it is

For each tool or skill that is under-used or misused, add an explicit trigger rule where the model always sees it (system prompt, AGENTS.md): the situation that calls for the tool, and what to use it instead of (e.g. the dedicated read or edit tool rather than bash). Test the wording, since results swing with it. It will not make a model that rarely calls tools start calling them. The cheapest form is one sentence per tool stating what it is for: that alone recovered most of a 34.7-point loss caused by offering the model an irrelevant tool.

## When it applies

- **In the code:** tools or skills whose intended use is stated nowhere the model always sees; overlapping tools with no rule for choosing between them
- **In traces:** tool spans: a tool called on under about 5% of cases where its trigger condition held (e.g. a docs skill never invoked in 56% of runs); bash spans where a dedicated tool exists; failure rows labeled incorrect-tool-selection
- **In eval results:** failures where the right tool existed but was not called

## How (outline)

1. From traces, list tools with a low call rate on cases where they would have helped, and tools chosen wrongly.
2. For each, write one rule: when to use it, and instead of what.
3. Put the rules in always-loaded context, not in an optional skill.
4. A/B two wordings; keep the one with the higher call rate and pass rate.

## How to measure

- **experiment** (Tier 3): paired eval with and without the rule, plus the tool's call rate in traces

## Expected impact

- **Quality:** improves, large: Vercel: pass rate 53% to 79% once told when to invoke the docs skill (Jan 2026); VeRO mixed: -5 and +4.5 points; one sentence of tool scope recovered most of a 34.7-point loss from an irrelevant tool (Paturi et al., Sep 2026)

## Evidence (summary)

- paper Figure 12 (Orchestrator, Sonnet 4.5; 'Early Peaker'): Phase 3, 'Enhanced tool usage instructions', added right after phase 2 added a SymPy calculator tool: validation 0.917 to 0.867 (regressed), train flat at 0.813. The figure gives only the label, not the instruction text.
- paper Figure 15 (Orchestrator, Opus 4.5; 'Best SimpleQA'): Phase 1, 'Improved prompt, tool descriptions', bundled with prompt changes: validation 0.577 to 0.622, train 0.456 to 0.587. Not separable from the description changes (T35).
- Jude Gao (Vercel), "AGENTS.md outperforms skills in our agent evals"… (2026-01-27): Trigger rate to 95%+, pass rate 53% -> 79% (+26pp); Build/Lint/Test 95/100/84. Still 21pp below the AGENTS.md index. Vercel calls the wording sensitivity "brittle for production use".
- Jude Gao (Vercel), "AGENTS.md outperforms skills in our agent evals"… (2026-01-27): Skill never invoked in 56% of eval cases; pass rate 53% = baseline 53% (+0pp); on tests 58% vs baseline 63%, lint 89% vs 95%.
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Claude Code "Do NOT use the Bash tool to run commands when a relevant dedicated tool is provided ... allows the user to better understand and review your work."
- …and 4 more sources in `library/entries/tool-use-guidance.yaml`.

## Related

- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:parallel-read-only-tools` (6.b.i, Parallel tool execution for read-only calls)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)

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
