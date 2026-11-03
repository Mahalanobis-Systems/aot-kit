---
name: restructure-system-prompt
description: "AOT optimization 3.a.iv (Tier 3, Tuning): Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need. Placeholder. Use when an agent shows: failure rows labeled instruction-following-failure or instruction-grader-mismatch where the requirement was never in the prompt; prompt tokens the largest share of input per step; context-overflow outcomes."
---

<!-- Generated from library/entries/restructure-system-prompt.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need

> **Placeholder.** Generated from `library/entries/restructure-system-prompt.yaml` (entry 3.a.iv). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 3.a.iv |
| Earlier id | T04 |
| Tier | 3 (Tuning): it changes what the model sees |
| Categories | Prompts: Structuring |
| Change | prompt / system_prompt (restructure) |
| Also covers | System prompt altitude and sectioned structure |

## What it is

State each requirement once, in its own named section near the top of the system prompt, and cut what the model does not need. It pays most where rules have piled up or crowd out the task: with 80 rules in one prompt at most 1.9% of responses met them all across five current models, a one-call rewrite that merged and ranked stacked rules recovered 11.0 points of follow rate for GPT-5-mini, and generated repository context files raised coding agents' cost 20% and 23% with no significant gain in success. The limits: the same rewrite did nothing for Claude Sonnet 4.6 (-1.2 points), markdown against plain text made no reliable difference in one study, and in VeRO's TerminalBench runs a three-section rewrite broke as many passing tasks as it fixed while the hardest cut gave the best pass rate (37.1%). Add a domain procedure section only when failures cluster on a step an expert would take, and judge any section an optimizer writes on held-out cases (on one deep-research agent the gain was 0.079 held out against 0.202 on the validation set).

## When it applies

- **In the code:** system prompt with no named sections; requirements repeated, contradictory, or absent (no answer format, no completion criteria); pairs of rules that cannot both hold (JSON output and markdown headers); several dozen or more simultaneous rules in one prompt; context files that restate what the agent can find in the repository (overviews, directory listings); case-specific facts or answers left in the prompt by an optimizer; prompt plus tool descriptions over about a quarter of the context window
- **In traces:** failure rows labeled instruction-following-failure or instruction-grader-mismatch where the requirement was never in the prompt; prompt tokens the largest share of input per step; context-overflow outcomes
- **In eval results:** an ablation that removes a section and shows no loss (cut it), especially one that also lowers cost; failures that cluster on one step of the task procedure (add it); compliance per rule that falls as rules are added, or pairs of rules that fail together more often than each fails alone; an optimized prompt whose validation gain far exceeds its held-out gain
- **Probes:** One deterministic check per rule in the prompt, run with all rules, with each rule alone and with each section removed.

## How (outline)

1. Start from the current prompt as the baseline: run it on development and held-out cases and record pass rate, which cases pass and fail, compliance with each rule, steps, input tokens and cost per task. List every instruction the model receives (system prompt, context files such as AGENTS.md, checklists) and the requirements the task actually has, from the task spec and from failures.
2. Cut what the model does not need: content it can find or would do anyway (repository overviews, restated documentation), duplicated rules, and leftovers such as answers to specific eval cases. Across four coding agents, LLM-generated context files changed success by -0.5% and -2% while adding 20% and 23% to cost, their overviews did not shorten the search for the relevant file, and dropping only the testing section cut cost per task from $0.4715 to $0.3730 with no significant change in accuracy; the same files helped (+2.7%) only once the repository's other documentation was removed. Keep what the model cannot infer, such as non-standard conventions and requirements (developer-written files did better than generated ones). In VeRO's TerminalBench run, cutting the prompt from 7 lines to 3 and its checklist from 10 lines to 4, with shorter tool descriptions (2.a.ii) and a tighter output cap in the same commit, gave the best pass rate, 37.1%, and context-overflow failures fell from 13 to
2. 3. State each remaining requirement once, in a named section, and give the answer format and the completion check their own sections (what the format says and how the answer is read is 9.b.i). Merge duplicates and settle conflicts: where two rules cannot both hold (JSON output with markdown headers), drop one or say which wins. Keep the count down, since compliance falls as rules stack: three models followed about 96% of instructions given one at a time but 20% to 60% with twenty, and in another study the share of responses meeting every rule fell from 0.59-0.94 with 10 rules to at most 0.019 with 80; that author recommends treating about 40 rules as the point to split them across turns, tools or a validation check (not tested). A one-call rewrite that grouped rules by kind, merged duplicates, added a precedence note for conflicts and listed reasoning rules first and format rules last recovered 11.0 points of follow rate for GPT-5-mini and 3.3 for Gemini 2.5 Flash but -1.2 for Claude Sonnet 4.6, so expect the most from smaller models.
4. Pick one consistent way to mark sections (headings or tags) and do not expect the format itself to buy accuracy: across five current models none showed a reliable markdown advantage over plain text for a block of rules, and the one consistent difference favored plain text (4.8 points for one Qwen model at 160 rules). Test your own model anyway: Gemini Flash fell 18.1 points with 40 rules written as prose, and moving the same rules from the system prompt to the user turn changed adherence by -8.7 to +6.6 points depending on the model.
5. Add a domain procedure section only if failures cluster on a step; write it from those failures or from an expert, or generate variants with an optimizer such as GEPA. If an optimizer writes it, judge it on held-out cases that share no topic with those it saw, over several seeds, and strip case-specific content: on a deep-research agent GEPA's held-out gain was 0.079 against 0.202 on its 24-task validation set, memorized answers made up 52% and 39% of the two winning prompts without adding reward, the two longer candidates regressed, and a hand-written prompt keeping only the rules it found recovered about 57% of the gain.
6. Run the paired eval, old against restructured prompt, on the full development and held-out sets, not a subset (a VeRO rewrite scored 45% on a 20-task subset, then broke as many passing tasks as it fixed); report new passes and regressions per case as well as the net, compliance per rule, context-overflow failures, steps, tokens and cost; keep only sections that earn their place, and re-run after any model change.

## How to measure

- **experiment** (Tier 3): paired eval, old against restructured prompt, on the full development and held-out sets (topics disjoint from any an optimizer saw), over several runs or seeds and for each model in use: pass rate with new passes and regressions per case, compliance per rule from one deterministic check per rule, context-overflow failures, steps, input tokens and cost per task; remove one section at a time to find sections that cost tokens without changing outcomes
- **monitor**: in production: violation rate per rule and format-compliance rate on sampled traffic, prompt tokens as a share of input per step, steps and cost per task, and prompt growth (rules and lines added since the last restructure); re-run the paired eval when the model changes, since the value of a rewrite depended on the model

## Expected impact

- **Quality:** mixed, small: restructuring: a one-call rewrite of stacked instructions +11.0 points of follow rate for GPT-5-mini, +3.3 for Gemini 2.5 Flash, -1.2 (not significant) for Claude Sonnet 4.6 (Anand, Jul 2026); a dedicated verification section +4.75 to +5.0 points on GSM-Plus (Cemri, Mar 2025); a three-section rewrite gave 6 new passes and 6 regressions on TerminalBench, and MATH validation +0.10 with train -0.07 (VeRO, Feb 2026); an optimizer-written procedure on a deep-research agent +0.079 held-out reward (Lumer, Oct 2026); cutting: TerminalBench +6.8 points where the prompt crowded out context, GPQA train -0.04 where the optimizer could change only prompts, tool descriptions and parameters (VeRO, Feb 2026); repository context files changed coding-agent success by -2% to +2.4%, none significant (Gloaguen, Feb 2026); format: no reliable markdown advantage over plain text across five models (Eliav, Jul 2026)
- **Cost:** mixed, medium: cutting saves: LLM-generated context files raised cost 20% and 23% and developer-written ones up to 19% with no significant gain in success, and dropping one testing section cut cost per task from $0.4715 to $0.3730 (Gloaguen, Feb 2026); adding can cost more: followed instructions brought extra testing and exploration (2.45 to 3.92 more steps per task) (Gloaguen, Feb 2026), and an optimized deep-research prompt raised policy tokens per query about 32%, 146.0k to 193.1k, on 6 queries (Lumer, Oct 2026); context rendered as markdown costs 1.258x the tokens of plain text (Eliav, Jul 2026)
- **Performance:** improves, small: cutting saves steps: context files added 2.45 to 3.92 steps per task and raised GPT-5.2's reasoning tokens 22% on SWE-bench (Gloaguen, Feb 2026); an optimizer-written prompt added no latency (138.8 s against 159.9 s per query, 6 queries) (Lumer, Oct 2026)

## Evidence (summary)

- paper §A.4 (2026-02): 8 lines to 23 lines in Filesystem-B=178. Net-zero pass rate (6 new passes, 6 regressions) although the run had the largest crash reduction (46.1% to 30.3%).
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", https://arxiv.org/abs/2310.01798 (2023-10-03): Table 8, CommonGen-Hard concept coverage, gpt-3.5-turbo-0613: Madaan et al. reported standard 44.0 -> self-correct 67.0 (7 calls); replication 53.0 -> 61.1; adding "Write a reasonable paragraph that includes *ALL* of the above concepts"…
- Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs"… (2024-06-03): Self-Refine used wrong few-shot labels or mismatched instructions only for initial generation (Tables 9-10); detoxification studies often do not ask for harmless output initially.
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", https://arxiv.org/abs/2503.13657 (2025-03-17): Table 5, GSM-Plus (200 sampled problems, 6 repetitions): GPT-4 84.75±1.94 -> 89.75±1.44, which the authors call significant without giving a p-value; GPT-4o 84.25±1.86 -> 89.00±1.38 (Wilcoxon p=0.03 against baseline, as for the new…
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", https://arxiv.org/abs/2503.13657 (2025-03-17): Proposed tactic (App. L.2 is the example; measured forms are the ChatDev/AG2 entries above). Such tactics "often prove inconsistent".
- …and 10 more sources in `library/entries/restructure-system-prompt.yaml`.

## Caveats

Restructuring is not a reliable gain on its own: in VeRO's TerminalBench study a rewrite into three named sections scored 45% on a 20-task subset but broke as many passing tasks as it fixed on the full set (6 new passes, 6 regressions), the run that cut the prompt hardest had the best pass rate (12 new passes, 6 regressions) but also shortened tool descriptions, set the output cap to 17 KB and left 11 parser crashes in place, and on reasoning tasks (GPQA, MATH) VeRO's optimizers, including its prompt-only variant, gained little or nothing. The value depends on the model: a merge-and-rank rewrite of stacked rules helped smaller models and was neutral to negative for the strongest (Claude Sonnet 4.6 went from 0.627 to 0.560 at twenty instructions, significant only at that size), format effects were small and changed sign between models, and a hand-written version of the deep-research optimizer's rules recovered about 57% of its gain with a confidence interval that included zero. The newer studies are narrow: synthetic, verifier-checked rules on three to five models (20 trials per cell in the format study), one agent with a judge-scored reward in the optimizer study, and Python repositories with one sample per setting in the context-file study, so measure the change on your own agent.

## Related

- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:inject-runtime-context` (3.a.iii, Dynamic context injection)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)

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
