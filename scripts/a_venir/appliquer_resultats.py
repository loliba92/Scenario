#!/usr/bin/env python3
"""Fusionne les résultats ACCEPTÉS (verifier_resultats.py) dans data/a-venir.json et met à jour le journal des essais.

Ne remplace jamais un résultat déjà présent ; revalide chaque résultat (verifier_resultat) avant écriture. Idempotent.
Usage : python3 scripts/a_venir/appliquer_resultats.py patch.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_a_venir as g  # noqa: E402

DONNEES = g.RACINE / "data" / "a-venir.json"
JOURNAL = g.RACINE / "data" / "a-venir-journal.json"


def appliquer(donnees, journal, patch):
    """Retourne (donnees, journal, nombre_de_résultats_ajoutés)."""
    n = 0
    par_id = {r["id"]: r for r in donnees["rendez_vous"]}
    for rid, res in patch.get("resultats", {}).items():
        r = par_id.get(rid)
        if r is None or "resultat" in r:
            continue
        r["resultat"] = res
        g.verifier_resultat(r)          # lève ValueError : un résultat invalide n'est jamais écrit
        n += 1
    journal.update(patch.get("journal", {}))
    return donnees, journal, n


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    patch = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    donnees = json.loads(DONNEES.read_text(encoding="utf-8"))
    journal = json.loads(JOURNAL.read_text(encoding="utf-8")) if JOURNAL.exists() else {}
    donnees, journal, n = appliquer(donnees, journal, patch)
    DONNEES.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JOURNAL.write_text(json.dumps(journal, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{n} résultat(s) ajouté(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
