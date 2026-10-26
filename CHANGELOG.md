# Changelog

All notable changes to aot-kit. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/) as described in
[CONTRIBUTING.md](CONTRIBUTING.md#versioning). A release lists the optimizations it adds or
changes, and credits whoever contributed them.

## Unreleased

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
