import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_hot_topics as ht  # noqa: E402
import sujets as sj  # noqa: E402


def proposition(**kw):
    base = {
        "accroche": "Terres rares : la Chine peut-elle garder son monopole ?",
        "question": "Terres rares : la Chine peut-elle garder son monopole ?",
        "contexte": "x" * (sj.MIN_CONTEXTE + 20),
        "rationnel": "y" * (sj.MIN_RATIONNEL + 20),
        "mots_cles": ["terres rares", "Chine", "monopole"],
        "sources": [{"titre": "A", "url": "https://www.lemonde.fr/a"},
                    {"titre": "B", "url": "https://www.reuters.com/b"}],
        "a_verifier": "",
    }
    base.update(kw)
    return base


class ScoreSoliditeTest(unittest.TestCase):
    def test_dossier_solide_atteint_le_seuil(self):
        self.assertEqual(ht.score_solidite(proposition()), 100)
        self.assertGreaterEqual(ht.score_solidite(proposition()), ht.SEUIL_VALIDATION_AUTO)

    def test_une_seule_source_baisse_le_score(self):
        s = ht.score_solidite(proposition(sources=[{"url": "https://www.lemonde.fr/a"}]))
        self.assertEqual(s, 85)
        self.assertLess(s, ht.SEUIL_VALIDATION_AUTO + 10)

    def test_meme_domaine_deux_fois_compte_comme_une_source(self):
        s = ht.score_solidite(proposition(sources=[{"url": "https://www.lemonde.fr/a"},
                                                   {"url": "https://lemonde.fr/b"}]))
        self.assertEqual(s, 85)

    def test_point_a_verifier_fait_douter(self):
        s = ht.score_solidite(proposition(a_verifier="Le chiffre de production 2026 reste à confirmer."))
        self.assertEqual(s, ht.SEUIL_VALIDATION_AUTO - 1)
        self.assertLess(s, ht.SEUIL_VALIDATION_AUTO)

    def test_dossier_incomplet_reste_a_valider(self):
        s = ht.score_solidite(proposition(contexte="", rationnel="", mots_cles=[]))
        self.assertLess(s, ht.SEUIL_VALIDATION_AUTO)

    def test_sans_source_jamais_auto_valide(self):
        s = ht.score_solidite(proposition(sources=[]))
        self.assertLess(s, ht.SEUIL_VALIDATION_AUTO)

    def test_score_borne_entre_0_et_100(self):
        s = ht.score_solidite({})
        self.assertTrue(0 <= s <= 100)


if __name__ == "__main__":
    unittest.main()
