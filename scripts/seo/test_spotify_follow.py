import unittest
import add_spotify_follow as a


class TestSpotifyFollow(unittest.TestCase):
    def test_ajout_apres_telegram_et_idempotent(self):
        html = '<div><a class="follow-btn" href="https://t.me/scenario_fr" target="_blank"><svg></svg> Telegram</a></div>'
        une = a.ajouter(html)
        self.assertIn(a.URL, une)
        self.assertLess(une.index("Telegram</a>"), une.index(a.URL))
        self.assertEqual(a.ajouter(une), une)

    def test_editions_passees_figees(self):
        noms = {p.relative_to(a.ROOT).as_posix() for p in a.pages("2026-10-04")}
        self.assertIn("archives/2026-10-04.html", noms)
        self.assertNotIn("archives/2026-10-03.html", noms)
        self.assertNotIn("archives/2026-10-02.html", noms)
        self.assertIn("index.html", noms)


if __name__ == "__main__":
    unittest.main()
