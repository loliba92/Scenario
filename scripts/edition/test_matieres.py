#!/usr/bin/env python3
"""Tests des liens vers les pages « matières » (accueil et bas d'édition)."""
import unittest

import build_html as b


class Matieres(unittest.TestCase):
    def test_accueil_a_les_six_matieres(self):
        h = b.build_home_hero()
        self.assertIn('id="matieres"', h)
        for slug in b.THEME_SLUG_LABELS:
            self.assertIn(f'href="themes/{slug}.html"', h)
        self.assertNotIn("& ", h.split('id="matieres"')[1])  # & échappé

    def test_bas_d_edition_exclut_le_jour_et_limite_a_deux(self):
        h = b.build_theme_more({"sujet": {"domain": "international"}}, "2026-10-05")
        self.assertEqual(h.count('class="related-articles-item"'), 2)
        self.assertIn('href="themes/international.html"', h)
        h = b.build_theme_more({"sujet": {"domain": "international"}}, "2026-09-28")
        self.assertNotIn("archives/2026-09-28.html", h)

    def test_domaine_sans_page_theme_donne_rien(self):
        self.assertEqual(b.build_theme_more({"sujet": {"domain": "sport"}}, "2026-10-05"), "")
        self.assertEqual(b.build_theme_more({}, "2026-10-05"), "")


if __name__ == "__main__":
    unittest.main()
