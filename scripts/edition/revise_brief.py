"""Construit un brief « révisé » pour régénérer l'édition après la critique
automatique (scripts/edition/critique_preview.py), dans la séquence :
brief -> édition -> critique -> brief révisé -> édition régénérée (voir
.github/workflows/daily-preview.yml, étape « Revise brief from critique »).

**Jamais un patch direct de `.preview-content.json`.** On repasse par
`generate_daily_edition.py` avec le même prompt de rédaction et les mêmes
validations de schéma que la génération initiale, au lieu de bricoler le
JSON déjà produit à la main — plus fiable qu'un patch chirurgical, au prix
d'une régénération complète de l'édition (nouvel appel OpenRouter, ~$0.02).

Ne modifie ni le brief ni le contenu déjà commités sur disque : lit les deux,
écrit un nouveau fichier brief (--out), jamais un overwrite en place.

Le brief révisé ajoute 2 champs au brief original — voir
docs/routine-redaction-prompt.md § « Édition précédente et corrections à
appliquer » pour ce que le modèle de rédaction en fait :
  - edition_precedente : le contenu déjà rédigé (.preview-content.json),
    pour que le modèle RÉVISE ce texte plutôt que d'en réécrire un autre ;
  - corrections_a_appliquer : les `findings` de la critique automatique
    (déjà filtrés des faux positifs par critique_preview.py::drop_empty_
    findings — jamais re-filtrés ici).

N'écrit rien et sort en erreur (exit 1) si la critique n'a aucun finding :
rien à réviser, la régénération ne doit jamais être déclenchée pour rien
(voir l'appelant dans daily-preview.yml, qui teste ce cas AVANT d'appeler
ce script plutôt que de s'appuyer sur ce garde-fou seul, pour ne jamais
lancer un appel OpenRouter inutile).

Usage :
    python3 revise_brief.py --brief ../../editorial-briefs/2026-09-23.json \
        --content ../../.preview-content.json \
        --critique-json /tmp/critique.json \
        --out /tmp/brief-revise.json
"""
import argparse
import json
import sys
from pathlib import Path


def build_revised_brief(brief, content, critique):
    findings = critique.get("findings") or []
    if not findings:
        raise ValueError("critique sans finding : rien à réviser")
    revised = dict(brief)
    revised["edition_precedente"] = content
    revised["corrections_a_appliquer"] = findings
    return revised


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, help="chemin du brief original")
    parser.add_argument("--content", required=True, help="chemin du .preview-content.json déjà généré")
    parser.add_argument("--critique-json", required=True, help="chemin du JSON de critique (--out-json de critique_preview.py)")
    parser.add_argument("--out", required=True, help="chemin du brief révisé à écrire")
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    content = json.loads(Path(args.content).read_text(encoding="utf-8"))
    critique = json.loads(Path(args.critique_json).read_text(encoding="utf-8"))

    try:
        revised = build_revised_brief(brief, content, critique)
    except ValueError as e:
        print(f"[revise_brief] {e}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(revised, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[revise_brief] {len(revised['corrections_a_appliquer'])} correction(s) injectée(s) -> {out_path}")


if __name__ == "__main__":
    main()
