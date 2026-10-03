"""Tests du podcast (sans réseau)."""
import io
import sys
import unittest
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_podcast as gp  # noqa: E402
import musique as mu  # noqa: E402
from array import array  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


class PodcastTest(unittest.TestCase):
    def test_lecture_edition(self):
        pages = sorted(p for p in (ROOT / "archives").glob("2026-10-0*.html"))
        ed = gp.lire_edition(pages[-1])
        self.assertTrue(ed["titre"] and ed["faits"])
        self.assertEqual(len(ed["scenarios"]), 3)
        self.assertTrue(all(s["probabilite"] for s in ed["scenarios"]))
        self.assertIn("SCÉNARIO FAVORABLE", gp.texte_source(ed).upper())

    def test_nombres(self):
        self.assertEqual(gp.nombres("84 % et 31,4 % ; 120 tonnes ; 100 000 euros ; 30 50 20"),
                         {"84", "31.4", "120", "100000", "30", "50", "20"})

    def test_garde_fou(self):
        source = "Le taux passe de 84 % à 75 %. 3 millions d'euros."
        ok = [{"orateur": o, "texte": "Le taux passe de 84 pour cent à 75 pour cent, soit 3 millions. " + "mot " * 25}
              for o in gp.ANIMATEURS * 10]
        self.assertEqual(gp.verifier_dialogue(ok, source), [])
        faux = [dict(l) for l in ok]
        faux[3]["texte"] += " Il y a 99 pour cent de chances."
        self.assertTrue(any("99" in p for p in gp.verifier_dialogue(faux, source)))
        self.assertTrue(gp.verifier_dialogue(ok[:5], source), "trop court")
        mono = [{"orateur": "Léa", "texte": l["texte"]} for l in ok]
        self.assertTrue(any("deux animateurs" in p for p in gp.verifier_dialogue(mono, source)))

    def test_decoupage_et_assemblage(self):
        lignes = [{"orateur": "Léa", "texte": "a" * 500}, {"orateur": "Hugo", "texte": "b" * 500},
                  {"orateur": "Léa", "texte": "c" * 500}, {"orateur": "Hugo", "texte": "d" * 100}]
        morceaux = gp.decouper(lignes, 1100)
        self.assertEqual([len(m) for m in morceaux], [2, 2])
        pcm = gp.assembler([b"\x01\x00" * 10, b"\x02\x00" * 10], silence_s=0.1)
        self.assertEqual(len(pcm), 40 + 2 * int(gp.SAMPLE_RATE * 0.1))

    def test_reponse_wav_ou_pcm(self):
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b"\x05\x00" * 8)
        self.assertEqual(gp._pcm_depuis_reponse(buf.getvalue(), "audio/wav"), b"\x05\x00" * 8)
        self.assertEqual(gp._pcm_depuis_reponse(b"\x07\x00" * 4, "audio/L16;rate=24000"), b"\x07\x00" * 4)

    def test_ouverture_annonce_la_voix_de_synthese(self):
        debut, fin = gp.ouverture_fermeture({"date": "2026-10-03"})
        self.assertIn("intelligence artificielle", " ".join(l["texte"] for l in debut))
        self.assertIn("lesscenarios.fr", " ".join(l["texte"] for l in fin))

    def test_habillage_musical(self):
        voix = array("h", [int(8000 * (1 if (i // 40) % 2 else -1)) for i in range(mu.SR * 2)]).tobytes()
        sortie = mu.habiller(voix)
        a = array("h")
        a.frombytes(sortie)
        n_attendu = len(voix) // 2 + int(mu.SR * mu.INTRO_S) + int(mu.SR * mu.OUTRO_S)
        self.assertEqual(len(a), n_attendu, "ouverture + voix + fermeture")
        self.assertLess(max(abs(x) for x in a), 32767, "pas d'écrêtage")
        debut = max(abs(x) for x in a[: int(mu.SR * 4)])
        sous_voix = max(abs(x) for x in a[int(mu.SR * (mu.INTRO_S + 0.2)): int(mu.SR * (mu.INTRO_S + 1.8))])
        self.assertGreater(debut, 3000, "l'ouverture est audible")
        self.assertGreater(sous_voix, 7000, "la voix reste bien au premier plan")
        self.assertEqual(sortie, mu.habiller(voix), "musique déterministe")

    def test_fond_discret_sous_les_voix(self):
        pts = mu.enveloppe_fond(60.0)
        self.assertAlmostEqual(mu._gain(pts, 1.0), mu.NIVEAU_OUVERTURE)
        self.assertAlmostEqual(mu._gain(pts, 30.0), mu.NIVEAU_SOUS_VOIX)
        self.assertLess(mu._gain(pts, 59.9), 0.02)



class TestFlux(unittest.TestCase):
    def test_flux_podcast(self):
        import build_feed
        import xml.etree.ElementTree as ET
        eps = [{"date": "2026-10-03", "titre": "A & B", "description": "d", "url": "https://x/y.mp3?a=1&b=2",
                "taille": 100, "duree": 3725}]
        xml = build_feed.construire(eps, "contact@example.org")
        racine = ET.fromstring(xml)
        ns = {"i": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
        self.assertEqual(racine.find("channel/item/enclosure").get("url"), "https://x/y.mp3?a=1&b=2")
        self.assertEqual(racine.find("channel/item/i:duration", ns).text, "01:02:05")
        self.assertEqual(racine.find("channel/i:owner/i:email", ns).text, "contact@example.org")
        self.assertNotIn("itunes:owner", build_feed.construire(eps, ""))



class TestNarration(unittest.TestCase):
    def test_decoupe_entre_paragraphes(self):
        texte = "\n\n".join(f"Paragraphe {i} " + "mot " * 99 + "mot" for i in range(10))
        morceaux = gp.decouper_texte(texte, limite=1000)
        self.assertGreater(len(morceaux), 1)
        self.assertTrue(all(len(m) <= 1000 for m in morceaux))
        self.assertEqual("\n\n".join(morceaux), texte)



class TestTexteNarration(unittest.TestCase):
    def test_exemple_valide_et_defauts_refuses(self):
        import texte_narration as tn
        from pathlib import Path as P
        ed = gp.lire_edition(sorted((gp.ROOT / "archives").glob("2026-10-03.html"))[0])
        src = gp.texte_source(ed)
        exemple = tn.EXEMPLE.read_text(encoding="utf-8")
        self.assertEqual(tn.verifier(exemple, src), [])
        self.assertTrue(tn.verifier("Bonjour. " + exemple, src))          # formule d'accueil
        self.assertTrue(tn.verifier(exemple + " Le chiffre 4242 est faux.", src))  # nombre inventé
        self.assertTrue(tn.verifier("Trop court.", src))



class TestOuverture(unittest.TestCase):
    def test_ouverture_energique(self):
        voix = array("h", [3000] * (mu.SR * 2)).tobytes()
        pcm = array("h")
        pcm.frombytes(mu.avec_ouverture_energique(voix))
        duree = len(pcm) / mu.SR
        self.assertAlmostEqual(duree, mu.OUVERTURE_S + 2 + 0.5, delta=0.1)
        crete = max(abs(x) for x in pcm) / 32768
        self.assertTrue(0.3 < crete < 0.95, crete)           # audible, sans saturation
        debut = sum(abs(x) for x in pcm[:mu.SR * 4]) / (mu.SR * 4)
        self.assertGreater(debut, 500)                       # la musique joue bien avant la voix



class TestTheme(unittest.TestCase):
    def test_melange_theme(self):
        theme = array("h", [4000] * (mu.SR * 6)).tobytes()
        voix = array("h", [3000] * (mu.SR * 3)).tobytes()
        pcm = array("h")
        pcm.frombytes(mu.melanger_theme(theme, voix))
        # la voix démarre 1,5 s avant la fin du thème : durée = 6 - 1,5 + 3 + 0,5 s
        self.assertAlmostEqual(len(pcm) / mu.SR, 8.0, delta=0.05)
        self.assertGreater(abs(pcm[mu.SR]), 2000)                 # thème audible au début
        self.assertGreater(abs(pcm[int(mu.SR * 6.5)]), 2000)      # voix audible après le thème
        self.assertIsNone(mu.trouver_theme("/inexistant"))


if __name__ == "__main__":
    unittest.main()
