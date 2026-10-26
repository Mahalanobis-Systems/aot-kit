---
name: cache-stable-prefix
description: "AOT optimization 3.b.i (Tier 1, Hygiene): Keep the prompt prefix cache-stable. Placeholder. Use when an agent shows: cache_read tokens near zero across calls that share a prefix; cache-hit rate below about 50% on multi-turn runs."
---

<!-- Generated from library/entries/cache-stable-prefix.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Keep the prompt prefix cache-stable

> **Placeholder.** Generated from `library/entries/cache-stable-prefix.yaml` (entry 3.b.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 3.b.i |
| Earlier id | T63 |
| Tier | 1 (Hygiene): a reordering that leaves what the model sees unchanged, verified on the hand-labeled set |
| Categories | Prompts: Caching |
| Change | prompt / formatting (restructure) |
| Also covers | KV-cache-friendly prompt layout |

## What it is

Put static content (identity, rules, tool definitions) before a boundary and per-turn content (date, state, memory) after it; keep the prefix bit-for-bit identical across turns; strip thinking text from persisted history; and track per-turn cache-miss cost. Check the provider's caching minimum: a prefix below it never caches.

## When it applies

- **In the code:** a timestamp, session id or per-turn state before the static block; non-deterministic serialization; a marked-for-caching prefix shorter than the provider's minimum (in one image-labeling agent, 504 tokens against Haiku 4.5's 4,096)
- **In traces:** cache_read tokens near zero across calls that share a prefix; cache-hit rate below about 50% on multi-turn runs

## How (outline)

1. Read the prompt assembly code: find timestamps, per-turn state, or non-deterministic serialization (dict order, ids) early in the prompt.
2. Move them after the static block; sort and fix serialization.
3. Confirm the static prefix exceeds the provider's minimum cacheable length.
4. Replay the hand-labeled set; compare cache-hit rate before and after.

## How to measure

- **verify-fix** (Tier 1): replay the hand-labeled set; compare cache-hit rate
- **monitor**: cache-hit rate and cache-miss cost per turn

## Expected impact

- **Quality:** none
- **Cost:** improves, large: cached input is billed at a fraction of full price; RETRACE's cache hits rose 45.6% to 90.8% as a side effect (Aug 2026)
- **Performance:** improves, small

## Evidence (summary)

- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Claude Code SYSTEM_PROMPT_DYNAMIC_BOUNDARY; the static prefix is "cached via Blake2b hashing with scope 'global'" and "achieves high cache hit rates across turns and even across sub-agents"; OpenHands CacheTier.STATIC/DYNAMIC arrived at…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "prompt prefix is bit-perfect normalized (sorted compact re-serialization of tool-call JSON, a date-only timestamp, a frozen memory snapshot) so that even local llama.cpp and vLLM KV caches hit across turns"; places four…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): OpenCode "emits six providers' cache dialects simultaneously and shapes its system prompt to at most two messages (one by default) to match the cache slots."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI "Keeps extended-thinking parts out of persisted history at response-recording time so they don't pollute future cache lookups"; cited as a mitigation for "Multi-agent systems use ~15x more tokens than chat" [17].
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Pi "audits per-turn cache-miss dollar waste as a first-class metric"; "a per-turn cache-miss dollar-waste audit that prices every avoidable cache invalidation."
- …and 3 more sources in `library/entries/cache-stable-prefix.yaml`.

## Related

- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:inject-runtime-context` (3.a.iii, Dynamic context injection)
- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:language-agent-tree-search` (7.c.v, Language Agent Tree Search (LATS))
- `aot-kit:self-discover-reasoning` (3.c.i, Self-Discover reasoning structures)
- `aot-kit:oracle-worker-escalation` (6.a.i, Oracle-worker multi-model)

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
