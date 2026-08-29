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
  "context": "Infantino peut-il tenir jusqu'au bout de son mandat ?",
  "scenarios": [
    {"kind": "favorable", "label": "Infantino regagne la confiance"},
    {"kind": "stable", "label": "La méfiance dure, il reste en poste"},
    {"kind": "degrade", "label": "L'UEFA déclenche la motion de défiance"}
  ]
}

Champs "kind" attendus : favorable | stable | degrade (détermine la
couleur, la flèche ↑/→/↓, et le mot affiché en toutes lettres à côté de
la flèche — ajouté le 24 août, retour utilisateur : la flèche colorée
seule ne "parle" qu'à qui connaît déjà le code du site). Pas de
pourcentages dans l'image — c'est volontaire (effet teaser vers le
lien en bio).

"context" : UNE SEULE question simple et factuelle affichée sous le
titre — jamais une phrase de mise en scène qui reformule déjà les 3
scénarios (ils sont juste en dessous, dans l'encart : redondant, et
"fait trop d'image"). Recycler h2.section-title de l'édition (déjà
écrit comme reformulation courte et pédagogique de la question, donc
déjà calibré pour ça) plutôt que la meta description/og:description
(trop narrative) ou la question posée brute (trop longue) — voir
docs/routine-prompt.md. Structure finale : titre → question simple →
les 3 réponses possibles (scénarios). Remplace depuis le 24 août les
anciens champs séparés "hook" (accroche dorée) + "context" (ligne de
contexte grise) — retour utilisateur : deux légendes de couleurs
différentes l'une sous l'autre "fait brouillon" ; un seul paragraphe,
une seule couleur. Voir docs/routine-prompt.md pour la méthode de
rédaction, y compris pour les "label" des scénarios : wording simple,
direct, sans métaphore littéraire, compréhensible par quelqu'un qui ne
connaît rien au sujet (le teaser doit se suffire à lui-même,
contrairement aux titres de cartes du site qui vivent à côté du
paragraphe "why"). Toujours vérifier le rendu à taille mobile réelle
(~350px de large) avant de considérer un wording comme acceptable.

Champ optionnel "delta" (ajouté le 12 août, plusieurs itérations
visuelles le même jour — voir docs/ARCHITECTURE.md) : carte "France
Impact" en haut à droite de l'image, ex. {"direction": "negatif",
"intensity": 1, "label": "Léger négatif"}. "direction" attendu :
positif | negatif (jamais neutre) ; "intensity" 1/2/3 = léger/assez/
très (mêmes seuils que docs/routine-prompt.md, ±0,10/±0,30/±0,50) —
détermine le nombre d'étoiles pleines sur 3. "label" affiché tel quel
en toutes lettres sous les étoiles. Purement décoratif — si absent du
JSON, disparaît silencieusement (même repli que --photo), aucune
erreur. Supporté uniquement par instagram-photo-template.html (le
gabarit par défaut n'a pas le marqueur __DELTA_BADGE__, budget vertical
déjà tendu par le titre 1-3 lignes — voir docs/ARCHITECTURE.md).

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
# Mot affiché à côté de la flèche (ajouté le 24 août, retour utilisateur :
# la flèche colorée seule ne "parle" qu'à qui connaît déjà le code du
# site — voir docs/routine-prompt.md).
KIND_LABELS = {"favorable": "Favorable", "stable": "Stable", "degrade": "Dégradé"}
# Variante anglaise (ajoutée le 29 août pour les images sociales EN,
# voir docs/routine-en-prompt.md) — sélectionnée via --lang en.
KIND_LABELS_EN = {"favorable": "Favorable", "stable": "Stable", "degrade": "Degraded"}

# Étoile pleine, path standard 5 branches (viewBox 24x24), réutilisée
# pour les 3 crans d'intensité de "France Impact" (voir build_delta_badge).
_STAR_PATH = "M12 2 L14.9 8.6 L22 9.3 L16.5 14.1 L18.2 21 L12 17.3 L5.8 21 L7.5 14.1 L2 9.3 L9.1 8.6 Z"

_DELTA_FLAG_SVG = (
    '<svg class="delta-flag" viewBox="0 0 21 15" width="20" height="14" aria-hidden="true">'
    '<rect x="0" y="0" width="7" height="15" fill="#2a4d8f"/>'
    '<rect x="7" y="0" width="7" height="15" fill="#ece7da"/>'
    '<rect x="14" y="0" width="7" height="15" fill="#bd6248"/>'
    '</svg>'
)


# Couleurs figées (hex, pas var()) : un attribut SVG fill="var(--x)" ne
# se résout pas de façon fiable hors d'un attribut style — testé, voir
# docs/ARCHITECTURE.md. Doit rester synchronisé avec :root du template.
_FAVORABLE_HEX = "#5e9c78"
_DEGRADE_HEX = "#bd6248"
_STAR_EMPTY = "rgba(236,231,218,0.18)"

_STAR_W = 24
_STAR_GAP = 4


def _delta_scale_positions():
    """x de chaque étoile sur les 6, espacement régulier — pas de
    séparation visuelle particulière entre la 3e et la 4e (retour
    utilisateur : inutile)."""
    xs = []
    x = 0
    for i in range(6):
        xs.append(x)
        x += _STAR_W + _STAR_GAP
    return xs


def build_delta_badge(delta, lang="fr"):
    """Carte "France Impact" : petit drapeau (icône de label, pas un
    fond plein cadre — évite le côté trop identitaire du triangle
    tricolore précédent, voir docs/ARCHITECTURE.md) + une échelle fixe
    de 6 étoiles remplies de façon CUMULATIVE de gauche à droite (pas
    une seule étoile isolée + flèche — retour utilisateur explicite :
    position 1 = très défavorable ... position 6 = très favorable).
    **Couleur des étoiles pleines = sens du jour, pas la position** :
    toutes rouges si négatif, toutes vertes si favorable (retour
    utilisateur explicite : pas de mélange rouge+vert sur un seul
    score). **Caption "Notre évaluation" ajoutée devant le mot**
    (retour utilisateur : ambiguïté possible entre "c'est un fait" et
    "c'est notre appréciation pondérée" — jamais laisser croire que
    France Impact énonce une vérité plutôt qu'une estimation). Même
    recette de carte que .essentiel-box/.list-box (fond surface,
    bordure, ombre légère)."""
    direction = delta["direction"]
    intensity = max(1, min(3, int(delta.get("intensity", 1))))
    label = html.escape(delta["label"])

    xs = _delta_scale_positions()
    total_w = xs[-1] + _STAR_W
    total_h = _STAR_W

    # position 1..6 sur l'échelle : 1-3 = défavorable très/assez/léger,
    # 4-6 = favorable léger/assez/très. Toutes les étoiles <= position
    # sont pleines, dans la couleur du sens du jour (pas mélangées) ; le
    # reste est gris.
    position = (4 - intensity) if direction == "negatif" else (3 + intensity)
    filled_hex = _DEGRADE_HEX if direction == "negatif" else _FAVORABLE_HEX

    stars = []
    for i, x in enumerate(xs):
        fill = filled_hex if (i + 1) <= position else _STAR_EMPTY
        stars.append(f'<g transform="translate({x},0)"><path d="{_STAR_PATH}" fill="{fill}"/></g>')

    scale_svg = (
        f'<svg class="delta-mark-scale" viewBox="0 0 {total_w} {total_h}" '
        f'width="{total_w}" height="{total_h}">{"".join(stars)}</svg>'
    )

    caption = "Our assessment" if lang == "en" else "Notre évaluation"
    return f'''<div class="delta-mark" data-kind="{html.escape(direction)}">
      <div class="delta-mark-text">
        <span class="delta-mark-label">{_DELTA_FLAG_SVG} France Impact</span>
        {scale_svg}
        <span class="delta-mark-caption">{caption}</span>
        <span class="delta-mark-word">{label}</span>
      </div>
    </div>'''


def build_scenario_rows(scenarios, lang="fr"):
    rows = []
    for s in scenarios:
        kind = s["kind"]
        arrow = ARROWS.get(kind, "→")
        labels = KIND_LABELS_EN if lang == "en" else KIND_LABELS
        kind_word = labels.get(kind, kind.capitalize())
        label = html.escape(s["label"])
        rows.append(
            f'<div class="scenario-row" data-kind="{kind}">'
            f'<span class="arrow">{arrow}</span>'
            f'<span class="kind-word">{kind_word}</span>'
            f'<span class="label">{label}</span>'
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
    ap.add_argument(
        "--lang", default="fr", choices=["fr", "en"],
        help="Langue des libellés générés par ce script (KIND_LABELS, "
             "France Impact) — ajouté le 29 août pour les images sociales "
             "EN, voir docs/routine-en-prompt.md. N'affecte PAS title/"
             "context/scenario[].label : ces champs viennent déjà traduits "
             "du JSON --data. Utiliser un --template *-en.html en plus "
             "(bandeau/tagline en dur dans le gabarit, pas piloté par ce "
             "flag).",
    )
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    template = Path(args.template).read_text(encoding="utf-8")

    title_html = html.escape(data["title"])
    rows_html = build_scenario_rows(data["scenarios"], lang=args.lang)

    final_html = (
        template
        .replace("__TITLE__", title_html)
        .replace("__SCENARIO_ROWS__", rows_html)
    )

    if "__CONTEXT__" in final_html:
        if "context" not in data:
            sys.exit("ERREUR : le template attend un paragraphe de contexte (__CONTEXT__) mais le JSON n'a pas de champ \"context\".")
        final_html = final_html.replace("__CONTEXT__", html.escape(data["context"]))

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
        badge_html = build_delta_badge(delta, lang=args.lang) if delta else ""
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
