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
FLUX = ROOT / "podcast.xml"
SITE = "https://lesscenarios.fr"
EMAIL = "contact@lesscenarios.fr"  # adresse publique du flux : Spotify y envoie le code de vérification
TITRE = "Scénario — le podcast"
DESCRIPTION = (
    "Chaque jour, l'actualité clé décryptée en trois scénarios chiffrés, racontée en dialogue. "
    "Épisodes lus par deux voix de synthèse (voix artificielles, annoncées au début de chaque épisode), "
    "à partir de l'édition publiée sur lesscenarios.fr."
)


def charger():
    if EPISODES.exists():
        return json.loads(EPISODES.read_text(encoding="utf-8"))
    return []


def duree(s):
    s = int(s)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def rfc822(date_iso):
    d = datetime.strptime(date_iso, "%Y-%m-%d").replace(hour=7, tzinfo=timezone.utc)
    return format_datetime(d)


def construire(episodes, email=""):
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
                "      <itunes:explicit>false</itunes:explicit>",
                "    </item>"]
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
    FLUX.write_text(construire(eps, args.email), encoding="utf-8")
    print(f"podcast.xml : {len(eps)} épisode(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
