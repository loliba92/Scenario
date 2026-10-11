"""Tests de gsc_report.py — données fictives, sans réseau."""
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsc_report as r  # noqa: E402

AUJOURDHUI = date(2026, 10, 11)


def _donnees(dossier, *, inconnues_anciennes=True, clics=4, erreurs_plan="0"):
    d = Path(dossier)
    d.mkdir(parents=True, exist_ok=True)
    (d / "summary.json").write_text(json.dumps({
        "site": "sc-domain:lesscenarios.fr", "periode": {"debut": "2026-09-11", "fin": "2026-10-08"}, "mis_a_jour": "2026-10-11",
        "totaux": {"clicks": clics, "impressions": 286, "ctr": round(clics / 286, 4), "position": 9.1},
        "requetes": [{"requete": "les scénarios", "clicks": 0, "impressions": 3, "ctr": 0, "position": 47}],
        "pages": [{"page": "https://lesscenarios.fr/", "clicks": 0, "impressions": 12, "ctr": 0, "position": 6.3},
                  {"page": "https://lesscenarios.fr/index.html", "clicks": 1, "impressions": 5, "ctr": 0.2, "position": 10}]}))
    (d / "history.json").write_text(json.dumps({f"2026-09-{n:02d}": {"clicks": 0, "impressions": 5 if n < 20 else 10} for n in range(11, 29)}))
    rows = [{"url": "https://lesscenarios.fr/", "verdict": "PASS", "etat": "Envoyée et indexée", "derniere_exploration": "2026-10-07T00:00:00Z"},
            {"url": "https://lesscenarios.fr/guide-pedagogique.html", "verdict": "NEUTRAL", "etat": "Détectée, actuellement non indexée"},
            {"url": "https://lesscenarios.fr/archives/2026-10-11.html", "verdict": "NEUTRAL", "etat": "Google ne reconnaît pas cette URL"}]
    if inconnues_anciennes:
        rows.append({"url": "https://lesscenarios.fr/archives/2026-09-24.html", "verdict": "NEUTRAL", "etat": "Google ne reconnaît pas cette URL"})
    (d / "indexation.json").write_text(json.dumps({"mis_a_jour": "2026-10-11", "pages": rows}))
    (d / "sitemaps.json").write_text(json.dumps({"plans": [
        {"plan": "https://lesscenarios.fr/sitemap.xml", "derniere_lecture": "2026-10-09T10:00:00Z", "erreurs": erreurs_plan,
         "avertissements": "0", "contenus": [{"type": "web", "submitted": "162", "indexed": "0"}]}]}))


class TestClassification(unittest.TestCase):
    def test_etats_francais_et_anglais(self):
        self.assertEqual(r.classify("Envoyée et indexée")[0], "ok")
        self.assertEqual(r.classify("Submitted and indexed")[0], "ok")
        self.assertEqual(r.classify("Google ne reconnaît pas cette URL")[0], "inconnue")
        self.assertEqual(r.classify("URL is unknown to Google")[0], "inconnue")
        self.assertEqual(r.classify("Détectée, actuellement non indexée")[0], "decouverte")
        self.assertEqual(r.classify("Explorée, actuellement non indexée")[0], "exploree")
        self.assertEqual(r.classify("Exclue par la balise « noindex »")[0], "bloquee")
        self.assertEqual(r.classify("Introuvable (404)")[0], "introuvable")
        self.assertEqual(r.classify("quelque chose d'inédit")[0], "autre")
        self.assertEqual(r.classify(None, "PASS")[0], "ok")

    def test_age_page(self):
        self.assertEqual(r.page_age("https://lesscenarios.fr/archives/2026-10-01.html", AUJOURDHUI), 10)
        self.assertIsNone(r.page_age("https://lesscenarios.fr/archives.html", AUJOURDHUI))

    def test_date_en_francais(self):
        self.assertEqual(r.date_fr("2026-10-11"), "11 octobre 2026")
        self.assertEqual(r.date_fr("2026-11-01"), "1er novembre 2026")
        self.assertEqual(r.date_fr("pas une date"), "pas une date")

    def test_formats(self):
        self.assertEqual(r.fr(9.1), "9,1")
        self.assertEqual(r.pct(0.014), "1,4")
        self.assertEqual(r.n_(1, "page", "pages"), "1 page")
        self.assertEqual(r.n_(3, "page", "pages"), "3 pages")


class TestAnalyse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "archives").mkdir()
        (self.root / "sitemap.xml").write_text("")

    def tearDown(self):
        self.tmp.cleanup()

    def test_sans_donnees(self):
        A = r.analyser(self.root / "vide", AUJOURDHUI, self.root)
        self.assertFalse(A["donnees"])
        self.assertEqual(A["verdict"][0], "critique")
        self.assertIn("Aucune donnée", r.rendre_md(A))

    def test_probleme_de_decouverte_designe_les_agents(self):
        _donnees(self.root / "d")
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        self.assertEqual(A["verdict"][0], "critique")
        crit = A["critiques"][0]
        self.assertIn("inconnue", crit[0])
        self.assertEqual(crit[2], "seo-technical + seo-sitemap")
        self.assertTrue(crit[3])
        self.assertEqual(A["kpi"]["inconnues"], 2)           # l'édition du jour (0 j) compte, mais ne déclenche rien seule
        self.assertEqual(A["kpi"]["inconnues_anciennes"], 1)
        self.assertTrue(A["a_faire_par_vous"])

    def test_edition_recente_seule_nest_pas_critique(self):
        _donnees(self.root / "d", inconnues_anciennes=False)
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        self.assertFalse(A["critiques"])
        self.assertNotEqual(A["verdict"][0], "critique")

    def test_erreur_de_plan_du_site_est_critique(self):
        _donnees(self.root / "d", inconnues_anciennes=False, erreurs_plan="3")
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        self.assertTrue(any("erreur" in c[0] and c[2] == "seo-sitemap" for c in A["critiques"]))

    def test_donnees_perimees(self):
        _donnees(self.root / "d", inconnues_anciennes=False)
        A = r.analyser(self.root / "d", date(2026, 10, 20), self.root)
        self.assertTrue(any("jours" in c[0] for c in A["critiques"]))

    def test_controles_depot(self):
        bon = ('<html><head><title>Un titre propre — Scénario</title><link rel="canonical" href="x">'
               '<meta name="description" content="%s"></head><body><h1>Un titre</h1></body></html>' % ("a" * 120))
        mauvais = '<html><head><title>Titre coupé… — Scénario</title></head><body><h1>A</h1><h1>B</h1></body></html>'
        (self.root / "archives" / "2026-10-01.html").write_text(bon)
        (self.root / "archives" / "2026-10-02.html").write_text(mauvais)
        (self.root / "sitemap.xml").write_text("https://lesscenarios.fr/archives/2026-10-01.html")
        c = r.controles_depot(self.root)["fr"]
        self.assertEqual(c["pages"], 2)
        self.assertEqual((c["titre_coupe"], c["sans_h1"], c["sans_canonique"], c["hors_plan"]), (1, 1, 1, 1))
        self.assertEqual(c["desc_hors_norme"], 1)

    def test_rendus(self):
        _donnees(self.root / "d")
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        md = r.rendre_md(A)
        for titre in ("## À résoudre — critique", "## Ce qui fonctionne", "## Ce qui ne fonctionne pas", "**Agent à envoyer**"):
            self.assertIn(titre, md)
        page = r.rendre_html(A, "<main>{{CONTENT}}</main>")
        for morceau in ("À résoudre, avec les recommandations", "Agent à envoyer", "Ce qui fonctionne", "Ce qui ne fonctionne pas", "Page par page"):
            self.assertIn(morceau, page)
        self.assertNotIn("{{CONTENT}}", page)

    def test_html_echappe_les_donnees(self):
        _donnees(self.root / "d")
        s = json.loads((self.root / "d" / "summary.json").read_text())
        s["requetes"][0]["requete"] = "<script>alert(1)</script>"
        (self.root / "d" / "summary.json").write_text(json.dumps(s))
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        self.assertNotIn("<script>alert(1)</script>", r.rendre_html(A, "{{CONTENT}}"))


class TestConclusions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "archives").mkdir()
        (self.root / "sitemap.xml").write_text("")
        _donnees(self.root / "d")
        (self.root / "d" / "conclusions.json").write_text(json.dumps({"audits": [
            {"date": "2026-10-04", "titre": "ancien", "verdict": "v0", "agents": ["a"], "constats": []},
            {"date": "2026-10-11", "titre": "éditions inconnues", "verdict": "Pas de blocage technique.", "agents": ["seo-technical", "gsc-expert"],
             "constats": [{"titre": "Maillage", "certitude": "certain", "statut": "corrige", "cause": "L'accueil ne liait que 10 éditions.", "action": "Bloc ajouté."},
                          {"titre": "Indexation manuelle", "certitude": "probable", "statut": "proprietaire", "cause": "c", "action": "Demander l'indexation."}],
             "proprietaire": ["Demander l'indexation de /archives.html."], "inconnu": ["Erreur serveur ?"], "prochain_controle": "25 octobre 2026"}]}))

    def tearDown(self):
        self.tmp.cleanup()

    def test_rendu_page_et_texte(self):
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        page = r.rendre_html(A, "{{CONTENT}}")
        for morceau in ("Conclusions des agents", "Audit du 11 octobre 2026", "Pas de blocage technique.", "Corrigé", "Vous", "Maillage",
                        "25 octobre 2026", "Erreur serveur ?", "À faire par vous"):
            self.assertIn(morceau, page)
        md = r.rendre_md(A)
        self.assertIn("## Conclusions des agents — 11 octobre 2026", md)
        self.assertIn("[Corrigé] **Maillage**", md)
        self.assertLess(page.index("Audit du 11 octobre 2026"), page.index("Audit du 4 octobre 2026"))   # le plus récent d'abord

    def test_sans_fichier_pas_de_section(self):
        (self.root / "d" / "conclusions.json").unlink()
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        self.assertNotIn("Conclusions des agents", r.rendre_html(A, "{{CONTENT}}"))
        self.assertNotIn("## Conclusions des agents", r.rendre_md(A))

    def test_compteur_adresses_plan_actualites_non_double(self):
        (self.root / "d" / "sitemaps.json").write_text(json.dumps({"plans": [
            {"plan": "https://lesscenarios.fr/sitemap-news.xml", "derniere_lecture": "2026-10-10T00:00:00Z", "erreurs": "0", "avertissements": "0",
             "contenus": [{"type": "web", "submitted": "5"}, {"type": "news", "submitted": "5"}]}]}))
        A = r.analyser(self.root / "d", AUJOURDHUI, self.root)
        self.assertEqual(A["plans"][0]["envoyees"], 5)


class TestTableauDeBord(unittest.TestCase):
    def test_remplace_seulement_la_zone_reperee_et_reste_stable(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            _donnees(t / "d")
            A = r.analyser(t / "d", AUJOURDHUI, t)
            dash = t / "dashboard.html"
            dash.write_text("<p>avant</p><!-- SEO-CARD:START -->ancien<!-- SEO-CARD:END --><p>après</p>")
            self.assertTrue(r.maj_dashboard(A, dash))
            une_fois = dash.read_text()
            self.assertTrue(une_fois.startswith("<p>avant</p>") and une_fois.endswith("<p>après</p>"))
            self.assertIn('href="seo.html"', une_fois)
            self.assertNotIn("ancien", une_fois)
            self.assertTrue(r.maj_dashboard(A, dash))
            self.assertEqual(dash.read_text(), une_fois)       # idempotent

    def test_sans_reperes_ou_sans_donnees_ne_touche_rien(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            _donnees(t / "d")
            A = r.analyser(t / "d", AUJOURDHUI, t)
            dash = t / "dashboard.html"
            dash.write_text("<p>pas de repère</p>")
            self.assertFalse(r.maj_dashboard(A, dash))
            self.assertEqual(dash.read_text(), "<p>pas de repère</p>")
            dash.write_text("<!-- SEO-CARD:START -->x<!-- SEO-CARD:END -->")
            self.assertFalse(r.maj_dashboard(r.analyser(t / "vide", AUJOURDHUI, t), dash))


if __name__ == "__main__":
    unittest.main()
