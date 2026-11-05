import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import verifier_signaux as v

def sig(i, limite, statut="en_attente", eds=()):
    e = {"effet": "x", "renforce": "stable"}
    return {"id": i, "libelle": i, "date_limite": limite, "editions": list(eds),
            "si_concretise": e, "si_non_concretise": e, "statut": statut}

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

if __name__ == "__main__":
    unittest.main()
