---
name: isolated-subagent-context
description: "AOT optimization 5.c.ii (Tier 4, Restructuring): Sub-agent architectures with clean contexts. Placeholder. Use when an agent shows: Sub-agent spans: tokens consumed inside vs returned; the parent's peak context and input per call; empty or failed returns the parent builds on; delegations on tasks the parent could do alone; facts present in the sub-agent transcript but missing from the parent's answer (hand-off breakdowns, usually silent); share of the corpus read."
---

<!-- Generated from library/entries/isolated-subagent-context.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Sub-agent architectures with clean contexts

> **Placeholder.** Generated from `library/entries/isolated-subagent-context.yaml` (entry 5.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 5.c.ii |
| Earlier id | P20 (Long-Horizon, from the master cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds sub-agents with their own contexts |
| Categories | Context: Isolating subtasks |
| Change | tool / subagent |
| Also covers | Sub-agent spawning with isolated context |

## What it is

Hand a context-heavy side task (code search, reading many files, documents or logs) to a sub-agent with a fresh context and only the tools it needs, and have it return a short result or file references so the parent's context stays small. It pays when the parent would otherwise read or carry far more than it can hold: on legal data rooms of up to 80M tokens, delegating bounded reading raised rubric pass rate from 23.3% to 62.4% across seven models, and in a robot-manipulation harness, keeping each subgoal's history in a sub-agent cut mean input per model call 4.2 times and cost 2.4 times (success 45.0% against 40.8%). It is not a default win: on bounded repository questions, delegated exploration scored 46.2% against 65.2% for an indexed single agent, with 41.8% of its failures at the hand-off; on 166 tool-heavy work tasks, sub-agents raised cost for nearly every model and cost both closed models more tasks than they gained (GPT-5.6 Sol lost 45 and gained 9), mostly through failed or unverified sub-agent results; and on long-horizon coding, the same agent closing its own subtasks and keeping only their results matched recursive delegation at 73.7% lower cost.

## When it applies

- **In the code:** A sub-agent call with a fresh context, a scoped tool list and a summary or file-reference return; or a single agent that reads large search results, file sets, documents or logs into its own context. Warning signs: generic sub-agent roles, sub-agents that inherit the full history or can delegate further, prompts that push delegation for every task or force a planning sub-agent first, a parent that paraphrases sub-agent output or never checks whether a sub-agent finished.
- **In traces:** Sub-agent spans: tokens consumed inside vs returned; the parent's peak context and input per call; empty or failed returns the parent builds on; delegations on tasks the parent could do alone; facts present in the sub-agent transcript but missing from the parent's answer (hand-off breakdowns, usually silent); share of the corpus read.
- **In eval results:** Single agent vs delegation, per model (and vs an indexed retriever, or the same agent keeping only finished subtasks' results), on search-heavy tasks: success, cost per correct answer.
- **Judge:** Summary fidelity against the sub-agent's full transcript: facts found but not returned, claims returned but not supported.
- **Probes:** Broad search then synthesis.

## How (outline)

1. Start from the single agent: run it on your tasks and log peak context, input per call, tokens per task and which tool outputs fill the window. Try the cheaper fixes first: if the material is a corpus you can index, a retriever (see 8.a.i), since indexed retrieval beat delegated exploration on bounded repository questions; if the window fills with the details of finished subtasks, have the same agent close each subtask and keep only its result (see 5.a.i), which matched recursive sub-agent delegation on long-horizon coding at 73.7% lower cost; on inputs that fit in context (about 100K tokens), a minimal agent working with files and a shell (mini-swe-agent) scored higher than a recursive sub-call harness for four of five models, at lower cost for all five.
2. Delegate only side tasks whose raw output is large and not needed again (codebase search, reading many files, documents or logs) and whose result fits a short contract; keep work whose steps share a lot of context in the parent. Tell the parent when not to delegate as well as when to, and do not push delegation for every task: in one benchmark a current model delegated on 93.5% of the tasks that needed no sub-agent, unnecessary delegation added overhead without gains in 124 cases, and forcing a planning sub-agent first led to delegation on 61.0% of the tasks that needed none.
3. Define each sub-agent as a task-specific role with an input-output contract: the objective, the inputs it gets, an output schema (findings with file paths, line ranges or document ids, what it did not cover, and whether it finished) and a length cap; avoid generic roles (planner, explorer, coder) and lifecycle roles (requirements, design, code generation), which scored below task- or domain-specific ones in two studies.
4. Start it with a fresh context and a self-contained brief, not the parent's routing messages or whole history, and give it only the tools it needs: read-only search and read tools for exploration, no delegation tool (depth 1), and a turn cap; when every subtask could be delegated recursively, child agents made 75.5% of 32,650 model requests on long-horizon coding.
5. Protect the hand-off: have it write long outputs to files and return references (see 6.b.iii), have the parent forward or quote its findings instead of paraphrasing them, require it to list every policy- or risk-relevant fact it found, and have the parent check each result's status and coverage before building on it, then retry or take over a failed delegation: failed or unverified sub-agent results caused 33 of GPT-5.6 Sol's 45 and 14 of Claude Sonnet 5's 22 tasks lost to delegation in one benchmark.
6. Measure with a paired eval of the single agent against the delegating one on the same tasks, per model (in one benchmark both closed models lost tasks while two open models gained 10.2 points): success, cost per correct answer, total and parent tokens, the parent's peak context and input per call, latency, and how often it delegates on tasks that need no sub-agent; then label failures where the sub-agent's transcript holds a fact that the parent's answer lacks, or where the parent built on a failed sub-agent result.

## How to measure

- **experiment** (Tier 4): Paired eval on the same tasks, per model: the single agent against the same agent with a delegated sub-agent, and against the cheaper alternatives where they apply (an indexed retriever, the same agent keeping only the results of finished subtasks): success, cost per correct answer, total tokens, the parent's peak context and input per call, and latency; code each failure by mechanism, including hand-off breakdowns where the sub-agent found the answer and the parent lost or misreported it, and parents that built on a failed sub-agent result.
- **monitor**: Per sub-agent call: tokens consumed inside against tokens returned, empty or failed returns and whether the parent used them, sub-agent count against task size, delegations on tasks the parent could do alone, and the share of the corpus read; on a sample, have a judge check whether the facts in the sub-agent's transcript reach the parent's answer (fact attenuation).

## Expected impact

- **Quality:** mixed, large: Large corpora: +39.1 points rubric pass rate on legal data rooms (Grupen, Sep 2026); folding sub-tasks out of context 0.567 vs 0.540 for a 327K-context agent with the same RL on BrowseComp-Plus, at a 10x smaller active context (Sun, Oct 2025); sub-calls lifted GPT-5 on OOLONG 36.0 to 56.0 but cut Qwen3-Coder on CodeQA 66.0 to 56.0 (Zhang, Dec 2025); robot manipulation 45.0% vs 40.8% for one agent (Lee, Oct 2026). Bounded tasks: 46.2% vs 65.2% for an indexed single agent (Oskooei, Aug 2026); on about 100K-token inputs an RLM harness 53.5% vs 68.0% for a minimal file-and-shell agent and 60.0% for direct inference with GPT-5.6 Sol (Pham, Sep 2026); on 166 tool-heavy tasks GPT-5.6 Sol gained 9 and lost 45 tasks, Claude Sonnet 5 gained 15 and lost 22, two open models +10.2 points (Ding, Oct 2026); recursive delegation 42.4% vs 38.1% for compaction on long-horizon coding, 42.6% for the same agent scoping its own subtasks (Xiang, Oct 2026); task-specific sub-agents +5.91 and +4.46 points, generic ones lower (Hu, Sep 2026); medal rate 45.2% vs 55.7%, CIs overlapping (Brilliantov, Sep 2026); depth 2 cost 19 points (Grupen, Sep 2026)
- **Cost:** mixed, large: More total tokens (Piriyakulkij, Sep 2026): 2.3x cost per correct answer for delegated search (Oskooei, Aug 2026); +$0.1 to +$4.2 per task for nearly every model on tool-heavy work (Ding, Oct 2026); recursive delegation $1,749.73 vs $681.22 for compaction and $460.77 for in-agent subtask scoping on 98 milestones (Xiang, Oct 2026); RLM $4.30 vs $0.816 per instance for a minimal file-and-shell agent with GPT-5.6 Sol (Pham, Sep 2026); cost up for six of seven models in a delegating harness (Grupen, Sep 2026). Cost down where the parent would otherwise carry the whole history: $0.511 vs $1.221 per robot episode at 4.2x less input per call (Lee, Oct 2026); Opus 5 from ~$18 to ~$7 per data room (Grupen, Sep 2026); single-agent tokens grew with distractor domains while sub-agent setups stayed flat (Fu-Hinthorn, Jun 2025)
- **Performance:** mixed, small: Each fresh sub-agent must gather its own context; median latency was lower with delegation for two models and higher for two (Oskooei, Aug 2026); RL rollouts slowed from 48 to 74 minutes per step as the trained root sent more sub-agents (Grupen, Sep 2026). Parallel speedups belong to 6.b.iii
- **Security:** mixed, medium (unmeasured): Depends on tool scoping (see 10.a.i).
- **Governance:** degrades, small: Policy-relevant facts a sub-agent found often never reached the agent that had to act on them: 22 of 26 for a 32B model and 1 of 18 for gpt-4.1-mini, against none in a single loop, causing both under- and over-escalation (Li, Aug 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval"
- Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (Anthropic), "Effective context engineering for AI agents"… (2025-09-29): "specialized sub-agents can handle focused tasks with clean context windows"; each "might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000…
- Amirkia Rafiei Oskooei, Bora Ilci, Alperen Kayim, Mehmet Egemen Uzun, Berat Can, Kaan Emre Kara, Ozan Orhan, Mehmet S. Aktas, "Deep Agentic… (2026-08-02): "Semantic search answered 65.2% of questions correctly against 46.2% for deep agentic search"; pass-rate gap 5.6 (Gemini 2.5 Flash), 10.0 (Gemini 2.5 Pro), 10.6 (Qwen3-235B) and 49.6 (Gemini 3 Flash) points, all significant after FDR…
- Bowen Li, Guojun Wang, "Governance at the Boundary: How Agent Decomposition Degrades Policy Compliance", https://arxiv.org/abs/2608.16055 (2026-08-17): Fact attenuation at constraint distance 2, conditional on discovery: Qwen2.5-32B 0/16 (0%) single loop, 9/16 (56%) pipeline, 22/26 (85%) orchestrator-subagent; gpt-4.1-mini 0/27 (0%), 1/30 (3%), 1/18 (6%). The orchestrator-subagent arm…
- …and 11 more sources in `library/entries/isolated-subagent-context.yaml`.

## Caveats

The large gains come from very large corpora (data rooms, multi-million-token inputs) and from setups that also change other things (a REPL holding the corpus, RL training), so they do not isolate the sub-agent; on bounded tasks with a strong single agent the gain vanished or reversed (repository questions, MLE-bench, generic roles on ProgramBench, about 100K-token reasoning inputs), and on 166 tool-heavy work tasks both closed models (GPT-5.6 Sol, Claude Sonnet 5) lost more tasks with sub-agents than they gained while some open models gained. The hand-off is the new failure point: it caused 41.8% of delegated-search failures, usually with a confident wrong answer; failed or unverified sub-agent results caused most of the tasks GPT-5.6 Sol and Claude Sonnet 5 lost to delegation; and a 32B model lost 85% of discovered facts across an orchestrator-subagent boundary, against 3-6% for gpt-4.1-mini. Delegation can buy quality at a high price: recursive delegation beat compaction on long-horizon coding (42.4% against 38.1%) at $1,749.73 against $681.22, and the same agent closing its own subtasks matched it at $460.77. Several studies are small, single-run or by the method's authors (one run per repository over 98 milestones, a 4-point success gap over 120 robot episodes without a test, 14 data rooms for the depth test, 16-30 facts per cell), and Harvey's hold-out sets are unreleased.

## Related

- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)
- `aot-kit:llm-map-reduce` (6.b.ii, LLM map-reduce)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:no-self-written-tests` (9.c.i, Drop ad-hoc test-writing prompts; tell test-heavy models not to write tests)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:continuous-task-loop` (7.d.i, Continuous autonomous task loop)
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
