#!/usr/bin/env python3
"""Build the website's data from library/: one JSON file the site (mahalsystems.ai) imports.

    build_site.py [--out dist/library.json] [--today YYYY-MM-DD]

The release workflow builds it and attaches it to the GitHub release; demand-gen pulls it from
there. It holds the vocabulary and every entry, stamped with the plugin version and the commit:

    {"version": "0.2.0", "commit": "abc1234", "generated": "YYYY-MM-DD",
     "vocabulary": {levers, domains, tiers, categories}, "entries": {slug: entry, ...}}

Shaping for readers happens here:
- VeRO shorthand ("paper §A.4", "repo figure_04", "blog tricks table") becomes a real citation
  with a link, keeping the shorthand as the locator.
- Each source in `evidence` keeps its date and is marked `older` past 12 months of `generated`.
- Retired-id markers such as "[from T21]" are dropped, and provenance stays out.
Which entries to show (all, or cards only) is the site's choice; every entry is here with its
`status`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "library"

VERO_PAPER = (
    'Scale AI, "VeRO: A Harness for Agents to Optimize Agents" (ICML 2026)',
    "https://arxiv.org/abs/2602.22480",
    "2026-02",
)
VERO_REPO = ("Scale AI, VeRO code release", "https://github.com/scaleapi/vero", None)
VERO_BLOG = (
    'Scale AI, "Can AI Agents Build Better AI Agents?"',
    "https://labs.scale.com/blog/vero",
    None,
)

RETIRED_MARKER = re.compile(r"\s*\[from T\d{2}\]")
URL_TAIL = re.compile(r",?\s*(https?://\S+?)[.,]?$")


def clean(text: str | None) -> str | None:
    if text is None:
        return None
    return RETIRED_MARKER.sub("", " ".join(str(text).split()))


def cite(row: dict) -> dict:
    src = " ".join(row["source"].split())
    locator = row.get("locator")
    date = row.get("date")
    url = None
    if src.startswith(("paper", "cookbook")):
        name, url, d = VERO_PAPER if src.startswith("paper") else VERO_REPO
        locator = "; ".join(x for x in (src, locator) if x)
        date = date or d
        src = name
    elif src.startswith("repo"):
        name, url, _ = VERO_REPO
        locator = "; ".join(x for x in (src.removeprefix("repo ").strip(), locator) if x)
        src = name
    elif src.startswith("blog"):
        name, url, _ = VERO_BLOG
        locator = "; ".join(x for x in (src.removeprefix("blog ").strip(), locator) if x)
        src = name
    else:
        m = URL_TAIL.search(src)
        if m:
            url = m.group(1)
            src = src[: m.start()].rstrip(" ,")
    return {
        "source": src,
        "url": url,
        "date": str(date) if date else None,
        "locator": clean(locator),
    }


def older(date: str | None, today: dt.date) -> bool:
    if not date:
        return False
    parts = [int(x) for x in date.split("-")] + [1, 1]
    return (today - dt.date(parts[0], parts[1], parts[2])).days > 365


def steps(how: str | None) -> list[str]:
    if not how:
        return []
    parts = re.split(r"(?:^|\s)\d\.\s", how.strip())
    return [clean(p) for p in parts if p.strip()]


def unmark(text):
    return re.sub(r"\[from [TP]\d{2}\]\s*", "", text) if text else text


def entry_json(e: dict, by_id: dict, vocab: dict, today: dt.date) -> dict:
    tiers = {t["tier"]: t for t in vocab["tiers"]}
    cat = {i["id"]: i["name"] for c in vocab["categories"] for i in c["items"]}
    t = e["tiers"][0]
    back = [x["id"] for x in by_id.values() if e["id"] in x.get("related", [])]
    related = []
    for rid in dict.fromkeys(e.get("related", []) + back):
        if rid == e["id"]:
            continue
        host = by_id.get(rid) or next(
            (h for h in by_id.values() for a in h.get("absorbs", []) if a["legacy_id"] == rid), None
        )
        if host and host["id"] != e["id"] and host["slug"] not in [r["slug"] for r in related]:
            related.append({"id": host["id"], "slug": host["slug"], "name": host["name"]})

    dims = {k: v for k, v in e["impact"].items() if k != "primary"}
    impact = {
        # true when the entry's main dimensions rest on its sources rather than the first-pass assessment
        "measured_basis": any(v.get("basis") == "evidence" for v in dims.values()),
        "primary": e["impact"].get("primary", []),
        "rows": [
            {
                "dimension": k,
                "effect": v["effect"],
                "size": v.get("size"),
                "when": clean(v.get("when")),
                "basis": v.get("basis"),
            }
            for k, v in dims.items()
        ],
    }
    if e.get("measure"):
        measure = [
            {"method": m["method"], "tier": m.get("tier"), "how": clean(m["how"])}
            for m in e["measure"]
        ]
    else:
        qa = e.get("assessment", {}).get("qa", {})
        measure = [
            {"method": k, "tier": None, "how": clean(qa[k])}
            for k in ("unit", "examples", "benchmark", "production")
            if qa.get(k)
        ]
    d = e["detect"]
    evidence = []
    for r in e.get("evidence", []):
        c = cite(r)
        evidence.append(
            c
            | {
                "task": clean(r.get("task")),
                "effect": clean(r["effect"]),
                "direction": r.get("direction", "supports"),
                "measured": r.get("measured"),
                "conditions": clean(r.get("conditions")),
                "older": older(c["date"], today),
            }
        )
    return {
        "id": e["id"],
        "legacy_id": e.get("legacy_id"),  # the id before 2026-10-19 (T35); not shown on the site
        "former_ids": e.get("former_ids", []),
        "slug": e["slug"],
        "name": e["name"],
        "kind": e["kind"],
        "status": e["status"],
        "tier": {
            "tier": t["tier"],
            "name": tiers[t["tier"]]["name"],
            "why": t["why"],
            "proposed": bool(t.get("proposed")),
        },
        "levers": e["levers"],
        "domains": e["domains"],
        "evidence_domains": e["evidence_domains"],
        "categories": [cat[c] for c in e["categories"]],
        "category_ids": e["categories"],  # the first is the entry's home in the library's left rail
        "summary": clean(e["summary"]),
        "how": steps(e.get("how")),
        "detect": {k: clean(d[k]) for k in ("static", "traces", "evals", "judge") if d.get(k)}
        | ({"probes": clean(d["probes"]["what"])} if d.get("probes") else {}),
        "impact": impact,
        "measure": measure,
        "evidence": evidence,
        # "[from T08]" marks a caveat inherited from a retired entry: provenance for the register,
        # noise for a reader.
        "caveats": unmark(clean(e.get("caveats"))),
        "also_covers": [{"name": a["name"]} for a in e.get("absorbs", [])],
        "related": related,
    }


def commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short=7", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "dist" / "library.json"))
    ap.add_argument("--today", default=dt.date.today().isoformat())
    args = ap.parse_args()
    today = dt.date.fromisoformat(args.today)

    vocab = yaml.safe_load((LIB / "vocabulary.yaml").read_text())
    by_id = {}
    for p in sorted((LIB / "entries").glob("*.yaml")):
        e = yaml.safe_load(p.read_text())
        by_id[e["id"]] = e
    docs = {e["slug"]: entry_json(e, by_id, vocab, today) for e in by_id.values()}
    used_domains = {d for x in docs.values() for d in x["domains"] + x["evidence_domains"]}
    vocabulary = {
        "levers": [
            {"id": v["id"], "name": v["name"], "covers": v["covers"]} for v in vocab["levers"]
        ],
        "domains": [
            {"id": v["id"], "name": v["name"], "covers": v["covers"]}
            for v in vocab["domains"]
            if v["id"] in used_domains
        ],
        "tiers": [{k: v for k, v in t.items() if k != "default_measure"} for t in vocab["tiers"]],
        # The families and their sub-categories, in order, with their stable numbers and letters
        # (2, 2.a): the library's left rail and every entry's number (2.a.ii) are built on them.
        "categories": [
            {
                "id": c["id"],
                "number": c["number"],
                "name": c["name"],
                "summary": c.get("summary"),
                "items": [
                    {
                        "id": i["id"],
                        "letter": i["letter"],
                        "name": i["name"],
                        "summary": i.get("summary"),
                        "lever": i["lever"],
                    }
                    for i in c["items"]
                ],
            }
            for c in vocab["categories"]
        ],
    }
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    doc = {
        "version": plugin["version"],
        "commit": commit(),
        "generated": today.isoformat(),
        "vocabulary": vocabulary,
        "entries": dict(sorted(docs.items())),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"OK: {len(docs)} entries, version {doc['version']} ({doc['commit']}) -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
