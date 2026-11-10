import re
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_a_venir as g


def rv(i, d, p="jour", dom="Sport", eds=()):
    return {"id": i, "date": d, "precision": p, "domaine": dom, "question": f"Q {i} ?",
            "commentaire": "c", "editions": list(eds), "qui": "Qui (détail)", "nature": "Vote officiel",
            "officiel": True, "calendrier": "date_limite"}


class T(unittest.TestCase):
    def test_donnees_reelles_valides(self):
        r = g.charger()
        self.assertGreaterEqual(len(r), 1)
        for x in r:
            self.assertTrue(x["editions"], x["id"])
            for iso in x["editions"]:
                self.assertTrue((g.RACINE / "archives" / f"{iso}.html").exists(), iso)
            # un rendez-vous « à venir » ne peut pas précéder l'édition qui l'annonce
            self.assertGreaterEqual(x["date"], min(x["editions"]), x["id"])
        ids = [x["id"] for x in r]
        self.assertEqual(len(ids), len(set(ids)), "identifiants en double")

    def test_tri_et_filtre(self):
        j = date(2026, 11, 10)
        res = g.a_venir([rv("b", "2026-12-01"), rv("a", "2026-11-01"), rv("c", "2026-11-10")], j)
        self.assertEqual([x["id"] for x in res], ["c", "b"])

    def test_periodes(self):
        j = date(2026, 11, 10)
        self.assertEqual(g.periode("2026-12-31", j), "Décembre 2026")
        self.assertEqual(g.periode("2027-02-01", j), "En 2027")

    def test_textes_de_date(self):
        self.assertEqual(g.texte_quand(rv("x", "2026-11-30", "jour")), "30 novembre")
        self.assertEqual(g.texte_quand(rv("x", "2026-12-31", "limite")), "D'ici le 31 décembre")
        self.assertEqual(g.texte_quand(rv("x", "2026-11-30", "fin_mois")), "Fin novembre")
        self.assertEqual(g.texte_quand(rv("x", "2027-02-01", "mois")), "Février 2027")
        self.assertEqual(g.texte_quand(rv("x", "2026-12-31", "fin_annee")), "D'ici fin 2026")

    def test_decompte(self):
        j = date(2026, 11, 10)
        self.assertEqual(g.reste(rv("x", "2026-11-11"), j)[0], "dans 1 jour")
        self.assertEqual(g.reste(rv("x", "2026-11-30"), j)[0], "dans 20 jours")
        self.assertEqual(g.reste(rv("x", "2026-11-10"), j)[0], "aujourd'hui")

    def test_page_sans_rendez_vous(self):
        h = g.contenu([], date(2026, 11, 10))
        self.assertIn("Aucun rendez-vous à venir", h)

    def test_page_complete_sans_probabilite(self):
        h = g.page(g.charger(), date(2026, 11, 10))
        self.assertIn("<h1>Ce qui va arriver</h1>", h)
        self.assertNotIn("{{", h)
        self.assertIn('href="a-venir.html" aria-current="page"', h)
        visible = re.sub(r"<[^>]+>", " ", g.contenu(g.charger(), date(2026, 11, 10)))
        self.assertNotIn("%", visible)

    def test_fiche_qui_nature_calendrier(self):
        r = rv("x", "2026-12-31", "limite")
        h = g.fiche(r)
        self.assertIn("<dt>Qui</dt>", h)
        self.assertIn("Officiel", h)
        self.assertEqual(g.texte_calendrier(r), "Pas de date fixée, avant le 31 décembre 2026")
        r.update(calendrier="date_fixee", date="2027-02-12", officiel=False)
        self.assertEqual(g.texte_calendrier(r), "Date fixée : 12 février 2027")
        self.assertIn("Non officiel", g.fiche(r))
        r.update(calendrier="non_programme", date="2026-11-30")
        self.assertEqual(g.texte_calendrier(r), "Non programmé, surveillé jusqu'au 30 novembre 2026")
        r.update(calendrier="periode_annoncee", precision="fin_mois")
        self.assertEqual(g.texte_calendrier(r), "Période annoncée : fin novembre")

    def test_donnees_completes(self):
        for r in g.charger():
            self.assertTrue(r["qui"].strip() and r["nature"].strip())

    def test_echappement(self):
        r = rv("x", "2026-12-31")
        r["question"] = "A <b>&</b> B ?"
        h = g.carte(r, 0, date(2026, 11, 10), g.RACINE)
        self.assertNotIn("<b>&</b>", h)


def resolu(i="r", scen="stable", sources=None, statut="arrive"):
    r = rv(i, "2026-11-30", eds=["2026-10-27"])
    r["resultat"] = {"statut": statut, "date": "2026-11-28", "reponse": "Réponse en une phrase.",
                     "chiffres": [{"libelle": "Taux", "valeur": "88 %"}], "scenario": scen,
                     "sources": sources if sources is not None else [{"titre": "S", "url": "https://exemple.fr/a"}]}
    return r


class TestPasses(unittest.TestCase):
    J = date(2026, 12, 5)

    def test_classement(self):
        verif = rv("v", "2026-11-20")
        a_venir = rv("f", "2026-12-20")
        r = resolu()
        av, res = g.passes([verif, a_venir, r], self.J)
        self.assertEqual([x["id"] for x in av], ["v"])
        self.assertEqual([x["id"] for x in res], ["r"])
        self.assertEqual([x["id"] for x in g.a_venir([verif, a_venir, r], self.J)], ["f"])

    def test_couleur_et_scenario_reel_de_l_edition(self):
        h = g.carte_passee(resolu(scen="stable"), 0, g.RACINE)
        self.assertIn("c-stable", h)
        self.assertIn("Un statu quo militarisé", h)   # titre réel du scénario, lu dans l'édition du 27 octobre
        self.assertIn("45", h)                        # pourcentage de l'édition, pas recalculé
        self.assertIn("bleu", h)
        self.assertIn("orange", g.carte_passee(resolu(scen="degrade"), 0, g.RACINE))
        self.assertIn("vert", g.carte_passee(resolu(scen="favorable"), 0, g.RACINE))

    def test_sans_scenario(self):
        h = g.carte_passee(resolu(scen=None), 0, g.RACINE)
        self.assertIn("ne tranche pas", h)
        self.assertIn("c-neutre", h)

    def test_statuts_en_toutes_lettres(self):
        self.assertIn("S'est produit le 28 novembre", g.carte_passee(resolu(), 0, g.RACINE))
        self.assertIn("Ne s'est pas produit", g.carte_passee(resolu(statut="pas_arrive"), 0, g.RACINE))

    def test_page_affiche_passes_et_legende(self):
        h = g.contenu([resolu(), rv("v", "2026-11-20")], self.J)
        self.assertIn("Déjà arrivés", h)
        self.assertIn("vert, favorable", h)
        self.assertIn("réponse en cours de vérification", h)
        self.assertIn("La réponse", h)
        self.assertIn("88 %", h)

    def test_validation_du_resultat(self):
        for mauvais in (resolu(sources=[]), resolu(sources=[{"url": "pas-un-lien"}])):
            with self.assertRaises(ValueError):
                g.verifier_resultat(mauvais)
        r = resolu(); r["resultat"]["scenario"] = "rose"
        with self.assertRaises(ValueError):
            g.verifier_resultat(r)
        r = resolu(); r["resultat"]["reponse"] = " "
        with self.assertRaises(ValueError):
            g.verifier_resultat(r)

    def test_filtres_et_reperes(self):
        h = g.contenu([resolu(), rv("v", "2026-11-20"), rv("f", "2026-12-20", dom="Culture")], self.J)
        self.assertIn('class="filtres" hidden', h)           # affiché seulement par le script
        self.assertIn('data-f="periode" data-v="passe"', h)
        self.assertIn('data-f="domaine" data-v="Culture"', h)
        self.assertIn('data-f="couleur" data-v="stable"', h)
        self.assertIn('data-periode="avenir"', h)
        self.assertIn('data-couleur="stable"', h)
        self.assertIn("Aujourd'hui · 5 décembre 2026", h)

    def test_etat_vide_du_passe(self):
        h = g.contenu([rv("f", "2026-12-20")], date(2026, 11, 10))
        self.assertIn("Aucun résultat pour l'instant", h)
        self.assertIn("20 décembre 2026", h)

    def test_accueil_ignore_les_passes(self):
        import accueil
        self.assertEqual(accueil.bloc(date(2030, 1, 1)), "")


class TestAccueil(unittest.TestCase):
    def test_bloc_trois_cartes_max(self):
        import accueil
        h = accueil.bloc(date(2026, 11, 10))
        self.assertEqual(h.count('class="avh-point"'), 3)
        self.assertIn('href="a-venir.html#rv-', h)
        self.assertTrue(h.startswith(accueil.START) and h.endswith(accueil.END))

    def test_bloc_vide_sans_rendez_vous(self):
        import accueil
        self.assertEqual(accueil.bloc(date(2030, 1, 1)), "")

    def test_injection_remplace_ancien_bloc_et_est_idempotente(self):
        import accueil
        base = ('<section class="featured-article"><p>ed</p></section>\n'
                '<!-- dernier-suivi:start -->\n<section>vieux</section>\n<!-- dernier-suivi:end -->\n<footer></footer>')
        b = accueil.bloc(date(2026, 11, 10))
        un = accueil.injecter(base, b)
        self.assertNotIn("vieux", un)
        self.assertEqual(un.count(accueil.START), 1)
        self.assertEqual(accueil.injecter(un, b), un)
        self.assertLess(un.index("featured-article"), un.index(accueil.START))

    def test_traits_d_union_insecables(self):
        self.assertIn("est&#8209;il", g.nbsp("Le budget est-il voté ?"))
        self.assertIn("a&#8209;t&#8209;il", g.nbsp("Va-t-il tenir ?"))
        self.assertIn("cessez-le-feu", g.nbsp("cessez-le-feu"))


if __name__ == "__main__":
    unittest.main()
