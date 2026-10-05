#!/usr/bin/env python3
"""Construit podcast.xml (flux RSS lu par Spotify) à partir de data/podcast-episodes.json.

Chaque épisode : date, titre, description, url (fichier MP3), taille en octets, durée en secondes.
Les fichiers MP3 ne sont pas dans le dépôt (trop lourds) : ils sont dans les Releases GitHub.

Usage :
  build_feed.py --ajouter 2026-10-03 --url https://… --taille 12345678 --duree 1380 --titre "…" --description "…"
  build_feed.py            # régénère seulement podcast.xml
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent.parent
EPISODES = ROOT / "data" / "podcast-episodes.json"
DIR_IMAGES = ROOT / "podcast" / "episodes"                 # pochettes d'épisode publiées : podcast/episodes/AAAA-MM-JJ.jpg
DIR_PHOTOS = ROOT / "assets" / "social" / "topic-images"   # image carrée de chaque édition (1080 px)
FLUX = ROOT / "podcast.xml"
SITE = "https://lesscenarios.fr"
EMAIL = "contact@lesscenarios.fr"  # adresse publique du flux : Spotify y envoie le code de vérification
TITRE = "Scénario — le podcast"
DESCRIPTION = (
    "Chaque jour, une question d'actualité et trois évolutions possibles, racontées en quelques minutes. "
    "Épisodes lus par une voix de synthèse (voix artificielle), à partir de l'édition publiée sur lesscenarios.fr. "
    "Rien n'est écrit à l'avance."
)


def charger():
    if EPISODES.exists():
        return json.loads(EPISODES.read_text(encoding="utf-8"))
    return []


def preparer_image(date_iso, dir_images=None, dir_photos=None):
    """Pochette de l'épisode : l'image carrée de l'édition, mise à 1400 x 1400 px (minimum de Spotify), JPEG de moins
    de 500 Ko. Retourne le chemin du fichier, ou None s'il n'y a pas d'image à utiliser."""
    dir_images = Path(dir_images or DIR_IMAGES)
    dir_photos = Path(dir_photos or DIR_PHOTOS)
    cible = dir_images / f"{date_iso}.jpg"
    if cible.exists():
        return cible
    source = dir_photos / f"{date_iso}.jpg"
    if not source.exists():
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(source).convert("RGB")
    c = min(im.size)  # recadrage carré centré si l'image ne l'est pas
    im = im.crop(((im.width - c) // 2, (im.height - c) // 2, (im.width - c) // 2 + c, (im.height - c) // 2 + c))
    im = im.resize((1400, 1400), Image.LANCZOS)
    dir_images.mkdir(parents=True, exist_ok=True)
    for qualite in (88, 82, 76, 70):
        im.save(cible, "JPEG", quality=qualite, optimize=True)
        if cible.stat().st_size <= 500_000:
            break
    return cible


def duree(s):
    s = int(s)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def rfc822(date_iso):
    d = datetime.strptime(date_iso, "%Y-%m-%d").replace(hour=7, tzinfo=timezone.utc)
    return format_datetime(d)


def construire(episodes, email="", dir_images=None):
    eps = sorted(episodes, key=lambda e: e["date"], reverse=True)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
           'xmlns:content="http://purl.org/rss/1.0/modules/content/">',
           "  <channel>",
           f"    <title>{escape(TITRE)}</title>",
           f"    <link>{SITE}/</link>",
           "    <language>fr</language>",
           f"    <description>{escape(DESCRIPTION)}</description>",
           "    <itunes:author>Scénario</itunes:author>",
           f"    <itunes:summary>{escape(DESCRIPTION)}</itunes:summary>",
           "    <itunes:explicit>false</itunes:explicit>",
           "    <itunes:type>episodic</itunes:type>",
           f'    <itunes:image href="{SITE}/podcast/cover.jpg"/>',
           '    <itunes:category text="News"/>']
    if email:
        out += ["    <itunes:owner>", "      <itunes:name>Scénario</itunes:name>",
                f"      <itunes:email>{escape(email)}</itunes:email>", "    </itunes:owner>"]
    dir_images = Path(dir_images or DIR_IMAGES)
    for e in eps:
        lien = f"{SITE}/archives/{e['date']}.html"
        out += ["    <item>",
                f"      <title>{escape(e['titre'])}</title>",
                f"      <link>{lien}</link>",
                f'      <guid isPermaLink="false">scenario-podcast-{e["date"]}</guid>',
                f"      <pubDate>{rfc822(e['date'])}</pubDate>",
                f"      <description>{escape(e['description'])}</description>",
                f'      <enclosure url="{escape(e["url"])}" length="{int(e["taille"])}" type="audio/mpeg"/>',
                f"      <itunes:duration>{duree(e['duree'])}</itunes:duration>",
                "      <itunes:explicit>false</itunes:explicit>"]
        if (dir_images / f"{e['date']}.jpg").exists():
            out.append(f'      <itunes:image href="{SITE}/podcast/episodes/{e["date"]}.jpg"/>')
        out += ["    </item>"]
    out += ["  </channel>", "</rss>", ""]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ajouter", metavar="DATE")
    ap.add_argument("--url")
    ap.add_argument("--taille", type=int)
    ap.add_argument("--duree", type=int)
    ap.add_argument("--titre")
    ap.add_argument("--description", default="")
    ap.add_argument("--email", default=os.environ.get("PODCAST_OWNER_EMAIL") or EMAIL)
    args = ap.parse_args(argv)
    eps = charger()
    if args.ajouter:
        if not (args.url and args.taille and args.duree and args.titre):
            print("ERREUR : --url, --taille, --duree et --titre sont requis avec --ajouter", file=sys.stderr)
            return 1
        eps = [e for e in eps if e["date"] != args.ajouter]
        eps.append({"date": args.ajouter, "titre": args.titre, "description": args.description or args.titre,
                    "url": args.url, "taille": args.taille, "duree": args.duree})
        EPISODES.write_text(json.dumps(sorted(eps, key=lambda e: e["date"]), ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")
    for e in eps:
        preparer_image(e["date"])
    FLUX.write_text(construire(eps, args.email), encoding="utf-8")
    print(f"podcast.xml : {len(eps)} épisode(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
