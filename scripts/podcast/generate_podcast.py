#!/usr/bin/env python3
"""Épisode audio d'une édition : dialogue à deux voix (texte contrôlé) puis synthèse vocale Gemini.

TEST demandé le 3 octobre 2026 (alternative automatisable à NotebookLM, qui n'a pas d'interface
automatique). Principe :
  1. lire l'édition publiée (archives/AAAA-MM-JJ.html) ;
  2. un modèle (OpenRouter) écrit un dialogue de deux animateurs, SANS rien ajouter à l'article ;
  3. garde-fou : tout nombre cité dans le dialogue doit figurer dans l'article, sinon on redemande ;
  4. synthèse vocale à deux voix (API Gemini), assemblage en un seul fichier ;
  5. habillage musical original (musique.py : ouverture, fond discret sous les voix, fermeture) ;
  6. conversion en MP3.
Le dialogue contient toujours, écrites par le script (jamais par le modèle), l'ouverture qui annonce
que les voix sont générées par intelligence artificielle et la fermeture qui renvoie au site.

Utilisation (clés dans l'environnement : OPENROUTER_API_KEY, GEMINI_API_KEY) :
    python3 scripts/podcast/generate_podcast.py [--date 2026-10-03] [--dialogue-seulement]
Sortie : _podcast-out/AAAA-MM-JJ.mp3, .dialogue.json et .txt (transcription).
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "edition"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

ANIMATEURS = ("Léa", "Hugo")
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
        "octobre", "novembre", "décembre")
MODELES_TTS = ("gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
SAMPLE_RATE = 24000
MAX_CARACTERES_PAR_APPEL = 1400
MOTS_MIN, MOTS_MAX = 550, 1100


class PodcastError(Exception):
    pass


# ---------------------------------------------------------------- lecture de l'édition
def _txt(el) -> str:
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""


def lire_edition(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    ed = {
        "date": path.stem,
        "titre": _txt(soup.h1),
        "faits": [_txt(p) for p in soup.select("p.dek")],
        "essentiel": [_txt(p) for p in soup.select(".essentiel-box p.essentiel-text")],
        "comprendre": _txt(soup.select_one(".comprendre-text")),
        "question": _txt(soup.select_one("#scenarios .section-title")),
        "scenarios": [],
    }
    for card in soup.select("#scenarios article.card"):
        gauge = card.select_one(".gauge-value")
        ed["scenarios"].append({
            "type": _txt(card.select_one(".kind-tag")),
            "probabilite": gauge.get("data-pct") if gauge else _txt(card.select_one(".gauge-num")).rstrip("% "),
            "titre": _txt(card.select_one("h3")),
            "analyse": [_txt(p) for p in card.select("p.why")],
            "indicateurs": [
                f"{_txt(li.select_one('.field-name'))} : {_txt(li.select_one('.evo-current'))} (avant : {_txt(li.select_one('.evo-prev'))})"
                for li in card.select(".field li") if li.select_one(".field-name")
            ],
            "france": _txt(card.select_one(".france-line")).replace("Concrètement en France", "").strip(),
        })
    if not ed["titre"] or len(ed["scenarios"]) < 2 or not ed["faits"]:
        raise PodcastError(f"édition illisible : {path}")
    return ed


def date_longue(iso: str) -> str:
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d}{'er' if d == 1 else ''} {MOIS[m - 1]} {y}"


def texte_source(ed: dict) -> str:
    """Tout ce que le modèle a le droit d'utiliser (et rien d'autre)."""
    parts = [f"TITRE : {ed['titre']}", "LES FAITS :", *ed["faits"], "L'ESSENTIEL :", *ed["essentiel"]]
    if ed["comprendre"]:
        parts += ["POUR LES NOUVEAUX LECTEURS :", ed["comprendre"]]
    parts.append(f"QUESTION POSÉE : {ed['question']}")
    for s in ed["scenarios"]:
        parts += [f"SCÉNARIO {s['type'].upper()} — {s['probabilite']} % de probabilité — {s['titre']}",
                  *s["analyse"], "Indicateurs : " + " ; ".join(s["indicateurs"]), f"En France : {s['france']}"]
    return "\n".join(parts)


# ---------------------------------------------------------------- garde-fou sur les nombres
_NOMBRE = re.compile(r"\d{1,3}(?:[ \u00a0\u202f]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?")


def nombres(texte: str) -> set[str]:
    out = set()
    for m in _NOMBRE.finditer(texte):
        brut = re.sub(r"[\s  ]", "", m.group(0)).replace(",", ".")
        if brut:
            out.add(brut.rstrip("."))
    return out


def verifier_dialogue(lignes: list[dict], source: str) -> list[str]:
    problemes = []
    if len(lignes) < 16:
        problemes.append(f"dialogue trop court ({len(lignes)} répliques)")
    if {l.get("orateur") for l in lignes} != set(ANIMATEURS):
        problemes.append("il faut exactement deux animateurs : " + " et ".join(ANIMATEURS))
    texte = " ".join(str(l.get("texte", "")) for l in lignes)
    mots = len(texte.split())
    if not MOTS_MIN <= mots <= MOTS_MAX:
        problemes.append(f"{mots} mots (attendu entre {MOTS_MIN} et {MOTS_MAX})")
    if "**" in texte or "http" in texte:
        problemes.append("pas de Markdown ni d'adresse web dans le texte lu")
    connus = nombres(source)
    inconnus = sorted(n for n in nombres(texte) if n not in connus and not (n.isdigit() and int(n) <= 10))
    if inconnus:
        problemes.append("nombres absents de l'article : " + ", ".join(inconnus))
    return problemes


# ---------------------------------------------------------------- dialogue
def construire_prompt(ed: dict, remarques: list[str] | None = None) -> str:
    a, b = ANIMATEURS
    suite = ("\n\nTa version précédente a été refusée pour ces raisons, corrige-les :\n- " + "\n- ".join(remarques)) if remarques else ""
    return f"""Tu écris le texte parlé d'un court podcast quotidien du site d'actualité Scénario (lesscenarios.fr), à partir de l'édition du {date_longue(ed['date'])} ci-dessous. Deux animateurs, {a} et {b}, discutent comme à la radio.

RÈGLES ABSOLUES
- N'ajoute AUCUN fait, chiffre, nom, date ni exemple qui ne figure pas dans l'article. Chaque nombre cité doit venir de l'article (écris les nombres en chiffres, par exemple « 84 pour cent »).
- Pas de Markdown, pas d'adresse web, pas de liste : uniquement du langage parlé, phrases courtes, quelques réactions brèves (« Exactement. », « Attends, explique. »).
- Ne dis jamais « selon l'article » ; ne parle pas des animateurs ni de l'intelligence artificielle.
- Ne dis PAS bonjour, bienvenue ni au revoir : le script ajoute lui-même l'ouverture et la fermeture. Commence directement par la question du jour.

STRUCTURE (environ 850 mots, soit 6 minutes)
1. {a} pose la question du jour en une phrase.
2. Les faits, en deux ou trois échanges.
3. Les trois scénarios, un par un : favorable, stable, dégradé, chacun avec sa probabilité, ce qui le rend plausible et ce qu'il changerait en France. Dis clairement lequel est le plus probable.
4. Ce qu'il faut retenir, en deux échanges.
Alterne les répliques ; aucune ne dépasse 70 mots.

ARTICLE
{texte_source(ed)}{suite}

Réponds UNIQUEMENT avec un JSON : {{"lignes": [{{"orateur": "{a}", "texte": "..."}}, {{"orateur": "{b}", "texte": "..."}}]}}"""


def ouverture_fermeture(ed: dict) -> tuple[list[dict], list[dict]]:
    a, b = ANIMATEURS
    debut = [
        {"orateur": a, "texte": f"Bonjour, et bienvenue dans Scénario, l'édition du {date_longue(ed['date'])}."},
        {"orateur": b, "texte": "Une précision d'abord : les voix de ce podcast sont générées par intelligence artificielle. Le texte, lui, suit l'article publié sur le site."},
    ]
    fin = [
        {"orateur": a, "texte": "L'édition complète, avec les indicateurs et le lexique, est sur lesscenarios.fr."},
        {"orateur": b, "texte": "À demain pour une nouvelle question à issue ouverte."},
    ]
    return debut, fin


def generer_dialogue(ed: dict, modele: str, cle: str, essais: int = 3) -> tuple[list[dict], list[str]]:
    import enrich_sujets as en  # relais de modèles gratuits (voir enrich_sujets.py)

    source = texte_source(ed)
    remarques: list[str] = []
    dernier: list[dict] = []
    for n in range(1, essais + 1):
        resultat, _ = en._appeler_avec_reprises(construire_prompt(ed, remarques or None), modele, cle,
                                                temperature=0.6, max_tokens=8000, timeout=240)
        lignes = [
            {"orateur": str(l.get("orateur", "")).strip(), "texte": re.sub(r"\s+", " ", str(l.get("texte", ""))).strip()}
            for l in (resultat or {}).get("lignes", []) if isinstance(l, dict) and str(l.get("texte", "")).strip()
        ]
        dernier = lignes
        remarques = verifier_dialogue(lignes, source)
        print(f"  essai {n}/{essais} : {len(lignes)} répliques, {'conforme' if not remarques else '; '.join(remarques)}", flush=True)
        if not remarques:
            break
    else:
        raise PodcastError("dialogue refusé par le garde-fou : " + "; ".join(remarques))
    debut, fin = ouverture_fermeture(ed)
    return debut + dernier + fin, remarques


# ---------------------------------------------------------------- synthèse vocale
def decouper(lignes: list[dict], limite: int = MAX_CARACTERES_PAR_APPEL) -> list[list[dict]]:
    morceaux, courant, taille = [], [], 0
    for l in lignes:
        t = len(l["texte"]) + 8
        if courant and taille + t > limite:
            morceaux.append(courant)
            courant, taille = [], 0
        courant.append(l)
        taille += t
    if courant:
        morceaux.append(courant)
    return morceaux


def _pcm_depuis_reponse(data: bytes, mime: str) -> bytes:
    if data[:4] == b"RIFF" or "wav" in mime.lower():
        with wave.open(io.BytesIO(data)) as w:
            return w.readframes(w.getnframes())
    return data


def synthese(morceau: list[dict], voix: tuple[str, str], modeles: tuple[str, ...], cle: str) -> bytes:
    texte = ("Lis cette conversation de podcast d'actualité en français, ton posé, naturel et chaleureux, "
             "sans accentuer artificiellement :\n" + "\n".join(f"{l['orateur']}: {l['texte']}" for l in morceau))
    corps = json.dumps({
        "contents": [{"parts": [{"text": texte}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
                {"speaker": ANIMATEURS[0], "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voix[0]}}},
                {"speaker": ANIMATEURS[1], "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voix[1]}}},
            ]}},
        },
    }).encode()
    derniere = ""
    for modele in modeles:
        for attente in (0, 20, 45):
            if attente:
                time.sleep(attente)
            req = urllib.request.Request(GEMINI_URL.format(model=modele), data=corps, method="POST",
                                         headers={"Content-Type": "application/json", "x-goog-api-key": cle})
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    rep = json.loads(r.read())
                part = rep["candidates"][0]["content"]["parts"][0]["inlineData"]
                return _pcm_depuis_reponse(base64.b64decode(part["data"]), part.get("mimeType", ""))
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")[:300]
                derniere = f"{modele} : HTTP {e.code} {detail}"
                print("  … " + derniere, file=sys.stderr, flush=True)
                if e.code not in (429, 500, 503):
                    break  # erreur de requête (modèle inconnu, clé refusée…) : modèle suivant
            except (KeyError, IndexError, ValueError, TimeoutError, urllib.error.URLError) as e:
                derniere = f"{modele} : réponse inutilisable ({type(e).__name__}: {e})"
                print("  … " + derniere, file=sys.stderr, flush=True)
    raise PodcastError("synthèse vocale impossible : " + derniere)


def assembler(pcms: list[bytes], silence_s: float = 0.4) -> bytes:
    blanc = b"\x00\x00" * int(SAMPLE_RATE * silence_s)
    return blanc.join(pcms)


def ecrire_wav(pcm: bytes, chemin: Path) -> None:
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm)


def vers_mp3(wav: Path, mp3: Path) -> bool:
    if not shutil.which("ffmpeg"):
        return False
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-codec:a", "libmp3lame", "-b:a", "96k", str(mp3)], check=True)
    return True


# ---------------------------------------------------------------- programme
def main(argv=None) -> int:
    sys.stdout.reconfigure(line_buffering=True)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=None, help="AAAA-MM-JJ ; défaut : dernière édition publiée")
    ap.add_argument("--dialogue-model", default="gratuits", help="modèle(s) OpenRouter du dialogue, ou « gratuits »")
    ap.add_argument("--tts-models", default=",".join(MODELES_TTS), help="modèles Gemini de synthèse vocale, par ordre de préférence")
    ap.add_argument("--voix", default="Kore,Puck", help="voix de Léa et de Hugo (voix prédéfinies Gemini)")
    ap.add_argument("--sans-musique", action="store_true", help="voix seules, sans ouverture ni fond musical")
    ap.add_argument("--dialogue-seulement", action="store_true", help="n'écrit que le dialogue (aucune clé Gemini nécessaire)")
    ap.add_argument("--out", default=str(ROOT / "_podcast-out"))
    args = ap.parse_args(argv)

    archives = sorted(p for p in (ROOT / "archives").glob("*.html") if re.match(r"\d{4}-\d{2}-\d{2}\.html$", p.name))
    chemin = (ROOT / "archives" / f"{args.date}.html") if args.date else archives[-1]
    if not chemin.exists():
        print(f"ERREUR : {chemin} introuvable", file=sys.stderr)
        return 1
    ed = lire_edition(chemin)
    print(f"Édition du {date_longue(ed['date'])} : {ed['titre']}")

    cle_or = os.environ.get("OPENROUTER_API_KEY")
    cle_g = os.environ.get("GEMINI_API_KEY")
    if not cle_or:
        print("ERREUR : OPENROUTER_API_KEY absent.", file=sys.stderr)
        return 1
    if not args.dialogue_seulement and not cle_g:
        print("ERREUR : GEMINI_API_KEY absent (ou utiliser --dialogue-seulement).", file=sys.stderr)
        return 1

    try:
        lignes, _ = generer_dialogue(ed, args.dialogue_model, cle_or)
    except PodcastError as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        return 1
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{ed['date']}.dialogue.json").write_text(json.dumps(lignes, ensure_ascii=False, indent=1), encoding="utf-8")
    transcription = "\n\n".join(f"{l['orateur']} : {l['texte']}" for l in lignes)
    (out / f"{ed['date']}.txt").write_text(transcription + "\n", encoding="utf-8")
    mots = sum(len(l["texte"].split()) for l in lignes)
    print(f"\nDIALOGUE ({len(lignes)} répliques, {mots} mots, environ {mots / 150:.1f} min) :\n\n{transcription}\n", flush=True)
    if args.dialogue_seulement:
        return 0

    voix = tuple(v.strip() for v in args.voix.split(","))[:2]
    modeles = tuple(m.strip() for m in args.tts_models.split(",") if m.strip())
    morceaux = decouper(lignes)
    pcms = []
    for i, m in enumerate(morceaux, 1):
        print(f"Synthèse vocale {i}/{len(morceaux)} ({sum(len(l['texte']) for l in m)} caractères)…", flush=True)
        try:
            pcms.append(synthese(m, voix, modeles, cle_g))
        except PodcastError as e:
            print(f"ERREUR : {e}", file=sys.stderr)
            return 1
    pcm = assembler(pcms)
    if not args.sans_musique:
        import musique  # musique originale synthétisée (voir musique.py)
        pcm = musique.habiller(pcm)
    wav = out / f"{ed['date']}.wav"
    ecrire_wav(pcm, wav)
    duree = len(pcm) / 2 / SAMPLE_RATE
    mp3 = out / f"{ed['date']}.mp3"
    if vers_mp3(wav, mp3):
        wav.unlink()
        print(f"OK : {mp3} ({duree / 60:.1f} min, {mp3.stat().st_size / 1e6:.1f} Mo)")
    else:
        print(f"OK : {wav} (ffmpeg absent, pas de MP3 ; {duree / 60:.1f} min)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
