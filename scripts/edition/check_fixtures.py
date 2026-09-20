"""
Vérifie que le brief de référence (`editorial-briefs/2026-09-20.json`,
cité comme exemple par `docs/routine-brief-format.md` § Exemple, et
valeur par défaut de `.github/workflows/edition.yml`) et sa fixture
`--dry-run` associée (`scripts/edition/fixtures/2026-09-20-dry-run.json`)
restent conformes au schéma réellement vérifié par
`generate_daily_edition.py` — jamais une resaisie séparée des règles,
seulement un appel direct à `validate_brief()`/`validate_content_schema()`.

Root cause de l'incident du 20 septembre 2026 (édition #59, run
`edition.yml`) : `sujet.complexite` a été rendu obligatoire le 16
septembre, `phrase_a_retenir`/`phrase_a_retenir_stat` le 19 — mais rien
ne vérifiait que ce brief/fixture de référence suivait ces changements
de schéma. Le premier signal a été un run réel du workflow (coût en
tokens en plus de l'échec) plutôt qu'un échec rapide en CI. Ce script
comble ce trou : il tourne sur chaque push/PR touchant
`generate_daily_edition.py`, `editorial-briefs/` ou `scripts/edition/fixtures/`
(voir `.github/workflows/edition-checks.yml`), sans appel réseau ni clé
API — seulement les mêmes validations Python que la génération réelle.

Usage :
    python3 scripts/edition/check_fixtures.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import json

from generate_daily_edition import validate_brief, validate_content_schema

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BRIEFS_DIR = REPO_ROOT / "editorial-briefs"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def check_fixture_pair(fixture_path):
    date_str = fixture_path.name.removesuffix("-dry-run.json")
    # Le brief associé vit normalement à côté de sa fixture, dans
    # scripts/edition/fixtures/ (voir la relocation du 20 septembre 2026,
    # docs/ARCHITECTURE.md : un brief-exemple ne doit jamais squatter le
    # chemin daté réel qu'utilise le pipeline de production pour publier
    # l'édition du jour) — repli sur editorial-briefs/{date}.json pour un
    # ancien brief réel qui aurait une fixture associée.
    brief_path = FIXTURES_DIR / f"{date_str}.json"
    if not brief_path.exists():
        brief_path = BRIEFS_DIR / f"{date_str}.json"
    errors = []

    if not brief_path.exists():
        return [f"{fixture_path.name} : brief correspondant introuvable ({FIXTURES_DIR / f'{date_str}.json'} ou {brief_path})"]

    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    brief_errors = validate_brief(brief)
    if brief_errors:
        errors += [f"{brief_path.name} : {e}" for e in brief_errors]
        return errors  # inutile de valider le contenu contre un brief déjà invalide

    content = json.loads(fixture_path.read_text(encoding="utf-8"))
    content_errors = validate_content_schema(content, brief)
    errors += [f"{fixture_path.name} : {e}" for e in content_errors]
    return errors


def main():
    fixtures = sorted(FIXTURES_DIR.glob("*-dry-run.json"))
    if not fixtures:
        print("[check_fixtures] aucune fixture --dry-run trouvée, rien à vérifier")
        return

    all_errors = []
    for fixture_path in fixtures:
        all_errors += check_fixture_pair(fixture_path)

    if all_errors:
        print("[check_fixtures] ÉCHEC — brief(s)/fixture(s) désynchronisé(s) du schéma :", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[check_fixtures] OK — {len(fixtures)} fixture(s) conforme(s) au schéma actuel")


if __name__ == "__main__":
    main()
