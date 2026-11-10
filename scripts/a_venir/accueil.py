#!/usr/bin/env python3
"""Encadré « Ce qui va arriver » de l'accueil : les 3 prochains rendez-vous de data/a-venir.json.

Remplace l'ancien bloc « Le dernier suivi ». Le bloc est placé juste après « La dernière édition »,
entre <!-- a-venir:start --> et <!-- a-venir:end -->. Il ne lève jamais d'exception (accueil jamais bloqué).
Usage : python3 scripts/a_venir/accueil.py [--check] [--date AAAA-MM-JJ]
Appelé aussi par scripts/edition/build_html.py (assemblage quotidien) et par signaux.yml.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_a_venir as g  # noqa: E402

RACINE = g.RACINE
INDEX = RACINE / "index.html"
START, END = "<!-- a-venir:start -->", "<!-- a-venir:end -->"
ANCIEN_START, ANCIEN_END = "<!-- dernier-suivi:start -->", "<!-- dernier-suivi:end -->"
CSS_START, CSS_END = "/* a-venir-accueil:start */", "/* a-venir-accueil:end */"
NB = 3


def qui_court(r):
    """« DGFiP (Direction…) » → « DGFiP » ; « Gouvernements …, sous médiation » → « Gouvernements … »."""
    return re.split(r" \(|, ", r["qui"])[0]


def carte(r, jour):
    texte, _ = g.reste(r, jour)
    return (f'<li class="avh-point"><a href="a-venir.html#rv-{g.esc(r["id"])}">'
            '<span class="avh-noeud" aria-hidden="true"></span>'
            f'<span class="avh-tuile" aria-hidden="true">{g.tuile(r)}</span>'
            f'<span class="avh-date"><svg viewBox="0 0 24 24" aria-hidden="true">{g.ICONES[r["domaine"]]}</svg>'
            f'<span class="avh-dom">{g.esc(r["domaine"])}</span>'
            f'<span class="avh-q">{g.esc(g.quand_court(r))}</span><i>{texte}</i></span>'
            f'<span class="avh-question">{g.nbsp(r["question"])}</span>'
            f'<span class="avh-qui">{g.esc(qui_court(r))} · {"officiel" if r["officiel"] else "non officiel"}</span></a></li>')


def bloc(jour=None, racine=RACINE):
    """Bloc HTML, ou "" au moindre problème ou s'il n'y a aucun rendez-vous à venir."""
    try:
        jour = jour or g.aujourdhui()
        prochains = g.a_venir(g.charger(racine), jour)[:NB]
        if not prochains:
            return ""
        return (f'{START}\n<section class="av-home" id="a-venir"><div class="wrap">\n<div class="avh-bande">\n'
                '<div class="avh-entete"><p class="section-label">À venir</p>'
                '<a class="avh-tout" href="a-venir.html">Tous les rendez-vous →</a></div>\n'
                '<ol class="avh-frise">' + "".join(carte(r, jour) for r in prochains) + '</ol>\n'
                '</div></div></section>\n' + END)
    except Exception as e:  # noqa: BLE001 — l'accueil ne doit jamais dépendre de ce bloc
        print(f"[a_venir] bloc ignoré : {e}", file=sys.stderr)
        return ""


def injecter(index_html, bloc_html):
    """Remplace le bloc (ou l'ancien « dernier suivi »), ou l'insère après « La dernière édition »."""
    sans = index_html
    for debut, fin in ((START, END), (ANCIEN_START, ANCIEN_END)):
        sans = re.sub(r"\n*[ \t]*" + re.escape(debut) + r".*?" + re.escape(fin) + r"\n*", "\n\n", sans, flags=re.S)
    if not bloc_html:
        return sans
    m = re.search(r'<section class="featured-article">.*?</section>', sans, re.S)
    if not m:
        return sans
    return sans[:m.end()] + "\n\n" + bloc_html + "\n\n" + sans[m.end():].lstrip("\n")


def injecter_css(index_html):
    """Place la feuille de style de l'encadré dans le <style> de l'accueil (les éditions la reprennent)."""
    css = (Path(__file__).resolve().parent / "accueil.css").read_text(encoding="utf-8")
    nouveau = f"  {CSS_START}\n{css.rstrip()}\n  {CSS_END}\n"
    motif = re.compile(r"[ \t]*" + re.escape(CSS_START) + r".*?" + re.escape(CSS_END) + r"\n", re.S)
    if motif.search(index_html):
        return motif.sub(lambda _: nouveau, index_html, count=1)
    i = index_html.index("</style>")
    return index_html[:i] + nouveau + index_html[i:]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="ne rien écrire ; code 1 si index.html n'est pas à jour")
    ap.add_argument("--date")
    args = ap.parse_args(argv)
    jour = date.fromisoformat(args.date) if args.date else None
    ancien = INDEX.read_text(encoding="utf-8")
    nouveau = injecter(injecter_css(ancien), bloc(jour))
    if nouveau == ancien:
        print("index.html : encadré « À venir » déjà à jour")
        return 0
    if args.check:
        print("index.html : encadré « À venir » à mettre à jour")
        return 1
    INDEX.write_text(nouveau, encoding="utf-8")
    print("index.html : encadré « À venir » mis à jour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
