import unittest

import add_google_source as g
import add_spotify_follow as sp


class TestGoogleSource(unittest.TestCase):
    def test_ajout_apres_spotify_et_idempotent(self):
        html = '<div><a class="follow-btn" href="' + sp.URL + '" target="_blank"><svg></svg> Spotify</a></div>'
        une = g.ajouter(html)
        self.assertIn(g.URL, une)
        self.assertLess(une.index("Spotify</a>"), une.index(g.URL))
        self.assertEqual(g.ajouter(une), une)

    def test_lien_officiel(self):
        self.assertEqual(g.URL, "https://google.com/preferences/source?q=lesscenarios.fr")

    def test_editions_passees_figees(self):
        noms = {p.relative_to(g.ROOT).as_posix() for p in sp.pages("2026-10-04")}
        self.assertNotIn("archives/2026-10-03.html", noms)


if __name__ == "__main__":
    unittest.main()
