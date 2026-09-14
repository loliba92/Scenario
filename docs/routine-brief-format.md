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
    "domain": "un des 6 slugs de docs/tags.md",
    "image_keywords": "string, 2-3 mots-clés thématiques EN, ou null"
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

## Champ `sujet.image_keywords` (utilisé par `generate_post_edition.py`, pas la rédaction)

2-3 mots-clés thématiques **génériques en anglais** pour la recherche de
photo de sujet (Pexels) — même règle que la routine complète
(`docs/routine-prompt.md`, étape « Image du sujet ») : jamais le titre
recopié tel quel, jamais un nom propre/marque/acronyme isolé (un lieu
générique + concept reste valable, ex. « government building paris »).
`null` si aucun concept visuel générique clair ne se dégage du sujet —
dans ce cas `generate_post_edition.py` retombe directement sur l'image
générique, sans appel Pexels.

**Sélection automatique du candidat, sans revue humaine** (décision
assumée le 14 septembre 2026, changement de comportement par rapport à
`fetch_topic_image.py` qui documente une sélection humaine par défaut) :
`generate_post_edition.py` retient le premier candidat renvoyé par
Pexels pour cette requête, jamais un choix éditorial. La qualité du
résultat final dépend donc entièrement de la précision des mots-clés
choisis ici — les mêmes précautions que la routine complète restent
valables (pas de visage reconnaissable suggéré, pas de photomontage
stock clicheté), même si elles ne sont plus vérifiées après coup.

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
