---
name: cache-stable-prefix
description: "AOT optimization 3.b.i (Tier 1, Hygiene): Keep the prompt prefix cache-stable. Placeholder. Use when an agent shows: cache_read tokens near zero across calls that share a prefix; cache-hit rate below about 50% on multi-turn runs; cache breaks on turns where the tool list, reasoning effort or mode changed, or after compaction; turns deep in a session that re-read most of the prompt; cache-token counts that read zero while the bill shows caching."
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

Build each agent request as a byte-identical static prefix followed by an append-only history, so every turn reads the prompt cache instead of reprocessing it. Put identity, rules and tool definitions before the cache boundary and anything that changes (date, state, memory, mode, settings) after it as appended messages; serialize deterministically; send earlier turns back verbatim, thinking blocks included where the model keeps them; check the provider's caching minimum (a prefix below it never caches); and track per-turn cache misses, since 108 of 120 fixed caching defects in ten open-source agents raised no error. Against a prefix broken on every call, caching cut cost 41-80% and time to first token 6-31% on one research benchmark, and in one inference provider's traffic a change to the tool list or reasoning effort made a cache break more than 20 times as likely. The evidence is small and covers cost and latency, not quality; caching the whole context raised latency on one model, and a cache shared across customers lets them test whether a known prompt was sent.

## When it applies

- **In the code:** a timestamp, session id or per-turn state before the static block; non-deterministic serialization (unsorted keys, random call ids, tools rebuilt in a different order or inserted mid-list); a cache marker on a block that changes every request; caching enabled by hard-coded model-name checks rather than a capability lookup; history items edited, pruned or replaced in place, or mode reminders and setting changes written into earlier messages or the system prompt; a compaction or side call with its own system prompt over a re-serialized transcript; a marked-for-caching prefix shorter than the provider's minimum (in one image-labeling agent, 504 tokens against Haiku 4.5's 4,096)
- **In traces:** cache_read tokens near zero across calls that share a prefix; cache-hit rate below about 50% on multi-turn runs; cache breaks on turns where the tool list, reasoning effort or mode changed, or after compaction; turns deep in a session that re-read most of the prompt; cache-token counts that read zero while the bill shows caching
- **Probes:** Scripted sessions that change settings and modes midway.

## How (outline)

1. Start from the baseline: log per request the cache read, cache write and uncached input tokens (on Claude: cache_read_input_tokens, cache_creation_input_tokens, input_tokens), a hash of the tools, system prompt and messages, and where the request first differs from the previous one, or the provider's cache-miss reason (Anthropic's cache diagnostics names whether the model, system prompt, tools or messages diverged). Compute the token-weighted hit rate per session and the cost of each avoidable miss, and check the meter itself: 23 of 120 fixed caching defects in ten open-source agents miscounted cache tokens.
2. Read the prompt assembly code and order content by how often it changes: tool definitions and static instructions first, then project or session content, then the growing history. Keep the system prompt byte-stable, with no timestamp, request or session id, git status or memory in it (a live timestamp there meant the cache never hit); put per-turn values after the history as an appended message that supersedes earlier ones, keep the date to the day and fixed for the session, and announce a date change with an appended note.
3. Make the bytes deterministic: rebuild each request from an append-only session log so retries and resumes are byte-identical; sort keys in tool schemas and tool-call JSON (some languages randomize key order) and avoid random per-request ids; keep the tool list sorted and identical in every mode, appending new tools at the end, since a tool inserted mid-list re-reads everything after it (to restrict tools without editing the list, see 3.b.ii); send assistant turns and tool results back verbatim. Keep thinking out of persisted history only where the provider does not expect it back (as Gemini CLI does); on Claude models that keep prior thinking (Opus 4.5 and later, Sonnet 4.6 and later, Haiku 5.5), pass thinking blocks back unmodified, because a dropped block changes the cached prefix from that point on.
4. Mark the boundary to fit the provider. Put the cache breakpoint on the last block that is identical across requests, never on the block that varies: on Claude, writes happen only at breakpoints, reads look back at most 20 blocks and up to 4 breakpoints are allowed, so add an intermediate one when a turn appends 20 or more blocks, or use automatic caching on an append-only history. Do not assume caching everything is best: in one study with a 10,000-token system prompt, caching the full context raised GPT-4o's time to first token 8.8% where caching only the stable system prompt cut it 30.9% (cost differed by 2-4 points across placements), so compare placements on your own provider and session lengths. Enable caching through a capability lookup, not model-name checks (37 of the 120 defects silently lost caching when a model was renamed or added). Confirm the static prefix clears the model's minimum (512 to 4,096 tokens across current Claude models; below it nothing caches and no error is returned). Choose the lifetime from the gap between turns: Claude's default is 5 minutes from the start of the request, refreshed on each hit, with writes at 1.25x input; 1-hour writes cost 2x and pay when turns or side agents run 5 to 60 minutes apart. Keep the model fixed within a cached conversation (caches are per model; see 1.b.i), and send one stable cache key or session id per conversation where the API routes by one.
5. Keep settings, modes and compaction from rewriting the prefix. Settle reasoning effort and thinking settings per session, or carry a change in an appended message where the API allows it: two open-model chat templates write effort at token 8, and on Claude a thinking or top-level effort change restarts the cache while a per-message effort change does not. Put mode reminders in their own appended message (a plan-mode reminder edited into and out of the user message re-read 330 to 2,340 tokens a turn) and do not prune or replace earlier history in place each turn (one replacement re-read 5,846 of 15,520 tokens). Compact late, running the summarizer on the conversation's exact prefix with the instruction appended rather than over a re-serialized transcript (22% cached in the largest such workload one provider saw). Run forks and sub-agents that share the parent's context the same way, and for parallel calls on a shared prefix send the rest after the first response starts, since a Claude cache entry exists only from then.
6. If several customers share one provider credential (a relay, gateway or shared workspace), keep their cache state apart: carry a namespace derived from the authenticated customer into every cache lookup and write, or split after a verified public prefix. Under a shared credential five of five open-source gateways exposed cross-customer cache reads; the split kept most reuse at a modeled 1.7 to 2.5% cost increase, against 2.29 to 3.14 times for full separation.
7. Measure: replay the hand-labeled set (or recorded sessions with the date fixed) before and after, plus scripted sessions that switch mode, change effort and back, connect and disconnect a tool server, add a skill, cross midnight, idle past the cache lifetime, restart and resume, spawn a sub-agent and compact; confirm outputs and task success are unchanged, and compare token-weighted cache read share, cost per task, time to first token by context depth and the first divergence position, per model and provider. In production, alert on hit-rate drops and on deep turns that re-read most of the prompt: 108 of the 120 defects raised no error.

## How to measure

- **verify-fix** (Tier 1): replay the hand-labeled set (or recorded sessions with the date fixed) before and after the change, plus scripted sessions that switch mode, change reasoning effort and switch back, connect and disconnect a tool server, add a skill, cross midnight, idle past the cache lifetime, restart and resume, spawn a sub-agent and compact; confirm outputs and task success are unchanged, and compare token-weighted cache read share, cost per task, time to first token by context depth and the first position where each request differs from the previous one, per model and provider
- **monitor**: per turn: cache read, write and uncached input tokens, the first divergence position or the provider's cache-miss reason, time to first token and the cost of each avoidable miss; alert on drops in session hit rate and on deep turns that re-read most of the prompt; reconcile reported cache tokens with the bill; where a relay serves several customers, test periodically that one customer's cached prefix is not readable from another account

## Expected impact

- **Quality:** none: the provider states the response is identical with and without caching (Anthropic docs, Nov 2026), and the caching defects studied left model output correct (Zhang, Oct 2026); no source here measures task quality, so moving instructions to suit the cache is a separate change (see 3.a.iv)
- **Cost:** improves, large: against a prefix broken on every call, caching cut agent cost 41.4-79.6% across four models and 88-89% at 50,000-token prompts on GPT-5.2 and Claude Sonnet 4.5 (Lumer, Jan 2026); RETRACE's cache hits rose 45.6% to 90.8% as a side effect (Li, Aug 2026); a gateway that rebuilt its system prompt every turn raised cost about 75% (Zhang, Oct 2026); on Claude, reads bill at 0.1x input (0.05x on Opus 5.5 and Sonnet 5.5) but 5-minute writes at 1.25x, so a prefix written and never read costs 25% more than no caching (Anthropic docs, Nov 2026)
- **Performance:** improves, medium: time to first token 6.1-30.9% better with the best cache placement per model and 60% better on GPT-4o at 50,000-token prompts, but 8.8% worse on GPT-4o when the full context was cached (Lumer, Jan 2026); deep in a session, turns that re-read most of the prompt took 5 to 41 s to a first token against 0.8 to 2.8 s for normal turns (Neuralwatt, Oct 2026)
- **Security:** degrades, small: only where customers share a cache: under a shared provider credential five of five open-source gateways exposed cross-customer cache reads and 12 of 28 high-volume model labels on one relay had a cross-account route; public agent prefixes (15 of 17 with no per-run value) let a probe confirm a known prompt, while recovering unknown text succeeded once, for 16 bits (Sun, Aug 2026); direct Claude API caches are isolated per organization and workspace (Anthropic docs, Nov 2026)
- **Governance:** none: on Claude, cache entries are held in memory only, not at rest, for their 5-minute or 1-hour lifetime and prompt caching is eligible for zero data retention (Anthropic docs, Nov 2026); other providers' terms differ; 23 of 120 fixed caching defects misreported cache tokens, so reconcile cost reports with the bill (Zhang, Oct 2026)

## Evidence (summary)

- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Claude Code SYSTEM_PROMPT_DYNAMIC_BOUNDARY; the static prefix is "cached via Blake2b hashing with scope 'global'" and "achieves high cache hit rates across turns and even across sub-agents"; OpenHands CacheTier.STATIC/DYNAMIC arrived at…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Hermes "prompt prefix is bit-perfect normalized (sorted compact re-serialization of tool-call JSON, a date-only timestamp, a frozen memory snapshot) so that even local llama.cpp and vLLM KV caches hit across turns"; places four…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): OpenCode "emits six providers' cache dialects simultaneously and shapes its system prompt to at most two messages (one by default) to match the cache slots."
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Gemini CLI "Keeps extended-thinking parts out of persisted history at response-recording time so they don't pollute future cache lookups"; cited as a mitigation for "Multi-agent systems use ~15x more tokens than chat" [17].
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Pi "audits per-turn cache-miss dollar waste as a first-class metric"; "a per-turn cache-miss dollar-waste audit that prices every avoidable cache invalidation."
- …and 8 more sources in `library/entries/cache-stable-prefix.yaml`.

## Caveats

The measured evidence is small: one controlled study on one research benchmark (40 sessions per model and cache mode, a 10,000-token system prompt that dominated the prompt), one inference provider's report on its own traffic with open models (its server-side figures mix harness edits with cache eviction), and counts of fixed defects; none measures task quality. Caching more is not always better: in that study caching only the stable system prompt gave the most consistent latency gains while caching the full context raised GPT-4o's time to first token 8.8%, and a Claude 5-minute write costs 1.25x input and expires 5 minutes after the last request that used it started, so short sessions, long gaps or low reuse can cost more than no caching. Mechanics differ and change (current Claude minimums alone span 512 to 4,096 tokens, caches are per model, effort settings are rendered into the prompt), so a layout tuned to one provider can miss on another. In one relay study a shared cache leaked membership of known prompts across customers on several production routes but yielded unknown text only once (16 bits), and its tenant-split cost is modeled, not billed.

## Related

- `aot-kit:mask-tools-not-remove` (3.b.ii, Mask tools instead of removing them)
- `aot-kit:inject-runtime-context` (3.a.iii, Dynamic context injection)
- `aot-kit:restructure-system-prompt` (3.a.iv, Restructure the system prompt: every requirement once, up front, in named sections; nothing the model doesn't need)
- `aot-kit:staged-compaction` (5.a.i, Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:few-shot-examples` (3.a.i, Add worked examples to the prompt (few-shot), or curated example queries for data agents)
- `aot-kit:ground-queries-in-schema` (5.b.i, Give the model the schema it queries, in context: descriptions, keys, codes, sample values)
- `aot-kit:semantic-layer-routing` (7.a.i, Route metric questions through a deterministic semantic layer; fall back to text-to-SQL)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
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
