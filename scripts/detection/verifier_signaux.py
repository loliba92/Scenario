#!/usr/bin/env python3
"""Lit data/signaux.json et écrit data/signaux-rapport.md. Ne modifie jamais signaux.json."""
import argparse
import json
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
STATUTS = {"en_attente", "concretise", "non_concretise"}
SEUIL_PROCHE = 7


def analyser(signaux, aujourdhui, racine=RACINE):
    """Classe chaque signal : echu, proche, en_cours, tranche, ou anomalies."""
    res = {"echus": [], "proches": [], "en_cours": [], "tranches": [], "anomalies": []}
    for s in signaux:
        sid = s.get("id", "?")
        if s.get("statut") not in STATUTS:
            res["anomalies"].append((sid, f"statut inconnu : {s.get('statut')!r}"))
            continue
        try:
            limite = date.fromisoformat(s["date_limite"])
        except (KeyError, ValueError):
            res["anomalies"].append((sid, "date_limite absente ou illisible"))
            continue
        for ed in s.get("editions", []):
            if not (racine / ed).exists():
                res["anomalies"].append((sid, f"édition introuvable : {ed}"))
        if s["statut"] != "en_attente":
            res["tranches"].append((s, limite))
            continue
        jours = (limite - aujourdhui).days
        if jours < 0:
            res["echus"].append((s, limite, -jours))
        elif jours <= SEUIL_PROCHE:
            res["proches"].append((s, limite, jours))
        else:
            res["en_cours"].append((s, limite, jours))
    return res


def rapport(res, aujourdhui):
    L = [f"# Événements à surveiller — point du {aujourdhui.strftime('%d/%m/%Y')}", "",
         "Fichier généré par `scripts/detection/verifier_signaux.py` (source : `data/signaux.json`).", ""]

    def bloc(titre, items, fmt):
        L.append(f"## {titre}")
        L.extend(fmt(*i) for i in items) if items else L.append("Aucun.")
        L.append("")

    def detail(s, limite):
        eds = ", ".join(s.get("editions", [])) or "aucune édition liée"
        return (f"- **{s['libelle']}** (`{s['id']}`) — limite le {limite.strftime('%d/%m/%Y')}.\n"
                f"  - Si oui : {s['si_concretise']['effet']} (renforce : {s['si_concretise']['renforce']})\n"
                f"  - Si non : {s['si_non_concretise']['effet']} (renforce : {s['si_non_concretise']['renforce']})\n"
                f"  - Édition(s) : {eds}")

    bloc("À trancher maintenant (date limite dépassée)", res["echus"],
         lambda s, l, j: detail(s, l) + f"\n  - Dépassé de {j} jour(s)")
    bloc(f"Échéance dans {SEUIL_PROCHE} jours ou moins", res["proches"],
         lambda s, l, j: detail(s, l) + f"\n  - Reste {j} jour(s)")
    bloc("En cours", res["en_cours"],
         lambda s, l, j: f"- {s['libelle']} — limite le {l.strftime('%d/%m/%Y')} (dans {j} jours)")
    bloc("Déjà tranchés", res["tranches"],
         lambda s, l: f"- {s['libelle']} — {s['statut']}")
    bloc("Anomalies dans le fichier", res["anomalies"], lambda i, m: f"- `{i}` : {m}")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="AAAA-MM-JJ (par défaut : aujourd'hui)")
    p.add_argument("--sortie", default=str(RACINE / "data" / "signaux-rapport.md"))
    a = p.parse_args()
    jour = date.fromisoformat(a.date) if a.date else date.today()
    signaux = json.loads((RACINE / "data" / "signaux.json").read_text(encoding="utf-8"))
    texte = rapport(analyser(signaux, jour), jour)
    Path(a.sortie).write_text(texte + "\n", encoding="utf-8")
    print(texte)


if __name__ == "__main__":
    main()
