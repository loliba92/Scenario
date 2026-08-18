#!/usr/bin/env python3
"""
Génère l'image carrée (1080x1080) du récap hebdomadaire "On refait le
scénario de la semaine" (voir docs/routine-hebdo-prompt.md) — utilisée
comme og:image/twitter:image de hebdo/{date}.html et, si besoin, comme
image de partage social du récap.

Contrairement à generate_pub_image.py et generate_instagram_image.py,
la PHOTO et le GABARIT sont fixés en dur ci-dessous (retour utilisateur,
18 août : "une belle image de paysage, toujours la même... plus simple,
tu écris en dur l'image qu'on prend") — jamais de recherche Pexels ni de
choix à faire chaque semaine, contrairement aux photos par sujet/
catégorie. Crédit de la photo : assets/social/hebdo-photo-credit.json.

Usage:
    python3 scripts/social/generate_hebdo_image.py \\
        --data data.json \\
        --output assets/social/hebdo/2026-08-16.png

data.json:
{
  "weekrange": "11 → 17 août",
  "message": "Version condensée de la conclusion de la semaine (~150-160
              caractères, même texte que la meta description — voir
              docs/routine-hebdo-prompt.md, étape 3).",
  "cta": "👉 Lire le récap complet"
}

"cta" est optionnel (chaîne vide si absent).
"""
import argparse
import base64
import html
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR / "hebdo-template.html"
PHOTO_PATH = SCRIPT_DIR.parent.parent / "assets" / "social" / "hebdo-bg.jpg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Chemin vers le JSON (weekrange + message + cta optionnel)")
    ap.add_argument("--output", required=True, help="Chemin du PNG de sortie")
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    weekrange_html = html.escape(data["weekrange"])
    message_html = html.escape(data["message"])
    cta_html = html.escape(data.get("cta", ""))

    data_uri = f"data:image/jpeg;base64,{base64.b64encode(PHOTO_PATH.read_bytes()).decode()}"

    final_html = (
        template
        .replace("__PHOTO_SRC__", data_uri)
        .replace("__WEEKRANGE__", weekrange_html)
        .replace("__MESSAGE__", message_html)
        .replace("__CTA__", cta_html)
    )

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
    print(f"OK : {output_path}")


if __name__ == "__main__":
    main()
