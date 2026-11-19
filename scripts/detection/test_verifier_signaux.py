import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import verifier_signaux as v

def sig(i, limite, statut="en_attente", eds=()):
    e = {"effet": "x", "renforce": "stable"}
    return {"id": i, "libelle": i, "date_limite": limite, "editions": list(eds),
            "si_concretise": e, "si_non_concretise": e, "statut": statut, "pourquoi": "p"}

class T(unittest.TestCase):
    def test_classement(self):
        j = date(2026, 11, 5)
        r = v.analyser([sig("a", "2026-11-01"), sig("b", "2026-11-10"), sig("c", "2026-12-31"),
                        sig("d", "2026-11-01", "concretise")], j)
        self.assertEqual([x[0]["id"] for x in r["echus"]], ["a"])
        self.assertEqual([x[0]["id"] for x in r["proches"]], ["b"])
        self.assertEqual([x[0]["id"] for x in r["en_cours"]], ["c"])
        self.assertEqual(len(r["tranches"]), 1)

    def test_anomalies(self):
        r = v.analyser([sig("a", "n'importe quoi"), sig("b", "2026-12-01", "bizarre"),
                        sig("c", "2026-12-01", eds=["archives/inexistant.html"])], date(2026, 11, 5))
        self.assertEqual(len(r["anomalies"]), 3)

    def test_pourquoi_obligatoire(self):
        s = sig("a", "2026-12-31"); del s["pourquoi"]
        r = v.analyser([s], date(2026, 11, 5))
        self.assertEqual(len(r["anomalies"]), 1)
        self.assertEqual(len(r["en_cours"]), 1)

    def test_rapport_affiche_pourquoi(self):
        j = date(2026, 11, 5)
        txt = v.rapport(v.analyser([sig("a", "2026-11-01"), sig("c", "2026-12-31")], j), j)
        self.assertEqual(txt.count("Pourquoi on le suit : p"), 2)


if __name__ == "__main__":
    unittest.main()
