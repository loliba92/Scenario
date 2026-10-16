"""Tests de « L'enjeu en clair » (16 octobre 2026) : exigé sur les sujets
scientifiques/techniques, rendu avant les faits, plancher de complexité."""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_html  # noqa: E402
import generate_daily_edition as g  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BRIEF = ROOT / "editorial-briefs" / "2026-10-16.json"
CONTENT = ROOT / "editorial-previews" / "2026-10-16.content.json"


def test_enjeu_exige_sur_sujet_scientifique():
    brief = g.load_brief(str(BRIEF))
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    assert g.validate_content_schema(content, brief) == []
    sans = copy.deepcopy(content)
    del sans["enjeu_en_clair"]
    errs = g.validate_content_schema(sans, brief)
    assert any(e.startswith("enjeu_en_clair") for e in errs)


def test_enjeu_trop_court_refuse():
    brief = g.load_brief(str(BRIEF))
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    content["enjeu_en_clair"] = {"lead": "Court.", "text": "Trop court."}
    assert any("mots" in e for e in g.validate_content_schema(content, brief))


def test_plancher_complexite_sujet_scientifique(tmp_path):
    brief = json.loads(BRIEF.read_text(encoding="utf-8"))
    brief["sujet"]["complexite"] = 3
    p = tmp_path / "brief.json"
    p.write_text(json.dumps(brief, ensure_ascii=False), encoding="utf-8")
    loaded = g.load_brief(str(p))
    assert loaded["sujet"]["complexite"] == 4
    assert loaded["sujet"]["complexite_recherche"] == 3


def test_rendu_avant_les_faits():
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    html = build_html.build_hero(content, "2026-10-16", photo={"hero_image_url": "x", "alt": "x"})
    assert html.index("L'enjeu en clair") > html.index("Les faits")
    assert html.index("L'enjeu en clair") < html.index('<p class="dek">')


if __name__ == "__main__":
    import tempfile
    test_enjeu_exige_sur_sujet_scientifique()
    test_enjeu_trop_court_refuse()
    test_plancher_complexite_sujet_scientifique(Path(tempfile.mkdtemp()))
    test_rendu_avant_les_faits()
    print("OK")
