import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import add_edition_nav as nav

PAGE = '<html><head><title>{t} — Scénario</title></head><body><section class="share-block" id="x"></section><footer></footer></body></html>'


class AddEditionNavTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for d, t in (("2026-10-01", "Premier sujet ?"), ("2026-10-02", "Deuxième"), ("2026-10-03", "Troisième")):
            (self.tmp / f"{d}.html").write_text(PAGE.format(t=t), encoding="utf-8")
        self.dates = ["2026-10-01", "2026-10-02", "2026-10-03"]

    def run_on(self, d):
        return nav.appliquer((self.tmp / f"{d}.html").read_text(encoding="utf-8"), d, self.dates, self.tmp)

    def test_middle_edition_has_both_links(self):
        out = self.run_on("2026-10-02")
        self.assertIn('rel="prev" href="2026-10-01.html"', out)
        self.assertIn('rel="next" href="2026-10-03.html"', out)
        self.assertIn("Premier sujet&nbsp;?", out)
        self.assertLess(out.index(nav.DEBUT), out.index('<section class="share-block"'))

    def test_ends_have_one_link(self):
        self.assertNotIn('rel="prev"', self.run_on("2026-10-01"))
        self.assertNotIn('rel="next"', self.run_on("2026-10-03"))

    def test_idempotent_and_refreshes(self):
        once = self.run_on("2026-10-02")
        self.assertEqual(once.count(nav.DEBUT), 1)
        self.assertEqual(once.count(nav.CSS_ID), 1)
        self.assertEqual(nav.appliquer(once, "2026-10-02", self.dates, self.tmp), once)

    def test_footer_fallback_without_share_block(self):
        texte = '<html><head></head><body><footer></footer></body></html>'
        out = nav.appliquer(texte, "2026-10-02", self.dates, self.tmp)
        self.assertLess(out.index(nav.DEBUT), out.index("<footer"))


if __name__ == "__main__":
    unittest.main()
