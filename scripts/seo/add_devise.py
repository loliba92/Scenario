#!/usr/bin/env python3
"""Ajoute la devise « Rien n'est écrit à l'avance. » au pied de page des pages vivantes.

Demandé le 5 octobre 2026 : la phrase conclut chaque épisode du podcast et devient l'adage du site. Ligne en italique doré juste
avant les mentions légales ; le CSS est ajouté à chaque page (elles ont chacune leur <style>). Gabarit (index.html : les futures
éditions reprennent le CSS) et édition du jour via --edition ; éditions passées figées ; version anglaise non concernée. Idempotent.
Usage : python3 scripts/seo/add_devise.py [--edition 2026-10-05] [--dry-run]
"""
import argparse

import add_spotify_follow as sp

ROOT = sp.ROOT
DEVISE = "Rien n'est écrit à l'avance."
LIGNE = f'<p class="devise-footer">{DEVISE}</p>\n'
MARQUE = '<div class="legal-links">'
CSS = '''
  /* ---- Devise du site (5 oct. 2026) ---- */
  .devise-footer{
    flex: 1 0 100%; margin: 0 0 14px;
    font-family: "Fraunces", Georgia, serif; font-style: italic; font-size: 1.05rem;
    color: var(--gold, #cf9d4c);
  }
'''


def ajouter(html: str) -> str:
    if "devise-footer" in html or MARQUE not in html:
        return html
    html = html.replace(MARQUE, LIGNE + MARQUE, 1)
    return html.replace("</style>", CSS + "</style>", 1) if "</style>" in html else html


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
