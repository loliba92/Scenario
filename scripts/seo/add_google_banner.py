#!/usr/bin/env python3
"""Ajoute la balise <script defer src=".../assets/google-source-banner.js"> (bandeau « Scénario dans vos sources Google »).

Demandé le 4 octobre 2026. Mises à la suite de la balise de pwa-install.js : pages vivantes (accueil, archives, thèmes, suivis…),
gabarits (index.html, en/index.html, preview.html : les futures éditions reprennent leurs balises) et édition du jour indiquée par
--edition. Les éditions passées restent figées. Idempotent. Usage : python3 scripts/seo/add_google_banner.py [--edition 2026-10-04] [--dry-run]
"""
import argparse
import re

import add_spotify_follow as sp

ROOT = sp.ROOT
TAG = re.compile(r'<script\b[^>]*\bsrc="((?:\.\./)*)assets/pwa-install\.js"[^>]*></script>')


def ajouter(html: str) -> str:
    if "google-source-banner" in html:
        return html
    return TAG.sub(lambda m: m.group(0) + f'\n<script src="{m.group(1)}assets/google-source-banner.js" defer></script>',
                   html, count=1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition")
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
