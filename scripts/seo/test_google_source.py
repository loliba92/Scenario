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



class TestGoogleSourceEdition(unittest.TestCase):
    def test_hero_et_css_idempotents(self):
        import add_google_source_edition as e
        html = '<style>a{}</style><p class="share-inline"><a>x</a></p><nav class="toc"></nav>'
        une = e.ajouter_hero(e.ajouter_css(html), False)
        self.assertIn("Ajouter Scénario à vos sources Google", une)
        self.assertLess(une.index("share-inline"), une.index('<p class="source-google">'))
        self.assertLess(une.index('<p class="source-google">'), une.index("<nav"))
        self.assertEqual(e.ajouter_hero(e.ajouter_css(une), False), une)
        self.assertIn("Add Scénario to your Google sources", e.ajouter_hero(html, True))

    def test_cibles_sans_editions_passees(self):
        import add_google_source_edition as e
        noms = {c[0].relative_to(e.ROOT).as_posix() for c in e.cibles("2026-10-04")}
        self.assertNotIn("archives/2026-10-03.html", noms)
        self.assertIn("archives/2026-10-04.html", noms)


if __name__ == "__main__":
    unittest.main()
