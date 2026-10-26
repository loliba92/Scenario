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

    def test_h1_complet_plutot_que_titre_coupe(self):
        long = "IA et cosmologie : l'analyse de 100 millions de galaxies par le CEA résout-elle le mystère de l'énergie sombre ?"
        t = g._build_title(brief(long, h1="Énergie sombre : l'IA du CEA cartographie 100 millions de galaxies"))
        self.assertNotIn("…", t)
        self.assertEqual(t, "Énergie sombre : l'IA du CEA cartographie 100 millions de galaxies")   # 66 caractères : sans la marque
        self.assertLessEqual(len(t), 70)

    def test_h1_un_peu_long_garde_entier(self):
        long = "Mobilisation lycéenne : le mouvement peut-il obtenir la refonte de Parcoursup et des rythmes scolaires ?"
        h1 = "Mobilisation lycéenne : le mouvement peut-il arracher une refonte de Parcoursup ?"   # 80 caractères
        self.assertEqual(g._build_title(brief(long, h1=h1)), h1)

    def test_h1_court_garde_la_marque(self):
        long = "L'IA va-t-elle détruire l'humanité, ou cette peur est-elle exagérée selon les chercheurs ?"
        t = g._build_title(brief(long, h1="IA : risque d'extinction ou peur exagérée ?"))
        self.assertEqual(t, "IA : risque d'extinction ou peur exagérée ? — Scénario")


class TestTitreDepuisH1(unittest.TestCase):
    """Le h1 court de l'édition est le titre de la page, avant la question (titre_propose)."""

    ADDIS_QUESTION = ("Éthiopie-Érythrée : la déclaration de guerre d'Addis-Abeba va-t-elle déclencher "
                      "un nouveau conflit régional ?")
    ADDIS_H1 = "Éthiopie-Érythrée : vers une nouvelle guerre régionale ?"

    def test_h1_court_passe_avant_la_question(self):
        t = g._build_title(brief(self.ADDIS_QUESTION, h1=self.ADDIS_H1))
        self.assertEqual(t, self.ADDIS_H1 + " — Scénario")   # 56 caractères : la marque tient encore
        self.assertNotIn("…", t)

    def test_titre_depuis_h1_sans_coupure(self):
        for h1 in ["Court titre ?", "Un titre de longueur moyenne qui tient en soixante-six caractères ici ?",
                   "Un h1 un peu plus long que la moyenne, gardé entier sans la marque, sans rien couper"]:
            t = g.titre_depuis_h1(h1)
            self.assertIsNotNone(t)
            self.assertNotIn("…", t)

    def test_h1_trop_long_laisse_la_main_au_titre_propose(self):
        self.assertIsNone(g.titre_depuis_h1("x" * 91))
        t = g._build_title(brief("Art : de l'œuvre à l'expérience", h1="x" * 91))
        self.assertEqual(t, "Art : de l'œuvre à l'expérience — Scénario")


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


class TestSeoOptimizerTitre(unittest.TestCase):
    """seo_optimizer reprend le même titre : h1 court de l'édition, jamais coupé en plein mot."""

    def test_titre_du_h1_affiche(self):
        import seo_optimizer as so
        h1 = "Éthiopie-Érythrée : vers une nouvelle guerre régionale ?"
        b = {"date": "2026-10-27", "sujet": {"h1": "Éthiopie-Érythrée : la déclaration de guerre d'Addis-Abeba va-t-elle déclencher un nouveau conflit régional ?", "question_posee": "Question ?"}}
        self.assertEqual(so.generate_seo_metadata(b, "geopolitique", h1_court=h1)["title"], h1 + " — Scénario")

    def test_secours_sans_coupure_en_plein_mot(self):
        import seo_optimizer as so
        h1 = "Éthiopie-Érythrée : la déclaration de guerre d'Addis-Abeba va-t-elle déclencher un nouveau conflit régional"
        t = so.generate_seo_title(h1, "geopolitique", [])
        corps = t.split(" — ")[0]
        self.assertTrue(corps.endswith("…"))
        self.assertEqual(h1[len(corps) - 1], " ")   # la coupure tombe à la fin d'un mot, jamais au milieu
