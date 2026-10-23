# aot-kit: working on this repo

- `library/` is the record of every optimization: one entry per skill in
  `library/entries/<slug>.yaml`, where the slug is the skill's name. Change an optimization by
  changing its entry, then `make render`: it regenerates each skill's frontmatter and generated
  part, `catalog.yaml`, and the lists in `README.md` and the `start` skill. Never edit those by
  hand; `make check` (CI) fails when they are out of date. Keep ids and slugs stable; ids are
  sparse on purpose (see `library/README.md`).
- A skill's hand-written part is everything after its end-of-generated-part marker. A new entry
  gets a new skill from `make render`; a skill with no entry is an error.
- The website (demand-gen) and aot-engine are downstream: they take the library from a release
  (`tools/build_site.py` builds `dist/library.json`). Nothing here reads from them.
- Skills are placeholders until their **To build** checklist is done. When you fill one in, take
  the checklist out of the hand-written part; `make render` then drops the placeholder banner
  and the word "Placeholder." from the description.
- A pattern's tier is marked `proposed: true` in its entry (`tier_proposed` in `catalog.yaml`)
  until a maintainer with the evidence confirms it.
- Measurement belongs to aot-evals: a skill says what to measure and at which tier's evidence
  gate, and hands the run to `aot-evals:run` rather than reimplementing it.
- Every change a user or a reader of the website would notice gets a line under `## Unreleased`
  in CHANGELOG.md: which optimization, what changed, the source, and who contributed it.
  Releases follow CONTRIBUTING.md ("Versioning", "Releasing"); never move a published tag.
