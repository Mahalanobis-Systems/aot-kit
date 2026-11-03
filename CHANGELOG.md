# Changelog

All notable changes to aot-kit. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/) as described in
[CONTRIBUTING.md](CONTRIBUTING.md#versioning). A release lists the optimizations it adds or
changes, and credits whoever contributed them.

## Unreleased

## 0.3.0 — 2026-11-03

- 11 cards are rewritten, with a sharper summary and how-to and 53 new sources (each dated, quoted
  and located in its entry): size run budgets (7.b.iii, 5 new sources; set caps from successful
  runs and show the agent the budget left), make the final answer extractable (9.b.i, 4), restructure
  the system prompt (3.a.iv, 4), link large schemas by exploration (8.b.ii, 5; first check the
  schema really is too large to load whole), tune the search tool (8.b.i, 4; a reader that keeps the
  pages it opens), bound tool output (2.c.i, 5; cut by whole lines or records, never by character
  position), route metric questions through a semantic layer (7.a.i, 12), verify citations claim by
  claim (9.a.ii, 4), triage false success with a trained detector (9.b.ii, 4; never show the judge
  the agent's own success claim), and surface information the source holds but the agent cannot read
  (8.a.ii, 4). Contributed by the Mahalanobis Systems maintainers.
- 9.c.i is narrowed and renamed "Drop ad-hoc test-writing prompts; tell test-heavy models not to
  write tests" (was "Don't prompt agents to write their own tests"), with 2 new sources; a test
  written before the fix and shown to fail is a different change. Contributed by the Mahalanobis
  Systems maintainers.

## 0.2.0 — 2026-10-26

- 20 optimizations go from outline to full card, with a summary, a how-to and the signals that say
  each applies, backed by 122 new sources (each dated, quoted and located in its entry): few-shot
  examples (3.a.i), self-discover reasoning (3.c.i), filesystem checkpoints (4.b.i),
  initializer and maintainer agents (4.b.ii), episodic memory (4.c.i), skill library (4.c.ii),
  discrete phase separation (5.c.i), oracle-worker escalation (6.a.i), parallel read-only tools
  (6.b.i), LLM map-reduce (6.b.ii), code-then-execute (6.c.i), plan-then-execute (6.c.ii),
  reflection loop (7.c.i), self-critique evaluator (7.c.ii), graph of thought (7.c.iv),
  language agent tree search (7.c.v), multi-agent debate (7.c.vi), tree of thought (7.c.vii),
  continuous task loop (7.d.i) and inversion of control (7.d.ii). Contributed by the
  Mahalanobis Systems maintainers.
- 5 cards gain new sources: model and effort per call site (1.b.i, 3 sources), fail-soft tools
  (2.b.i, 4), multi-window task state (4.b.iii, 1: Knowledge Graph of Thoughts on GAIA, a mixed
  result), evaluator-optimizer loop (7.c.iii, 4), and samples before verification (9.c.ii, 1: Ghosal
  et al. 2025, "Mirage of Test-Time Scaling"), whose how-to now says that at a fixed thinking budget,
  parallel traces with a majority vote beat forcing one trace to think longer. Contributed by the
  Mahalanobis Systems maintainers.

## 0.1.0 — 2026-10-23

The first public release.

- 60 agent optimizations, one Claude Code skill each, listed by evidence tier: 3 Hygiene,
  14 Reliability, 22 Tuning and 21 Restructuring. Each skill says what the change is, the signals
  in an agent's code, traces and eval results that say it applies, how to measure it at its tier's
  evidence gate (with [aot-evals](https://github.com/Mahalanobis-Systems/aot-evals)), its expected
  impact, and its evidence. All are placeholders for now: each ends with a **To build** checklist
  for detecting, applying and measuring the change.
- `library/` holds the record behind them: one entry per optimization with every source of
  evidence, dated and quoted in its own numbers. The skills and the public library at
  [mahalsystems.ai/aot/optimizations](https://mahalsystems.ai/aot/optimizations/) are generated
  from it, and each release attaches its data as `library.json`.
- Contributions are welcome: new evidence, corrections and results from real agents. See
  [CONTRIBUTING.md](CONTRIBUTING.md).
