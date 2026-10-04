#!/usr/bin/env python3
"""Articles connexes : donner au modèle du brief TOUTES les éditions passées, et vérifier son choix.

Retour de l'éditeur (4 octobre 2026) : l'édition « GPS et Russie » proposait en articles connexes l'économie mondiale, le
Bab el-Mandeb et l'électricité, alors que l'édition du 23 septembre sur la menace hybride russe existait. Deux causes :
- la consigne (étape 2bis) limitait la recherche aux « 30 derniers jours » ;
- le modèle n'avait sous les yeux que les 20 dernières éditions (summarize_recent_archives, prévu pour l'anti-doublon).
Un classement lexical automatique a été essayé : trop de bruit (« France », « monde » ressortent partout, et « Russia » ≠ « Russie »),
donc le choix reste au modèle, mais avec la liste complète ; le code ne fait que vérifier le résultat.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARCHIVES_HTML_PATH = REPO_ROOT / "archives.html"
NB_CONNEXES = 3
QUESTION_MAX = 170


def _texte(s: str) -> str:
    return " ".join(html.unescape(s).replace("\xa0", " ").replace("❓", "").split())


def charger_archives(chemin: Path | None = None) -> list[dict]:
    """[{date, domaine, titre, question}] de toutes les éditions de archives.html (ordre du fichier : plus récente d'abord)."""
    texte = (chemin or ARCHIVES_HTML_PATH).read_text(encoding="utf-8")
    ligne = re.compile(
        r'<tr data-domain="([^"]*)"[^>]*data-date="([^"]*)"[^>]*>.*?'
        r'<a href="archives/[^"]*\.html" title="([^"]*)">([^<]*)</a>', re.S)
    editions = []
    for m in ligne.finditer(texte):
        domaine, date, question, titre = m.groups()
        editions.append({"date": date, "domaine": domaine, "titre": _texte(titre), "question": _texte(question)})
    return editions


def toutes_les_editions(editions: list[dict] | None = None, exclure: set[str] | None = None) -> str:
    """Liste compacte de TOUTES les éditions passées, pour le prompt du brief (une ligne par édition)."""
    editions = editions if editions is not None else charger_archives()
    lignes = []
    for e in editions:
        if e["date"] in (exclure or set()):
            continue
        q = e["question"]
        q = q if len(q) <= QUESTION_MAX else q[:QUESTION_MAX].rsplit(" ", 1)[0] + "…"
        lignes.append(f"- {e['date']} ({e['domaine']}) — {e['titre']} : {q}")
    return "\n".join(lignes) if lignes else "(aucune édition passée)"


def normaliser_connexes(brief: dict, editions: list[dict] | None = None) -> list[str]:
    """Vérifie `brief["articles_connexes"]` sans appel réseau : retire les dates inconnues, celle du jour et les doublons ;
    remplace le titre par le titre exact de l'édition (jamais une paraphrase) ; limite à 3. Ne remplit pas à la place du
    modèle : un lien factice vaut moins que pas de lien. Renvoie les modifications (pour le journal)."""
    editions = editions if editions is not None else charger_archives()
    par_date = {e["date"]: e for e in editions}
    aujourdhui = str(brief.get("date") or "")
    vus, propres, notes = set(), [], []
    for a in brief.get("articles_connexes") or []:
        date = str(a.get("date") or "")
        e = par_date.get(date)
        if not e or date == aujourdhui:
            notes.append(f"{date or '?'} écarté : édition inconnue ou du jour")
            continue
        if date in vus:
            notes.append(f"{date} écarté : doublon")
            continue
        vus.add(date)
        if a.get("titre") != e["titre"]:
            notes.append(f"{date} : titre remplacé par le titre exact de l'édition")
        propres.append({"date": date, "titre": e["titre"], "lien": a.get("lien") or ""})
    if len(propres) > NB_CONNEXES:
        notes.append(f"{len(propres) - NB_CONNEXES} article(s) en trop retiré(s)")
    brief["articles_connexes"] = propres[:NB_CONNEXES]
    return notes


if __name__ == "__main__":
    print(toutes_les_editions())
