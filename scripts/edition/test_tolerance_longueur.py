import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_daily_edition as g


class T(unittest.TestCase):
    def test_seuil_baisse_a_chaque_essai(self):
        self.assertEqual([g.min_words_pour_essai(i) for i in range(3)], [1100, 1045, 990])

    def test_au_dela_du_dernier_essai_le_seuil_reste_le_plus_bas(self):
        self.assertEqual(g.min_words_pour_essai(7), 990)
        self.assertEqual(g.min_words_pour_essai(-1), 1100)

    def test_997_mots_refuse_au_1er_essai_accepte_au_3e(self):
        self.assertLess(997, g.min_words_pour_essai(0))
        self.assertLess(997, g.min_words_pour_essai(1))
        self.assertGreaterEqual(997, g.min_words_pour_essai(2))

    def test_controle_final_du_html_aussi_tolerant_que_le_dernier_essai(self):
        self.assertEqual(g.MIN_WORDS_FINAL, g.min_words_pour_essai(2))
        self.assertGreaterEqual(993, g.MIN_WORDS_FINAL)


if __name__ == "__main__":
    unittest.main()
