"""Tests de la purge du plan Actualités (fenêtre de 2 jours, marge contre la dérive horaire, entrées FR et EN)."""
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import generate_post_edition as g

NS = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">')


def entree_fr(jour, publie):
    return (f"<url><loc>https://lesscenarios.fr/archives/{jour}.html</loc><news:news><news:publication>"
            f"<news:name>Scénario</news:name><news:language>fr</news:language></news:publication>"
            f"<news:publication_date>{publie.isoformat(timespec='seconds')}</news:publication_date>"
            f"<news:title>t</news:title></news:news></url>")


class TestPurgeFrancais(unittest.TestCase):
    def test_entree_de_47h59_est_purgee(self):
        maintenant = datetime.now(g.PARIS_TZ)
        vieille = maintenant - timedelta(hours=47, minutes=59)
        recente = maintenant - timedelta(hours=20)
        xml = f"{NS}{entree_fr('2026-10-09', vieille)}{entree_fr('2026-10-10', recente)}</urlset>"
        out = g.update_sitemap_news_xml(xml, "2026-10-11", "Titre")
        self.assertNotIn("2026-10-09", out)
        self.assertIn("2026-10-10", out)
        self.assertIn("2026-10-11", out)

    def test_fuseau_paris_reel(self):
        d = datetime(2026, 12, 1, 12, 0, tzinfo=timezone.utc).astimezone(g.PARIS_TZ)
        self.assertEqual(d.utcoffset(), timedelta(hours=1))      # heure d'hiver
        d = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc).astimezone(g.PARIS_TZ)
        self.assertEqual(d.utcoffset(), timedelta(hours=2))      # heure d'été


class TestPurgeAnglais(unittest.TestCase):
    def test_purge_aussi_les_entrees_francaises_sur_une_ligne(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "en"))
        try:
            import translate_daily as t
        except Exception as e:  # noqa: BLE001
            self.skipTest(f"translate_daily non importable ici : {e}")
        maintenant = datetime.now(timezone.utc)
        vieille = maintenant - timedelta(hours=47, minutes=59)
        xml = (f'<?xml version="1.0" encoding="UTF-8"?>\n{NS}\n'
               f"{entree_fr('2026-10-09', vieille)}\n"
               f"{entree_fr('2026-10-10', maintenant - timedelta(hours=5))}\n</urlset>\n")
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "sitemap-news.xml").write_text(xml, encoding="utf-8")
            with mock.patch.object(t, "REPO_ROOT", Path(d)):
                t.update_sitemap_news("2026-10-11", "English title", maintenant.isoformat(timespec="seconds"))
            out = (Path(d) / "sitemap-news.xml").read_text(encoding="utf-8")
        self.assertNotIn("archives/2026-10-09.html", out)     # entrée française périmée : purgée
        self.assertIn("archives/2026-10-10.html", out)
        self.assertIn("en/archives/2026-10-11.html", out)


if __name__ == "__main__":
    unittest.main()
