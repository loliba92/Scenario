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
  "question": "🤔 Infantino peut-il regagner la confiance de l'UEFA avant l'élection de mars 2027 ?",
  "scenarios": [
    {"kind": "favorable", "label": "Infantino regagne la confiance"},
    {"kind": "stable", "label": "La méfiance dure, il reste en poste"},
    {"kind": "degrade", "label": "L'UEFA déclenche la motion de défiance"}
  ]
}

Champs "kind" attendus : favorable | stable | degrade (détermine la
couleur et la flèche ↑/→/↓). Pas de pourcentages dans l'image — c'est
volontaire (effet teaser vers le lien en bio).
"""
import argparse
import html
import json
import sys
from pathlib import Path

ARROWS = {"favorable": "↑", "stable": "→", "degrade": "↓"}


def build_scenario_rows(scenarios):
    rows = []
    for s in scenarios:
        kind = s["kind"]
        arrow = ARROWS.get(kind, "→")
        label = html.escape(s["label"])
        rows.append(
            f'<div class="scenario-row" data-kind="{kind}">'
            f'<span class="arrow">{arrow}</span>{label}'
            f'</div>'
        )
    return "\n    ".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Chemin vers le JSON (title + question + scenarios)")
    ap.add_argument("--output", required=True, help="Chemin du PNG de sortie")
    ap.add_argument("--template", required=True, help="Chemin du template HTML")
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    template = Path(args.template).read_text(encoding="utf-8")

    title_html = html.escape(data["title"])
    question_html = html.escape(data["question"])
    rows_html = build_scenario_rows(data["scenarios"])

    final_html = (
        template
        .replace("__TITLE__", title_html)
        .replace("__QUESTION__", question_html)
        .replace("__SCENARIO_ROWS__", rows_html)
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
    sys.exit(main())
