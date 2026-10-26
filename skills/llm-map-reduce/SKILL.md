---
name: llm-map-reduce
description: "AOT optimization 6.b.ii (Tier 2, Reliability): LLM map-reduce. Placeholder. Use when an agent shows: Per-chunk outputs conform to schema."
---

<!-- Generated from library/entries/llm-map-reduce.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# LLM map-reduce

> **Placeholder.** Generated from `library/entries/llm-map-reduce.yaml` (entry 6.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.b.ii |
| Earlier id | P45 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 2 (Reliability): it contains prompt injection to the item it arrives in |
| Categories | Topologies: Parallelizing |
| Change | workflow / parallelization |

## What it is

Give each piece of a large or untrusted input its own tool-less model call that sees only that piece and must answer in a fixed schema, then combine the answers in code or in a reducer that never sees the raw text. Against prompt injection it confines an attack to the item it sits in: with each product review mapped to two integers and a median, injected reviews swayed a GPT-4o shopping agent 0.0% of the time against 31.7% undefended at the same utility, but a schema too narrow for the task cut fixes on 180 curated SWE-bench Lite issues from 68.3% to 45.0%. On long input it pays when the model degrades with length and the answer needs little reasoning across chunks: prompted chunk readers on a 4B model held 72.92% on multi-hop QA at 896K tokens where the same model given the whole document fell to 31.25%, while character inference, which depends on relations spread across a dialogue, scored below the whole-input call at every chunk size. A frontier long-context model is the baseline to beat: DeepSeek-V4-Pro at maximum reasoning kept 78.91% at 896K, and whole-input Gemini 2.5 Pro beat a map-reduce whose per-document sub-agents searched only their own document 68.0 to 58.1 on 102 multi-document questions, where map-reduce won only on cost.

## When it applies

- **In the code:** Chunking, a sandboxed model per chunk with a constrained output schema, a deterministic reducer. Flag map calls that hold tools, free-text map outputs read by a privileged or tool-using reducer, and chunking applied to tasks whose answer depends on relations across chunks.
- **In traces:** Per-chunk outputs conform to schema.
- **In eval results:** Injection containment (attack success with one poisoned item); accuracy against the whole-input call at several input lengths, with cost and latency.
- **Probes:** One injected item among clean items; long inputs with the evidence placed at different positions and split across chunks.

## How (outline)

1. Start from the baseline: the whole input in one call to your current model with thinking on, at the input lengths you actually see, and for untrusted input an injection eval with one poisoned item among clean ones; record accuracy, cost and p50/p95 latency per item. Expect it to be strong: DeepSeek-V4-Pro at maximum reasoning held 78.91% on multi-hop QA at 896K tokens, whole-input Gemini 2.5 Pro beat per-document retrieval map-reduce 68.0 to 58.1, and at 7K tokens a 4B model given the whole document with thinking beat prompted chunk readers 80.47% to 72.92%.
2. Check that the task decomposes: per-item judgments (does this file hold an invoice, how does this review rate the product, how many years of experience does this resume show), extraction, filters, counts and extremes do; answers that hinge on relations across chunks do not (character inference over a dialogue scored below the whole input at every chunk size). For multi-hop questions use rounds (step 5), not one pass.
3. Split on item boundaries (one file, review, resume, email or document per call), so a poisoned item can only change its own record. For long running text, try a few chunk sizes on 5 sampled documents each and keep the best (this picked the exhaustive-search optimum in 4 of 6 settings and came within 0.04 in the others); the best sizes ran from 4K to 32K tokens across models and tasks, and a 1K-token overlap did not help.
4. Map: one isolated call per piece with no tools, the task rewritten as a per-piece subtask the reducer can combine (for the second-smallest number, ask each chunk for its two smallest), and the output schema enforced with structured outputs. For untrusted data allow only integers, floats, booleans, enums from a vetted list or short arrays of them, never free text that a later privileged or tool-using call reads; for trusted long text, short JSON findings with an explicit not-found answer. The map can run on a smaller model (1.b.i): 4B chunk readers scored as well as 9B ones.
5. Reduce in code where you can (count, filter, median, top-K), which no single tampered input can redirect; if the reducer is a model with tools, pass it only the validated schema fields. For questions that need several hops, let a lead call that never sees the document send focused queries to all chunk readers and ask follow-ups over a few rounds; prompted, this held 72.92% to 76.04% from 7K to 896K tokens, and RL training of the lead added about 10 points.
6. Measure against the baseline on the same items at each input length: accuracy, cost per item and latency (parallel chunk reading, measured on the RL-trained version on two GPUs against one, took 78.22 s against 375.32 s for the whole 896K document with thinking, but 5.33 s against 1.16 s at 7K, and a three-stage per-document retrieval pipeline took 54.8 s against 45.6 s). For injection, report attack success with a canary in one item, check that the reduce output changes only through that item's own fields, and track the per-chunk schema-violation rate.

## How to measure

- **before-after** (Tier 2): injection eval on your own items: plant a canary instruction in one item (review, file, email, document) among clean ones and compare attack success with the raw-text design; the reduce output may change only through the poisoned item's own schema fields, and no tool call may follow the canary; report utility on clean items alongside
- **experiment** (Tier 4): paired eval against the whole-input call with thinking on, at several input lengths you actually see: accuracy, cost per item, p50/p95 latency; include items whose evidence spans chunk boundaries and pick the chunk size on a few sampled documents per size before the full run; confirm with a production A/B before switching
- **monitor**: per-chunk schema-violation and not-found rates, chunks per request, reducer input size, slowest-chunk latency, cost per request; on a regularly audited sample, answers that depended on facts spread across chunks

## Expected impact

- **Quality:** mixed, large: gains on long input when the model degrades with length and evidence sits within chunks: 72.92% vs 31.25% for the whole 896K-token document on a 4B model (Li, Sep 2026); synthetic Math 0.11 to 0.55 and LongBench-v2 QA 0.31 to 0.48 for gpt-4o-mini at 128K, at a chunk size picked after the fact on test data (Xu, Jun 2025). Losses when the answer spans chunks (character inference below whole input at every chunk size; Xu, Jun 2025), against a frontier whole-input call (Gemini 2.5 Pro 68.0 vs 58.1; Akay, Mar 2026) and when the schema is too narrow for the task (180 curated SWE-bench Lite issues 68.3% to 45.0%; Jacob, Sep 2025)
- **Cost:** mixed, medium: every chunk is still read once, plus per-call instructions and a reduce call; cheaper when the map runs on a smaller model: $0.103 vs $0.273 per query with Gemini 2.5 Flash readers against whole-input Gemini 2.5 Pro (Akay, Mar 2026); repeated rounds re-read every chunk unless the KV cache is reused (Li, Sep 2026)
- **Performance:** mixed, medium: faster on long input with a parallel map: 78.22 s vs 375.32 s per question at 896K tokens against the whole document with thinking (RL-trained version on two GPUs vs one), but 5.33 s vs 1.16 s at 7K (Li, Sep 2026); a coordinator, per-document retrieval map and reduce pipeline took 54.8 s vs 45.6 s for one whole-input call (Akay, Mar 2026)
- **Security:** improves, large: per-item calls with typed outputs and a median reducer took injected-review attack success on a GPT-4o shopping agent from 31.7% to 0.0% at equal utility; typed hand-offs took calendar scheduling from 63.0% and bug fixing from 98.9% to 0.0% (Jacob, Sep 2025); a poisoned item can still set its own values (Beurer-Kellner, Jun 2025)
- **Governance:** improves, medium (unmeasured): each item's contribution is a typed record that can be validated, logged and audited
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", https://arxiv.org/abs/2506.08837 (2025-06-10): Proposed as a design pattern with "provable resistance to prompt injection"; analyzed for trade-offs and case studies, not benchmarked. Two reduce designs: one that "does not use an LLM, and simply applies operations that are robust to…
- Kun Li, Zexuan Qiu, Tianhua Zhang, Irwin King, Helen Meng (CUHK), "PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents"… (2026-09-06): HotpotQA Sub_EM, Qwen3.5-4B, 7K / 896K tokens / average: prompted PARSER (no RL) 72.92 / 72.92 / 74.42; whole document with thinking 80.47 / 31.25 / 65.82; whole document without thinking 75.78 / 34.38 / 64.36; untrained MemAgent 69.53 /…
- Yagiz Can Akay, Muhammed Yusuf Kartal, Esra Alparslan, Faruk Ortakoyluoglu, Arda Akpinar, "SPD-RAG: Sub-Agent Per Document… (2026-03-09): Avg Score (GPT-5 judge) / perfect rate / cost / latency per query: whole input 68.0 / 31.4% / $0.273 / 45.6 s; per-document retrieval map-reduce 58.1 / 18.6% / $0.103 / 54.8 s; Normal RAG 33.0 / 13.7% / $0.080 / 42.6 s; Agentic RAG 32.8 /…
- Dennis Jacob, Emad Alghamdi, Zhanhao Hu, Basel Alomair, David Wagner, "Preventing Prompt Injection with Type-Directed Privilege… (2025-09-30): Utility / attack success rate, undefended vs defended: online shopping (GPT-4o) 21.8% / 31.7% vs 22.4% / 0.0%; calendar scheduling (GPT-4o) 90.0% / 63.0% vs 91.0% / 0.0%; bug fixing (GPT-5.2, medium effort) 68.3% / 98.9% vs 45.0% / 0.0%, a…
- …and 1 more sources in `library/entries/llm-map-reduce.yaml`.

## Caveats

The injection result is one study with one fixed payload per case and no adaptive attacker; containment holds by construction only for instruction injection, a poisoned item can still lie about itself, and a free-text map output read by a privileged reducer gives the protection up. The long-input gains come from packed or synthetic benchmarks (HotpotQA paragraphs padded with distractors, synthetic number lists), from 2024 non-reasoning models in one study and 4B to 9B models in another, where beyond 262K tokens the whole-input baseline ran on a context stretched with YaRN. The one comparison against a frontier long-context model on real documents is a 102-question study whose map ran on a cheaper model, so its cost gap mixes the split with the model change; PARSER's headline 11x latency cut is against a sequential memory agent, and its 6.3-point lead over DeepSeek-V4-Pro needs RL on the lead agent and shrinks to 0.3 points out of distribution.

## Related

- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:graph-of-thought` (7.c.iv, Graph-of-Thought)
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
