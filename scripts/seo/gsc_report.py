#!/usr/bin/env python3
"""Analyse d'expert Search Console : data/gsc/*.json  ->  constats priorisés  ->  rapport.md + seo.html.

Sorties (écrites par `.github/workflows/gsc.yml` après `gsc_sync.py`) :
  - `data/gsc/rapport.md` : texte lu par l'agent `gsc-expert`.
  - `seo.html`            : page privée (noindex, interdite aux robots) pour le propriétaire : problèmes à résoudre,
                            ce qui fonctionne, ce qui ne fonctionne pas.
Aucune dépendance, aucun réseau.

    python3 scripts/seo/gsc_report.py            # écrit les deux fichiers
    python3 scripts/seo/gsc_report.py --stdout   # affiche le rapport texte seulement

Principes de lecture (détail dans .claude/agents/gsc-expert.md) :
  - les chiffres de Google ont ~3 jours de retard : on ne juge jamais une page de moins de 3 jours ;
  - « Google ne reconnaît pas cette URL » sur une page de plus de 7 jours = problème de découverte ;
  - le compteur « indexées » des plans du site est peu fiable : l'inspection page par page fait foi.
"""
from __future__ import annotations

import argparse
import html as _h
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "gsc"
TEMPLATE = Path(__file__).with_name("gsc_page_template.html")
PUBLIC = "https://lesscenarios.fr"
BRAND = re.compile(r"sc[eé]nario|lesscenarios", re.I)

# État d'indexation (texte renvoyé par Google) -> (famille, explication, action recommandée)
ETATS = [
    (r"envoy[ée]e et index[ée]e|submitted and indexed|^index[ée]e|indexed", "ok", "Indexée.", ""),
    (r"ne reconna[iî]t pas|unknown to google", "inconnue",
     "Google n'a pas encore découvert ou traité ces adresses.",
     "Demander l'indexation dans Search Console, vérifier un lien interne depuis une page déjà indexée, patienter si la page a moins de 7 jours."),
    (r"d[ée]tect[ée]e.*non index|discovered.*not indexed", "decouverte",
     "Google connaît l'adresse mais ne l'a pas encore explorée ou retenue.",
     "Renforcer les liens internes vers la page, enrichir son contenu, demander l'indexation."),
    (r"explor[ée]e.*non index|crawled.*not indexed", "exploree",
     "Google a lu la page et a décidé de ne pas l'indexer (qualité ou doublon perçu).",
     "Apporter de la valeur propre (analyse, chiffres, sources) et vérifier les doublons."),
    (r"canonique|canonical|doublon|duplicate", "canonique",
     "Google retient une autre adresse que celle déclarée.",
     "Vérifier la balise canonique et les variantes d'adresse (index.html, http/https, barre finale)."),
    (r"noindex|bloqu[ée]e|robots", "bloquee",
     "La page est exclue par une balise noindex ou par robots.txt.",
     "Vérifier que ce blocage est voulu ; sinon le retirer."),
    (r"404|introuvable|not found", "introuvable", "Adresse introuvable (404).", "Corriger le lien ou rediriger l'adresse."),
    (r"redirection|redirect", "redirection", "L'adresse redirige vers une autre.", "Normal si voulu ; sinon corriger les liens."),
]


def classify(etat, verdict=None):
    t = (etat or "").lower()
    for pat, fam, expl, action in ETATS:
        if re.search(pat, t):
            return fam, expl, action
    if verdict == "PASS":
        return "ok", "Indexée.", ""
    return "autre", f"État non reconnu : {etat or 'inconnu'}.", "Inspecter la page dans Search Console."


def load(dir_, name):
    p = Path(dir_) / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def page_age(url, today):
    m = re.search(r"/archives/(\d{4})-(\d{2})-(\d{2})\.html$", url)
    return (today - date(int(m.group(1)), int(m.group(2)), int(m.group(3)))).days if m else None


def fr(x):
    """Nombre à la française (virgule décimale)."""
    return str(x).replace(".", ",")


def n_(n, sg, pl):
    """Accord simple : n_(1, 'page', 'pages') -> '1 page'."""
    return f"{n} {sg if n < 2 else pl}"


def pct(ratio):
    """0.014 -> « 1,4 »."""
    return fr(f"{ratio * 100:.1f}")


def chemin(url):
    return url.replace(PUBLIC, "") or "/"


def tendance(history):
    days = sorted(history or {})
    if len(days) < 8:
        return None
    half = min(14, len(days) // 2)
    cur, prev = days[-half:], days[-2 * half:-half]
    agg = lambda ds: {"clics": sum(history[d].get("clicks", 0) for d in ds),
                      "impressions": sum(history[d].get("impressions", 0) for d in ds)}
    return {"jours": half, "recent": agg(cur), "precedent": agg(prev), "fin": cur[-1]}


# ------------------------------------------------------------------ contrôles sur le dépôt
def _meta(text, key):
    for tag in re.findall(r"<meta\b[^>]*>", text):
        if re.search(r'(?:name|property)="%s"' % re.escape(key), tag):
            m = re.search(r'content="([^"]*)"', tag)
            return _h.unescape(m.group(1)) if m else ""
    return None


def controles_depot(root=ROOT):
    """Santé technique mesurée directement sur les pages du dépôt (sans réseau)."""
    res = {}
    sitemap = (root / "sitemap.xml").read_text(encoding="utf-8") if (root / "sitemap.xml").exists() else ""
    for nom, dossier, prefixe in (("fr", root / "archives", "archives"), ("en", root / "en" / "archives", "en/archives")):
        pages = sorted(dossier.glob("2026-*.html")) if dossier.exists() else []
        c = {"pages": len(pages), "titre_long": 0, "titre_coupe": 0, "desc_hors_norme": 0, "sans_h1": 0,
             "sans_canonique": 0, "hors_plan": 0}
        for f in pages:
            t = f.read_text(encoding="utf-8")
            titre = re.search(r"<title>(.*?)</title>", t, re.S)
            titre = _h.unescape(titre.group(1)) if titre else ""
            desc = _meta(t, "description") or ""
            c["titre_long"] += len(titre) > 82
            c["titre_coupe"] += "…" in titre
            c["desc_hors_norme"] += not 100 <= len(desc) <= 160 or "…" in desc
            c["sans_h1"] += len(re.findall(r"<h1\b", t)) != 1
            c["sans_canonique"] += 'rel="canonical"' not in t
            c["hors_plan"] += f"{PUBLIC}/{prefixe}/{f.name}" not in sitemap
        res[nom] = c
    return res


# ------------------------------------------------------------------ analyse
def analyser(dir_=DATA, today=None, root=ROOT):
    today = today or date.today()
    summary, indexation, sitemaps, history = (load(dir_, n) for n in
                                              ("summary.json", "indexation.json", "sitemaps.json", "history.json"))
    A = {"date": today.isoformat(), "donnees": bool(summary), "critiques": [], "importants": [], "surveiller": [],
         "fonctionne": [], "ne_fonctionne_pas": [], "kpi": {}, "requetes": [], "pages": [], "indexation": [],
         "plans": [], "controles": {}, "verdict": ("moyen", "Aucune donnée Google pour l'instant.")}
    if not summary:
        A["critiques"].append(("Aucune donnée Search Console.", "Installer le secret GSC_SERVICE_ACCOUNT_JSON puis lancer le workflow « Sync Search Console » (docs/gsc-installation.md).", None, None))
        A["verdict"] = ("critique", "Pas de données : la connexion à Search Console n'est pas en place.")
        return A

    maj = date.fromisoformat(summary.get("mis_a_jour", today.isoformat()))
    A["site"], A["periode"], A["synchro"] = summary.get("site"), summary.get("periode", {}), maj.isoformat()
    if (today - maj).days > 3:
        A["critiques"].append((f"Les données ont {(today - maj).days} jours.", "La synchronisation quotidienne ne tourne plus : ouvrir l'onglet Actions de GitHub, workflow « Sync Search Console ».", None, None))

    t = summary["totaux"]
    tr = tendance(history)
    A["kpi"] = {"clics": t["clicks"], "impressions": t["impressions"], "ctr": t["ctr"], "position": t["position"], "tendance": tr}
    if t["clicks"] < 10:
        A["ne_fonctionne_pas"].append(f"Presque aucune visite venue de Google : {n_(t['clicks'], 'clic', 'clics')} en 28 jours.")
    if t["impressions"] and t["position"] and t["position"] < 12 and t["clicks"] / t["impressions"] < 0.02:
        A["importants"].append((f"Le site apparaît (position moyenne {fr(t['position'])}) mais est très peu cliqué ({pct(t['ctr'])} %).",
                                "Retravailler les titres et descriptions des pages les plus vues.",
                                "seo-content", "Proposer de nouveaux titres (≤ 59 caractères) et descriptions (100–160) plus incitatifs pour les pages les plus vues, dans le ton sobre de Scénario ; ne rien promettre."))
    if tr:
        r, p = tr["recent"], tr["precedent"]
        if p["impressions"] and r["impressions"] > p["impressions"] * 1.15:
            A["fonctionne"].append(f"Visibilité en hausse : {r['impressions']} impressions sur les {tr['jours']} derniers jours contre {p['impressions']} avant.")
        elif p["impressions"] and r["impressions"] < p["impressions"] * 0.7:
            A["ne_fonctionne_pas"].append(f"Visibilité en baisse : {r['impressions']} impressions sur {tr['jours']} jours contre {p['impressions']} avant.")
    if t["position"] and t["position"] < 10 and t["impressions"] >= 50:
        A["fonctionne"].append(f"Google affiche le site en position moyenne {fr(t['position'])} (première page) sur {t['impressions']} impressions.")

    qs = summary.get("requetes", [])
    A["requetes"] = sorted(qs, key=lambda q: (-q["clicks"], -q["impressions"]))[:8]
    marque = [q for q in qs if BRAND.search(q["requete"])]
    A["kpi"]["requetes"], A["kpi"]["requetes_marque"] = len(qs), len(marque)
    if len(qs) < 20:
        A["surveiller"].append((f"Seulement {len(qs)} requêtes enregistrées.", "Trop peu pour piloter par mots-clés : viser d'abord l'indexation des éditions.",
                                "seo-cluster", "Proposer des axes thématiques (matières, sujets récurrents) et un maillage interne pour élargir les requêtes, sans produire de pages en série."))
    pages = summary.get("pages", [])
    A["pages"] = sorted(pages, key=lambda p: (-p["impressions"], -p["clicks"]))[:8]
    sans_clic = [p for p in pages if p["impressions"] >= 10 and p["clicks"] == 0 and p["position"] <= 10]
    if sans_clic:
        A["surveiller"].append(("Pages en première page de Google sans aucun clic : " + ", ".join(f"`{chemin(p['page'])}`" for p in sans_clic[:5]) + ".",
                                "Titre ou description à rendre plus incitatif.",
                                "seo-content", "Réécrire titre et description de ces pages (liste dans le rapport), puis vérifier la cohérence avec le contenu."))
    if any(p["page"].rstrip("/").endswith("/index.html") for p in pages):
        A["surveiller"].append(("L'adresse `/index.html` apparaît dans Google en plus de `/`.", "Vérifier la balise canonique de l'accueil.",
                                "seo-technical", "Vérifier la canonique de l'accueil, les redirections et les liens internes qui pointent vers /index.html."))

    # indexation
    rows = (indexation or {}).get("pages") or []
    fam = {}
    for r in rows:
        if r.get("erreur"):
            f, e, a = "erreur", f"Inspection impossible : {r['erreur']}", "Vérifier les droits du compte de service dans Search Console."
        else:
            f, e, a = classify(r.get("etat"), r.get("verdict"))
        age = page_age(r["url"], today)
        fam.setdefault(f, []).append({"url": r["url"], "age": age, "etat": r.get("etat"), "exploration": (r.get("derniere_exploration") or "")[:10]})
        A["indexation"].append({"url": r["url"], "famille": f, "age": age, "etat": r.get("etat"), "exploration": (r.get("derniere_exploration") or "")[:10]})
    ok = len(fam.get("ok", []))
    A["kpi"]["inspectees"], A["kpi"]["indexees"] = len(rows), ok
    if rows:
        cles = [x for x in fam.get("ok", []) if x["age"] is None]
        if cles:
            A["fonctionne"].append(f"{n_(len(cles), 'page principale indexée', 'pages principales indexées')} : " + ", ".join(f"`{chemin(x['url'])}`" for x in cles[:6]) + ".")
        eds = [x for x in fam.get("ok", []) if x["age"] is not None]
        if eds:
            A["fonctionne"].append(f"{n_(len(eds), 'édition indexée', 'éditions indexées')} par Google.")
    inconnues = fam.get("inconnue", [])
    vieilles = [x for x in inconnues if (x["age"] or 0) > 7]
    A["kpi"]["inconnues"] = len(inconnues)
    A["kpi"]["inconnues_anciennes"] = len(vieilles)
    if vieilles:
        _, e, a = classify("Google ne reconnaît pas cette URL")
        A["critiques"].append((f"{n_(len(vieilles), 'édition de plus de 7 jours est inconnue', 'éditions de plus de 7 jours sont inconnues')} de Google (sur {len(rows)} pages inspectées).", a,
                               "seo-technical + seo-sitemap",
                               "Diagnostiquer pourquoi ces éditions restent inconnues de Google : profondeur de clics depuis l'accueil, liens internes vers les éditions récentes, structure et dates du plan du site, robots.txt, vitesse. Rendre un plan correctif chiffré, classé par impact."))
        A["ne_fonctionne_pas"].append(f"Découverte trop lente : {n_(len(vieilles), 'édition publiée depuis plus d’une semaine n’est pas connue', 'éditions publiées depuis plus d’une semaine ne sont pas connues')} de Google.")
    for f in ("decouverte", "exploree", "canonique", "bloquee", "introuvable", "erreur"):
        items = fam.get(f, [])
        if items:
            _, e, a = classify({"decouverte": "détectée non indexée", "exploree": "explorée non indexée", "canonique": "canonique",
                                "bloquee": "noindex", "introuvable": "404", "erreur": ""}[f])
            cle = [x for x in items if x["age"] is None]
            msg = f"{n_(len(items), 'page', 'pages')} : {e.rstrip('.')} (" + ", ".join(f"`{chemin(x['url'])}`" for x in items[:4]) + ")."
            ag, mi = (("seo-content", "Comprendre pourquoi Google retient ou écarte ces pages (profondeur, unicité, qualité perçue) et proposer des améliorations de contenu et de liens internes.")
                      if f in ("decouverte", "exploree") else ("seo-technical", "Diagnostiquer et corriger la cause (canonique, blocage, redirection, adresse introuvable)."))
            (A["importants"] if cle else A["surveiller"]).append((msg, a, ag, mi))
            if cle:
                A["ne_fonctionne_pas"].append(f"{'Page principale non indexée' if len(cle) == 1 else 'Pages principales non indexées'} : " + ", ".join(f"`{chemin(x['url'])}`" for x in cle[:4]) + ".")

    # plans du site
    for s in (sitemaps or {}).get("plans", []):
        nom = s["plan"].replace(PUBLIC, "")
        envoyees = sum(int(c.get("submitted", 0)) for c in (s.get("contenus") or []))
        A["plans"].append({"plan": nom, "envoyees": envoyees, "erreurs": s.get("erreurs"), "avertissements": s.get("avertissements"),
                           "lecture": (s.get("derniere_lecture") or "")[:10], "erreur_api": s.get("erreur")})
        if s.get("erreur"):
            A["importants"].append((f"Le plan du site `{nom}` n'a pas pu être lu : {s['erreur'][:100]}", "Vérifier le droit « Complète » du compte de service.", "seo-sitemap", "Valider le plan du site et diagnostiquer l'erreur de lecture."))
        elif str(s.get("erreurs", "0")) not in ("0", "None"):
            A["critiques"].append((f"Le plan du site `{nom}` signale {s.get('erreurs')} erreur(s).", "Ouvrir « Sitemaps » dans Search Console.", "seo-sitemap", "Valider le plan du site, lister les adresses en erreur et proposer la correction."))
        else:
            A["fonctionne"].append(f"Plan du site `{nom}` lu par Google sans erreur ({envoyees} adresses envoyées).")

    # contrôles sur le dépôt
    ctl = controles_depot(root)
    A["controles"] = ctl
    for nom, c in ctl.items():
        if not c["pages"]:
            continue
        pb = {k: v for k, v in c.items() if k != "pages" and v}
        lib = "français" if nom == "fr" else "anglais"
        if not pb:
            A["fonctionne"].append(f"Balises des {c['pages']} éditions en {lib} conformes : titres sans coupure, descriptions de 100 à 160 caractères, un seul titre principal, canonique présente, toutes dans le plan du site.")
        else:
            noms = {"titre_long": "titres trop longs", "titre_coupe": "titres coupés", "desc_hors_norme": "descriptions hors norme",
                    "sans_h1": "pages sans titre principal unique", "sans_canonique": "pages sans canonique", "hors_plan": "pages absentes du plan du site"}
            A["importants"].append((f"Éditions en {lib} : " + ", ".join(f"{v} {noms[k]}" for k, v in pb.items()) + ".", "Corriger via les générateurs (voir .claude/seo-routage.md).", None, "Correction directe dans les générateurs (generate_seo_head.py, translate_daily.py), puis régénération et tests."))

    # gestes que seul le propriétaire peut faire
    A["a_faire_par_vous"] = []
    if inconnues:
        A["a_faire_par_vous"].append("Dans Search Console, collez l'adresse de l'édition du jour dans la barre du haut, puis « Demander une indexation » (quota limité par jour) ; répétez pour les éditions inconnues les plus récentes.")
    if any(x["famille"] in ("decouverte", "exploree") and x["age"] is None for x in A["indexation"]):
        A["a_faire_par_vous"].append("Faites de même pour les pages principales « détectées, non indexées » (guide pédagogique, par exemple).")
    if A["importants"] or A["critiques"]:
        A["a_faire_par_vous"].append("Relisez les recommandations des agents avant de valider tout changement de titres ou de contenu.")

    # verdict
    if A["critiques"]:
        A["verdict"] = ("critique", A["critiques"][0][0] + " " + A["critiques"][0][1])
    elif A["importants"]:
        A["verdict"] = ("moyen", A["importants"][0][0])
    else:
        A["verdict"] = ("bon", "Rien d'anormal : poursuivre la surveillance quotidienne.")
    return A


# ------------------------------------------------------------------ rendu texte
def rendre_md(A):
    if not A["donnees"]:
        return "# Rapport Search Console\n\nAucune donnée Google : `data/gsc/summary.json` est absent (secret `GSC_SERVICE_ACCOUNT_JSON` non installé ou workflow jamais lancé).\n"
    k = A["kpi"]
    L = ["# Rapport Search Console", "",
         f"Site `{A['site']}` · données Google du {A['periode'].get('debut')} au {A['periode'].get('fin')} · synchronisé le {A['synchro']} (les chiffres de Google ont ~3 jours de retard).", "",
         f"**Verdict : {A['verdict'][0].upper()}** — {A['verdict'][1]}", "",
         "## Chiffres (28 jours)", "",
         f"- {k['clics']} clics, {k['impressions']} impressions, taux de clic {pct(k['ctr'])} %, position moyenne {fr(k['position'])}.",
         f"- Pages indexées : {k.get('indexees', 0)} sur {k.get('inspectees', 0)} inspectées ; éditions inconnues de Google : {k.get('inconnues', 0)} (dont {k.get('inconnues_anciennes', 0)} de plus de 7 jours).",
         f"- Requêtes : {k.get('requetes', 0)} (dont {k.get('requetes_marque', 0)} avec le nom du site)."]
    if k.get("tendance"):
        r, p = k["tendance"]["recent"], k["tendance"]["precedent"]
        L.append(f"- Tendance ({k['tendance']['jours']} jours, jusqu'au {k['tendance']['fin']}) : impressions {r['impressions']} contre {p['impressions']}, clics {r['clics']} contre {p['clics']}.")
    for titre, cle in (("À résoudre — critique", "critiques"), ("À résoudre — important", "importants"), ("À surveiller", "surveiller")):
        L += ["", f"## {titre}", ""]
        L += [f"- {c[0]} **Action** : {c[1]}" + (f" **Agent à envoyer** : {c[2]}." if c[2] else "") + (f" **Mission** : {c[3]}" if c[3] else "") for c in A[cle]] or ["- Rien."]
    for titre, cle in (("Ce qui fonctionne", "fonctionne"), ("Ce qui ne fonctionne pas", "ne_fonctionne_pas")):
        L += ["", f"## {titre}", ""] + ([f"- {m}" for m in A[cle]] or ["- Rien à signaler."])
    if A.get("a_faire_par_vous"):
        L += ["", "## Ce que seul le propriétaire peut faire", ""] + [f"- {x}" for x in A["a_faire_par_vous"]]
    L += ["", "## Requêtes principales", ""] + [f"- « {q['requete']} » : {q['clicks']} clic(s), {q['impressions']} impression(s), position {fr(q['position'])}" for q in A["requetes"]]
    L += ["", "## Pages les plus vues", ""] + [f"- `{chemin(p['page'])}` : {p['impressions']} impressions, {p['clicks']} clic(s), position {fr(p['position'])}" for p in A["pages"]]
    L += ["", "## Indexation page par page", ""]
    for r in A["indexation"]:
        L.append(f"- `{chemin(r['url'])}` : {r['famille']}" + (f" ({r['etat']})" if r["famille"] != "ok" and r["etat"] else "") + (f", publiée il y a {r['age']} j" if r["age"] is not None else ""))
    L += ["", "Le compteur « indexées » des plans du site n'est pas fiable : l'inspection page par page fait foi.", ""]
    return "\n".join(L)


# ------------------------------------------------------------------ rendu page
def _code(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", _h.escape(s))


def rendre_html(A, tpl=None):
    tpl = tpl or TEMPLATE.read_text(encoding="utf-8")
    e = _h.escape
    niveau, texte = A["verdict"]
    nom_niv = {"critique": "Critique", "moyen": "À améliorer", "bon": "Bon état"}[niveau]
    if not A["donnees"]:
        corps = f'''<section class="hero"><div class="wrap"><p class="eyebrow">Tableau de bord SEO</p><h1>Où en est le référencement ?</h1>
<p class="dek">{_code(texte)}</p></div></section>
<section class="block"><div class="wrap"><div class="verdict is-critique"><span class="verdict-tag">Critique</span><p>{_code(A['critiques'][0][1])}</p></div></div></section>'''
        return tpl.replace("{{CONTENT}}", corps)
    k = A["kpi"]

    def kpi(val, nom, note="", cls=""):
        return f'<div class="kpi {cls}"><div class="kpi-val">{e(str(val))}</div><div class="kpi-name">{e(nom)}</div>' + (f'<div class="kpi-note">{e(note)}</div>' if note else "") + "</div>"
    ins, idx = k.get("inspectees", 0), k.get("indexees", 0)
    tend = ""
    if k.get("tendance"):
        r, p = k["tendance"]["recent"], k["tendance"]["precedent"]
        tend = f"{r['impressions']} contre {p['impressions']} avant"
    kpis = "".join([
        kpi(k["clics"], "clics Google", "sur 28 jours", "is-bad" if k["clics"] < 10 else ""),
        kpi(k["impressions"], "impressions", tend),
        kpi(fr(f"{k['ctr'] * 100:.1f}") + " %", "taux de clic", "", "is-bad" if k["ctr"] < 0.02 else ""),
        kpi(fr(k["position"]), "position moyenne", "plus petit = mieux", "is-good" if k["position"] and k["position"] < 10 else ""),
        kpi(f"{idx} / {ins}", "pages indexées", "échantillon inspecté", "is-good" if ins and idx / ins > .7 else ("is-bad" if ins and idx / ins < .5 else "")),
        kpi(k.get("inconnues_anciennes", 0), "éditions inconnues", "publiées depuis plus de 7 jours", "is-bad" if k.get("inconnues_anciennes") else "is-good"),
    ])

    def todo(items, cls, nom):
        out = ""
        for c in items:
            m, a, ag, mi = (list(c) + [None, None])[:4]
            ligne_ag = (f'<p class="how"><strong>Agent à envoyer :</strong> <code>{e(ag)}</code>' + (f" — {_code(mi)}" if mi else "") + "</p>") if ag else (f'<p class="how"><strong>Mission :</strong> {_code(mi)}</p>' if mi else "")
            out += f'<div class="todo-item {cls}"><p class="todo-prio">{nom}</p><p>{_code(m)}</p><p class="how"><strong>Recommandation :</strong> {_code(a)}</p>{ligne_ag}</div>'
        return out
    a_faire = todo(A["critiques"], "p1", "Critique") + todo(A["importants"], "p2", "Important") + todo(A["surveiller"], "p3", "À surveiller")
    a_faire = a_faire or '<div class="todo-item"><p>Rien à résoudre pour le moment.</p></div>'

    def col(items, cls, titre):
        li = "".join(f"<li>{_code(m)}</li>" for m in items) or '<li class="empty">Rien à signaler.</li>'
        return f'<div class="col {cls}"><h3>{titre}</h3><ul>{li}</ul></div>'

    lib = {"ok": ("ok", "Indexée"), "inconnue": ("bad", "Inconnue de Google"), "decouverte": ("mid", "Détectée, non indexée"),
           "exploree": ("mid", "Explorée, non indexée"), "canonique": ("mid", "Canonique"), "bloquee": ("bad", "Bloquée"),
           "introuvable": ("bad", "Introuvable"), "redirection": ("mid", "Redirection"), "erreur": ("bad", "Erreur"), "autre": ("mid", "À vérifier")}
    ordre = {"inconnue": 0, "bloquee": 1, "introuvable": 1, "erreur": 1, "exploree": 2, "decouverte": 2, "canonique": 2, "autre": 3, "redirection": 3, "ok": 4}
    lignes = ""
    for r in sorted(A["indexation"], key=lambda r: (ordre.get(r["famille"], 3), r["url"])):
        cls, nom = lib.get(r["famille"], ("mid", r["famille"]))
        meta = (f"publiée il y a {r['age']} j" if r["age"] is not None else "page principale") + (f" · explorée le {r['exploration']}" if r["exploration"] else "")
        lignes += f'<li><span><span class="pill {cls}">{e(nom)}</span><span class="url">{e(chemin(r["url"]))}</span></span><span class="meta">{e(meta)}</span></li>'
    q = "".join(f'<li><span>« {e(x["requete"])} »</span><span class="meta">{x["clicks"]} clic(s) · {x["impressions"]} imp. · pos. {fr(x["position"])}</span></li>' for x in A["requetes"]) or '<li><span>Aucune requête.</span></li>'
    p = "".join(f'<li><span class="url">{e(chemin(x["page"]))}</span><span class="meta">{x["clicks"]} clic(s) · {x["impressions"]} imp. · pos. {fr(x["position"])}</span></li>' for x in A["pages"])
    plans = "".join(f'<li><span class="url">{e(s["plan"])}</span><span class="meta">{s["envoyees"]} adresses · {e(str(s["erreurs"]))} erreur(s) · lu le {e(s["lecture"] or "?")}</span></li>' for s in A["plans"]) or "<li><span>Aucun plan lu.</span></li>"
    ctl = ""
    for nom, c in A["controles"].items():
        if not c["pages"]:
            continue
        pb = sum(v for kk, v in c.items() if kk != "pages")
        ctl += f'<li><span><span class="pill {"ok" if not pb else "mid"}">{"Conforme" if not pb else str(pb) + " écart(s)"}</span>Éditions en {"français" if nom == "fr" else "anglais"} ({c["pages"]} pages)</span><span class="meta">titres, descriptions, titre principal, canonique, plan du site</span></li>'

    moi = ""
    if A.get("a_faire_par_vous"):
        moi = ('<section class="block"><div class="wrap"><p class="label">Votre part</p><h2>Ce que seul vous pouvez faire</h2><div class="todo">'
               + "".join(f'<div class="todo-item p2"><p class="todo-prio">À faire par vous</p><p>{e(x)}</p></div>' for x in A["a_faire_par_vous"]) + "</div></div></section>")
    corps = f'''<section class="hero"><div class="wrap">
<p class="eyebrow">Tableau de bord SEO</p><h1>Où en est le référencement ?</h1>
<p class="dek">Analyse automatique des données réelles de Google Search Console, mise à jour chaque jour : ce qui est critique, ce qui fonctionne et surtout ce qui ne fonctionne pas.</p>
<p class="stamp">Données Google du {e(str(A["periode"].get("debut")))} au {e(str(A["periode"].get("fin")))} · synchronisées le {e(A["synchro"])} · ~3 jours de retard côté Google</p>
</div></section>
<section class="block"><div class="wrap">
<p class="label">Verdict</p>
<div class="verdict is-{niveau}"><span class="verdict-tag">{nom_niv}</span><p>{_code(texte)}</p></div>
</div></section>
<section class="block"><div class="wrap"><p class="label">Chiffres</p><h2>28 derniers jours</h2><div class="kpis">{kpis}</div></div></section>
<section class="block"><div class="wrap"><p class="label">Priorités</p><h2>À résoudre, avec les recommandations</h2><div class="todo">{a_faire}</div></div></section>
{moi}
<section class="block"><div class="wrap"><p class="label">Bilan</p><h2>Ce qui marche, ce qui ne marche pas</h2>
<div class="duo">{col(A["fonctionne"], "", "Ce qui fonctionne")}{col(A["ne_fonctionne_pas"], "is-bad", "Ce qui ne fonctionne pas")}</div></div></section>
<section class="block"><div class="wrap"><p class="label">Indexation</p><h2>Page par page</h2><ul class="list">{lignes or "<li><span>Aucune inspection.</span></li>"}</ul></div></section>
<section class="block"><div class="wrap"><p class="label">Recherches</p><h2>Requêtes et pages vues</h2>
<ul class="list">{q}</ul><p style="margin-top:14px"></p><ul class="list">{p}</ul></div></section>
<section class="block"><div class="wrap"><p class="label">Santé technique</p><h2>Plans du site et balises</h2>
<ul class="list">{plans}{ctl}</ul>
<p style="margin-top:14px">Le compteur « indexées » des plans du site est peu fiable : l'inspection page par page ci-dessus fait foi.</p></div></section>'''
    return tpl.replace("{{CONTENT}}", corps)


def maj_dashboard(A, chemin_dash):
    """Met à jour la carte SEO du tableau de bord (entre les repères SEO-CARD) ; sans effet si les repères manquent."""
    p = Path(chemin_dash)
    if not p.exists():
        return False
    h = p.read_text(encoding="utf-8")
    m = re.search(r"(<!-- SEO-CARD:START -->)(.*?)(<!-- SEO-CARD:END -->)", h, re.S)
    if not m or not A["donnees"]:
        return False
    k, e = A["kpi"], _h.escape
    niveau, texte = A["verdict"]
    nom = {"critique": "Critique", "moyen": "À améliorer", "bon": "Bon état"}[niveau]
    n_prob = len(A["critiques"]) + len(A["importants"])
    carte = f"""
    <span class="chart-label" style="margin-top:24px; display:block;">Référencement Google (SEO)</span>
    <div class="kpi-grid">
      <a class="kpi-card kpi-card-seo kpi-card-wide is-{niveau}" href="seo.html">
        <p class="kpi-label">Tableau de bord SEO — {e(A['synchro'])}</p>
        <div class="kpi-value">{nom}</div>
        <p class="kpi-sub">{e(texte.replace('`', ''))[:230]}</p>
        <div class="kpi-breakdown kpi-breakdown-4col">
          <div class="kpi-breakdown-item"><span>Clics (28 j)</span><strong>{k['clics']}</strong></div>
          <div class="kpi-breakdown-item"><span>Impressions</span><strong>{k['impressions']}</strong></div>
          <div class="kpi-breakdown-item"><span>Pages indexées</span><strong>{k.get('indexees', 0)} / {k.get('inspectees', 0)}</strong></div>
          <div class="kpi-breakdown-item"><span>Problèmes à résoudre</span><strong>{n_prob}</strong></div>
        </div>
        <p class="kpi-go">Ouvrir l'analyse complète, les recommandations et les agents à envoyer →</p>
      </a>
    </div>
    """
    nouveau = h[:m.start(2)] + carte + h[m.end(2):]
    if nouveau != h:
        p.write_text(nouveau, encoding="utf-8")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=str(DATA))
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--page", default=str(ROOT / "seo.html"))
    ap.add_argument("--dashboard", default=str(ROOT / "dashboard.html"))
    args = ap.parse_args(argv)
    d = Path(args.dir)
    A = analyser(d)
    if args.stdout:
        print(rendre_md(A))
        return 0
    if not (d / "summary.json").exists():
        print("Aucune donnée Search Console : rapport et page non écrits.")
        return 0
    (d / "rapport.md").write_text(rendre_md(A), encoding="utf-8")
    Path(args.page).write_text(rendre_html(A), encoding="utf-8")
    maj_dashboard(A, args.dashboard)
    print(f"Écrits : {d / 'rapport.md'} et {args.page} — verdict : {A['verdict'][0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
