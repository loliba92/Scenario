#!/usr/bin/env python3
"""Simplifie le menu du haut (FR) : 9 entrées → Accueil · Éditions · Glossaire · Le projet · Nous suivre + loupe.

Demandé le 4 octobre 2026. « Matières » et « Recherche » sont atteintes depuis la page Éditions (archives.html) ; Newsletter et
Soutenir rejoignent le bloc « Nous suivre », Contact rejoint le pied de page. Pages vivantes + gabarit (index.html) + édition du jour
via --edition ; éditions passées figées, version anglaise non concernée. Idempotent.
Usage : python3 scripts/seo/simplify_nav.py [--edition 2026-10-04] [--dry-run]
"""
import argparse
import re

import add_spotify_follow as sp

ROOT = sp.ROOT
NAV = re.compile(r'<nav class="topnav".*?</nav>', re.S)
LINK = re.compile(r'<a href="([^"]*)"([^>]*)>(.*?)</a>', re.S)
SVG = re.compile(r'<svg.*?</svg>', re.S)
LOUPE = ('<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.7" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/>'
         '<line x1="16" y1="16" x2="20.5" y2="20.5"/></svg>')
KEPT = [("index.html", "Accueil"), ("archives.html", "Éditions"), ("glossaire.html", "Glossaire"),
        ("le-projet.html", "Le projet"), ("#nous-suivre", "Nous suivre")]
ICON_FALLBACK = {}


def nouveau_menu(nav: str) -> str:
    if "Éditions" in nav and 'aria-label="Recherche"' in nav:
        return nav
    icons, current = {}, set()
    for href, attrs, inner in LINK.findall(nav):
        base = re.sub(r'^(?:\.\./)+', '', href)
        m = SVG.search(inner)
        if m:
            icons[base] = m.group(0)
        if "aria-current" in attrs:
            current.add(base)
    prefix = re.search(r'<a href="((?:\.\./)*)index\.html"', nav)
    prefix = prefix.group(1) if prefix else ""
    head = nav[:nav.index(">") + 1]
    tail = '</nav>'
    wrap = re.search(r'<div class="wrap">', nav) is not None
    items = []
    for base, label in KEPT:
        href = base if base.startswith("#") else prefix + base
        cur = ' aria-current="page"' if base in current else ""
        icon = icons.get(base, "")
        items.append(f'<a href="{href}"{cur}>{icon} {label}</a>')
    cur = ' aria-current="page"' if "recherche.html" in current else ""
    items.append(f'<a href="{prefix}recherche.html" aria-label="Recherche" title="Recherche"{cur}>{LOUPE}</a>')
    body = "\n".join("    " + i for i in items)
    return f'{head}\n  <div class="wrap">\n{body}\n  </div>\n{tail}' if wrap else f'{head}\n{body}\n{tail}'


def follow(html: str) -> str:
    m = re.search(r'<div class="follow-block-row">\n', html)
    if not m or "newsletter.html" in html[m.start():m.start() + 600]:
        return html
    pre = re.search(r'href="((?:\.\./)*)mentions-legales\.html"', html)
    pre = pre.group(1) if pre else ""
    add = (f'      <a class="follow-btn" href="{pre}newsletter.html">Newsletter</a>\n'
           '      <a class="follow-btn" href="https://buymeacoffee.com/scenario" target="_blank" rel="noopener noreferrer">Soutenir</a>\n')
    return html[:m.end()] + add + html[m.end():]


def footer(html: str) -> str:
    m = re.search(r'(<div class="legal-links">\n?)(\s*)(<a href="((?:\.\./)*)mentions-legales\.html")', html)
    if not m or "contact.html" in html[m.start():m.start() + 500]:
        return html
    return html[:m.end(1)] + m.group(2) + f'<a href="{m.group(4)}contact.html">Contact</a>\n' + m.group(2) + html[m.start(3):]


def transformer(html: str) -> str:
    html = NAV.sub(lambda n: nouveau_menu(n.group(0)), html, count=1)
    return footer(follow(html))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    for p in sp.pages(args.edition):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("en/"):
            continue
        html = p.read_text(encoding="utf-8")
        nouveau = transformer(html)
        if nouveau != html:
            n += 1
            print(("à modifier : " if args.dry_run else "modifié : ") + rel)
            if not args.dry_run:
                p.write_text(nouveau, encoding="utf-8")
    print(f"{n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
