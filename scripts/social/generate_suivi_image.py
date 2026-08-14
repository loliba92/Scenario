#!/usr/bin/env python3
"""
Génère l'image carrée (1080x1080) qui accompagne l'annonce d'une mise à
jour de suivi (Telegram/LinkedIn/Instagram/Facebook, voir feed-suivi.xml
et docs/ARCHITECTURE.md § « Annonce des mises à jour sur Telegram/
LinkedIn »), à partir de scripts/social/suivi-template.html.

Avant le 14 août, l'<enclosure> de feed-suivi.xml pointait directement
vers la photo Pexels brute (assets/social/topic-images/suivi-
{sujet}.jpg), sans aucune incrustation — juste la photo, sans logo ni
texte. Retour utilisateur du 14 août : pas assez "clean", il faut le
logo + un petit tag "mise à jour" + la conclusion. Ce script compose
donc logo + pastille + sujet + conclusion sur cette même photo (jamais
retouchée elle-même, voir generate_pub_image.py pour la même logique de
composition), avec un fichier de sortie séparé — la photo brute reste
disponible telle quelle pour d'autres usages.

Usage:
    python3 scripts/social/generate_suivi_image.py \\
        --data data.json \\
        --output assets/social/suivi/fifa-infantino-v1.png \\
        --template scripts/social/suivi-template.html \\
        --photo assets/social/topic-images/suivi-fifa-infantino.jpg

data.json:
{
  "topic": "FIFA : la crise autour d'Infantino",
  "conclusion": "📉 Favorable en net recul, -10 points (10%) — le scénario où Infantino regagne la confiance de l'UEFA recule fortement, la méfiance dure progresse à 50%."
}

"conclusion" = reprendre tel quel le texte déjà écrit dans <comments> de
l'item feed-suivi.xml correspondant (même phrase, ne pas en réécrire une
nouvelle) — voir docs/ARCHITECTURE.md pour le format de cet item.
"""
import argparse
import base64
import html
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Chemin vers le JSON (topic + conclusion)")
    ap.add_argument("--output", required=True, help="Chemin du PNG de sortie")
    ap.add_argument("--template", required=True, help="Chemin du template HTML")
    ap.add_argument(
        "--photo", required=True,
        help="Photo de fond — assets/social/topic-images/suivi-{sujet}.jpg, "
             "jamais régénérée/re-choisie ici (voir docstring).",
    )
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    template = Path(args.template).read_text(encoding="utf-8")

    topic_html = html.escape(data["topic"])
    conclusion_html = html.escape(data["conclusion"])

    photo_path = Path(args.photo)
    ext = photo_path.suffix.lstrip(".").lower() or "jpeg"
    if ext == "jpg":
        ext = "jpeg"
    data_uri = f"data:image/{ext};base64,{base64.b64encode(photo_path.read_bytes()).decode()}"

    final_html = (
        template
        .replace("__PHOTO_SRC__", data_uri)
        .replace("__TOPIC__", topic_html)
        .replace("__CONCLUSION__", conclusion_html)
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
    size_bytes = output_path.stat().st_size
    print(f"OK: {output_path} ({size_bytes} octets)")


if __name__ == "__main__":
    main()
