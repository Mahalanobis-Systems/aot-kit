---
name: oracle-worker-escalation
description: "AOT optimization 6.a.i (Tier 4, Restructuring): Oracle-worker multi-model. Placeholder. Use when an agent shows: Escalation or consult rate and when it fires (turn of the first consult, share in the last third of the run); strong-model share of tokens and cost; escalated tasks whose outcome changed; advice the worker then ignored."
---

<!-- Generated from library/entries/oracle-worker-escalation.yaml by tools/render_skills.py. Edit the entry, not this part. -->

# Oracle-worker multi-model

> **Placeholder.** Generated from `library/entries/oracle-worker-escalation.yaml` (entry 6.a.i). It
> describes the optimization; it does not yet walk an agent through applying it. The tier is proposed. See **To build** below.

| | |
|---|---|
| Id | 6.a.i |
| Earlier id | P42 (Multi-Agent, from the catalog cookbook) |
| Tier (proposed) | 4 (Restructuring): it adds a multi-model topology |
| Categories | Topologies: Escalating; Models: Using cheaper models |
| Change | workflow / orchestration |

## What it is

Let a cheap model do the work and call an expensive one only when a trigger fires: a cascade escalates when the cheap answer looks unreliable or fails a check, a router picks the model before the call, and an advisor tool lets a cheap agent consult a stronger model mid-task. It pays when the trigger really separates the cheap model's failures: a two-model cascade beat the best single model at the same budget by 2.1 to 8.2 points on average across budgets, a learned consult policy recovered 44% to 81% of the gap to the strong model on three agent benchmarks at 34.5% to 48.1% of its cost, and re-running only the failures of a low-effort run at high effort matched an all-high run for about 40% less (computed task by task from existing runs, not run end to end). The trigger is the weak link: none of six commercial routers beat a random mix of two well-chosen models at matched cost (the worst trailed by 10.5 points), a third to fifth model in a cascade added at most 0.43 points, and agents left to decide for themselves consulted rarely and late. In Anthropic's tests on current models the advisor bought about what more effort does (1.7 points for 2.1 times the cost on coding) and scored 7 points lower on chart reading, where it was configured but consulted on 1 of 300 tasks.

## When it applies

- **In the code:** Two models with an escalation call from worker to oracle.
- **In traces:** Escalation or consult rate and when it fires (turn of the first consult, share in the last third of the run); strong-model share of tokens and cost; escalated tasks whose outcome changed; advice the worker then ignored.
- **In eval results:** Success and cost per completed task against each model alone across effort settings and against a random mix of the two at the same spend.
- **Judge:** Whether escalations were warranted.
- **Probes:** Tasks the worker solves, tasks only the oracle solves, and tasks neither solves.

## How (outline)

1. Start from single-model baselines on your own tasks: the cheap and the strong model alone, each across effort settings (the strong one at low effort too), priced per completed task, plus a random mix of the two at the same spend. A pairing must beat that whole curve: Anthropic's coding advisor pairing (90.1% at $2.92 per attempt) landed on its executor's own effort curve (88.4% at $1.38 on high, 91.1% at $4.11 on xhigh), and no commercial router beat the random mix. Picking one model per call site statically is 1.b.i.
2. If the outcome is checkable (tests, a schema, a sound verifier), try the simplest cascade first: run cheap and escalate only the failures. Opus 5.5 at low effort with its failures re-run at high solved about 97% for about $0.17 a task, against 95.3% for $0.29 with everything at high, a figure computed task by task from existing runs rather than run end to end. A checker that passes bad work lets those failures through, so audit it on a gold sample (9.c.iii).
3. Use two models, not a ladder: allowing three to five models did not raise mean test accuracy in 118 of 135 comparisons (at most +0.43 points), and even with true query difficulty known a two-model roster was within 1 point of the best roster of any size. Take the cheap model from the cost-accuracy frontier; in one 26-model set it trailed the strongest by 1.6 points at a 96% discount.
4. Measure the trigger before trusting it. For a confidence-score cascade, check how well the score separates the cheap model's errors from the strong model's: log-probability scores reached AUROC 0.63 to 0.80 for the cheap model's correctness yet beat random escalation at the same escalation rate (not the same cost) by only about 0.3 points on MATH. For a pre-call router, check it against the random two-model mix at the same spend (commercial routers trailed it by 1.0 to 10.5 points).
5. In agents, trigger consults on execution evidence and workflow phase rather than on the agent's own sense of being stuck, and cap them. On SWE-bench Verified, a learned policy at 2.78 consults per episode solved 48.0%, fixed triggers (before committing to an approach, before finishing, on stalls) 41.3%, random placement at similar volume 28.0%, and the orchestrating model left to choose (not volume-matched) made 0.41 consults per episode, 77% of them in the last third; on Terminal-Bench the learned policy only tied the fixed triggers (34.7% each). Do not re-run whole agent tasks on the strong model after a failed self-check: that cascade cost $59.68 against $45.90 for the strong model alone.
6. Watch the consult rate and whether the advice is used. Sonnet 5.5 at its default effort never consulted on 20 SWE-bench Pro problems; a pairing that consulted on most tasks at default effort consulted on few once its effort was lowered, and then scored below the executor alone; with the advisor tool attached but never called, GPQA cost 12% to 25% more (its definition is about 1,000 prompt tokens per request); ignored advice made up 58% of the learned policy's remaining SWE-bench failures. A consult that fires on most tasks can cost more than the strong model alone (1.8 times on chart reading).
7. Measure on held-out tasks with gold outcomes over several seeds: success and cost per completed task (counting failed cheap attempts and strong-model tokens) against every step-1 baseline, escalation or consult rate, and latency on escalated tasks; re-run at every model or price change.

## How to measure

- **experiment** (Tier 4): paired eval on held-out tasks with gold outcomes, 3 or more seeds: the escalation setup against the cheap and the strong model alone across effort settings and against a random mix of the two at the same spend; success, cost per completed task counting failed cheap attempts and strong-model tokens, escalation or consult rate, latency of escalated tasks
- **monitor**: escalation or consult rate by task type and when it fires, strong-model share of tokens and cost, success of escalated against kept tasks, advice the worker ignored, and true error on a gold-labeled audit sample the trigger never sees (9.c.iii); repeat the experiment at each model or price change

## Expected impact

- **Quality:** mixed, medium: gains where the trigger separates failures: two-model cascades +2.1 to 8.2 points over the best single model at the same budget, on average across budgets (Bouchard, May 2026); a learned consult policy recovered 44% to 81% of the cheap-to-strong gap on SWE-bench Verified, Terminal-Bench 2.1 and tau2-bench (Sowietzki, Oct 2026); FrugalGPT matched GPT-4 on three 2023 tasks (Chen, May 2023). Losses where it does not: six commercial routers 1.0 to 10.5 points below a random two-model mix at matched cost (Wang, Oct 2026); Anthropic's advisor +1.7 points on coding at the edge of noise, within noise on GPQA with no consults, 7 points lower on chart reading (Anthropic, Oct 2026)
- **Cost:** mixed, large: cheaper than the strong model alone when escalation is selective: 34.5% to 48.1% of its cost with a learned consult policy (Sowietzki, Oct 2026); 59.2% to 98.3% less at matched accuracy on 2023 classification tasks (Chen, May 2023); re-running only failures at high effort about 40% below an all-high run, computed from existing runs (Anthropic, Oct 2026). Dearer when escalation is frequent or task-level: the coding advisor pairing cost 2.1 times its executor alone, GPQA 12% to 25% more with no consults, and a pairing that consulted on 88% of chart tasks 1.8 times the strong model alone (Anthropic, Oct 2026); verify-then-escalate cost $59.68 against $45.90 for the strong model alone on SWE-bench Verified (Sowietzki, Oct 2026)
- **Performance:** mixed, small (unmeasured): each escalation or consult is a serial strong-model call on the critical path (about 1.4 per coding attempt), and a re-run failure takes two runs of wall-clock time (Anthropic, Oct 2026); work the cheap model finishes may be faster, which no source here times
- **Security:** none (unmeasured)
- **Governance:** improves, small (unmeasured): an explicit escalation policy can be read and audited (the learned policies consult in 4 to 9 of 24 states; Sowietzki, Oct 2026); count the strong model's tokens separately, since Anthropic reports advisor tokens per iteration rather than in the top-level usage totals
- **Brand:** none (unmeasured)

## Evidence (summary)

- paper Table 6 (2026-02): Names the practice as a known agent optimization; reports no measured effect for it.
- Lingjiao Chen, Matei Zaharia, James Zou, "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance"… (2023-05-09): "FrugalGPT can match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost". The 98% is the best of three datasets: the cost of matching the best…
- Anthropic, "Optimizing for cost and intelligence" (Claude Platform docs)… (2026-10-17): Internal agentic-coding benchmark, Opus 5.5 at high with a Fable 5.1 advisor: 90.1%, "1.7 points over the executor alone, at the edge of run-to-run noise", for $2.92 per attempt, about 2.1 times the executor alone, about 1.4 consults per…
- Pascal Sowietzki, Steffen Holter, Yannick Metz, Emil Kasper, Raphael Baur, Mennatallah El-Assady (ETH Zurich), "Ask Your Advisor: Learning… (2026-10-09): Success and run cost (mean of 3 seeds), executor alone / advisor alone / learned policy: SWE-bench Verified 18.0% $11.48 / 62.0% $45.90 / 48.0% $22.09; Terminal-Bench 2.1 21.3% $9.76 / 51.3% $60.99 / 34.7% $24.93; tau2-bench telecom 72.5%…
- Sam Wang, Julia White, Sahibzada Allahyar, Dhruv Atreja, Urchade Zaratiana, Kelton Zhang, "Dynamic LLM Routers are Often Misguided"… (2026-10-02): Every setting trailed the random two-model mix: from -1.0 ± 1.8 points (vLLM SR) to -10.5 ± 2.8 (Orca adaptive); OpenRouter auto -3.3 to -5.5, Not Diamond -4.1 to -8.8, Azure -2.2 to -8.4. Only the smallest gap (vLLM SR) is within error…
- …and 1 more sources in `library/entries/oracle-worker-escalation.yaml`.

## Caveats

The agent results are small or vendor-run: the learned consult policy was tested on one Gemini model pair in one framework, on 40 to 50 held-out tasks per benchmark with 3 seeds (success standard deviations up to 7.2 points) and outcome-screened development tasks, and Anthropic's advisor figures are internal, sometimes single runs on Claude models, from a living page whose August 2026 revision rated the advisor more favorably (closing 60% to 90% of the gap). The router and cascade studies are single-turn QA, math and code with list-price costs; the router study's random baseline uses a pair picked from the frontier with hindsight, and the cascade study tested only log-probability and trained scores on older open and GPT-4o-class models, not verbalized confidence, self-consistency or judges. FrugalGPT's 98% is its best of three 2023 classification datasets (59.2% and 73.3% on the other two). A cheap verifier used as the trigger can hide most of the cascade's errors, so measure true error outside it (9.c.iii).

## Related

- `aot-kit:model-and-effort-per-call-site` (1.b.i, Match the model and its effort to each call site and query class)
- `aot-kit:audit-verifier-cascade` (9.c.iii, Audit a verifier-gated cascade against a gold sample the verifier never sees)
- `aot-kit:samples-before-verification` (9.c.ii, Spend extra samples before extra verification: parallel attempts with a vote or judge; verify only where it pays)
- `aot-kit:plan-then-execute` (6.c.ii, Plan-then-execute)
- `aot-kit:multi-agent-for-breadth` (6.b.iii, Use multi-agent orchestration only for breadth-first, independent sub-tasks)
- `aot-kit:external-verifier-feedback` (9.a.i, Feed back a sound external verifier's verdict; never the model's own critique)
- `aot-kit:cache-stable-prefix` (3.b.i, Keep the prompt prefix cache-stable)
- `aot-kit:multi-agent-debate` (7.c.vi, Multi-agent debate)
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
