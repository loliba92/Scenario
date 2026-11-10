import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hreflang_sitemap import ajouter_hreflang, equivalent, SITE  # noqa: E402

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "xhtml": "http://www.w3.org/1999/xhtml"}

ENTETE = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
PIED = "</urlset>\n"


def url(loc, lastmod="2026-11-09"):
    return (f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n  </url>\n")


def plan(*locs):
    return ENTETE + "".join(url(l) for l in locs) + PIED


class EquivalenceTest(unittest.TestCase):
    def test_accueil(self):
        self.assertEqual(equivalent(f"{SITE}/"), (f"{SITE}/", f"{SITE}/en/"))
        self.assertEqual(equivalent(f"{SITE}/en/"), (f"{SITE}/", f"{SITE}/en/"))

    def test_edition_fr_vers_en(self):
        self.assertEqual(
            equivalent(f"{SITE}/archives/2026-11-09.html"),
            (f"{SITE}/archives/2026-11-09.html", f"{SITE}/en/archives/2026-11-09.html"))

    def test_edition_en_vers_fr(self):
        self.assertEqual(
            equivalent(f"{SITE}/en/archives/2026-11-09.html"),
            (f"{SITE}/archives/2026-11-09.html", f"{SITE}/en/archives/2026-11-09.html"))

    def test_page_sans_equivalent(self):
        self.assertIsNone(equivalent(f"{SITE}/archives.html"))
        self.assertIsNone(equivalent(f"{SITE}/le-projet.html"))


class AjouterHreflangTest(unittest.TestCase):
    def test_paire_fr_en_ajoutee(self):
        xml = plan(f"{SITE}/archives/2026-11-09.html",
                   f"{SITE}/en/archives/2026-11-09.html")
        out = ajouter_hreflang(xml)
        self.assertIn(f'hreflang="en" href="{SITE}/en/archives/2026-11-09.html"', out)
        self.assertIn(f'hreflang="fr" href="{SITE}/archives/2026-11-09.html"', out)
        self.assertEqual(out.count('hreflang="x-default"'), 2)

    def test_paire_incomplete_ignoree(self):
        # l'édition anglaise n'est pas dans le plan : aucun lien
        xml = plan(f"{SITE}/archives/2026-11-09.html")
        out = ajouter_hreflang(xml)
        self.assertNotIn("xhtml:link", out)

    def test_page_sans_equivalent_inchangee(self):
        xml = plan(f"{SITE}/archives.html", f"{SITE}/le-projet.html")
        out = ajouter_hreflang(xml)
        self.assertNotIn("xhtml:link", out)
        self.assertNotIn("xmlns:xhtml", out)

    def test_idempotent(self):
        xml = plan(f"{SITE}/", f"{SITE}/en/",
                   f"{SITE}/archives/2026-11-09.html",
                   f"{SITE}/en/archives/2026-11-09.html")
        une_fois = ajouter_hreflang(xml)
        deux_fois = ajouter_hreflang(une_fois)
        self.assertEqual(une_fois, deux_fois)

    def test_lastmod_inchange(self):
        xml = plan(f"{SITE}/archives/2026-11-09.html",
                   f"{SITE}/en/archives/2026-11-09.html")
        out = ajouter_hreflang(xml)
        self.assertEqual(out.count("<lastmod>2026-11-09</lastmod>"), 2)

    def test_namespace_declare_une_fois(self):
        xml = plan(f"{SITE}/", f"{SITE}/en/")
        out = ajouter_hreflang(ajouter_hreflang(xml))
        self.assertEqual(out.count("xmlns:xhtml="), 1)

    def test_xml_valide_et_liens_lisibles(self):
        xml = plan(f"{SITE}/", f"{SITE}/en/",
                   f"{SITE}/archives/2026-11-09.html",
                   f"{SITE}/en/archives/2026-11-09.html")
        racine = ET.fromstring(ajouter_hreflang(xml))
        urls = racine.findall("sm:url", NS)
        self.assertEqual(len(urls), 4)
        for u in urls:
            liens = u.findall("xhtml:link", NS)
            self.assertEqual({l.get("hreflang") for l in liens},
                             {"fr", "en", "x-default"})

    def test_tout_le_plan_reel(self):
        # garde-fou sur le vrai fichier : chaque lien pointe vers une
        # adresse présente dans le plan, et le fichier reste valide
        chemin = Path(__file__).resolve().parents[2] / "sitemap.xml"
        if not chemin.exists():
            self.skipTest("sitemap.xml absent")
        out = ajouter_hreflang(chemin.read_text(encoding="utf-8"))
        racine = ET.fromstring(out)
        locs = {u.findtext("sm:loc", namespaces=NS)
                for u in racine.findall("sm:url", NS)}
        for lien in racine.iter("{%s}link" % NS["xhtml"]):
            self.assertIn(lien.get("href"), locs)


if __name__ == "__main__":
    unittest.main()
