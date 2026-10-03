"""Garde-fous de la lecture des scénarios en onglets (assets/scenarios-reader.js)."""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ScenariosReaderTest(unittest.TestCase):
    def test_gabarits_chargent_le_script(self):
        # Les nouvelles éditions reprennent leurs balises <script> du gabarit (index.html).
        for rel, prefix in (("index.html", ""), ("en/index.html", "../"), ("preview.html", "")):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertRegex(text, rf'src="{re.escape(prefix)}assets/scenarios-reader\.js"', rel)

    def test_rattrapage_idempotent(self):
        out = subprocess.run(["python3", str(ROOT / "scripts/seo/add_scenarios_reader.py"), "--dry-run"],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("0 page(s)", out, "toutes les pages avec scénarios ont déjà la balise")

    def test_script_sans_dependance(self):
        src = (ROOT / "assets/scenarios-reader.js").read_text(encoding="utf-8")
        self.assertNotIn("import ", src)
        self.assertIn("@media screen", src, "l'impression garde les trois scénarios en entier")
        self.assertIn("nav.toc a[href^='#']", src, "le sommaire de tête est relibellé et stylé")


if __name__ == "__main__":
    unittest.main()
