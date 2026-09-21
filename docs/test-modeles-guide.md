# Guide: Test comparatif des modèles OpenRouter

**Objectif:** Évaluer 4 modèles OpenRouter sur la tâche réelle de recherche éditorial et recommander le meilleur ratio coût/qualité.

**Modèles testés:**
1. **Haiku 4.5** - $1/$5 (50% moins cher que Sonnet)
2. **Sonnet 5** - $2/$10 (baseline actuel)
3. **Sakana Fugu Max** - $2/$6 (web search spécialisé)
4. **DeepSeek v4** - $0.12/$0.48 (ultra-budget)

---

## Avant de lancer le test

### 1. Vérifier la clé API OpenRouter

```bash
# Récupérer votre clé depuis https://openrouter.ai/keys
export OPENROUTER_API_KEY=sk-or-v1-...

# Vérifier que la clé est valide
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | jq .
```

### 2. Vérifier les quotas et le solde

```bash
# Affiche votre utilisation et solde restant
curl -s https://openrouter.ai/api/v1/credits \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | jq .
```

**Coût estimé du test complet:** ~$0.05–0.10 (4 modèles × 2000 tokens, web search inclus)

---

## Exécuter le test

### Option 1: Lancer le script complet

```bash
cd /home/user/Scenario

# Avec API key en variable d'environnement
export OPENROUTER_API_KEY=sk-or-v1-...
python3 scripts/edition/test-model-comparison.py

# Résultats: scripts/edition/test-results.json
```

**Durée estimée:** 2–3 minutes (1 appel par modèle, ~30–60s chacun)

### Option 2: Tester un modèle individuellement

```bash
# Test Haiku 4.5 uniquement (repli recherche)
python3 scripts/edition/generate_fallback_brief.py \
  --date 2026-09-21 \
  --test-haiku

# Test Sonnet 5 (baseline)
python3 scripts/edition/generate_fallback_brief.py \
  --date 2026-09-21

# Test modèle custom
python3 scripts/edition/generate_fallback_brief.py \
  --date 2026-09-21 \
  --model sakana/fugu-max
```

---

## Interpréter les résultats

### Tableau de comparaison

Le script génère un résumé comparatif avec 3 colonnes:

```
Modèles fonctionnels:
  - Sonnet 5               | Coût: $0.0234 | Temps: 42.3s
  - Haiku 4.5              | Coût: $0.0089 | Temps: 38.1s
  - Sakana Fugu Max        | Coût: $0.0198 | Temps: 55.2s

Modèles échoués:
  - DeepSeek v4            | Erreur: Invalid tool call
```

### Critères d'évaluation

Pour chaque modèle réussi, la recommandation considère:

1. **Coût réel** (le plus important pour le budget)
   - Voir colonne `Coût` → comparer $/appel
   - Extrapoler à 365 jours: `$0.01 × 365 = $3.65/mois`

2. **Temps d'exécution**
   - Voir colonne `Temps` → mesure la latence
   - Moins important que le coût pour une recherche quotidienne (~5 min de tolérance)

3. **Qualité de la réponse**
   - Vérifier que le JSON est valide (le script le vérifie)
   - Lire le préaperçu de la réponse → contexte et sujets pertinents
   - Vérifier que web_search a été utilisé (voir logs)

### Fichier de résultats complets

`scripts/edition/test-results.json` contient les données brutes:

```json
{
  "timestamp": "2026-09-21T14:30:00...",
  "models": [
    {
      "name": "Haiku 4.5",
      "model_id": "anthropic/claude-haiku-4-5-20251001",
      "success": true,
      "cost": 0.0089,
      "elapsed_s": 38.1,
      "error": null
    },
    ...
  ]
}
```

---

## Recommandation basée sur résultats

### Cas 1: Haiku 4.5 réussit et coûte 50% moins cher

✅ **→ Lancer Phase 1 de test en production**

```bash
# Modifier generate_fallback_brief.py pour utiliser Haiku par défaut
# (ou via --test-haiku pendant 5–7 jours)
python3 scripts/edition/generate_fallback_brief.py --test-haiku
```

Mesurer pendant 5–7 jours:
- Coût réel sur dashboard OpenRouter (`assets/data/openrouter-cost.json`)
- Qualité des briefs (pas de doublon, faits sourcés)
- Qualité de la rédaction finale (article publié)

### Cas 2: Sakana Fugu Max réussit mais Haiku échoue

→ Phase 2: Tester Sakana Fugu Max

```bash
python3 scripts/edition/generate_fallback_brief.py \
  --date 2026-09-21 \
  --model sakana/fugu-max
```

### Cas 3: Tous échouent

→ Vérifier:
- Clé API valide et solde suffisant
- Quotas OpenRouter respectés (rate limiting)
- Logs d'erreur détaillés dans la sortie

---

## Annexe: Architecture du test

### Test prompt

Le script utilise un prompt simplifié qui:
1. Demande 3 sujets d'actualité pertinents (derniers 7 jours)
2. Demande impact économique/géopolitique mesurable
3. Demande 3 chiffres-clés avec sources
4. Demande format JSON structuré

**Rationale:** C'est la tâche réelle que `generate_fallback_brief.py` fait, mais condensée pour tester vite (2000 tokens max vs 12000 en production).

### Web search usage

Le script inclut `"tools": [{"type": "openrouter:web_search", ...}]` pour tous les modèles. Cela force le modèle à:
- Décider d'utiliser web_search ou pas
- Formule des requêtes pertinentes
- Intègre résultats dans réponse

C'est le **critère clé** pour la recherche éditorial: le modèle doit vraiment chercher, pas halluciner.

---

## Notes importantes

⚠️ **Budget:** Le test complet coûte ~$0.05–0.10. À faire après vérification du solde.

⚠️ **Timeout:** Chaque appel timeout après 120s (web_search côté serveur peut être lent).

⚠️ **Reasoning disabled:** Pour Anthropic et DeepSeek, le raisonnement étendu est désactivé (sinon JSON vide, voir incident GPT-5 dans `docs/modeles-openrouter.md`).

⚠️ **Modèles:** Si un modèle change d'ID/disponibilité, editer `test-model-comparison.py` `MODELS_TO_TEST`.

---

## Historique des tests

| Date | Modèles | Gagnant | Note |
|------|---------|---------|------|
| 2026-09-21 | H4.5, S5, Fugu, DS | TBD | Phase 1 initiale |
