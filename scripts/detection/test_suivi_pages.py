#!/usr/bin/env python3
"""Vérifie que chaque page de suivi a une section « timeline » dont les <div> sont équilibrés.

Un <div> fermé en trop ferme le conteneur de la page : la version suivante s'affiche alors
collée au bord de l'écran, hors marges (cas réel du 9 octobre 2026 sur « Taux : marche arrière »).

    python3 -m unittest scripts/detection/test_suivi_pages.py
"""
import re
import unittest
from pathlib import Path

SUIVI = Path(__file__).resolve().parents[2] / "suivi"


class TestSuiviPages(unittest.TestCase):
    def test_timeline_equilibree(self):
        pages = sorted(SUIVI.glob("*.html"))
        self.assertTrue(pages)
        for page in pages:
            texte = page.read_text(encoding="utf-8")
            debut = texte.index('<section class="timeline">')
            fin = texte.index('<section class="follow-block"')
            segment = texte[debut:fin]
            ouverts = len(re.findall(r"<div\b", segment))
            fermes = len(re.findall(r"</div>", segment))
            self.assertEqual(ouverts, fermes, f"{page.name} : {ouverts} <div> ouverts, {fermes} fermés dans la timeline")

    def test_chaque_version_dans_le_conteneur(self):
        """Chaque .version doit rester à l'intérieur du <div class="wrap"> de la timeline."""
        for page in sorted(SUIVI.glob("*.html")):
            texte = page.read_text(encoding="utf-8")
            segment = texte[texte.index('<section class="timeline">'):texte.index('<section class="follow-block"')]
            profondeur = 0
            for ligne in segment.split("\n"):
                if 'class="version' in ligne and 'class="version-' not in ligne:
                    self.assertGreaterEqual(profondeur, 1, f"{page.name} : une version sort du conteneur")
                profondeur += len(re.findall(r"<div\b", ligne)) - len(re.findall(r"</div>", ligne))


if __name__ == "__main__":
    unittest.main()
