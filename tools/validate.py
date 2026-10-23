#!/usr/bin/env python3
"""The optimization library: schema-check every file, cross-check ids, and report.

    validate.py            schema + cross-checks (the default; what `make validate` runs)
    validate.py stats      counts by kind, status, tier, lever and domain

library/ is the record of every agent optimization in AOT. The skills, catalog.yaml and the
website's data are generated from it (tools/render_skills.py, tools/build_site.py).
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1] / "library"
SCHEMA = ROOT / "schema"


def load(name: str):
    return yaml.safe_load((ROOT / name).read_text())


def entries() -> list[dict]:
    return [
        yaml.safe_load(p.read_text()) | {"_file": p.name}
        for p in sorted((ROOT / "entries").glob("*.yaml"))
    ]


def check(doc, schema_file: str, label: str, errors: list[str]) -> None:
    schema = yaml.safe_load((SCHEMA / schema_file).read_text())
    for err in jsonschema.Draft202012Validator(schema).iter_errors(doc):
        path = "/".join(str(p) for p in err.absolute_path)
        errors.append(f"{label}: {path}: {err.message[:200]}")


def validate() -> int:
    errors: list[str] = []
    vocab = load("vocabulary.yaml")
    check(vocab, "vocabulary.schema.json", "vocabulary.yaml", errors)
    check(load("excluded.yaml"), "excluded.schema.json", "excluded.yaml", errors)
    check(load("library.yaml"), "library.schema.json", "library.yaml", errors)
    check(load("vero-taxonomy.yaml"), "vero-taxonomy.schema.json", "vero-taxonomy.yaml", errors)

    levers = {lv["id"] for lv in vocab["levers"]}
    domains = {d["id"] for d in vocab["domains"]}
    cat_lever = {i["id"]: i["lever"] for c in vocab["categories"] for i in c["items"]}
    cat_prefix = {i["id"]: f"{c['number']}.{i['letter']}" for c in vocab["categories"] for i in c["items"]}
    if len({c["number"] for c in vocab["categories"]}) != len(vocab["categories"]):
        errors.append("vocabulary.yaml: two category families share a number")
    for c in vocab["categories"]:
        if len({i["letter"] for i in c["items"]}) != len(c["items"]):
            errors.append(f"vocabulary.yaml: two sub-categories of {c['id']} share a letter")
    for item, lever in cat_lever.items():
        if lever not in levers:
            errors.append(f"vocabulary.yaml: category {item} sits under unknown lever {lever!r}")

    es = entries()
    for e in es:
        f = e.pop("_file")
        check(e, "entry.schema.json", f, errors)
        if f != f"{e.get('slug')}.yaml":
            errors.append(f"{f}: file name does not match slug {e.get('slug')!r}")
        for lv in e.get("levers", []):
            if lv not in levers:
                errors.append(f"{f}: unknown lever {lv!r}")
        ds = e.get("domains", [])
        if "general" in ds and len(ds) > 1:
            errors.append(f"{f}: `general` must stand alone in domains")
        for d in ds:
            if d != "general" and d not in domains:
                errors.append(f"{f}: unknown domain {d!r}")
        for d in e.get("evidence_domains", []):
            if d not in domains:
                errors.append(f"{f}: unknown evidence domain {d!r}")
        for c in e.get("categories", []):
            if c not in cat_lever:
                errors.append(f"{f}: unknown category {c!r}")
            elif cat_lever[c] not in e.get("levers", []):
                # Categories are the finer level under a lever, so the lever must be listed too.
                errors.append(
                    f"{f}: category {c} sits under lever {cat_lever[c]!r}, which the entry does not list"
                )
        cats = e.get("categories", [])
        if not cats:
            errors.append(f"{f}: no category, so no home for its number")
        elif cats[0] in cat_prefix and not str(e.get("id", "")).startswith(cat_prefix[cats[0]] + "."):
            # The id is the library number, built on the home (first) category: 2.a.ii lives in 2.a.
            errors.append(f"{f}: id {e.get('id')} is not under its home category {cats[0]} ({cat_prefix[cats[0]]})")
        if e.get("status") == "card" and not e.get("how"):
            errors.append(f"{f}: status card but no `how`")
        own = {t["tier"] for t in e.get("tiers", [])}
        for m in e.get("measure", []):
            if "tier" in m and m["tier"] not in own:
                errors.append(f"{f}: measure tier {m['tier']} is not among its tiers {sorted(own)}")

    # Every id (library number), current or former, belongs to one entry and is never reused.
    numbered: dict[str, str] = {}
    for e in es:
        for n in [e.get("id")] + e.get("former_ids", []):
            if n in numbered:
                errors.append(f"id {n} claimed by both {numbered[n]} and {e['slug']}")
            numbered[n] = e["slug"]

    # Every legacy T/P id is owned exactly once: by an entry, as a pattern an entry absorbs, or in
    # excluded.yaml.
    owner: dict[str, str] = {}

    def own(i: str, by: str) -> None:
        if i in owner:
            errors.append(f"id {i} claimed by both {owner[i]} and {by}")
        owner[i] = by

    for e in es:
        if e.get("legacy_id"):
            own(e["legacy_id"], e["slug"])
        for a in e.get("absorbs", []):
            own(a["legacy_id"], f"{e['slug']} (absorbed)")
    for x in load("excluded.yaml")["excluded"]:
        if x["id"][0] in "TP" and len(x["id"]) == 3:
            own(x["id"], "excluded.yaml")
    slugs = Counter(e["slug"] for e in es)
    errors += [f"duplicate slug {s}" for s, n in slugs.items() if n > 1]
    for e in es:
        for r in e.get("related", []):
            if r not in numbered or r == e["id"]:
                errors.append(f"{e['slug']}.yaml: related {r} is not another entry's id")

    for msg in errors:
        print(f"FAIL: {msg}", file=sys.stderr)
    if errors:
        print(f"{len(errors)} error(s)", file=sys.stderr)
        return 1
    absorbed = sum(len(e.get("absorbs", [])) for e in es)
    print(f"OK: {len(es)} entries ({absorbed} absorbed patterns), {len(owner)} ids owned")
    return 0


def stats() -> int:
    es = entries()
    print(f"entries: {len(es)}")
    for label, key in [("kind", "kind"), ("status", "status")]:
        print(
            f"  by {label}: "
            + ", ".join(f"{k} {n}" for k, n in Counter(e[key] for e in es).most_common())
        )
    print(
        "  by tier: "
        + ", ".join(
            f"{k} {n}"
            for k, n in sorted(Counter(t["tier"] for e in es for t in e["tiers"][:1]).items())
        )
    )
    for label, key in [
        ("lever", "levers"),
        ("domain", "domains"),
        ("evidence domain", "evidence_domains"),
    ]:
        c = Counter(v for e in es for v in e[key])
        print(f"\nby {label}:")
        for k, n in c.most_common():
            print(f"  {k:22s} {n}")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    raise SystemExit({"validate": validate, "stats": stats}[cmd]())
