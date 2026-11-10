#!/usr/bin/env python3
"""Génère a-venir.html (« Ce qui va arriver ») à partir de data/a-venir.json.

Rendez-vous classés par date, sans probabilité. Une édition passée n'est jamais modifiée.
Usage : python3 scripts/a_venir/generate_a_venir.py [--date AAAA-MM-JJ] [--sortie fichier]
"""
import argparse
import html
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

RACINE = Path(__file__).resolve().parents[2]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
MOIS_COURT = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août",
              "sept.", "oct.", "nov.", "déc."]
PRECISIONS = {"jour", "limite", "fin_mois", "mois", "fin_annee"}
ICONES = {
    "Géopolitique": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M5 7.5c2 1 4.3 1.5 7 1.5s5-.5 7-1.5M5 16.5c2-1 4.3-1.5 7-1.5s5 .5 7 1.5"/>',
    "Économie": '<path d="M4 4v16h16"/><path d="M8 15l3.5-4 3 2.5L20 7"/><path d="M16 7h4v4"/>',
    "Politique": '<path d="M3 9l9-5 9 5z"/><path d="M5.5 12v6M10 12v6M14 12v6M18.5 12v6M3 20.5h18"/>',
    "Technologie": '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 10.5h4v3h-4zM9.5 3.5v3.5M14.5 3.5v3.5M9.5 17v3.5M14.5 17v3.5M3.5 9.5H7M3.5 14.5H7M17 9.5h3.5M17 14.5h3.5"/>',
    "Sport": '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5.5a2.5 2.5 0 0 0 2.7 3.8M16 6h2.5a2.5 2.5 0 0 1-2.7 3.8"/><path d="M12 13v4M9 20h6M10 17h4"/>',
    "Culture": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M10 9l5 3-5 3z"/><path d="M7 5v14M17 5v14" opacity=".35"/>',
}
TITRE = "Ce qui va arriver — les rendez-vous à surveiller — Scénario"
DESCRIPTION = ("Les rendez-vous à surveiller relevés dans nos éditions, du plus proche au plus lointain, "
               "avec les éditions concernées.")


def esc(t):
    return html.escape(str(t), quote=True)


def aujourdhui():
    return datetime.now(ZoneInfo("Europe/Paris")).date()


def charger(racine=RACINE):
    donnees = json.loads((racine / "data" / "a-venir.json").read_text(encoding="utf-8"))
    for r in donnees["rendez_vous"]:
        date.fromisoformat(r["date"])
        if r["precision"] not in PRECISIONS:
            raise ValueError(f"precision inconnue pour {r['id']} : {r['precision']}")
        if r["domaine"] not in ICONES:
            raise ValueError(f"domaine inconnu pour {r['id']} : {r['domaine']}")
    return donnees["rendez_vous"]


def a_venir(rendez_vous, jour):
    """Rendez-vous dont la date limite n'est pas passée, triés par date."""
    return sorted((r for r in rendez_vous if date.fromisoformat(r["date"]) >= jour),
                  key=lambda r: (r["date"], r["id"]))


def periode(d, jour):
    d = date.fromisoformat(d)
    if d.year == jour.year:
        return f"{MOIS[d.month - 1].capitalize()} {d.year}"
    return f"En {d.year}"


def texte_quand(r):
    d = date.fromisoformat(r["date"])
    p = r["precision"]
    if p == "jour":
        return f"{d.day} {MOIS[d.month - 1]}"
    if p == "limite":
        return f"D'ici le {d.day} {MOIS[d.month - 1]}"
    if p == "fin_mois":
        return f"Fin {MOIS[d.month - 1]}"
    if p == "fin_annee":
        return f"D'ici fin {d.year}"
    return f"{MOIS[d.month - 1].capitalize()} {d.year}"


def tuile(r):
    d = date.fromisoformat(r["date"])
    court = MOIS_COURT[d.month - 1].capitalize() if r["precision"] == "mois" else MOIS_COURT[d.month - 1]
    p = r["precision"]
    if p == "jour":
        haut, gros, bas, moy = court, str(d.day), "", False
    elif p == "limite":
        haut, gros, bas, moy = "D'ici le", str(d.day), court, False
    elif p == "fin_mois":
        haut, gros, bas, moy = "Fin", court, "", True
    elif p == "fin_annee":
        haut, gros, bas, moy = "D'ici fin", str(d.year), "", True
    else:
        haut, gros, bas, moy = str(d.year), court, "", True
    cls = "tuile" + ("" if p == "jour" else " flou")
    classes_gros = "gros" + (" moy" if moy else "") + ("" if bas else " sans-bas")
    return (f'<div class="{cls}" aria-hidden="true"><span class="haut">{esc(haut)}</span>'
            f'<span class="{classes_gros}">{esc(gros)}</span>'
            + (f'<span class="bas">{esc(bas)}</span>' if bas else "") + "</div>")


def reste(r, jour):
    j = (date.fromisoformat(r["date"]) - jour).days
    if j <= 0:
        return "aujourd'hui", 100
    pct = max(4, round((1 - min(j, 90) / 90) * 100))
    return f"dans {j} jour{'s' if j > 1 else ''}", pct


def titre_edition(racine, iso):
    """Titre (h1) et date lisible de l'édition archives/AAAA-MM-JJ.html, ou None si absente."""
    f = racine / "archives" / f"{iso}.html"
    if not f.exists():
        return None
    m = re.search(r"<h1[^>]*>(.*?)</h1>", f.read_text(encoding="utf-8"), re.S)
    if not m:
        return None
    titre = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    d = date.fromisoformat(iso)
    return titre, f"{d.day}{'er' if d.day == 1 else ''} {MOIS[d.month - 1]}"


def nbsp(t):
    """Espace insécable avant « ? » ; traits d'union insécables (« est-il », « va-t-il », « week-end »)."""
    s = esc(t).replace(" ?", "&nbsp;?").replace("week-end", "week&#8209;end")
    return re.sub(r"(?<=\w)-(t-)?(il|ils|elle|elles|on)\b",
                  lambda m: "&#8209;" + ("t&#8209;" if m.group(1) else "") + m.group(2), s)


def carte(r, i, jour, racine):
    texte_reste, pct = reste(r, jour)
    eds = [(iso, titre_edition(racine, iso)) for iso in r["editions"]]
    eds = [(iso, e) for iso, e in eds if e]
    h = f'<article class="signal" id="rv-{esc(r["id"])}" style="--i:{i}">{tuile(r)}<div class="carte">'
    h += (f'<div class="entete"><span class="pastille"><svg viewBox="0 0 24 24" aria-hidden="true">'
          f'{ICONES[r["domaine"]]}</svg>{esc(r["domaine"])}</span>'
          f'<span class="jauge"><span class="piste" aria-hidden="true"><i style="width:{pct}%"></i></span>'
          f'<b>{texte_reste}</b></span></div>')
    h += (f'<h2><span class="sr">{esc(texte_quand(r))} : </span>{nbsp(r["question"])}</h2>'
          f'<p class="comm">{esc(r["commentaire"])}</p>')
    if eds:
        h += f'<ul class="eds"><b>{"Éditions concernées" if len(eds) > 1 else "Édition concernée"}</b>'
        for iso, (t, d) in eds:
            h += (f'<li><a href="archives/{iso}.html"><span class="t">{esc(t)}'
                  f'<span class="d">— {esc(d)}</span></span></a></li>')
        h += "</ul>"
    return h + "</div></article>"


def contenu(rendez_vous, jour, racine=RACINE):
    h = ('<section class="hero contact-hero"><div class="wrap"><p class="eyebrow">À venir</p>'
         '<h1>Ce qui va arriver</h1><p class="dek">Les rendez-vous à surveiller, relevés dans nos éditions, '
         'du plus proche au plus lointain.</p></div></section>\n')
    h += '<section class="body-section av"><div class="wrap">'
    prochains = a_venir(rendez_vous, jour)
    if not prochains:
        h += '<div class="vide">Aucun rendez-vous à surveiller pour le moment.</div>'
    else:
        groupes, ordre = {}, []
        for r in prochains:
            p = periode(r["date"], jour)
            if p not in groupes:
                groupes[p] = []
                ordre.append(p)
            groupes[p].append(r)
        h += '<div class="tl">'
        n = 0
        for p in ordre:
            h += f'<section class="periode" aria-label="{esc(p)}"><p class="section-label">{esc(p)}</p>'
            for r in groupes[p]:
                h += carte(r, n, jour, racine)
                n += 1
            h += "</section>"
        h += ('</div><p class="pied">Ces rendez-vous sont des repères, pas des prévisions. '
              'Nous ne recalculons pas de probabilités ici : à chacun de se faire son idée.</p>')
    return h + "</div></section>"


def css():
    return (RACINE / "scripts" / "a_venir" / "a-venir.css").read_text(encoding="utf-8")


def page(rendez_vous, jour, racine=RACINE):
    gabarit = (RACINE / "scripts" / "a_venir" / "gabarit.html").read_text(encoding="utf-8")
    return (gabarit.replace("{{TITRE}}", esc(TITRE)).replace("{{DESCRIPTION}}", esc(DESCRIPTION))
            .replace("{{CSS}}", css()).replace("{{HERO_ET_CONTENU}}", contenu(rendez_vous, jour, racine)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date")
    p.add_argument("--sortie", default=str(RACINE / "a-venir.html"))
    a = p.parse_args()
    jour = date.fromisoformat(a.date) if a.date else aujourdhui()
    Path(a.sortie).write_text(page(charger(), jour), encoding="utf-8")
    print(f"a-venir.html écrit ({len(a_venir(charger(), jour))} rendez-vous à venir)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
