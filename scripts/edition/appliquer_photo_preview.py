#!/usr/bin/env python3
"""Reconstruit preview.html d'une date avec la photo décrite dans editorial-previews/{date}.photo-credits.json.

Sert à remplacer la photo d'un aperçu déjà validé SANS refaire la rédaction (aucun appel au modèle, aucun coût) :
le texte vient de editorial-previews/{date}.content.json, la photo de la fiche de crédit.
  - fiche `"source": "manuelle"` : photo rangée dans le dépôt (voir scripts/social/photo_manuelle.py), recadrée ici
    en carré et en large, centrée sur le visage ;
  - sinon : photo Pexels, comme le fait daily-preview.yml.
La publication du lendemain relit la même fiche (generate_post_edition.py) : l'image publiée est celle de l'aperçu.

    python3 scripts/edition/appliquer_photo_preview.py --date 2026-10-18
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "social"))

import build_html  # noqa: E402
import generate_daily_edition as gde  # noqa: E402
import photo_manuelle  # noqa: E402

SITE_URL = "https://lesscenarios.fr"


def construire_photo(credits, date_str, h1):
    if credits.get("source") == "manuelle":
        dossier = REPO_ROOT / "assets" / "social" / "photos-manuelles"
        photo_manuelle.produire_recadrages(credits, REPO_ROOT, dossier, date_str)
        base = f"{SITE_URL}/assets/social/photos-manuelles/{date_str}"
        return {
            "og_image_url": f"{base}-carre.jpg", "hero_image_url": f"{base}-large.jpg",
            "alt": credits.get("alt") or f"Photo d'illustration — {h1}",
            "photographer": credits["photographer"], "pexels_url": credits["source_url"],
            "source_label": credits.get("source_label"), "licence": credits.get("licence"),
            "licence_url": credits.get("licence_url"),
        }
    url = credits["original_url"]
    og = f"{url}{'&' if '?' in url else '?'}auto=compress&cs=tinysrgb&fit=crop&w=1080&h=1080&crop=bottom"
    return {"og_image_url": og, "hero_image_url": og, "alt": f"Illustration du sujet: {credits.get('query', '')}",
            "photographer": credits["photographer"], "pexels_url": credits["pexels_url"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    args = ap.parse_args()
    d = args.date
    brief = gde.load_brief(REPO_ROOT / "editorial-briefs" / f"{d}.json")
    content = json.loads((REPO_ROOT / "editorial-previews" / f"{d}.content.json").read_text(encoding="utf-8"))
    credits = json.loads((REPO_ROOT / "editorial-previews" / f"{d}.photo-credits.json").read_text(encoding="utf-8"))
    photo = construire_photo(credits, d, content["h1"])
    shell = build_html.extract_shell((REPO_ROOT / "index.html").read_text(encoding="utf-8"))
    html_text, numero = build_html.assemble_index_html(shell, content, brief, d, photo=photo)
    html_text = gde.convert_markdown_bold_in_html(html_text)
    erreurs = gde.validate_assembled_html(html_text, content)
    if erreurs:
        raise SystemExit("validation du HTML assemblé échouée :\n  - " + "\n  - ".join(erreurs))
    (REPO_ROOT / "preview.html").write_text(html_text, encoding="utf-8")
    print(f"preview.html reconstruit pour {d} (édition N°{numero}), photo : {credits['photographer']}")


if __name__ == "__main__":
    main()
