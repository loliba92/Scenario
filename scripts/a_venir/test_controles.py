import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import appliquer_resultats as ap
import controles as c
import generate_a_venir as g
import verifier_resultats as v

R = {"id": "x", "date": "2026-11-30", "precision": "limite", "domaine": "Géopolitique", "question": "Un cessez-le-feu est-il annoncé entre l'Éthiopie et l'Érythrée ?",
     "commentaire": "c", "editions": ["2026-10-27"], "qui": "Gouvernements éthiopien et érythréen", "nature": "Annonce", "officiel": True,
     "calendrier": "non_programme"}
J = date(2026, 12, 2)
EX1 = "Le cessez-le-feu entre l'Éthiopie et l'Érythrée a été annoncé ce samedi sous médiation africaine"
EX2 = "Addis-Abeba et Asmara ont accepté un cessez-le-feu, selon un communiqué commun publié à Nairobi"
PAGES = {
    "https://www.presse-a.fr/a": f"<html><body><p>Titre. {EX1}. Le taux est de 88 %.</p></body></html>",
    "https://agence-b.org/b": f"<p>{EX2}. Après des semaines de tensions entre l'Éthiopie et l'Érythrée.</p>",
    "https://www.facebook.com/p": f"<p>{EX1}</p>",
}


def pages(url):
    t = PAGES.get(url)
    return c.charger_page.__globals__["_html"].unescape(t) if t else None


def prop(**kw):
    p = {"statut": "arrive", "date_reponse": "2026-11-28", "reponse": "Un cessez-le-feu a été annoncé le 28 novembre, sans accord sur le fond.",
         "chiffres": [], "scenario": "stable",
         "sources": [{"titre": "A", "url": "https://www.presse-a.fr/a", "extrait": EX1},
                     {"titre": "B", "url": "https://agence-b.org/b", "extrait": EX2}]}
    p.update(kw)
    return p


def verifier(p, r=R, j=J):
    return c.verifier(r, p, j, date(2026, 10, 27), pages)


class TestControles(unittest.TestCase):
    def test_cas_valide(self):
        ok, motifs, res = verifier(prop())
        self.assertTrue(ok, motifs)
        self.assertEqual(len(res["sources"]), 2)
        self.assertEqual(res["scenario"], "stable")
        g.verifier_resultat({**R, "resultat": res})   # le générateur l'accepte

    def test_incertain_refuse(self):
        self.assertFalse(verifier(prop(statut="incertain"))[0])

    def test_citation_inventee_refusee(self):
        p = prop()
        p["sources"][0]["extrait"] = "Une phrase que la page ne contient absolument pas, inventée de toutes pièces ici"
        ok, motifs, _ = verifier(p)
        self.assertFalse(ok)
        self.assertTrue(any("source(s) vérifiée(s)" in m for m in motifs))

    def test_une_seule_source_refusee(self):
        p = prop()
        p["sources"] = p["sources"][:1]
        self.assertFalse(verifier(p)[0])

    def test_meme_domaine_compte_une_fois(self):
        p = prop()
        p["sources"][1] = {"titre": "A bis", "url": "https://www.presse-a.fr/a", "extrait": EX1}
        self.assertFalse(verifier(p)[0])

    def test_domaine_refuse(self):
        p = prop()
        p["sources"][1] = {"titre": "FB", "url": "https://www.facebook.com/p", "extrait": EX1}
        self.assertFalse(verifier(p)[0])

    def test_http_refuse(self):
        p = prop()
        p["sources"][0]["url"] = "http://www.presse-a.fr/a"
        self.assertFalse(verifier(p)[0])

    def test_chiffre_present_accepte_absent_refuse(self):
        ok, _, res = verifier(prop(chiffres=[{"libelle": "Taux", "valeur": "88 %"}]))
        self.assertTrue(ok)
        self.assertEqual(res["chiffres"], [{"libelle": "Taux", "valeur": "88 %"}])
        ok, motifs, _ = verifier(prop(chiffres=[{"libelle": "Taux", "valeur": "91 %"}]))
        self.assertFalse(ok)
        self.assertTrue(any("introuvable" in m for m in motifs))

    def test_dates(self):
        self.assertFalse(verifier(prop(date_reponse="2027-01-01"))[0])      # futur
        self.assertFalse(verifier(prop(date_reponse="2026-10-01"))[0])      # avant l'édition
        self.assertFalse(verifier(prop(date_reponse="pas une date"))[0])

    def test_pas_arrive_jamais_avant_l_echeance(self):
        self.assertFalse(c.verifier(R, prop(statut="pas_arrive"), date(2026, 11, 29), date(2026, 10, 27), pages)[0])
        ok, _, res = verifier(prop(statut="pas_arrive", reponse="Aucun cessez-le-feu n'a été annoncé avant la date limite."))
        self.assertTrue(ok)
        self.assertEqual(res["date"], "2026-11-30")   # date limite, pas celle du modèle

    def test_conditionnel_refuse(self):
        self.assertFalse(verifier(prop(reponse="Un cessez-le-feu serait annoncé."))[0])
        self.assertFalse(verifier(prop(reponse="x" * 400))[0])

    def test_scenario_inconnu_devient_neutre(self):
        self.assertIsNone(verifier(prop(scenario="rose"))[2]["scenario"])

    def test_source_hors_sujet_refusee(self):
        ex = "Les résultats du championnat régional de volley ont été publiés ce week-end à Lyon pour la saison"
        PAGES["https://hors-sujet.fr/z"] = f"<p>{ex}.</p>"
        p = prop()
        p["sources"][1] = {"titre": "Z", "url": "https://hors-sujet.fr/z", "extrait": ex}
        self.assertFalse(verifier(p)[0])      # la citation existe, mais ne parle pas du sujet

    def test_domaine_helper(self):
        self.assertEqual(c.domaine("https://www.lemonde.fr/x"), "lemonde.fr")
        self.assertEqual(c.domaine("https://www.bbc.co.uk/x"), "bbc.co.uk")


class TestPipeline(unittest.TestCase):
    def modele(self, reponses):
        appels = []

        def appel(prompt, modele, cle):
            appels.append(modele)
            return reponses[modele], 0.01
        return appel, appels

    def test_accepte_quand_tout_concorde(self):
        appel, appels = self.modele({v.MODELE: prop(), v.MODELE_CONFIRMATION: {"statut": "arrive", "scenario": "stable"}})
        res, motifs, cout = v.traiter(R, J, g.RACINE, "k", appel, pages)
        self.assertIsNotNone(res, motifs)
        self.assertEqual(res["controle"]["sources_verifiees"], 2)
        self.assertEqual(appels, [v.MODELE, v.MODELE_CONFIRMATION])

    def test_second_modele_en_desaccord_refuse(self):
        appel, _ = self.modele({v.MODELE: prop(), v.MODELE_CONFIRMATION: {"statut": "pas_arrive", "scenario": None}})
        res, motifs, _ = v.traiter(R, J, g.RACINE, "k", appel, pages)
        self.assertIsNone(res)
        self.assertIn("ne confirme pas", motifs[0])

    def test_desaccord_de_scenario_donne_neutre(self):
        appel, _ = self.modele({v.MODELE: prop(), v.MODELE_CONFIRMATION: {"statut": "arrive", "scenario": "degrade"}})
        res, _, _ = v.traiter(R, J, g.RACINE, "k", appel, pages)
        self.assertIsNone(res["scenario"])

    def test_pas_de_confirmation_si_controles_echouent(self):
        appel, appels = self.modele({v.MODELE: prop(sources=[]), v.MODELE_CONFIRMATION: {}})
        res, _, _ = v.traiter(R, J, g.RACINE, "k", appel, pages)
        self.assertIsNone(res)
        self.assertEqual(appels, [v.MODELE])           # pas de second appel payant inutile

    def test_erreur_du_modele_ne_publie_rien(self):
        def appel(*a):
            raise RuntimeError("panne")
        res, motifs, _ = v.traiter(R, J, g.RACINE, "k", appel, pages)
        self.assertIsNone(res)

    def test_panne_technique_ne_compte_pas_comme_essai(self):
        self.assertTrue(v.PANNES[0].startswith("appel du modèle"))
        def appel(*a):
            raise RuntimeError("panne")
        res, motifs, _ = v.traiter(R, J, g.RACINE, "k", appel, pages)
        self.assertTrue(motifs[0].startswith(v.PANNES))

    def test_candidats_echus_d_abord_et_plafonnes(self):
        rvs = [dict(R, id=f"r{i}", date=d) for i, d in enumerate(["2026-12-20", "2026-11-10", "2026-11-20", "2026-11-25", "2026-11-28"])]
        cands = v.candidats(rvs, {}, J)
        self.assertEqual(len(cands), v.MAX_PAR_PASSAGE)
        self.assertTrue(all(date.fromisoformat(r["date"]) < J for r in cands))

    def test_pas_deux_essais_le_meme_jour_ni_au_dela_du_plafond(self):
        r = dict(R, id="a", date="2026-11-10")
        self.assertEqual(v.candidats([r], {"a": {"dernier_essai": J.isoformat(), "essais": 1}}, J), [])
        self.assertEqual(v.candidats([r], {"a": {"dernier_essai": "2026-12-01", "essais": v.MAX_ESSAIS_ECHUS}}, J), [])

    def test_avant_echeance_une_fois_par_semaine(self):
        r = dict(R, id="a", date="2026-12-20")
        self.assertEqual(len(v.candidats([r], {}, J)), 1)
        self.assertEqual(v.candidats([r], {"a": {"dernier_essai": "2026-11-30"}}, J), [])
        self.assertEqual(len(v.candidats([r], {"a": {"dernier_essai": "2026-11-20"}}, J)), 1)


class TestAppliquer(unittest.TestCase):
    def test_ajoute_sans_ecraser_et_revalide(self):
        ok, _, res = verifier(prop())
        donnees = {"rendez_vous": [dict(R), dict(R, id="deja", resultat={"statut": "arrive", "date": "2026-11-01", "reponse": "x", "scenario": None,
                                                                          "sources": [{"url": "https://a.fr/x"}]})]}
        d, j, n = ap.appliquer(donnees, {}, {"resultats": {"x": res, "deja": res}, "journal": {"x": {"essais": 1}}})
        self.assertEqual(n, 1)
        self.assertEqual(d["rendez_vous"][1]["resultat"]["reponse"], "x")     # jamais écrasé
        self.assertEqual(j["x"]["essais"], 1)

    def test_resultat_invalide_jamais_ecrit(self):
        donnees = {"rendez_vous": [dict(R)]}
        with self.assertRaises(ValueError):
            ap.appliquer(donnees, {}, {"resultats": {"x": {"statut": "arrive", "date": "2026-11-28", "reponse": "r", "scenario": None, "sources": []}}})


if __name__ == "__main__":
    unittest.main()
