import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import synchro_sujets as ss  # noqa: E402

AUJOURDHUI = date(2026, 11, 12)


def sujet(ident, titre, date_ech, ferme=True, evenement="Réunion test", edition=None, statut="a_traiter"):
    e = {"id": ident, "type": "sujet", "titre": titre, "statut": statut, "validation": "valide", "edition": edition}
    if date_ech:
        e["echeance"] = {"date": date_ech, "raison": "Motif de test.", "precision": "jour",
                         "qui": "Organisme test", "nature": "Nature test", "officiel": True,
                         "calendrier": "date_fixee", "evenement": evenement}
        if ferme:
            e["echeance"]["ferme"] = True
    return e


def donnees_test():
    return {"sections": [
        {"cle": "economie", "entrees": [
            sujet("economie-a", "Sujet A ?", "2026-12-17", evenement="Réunion BCE"),
            sujet("economie-flou", "Flou ?", "2026-12-20", ferme=False),
            sujet("economie-passe", "Passé ?", "2026-10-01"),
        ]},
        {"cle": "sport", "entrees": [
            sujet("sport-b", "Sujet B ?", "2026-12-17", evenement="Réunion BCE", edition="2026-11-05"),
            sujet("sport-c", "Sujet C ?", "2026-11-29", evenement="Finale", edition="2026-10-04"),
        ]},
        {"cle": "priorite_absolue", "entrees": [
            sujet("priorite-d", "D ?", "2026-12-21", evenement="Autre"),
        ]},
    ]}


def fermes_test():
    base = {"ferme": True, "precision": "jour", "qui": "Organisme test", "nature": "Nature test",
            "officiel": True, "calendrier": "date_fixee"}
    return {
        "economie-a": dict(base, evenement="Réunion BCE"),
        "sport-b": dict(base, evenement="Réunion BCE"),
        "sport-c": dict(base, evenement="Finale"),
        "priorite-d": dict(base, evenement="Autre"),
    }


class SynchroTest(unittest.TestCase):
    def test_seulement_les_dates_fermes_a_venir(self):
        v = ss.desires(donnees_test(), AUJOURDHUI, fermes_test())
        self.assertEqual(len(v), 2, "un flou, un passé et une priorité absolue sont exclus")
        self.assertIn("evt-reunion-bce-2026-12-17", v)
        self.assertIn("evt-finale-2026-11-29", v)

    def test_un_evenement_pour_plusieurs_sujets_une_seule_carte(self):
        v = ss.desires(donnees_test(), AUJOURDHUI, fermes_test())
        bce = v["evt-reunion-bce-2026-12-17"]
        self.assertEqual(bce["editions"], ["2026-11-05"], "rattaché à l'édition qui le traite")
        self.assertEqual(bce["source"], "sujets")
        self.assertEqual(bce["domaine"], "Économie")

    def test_ajout_mise_a_jour_et_manuel_intact(self):
        donnees = {"rendez_vous": [
            {"id": "evt-finale-2026-11-29", "date": "2026-11-01", "source": "sujets", "domaine": "Sport",
             "question": "vieux", "commentaire": "vieux", "precision": "jour", "editions": [],
             "qui": "vieux", "nature": "vieux", "officiel": False, "calendrier": "date_fixee"},
            {"id": "manuel-x", "date": "2026-12-05", "domaine": "Politique", "question": "M",
             "commentaire": "M", "qui": "Mairie", "nature": "N", "officiel": True,
             "calendrier": "date_fixee", "precision": "jour", "editions": []},
        ]}
        v = ss.desires(donnees_test(), AUJOURDHUI, fermes_test())
        ajoutes, maj, retires = ss.synchroniser(donnees, v, set())
        self.assertEqual((ajoutes, maj, retires), (1, 1, []))
        mis_a_jour = next(r for r in donnees["rendez_vous"] if r["id"] == "evt-finale-2026-11-29")
        self.assertEqual(mis_a_jour["date"], "2026-11-29")
        manuel = next(r for r in donnees["rendez_vous"] if r["id"] == "manuel-x")
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


class ValiderFixeTest(unittest.TestCase):
    BON = {"ferme": True, "evenement": "Réunion BCE", "precision": "jour", "qui": "BCE",
           "nature": "Décision de taux", "officiel": True, "calendrier": "date_fixee"}

    def test_complet_accepte(self):
        self.assertEqual(ss.valider_fixe(dict(self.BON))["evenement"], "Réunion BCE")

    def test_refuse_si_pas_ferme_ou_champ_manquant(self):
        self.assertIsNone(ss.valider_fixe(dict(self.BON, ferme=False)))
        self.assertIsNone(ss.valider_fixe(dict(self.BON, qui="")))
        self.assertIsNone(ss.valider_fixe({k: v for k, v in self.BON.items() if k != "nature"}))

    def test_refuse_valeurs_inconnues(self):
        self.assertIsNone(ss.valider_fixe(dict(self.BON, precision="bientot")))
        self.assertIsNone(ss.valider_fixe(dict(self.BON, calendrier="peut-etre")))
        self.assertIsNone(ss.valider_fixe(dict(self.BON, officiel="oui")))


if __name__ == "__main__":
    unittest.main()
