#!/usr/bin/env python3
"""Lit un texte déjà écrit avec UNE voix Gemini (narration), sans dialogue.

Test du 3 octobre 2026 : le dialogue à deux voix sonnait trop artificiel. Ici, le texte est écrit à part
(podcast/textes/AAAA-MM-JJ.txt), une seule voix le lit avec une consigne d'interprétation chaleureuse.

    GEMINI_API_KEY=... python3 scripts/podcast/narration.py podcast/textes/2026-10-03.txt --voix Sulafat
Sortie : _podcast-out/AAAA-MM-JJ.mp3 (ou .wav sans ffmpeg).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_podcast as gp  # noqa: E402


def main(argv=None) -> int:
    sys.stdout.reconfigure(line_buffering=True)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("texte", help="fichier texte à lire, ou « auto » : le texte est écrit à partir d'une édition publiée")
    ap.add_argument("--date", default=None, help="avec « auto » : édition AAAA-MM-JJ (défaut : la dernière)")
    ap.add_argument("--modele", default=gp.MODELES_NARRATION, help="avec « auto » : modèle(s) OpenRouter qui écrivent le texte (gratuits d'abord, puis un modèle payant bon marché)")
    ap.add_argument("--voix", default="Sulafat", help="voix prédéfinie Gemini (Sulafat, Achird, Vindemiatrix, Aoede, Kore…)")
    ap.add_argument("--tts-models", default=",".join(gp.MODELES_TTS_NARRATION))
    ap.add_argument("--musique", action="store_true", help="ajouter l'ancien habillage musical de musique.py (désactivé par défaut)")
    ap.add_argument("--ouverture", action="store_true", help="ajouter le thème podcast/musique/ouverture.mp3 avant la voix, s'il existe (sinon : sans musique)")
    ap.add_argument("--suffixe", default="", help="ajouté au nom du fichier (comparer plusieurs voix)")
    ap.add_argument("--out", default=str(gp.ROOT / "_podcast-out"))
    args = ap.parse_args(argv)

    cle = os.environ.get("GEMINI_API_KEY")
    if not cle:
        print("ERREUR : GEMINI_API_KEY absent.", file=sys.stderr)
        return 1
    if args.texte == "auto":
        import texte_narration
        cle_or = os.environ.get("OPENROUTER_API_KEY")
        if not cle_or:
            print("ERREUR : OPENROUTER_API_KEY absent.", file=sys.stderr)
            return 1
        archives = sorted(p for p in (gp.ROOT / "archives").glob("*.html") if re.match(r"\d{4}-\d{2}-\d{2}\.html$", p.name))
        edition = (gp.ROOT / "archives" / f"{args.date}.html") if args.date else archives[-1]
        ed = gp.lire_edition(edition)
        print(f"Édition du {gp.date_longue(ed['date'])} : {ed['titre']}", flush=True)
        try:
            texte = texte_narration.generer(ed, args.modele, cle_or)
        except gp.PodcastError as e:
            print(f"ERREUR : {e}", file=sys.stderr)
            return 1
        nom = ed["date"] + args.suffixe
        print("\nTEXTE :\n\n" + texte + "\n", flush=True)
    else:
        chemin = Path(args.texte)
        texte = chemin.read_text(encoding="utf-8").strip()
        m = re.search(r"\d{4}-\d{2}-\d{2}", chemin.name)
        nom = (m.group(0) if m else chemin.stem) + args.suffixe
    modeles = tuple(x.strip() for x in args.tts_models.split(",") if x.strip())
    import texte_narration
    parts = texte_narration.parties(texte)
    print(f"{len(texte.split())} mots, {len(parts)} partie(s), voix {args.voix}", flush=True)
    parties_pcm = []
    for i, partie in enumerate(parts, 1):
        pcms = []
        for morceau in gp.decouper_texte(partie, limite=2600):
            print(f"Synthèse vocale partie {i}/{len(parts)} ({len(morceau)} caractères)…", flush=True)
            try:
                pcms.append(gp.synthese_unique(morceau, args.voix, modeles, cle))
            except gp.PodcastError as e:
                print(f"ERREUR : {e}", file=sys.stderr)
                return 1
        parties_pcm.append(gp.assembler(pcms, silence_s=0.5))
    ok, transcription = gp.verifier_debut(parties_pcm[0], texte_narration.parties(texte)[0], cle)
    if ok is None:
        print(f"ATTENTION : contrôle du début impossible ({transcription}) ; épisode gardé sans contrôle.", flush=True)
    elif not ok:
        print(f"ERREUR : le début de l'audio ne correspond pas au texte. Transcription : « {transcription} »", file=sys.stderr)
        return 1
    else:
        print(f"Contrôle du début : conforme (« {transcription[:90]}… »)", flush=True)
    import musique
    theme = musique.trouver_theme(gp.ROOT) if args.ouverture else None
    theme_pcm = musique.decoder_theme(theme) if theme else None
    if args.ouverture and theme is None:
        print("Pas de thème musical (podcast/musique/ouverture.mp3) : épisode sans musique.", flush=True)
    jingle = musique.jingle_depuis_theme(theme_pcm) if theme_pcm else None
    pcm = musique.assembler_parties(parties_pcm, jingle)
    if args.musique:
        pcm = musique.habiller(pcm)
    elif theme_pcm:
        print(f"Thème musical : {theme.name} ; {max(0, len(parts) - 1)} jingle(s) entre les parties", flush=True)
        pcm = musique.melanger_theme(theme_pcm, pcm)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    wav = out / f"{nom}.wav"
    gp.ecrire_wav(pcm, wav)
    duree = len(pcm) / 2 / gp.SAMPLE_RATE
    mp3 = out / f"{nom}.mp3"
    if gp.vers_mp3(wav, mp3):
        wav.unlink()
        print(f"OK : {mp3} ({duree / 60:.1f} min, {mp3.stat().st_size / 1e6:.1f} Mo)")
    else:
        print(f"OK : {wav} (ffmpeg absent, pas de MP3 ; {duree / 60:.1f} min)")
    (out / f"{nom}.txt").write_text(texte + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
