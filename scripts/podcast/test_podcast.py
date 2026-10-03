"""Tests du podcast (sans réseau)."""
import io
import sys
import unittest
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_podcast as gp  # noqa: E402

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
        ok = [{"orateur": o, "texte": "Le taux passe de 84 pour cent à 75 pour cent, soit 3 millions. " + "mot " * 40}
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


if __name__ == "__main__":
    unittest.main()
