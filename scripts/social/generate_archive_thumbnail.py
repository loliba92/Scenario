#!/usr/bin/env python3
"""
Génère la vignette carrée compressée d'une édition pour la liste
archives.html (`.entry-thumb`).

Source de l'image, dans cet ordre — jamais de nouvelle recherche Pexels,
uniquement des images déjà validées par un humain (même principe que
fetch_topic_image.py/routine-pub-prompt.md) :
1. assets/social/topic-images/{date}.jpg — la vraie photo du sujet du
   jour, quand elle existe (choisie en session lors de la rédaction).
2. À défaut, assets/social/pub-photos/{registre}.jpg — la banque de
   secours pré-validée, un paysage par registre (voir credits.json du
   même dossier). `culture-francaise`/`culture-internationale` (tags
   historiques, fusionnés en `culture` le 12 août — voir docs/tags.md)
   pointent tous les deux vers `culture.jpg`.

Recadrage centré en carré (cover), redimensionné à --size px (défaut
144 — 2x un affichage 72px pour rester net sur écran retina), export
JPEG qualité 72 : suffisant pour une vignette de liste, un fichier de
quelques Ko au lieu des centaines de Ko/plusieurs Mo de la source.

Usage :
    python3 scripts/social/generate_archive_thumbnail.py --date 2026-08-14 --registre sciences
    python3 scripts/social/generate_archive_thumbnail.py --date 2026-08-06 --registre sport --force

Écrit assets/social/archive-thumbs/{date}.jpg. N'écrase pas un fichier
existant sauf --force (le backfill initial peut tourner plusieurs fois
sans regénérer ce qui est déjà fait).
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
TOPIC_IMAGES = ROOT / "assets/social/topic-images"
PUB_PHOTOS = ROOT / "assets/social/pub-photos"
OUT_DIR = ROOT / "assets/social/archive-thumbs"

# Tags historiques (docs/tags.md) qui n'ont plus de photo dédiée dans la
# banque de secours depuis la fusion du 12 août — retombent sur culture.jpg.
REGISTRE_ALIASES = {
    "culture-francaise": "culture",
    "culture-internationale": "culture",
}

VALID_REGISTRES = {
    "geopolitique", "carte-blanche", "actualite-francaise",
    "economie-mondiale", "sciences", "culture", "sport",
}


def resolve_source(date: str, registre: str) -> tuple[Path, str]:
    """Retourne (chemin_source, origine) où origine est 'topic-image' ou
    'pub-photos' — utile pour le résumé affiché en fin de script."""
    topic_path = TOPIC_IMAGES / f"{date}.jpg"
    if topic_path.exists():
        return topic_path, "topic-image"

    slug = REGISTRE_ALIASES.get(registre, registre)
    if slug not in VALID_REGISTRES:
        raise SystemExit(
            f"Registre inconnu « {registre} » (alias résolu « {slug} ») — "
            f"ni topic-image ni banque de secours pour ce registre. "
            f"Registres valides : {sorted(VALID_REGISTRES)}"
        )
    fallback_path = PUB_PHOTOS / f"{slug}.jpg"
    if not fallback_path.exists():
        raise SystemExit(f"Photo de secours introuvable : {fallback_path}")
    return fallback_path, f"pub-photos/{slug}.jpg"


def make_square_thumb(src: Path, dest: Path, size: int) -> None:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)  # respecte l'orientation EXIF des photos telephone/appareil
        im = im.convert("RGB")
        cropped = ImageOps.fit(im, (size, size), method=Image.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(dest, "JPEG", quality=72, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", required=True, help="AAAA-MM-JJ de l'édition")
    parser.add_argument("--registre", required=True, help="registre du jour (voir data-tag dans archives.html)")
    parser.add_argument("--size", type=int, default=144, help="côté de la vignette en px (défaut 144)")
    parser.add_argument("--force", action="store_true", help="régénérer même si le fichier existe déjà")
    args = parser.parse_args()

    dest = OUT_DIR / f"{args.date}.jpg"
    if dest.exists() and not args.force:
        print(f"OK (déjà présent, --force pour régénérer) : {dest.relative_to(ROOT)}")
        return

    src, origin = resolve_source(args.date, args.registre)
    make_square_thumb(src, dest, args.size)
    kb = dest.stat().st_size / 1024
    print(f"OK {args.date} <- {origin} ({src.name}) -> {dest.relative_to(ROOT)} ({kb:.0f} Ko)")


if __name__ == "__main__":
    main()
