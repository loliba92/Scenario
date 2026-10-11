"""Tests du bloc « Les éditions du mois » de l'accueil (liens HTML vers chaque édition des 30 derniers jours)."""
import unittest
from unittest import mock

import build_html as b


def entree(jour, titre="Un titre ?", edition_id=None):
    return {"edition_id": edition_id or jour, "date_str": jour, "title": titre, "image_url": "x.jpg", "domain": "sport"}


RECENTES = [entree("2026-10-10"), entree("2026-10-01"), entree("2026-09-20"), entree("2026-09-11"), entree("2026-09-10"), entree("2026-08-01")]


class TestRestantes(unittest.TestCase):
    def _restantes(self, deja):
        with mock.patch.object(b, "get_latest_archives", return_value=RECENTES):
            return [a["date_str"] for a in b.editions_du_mois_restantes(".", "2026-10-11", deja)]

    def test_fenetre_de_30_jours(self):
        # 11 octobre - 30 jours = 11 septembre : le 10 septembre et le 1er août sont hors fenêtre
        self.assertEqual(self._restantes(set()), ["2026-10-10", "2026-10-01", "2026-09-20", "2026-09-11"])

    def test_exclut_les_editions_deja_en_carte(self):
        self.assertEqual(self._restantes({"2026-10-10", "2026-09-20"}), ["2026-10-01", "2026-09-11"])

    def test_tout_deja_affiche(self):
        self.assertEqual(self._restantes({a["edition_id"] for a in RECENTES}), [])


class TestRendu(unittest.TestCase):
    def test_vrais_liens_html_vers_chaque_edition(self):
        html = b.build_editions_du_mois([entree("2026-10-01", "Bitcoin : le bitcoin devient-il un actif institutionnel ?"),
                                         entree("2026-09-30", "Plans sociaux", edition_id="2026-09-30-extra")])
        self.assertIn('href="archives/2026-10-01.html"', html)
        self.assertIn('href="archives/2026-09-30-extra.html"', html)       # édition supplémentaire du même jour
        self.assertIn("1 oct.", html)
        self.assertIn('id="editions-du-mois"', html)
        self.assertIn("Les éditions du mois", html)
        self.assertIn("&nbsp;?", html)                                      # typographie française : « ? » ne reste pas seul

    def test_vide_ou_anglais_ne_produit_rien(self):
        self.assertEqual(b.build_editions_du_mois([]), "")
        self.assertEqual(b.build_editions_du_mois([entree("2026-10-01")], lang="en"), "")


if __name__ == "__main__":
    unittest.main()
