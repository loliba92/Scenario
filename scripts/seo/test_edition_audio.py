"""Garde-fous du bouton « Écouter » des éditions (assets/edition-audio.js)."""
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class EditionAudioTest(unittest.TestCase):
    def test_gabarits_chargent_le_script(self):
        # Les nouvelles éditions reprennent les balises <script> du gabarit (index.html).
        for rel, prefix in (("index.html", ""), ("en/index.html", "../"), ("preview.html", "")):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertRegex(text, rf'src="{re.escape(prefix)}assets/edition-audio\.js"', rel)

    def test_rattrapage_idempotent(self):
        out = subprocess.run(["python3", str(ROOT / "scripts/seo/add_edition_audio.py"), "--dry-run"],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("0 page(s)", out)

    def test_script_discret(self):
        src = (ROOT / "assets/edition-audio.js").read_text(encoding="utf-8")
        self.assertNotIn("import ", src)
        self.assertIn("@media print{.ea{display:none}}", src, "rien à l'impression")
        # le fichier audio n'est demandé qu'au clic (vie privée)
        self.assertIn("audio.src = ep.url", src)
        self.assertIn("btn.addEventListener(\"click\"", src)
        self.assertIn("/^https:\\/\\//", src, "seules des adresses https sont acceptées")

    def test_liste_des_episodes(self):
        liste = json.loads((ROOT / "data/podcast-episodes.json").read_text(encoding="utf-8"))
        dates = [e["date"] for e in liste]
        self.assertEqual(len(dates), len(set(dates)), "un seul épisode par date")
        for e in liste:
            self.assertRegex(e["date"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertTrue(e["url"].startswith("https://"))
            self.assertGreater(e["duree"], 0)


if __name__ == "__main__":
    unittest.main()
