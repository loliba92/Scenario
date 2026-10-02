"""Tests de la file de sujets structurée (scripts/edition/sujets.py) et de ses utilisateurs :
veille (generate_hot_topics), enrichissement (enrich_sujets), brief de secours
(generate_fallback_brief), tableau de bord (update_audience), cochage (generate_post_edition).

Lancer :  python3 -m unittest discover -s scripts/edition -p "test_sujets.py" -v
Sans clé API ni réseau ; seul beautifulsoup4 est nécessaire (importé par build_html).
"""
import copy
import datetime
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts" / "seo"))

import sujets as sj  # noqa: E402

# Les tests sur des données fictives ne doivent JAMAIS lire les vrais briefs du dépôt : un brief réel
# cite un vrai `origine_id`, absent des données fictives (défaut trouvé le 1er octobre 2026, quand le
# brief du 2 octobre a cité un identifiant et a fait échouer ces tests sur main).
BRIEFS_VIDE = Path(tempfile.mkdtemp())


def verif(data, *args, **kwargs):
    kwargs.setdefault("briefs_dir", BRIEFS_VIDE)
    return sj.verifier(data, *args, **kwargs)


CONTEXTE_LONG = ("Le 3 octobre 2026, le pays X a annoncé une mesure sans précédent qui touche 12 millions de "
                 "personnes ; les marchés ont réagi dès l'ouverture et trois grands acteurs ont répliqué.")
RATIONNEL_LONG = ("Le sujet bascule maintenant parce que l'échéance approche ; l'issue reste ouverte car les "
                  "forces en présence s'équilibrent, et un lecteur français est directement concerné.")


def mini_md():
    """Un fichier au format v2 (commentaires étiquetés) ET à l'ancien format (note libre)."""
    return f"""# Sujets prioritaires — Test

Texte d'en-tête.

---

## 🔥 Priorité absolue (n'importe quel jour, avant tout le reste)
<!-- intro urgente -->
- [x] Sujet urgent déjà publié ? [géopolitique]
  <!-- Ajouté le 6 septembre 2026, contexte -->

## Culture — samedi
<!-- Lot ajouté le 3 septembre 2026 : idées -->
- [ ] La Chine peut-elle créer la prochaine pop culture mondiale ? Cinéma, jeux, musique, plateformes. [culture & géopolitique]
  <!-- Reformulation de "favori #6". Problématique : Pékin investit massivement et ses jeux et films s'exportent. → 3 scénarios (brouillon) : favorable = A gagne ; stable = rien ne bouge ; dégradé = B domine. Sources : Le Monde, Variety. Angle : le soft power. À vérifier/chiffrer avant rédaction : parts de marché. -->
- [ ] 🔍 Proposition automatique non validée [culture]
  <!-- Ajouté automatiquement le 2026-09-18 (veille) — à valider. -->
- [ ] Sujet complet au format v2 ? [culture]
  <!-- contexte: {CONTEXTE_LONG} -->
  <!-- rationnel: {RATIONNEL_LONG} -->
  <!-- mots-clés: réforme X ; marchés ; taux directeur ; Y -->
  <!-- origine: utilisateur -->
- [ ] Sujet sans tag ni note

## Économie & finance mondiale — jeudi
- [ ] Bitcoin : le bitcoin devient-il un actif institutionnel ? [économie & finance]
- [ ] Bitcoin : le bitcoin devient-il un actif institutionnel ? [économie & finance]
"""


def par_debut(d, debut):
    return next(e for _, e in sj.sujets(d) if e["titre"].startswith(debut))


class ConversionTest(unittest.TestCase):
    def test_lecture_des_champs(self):
        d = sj.parse_md(mini_md())
        self.assertEqual(d["version"], 2)
        self.assertEqual([s["cle"] for s in d["sections"]], ["priorite_absolue", "culture", "economie"])
        self.assertEqual(d["sections"][1]["jour"], "samedi")
        urgent = par_debut(d, "Sujet urgent")
        self.assertEqual((urgent["statut"], urgent["ajoute_le"]), ("publie", "2026-09-06"))
        prop = par_debut(d, "Proposition")
        self.assertEqual((prop["validation"], prop["origine"], prop["ajoute_le"]), ("a_valider", "veille", "2026-09-18"))
        self.assertEqual(len({e["id"] for _, e in sj.sujets(d)}), 7, "les doublons de titre reçoivent des ids distincts")
        self.assertEqual(sum(1 for s in d["sections"] for e in s["entrees"] if e["type"] == "commentaire"), 2)

    def test_ancien_format_range_dans_les_champs(self):
        e = par_debut(sj.parse_md(mini_md()), "La Chine")
        self.assertEqual(e["titre"], "La Chine peut-elle créer la prochaine pop culture mondiale ?")
        self.assertEqual(e["tag"], "culture & géopolitique")
        # l'explication collée au « ? » et la « Problématique » deviennent le contexte
        self.assertIn("Cinéma, jeux, musique, plateformes.", e["contexte"])
        self.assertIn("Pékin investit massivement", e["contexte"])
        self.assertEqual(e["scenarios"], {"favorable": "A gagne", "stable": "rien ne bouge", "degrade": "B domine"})
        self.assertEqual(e["sources"], [{"titre": "Le Monde, Variety", "url": None}])
        self.assertEqual(e["angle"], "Le soft power", "majuscule initiale")
        self.assertEqual(e["a_verifier"], "Parts de marché")
        self.assertEqual(e["origine"], "utilisateur")
        self.assertEqual(e["note"], 'Reformulation de "favori #6"', "ne reste dans la note que la méta-information")
        self.assertEqual(e["mots_cles"], [])
        self.assertEqual(e["rationnel"], None)

    def test_ancienne_note_de_la_veille_separe_methode_et_contenu(self):
        md = ("# T\n\n## Géopolitique — lundi\n- [ ] Élections russes ? [géopolitique]\n"
              "  <!-- Ajouté automatiquement le 2026-09-18 (recherche OpenRouter, voir scripts/edition/generate_hot_topics.py) — validé. "
              "Repéré en veille sur le registre Géopolitique, remonté ici pour son urgence. Les Russes votent du 18 au 20 septembre pour "
              "renouveler 450 sièges. La question est : le verrouillage tiendra-t-il ? → 3 scénarios (brouillon) : favorable = a ; stable = b ; dégradé = c -->\n")
        e = par_debut(sj.parse_md(md), "Élections")
        self.assertTrue(e["contexte"].startswith("Les Russes votent"))
        self.assertIn("verrouillage tiendra-t-il", e["contexte"])
        self.assertTrue(e["note"].startswith("Ajouté automatiquement le 2026-09-18"))
        self.assertNotIn("Les Russes", e["note"])
        self.assertEqual((e["origine"], e["ajoute_le"]), ("veille", "2026-09-18"))
        self.assertEqual(e["scenarios"]["degrade"], "c")

    def test_format_v2_lu_tel_quel(self):
        e = par_debut(sj.parse_md(mini_md()), "Sujet complet")
        self.assertEqual(e["contexte"], CONTEXTE_LONG)
        self.assertEqual(e["rationnel"], RATIONNEL_LONG)
        self.assertEqual(e["mots_cles"], ["réforme X", "marchés", "taux directeur", "Y"])
        self.assertEqual(e["origine"], "utilisateur")
        self.assertIsNone(e["note"])

    def test_echeance_depuis_la_note(self):
        md = "# T\n\n## Sciences — vendredi\n- [ ] Octobre rose ? [santé]\n  <!-- Ajouté le 25 septembre 2026, à traiter vendredi 2 octobre. -->\n"
        e = par_debut(sj.parse_md(md), "Octobre rose")
        self.assertEqual(e["echeance"]["date"], "2026-10-02")

    def test_aller_retour_stable(self):
        d = sj.parse_md(mini_md())
        md = sj.render_md(d)
        d2 = sj.parse_md(md, d)
        self.assertEqual(sj.render_md(d2), md)
        self.assertEqual(json.dumps(d, sort_keys=True), json.dumps(d2, sort_keys=True))

    def test_tous_les_champs_survivent_a_la_vue_markdown(self):
        d = sj.parse_md(mini_md())
        e = par_debut(d, "Sujet sans tag")
        e.update(question="Une question précise ?", contexte=CONTEXTE_LONG, rationnel=RATIONNEL_LONG, angle="Un angle",
                 a_verifier="Un point", mots_cles=["a b", "c"], scenarios={"favorable": "f", "stable": "s", "degrade": "d"},
                 echeance={"date": "2026-11-05", "raison": "vote"},
                 sources=[{"titre": "Le Monde", "url": "https://x.fr/a"}, {"titre": "Notes", "url": None}],
                 origine="veille", enrichi_le="2026-10-02", note="Méta\nsur deux lignes")
        d2 = sj.parse_md(sj.render_md(d), d)
        e2 = par_debut(d2, "Sujet sans tag")
        for k in ("question", "contexte", "rationnel", "angle", "a_verifier", "mots_cles", "scenarios", "echeance",
                  "sources", "origine", "enrichi_le", "note"):
            self.assertEqual(e2[k], e[k], k)

    def test_texte_inattendu_refuse(self):
        with self.assertRaises(sj.SujetsError):
            sj.parse_md("# T\n\n## Culture — samedi\nune ligne libre perdue\n")

    def test_fichier_reel_aller_retour(self):
        data = json.loads((ROOT / "data" / "sujets.json").read_text(encoding="utf-8"))
        md = sj.render_md(data)
        d2 = sj.parse_md(md, data)
        data["meta"]["md_sha256"] = d2["meta"]["md_sha256"] = ""
        self.assertEqual(json.dumps(d2, sort_keys=True), json.dumps(data, sort_keys=True))


class CompletudeTest(unittest.TestCase):
    def test_manquants(self):
        d = sj.parse_md(mini_md())
        self.assertEqual(sj.manquants(par_debut(d, "Sujet complet")), [])
        self.assertTrue(sj.est_complet(par_debut(d, "Sujet complet")))
        m = sj.manquants(par_debut(d, "Sujet sans tag"))
        self.assertEqual(set(m), {"question", "contexte", "rationnel", "mots_cles"})
        self.assertNotIn("question", sj.manquants(par_debut(d, "La Chine")), "le titre est une question")

    def test_incomplets_ordre_et_filtre(self):
        d = sj.parse_md(mini_md())
        ids = [e["titre"][:10] for _, e in sj.incomplets(d)]
        self.assertNotIn("Sujet comp", ids)
        self.assertNotIn("Sujet urge", ids, "un sujet publié n'est pas à enrichir")


class CocherTest(unittest.TestCase):
    def setUp(self):
        self.d = sj.parse_md(mini_md())

    def etat(self, debut):
        return [e["statut"] for _, e in sj.sujets(self.d) if e["titre"].startswith(debut)]

    def test_par_identifiant(self):
        pop = par_debut(self.d, "La Chine")
        ids = sj.check_off(self.d, {"date": "2026-09-26", "sujet": {"origine_id": pop["id"]}})
        self.assertEqual(ids, [pop["id"]])
        self.assertEqual((pop["statut"], pop["publie_le"], pop["edition"]), ("publie", "2026-09-26", "2026-09-26"))

    def test_identifiant_recopie_avec_prefixe_ou_balises(self):
        for brut in ("id: {i}", "<!-- id: {i} -->", "  {i}  "):
            d = sj.parse_md(mini_md())
            pop = par_debut(d, "La Chine")
            self.assertEqual(sj.check_off(d, {"date": "2026-09-26", "sujet": {"origine_id": brut.format(i=pop["id"])}}), [pop["id"]], brut)

    def test_origine_recopiee_avec_puce_et_tag(self):
        """Cas réel du 26/09 : origine_prioritaire = ligne complète avec « - [ ] » et tag."""
        brief = {"date": "2026-09-26", "sujet": {"origine_prioritaire":
                 "- [ ] La Chine peut-elle créer la prochaine pop culture mondiale ? Cinéma, jeux, musique, plateformes. [culture & géopolitique]"}}
        # le titre du sujet est maintenant la seule question : le texte complet n'en est plus l'égalité,
        # le repli par le titre du brief prend le relais
        brief["sujet"]["titre_propose"] = "La Chine peut-elle créer la prochaine pop culture mondiale ?"
        self.assertEqual(len(sj.check_off(self.d, brief)), 1)
        self.assertEqual(self.etat("La Chine"), ["publie"])

    def test_sujet_repris_sans_origine_par_le_titre(self):
        """Cas réel du 01/10 : pas d'origine, mais le titre du brief est la ligne de la file ;
        les deux occurrences (doublon de la veille) sont cochées."""
        brief = {"date": "2026-10-01", "sujet": {"origine_prioritaire": None,
                 "titre_propose": "Bitcoin : le bitcoin devient-il un actif institutionnel ?"}}
        self.assertEqual(len(sj.check_off(self.d, brief)), 2)
        self.assertEqual(self.etat("Bitcoin"), ["publie", "publie"])

    def test_titre_court_ignore(self):
        self.assertEqual(sj.check_off(self.d, {"date": "2026-10-01", "sujet": {"titre_propose": "Sujet sans"}}), [])

    def test_deja_publie_non_recoche(self):
        brief = {"date": "2026-09-26", "sujet": {"origine_prioritaire": "Sujet urgent déjà publié ?"}}
        self.assertEqual(sj.check_off(self.d, brief), [])
        self.assertIsNone(par_debut(self.d, "Sujet urgent")["publie_le"])

    def test_aucune_correspondance(self):
        self.assertEqual(sj.check_off(self.d, {"date": "2026-10-02", "sujet": {"titre_propose": "Un titre totalement différent de la file"}}), [])


class AjoutEtEnrichissementTest(unittest.TestCase):
    def test_ajout_en_tete_a_valider(self):
        d = sj.parse_md(mini_md())
        sj.ajouter(d, "culture", "Nouveau sujet de veille ?", tag="culture", contexte=CONTEXTE_LONG, rationnel=RATIONNEL_LONG,
                   mots_cles=["a", "b", "c"], origine="veille", ajoute_le="2026-10-02")
        sec = next(s for s in d["sections"] if s["cle"] == "culture")
        premiers = [e for e in sec["entrees"] if e["type"] == "sujet"]
        self.assertEqual(premiers[0]["titre"], "Nouveau sujet de veille ?")
        self.assertEqual(sec["entrees"][0]["type"], "commentaire", "le commentaire d'intro reste en tête")
        self.assertIn("- [ ] 🔍 Nouveau sujet de veille ? [culture]", sj.render_md(d))
        self.assertEqual(verif(d), [])

    def test_ids_uniques_champs_inconnus_section_inconnue(self):
        d = sj.parse_md(mini_md())
        a = sj.ajouter(d, "culture", "Même texte ?")
        b = sj.ajouter(d, "culture", "Même texte ?")
        self.assertNotEqual(a["id"], b["id"])
        with self.assertRaises(sj.SujetsError):
            sj.ajouter(d, "inconnue", "x")
        with self.assertRaises(sj.SujetsError):
            sj.ajouter(d, "culture", "x", champ_inventé="y")

    def test_valider_passe_a_valide_et_rend_eligible(self):
        d = sj.parse_md(mini_md())
        a = sj.ajouter(d, "culture", "Sujet proposé ?")
        b = sj.ajouter(d, "culture", "Autre sujet proposé ?")
        self.assertFalse(sj.eligible(a))
        faits, inconnus = sj.valider(d, [a["id"], "n-existe-pas"])
        self.assertEqual((faits, inconnus), ([a["id"]], ["n-existe-pas"]))
        self.assertTrue(sj.eligible(a))
        self.assertFalse(sj.eligible(b), "les autres sujets ne changent pas")
        self.assertEqual(sj.valider(d, [a["id"]]), ([], []), "déjà validé : rien à faire")
        self.assertNotIn("🔍 Sujet proposé", sj.render_md(d))
        self.assertEqual(verif(d), [])

    def test_prioriser_puis_deprioriser(self):
        d = sj.parse_md(mini_md())
        e = par_debut(d, "La Chine")
        ident = e["id"]
        self.assertTrue(ident.startswith("culture-"))
        faits, inconnus, ignores = sj.prioriser(d, [ident, "n-existe-pas"])
        self.assertEqual((faits, inconnus, ignores), ([ident], ["n-existe-pas"], []))
        sec = next(s for s in d["sections"] if s["cle"] == "priorite_absolue")
        self.assertEqual([x["id"] for x in sec["entrees"] if x["type"] == "sujet"][0], ident, "en tête de la priorité")
        self.assertEqual(sec["entrees"][0]["type"], "commentaire", "le commentaire d'intro reste en tête")
        self.assertNotIn(ident, [x["id"] for s in d["sections"] if s["cle"] == "culture" for x in s["entrees"] if x["type"] == "sujet"])
        self.assertEqual(e["validation"], "valide")
        self.assertEqual(sj.sujet_du_jour(d, "economie")[1]["id"], ident, "traité avant le registre du jour")
        self.assertEqual(verif(d), [])
        d2 = sj.parse_md(sj.render_md(d))   # la vue Markdown garde le sujet en priorité
        self.assertEqual(next(s for s in d2["sections"] if s["cle"] == "priorite_absolue")["entrees"][1]["titre"], e["titre"])
        self.assertEqual(sj.prioriser(d, [ident]), ([], [], [ident]), "déjà en priorité : ignoré")

        faits, _, _ = sj.deprioriser(d, [ident])
        self.assertEqual(faits, [ident])
        culture = next(s for s in d["sections"] if s["cle"] == "culture")
        self.assertEqual([x["id"] for x in culture["entrees"] if x["type"] == "sujet"][0], ident)
        self.assertEqual(sj.deprioriser(d, [ident]), ([], [], [ident]), "plus en priorité : ignoré")

    def test_prioriser_ignore_un_sujet_publie(self):
        d = sj.parse_md(mini_md())
        publie = next(e for _, e in sj.sujets(d) if e["statut"] == "publie")
        self.assertEqual(sj.prioriser(d, [publie["id"]]), ([], [], [publie["id"]]))

    def test_enrichir_ne_remplit_que_l_absent(self):
        e = par_debut(sj.parse_md(mini_md()), "La Chine")
        contexte_avant = e["contexte"]
        faits = sj.enrichir(e, {"contexte": "AUTRE CONTEXTE", "rationnel": RATIONNEL_LONG, "mots_cles": ["a", "b", "c"],
                                "id": "pirate", "statut": "publie"}, "2026-10-02")
        self.assertEqual(sorted(faits), ["mots_cles", "rationnel"])
        self.assertEqual(e["contexte"], contexte_avant, "un champ déjà écrit n'est jamais écrasé")
        self.assertNotEqual(e["id"], "pirate")
        self.assertEqual((e["statut"], e["enrichi_le"]), ("a_traiter", "2026-10-02"))
        self.assertEqual(sj.enrichir(e, {"rationnel": "autre"}), [])

    def test_enrichir_complete_les_mots_cles_sans_rien_retirer(self):
        e = par_debut(sj.parse_md(mini_md()), "Sujet sans tag")
        e["mots_cles"] = ["déjà là"]
        faits = sj.enrichir(e, {"mots_cles": ["Déjà là", "nouveau un", "nouveau deux"]}, "2026-10-02")
        self.assertEqual(faits, ["mots_cles"])
        self.assertEqual(e["mots_cles"], ["déjà là", "nouveau un", "nouveau deux"], "l'existant reste, sans doublon")
        # assez de mots-clés : on n'y touche plus
        self.assertEqual(sj.enrichir(e, {"mots_cles": ["encore un autre"]}), [])
        self.assertEqual(len(e["mots_cles"]), 3)

    def test_veille_dossier_depuis_la_reponse_du_modele(self):
        import generate_hot_topics as ht
        rep = {"accroche": "x ?", "contexte": CONTEXTE_LONG, "rationnel": RATIONNEL_LONG,
               "mots_cles": ["Taux", "taux", "  marchés ", "", "Y"],
               "sources": [{"titre": "Le Monde", "url": "https://reel.fr/a"}, {"titre": "Inventé", "url": "https://faux.fr/b"}, {"titre": ""}],
               "scenarios": {"favorable": "f", "stable": "s", "degrade": "d"},
               "echeance": {"date": "2026-11-05", "raison": "vote"}}
        c = ht.dossier_depuis_reponse(rep, ["https://reel.fr/a"])
        self.assertEqual(c["mots_cles"], ["Taux", "marchés", "Y"], "dédoublonnés, nettoyés")
        self.assertEqual(c["sources"], [{"titre": "Le Monde", "url": "https://reel.fr/a"}, {"titre": "Inventé", "url": None}],
                         "une URL absente des citations réelles n'est pas gardée")
        self.assertEqual(c["echeance"], {"date": "2026-11-05", "raison": "vote"})
        self.assertIsNone(ht.dossier_depuis_reponse({"scenarios": {"favorable": "f"}})["scenarios"])
        self.assertIsNone(ht.dossier_depuis_reponse({"echeance": {"date": "demain"}})["echeance"])

    def test_veille_insertion_et_titres(self):
        import generate_hot_topics as ht
        d = sj.parse_md(mini_md())
        entrees = [({"accroche": "Premier ajout ?", "tag": "culture", "contexte": CONTEXTE_LONG, "rationnel": RATIONNEL_LONG,
                     "mots_cles": ["a", "b", "c", "d"]}, None),
                   ({"accroche": "Second ajout ?", "contexte": CONTEXTE_LONG, "rationnel": RATIONNEL_LONG,
                     "scenarios": {"favorable": "a", "stable": "b", "degrade": "c"}}, "Sport")]
        ht.insert_entries(d, "## Culture — samedi", entrees, datetime.date(2026, 10, 2))
        titres = [e["titre"] for e in next(s for s in d["sections"] if s["cle"] == "culture")["entrees"] if e["type"] == "sujet"]
        self.assertEqual(titres[:2], ["Premier ajout ?", "Second ajout ?"], "l'ordre reçu est conservé")
        second = par_debut(d, "Second ajout")
        self.assertEqual((second["origine"], second["validation"], second["ajoute_le"]), ("veille", "a_valider", "2026-10-02"))
        self.assertIn("Repéré en veille sur le registre Sport", second["note"])
        self.assertNotIn("scénarios", second["note"].lower(), "la note ne contient que la méthode, pas le fond")
        self.assertEqual(second["scenarios"]["favorable"], "a")
        self.assertEqual(sj.manquants(par_debut(d, "Premier ajout")), [], "dossier complet")
        self.assertIn("mots_cles", sj.manquants(second))
        before = ht.titles_in_section(d, "## Culture — samedi")
        self.assertTrue(any(t.startswith(sj.MARQUE_A_VALIDER) for t in before), "les titres gardent la marque 🔍")

    def test_enrichissement_applique_un_resultat(self):
        import enrich_sujets as en
        e = par_debut(sj.parse_md(mini_md()), "Sujet sans tag")
        faits = en.appliquer_resultat(e, {"depasse": False, "contexte": CONTEXTE_LONG, "rationnel": RATIONNEL_LONG,
                                           "mots_cles": ["a", "b", "c"], "sources": [{"titre": "S", "url": "https://u.fr"}]},
                                      ["https://u.fr"], datetime.date(2026, 10, 2))
        self.assertEqual(sorted(faits), ["contexte", "mots_cles", "rationnel", "sources"])
        self.assertTrue(sj.est_complet(e) or sj.manquants(e) == ["question"])
        self.assertEqual(e["sources"][0]["url"], "https://u.fr")

    def test_enrichissement_signale_un_sujet_depasse(self):
        import enrich_sujets as en
        e = par_debut(sj.parse_md(mini_md()), "La Chine")
        en.appliquer_resultat(e, {"depasse": True, "raison": "l'accord a été signé"}, [], datetime.date(2026, 10, 2))
        self.assertIn("Peut-être dépassé", e["a_verifier"])
        self.assertIn("l'accord a été signé", e["a_verifier"])
        self.assertIn("Parts de marché", e["a_verifier"], "l'existant est conservé")
        self.assertEqual(e["statut"], "a_traiter", "le sujet n'est jamais retiré automatiquement")

    def test_enrichissement_ordre_et_prompt(self):
        import enrich_sujets as en
        d = sj.parse_md(mini_md())
        cibles = en.ordre_de_passage(d, sj.incomplets(d))
        self.assertTrue(cibles)
        sec, e = cibles[0]
        p = en.construire_prompt(sec, e, datetime.date(2026, 10, 2))
        self.assertIn("rationnel", p)
        self.assertIn("n'invente AUCUN fait", p)
        self.assertIn(e["titre"], p)


class SynchroTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.dp, self.mp = self.tmp / "data" / "sujets.json", self.tmp / "sujets.md"
        sj.save_both(sj.parse_md(mini_md()), self.dp, self.mp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_a_jour(self):
        self.assertEqual(sj.load_synced(self.dp, self.mp)[1], "ok")

    def test_ancienne_version_refusee(self):
        d = json.loads(self.dp.read_text(encoding="utf-8"))
        d["version"] = 1
        self.dp.write_text(json.dumps(d), encoding="utf-8")
        with self.assertRaises(sj.SujetsError):
            sj.load_synced(self.dp, self.mp)

    def test_modification_du_markdown_reprise(self):
        self.mp.write_text(self.mp.read_text(encoding="utf-8").replace("- [ ] Sujet sans tag ni note", "- [x] Sujet sans tag ni note"), encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "md_repris")
        self.assertEqual(par_debut(data, "Sujet sans tag")["statut"], "publie")
        ids_avant = {e["id"] for _, e in sj.sujets(json.loads(self.dp.read_text(encoding="utf-8")))}
        self.assertEqual({e["id"] for _, e in sj.sujets(data)}, ids_avant, "les identifiants sont conservés")

    def test_champ_du_dossier_modifie_dans_le_markdown(self):
        md = self.mp.read_text(encoding="utf-8").replace("<!-- origine: utilisateur -->", "<!-- origine: utilisateur -->\n  <!-- angle: un angle ajouté à la main -->")
        self.mp.write_text(md, encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "md_repris")
        self.assertEqual(par_debut(data, "Sujet complet")["angle"], "un angle ajouté à la main")

    def test_nouveau_sujet_ajoute_a_la_main_dans_le_markdown(self):
        # ligne insérée AVANT les commentaires du sujet précédent : l'identifiant ne doit pas être « volé »
        md = self.mp.read_text(encoding="utf-8")
        md = md.replace("- [ ] Sujet complet au format v2 ? [culture]",
                        "- [ ] Sujet complet au format v2 ? [culture]\n- [ ] Ajout manuel dans le markdown [culture]")
        self.mp.write_text(md, encoding="utf-8")
        avant = par_debut(json.loads(self.dp.read_text(encoding="utf-8")), "Sujet complet")["id"]
        data, _ = sj.load_synced(self.dp, self.mp)
        nouveau = par_debut(data, "Ajout manuel")
        self.assertTrue(nouveau["id"].startswith("culture-ajout-manuel"))
        self.assertEqual(par_debut(data, "Sujet complet")["id"], avant, "le sujet garde son identifiant")

    def test_correction_du_texte_garde_l_identifiant_et_les_metadonnees(self):
        d0 = json.loads(self.dp.read_text(encoding="utf-8"))
        cible = par_debut(d0, "Sujet sans tag")
        cible.update(publie_le="2026-09-01", edition="2026-09-01", statut="publie")
        sj.save_both(d0, self.dp, self.mp)
        self.mp.write_text(self.mp.read_text(encoding="utf-8").replace("Sujet sans tag ni note", "Sujet sans tag ni note (corrigé)"), encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "md_repris")
        e = par_debut(data, "Sujet sans tag ni note (corrigé)")
        self.assertEqual((e["id"], e["edition"]), (cible["id"], "2026-09-01"))

    def test_modification_du_json_reprise(self):
        d = json.loads(self.dp.read_text(encoding="utf-8"))
        par_debut(d, "Sujet sans tag")["statut"] = "publie"
        self.dp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "json_repris")
        sj.save_both(data, self.dp, self.mp)
        self.assertIn("- [x] Sujet sans tag ni note", self.mp.read_text(encoding="utf-8"))
        self.assertEqual(sj.load_synced(self.dp, self.mp)[1], "ok")

    def test_conflit_refuse(self):
        d = json.loads(self.dp.read_text(encoding="utf-8"))
        par_debut(d, "Sujet sans tag")["statut"] = "publie"
        self.dp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        self.mp.write_text(self.mp.read_text(encoding="utf-8").replace("Bitcoin :", "Bitcoin ;"), encoding="utf-8")
        with self.assertRaises(sj.SujetsConflict):
            sj.load_synced(self.dp, self.mp)

    def test_cochage_apres_publication_de_bout_en_bout(self):
        """check_off_priority_topic() réel, sur une copie : le JSON ET la vue sont mis à jour."""
        import generate_post_edition as gpe
        ancien = gpe.REPO_ROOT
        gpe.REPO_ROOT = self.tmp
        (self.tmp / "sujets-prioritaires.md").write_text(self.mp.read_text(encoding="utf-8"), encoding="utf-8")
        try:
            gpe.check_off_priority_topic({"date": "2026-09-26", "sujet": {
                "titre_propose": "La Chine peut-elle créer la prochaine pop culture mondiale ?"}})
        finally:
            gpe.REPO_ROOT = ancien
        d = json.loads((self.tmp / "data" / "sujets.json").read_text(encoding="utf-8"))
        pop = par_debut(d, "La Chine")
        self.assertEqual((pop["statut"], pop["edition"]), ("publie", "2026-09-26"))
        self.assertIn("- [x] La Chine", (self.tmp / "sujets-prioritaires.md").read_text(encoding="utf-8"))
        self.assertEqual(sj.load_synced(self.tmp / "data" / "sujets.json", self.tmp / "sujets-prioritaires.md")[1], "ok")


class SujetDuJourTest(unittest.TestCase):
    def test_priorite_puis_registre_du_jour(self):
        d = sj.parse_md(mini_md())
        # samedi (2026-10-03) : « Priorité absolue » n'a rien d'éligible (publié) → culture
        sec, e = sj.sujet_du_jour(d, jour=datetime.date(2026, 10, 3))
        self.assertEqual((sec["cle"], e["titre"][:7]), ("culture", "La Chin"))
        # une priorité absolue valide passe avant tout
        sj.ajouter(d, "priorite_absolue", "Urgent du jour ?", validation="valide")
        sec, e = sj.sujet_du_jour(d, jour=datetime.date(2026, 10, 3))
        self.assertEqual((sec["cle"], e["titre"]), ("priorite_absolue", "Urgent du jour ?"))

    def test_saute_publie_et_a_valider(self):
        d = sj.parse_md(mini_md())
        par_debut(d, "La Chine")["statut"] = "publie"
        sec, e = sj.sujet_du_jour(d, jour=datetime.date(2026, 10, 3))
        self.assertTrue(e["titre"].startswith("Sujet complet"), "le 🔍 « Proposition » est sauté")

    def test_aucun_sujet_eligible(self):
        d = sj.parse_md(mini_md())
        for _, e in sj.sujets(d):
            e["statut"] = "publie"
        self.assertIsNone(sj.sujet_du_jour(d, jour=datetime.date(2026, 10, 3)))

    def test_dossier_texte(self):
        d = sj.parse_md(mini_md())
        sec, e = sj.sujet_du_jour(d, "culture")
        t = sj.dossier_texte(sec, e)
        self.assertIn(e["id"], t)
        self.assertIn("origine_id", t)
        self.assertIn("Dossier incomplet", t)
        self.assertIn("favorable = A gagne", t)
        complet = par_debut(d, "Sujet complet")
        t2 = sj.dossier_texte(sec, complet)
        self.assertIn("Mots-clés pour chercher les articles : réforme X ; marchés", t2)
        self.assertNotIn("Dossier incomplet", t2)

    def test_cli_prochain_et_sujet_du_jour_reel(self):
        data = json.loads((ROOT / "data" / "sujets.json").read_text(encoding="utf-8"))
        for jour in range(7):
            r = sj.sujet_du_jour(data, jour=datetime.date(2026, 10, 5 + jour))
            self.assertIsNotNone(r, f"jour {jour} : un sujet éligible doit exister")


class VerificationTest(unittest.TestCase):
    def test_donnees_valides(self):
        d = sj.parse_md(mini_md())
        sj.save_both(d, Path(tempfile.mkdtemp()) / "s.json", Path(tempfile.mkdtemp()) / "s.md")
        self.assertEqual(verif(d, sj.render_md(d)), [])

    def test_detecte_les_donnees_invalides(self):
        d = sj.parse_md(mini_md())
        subs = [e for _, e in sj.sujets(d)]
        subs[1]["id"] = subs[0]["id"]
        subs[2]["statut"] = "inconnu"
        subs[3]["validation"] = "peut-etre"
        subs[4]["mots_cles"] = "pas une liste"
        subs[5]["scenarios"] = {"favorable": "x"}
        subs[6]["origine"] = "alien"
        pb = " | ".join(verif(d))
        for attendu in ("en double", "statut invalide", "validation invalide", "mots_cles doit", "scenarios doit", "origine invalide"):
            self.assertIn(attendu, pb)

    def test_desynchronisation_simple_n_est_pas_une_erreur_mais_le_conflit_si(self):
        d = sj.parse_md(mini_md())
        md = sj.render_md(d)
        d["meta"]["md_sha256"] = sj.sha(md)
        self.assertIsNone(sj.desynchronisation(d, md))
        self.assertEqual(sj.desynchronisation(d, md + "\n"), "md")
        self.assertEqual(verif(d, md + "\n"), [], "modification du Markdown seul : se répare par sync")
        d2 = copy.deepcopy(d)
        next(e for _, e in sj.sujets(d2))["statut"] = "a_traiter"
        self.assertEqual(sj.desynchronisation(d2, md), "json")
        self.assertEqual(sj.desynchronisation(d2, md + "\n"), "conflit")
        self.assertTrue(any("conflit" in p for p in verif(d2, md + "\n")))

    def test_sujet_deja_publie_encore_a_traiter(self):
        d = sj.parse_md(mini_md())
        editions = {"2026-09-26": {sj.norm("La Chine peut-elle créer la prochaine pop culture mondiale ?")}}
        pb = verif(d, editions=editions)
        self.assertTrue(any("2026-09-26" in p and "culture" in p for p in pb), pb)

    def test_origine_id_inconnu_dans_un_brief(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "2026-10-02.json").write_text(json.dumps({"sujet": {"origine_id": "n-existe-pas"}}), encoding="utf-8")
        pb = verif(sj.parse_md(mini_md()), briefs_dir=tmp)
        self.assertTrue(any("n-existe-pas" in p for p in pb), pb)

    def test_fichiers_du_depot_coherents(self):
        """Garde-fou : le JSON et la vue du dépôt sont cohérents, ids uniques, briefs valides."""
        data = json.loads((ROOT / "data" / "sujets.json").read_text(encoding="utf-8"))
        md = (ROOT / "sujets-prioritaires.md").read_text(encoding="utf-8")
        self.assertEqual(sj.verifier(data, md, sj.editions_publiees()), [])
        self.assertIsNone(sj.desynchronisation(data, md), "data/sujets.json et sujets-prioritaires.md doivent être synchronisés")


class LecteursExistantsTest(unittest.TestCase):
    """La vue Markdown reste lisible par les scripts qui ne passent pas par sujets.py."""

    def test_tableau_de_bord_depuis_le_json(self):
        import update_audience as ua
        data = json.loads((ROOT / "data" / "sujets.json").read_text(encoding="utf-8"))
        cards, later, prio = ua.build_agenda(sj.render_md(data))
        self.assertEqual(len(cards), 7)
        self.assertTrue(all(c["topic"] for c in cards))
        self.assertTrue(all(len(c["topic"]) < 140 for c in cards), "la carte affiche la question, pas un paragraphe")

    def test_routine_voit_le_dossier_dans_la_vue(self):
        md = (ROOT / "sujets-prioritaires.md").read_text(encoding="utf-8")
        self.assertIn("<!-- id: ", md)
        self.assertRegex(md, r"<!-- contexte: ")

    def test_page_cachee_et_bouton_du_dashboard(self):
        dash = (ROOT / "dashboard.html").read_text(encoding="utf-8")
        self.assertIn('href="file-sujets.html"', dash)
        page = (ROOT / "file-sujets.html").read_text(encoding="utf-8")
        self.assertIn('content="noindex, nofollow"', page)
        # la page ne doit jamais être ajoutée au sitemap
        self.assertNotIn("file-sujets", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        # la règle de complétude de la page reproduit celle de sujets.py
        js = (ROOT / "assets" / "file-sujets.js").read_text(encoding="utf-8")
        for const, val in (("MIN_CONTEXTE", sj.MIN_CONTEXTE), ("MIN_RATIONNEL", sj.MIN_RATIONNEL), ("MIN_MOTS_CLES", sj.MIN_MOTS_CLES)):
            self.assertRegex(js, rf"{const}\s*=\s*{val}\b")


class PointDeDepartTest(unittest.TestCase):
    """Le dossier du sujet est le point de départ du brief (en JSON), et l'identifiant est fixé par le code."""

    def test_dossier_json(self):
        d = sj.parse_md(mini_md())
        sec = next(s for s in d["sections"] if s["cle"] == "culture")
        e = par_debut(d, "Sujet complet")
        j = sj.dossier_json(sec, e)
        self.assertEqual((j["id"], j["registre"], j["titre"]), (e["id"], "culture", e["titre"]))
        self.assertEqual(j["mots_cles"], ["réforme X", "marchés", "taux directeur", "Y"])
        self.assertEqual(j["dossier_incomplet"], [])
        self.assertEqual(sj.dossier_json(sec, par_debut(d, "Sujet sans tag"))["dossier_incomplet"],
                         sj.manquants(par_debut(d, "Sujet sans tag")))
        json.dumps(j)  # sérialisable

    def test_timbrer_brief(self):
        d = sj.parse_md(mini_md())
        e = par_debut(d, "Sujet complet")
        brief = {"sujet": {"titre_propose": "x", "origine_id": f"id: {e['id']}"}}
        self.assertEqual(sj.timbrer_brief(brief, d), e["id"])
        self.assertEqual(brief["sujet"]["origine_id"], e["id"], "l'identifiant est normalisé")
        self.assertEqual(brief["sujet"]["point_de_depart"]["contexte"], CONTEXTE_LONG)
        e["contexte"] = "Contexte mis à jour " + CONTEXTE_LONG
        sj.timbrer_brief(brief, d)
        self.assertTrue(brief["sujet"]["point_de_depart"]["contexte"].startswith("Contexte mis à jour"), "idempotent, version à jour")

    def test_timbrer_sans_sujet_de_la_file(self):
        d = sj.parse_md(mini_md())
        for sujet in ({"origine_id": None}, {"origine_id": "n-existe-pas"}, {}):
            brief = {"sujet": dict(sujet)}
            self.assertIsNone(sj.timbrer_brief(brief, d))
            self.assertNotIn("point_de_depart", brief["sujet"])
        self.assertIsNone(sj.timbrer_brief({}, d))

    def test_la_redaction_ne_voit_jamais_le_point_de_depart(self):
        import generate_daily_edition as gde
        brief = {"date": "2026-10-03", "sujet": {"titre_propose": "T", "origine_id": "x", "point_de_depart": {"contexte": "PISTE NON VÉRIFIÉE"}},
                 "faits_verifies": ["fait vérifié"]}
        p = gde.build_user_prompt("CONSIGNES", brief)
        self.assertNotIn("PISTE NON VÉRIFIÉE", p)
        self.assertNotIn("point_de_depart", p)
        self.assertIn("fait vérifié", p)
        self.assertIn("point_de_depart", json.dumps(brief), "le brief d'origine n'est pas modifié")

    def test_brief_de_secours_donne_le_json_et_ancre_l_identifiant(self):
        import generate_fallback_brief as gfb
        texte = gfb.dossier_du_jour("2026-10-03")           # samedi : culture, d'après les vraies données
        debut = texte.index("{")
        dossier, _ = json.JSONDecoder().raw_decode(texte[debut:])
        self.assertEqual(dossier["registre"], "culture")
        self.assertIn("POINT DE DÉPART", texte)
        self.assertIn("mots_cles", texte)
        # 1) le modèle cite le bon identifiant
        brief = {"sujet": {"origine_id": dossier["id"], "titre_propose": "autre"}}
        self.assertEqual(gfb.ancrer_sur_le_sujet(brief, "2026-10-03"), dossier["id"])
        self.assertEqual(brief["sujet"]["point_de_depart"]["id"], dossier["id"])
        # 2) il oublie l'identifiant mais traite ce sujet : titre proche -> le code l'ancre
        brief = {"sujet": {"origine_id": None, "titre_propose": dossier["titre"]}}
        self.assertEqual(gfb.ancrer_sur_le_sujet(brief, "2026-10-03"), dossier["id"])
        self.assertEqual(brief["sujet"]["origine_id"], dossier["id"])
        # 3) il a pris un autre sujet (auto-sélection) : rien n'est inscrit
        brief = {"sujet": {"origine_id": None, "titre_propose": "Un tout autre sujet sans rapport avec la file"}}
        self.assertIsNone(gfb.ancrer_sur_le_sujet(brief, "2026-10-03"))
        self.assertNotIn("point_de_depart", brief["sujet"])


class VeilleEnrichitTest(unittest.TestCase):
    def test_enrichissement_apres_ajout_nouveaux_d_abord_puis_retard_borne(self):
        import generate_hot_topics as ht
        import enrich_sujets as en
        d = sj.parse_md(mini_md())
        nouveau = sj.ajouter(d, "culture", "Nouveau sujet à enrichir ?", contexte=CONTEXTE_LONG, rationnel=RATIONNEL_LONG, mots_cles=["a"])
        appeles = []

        def faux(sec, e, model, key, today):
            appeles.append(e["id"])
            return ["mots_cles"], 0.0
        ancien = en.enrichir_un
        en.enrichir_un = faux
        try:
            fait = ht.enrichir_apres_ajout(d, [nouveau["id"]], "clé", "modèle", datetime.date(2026, 10, 2), retard=2)
        finally:
            en.enrichir_un = ancien
        self.assertEqual(appeles[0], nouveau["id"], "le nouveau dossier incomplet passe en premier")
        self.assertEqual(len(appeles), 3, "1 nouveau + 2 de retard au plus")
        self.assertEqual(fait, 3)

    def test_un_dossier_complet_n_est_pas_enrichi_et_un_echec_ne_bloque_pas(self):
        import generate_hot_topics as ht
        import enrich_sujets as en
        d = sj.parse_md(mini_md())
        complet = sj.ajouter(d, "culture", "Nouveau complet ?", contexte=CONTEXTE_LONG, rationnel=RATIONNEL_LONG, mots_cles=["a", "b", "c"])
        appeles = []

        def casse(sec, e, model, key, today):
            appeles.append(e["id"])
            raise RuntimeError("panne réseau")
        ancien = en.enrichir_un
        en.enrichir_un = casse
        try:
            fait = ht.enrichir_apres_ajout(d, [complet["id"]], "clé", "modèle", datetime.date(2026, 10, 2), retard=1)
        finally:
            en.enrichir_un = ancien
        self.assertNotIn(complet["id"], appeles)
        self.assertEqual((len(appeles), fait), (1, 0), "un échec est ignoré, jamais bloquant")
        self.assertEqual(ht.enrichir_apres_ajout(d, [], "k", "m", datetime.date(2026, 10, 2), retard=0), 0)

    def test_insert_entries_renvoie_les_identifiants(self):
        import generate_hot_topics as ht
        d = sj.parse_md(mini_md())
        ids = ht.insert_entries(d, "## Culture — samedi", [({"accroche": "A ?", "contexte": CONTEXTE_LONG, "rationnel": RATIONNEL_LONG}, None)],
                                datetime.date(2026, 10, 2))
        self.assertEqual(len(ids), 1)
        self.assertEqual(par_debut(d, "A ?")["id"], ids[0])
        self.assertEqual(ht.insert_entries(d, "## Culture — samedi", [], datetime.date(2026, 10, 2)), [])


class DashboardAgendaTest(unittest.TestCase):
    """update_audience : les sujets encore « à valider » ne sont pas le « prochain sujet »."""

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "seo"))
        import update_audience as ua
        self.ua = ua

    def test_sujet_a_valider_ecarte_de_l_agenda(self):
        d = sj.parse_md(mini_md())
        sj.ajouter(d, "culture", "Sujet proposé par la veille ?")   # 🔍 à valider, en tête de section
        culture = next(s for s in d["sections"] if s["cle"] == "culture")
        section = self.ua.parse_section(sj.render_md(d), culture["titre"])
        tous = self.ua.unchecked_items(section)
        valides = self.ua.unchecked_items(section, valides_seulement=True)
        self.assertTrue(tous[0].startswith("🔍 Sujet proposé"))
        self.assertTrue(all(not t.startswith("🔍") for t in valides))
        self.assertEqual(len(valides), sum(1 for t in tous if not t.startswith("🔍")))


class GrasMarkdownTest(unittest.TestCase):
    """Le gras Markdown du modèle (« **84 %** ») ne doit jamais apparaître tel quel dans une édition."""

    def setUp(self):
        import generate_daily_edition as gde
        self.gde = gde

    def test_conversion_en_strong(self):
        c = self.gde.convert_markdown_bold
        self.assertEqual(c("Alors que **84 %** des succès"), "Alors que <strong>84 %</strong> des succès")
        self.assertEqual(c("**31,4 %** et **1 million d'euros**"), "<strong>31,4 %</strong> et <strong>1 million d'euros</strong>")
        self.assertEqual(c("texte sans gras"), "texte sans gras")
        self.assertEqual(c("déjà <strong>propre</strong>"), "déjà <strong>propre</strong>")

    def test_etoile_saisie_avant_le_renvoi_au_lexique(self):
        c = self.gde.convert_markdown_bold
        lien = '<a class="lex-ref" href="#lex-soft-power" aria-label="Voir la définition dans le lexique">*</a>'
        self.assertEqual(c("le soft power*" + lien + " numérique"), "le soft power" + lien + " numérique")
        self.assertEqual(c("le **soft power**" + lien), "le <strong>soft power</strong>" + lien)
        self.assertEqual(c("le soft power" + lien), "le soft power" + lien, "le « * » du lien lui-même est conservé")

    def test_paire_mal_formee_ne_laisse_aucune_etoile_double(self):
        c = self.gde.convert_markdown_bold
        for brut in ("**ouvert sans fin", "fermé sans début**", "** vide **", "a ** b", "****"):
            self.assertNotIn("**", c(brut), brut)

    def test_toutes_les_chaines_du_contenu(self):
        contenu = {"dek": ["Un **fait** clé"], "essentiel_box": ["a", "**84 %** b"],
                   "cards": {"stable": {"why": ["**x**"], "indicateurs_touches": [{"field_name": "**k**"}]}},
                   "lexique": [{"terme": "t", "definition": "def **gras**"}], "n": 3}
        self.gde.normalize_content_markdown(contenu)
        texte = json.dumps(contenu, ensure_ascii=False)
        self.assertNotIn("**", texte)
        self.assertIn("<strong>84 %</strong>", texte)
        self.assertEqual(contenu["n"], 3)


class ProblematiqueTest(unittest.TestCase):
    """La rubrique « rationnel » est la problématique : elle commence par « La question », sans qualificatif de remplissage."""

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import enrich_sujets as en
        self.en = en

    def test_a_reformuler(self):
        ancien = {"rationnel": "Ce sujet est brûlant car l'escalade est documentée par les instances internationales."}
        nouveau = {"rationnel": "La question : le monde peut-il se passer du GPS ? L'issue est ouverte : deux forces s'opposent."}
        self.assertTrue(self.en.rationnel_a_reformuler(ancien))
        self.assertFalse(self.en.rationnel_a_reformuler(nouveau))
        self.assertFalse(self.en.rationnel_a_reformuler({"rationnel": None}), "absent : relève de l'enrichissement")

    def test_validation_du_nouveau_texte(self):
        v = self.en.problematique_valide
        bon = "La question : la monnaie peut-elle devenir une arme ? Les forces en présence s'opposent, et l'enjeu est concret."
        self.assertTrue(v(bon))
        self.assertFalse(v("Ce sujet est brûlant. " + bon), "ne commence pas par « La question »")
        self.assertFalse(v(bon + " Un sujet crucial."), "qualificatif interdit")
        self.assertFalse(v("La question : " + "x" * 5 + " **gras**"), "Markdown")
        self.assertFalse(v(""))

    def test_reformuler_un_applique_seulement_un_texte_conforme(self):
        from unittest import mock
        sec = {"cle": "geopolitique", "titre": "Géopolitique"}
        bon = "La question : un État peut-il encore rester souverain sans maîtriser ses données ? Les forces s'opposent, l'enjeu est concret."
        e = sj.sujet_vide(id="x", titre="Titre ?", rationnel="Ce sujet est brûlant car tout bouge vite.")
        with mock.patch.object(self.en, "call_openrouter", return_value=({"rationnel": bon}, {"cost": 0.001})):
            ok, cout = self.en.reformuler_un(sec, e, "m", "k", datetime.date(2026, 10, 2))
        self.assertTrue(ok)
        self.assertEqual((e["rationnel"], e["enrichi_le"], cout), (bon, "2026-10-02", 0.001))
        e2 = sj.sujet_vide(id="y", titre="T ?", rationnel="Ce sujet est brûlant car tout bouge vite.")
        with mock.patch.object(self.en, "call_openrouter", return_value=({"rationnel": "Un sujet crucial."}, {})):
            ok2, _ = self.en.reformuler_un(sec, e2, "m", "k", datetime.date(2026, 10, 2))
        self.assertFalse(ok2)
        self.assertEqual(e2["rationnel"], "Ce sujet est brûlant car tout bouge vite.", "texte non conforme : rien n'est écrasé")

    def test_apercu_ne_modifie_rien(self):
        from unittest import mock
        sec = {"cle": "geopolitique", "titre": "Géopolitique"}
        bon = "La question : un État peut-il encore rester souverain sans maîtriser ses données ? Les forces s'opposent, l'enjeu est concret."
        e = sj.sujet_vide(id="x", titre="Titre ?", rationnel="Ancien texte brûlant.")
        with mock.patch.object(self.en, "call_openrouter", return_value=({"rationnel": bon}, {"cost": 0.0})):
            texte, brut, cout = self.en.proposer_problematique(sec, e, "m", "k")
        self.assertEqual((texte, brut), (bon, bon))
        self.assertEqual(e["rationnel"], "Ancien texte brûlant.", "proposer ne modifie pas le sujet")

    def test_les_prompts_demandent_la_problematique(self):
        sec = {"cle": "geopolitique", "titre": "Géopolitique"}
        e = sj.sujet_vide(id="x", titre="Titre ?", contexte="c" * 300)
        for prompt in (self.en.construire_prompt(sec, e, datetime.date(2026, 10, 2)),
                       self.en.construire_prompt_reformulation(sec, e)):
            self.assertIn("La question :", prompt)
            self.assertIn("brûlant", prompt, "les qualificatifs interdits sont cités dans la consigne")


class ExtractionJsonTest(unittest.TestCase):
    """Réponse du modèle avec du texte avant le JSON (veille du 27 septembre 2026)."""

    def setUp(self):
        import generate_daily_edition as gde  # import tardif : charge bs4, absent des tests purs
        self.strip = gde.strip_markdown_json_fence

    def test_json_nu_inchange(self):
        self.assertEqual(self.strip('{"a": 1}'), '{"a": 1}')

    def test_bloc_cloture(self):
        self.assertEqual(json.loads(self.strip('Voici :\n```json\n{"a": 1}\n```\nFin.')), {"a": 1})

    def test_bloc_sans_barriere_finale(self):
        txt = 'Je vais chercher.\nJ\'ai terminé.\n```json\n{"geo": [{"accroche": "Ormuz ?"}]}'
        self.assertEqual(json.loads(self.strip(txt)), {"geo": [{"accroche": "Ormuz ?"}]})

    def test_prend_le_plus_grand_objet(self):
        txt = 'Note {"a": 1} puis le résultat : {"geo": [1, 2, 3], "sport": []}'
        self.assertEqual(json.loads(self.strip(txt)), {"geo": [1, 2, 3], "sport": []})

    def test_sans_json_rend_le_texte(self):
        self.assertEqual(self.strip("rien d'exploitable"), "rien d'exploitable")


if __name__ == "__main__":
    unittest.main()
