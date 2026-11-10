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
CALENDRIERS = {"date_fixee", "date_limite", "periode_annoncee", "non_programme"}
ICONES = {
    "Géopolitique": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M5 7.5c2 1 4.3 1.5 7 1.5s5-.5 7-1.5M5 16.5c2-1 4.3-1.5 7-1.5s5 .5 7 1.5"/>',
    "Économie": '<path d="M4 4v16h16"/><path d="M8 15l3.5-4 3 2.5L20 7"/><path d="M16 7h4v4"/>',
    "Politique": '<path d="M3 9l9-5 9 5z"/><path d="M5.5 12v6M10 12v6M14 12v6M18.5 12v6M3 20.5h18"/>',
    "Technologie": '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 10.5h4v3h-4zM9.5 3.5v3.5M14.5 3.5v3.5M9.5 17v3.5M14.5 17v3.5M3.5 9.5H7M3.5 14.5H7M17 9.5h3.5M17 14.5h3.5"/>',
    "Sport": '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5.5a2.5 2.5 0 0 0 2.7 3.8M16 6h2.5a2.5 2.5 0 0 1-2.7 3.8"/><path d="M12 13v4M9 20h6M10 17h4"/>',
    "Culture": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M10 9l5 3-5 3z"/><path d="M7 5v14M17 5v14" opacity=".35"/>',
}
MAX_PASSES = 12
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
        if r.get("calendrier") not in CALENDRIERS:
            raise ValueError(f"calendrier inconnu pour {r['id']} : {r.get('calendrier')}")
        for champ in ("qui", "nature"):
            if not str(r.get(champ, "")).strip():
                raise ValueError(f"{champ} manquant pour {r['id']}")
        if not isinstance(r.get("officiel"), bool):
            raise ValueError(f"officiel doit être vrai ou faux pour {r['id']}")
        if "resultat" in r:
            verifier_resultat(r)
    return donnees["rendez_vous"]


STATUTS = {"arrive": "S'est produit", "pas_arrive": "Ne s'est pas produit"}
SCENARIOS = {"favorable": "Favorable", "stable": "Stable", "degrade": "Dégradé"}


def verifier_resultat(r):
    """Un résultat exige : statut, date, réponse, au moins une source (lien http), scénario (ou null)."""
    x = r["resultat"]
    if x.get("statut") not in STATUTS:
        raise ValueError(f"resultat.statut inconnu pour {r['id']}")
    date.fromisoformat(x["date"])
    if not str(x.get("reponse", "")).strip():
        raise ValueError(f"resultat.reponse manquante pour {r['id']}")
    if x.get("scenario") is not None and x["scenario"] not in SCENARIOS:
        raise ValueError(f"resultat.scenario inconnu pour {r['id']}")
    if not [s for s in x.get("sources", []) if re.match(r"^https?://", str(s.get("url", "")))]:
        raise ValueError(f"resultat.sources : au moins un lien http est exigé pour {r['id']}")
    for c in x.get("chiffres", []):
        if not (str(c.get("libelle", "")).strip() and str(c.get("valeur", "")).strip()):
            raise ValueError(f"resultat.chiffres incomplet pour {r['id']}")


def passes(rendez_vous, jour):
    """(à vérifier, résolus) : date dépassée sans résultat ; résultat connu (le plus récent d'abord)."""
    a_verifier = sorted((r for r in rendez_vous if "resultat" not in r and date.fromisoformat(r["date"]) < jour),
                        key=lambda r: r["date"])
    resolus = sorted((r for r in rendez_vous if "resultat" in r),
                     key=lambda r: r["resultat"]["date"], reverse=True)
    return a_verifier, resolus


def a_venir(rendez_vous, jour):
    """Rendez-vous dont la date limite n'est pas passée, triés par date."""
    return sorted((r for r in rendez_vous if "resultat" not in r and date.fromisoformat(r["date"]) >= jour),
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


def date_longue(r):
    d = date.fromisoformat(r["date"])
    return f"{d.day}{'er' if d.day == 1 else ''} {MOIS[d.month - 1]} {d.year}"


def texte_calendrier(r):
    """Dit si la date est fixée, annoncée, ou seulement une échéance de surveillance."""
    c = r["calendrier"]
    if c == "date_fixee":
        return f"Date fixée : {date_longue(r)}"
    if c == "date_limite":
        return f"Pas de date fixée, avant le {date_longue(r)}"
    if c == "periode_annoncee":
        q = texte_quand(r)
        return f"Période annoncée : {q[0].lower() + q[1:]}"
    return f"Non programmé, surveillé jusqu'au {date_longue(r)}"


def fiche(r):
    chip = ('<span class="off oui">Officiel</span>' if r["officiel"] else '<span class="off non">Non officiel</span>')
    return ('<dl class="fiche">'
            f'<dt>Qui</dt><dd>{esc(r["qui"])}</dd>'
            f'<dt>Nature</dt><dd>{chip}{esc(r["nature"])}</dd>'
            f'<dt>Calendrier</dt><dd>{esc(texte_calendrier(r))}</dd></dl>')


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


def scenarios_edition(racine, iso):
    """{'favorable': (titre, pct), …} lus dans archives/AAAA-MM-JJ.html, ou {} si illisible."""
    f = racine / "archives" / f"{iso}.html"
    if not f.exists():
        return {}
    out = {}
    for m in re.finditer(r'<article class="card" data-kind="(favorable|stable|degrade)">(.*?)</article>',
                         f.read_text(encoding="utf-8"), re.S):
        pct = re.search(r'data-pct="(\d+)"', m.group(2))
        h3 = re.search(r"<h3[^>]*>(.*?)</h3>", m.group(2), re.S)
        if pct and h3:
            out[m.group(1)] = (html.unescape(re.sub(r"<[^>]+>", "", h3.group(1))).strip(), int(pct.group(1)))
    return out


def tuile_passee(r):
    d = date.fromisoformat(r["resultat"]["date"])
    return (f'<div class="tuile fait" aria-hidden="true"><span class="haut">{MOIS_COURT[d.month - 1]}</span>'
            f'<span class="gros sans-bas">{d.day}</span></div>')


def bloc_scenario(r, racine):
    x = r["resultat"]
    k = x.get("scenario")
    if not k:
        return '<p class="scen neutre">Cette réponse ne tranche pas entre les trois scénarios de l\'édition.</p>'
    eds = [i for i in r["editions"] if scenarios_edition(racine, i).get(k)]
    mot = {"favorable": "vert", "stable": "bleu", "degrade": "orange"}[k]
    if not eds:
        return (f'<p class="scen c-{k}"><b>{SCENARIOS[k]}</b> ({mot}) : la réponse correspond à notre scénario '
                f'« {SCENARIOS[k].lower()} ».</p>')
    iso = eds[0]
    titre, pct = scenarios_edition(racine, iso)[k]
    d = date.fromisoformat(iso)
    return (f'<p class="scen c-{k}"><b>{SCENARIOS[k]}</b> ({mot}) : la réponse correspond à notre scénario '
            f'« {esc(titre)} », annoncé à {pct}&nbsp;% dans l\'édition du {d.day} {MOIS[d.month - 1]}.</p>')


def carte_passee(r, i, racine):
    x = r["resultat"]
    k = x.get("scenario") or "neutre"
    d = date.fromisoformat(x["date"])
    h = f'<article class="signal passe" id="rv-{esc(r["id"])}" style="--i:{i}">{tuile_passee(r)}<div class="carte c-{k}">'
    h += (f'<div class="entete"><span class="pastille"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONES[r["domaine"]]}</svg>'
          f'{esc(r["domaine"])}</span><span class="statut {x["statut"]}">{STATUTS[x["statut"]]} le {d.day} {MOIS[d.month - 1]}</span></div>')
    h += f'<h2>{nbsp(r["question"])}</h2>'
    h += ('<dl class="fiche">' f'<dt>Qui</dt><dd>{esc(r["qui"])}</dd>'
          f'<dt>Nature</dt><dd>{"<span class=\"off oui\">Officiel</span>" if r["officiel"] else "<span class=\"off non\">Non officiel</span>"}{esc(r["nature"])}</dd></dl>')
    h += f'<div class="reponse"><b>La réponse</b><p>{esc(x["reponse"])}</p>'
    if x.get("chiffres"):
        h += '<ul class="chiffres">' + "".join(
            f'<li><span>{esc(c["libelle"])}</span><b>{esc(c["valeur"])}</b></li>' for c in x["chiffres"]) + "</ul>"
    h += "</div>" + bloc_scenario(r, racine)
    srcs = [s for s in x["sources"] if re.match(r"^https?://", str(s.get("url", "")))]
    h += ('<ul class="eds src"><b>Sources</b>' + "".join(
        f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer" target="_blank"><span class="t">{esc(s.get("titre") or s["url"])}</span></a></li>'
        for s in srcs) + "</ul>")
    eds = [(iso, titre_edition(racine, iso)) for iso in r["editions"]]
    eds = [(iso, e) for iso, e in eds if e]
    if eds:
        h += '<ul class="eds"><b>' + ("Éditions concernées" if len(eds) > 1 else "Édition concernée") + "</b>"
        for iso, (tt, dd) in eds:
            h += f'<li><a href="archives/{iso}.html"><span class="t">{esc(tt)}<span class="d">— {esc(dd)}</span></span></a></li>'
        h += "</ul>"
    return h + "</div></article>"


def carte_a_verifier(r, i, jour, racine):
    """Date dépassée, pas encore de résultat : carte sobre, sans décompte."""
    return carte(r, i, jour, racine, verifier=True)


def nbsp(t):
    """Espace insécable avant « ? » ; traits d'union insécables (« est-il », « va-t-il », « week-end »)."""
    s = esc(t).replace(" ?", "&nbsp;?").replace("week-end", "week&#8209;end")
    return re.sub(r"(?<=\w)-(t-)?(il|ils|elle|elles|on)\b",
                  lambda m: "&#8209;" + ("t&#8209;" if m.group(1) else "") + m.group(2), s)


def carte(r, i, jour, racine, verifier=False):
    texte_reste, pct = reste(r, jour)
    eds = [(iso, titre_edition(racine, iso)) for iso in r["editions"]]
    eds = [(iso, e) for iso, e in eds if e]
    h = f'<article class="signal" id="rv-{esc(r["id"])}" style="--i:{i}">{tuile(r)}<div class="carte">'
    droite = ('<span class="statut verif">Date passée : réponse en cours de vérification</span>' if verifier else
              f'<span class="jauge"><span class="piste" aria-hidden="true"><i style="width:{pct}%"></i></span>'
              f'<b>{texte_reste}</b></span>')
    h += (f'<div class="entete"><span class="pastille"><svg viewBox="0 0 24 24" aria-hidden="true">'
          f'{ICONES[r["domaine"]]}</svg>{esc(r["domaine"])}</span>{droite}</div>')
    h += (f'<h2><span class="sr">{esc(texte_quand(r))} : </span>{nbsp(r["question"])}</h2>'
          f'{fiche(r)}<p class="comm">{esc(r["commentaire"])}</p>')
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
         'du plus proche au plus lointain. Une fois la réponse connue, le résultat reste affiché plus bas.</p></div></section>\n')
    h += '<section class="body-section av"><div class="wrap">'
    prochains = a_venir(rendez_vous, jour)
    a_verifier, resolus = passes(rendez_vous, jour)
    if not prochains:
        h += '<div class="vide">Aucun rendez-vous à venir pour le moment.</div>'
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
        h += "</div>"
    if a_verifier or resolus:
        h += ('<section class="passes" id="deja-arrives"><p class="section-label">Déjà arrivés</p>'
              '<p class="legende">Couleur de la réponse, selon nos scénarios : '
              '<span class="c-favorable">vert, favorable</span> · <span class="c-stable">bleu, stable</span> · '
              '<span class="c-degrade">orange, dégradé</span>.</p><div class="tl tl-passe">')
        n = 0
        for r in a_verifier:
            h += carte_a_verifier(r, n, jour, racine)
            n += 1
        for r in resolus[:MAX_PASSES]:
            h += carte_passee(r, n, racine)
            n += 1
        h += "</div></section>"
    h += ('<p class="pied">Ces rendez-vous sont des repères, pas des prévisions. '
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
