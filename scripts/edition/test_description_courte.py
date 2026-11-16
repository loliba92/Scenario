"""Descriptions de 100 à 160 caractères : question courte (FR) et traduction courte (EN) complétées."""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "edition"))
sys.path.insert(0, str(REPO / "scripts" / "en"))

import generate_seo_head as g  # noqa: E402

try:
    import translate_daily as t  # noqa: E402
except Exception as e:  # noqa: BLE001
    t = None
    _ERREUR = e


class TestDescriptionFrancaise(unittest.TestCase):
    def test_question_courte_completee(self):
        q = "Le gouvernement tiendra-t-il jusqu'au vote du budget ?"
        d = g._build_description({"date": "2026-10-25", "sujet": {"question_posee": q, "h1": "x"}})
        self.assertTrue(d.startswith(q))
        self.assertTrue(100 <= len(d) <= 160, len(d))

    def test_question_normale_inchangee(self):
        q = "Le gouvernement tiendra-t-il jusqu'au vote du budget de l'année prochaine malgré la pression de l'opposition ?"
        self.assertTrue(100 <= len(q) <= 160)
        d = g._build_description({"date": "2026-10-25", "sujet": {"question_posee": q, "h1": "x"}})
        self.assertEqual(d, q)


class TestDescriptionAnglaise(unittest.TestCase):
    def setUp(self):
        if t is None:
            self.skipTest(f"translate_daily non importable ici : {_ERREUR}")

    def test_courte_completee(self):
        d = t._completer_description_en("Will the government survive until the budget vote this autumn?", "2026-11-08")
        self.assertTrue(100 <= len(d) <= 160, len(d))

    def test_normale_inchangee(self):
        longue = "x" * 120
        self.assertEqual(t._completer_description_en(longue, "2026-11-08"), longue)


if __name__ == "__main__":
    unittest.main()
