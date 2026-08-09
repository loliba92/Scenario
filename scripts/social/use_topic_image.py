#!/usr/bin/env python3
"""
Valide un candidat trouvé par fetch_topic_image.py comme image officielle
du jour : le copie vers assets/social/topic-images/{date}.jpg et écrit
la fiche de provenance (photographe, lien Pexels) à côté, pour garder une
trace même si l'attribution n'est pas légalement obligatoire (licence
Pexels : usage commercial libre sans attribution requise).

Geste toujours volontaire (jamais appelé automatiquement) : n'exécuter
qu'après avoir regardé le candidat (Read tool) et confirmé qu'il convient
au sujet du jour.

Usage:
    python3 scripts/social/use_topic_image.py \\
        /tmp/topic-image-candidates/candidate-2.jpg \\
        --date 2026-08-08 \\
        --credits /tmp/topic-image-candidates/credits.json

Ensuite, mettre à jour à la main (comme pour l'image générée habituelle) :
  - feed.xml : <enclosure url="https://lesscenarios.fr/assets/social/topic-images/{date}.jpg" .../>
  - index.html / archives/{date}.html : meta og:image, twitter:image, et
    le tableau "image" du JSON-LD NewsArticle.
"""

import argparse
import json
import os
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("candidate", help="Chemin du fichier candidat choisi (ex. candidate-2.jpg)")
    parser.add_argument("--date", required=True, help="Date de l'édition, format AAAA-MM-JJ")
    parser.add_argument("--credits", help="Chemin du credits.json produit par fetch_topic_image.py")
    parser.add_argument("--repo-root", default=".", help="Racine du dépôt (défaut : répertoire courant)")
    args = parser.parse_args()

    if not os.path.isfile(args.candidate):
        print(f"ERREUR : fichier introuvable : {args.candidate}", file=sys.stderr)
        sys.exit(1)

    out_dir = os.path.join(args.repo_root, "assets", "social", "topic-images")
    os.makedirs(out_dir, exist_ok=True)

    dest_img = os.path.join(out_dir, f"{args.date}.jpg")
    shutil.copyfile(args.candidate, dest_img)
    print(f"Image copiée : {dest_img}")

    credit_entry = None
    if args.credits and os.path.isfile(args.credits):
        with open(args.credits, encoding="utf-8") as f:
            all_credits = json.load(f)
        basename = os.path.basename(args.candidate)
        for c in all_credits:
            if os.path.basename(c["file"]) == basename:
                credit_entry = c
                break

    dest_json = os.path.join(out_dir, f"{args.date}.json")
    with open(dest_json, "w", encoding="utf-8") as f:
        json.dump(credit_entry or {"note": "provenance non retrouvée, à compléter à la main"}, f, ensure_ascii=False, indent=2)
    print(f"Fiche de provenance écrite : {dest_json}")

    print(
        "\nÀ faire ensuite à la main :\n"
        f"  1. feed.xml : <enclosure url=\"https://lesscenarios.fr/assets/social/topic-images/{args.date}.jpg\" type=\"image/jpeg\" length=\"0\"/>\n"
        f"  2. index.html + archives/{args.date}.html : meta og:image / twitter:image / JSON-LD \"image\" -> "
        f"https://lesscenarios.fr/assets/social/topic-images/{args.date}.jpg\n"
        "  3. Vérifier visuellement (Playwright) avant de pousser."
    )


if __name__ == "__main__":
    main()
