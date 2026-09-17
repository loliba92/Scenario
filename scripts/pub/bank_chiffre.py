#!/usr/bin/env python3
"""
Extrait et banque le chiffre "Le saviez-vous" d'une édition, au moment de
sa publication — plutôt que de le refaire, des jours plus tard, quand la
rotation `pub.yml` en a besoin (voir `generate_daily_pub.py`,
`get_chiffre_for_date()`).

Demandé le 17 septembre 2026, retour utilisateur : « pas facile à
comprendre [...] ce ne serait pas possible d'inclure cette production
dans le workflow de l'édition ? car on a déjà tout le contexte de
l'édition à ce moment ». L'extraction elle-même ne dépend en réalité que
du HTML déjà publié (archives/{date}.html), pas d'un contexte en mémoire
— le vrai gain n'est pas la fraîcheur, c'est qu'un seul endroit produit et
vérifie ce chiffre, une seule fois, au lieu de deux scripts qui se
recoordonnent dans le temps.

Écrit le résultat dans `editorial-briefs/{date}.json` (déjà committé par
ailleurs pour chaque édition) :
- `chiffre_candidat` : le chiffre trouvé (mêmes champs que le fields{}
  historique de `extract_chiffre()`) — absent si aucun candidat valable.
- `chiffre_candidat_checked: true` : toujours posé, que le candidat soit
  trouvé ou non — signale à `get_chiffre_for_date()` de ne jamais
  retenter une extraction déjà faite pour rien.

**Jamais bloquant pour la publication de l'édition elle-même** — voir
`continue-on-error: true` sur l'étape correspondante de
`post-edition.yml` : un échec ici (pas de chiffre exploitable, panne
OpenRouter) est journalisé mais ne doit jamais faire échouer le run.

Usage :
    OPENROUTER_API_KEY=xxx python3 scripts/pub/bank_chiffre.py --date 2026-09-17
"""
import argparse
import json
import os
import sys
from datetime import date

from generate_daily_pub import ROOT, extract_chiffre

BRIEFS_DIR = ROOT / "editorial-briefs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--model", default="deepseek/deepseek-v4-flash")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent — chiffre non banqué pour cette édition.", file=sys.stderr)
        return 1

    d = date.fromisoformat(args.date)
    brief_path = BRIEFS_DIR / f"{d.isoformat()}.json"
    if not brief_path.exists():
        print(f"ERREUR : {brief_path} introuvable — rien à banquer.", file=sys.stderr)
        return 1

    try:
        result = extract_chiffre(d, args.model, api_key)
    except Exception as e:  # noqa: BLE001 — jamais bloquant, voir docstring
        print(f"ATTENTION : extraction du chiffre échouée pour {d} : {e}", file=sys.stderr)
        result = None

    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    brief["chiffre_candidat_checked"] = True
    if result is not None:
        fields, usage = result
        brief["chiffre_candidat"] = fields
        print(f"Chiffre banqué pour {d} : {fields['stat']} — {fields['message'][:100]}")
    else:
        brief.pop("chiffre_candidat", None)
        print(f"Aucun chiffre exploitable pour {d} — banqué comme « vérifié, rien de bon ».")

    brief_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
