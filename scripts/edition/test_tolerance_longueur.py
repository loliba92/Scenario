import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_daily_edition as g


class T(unittest.TestCase):
    def test_seuil_baisse_a_chaque_essai(self):
        self.assertEqual([g.min_words_pour_essai(i) for i in range(3)], [1000, 900, 800])

    def test_au_dela_du_dernier_essai_le_seuil_reste_le_plus_bas(self):
        self.assertEqual(g.min_words_pour_essai(7), 800)
        self.assertEqual(g.min_words_pour_essai(-1), 1000)

    def test_seuils_de_l_editeur(self):
        # 1er essai 1000 mots, 2e 900, 3e 800 : 890 mots refusé aux essais 1 et 2, accepté au 3e
        self.assertLess(890, g.min_words_pour_essai(0))
        self.assertLess(890, g.min_words_pour_essai(1))
        self.assertGreaterEqual(890, g.min_words_pour_essai(2))
        self.assertGreaterEqual(997, g.min_words_pour_essai(1))

    def test_controle_final_du_html_aussi_tolerant_que_le_dernier_essai(self):
        self.assertEqual(g.MIN_WORDS_FINAL, g.min_words_pour_essai(2))
        self.assertGreaterEqual(993, g.MIN_WORDS_FINAL)


if __name__ == "__main__":
    unittest.main()
