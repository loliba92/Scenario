import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_hot_topics as ht  # noqa: E402


class MemeSujetTest(unittest.TestCase):
    def test_meme_sujet_formule_autrement(self):
        # cas réel : même sujet (raffineries russes), titre reformulé
        self.assertTrue(ht.meme_sujet(
            "Frappes sur les raffineries russes : la guerre peut-elle basculer ?",
            "Ukraine : la guerre des raffineries peut-elle faire basculer le conflit ?"))

    def test_meme_sujet_pluriel_et_adjectif(self):
        # « russes » et « russie » : même racine
        self.assertTrue(ht.meme_sujet(
            "Législatives russes : Poutine peut-il tenir sans crise ?",
            "Russie : Poutine verrouille-t-il le pouvoir après les législatives ?"))

    def test_sujets_differents_non_signales(self):
        self.assertFalse(ht.meme_sujet(
            "Terres rares : le nouveau pétrole ?",
            "Facturation électronique : les entreprises prêtes pour l'échéance ?"))
        self.assertFalse(ht.meme_sujet(
            "Robot domestique : entrera-t-il dans nos maisons ?",
            "Netflix : le nouveau cinéma mondial ?"))

    def test_mots_vides_seuls_ne_comptent_pas(self):
        self.assertFalse(ht.meme_sujet("Il peut faire avec sans les", "Elle peut faire sans des"))

    def test_titre_vide(self):
        self.assertFalse(ht.meme_sujet("", "Kaliningrad : la menace ?"))


class FindNearDuplicateTest(unittest.TestCase):
    def test_retrouve_le_sujet_meme_si_titre_reformule(self):
        connus = ["Ukraine : la guerre des raffineries peut-elle faire basculer le conflit ?"]
        self.assertEqual(
            ht.find_near_duplicate("Frappes sur les raffineries russes : la guerre peut-elle basculer ?", connus),
            connus[0])

    def test_titre_sans_rapport_passe(self):
        connus = ["Terres rares : le nouveau pétrole ?"]
        self.assertIsNone(ht.find_near_duplicate("Robot domestique : entrera-t-il dans nos maisons ?", connus))


class FenetreTest(unittest.TestCase):
    def test_tous_les_titres_publies_sans_fenetre(self):
        # le titre du 29 juillet (46 jours avant le 13 septembre) doit être connu
        titres = ht.tous_titres_publies()
        self.assertIn("Budget 2027 : le gouvernement Lecornu va-t-il tenir cet automne ?", titres)
        self.assertGreater(len(titres), 100)


if __name__ == "__main__":
    unittest.main()
