"""The library and what is generated from it (library/README.md, tools/)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


render = load("render_skills")
validate = load("validate")


def test_the_library_validates():
    assert validate.validate() == 0


def test_everything_generated_is_up_to_date():
    # The same as `make check`: edit library/entries/, then `make render`.
    result = subprocess.run([sys.executable, str(ROOT / "tools" / "render_skills.py"), "--check"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def entry_and_context():
    es, vocab, _ = render.load()
    by_id = {e["id"]: e for e in es}
    return es[0], by_id, vocab


def test_a_skill_keeps_its_hand_written_part():
    e, by_id, vocab = entry_and_context()
    current = render.skill(e, by_id, vocab, None)
    edited = current.replace(render.TO_BUILD, "## Apply\n\n1. Do the thing.\n")
    out = render.skill(e, by_id, vocab, edited)
    assert out.endswith(render.END + "\n\n## Apply\n\n1. Do the thing.\n")


def test_taking_out_to_build_ends_the_placeholder():
    e, by_id, vocab = entry_and_context()
    placeholder = render.skill(e, by_id, vocab, None)
    assert "Placeholder." in placeholder.split("---")[1]
    assert "> **Placeholder.**" in placeholder
    built = render.skill(e, by_id, vocab, placeholder.replace(render.TO_BUILD, "## Apply\n\nSteps.\n"))
    assert "Placeholder" not in built


def test_a_new_entry_gets_a_placeholder_skill():
    e, by_id, vocab = entry_and_context()
    out = render.skill(e, by_id, vocab, None)
    assert out.startswith(f"---\nname: {e['slug']}\n")
    assert out.endswith(render.TO_BUILD)


def test_the_site_data_is_stamped_and_complete(tmp_path):
    out = tmp_path / "library.json"
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_site.py"), "--out", str(out),
                    "--today", "2026-10-23"], check=True, capture_output=True)
    doc = json.loads(out.read_text())
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert doc["version"] == plugin["version"]
    assert doc["commit"] and doc["generated"] == "2026-10-23"
    slugs = {p.stem for p in (ROOT / "library" / "entries").glob("*.yaml")}
    assert set(doc["entries"]) == slugs
    assert {"levers", "domains", "tiers", "categories"} <= set(doc["vocabulary"])
