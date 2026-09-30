# Directives du Projet — Scénario (https://lesscenarios.fr)

Ce document consigne les règles fondamentales, contraintes architecturales et conventions éditoriales du projet **Scénario**. Tout agent Antigravity opérant dans ce dépôt doit impérativement respecter ces principes.

---

## 1. Vue d'ensemble du Projet

- **Site** : Journal d'actualité en ligne statique décryptant chaque sujet en 3 scénarios chiffrés.
- **URL de production** : https://lesscenarios.fr
- **Hébergement** : GitHub Pages (servi directement depuis la branche `main` du dépôt `loliba92/Scenario`).
- **Nom de domaine** : Configuré via le fichier `CNAME`.
- **Zéro backend / Zéro framework** : Tout le site repose sur du HTML, du CSS et du JavaScript pur (Vanilla). Aucun bundler (Vite, Webpack), aucun framework (React, Vue), aucun build Jekyll (présence du fichier `.nojekyll` à la racine).

---

## 2. RÈGLE D'OR ARCHITECTURALE : Autonomie des Fichiers HTML & CSS

> [!CAUTION]
> **Ne JAMAIS factoriser ou externaliser le CSS dans une feuille de style partagée (`style.css`).**
> Chaque page HTML (`index.html`, pages dans `archives/`, `suivi/`, `hebdo/`, etc.) doit rester **100% autonome**.

1. **CSS Inline obligatoire** : Tout le style d'une page doit être contenu dans un bloc `<style>` unique dans le `<head>` de cette page.
2. **Immuabilité des archives** : Les fichiers sous `archives/AAAA-MM-JJ.html` représentent des publications passées figées dans le temps. Ils ne doivent jamais être rétroactivement altérés ni dépendre d'un style global qui pourrait évoluer.
3. **Protection contre l'écrasement de style** : Lors de toute modification ou régénération du `<head>` (métadonnées SEO, tags sociaux, etc.), vérifier absolument que la balise `<style>` complète est préservée. *Incident de référence du 26/09/2026 : un script avait vidé le style lors d'une mise à jour SEO, rendant la page noire en production. Le workflow `.github/workflows/html-style-check.yml` sert désormais de garde-fou.*

---

## 3. Gabarit d'Édition (`index.html`)

Chaque édition quotidienne respecte une structure rigoureuse :
1. **Masthead** : Logo (`assets/logo.svg`), nom Scénario, numéro d'édition et date. La date d'affichage (« Publié le ... ») est déduite automatiquement en JavaScript depuis la ligne du bandeau (jamais codée en dur).
2. **Barre de navigation** : Liens Accueil, Archives, Le projet, Contact.
3. **Hero & Encarts** :
   - Eyebrow (registre du jour : Économie, Géopolitique, Santé, etc.).
   - Titre percutant.
   - Encart `.question-box` (« La question posée »).
   - 4 à 6 paragraphes de contexte (`.dek`).
   - Bandeau d'indicateurs chiffrés (`.indicator-strip`).
   - Encart optionnel `.list-box` pour les classements ou listes d'items scannables.
4. **Les 3 Scénarios** :
   - Trois cartes `.card[data-kind=favorable|stable|degrade]`.
   - Chacune comporte : jauge SVG animée (`data-pct`), mot-repère de probabilité, titre + emoji, explication détaillée, indicateurs chiffrés et la mention « Concrètement en France ».
   - **Règle absolue des probabilités** : La somme des pourcentages des 3 scénarios doit TOUJOURS faire strictement **100%**.
5. **Lexique & Sources** : Définition des termes techniques, sources officielles et avertissement méthodologique légal.

---

## 4. Pipeline d'Automatisation Quotidienne (cron-job.org ➔ OpenRouter)

Tous les schedulers sont pilotés depuis **cron-job.org** qui envoie des requêtes HTTP (`GET` vers l'API `workflow_dispatch` de GitHub Actions) :

### A. Phase 1 : La Preview de l'édition du lendemain (14h00 UTC / ~16h Paris)
Déclenché par `daily-preview.yml` via cron-job.org :
1. **Étape 1 — Le Brief (`editorial-briefs/AAAA-MM-JJ.json`)** :
   - Premier appel **OpenRouter** (modèle de recherche avec navigation web).
   - Sélectionne le sujet du jour dans `sujets-prioritaires.md`, vérifie les faits, teste les sources réelles et extrait les indicateurs chiffrés.
   - Produit un fichier JSON très structuré respectant le schéma de `docs/routine-brief-format.md`.
2. **Étape 2 — La Rédaction de l'édition** :
   - Deuxième appel **OpenRouter** (modèle de rédaction fluide, ex. Gemini Flash).
   - Rédige l'édition complète à partir du brief JSON.
   - Génère `preview.html` (page complète rendue) et `.preview-content.json`.
3. **Étape 3 — Critique automatique & Relecture** :
   - Un modèle tiers (`deepseek-v4-flash`) effectue une critique interne de cohérence (dates, chiffres, ton) et ouvre une issue GitHub récapitulative.
   - Relecture humaine de `preview.html` l'après-midi.

### B. Phase 2 : La Publication en production (06h00 UTC / ~8h Paris)
Déclenché par `post-edition.yml` via cron-job.org :
1. **Archivage immuable** : La version finale est copiée sous `archives/AAAA-MM-JJ.html`.
2. **Mise à jour vitrine** : `index.html` est mis à jour avec la nouvelle édition.
3. **Post-édition & Réseaux** :
   - Mise à jour des flux `feed.xml`, `sitemap.xml`, `sitemap-news.xml`, `glossaire.html`.
   - Génération de l'image de partage et du post réseaux sociaux (`pub.yml` ➔ `feed-pub.xml` ➔ Make.com).
   - Traduction miroir anglaise automatique (`translate-en.yml` ➔ `en/index.html` et `en/archives/`).

### C. Pages Clés de Pilotage & Ligne Éditoriale
- **`le-projet.html`** : Définit la mission, la promesse, la méthode de calcul et la grille thématique des 7 jours (lundi économie, mardi carte blanche, etc.). À consulter pour toute question de positionnement.
- **`dashboard.html`** : Tableau de bord de supervision interne mesurant l'audience via l'API GoatCounter (`reads.json`, hits cumulés), les coûts réels consommés sur OpenRouter et les derniers sujets détectés.

### D. Distribution Multicanale via RSS et Make.com (`assets/make/`)
Tous les jours à **9h00 Paris**, une automatisation **Make.com** lit les flux RSS du site et publie les contenus sur l'ensemble des canaux sociaux :
- **Scénario quotidien (`assets/make/scenario-daily.blueprint.json`)** :
  - **Flux consommés** : `feed.xml` (édition du jour), `feed-suivi.xml` (dossiers en cours), `feed-pub.xml` (posts optimisés réseaux), et leurs miroirs anglais (`en/feed*.xml`).
  - **Réseaux cibles** : Telegram, X/Twitter (via Buffer), Instagram Business, Facebook Pages, LinkedIn, Bluesky, Threads, notifications push OneSignal.
  - **Mécanique** : Téléchargement des visuels générés (`http:DownloadFile`), temporisations (`util:FunctionSleep`) pour respecter les quotas d'API, et tolérance aux pannes (`builtin:Ignore`) sur chaque canal.
- **Scénario hebdomadaire (`assets/make/scenario-weekly.blueprint.json`)** :
  - Consomme `feed-weekly.xml` pour diffuser le récapitulatif du dimanche (LinkedIn, Telegram, Buffer).



---

## 5. Rôle de l'Agent Antigravity dans ce Dépôt

1. **Assistance au développement et maintenance** :
   - Modifier ou créer des pages HTML en respectant la charte graphique et l'autonomie CSS.
   - Diagnostiquer et corriger les scripts Python dans `scripts/` ou les workflows dans `.github/workflows/`.
   - Mettre à jour `sujets-prioritaires.md`, `docs/ARCHITECTURE.md` et `docs/BACKLOG.md`.
2. **Validation par le navigateur (`browser_subagent`)** :
   - Avant de valider un changement visuel sur `index.html` ou une page de suivi, utiliser l'outil navigateur pour inspecter le rendu, vérifier la lisibilité sur mobile et desktop, et s'assurer de l'absence de bugs visuels.
3. **Gestion Git** :
   - La branche par défaut et de production est `main`.
   - Ne jamais committer de fichiers système (`.DS_Store`) ou de fichiers de logs temporaires.
