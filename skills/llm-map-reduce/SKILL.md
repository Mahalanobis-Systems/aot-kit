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

Give each piece of a large or untrusted input its own tool-less model call that sees only that piece and must answer in a fixed schema, then combine the answers in code or in a reducer that never sees the raw text. Against prompt injection it confines an instruction to the item it sits in (injected reviews swayed a GPT-4o shopping agent 0.0% of the time against 31.7% undefended, and a tool-less reader let 2 of 649 known attacks through on gpt-5-mini), but not data an item forges (a quarantined reader still took 25.0% of forged-record attacks on GPT-5.2, against 49.1% undefended), and a schema too narrow for the task cut fixes on 180 curated SWE-bench Lite issues from 68.3% to 45.0%. On long input it pays when the model degrades with length and the answer needs little reasoning across chunks: prompted 4B chunk readers held 72.92% on multi-hop QA at 896K tokens where the same model given the whole document fell to 31.25%, and a lead that sends rounds of lookups to the readers beat a single map pass, which scored below a whole input truncated to 128K on LongBench v2 (32.4 vs 40.6). A frontier whole-input call is the baseline to beat: DeepSeek-V4-Pro kept 78.91% at 896K, whole-input Gemini 2.5 Pro beat per-document map-reduce 68.0 to 58.1, and small chunk readers under a Gemini 3 Pro lead only tied Gemini 3 Pro reading the whole input (71.3% vs 72.2%), at about a sixth of the cost.

## When it applies

- **In the code:** Chunking, a sandboxed model per chunk with a constrained output schema, a deterministic reducer. Flag map calls that hold tools, free-text map outputs read by a privileged or tool-using reducer, items split or counted by a model in text that holds untrusted fields, trusted fields (sender, ID, origin) taken from a map's output instead of the parsed record, a single map pass over long running text, and chunking applied to tasks whose answer depends on relations across chunks.
- **In traces:** Per-chunk outputs conform to schema.
- **In eval results:** Injection containment (attack success with one poisoned item, for an injected instruction and for a forged record or field separately); accuracy against the whole-input call at several input lengths, with cost and latency, for one pass and for lead-driven rounds.
- **Probes:** One injected item among clean items; an item whose untrusted text forges another record or a trusted field; long inputs with the evidence placed at different positions and split across chunks.

## How (outline)

1. Start from the baseline: the whole input in one call to your current model with thinking on, at the input lengths you actually see, and for untrusted input an injection eval with one poisoned item among clean ones; record accuracy, cost and p50/p95 latency per item. Expect it to be strong: DeepSeek-V4-Pro at maximum reasoning held 78.91% on multi-hop QA at 896K tokens, whole-input Gemini 2.5 Pro beat per-document retrieval map-reduce 68.0 to 58.1, whole-input Gemini 3 Pro scored 72.2% on LongBench v2's Long subset (over 128K), and at 7K tokens a 4B model given the whole document with thinking beat prompted chunk readers 80.47% to 72.92%. Current models already resist most fixed instruction payloads on their own (GPT-5.2 let 0.2% of AgentDojo's through undefended, gpt-5-mini 2.83% of 22,899 known-successful LLMail-Inject payloads), so also plant data injection (an item that forges a record or a field) and, where you can, an attacker that adapts to your design.
2. Check that the task decomposes: per-item judgments (does this file hold an invoice, how does this review rate the product, how many years of experience does this resume show), extraction, filters, counts and extremes do; answers that hinge on relations across chunks do not (character inference over a dialogue scored below the whole input at every chunk size). For multi-hop questions and questions over long running text use rounds (step 5), not one pass: a single map pass with one aggregation step scored below a whole-input call truncated to 128K on real long documents (Qwen3-14B 32.4 vs 40.6 on LongBench v2, 48.77 vs 63.34 on InfiniteBench).
3. Split on item boundaries (one file, review, resume, email, record or document per call), so a poisoned item can only change its own record, and do the split and the item count in code from the source's own structure (API records, files, rows), never by asking a model to find or count records in text that holds untrusted fields: a fake object planted in one untrusted JSON field made six current models (GPT-5.2, Claude Opus 4.5 and Gemini 3 Pro among them) return the attacker's value 31.3% to 43.3% of the time, and with randomized field names, fake list entries were what still got through when an agent totaled a list. Take trusted fields (sender, author, ID, URL, origin) from the parsed record in code, not from a map's output; if a call must read structured data, suffix field names with a random nonce and tell the model to trust only those (this cut the attack to 0.0% to 3.0%). For long running text, try a few chunk sizes on 5 sampled documents each and keep the best (this picked the exhaustive-search optimum in 4 of 6 settings and came within 0.04 in the others); the best sizes ran from 4K to 32K tokens across models and tasks, and a 1K-token overlap did not help.
4. Map: one isolated call per piece with no tools, the task rewritten as a per-piece subtask the reducer can combine (for the second-smallest number, ask each chunk for its two smallest), and the output schema enforced with structured outputs. For untrusted data allow only integers, floats, booleans, enums from a vetted list or short arrays of them, never free text that a later privileged or tool-using call reads: on gpt-5-mini a reader without tools let 2 of 649 attacks through and the reader plus a JSON hand-off none, while the same JSON schema on the single acting agent let 92 through, and injected text still reached 63.7% of the reader's free-text summary fields. For trusted long text, short JSON findings with an explicit not-found answer. When items are trusted and each needs its own analysis, the map can be one agent per item with its own tools that writes a fixed structured report (findings, quantitative evidence, interpretation, references, caveats) into a store, with synthesis over the stored reports: one agent per perturbation was preferred in 45 of 60 blinded expert judgments over one agent given all of them (not compute-matched). The map can run on a smaller model (1.b.i): 4B chunk readers scored as well as 9B ones, and 4B to 14B readers added 2.9 points where a larger lead added 11.1.
5. Reduce in code where you can (count, filter, median, top-K), which no single tampered input can redirect; if the reducer is a model with tools, pass it only the validated schema fields. For questions that need several hops or span long running text, let a lead call that never sees the document send focused, atomic lookups (one entity or term each) to all chunk readers and ask follow-ups over a few rounds; prompted, this held 72.92% to 76.04% from 7K to 896K tokens, RL training of the lead added about 10 points, and with Gemini 3 Pro as the lead and 4B readers on 4,096-token chunks it scored 71.3% against 72.2% for Gemini 3 Pro on the whole input, at $20.4 against $126.7 for the evaluation set. Before adding sub-calls to a lead that holds the input in a REPL, try the same lead searching and slicing it in code without them (5.c.ii): with GPT-5, sub-model calls scored 59.5 against 65.2 on CodeQA and 86.0 against 89.7 on BrowseComp+ (but 53.0 against 50.5 on OOLONG), and within the model's window the recursive version often scored below the whole-input call.
6. Measure against the baseline on the same items at each input length: accuracy, cost per item and latency (parallel chunk reading, measured on the RL-trained version on two GPUs against one, took 78.22 s against 375.32 s for the whole 896K document with thinking, but 5.33 s against 1.16 s at 7K, and a three-stage per-document retrieval pipeline took 54.8 s against 45.6 s). For injection, report attack success with a canary in one item and, separately, with a forged record or field; check that the reduce output changes only through that item's own fields and that the item count and trusted fields match the source, and track the per-chunk schema-violation rate.

## How to measure

- **before-after** (Tier 2): injection eval on your own items: plant a canary instruction in one item (review, file, email, document) among clean ones, and separately a forged record or field inside one item's untrusted text (another sender or ID, an extra list entry), and compare attack success with the raw-text design; the reduce output may change only through the poisoned item's own schema fields, the item count and trusted fields must match the source, and no tool call may follow the canary; report utility on clean items alongside, and where possible add an attacker that adapts to the split
- **experiment** (Tier 4): paired eval against the whole-input call with thinking on, at several input lengths you actually see: accuracy, cost per item, p50/p95 latency; run one map pass and lead-driven rounds, and for a lead that holds the input in a REPL, the same lead with and without sub-calls; include items whose evidence spans chunk boundaries and pick the chunk size on a few sampled documents per size before the full run; confirm with a production A/B before switching
- **monitor**: per-chunk schema-violation and not-found rates, chunks per request, items per request against the source's record count, reducer input size, rounds per question, slowest-chunk latency, cost per request; on a regularly audited sample, answers that depended on facts spread across chunks

## Expected impact

- **Quality:** mixed, large: gains on long input when the model degrades with length and evidence sits within chunks: 72.92% vs 31.25% for the whole 896K-token document on a 4B model (Li, Sep 2026); synthetic Math 0.11 to 0.55 and LongBench-v2 QA 0.31 to 0.48 for gpt-4o-mini at 128K, at a chunk size picked after the fact on test data (Xu, Jun 2025); lead-driven rounds of lookups 48.7 vs 38.9 against a 128K-truncated whole input on LongBench v2 Long for Qwen3-14B, and 71.3 vs 72.2 against whole-input Gemini 3 Pro (Chen, Sep 2026); per-item agents preferred in 45 of 60 blinded expert judgments over one agent with all items, not compute-matched (Sun, Oct 2026). Losses when the answer spans chunks (character inference below whole input at every chunk size; Xu, Jun 2025), with a single map pass (32.4 vs 40.6 against a truncated whole input; Chen, Sep 2026), against a frontier whole-input call (Gemini 2.5 Pro 68.0 vs 58.1; Akay, Mar 2026), with sub-calls under a strong lead (GPT-5 CodeQA 59.5 vs 65.2 without them; Alizadeh, Mar 2026) and when the schema is too narrow for the task (180 curated SWE-bench Lite issues 68.3% to 45.0%; Jacob, Sep 2025)
- **Cost:** mixed, large: every chunk is still read once, plus per-call instructions, a reduce call and any rounds; cheaper when the map runs on a smaller model: $20.4 vs $126.7 on LongBench v2 Long for 4B readers under a Gemini 3 Pro lead against whole-input Gemini 3 Pro (Chen, Sep 2026), $0.103 vs $0.273 per query with Gemini 2.5 Flash readers against whole-input Gemini 2.5 Pro (Akay, Mar 2026); repeated rounds re-read every chunk unless the KV cache is reused (Li, Sep 2026)
- **Performance:** mixed, medium: faster on long input with a parallel map: 78.22 s vs 375.32 s per question at 896K tokens against the whole document with thinking (RL-trained version on two GPUs vs one), but 5.33 s vs 1.16 s at 7K (Li, Sep 2026); a coordinator, per-document retrieval map and reduce pipeline took 54.8 s vs 45.6 s for one whole-input call (Akay, Mar 2026); on a fixed 8-GPU budget a lead-driven chunked version stayed near flat from 256K to 1M tokens while one-pass and sequential chunk agents grew linearly, shown only in a figure and not against the whole-input call (Chen, Sep 2026)
- **Security:** improves, large: per-item calls with typed outputs and a median reducer took injected-review attack success on a GPT-4o shopping agent from 31.7% to 0.0% at equal utility; typed hand-offs took calendar scheduling from 63.0% and bug fixing from 98.9% to 0.0% (Jacob, Sep 2025); a tool-less reader cut 649 known-successful LLMail-Inject attacks on gpt-5-mini to 2, and with a JSON hand-off to 0, against 92 for the JSON schema alone (Cheng, Mar 2026); it does not stop data an item forges: a quarantined reader still let 25.0% of forged-record attacks through on GPT-5.2, against 49.1% undefended, while fixed instruction payloads succeeded 0.2% of the time undefended (Choi, Jul 2026), and a poisoned item can still set its own values (Beurer-Kellner, Jun 2025)
- **Governance:** improves, medium (unmeasured): each item's contribution is a typed record that can be validated, logged and audited
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", https://arxiv.org/abs/2506.08837 (2025-06-10): Proposed as a design pattern with "provable resistance to prompt injection"; analyzed for trade-offs and case studies, not benchmarked. Two reduce designs: one that "does not use an LLM, and simply applies operations that are robust to…
- Kun Li, Zexuan Qiu, Tianhua Zhang, Irwin King, Helen Meng (CUHK), "PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents"… (2026-09-06): HotpotQA Sub_EM, Qwen3.5-4B, 7K / 896K tokens / average: prompted PARSER (no RL) 72.92 / 72.92 / 74.42; whole document with thinking 80.47 / 31.25 / 65.82; whole document without thinking 75.78 / 34.38 / 64.36; untrained MemAgent 69.53 /…
- Yagiz Can Akay, Muhammed Yusuf Kartal, Esra Alparslan, Faruk Ortakoyluoglu, Arda Akpinar, "SPD-RAG: Sub-Agent Per Document… (2026-03-09): Avg Score (GPT-5 judge) / perfect rate / cost / latency per query: whole input 68.0 / 31.4% / $0.273 / 45.6 s; per-document retrieval map-reduce 58.1 / 18.6% / $0.103 / 54.8 s; Normal RAG 33.0 / 13.7% / $0.080 / 42.6 s; Agentic RAG 32.8 /…
- Dennis Jacob, Emad Alghamdi, Zhanhao Hu, Basel Alomair, David Wagner, "Preventing Prompt Injection with Type-Directed Privilege… (2025-09-30): Utility / attack success rate, undefended vs defended: online shopping (GPT-4o) 21.8% / 31.7% vs 22.4% / 0.0%; calendar scheduling (GPT-4o) 90.0% / 63.0% vs 91.0% / 0.0%; bug fixing (GPT-5.2, medium effort) 68.3% / 98.9% vs 45.0% / 0.0%, a…
- …and 6 more sources in `library/entries/llm-map-reduce.yaml`.

## Caveats

The injection evidence is three studies with fixed payloads and no attacker adapting to the split (one payload per case in one, 649 replayed attacks on one model without utility in another), and the third shows the split does not stop data an item forges (a fake record or field got through a quarantined reader 25.0% of the time on GPT-5.2, where fixed instruction payloads already failed almost always undefended); containment holds by construction only for instruction injection, and a free-text map output read by a privileged reducer gives the protection up. The long-input gains come mostly from packed or synthetic benchmarks and 4B to 14B models, often with an RL-trained lead, where the open-model whole-input baselines ran on contexts stretched with YaRN or truncated to 128K; the two comparisons against a frontier long-context model on real documents are a 102-question study whose map ran on a cheaper model (map-reduce lost 58.1 to 68.0) and one LongBench v2 run in which a Gemini 3 Pro lead tied its own whole-input call (thinking level and run count not stated), both by the method's authors, so their cost gaps mix the split with a model change. A single map pass lost to a truncated whole-input call on real long documents, and with GPT-5 as the lead, sub-calls lowered accuracy on two of three tasks against the same harness without them; PARSER's headline 11x latency cut is against a sequential memory agent, and its 6.3-point lead over DeepSeek-V4-Pro needs RL on the lead agent and shrinks to 0.3 points out of distribution. The per-item agent study behind structured reports per item is not compute-matched and was run with the model's vendor, and governance is unmeasured.

## Related

- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:code-then-execute` (6.c.i, Code-then-execute (CaMeL))
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:choose-retriever` (8.a.i, Choose the retriever by corpus size and question type)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
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
