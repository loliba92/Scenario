#!/usr/bin/env python3
"""Ajoute le bouton Spotify dans les sections « Nous suivre » (à la suite du bouton Telegram).

Demandé le 4 octobre 2026. Les éditions passées restent figées (« on ne change que l'actuel et les futurs ») :
sont traitées les pages vivantes (accueil, archives.html, thèmes, suivis, contact…) et les pages de l'édition du jour
indiquée par --edition. Idempotent. Usage : python3 scripts/seo/add_spotify_follow.py [--edition 2026-10-04] [--dry-run]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL = "https://open.spotify.com/show/1eycE00I2egdNO50oqeDFQ"
BOUTON = ('<a class="follow-btn" href="' + URL + '" target="_blank" rel="noopener noreferrer">'
          '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle>'
          '<path d="M6.8 9.4c3.6-1 7.4-.7 10.6 1"></path><path d="M7.4 12.6c3-.8 6-.5 8.6.9"></path>'
          '<path d="M8 15.6c2.4-.6 4.7-.4 6.6.7"></path></svg> Spotify</a>')
TELEGRAM = re.compile(r'<a\b[^>]*t\.me/scenario_fr[^>]*>.*?</a>', re.S)
FIGES = ("archives/", "en/archives/", "hebdo/", "en/hebdo/")


def pages(edition: str | None):
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "node_modules/", "_podcast-out/")):
            continue
        if rel.startswith(FIGES):
            if edition and rel in (f"archives/{edition}.html", f"en/archives/{edition}.html"):
                yield p
            continue
        yield p


def ajouter(html: str) -> str:
    if URL in html:
        return html
    return TELEGRAM.sub(lambda m: m.group(0) + "\n      " + BOUTON, html, count=1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", help="édition du jour (AAAA-MM-JJ) à traiter aussi")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    for p in pages(args.edition):
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
