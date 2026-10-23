# Contributing to aot-kit

Thanks for helping. aot-kit is only as good as the evidence behind it, so new sources, corrections
and results from running these changes on real agents are the most valuable contributions. By
contributing, you agree that your contribution is licensed under the
[Apache License 2.0](LICENSE), the same as the project.

## Ways to contribute

- **Evidence for an optimization** (a paper, benchmark, engineering post or your own measured
  result), or **a new optimization**:
  [open an issue](https://github.com/Mahalanobis-Systems/aot-kit/issues/new?template=evidence.yml)
  with the source, or send a pull request that adds it to the entry yourself.
- **A correction**: a misquoted number, a citation that doesn't resolve, an entry that
  overstates its evidence. An issue or a pull request.
- **Building out a skill.** Every skill is a placeholder with a **To build** checklist (detect,
  apply, measure, evidence). A pull request that fills in one item for one skill is a good first
  contribution.
- **A problem with a skill** in Claude Code: an issue with what you ran and what it did.

Security problems go to [SECURITY.md](SECURITY.md) instead.

## How the library works

[`library/`](library/README.md) is the record: one entry per optimization, in
`library/entries/<slug>.yaml`. The skills, `catalog.yaml`, the optimization lists in the README
and the `start` skill, and the public library at
[mahalsystems.ai/aot/optimizations](https://mahalsystems.ai/aot/optimizations/) are all generated
from it. So:

- To change what a skill says about its optimization, change the entry, then run `make render`.
  Never edit a skill above its `End of the generated part` marker; CI fails if the generated
  files don't match the entries.
- Work on how a skill *applies* the change (its Detect, Apply and Measure steps) goes below that
  marker, by hand. When all of a skill's To build items are done, take the checklist out and
  `make render` drops its placeholder banner.

[library/README.md](library/README.md) describes every field of an entry.

## What makes good evidence

Every source in an entry's `evidence` is checked before it is merged. Check these yourself first:

- **It is the primary source.** Cite the paper, post or benchmark itself, not a thread or a
  summary about it. Non-paper sources are welcome: much of the library's practitioner evidence
  comes from engineering posts.
- **The citation resolves**, and the title, authors and date match.
- **The numbers are the source's own**, compared like for like: same grader, same budget, all
  seeds, not the abstract's best case. Put the conditions (model, benchmark, n) in `conditions`
  and where in the source they are in `locator`.
- **Say whose claim it is.** A vendor describing its own product is evidence, but a weaker kind
  than an independent team's measurement. When a source describes a practice without a number,
  add it with `measured: false`.
- **Contradicting evidence is as welcome as supporting evidence.** Mark it
  `direction: contradicts` (or `mixed`). An entry's advice changes when newer evidence actually
  contradicts it, not because its sources are old (review policy B in
  [library/README.md](library/README.md)).

Never write a number the source doesn't contain. If you ran the change on your own agent, say so,
describe the agent and the eval in a sentence, and give the before and after.

## Writing or changing an entry

- **A new optimization** takes the next free numeral in its home (first) category, e.g. `2.a.iv`.
  Ids are never reused, including former ones, so they are sparse. Use `status: outline` unless
  you can fill `how`, `impact`, `measure` and `evidence`, which makes it a `card`. First check it
  isn't already an entry, a pattern an entry absorbs (`absorbs`), or in `excluded.yaml`; if it is
  the same change, add evidence to that entry instead.
- **Tiers.** A new entry's tier is `proposed: true`. Only a maintainer confirms a tier.
- **Impact** rates all six dimensions. Use `unknown` rather than guess, and `basis: evidence`
  only when the entry's own sources back the rating.
- Keep `levers` (at most three, most important first), `domains` and `evidence_domains` honest:
  evidence domains are where the change was measured, not where it might apply.
- **US English** in everything you write (behavior, labeled, summarize). Quotations and titles
  stay as published.

## Making a change

1. Fork the repository and create a branch from `main`.
2. Edit the entry (or the hand-written part of a skill).
3. Run the checks:

   ```bash
   make render     # regenerate the skills, catalog.yaml and the lists
   make check      # schema and cross-checks; fails if anything generated is stale
   uv run --no-project --with pyyaml --with jsonschema --with pytest python -m pytest -q
   ```

   They need [uv](https://docs.astral.sh/uv/); nothing else to install.
4. For a change to a skill, try it in Claude Code on a real or toy agent:
   `claude --plugin-dir /path/to/your/checkout` loads your working copy instead of the released
   plugin.
5. Add a line under `## Unreleased` in [CHANGELOG.md](CHANGELOG.md): which optimization, what
   changed, and the source.
6. Open a pull request. CI runs the checks, the tests and the plugin manifest validator.

## How contributions are decided

Maintainers read new issues and pull requests every week, check each source as above, and
decide together what changes the library. We may ask for changes, or edit the wording of an
entry so it reads like the rest; the substance and the credit stay yours. Accepted changes go
out in that week's release, and the changelog and release notes credit you by GitHub handle.

Working on this repository with Claude Code picks up `.claude/CLAUDE.md`, which repeats these
rules.

## Versioning

aot-kit follows [Semantic Versioning](https://semver.org/). While the version is `0.x`:

- **Minor** (`0.2.0`): new optimizations, new evidence that changes what an entry advises, and
  any breaking change. Breaking means something that pointed at aot-kit stops working: a skill
  renamed or removed (it is a slash command), an id changed, or a change to the entry schema or
  to `library.json` that its readers must follow. The changelog says what to change.
- **Patch** (`0.1.1`): corrections and wording that change no advice, and fixes to the tooling.

Most weeks have one minor release. From `1.0.0`, breaking changes take a major version.

## Releasing

Maintainers release from `main`. Claude Code offers users an update only when the plugin's
`version` changes, and the marketplace entry installs the plugin from its release tag, so
unreleased work on `main` never reaches users.

1. Make sure `## Unreleased` in CHANGELOG.md describes the release.
2. On a clean branch from `main`, run:

   ```bash
   python3 scripts/release.py 0.2.0
   ```

   It writes the version to `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
   (the version and the `ref` the plugin installs from, `aot-kit--v0.2.0`), and moves the
   `Unreleased` notes under `## 0.2.0 — <date>`.
3. Open a pull request titled `Release 0.2.0`, and merge it when CI passes.
4. On merge, the [release workflow](.github/workflows/release.yml) tags the merge commit
   `aot-kit--v0.2.0` and publishes a GitHub release with the changelog section and
   `library.json` attached. Users get it with `claude plugin marketplace update aot-kit` and
   `claude plugin update aot-kit@aot-kit` (then a restart), or automatically if they turned on
   auto-update for the marketplace.

If the workflow fails, fix the cause and re-run it from the Actions tab (it skips a tag that
already exists). Never move or delete a published tag: release a new patch version instead.
