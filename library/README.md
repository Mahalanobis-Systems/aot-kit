# library/

The record of every agent optimization in AOT, one entry per optimization. Everything else is
generated from it: the skills, `catalog.yaml` and the optimization lists in the README and the
`start` skill (`tools/render_skills.py`), and the data behind the public library at
[mahalsystems.ai/aot/optimizations](https://mahalsystems.ai/aot/optimizations/)
(`tools/build_site.py`). New optimizations and new evidence land here first.

The library enumerates optimizations. It does not promise that any of them helps a given agent.
Every entry records two things separately: where it applies, and where its evidence actually comes
from.

## Files

| Path | What it holds |
|---|---|
| `entries/<slug>.yaml` | One optimization per file (`make stats` counts them). The slug is also the skill's name and the website URL |
| `vocabulary.yaml` | Levers, capability domains, the finer categories under each lever, and the four tiers |
| `excluded.yaml` | Ids that are deliberately not entries (optimizer-side practices), plus archived entries kept whole |
| `library.yaml` | VeRO's pattern-library sources and anti-patterns |
| `vero-taxonomy.yaml` | VeRO's two edit taxonomies, the vocabulary behind each entry's `provenance` |
| `schema/*.schema.json` | One JSON Schema per file kind |

## An entry

```yaml
id: 2.c.i                   # the library number: family.sub-category.numeral, from the home category
legacy_id: T02              # the id before 2026-10-19 (T = technique, P = pattern); history only
slug: bound-tool-output     # public name: file, skill, website URL
name: 'Bound tool output: ...'
kind: technique             # or pattern
status: card                # outline (no `how` yet) | card (full format)
tiers: [{tier: 3, why: ...}]          # patterns carry `proposed: true` until a maintainer confirms the tier
levers: [tool-surface, context]       # where the change lands, most important first
domains: [general]                    # domains it is specific to, or [general]
evidence_domains: [code-generation, tool-use]   # where its evidence comes from
categories: [tools.lean-returns, ...] # finer level; each one's lever must be listed in `levers`
summary / how / detect / measure / evidence / caveats / related
impact:                     # required: all six dimensions
  quality: {effect: improves, size: medium, when: ..., basis: evidence}
  cost / performance / security / governance / brand: {...}   # performance = speed and latency
  primary: [quality]        # optional: the one or two dimensions the change is mainly for
assessment: {qa, impact}    # patterns only: the first-pass, unmeasured assessment, kept as found
absorbs: [...]              # library patterns that are the same change, kept whole
provenance: {layer, origin, change_type, sub_type, harness_role, action, ...}
```

Each source in `evidence` is a citation of an outside work: `source` (with its URL), `task`,
`effect` in the source's own numbers, `date` (publication), `conditions` (model, benchmark, n),
`locator` (where in the source), `measured: false` when it only describes the practice, and
`direction: contradicts|mixed` when it cuts against the entry.

`impact` rates each dimension `improves|degrades|mixed|none|unknown`, sized `small|medium|large`.
`basis` is `evidence` when the entry's sources back the rating and `assessment` when it was
carried over from the pattern library's first-pass assessment (latency became performance,
low/medium/high became small/medium/large); it is left off only for `unknown`.

`assessment`, and the `assessment` of each pattern under `absorbs`, is that first pass: how one
would detect the pattern (in code, traces, evals, with a judge or probes), how to test it, and a
rough impact. It is unmeasured, and kept as found; it is raw material for a skill's Detect and
Measure steps, not a result.

`id` is the entry's library number: its home (first) category's family number and sub-category
letter (`number` and `letter` in `vocabulary.yaml`), then a roman numeral, so 2.c.i is the first
entry in 2.c. It is the only id anything new should use: `related`, cross-references in an entry's
text ("consolidate instead (2.a.i)"), the website, the skills. Ids are assigned once and never
reused, so they are sparse. A new entry takes the next free numeral in its home sub-category (after
any former id there too). If an entry's home category changes, it gets a new id there and the old
one moves to `former_ids`, which the website redirects.

`legacy_id` keeps the T/P id an entry had before 2026-10-19 (the T numbers began as VeRO's technique
ids). History still uses those codes and is left as written: absorbed patterns
(`absorbs[].legacy_id`) and `excluded.yaml`.
Codes like "VeRO T12" in evidence and assessments are VeRO's own.

`status` describes the entry's content, not the skill. A skill is a placeholder until its To build
checklist is done; that is tracked in the skill itself.

## Review policies

- **A. Detection says what to look for, not what a tool can compute today.** Probes (constructed
  cases) and judges are valid detection methods. A skill runs in the developer's own repo, where
  Claude can read the code, build a probe set or apply a judge. A signal no trace field carries
  today (question type, query class, a tool's trigger condition) is not a reason to drop or
  weaken an entry.
- **B. Evidence age is shown, not argued per entry.** Every source in `evidence` keeps its own
  `date`. The website shows it and labels sources over 12 months old as older evidence. An entry's
  wording is changed only when newer evidence actually contradicts it.

## Checking

```bash
make validate   # schema + cross-checks
make stats      # counts by kind, status, tier, lever, domain
make render     # regenerate the skills, catalog.yaml and the lists from the entries
make check      # validate, and fail if anything generated is out of date (what CI runs)
```
