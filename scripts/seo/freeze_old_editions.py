#!/usr/bin/env python3
"""Fige les éditions déjà publiées sur la version figée du script des scénarios.

Règle du propriétaire (3 octobre 2026) : « on ne change que l'édition du jour et les futures ». Les pages
d'édition chargent assets/scenarios-reader.js ; ce script fait pointer toutes les éditions SAUF la plus
récente de chaque dossier (archives/ et en/archives/) vers assets/scenarios-reader.v1.js (copie figée).
Ainsi, modifier scenarios-reader.js ne change que l'édition du jour et les suivantes.

Idempotent ; lancé par post-edition.yml et translate-en.yml après la publication, sans jamais les bloquer.
Utilisation : python3 scripts/seo/freeze_old_editions.py [--dry-run]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")
LIVE = re.compile(r'(src="(?:\.\./)*assets/scenarios-reader)\.js"')


def main(dry=False):
    changed = 0
    for folder in ("archives", "en/archives"):
        editions = sorted(p for p in (ROOT / folder).glob("*.html") if DATED.match(p.name))
        for path in editions[:-1]:  # toutes sauf la plus récente
            text = path.read_text(encoding="utf-8")
            new, n = LIVE.subn(r'\1.v1.js"', text)
            if n and not dry:
                path.write_text(new, encoding="utf-8")
            changed += 1 if n else 0
    print(f"{changed} édition(s) {'à figer' if dry else 'figée(s)'}.")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
