# Cron-Job.org Setup — Scheduling centralisé

Tous les workflows automatiques du site passent par cron-job.org (décision
utilisateur, 21 septembre 2026) au lieu des crons GitHub natifs — plus
fiable, un seul endroit pour tout voir/modifier.

## 1. Créer un token GitHub (Personal Access Token)

1. Va sur https://github.com/settings/tokens
2. **Generate new token** → **Tokens (classic)**
3. Nom : `scenario-cron-trigger`
4. Permissions :
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (update GitHub Action workflows)
5. Génère et **copie le token** (ne le perds pas !)

## 2. Les jobs sur cron-job.org (relevé du 12 novembre 2026)

Chaque job = même structure (`POST` vers `dispatches`), seuls le workflow et
l'heure changent. Les horaires ci-dessous sont ceux configurés sur cron-job.org.

```
URL to call:          https://api.github.com/repos/loliba92/Scenario/actions/workflows/NOM.yml/dispatches
Request method:       POST
Custom HTTP headers:
  Authorization:       token YOUR_GITHUB_TOKEN
  Accept:               application/vnd.github+json
Request body (JSON):  {"ref": "main"}
```

| Job cron-job.org | Workflow (`.github/workflows/`) | Heure UTC | Fréquence | Rôle |
|---|---|---|---|---|
| Generation du Preview | `daily-preview.yml` | **13:15** | chaque jour | Génère le brief et `preview.html` pour DEMAIN |
| Redaction et publication | `post-edition.yml` | **06:00** | chaque jour | Publie l'édition du jour (index, archives, flux) |
| Pub | `pub.yml` | **08:00** | chaque jour | Post sur les réseaux, après la mise en ligne |
| Dashboard / Mise a jour audience | `audience.yml` | **08:00** et **12:00** | chaque jour | Tableau de bord, données d'audience |
| Mise a jour audience (reads) | `reads.yml` | **11:00** et **12:00** | chaque jour | Lectures par édition |
| Mise a Jour SEO Google Search Console | `gsc.yml` | **05:05** | chaque jour | Données Search Console |
| Signaux | `signaux.yml` | **16:00** | chaque jour | Point quotidien des échéances, résultats vérifiés, page « À venir » |
| Generation du Scenario de la semaine | `hebdo.yml` | **12:00** | dimanche | Récap hebdomadaire |
| Recherche des Sujets Priroitaires | `hot-topics.yml` | **05:00** | **dimanche seulement** | Veille des sujets chauds (cartes « Derniers sujets », échéances fermes) |
| Detection de sujets a réviser | `detection.yml` | **03:00** | lundi | Détection des sujets à suivre |

**Attention :** `hot-topics.yml` ne tourne que le dimanche. Les sujets chauds et
les nouvelles échéances fermes ne sont donc mis à jour qu'une fois par semaine.
`signaux.yml` tourne à 16h00 UTC, et non à 05h30 comme indiqué auparavant.

Les workflows `enrich-sujets.yml` (chaque soir à 18h23 UTC) et `valider-sujets.yml`
(manuel) sont déclenchés par GitHub ou à la main, sans job cron-job.org.

La traduction anglaise (`translate-en.yml`) n'a **pas besoin** de job cron :
elle se déclenche automatiquement dès que `index.html` est publié (push
trigger), donc elle suit le job #2 sans configuration supplémentaire.

## 3. Configurer chaque job sur cron-job.org

Pour chacun des 4 jobs ci-dessus :

1. https://cron-job.org → **Create** un nouveau job
2. Title : nom du job (ex. "Scénario — Publication prod")
3. URL, méthode, headers, body : voir tableau ci-dessus (adapter
   `event_type`)
4. **Execution schedule** :
   - Preview / Prod / Pub : `Daily`, heure UTC du tableau, Timezone `UTC`
   - Hebdo : `Weekly`, jour = `Sunday`, heure `11:00 UTC`
5. **Save**

## 4. Test manuel (avant d'activer le cron)

```bash
# Remplace EVENT_TYPE par trigger-preview / trigger-post-edition / trigger-pub / trigger-hebdo
curl -X POST \
  https://api.github.com/repos/loliba92/Scenario/dispatches \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"event_type":"EVENT_TYPE"}'
```

Si succès → le workflow correspondant se lance sur GitHub (onglet Actions).

## Architecture

```
Cron-Job.org (4 jobs, horaires différents)
    ↓
POST https://api.github.com/repos/loliba92/Scenario/dispatches
    ↓
GitHub reçoit un repository_dispatch event (event_type distinct par job)
    ↓
┌─────────────────┬──────────────────────┬───────────────┬────────────────┐
│ trigger-preview  │ trigger-post-edition │ trigger-pub   │ trigger-hebdo  │
│  daily-preview   │    post-edition      │    pub.yml    │   hebdo.yml    │
│      .yml        │        .yml          │               │                │
└─────────────────┴──────────────────────┴───────────────┴────────────────┘
                              ↓ (post-edition publie index.html)
                    translate-en.yml se déclenche automatiquement (push trigger)
```

## Logs & Monitoring

- Workflow logs : https://github.com/loliba92/Scenario/actions
- Cron-Job logs : https://cron-job.org/en/jobs (dashboard)

## Troubleshooting

**Workflow ne se déclenche pas :**
1. Vérifie le token GitHub (pas expiré ?)
2. Vérifie la config cron-job.org (event_type exact, URL correcte)
3. Teste avec `curl` (voir ci-dessus)
4. Check GitHub Actions logs

**Erreur "Unauthorized" :**
- Token expiré ? Crée-en un nouveau
- Permissions insuffisantes ? Ajoute le scope `workflow`

**Le site n'est pas publié malgré un run vert de post-edition.yml :**
- Vérifie que `publish` n'a pas été mis à `false` (input manuel uniquement
  — le trigger cron-job.org utilise toujours le défaut `true`)
