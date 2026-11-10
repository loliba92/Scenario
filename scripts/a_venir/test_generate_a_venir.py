import re
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_a_venir as g


def rv(i, d, p="jour", dom="Sport", eds=()):
    return {"id": i, "date": d, "precision": p, "domaine": dom, "question": f"Q {i} ?",
            "commentaire": "c", "editions": list(eds)}


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

    def test_echappement(self):
        r = rv("x", "2026-12-31")
        r["question"] = "A <b>&</b> B ?"
        h = g.carte(r, 0, date(2026, 11, 10), g.RACINE)
        self.assertNotIn("<b>&</b>", h)


if __name__ == "__main__":
    unittest.main()
