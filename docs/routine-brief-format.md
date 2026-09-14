# Format du brief éditorial (prototype)

**Statut : Phase 1, prototype.** Ce document décrit le schéma JSON produit
par la partie recherche de la routine (Claude Code — étapes 0 à 3bis de
`docs/routine-prompt.md`) et consommé par
`scripts/edition/generate_daily_edition.py` (GitHub Actions,
`workflow_dispatch` uniquement pour l'instant).

**Ce que le brief doit couvrir** : tout ce qui exige une vraie recherche
web en temps réel ou un jugement éditorial — sélection du sujet,
anti-doublon, faits vérifiés et leurs sources, décision sur les encarts
optionnels. **Ce que le brief ne couvre pas** : la rédaction elle-même
(phrases, style) — voir `docs/routine-redaction-prompt.md`.

**Emplacement** : `editorial-briefs/{AAAA-MM-JJ}.json`, un fichier par
jour — convention alignée sur `archives/fragments/{date}.html` et
`hebdo/{date}.html`, plutôt que le format "un objet par jour dans un seul
fichier" de `sources-log.json` (évite tout risque d'écriture concurrente
sur un fichier partagé entre deux process).

## Schéma

```json
{
  "date": "AAAA-MM-JJ",
  "registre": "slug du registre (voir docs/tags.md)",
  "sujet": {
    "titre_propose": "string",
    "h1": "string",
    "question_posee": "string, max 200 caractères",
    "eyebrow": "string, format '{Jour}, {registre}'",
    "angle": "string, 1-2 phrases",
    "tags": ["string"],
    "domain": "un des 6 slugs de docs/tags.md"
  },
  "anti_doublon": {
    "veille_ok": true,
    "meme_registre_ok": true,
    "notes": "string"
  },
  "faits_verifies": [
    {
      "affirmation": "string",
      "chiffre": "string ou null",
      "date_du_chiffre": "AAAA-MM-JJ ou null",
      "sources": ["id de source, voir sources[].id"],
      "confiance": "haute|moyenne"
    }
  ],
  "acteurs": [{"nom": "string", "role": "string"}],
  "chronologie_cle": [{"date": "AAAA-MM-JJ", "evenement": "string"}],
  "scenarios_prospectifs": {
    "favorable": {"resume": "string", "probabilite_suggeree": 0},
    "stable": {"resume": "string", "probabilite_suggeree": 0},
    "degrade": {"resume": "string", "probabilite_suggeree": 0}
  },
  "indicateurs_kpi": [
    {"label": "string", "valeur": "string", "tendance": "string"}
  ],
  "graphique_dc_chart": {
    "decision": "oui|non",
    "raison": "string",
    "serie": null
  },
  "encarts_decides": {
    "comprendre_box": [
      {"focus": "string", "rattache_a": "string (référence au fait/dek concerné)"}
    ],
    "list_box": null
  },
  "elements_incertains": ["string"],
  "a_ne_pas_affirmer": ["string"],
  "sources": [
    {
      "id": "string, référencé par faits_verifies[].sources",
      "title": "string",
      "source": "string (nom du média)",
      "url": "string",
      "image": "string ou null",
      "lang": "fr|en|other",
      "domain": "un des 6 slugs de docs/tags.md",
      "summary": "string",
      "read_minutes": 0
    }
  ],
  "recommandations_redaction": ["string"]
}
```

## Règles de validité (vérifiées par `generate_daily_edition.py`)

- `date` : format `AAAA-MM-JJ` valide.
- `sujet.question_posee` : non vide, ≤ 200 caractères.
- `scenarios_prospectifs` : exactement les 3 clés `favorable`/`stable`/
  `degrade`, chacune avec `probabilite_suggeree` entre 0 et 100 ; la somme
  des 3 n'est **pas** forcée à 100 par le brief (ajustement possible en
  rédaction), mais un écart de plus de 10 points au total déclenche un
  avertissement.
- `indicateurs_kpi` : entre 1 et 3 éléments (2 est la norme, voir règle de
  cohérence des KPI dans `docs/routine-prompt.md`).
- `sources` : au moins 1 élément ; chaque `id` référencé dans
  `faits_verifies[].sources` doit exister dans `sources`.
- `encarts_decides.comprendre_box` : au maximum 2 éléments.

## Exemple

Voir `editorial-briefs/2026-09-20.json` — brief **fictif**, créé
uniquement pour tester la mécanique du prototype (Phase 1, point G.2 de
l'audit), pas une vraie édition.
