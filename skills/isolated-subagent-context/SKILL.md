---
name: isolated-subagent-context
description: "AOT optimization 5.c.ii (Tier 4, Restructuring): Sub-agent architectures with clean contexts. Placeholder. Use when an agent shows: Sub-agent spans: tokens consumed inside vs returned; the parent's peak context; empty returns; facts present in the sub-agent transcript but missing from the parent's answer (hand-off breakdowns, usually silent); share of the corpus read."
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

Hand a context-heavy side task (code search, reading many files, documents or logs) to a sub-agent that starts with a fresh context and only the tools it needs, and have it return a short result or file references so the parent's context stays small. It pays when the parent would otherwise read far more than it can hold: on legal data rooms of up to 80M tokens, delegating bounded reading raised rubric pass rate from 23.3% to 62.4% across seven models. It is not a default win: on bounded repository questions, delegated exploration scored 46.2% against 65.2% for an indexed single agent at 2.3 times the cost per correct answer, with 41.8% of its failures at the hand-off, mostly silent; generic sub-agent roles and a second level of delegation also lost quality.

## When it applies

- **In the code:** A sub-agent call with a fresh context, a scoped tool list and a summary or file-reference return; or a single agent that reads large search results, file sets, documents or logs into its own context. Warning signs: generic lifecycle sub-agents, sub-agents that inherit the full history or can delegate further, a parent that paraphrases sub-agent output.
- **In traces:** Sub-agent spans: tokens consumed inside vs returned; the parent's peak context; empty returns; facts present in the sub-agent transcript but missing from the parent's answer (hand-off breakdowns, usually silent); share of the corpus read.
- **In eval results:** Single agent vs delegation (and vs an indexed retriever) on search-heavy tasks: success, cost per correct answer.
- **Judge:** Summary fidelity against the sub-agent's full transcript: facts found but not returned, claims returned but not supported.
- **Probes:** Broad search then synthesis.

## How (outline)

1. Start from the single agent: run it on your tasks and log peak context, tokens per task and which tool outputs fill the window; if the material is a corpus you can index, try a retriever before delegating (see 8.a.i), since indexed retrieval beat delegated exploration on bounded repository questions.
2. Delegate only side tasks whose raw output is large and not needed again (codebase search, reading many files, documents or logs) and whose result fits a short contract; keep work whose steps share a lot of context in the parent.
3. Define each sub-agent as a task-specific role with an input-output contract: the objective, the inputs it gets, an output schema (findings with file paths, line ranges or document ids, plus what it did not cover) and a length cap; avoid generic lifecycle roles such as requirements, design or code generation.
4. Start it with a fresh context and a self-contained brief, not the parent's routing messages or whole history, and give it only the tools it needs: read-only search and read tools for exploration, no delegation tool (depth 1), and a turn cap.
5. Protect the hand-off: have it write long outputs to files and return references (see 6.b.iii), have the parent forward or quote its findings instead of paraphrasing them, and require it to list every policy- or risk-relevant fact it found.
6. Measure with a paired eval of the single agent against the delegating one on the same tasks and models: success, cost per correct answer, total and parent tokens, the parent's peak context and latency; then label failures where the sub-agent's transcript holds a fact that the parent's answer lacks.

## How to measure

- **experiment** (Tier 4): Paired eval on the same tasks and models: the single agent against the same agent with a delegated sub-agent (and against an indexed retriever where the corpus allows): success, cost per correct answer, total tokens, the parent's peak context and latency; code each failure by mechanism, including hand-off breakdowns where the sub-agent found the answer and the parent lost or misreported it.
- **monitor**: Per sub-agent call: tokens consumed inside against tokens returned, empty returns, sub-agent count against task size and the share of the corpus read; on a sample, have a judge check whether the facts in the sub-agent's transcript reach the parent's answer (fact attenuation).

## Expected impact

- **Quality:** mixed, large: Large corpora: +39.1 points rubric pass rate on legal data rooms (Grupen, Sep 2026); folding sub-tasks out of context 0.567 vs 0.540 for a 327K-context agent with the same RL on BrowseComp-Plus, at a 10x smaller active context (Sun, Oct 2025); sub-calls lifted GPT-5 on OOLONG 36.0 to 56.0 but cut Qwen3-Coder on CodeQA 66.0 to 56.0 (Zhang, Dec 2025). Bounded tasks: 46.2% vs 65.2% for an indexed single agent (Oskooei, Aug 2026); task-specific sub-agents +5.91 and +4.46 points, generic ones lower (Hu, Sep 2026); medal rate 45.2% vs 55.7%, CIs overlapping (Brilliantov, Sep 2026); depth 2 cost 19 points (Grupen, Sep 2026)
- **Cost:** mixed, large: More total tokens (Piriyakulkij, Sep 2026): 2.3x cost per correct answer for delegated search (Oskooei, Aug 2026), cost up for six of seven models in a delegating harness while Opus 5 fell from ~$18 to ~$7 per data room (Grupen, Sep 2026); single-agent tokens grew with distractor domains while sub-agent setups stayed flat (Fu-Hinthorn, Jun 2025)
- **Performance:** mixed, small: Each fresh sub-agent must gather its own context; median latency was lower with delegation for two models and higher for two (Oskooei, Aug 2026); RL rollouts slowed from 48 to 74 minutes per step as the trained root sent more sub-agents (Grupen, Sep 2026). Parallel speedups belong to 6.b.iii
- **Security:** mixed, medium (unmeasured): Depends on tool scoping (see 5.c.ii).
- **Governance:** degrades, small (unmeasured): Nested traces.
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford (Anthropic), "How we built our multi-agent research… (2025-06-13): "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval"
- Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (Anthropic), "Effective context engineering for AI agents"… (2025-09-29): "specialized sub-agents can handle focused tasks with clean context windows"; each "might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000…
- Amirkia Rafiei Oskooei, Bora Ilci, Alperen Kayim, Mehmet Egemen Uzun, Berat Can, Kaan Emre Kara, Ozan Orhan, Mehmet S. Aktas, "Deep Agentic… (2026-08-02): "Semantic search answered 65.2% of questions correctly against 46.2% for deep agentic search"; pass-rate gap 5.6 (Gemini 2.5 Flash), 10.0 (Gemini 2.5 Pro), 10.6 (Qwen3-235B) and 49.6 (Gemini 3 Flash) points, all significant after FDR…
- Bowen Li, Guojun Wang, "Governance at the Boundary: How Agent Decomposition Degrades Policy Compliance", https://arxiv.org/abs/2608.16055 (2026-08-17): Fact attenuation at constraint distance 2, conditional on discovery: Qwen2.5-32B 0/16 (0%) single loop, 9/16 (56%) pipeline, 22/26 (85%) orchestrator-subagent; gpt-4.1-mini 0/27 (0%), 1/30 (3%), 1/18 (6%). The orchestrator-subagent arm…
- …and 7 more sources in `library/entries/isolated-subagent-context.yaml`.

## Caveats

The large gains come from very large corpora (data rooms, multi-million-token inputs) and from setups that also change other things (a REPL holding the corpus, RL training), so they do not isolate the sub-agent; on bounded tasks with a strong single agent the gain vanished or reversed (repository questions, MLE-bench, generic roles on ProgramBench). The hand-off is the new failure point: it caused 41.8% of delegated-search failures, usually with a confident wrong answer, and a 32B model lost 85% of discovered facts across an orchestrator-subagent boundary, against 3-6% for gpt-4.1-mini. Several studies are small or chart-only (14 data rooms for the depth test, 16-30 facts per cell, SkillsBench accuracies in figures), and Harvey's hold-out sets are unreleased.

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
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)

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
