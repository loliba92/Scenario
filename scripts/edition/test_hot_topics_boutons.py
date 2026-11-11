import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_hot_topics as g  # noqa: E402


class BoutonsTriTest(unittest.TestCase):
    def test_trois_boutons_avec_l_identifiant(self):
        h = g._boutons_tri("economie-la-bce")
        self.assertIn('data-id="economie-la-bce"', h)
        for action in ("monter", "mardi", "prioriser"):
            self.assertIn(f'data-action="{action}"', h)

    def test_rien_sans_identifiant(self):
        self.assertEqual(g._boutons_tri(None), "")
        self.assertEqual(g._boutons_tri(""), "")

    def test_identifiant_echappe(self):
        h = g._boutons_tri('x"><script>')
        self.assertNotIn("<script>", h)


if __name__ == "__main__":
    unittest.main()
