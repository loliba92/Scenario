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

## 2. Les 4 jobs à créer sur cron-job.org

Chaque job = même structure (`POST` vers `dispatches`), seul `event_type`
et l'heure changent.

```
URL to call:          https://api.github.com/repos/loliba92/Scenario/dispatches
Request method:       POST
Custom HTTP headers:
  Authorization:       token YOUR_GITHUB_TOKEN
  Accept:               application/vnd.github.v3+json
Request body (JSON):  {"event_type": "EVENT_TYPE_ICI"}
```

| # | Job | event_type | Heure UTC | Heure Paris (été) | Rôle |
|---|-----|-----------|-----------|---------------------|------|
| 1 | 🔍 Preview | `trigger-preview` | **14:00** | 16h | Génère brief + `preview.html` pour DEMAIN — fenêtre de validation avant publication |
| 2 | 🚀 Publication (prod) | `trigger-post-edition` | **05:00** | 7h | Publie le vrai site (index.html, archives, feed.xml) du jour |
| 3 | 📱 Pub réseaux sociaux | `trigger-pub` | **06:00** | 8h | Post Telegram/X/LinkedIn/Instagram — APRÈS que le site soit en ligne |
| 4 | 📰 Récap hebdo | `trigger-hebdo` | **11:00** dimanche uniquement | 13h | Récap de la semaine + email Buttondown |

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
