import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import synchro_sujets as ss  # noqa: E402


def sujet(ident, titre, sec_cle, date_ech=None, statut="a_traiter"):
    e = {"id": ident, "type": "sujet", "titre": titre, "statut": statut, "validation": "valide"}
    if date_ech:
        e["echeance"] = {"date": date_ech, "raison": "Motif de test."}
    return e


def donnees_test():
    return {"sections": [
        {"cle": "economie", "entrees": [sujet("economie-a", "Sujet A ?", "economie", "2026-12-17")]},
        {"cle": "sport", "entrees": [sujet("sport-b", "Sujet B ?", "sport", "2026-10-01")]},
        {"cle": "priorite_absolue", "entrees": [sujet("priorite-c", "C ?", "priorite_absolue", "2026-12-20")]},
    ]}


class SynchroTest(unittest.TestCase):
    def test_desires_seulement_les_echeances_a_venir(self):
        v = ss.desires(donnees_test(), date(2026, 11, 12))
        self.assertEqual(set(v), {"economie-a"}, "passée et priorité absolue exclues")
        self.assertEqual(v["economie-a"]["source"], "sujets")
        self.assertEqual(v["economie-a"]["domaine"], "Économie")

    def test_ajout_mise_a_jour_et_manuel_intact(self):
        donnees = {"rendez_vous": [
            {"id": "economie-a", "date": "2026-12-01", "source": "sujets", "domaine": "Économie",
             "question": "vieux", "commentaire": "vieux", "resultat": None},
            {"id": "manuel-x", "date": "2026-12-05", "domaine": "Politique", "question": "M",
             "commentaire": "M", "qui": "Mairie", "nature": "N", "officiel": True,
             "calendrier": "date_fixee", "precision": "jour", "editions": []},
        ]}
        v = ss.desires(donnees_test(), date(2026, 11, 12))
        ajoutes, maj, retires = ss.synchroniser(donnees, v, {"economie-a"})
        self.assertEqual((ajoutes, maj, retires), (0, 1, []))
        r = donnees["rendez_vous"][0]
        self.assertEqual(r["date"], "2026-12-17")
        manuel = donnees["rendez_vous"][1]
        self.assertEqual(manuel["qui"], "Mairie", "écrit à la main : jamais modifié")

    def test_retire_auto_disparu_sauf_resultat(self):
        donnees = {"rendez_vous": [
            {"id": "ancien", "date": "2026-12-01", "source": "sujets", "domaine": "Économie", "question": "q",
             "commentaire": "c"},
            {"id": "ancien-verifie", "date": "2026-12-01", "source": "sujets", "domaine": "Économie",
             "question": "q", "commentaire": "c", "resultat": {"statut": "x"}},
        ]}
        ajoutes, maj, retires = ss.synchroniser(donnees, {}, set())
        self.assertEqual(retires, ["ancien"])
        self.assertEqual([r["id"] for r in donnees["rendez_vous"]], ["ancien-verifie"])


if __name__ == "__main__":
    unittest.main()
