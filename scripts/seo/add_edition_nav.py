#!/usr/bin/env python3
"""Ajoute en bas des éditions les liens « Édition précédente / Édition suivante ».

Demandé par le propriétaire le 10 octobre 2026 : Search Console montre que Google connaît beaucoup d'éditions sans
les avoir lues (« détectée, actuellement non indexée »). Une édition ne renvoyait qu'à 3 autres éditions, sans ordre
chronologique. Ces liens créent un chemin continu d'une édition à l'autre : les éditions déjà lues par Google
mènent à leurs voisines, lues ou non.

Les éditions sont chaînées par date (archives/AAAA-MM-JJ.html, version française seulement). Le bloc est placé
avant « Reste connecté » et délimité par des marqueurs : le script est idempotent et ne touche à rien d'autre.

Utilisation :
  python3 scripts/seo/add_edition_nav.py                      # éditions ayant déjà le bloc + les deux plus récentes
  python3 scripts/seo/add_edition_nav.py --dates 2026-09-28,… # amorçage : ces éditions (+ les deux plus récentes)
  python3 scripts/seo/add_edition_nav.py --dry-run
Lancé par post-edition.yml après la publication, sans jamais la bloquer.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})\.html$")
DEBUT, FIN = "<!-- edition-nav -->", "<!-- /edition-nav -->"
BLOC = re.compile(re.escape(DEBUT) + r".*?" + re.escape(FIN) + r"\n*", re.S)
CSS_ID = 'id="edition-nav-css"'
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]

CSS = f"""<style {CSS_ID}>
  .edition-nav{{ padding: 28px 0 8px; }}
  .edition-nav-row{{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px; }}
  .edition-nav-link{{ display: block; padding: 14px 16px; border: 1px solid var(--border, rgba(128,128,128,.3)); border-radius: 10px; text-decoration: none; color: inherit; }}
  .edition-nav-link:hover{{ border-color: var(--gold); }}
  .edition-nav-link.next{{ text-align: right; grid-column: 2; }}
  .edition-nav-dir{{ display: block; font-size: .8rem; color: var(--gold); margin-bottom: 4px; }}
  .edition-nav-title{{ display: block; font-weight: 600; line-height: 1.35; }}
  @media (max-width: 600px){{
    .edition-nav-row{{ grid-template-columns: 1fr; }}
    .edition-nav-link.next{{ grid-column: auto; text-align: left; }}
  }}
  @media print{{ .edition-nav{{ display: none !important; }} }}
</style>
"""


def court(date):
    return f"{int(date[8:10])} {MOIS[int(date[5:7]) - 1]}"


def titre(path):
    m = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8"), re.S)
    t = m.group(1).strip() if m else path.stem
    t = re.sub(r"\s+[—-]\s+Scénario\s*$", "", t)
    t = re.sub(r"[ \u00a0\u202f]+([?!:;»])", r"&nbsp;\1", t)  # ponctuation haute collée au mot (pas de « ? » seul)
    return re.sub(r"(«)[ \u00a0\u202f]+", r"\1&nbsp;", t)


def lien(classe, rel, sens, date, dossier):
    fleche = "→" if rel == "next" else "←"
    sens = f"{sens} · {court(date)} {fleche}" if rel == "next" else f"{fleche} {sens} · {court(date)}"
    return (f'      <a class="edition-nav-link {classe}" rel="{rel}" href="{date}.html">\n'
            f'        <span class="edition-nav-dir">{sens}</span>\n'
            f'        <span class="edition-nav-title">{titre(dossier / (date + ".html"))}</span>\n'
            f'      </a>\n')


def bloc(date, dates, dossier):
    i = dates.index(date)
    liens = ""
    if i > 0:
        liens += lien("prev", "prev", "Édition précédente", dates[i - 1], dossier)
    if i < len(dates) - 1:
        liens += lien("next", "next", "Édition suivante", dates[i + 1], dossier)
    if not liens:
        return ""
    return (f'{DEBUT}\n<nav class="edition-nav" aria-label="Autres éditions">\n  <div class="wrap">\n'
            f'    <p class="section-label">Autres éditions</p>\n    <div class="edition-nav-row">\n{liens}'
            f'    </div>\n  </div>\n</nav>\n{FIN}\n\n')


def appliquer(texte, date, dates, dossier):
    """Renvoie le texte avec le bloc à jour (ou inchangé si la page n'a pas la structure attendue)."""
    texte = BLOC.sub("", texte)
    html = bloc(date, dates, dossier)
    ancre = next((a for a in ('<section class="share-block"', "<footer") if a in texte), None)
    if not html or ancre is None:
        return texte
    texte = texte.replace(ancre, html + ancre, 1)
    if CSS_ID not in texte and "</head>" in texte:
        texte = texte.replace("</head>", CSS + "</head>", 1)
    return texte


def main(argv):
    dry = "--dry-run" in argv
    amorce = set()
    if "--dates" in argv:
        amorce = {d for d in argv[argv.index("--dates") + 1].split(",") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d)}
    dossier = ROOT / "archives"
    dates = sorted(m.group(1) for p in dossier.glob("*.html") if (m := DATED.match(p.name)))
    cibles = set(dates[-2:]) | (amorce & set(dates))
    cibles |= {d for d in dates if DEBUT in (dossier / f"{d}.html").read_text(encoding="utf-8")}
    changes = 0
    for d in sorted(cibles):
        chemin = dossier / f"{d}.html"
        ancien = chemin.read_text(encoding="utf-8")
        nouveau = appliquer(ancien, d, dates, dossier)
        if nouveau != ancien:
            changes += 1
            if not dry:
                chemin.write_text(nouveau, encoding="utf-8")
    print(f"{changes} édition(s) {'à mettre à jour' if dry else 'mise(s) à jour'} (liens précédente/suivante).")


if __name__ == "__main__":
    main(sys.argv[1:])
