#!/usr/bin/env python3
"""Icône « source préférée Google » (étoile) dans la ligne de partage, en haut de chaque édition (demandé le 4 octobre 2026).

Première version : une ligne de texte sous « Partager : » — jugée trop grande, trop bavarde, sans discrétion ni beauté. Remplacée par
une simple étoile dorée dans un rond, identique aux icônes de partage ; l'info-bulle (et l'étiquette pour lecteurs d'écran) dit
« Ajouter Scénario à vos sources Google ». Lien officiel : https://google.com/preferences/source?q=lesscenarios.fr.
Concerne l'édition du jour (FR et EN) et le modèle preview.html ; les éditions passées restent figées. Le script retire aussi la
première version. Idempotent. Usage : python3 scripts/seo/add_google_source_edition.py [--edition 2026-10-04] [--dry-run]
"""
import argparse
import re

import add_google_source as g

ROOT = g.ROOT
LIEN = g.URL


def icone(en: bool) -> str:
    texte = "Add Scénario to your Google sources" if en else "Ajouter Scénario à vos sources Google"
    return (f'<a href="{LIEN}" id="share-google" target="_blank" rel="noopener noreferrer" aria-label="{texte}" title="{texte}">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5l2.5 5.4 5.9.7-4.4 4 1.2 5.8L12 16.5l-5.2 2.9 1.2-5.8-4.4-4 5.9-.7z"/></svg></a>')


ANCIEN_PARAGRAPHE = re.compile(r'\n[ \t]*<p class="source-google">.*?</p>', re.S)
ANCIEN_CSS = re.compile(r'\n  /\* ---- Lien discret « Ajouter Scénario à vos sources Google ».*?@media print\{ \.source-google\{ display: none; \} \}\n', re.S)
FIN_SHARE = re.compile(r'(<p class="share-inline">.*?)(\n\s*</p>)', re.S)


def nettoyer(html: str) -> str:
    return ANCIEN_CSS.sub("\n", ANCIEN_PARAGRAPHE.sub("", html))


def ajouter_hero(html: str, en: bool) -> str:
    html = nettoyer(html)
    if 'id="share-google"' in html:
        return html
    return FIN_SHARE.sub(lambda m: m.group(1) + "\n      " + icone(en) + m.group(2), html, count=1)


def cibles(edition: str | None):
    liste = [(ROOT / "preview.html", False)]
    if edition:
        liste += [(ROOT / "archives" / f"{edition}.html", False), (ROOT / "en" / "archives" / f"{edition}.html", True)]
    return [c for c in liste if c[0].exists()]


def pages_a_nettoyer():
    return [ROOT / "index.html", ROOT / "en" / "index.html"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    for chemin, en in cibles(args.edition):
        html = chemin.read_text(encoding="utf-8")
        nouveau = ajouter_hero(html, en)
        if nouveau != html:
            n += 1
            print(("à modifier : " if args.dry_run else "modifié : ") + chemin.relative_to(ROOT).as_posix())
            if not args.dry_run:
                chemin.write_text(nouveau, encoding="utf-8")
    for chemin in pages_a_nettoyer():     # gabarits de feuille de style : on retire seulement l'ancien style
        if chemin.exists():
            html = chemin.read_text(encoding="utf-8")
            nouveau = ANCIEN_CSS.sub("\n", html)
            if nouveau != html:
                n += 1
                print(("à nettoyer : " if args.dry_run else "nettoyé : ") + chemin.relative_to(ROOT).as_posix())
                if not args.dry_run:
                    chemin.write_text(nouveau, encoding="utf-8")
    print(f"{n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
