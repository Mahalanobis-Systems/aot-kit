---
name: multi-agent-debate
description: "AOT optimization 7.c.vi (Tier 4, Restructuring): Multi-agent debate. Placeholder. Use when an agent shows: Rounds per item; share of items where the final answer differs from the first-round vote and, on items with ground truth, whether the change fixed or broke it; right-to-wrong and wrong-to-right flips per round; empty or truncated final-round answers; prompt and total tokens per round."
---

<!-- Generated from library/entries/multi-agent-debate.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Multi-agent debate

> **Placeholder.** Generated from `library/entries/multi-agent-debate.yaml` (entry 7.c.vi). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 7.c.vi |
| Earlier id | P43 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a multi-agent topology |
| Categories | Orchestration: Scaling compute |
| Change | workflow / orchestration |

## What it is

Several model instances answer the same question, read each other's answers and revise over one or more rounds, and a vote or judge settles the final answer. It beats a single answer on closed-form reasoning (+3.3 to +6.6 points across 23 open models where tasks had headroom), but a plain majority vote over the same number of independent samples gets the same gain: in budget-matched tests debate tied or lost to the vote on every task, GPQA Diamond at full thinking budget included, at 1.6x the wall-clock and 3.4x the tokens, and a vote over the first-round answers alone beat every debate variant on average, though mostly on one arithmetic task (0.99 vs 0.76; Choi, NeurIPS 2025). Mixing model families lifted debate above the average of its single-model runs in one study but lost to a vote over the same mixed roster in another (-1.04 points over 80 teams), and with frontier models on real paper feedback, authors ranked a single pass above two debate tools that spent 9x and 30x the tokens. Treat debate as an experiment against a vote at matched compute, worth keeping only where the vote is often wrong while some agent has the right answer.

## When it applies

- **In the code:** Several agents answer the same question, see each other's answers and revise over rounds, with a vote, judge or synthesizer at the end. Flag it when the eval has no majority-vote arm at the same number of generations, when more than one exchange round runs, when transcripts can outgrow the context window (agents x rounds x per-turn budget, thinking included), when agents get persona prompts, or when arms parse answers differently.
- **In traces:** Rounds per item; share of items where the final answer differs from the first-round vote and, on items with ground truth, whether the change fixed or broke it; right-to-wrong and wrong-to-right flips per round; empty or truncated final-round answers; prompt and total tokens per round.
- **In eval results:** Accuracy against a majority vote over the same number of independent generations (same model, or the same mixed roster) and against the single pass at full thinking budget, with the same answer extractor; for open-ended output, blind ranking by intended users against a single pass of equal length.
- **Judge:** Secondary only: an external AI judge agreed with paper authors at 0.14 and would have reversed their ranking of debate against a single pass; for open-ended output rank with intended users, and balance any judge panel across vendors.
- **Probes:** Items where the first-round majority is wrong but at least one agent is right, mixed with items where the majority is right.

## How (outline)

1. Start from the cheap baselines on your own items: the single pass at full thinking budget (1.b.i) and a majority vote over as many independent generations as the debate would spend (agents x rounds) from the same model or roster (9.c.ii). Across 23 open models debate with 3 agents and 3 rounds tied or lost to a 9-sample vote on every task, never significantly ahead (GPQA Diamond 54.9 vs 54.3, CommonsenseQA 80.6 vs 78.3), and a vote over 5 first-round answers beat every debate variant on average (Qwen2.5-7B 0.7691 vs at best 0.7377), mostly on one arithmetic task (0.99 vs 0.76); on the other six benchmarks the two averaged about 0.73 each. Build debate only where the vote leaves headroom.
2. Give every arm the same final-answer format and extractor, and parse the last answer an agent states, since debate replies quote their peers' answers (9.b.i). With Du et al.'s parser debate beat the vote on GSM8K (0.7533 vs 0.6700); with a fixed answer format the vote won (0.9400 vs 0.8867).
3. To use several models, pool them and vote before adding debate, and compare any mixed debate against a vote over the same mixed roster and against the strongest model alone. Mixing GPT-4o-mini and Llama-3.1-70B lifted every debate framework over the mean of its single-model runs (Society of Minds 76.7 vs 74.3 and 69.9), but no vote over that mix was run; across 80 three-model teams where it was, debate lost 1.04 points to it, and in the 19 team-task cells where mixed debate beat the team's best member by 10 points or more, the roster vote gained more (+16.4 vs +13.5). Do not add persona prompts on small models: they cost 2.1 to 4.4 points.
4. If debate stays, run one exchange after the first answers and stop. In mixed-team debate accuracy went from 84.6% (vote over first answers) to 87.2% after one exchange and stayed at 87.0-87.5% through five rounds; Decentralized debate fell from 0.7377 at two rounds to 0.7050 at five. Letting an agent keep an answer that matched the last majority raised debate to 0.7625, still below the vote (0.7691).
5. Size the context window to agents x rounds x per-turn budget, thinking tokens included, and give the debate and the vote the same thinking budget. With long-thinking models at 16-32K windows, 93-100% of some cells' final-round answers came back empty (one GPQA cell 0.24 at 16K vs 0.82 at 131K); three 40K-budget thinkers reached 100-112K-token prompts by round 3; and a 4,096-token thinking cap left on some reasoning models hurt the single-shot arm more than debate, creating a 3.2-point debate lead that became -0.6 at the full budget.
6. For open-ended output with no answer to vote on (reviews, critiques, reports), compare against a single pass of equal length, ranked blind by the people who use it, not by an LLM judge: authors ranked a single Claude Opus 4.8 pass (mean rank 1.59) above a cross-family debate (2.25) and a multi-agent workshop (2.16) that cost 9x and 30x the tokens, and an external AI judge agreed with them at only 0.14 and would have reversed the verdict.
7. Measure on held-out items with ground truth: paired accuracy of debate against the vote at matched generations, with confidence intervals; total tokens including re-read transcripts (3.4x the vote's, though generated tokens matched at 1.06x) and wall-clock (1.6x); empty or truncated final answers; and how often debate changes the vote's answer and in which direction. Re-run on model upgrades.

## How to measure

- **experiment** (Tier 4): paired eval on held-out items with ground truth: debate (agents x rounds) against a majority vote over the same number of independent generations from the same model or the same mixed roster, and against the single pass at full thinking budget; identical answer format and extractor in every arm; context window at least agents x rounds x per-turn budget; accuracy with paired confidence intervals, total tokens including re-read transcripts, wall-clock; for open-ended output, blind ranking by the intended users against a single pass of equal length
- **monitor**: per item: rounds run, empty or truncated final-round answers, prompt and total tokens, latency, share of items where debate changes the first-round vote; on a regularly audited sample, whether those changes fix or break the answer

## Expected impact

- **Quality:** mixed, medium: over one answer +3.3 to +6.6 points where tasks had headroom (Ferreira, Sep 2026; GSM 85.0 vs 77.0, Du, May 2023); against a vote at matched or lower compute none or negative: ties or losses on every task, -1.04 for mixed-model teams (Ferreira, Sep 2026), vote 0.7691 vs best debate 0.7377 (Choi, Aug 2025), debate beat CoT in at most 5 of 36 scenarios (13.9%) (Zhang, Feb 2025); paper feedback from frontier models: single pass mean rank 1.59 vs 2.25 and 2.16 for debate tools (Havranek, Jul 2026)
- **Cost:** degrades, large: 3.4x the total tokens of a matched 9-sample vote (2.3x to 4.1x by task) because each round re-reads peers' transcripts (Ferreira, Sep 2026); 9x and 30x the tokens of a single pass, $1.87 and $7.20 vs $0.20 per paper (Havranek, Jul 2026)
- **Performance:** degrades, large: 1.6x the wall-clock of a matched vote; 20 vs 12 vs 5 minutes per 100-problem job for debate, vote and single pass on local serving (Ferreira, Sep 2026); rounds run in series
- **Security:** none (unmeasured)
- **Governance:** improves, small (unmeasured): Recorded arguments.
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Du et al., "Improving Factuality and Reasoning in Language Models through Multiagent Debate", https://arxiv.org/abs/2305.14325 (2023-05-23): Arithmetic: debate 81.8 vs 67.0 single agent and 69.0 majority vote; Grade School Math: 85.0 vs 77.0 and 81.0; chess pawn-score gain 122.9 vs 91.4 and 102.2 (Table 1)
- Tomas Havranek, Zuzana Irsova, "Does Multi-Agent Debate Improve AI Feedback on Research Papers?", https://arxiv.org/abs/2607.14713 (2026-07-16): Mean rank (1 = most useful), 44 papers: single pass 1.59 [1.39, 1.82], mad-research 2.25, paper-workshop 2.16; the single pass was first on 55% of papers and ranked above mad-research on 32 of 44 and above paper-workshop on 30 of 44…
- Leonardo Ferreira, Gardenia Liu, Kaden Zheng, "Beyond Symmetric Agents: Cognitive Diversity and Multi-Agent Debate in Small Language… (2026-09-26): Mean accuracy over 23 models, solo / debate / SC-9: GSM8K 87.9 / 91.2 / 91.0; MMLU 69.9 / 76.5 / 76.8; CommonsenseQA 72.6 / 78.3 / 80.6 (sampling +2.3, p=0.011); arithmetic 91.2 / 91.5 / 90.6; biography claim precision 54.6 / 55.6 / 64.6.…
- Hyeong Kyu Choi, Xiaojin Zhu, Sharon Li, "Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?"… (2025-08-24): Average over seven benchmarks, Qwen2.5-7B-Instruct: vote 0.7691; best debate 0.7377 (Decentralized, 2 rounds), 0.7050 at 5 rounds; single agent 0.7205. Llama3.1-8B-Instruct: vote 0.7242; best debate 0.6990 (Sparse, 2 rounds); single agent…
- …and 1 more sources in `library/entries/multi-agent-debate.yaml`.

## Caveats

Most matched-compute evidence is closed-form QA and math on open models from 0.6B to 109B (100 problems per task in the 23-model study, an unreviewed preprint), where there is an answer to vote on; the one frontier-model study measures how useful 44 authors found length-normalized reports, not correctness, and its authors built the debate tools. Heterogeneity is contested: mixing GPT-4o-mini with Llama-3.1-70B lifted every debate framework over the two models' average, but no vote over that mix was run and one mixed framework stayed below its GPT-4o-mini-only run (74.0 vs 75.7), while the study that did run a roster vote found the vote ahead (-1.04 points for debate). Debate results are fragile to evaluation details: a different answer parser reversed debate against the vote on GSM8K, and in one study a capped thinking budget and context overflow each moved the comparison by about two to four points before correction. Biasing agents toward the last majority narrowed the gap to the vote but did not close it (0.7625 vs 0.7691), and Du et al.'s original gains (GSM 85.0 vs an 81.0 vote) came from a 2023 ChatGPT model with an answer parser that, rerun on Qwen2.5-7B, cut the vote's GSM8K score far more than debate's (0.6700 vs 0.9400 for the vote, 0.7533 vs 0.8867 for debate).

## Related

- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:extractable-final-answer` (9.b.i, Make the final answer reliably extractable: state the format, extract robustly, force an answer at the limit)
- `aot-kit:reflection-loop` (7.c.i, Reflection loop)
- `aot-kit:evaluator-optimizer-loop` (7.c.iii, Evaluator-optimizer loop)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
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
