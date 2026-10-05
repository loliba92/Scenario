#!/usr/bin/env python3
"""Ajoute dans l'en-tête, à côté du cadenas « Accès privé », une petite icône Spotify (écouter le podcast).

Demandé le 5 octobre 2026. Les éditions passées restent figées : sont traitées les pages vivantes et l'édition du jour
indiquée par --edition (même règle que add_spotify_follow.py). Les futures éditions héritent d'index.html. Idempotent.
Usage : python3 scripts/seo/add_spotify_masthead.py [--edition 2026-10-05] [--dry-run]
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from add_spotify_follow import ROOT, URL, pages  # noqa: E402

BOUTON = ('<a aria-label="Écouter sur Spotify" class="masthead-notif-btn" href="' + URL + '" target="_blank" '
          'rel="noopener noreferrer" title="Écouter sur Spotify"><svg aria-hidden="true" fill="none" height="16" '
          'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.7" viewbox="0 0 24 24" '
          'width="16"><circle cx="12" cy="12" r="9.5"></circle><path d="M7 9.6c3.4-1 7-.7 10 1"></path>'
          '<path d="M7.6 12.7c2.9-.8 5.7-.5 8.1.9"></path><path d="M8.2 15.5c2.2-.6 4.4-.4 6.2.7"></path></svg></a>\n')
CIBLE = re.compile(r'(<span aria-hidden="true" class="masthead-divider"></span>\n)(<a aria-label="Accès privé")')


def ajouter(html: str) -> str:
    if "Écouter sur Spotify" in html:
        return html
    return CIBLE.sub(lambda m: BOUTON + m.group(1) + m.group(2), html, count=1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    for p in pages(args.edition):
        html = p.read_text(encoding="utf-8")
        nouveau = ajouter(html)
        if nouveau != html:
            n += 1
            if not args.dry_run:
                p.write_text(nouveau, encoding="utf-8")
    print(f"{n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
