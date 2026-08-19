#!/usr/bin/env python3
"""
Valide un candidat trouvé par fetch_topic_image.py comme image officielle
du jour : le copie vers assets/social/topic-images/{date}.jpg et écrit
la fiche de provenance (photographe, lien source) à côté, pour garder une
trace même si l'attribution n'est pas légalement obligatoire (licences
Pexels/Pixabay : usage commercial libre sans attribution requise).

Geste toujours volontaire (jamais appelé automatiquement) : n'exécuter
qu'après avoir regardé le candidat (Read tool) et confirmé qu'il convient
au sujet du jour.

**Recadrage large pour l'article, ajouté le 10 août.** En plus du carré
1080×1080 (usage Instagram), produit un second recadrage 16:9 (1600×900)
de la MÊME photo déjà validée — vers
assets/social/topic-images/{date}-wide.jpg — pour l'image en tête
d'article (voir docs/ARCHITECTURE.md, section "Image dans le corps de
l'article"). Pas de nouvelle revue nécessaire : c'est un recrop de la
photo déjà choisie, pas un nouveau candidat.

**Deux méthodes selon la source** (lue depuis `credit_entry["source"]`,
écrit par fetch_topic_image.py — `pexels` par défaut si absent, pour la
compatibilité avec les fiches de provenance générées avant ce champ) :
- `pexels` : recadrage à la volée via les paramètres du CDN Pexels
  (`crop_url`), retéléchargé depuis `original_url`. Nécessite
  `original_url` dans credits.json (présent pour toute recherche faite
  après le 10 août) ; si absent, ce fichier -wide.jpg n'est simplement
  pas produit — jamais bloquant, l'image carrée reste disponible.
- `pixabay` : pas de recadrage à la volée par URL côté Pixabay —
  recadrage local (Pillow) depuis le fichier `raw_file` déjà téléchargé
  par fetch_topic_image.py (la même image pleine résolution qui a servi
  au candidat carré), pas de second appel réseau. Source plafonnée à
  1280px sur son plus grand côté (compte standard, pas de "full API
  access") : le recadrage 1600×900 implique donc un léger upscale,
  masqué en grande partie par le dégradé sombre superposé côté CSS
  (`.article-image-scrim`).

Usage:
    python3 scripts/social/use_topic_image.py \\
        /tmp/topic-image-candidates/candidate-2.jpg \\
        --date 2026-08-08 \\
        --credits /tmp/topic-image-candidates/credits.json

Ensuite, mettre à jour à la main (comme pour l'image générée habituelle) :
  - feed.xml : <enclosure url="https://lesscenarios.fr/assets/social/topic-images/{date}.jpg" .../>
  - index.html / archives/{date}.html : meta og:image, twitter:image, et
    le tableau "image" du JSON-LD NewsArticle.
  - index.html : bloc image en tête d'article, avec {date}-wide.jpg si
    produit (voir docs/routine-prompt.md, étape technique 8).
"""

import argparse
import json
import os
import shutil
import sys
import urllib.request


def crop_url(original_url: str, w: int, h: int) -> str:
    """Copie de scripts/social/fetch_topic_image.py::crop_url — dupliquée
    ici pour ne pas complexifier l'import inter-scripts pour une seule
    fonction utilitaire. Pexels uniquement."""
    sep = "&" if "?" in original_url else "?"
    return f"{original_url}{sep}auto=compress&cs=tinysrgb&fit=crop&w={w}&h={h}"


def download(url: str, dest_path: str) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Scenario/1.0 (lesscenarios.fr)"})
    with urllib.request.urlopen(req, timeout=20) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())


def wide_crop_local(src_path: str, dest_path: str, w: int = 1600, h: int = 900) -> None:
    """Recadrage large local via Pillow — utilisé pour Pixabay (pas de
    recadrage arbitraire par URL, voir docstring du module)."""
    from PIL import Image, ImageOps
    im = Image.open(src_path).convert("RGB")
    wide = ImageOps.fit(im, (w, h), method=Image.LANCZOS, centering=(0.5, 0.45))
    wide.save(dest_path, "JPEG", quality=90)


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

    source = (credit_entry or {}).get("source", "pexels")
    wide_ok = False
    dest_wide = os.path.join(out_dir, f"{args.date}-wide.jpg")

    if source == "pixabay":
        raw_file = (credit_entry or {}).get("raw_file")
        if raw_file and os.path.isfile(raw_file):
            try:
                wide_crop_local(raw_file, dest_wide)
                wide_ok = True
                print(f"Recadrage large (article) produit localement : {dest_wide}")
            except Exception as e:
                print(f"  (pas de recadrage large -wide.jpg : échec recadrage local, {e} — "
                      "pas bloquant, l'image carrée reste disponible)", file=sys.stderr)
        else:
            print("  (pas de recadrage large -wide.jpg : raw_file absent ou introuvable — "
                  "normal si credits.json a été généré/modifié à la main)", file=sys.stderr)
    else:  # pexels
        original_url = (credit_entry or {}).get("original_url")
        if original_url:
            try:
                download(crop_url(original_url, 1600, 900), dest_wide)
                wide_ok = True
                print(f"Recadrage large (article) téléchargé : {dest_wide}")
            except Exception as e:
                print(f"  (pas de recadrage large -wide.jpg : échec téléchargement, {e} — "
                      "pas bloquant, l'image carrée reste disponible)", file=sys.stderr)
        else:
            print("  (pas de recadrage large -wide.jpg : original_url absent de la fiche de "
                  "provenance — normal pour un candidat trouvé avant le 10 août)", file=sys.stderr)

    print(
        "\nÀ faire ensuite à la main :\n"
        f"  1. feed.xml : <enclosure url=\"https://lesscenarios.fr/assets/social/topic-images/{args.date}.jpg\" type=\"image/jpeg\" length=\"0\"/>\n"
        f"  2. index.html + archives/{args.date}.html : meta og:image / twitter:image / JSON-LD \"image\" -> "
        f"https://lesscenarios.fr/assets/social/topic-images/{args.date}.jpg\n"
        + (f"  3. index.html : bloc image en tête d'article -> "
           f"https://lesscenarios.fr/assets/social/topic-images/{args.date}-wide.jpg\n"
           if wide_ok else
           "  3. Pas de -wide.jpg disponible : pas de bloc image en tête d'article ce jour-là "
           "(comportement normal, pas bloquant).\n")
        + "  4. Vérifier visuellement (Playwright) avant de pousser."
    )


if __name__ == "__main__":
    main()
