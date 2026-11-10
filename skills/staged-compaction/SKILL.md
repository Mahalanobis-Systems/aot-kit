---
name: staged-compaction
description: "AOT optimization 5.a.i (Tier 2, Reliability): Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary. Placeholder. Use when an agent shows: context-overflow outcomes; peak context over about 85% of the window; a reasoning turn ending at the window limit because the history left too little room; summaries that drop file changes, decisions, prohibitions or approval requirements; the last completed call missing after a compaction and then repeated; failure rows labeled context-rationale-erosion."
---

<!-- Generated from library/entries/staged-compaction.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Compact conversation history in stages: elide stale tool outputs, then keep an anchored summary

> **Placeholder.** Generated from `library/entries/staged-compaction.yaml` (entry 5.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. See **To build** below.

| | |
|---|---|
| Id | 5.a.i |
| Earlier id | T31 |
| Tier | 2 (Reliability): stops runs dying on context overflow, a hard failure |
| Categories | Context: Compacting |
| Change | workflow / state_management (tune) |
| Also covers | Context compaction |

## What it is

Clear old tool outputs, then summarize, only when the context window binds, and carry the task's rules and the last completed call forward verbatim, because summaries drop them. It pays most at small windows (+35.7 points at 32k against +2.7 at 128k on coding tasks; +12.3 points on long sessions of a reasoning model in a 49K window), while two 1M-window frontier models scored the same with the trigger anywhere from 160K to 380K tokens and no strategy beat their default self-summarization. Do it in stages and in batches: past about 60% of the usable window replace old tool outputs with stubs, past about 85% summarize the oldest turns into fixed sections updated in place, keep the recent tail verbatim, and avoid edits every turn (each one forces a re-prefill; trimming every turn cost 1.85 times the full context). The losses are ones benchmarks rarely score: the first summary dropped about one of a task's three rules, rules kept in the summary were still broken 2.6 times as often as with the full history, and harnesses that flatten roles into text let forged user turns into the summary in 87% to 100% of trials; work that outlives one window needs its state in files (4.b.iii).

## When it applies

- **In the code:** no compaction, or compaction that summarizes the whole history at once; elision or trimming applied every turn; history flattened into role-labeled text (such as '[User]:') before it is summarized; summaries written by a smaller model than the agent; operating rules kept only in the conversation; a context window under about 64k
- **In traces:** context-overflow outcomes; peak context over about 85% of the window; a reasoning turn ending at the window limit because the history left too little room; summaries that drop file changes, decisions, prohibitions or approval requirements; the last completed call missing after a compaction and then repeated; failure rows labeled context-rationale-erosion
- **In eval results:** failures concentrated in the longest trajectories; rule violations after compaction that a matched full-history run does not make
- **Probes:** Long runs in which a rule stated once early (a prohibition, a scope exclusion, an approval requirement) or an exact identifier must still hold after one or more compactions

## How (outline)

1. Start from the baseline, per model: on the longest runs, measure peak context against the usable window (the window minus the reply and reasoning reserve), overflow and turn-cap endings, runs that end when one reasoning turn fills the room the history left, success, and tokens and cost per task. Compaction pays where the window binds: managed history added 35.7 points at 32k but 2.7 at 128k on SWE-bench Verified, and for two 1M-window frontier models moving the trigger between 160K and 380K tokens (16% to 38% of the window) did not change scores and no strategy beat the scaffold's default self-summarization. If runs rarely approach the window, keep the default compaction and spend the effort on what it must not lose (steps 5 and 6) instead.
2. Set two thresholds on the usable window and leave room for a full turn. Past a soft threshold (about 60%) replace old tool outputs with a stub that keeps the tool name, the arguments and a handle to get the content back (a file path, a command to re-run, an ID); re-reading or re-running is the recovery path, since a dedicated recall tool went unused in more than half of the settings tested and did not raise success. Past a hard threshold (about 85%) summarize the oldest turns and keep a verbatim recent tail (about 30% of the window, at least two turns). For reasoning models in tight windows trigger earlier: in a 49K window most uncompacted failures (102 of 200 sessions) were one reasoning turn exhausting the room left, compacting at about half the input budget raised the long-session resolve rate from 41.2% to 52.9%, and a trigger at 48K of a 51.7K budget fired in 4 of 50 sessions and behaved like no compaction. Do not compact earlier than needed to save tokens: a 400K-window model scored 0.38 with a 160K trigger against about 0.60 at 260K and above, and summarizing at 48K instead of the standard 96K or 192K threshold lowered the average score of two of three open models (51.0 to 48.3 and 44.1 to 37.1).
3. Elide in batches at the threshold, not every turn. Every edit to earlier history rewrites the cached prefix and forces a re-prefill of everything after it: trimming tool outputs to the latest 12 rounds on every turn cost 1.85 times as much as keeping the full context. Fire elision only when it frees a large block (OpenCode prunes only when more than 20K tokens are reclaimable and protects the newest 40K; with that rule elision stayed close to self-summarization on PaperBench for every model tested), keep the rest of the prefix byte-stable (3.b.i), and expect each summary to cost one turn of cache reuse (96% against 98% of prompt tokens reusable). On a self-hosted engine, dropping old tool-output KV cache instead of editing the text avoids the re-prefill (27.7% lower pooled cost and +1.7 points against threshold summarization); hosted APIs do not offer it.
4. Summarize into fixed sections and update them in place. Keep sections for the goal, files and other artifacts touched, done, pending, errors and decisions, and the next step; give the summarizer the previous summary plus the newly folded turns and merge, instead of regenerating from the whole history. Task records revised in place scored 55.93 (OSWorld partial score) against 50.93 for a summary following the same principles, 44.94 for a generic summary and 50.32 for no compaction on 40 tasks, and anchored iterative summaries beat full regeneration 3.70 to 3.44 on one vendor's 0-5 probe scale. Write summaries with the agent's own model or a tested equal: Claude Haiku 4.5 summaries kept Claude Opus 4.6 within its baseline interval but cost GPT-5.4 16 points and GPT-5.3-Codex 20, and removing old reasoning blocks before summarizing cost GPT-5.4 16. Check paths, identifiers, error lines and numbers in the summary against the source and drop any that occur nowhere. Where sessions are time-bound, write the summary in the background and apply it on the next turn: a 27B reasoning writer took a median 161 s per summary, and under a 45-minute session cap the success gain vanished.
5. Carry forward verbatim what a summary cannot be trusted with: the task statement, every operating rule (prohibitions, scope exclusions, approval requirements, process instructions) and the most recent completed call with its result. Summaries drop rules even when the prompt asks to keep them: the first summary dropped on average 0.92 of a task's three anti-cheating rules and 1.93 by the tenth compaction, because later summaries are written from earlier ones that already lost them, and on real coding sessions process instructions and scope exclusions were dropped 35.9% and 36.8% of the time against 6.2% for feature requirements. Re-inject the original task and rule messages after each compaction (one published harness re-injects prior user messages for this) or keep them in a file the agent re-reads (4.b.iii), and tell the summarizer to preserve rules with their scope, exceptions and negation: in one benchmark that instruction was the only compaction strategy below the full-history violation rate (9.0% against 11.9%). Never compact by dropping whole turns (first-in-first-out lost the rule in every run) or into a summary budget of a few hundred tokens (at 300 and 200 tokens at least 95.1% of runs lost it). Keeping the rule is not enough: runs whose summary kept it still broke it 2.6 times as often as full-history runs, so enforce rules that matter outside the model (10.b.i). Removing the last completed call raised immediate repeats of it from 3.3% to 48.8%, and an explicit trace or ledger of past actions in the summary did not stop loops (52.0% to 62.7% of runs against 57.3%), so keep the call itself in the tail (7.b.i).
6. Treat the summarizer's input as a trust boundary and keep the raw history. Pass the history role-typed, or escape role labels inside tool output, rather than flattening it into text such as '[User]:': forged user turns planted in tool output became user instructions in the summary in 87% to 100% of trials in five harnesses that flatten roles, against 0% in four that keep messages typed, and a laundered approval led an agent to run an attacker's command in 3 of 6 live sessions (0 of 5 clean). A prompt rule against injected instructions stopped only 13% to 25% of laundering; a code check of the summary's user-attributed claims against the stored user turns caught 77% with 2% of legitimate claims demoted. Keep the full history in an append-only log or a linked session for audit and recovery and tell the agent where it is, but don't expect a score gain from it: writing the pre-compaction context to a file did not beat plain self-summarization and lowered one model from 0.38 to about 0.24.
7. Measure on the same long tasks and model, several runs per arm: the default or no compaction, elision only, and staged; report success, overflow and cap endings, tokens and cost per task including summarizer calls, cache-hit rate around compactions, time per compaction and wall-clock. Add probes a benchmark score misses: a rule stated once early and a later request that would break it (graded from the tool calls against a full-history run, not from the summary), recall of exact identifiers and files changed, completed work described as pending, repeats of the last completed call, and a forged user line planted in a tool output. Re-run per model: summarizer and strategy effects that held for one model did not transfer to another.

## How to measure

- **experiment** (Tier 3): same long tasks and model, several runs per arm: default or no compaction, elision only, staged; success, overflow and cap endings, tokens and cost per task including summarizer calls, cache-hit rate, time per compaction; plus rule-compliance probes graded from tool calls against a full-history run, exact-identifier recall, and a forged user line planted in a tool output
- **monitor**: per model in production: peak context against the usable window, overflow errors, compactions per session and time per compaction, cache-hit rate on the turn after a compaction, a sampled judge check of rules and identifiers missing from summaries, and repeats of the last completed call after a compaction; re-run the experiment when the model or summarizer changes

## Expected impact

- **Quality:** improves, large: where the window binds: managed history +35.7 points at 32k and +2.7 at 128k on SWE-bench Verified (Fan, Sep 2026); +12.3 points on long sessions of a 27B reasoning model in a 49K window (Jithin VG, Oct 2026); task records kept in place +5.8 points partial score on OSWorld 2.0 (Lu, Oct 2026); near zero for 1M-window frontier models, where no strategy beat default self-summarization (Salle, Oct 2026); a generic regenerated summary scored 5.4 points below no compaction (Lu, Oct 2026), and smaller-model summaries or dropped reasoning cost some models 16 to 20 points (Salle, Oct 2026)
- **Cost:** improves, medium: staged elision lowest cost in 7 of 8 panels, e.g. $1.45 against $2.57 (Fan, Sep 2026); task records 51.9% fewer tokens and 35.9% lower cost per task over a 500-step budget (Lu, Oct 2026); equal total tokens and 13% fewer per resolved session in a 49K window (Jithin VG, Oct 2026); but trimming tool outputs every turn cost 1.85 times the full context because each edit forces a re-prefill (Fu, Oct 2026)
- **Performance:** mixed, medium: each summary took a median 161 s with a 27B reasoning writer, model time rose 14%, and under a 45-minute session cap the success gain vanished (Jithin VG, Oct 2026); dropping old tool-output KV cache in a self-hosted engine gave 1.51 times faster P95 request latency than threshold summarization (Fu, Oct 2026)
- **Security:** degrades, medium: the summary is an injection channel: forged user turns in tool output were laundered into it as user instructions in 87% to 100% of trials in harnesses that flatten roles to text, 0% in role-typed ones (Dabirsiaghi, Oct 2026); a compactor-targeted injection raised rule violations from 37.8% to 46.3%, and from 23.5% to 58.8% at its strongest (Zha, Nov 2026)
- **Governance:** degrades, medium: operating rules are lost or ignored after compaction: violation@3 rose from 9.6% to 37.8% with most rules still in the summary, and organizational rules never broken with the full history were broken after it (Zha, Nov 2026); summaries dropped process instructions and scope exclusions 35.9% and 36.8% of the time against 6.2% for feature requirements (Salle, Oct 2026); an instruction to preserve rules brought violations to 9.0% against 11.9% with full history (Zha, Nov 2026)

## Evidence (summary)

- repo figure_04 (2026-02): MAX_HISTORY_CHARS lowered twice, never raised.
- repo figure_01 (2026-02): Context-management edits in 6 to 10 of 20 runs per benchmark.
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): Managed tiers (T1-T4) vs no management (T0), averaged over 4 models (Nemotron-3 30B/120B/550B, Mistral-Medium-3.5-128B): the gap is 35.7, 15.9, 5.5 and 2.7 pp on SWE-Bench Verified (n=500) and 9.5, 7.5, 4.8 and 2.8 pp on Terminal-Bench 2.1…
- Fan et al., "An Empirical Study of Harness Design for Coding Agents", https://arxiv.org/abs/2609.20804 (2026-09-17): T2 (elision+recall) vs T1 (elision) over 32 model-benchmark-window comparisons: 15 wins, 14 losses, 3 ties. Mean -0.36 pp (+0.40 SWE, -1.12 TB). 36 of 64 T2/T4 settings never call recall_event and the median rate is zero. Use is…
- Barbaste et al., "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems"… (2026-07-15): Claude Code "AUTOCOMPACT_BUFFER_TOKENS = 13 000"; post-compact restores "up to 5 files (POST_COMPACT_TOKEN_BUDGET = 50 000)"; Gemini "fires when history exceeds 50% ... preserves the most recent 30%"; Mistral Vibe envelope "re-injects…
- …and 21 more sources in `library/entries/staged-compaction.yaml`.

## Caveats

Most measured evidence is narrow: the frontier-model strategy study ran two runs per configuration on two or three tasks per benchmark, the comparison with task records ran once on 40 tasks, rule compliance was measured on 17 cases with flash-tier models and an aggressive default summary target, and the loop and last-call results come from small open models at 1,400- to 4,096-token thresholds. Effects depend on the model and on what is scored: a cheaper summarizer or dropped reasoning cost one model 16 to 20 points and left another unchanged, the 60% and 85% thresholds come from one study and were not swept, and benchmarks with a fixed goal and progress on disk hide the loss of rules that exist only in the conversation, which is where summaries fail most. Compaction also costs time (a median 161 s per summary with a reasoning writer, enough to erase the gain under a 45-minute cap), the cheapest measured option (KV-level dropping) needs a self-hosted engine, and the strongest security result is one author's test of nine harnesses at 15 trials each.

## Related

- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:bound-tool-output` (2.c.i, Bound tool output: cap it, or write it to a file the agent can read)
- `aot-kit:detect-loops-and-stalls` (7.b.i, Detect stalls and loops: warn, then stop early)
- `aot-kit:track-task-progress` (7.b.iv, Track explicit progress: a task list with a status per item, re-injected each turn)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:risky-action-policy` (10.b.i, Gate irreversible actions: allow, ask or deny by side effect)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:size-execution-budgets` (7.b.iii, Size run budgets so productive runs aren't cut off: turn caps, deadlines, command timeouts)
- `aot-kit:keep-errors-in-context` (7.b.ii, Keep errors in context)
- `aot-kit:vary-few-shot-examples` (3.a.ii, Avoid few-shot ruts)
- `aot-kit:discrete-phase-separation` (5.c.i, Discrete phase separation)

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
