#!/usr/bin/env python3
"""Cherche sur le web si les événements échus ou proches de data/signaux.json ont eu lieu.

Écrit data/signaux-verification.md. Ne modifie jamais signaux.json : le propriétaire valide.
Usage : OPENROUTER_API_KEY=xxx python3 scripts/detection/verifier_signaux_web.py [--dry-run]
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "scripts" / "edition"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_daily_edition import GenerationError, call_openrouter  # noqa: E402
import verifier_signaux  # noqa: E402

MODELE = "deepseek/deepseek-v4-flash"
MAX_SIGNAUX_PAR_PASSAGE = 3
VERDICTS = {"concretise", "non_concretise", "incertain"}
OUTILS = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 6}}]


def candidats(res):
    """Échus d'abord (le plus en retard en premier), puis proches ; plafonnés."""
    echus = sorted(res["echus"], key=lambda x: -x[2])
    proches = sorted(res["proches"], key=lambda x: x[2])
    tous = echus + proches
    return tous[:MAX_SIGNAUX_PAR_PASSAGE], tous[MAX_SIGNAUX_PAR_PASSAGE:]


def prompt(signal, limite, aujourdhui):
    return (
        f"Nous sommes le {aujourdhui.isoformat()}. Événement à vérifier : « {signal['libelle']} » "
        f"(date limite : {limite.isoformat()}).\n"
        "Cherche sur le web si cet événement a eu lieu. Réponds uniquement par un objet JSON :\n"
        '{"verdict": "concretise" | "non_concretise" | "incertain", '
        '"resume": "2 phrases maximum, faits datés", '
        '"sources": [{"titre": "...", "url": "https://..."}]}\n'
        "Règles : n'invente rien ; sans source datée qui le confirme, réponds « incertain » ; "
        "« non_concretise » seulement si la date limite est dépassée et qu'aucune annonce n'a eu lieu."
    )


def valider(r):
    """Normalise la réponse du modèle ; sans source valide, un verdict ferme devient « incertain »."""
    if not isinstance(r, dict) or r.get("verdict") not in VERDICTS:
        raise GenerationError(f"réponse inattendue : {r!r}")
    sources = [
        {"titre": str(s.get("titre") or s["url"]).strip(), "url": str(s["url"]).strip()}
        for s in (r.get("sources") or [])
        if isinstance(s, dict) and re.match(r"^https?://", str(s.get("url", "")))
    ]
    verdict = r["verdict"]
    if verdict != "incertain" and not sources:
        verdict = "incertain"
    return {"verdict": verdict, "resume": str(r.get("resume") or "").strip(), "sources": sources}


def rapport(lignes, reportes, cout, modele, aujourdhui, dry_run):
    L = [f"# Vérification web des événements — {aujourdhui.strftime('%d/%m/%Y')}", "",
         f"Modèle : `{modele}` · coût du passage : {cout:.4f} $"
         + (" · **à vide, aucun appel**" if dry_run else ""),
         "Constats à valider par le propriétaire : aucun statut n'est modifié dans `data/signaux.json`.", ""]
    if not lignes:
        L.append("Aucun événement échu ni proche de son échéance : rien à vérifier.")
    for sid, libelle, res in lignes:
        L.append(f"## {libelle} (`{sid}`)")
        if res is None:
            L.append("À vérifier (mode à vide).")
        elif "erreur" in res:
            L.append(f"Vérification impossible ce jour : {res['erreur']}")
        else:
            L.append(f"**Constat : {res['verdict']}**")
            L.append(res["resume"] or "Pas de résumé.")
            for s in res["sources"]:
                L.append(f"- [{s['titre']}]({s['url']})")
        L.append("")
    if reportes:
        L.append("## Reportés au prochain passage (plafond atteint)")
        L.extend(f"- {s['libelle']}" for s, *_ in reportes)
        L.append("")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date")
    p.add_argument("--model", default=MODELE)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--sortie", default=str(RACINE / "data" / "signaux-verification.md"))
    a = p.parse_args()
    jour = date.fromisoformat(a.date) if a.date else date.today()
    signaux = json.loads((RACINE / "data" / "signaux.json").read_text(encoding="utf-8"))
    ce_passage, reportes = candidats(verifier_signaux.analyser(signaux, jour))

    cle = os.environ.get("OPENROUTER_API_KEY")
    if ce_passage and not a.dry_run and not cle:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    lignes, cout = [], 0.0
    for s, limite, _ in ce_passage:
        if a.dry_run:
            lignes.append((s["id"], s["libelle"], None))
            continue
        try:
            brut, usage = call_openrouter(prompt(s, limite, jour), a.model, cle, temperature=0.2,
                                          max_tokens=4000, timeout=180, tools=OUTILS)
            cout += (usage or {}).get("cost") or 0.0
            lignes.append((s["id"], s["libelle"], valider(brut)))
        except GenerationError as e:
            print(f"{s['id']} : {e}", file=sys.stderr)
            lignes.append((s["id"], s["libelle"], {"erreur": str(e)[:200]}))

    texte = rapport(lignes, reportes, cout, a.model, jour, a.dry_run)
    Path(a.sortie).write_text(texte + "\n", encoding="utf-8")
    print(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
