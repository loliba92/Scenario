#!/usr/bin/env python3
"""
Génère l'image carrée (1080x1080) pour un post "pub" hebdomadaire —
manifeste du projet ou citation sur le hasard/l'incertitude, voir
docs/pub-messages.md pour la banque de messages et docs/routine-pub-
prompt.md pour la routine qui appelle ce script chaque semaine.

Même gabarit visuel que scripts/social/instagram-template.html (masthead,
couleurs, polices) pour rester reconnaissable comme un post du même
compte, mais contenu texte pur — jamais de titre d'article ni de
scénarios chiffrés ici.

Usage:
    python3 scripts/social/generate_pub_image.py \\
        --data data.json \\
        --output assets/social/pub/2026-08-16.png \\
        --template scripts/social/pub-template.html

data.json:
{
  "eyebrow": "POURQUOI SCÉNARIO",
  "message": "Gratuit. Indépendant. Ni de gauche ni de droite.",
  "attribution": "",
  "cta": "👉 Abonne-toi, c'est gratuit"
}

"attribution" et "cta" sont optionnels (chaîne vide si absents) —
"attribution" sert pour les citations (ex. "— Sénèque"), jamais utilisé
pour un message manifeste.
"""
import argparse
import base64
import html
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Chemin vers le JSON (eyebrow + message)")
    ap.add_argument("--output", required=True, help="Chemin du PNG de sortie")
    ap.add_argument("--template", required=True, help="Chemin du template HTML")
    ap.add_argument(
        "--photo", default=None,
        help="Optionnel : photo de fond (voir __PHOTO_SRC__ dans le template) — "
             "peut changer chaque semaine, contrairement au fond uni.",
    )
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    template = Path(args.template).read_text(encoding="utf-8")

    eyebrow_html = html.escape(data.get("eyebrow", ""))
    # Le message peut contenir des sauts de ligne volontaires (\n dans le
    # JSON) pour contrôler la coupure sur l'image plutôt que de laisser
    # le navigateur couper n'importe où sur une phrase longue. **mot**
    # met le mot en évidence (couleur d'accent) — repris du même besoin
    # que build_delta_badge : un mot-clé sur lequel accrocher le regard.
    def _format_message(raw):
        escaped = html.escape(raw)
        parts = escaped.split("**")
        out = []
        for idx, part in enumerate(parts):
            out.append(f'<span class="hl">{part}</span>' if idx % 2 == 1 else part)
        return "".join(out).replace("\n", "<br>")

    message_html = _format_message(data["message"])
    attribution_html = html.escape(data.get("attribution", ""))
    cta_html = html.escape(data.get("cta", ""))

    accent_html = html.escape(data.get("accent", "manifeste"))

    final_html = (
        template
        .replace("__EYEBROW__", eyebrow_html)
        .replace("__MESSAGE__", message_html)
        .replace("__ATTRIBUTION__", attribution_html)
        .replace("__CTA__", cta_html)
        .replace("__ACCENT__", accent_html)
    )

    if "__PHOTO_SRC__" in final_html:
        if not args.photo:
            raise SystemExit("ERREUR : le template attend une photo (__PHOTO_SRC__) mais --photo n'a pas été fourni.")
        photo_path = Path(args.photo)
        ext = photo_path.suffix.lstrip(".").lower() or "jpeg"
        if ext == "jpg":
            ext = "jpeg"
        data_uri = f"data:image/{ext};base64,{base64.b64encode(photo_path.read_bytes()).decode()}"
        final_html = final_html.replace("__PHOTO_SRC__", data_uri)

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
