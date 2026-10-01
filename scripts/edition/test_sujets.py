"""Tests de la file de sujets structurée (scripts/edition/sujets.py).

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


def mini_md():
    return """# Sujets prioritaires — Test

Texte d'en-tête.

---

## 🔥 Priorité absolue (n'importe quel jour, avant tout le reste)
<!-- intro urgente -->
- [x] Sujet urgent déjà publié ? [géopolitique]
  <!-- Ajouté le 6 septembre 2026, contexte -->

## Culture — samedi
<!-- Lot ajouté le 3 septembre 2026 : idées -->
- [ ] La Chine peut-elle créer la prochaine pop culture mondiale ? Cinéma, jeux, musique, plateformes. [culture & géopolitique]
  <!-- Note sur\n  deux lignes -->
- [ ] 🔍 Proposition automatique non validée [culture]
  <!-- Ajouté automatiquement le 2026-09-18 (veille) — à valider. -->
- [ ] Sujet sans tag ni note

## Économie & finance mondiale — jeudi
- [ ] Bitcoin : le bitcoin devient-il un actif institutionnel ? [économie & finance]
- [ ] Bitcoin : le bitcoin devient-il un actif institutionnel ? [économie & finance]
"""


class ConversionTest(unittest.TestCase):
    def test_lecture_et_champs(self):
        d = sj.parse_md(mini_md())
        self.assertEqual([s["cle"] for s in d["sections"]], ["priorite_absolue", "culture", "economie"])
        self.assertEqual(d["sections"][1]["jour"], "samedi")
        pop = next(e for _, e in sj.sujets(d) if e["texte"].startswith("La Chine"))
        self.assertEqual(pop["tag"], "culture & géopolitique")
        self.assertEqual(pop["statut"], "a_traiter")
        self.assertEqual(pop["validation"], "valide")
        self.assertIn("deux lignes", pop["note"])
        prop = next(e for _, e in sj.sujets(d) if e["texte"].startswith("Proposition"))
        self.assertEqual(prop["validation"], "a_valider")
        self.assertEqual(prop["ajoute_le"], "2026-09-18")
        urgent = next(e for _, e in sj.sujets(d) if e["texte"].startswith("Sujet urgent"))
        self.assertEqual((urgent["statut"], urgent["ajoute_le"]), ("publie", "2026-09-06"))
        self.assertEqual(sum(1 for sec in d["sections"] for e in sec["entrees"] if e["type"] == "commentaire"), 2)
        self.assertEqual(len({e["id"] for _, e in sj.sujets(d)}), 6, "les doublons de texte reçoivent des ids distincts")

    def test_aller_retour_stable(self):
        d = sj.parse_md(mini_md())
        md = sj.render_md(d)
        d2 = sj.parse_md(md, d)
        self.assertEqual(sj.render_md(d2), md)
        self.assertEqual(json.dumps(d, sort_keys=True), json.dumps(d2, sort_keys=True))

    def test_texte_inattendu_refuse(self):
        with self.assertRaises(sj.SujetsError):
            sj.parse_md("# T\n\n## Culture — samedi\nune ligne libre perdue\n")

    def test_fichier_reel_aucune_perte(self):
        """Le vrai fichier : mêmes lignes de sujets (section, case, texte complet) après
        un aller-retour, et tous les commentaires d'origine présents."""
        md = (ROOT / "sujets-prioritaires.md").read_text(encoding="utf-8")
        d = sj.parse_md(md)
        md2 = sj.render_md(d)

        def lignes(t):
            out, sec = [], None
            for l in t.split("\n"):
                if l.startswith("## "):
                    sec = l
                m = re.match(r"^- \[([ xX])\] (.*)$", l)
                if m:
                    out.append((sec, m.group(1).lower(), m.group(2).rstrip()))
            return out

        self.assertEqual(lignes(md), lignes(md2))

        def mots(t):
            texte = " ".join(re.findall(r"<!--(.*?)-->", t, re.S))
            return re.findall(r"\w+", texte.lower())

        manquants = set(mots(md)) - set(mots(md2))
        self.assertFalse(manquants, f"mots de commentaires perdus : {sorted(manquants)[:10]}")


class CocherTest(unittest.TestCase):
    def setUp(self):
        self.d = sj.parse_md(mini_md())

    def etat(self, debut):
        return [e["statut"] for _, e in sj.sujets(self.d) if e["texte"].startswith(debut)]

    def test_par_identifiant(self):
        pop = next(e for _, e in sj.sujets(self.d) if e["texte"].startswith("La Chine"))
        ids = sj.check_off(self.d, {"date": "2026-09-26", "sujet": {"origine_id": pop["id"]}})
        self.assertEqual(ids, [pop["id"]])
        self.assertEqual((pop["statut"], pop["publie_le"], pop["edition"]), ("publie", "2026-09-26", "2026-09-26"))

    def test_identifiant_recopie_avec_prefixe_ou_balises(self):
        for brut in ("id: {i}", "<!-- id: {i} -->", "  {i}  "):
            d = sj.parse_md(mini_md())
            pop = next(e for _, e in sj.sujets(d) if e["texte"].startswith("La Chine"))
            ids = sj.check_off(d, {"date": "2026-09-26", "sujet": {"origine_id": brut.format(i=pop["id"])}})
            self.assertEqual(ids, [pop["id"]], brut)

    def test_origine_recopiee_avec_puce_et_tag(self):
        """Cas réel du 26/09 : origine_prioritaire = ligne complète avec « - [ ] » et tag."""
        brief = {"date": "2026-09-26", "sujet": {"origine_prioritaire":
                 "- [ ] La Chine peut-elle créer la prochaine pop culture mondiale ? Cinéma, jeux, musique, plateformes. [culture & géopolitique]"}}
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
        brief = {"date": "2026-10-01", "sujet": {"titre_propose": "Sujet sans"}}
        self.assertEqual(sj.check_off(self.d, brief), [])

    def test_deja_publie_non_recoche(self):
        brief = {"date": "2026-09-26", "sujet": {"origine_prioritaire": "Sujet urgent déjà publié ?"}}
        self.assertEqual(sj.check_off(self.d, brief), [])
        self.assertEqual(next(e for _, e in sj.sujets(self.d) if e["texte"].startswith("Sujet urgent"))["publie_le"], None)

    def test_aucune_correspondance(self):
        self.assertEqual(sj.check_off(self.d, {"date": "2026-10-02", "sujet": {"titre_propose": "Un titre totalement différent de la file"}}), [])


class AjoutTest(unittest.TestCase):
    def test_ajout_en_tete_a_valider(self):
        d = sj.parse_md(mini_md())
        sj.ajouter(d, "culture", "Nouveau sujet de veille ?", tag="culture", note="Ajouté automatiquement.", ajoute_le="2026-10-02")
        sec = next(s for s in d["sections"] if s["cle"] == "culture")
        premiers = [e for e in sec["entrees"] if e["type"] == "sujet"]
        self.assertEqual(premiers[0]["texte"], "Nouveau sujet de veille ?")
        self.assertEqual(sec["entrees"][0]["type"], "commentaire", "le commentaire d'intro reste en tête")
        md = sj.render_md(d)
        self.assertIn("- [ ] 🔍 Nouveau sujet de veille ? [culture]", md)
        self.assertEqual(sj.verifier(d), [])

    def test_ids_uniques_sur_texte_identique(self):
        d = sj.parse_md(mini_md())
        a = sj.ajouter(d, "culture", "Même texte ?")
        b = sj.ajouter(d, "culture", "Même texte ?")
        self.assertNotEqual(a["id"], b["id"])

    def test_section_inconnue(self):
        with self.assertRaises(sj.SujetsError):
            sj.ajouter(sj.parse_md(mini_md()), "inconnue", "x")

    def test_veille_insert_entries_et_titres(self):
        import generate_hot_topics as ht
        d = sj.parse_md(mini_md())
        # sections de la veille : on s'appuie sur les titres réels du fichier de test
        ht_heading = "## Culture — samedi"
        before = ht.titles_in_section(d, ht_heading)
        self.assertTrue(before[1].startswith(sj.MARQUE_A_VALIDER), "les titres gardent la marque 🔍")
        entries = [({"accroche": "Premier ajout ?", "tag": "culture", "contexte": "Contexte A."}, None),
                   ({"accroche": "Second ajout ?", "tag": "", "contexte": "Contexte B.",
                     "scenarios": {"favorable": "a", "stable": "b", "degrade": "c"}}, "Sport")]
        ht.insert_entries(d, ht_heading, entries, datetime.date(2026, 10, 2))
        titres = [e["texte"] for e in next(s for s in d["sections"] if s["cle"] == "culture")["entrees"] if e["type"] == "sujet"]
        self.assertEqual(titres[:2], ["Premier ajout ?", "Second ajout ?"], "l'ordre reçu est conservé")
        note = next(e for _, e in sj.sujets(d) if e["texte"] == "Second ajout ?")["note"]
        self.assertIn("Repéré en veille sur le registre Sport", note)
        self.assertIn("→ 3 scénarios (brouillon)", note)


class SynchroTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.dp, self.mp = self.tmp / "data" / "sujets.json", self.tmp / "sujets.md"
        sj.save_both(sj.parse_md(mini_md()), self.dp, self.mp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_a_jour(self):
        self.assertEqual(sj.load_synced(self.dp, self.mp)[1], "ok")

    def test_modification_du_markdown_reprise(self):
        md = self.mp.read_text(encoding="utf-8").replace("- [ ] Sujet sans tag ni note", "- [x] Sujet sans tag ni note")
        md += ""
        self.mp.write_text(md, encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "md_repris")
        e = next(e for _, e in sj.sujets(data) if e["texte"] == "Sujet sans tag ni note")
        self.assertEqual(e["statut"], "publie")
        ids_avant = {e["id"] for _, e in sj.sujets(json.loads(self.dp.read_text(encoding="utf-8")))}
        self.assertEqual({e["id"] for _, e in sj.sujets(data)}, ids_avant, "les identifiants sont conservés")

    def test_nouveau_sujet_ajoute_a_la_main_dans_le_markdown(self):
        md = self.mp.read_text(encoding="utf-8").replace(
            "- [ ] Sujet sans tag ni note", "- [ ] Sujet sans tag ni note\n- [ ] Ajout manuel dans le markdown [culture]")
        self.mp.write_text(md, encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "md_repris")
        e = next(e for _, e in sj.sujets(data) if e["texte"].startswith("Ajout manuel"))
        self.assertTrue(e["id"].startswith("culture-ajout-manuel"))

    def test_correction_du_texte_garde_l_identifiant_et_les_metadonnees(self):
        d0 = json.loads(self.dp.read_text(encoding="utf-8"))
        cible = next(e for _, e in sj.sujets(d0) if e["texte"] == "Sujet sans tag ni note")
        cible["publie_le"] = cible["edition"] = "2026-09-01"
        cible["statut"] = "publie"
        sj.save_both(d0, self.dp, self.mp)
        md = self.mp.read_text(encoding="utf-8").replace("Sujet sans tag ni note", "Sujet sans tag ni note (corrigé)")
        self.mp.write_text(md, encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "md_repris")
        e = next(e for _, e in sj.sujets(data) if e["texte"].endswith("(corrigé)"))
        self.assertEqual((e["id"], e["edition"]), (cible["id"], "2026-09-01"))

    def test_modification_du_json_reprise(self):
        d = json.loads(self.dp.read_text(encoding="utf-8"))
        next(e for _, e in sj.sujets(d) if e["texte"] == "Sujet sans tag ni note")["statut"] = "publie"
        self.dp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        data, action = sj.load_synced(self.dp, self.mp)
        self.assertEqual(action, "json_repris")
        sj.save_both(data, self.dp, self.mp)
        self.assertIn("- [x] Sujet sans tag ni note", self.mp.read_text(encoding="utf-8"))
        self.assertEqual(sj.load_synced(self.dp, self.mp)[1], "ok")

    def test_conflit_refuse(self):
        d = json.loads(self.dp.read_text(encoding="utf-8"))
        next(e for _, e in sj.sujets(d) if e["texte"] == "Sujet sans tag ni note")["statut"] = "publie"
        self.dp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        self.mp.write_text(self.mp.read_text(encoding="utf-8").replace("Bitcoin :", "Bitcoin ;"), encoding="utf-8")
        with self.assertRaises(sj.SujetsConflict):
            sj.load_synced(self.dp, self.mp)

    def test_cochage_apres_publication_de_bout_en_bout(self):
        """check_off_priority_topic() réel, sur une copie : le JSON ET la vue sont mis à jour."""
        import generate_post_edition as gpe
        ancien = gpe.REPO_ROOT
        gpe.REPO_ROOT = self.tmp
        (self.tmp / "data").mkdir(exist_ok=True)
        (self.tmp / "sujets-prioritaires.md").write_text(self.mp.read_text(encoding="utf-8"), encoding="utf-8")
        try:
            gpe.check_off_priority_topic({"date": "2026-09-26", "sujet": {
                "origine_prioritaire": "- [ ] La Chine peut-elle créer la prochaine pop culture mondiale ? Cinéma, jeux, musique, plateformes. [culture & géopolitique]"}})
        finally:
            gpe.REPO_ROOT = ancien
        d = json.loads((self.tmp / "data" / "sujets.json").read_text(encoding="utf-8"))
        pop = next(e for _, e in sj.sujets(d) if e["texte"].startswith("La Chine"))
        self.assertEqual((pop["statut"], pop["edition"]), ("publie", "2026-09-26"))
        self.assertIn("- [x] La Chine", (self.tmp / "sujets-prioritaires.md").read_text(encoding="utf-8"))
        self.assertEqual(sj.load_synced(self.tmp / "data" / "sujets.json", self.tmp / "sujets-prioritaires.md")[1], "ok")


class VerificationTest(unittest.TestCase):
    def test_donnees_valides(self):
        d = sj.parse_md(mini_md())
        sj.save_both(d, Path(tempfile.mkdtemp()) / "s.json", Path(tempfile.mkdtemp()) / "s.md")
        self.assertEqual(sj.verifier(d, sj.render_md(d)), [])

    def test_detecte_id_en_double_statut_et_validation(self):
        d = sj.parse_md(mini_md())
        subs = [e for _, e in sj.sujets(d)]
        subs[1]["id"] = subs[0]["id"]
        subs[2]["statut"] = "inconnu"
        subs[3]["validation"] = "peut-etre"
        pb = " | ".join(sj.verifier(d))
        self.assertIn("en double", pb)
        self.assertIn("statut invalide", pb)
        self.assertIn("validation invalide", pb)

    def test_desynchronisation_simple_n_est_pas_une_erreur_mais_le_conflit_si(self):
        d = sj.parse_md(mini_md())
        md = sj.render_md(d)
        d["meta"]["md_sha256"] = sj.sha(md)
        self.assertIsNone(sj.desynchronisation(d, md))
        self.assertEqual(sj.desynchronisation(d, md + "\n"), "md")
        self.assertEqual(sj.verifier(d, md + "\n"), [], "modification du Markdown seul : se répare par sync")
        d2 = copy.deepcopy(d)
        next(e for _, e in sj.sujets(d2))["statut"] = "a_traiter"
        self.assertEqual(sj.desynchronisation(d2, md), "json")
        self.assertEqual(sj.desynchronisation(d2, md + "\n"), "conflit")
        self.assertTrue(any("conflit" in p for p in sj.verifier(d2, md + "\n")))

    def test_sujet_deja_publie_encore_a_traiter(self):
        d = sj.parse_md(mini_md())
        editions = {"2026-09-26": {sj.norm("La Chine peut-elle créer la prochaine pop culture mondiale ?")}}
        pb = sj.verifier(d, editions=editions)
        self.assertTrue(any("2026-09-26" in p and "culture" in p for p in pb), pb)

    def test_origine_id_inconnu_dans_un_brief(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "2026-10-02.json").write_text(json.dumps({"sujet": {"origine_id": "n-existe-pas"}}), encoding="utf-8")
        pb = sj.verifier(sj.parse_md(mini_md()), briefs_dir=tmp)
        self.assertTrue(any("n-existe-pas" in p for p in pb), pb)

    def test_fichiers_du_depot_coherents(self):
        """Garde-fou : le JSON et la vue du dépôt sont cohérents, ids uniques, briefs valides."""
        data = json.loads((ROOT / "data" / "sujets.json").read_text(encoding="utf-8"))
        md = (ROOT / "sujets-prioritaires.md").read_text(encoding="utf-8")
        graves = [p for p in sj.verifier(data, md, sj.editions_publiees())]
        self.assertEqual(graves, [])


class LecteursExistantsTest(unittest.TestCase):
    """La vue Markdown reste lisible par les scripts qui ne passent pas par sujets.py."""

    def test_tableau_de_bord_et_brief_de_secours(self):
        import update_audience as ua
        import generate_fallback_brief as gfb
        md = (ROOT / "sujets-prioritaires.md").read_text(encoding="utf-8")
        cards, later, prio = ua.build_agenda(md)
        self.assertEqual(len(cards), 7)
        self.assertTrue(all(c["topic"] for c in cards))
        q = gfb.extract_priority_queue(ROOT / "sujets-prioritaires.md")
        self.assertGreaterEqual(len(re.findall(r"^- \[ \] ", q, re.M)), 6)
        self.assertIn("<!-- id:", q, "le brief de secours voit l'identifiant du sujet à citer")


if __name__ == "__main__":
    unittest.main()
