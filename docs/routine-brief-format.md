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
    "image_keywords": "string, 2-3 mots-clés thématiques EN, ou null",
    "complexite": "entier 1 à 5, voir § dédié plus bas"
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
    "serie": "null si decision=non, sinon voir § dédié plus bas pour le schéma exact"
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
  "revue_de_presse": [
    {
      "title": "string",
      "source": "string (nom du média)",
      "url": "string",
      "image": "string ou null (URL og:image du média, jamais téléchargée/hébergée chez nous)",
      "lang": "fr|en|other",
      "domain": "un des 6 slugs de docs/tags.md",
      "summary": "string, 1-2 phrases factuelles, jamais un avis",
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

## Champ `sujet.complexite` (utilisé par `generate_daily_edition.py` et la rédaction)

Ajouté le 16 septembre 2026, retour utilisateur : entier de 1 à 5,
question à se poser au moment de la recherche : **« un lecteur français
grand public, sans connaissance préalable du domaine, comprend-il ce
sujet sans effort ? »**

- **1-2** : sujet limpide (un chiffre qui monte/baisse, une décision
  simple à comprendre même sans contexte).
- **3** : nécessite au moins un mécanisme ou un acteur/dispositif à
  expliquer pour suivre le fil (ex. un mécanisme réglementaire, un
  dispositif à plusieurs seuils).
- **4-5** : plusieurs mécanismes imbriqués, ou un domaine technique
  (financier, juridique, scientifique) sans équivalent grand public
  immédiat.

**Ce champ pilote deux choses en aval, jamais à recalculer ailleurs :**
- `encarts_decides.comprendre_box` : au moins 1 élément toujours requis ;
  **exactement 2 à partir de complexite ≥ 3** (voir § Règles de validité
  plus bas, vérifié par `generate_daily_edition.py`).
- Le niveau d'exigence pédagogique de la rédaction elle-même (phrases
  plus courtes, termes techniques expliqués en incise) — voir
  `docs/routine-redaction-prompt.md` § Règles de style.

Une note **délibérément haute sur un sujet qui n'est pas réellement
complexe** revient à forcer un 2e `comprendre_box` sans matière
distincte — le même garde-fou anti contenu artificiel que pour l'encart
lui-même s'applique ici : la note doit refléter une vraie difficulté de
compréhension, jamais être gonflée pour obtenir plus d'encarts.

## Champ `revue_de_presse` (utilisé par `generate_post_edition.py`, pas la rédaction)

Ajouté le 14 septembre 2026 pour automatiser `sources-log.json`/
`sources.html` — voir `docs/routine-prompt.md`, § « Revue de presse » pour
la règle éditoriale complète (2 à 5 liens croisés pendant la recherche,
même hors sujet du jour, jamais un avis dessus). **Distinct de `sources[]`
ci-dessus** : `sources[]` porte les sources qui servent directement aux
`faits_verifies` de l'édition du jour (presque toujours sur le même
sujet) ; `revue_de_presse` porte au contraire des articles croisés au
passage, pas forcément liés au sujet du jour, gardés juste pour leur
intérêt factuel propre — les deux listes ne se recoupent pas forcément et
aucune des deux ne doit être déduite de l'autre.

`generate_post_edition.py` construit l'entrée du jour de
`sources-log.json` **directement à partir de `revue_de_presse`** (mêmes
champs, sans `id`) et régénère `sources.html` — aucune action manuelle.
**Jamais bloquant** : `[]` ou champ absent → aucun jour ajouté pour la
date du brief (comme le faisait la routine manuelle : « rien de notable
croisé aujourd'hui → section vide ce jour-là », jamais une entrée vide
forcée). Relancer le pipeline sur un brief déjà traité **remplace**
l'entrée du jour plutôt que de la dupliquer (idempotent, mêmes garanties
que le reste de la post-édition).

## Champ `graphique_dc_chart.serie` (utilisé par `scripts/edition/build_html.py`, pas la rédaction)

Composant `.dc-chart-box` — graphique en escalier pour une série
historique longue en complément d'un chiffre déjà cité dans
`indicateurs_kpi`/`.indicator-strip`, jamais pour le remplacer (voir
`docs/routine-prompt.md`, § « Graphique en escalier » pour la règle de
décision éditoriale complète : 5 points réels vérifiés minimum, jamais
forcé). **Avant le 15 septembre 2026, ce composant n'existait que via un
`<script>` JS écrit à la main par la routine manuelle** (voir
`archives/2026-08-21.html`/`archives/2026-08-24.html`, gardées comme
référence historique de ce à quoi le graphique doit ressembler) — jamais
porté dans la chaîne automatisée. Depuis, `build_html.py` rend le SVG
lui-même, côté serveur, de façon entièrement déterministe à partir de ce
champ : toutes les décisions éditoriales (unités, graduations, années
affichées sur l'axe X, points notables) doivent donc être posées ici, en
JSON, plutôt que dans un script à écrire.

`serie` (uniquement si `decision` = `"oui"`, sinon toujours `null`) :
```json
{
  "aria_label": "string — description accessible du <svg> (lu par un lecteur d'écran)",
  "lead": "string — texte d'intro juste avant le graphique",
  "caption": "string — texte juste après le graphique (source des données notamment)",
  "y_max": 1080,
  "y_gridlines": [
    {"valeur": 180, "label": "3 min"}
  ],
  "x_axis_years": [1947, 1960, 1974, 1991, 2007, 2019, 2026],
  "points": [
    {"annee": 1947, "valeur": 420, "tooltip": "1947 — 7 min avant minuit"},
    {"annee": 1991, "valeur": 1020, "tooltip": "...", "peak": true, "peak_label": "17 min — record de recul"},
    {"annee": 2026, "valeur": 85, "tooltip": "...", "last": true, "last_label": "85 s aujourd'hui"}
  ]
}
```
- `points` : chronologique, valeur dans une unité fine et cohérente d'un
  point à l'autre (ex. secondes plutôt que minutes arrondies) — le
  graphique relie les points en escalier (la valeur tient jusqu'au point
  suivant, jamais d'interpolation continue), donc l'ordre fait le tracé.
- `y_gridlines`/`x_axis_years` : jamais tous les points/années si la série
  est longue (surcharge visuelle) — un sous-ensemble choisi à la main,
  même logique que l'original manuel.
- `peak`/`peak_label` : au plus un point marquant à mettre en avant en
  dehors du dernier (ex. un record) — optionnel.
- `last`/`last_label` : toujours sur le dernier point chronologique
  (`points[-1]`), jamais ailleurs — c'est lui qui reçoit le point
  agrandi (`is-highlight`) sur le graphique.
- `tooltip` : texte au survol de chaque point (élément SVG `<title>`),
  jamais vide.

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
- `revue_de_presse` : **pas** de minimum, absent ou `[]` valide (à
  l'inverse de `sources` ci-dessus) — voir § dédié plus haut.
- `sujet.complexite` : entier entre 1 et 5 (ajouté le 16 septembre 2026,
  voir § dédié plus haut).
- `encarts_decides.comprendre_box` : le nombre requis dépend de
  `sujet.complexite` (changement du 16 septembre 2026, ajusté le même
  jour dans l'après-midi — la version précédente forçait toujours
  exactement 2, quel que soit le sujet) :
  - `complexite` < 3 : **au moins 1 élément** (jamais 0).
  - `complexite` ≥ 3 : **exactement 2 éléments**.

  Que ce soit 1 ou 2, chaque élément doit porter sur un mécanisme
  réellement distinct du sujet — jamais deux angles du même — voir
  `docs/routine-prompt.md`, § « Encart Comprendre » pour la règle
  complète et le garde-fou anti contenu artificiel.

## Exemple

Voir `editorial-briefs/2026-09-20.json` — brief **fictif**, créé
uniquement pour tester la mécanique du prototype (Phase 1, point G.2 de
l'audit), pas une vraie édition.
