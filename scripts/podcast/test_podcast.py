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
        # la voix démarre 2 s avant la fin du thème : durée = 6 - 2 + 3 + 0,5 s
        self.assertAlmostEqual(len(pcm) / mu.SR, 7.5, delta=0.05)
        self.assertGreater(abs(pcm[mu.SR]), 2000)                 # thème audible au début
        self.assertGreater(abs(pcm[int(mu.SR * 6.5)]), 2000)      # voix audible après le thème
        self.assertIsNone(mu.trouver_theme("/inexistant"))



class TestControleDebut(unittest.TestCase):
    def test_debut_correspond(self):
        texte = "Une question qui touche beaucoup de femmes : faut-il continuer ?"
        self.assertTrue(gp.debut_correspond("Une question qui touche beaucoup de femmes, faut-il", texte))
        self.assertTrue(gp.debut_correspond("une question qui touche beaucoup de femme", texte))   # accent, pluriel proche
        # la consigne lue à voix haute au lieu du texte : refusé
        self.assertFalse(gp.debut_correspond("Lis ce texte en français avec une voix chaleureuse proche et naturelle", texte))



class TestJingles(unittest.TestCase):
    def test_parties_et_verification(self):
        import texte_narration as tn
        txt = "Première partie.\n\nSuite.\n---\nDeuxième partie.\n  ---  \nTroisième."
        self.assertEqual(tn.parties(txt), ["Première partie.\n\nSuite.", "Deuxième partie.", "Troisième."])
        exemple = tn.EXEMPLE.read_text(encoding="utf-8")
        ed = gp.lire_edition(sorted((gp.ROOT / "archives").glob("2026-10-03.html"))[0])
        avec_sep = exemple.replace("\n\nAlors, que peut-il", "\n---\nAlors, que peut-il")
        self.assertEqual(tn.verifier(avec_sep, gp.texte_source(ed)), [])   # --- n'est pas du Markdown

    def test_probabilites_en_fractions(self):
        import texte_narration as tn
        src = "25 % 50 % 84 %"
        base = "Le sujet est simple. " * 10
        mauvais = tn.verifier(base + "Le premier scénario a 25 % de chances.", src)
        self.assertTrue(any("fractions" in x for x in mauvais))
        ok = tn.verifier(base + "Selon l'étude, 84 % des morceaux ont émergé en ligne. Une chance sur quatre.", src)
        self.assertFalse(any("fractions" in x for x in ok))

    def test_derniere_chance_phrase_un_peu_longue(self):
        # 6 octobre 2026 : un seul texte avec une phrase de 33 mots a fait perdre l'épisode du jour
        import texte_narration as tn
        exemple = tn.EXEMPLE.read_text(encoding="utf-8")
        ed = gp.lire_edition(sorted((gp.ROOT / "archives").glob("2026-10-03.html"))[0])
        src = gp.texte_source(ed)
        moyenne = "Voici une phrase un peu longue qui " + "continue avec des mots simples " * 5 + "puis finit."
        n = len(moyenne.split())
        self.assertTrue(tn.MOTS_PHRASE_MAX < n <= tn.MOTS_PHRASE_MAX_DERNIER_ESSAI, n)
        texte = exemple + "\n" + moyenne
        strict = [x for x in tn.verifier(texte, src) if "phrases trop longues" in x]
        self.assertTrue(strict)
        self.assertIn("à couper en deux", strict[0])                       # la phrase fautive est citée au modèle
        self.assertFalse(any("phrases trop longues" in x for x in tn.verifier(texte, src, dernier_essai=True)))

    def test_derniere_chance_texte_un_peu_long(self):
        # 6 octobre 2026 : 1010, 981 puis 761 mots pour un maximum de 720 (relevé à 1000) : épisode perdu deux fois
        import texte_narration as tn
        exemple = tn.EXEMPLE.read_text(encoding="utf-8")
        ed = gp.lire_edition(sorted((gp.ROOT / "archives").glob("2026-10-03.html"))[0])
        src = gp.texte_source(ed)
        reste = tn.MOTS_MAX - len(exemple.split()) + 40
        long = exemple + "\n\n" + ("Une phrase courte et claire sur le sujet du jour. " * (reste // 9 + 1))
        n = len(tn.verifier(long, src, dernier_essai=True))
        self.assertFalse(any("mots" in x and "trop long" in x for x in tn.verifier(long, src, dernier_essai=True)), n)
        strict = [x for x in tn.verifier(long, src) if "trop long de" in x]
        self.assertTrue(strict)
        self.assertIn(str(tn.MOTS_CIBLE), strict[0])                       # le modèle reçoit un objectif chiffré
        enorme = exemple + "\n\n" + ("Une phrase courte et claire sur le sujet du jour. " * 120)
        self.assertTrue(any("trop long de" in x for x in tn.verifier(enorme, src, dernier_essai=True)))

    def test_pedagogie_phrases_courtes_et_accueil(self):
        import texte_narration as tn
        exemple = tn.EXEMPLE.read_text(encoding="utf-8")
        ed = gp.lire_edition(sorted((gp.ROOT / "archives").glob("2026-10-03.html"))[0])
        src = gp.texte_source(ed)
        longue = "Voici une phrase interminable qui " + "continue encore et encore avec des mots " * 6 + "et finit."
        self.assertTrue(any("phrases trop longues" in x for x in tn.verifier(exemple + "\n" + longue, src)))
        self.assertFalse(any("phrases trop longues" in x for x in tn.verifier(exemple, src)))
        self.assertIn("trois évolutions possibles", tn.OUVERTURE)
        sans = exemple.replace("scénarios", "trajectoires").replace("scénario", "trajectoire")
        self.assertTrue(any("scénarios" in x for x in tn.verifier(sans, src)))
        self.assertFalse(any("« scénarios »" in x for x in tn.verifier(exemple, src)))
        self.assertNotIn("façons", tn.OUVERTURE)
        self.assertLess(len(tn.OUVERTURE.split()), 20)

    def test_lexique_et_regles_pour_l_oreille(self):
        import texte_narration as tn
        ed = gp.lire_edition(gp.ROOT / "archives" / "2026-10-05.html")
        termes = [x["terme"] for x in ed["lexique"]]
        self.assertIn("OSNMA", termes)
        self.assertIn("brouillage", termes)
        self.assertIn("LEXIQUE DE LA RÉDACTION", gp.texte_source(ed))
        prompt = tn.construire_prompt(ed)
        for attendu in ("LEXIQUE (termes à expliquer", "jamais de sigle de quatre lettres", "une seule cause par phrase",
                        "image du quotidien", "En clair,", "OSNMA : "):
            self.assertIn(attendu, prompt)

    def test_controles_sigles_chaines_et_reformulation(self):
        import re
        import texte_narration as tn
        ed = gp.lire_edition(sorted((gp.ROOT / "archives").glob("2026-10-03.html"))[0])
        src = gp.texte_source(ed)
        base = tn.EXEMPLE.read_text(encoding="utf-8")
        self.assertEqual(tn.verifier(base, src), [])
        self.assertTrue(any("sigle" in x for x in tn.verifier(base + "\nLe protocole OSNMA protège les signaux.", src)))
        self.assertTrue(any("sigle" in x for x in tn.verifier(base + "\nLe système GLONASS est russe.", src)))
        self.assertFalse(any("sigle" in x for x in tn.verifier(base + "\nL'OTAN et le GPS sont connus.", src)))
        chaine = "\nLe signal se perd, ce qui décale les horloges, ce qui coupe les téléphones."
        self.assertTrue(any("chaîne" in x for x in tn.verifier(base + chaine, src)))
        sans_resume = re.sub(r"(?i)\b(en clair|autrement dit|en d'autres termes|en deux mots)\b", "Bref", base)
        self.assertTrue(any("reformulation" in x for x in tn.verifier(sans_resume, src)))

    def test_sept_accueils_et_sept_fermetures(self):
        import re
        from datetime import date, timedelta
        import texte_narration as tn
        self.assertEqual((len(tn.OUVERTURES), len(tn.FERMETURES)), (7, 7))
        self.assertEqual((len(set(tn.OUVERTURES)), len(set(tn.FERMETURES))), (7, 7), "tous différents")
        for o in tn.OUVERTURES:
            self.assertIn("Scénario", o)
            self.assertIn("trois évolutions possibles", o)
            self.assertNotIn("façons", o)
            self.assertLess(len(o.split()), 24)
        for f in tn.FERMETURES:
            self.assertIn("lesscenarios.fr", f)
            self.assertRegex(f, r"[Àà] demain, pour un nouveau scénario|à demain pour un nouveau scénario")
            self.assertNotIn("évolution", f)
            self.assertTrue(f.endswith("Prenez soin de vous. Rien n'est écrit à l'avance. À demain, pour un nouveau scénario."),
                            "rituel fixe : la devise du site, mot pour mot")
            self.assertFalse(re.search(r"\b(tu|ton|ta|tes|toi|te)\b", f, re.I), "vouvoiement")
            self.assertFalse(re.search(tn.MOTS_INTERDITS, f, re.I))
            for phrase in re.split(r"[.!?]", f):
                self.assertLessEqual(len(phrase.split()), tn.MOTS_PHRASE_MAX)
        jours = [date(2026, 10, 5) + timedelta(days=i) for i in range(70)]
        o = [tn.ouverture(j.isoformat()) for j in jours]
        f = [tn.fermeture(j.isoformat()) for j in jours]
        self.assertTrue(all(a != b for a, b in zip(o, o[1:])), "jamais deux accueils identiques de suite")
        self.assertTrue(all(a != b for a, b in zip(f, f[1:])), "jamais deux fermetures identiques de suite")
        self.assertEqual(len(set(o[:7])), 7, "les sept accueils sont joués chaque semaine")
        self.assertEqual(len(set(f[:14])), 7, "les sept fermetures sont toutes jouées en deux semaines")
        self.assertEqual(len(set(f)), 7)
        self.assertNotEqual(list(zip(o[:7], f[:7])), list(zip(o[7:14], f[7:14])), "le couple change d'une semaine à l'autre")
        self.assertEqual(tn.ouverture("2026-10-05"), tn.ouverture("2026-10-05-1253"), "suffixe ignoré")
        self.assertEqual(tn.ouverture("n'importe quoi"), tn.OUVERTURE)

    def test_registre_sans_mots_pejoratifs(self):
        import re
        import texte_narration as tn
        for mauvais in ("Ça n'a pas de gueule.", "Un tournoi nul.", "Quelle merde.", "Des joueurs minables."):
            self.assertTrue(re.search(tn.MOTS_INTERDITS, mauvais, re.I), mauvais)
        for bon in ("Le public adhère très vite.", "C'est un pari audacieux, et pas évident.", "Le tournoi est accepté.", "Aucune fatigue nulle part."):
            self.assertFalse(re.search(tn.MOTS_INTERDITS, bon, re.I), bon)
        exemple = tn.EXEMPLE.read_text(encoding="utf-8")
        self.assertFalse(re.search(tn.MOTS_INTERDITS, exemple, re.I))

    def test_assemblage_avec_jingles(self):
        theme = array("h", [5000] * (mu.SR * 6)).tobytes()
        jingle = mu.jingle_depuis_theme(theme)
        self.assertAlmostEqual(len(jingle) / 2 / mu.SR, 2.5, delta=0.01)
        a = array("h", [3000] * (mu.SR * 2)).tobytes()
        sans = mu.assembler_parties([a, a, a], None)
        avec = mu.assembler_parties([a, a, a], jingle, recouvrement_s=2.0)
        self.assertAlmostEqual(len(sans) / 2 / mu.SR, 6 + 2 * 0.7, delta=0.01)
        self.assertAlmostEqual(len(avec) / 2 / mu.SR, 6 + 2 * (0.3 + 2.5 - 2.0), delta=0.01)
        # jingles différents, bien pris à des endroits distincts du thème
        self.assertEqual(mu._lisse(0.0), 0.0)
        self.assertEqual(mu._lisse(1.0), 1.0)
        self.assertLess(mu._lisse(0.1), 0.1)   # départ en douceur, pas linéaire
        t30 = array("h", [(i // 24000) * 500 for i in range(mu.SR * 61)]).tobytes()
        js = mu.jingles_depuis_theme(t30, 4)
        self.assertEqual(len(js), 4)
        self.assertEqual(len({j for j in js}), 4)



class TestImageEpisode(unittest.TestCase):
    def test_pochette_et_balise(self):
        import tempfile
        import build_feed
        from PIL import Image
        import xml.etree.ElementTree as ET
        with tempfile.TemporaryDirectory() as t:
            photos, images = Path(t) / "photos", Path(t) / "images"
            photos.mkdir()
            Image.new("RGB", (1080, 1200), (200, 120, 60)).save(photos / "2026-10-04.jpg")   # pas carrée : recadrée
            chemin = build_feed.preparer_image("2026-10-04", images, photos)
            im = Image.open(chemin)
            self.assertEqual(im.size, (1400, 1400))
            self.assertLessEqual(chemin.stat().st_size, 500_000)
            self.assertIsNone(build_feed.preparer_image("2026-10-05", images, photos))        # pas d'image : rien
            eps = [{"date": d, "titre": "t", "description": "d", "url": "https://x/y.mp3", "taille": 1, "duree": 60}
                   for d in ("2026-10-04", "2026-10-05")]
            racine = ET.fromstring(build_feed.construire(eps, "", images))
            ns = {"i": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
            images_item = [it.find("i:image", ns) for it in racine.findall("channel/item")]
            self.assertIsNotNone(images_item[1])                    # 2026-10-04 (triés du plus récent au plus ancien)
            self.assertIsNone(images_item[0])
            self.assertTrue(images_item[1].get("href").endswith("/podcast/episodes/2026-10-04.jpg"))


class TestFondus(unittest.TestCase):
    def test_fondus_ouverture_et_fermeture(self):
        theme = array("h", [6000] * (mu.SR * 12)).tobytes()
        fin = array("h", [6000] * (mu.SR * 9)).tobytes()
        voix = array("h", [3000] * (mu.SR * 20)).tobytes()
        out = array("h")
        out.frombytes(mu.melanger_theme(theme, voix, fin_pcm=fin))
        self.assertEqual(out[0], 0)                 # entrée en fondu depuis le silence
        self.assertEqual(out[-1], 0)                # sortie en fondu jusqu'à zéro
        self.assertEqual(abs(out[-mu.SR // 2]), 0)
        # la musique de fermeture commence après la voix (fin de la voix à 30 s, puis 9 s de musique)
        self.assertGreater(len(out) / mu.SR, 10 + 20 + 8)
        self.assertLess(max(abs(x) for x in out[: int(mu.SR * 29)]), 32767)


class TestFondContinu(unittest.TestCase):
    def test_fond_leger_et_jingles(self):
        theme = array("h", [(i // 12000 % 2) * 12000 - 6000 for i in range(mu.SR * 40)]).tobytes()
        voix = array("h", [3000] * (mu.SR * 15)).tobytes()
        out = array("h")
        out.frombytes(mu.habiller_fond(theme, [voix, voix, voix]))
        self.assertEqual(out[0], 0)
        self.assertEqual(out[-1], 0)
        w = mu.SR
        niveaux = [mu._rms(out[i * w:(i + 1) * w]) for i in range(len(out) // w)]
        # sous la voix (ex. 3e seconde de la 1re partie, vers 15 s) : voix + fond très léger, donc à peine plus de 3000
        self.assertLess(niveaux[16], 3000 * 1.12)
        self.assertGreater(len(out) / mu.SR, 10 + 15 * 3 + 2 * (mu.JINGLE_S - 3 + 0.3))
        # avec accueil : 1re partie = accueil (6 s) dite à partir de DEBUT_VOIX_S ; musique plus présente dessous, puis seule 4 s avant la question
        D = int(mu.DEBUT_VOIX_S)
        accueil = array("h", [3000] * (mu.SR * 6)).tobytes()
        out2 = array("h")
        out2.frombytes(mu.habiller_fond(theme, [accueil, voix, voix], accueil=True))
        n2 = [mu._rms(out2[i * w:(i + 1) * w]) for i in range(len(out2) // w)]
        self.assertGreater(n2[D + 2], 3050)        # sous l'accueil : voix + musique présente
        # la question entre 4,15 s après la fin de l'accueil (D + 6 + 0,15 + 4) : musique seule juste avant
        seule = n2[D + 6 + 2]
        self.assertGreater(seule, 1500)                    # la musique est bien là, audible
        self.assertLess(seule, 3500)                       # et il n'y a pas de voix (3000 de voix seule + musique serait plus fort)
        self.assertGreater(n2[D + 6 + 6], 2850)            # puis la question
        # dernière partie : musique plus présente que le fond ordinaire
        t_fin = mu.DEBUT_VOIX_S + 6 + (0.15 + 7 - 3) + 15 + (0.3 + mu.JINGLE_S - 3)
        self.assertGreater(n2[int(t_fin) + 5], niveaux[int(t_fin) + 5] * 0.99)

    def test_pause_entre_parties_raccourcie(self):
        # entre deux parties ordinaires : environ 4,8 s de musique seule (avant : 6,3 s)
        self.assertLessEqual(0.3 + mu.JINGLE_S - mu.RECOUVREMENT_JINGLE_S, 5.0)

    def test_chronologie_accueil_7_s_et_pause_courte(self):
        """La voix d'accueil démarre à 7 s ; entre l'accueil et la question, environ 4 s de musique, sans silence en trop."""
        muet = array("h", [0] * (mu.SR * 40)).tobytes()          # thème silencieux : on ne voit que les voix
        silence = array("h", [0] * (mu.SR * 1)).tobytes()
        voix_a = array("h", [4000] * (mu.SR * 6)).tobytes()
        voix_q = array("h", [4000] * (mu.SR * 10)).tobytes()
        # la synthèse laisse 1 s de silence avant et après chaque partie : elles doivent être rognées
        a_tts, q_tts = silence + voix_a + silence, silence + voix_q + silence
        out = array("h")
        out.frombytes(mu.habiller_fond(muet, [a_tts, q_tts, q_tts], accueil=True))
        seuil = 100
        actif = [i for i, x in enumerate(out) if abs(x) > seuil]
        debut = actif[0] / mu.SR
        self.assertEqual(mu.DEBUT_VOIX_S, 7.0)
        self.assertAlmostEqual(debut, 7.0, delta=0.2)   # démarre à 7 s (marge de 0,08 s avant la voix)
        fin_accueil = next(i for i in range(int(mu.SR * (mu.DEBUT_VOIX_S + 1)), len(out)) if abs(out[i]) <= seuil) / mu.SR
        debut_question = next(i for i in range(int(fin_accueil * mu.SR), len(out)) if abs(out[i]) > seuil) / mu.SR
        pause = debut_question - fin_accueil
        self.assertGreater(pause, 3.8)
        self.assertLess(pause, 4.8, "avant : plus de 6 s (pause de 5 s + silences de la synthèse + remontée lente)")

    def test_mp3_volume_normalise(self):
        """Le MP3 final passe par la normalisation du volume (-16 LUFS), sauf demande contraire."""
        from unittest import mock
        with mock.patch.object(gp.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                mock.patch.object(gp.subprocess, "run") as run:
            gp.vers_mp3(Path("a.wav"), Path("a.mp3"))
            gp.vers_mp3(Path("a.wav"), Path("b.mp3"), normaliser=False)
        avec, sans = run.call_args_list[0].args[0], run.call_args_list[1].args[0]
        self.assertIn("loudnorm=I=-16:TP=-1.5:LRA=11", avec)
        self.assertIn("-ac", avec)
        self.assertNotIn("-af", sans)

    def test_mp3_option_clarte_seulement_a_la_demande(self):
        from unittest import mock
        with mock.patch.object(gp.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                mock.patch.object(gp.subprocess, "run") as run:
            gp.vers_mp3(Path("a.wav"), Path("a.mp3"))
            gp.vers_mp3(Path("a.wav"), Path("b.mp3"), clair=True)
        normal, clair = (c.args[0][c.args[0].index("-af") + 1] for c in run.call_args_list)
        self.assertNotIn("highshelf", normal)
        self.assertTrue(clair.startswith("equalizer=") and clair.endswith(gp.FILTRE_VOLUME))


if __name__ == "__main__":
    unittest.main()
