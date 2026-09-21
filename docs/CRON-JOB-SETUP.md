# Cron-Job Setup pour Daily Preview

## Configuration Cron-Job.org

### 1. Créer un token GitHub (Personal Access Token)

1. Va sur https://github.com/settings/tokens
2. **Generate new token** → **Tokens (classic)**
3. Donne un nom : `preview-cron-trigger`
4. Donne les permissions :
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (update GitHub Action workflows)
5. Génère et **copy le token** (ne le perds pas!)

### 2. Configurer le job sur Cron-Job.org

1. Va sur https://cron-job.org
2. **Login** ou crée un compte
3. **Create** un nouveau job
4. Remplis avec :

```
Title:                Preview Generation (14h UTC)
URL to call:          https://api.github.com/repos/loliba92/Scenario/dispatches
Request method:       POST
Request body (JSON):  {
  "event_type": "trigger-preview"
}

HTTP Basic Auth:
  Username:           (laisse vide)
  Password:           (laisse vide)

Custom HTTP headers:
  Name:               Authorization
  Value:              token sk-or-v1-... (TON GITHUB TOKEN)
  
  Name:               Accept
  Value:              application/vnd.github.v3+json
```

5. **Execution schedule** :
   - Frequency: `Daily`
   - Time: `14:00` (UTC)
   - Timezone: `UTC`

6. **Save** le job

### 3. Test du job

```bash
# Déclencher manuellement une fois pour tester:
curl -X POST \
  https://api.github.com/repos/loliba92/Scenario/dispatches \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"event_type":"trigger-preview"}'
```

Si succès → le workflow se lance sur GitHub ! ✅

## Architecture

```
Cron-Job.org (14h UTC)
    ↓
POST https://api.github.com/repos/loliba92/Scenario/dispatches
    ↓
GitHub receives repository_dispatch event
    ↓
daily-preview.yml workflow triggered
    ↓
Phase 1: Brief Generation
Phase 2: Edition Generation
    ↓
preview.html committed to main
```

## Logs & Monitoring

- Workflow logs: https://github.com/loliba92/Scenario/actions/workflows/daily-preview.yml
- Cron-Job logs: https://cron-job.org/en/jobs (sur ton dashboard)

## Troubleshooting

**Workflow ne se déclenche pas:**
1. Vérifie le token GitHub (pas expiré ?)
2. Vérifie la config cron-job.org
3. Teste avec `curl` (voir ci-dessus)
4. Check GitHub Actions logs

**Erreur "Unauthorized":**
- Token expiré ? Crée-en un nouveau
- Permissions insuffisantes ? Ajoute `workflow` scope
