#!/usr/bin/env python3
"""
Génère l'image Instagram carrée (1080x1080) pour l'édition du jour,
à partir de scripts/social/instagram-template.html.

Utilisé par la routine éditoriale quotidienne : après avoir écrit
l'édition et construit l'item de feed.xml, générer cette image, la
committer dans assets/social/instagram/{date}.png, et référencer son
URL dans un tag <enclosure> du feed.xml (voir docs/ARCHITECTURE.md).

Usage:
    python3 scripts/social/generate_instagram_image.py \\
        --data data.json \\
        --output assets/social/instagram/2026-08-08.png \\
        --template scripts/social/instagram-template.html

data.json:
{
  "title": "FIFA : la présidence d'Infantino vacille",
  "hook": "Le vote de défiance approche : Infantino peut-il tenir ?",
  "scenarios": [
    {"kind": "favorable", "label": "Infantino regagne la confiance"},
    {"kind": "stable", "label": "La méfiance dure, il reste en poste"},
    {"kind": "degrade", "label": "L'UEFA déclenche la motion de défiance"}
  ]
}

Champs "kind" attendus : favorable | stable | degrade (détermine la
couleur et la flèche ↑/→/↓). Pas de pourcentages dans l'image — c'est
volontaire (effet teaser vers le lien en bio).

Champ optionnel "delta" (ajouté le 12 août) : badge Δ France en bas de
l'image, ex. {"direction": "negatif", "label": "Léger négatif"}.
"direction" attendu : positif | negatif (jamais neutre, voir
docs/routine-prompt.md). Purement décoratif — si absent du JSON, le
badge disparaît silencieusement (même repli que --photo), aucune
erreur. Supporté uniquement par instagram-photo-template.html (marge
suffisante) — le gabarit par défaut (fond dégradé, sans photo) n'a pas
le marqueur __DELTA_BADGE__ : budget vertical déjà tendu par le titre
1-3 lignes, testé, tout ajout y fait chevaucher le CTA.

"hook" (ajouté le 11 août, retour utilisateur) : une accroche courte
(≤ 12 mots, une seule ligne à l'écran), affichée sous le titre, en doré.
Ce n'est PAS la question posée du site (bien trop longue pour tenir
lisiblement — c'est justement ce qui avait été retiré le 7 août) : une
phrase distincte, courte et percutante, écrite spécifiquement pour cette
image, qui donne juste assez de contexte pour qu'un lecteur qui scrolle
sans lire la légende ni cliquer le lien en bio comprenne l'enjeu.
Toujours vérifier le rendu à taille mobile réelle (~350px de large)
avant de considérer une accroche comme acceptable.

Option --photo (ajoutée le 9 août) : incruste titre + scénarios sur une
vraie photo Pexels du sujet du jour (voir fetch_topic_image.py /
use_topic_image.py) au lieu du fond dégradé uni, avec
scripts/social/instagram-photo-template.html (dégradés haut/bas +
encart noir pour les scénarios, mêmes couleurs que d'habitude). Purement
optionnel et manuel — la routine quotidienne automatique n'appelle
jamais --photo, elle continue d'utiliser exactement le même template et
comportement qu'avant. Ne pas câbler dans docs/routine-prompt.md ni les
blueprints Make tant que ce n'est pas validé sur plusieurs éditions.
"""
import argparse
import base64
import html
import json
import sys
from pathlib import Path

ARROWS = {"favorable": "↑", "stable": "→", "degrade": "↓"}

# Flèche découpée dans le disque tricolore du badge Δ France (voir
# build_delta_badge) — chevron + hampe, 64x64, pointe vers le haut ou
# le bas selon le sens du score.
_DELTA_ARROW_PATHS = {
    "positif": "M32,15 L46,31 L37,31 L37,49 L27,49 L27,31 L18,31 Z",
    "negatif": "M32,49 L46,33 L37,33 L37,15 L27,15 L27,33 L18,33 Z",
}


def build_delta_badge(delta):
    """Badge Δ France : disque tricolore (bleu/blanc/rouge) avec la
    flèche de sens directement découpée dedans (masque SVG, pas une
    icône posée à côté) — plus texte du mot en gros à côté."""
    direction = delta["direction"]
    arrow_path = _DELTA_ARROW_PATHS.get(direction, _DELTA_ARROW_PATHS["positif"])
    label = html.escape(delta["label"])
    return f'''<div class="delta-badge" data-kind="{html.escape(direction)}">
      <svg class="delta-badge-icon" viewBox="0 0 64 64" width="60" height="60">
        <defs>
          <clipPath id="deltaFlagClip"><circle cx="32" cy="32" r="30"/></clipPath>
          <mask id="deltaArrowCut">
            <rect width="64" height="64" fill="white"/>
            <path d="{arrow_path}" fill="black"/>
          </mask>
        </defs>
        <g clip-path="url(#deltaFlagClip)" mask="url(#deltaArrowCut)">
          <rect x="2" y="2" width="20" height="60" fill="#2a4d8f"/>
          <rect x="22" y="2" width="20" height="60" fill="#ece7da"/>
          <rect x="42" y="2" width="20" height="60" fill="#bd6248"/>
        </g>
        <circle class="delta-badge-ring" cx="32" cy="32" r="30" fill="none" stroke-width="3"/>
      </svg>
      <div class="delta-badge-text">
        <span class="delta-badge-label">Δ France</span>
        <span class="delta-badge-word">{label}</span>
      </div>
    </div>'''


def build_scenario_rows(scenarios):
    rows = []
    for s in scenarios:
        kind = s["kind"]
        arrow = ARROWS.get(kind, "→")
        label = html.escape(s["label"])
        rows.append(
            f'<div class="scenario-row" data-kind="{kind}">'
            f'<span class="arrow">{arrow}</span><span class="label">{label}</span>'
            f'</div>'
        )
    return "\n    ".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Chemin vers le JSON (title + scenarios)")
    ap.add_argument("--output", required=True, help="Chemin du PNG de sortie")
    ap.add_argument("--template", required=True, help="Chemin du template HTML")
    ap.add_argument(
        "--photo", default=None,
        help="Optionnel : chemin vers une photo (ex. assets/social/topic-images/"
             "{date}.jpg) à incruster en fond, à la place du dégradé uni. "
             "Nécessite un template avec le marqueur __PHOTO_SRC__, ex. "
             "scripts/social/instagram-photo-template.html.",
    )
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    template = Path(args.template).read_text(encoding="utf-8")

    title_html = html.escape(data["title"])
    rows_html = build_scenario_rows(data["scenarios"])

    final_html = (
        template
        .replace("__TITLE__", title_html)
        .replace("__SCENARIO_ROWS__", rows_html)
    )

    if "__HOOK__" in final_html:
        if "hook" not in data:
            sys.exit("ERREUR : le template attend une accroche (__HOOK__) mais le JSON n'a pas de champ \"hook\".")
        final_html = final_html.replace("__HOOK__", html.escape(data["hook"]))

    if "__PHOTO_SRC__" in final_html:
        if not args.photo:
            sys.exit("ERREUR : le template attend une photo (__PHOTO_SRC__) mais --photo n'a pas été fourni.")
        photo_path = Path(args.photo)
        ext = photo_path.suffix.lstrip(".").lower() or "jpeg"
        if ext == "jpg":
            ext = "jpeg"
        data_uri = f"data:image/{ext};base64,{base64.b64encode(photo_path.read_bytes()).decode()}"
        final_html = final_html.replace("__PHOTO_SRC__", data_uri)
    elif args.photo:
        print("ATTENTION : --photo fourni mais le template n'a pas de marqueur "
              "__PHOTO_SRC__ — ignoré, image générée sans photo.", file=sys.stderr)

    if "__DELTA_BADGE__" in final_html:
        delta = data.get("delta")
        badge_html = build_delta_badge(delta) if delta else ""
        final_html = final_html.replace("__DELTA_BADGE__", badge_html)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_html = output_path.with_suffix(".tmp.html")
    tmp_html.write_text(final_html, encoding="utf-8")

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        page.goto(f"file://{tmp_html.resolve()}")
        page.wait_for_timeout(300)
        page.screenshot(path=str(output_path))
        browser.close()

    tmp_html.unlink()
    size_bytes = output_path.stat().st_size
    print(f"OK: {output_path} ({size_bytes} octets)")


if __name__ == "__main__":
    sys.exit(main())
