import tempfile
import unittest
from pathlib import Path

import connexes as c

ARCHIVES = """<table>
<tr data-domain="politique" class="x" data-date="2026-09-23"><td><a href="archives/2026-09-23.html" title="La menace hybride russe">Carburants et menaces hybrides</a></td></tr>
<tr data-domain="economie" class="x" data-date="2026-09-22"><td><a href="archives/2026-09-22.html" title="Le commerce maritime">Bab el-Mandeb</a></td></tr>
<tr data-domain="international" class="x" data-date="2026-08-19"><td><a href="archives/2026-08-19.html" title="Piratages attribués à la Russie">2027 sous influence</a></td></tr>
</table>"""


class ConnexesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        chemin = Path(self.tmp.name) / "archives.html"
        chemin.write_text(ARCHIVES, encoding="utf-8")
        self.editions = c.charger_archives(chemin)

    def tearDown(self):
        self.tmp.cleanup()

    def test_chargement_et_liste_complete(self):
        self.assertEqual([e["date"] for e in self.editions], ["2026-09-23", "2026-09-22", "2026-08-19"])
        texte = c.toutes_les_editions(self.editions, exclure={"2026-09-22"})
        self.assertIn("2026-08-19", texte)
        self.assertNotIn("2026-09-22", texte)
        self.assertIn("La menace hybride russe", texte)

    def test_normalisation(self):
        brief = {"date": "2026-10-05", "articles_connexes": [
            {"date": "2026-09-23", "titre": "paraphrase", "lien": "même menace"},
            {"date": "2026-09-23", "titre": "doublon", "lien": "x"},
            {"date": "2026-01-01", "titre": "inconnue", "lien": "x"},
            {"date": "2026-10-05", "titre": "du jour", "lien": "x"},
            {"date": "2026-08-19", "titre": "2027 sous influence", "lien": "même acteur"},
        ]}
        notes = c.normaliser_connexes(brief, self.editions)
        self.assertEqual([a["date"] for a in brief["articles_connexes"]], ["2026-09-23", "2026-08-19"])
        self.assertEqual(brief["articles_connexes"][0]["titre"], "Carburants et menaces hybrides")   # titre exact
        self.assertEqual(len(notes), 4)   # titre remplacé, doublon, inconnue, du jour

    def test_ne_remplit_pas_a_la_place_du_modele(self):
        brief = {"date": "2026-10-05", "articles_connexes": []}
        c.normaliser_connexes(brief, self.editions)
        self.assertEqual(brief["articles_connexes"], [])

    def test_archives_reelles(self):
        editions = c.charger_archives()
        self.assertGreater(len(editions), 30)
        self.assertTrue(all(e["date"] and e["titre"] for e in editions))


if __name__ == "__main__":
    unittest.main()
