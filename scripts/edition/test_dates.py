"""Tests du format court des dates sur les cartes (build_html._format_date_short).

Régression du 2 octobre 2026 : le mois était dérivé de MOIS_FR[:4], ce qui affichait
« 2 octo. » (au lieu de « 2 oct. ») et « 30 août. » (point abusif sur un mois non abrégé).

Lancer :  python3 -m unittest discover -s scripts/edition -p "test_dates.py" -v
Sans clé API ni réseau ; seul beautifulsoup4 est nécessaire (importé par build_html).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_html as bh  # noqa: E402

ATTENDU_FR = [
    "2 janv.", "2 févr.", "2 mars", "2 avr.", "2 mai", "2 juin",
    "2 juil.", "2 août", "2 sept.", "2 oct.", "2 nov.", "2 déc.",
]


class FormatDateCourte(unittest.TestCase):
    def test_fr_douze_mois(self):
        obtenu = [bh._format_date_short(f"2026-{m:02d}-02") for m in range(1, 13)]
        self.assertEqual(obtenu, ATTENDU_FR)

    def test_fr_jamais_de_troncature_a_quatre_lettres(self):
        for m in range(1, 13):
            self.assertNotIn("octo", bh._format_date_short(f"2026-{m:02d}-02"))

    def test_en(self):
        self.assertEqual(bh._format_date_short("2026-10-02", "en"), "Oct 2")

    def test_table_complete(self):
        self.assertEqual(len(bh.MOIS_FR_ABBR), 12)
        for long, court in zip(bh.MOIS_FR, bh.MOIS_FR_ABBR):
            self.assertTrue(long.startswith(court.rstrip(".")), (long, court))


if __name__ == "__main__":
    unittest.main()
