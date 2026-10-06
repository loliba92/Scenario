#!/usr/bin/env python3
"""Voix de synthèse via OpenRouter (POST /api/v1/audio/speech) : moteur de remplacement des voix Google.

Les voix Google gratuites ont un quota quotidien trop juste (3-4 octobre 2026). OpenRouter facture à l'usage, sans quota
journalier, avec la clé déjà utilisée pour les textes. La sortie « pcm » est du 24 kHz mono 16 bits, comme le reste du
programme.

Utilisation comparative (échantillons d'un même texte) :
    OPENROUTER_API_KEY=... python3 scripts/podcast/voix_openrouter.py podcast/textes/2026-10-02.txt \
        "microsoft/mai-voice-2.1|fr-FR-Harper:MAI-Voice-2.1" "mistralai/voxtral-mini-tts-2603|fr_marie_neutral"
Sortie : _podcast-out/echantillon-<texte>-<modèle>-<voix>.mp3 (ou .wav sans ffmpeg).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_podcast as gp  # noqa: E402

URL = "https://openrouter.ai/api/v1/audio/speech"


def synthese_openrouter(texte: str, modele: str, voix: str, cle: str, essais: int = 3) -> bytes:
    """PCM 16 bits mono 24 kHz du texte lu par `voix` du `modele`."""
    charge = {"model": modele, "input": texte, "response_format": "pcm"}
    if voix:  # certains modèles (Fish Audio) n'ont pas de liste de voix : le champ est alors omis
        charge["voice"] = voix
    corps = json.dumps(charge).encode()
    derniere = ""
    for n in range(essais):
        if n:
            time.sleep(15 * n)
        req = urllib.request.Request(URL, data=corps, method="POST",
                                     headers={"Content-Type": "application/json", "Authorization": f"Bearer {cle}"})
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                donnees = r.read()
            if len(donnees) < 4800:  # moins de 0,1 s : réponse d'erreur ou vide
                derniere = f"réponse trop courte ({len(donnees)} octets) : {donnees[:200]!r}"
                continue
            return donnees
        except urllib.error.HTTPError as e:
            derniere = f"HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}"
            if e.code not in (429, 500, 502, 503):
                break
        except (TimeoutError, urllib.error.URLError) as e:
            derniere = f"{type(e).__name__}: {e}"
    raise gp.PodcastError(f"synthèse OpenRouter impossible ({modele}, {voix}) : {derniere}")


def _nom(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")


def main(argv=None) -> int:
    sys.stdout.reconfigure(line_buffering=True)
    args = list(sys.argv[1:] if argv is None else argv)
    # --car=N : échantillon très court (N caractères environ, coupés à la fin d'un mot) pour juger la couleur d'une voix
    car = next((int(a[6:]) for a in args if re.fullmatch(r"--car=\d{1,4}", a)), None)
    args = [a for a in args if not a.startswith("--car=")]
    # --clair : écrit en plus une version « -clair » (aigus relevés) de chaque échantillon, pour une voix étouffée
    clair = "--clair" in args
    args = [a for a in args if a != "--clair"]
    if len(args) < 2:
        print(__doc__)
        return 1
    cle = os.environ.get("OPENROUTER_API_KEY")
    if not cle:
        print("ERREUR : OPENROUTER_API_KEY absent.", file=sys.stderr)
        return 1
    texte = Path(args[0]).read_text(encoding="utf-8")
    # échantillon : les premières parties jusqu'à 600 caractères au moins (1 à 1,5 minute de voix)
    import texte_narration
    echantillon, total = [], 0
    for p in texte_narration.parties(texte):
        echantillon.append(p)
        total += len(p)
        if total >= 600:
            break
    extrait = "\n\n".join(echantillon)
    if car:
        extrait = extrait[:car].rsplit(" ", 1)[0].strip()
    print(f"Échantillon : {len(extrait)} caractères", flush=True)
    out = gp.ROOT / "_podcast-out"
    out.mkdir(parents=True, exist_ok=True)
    echecs = 0
    for couple in args[1:]:
        modele, _, voix = couple.partition("|")
        try:
            pcm = synthese_openrouter(extrait, modele, voix, cle)
        except gp.PodcastError as e:
            print(f"ECHEC : {e}", file=sys.stderr)
            echecs += 1
            continue
        nom = f"echantillon-{Path(args[0]).stem}-{_nom(modele)}-{_nom(voix)}"
        wav = out / f"{nom}.wav"
        gp.ecrire_wav(pcm, wav)
        mp3 = out / f"{nom}.mp3"
        if clair:
            gp.vers_mp3(wav, out / f"{nom}-clair.mp3", clair=True)
        if gp.vers_mp3(wav, mp3):
            wav.unlink()
        print(f"OK : {nom} ({len(pcm) / 2 / gp.SAMPLE_RATE:.0f} s)", flush=True)
    return 1 if echecs == len(args[1:]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
