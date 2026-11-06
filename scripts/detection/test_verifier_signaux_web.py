import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import verifier_signaux_web as w
from test_verifier_signaux import sig
import verifier_signaux as v

class T(unittest.TestCase):
    def test_plafond_et_ordre(self):
        j = date(2026, 11, 20)
        sigs = [sig("a", "2026-11-15"), sig("b", "2026-11-10"), sig("c", "2026-11-22"),
                sig("d", "2026-11-18"), sig("e", "2027-06-01")]
        ce, rep = w.candidats(v.analyser(sigs, j))
        self.assertEqual([x[0]["id"] for x in ce], ["b", "a", "d"])
        self.assertEqual([x[0]["id"] for x in rep], ["c"])

    def test_valider_sans_source_devient_incertain(self):
        r = w.valider({"verdict": "concretise", "resume": "x", "sources": []})
        self.assertEqual(r["verdict"], "incertain")

    def test_valider_avec_source(self):
        r = w.valider({"verdict": "concretise", "resume": "x",
                       "sources": [{"titre": "T", "url": "https://exemple.fr/a"}, {"url": "pas-une-url"}]})
        self.assertEqual(r["verdict"], "concretise")
        self.assertEqual(len(r["sources"]), 1)

    def test_valider_verdict_inconnu(self):
        with self.assertRaises(w.GenerationError):
            w.valider({"verdict": "peut-etre"})

if __name__ == "__main__":
    unittest.main()
