#!/usr/bin/env python3
"""
Cherche des images libres de droits (Pexels, usage commercial autorisé
sans attribution obligatoire) pour illustrer le sujet du jour, et
télécharge les meilleurs candidats pour revue visuelle avant usage.

Ne choisit JAMAIS automatiquement une image finale — ce script ne fait
que proposer des candidats téléchargés localement (jamais un simple
lien externe). La sélection reste toujours un geste humain/en session :
regarder les candidats, choisir le plus pertinent (ou aucun si rien ne
convient), puis appeler `use_topic_image.py` pour le committer comme
image officielle du jour. Voir docs/ARCHITECTURE.md, section "Image
custom par sujet (Pexels)".

Principe non négociable : mots-clés THÉMATIQUES/GÉNÉRIQUES uniquement
(ex. "football stadium", "oil tanker", "wildfire forest") — jamais le
nom d'une personne réelle, pour ne jamais laisser une photo générique
suggérer qu'elle représente un individu précis.

Usage:
    export PEXELS_API_KEY=...  (déjà en variable d'environnement normalement)
    python3 scripts/social/fetch_topic_image.py "football stadium crowd" \\
        --count 5 --out /tmp/topic-image-candidates

Produit, dans le dossier --out :
    candidate-1.jpg, candidate-2.jpg, ... + credits.json (photographe,
    lien source Pexels, requête utilisée) pour traçabilité.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"


def search_pexels(query: str, count: int, api_key: str) -> list[dict]:
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": count,
        "orientation": "square",
    })
    req = urllib.request.Request(
        f"{PEXELS_SEARCH_URL}?{params}",
        headers={
            "Authorization": api_key,
            "User-Agent": "Scenario/1.0 (lesscenarios.fr)",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("photos", [])


def download(url: str, dest_path: str) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Scenario/1.0 (lesscenarios.fr)"})
    with urllib.request.urlopen(req, timeout=20) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help="Mots-clés thématiques en anglais, ex. 'football stadium'")
    parser.add_argument("--count", type=int, default=5, help="Nombre de candidats à télécharger (défaut 5)")
    parser.add_argument("--out", default="/tmp/topic-image-candidates", help="Dossier de sortie")
    args = parser.parse_args()

    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        print("ERREUR : PEXELS_API_KEY absente de l'environnement. "
              "Vérifie la config de l'environnement Claude Code Remote "
              "(variable ajoutée récemment, nécessite une session neuve).",
              file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    try:
        photos = search_pexels(args.query, args.count, api_key)
    except Exception as e:
        print(f"ERREUR lors de la recherche Pexels : {e}", file=sys.stderr)
        sys.exit(1)

    if not photos:
        print(f"Aucun résultat Pexels pour « {args.query} ». "
              "Pas de candidat — garder le visuel généré habituel.")
        sys.exit(0)

    credits = []
    for i, photo in enumerate(photos, start=1):
        img_url = photo["src"]["large"]
        dest = os.path.join(args.out, f"candidate-{i}.jpg")
        try:
            download(img_url, dest)
        except Exception as e:
            print(f"  (échec téléchargement candidat {i} : {e})", file=sys.stderr)
            continue
        credit = {
            "candidate": i,
            "file": dest,
            "photographer": photo.get("photographer"),
            "pexels_url": photo.get("url"),
            "query": args.query,
        }
        credits.append(credit)
        print(f"  candidat {i} : {dest}  (photo par {credit['photographer']}, {credit['pexels_url']})")

    with open(os.path.join(args.out, "credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)

    print(f"\n{len(credits)} candidat(s) téléchargé(s) dans {args.out}/ — "
          "à regarder avant tout usage (Read tool), jamais un choix automatique.")


if __name__ == "__main__":
    main()
