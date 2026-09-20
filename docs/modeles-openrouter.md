# Modèles OpenRouter dans les workflows GitHub

Référence technique : quel modèle OpenRouter tourne sur quel workflow, à
quelle fréquence, pourquoi, et les incidents réels déjà rencontrés par
modèle. Voir `docs/BACKLOG.md` ticket **B152** pour l'historique de la
répartition actuelle (décidée le 18 septembre 2026).

## Vue d'ensemble

Onze workflows tournent dans `.github/workflows/`. Neuf appellent
OpenRouter pour générer du texte ; deux (`audience.yml`, `reads.yml`) ne
font que lire des données (GoatCounter, coût OpenRouter) sans appeler de
modèle.

La **recherche quotidienne** (choix du sujet, anti-doublon, faits
sourcés) devait tourner sur un trigger Claude Code Remote
(`trig_013z1speQQCqE9gvGkiwTZa7`, 6h Paris) — **ce trigger est
aujourd'hui désactivé**. En pratique, c'est donc le repli GitHub/
OpenRouter qui fait la recherche : `post-edition.yml` appelle
`scripts/edition/generate_fallback_brief.py` dès que le brief du jour
est absent, ce qui est le cas en continu tant que le trigger reste
éteint. La recherche tourne donc bien sur OpenRouter/GitHub Actions
aujourd'hui, pas hors périmètre.

Trois modèles OpenRouter sont utilisés aujourd'hui :

- **`anthropic/claude-sonnet-5`** — rédaction quotidienne, recherche
  quotidienne (repli, voir ci-dessus), détection de sujets à suivre,
  traduction anglaise.
- **`openai/gpt-5`** — récap hebdomadaire uniquement, depuis le
  16 septembre 2026.
- **`deepseek/deepseek-v4-flash`** — posts « pub » courts (génération +
  réparation/banque de chiffres) et repérage de sujets chauds.

**Opus abandonné le 20 septembre 2026** (retour utilisateur explicite :
« opus sur openrouter dans la recherche n'apporte rien ») — il n'avait
qu'un seul usage dans ce dépôt (recherche quotidienne, depuis le
18 septembre) et n'est plus utilisé nulle part. Voir `docs/BACKLOG.md`
ticket B152 pour l'historique complet des deux décisions.

## Les 11 workflows

| Workflow | Fréquence | Script | Modèle par défaut | Changeable au run ? |
| --- | --- | --- | --- | --- |
| `post-edition.yml` — rédaction | quotidien, 4h30 et 5h30 UTC (2 créneaux) | `generate_daily_edition.py` | `anthropic/claude-sonnet-5` | Oui — input `model` ou variable de dépôt `OPENROUTER_MODEL` |
| `post-edition.yml` — repli recherche | quotidien tant que le trigger CCR reste désactivé (voir ci-dessus) | `generate_fallback_brief.py` | `anthropic/claude-sonnet-5` (Opus du 18 au 20 septembre 2026, abandonné — voir plus bas) | Oui — même input `model`/`OPENROUTER_MODEL` que la rédaction (partagé, voir note ci-dessous) |
| `edition.yml` | manuel seulement (prototype Phase 1, sans publication) | `generate_daily_edition.py` | `anthropic/claude-sonnet-5` | Non |
| `translate-en.yml` | manuel + auto-déclenché en fin de `post-edition.yml` | `translate_daily.py` | `anthropic/claude-sonnet-5` | Non dans le workflow (le script accepte `--model` en local) |
| `detection.yml` | lun/jeu/ven/sam, 1h UTC | `generate_suivi_update.py` | `anthropic/claude-sonnet-5` | Non |
| `hot-topics.yml` | mar/ven, 19h UTC (~21h Paris été) | `generate_hot_topics.py` | `deepseek/deepseek-v4-flash` | Non |
| `hebdo.yml` | dimanche, 12h UTC | `generate_weekly_recap.py` | `openai/gpt-5` (DeepSeek jusqu'au 16 septembre) | Oui — input `model` |
| `pub.yml` | quotidien, 2h UTC | `generate_daily_pub.py` | `deepseek/deepseek-v4-flash` (traduction EN seulement depuis le 19 septembre 2026 — la catégorie `chiffre` elle-même n'appelle plus aucun modèle, voir `docs/ARCHITECTURE.md`) | Non |
| `audience.yml` | quotidien, 5h UTC | `update_audience.py` | — (lit le coût OpenRouter, n'appelle aucun modèle) | — |
| `reads.yml` | horaire | `update_reads_json.py` | — (GoatCounter uniquement) | — |

Secret commun : `OPENROUTER_API_KEY` (les 7 workflows qui génèrent du
texte + `audience.yml` pour le KPI de coût — `bank-chiffre.yml` et
`fix-pub.yml` retirés le 19 septembre 2026 avec les scripts qu'ils
appelaient, voir `docs/ARCHITECTURE.md`).

**Point de vigilance** : dans `post-edition.yml`, la variable de dépôt
`OPENROUTER_MODEL`/l'input manuel `model` s'applique **aux deux** étapes
(rédaction et repli recherche) — les deux tournant maintenant sur Sonnet
5 par défaut, ce n'est plus un risque de bascule silencieuse d'un modèle
vers un autre comme du temps d'Opus, mais reste vrai : tester un autre
modèle de rédaction via ce canal écrase aussi temporairement celui du
repli recherche. Pas de canal séparé pour l'instant.

## Particularités réelles par modèle

**`anthropic/claude-sonnet-5`** — modèle par défaut sur le JSON
structuré volumineux (rédaction, détection, traduction).
- 14 septembre 2026 : au tout premier vrai appel, Sonnet a tourné plus
  de 16 minutes sans répondre (raisonnement étendu jamais désactivé) —
  corrigé en ajoutant `"reasoning":{"enabled":false}` pour tout modèle
  `anthropic/*`.
- 16 septembre 2026 : `translate_daily.py` tournait jusque-là sur
  DeepSeek ; basculé sur Sonnet 5 après un 2e incident de troncature/
  segments manquants sur DeepSeek (« si pb de modèle on peut passer sur
  un modèle un peu plus puissant », retour utilisateur). `max_tokens`
  relevé de 8000 à 16000 à cette occasion.

**`anthropic/claude-opus-5`** — [RETIRÉ le 20 septembre 2026, gardé ici
comme repère historique, plus jamais utilisé] recherche quotidienne
uniquement du 18 au 20 septembre 2026 (voir B152). Même famille que
Sonnet côté API : le garde-fou `"reasoning":{"enabled":false}`
(`anthropic/*`) s'appliquait aussi à Opus, aucun quirk spécifique
n'avait été identifié — le retrait est un choix de rapport
qualité/coût (« n'apporte rien »), pas un incident technique.

**`openai/gpt-5`** — seul le récap hebdomadaire l'utilise, depuis un
comparatif réel fait par l'utilisateur sur la même semaine. Deux quirks
trouvés au premier test (16 septembre 2026) :
- Il impose son raisonnement interne et **refuse qu'on le désactive**
  (« Reasoning is mandatory for this endpoint and cannot be disabled »),
  contrairement à Sonnet et DeepSeek.
- Avec `max_tokens=3000` (suffisant pour DeepSeek), GPT-5 a renvoyé un
  contenu **vide** — tout le budget était parti dans son raisonnement
  obligatoire. Relevé à 16000 pour tout modèle dont le raisonnement ne
  peut pas être coupé.
- **Conséquence concrète** : `generate_daily_pub.py` envoie
  `"reasoning":{"enabled":false}` **sans condition** (seul appel restant
  après le retrait de `bank_chiffre.py`/`fix_chiffre_post.py` le
  19 septembre 2026, voir `docs/ARCHITECTURE.md`) — le basculer sur GPT-5
  tel quel ferait échouer l'appel immédiatement (erreur explicite, pas un
  échec silencieux, mais à corriger avant de tester).

**`deepseek/deepseek-v4-flash`** — le moins cher, réservé aux tâches
courtes/formatées (posts pub, chiffres) et au repérage de sujets chauds
(candidats non publiés directement, filtrés par une relecture humaine).
Accepte `"reasoning":{"enabled":false}` sans problème — ce garde-fou est
appliqué pour `deepseek/*` dans `call_openrouter()` (`generate_daily_
edition.py`) depuis le 18 septembre 2026, pour permettre à
`generate_hot_topics.py` de tourner dessus sans reproduire le bug
« contenu vide » de GPT-5. Faiblesse constatée : troncature/segments
manquants sur du texte long et structuré (cause de son remplacement par
Sonnet 5 sur la traduction et sur la détection — voir B152).

## Suivi des coûts existant

`audience.yml` interroge chaque jour les endpoints `/credits` et `/key`
d'OpenRouter (`update_audience.py::fetch_openrouter_cost()`) et
alimente `assets/data/openrouter-cost.json`, affiché sur
`dashboard.html` (coût d'hier, de la semaine, du mois, cumulé).

**Limite à connaître** : ces deux endpoints ne renvoient qu'un
**montant total sur tout le compte**, jamais ventilé par modèle ni par
workflow, et aucun des deux n'expose de nombre de requêtes. Impossible
aujourd'hui de savoir, depuis le dashboard, si une variation de coût
vient de la recherche (Opus, tous les jours), de la rédaction (Sonnet,
tous les jours) ou du récap hebdo (GPT-5, une fois par semaine) — il
faut croiser à la main la date et les logs de run GitHub Actions.

## Répartition retenue (18 septembre 2026)

Décision détaillée dans `docs/BACKLOG.md` ticket **B152**. Résumé :

- **Recherche quotidienne → Opus.** C'est l'étape qui demande le plus
  de jugement éditorial (sujet, sources, anti-doublon), et elle tourne
  désormais tous les jours (trigger CCR désactivé) — le candidat le
  plus justifié pour un modèle plus poussé.
- **Sujets chauds (`hot-topics.yml`) → DeepSeek.** Simple repérage de
  candidats non publiés directement, toujours filtrés par une relecture
  humaine avant promotion — enjeu qualité faible, finance une partie du
  surcoût d'Opus.
- **Détection de sujets à suivre (`detection.yml`) → resté sur
  Sonnet 5.** Erreur évitée de justesse : ce script ne fait pas du tri,
  il réestime réellement les 3 scénarios et écrit le texte **publié**
  de la mise à jour — un downgrade DeepSeek y avait été appliqué puis
  annulé le jour même.
- **GPT-5 écarté sur `hot-topics.yml`** malgré la tentation : coûte plus
  cher que DeepSeek (raisonnement obligatoire non désactivable,
  `max_tokens` à relever) pour un enjeu qualité faible sur cette tâche —
  aurait mangé une bonne partie de l'économie qui finance Opus.

**Reste ouvert** : pas de ventilation de coût par modèle/workflow (voir
« Suivi des coûts existant » ci-dessus) — à surveiller au jugé dans les
prochains jours plutôt qu'avec des chiffres précis.

## Correction du 20 septembre 2026 : Opus abandonné sur la recherche

Retour utilisateur explicite, deux jours après la répartition ci-dessus :
« opus sur openrouter dans la recherche n'apporte rien on repasse en
sonnet ». Le pari du 18 septembre (un modèle plus poussé sur l'étape à
plus fort jugement éditorial) ne s'est pas vérifié en pratique — aucun
gain de qualité observé qui justifie le surcoût par rapport à Sonnet 5.
`FALLBACK_MODEL` dans `generate_fallback_brief.py` repassé à
`anthropic/claude-sonnet-5`. Les deux autres volets de B152 (DeepSeek sur
`hot-topics.yml`, Sonnet resté sur `detection.yml`) ne changent pas — ce
n'était pas leur pari qui a échoué, seulement celui d'Opus sur la
recherche.

**Reste ouvert** : l'utilisateur envisage un autre modèle spécifiquement
plus fort en recherche (pas nécessairement un simple retour au statu quo
d'avant le 18) — pas encore choisi, voir `docs/BACKLOG.md` ticket B152.
