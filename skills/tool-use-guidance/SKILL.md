---
name: tool-use-guidance
description: "AOT optimization 2.b.ii (Tier 3, Tuning): Tell the agent when to use each tool, in context it always sees. Placeholder. Use when an agent shows: tool spans: a tool or skill not called on cases where its trigger condition held (a docs skill was never invoked in 56% of eval cases), or called where it was not needed (open models made more than one call per task by default, including on tasks they could answer directly); bash spans where a dedicated tool exists; a skill opened whose rule the agent then did not follow; failure rows labeled incorrect-tool-selection."
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

Write down when the agent should use each tool, and put it where the model always reads it. For each under-used or misused tool or skill, add a rule to the system prompt or AGENTS.md naming the situation, the tool and what it replaces (e.g. the dedicated read or edit tool rather than bash), instead of leaving it inside a skill the agent must choose to open: an explicit AGENTS.md instruction took a docs skill that was never invoked in 56% of cases from a 53% to a 79% pass rate, and in another study a rule loaded only on demand kept about half of its effect. Test the wording against no rule and an irrelevant rule of the same length, since results swing with it: a one-line skill reminder did nothing where a per-skill YES/NO check reached 100% activation, telling models to call tools 'only if necessary' changed almost nothing while 'use sparingly' also cut needed calls, and a scope instruction that recovered most of the answers an unnecessary tool had cost reduced one model's needed tool use. It will not make a model that rarely calls tools start calling them, and in one coding study random rule files helped as much as curated ones, so measure the rule's own effect on call rates, not only pass rate.

## When it applies

- **In the code:** tools or skills whose intended use is stated nowhere the model always sees; overlapping tools with no rule for choosing between them
- **In traces:** tool spans: a tool or skill not called on cases where its trigger condition held (a docs skill was never invoked in 56% of eval cases), or called where it was not needed (open models made more than one call per task by default, including on tasks they could answer directly); bash spans where a dedicated tool exists; a skill opened whose rule the agent then did not follow; failure rows labeled incorrect-tool-selection
- **In eval results:** failures where the right tool existed but was not called; questions the model can answer alone that it refuses or gets wrong once a related tool is offered
- **Probes:** Cases at each rule's trigger boundary: ones that need the tool phrased with and without its obvious keywords, ones that do not need it, and boundary cases between overlapping tools.

## How (outline)

1. Start from the baseline: on the eval set (or recorded sessions), log per tool and skill the call rate on cases where its trigger condition holds and where it does not, wrong-tool calls (bash used to read, search or edit files where a dedicated tool exists; the wrong one of two overlapping tools), pass rate, tokens, turns and latency. Include cases that need the tool, phrased with and without its obvious keywords, and cases that do not: in one practitioner test a skill fired about 100% of the time when the prompt held its keyword, 20-40% on generic phrasing and about 0% on indirect phrasing, and in one benchmark open models made more than one tool call per task by default, even on tasks they could answer directly.
2. Pick the targets from those traces: tools or skills rarely called where they would have helped (a docs skill was never invoked in 56% of one vendor's eval cases), tools called where they are not needed or where a dedicated one exists, and questions a tool's mere presence made the model refuse or get wrong (one related but unnecessary tool cut answer rates from 98.2% to 63.5% across six models). If the model rarely calls any tool, a rule will not fix it (weak models barely searched when told to), so change the model (1.b.i) rather than the wording.
3. Write one rule per target: the situation, the tool, and what it replaces (e.g. to read or search files, use the Read and Grep tools instead of cat or grep in Bash; for questions about X use tool A, for Y tool B), naming the exact tool, command or path. In one study of rules added to real Skills, the gain came mainly from rules that named a command or path the agent had not been given, and stating the rule added 0.15 compliance beyond merely mentioning the token. Where a tool is over-used, name the cases that do not need it rather than adding a blanket instruction: across six open models 'only if necessary' changed almost nothing (-1.0 points, 0.06 fewer calls per task) and 'expensive, use sparingly' cut needed calls too, costing 8.4 points of accuracy (11.1 on hard tasks).
4. Put the rules where the model always reads them (system prompt, AGENTS.md or CLAUDE.md), not in an optional skill body: with the rule inside a Skill the agent had to choose to open, four coding agents kept 51% of its effect on the required action on average (three open models 38%, Claude Sonnet 4.5 all of it). Generate the rules from the active toolset, as Pi does with per-tool prompt snippets, so the prompt never names a tool that is not offered, and keep them short: carrying a whole Skill body in context cost 37-57% more tokens per episode. If triggers still fail, re-inject a short check each turn: a hook that made Claude Code state YES or NO for each skill before acting took activation from 50-55% to 100% on 22 prompts in two runs, where a one-line reminder (50-59%) and the harness's built-in prompt hook (41-55%) did not help.
5. Check both directions before keeping a rule: a scope instruction that restored 27.8 to 45.6 points of answers on four models cut GPT-OSS 20B's tool use where the tool was needed from 94.4% to 72.4%, and asking the model to reason about need before every call collapsed tool calling on two Llama models (Llama-3.3-70B accuracy 83.1% to 47.9%).
6. A/B two or more wordings against no rule and against an irrelevant rule of the same length, with several runs per arm, because a gain may not come from the rule's content: in one coding study random rule files matched curated ones (63.8% each against a 50.0% baseline), while another found same-length unrelated text had no effect. Keep the wording with the highest trigger recall and pass rate and no rise in false triggers or in failures on previously passing cases, and drop rules the model already follows or ignores (one rule-model pair in five added tokens with no detected gain).
7. Measure: run the paired eval per model and re-run it when the model, harness or toolset changes; report per tool the trigger recall and false-trigger rate, the wrong-tool rate, pass rate overall and on cases that need the tool, and tokens, turns and latency; track the same call rates in production traces.

## How to measure

- **experiment** (Tier 3): paired eval per model with no rule, the rule in two or more wordings and an irrelevant rule of the same length, several runs per arm: trigger recall per tool on cases that need it (including phrasings without its keywords), false-trigger rate on cases that do not, wrong-tool rate between overlapping tools, pass rate overall, on hard cases that need the tool and on previously passing cases, and tokens, turns and latency per task
- **monitor**: per tool and skill in production traces: call rate where its trigger condition holds and where it does not, bash calls where a dedicated tool exists, and skills opened but not acted on; re-run the paired eval when the model, harness or toolset changes, and retire rules the model now follows without them or ignores

## Expected impact

- **Quality:** improves, medium: an explicit AGENTS.md instruction took a docs skill's pass rate from 53% to 79% (Vercel, Jan 2026); added rules raised the rate agents took the required action by 0.23 and human-judged correctness by 0.10 on average (Wang, Oct 2026); a per-turn skill check took activation from 50-55% to 100% on 22 prompts (Spence, Feb 2026); a scope instruction recovered 27.8 to 45.6 points of answers lost to an unnecessary tool on four of six models (Paturi, Sep 2026); against that, VeRO's tool-instruction edit lost 5 points on MATH (VeRO, Feb 2026), 'use sparingly' cost 8.4 points (Sun, May 2026), and random rule files matched curated ones (Zhang, Apr 2026)
- **Cost:** mixed, small: a rule adds input on every call (a revised Skill added 18-19% to a single answer), but tokens per agent episode moved -2.3 to +3.0% because agents took fewer steps, while carrying a whole Skill body cost 37-57% more, and one rule-model pair in five added tokens with no detected gain (Wang, Oct 2026); with no instruction open models made more than one tool call per task, and 'use sparingly' cut 0.46 calls per task only by dropping needed calls too (Sun, May 2026)
- **Performance:** mixed, small: a short rule cut single-answer latency 1.6-7.2% because answers got shorter (Wang, Oct 2026); a per-turn instruction to evaluate every skill raised time per turn from 8.7 s to 10.7 s, against 6.4 s with a small pre-classifier that named the skills (Spence, Feb 2026)
- **Governance:** improves, small (unmeasured): a written rule documents each tool's intended use, and routing reads and edits to dedicated tools rather than shell leaves actions a reviewer can follow, Claude Code's stated reason for its rule (Barbaste, Jul 2026); no source measures it

## Evidence (summary)

- paper Figure 12 (Orchestrator, Sonnet 4.5; 'Early Peaker') (2026-02): Phase 3, 'Enhanced tool usage instructions', added right after phase 2 added a SymPy calculator tool: validation 0.917 to 0.867 (regressed), train flat at 0.813. The figure gives only the label, not the instruction text.
- paper Figure 15 (Orchestrator, Opus 4.5; 'Best SimpleQA') (2026-02): Phase 1, 'Improved prompt, tool descriptions', bundled with prompt changes: validation 0.577 to 0.622, train 0.456 to 0.587. Not separable from the description changes (T35).
- Jude Gao (Vercel), "AGENTS.md outperforms skills in our agent evals"… (2026-01-27): Trigger rate to 95%+, pass rate 53% -> 79% (+26pp); Build/Lint/Test 95/100/84. Still 21pp below the AGENTS.md index. Vercel calls the wording sensitivity "brittle for production use".
- Jude Gao (Vercel), "AGENTS.md outperforms skills in our agent evals"… (2026-01-27): Skill never invoked in 56% of eval cases; pass rate 53% = baseline 53% (+0pp); on tests 58% vs baseline 63%, lint 89% vs 95%.
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Claude Code "Do NOT use the Bash tool to run commands when a relevant dedicated tool is provided ... allows the user to better understand and review your work."
- …and 8 more sources in `library/entries/tool-use-guidance.yaml`.

## Caveats

The measured evidence is small and mostly from coding agents: one vendor's eval of one docs skill, one study of rules added to real Skills (80 sandbox tasks, thinking off, Claude Sonnet 4.5 run once per cell), one practitioner test of skill activation (22 prompts, one turn, no task outcome) and one CLAUDE.md study on one model whose single contrasts were not significant. Wording and model decide the result: across six open models 'use tools only if necessary' changed almost nothing and 'use sparingly' also cut needed calls (8.4 points of accuracy), asking for a necessity check before acting collapsed two Llama models' tool calling (Llama-3.1-8B 79.5% to 31.2%) while a per-skill YES/NO check took Sonnet 4.5 to 100% activation, and a scope instruction that restored answers on four models cut another's needed tool use from 94.4% to 72.4%. A rule's gain may not come from its content: random CLAUDE.md rule files raised Opus 4.6's pass rate as much as curated ones (63.8% each against 50.0%), though another study found same-length unrelated text had no effect on rule compliance, and VeRO's tool-instruction edit lost 5 points on MATH while its SimpleQA gain is bundled with description changes. Rules do not create tool use a model lacks: weak models barely searched when told to (BrowseComp-Plus), and agents that had read a rule acted on it in 61% (Qwen 3.5-27B) to 88% (Sonnet 4.5) of episodes.

## Related

- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:skill-library` (4.c.ii, Skill library evolution)
- `aot-kit:inject-runtime-context` (3.a.iii, Dynamic context injection)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
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
