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
    def test_icone_dans_la_ligne_de_partage_idempotente(self):
        import add_google_source_edition as e
        html = '<p class="share-inline">\n      <a id="share-x">x</a>\n    </p><nav class="toc"></nav>'
        une = e.ajouter_hero(html, False)
        self.assertIn('id="share-google"', une)
        self.assertIn('title="Ajouter Scénario à vos sources Google"', une)
        self.assertLess(une.index('id="share-google"'), une.index("</p>"))   # dans la ligne de partage, pas une ligne en plus
        self.assertNotIn("source-google", une)
        self.assertEqual(e.ajouter_hero(une, False), une)
        self.assertIn('title="Add Scénario to your Google sources"', e.ajouter_hero(html, True))

    def test_ancienne_version_retiree(self):
        import add_google_source_edition as e
        ancien = ('<style>a{}\n  /* ---- Lien discret « Ajouter Scénario à vos sources Google » sous la ligne de partage (4 octobre 2026). ---- */\n'
                  '  .source-google{ margin: 0; }\n  @media print{ .source-google{ display: none; } }\n</style>'
                  '<p class="share-inline">\n      <a id="share-x">x</a>\n    </p>\n    <p class="source-google"><a>vieux texte</a></p>')
        nettoye = e.ajouter_hero(ancien, False)
        self.assertNotIn("source-google", nettoye)
        self.assertNotIn("vieux texte", nettoye)
        self.assertIn('id="share-google"', nettoye)

    def test_cibles_sans_editions_passees(self):
        import add_google_source_edition as e
        noms = {c[0].relative_to(e.ROOT).as_posix() for c in e.cibles("2026-10-04")}
        self.assertNotIn("archives/2026-10-03.html", noms)
        self.assertIn("archives/2026-10-04.html", noms)


if __name__ == "__main__":
    unittest.main()
