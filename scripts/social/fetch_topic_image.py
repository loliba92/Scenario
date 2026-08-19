#!/usr/bin/env python3
"""
Cherche des images libres de droits pour illustrer le sujet du jour, et
télécharge les meilleurs candidats pour revue visuelle avant usage.

**Source par défaut : Pixabay (basculé le 19 août 2026).** Pexels reste
disponible (`--source pexels`) mais n'est plus la source par défaut : son
téléchargement (`images.pexels.com`) est bloqué par la politique d'egress
réseau de cet environnement depuis début août (recherche `api.pexels.com`
OK, mais le téléchargement échoue systématiquement en routine automatique
— voir `docs/ARCHITECTURE.md`, backlog, entrée « Ajouter Pixabay comme
seconde source d'image »). Pixabay a été testé en conditions réelles le
19 août : recherche ET téléchargement fonctionnent tous les deux dans cet
environnement.

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
type noms propres/marques/acronymes (ex. "Suno", "IA"). Les deux banques
indexent leurs photos par tags descriptifs écrits par les contributeurs
(catalogue anglais bien plus riche), pas par recherche sémantique : un
nom propre ou un acronyme ne matche aucun tag, dans aucune langue, et
fait retomber la recherche sur un mot isolé, avec des résultats
hors-sujet à la clé. Partir des 2-3 idées clés du sujet et les traduire
en scène visuelle générique, ex. pour un sujet "IA + musique + procès" :
    mauvais : "IA Suno musique"            -> portraits sans rapport
    bon      : "artificial intelligence music technology" -> studio/MAO

Repli en français : sur Pexels, testé avec `locale=fr-FR`, ça ne change
RIEN à la pertinence du matching (seuls les libellés affichés se
traduisent) — mais des mots du dictionnaire français COURANTS matchent
correctement, à condition de rester sur des noms communs, jamais des
noms propres/acronymes. Utile si l'anglais ne sort rien de convaincant,
mais l'anglais reste le premier réflexe (catalogue plus large). Pixabay
supporte un paramètre `lang` similaire (non branché ici, même logique
de repli si besoin un jour).

Une requête composée sur deux concepts distincts (ex. "IA" + "musique")
sort souvent des résultats faibles — mais corrigé le 9 août (Pexels) :
ce n'est PAS que ces photos combinées n'existent pas, c'est qu'un filtre
`orientation=square` sur la RECHERCHE elle-même écarte une bonne partie
du catalogue (donc du classement par pertinence) avant même d'avoir pu
voir les meilleurs candidats. Recherche donc SANS filtre d'orientation
sur les deux sources ; le format carré (pour usage Instagram) est
appliqué après coup, au téléchargement/recadrage, sur la photo déjà
choisie pour sa pertinence — jamais sur la recherche.

Si malgré ça une requête composée ne sort toujours rien de bon, chercher
chaque concept séparément et choisir/trancher humainement reste une
option valable — mais commencer par la requête composée sans a priori.

**Limite Pixabay sans compte "full API access" approuvé (compte standard
utilisé ici)** : la plus grande image disponible est `largeImageURL`,
plafonnée à 1280px sur son plus grand côté (pas d'accès à l'image
originale pleine résolution). Suffisant pour le carré 1080×1080, mais
implique un léger upscale pour le recadrage large 1600×900 de
`use_topic_image.py` (object-fit:cover côté CSS masque en grande partie
la perte de netteté sur un fond d'image avec dégradé sombre superposé).

Usage:
    export PIXABAY_KEY=...  (déjà en variable d'environnement normalement)
    python3 scripts/social/fetch_topic_image.py "government building paris" \\
        --count 5 --out /tmp/topic-image-candidates

    # Pour retenter avec Pexels (source dormante, pas de garantie de
    # téléchargement dans cet environnement) :
    export PEXELS_API_KEY=...
    python3 scripts/social/fetch_topic_image.py "government building paris" \\
        --source pexels --count 5 --out /tmp/topic-image-candidates

Produit, dans le dossier --out :
    candidate-1.jpg, candidate-2.jpg, ... (recadrage carré 1080×1080,
    pour la revue visuelle) + credits.json (photographe, lien source,
    requête, et pour Pixabay un fichier candidate-N-raw.jpg conservé
    pour le recadrage large ultérieur) pour traçabilité.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
PIXABAY_SEARCH_URL = "https://pixabay.com/api/"

USER_AGENT = "Scenario/1.0 (lesscenarios.fr)"


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
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("photos", [])


def search_pixabay(query: str, count: int, api_key: str, color: str | None = None) -> list[dict]:
    # per_page doit être entre 3 et 200 côté API — count peut valoir
    # moins (ex. 1 pour un test rapide), on demande donc le max des deux
    # et on tronque nous-mêmes ensuite à `count` résultats.
    params_dict = {
        "key": api_key,
        "q": query,
        "image_type": "photo",  # exclut illustrations/vecteurs/clipart, cohérent avec Pexels (photos uniquement)
        "safesearch": "true",
        "per_page": max(count, 3),
        "min_width": 1280,  # garantit que largeImageURL (plafonné à 1280) sera bien à sa taille max
    }
    if color:
        # Vocabulaire couleur différent de Pexels : grayscale, transparent,
        # red, orange, yellow, green, turquoise, blue, lilac, pink, white,
        # gray, black, brown — pas de code hex accepté ici (accepté côté
        # Pexels). À adapter à la main si besoin, pas de traduction
        # automatique du vocabulaire Pexels vers Pixabay.
        params_dict["colors"] = color
    params = urllib.parse.urlencode(params_dict)
    req = urllib.request.Request(
        f"{PIXABAY_SEARCH_URL}?{params}",
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("hits", [])[:count]


def crop_url(original_url: str, w: int, h: int) -> str:
    """Construit l'URL de rognage Pexels à partir de la photo d'origine
    (quel que soit son ratio natif), via les paramètres d'image du CDN
    Pexels — testé le 9 août (variante carrée), fonctionne sur
    n'importe quelle photo/ratio, pas besoin qu'elle soit déjà au bon
    format nativement. N'a pas d'équivalent côté Pixabay (pas de
    recadrage à la volée par URL, voir square_crop_local())."""
    sep = "&" if "?" in original_url else "?"
    return f"{original_url}{sep}auto=compress&cs=tinysrgb&fit=crop&w={w}&h={h}"


def square_crop_url(original_url: str, size: int = 1080) -> str:
    """Rognage carré (image Instagram) — cas particulier de crop_url(),
    Pexels uniquement."""
    return crop_url(original_url, size, size)


def square_crop_local(src_path: str, dest_path: str, size: int = 1080) -> None:
    """Recadrage carré local via Pillow — utilisé pour Pixabay, qui ne
    permet pas de recadrage arbitraire par URL (seulement quelques
    tailles fixes en suffixe : _180/_340/_640/_960)."""
    from PIL import Image, ImageOps
    im = Image.open(src_path).convert("RGB")
    square = ImageOps.fit(im, (size, size), method=Image.LANCZOS, centering=(0.5, 0.45))
    square.save(dest_path, "JPEG", quality=90)


def download(url: str, dest_path: str) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help="Mots-clés thématiques en anglais, ex. 'football stadium'")
    parser.add_argument("--count", type=int, default=5, help="Nombre de candidats à télécharger (défaut 5)")
    parser.add_argument("--out", default="/tmp/topic-image-candidates", help="Dossier de sortie")
    parser.add_argument(
        "--source", choices=["pixabay", "pexels"], default="pixabay",
        help="Banque d'images à interroger (défaut : pixabay — voir docstring pour pourquoi Pexels "
             "est dormant dans cet environnement).",
    )
    parser.add_argument(
        "--color", default=None,
        help="Filtre couleur dominante (optionnel), vocabulaire différent selon --source : "
             "Pexels accepte des noms (red, orange, ..., violet, brown) ou un hex ('cf9d4c') ; "
             "Pixabay accepte une liste fermée différente (voir search_pixabay()), pas de hex.",
    )
    args = parser.parse_args()

    if any(c in args.query for c in "àâäéèêëïîôöùûüçÀÂÄÉÈÊËÏÎÔÖÙÛÜÇ"):
        print(f"ATTENTION : la requête « {args.query} » contient des accents "
              "français. Les deux banques indexent leurs photos en anglais par "
              "concepts génériques, pas par recherche sémantique sur le titre — "
              "reformule en 2-3 mots-clés anglais (voir docstring du script) "
              "pour de meilleurs résultats.\n", file=sys.stderr)

    if args.source == "pixabay":
        api_key = os.environ.get("PIXABAY_KEY")
        env_var_name = "PIXABAY_KEY"
    else:
        api_key = os.environ.get("PEXELS_API_KEY")
        env_var_name = "PEXELS_API_KEY"

    if not api_key:
        print(f"ERREUR : {env_var_name} absente de l'environnement. "
              "Vérifie la config de l'environnement Claude Code Remote "
              "(variable ajoutée récemment, nécessite une session neuve).",
              file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    try:
        if args.source == "pixabay":
            results = search_pixabay(args.query, args.count, api_key, color=args.color)
        else:
            results = search_pexels(args.query, args.count, api_key, color=args.color)
    except Exception as e:
        print(f"ERREUR lors de la recherche {args.source} : {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print(f"Aucun résultat {args.source} pour « {args.query} ». "
              "Pas de candidat — garder le visuel généré habituel.")
        sys.exit(0)

    credits = []
    for i, item in enumerate(results, start=1):
        dest = os.path.join(args.out, f"candidate-{i}.jpg")

        if args.source == "pexels":
            img_url = square_crop_url(item["src"]["original"])
            try:
                download(img_url, dest)
            except Exception as e:
                print(f"  (échec téléchargement candidat {i} : {e})", file=sys.stderr)
                continue
            credit = {
                "candidate": i,
                "source": "pexels",
                "file": dest,
                "photographer": item.get("photographer"),
                "pexels_url": item.get("url"),
                "original_url": item.get("src", {}).get("original"),
                "query": args.query,
                "color": args.color,
            }
            print(f"  candidat {i} : {dest}  (photo par {credit['photographer']}, {credit['pexels_url']})")

        else:  # pixabay
            raw_dest = os.path.join(args.out, f"candidate-{i}-raw.jpg")
            large_url = item.get("largeImageURL") or item.get("webformatURL")
            try:
                download(large_url, raw_dest)
                square_crop_local(raw_dest, dest)
            except Exception as e:
                print(f"  (échec téléchargement/recadrage candidat {i} : {e})", file=sys.stderr)
                continue
            credit = {
                "candidate": i,
                "source": "pixabay",
                "file": dest,
                "raw_file": raw_dest,
                "photographer": item.get("user"),
                "user_id": item.get("user_id"),
                "pixabay_url": item.get("pageURL"),
                "large_image_url": large_url,
                "image_width": item.get("imageWidth"),
                "image_height": item.get("imageHeight"),
                "query": args.query,
                "color": args.color,
            }
            print(f"  candidat {i} : {dest}  (photo par {credit['photographer']}, {credit['pixabay_url']})")

        credits.append(credit)

    with open(os.path.join(args.out, "credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)

    print(f"\n{len(credits)} candidat(s) téléchargé(s) dans {args.out}/ — "
          "à regarder avant tout usage (Read tool), jamais un choix automatique.")


if __name__ == "__main__":
    main()
