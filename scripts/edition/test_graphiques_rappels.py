import unittest

import build_html as bh

BARRES = {
    "aria_label": "Comparaison", "lead": "Trois chiffres.", "caption": "Source : test, 4 octobre 2026.", "unite": "%",
    "valeurs": [
        {"label": "A", "valeur": 12.5}, {"label": "B", "valeur": 8, "mis_en_avant": True}, {"label": "C", "valeur": 3},
    ],
}
CONTENT = {
    "dek": ["Un.", "Deux.", "Trois.", "Quatre.", "Cinq."], "list_box": None, "indicators": [],
    "h1": "Titre", "question_text": "Question ?", "eyebrow_suffix": "sport",
    "meta": {"og_image_alt": "alt"},
}


class TestBarres(unittest.TestCase):
    def test_validation(self):
        self.assertTrue(bh._barres_valides(BARRES))
        self.assertFalse(bh._barres_valides({**BARRES, "valeurs": BARRES["valeurs"][:2]}))
        self.assertFalse(bh._barres_valides({**BARRES, "valeurs": [{"label": "A", "valeur": -1}] * 3}))
        self.assertFalse(bh._barres_valides({**BARRES, "caption": ""}))
        self.assertFalse(bh._barres_valides({}))

    def test_rendu_et_repli(self):
        html = bh._barres_box_html(BARRES)
        self.assertIn('class="dc-bar is-highlight"', html)
        self.assertIn("12,5 %", html)
        hero = bh.build_hero(CONTENT, "2026-10-05", graphique_dc_chart={"decision": "non"},
                             graphique_chiffres={"decision": "oui", "barres": BARRES})
        self.assertIn("dc-bar", hero)
        hero_sans = bh.build_hero(CONTENT, "2026-10-05", graphique_chiffres={"decision": "oui", "barres": {**BARRES, "valeurs": []}})
        self.assertNotIn("dc-bar", hero_sans)
        hero_non = bh.build_hero(CONTENT, "2026-10-05", graphique_chiffres={"decision": "non", "barres": BARRES})
        self.assertNotIn("dc-bar", hero_non)


class TestRappels(unittest.TestCase):
    def test_rappels_inseres_dans_les_faits(self):
        brief = {"articles_connexes": [
            {"date": "2026-08-16", "titre": "Rugby : le choc de trop ?"},
            {"date": "2026-09-20", "titre": "Basket : la NBA débarque en Europe"},
            {"date": "2026-09-27", "titre": "Troisième"},
        ]}
        rappels = bh._rappels_depuis_connexes(brief)
        self.assertEqual(len(rappels), 2)
        hero = bh.build_hero(CONTENT, "2026-10-05", rappels=rappels)
        self.assertEqual(hero.count('class="rappel-edition"'), 2)
        self.assertIn('href="archives/2026-08-16.html"', hero)
        self.assertIn("(16 août)", hero)
        # après le 2e paragraphe
        self.assertLess(hero.index("Deux."), hero.index("archives/2026-08-16.html"))
        self.assertLess(hero.index("archives/2026-08-16.html"), hero.index("Trois."))

    def test_sans_connexes_ni_date_valide(self):
        self.assertEqual(bh._rappels_depuis_connexes({}), [])
        self.assertEqual(bh._rappels_depuis_connexes({"articles_connexes": [{"date": "x", "titre": "T"}]}), [])


class TestRenvoiInline(unittest.TestCase):
    def test_phrase_de_renvoi_retiree(self):
        dek = ("La dette grimpe. Un sujet similaire sur les passifs souverains a déjà été analysé dans nos "
               'archives : <a href="archives/2026-08-27.html">voir l\'édition du 27 août</a>.')
        hero = bh.build_hero({**CONTENT, "dek": [dek, "Deux.", "Trois."]}, "2026-10-08")
        self.assertNotIn("sujet similaire", hero)
        self.assertNotIn("voir l'édition", hero)
        self.assertIn("La dette grimpe.", hero)


if __name__ == "__main__":
    unittest.main()
