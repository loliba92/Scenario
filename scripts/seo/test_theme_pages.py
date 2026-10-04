#!/usr/bin/env python3
"""Tests de scripts/seo/generate_theme_pages.py (pages thèmes en cartes)."""
import unittest

import generate_theme_pages as g

ARCHIVES = """
<tr data-domain="international" data-date="2026-09-28">
  <td class="col-title"><a href="archives/2026-09-28.html" title="Une question &#x27;ouverte&#x27; ?">Un titre</a></td>
  <td class="col-eval"><span class="eval-badge eval-stable" data-kind="stable"><span class="eval-label">Stable</span><span class="eval-pct">50%</span></span></td>
  <td class="col-france"><span class="france-scale" title="Plutôt défavorable"></span></td>
</tr>
"""


class ParseEntries(unittest.TestCase):
    def test_champs_enrichis(self):
        old = g.ARCHIVES_HTML
        import tempfile, pathlib
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "a.html"
            f.write_text(ARCHIVES, encoding="utf-8")
            g.ARCHIVES_HTML = f
            try:
                e = g.parse_entries()[0]
            finally:
                g.ARCHIVES_HTML = old
        self.assertEqual(e["question"], "Une question 'ouverte' ?")
        self.assertEqual((e["kind"], e["label"]), ("stable", "Stable"))
        self.assertEqual(e["france"], "Plutôt défavorable")


class RenderPage(unittest.TestCase):
    def setUp(self):
        self.pieces = g.build_shared_pieces()
        base = {"display_date": "28.09.2026", "href": "archives/2026-09-28.html", "registre": None,
                "domain_slug": "international", "question": "", "kind": "degrade", "label": "Dégradé",
                "france": "Assez favorable"}
        self.entries = [dict(base, iso_date="2026-09-28", title="A"),
                        dict(base, iso_date="2026-09-21", title="B", display_date="21.09.2026")]

    def page(self):
        return g.render_page(g.DOMAINS[2], self.entries, *self.pieces, counts={"international": 2})

    def test_une_et_cartes(self):
        h = self.page()
        self.assertIn('class="theme-featured"', h)
        self.assertEqual(h.count('class="theme-card"'), 1)
        self.assertIn("archive-thumbs/2026-09-21.jpg", h)

    def test_selecteur_de_theme(self):
        h = self.page()
        self.assertEqual(h.count('class="theme-chip"'), len(g.DOMAINS) + 2)  # + archives, recherche
        self.assertIn('aria-current="page">International', h)

    def test_chemins_relatifs(self):
        h = self.page()
        self.assertNotIn('src="assets/', h)

    def test_question_identique_au_titre_masquee(self):
        self.entries[0]["question"] = "A ?"
        self.assertNotIn('class="q"', self.page())


if __name__ == "__main__":
    unittest.main()
