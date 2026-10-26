---
name: skill-library
description: "AOT optimization 4.c.ii (Tier 4, Restructuring): Skill library evolution. Placeholder. Use when an agent shows: Skill reuse rate; skills authored per session; loaded-skill recall and zero-load rate per run; per-skill opens and outcomes; skills never opened; skills distilled from failed or unlabeled runs; authored skills that copy retrieved code verbatim."
---

<!-- Generated from library/entries/skill-library.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Skill library evolution

> **Placeholder.** Generated from `library/entries/skill-library.yaml` (entry 4.c.ii). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 4.c.ii |
| Earlier id | P58 (Learning, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a reusable skill memory |
| Categories | Memory: Reusing work |
| Change | tool / memory |

## What it is

Have the agent turn runs that passed a verifier into reusable skills (a code function or a SKILL.md procedure), store them in a library, and on later tasks show it only the few a separate selection step picks, reviewing what goes in and pruning what goes unused. It pays on recurring task families when skills come from verified successes: skills distilled from an agent's own successful runs raised success on those tasks (Terminal-Bench-2 0.5935 to 0.7548 with GPT-5.3-Codex), but skills distilled from failed runs fell below no experience, and skills a model wrote before attempting the task scored 8.1 to 11.5 points below no skills with Opus 4.7, GPT-5.5 and Gemini 3.1 Pro. Two costs grow with the library: agents stop opening the right skill (loaded-skill recall 73.6% to 27.4% with 1,000 irrelevant skills listed) unless a preselector chooses, and an agent that writes skills from retrieved ones copied planted malicious code into its own library on 20.3% to 41.8% of tasks across six models.

## When it applies

- **In the code:** A skills directory or store the agent writes to after runs; skills written without a verifier outcome, or from the model's own knowledge before it attempts the task; new skills retrievable with no review or quarantine; authoring that reads retrieved skills as templates; every skill's name and description listed to the agent on every run.
- **In traces:** Skill reuse rate; skills authored per session; loaded-skill recall and zero-load rate per run; per-skill opens and outcomes; skills never opened; skills distilled from failed or unlabeled runs; authored skills that copy retrieved code verbatim.
- **In eval results:** Paired runs with and without the library on held-out tasks from recurring families (pass rate, tokens, time); pass rate and loaded-skill recall as the library is padded with irrelevant skills.
- **Judge:** Review each new skill before it becomes retrievable: task-specific paths or values baked in, confident assumptions no verifier checked, boilerplate copied from retrieved skills, overlap with existing skills.
- **Probes:** Recurring task families; a growing library; planted skills.

## How (outline)

1. Start from the baseline: the same model and harness with no skill library, plus an arm with cleaned traces of past runs in context (cheaper: 95.3K fewer tokens per task than distilled skills, for 4.8 points less success in one study), on recurring task families with a deterministic verifier, scored on held-out instances. Do not ask the model to write skills from what it already knows before it attempts the task: such self-generated skills scored 8.1 to 11.5 points below no skills with Opus 4.7, GPT-5.5 and Gemini 3.1 Pro, because solvers never opened them or followed confident errors such as a hard-coded 1000x unit conversion.
2. Write a skill only from a run the verifier passed: distill the trajectory into a code function or a SKILL.md (when to use it, preconditions, steps, failure modes, a verify step) with task-specific paths and values replaced by placeholders. If failed runs feed the writer, label them: skills distilled from failed runs alone fell below no experience in all six benchmark-model cells, and hiding the success and failure labels cut Gemini 3.1 Pro on Terminal-Bench-2 from 0.7462 to 0.4000. Voyager added a program only after self-verification passed, and removing self-verification cut discovered items by 73%.
3. Gate admission: keep agent-authored skills in a quarantine that retrieval cannot see until a reviewer or a signed admission step approves them, and tell the authoring agent that retrieved skills are untrusted and that banner-style "REQUIRED PATTERN" or "DO NOT MODIFY" boilerplate must not be copied (10.c.i). In one study that four-line instruction cut self-poisoning from 20.3% to 41.8% of tasks to at most 6.7% with no significant loss in task completion, while a name blocklist caught none of the authored copies and a code scanner fell to 7% after a one-line rewrite.
4. Retrieve a few skills through a separate step instead of listing them all (the same deferral idea as 2.a.i): near 100 skills, an LLM preselector over names and descriptions; at thousands, retrieval followed by an LLM selector; expose a handful (at most five in the study). With 1,000 irrelevant skills listed, loaded-skill recall fell from 73.6% to 27.4% although a selector given the same list found 73.9%; LLM preselection cut tokens per run from 1,966k to 547k and added a median 8 to 41 seconds of routing; asking the agent to plan its skill use first did less than preselection.
5. Prune and revise from telemetry: log which skills each run opens and its outcome; retire skills that are never opened or whose runs keep failing, and merge near-duplicates, since irrelevant descriptions suppress loading (masking them restored recall from 18.3% to 63.3%) and similar skills are the hardest to tell apart (top-1 precision 70.5% to 53.4% on similar pools). If a poisoned skill is found, scrub the agent-authored copies too: in one model the infection rose to 68% of tasks after the planted seeds were removed.
6. Measure paired against the baseline, same model and harness, on held-out tasks (not only the tasks the skills came from): pass rate, tokens and time per task, loaded-skill recall, zero-load rate and the misapplied-skill rate (10.0% of skill runs in one study); rerun with the library padded to its expected size and with planted-skill probes, since task success can stay flat while skill use collapses (precision 29.6% to 3.3% with success 36.4% to 39.3%).

## How to measure

- **experiment** (Tier 4): paired runs, same model and harness: no library, the agent-built library, and where available a curated library or cleaned traces of past runs, on held-out instances of recurring task families scored by a deterministic verifier; pass rate, tokens and time per task, loaded-skill recall, zero-load rate and misapplied-skill rate; repeat with the library padded to its expected size with irrelevant skills, with implicit loading against a preselector, and with planted skills carrying copy-me boilerplate and a harmless callback to measure how often authored skills reproduce them
- **monitor**: per-skill loads and outcomes, the zero-load rate on tasks that have a matching skill, skills never opened (prune), skills admitted and rejected with their source run and verifier result, authored skills that copy retrieved code or add network or credential access, and pass rate on the task families the library serves

## Expected impact

- **Quality:** mixed, large: skills distilled from an agent's own successful runs raised success on the same tasks (Terminal-Bench-2 0.5935 to 0.7548 with GPT-5.3-Codex, 0.5000 to 0.7923 with Gemini 3.1 Pro), but skills from failed runs fell below no experience in all six cells and hiding outcome labels cut 0.7462 to 0.4000 (Jiang, Aug 2026); skills written before any attempt scored 8.1 to 11.5 points below no skills while curated ones added 18.2 to 24.8 (Li, Feb 2026); with 1,000 irrelevant skills listed, Pass@3 fell from 51.6% to 38.6% (Liu, Oct 2026); Voyager found 3.3x more unique items than prior agents (Wang, May 2023)
- **Cost:** mixed, medium: skills used 34.2K fewer tokens per task than the Raw arm but 95.3K more than cleaned traces of the same runs, on 83 matched tasks (Jiang, Aug 2026); listing every skill's description raised tokens per run from 498k to 1,966k with 1,000 irrelevant skills added, and an LLM preselector brought it to 547k (Liu, Oct 2026)
- **Performance:** mixed, small: Voyager reached tech-tree milestones up to 15.3x faster, counted in prompting iterations, than prior agents (Wang, May 2023); a run took 15.3 minutes with only the relevant skills and 17.0 with 1,000 more listed, and preselection adds a median 8 to 41 seconds of routing (Liu, Oct 2026)
- **Security:** degrades, large: planted skills were copied into agent-authored skills on 20.3% to 41.8% of SWE-bench Verified tasks across six open-weight models, leaving 4.9 to 9.0 times the planted count, and one model's infection rose to 68% after the plants were removed; a name blocklist caught 0 of 275 authored copies; a four-line counter-prompt cut it to at most 6.7%, and a curator-signed quarantine stops re-retrieval (Wu, Aug 2026)
- **Governance:** mixed, medium: skills are versioned files a reviewer can read, but task success hides library failure: skill-use precision fell from 29.6% to 3.3% as the pool grew from 5 to 100 while success moved from 36.4% to 39.3% (Jiang, Aug 2026), and Claude Opus 4.6 kept Pass@3 at 62.2% (from 64.9%) while its loaded-skill recall fell from 81.3% to 30.9% (Liu, Oct 2026); agent-authored skills bypass submission-side review unless new entries wait in a curator-signed quarantine (Wu, Aug 2026)
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Wang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models", https://arxiv.org/abs/2305.16291 (2023-05-25): "obtains 3.3x more unique items, travels 2.3x longer distances, and unlocks key tech tree milestones up to 15.3x faster than prior SOTA". Ablation: without the skill library, progress plateaus in later stages (figure only, no number)…
- Jinlin Liu, Wei Chen, Xiaojin Zhang, "Lost in Implicit Routing: How LLM Agents Fail to Load Relevant Skills at Scale"… (2026-10-13): Implicit routing, 0 to 1,000 irrelevant skills: loaded-skill recall 73.6% to 27.4%, zero-load rate 9.3% to 51.6%, Pass@3 51.6% to 38.6% (no skills: 26.8% to 34.1% per model); the same models selecting from the full list without executing…
- Xiaodong Wu, Yu Shi, Qi Li, Zhimin Zhao, Xiangman Li, Bram Adams, Ahmed E. Hassan, Jianbing Ni, "EVOMAL: Self-Poisoning in Self-Evolving… (2026-08-26): Agent self-poisoning rate 20.3% to 41.8% across six models on 153 tool-relevant SWE-bench Verified tasks, 18.3 to 32.0 points above a payload-free control; 31 to 64 newly authored malicious skills, 4.9 to 9.0 times the 8 planted.…
- Zhiyuan Jiang, Fangrui Huang, Hanwen Xing, Xander Wu, Yipeng Gao, Rui Cao, Mengdi Wang, Shilong Liu, Yijiang Li, "Demystifying Agent… (2026-08-14): Success-only skills against no prior experience: Terminal-Bench-2 0.5935 to 0.7548 (Codex + GPT-5.3-Codex) and 0.5000 to 0.7923 (Gemini CLI + Gemini 3.1 Pro); SkillsBench 0.5083 to 0.7250 and 0.4762 to 0.7429. Failure-only skills fell…
- …and 1 more sources in `library/entries/skill-library.yaml`.

## Caveats

The positive evidence for agent-built skills is narrow: the strongest controlled gain scored skills on the same tasks whose runs they were distilled from (tasks chosen because raw runs both passed and failed), its 6.06-point lead is over cleaned traces with a lower bound of 0.76, and Voyager's headline compares its whole system, not the library alone, with GPT-4 in Minecraft. The self-generated deficit comes from skills written before any attempt, so it does not test skills distilled from verified successes, and one configuration ran that arm at a higher effort level. The poisoning study used six open-weight models, attacker-planted seeds and an agent asked to author a tool on every task; the routing study used curated SkillsBench skills with marketplace distractors, mostly on open-weight models with a 37-task check on Claude Opus 4.6, Gemini 3.1 Pro and GPT-5.4. No source here measures an agent-grown library over months of production use.

## Related

- `aot-kit:episodic-memory` (4.c.i, Episodic memory retrieval)
- `aot-kit:reduce-tool-surface` (2.a.i, Reduce the tool surface: remove and consolidate tools, then defer the rest behind search)
- `aot-kit:tool-use-guidance` (2.b.ii, Tell the agent when to use each tool, in context it always sees)
- `aot-kit:isolated-subagent-context` (5.c.ii, Sub-agent architectures with clean contexts)
- `aot-kit:choose-action-interface` (2.a.iii, Choose how the agent acts: typed tools, code execution, or shell, matched to the model and task)
- `aot-kit:contain-untrusted-input` (10.c.i, Contain sensitive data and untrusted input)
- `aot-kit:inversion-of-control` (7.d.ii, Inversion of control)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:multi-window-task-state` (4.b.iii, Keep plan, progress and results in files when work outlives one context window)

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
