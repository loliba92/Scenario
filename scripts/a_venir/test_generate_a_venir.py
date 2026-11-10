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
            for iso in x["editions"]:
                self.assertTrue((g.RACINE / "archives" / f"{iso}.html").exists(), iso)

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
        self.assertIn("Aucun rendez-vous à surveiller", h)

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


class TestAccueil(unittest.TestCase):
    def test_bloc_trois_cartes_max(self):
        import accueil
        h = accueil.bloc(date(2026, 11, 10))
        self.assertEqual(h.count('class="avh-carte"'), 3)
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
