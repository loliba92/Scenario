"""Tests de revue_de_presse.py. Sans réseau : l'appel au modèle et le test HTTP des liens sont simulés.
    python3 -m unittest scripts/edition/test_revue_de_presse.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import revue_de_presse as rp  # noqa: E402

BRIEF = {"sujet": {"titre_propose": "Art : de l'œuvre à l'expérience"}}


def art(n, **kw):
    a = {"title": f"Titre {n}", "source": "franceinfo", "url": f"https://exemple.fr/a{n}", "lang": "fr",
         "domain": "international", "summary": f"Résumé factuel {n}.", "read_minutes": 2}
    a.update(kw)
    return a


def faux_appel(articles, cited=None):
    def appel(prompt, model, api_key, **kw):
        appel.prompt, appel.kw = prompt, kw
        return {"revue_de_presse": articles}, {"cited_urls": cited, "cost": 0.001}
    return appel


def ok(url):  # tous les liens répondent 200
    return 200


class RevueDePresseTest(unittest.TestCase):
    def test_trois_articles_valides(self):
        appel = faux_appel([art(1), art(2), art(3)])
        res = rp.rechercher(BRIEF, "2026-10-11", "cle", appel=appel, verifier=ok)
        self.assertEqual([a["url"] for a in res], ["https://exemple.fr/a1", "https://exemple.fr/a2", "https://exemple.fr/a3"])
        self.assertIsNone(res[0]["image"])   # l'image est lue ensuite (press_images)
        self.assertIn("2026-10-11", appel.prompt)
        self.assertIn("Art : de l'œuvre", appel.prompt)   # sujet du jour à éviter
        self.assertEqual(appel.kw["tools"][0]["type"], "openrouter:web_search")

    def test_lien_absent_des_pages_consultees_est_ecarte(self):
        appel = faux_appel([art(1), art(2), art(3)], cited=["https://exemple.fr/a1", "https://exemple.fr/a2"])
        res = rp.rechercher(BRIEF, "2026-10-11", "cle", appel=appel, verifier=ok)
        self.assertEqual([a["url"] for a in res], ["https://exemple.fr/a1", "https://exemple.fr/a2"])

    def test_lien_mort_est_ecarte(self):
        res = rp.rechercher(BRIEF, "2026-10-11", "cle", appel=faux_appel([art(1), art(2), art(3)]),
                            verifier=lambda u: 404 if u.endswith("a3") else 200)
        self.assertEqual(len(res), 2)

    def test_domaine_inconnu_et_champs_manquants_ecartes(self):
        res = rp.nettoyer([art(1, domain="sport"), art(2, summary=""), art(3, url="pas-une-url"), art(4)], None, ok)
        self.assertEqual([a["url"] for a in res], ["https://exemple.fr/a4"])

    def test_moins_de_deux_articles_valables_donne_une_revue_vide(self):
        res = rp.rechercher(BRIEF, "2026-10-11", "cle", appel=faux_appel([art(1)]), verifier=ok)
        self.assertEqual(res, [])

    def test_jamais_bloquant(self):
        def panne(*a, **k):
            raise RuntimeError("OpenRouter indisponible")
        self.assertEqual(rp.rechercher(BRIEF, "2026-10-11", "cle", appel=panne), [])

    def test_doublons_et_plafond(self):
        res = rp.nettoyer([art(1), art(1)] + [art(i) for i in range(2, 9)], None, ok)
        self.assertEqual(len(res), rp.MAX_ARTICLES)
        self.assertEqual(len({a["url"] for a in res}), len(res))


if __name__ == "__main__":
    unittest.main()
