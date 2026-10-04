#!/usr/bin/env python3
"""Lien « Ajouter Scénario à vos sources Google » bien en vue mais discret, en haut de chaque édition (demandé le 4 octobre 2026).

Placé juste sous la ligne « Partager : », en petit caractère mono et en gris, avec une étoile dorée. Pointe vers le lien officiel
https://google.com/preferences/source?q=lesscenarios.fr. Concerne l'édition du jour (FR et EN) et le modèle preview.html ; les
éditions passées restent figées. Le style (.source-google) est aussi ajouté aux gabarits (index.html, en/index.html, preview.html)
dont les futures éditions reprennent la feuille de style. Idempotent.
Usage : python3 scripts/seo/add_google_source_edition.py [--edition 2026-10-04] [--dry-run]
"""
import argparse
import re
from pathlib import Path

import add_google_source as g

ROOT = g.ROOT
LIEN = g.URL
ETOILE = ('<svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor" aria-hidden="true">'
          '<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"></path></svg>')


def bloc(en: bool) -> str:
    texte = "Add Scénario to your Google sources" if en else "Ajouter Scénario à vos sources Google"
    return (f'<p class="source-google"><a href="{LIEN}" target="_blank" rel="noopener noreferrer">{ETOILE} {texte}</a></p>')


CSS = """
  /* ---- Lien discret « Ajouter Scénario à vos sources Google » sous la ligne de partage (4 octobre 2026). ---- */
  .source-google{ margin: 2px 0 10px; font-family: "JetBrains Mono", monospace; font-size: 0.7rem; letter-spacing: 0.04em; }
  .source-google a{ color: var(--paper-dim); text-decoration: none; border-bottom: 1px dotted var(--hairline); }
  .source-google a:hover{ color: var(--paper); border-bottom-color: var(--paper); }
  .source-google svg{ color: var(--gold, #c9a24a); vertical-align: -1px; margin-right: 3px; }
  @media print{ .source-google{ display: none; } }
"""
FIN_SHARE = re.compile(r'(<p class="share-inline">.*?</p>)', re.S)


def ajouter_hero(html: str, en: bool) -> str:
    if "source-google" in html.split("</style>", 1)[-1]:
        return html
    return FIN_SHARE.sub(lambda m: m.group(1) + "\n    " + bloc(en), html, count=1)


def ajouter_css(html: str) -> str:
    if ".source-google{" in html:
        return html
    return html.replace("</style>", CSS + "</style>", 1)


def cibles(edition: str | None):
    """(chemin, hero ?, EN ?) : hero + CSS pour l'édition du jour et le modèle ; CSS seul pour les gabarits de la feuille de style."""
    liste = [(ROOT / "preview.html", True, False), (ROOT / "index.html", False, False), (ROOT / "en" / "index.html", False, True)]
    if edition:
        liste += [(ROOT / "archives" / f"{edition}.html", True, False), (ROOT / "en" / "archives" / f"{edition}.html", True, True)]
    return [c for c in liste if c[0].exists()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    for chemin, hero, en in cibles(args.edition):
        html = chemin.read_text(encoding="utf-8")
        nouveau = ajouter_css(html)
        if hero:
            nouveau = ajouter_hero(nouveau, en)
        if nouveau != html:
            n += 1
            print(("à modifier : " if args.dry_run else "modifié : ") + chemin.relative_to(ROOT).as_posix())
            if not args.dry_run:
                chemin.write_text(nouveau, encoding="utf-8")
    print(f"{n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
