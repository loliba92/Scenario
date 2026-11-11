import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_post_edition as gp  # noqa: E402

SITEMAP = Path(__file__).resolve().parents[2] / "sitemap.xml"
EDITION = "2026-11-11"


class SitemapLastmodTest(unittest.TestCase):
    def setUp(self):
        self.texte = SITEMAP.read_text(encoding="utf-8")

    def test_plan_reel_accueil_mis_a_jour(self):
        # Liens hreflang entre <loc> et <lastmod> de l'accueil.
        out = gp.update_sitemap_xml(self.texte, EDITION)
        self.assertIn(f"<loc>{gp.SITE_URL}/</loc>", out)
        self.assertRegex(
            out,
            rf"<loc>{gp.SITE_URL}/</loc>(?:(?!</url>)[\s\S])*?<lastmod>{EDITION}</lastmod>")

    def test_archives_et_nouvelle_entree(self):
        out = gp.update_sitemap_xml(self.texte, EDITION)
        self.assertRegex(
            out,
            rf"<loc>{gp.SITE_URL}/archives.html</loc>\s*<lastmod>{EDITION}</lastmod>")
        self.assertIn(f"<loc>{gp.SITE_URL}/archives/{EDITION}.html</loc>", out)

    def test_liens_hreflang_conserves(self):
        out = gp.update_sitemap_xml(self.texte, EDITION)
        self.assertIn('hreflang="en" href="https://lesscenarios.fr/en/"', out)

    def test_glossaire_seulement_si_demande(self):
        out = gp.update_sitemap_xml(self.texte, EDITION, bump_glossaire=True)
        self.assertRegex(
            out,
            rf"<loc>{gp.SITE_URL}/glossaire.html</loc>\s*<lastmod>{EDITION}</lastmod>")

    def test_page_absente_reste_une_erreur(self):
        # Une page manquante doit toujours arrêter la publication.
        sans_accueil = self.texte.replace(f"<loc>{gp.SITE_URL}/</loc>", "<loc>x</loc>", 1)
        with self.assertRaises(gp.PostEditionError):
            gp.update_sitemap_xml(sans_accueil, EDITION)


if __name__ == "__main__":
    unittest.main()
