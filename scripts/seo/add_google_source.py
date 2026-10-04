#!/usr/bin/env python3
"""Ajoute le bouton « Source préférée Google » dans les sections « Nous suivre » (à la suite du bouton Spotify).

Lien officiel documenté par Google Search Central (« Preferred sources ») : https://google.com/preferences/source?q=<domaine>.
Le lecteur arrive sur son écran de préférences Google, où il ajoute lesscenarios.fr à ses sources : nos articles remontent
alors plus souvent dans « À la une » de Google Actualités et de la recherche. Demandé le 4 octobre 2026.
Mêmes règles que add_spotify_follow.py : pages vivantes et édition du jour seulement, jamais les éditions passées. Idempotent.
Usage : python3 scripts/seo/add_google_source.py [--edition 2026-10-04] [--dry-run]
"""
import argparse
import re
from pathlib import Path

import add_spotify_follow as sp

ROOT = sp.ROOT
URL = "https://google.com/preferences/source?q=lesscenarios.fr"
BOUTON = ('<a class="follow-btn" href="' + URL + '" target="_blank" rel="noopener noreferrer">'
          '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"></path></svg> Source préférée Google</a>')
SPOTIFY = re.compile(r'<a\b[^>]*' + re.escape(sp.URL) + r'[^>]*>.*?</a>', re.S)


def ajouter(html: str) -> str:
    if URL in html:
        return html
    return SPOTIFY.sub(lambda m: m.group(0) + "\n      " + BOUTON, html, count=1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", help="édition du jour (AAAA-MM-JJ) à traiter aussi")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    for p in sp.pages(args.edition):
        html = p.read_text(encoding="utf-8")
        nouveau = ajouter(html)
        if nouveau != html:
            n += 1
            print(("à modifier : " if args.dry_run else "modifié : ") + p.relative_to(ROOT).as_posix())
            if not args.dry_run:
                p.write_text(nouveau, encoding="utf-8")
    print(f"{n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
