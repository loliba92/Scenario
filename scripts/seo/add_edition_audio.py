#!/usr/bin/env python3
"""Ajoute la balise <script defer src=".../assets/edition-audio.js"> après celle de scenarios-reader.js
dans les pages qui chargent la version évolutive de la lecture des scénarios : gabarits (index.html, en/index.html,
preview.html) et dernières éditions. Les nouvelles éditions reprennent la balise du gabarit ; ce script rattrape
les pages déjà publiées. Idempotent. Les éditions figées (scenarios-reader.v1.js) ne sont pas touchées.
Utilisation : python3 scripts/seo/add_edition_audio.py [--dry-run]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG_RE = re.compile(r'(<script (defer(?:="")?) src="((?:\.\./)*)assets/scenarios-reader\.js"></script>)')


def main(dry=False):
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("node_modules/", "test/", "docs/")):
            continue
        text = path.read_text(encoding="utf-8")
        if "edition-audio" in text:
            continue
        m = TAG_RE.search(text)
        if not m:
            continue
        new = text[:m.end()] + f'\n<script {m.group(2)} src="{m.group(3)}assets/edition-audio.js"></script>' + text[m.end():]
        if not dry:
            path.write_text(new, encoding="utf-8")
        changed += 1
    print(f"{changed} page(s) {'à modifier' if dry else 'modifiée(s)'}.")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
