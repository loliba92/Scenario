#!/usr/bin/env python3
"""Ajoute la balise <script defer src=".../assets/scenarios-reader.js"> après celle de bottom-nav.js
dans toutes les pages qui contiennent la section des scénarios (éditions, aperçu, accueil FR/EN).

Les nouvelles éditions reprennent cette balise du gabarit (index.html) ; ce script sert à rattraper
les pages déjà publiées. Idempotent : une page qui a déjà la balise n'est pas modifiée.
Utilisation : python3 scripts/seo/add_scenarios_reader.py [--dry-run]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG_RE = re.compile(r'(<script (defer(?:="")?) src="((?:\.\./)*)assets/bottom-nav\.js"></script>)')


def main(dry=False):
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("node_modules/", "test/", "docs/")):
            continue
        text = path.read_text(encoding="utf-8")
        if 'class="scenarios"' not in text or "scenarios-reader.js" in text:
            continue
        m = TAG_RE.search(text)
        if not m:
            continue
        new = text[:m.end()] + f'\n<script {m.group(2)} src="{m.group(3)}assets/scenarios-reader.js"></script>' + text[m.end():]
        if not dry:
            path.write_text(new, encoding="utf-8")
        changed += 1
    print(f"{changed} page(s) {'à modifier' if dry else 'modifiée(s)'}.")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
