"""Tests des titres et descriptions produits par generate_seo_head (titre ≤ 70 avec la marque, description sans coupure)."""
import unittest

import generate_seo_head as g


def brief(titre="", question="", h1=""):
    return {"sujet": {"titre_propose": titre, "question_posee": question, "h1": h1}}


class TestTitre(unittest.TestCase):
    def test_court_inchange(self):
        self.assertEqual(g._build_title(brief("Art : de l'œuvre à l'expérience")), "Art : de l'œuvre à l'expérience — Scénario")

    def test_jamais_plus_de_70_caracteres(self):
        t = g._build_title(brief("Sommes-nous en train de passer d'une culture de l'œuvre à une culture de l'expérience éphémère ?"))
        self.assertLessEqual(len(t), 70)
        self.assertTrue(t.endswith(" — Scénario"))

    def test_jamais_de_mot_outil_avant_les_points_de_suspension(self):
        t = g._build_title(brief("Sommes-nous en train de passer d'une culture de l'œuvre à une culture de l'expérience éphémère ?"))
        avant = t.split("… —")[0].split(" ")[-1].lower().rstrip("'’")
        self.assertNotIn(avant, g._MOTS_OUTILS)


class TestDescription(unittest.TestCase):
    def test_question_courte_inchangee(self):
        q = "L'art passe-t-il d'une culture de l'œuvre à une culture de l'expérience ?"
        self.assertEqual(g._build_description(brief(question=q)), q)

    def test_premiere_phrase_si_elle_convient(self):
        premiere = "Le rachat à 110 milliards de dollars de Warner Bros. Discovery par Paramount va-t-il aboutir, rester bloqué des mois ?"
        q = premiere + " Ou bien les régulateurs vont-ils imposer des cessions qui changeront la nature même de l'opération ?"
        self.assertGreater(len(q), 160)
        self.assertEqual(g._build_description(brief(question=q, h1="Titre")), premiere)

    def test_question_longue_devient_titre_plus_complement(self):
        q = ("Alors que la participation stagne à 45,7 % en 2024-2025 et que l'IA et la personnalisation du risque arrivent, "
             "le dépistage du cancer du sein va-t-il basculer vers un modèle ciblé selon le risque de chaque femme ?")
        d = g._build_description(brief(question=q, h1="Dépistage du cancer du sein : le modèle va-t-il basculer ?"))
        self.assertTrue(100 <= len(d) <= 160, len(d))
        self.assertNotIn("…", d)
        self.assertTrue(d.startswith("Dépistage du cancer du sein : le modèle va-t-il basculer ?"))
        self.assertIn("Trois scénarios chiffrés", d)

    def test_h1_sans_ponctuation_recoit_un_point(self):
        q = "x" * 200
        d = g._build_description(brief(question=q, h1="Big Tech face à la justice"))
        self.assertTrue(d.startswith("Big Tech face à la justice. Trois"))

    def test_dernier_recours_sans_h1(self):
        d = g._build_description(brief(question="mot " * 80))
        self.assertLessEqual(len(d), 160)
        self.assertTrue(d.endswith("…"))


if __name__ == "__main__":
    unittest.main()
