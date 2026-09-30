---
name: scenario-editorial
description: Aide à la production, la relecture, le test et la publication d'une édition ou d'un suivi pour le site Scénario (lesscenarios.fr). Utilise ce skill dès que l'utilisateur souhaite créer, modifier, auditer une édition quotidienne, un brief éditorial, vérifier l'état des workflows GitHub Actions ou inspecter visuellement le rendu du site.
---

# Skill : Gestion Éditoriale & Workflows Scénario

Ce skill fournit les procédures opérationnelles pour travailler sur le site **Scénario** dans Antigravity.

---

## 1. Vérification de l'État des Workflows GitHub

Pour vérifier si les routines matinales ont bien tourné :

```bash
# Lister les 10 dernières exécutions de workflows
gh run list --limit 10

# Voir les détails d'un run spécifique
gh run view <run-id> --log-failed
```

Workflows clés :
- `post-edition.yml` : Rédaction et publication de l'édition du jour
- `detection.yml` : Suivis thématiques hebdomadaires
- `pub.yml` : Post réseaux sociaux (feed-pub.xml)
- `translate-en.yml` : Traduction miroir EN
- `html-style-check.yml` : Vérification de la présence du CSS sur toutes les pages

Pour déclencher un workflow manuellement :
```bash
# Déclencher post-edition en publication réelle (défaut)
gh workflow run post-edition.yml

# Déclencher post-edition en bac à sable (sans commit/push)
gh workflow run post-edition.yml -f publish=false
```

---

## 2. Règles Éditoriales Fondamentales

Toute édition produite ou modifiée doit respecter :
1. **Les 3 scénarios** : Favorable, Stable, Dégradé.
2. **La somme des probabilités** : Strictement égale à **100%**.
3. **Le style HTML** : Le CSS doit TOUJOURS rester inline dans `<style>` au sein du `<head>`. Ne jamais le factoriser.
4. **Composants visuels** :
   - `.question-box` pour la question centrale.
   - `.indicator-strip` pour les chiffres clés.
   - `.card` avec `data-kind` et `data-pct` pour les scénarios.
   - `.list-box` pour tout classement ou liste structurée (jamais de liste brute non stylée).

---

## 3. Inspection Visuelle avec le Browser Subagent

Avant de valider ou committer une modification visuelle sur `index.html` ou une page d'archive :
1. Utiliser `browser_subagent` pour charger la page en local (`file:///Volumes/Data/Scenario/index.html`) ou en production (`https://lesscenarios.fr`).
2. Vérifier :
   - Présence du logo et du masthead.
   - Animation des jauges des cartes.
   - Cohérence visuelle en mode desktop et mobile.
   - Absence de page noire ou de style manquant.
