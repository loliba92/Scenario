"""La mise à jour du plan du site par la traduction anglaise doit fonctionner avec les liens hreflang du bloc /en/."""
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "en"))
sys.path.insert(0, str(REPO / "scripts" / "seo"))

try:
    import translate_daily as t  # noqa: E402
except Exception as e:  # noqa: BLE001
    t = None
    _ERREUR = e

PLAN = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://lesscenarios.fr/</loc>
    <lastmod>2026-11-10</lastmod>
  </url>
  <url>
    <loc>https://lesscenarios.fr/en/</loc>
    <xhtml:link rel="alternate" hreflang="fr" href="https://lesscenarios.fr/"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://lesscenarios.fr/en/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://lesscenarios.fr/"/>
    <lastmod>2026-11-10</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://lesscenarios.fr/en/archives/2026-11-10.html</loc>
    <lastmod>2026-11-10</lastmod>
  </url>
  <url>
    <loc>https://lesscenarios.fr/archives/2026-11-11.html</loc>
    <lastmod>2026-11-11</lastmod>
  </url>
</urlset>
"""


class TestPlanAvecHreflang(unittest.TestCase):
    def test_bloc_en_avec_liens_hreflang(self):
        if t is None:
            self.skipTest(f"translate_daily non importable ici : {_ERREUR}")
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "sitemap.xml").write_text(PLAN, encoding="utf-8")
            ancien = t.REPO_ROOT
            t.REPO_ROOT = Path(d)
            try:
                t.update_sitemap("2026-11-11")
            finally:
                t.REPO_ROOT = ancien
            out = (Path(d) / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/en/archives/2026-11-11.html", out)
        bloc = out.split("<loc>https://lesscenarios.fr/en/</loc>")[1].split("</url>")[0]
        self.assertIn("<lastmod>2026-11-11</lastmod>", bloc)


if __name__ == "__main__":
    unittest.main()
