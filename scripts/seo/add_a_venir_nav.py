#!/usr/bin/env python3
"""Ajoute le lien « À venir » (→ a-venir.html) au menu du haut, après « Archives ».

Pages vivantes + gabarit (index.html : les futures éditions reprennent le menu) ; les éditions passées restent figées,
la version anglaise n'est pas concernée. Idempotent.
Usage : python3 scripts/seo/add_a_venir_nav.py [--edition 2026-11-10] [--dry-run]
"""
import argparse
import re

import add_spotify_follow as sp

ROOT = sp.ROOT
NAV = re.compile(r'<nav class="topnav".*?</nav>', re.S)
ARCHIVES = re.compile(r'<a href="((?:\.\./)*)archives\.html"[^>]*>.*?</a>', re.S)
ICONE = ('<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.7" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="5.5" width="16" height="14" rx="2"/>'
         '<path d="M4 10h16M8.5 3.5v4M15.5 3.5v4"/></svg>')


def ajouter(html: str) -> str:
    def dans_nav(nav: re.Match) -> str:
        bloc = nav.group(0)
        if "a-venir.html" in bloc:
            return bloc
        return ARCHIVES.sub(
            lambda m: m.group(0) + f'\n<a href="{m.group(1)}a-venir.html">{ICONE} À venir</a>', bloc, count=1)
    return NAV.sub(dans_nav, html, count=1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    for p in sp.pages(args.edition):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(("en/", "test/")) or rel == "a-venir.html":
            continue
        html = p.read_text(encoding="utf-8")
        nouveau = ajouter(html)
        if nouveau != html:
            n += 1
            print(("à modifier : " if args.dry_run else "modifié : ") + rel)
            if not args.dry_run:
                p.write_text(nouveau, encoding="utf-8")
    print(f"{n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
