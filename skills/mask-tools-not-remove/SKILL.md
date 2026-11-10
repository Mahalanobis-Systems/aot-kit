---
name: mask-tools-not-remove
description: "AOT optimization 3.b.ii (Tier 3, Tuning): Mask tools instead of removing them. Placeholder. Use when an agent shows: A different tools-array hash between turns of one session, followed by cache reads near zero (provider cache diagnostics name the tools as the point of divergence); on Claude, tool_choice changing between turns, thread_fingerprint_mismatch errors when it changes inside a message thread, and on recent models (every account on Claude Fable 5.2) 400 errors saying a thinking block is bound to a different conversation, or dropped thinking blocks, after a tool edit; calls to tools no longer defined or not allowed, rejected or executed."
---

<!-- Generated from library/entries/mask-tools-not-remove.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Mask tools instead of removing them

> **Placeholder.** Generated from `library/entries/mask-tools-not-remove.yaml` (entry 3.b.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 3.b.ii |
| Earlier id | P23 (Production, from the master cookbook) |
| Tier (proposed) | 3 (Tuning): it changes which tools the model can choose |
| Categories | Prompts: Caching; Tools: Avoiding misuse |
| Change | tool / api |

## What it is

Keep every tool defined for the whole session and change only which ones the agent may call. When availability changes by mode, phase or permission, declare every tool once, keep the definitions byte-stable, and restrict the choice another way: OpenAI's allowed_tools or tool_choice "none", Anthropic's appended tool_removal and tool_addition blocks (inside a Claude message thread, tools and tool_choice cannot change at all), a grammar or logit mask on self-hosted models, and a harness check that rejects calls outside the allowed set. It pays in long sessions, because an edited tool list re-reads the whole cached conversation and, on Claude Fable 5.2, makes replayed thinking blocks fail on every account; caching cut agent cost 41-80% against a prefix broken on every call, and in one small coding study a visible-but-disallowed interface behind the same check ran no forbidden actions, as removal did. No study measures masking against removal on cost within a session, and visibility has measured costs: one unneeded tool cut answer rates from 98.2% to 63.5%, and on single requests over about 450 tools, pruning to 10 per request cost about the same as a cached full list while scoring higher (0.840 against 0.787).

## When it applies

- **In the code:** Tool list rebuilt per turn from mode, phase, permissions or connected servers (a tools array filtered by state, or prompt text that co-varies with the active toolset); no allowed-tools or tool_choice restriction, appended tool_removal or tool_addition blocks, decode-time mask, or harness check of each call against the allowed set; an MCP connector server whose tool list is not pinned; on Claude, every declared tool deferred; on self-hosted models, a grammar or mask rebuilt per request from the allowed subset.
- **In traces:** A different tools-array hash between turns of one session, followed by cache reads near zero (provider cache diagnostics name the tools as the point of divergence); on Claude, tool_choice changing between turns, thread_fingerprint_mismatch errors when it changes inside a message thread, and on recent models (every account on Claude Fable 5.2) 400 errors saying a thinking block is bound to a different conversation, or dropped thinking blocks, after a tool edit; calls to tools no longer defined or not allowed, rejected or executed.
- **In eval results:** Cache hit rate; invalid tool call rate; blocked and executed calls to disallowed tools.
- **Probes:** Sessions where a tool becomes unavailable midway.

## How (outline)

1. Start from the baseline: find where the harness rebuilds the tool list per turn (by mode, phase, permission or connected MCP servers) and log a hash of the tools array on every request with the cache read and write tokens, so each mid-session change and the cache miss after it is visible.
2. Declare the full tool set once at session start, in a fixed order with deterministic serialization, and give tools that switch on and off together a shared name prefix (browser_, shell_) so a group can be allowed or blocked as one. Add tools unknown at the start by appending them (tool search with defer_loading, OpenAI's additional_tools input item, Anthropic's tool_addition block), never by editing the array. On Claude, keep at least one declared tool not deferred (if every tool is deferred, the first tool defined in a message costs one full cache miss) and pin an MCP connector server's tool list, since a server that returns a different list edits the prefix.
3. Write availability as a state machine in the harness (state to allowed set) and enforce it without touching the definitions: on OpenAI, tool_choice {"type": "allowed_tools", ...} or "none"; on Claude, an appended system message with tool_removal or tool_addition blocks (beta), because changing tool_choice re-reads the message history and is not allowed inside a message thread (it returns a 400), and forced tool choice and prefill are rejected on recent models; on self-hosted models, a grammar or logit mask over the allowed names, or a prefill up to the shared name prefix, compiled once per state and reused: in one engine a grammar rebuilt per request around a different 100-tool subset lost all whole-grammar reuse and took 219.50 ms to compile against 4.18 ms, while constrained tool calling itself added 0.8% to 6.2% end-to-end latency.
4. Keep a harness-side check whatever the provider: validate every call against the current allowed set (not the set in force when a permission was granted) and the full registry, return an error result that names what is allowed instead of executing or silently dropping the call, and leave earlier calls to now-unavailable tools in the history. In one coding-agent study the check decided the outcome: behind it, a visible-but-disallowed interface executed 0 of 20 forbidden actions, as removal did, while a design that never revoked a temporary capability let it be reused 10 of 10 times.
5. Keep the model able to stop and to decline: do not force a tool call on every turn, and keep a final-answer or no-tool path inside any mask.
6. Check what visibility costs. If tools stay visible but disallowed for long stretches, check accuracy, since a visible unneeded tool can lower answer rates: add a one-sentence note that tools are optional and narrow in scope, and move groups that are rarely allowed behind deferred loading (see 2.a.i). Where the tool list itself is most of the prompt (hundreds of tools, short sessions), also test pruning per request: on single requests over about 450 tools, a cached full list (98.9% cache hits) cost about the same per request as retrieving 10 tools per request, and the pruned list was more accurate (0.840 against 0.787) and 1.43 s faster, so the cache case for masking is strongest in long sessions, where an edit re-reads the whole conversation.
7. Measure with paired runs on sessions that change availability midway, the list rebuilt per state against the stable list plus a restriction (and a per-request pruned list where the catalog is large): cache read share, cost per task, time to first token, calls to unavailable or undefined tools (blocked and executed), task success and turns to finish, per model and provider.

## How to measure

- **experiment** (Tier 3): paired runs on probe sessions where the allowed tool set changes midway (a mode or phase switch, a revoked permission, a tool the model used earlier becoming unavailable): the tool list rebuilt per state against stable definitions with the provider's restriction (allowed_tools or tool_choice, tool_removal blocks, or a decode-time mask compiled once per state) plus a harness check, and, where the catalog runs to hundreds of tools, a per-request pruned list; compare cache read share and cost per task, time to first token, calls to unavailable or undefined tools (blocked and executed), task success and turns to finish, per model and provider
- **monitor**: per session: a hash of the tools array on every request, with cache read and write tokens on the turn after any change (or the provider's cache diagnostics); calls rejected for naming an unavailable or undefined tool, and any disallowed call that executed; on Claude, prefix-check 400s, dropped thinking blocks and thread_fingerprint_mismatch errors after a tool change; sessions that hit the turn cap while a tool call was forced on every turn

## Expected impact

- **Quality:** mixed, medium: schema-enforced calling cut calls to nonexistent tools from 34 to 3 across ten models (Iyer, Sep 2026); behind the same execution check, a visible-but-disallowed interface matched removal on task success, 5 of 20 each, in one small coding study (Santos-Grueiro, Jun 2026); but forcing a call on every turn made weak local models loop for 600-900 turns (Tang, Sep 2026), one visible unneeded tool cut answer rates from 98.2% to 63.5% (Paturi, Sep 2026), per-step pruning beat a full list with the retrieved tools emphasized on small models (Patel, Dec 2025), and on single requests over about 450 tools a pruned top-10 list scored 0.840 against 0.787 for the full list (Tian, Sep 2026)
- **Cost:** improves, medium: avoids a full-prefix recompute at each tool-set change; caching cut agent cost 41.4-79.6% against a prefix broken on every call (Lumer, Jan 2026); cached reads cost 0.1x input on most GPT-5.6+ models (OpenAI docs, Oct 2026); on Claude a tool_choice change still re-reads the message history (Anthropic docs, Oct 2026); the saving scales with how often the tool set changes and how long the cached history is: on single requests over about 450 tools, a stable full list at 98.9% cache hits cost $0.000749 per request against $0.037879 with caching suppressed, but no less than a pruned top-10 list ($0.000819) (Tian, Sep 2026)
- **Performance:** mixed, small: time to first token 6.1-30.9% better with caching than with a prefix broken on every call (Lumer, Jan 2026); but a cached full list of about 450 tools answered in 3.76 s against 2.33 s for a pruned top-10 list (Tian, Sep 2026); a grammar mask added 0.8-6.2% end-to-end latency, and rebuilding it per request around a different 100-tool subset raised compile time from 4.18 to 219.50 ms (Li, Jan 2026); a mask that forces a call every turn can stop a weak model from finishing (Tang, Sep 2026)
- **Security:** mixed, small: the execution-time check, not visibility, decided it in one coding-agent study: behind the same check a visible-but-disallowed interface executed 0 of 20 forbidden actions, as removal did, with more blocked attempts in one task family (84 against 67) and fewer in another (39 against 48); a design that never revoked a temporary capability let it be reused 10 of 10 times, and a coarser check let 10 forbidden effects through (Santos-Grueiro, Jun 2026)
- **Governance:** improves, small (unmeasured)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Yichao 'Peak' Ji (Manus), "Context Engineering for AI Agents: Lessons from Building Manus"… (2025-07-18): Advises "avoid dynamically adding or removing tools mid-iteration" because changes "invalidate the KV-cache" and leave references to undefined tools; Manus instead "masks the token logits during decoding". No numbers.
- OpenAI, "Prompt caching" and "Function calling" (API guides), https://platform.openai.com/docs/guides/prompt-caching … (2026-10-17): Prompt caching guide: a change to tools ("tool names, descriptions, schemas, ordering, or tool-specific instructions") breaks prefix reuse. "When the tools your application needs vary between requests, change which tools are callable while…
- Anthropic, "Prompt caching" and "Tool use with prompt caching" (Claude API docs)… (2026-10-17): The cache follows tools, then system, then messages: "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache", while "Changes to `tool_choice` parameter only affect message blocks" (the tools and system…
- Anthropic, "Mid-conversation system messages and tool changes" (Claude API docs)… (2026-07-24): "The `tools` array sits even earlier in the hashed request prefix than the top-level `system` field, so editing it invalidates the prompt cache for the entire conversation." Instead, "declare the full tool set in `tools` up front, then use…
- …and 10 more sources in `library/entries/mask-tools-not-remove.yaml`.

## Caveats

No study measures masking against removal on cache cost within one multi-turn session: the cache case rests on vendor documentation and on measurements of caching in general, and the saving scales with how often the tool set changes and how long the cached history is. Removal has measured advantages where the tool list dominates the prompt: on single requests over about 450 tools, pruning to 10 per request matched a cached full list on billed cost and won on accuracy and latency (one study, one provider), one unneeded visible tool cut answer rates from 98.2% to 63.5%, and per-step pruning beat a full list on small models. The security comparison is one small coding-agent study on one open model, where the execution-time check, not visibility, decided whether forbidden actions ran. Mechanisms differ by provider and keep changing: on Claude a tool_choice change re-reads the message history and is not allowed inside a message thread, forced tool choice and prefill are rejected on recent models, so Manus's prefill recipe now applies mainly to self-hosted models, where the grammar and constrained-decoding numbers come from small open models.

## Related

- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:constrain-agent-reach` (10.a.i, Constrain what the agent can touch)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:fail-soft-tools` (2.b.i, Make tool calls and tool results fail soft, and retry transient failures)
- `aot-kit:rewrite-tool-surface` (2.a.ii, Rewrite the tool surface: names, schemas, descriptions)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)

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
