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

Toujours en ANGLAIS de préférence, et toujours des CONCEPTS reformulés
— jamais le titre de l'édition recopié tel quel, ni des mots-clés bruts
type noms propres/marques/acronymes (ex. "Suno", "IA"). Pexels indexe
ses photos par tags descriptifs écrits par les photographes (catalogue
anglais bien plus riche), pas par recherche sémantique : un nom propre
ou un acronyme ne matche aucun tag, dans aucune langue, et fait
retomber la recherche sur un mot isolé, avec des résultats hors-sujet
à la clé. Partir des 2-3 idées clés du sujet et les traduire en scène
visuelle générique, ex. pour un sujet "IA + musique + procès" :
    mauvais : "IA Suno musique"            -> portraits sans rapport
    bon      : "artificial intelligence music technology" -> studio/MAO

Repli en français : testé avec le paramètre `locale=fr-FR` de l'API,
ça ne change RIEN à la pertinence du matching (seuls les libellés
affichés se traduisent) — mais des mots du dictionnaire français
COURANTS (ex. "intelligence artificielle musique procès") matchent
correctement, à condition de rester sur des noms communs, jamais des
noms propres/acronymes. Utile si l'anglais ne sort rien de convaincant,
mais l'anglais reste le premier réflexe (catalogue plus large).

Une requête composée sur deux concepts distincts (ex. "IA" + "musique")
sort souvent des résultats faibles — mais corrigé le 9 août : ce n'est
PAS que ces photos combinées n'existent pas sur Pexels, c'est que le
script forçait avant `orientation=square` sur la RECHERCHE elle-même,
ce qui écarte une bonne partie du catalogue (donc du classement par
pertinence) avant même d'avoir pu voir les meilleurs candidats — trouvé
en comparant avec l'appli Pexels, qui ne filtre pas par défaut et sort
de bien meilleurs résultats sur la même requête. Recherche maintenant
SANS filtre d'orientation ; le format carré (pour usage Instagram) est
appliqué après coup, au téléchargement, sur la photo déjà choisie pour
sa pertinence — voir `square_crop_url()`.

Si malgré ça une requête composée ne sort toujours rien de bon, chercher
chaque concept séparément et choisir/trancher humainement reste une
option valable — mais commencer par la requête composée sans a priori.

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


def search_pexels(query: str, count: int, api_key: str, color: str | None = None) -> list[dict]:
    # Pas de filtre "orientation" ici : testé le 9 août, forcer
    # orientation=square sur la RECHERCHE écarte une bonne partie du
    # catalogue (donc du classement par pertinence) avant même d'avoir
    # pu voir les meilleurs candidats — l'appli Pexels ne filtre pas non
    # plus par défaut. Le format carré est appliqué ensuite au moment du
    # téléchargement (voir square_crop_url), sur l'image déjà choisie
    # pour sa pertinence plutôt que pour son ratio d'origine.
    params_dict = {
        "query": query,
        "per_page": count,
    }
    if color:
        params_dict["color"] = color
    params = urllib.parse.urlencode(params_dict)
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


def square_crop_url(original_url: str, size: int = 1080) -> str:
    """Construit l'URL de rognage carré Pexels à partir de la photo
    d'origine (quel que soit son ratio natif), via les paramètres
    d'image du CDN Pexels — testé le 9 août, fonctionne sur n'importe
    quelle photo, pas besoin qu'elle soit carrée nativement."""
    sep = "&" if "?" in original_url else "?"
    return f"{original_url}{sep}auto=compress&cs=tinysrgb&fit=crop&w={size}&h={size}"


def download(url: str, dest_path: str) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Scenario/1.0 (lesscenarios.fr)"})
    with urllib.request.urlopen(req, timeout=20) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help="Mots-clés thématiques en anglais, ex. 'football stadium'")
    parser.add_argument("--count", type=int, default=5, help="Nombre de candidats à télécharger (défaut 5)")
    parser.add_argument("--out", default="/tmp/topic-image-candidates", help="Dossier de sortie")
    parser.add_argument(
        "--color", default=None,
        help="Filtre couleur dominante Pexels (optionnel), ex. 'gray' ou un hex "
             "comme 'cf9d4c' (or) / 'ece7da' (papier) pour coller à la charte du "
             "site. Valeurs nommées : red, orange, yellow, green, turquoise, "
             "blue, violet, pink, brown, black, gray, white.",
    )
    args = parser.parse_args()

    if any(c in args.query for c in "àâäéèêëïîôöùûüçÀÂÄÉÈÊËÏÎÔÖÙÛÜÇ"):
        print(f"ATTENTION : la requête « {args.query} » contient des accents "
              "français. Pexels indexe ses photos en anglais par concepts "
              "génériques, pas par recherche sémantique sur le titre — "
              "reformule en 2-3 mots-clés anglais (voir docstring du script) "
              "pour de meilleurs résultats.\n", file=sys.stderr)

    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        print("ERREUR : PEXELS_API_KEY absente de l'environnement. "
              "Vérifie la config de l'environnement Claude Code Remote "
              "(variable ajoutée récemment, nécessite une session neuve).",
              file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    try:
        photos = search_pexels(args.query, args.count, api_key, color=args.color)
    except Exception as e:
        print(f"ERREUR lors de la recherche Pexels : {e}", file=sys.stderr)
        sys.exit(1)

    if not photos:
        print(f"Aucun résultat Pexels pour « {args.query} ». "
              "Pas de candidat — garder le visuel généré habituel.")
        sys.exit(0)

    credits = []
    for i, photo in enumerate(photos, start=1):
        img_url = square_crop_url(photo["src"]["original"])
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
            "color": args.color,
        }
        credits.append(credit)
        print(f"  candidat {i} : {dest}  (photo par {credit['photographer']}, {credit['pexels_url']})")

    with open(os.path.join(args.out, "credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)

    print(f"\n{len(credits)} candidat(s) téléchargé(s) dans {args.out}/ — "
          "à regarder avant tout usage (Read tool), jamais un choix automatique.")


if __name__ == "__main__":
    main()
