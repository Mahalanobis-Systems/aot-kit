# Changelog

All notable changes to aot-kit. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/) as described in
[CONTRIBUTING.md](CONTRIBUTING.md#versioning). A release lists the optimizations it adds or
changes, and credits whoever contributed them.

## Unreleased

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
