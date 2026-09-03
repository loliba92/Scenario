#!/usr/bin/env python3
"""
Récupère les lectures cumulées par édition depuis l'API GoatCounter et
régénère assets/data/reads.json — consommé par archives.html (colonne
"Lectures" + badge 🔥, voir scripts/seo/generate_archives_table.py,
variable reads_script) pour afficher, par édition, le nombre de lectures
cumulées depuis le lancement.

Historique (3 septembre 2026) : cette tâche était auparavant l'étape 3ter
de la routine Claude Code "Scénario — Audience" (docs/routine-audience-
prompt.md), hebdomadaire. Retour utilisateur : « ça se met pas à jour
tous les jours ? » — purement mécanique (appel API + agrégation, aucun
jugement éditorial requis), donc déplacée dans un GitHub Action
(.github/workflows/reads.yml) qui peut tourner beaucoup plus souvent
(toutes les heures) sans le coût d'une session LLM. La routine Claude
Code "Scénario — Audience" ne touche plus jamais ce fichier — voir la
note dans son propre prompt.

Le token GoatCounter (lecture seule) est lu depuis la variable
d'environnement GOATCOUNTER_TOKEN, jamais commité dans ce dépôt public —
fourni par le secret GitHub Actions du même nom (Settings → Secrets and
variables → Actions).

Usage (en local, pour tester) :
    GOATCOUNTER_TOKEN=xxx python3 scripts/seo/update_reads_json.py
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets" / "data" / "reads.json"
API_URL = "https://scenario.goatcounter.com/api/v0/stats/hits"

# Premier hit jamais enregistré sur le site — constante connue, jamais à
# redécouvrir dynamiquement (même valeur que docs/routine-audience-prompt.md).
START_DATE = "2026-07-29"

# Ne garder que les éditions quotidiennes françaises, jamais les autres
# chemins (accueil, archives.html, le-projet.html, suivi/, hebdo/, en/...)
# — même périmètre que le tableau top/flop du dashboard et la colonne
# "Lectures" de archives.html (qui n'affiche que les éditions FR).
PATH_RE = re.compile(r"^/archives/(\d{4}-\d{2}-\d{2})\.html(?:\?.*)?$")


def fetch_hits(token):
    # end = demain + 1 jour de marge, pas aujourd'hui — vérifié empiriquement
    # côté routine LLM (docs/routine-audience-prompt.md, étape 1) : end = date
    # du jour omettait les hits du jour lui-même dans la réponse.
    end = (date.today() + timedelta(days=2)).isoformat()
    url = f"{API_URL}?start={START_DATE}&end={end}&limit=200"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def aggregate(payload):
    """Additionne les lectures cumulées par édition (chemin /archives/{date}.html),
    variantes avec query string regroupées sous la même date — même règle que
    docs/routine-audience-prompt.md, étape 2."""
    totals = defaultdict(int)
    for hit in payload.get("hits", []):
        match = PATH_RE.match(hit.get("path", ""))
        if not match:
            continue
        iso_date = match.group(1)
        daily_total = sum(s.get("daily", 0) for s in hit.get("stats", []))
        totals[iso_date] += daily_total
    return dict(totals)


def main():
    token = os.environ.get("GOATCOUNTER_TOKEN")
    if not token:
        print("ERREUR : GOATCOUNTER_TOKEN absent de l'environnement.", file=sys.stderr)
        sys.exit(1)

    try:
        payload = fetch_hits(token)
    except urllib.error.HTTPError as e:
        print(f"ERREUR API GoatCounter : {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERREUR réseau : {e.reason}", file=sys.stderr)
        sys.exit(1)

    totals = aggregate(payload)

    # Ne jamais écraser des vraies données par un fichier vide en cas de
    # réponse API anormale (payload vide, format inattendu...) — mieux vaut
    # échouer bruyamment et garder l'ancien reads.json que publier du vide.
    if not totals:
        print("ERREUR : aucune lecture agrégée à partir de la réponse API — reads.json non modifié.", file=sys.stderr)
        sys.exit(1)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(totals, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"OK — {len(totals)} éditions, {sum(totals.values())} lectures cumulées.")


if __name__ == "__main__":
    main()
