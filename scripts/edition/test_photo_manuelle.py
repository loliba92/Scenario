"""Photo choisie à la main (hors Pexels) : recadrage, reprise à la publication, crédit avec licence."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "scripts" / "social"))

import build_html
import generate_daily_edition as gde
import generate_post_edition as gpe
import photo_manuelle
from PIL import Image

CREDITS = {
    "source": "manuelle", "local_file": "assets/social/photos-manuelles/2026-10-18-zidane.jpg",
    "photographer": "Oleg Dubyna", "source_label": "Wikimedia Commons",
    "source_url": "https://commons.wikimedia.org/wiki/File:Zinedine_Zidane_(41758545214).jpg",
    "licence": "CC BY-SA 2.0", "licence_url": "https://creativecommons.org/licenses/by-sa/2.0/",
    "focus_x": 0.55, "focus_y": 0.35, "query": "Zinedine Zidane",
}


class PhotoManuelle(unittest.TestCase):
    def test_recadrages_aux_bonnes_tailles(self):
        with tempfile.TemporaryDirectory() as d:
            carre, large = photo_manuelle.produire_recadrages(CREDITS, REPO, d, "t")
            self.assertEqual(Image.open(carre).size, (1080, 1080))
            self.assertEqual(Image.open(large).size, (1600, 900))

    def test_reprise_a_la_publication(self):
        """generate_post_edition reprend la photo manuelle de la fiche : mêmes fichiers qu'une photo Pexels."""
        with tempfile.TemporaryDirectory() as d:
            photo = gpe.select_topic_photo_from_preview(CREDITS, "2099-01-01", Path(d))
            self.assertIsNotNone(photo)
            self.assertTrue(photo["square_path"].exists())
            self.assertTrue(photo["wide_path"].exists())
            self.assertEqual(photo["licence"], "CC BY-SA 2.0")
            self.assertTrue((Path(d) / "assets/social/topic-images/2099-01-01.json").exists())

    def test_fichier_absent_ne_bloque_pas(self):
        faux = dict(CREDITS, local_file="assets/social/photos-manuelles/introuvable.jpg")
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(gpe.select_topic_photo_from_preview(faux, "2099-01-01", Path(d)))

    def test_credit_avec_source_et_licence(self):
        date = "2026-10-18"
        brief = gde.load_brief(REPO / "editorial-briefs" / f"{date}.json")
        content = json.loads((REPO / "editorial-previews" / f"{date}.content.json").read_text(encoding="utf-8"))
        shell = build_html.extract_shell((REPO / "index.html").read_text(encoding="utf-8"))
        photo = {"og_image_url": "https://x/o.jpg", "hero_image_url": "https://x/h.jpg", "alt": "a",
                 "photographer": CREDITS["photographer"], "pexels_url": CREDITS["source_url"],
                 "source_label": CREDITS["source_label"], "licence": CREDITS["licence"], "licence_url": CREDITS["licence_url"]}
        page, _ = build_html.assemble_index_html(shell, content, brief, date, photo=photo)
        credit = re.search(r'<p class="footer-photo-credit">.*?</p>', page, re.S).group(0)
        self.assertIn("Wikimedia Commons ↗", credit)
        self.assertIn("CC BY-SA 2.0", credit)
        self.assertNotIn("Pexels", credit)

    def test_credit_pexels_inchange(self):
        date = "2026-10-18"
        brief = gde.load_brief(REPO / "editorial-briefs" / f"{date}.json")
        content = json.loads((REPO / "editorial-previews" / f"{date}.content.json").read_text(encoding="utf-8"))
        shell = build_html.extract_shell((REPO / "index.html").read_text(encoding="utf-8"))
        photo = {"og_image_url": "https://x/o.jpg", "hero_image_url": "https://x/h.jpg", "alt": "a",
                 "photographer": "Jane", "pexels_url": "https://www.pexels.com/photo/x/"}
        page, _ = build_html.assemble_index_html(shell, content, brief, date, photo=photo)
        credit = re.search(r'<p class="footer-photo-credit">.*?</p>', page, re.S).group(0)
        self.assertIn("Jane / <a href=\"https://www.pexels.com/photo/x/\"", credit)
        self.assertIn("Pexels ↗</a></p>", credit)


if __name__ == "__main__":
    unittest.main()
