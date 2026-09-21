# 📊 RAPPORT COMPLET - TESTS MODÈLES OPENROUTER
**Date:** 2026-09-21  
**Objectif:** Trouver modèles optimisant budget à 10 $/mois

---

## 🎯 RÉSUMÉ EXÉCUTIF

### ✅ OBJECTIF ATTEINT

**Combinaison gagnante identifiée :**

| Task | Modèle | Coût/unité | Coût mensuel |
|------|--------|-----------|--------------|
| **Recherche** | Upstage Solar Pro 4 | $0.00013257/brief | ~$0.004 |
| **Rédaction** | NVIDIA Nemotron 3 Ultra | $0/article | **$0.00** |
| **Autres** | (existants) | - | ~$0.5 |
| | | **TOTAL** | **~$0.50/mois** |

**Budget actuel:** 21.5 $/mois → **Nouvel budget: 0.50 $/mois** ✅  
**Réduction:** 97.7% | **Économie:** 21 $/mois

---

## 📈 RÉSULTATS RECHERCHE (complet)

**10 modèles testés** - Tous fonctionnels sauf 1 timeout

### Classement par coût

1. 🥇 **Upstage Solar Pro 4** - $0.00013257 (2.8s) ✅ **WINNER**
2. 🥈 Sakana Fugu Max - $0.001324 (3.0s)
3. 🥉 DeepSeek v4 - $0.00931006 (23.1s)
4. Xiaomi MIMO v2.5 - $0.0235563664 (37.5s)
5. Mistral Medium 3.1 - $0.03594472 (17.3s)
6. DeepSeek v4.1 Flash - $0.0390094 (64.4s)
7. GLM 5.3 Flash - $0.0488397 (39.3s)
8. Tencent HY4 Preview - $0.066006877 (55.7s)
9. Sonnet 5 (baseline) - $0.171432 (25.3s)
10. ❌ NVIDIA Nemotron - TIMEOUT

### Qualité réponse

- **Upstage Solar Pro 4:** Réponse complète, bien structurée, sources variées ✅ Excellent
- **Sakana Fugu Max:** JSON tool-calls brutes (valides mais raw)
- **DeepSeek v4:** Texte libre avec bonne structure
- **Autres:** Acceptables, quelques variations format

### Performance

- **Plus rapide:** Upstage (2.8s) & Sakana (3.0s)
- **Acceptable (<30s):** Sonnet, Mistral, DeepSeek v4
- **Lent (>30s):** Tous les autres

---

## 📝 RÉSULTATS RÉDACTION (partiel)

**3 modèles complètement testés** avant timeout système

### Résultats

| Modèle | Coût | Temps | JSON valide | Status |
|--------|------|-------|-------------|--------|
| **NVIDIA Nemotron 3 Ultra** | **$0** | 159s | ✅ **YES** | ✅ EXCELLENT |
| GLM 5.3 Flash | $0.0077292 | 49.9s | ❌ No | ⚠️ Acceptable |
| Tencent HY4 Preview | $0.040121748 | 129.9s | ❌ No | ⚠️ Lent |

### Analyse

**NVIDIA Nemotron 3 Ultra :**
- ✅ **GRATUIT** ($0/article)
- ✅ **JSON valide** avec structure complète
- ✅ Structure correcte : h1, question_text, section_title, dek, stakes_branches
- ⚠️ Lent (159s) mais acceptable pour rédaction asynchrone quotidienne
- 🎯 **PERFECT pour Phase 1 rédaction**

**GLM 5.3 Flash :**
- ✅ Coût très bas ($0.0077)
- ❌ JSON invalide (parsing failed)
- ⚠️ Latence moyenne (49.9s)
- ℹ️ Candidat secondaire si Nemotron échoue

**Tencent HY4 Preview :**
- ⚠️ Coût modéré ($0.040)
- ❌ JSON invalide
- ❌ Très lent (129.9s)
- ℹ️ Pas recommandé

---

## 🚀 PLAN DE DÉPLOIEMENT

### Phase 1 : Recherche (semaine 1)

**Changement :** Remplacer Sonnet 5 par Upstage Solar Pro 4

```python
# scripts/edition/generate_fallback_brief.py
FALLBACK_MODEL = "upstage/solar-pro4"  # Was: "anthropic/claude-sonnet-5"
```

**Monitoring :**
- Validité JSON briefs (chaque jour)
- Coûts réels vs estimés
- Qualité rédactionnelle articles
- Absence doublon sujets

**Critères succès :**
- 0 failures sur 7 jours
- Coûts réels ≤ $0.0005/brief
- Qualité stable vs Sonnet

**Rollback si :** 2 failures ou coûts > seuil

---

### Phase 2 : Rédaction (semaine 2+)

**Changement :** Remplacer Sonnet 5 par NVIDIA Nemotron 3 Ultra

```python
# scripts/edition/generate_daily_edition.py
EDITION_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
```

**Monitoring :**
- Validité JSON articles
- Pas d'erreurs parsing
- Qualité rédactionnelle (lecture humaine)

**Critères succès :**
- Coûts confirmés à $0
- JSON valide tous les jours
- Qualité ≥ baseline Sonnet

**Rollback si :** JSON parsing failures 2x, ou dégradation qualité

---

## 💡 INSIGHTS CLÉS

### 1. Upstage Solar Pro 4 = "Dark horse" 
- Modèle coréen peu connu en Occident
- **1294× moins cher que Sonnet** sur recherche
- Réponse structurée, rapide, qualité conservée
- Aucun risque apparent → LOW RISK pick

### 2. NVIDIA Nemotron = "Free tier surprise"
- Modèle "frontier reasoning" gratuit sur OpenRouter (!?)
- JSON valide pour rédaction
- Lenteur acceptable pour workflow asynchrone
- Réduit coût rédaction de 9 $/mois à **0**

### 3. Sakana Fugu Max = "Backup option"
- Si Upstage échoue, fallback à Sakana Fugu Max
- Très compétitif ($0.001324 vs $0.00013257)
- Web search natif (peut être advantage ou disadvantage)

### 4. Autres modèles
- Mistral Medium 3.1 = bon, mais 273× plus cher qu'Upstage
- DeepSeek v4 = acceptable, mais 71× plus cher
- Tencent/GLM/Xiaomi = lents + problèmes JSON

---

## 📋 DÉCISIONS RECOMMANDÉES

### ✅ MAINTENANT
1. Merger branch `claude/article-key-takeaway-rl8p4p`
2. Deployer Phase 1 (Upstage recherche)
3. Monitorer 7 jours en production

### ⏳ APRÈS 7 JOURS
1. Si recherche stable → Déployer Phase 2 (Nemotron rédaction)
2. Évaluer économies réelles vs estimées
3. Décider : garder, affiner, ou rollback

### 🆘 SI PROBLEME
1. Recherche échoue → Basculer Sakana Fugu Max ($0.001324)
2. Rédaction échoue → Basculer GLM 5.3 Flash ($0.0077)
3. Catastrophe → Rollback complet Sonnet 5

---

## 🎓 APPRENTISSAGES

1. **Modèles asiatiques ultra-compétitifs** - Upstage, GLM, Tencent dominent coût
2. **Frontier models = gratuité** - Nemotron libre suggère stratégie OpenRouter
3. **Latence acceptable pour async** - 159s ok pour rédaction quotidienne
4. **Web search != coût réduit** - Sakana cher malgré web search built-in
5. **JSON parsing = blocker** - GLM/Tencent invalides, disqualifie candidats

---

## 📞 CONTACTS POUR ESCALADE

- **Problème Upstage** → Tester Sakana ou DeepSeek v4
- **Problème Nemotron (timeout recherche)** → Nemotron rédaction ok, utiliser Upstage
- **Problème coûts** → Vérifier token counts OpenRouter dashboard
- **Problème qualité** → Comparer articles Upstage vs Sonnet manuellement

---

**Statut:** ✅ **PRÊT POUR PRODUCTION**  
**Date recommandée déploiement Phase 1:** ASAP (lendemain 2026-09-22)  
**Budget attendu post-déploiement:** **$0.50/mois** (vs 21.5 $/mois)

