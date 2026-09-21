# Étude : Modèle plus efficace pour la recherche quotidienne

**Date:** 2026-09-21  
**Statut:** Analyse + plan de test  
**Objectif:** Atteindre 10 $/mois max pour OpenRouter (actuellement ~18.5 $/mois)

## Contexte

- Recherche quotidienne (`generate_fallback_brief.py`): 0.40 $/jour = **12 $/mois** (Sonnet 5)
- Rédaction quotidienne (`generate_daily_edition.py`): 0.30 $/jour = **9 $/mois** (Sonnet 5, non négociable)
- Autres workflows: ~0.5 $/mois
- **Total actuel:** ~21.5 $/mois
- **Cible:** 10 $/mois max

Le défi : la rédaction est déjà à 9 $/mois, il ne reste 1 $ pour tous les autres workflows. **La recherche doit passer de 12 $ à <1 $**, ce qui demande soit un modèle 90% moins cher, soit de réduire drastiquement la fréquence.

## Candidats identifiés

### 1. Claude Haiku 4.5 (Anthropic)

**Pricing:** $1 input / $5 output (50% moins cher que Sonnet 5)

**Pros:**
- Même famille que Sonnet → compatible avec `openrouter:web_search`
- Partage le même écosystème de tools/tokens
- Retrait instantané si qualité insuffisante (pas de breaking changes)

**Cons:**
- Haiku est positionné comme modèle d'entrée de gamme
- Peut être moins efficace sur jugement éditorial complexe (sujet, anti-doublon)
- Économie : ~0.20 $/jour = 6 $/mois, porte le total à ~15.5 $/mois (toujours au-dessus de 10 $)

**Test suggéré:** `generate_fallback_brief.py --model anthropic/claude-haiku-4-5`

---

### 2. Sakana Fugu Max (Sakana AI)

**Pricing:** $2 input / $6 output (compétitif vs Sonnet 5)

**Pros:**
- Web search **intégré** (`built-in web search and web fetch`) — pas besoin du tool OpenRouter
- Modèle optimisé pour recherche et analysis
- Expert agent selection (multi-expert routing selon la tâche)

**Cons:**
- Pas d'économie réelle vs Sonnet (identique en input, moins cher en output)
- Nouveau modèle, peu d'historique en production
- Nécessiterait vérifier que la réponse JSON reste compatible

**Test suggéré:** `generate_fallback_brief.py --model sakana/fugu-max`

---

### 3. DeepSeek v4 (OpenRouter)

**Pricing:** $0.12 input / $0.48 output (95% moins cher)

**Pros:**
- Réduction drastique du coût (~0.02 $/jour = 0.6 $/mois)
- Déjà utilisé avec succès pour `hot-topics.py` (repérage, pas rédaction)

**Cons:**
- **Problème critique:** pas de web search natif documenté
- Historique de troncature sur texte long/structuré (voir `docs/modeles-openrouter.md`)
- Utilisé seulement pour tâches courtes, pas production-grade pour recherche complète
- Risque élevé de défaillance sur anti-doublon/sources complexes

**Test:** Non recommandé comme remplacement direct

---

### 5. NVIDIA Nemotron 3 Ultra (NVIDIA) — 🆕 GRATUIT

**Pricing:** $0 input / $0 output (GRATUIT sur OpenRouter)

**Pros:**
- Coût zéro = résout directement le budget (1 $/mois complet)
- Modèle frontier reasoning récent et puissant
- Support natif du web search (built-in reasoning)

**Cons:**
- Modèle très récent, peu d'historique production
- Peut être lent (frontier reasoning coûte en latence)
- Nécessite vérifier que JSON output reste compatible

**Potentiel:** Si fonctionne = 100% de réduction, total = 9 $/mois (objectif atteint)

---

### 6. GLM 5.3 Flash (Zhipu AI) — 🆕

**Pricing:** ? (à vérifier sur OpenRouter, probablement très bas)

**Pros:**
- Nouvelle génération modèle chinois, optimisé pour latence basse
- "Flash" dans le nom = probablement budget-friendly
- Support web search potentiel

**Cons:**
- Pricing inconnu
- Peu de données sur qualité rédaction en français/recherche éditoriale

**Potentiel:** À tester pour déterminer coût et qualité

---

### 7. Tencent HY4 Preview (Tencent) — 🆕

**Pricing:** ? (à vérifier, modèle preview)

**Pros:**
- Modèle frontier chinois récent
- Preview = peut être gratuit ou très bon marché
- Support web search potentiel

**Cons:**
- Status "preview" = stabilité incertaine
- Pricing complètement inconnu
- Peu de données de qualité

**Potentiel:** À tester si Nemotron ou GLM ne suffisent pas

---

### 8. Xiaomi MIMO v2.5 (Xiaomi) — 🆕

**Pricing:** ? (à vérifier)

**Pros:**
- Modèle mobile-optimized récent
- Peut être très bon marché pour latence basse
- Support web search potentiel

**Cons:**
- Pricing inconnu
- Modèle peu connu en contexte production occidental
- Données de qualité limitées

**Potentiel:** À tester pour évaluer coût et capacité recherche

---

### 9. Upstage Solar Pro 4 (Upstage) — 🆕

**Pricing:** ? (à vérifier)

**Pros:**
- Modèle frontier coréen récent
- Peut être optimisé pour recherche et extraction
- Support web search potentiel

**Cons:**
- Pricing inconnu
- Modèle peu connu en Occident
- Données de qualité limitées

**Potentiel:** À tester pour évaluer coût et qualité rédaction

---

### 10. Mistral Medium 3.1 (Mistral AI) — 🆕

**Pricing:** ? (compétitif, probablement bas)

**Pros:**
- Mistral est leader en modèles ouverts cost-efficient
- Medium 3.1 = nouveau, probablement meilleur ratio coût/qualité
- Support web search documenté

**Cons:**
- Pricing inconnu mais probablement > DeepSeek
- Historique de régressions en JSON structuré
- Pas testé sur recherche éditoriale française

**Potentiel:** Candidat sérieux si pricing bas

---

### 11. DeepSeek v4.1 Flash (DeepSeek) — 🆕

**Pricing:** ? (ultra-budget, probablement < $0.12/$0.48)

**Pros:**
- Version "Flash" = optimisée pour coût ultra-bas
- DeepSeek connu pour tarifs imbattables
- Amélioration probable vs v4 standard

**Cons:**
- "Flash" = peut sacrifier qualité pour vitesse
- Historique de troncature sur texte long
- v4 déjà problématique sur rédaction

**Potentiel:** À tester mais risqué pour recherche complète

---

### Modèles alternatifs non explorés

- **Claude Haiku 3.5** (ancienne génération) — coûts similaires à Haiku 4.5, qualité inférieure
- **Qwen** (Alibaba) — modèles bon marché, mais web search non documenté
- **Mistral** — modèles compétitifs, web search pas clair
- **Open models** (Llama, etc.) — existent sur OpenRouter, mais pas d'avantage prouvé + web search généralement absent

---

## Calcul du gap

Pour atteindre 10 $/mois avec rédaction = 9 $/mois **immuable** :

- Budget restant : 1 $
- Recherche doit coûter : < 0.033 $/jour
- Réduction requise vs Sonnet 5 (0.40 $/jour) : **92%**

**Conclusion:** Aucun modèle seul ne suffira. Deux approches :

1. **Combinaison Haiku 4.5 + réduction fréquence** (par exemple : recherche 3x/semaine au lieu de 7x/semaine → 0.20 $ * 3/7 = 0.086 $/jour, mais perte d'actualité)
2. **Réactiver trigger CCR** (routine recherche/brief interactif) avec safeguards token + laisser recherche OpenRouter en vrai repli → élimine les appels quotidiens déterministes

---

## Plan de test immédiat

**Hypothèse de travail:** Haiku 4.5 est un bon candidat pour tester si la qualité de recherche peut être préservée avec 50% de réduction.

### Phase 1 : Test Haiku 4.5 sur recherche (3–5 jours)

1. **Branche:** `test/haiku-fallback-brief`
2. **Changement:** `FALLBACK_MODEL = "anthropic/claude-haiku-4-5"` dans `generate_fallback_brief.py`
3. **Fréquence:** Laisser les runs quotidiens se faire normalement (lun-dim, 14:00 UTC `post-edition.yml`)
4. **Critères de succès:**
   - Brief JSON valide chaque jour (passe `validate_brief()`)
   - Coûts réels vs estimés (dashboard OpenRouter)
   - Qualité rédactionnelle de l'article final (lecture humaine)
   - Pas de régression sur anti-doublon (pas de répétition d'anciens sujets)

5. **Rollback automatique si:** Brief invalide deux fois de suite, ou coûts > estimé + 20%

### Phase 2 (conditionnel) : Test Sakana Fugu Max

- Si Haiku fonctionne mais insuffisant en qualité
- Même durée (3–5 jours)
- Critères identiques

### Phase 3 (optionnel) : Réactivation CCR avec safeguards

- Pas de changement de modèle, mais activation du trigger CCR avec monitoring token strict
- Laisser OpenRouter comme repli uniquement si CCR timeout/blocage

---

## Recommendation immédiate

✅ **Lancer le test Phase 1 (Haiku 4.5) dès aujourd'hui**

Raison : Haiku 4.5 est un candidat très faible risque (même famille Anthropic, API compatible, rollback trivial en une ligne), avec un upside potentiel de 50% de réduction. Même si la qualité se dégrade légèrement, c'est l'unique levier visible pour approcher le budget de 10 $/mois sans sacrifier la rédaction (le vrai produit).

La décision définitive (garder Haiku, basculer sur Sakana, ou réactiver CCR) pourra être prise après 5 jours de données réelles.
