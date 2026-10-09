#!/usr/bin/env python3
"""Tests de suivi_home.py (bloc « Le dernier suivi » de l'accueil). Sans réseau.

    python3 -m unittest scripts/edition/test_suivi_home.py
"""
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import suivi_home as sh  # noqa: E402

PAGE = """<html><body><h1>Sujet : où en est-on ?</h1>
<div class="version"><div class="version-head"><span class="version-tag">V0 — Point de départ</span>
<span class="version-date">1 septembre 2026</span></div></div>
<div class="version is-update"><div class="version-head"><span class="version-tag">V1 — Mise à jour</span>
<span class="version-date">{d}</span></div>
<div class="version-content"><div class="version-content-inner"><p>Premier fait. Deuxième fait important. Troisième fait qui n'apparaît pas forcément.</p>
<div class="mini-scenario"><p>à ignorer</p></div></div></div></div>
</body></html>"""

INDEX = ('<body><section class="featured-article"><div class="wrap">édition</div></section>\n\n'
         '<section class="hero">hero</section></body>')


class TestSuiviHome(unittest.TestCase):
    def test_date_fr(self):
        self.assertEqual(sh._date_fr("1er septembre 2026"), date(2026, 9, 1))
        self.assertEqual(sh._date_fr("12 décembre 2026"), date(2026, 12, 12))
        self.assertIsNone(sh._date_fr("{DATE DE CETTE MISE À JOUR}"))

    def test_debut_garde_des_phrases_entieres(self):
        t = "Un fait. Deux faits. " + "Trois faits très longs " * 20 + "."
        d = sh._debut(t, 60)
        self.assertTrue(d.endswith("."))
        self.assertLessEqual(len(d), 60)

    def test_dernier_suivi_prend_le_plus_recent(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "ancien.html").write_text(PAGE.format(d="4 septembre 2026"), encoding="utf-8")
            (tmp / "recent.html").write_text(PAGE.format(d="12 septembre 2026"), encoding="utf-8")
            (tmp / "_gabarit.html").write_text(PAGE.format(d="30 septembre 2026"), encoding="utf-8")
            s = sh.dernier_suivi(tmp)
            self.assertEqual(s["slug"], "recent")
            self.assertEqual(s["maj"], 1)
            self.assertIn("Premier fait", s["fait"])

    def test_rendu_et_injection_idempotente(self):
        s = {"slug": "x", "titre": "Titre : test ?", "date": date(2026, 9, 12), "maj": 1,
             "fait": "Un fait. Un autre.", "image": "", "rubrique": "Économie"}
        bloc = sh.rendre(s)
        self.assertIn("mis à jour le 12 sept.", bloc)
        self.assertIn("Économie ·", bloc)
        self.assertIn("&nbsp;?", bloc)
        un = sh.injecter(INDEX, bloc)
        self.assertEqual(un, sh.injecter(un, bloc))               # relancer ne change rien
        self.assertLess(un.index("édition"), un.index("Le dernier suivi"))
        self.assertLess(un.index("Le dernier suivi"), un.index("hero"))
        self.assertEqual(sh.injecter(un, ""), sh.injecter(INDEX, ""))  # sans bloc : retrait propre

    def test_ne_leve_jamais(self):
        orig = sh.dernier_suivi
        sh.dernier_suivi = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("panne"))
        try:
            self.assertEqual(sh.bloc_dernier_suivi(), "")
        finally:
            sh.dernier_suivi = orig


if __name__ == "__main__":
    unittest.main()
