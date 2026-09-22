# Daily Preview Workflow

## 📋 Process

### Daily at 14:00 UTC (GitHub Actions)
Automated workflow generates and previews tomorrow's edition:

1. **Phase 1 (Research)** — Upstage Solar Pro4
   - Generates brief for tomorrow (editorial-briefs/YYYY-MM-DD.json)
   - Cost: ~$0.0035 per brief

2. **Phase 2 (Rédaction)** — Google Gemini 3.7 Flash
   - Generates full editorial content
   - Produces preview.html (rendered) + .preview-content.json (raw data)
   - Cost: ~$0.0295 per edition

3. **Commit & Push**
   - Both files committed to `main` branch
   - GitHub Actions notification posted
   - Total cost: ~$0.033 per edition

4. **Critique automatique** (`scripts/edition/critique_preview.py`, added
   22 September 2026) — `deepseek/deepseek-v4-flash`, deliberately a different model
   from the one that wrote the edition
   - Static/internal checks only (never a live fact-check): number/date
     consistency across sections, named attributions matching a listed
     source, tone breaks, lexical repetition, scenario-probability
     framing, chart consistency
   - Never blocks the pipeline — advisory only, runs with
     `continue-on-error: true`
   - Result posted as a **GitHub issue** (title prefixed ✅/⚠️/🛑/❌
     depending on verdict) — GitHub notifies you (email/mobile) as soon
     as it's created, no separate notification channel needed
   - Root cause it addresses: the 22 September 2026 edition went live
     with a stale Brent price, an unverifiable "selon JPMorgan" claim and
     a tone break — see `docs/routine-prompt.md` § Anti-péremption /
     Relecture de cohérence / Relecture stylistique for the corresponding
     redaction-side rules this step cross-checks independently

### Afternoon Review (14:00-18:00 UTC)
Read the critique issue first, then review `preview.html` in your browser:
- Check editorial quality
- Verify JSON structure
- Look for any generation issues

### Validation
- **No feedback** = Implicit approval ✅
- **Questions/Issues** = Comment on commit or open issue
- Errors are caught and can be fixed before going to production

### Production Rollout
When ready:
- Copy validated `preview.html` → `index.html`
- Deploy to production
- Schedule: typically next morning or manually when validated

## 🛠️ Files

```
main branch (git tracked)
├── .github/workflows/daily-preview.yml    (this workflow)
├── docs/PREVIEW-WORKFLOW.md               (this doc)
└── .gitignore                             (excludes preview files)

Generated daily (in main branch)
├── preview.html                           (tomorrow's preview)
├── .preview-content.json                  (raw JSON data)
└── editorial-briefs/YYYY-MM-DD.json       (brief for tomorrow)

Local only (not tracked)
└── _prototype-out/                        (intermediate files)
```

## 🔧 Configuration

**Secrets required in GitHub:**
- `OPENROUTER_API_KEY` — OpenRouter API key for model calls

**Cron schedule:**
- `0 14 * * *` — Every day at 14:00 UTC

## 📊 Cost Analysis

| Component | Model | Cost | Status |
|-----------|-------|------|--------|
| Phase 1 | Upstage Solar Pro4 | $0.00346 | ✅ |
| Phase 2 | Google Gemini 3.7 | $0.02948 | ✅ |
| **Total per edition** | — | **$0.033** | ✅ |
| **Monthly (30 editions)** | — | **~$1.00** | ✅ |

## ⚠️ Failure Handling

If the workflow fails:
1. GitHub Actions logs show the error
2. No commit is made to main
3. You can review logs and investigate
4. Manually re-run workflow via GitHub UI if needed

## 📝 Manual Trigger

Run preview generation manually:
```bash
# Via GitHub UI: Actions → Daily Preview Generation → Run workflow
# Or via CLI:
gh workflow run daily-preview.yml
```

## 🔄 Workflow Diagram

```
Daily 14:00 UTC
    ↓
[Phase 1: Brief Generation]
    ↓
[Phase 2: Edition Generation]
    ↓
[Commit preview.html to main]
    ↓
[Automatic critique (deepseek/deepseek-v4-flash) → GitHub issue]
    ↓
[Afternoon: Manual Review]
    ↓
[No issues → Implicit validation]
    ↓
[Manually copy preview → index.html when ready]
    ↓
[Production Live]
```

## 🚀 Going Live

When preview is validated and ready:

```bash
# Manual deployment (when validated)
cp preview.html index.html
git add index.html
git commit -m "Production: Deploy edition YYYY-MM-DD"
git push origin main
```

Or integrate into automated production deployment if desired.
