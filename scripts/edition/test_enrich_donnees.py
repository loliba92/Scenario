import unittest
from datetime import date

import enrich_sujets as en
import sujets as sj

URL = "https://exemple.org/rapport-2026"
BON = (f"Incidents de brouillage par pays (unité : incidents). Suède = 733 (2024) ; Finlande = 410 (2024) ; "
       f"Estonie = 210 (2024). Sources : {URL}")


class DonneesTest(unittest.TestCase):
    def test_validation(self):
        self.assertTrue(en.donnees_valides(BON, [URL]))
        self.assertFalse(en.donnees_valides(BON, []))                      # URL non citée par la recherche
        self.assertFalse(en.donnees_valides(BON.replace("Finlande = 410 (2024) ; ", ""), [URL]))  # moins de 3 chiffres
        self.assertFalse(en.donnees_valides(BON + "\nautre ligne", [URL]))
        self.assertFalse(en.donnees_valides(None, [URL]))

    def test_application_sans_ecrasement(self):
        e = sj.sujet_vide(id="x", titre="T ?")
        self.assertTrue(en.appliquer_donnees(e, {"donnees": BON}, [URL], date(2026, 10, 4)))
        self.assertTrue(e["donnees"].startswith("[relevé du 2026-10-04]"))
        self.assertFalse(en.appliquer_donnees(e, {"donnees": BON}, [URL], date(2026, 10, 5)))   # déjà présent
        e2 = sj.sujet_vide(id="y", titre="U ?")
        self.assertFalse(en.appliquer_donnees(e2, {"donnees": None, "raison": "rien"}, [URL], date(2026, 10, 4)))
        self.assertIsNone(e2["donnees"])

    def test_aller_retour_markdown_et_dossier(self):
        e = sj.sujet_vide(id="x", titre="Titre ?", contexte="c" * 100, rationnel="La question : " + "r" * 80,
                          mots_cles=["a", "b", "c"], donnees=BON)
        data = {"version": sj.VERSION, "meta": {}, "preambule": "# P", "sections": [
            {"cle": "culture", "titre": "Culture — samedi", "entrees": [e]}]}
        md = sj.render_md(data)
        self.assertIn("données chiffrées:", md)
        d2 = sj.parse_md(md, data)
        e2 = d2["sections"][0]["entrees"][0]
        self.assertEqual(e2["donnees"], BON)
        self.assertIn("Chiffres relevés pour un graphique", sj.dossier_texte(data["sections"][0], e))
        self.assertEqual(sj.dossier_json(data["sections"][0], e)["donnees_graphique"], BON)


if __name__ == "__main__":
    unittest.main()
