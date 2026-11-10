import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tendances_google as tg  # noqa: E402

FLUX = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:ht="https://trends.google.com/trending/rss" version="2.0">
  <channel>
    <title>Daily Search Trends</title>
    <item>
      <title>terres rares</title>
      <ht:approx_traffic>200+</ht:approx_traffic>
      <description/>
    </item>
    <item>
      <title>   </title>
      <ht:approx_traffic>50+</ht:approx_traffic>
    </item>
    <item>
      <title>budget 2027</title>
      <ht:approx_traffic>500+</ht:approx_traffic>
    </item>
    <item>
      <title>Kaliningrad</title>
    </item>
  </channel>
</rss>
"""


class ParserFluxTest(unittest.TestCase):
    def test_lit_titre_et_trafic(self):
        out = tg.parser_flux(FLUX)
        self.assertEqual(out[0], {"titre": "terres rares", "trafic": "200+"})
        self.assertEqual(out[1], {"titre": "budget 2027", "trafic": "500+"})

    def test_ignore_titre_vide_et_garde_trafic_absent(self):
        out = tg.parser_flux(FLUX)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[2], {"titre": "Kaliningrad", "trafic": ""})

    def test_limite_de_dix(self):
        items = "".join(f"<item><title>mot {i}</title></item>" for i in range(25))
        xml = f'<rss xmlns:ht="https://trends.google.com/trending/rss"><channel>{items}</channel></rss>'
        self.assertEqual(len(tg.parser_flux(xml)), tg.MAX_TENDANCES)


class LireTendancesTest(unittest.TestCase):
    def test_panne_renvoie_liste_vide(self):
        # port fermé : connexion refusée tout de suite, sans attendre
        self.assertEqual(tg.lire_tendances(url="http://127.0.0.1:9/", timeout=2), [])


class BlocPromptTest(unittest.TestCase):
    def test_vide_sans_tendances(self):
        self.assertEqual(tg.bloc_prompt([]), "")

    def test_contient_recherches_et_garde_fou(self):
        bloc = tg.bloc_prompt([{"titre": "terres rares", "trafic": "200+"}])
        self.assertIn("- terres rares (200+ recherches)", bloc)
        self.assertIn("barre d'importance", bloc)
        self.assertIn("Ne retiens jamais un sujet seulement parce qu'il est recherché", bloc)


class BuildPromptTest(unittest.TestCase):
    def _prompt(self, tendances):
        import generate_hot_topics as ht
        return ht.build_prompt({}, [], [], [], date(2026, 11, 10), tendances)

    def test_sans_tendances_prompt_inchange(self):
        self.assertNotIn("Recherches actuellement en hausse", self._prompt(None))
        self.assertNotIn("Recherches actuellement en hausse", self._prompt([]))

    def test_avec_tendances_le_bloc_est_ajoute(self):
        p = self._prompt([{"titre": "terres rares", "trafic": "200+"}])
        self.assertIn("Recherches actuellement en hausse sur Google en France", p)
        self.assertIn("- terres rares (200+ recherches)", p)
        # le bloc vient avant la date du jour, comme les autres consignes
        self.assertLess(p.index("terres rares (200+"), p.index("Date d'aujourd'hui"))


if __name__ == "__main__":
    unittest.main()
