# BACKLOG

> Backlog produit et technique de Scénario. Contenu déplacé à l'origine depuis `docs/ARCHITECTURE.md` (sections « Backlog » et « Ce qui reste à faire (suivi) »), pour garder `ARCHITECTURE.md` focalisé sur l'architecture technique. Les anciens renvois internes du type « voir plus haut/plus bas dans ce backlog » font référence à ce fichier-ci ; ils ont été remplacés par des renvois d'ID (`B0xx`) partout où c'était possible.

**Comment lire ce fichier.** Un ticket existe à **un seul endroit** et ne se déplace **jamais** : quand son statut change, seuls ses champs (Statut / Dernière MAJ / Prochaine action / Blocage / État actuel) et sa ligne d'index sont mis à jour, plus un événement ajouté en Historique. Pour répondre à une question : chercher le sujet dans l'**INDEX RAPIDE** → lire statut + prochaine action → si insuffisant, ouvrir la fiche (État actuel d'abord, puis Décisions/Historique).

**Statuts utilisés** : `À FAIRE`, `EN COURS`, `EN TEST`, `BLOQUÉ`, `STANDBY`, `À DÉCIDER`, `FAIT`, `ABANDONNÉ`. Un statut suivi de « (à confirmer) » signale que le contenu d'origine ne permet pas de trancher avec certitude.

**Priorités** : P0 (le plus urgent, échelle reprise de l'audit externe du 27 août) à P3 (utile mais plus lourd ou moins prioritaire). « — » = jamais chiffrée dans le backlog d'origine.

**Ordre des tickets** : ordre d'apparition dans le backlog d'origine, figé. Les IDs `B001`…`B151` sont stables et ne changent jamais, même si le titre change.

**Dates** : toutes les dates de ce fichier sont en 2026, sauf mention contraire. Dernière restructuration complète : 2026-09-18.

## INDEX RAPIDE

| ID | Sujet | Statut | Priorité | Dernière MAJ | Prochaine action |
|---|---|---|---|---|---|
| B001 | Recadrage photo des images sociales (pub/suivi) | À FAIRE | P2 | 2026-09-17 | Remonter l'ancrage vertical du crop, valider sur plusieurs photos |
| B002 | Chaîne rédaction + post-édition OpenRouter (prototype) | EN TEST | P1 | 2026-09-14 | Tester en conditions réelles sur GitHub Actions |
| B003 | Threads comme canal de diffusion (via Buffer) | FAIT | P1 | 2026-09-05 | — |
| B004 | Migrer la newsletter de Buttondown vers OneSignal | STANDBY | P3 | 2026-08-29 | Ne rien entamer avant le rappel du 2027-04-01 |
| B005 | Version anglaise du site (MVP `en/`) | FAIT | P3 | 2026-09-03 | — |
| B006 | Traduire le récap hebdo en anglais | À DÉCIDER | P2 | 2026-08-29 | Trancher le scope des liens « Lire l'édition → » |
| B007 | Traduire `le-projet.html` et les pages légales en anglais | À DÉCIDER | — | 2026-08-29 | Lever les 2 réserves (RGPD/juridique, glossaire) |
| B008 | Traduction rétroactive des archives en anglais | À DÉCIDER | — | 2026-08-31 | Revisiter le 2026-09-15, avec B139 |
| B009 | Déclinaison papier — « Les Cahiers de Scénario » | STANDBY | P3 | 2026-08-25 | Partir de la maquette du 25 août pour la Phase 1 |
| B010 | Image de pub Instagram générique (brand-teaser) | FAIT | — | 2026-08-09 | Pousser l'image en pub Meta (geste utilisateur) |
| B011 | WhatsApp comme canal de distribution | À FAIRE | P2 | 2026-08 | Explorer le module natif WhatsApp Business Cloud API |
| B012 | Pub payante (Meta/X) et distribution gratuite | À FAIRE | P2 | 2026-08-10 | Tracking de conversion avant toute dépense |
| B013 | Flux RSS dérivé propre pour les lecteurs RSS | À FAIRE | P3 | 2026-08-15 | Scoper le script (nom, fréquence, lien) |
| B014 | Bluesky comme canal de diffusion | FAIT | P1 | 2026-08-15 | — |
| B015 | Mastodon comme canal de diffusion | À FAIRE | P1 (à confirmer) | 2026-08-15 | Vérifier s'il existe un module Mastodon natif dans Make |
| B016 | Réseaux écartés (Pinterest, Reddit, Discord, YouTube) | ABANDONNÉ | — | 2026-08-15 | — |
| B017 | Posts « pub » en Reel + TikTok | BLOQUÉ | P2 | 2026-08-15 | Construire l'étape de génération vidéo (mp4) |
| B018 | Giveaway newsletter (tirage au sort) | STANDBY | P3 | 2026-08-10 | Reprendre à quelques dizaines/centaines d'abonnés |
| B019 | Boutons de partage sur chaque édition (+ icônes) | FAIT | — | 2026-08-08 | — |
| B020 | X (Twitter) comme canal de diffusion | FAIT | — | 2026-08-15 | — |
| B021 | Image sur les posts X et Facebook (Daily) | FAIT | — | 2026-08-08 | — |
| B022 | LinkedIn : passage au post Image natif | FAIT | — | 2026-08-11 | — |
| B023 | Teaser des posts sociaux : `source` vs `comments` | FAIT | — | 2026-08-11 | — |
| B024 | Diffusion automatique sur Instagram | FAIT | — | 2026-08-15 | — |
| B025 | Diffusion automatique sur Facebook | FAIT | — | 2026-08-15 | — |
| B026 | Génération de l'image Instagram par édition | FAIT | — | 2026-08-11 | — |
| B027 | Image du sujet par photo libre de droits (Pexels/Pixabay) | FAIT | P1 | 2026-08-19 | — |
| B028 | Image Instagram pour le récap hebdo | ABANDONNÉ | — | 2026-08-08 | — |
| B029 | Abonnement quotidienne + hebdo (metadata Buttondown) | FAIT | — | 2026-08-07 | Tester le cas « se désabonner d'une seule formule » |
| B030 | Widget Telegram embarqué sur le site | ABANDONNÉ | P2 | 2026-08-08 | — |
| B031 | Groupe de discussion Telegram lié au canal | FAIT | — | 2026-08-04 | Modération humaine occasionnelle quand il y aura du trafic |
| B032 | Teaser du registre du lendemain | FAIT | — | 2026-08-04 | — |
| B033 | Brief audio quotidien (TTS) | À FAIRE | P3 | 2026-08-10 | — |
| B034 | Image en tête de la newsletter Buttondown | EN TEST | P3 | 2026-08-11 | Vérifier passivement sur un item réellement neuf |
| B035 | Image sur les posts du circuit RSS SUIVI | FAIT | — | 2026-08-12 | — |
| B036 | Fenêtre de dates des modules RSS de Make | FAIT | — | 2026-08-15 | — |
| B037 | Branche « RSS PUB » dans le scénario Make Daily | FAIT | — | 2026-08-15 | — |
| B038 | Bug du bouton notifications (faux positif OneSignal) | FAIT | — | 2026-08-21 | Trancher le sort des 3 archives publiées avec le bug |
| B039 | Temps de lecture estimé | EN COURS | — | 2026-08-04 | Synchroniser le prompt live pour le volet email (B108) |
| B040 | Sommaire ancré en haut de chaque édition | FAIT | — | 2026-08-08 | Fusionner les sections Lexique et Sources |
| B041 | Bloc de synthèse « L'essentiel » | FAIT | — | 2026-08-12 | — |
| B042 | Page glossaire (`glossaire.html`) | FAIT | — | 2026-08-05 | — |
| B043 | Recherche en texte intégral sur `archives.html` | À FAIRE | P3 | 2026-08 | — |
| B044 | Navigation « édition suivante » | À DÉCIDER | P3 | 2026-08 | Trancher : « précédente » seule ou exception aux archives figées |
| B045 | Graphiques de séries chiffrées dans le contexte | À FAIRE | P2 | 2026-08-10 | Livrer une v1 bornée aux indices cotés |
| B046 | Cohérence des KPI `indicator-strip` / cartes | FAIT | — | 2026-08-08 | — |
| B047 | Lisibilité des 3 cartes de scénarios | FAIT | — | 2026-09-02 | — |
| B048 | Retrait de la ligne `.ai-disclosure` du footer | FAIT | — | 2026-08-08 | — |
| B049 | Bande `.top-updates` (dernier suivi, dernier hebdo) | FAIT | — | 2026-08-11 | — |
| B050 | Vignettes Instagram sur le récap hebdo | FAIT | — | 2026-08-11 | — |
| B051 | « Signaux à surveiller » par scénario | À FAIRE | P2 | 2026-08-10 | Chiffrer emplacement, longueur, non-duplication |
| B052 | Faire comprendre Scénario à un premier visiteur | FAIT | P2 | 2026-08-28 | — |
| B053 | Prompt de la routine quotidienne allégé de 42 % | FAIT | — | 2026-08-11 | — |
| B054 | Mettre en avant les sujets suivis sur `archives.html` | À FAIRE | P2 | 2026-08-29 | Comparer plusieurs variantes visuelles |
| B055 | Mémoriser la langue de lecture (FR/EN) | À FAIRE | P3 | 2026-08-30 | — |
| B056 | Basculer vers un CMS / générateur de site statique | À DÉCIDER | — | 2026-08-31 | Clarifier qui édite le contenu avant d'évaluer les outils |
| B057 | Copie intégrale du `<style>` (`.list-box`/`.dek-list`) | FAIT | — | 2026-08-14 | — |
| B058 | Optimisation d'`archives.html` (fragments à la demande) | FAIT | — | 2026-08-04 | — |
| B059 | Lien Instagram au footer | FAIT | — | 2026-08-07 | — |
| B060 | Site figé par un bug de build Jekyll (`.nojekyll`) | FAIT | — | 2026-08-11 | — |
| B061 | Découpage d'`archives.html` par année | À FAIRE | P2 | 2026-08-04 | Trancher URL/sélecteur/impact routine (avant fin 2026) |
| B062 | Données ouvertes / API publique (`feed.json`) | À FAIRE | P3 | 2026-08-27 | Trancher la garantie de stabilité du schéma |
| B063 | Byline auteur nommé + JSON-LD `Person` | STANDBY | P3 | 2026-08-31 | Ne pas relancer sans feu vert explicite |
| B064 | Graphique en escalier (série historique longue) | FAIT | — | 2026-08-21 | — |
| B065 | Guide pédagogique (`guide-pedagogique.html`) | FAIT | — | 2026-08-20 | — |
| B066 | Partenariats éducatifs formels | À FAIRE | P2 | 2026-08-20 | — |
| B067 | Netlinking / « SEO passif » | EN COURS | P2 | 2026-09-03 | Envoyer les messages du Tier 1 (geste humain) |
| B068 | Audit SEO : passe du 21 août + process récurrent | EN COURS | P2 | 2026-08-21 | Définir un process d'audit récurrent |
| B069 | Newsletter enrichie (Q&A, aperçus) | À FAIRE | P3 | 2026-08-20 | — |
| B070 | Restructuration des registres du week-end | FAIT | — | 2026-08-12 | Confirmer la resynchronisation du prompt live (B108) |
| B071 | Permutation Sport ↔ Économie (jeudi/dimanche) | FAIT | — | 2026-08-12 | — |
| B072 | Pondération France Impact par registre | À DÉCIDER | — | 2026-08-12 | Reprendre la discussion sur le poids −1,5/+1 |
| B073 | Pondération France Impact par `kind` de scénario | STANDBY | P3 | 2026-09-02 | Relire l'avis critique avant toute implémentation |
| B074 | `le-projet.html` : rôle technique = la méthode | FAIT | — | 2026-08-07 | — |
| B075 | Images de partage par édition | ABANDONNÉ | — | 2026-08-04 | — |
| B076 | Image dans le corps de l'article | FAIT | P1 | 2026-08-10 | — |
| B077 | Routine « Inspecteur » de re-vérification matinale | EN COURS | — | 2026-08-13 | Avancer la routine principale à 6h Paris (geste utilisateur) |
| B078 | Routine « pub » hebdomadaire | EN COURS | — | 2026-08-21 | Trancher `citation-13` (B085) |
| B079 | Gabarits d'image des posts pub (V4 hybride, V5 stat) | FAIT | — | 2026-08-21 | — |
| B080 | Source et crédit de la photo des posts pub | FAIT | — | 2026-08-13 | — |
| B081 | Catégorie pub « Questions à la communauté » | STANDBY | — | 2026-08-14 | — |
| B082 | Catégorie pub « Le saviez-vous » (chiffre) | FAIT | — | 2026-08-21 | — |
| B083 | Catégorie pub « Grands futurs » (futur) | STANDBY | — | 2026-08-21 | — |
| B084 | Banque de secours de photos pour les posts pub | FAIT | — | 2026-08-13 | — |
| B085 | `citation-13` (Einstein) à vérifier | À DÉCIDER | — | 2026-08-13 | Vérifier l'attribution puis réintégrer ou non |
| B086 | Table jour → catégorie de la routine pub | FAIT | — | 2026-08-21 | — |
| B087 | Planning horaire des routines automatiques | FAIT | — | 2026-08-14 | — |
| B088 | Heatmap « Le monde en ce moment » par domaine | À FAIRE | P2 | 2026-08-12 | Trancher job mensuel vs page 100 % JS |
| B089 | France Impact (ex « Δ France ») | FAIT | — | 2026-08-17 | — |
| B090 | Carte de pari partageable, sans backend | À FAIRE | P3 | 2026-08-10 | Chiffrer design + calcul de la date de clôture |
| B091 | Confronter à un marché de prédiction | À FAIRE | P3 | 2026-08-10 | — |
| B092 | Page de calibration (« avions-nous raison ») | BLOQUÉ | P3 | 2026-08-27 | Revisiter quand des suivis seront clôturés |
| B093 | Arabie saoudite / sport — dossier ouvert | FAIT (à confirmer) | — | 2026-08-15 | Confirmer l'état réel du suivi |
| B094 | Idées explicitement écartées (registre) | ABANDONNÉ | — | 2026-08-09 | — |
| B095 | Emails de la newsletter qui arrivaient en spam | FAIT | — | 2026-07-31 | — |
| B096 | Pipeline Make LinkedIn (RSS → LinkedIn) | FAIT | — | 2026-07-31 | Garder le scénario Make activé |
| B097 | Identité visuelle de la Page LinkedIn | FAIT | — | 2026-07-31 | — |
| B098 | Sondage Telegram sur le sujet du lendemain | À FAIRE | — | 2026-07-31 | — |
| B099 | Canal Telegram : création, egress, bascule Make | FAIT | — | 2026-08-01 | — |
| B100 | Soumission du canal Telegram aux annuaires | EN COURS | — | 2026-07-31 | Envoyer l'email ActuZones |
| B101 | Équilibre encart Telegram / formulaire email | À DÉCIDER | — | 2026-07-31 | Trancher le rééquilibrage de `newsletter.html` |
| B102 | Nom de domaine dédié | FAIT | — | 2026-07 | — |
| B103 | SEO de base (`robots.txt`, sitemap, Search Console) | FAIT | — | 2026-07-30 | — |
| B104 | `NewsArticle` JSON-LD + Google Actualités | EN TEST | — | 2026-08-21 | Check Search Console « Actualités » le 2026-09-15 |
| B105 | Mentions légales + politique de confidentialité | FAIT | — | 2026-08 | — |
| B106 | Newsletter par email (Buttondown, RSS-to-email) | FAIT | — | 2026-08-11 | — |
| B107 | Newsletter hebdo + routine hebdo | FAIT | — | 2026-08-09 | — |
| B108 | Synchronisation manuelle du prompt de la routine quotidienne | BLOQUÉ | — | 2026-08-11 | Copier-coller manuel par l'utilisateur à chaque correction |
| B109 | Page dédiée par récap hebdo + découverte | FAIT | — | 2026-08-06 | — |
| B110 | Relais social du hebdo (Make « Weekly ») | FAIT | — | 2026-08-07 | — |
| B111 | Photo dans les éditions (première discussion) | ABANDONNÉ | — | 2026-08-01 | — |
| B112 | Pages de suivi par sujet (`suivi/{sujet}.html`) | FAIT | — | 2026-08-08 | — |
| B113 | Date affichée sur `.entry-date` d'une entrée révisée | FAIT (à confirmer) | — | 2026-08-22 | Vérifier la couverture sur les entrées révisées |
| B114 | Image d'illustration des pages de suivi | FAIT | — | 2026-08-12 | — |
| B115 | Règles de rédaction d'une mise à jour de suivi | FAIT | — | 2026-08-15 | — |
| B116 | Clôture d'un sujet suivi (« VF — Résolu ») | FAIT | — | 2026-08-27 | — |
| B117 | Préciser le déclencheur idéal de clôture | À FAIRE | P1 | 2026-08-08 | Retravailler la règle avant de l'ajouter au prompt détection |
| B118 | Annonce des mises à jour de suivi (`feed-suivi.xml`) | FAIT | — | 2026-08-08 | — |
| B119 | Image composée des posts de mise à jour de suivi | FAIT | — | 2026-08-14 | — |
| B120 | Graphique d'évolution des pages de suivi | FAIT | — | 2026-08-01 | — |
| B121 | Anciennes versions de suivi repliées (accordéon) | FAIT | — | 2026-08-01 | — |
| B122 | Journal quotidien auto-alimenté des sujets publiés | FAIT | — | 2026-08-01 | — |
| B123 | Routine de détection des sujets à mettre à jour | FAIT | — | 2026-08-14 | Confirmer le silence des emails les jours « RAS » |
| B124 | Vitrine des suivis clôturés / track record | BLOQUÉ | — | 2026-08-27 | Attendre de vrais cas clôturés |
| B125 | Transparence IA (article 50 du règlement IA) | FAIT | — | 2026-08-04 | — |
| B126 | Audit externe du 27 août : cadrage et mapping | FAIT | — | 2026-08-27 | — |
| B127 | Réécriture éditoriale des versions de suivi publiées | À FAIRE | — | 2026-08-27 | Reprendre le texte des 7 pages `suivi/*.html` |
| B128 | Identité du fondateur (photo, 1ʳᵉ personne) | À FAIRE | — | 2026-08-27 | — |
| B129 | Clarifier « probabilité à l'instant T » | FAIT | P0 | 2026-08-27 | — |
| B130 | Ajouter « Pourquoi cette probabilité ? » | FAIT | P0 | 2026-08-27 | — |
| B131 | Distinguer Faits / Analyse / Scénarios | FAIT | P0 | 2026-08-28 | — |
| B132 | Étendre le balisage à la newsletter | FAIT | — | 2026-08-28 | — |
| B133 | Renforcer « Notre méthode » | FAIT | P0 | 2026-08-27 | — |
| B134 | Rattrapage historique des tickets éditoriaux | ABANDONNÉ | — | 2026-08-27 | — |
| B135 | CTA newsletter (wording) | FAIT | — | 2026-08-27 | — |
| B136 | Pages thématiques `themes/*.html` + maillage interne | FAIT | P1 | 2026-08-31 | — |
| B137 | Menu déroulant « Archives ▾ » dans le nav | FAIT | — | 2026-08-31 | — |
| B138 | Rôle et avenir d'`archives.html` | À DÉCIDER | — | 2026-08-31 | Partir de la liste des fonctions à préserver |
| B139 | Pages thématiques en anglais (`en/themes/`) | À DÉCIDER | — | 2026-08-31 | Revisiter le 2026-09-15, avec B008 |
| B140 | Titres SEO + développement du glossaire | À FAIRE | P1 | 2026-08-31 | Traiter le volet « titres SEO » |
| B141 | Vote sur site, puis « mardi participatif » | STANDBY | P2 | 2026-08-27 | Ne pas relancer ; trancher d'abord le % en direct |
| B142 | Score historique de Scénario | BLOQUÉ | P3 | 2026-09-02 | Définir l'export scénario ↔ résultat (commun B092/B062) |
| B143 | Créer « Nos erreurs / enseignements » | À FAIRE | P1/P2 | 2026-08-27 | Cadrer le contenu |
| B144 | Boucle réseaux → site → newsletter | À FAIRE | P2 | 2026-08-27 | Ajouter l'appel newsletter au gabarit de légende |
| B145 | Titres de scénarios littéraux | FAIT | — | 2026-08-28 | — |
| B146 | Français naturel partout | FAIT | — | 2026-08-28 | — |
| B147 | « Ce qu'on évalue » en 3 branches étiquetées | FAIT | — | 2026-09-02 | — |
| B148 | Dashboard de pilotage interne (`dashboard.html`) | FAIT | P2 | 2026-09-03 | — |
| B149 | KPI niveaux 2-3 du dashboard | À FAIRE | P2 | 2026-09-03 | Commencer par 1-2 réseaux (Bluesky, Telegram) |
| B150 | Lectures par édition sur `archives.html` (`reads.json`) | FAIT | — | 2026-09-03 | — |
| B151 | Migrer le dashboard et `#audience` vers un GitHub Action | À DÉCIDER | — | 2026-09-03 | Valider le plan de migration avec l'utilisateur |
| B152 | Répartition des modèles OpenRouter par tâche (Opus / Sonnet / DeepSeek) | FAIT | — | 2026-09-18 | Surveiller coût et qualité après la bascule |

## TICKETS

## B001 — Recadrage photo des images sociales (pub / suivi)

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-09-17
**Prochaine action:** Tester un ancrage vertical plus haut (`background-position: center 25%` ou `center top`) sur plusieurs photos réelles avant de généraliser
**Blocage:** Aucun

### État actuel
Les 3 gabarits qui posent une photo en fond — `scripts/social/pub-template-v4-hybride.html`, `pub-template-v5-stat.html`, `suivi-template.html` — utilisent tous `background-position:center` sur `.photo-bg`. Le recadrage se fait donc sur le centre géométrique de la photo et pas sur son sujet, souvent trop haut dans le cadre source, donc coupé ou poussé hors champ.

### À faire
- Remonter le point d'ancrage vertical (piste : `background-position: center 25%` ou `center top`).
- Valider visuellement sur plusieurs photos réelles avant de généraliser : un ancrage fixe pourrait mal tomber sur une photo au cadrage différent.

### Décisions
- Ne pas généraliser un ancrage fixe sans validation visuelle multi-photos.

### Historique
- **2026-09-17** — Demande utilisateur : « le crop [...] ce qui doit être vu est encore trop bas ». Diagnostic posé (les 3 gabarits sur `background-position:center`), piste d'ancrage vertical notée, rien d'implémenté.

---

## B002 — Chaîne rédaction + post-édition OpenRouter (prototype)

**Statut:** EN TEST
**Priorité:** P1
**Dernière MAJ:** 2026-09-14
**Prochaine action:** Tester la chaîne en conditions réelles sur GitHub Actions (testée seulement en local de bout en bout)
**Blocage:** Aucun — mais publication réelle (commit/push) volontairement hors périmètre tant que la qualité rédactionnelle n'est pas éprouvée sur plusieurs jours réels

### État actuel
Prototype en deux workflows : `.github/workflows/edition.yml` (rédaction) et `.github/workflows/post-edition.yml` (post-édition), créés le 14 septembre 2026. Toujours **Phase 1** : `workflow_dispatch` uniquement, AUCUN commit/push, tout sous `_prototype-out/`, jamais les vrais fichiers du dépôt (vérifié : `git status` inchangé après plusieurs runs locaux complets, avec et sans photo). Testé en local de bout en bout (rédaction dry-run → post-édition, avec et sans photo, repli Pexels sans clé API vérifié), **pas encore testé en conditions réelles sur GitHub Actions**.

### À faire
- Lancer un run réel sur GitHub Actions.
- Corriger la simplification Instagram si le rendu déçoit à l'usage : aujourd'hui `context`/labels réutilisent `section_title`/titres de cartes déjà rédigés, jamais une reformulation dédiée à l'image, alors que `docs/routine-prompt.md` demande explicitement l'inverse.
- Hors périmètre, explicitement : `feed-suivi.xml`/`feed-pub.xml` (pas mis à jour par ce prototype), traduction EN/`en/feed.xml` (gérée séparément par `translate-en.yml`), décision de publication réelle (commit + push sur `main`).

### Décisions
- **Photo de sujet (Pexels) : sélection automatique du 1er candidat** — décision assumée, changement de comportement volontaire par rapport à `fetch_topic_image.py`/`use_topic_image.py`, qui documentent une sélection humaine par défaut (voir `docs/routine-brief-format.md` § `image_keywords`, nouveau champ du brief). Repli automatique sur l'image générique si Pexels échoue ou si `image_keywords` est absent — jamais bloquant.
- `feed.xml` (nouvel `<item>`, structure Question/Faits/Scénarios), `sitemap.xml`/`sitemap-news.xml` (purge >48h) : mis à jour par du texte/XML **déterministe**, jamais par le modèle.
- `archives.html` régénéré via `scripts/seo/generate_archives_table.py`, réutilisé sans modification — en contournant son calcul de racine basé sur `__file__` : le script et les fichiers qu'il lit sont copiés sous un bac à sable, jamais le vrai dépôt.

### Historique
- **2026-09-14 (Phase 1, rédaction)** — `scripts/edition/generate_daily_edition.py` + `scripts/edition/build_html.py` produisent un `index.html` de test complet (chrome recopié du gabarit + contenu du modèle) à partir d'un brief (`editorial-briefs/{date}.json`), avec validations strictes et retry automatique. Validé deux fois en conditions réelles (brief fictif puis brief réel, sujet Taïwan/Chine/États-Unis du 14 septembre) — **deux bugs réels trouvés et corrigés** : guillemets JSON non échappés dans `.lex-ref`, encart `.comprendre-box` perdu à l'assemblage HTML.
- **2026-09-14 [FAIT]** — Second workflow dédié à la post-édition (`.github/workflows/post-edition.yml`, `scripts/edition/generate_post_edition.py`) : photo de sujet Pexels (sélection auto du 1er candidat), image Instagram via `scripts/social/generate_instagram_image.py` réutilisé tel quel, `feed.xml`, `sitemap.xml`/`sitemap-news.xml`, `archives.html`.

---

## B003 — Threads comme canal de diffusion (via Buffer)

**Statut:** FAIT
**Priorité:** P1 (à l'origine, avec Bluesky/Mastodon)
**Dernière MAJ:** 2026-09-05
**Prochaine action:** Aucune côté français. Pas de stratégie Threads anglaise (voir `docs/strategie-anglais.md`)
**Blocage:** Aucun

### État actuel
Threads est branché sur les **3 branches françaises** du scénario Make « Scenario Daily » : PUB (module `buffer:ActionCreateStatus` id `255`), Daily (id `256`), Suivi (id `257`), tous via le profil Buffer « Threads (scenarios.actu) », `type: "now"` (post immédiat, contrairement aux modules Twitter équivalents qui postent en différé). Les **branches anglaises (EN MAIN/SUIVI/PUB) sont volontairement non modifiées**. Export final vérifié : 64 modules, aucun doublon d'id, les 3 modules Threads cohérents entre eux, les 3 branches anglaises intactes.

### À faire
- Rien pour le périmètre français. Une éventuelle diffusion Threads anglaise dépend de la stratégie anglaise (voir `docs/strategie-anglais.md`).

### Décisions
- Passer par **Buffer** plutôt que par un module natif ou l'API Threads en HTTP/OAuth manuel.
- Ne pas toucher aux 3 branches anglaises : demande explicite de l'utilisateur.

### Historique
- **2026-08-15** — Threads noté comme piste P1 (avec Bluesky et Mastodon, voir B014/B015). Même connexion Meta déjà branchée pour Instagram/Facebook natifs (`Olivier's Facebook connection`) — coût marginal quasi nul **si un module natif existe**, mais non confirmé côté Make ce jour-là (recherches web inconclusives, aucun module trouvé dans le catalogue). Consigne posée : ne pas conclure trop vite à l'absence, vu que Bluesky s'est finalement révélé disponible nativement malgré une recherche tout aussi inconcluante — vérifier directement dans la barre de recherche des apps Make. Replis possibles envisagés : Buffer (à vérifier s'il supporte Threads) ou l'API Threads de Meta en HTTP/OAuth manuel, « moins recommandé » vu l'expérience déjà vécue avec X (tentative OAuth manuelle abandonnée après échecs répétés, voir B020). **Remis à plus tard, retour utilisateur du 15 août.**
- **2026-09-05 [FAIT]** — L'utilisateur avait déjà construit et validé le module Threads pour la branche PUB (`buffer:ActionCreateStatus`, id `255`). Retour utilisateur : « j'ai avancé pour intégrer thread (via buffer) peux-tu compléter sur tout les autres RSS type sauf anglais ». Complété par analyse directe du blueprint `assets/make/scenario-daily.blueprint.json` :
  - **Branche Daily (id `256`)** : un module Threads existait déjà à l'état d'ébauche cassée (texte mappé sur l'URL de l'image au lieu du vrai contenu du post) — corrigé pour reprendre exactement le texte/média du module Twitter Daily (id `14`), seuls `type` et `profileIds` changent.
  - **Branche Suivi** : aucun module Threads n'existait — nouvelle route ajoutée dans le sous-routeur Suivi, copiant le texte/média du module Twitter Suivi (id `24`, « 🔄 Un sujet suivi vient d'être mis à jour... »).
- **2026-09-05, dans la foulée — orphelins retirés** (retour utilisateur : « tu enlèves les orphelins ») : route 12 du routeur principal (ne contenait qu'un `placeholder:Placeholder`, id `253`, aucun rôle fonctionnel) supprimée ; les 2 modules que Make trackait lui-même comme orphelins dans `metadata.designer.orphans` — id `248` (`builtin:Ignore`, en erreur « Directive is outside of an error handler », non connecté au flux) et id `252` (`placeholder:Placeholder`, non connecté) — retirés après vérification qu'aucun autre module ne les référençait (`{{248.*}}`/`{{252.*}}`/`{{253.*}}` absents du reste du blueprint), avant d'écraser `assets/make/scenario-daily.blueprint.json`.

---

## B004 — Migrer la newsletter email de Buttondown vers OneSignal

**Statut:** STANDBY
**Priorité:** P3 (passée de P2 à P3 le 29 août 2026)
**Dernière MAJ:** 2026-08-29
**Prochaine action:** Ne rien entamer avant le rappel programmé du 1er avril 2027 (`trig_01Ntw6KBaiZsCFh4th7iPosP`), sauf retour utilisateur explicite ; reprendre le ticket en avril-mai 2027 au plus tard
**Blocage:** **Forfait Buttondown déjà payé jusqu'au 29 juillet 2027** — pas d'intérêt à migrer avant cette échéance

### État actuel
Ticket cadré et prêt à reprendre, gelé volontairement. Retour utilisateur du 29 août : « pour l'instant standby ». Gelé pour le motif du forfait déjà payé, pas par manque d'intérêt. Deux points déjà vérifiés côté utilisateur, trois restent à vérifier avant de lancer. Un rappel programmé existe (`trig_01Ntw6KBaiZsCFh4th7iPosP`, déclenchement unique le 1er avril 2027, nouvelle session dédiée) : il relit ce ticket et fait le point avec l'utilisateur avant tout travail technique — pas la peine de recréer un rappel manuellement d'ici là.

### À faire
- **Vérifier** : domaine expéditeur et délivrabilité réelle des e-mails OneSignal (pas seulement le volume/prix) — non couvert par les deux points déjà vérifiés.
- **Contenu de l'email** : reprend la structure Question/Faits/Scénarios déjà en place dans la `<description>` de `feed.xml` depuis le 28 août (voir B132), pas à reconstruire.
- **Bascule des pages d'inscription** : `newsletter.html`, `confirmez-votre-email.html`, `bienvenue.html` (aujourd'hui branchés sur le flux d'inscription Buttondown) vers le flux d'inscription e-mail OneSignal.
- **Décommissionner Buttondown seulement après** confirmation que la bascule fonctionne — double-run temporaire recommandé plutôt qu'une coupure nette.
- Séquence à prévoir sans urgence : export CSV Buttondown → import OneSignal → bascule des pages d'inscription → double-run de vérification → coupure Buttondown.

### Décisions
- **Option de déclenchement retenue : la 2** — le scénario Make.com existant (qui surveille déjà `feed.xml` pour Telegram/Instagram/Facebook/LinkedIn/Bluesky/X et déclenche déjà le **push** OneSignal, branche « Daily », voir `docs/routine-prompt.md` étape technique 11) reçoit un module e-mail OneSignal sur ce même déclencheur. Motif : centraliser tous les flux vers les lecteurs dans Make plutôt que d'éparpiller les intégrations — cohérent avec le choix déjà fait pour le push le 23 août.
- **Échéance à retenir** : reprendre en avril-mai 2027 au plus tard, pour ne pas tout faire dans l'urgence des derniers jours du forfait.
- **Ne pas relancer de son propre chef** avant le 1er avril 2027.

### Historique
- **2026-08-29 (idée)** — Constat utilisateur : Buttondown est payant (voir B106), OneSignal permet aussi l'envoi d'e-mails et c'est gratuit — pas besoin de payer deux outils pour deux canaux (push + email) qui peuvent tenir sur un seul. Deux options de déclenchement envisagées : (1) la routine ou un script appelle directement l'API e-mail OneSignal quand `feed.xml` est mis à jour ; (2) le scénario Make existant ajoute un module e-mail OneSignal. **Option 2 retenue.**
- **2026-08-29 (deux points vérifiés côté utilisateur)** :
  - **Plan gratuit OneSignal confirmé** : gratuit en dessous de 10 000 contacts. Base d'abonnés actuelle très réduite (« 3 pelés » — retour utilisateur), largement sous le seuil.
  - **Migration des abonnés confirmée possible** : OneSignal accepte l'import de la liste de destinataires par CSV — export Buttondown → import OneSignal, pas de réinscription à demander.
- **2026-08-29 (blocage + dépriorisation)** — Forfait Buttondown déjà payé jusqu'au 29 juillet 2027 : ticket passé de P2 à P3 et gelé. Rappel programmé posé le même jour.
- *Note de traçabilité* : le renvoi d'origine « voir plus bas, "Retiré le 23 août" » ne correspond à aucune section de ce backlog — la trace du choix du 23 août sur le push vit probablement dans `docs/ARCHITECTURE.md`.

---

## B005 — Version anglaise du site (MVP `en/`)

**Statut:** FAIT (MVP lancé le 29 août 2026, enrichi jusqu'au 3 septembre)
**Priorité:** P3 à l'origine
**Dernière MAJ:** 2026-09-03
**Prochaine action:** Rien d'obligatoire ; la traduction quotidienne tourne. Questions ouvertes traitées séparément : B006 (hebdo EN), B007 (pages statiques/légales EN), B008 (archives rétroactives), B139 (pages thématiques EN), B055 (mémoriser la langue)
**Blocage:** Aucun

### État actuel
Le site a une version anglaise en production sous `en/` : `en/index.html` (édition du jour), `en/archives/AAAA-MM-JJ.html`, `en/feed.xml`, `en/feed-pub.xml`, `en/feed-suivi.xml`, `en/manifest.webmanifest`. La traduction est **FR→EN de l'édition quotidienne uniquement**, faite après coup à la suite de la routine française (procédure : `docs/routine-en-prompt.md` ; décisions et scope : `docs/strategie-anglais.md`). Bouton de bascule `.masthead-lang-btn` + balises `hreflang` (`x-default` toujours vers le français) sur les pages traduites ; badge `.entry-lang-badge` sur `archives.html` pour les entrées déjà traduites. Le français reste la langue prioritaire et par défaut. Pas de comptes réseaux sociaux anglophones ni de diffusion Make.com dédiée. Au 30 août, seules 2 éditions avaient une version anglaise (29 et 30 août) ; au 31 août, 5 articles étaient traduits sous `en/archives/`.

### À faire
- Rien de bloquant. Suites éventuelles : traduction des pages statiques (B007), traduction rétroactive des archives (B008), récap hebdo (B006), pages thématiques EN (B139), comptes/diffusion sociale anglophones (à revoir une fois l'audience mesurée).
- Incohérence connue non corrigée, hors scope : le libellé `.comprendre-label` est tantôt « Context », tantôt « Comprendre » non traduit, d'un article EN à l'autre.

### Décisions
- **Portée** : traduction FR→EN de l'édition quotidienne uniquement — jamais de rédaction indépendante en anglais, jamais de nouvelle recherche ni de nouveaux chiffres.
- **Structure d'URL** : chemin, pas sous-domaine — `lesscenarios.fr/en/` et `lesscenarios.fr/en/archives/AAAA-MM-JJ.html`, même relation à deux niveaux que la version française. Toute l'adresse d'une page anglaise est son équivalent français avec `en/` ajouté après le domaine.
- **Mécanisme** : traduction manuelle/assistée après coup, à la suite de la routine française quotidienne, jamais en parallèle ni avant — traduction section par section, y compris les chaînes générées par JS, jamais de reformulation du fond déjà validé côté français.
- **Glossaire en anglais explicitement écarté** — retour utilisateur direct : « on ne fait pas le glossaire en anglais ».
- **`archives.html` reste entièrement en français** (page, filtres, accordéon « Scénarios ▾ ») : pas de bascule de langue sur cette page. Seul ajout, un badge `.entry-lang-badge` (pilule dorée, même famille visuelle que `.masthead-lang-btn`) à côté du titre de chaque entrée déjà traduite, lien direct vers `en/archives/{date}.html`. Classe CSS volontairement distincte de `.tag` (pas `data-tag`) pour ne pas perturber le JS de filtrage qui indexe `.tag` — vérifié : aucun tag fantôme « undefined », filtre intact. **L'accordéon reste toujours en français**, même sur une entrée traduite : dupliquer le fragment de scénarios en anglais aurait demandé un vrai second système de fragments pour un gain marginal, le badge EN emmène déjà vers l'article complet.
- **Traduction en cascade des articles cités** : un lien de l'édition du jour vers une édition passée pointe vers `en/archives/...`, traduite à la volée si besoin — **un seul niveau de cascade**.
- **Pas de détection de langue navigateur, pas de redirection automatique** (`docs/strategie-anglais.md` § « UX de bascule entre langues ») : le bouton offre un accès direct, jamais un choix imposé.
- **Procédure pour chaque nouvel article traduit** : ajouter le badge sur `archives.html` en même temps que le reste de l'étape 1bis (`docs/routine-en-prompt.md`).

### Historique
- **2026-08-07 (P3, première discussion)** — Idée ouverte : garder la version française telle quelle et ajouter une version anglaise en parallèle, avec sa propre routine dédiée (traduction et/ou rédaction directe en anglais, à trancher). Rien de tranché : ni l'architecture (sous-dossier `en/` ? sous-domaine ? champ de langue par édition ?), ni si la routine anglaise republie les mêmes sujets, ni le rythme.
- **2026-08-07 (variante légère envisagée)** — Pas de site anglais complet, juste une distribution anglophone : traduction du titre + du commentaire de chaque édition, publiée dans un `en/feed.xml` séparé, branché côté Make sur une route Buffer dédiée postant **uniquement sur X** (audience X jugée nettement plus anglophone). Aucune nouvelle page HTML anglaise.
- **2026-08-07** — Les deux options explicitement mises de côté par l'utilisateur pour être rediscutées plus tard : **ne rien commencer sans un go explicite**, y compris la variante légère.
- **2026-08-08 (troisième variante, comparée)** — Traduire l'édition complète chaque jour + un sélecteur de langue (drapeau FR/EN), sans routine séparée ni nouvelle sélection de sujets. Coût jugé **plus élevé que la variante légère** malgré une apparente simplicité : traduire toute une édition (contexte + 3 cartes + indicateurs + lexique + sources) avec la même rigueur terminologique revient quasiment à doubler la rédaction quotidienne, et double la surface à maintenir à chaque ajustement du gabarit (JSON-LD, sommaire, « L'essentiel », balises `feed.xml`...). Recommandation d'alors : si une distribution anglophone est lancée, commencer par la variante légère pour tester l'intérêt réel.
- **2026-08-08 (compromis recommandé alors, finalement non retenu)** — Traduire uniquement le bloc « L'essentiel » (3-4 phrases déjà rédigées chaque jour) plutôt que toute l'édition : coût marginal, architecture inchangée (un sous-dossier `en/` avec une page listant les « L'essentiel » du jour et des précédents, chacun lié vers l'édition française complète, « Read the full analysis (in French) »), pas de gabarit à dupliquer, pas de JSON-LD/sommaire à traduire ; vrai point d'entrée anglophone (SEO, partage X) sans prétendre à un site bilingue ; le lecteur qui veut aller plus loin retombe sur le français, où la traduction passive du navigateur prend le relais. Aurait remplacé la variante légère du 7 août.
- **2026-08-07/08 (points à réfléchir posés sur demande explicite de l'utilisateur, « tout doit être pensé d'abord »)** :
  - **Précision et cohérence de la traduction** : les termes récurrents (favorable/stable/dégradé, « scénario », formulations types du caveat probabilités) doivent être traduits de façon strictement identique à chaque édition — envisager un **glossaire de référence** (ex. `docs/glossaire-en.md`) consulté systématiquement.
  - **Archives** : décider si la traduction s'applique aux éditions futures seulement ou aussi rétroactivement (voir B008).
  - **Pages légales en anglais** : `politique-de-confidentialite.html` et les mentions légales doivent avoir un équivalent aussi rigoureux — pas une traduction automatique vu la sensibilité RGPD/juridique (voir B007).
  - Même un simple post traduit (variante légère) doit rester juridiquement/factuellement aussi rigoureux que l'édition française.
- **2026-08-29 [SUPERSÉDÉ]** — La discussion du 7-8 août est explicitement supersédée : l'option retenue est un chemin (`en/`/`en/archives/`), traduction de l'édition du jour uniquement, pas le « compromis L'essentiel seul ».
- **2026-08-29 [FAIT — MVP lancé]** — Retour utilisateur : « il faudrait élargir et proposer une version anglaise, à voir comment on peut faire proprement et simplement », puis directive concrète le même jour : « tu fais ta routine classique et tu fais la traduction fr vers en, on stocke cette version dans archive-en avec un en/feed.xml ». Première édition traduite : « Global Cinema: Can It Survive Streaming? » (2026-08-29) — `en/index.html` + `en/archives/2026-08-29.html` + item `en/feed.xml`. Sert de validation du pipeline avant généralisation. Diffusion : `en/feed.xml` (`<language>en</language>`), `sitemap.xml` mis à jour.
- **2026-08-29 (même jour) [FAIT] — extension aux routines auxiliaires** : `en/feed-pub.xml` (miroir anglais de `feed-pub.xml`, image régénérée avec la même photo mais un gabarit anglais dédié `pub-template-v{N}-*-en.html`) et `en/feed-suivi.xml` (même logique, `suivi-template-en.html`) — voir `docs/routine-en-prompt.md` §§ « Traduction des posts pub » / « Traduction des mises à jour de suivi ». Glossaire anglais écarté à cette occasion.
- **2026-08-29 (même jour) [FAIT] — réarborescence sous `en/`** : retour utilisateur (« archive-en à la racine, j'aurais mis plutôt dans le folder en ») — `archive-en/` → `en/archives/`, `feed-en.xml` → `en/feed.xml`, `feed-pub-en.xml` → `en/feed-pub.xml`, `feed-suivi-en.xml` → `en/feed-suivi.xml`, `assets/social/pub-en/` → `en/assets/social/pub/`, `assets/social/suivi-en/` → `en/assets/social/suivi/`.
- **2026-08-29 (même jour) [FAIT] — bouton de bascule FR/EN + `hreflang`** : retour utilisateur (« il manque des trucs sur l'ux pour bien gérer français et anglais, français reste le prioritaire et défaut ») — `.masthead-lang-btn` (EN sur les pages françaises, FR sur les pages anglaises) ajouté sur les 4 fichiers de l'édition traduite du jour + balises `hreflang`. Détail : `docs/routine-en-prompt.md` § « Étape 4bis ».
- **2026-08-29 (même jour) [FAIT] — traduction en cascade des articles cités** : retour utilisateur (« les liens qui font référence à nos précédents articles doivent aussi pointer sur la version anglaise si elle existe »). Deux éditions traduites pour valider : `archives/2026-08-08.html` et `archives/2026-08-22.html`, toutes deux citées par l'édition du 29 août, plus les deux fichiers FR correspondants retrofités avec le bouton de langue. Procédure : `docs/routine-en-prompt.md` § « Étape 1bis ».
- **2026-08-29 (même jour) [FAIT] — popup d'installation PWA + manifest bilingues** : retour utilisateur « le popup en français, possible de mettre en anglais aussi ? ». `assets/pwa-install.js` détecte la langue de la page (`document.documentElement.lang`) et affiche le bon texte, sans fichier dupliqué. `en/manifest.webmanifest` créé (nom/description en anglais). Détail : `docs/strategie-anglais.md` § « Bandeau d'installation PWA + manifest ».
- **2026-08-29 (même jour) [FAIT] — badge EN sur `archives.html`** (fusionne les deux tickets d'alors : point d'entrée EN + badge de découvrabilité). Retour utilisateur : « sur archive on garde archive [en français] mais on peut ajouter un lien EN pour les articles où c'est dispo ».
- **2026-09-03 [FAIT] — cascade appliquée à `archives/2026-08-20.html`** (« Taux : marche arrière »). Retour utilisateur : « tu oublies toujours de mettre à jour la version anglaise » — déclenché par le lien ajouté ce jour-là depuis l'édition du 3 septembre. Traduction complète de `en/archives/2026-08-20.html` : tête de page (title, canonical, hreflang fr/en/x-default, og/twitter, JSON-LD), masthead, intro-banner, hero (accroche, dek, les deux `.comprendre-box`, indicator-strip), les 3 cartes de scénario, essentiel-box, lexique, sources (titres d'articles gardés tels quels, déjà en anglais dans la source), blocs de partage/notifications, footer, et tous les `<script>` porteurs de texte visible (regex de date `Edition of...`, temps de lecture, compteur GoatCounter, dictionnaire des registres pour le teaser « Tomorrow: … », messages de partage/lien copié, tous les messages OneSignal). Vérifié via Playwright (`node --check` sur les scripts extraits, captures d'écran haut/bas de page, lecture du texte final de `.pubdate` et `#tomorrow-teaser` après exécution des scripts). Photo `assets/social/topic-images/2026-08-20.jpg` réutilisée telle quelle (simple photo, pas de texte français incrusté). Bouton de bascule FR→EN ajouté sur l'article français d'origine (CSS `.masthead-lang-btn` absente jusque-là, recopiée depuis un article déjà traduit) et `hreflang` ajoutés à son `<head>` (absents eux aussi). Lien `EN` ajouté sur la ligne du 20 août dans `archives.html` (classe `lang-link`). Entrée ajoutée dans `sitemap.xml`.
- **2026-09-03 (même jour) [FAIT] — répercuté sur `en/index.html` et `en/archives/2026-09-03.html`** : ces deux pages avaient été traduites par la routine quotidienne **avant** les ajouts du jour sur l'édition française, elles leur manquaient donc entièrement. Mêmes 4 ajouts sur les deux fichiers EN : icône cadenas « Private access » dans le masthead (avec le séparateur `.masthead-divider` qui la précède, oublié au premier passage puis corrigé) ; encadré `.comprendre-box` manquant sur le CAPE ratio (celui sur le financement circulaire était déjà traduit) ; phrase de renvoi vers l'article sur les banques centrales pointant vers `en/archives/2026-08-20.html` maintenant que sa traduction existe ; mention « black swan » dans le paragraphe `.why` du scénario dégradé + entrée `#lex-cygne-noir` dans le lexique de chaque page. Vérifié via Playwright : nombre de `.comprendre-box` identique entre FR et EN (2 par page), lien vers l'article du 20 août résolu, entrée lexique présente, captures du masthead et de l'encadré CAPE. Libellé `.comprendre-label` laissé en français (« Comprendre », pas « Understand ») pour rester cohérent avec l'encart déjà existant dans ces deux mêmes pages — incohérence de traduction déjà présente sur ce label d'un article EN à l'autre, pas corrigée ici, hors scope.

---

## B006 — Traduire le récap hebdomadaire en anglais (`hebdo/{AAAA-MM-JJ}.html`)

**Statut:** À DÉCIDER
**Priorité:** P2
**Dernière MAJ:** 2026-08-29
**Prochaine action:** Confirmer avec l'utilisateur la question de scope des liens « Lire l'édition → » avant de commencer (recommandation : pas de cascade automatique)
**Blocage:** Question de scope non tranchée + décision de cadence (ponctuel vs récurrent)

### État actuel
Pas commencé. Évalué le 29 août : **ce n'est pas un travail de 5 minutes**, donc passé en ticket plutôt qu'improvisé. Retour utilisateur d'origine : « il faudrait le faire si tu le fais en 5 minutes tu fais now ». Le scope est déjà posé pour ne pas repartir de zéro.

### À faire
- **Trancher la question de scope avec l'utilisateur** : chaque carte jour a un lien « Lire l'édition → » vers `archives/{AAAA-MM-JJ}.html`. Sur les 7 dates d'une semaine, seule une poignée aura une traduction déjà faite (cascade des éditions citées, voir B005) — la plupart pointeraient vers du français même sur une page par ailleurs en anglais.
- **Trancher la cadence** : `hebdo/` est produit **chaque semaine**. Si celui-ci est traduit, se pose la question des suivants — nouvelle étape récurrente dans `docs/routine-hebdo-prompt.md`, symétrique à l'étape 13 de `docs/routine-prompt.md` — pas juste un geste ponctuel sur l'édition du 23 août.
- Puis traduire.

### Décisions
- **Recommandation (à confirmer, pas à trancher seul en cours de traduction)** : ne pas déclencher de cascade automatique sur les liens hebdo (7 articles complets d'un coup serait disproportionné) — les laisser pointer vers le français par défaut, sauf si une traduction existe déjà pour cette date précise. Même logique que les liens `suivi/`/`hebdo/` déjà laissés en français à l'intérieur des articles quotidiens.

### Historique
- **2026-08-29** — Volume réel mesuré sur `hebdo/2026-08-23.html` (gabarit type) : 1 paragraphe de conclusion (~150 mots) + 7 cartes jour, chacune question + 3 mini-scénarios (titre + 1-2 phrases) — une trentaine de blocs de texte courts, plus masthead/nav/footer/scripts déjà connus. Plus léger qu'un article complet (pas de dek/essentiel-box/lexique/sources/list-box) mais **grossièrement la moitié du volume d'un article déjà traduit**.

---

## B007 — Traduire en anglais `le-projet.html` et les pages légales

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée (question ouverte issue de B005)
**Dernière MAJ:** 2026-08-29
**Prochaine action:** Lever les deux réserves (sensibilité RGPD/juridique, dépendance au glossaire resté hors scope) avant de s'y lancer — voir `docs/strategie-anglais.md` § « UX de bascule entre langues »
**Blocage:** Question ouverte, pas tranchée

### État actuel
Les pages statiques (`le-projet.html`, `glossaire.html`...) ne sont pas traduites. Question explicitement ouverte : les traduire avec le même bouton de bascule FR/EN que les éditions, ou non. Prochaine étape éventuelle « si l'audience confirme l'hypothèse ».

### À faire
- Décider si `le-projet.html` et les pages légales (mentions légales, politique de confidentialité) sont traduites.
- Si oui, produire un équivalent anglais **tout aussi rigoureux** : pas une simple traduction automatique vu la sensibilité RGPD/juridique.

### Décisions
- Deux réserves posées avant de s'y lancer : (1) sensibilité RGPD/juridique du contenu légal ; (2) dépendance au glossaire anglais, resté hors scope (écarté, voir B005).

### Historique
- **2026-08-07** — Point de vigilance posé : si une vraie version anglaise voit le jour (pas juste la variante « posts X »), `politique-de-confidentialite.html` et les mentions légales doivent avoir un équivalent anglais aussi rigoureux.
- **2026-08-29** — Question laissée explicitement ouverte au moment de l'ajout du bouton de bascule + `hreflang` (voir B005), avec les deux réserves ci-dessus.

---

## B008 — Traduction rétroactive des archives françaises en anglais

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée (question ouverte issue de B005)
**Dernière MAJ:** 2026-08-31
**Prochaine action:** À revisiter au plus tôt le 15 septembre 2026, en même temps que le check Google Actualités posé sur `en/` — et à retraiter **ensemble** avec les pages thématiques EN (B139), pas l'un sans l'autre
**Blocage:** Dépend de la confirmation d'une audience anglophone

### État actuel
Seules les éditions traduites au fil de l'eau existent en anglais : la traduction quotidienne à partir du 29 août, plus les archives tirées par la cascade des articles cités (voir B005). Au 31 août : 5 articles traduits sous `en/archives/`. Aucune campagne de traduction rétroactive décidée.

### À faire
- Décider si la traduction s'applique seulement aux éditions futures ou aussi rétroactivement aux `archives/*.html` existantes — et si oui, lesquelles, et avec quelle méthode de contrôle qualité vu le volume.

### Décisions
- Aucune décision prise. La question est explicitement notée comme « encore ouverte » depuis le 7 août.

### Historique
- **2026-08-07** — Question posée dans les « points à réfléchir » de la version anglaise (voir B005).
- **2026-08-29** — La cascade des articles cités (un seul niveau) traduit de fait quelques archives au passage, mais ce n'est pas une politique de rattrapage.
- **2026-08-31** — Repère de calendrier posé : revisiter au plus tôt le 15 septembre 2026, conjointement avec « pages thématiques EN » (B139).

---

## B009 — Déclinaison papier de Scénario — « Les Cahiers de Scénario »

**Statut:** STANDBY
**Priorité:** P3
**Dernière MAJ:** 2026-08-25
**Prochaine action:** Si on avance : partir de la maquette `docs/mockups/cahier-scenario-2026-08-25.html` pour la Phase 1 de `docs/strategie-papier.md` (PDF hebdo freemium réservé aux abonnés newsletter) — ne pas repartir d'une page blanche
**Blocage:** Rien d'engagé ; attend que l'utilisateur veuille avancer. Prix de la Phase 3 à revoir une fois un devis de fulfillment obtenu

### État actuel
Stratégie complète et phasage déjà tranchés et documentés dans `docs/strategie-papier.md` — **ce fichier reste la source de vérité**, ne pas le recopier. Rien n'est engagé. Une maquette de mise en page 2 pages A4 est déjà réalisée et versionnée : `docs/mockups/cahier-scenario-2026-08-25.html` (ouvrir tel quel dans un navigateur, imprimable A4 via Ctrl/Cmd+P), **à ne pas refaire**. Aussi publiée comme Artifact : https://claude.ai/code/artifact/d5e72207-faf4-4b9d-b0ed-24ccaa21e626 (peut avoir divergé du fichier versionné si retouchée côté Artifact sans re-synchro).

### À faire
- Phase 1 : PDF hebdo **freemium**, réservé aux abonnés de la newsletter gratuite existante (Buttondown, `newsletter.html`), pas de téléchargement public libre — pour transformer chaque diffusion en inscription qualifiée plutôt qu'un fichier diffusé dans le vide ; ciblé profs HGGSP/SES déjà identifiés comme public dans `le-projet.html`.
- Phase 2, si traction : kit pédagogique par sujet (3 scénarios + questions de classe), coconçu avec des profs volontaires.
- Phase 3, si la demande est confirmée : objet imprimé payant, **cadence trimestrielle** (~100-120 pages/numéro en compilant 3 mois).
- Obtenir un devis de fulfillment (commission/tarif au pli) avant de figer un prix.

### Décisions
- **Pas de quotidien imprimé** : charge solo trop lourde, et incompatible avec le mécanisme de suivi/réévaluation des probabilités, cœur différenciant du projet. Un format ponctuel a du sens en partant du hebdo existant.
- **Phase 0 (tranchée le 17 août) : d'abord le développement de la marque, le revenu ne vient qu'en Phase 3.**
- **Cadence trimestrielle arbitrée le 17 août** pour la Phase 3 : ~100-120 pages/numéro en compilant 3 mois, pour amortir le coût d'expédition qui pèse presque autant que l'impression sur un objet léger.
- **Automatisation maison écartée le 17 août** (Steady/Stripe + Make.com + API Gelato/Pumbo construits et maintenus en solo) : un bug de RPA sur ce pipeline toucherait des abonnés déjà payés (adresse, envoi, prélèvement), risque jugé trop lourd à porter seul. **Décision de déléguer** la chaîne abonnement/impression/envoi à un prestataire externe : routeur presse spécialisé, ou plateforme d'abonnement avec intégration impression déjà maintenue par un tiers, plutôt qu'un scénario Make.com fait main.
- **Freemium (précisé le 17 août)** pour la Phase 1.

### Historique
- **2026-08-17 (idée)** — Question posée par l'utilisateur : faut-il décliner Scénario en version papier, et si oui comment. Avis et stratégie détaillés dans `docs/strategie-papier.md`. Chiffrage indicatif de la Phase 3 : « Cahier Scénario », impression à la demande sans stock (devis Gelato ~40p : ≈7,55 € HT en promo / ≈11 € HT hors promo, à réévaluer sur le format 100-120p réel), prix indicatif 12-15 € TTC/numéro ou ~45-55 €/an en abonnement — **impact prix à revoir** une fois un devis de fulfillment obtenu (commission/tarif au pli non inclus dans le calcul DIY). Serait le premier revenu récurrent au-delà du don libre Buy Me a Coffee.
- **2026-08-25** — Maquette 2 pages A4 réalisée et versionnée (`docs/mockups/cahier-scenario-2026-08-25.html`) : couverture plein cadre + page article, contenu réel du site (chiffres, scénarios, « L'essentiel », vraie photo Pexels déjà utilisée sur le site — rien d'inventé), calibrée A4 210×297 mm, imprimable directement. Sert à juger du ton d'un numéro payant à focus thématique tournant — exemple pris : « IA chinoise : cadeau ou piège ? ».
---

## B010 — Image de pub Instagram générique (« brand-teaser », ex « Suis @scenarios.actu »)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-09
**Prochaine action:** Diffusion pas encore branchée — image prête, pas encore poussée en pub Meta/Instagram par l'utilisateur. Comparer `brand-teaser-4x5-v2.png` et `-v3.png` avant de choisir laquelle utiliser
**Blocage:** Aucun

### État actuel
Trois fichiers finaux sans CTA, réutilisables sur plusieurs plateformes : `assets/social/instagram-ads/brand-teaser-square.png` (1:1), `assets/social/instagram-ads/brand-teaser-4x5-v2.png` (4:5, base v2), `assets/social/instagram-ads/brand-teaser-4x5-v3.png` (4:5, base v3 avec étoiles). Les 3 fichiers originaux `follow-cta-v2-*`/`v3-4x5.png` (avec la phrase « 👉 Suis @scenarios.actu ») restent aussi dans le dépôt, au cas où une version avec CTA spécifique Instagram soit utile un jour. Concept visuel : une route qui se sépare en trois (verte/bleue/rouge, tronc doré), reprenant le tronc/branches du logo du site.

### À faire
- Pousser l'image en pub Meta/Instagram (geste utilisateur).
- Choisir entre v2 et v3 (4:5).
- **Point de vigilance mineur, non corrigé** (présent sur les deux versions 4:5) : le rayon doré central passe juste derrière « LESSCENARIOS.FR » en bas — reste lisible mais contraste réduit à cet endroit (texte doré sur lueur dorée). Pas bloquant ; si itération future, baisser l'intensité du rayon à cette hauteur.

### Décisions
- **Retrait de la phrase « 👉 Suis @scenarios.actu » (9 août)** : l'image doit être réutilisable sur plusieurs plateformes (Instagram, X...) qui n'ont pas le même identifiant de compte — un CTA avec un handle spécifique n'a plus sa place sur ce visuel générique.
- **Pas de régénération via l'outil IA** pour ce retrait (économise des crédits) : retrait en local par interpolation verticale simple.
- Garde-fous de prompt IA repris des tentatives précédentes : aucune modification du texte, aucun chiffre/texte inventé.

### Historique
- **2026-08-08** — Deux premiers résultats écartés : vocabulaire des scénarios renommé sur l'un, chiffre parasite dans le fond sur l'autre (détail dans le diff, plus la peine de le détailler). Base : `assets/social/instagram-ads/follow-cta-v1.png` (gabarit maison, identique visuellement aux posts quotidiens).
- **2026-08-09 [FAIT]** — Repris une fois les crédits IA renouvelés, avec le nouveau concept demandé (route qui se sépare en trois) plutôt qu'un simple fond texturé. Résultat validé, formats sauvegardés : `assets/social/instagram-ads/follow-cta-v2-square.png` (1:1, 1254×1254), `assets/social/instagram-ads/follow-cta-v2-4x5.png` (4:5, 1122×1402 — format demandé en second, généralement préférable sur le fil Instagram pour l'espace vertical), `assets/social/instagram-ads/follow-cta-v3-4x5.png` (4:5, 1122×1402, variante envoyée juste après avec un léger semis d'étoiles en fond ; pas un doublon exact du v2-4x5).
- **2026-08-09 (retrait du CTA)** — Méthode : pour chaque colonne de pixels, la bande contenant le texte est remplacée par un dégradé entre la ligne juste au-dessus et celle juste en dessous, ce qui se fond dans la lueur de la route en arrière-plan (script Python ponctuel, pas conservé). Fichiers renommés (`follow-cta-*` ne convenait plus) en `brand-teaser-*`.
- **2026-08-09 (piège rencontré et corrigé)** — La bande de texte n'est pas à la même hauteur d'un fichier à l'autre (généré indépendamment par l'outil IA externe à chaque fois) : appliquer la bande détectée sur v3 (y≈1019-1047) au fichier v2 (texte en réalité à y≈967-991) a produit un résultat raté (texte à moitié effacé, effet de stries). **Fix** : détecter la bande de texte séparément pour chaque fichier (recherche des pixels de la couleur dorée du texte, `#cf9d4c` avec tolérance) avant de choisir la zone à interpoler.

---

## B011 — WhatsApp comme canal de distribution supplémentaire

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-08 (non daté précisément)
**Prochaine action:** Explorer le module natif Make **WhatsApp Business Cloud API** — nécessite un compte WhatsApp Business + accès à l'API Cloud Meta
**Blocage:** Pas encore configuré ; attend que l'utilisateur veuille avancer

### État actuel
Aucune diffusion WhatsApp. Buffer limite à 3 connecteurs gratuits, déjà pris par X, Facebook et Instagram — un 4e connecteur Buffer serait payant.

### À faire
- Brancher WhatsApp directement dans Make.com via son module natif **WhatsApp Business Cloud API** (comme Telegram/LinkedIn aujourd'hui), sans passer par Buffer — nécessite un compte WhatsApp Business + accès à l'API Cloud Meta (gratuit jusqu'à un certain volume de messages).

### Décisions
- **Option écartée** : créer un second compte Buffer gratuit avec une autre adresse email pour contourner la limite des 3 connecteurs — risque réel de détection (même site `lesscenarios.fr`, mêmes réseaux sociaux liés, probablement même appareil/IP) et de suspension des comptes liés, ce qui casserait aussi X/Facebook/Instagram qui tournent déjà bien. Non recommandé, écarté après discussion.
- **WhatsApp Channels écarté** : pas d'API officielle gratuite, seulement des services tiers payants et non garantis par Meta (voir B094).

### Historique
- **2026-08-01 (env.)** — WhatsApp Channels écarté au moment de la mise en place de Telegram, faute d'API officielle gratuite.
- **2026-08 (non daté)** — Limite Buffer identifiée, contournement par second compte écarté, piste module natif Make retenue.

---

## B012 — Stratégie de pub payante (Meta/Instagram, X) et distribution gratuite

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-08-10
**Prochaine action:** Mettre en place un vrai tracking de conversion (UTM / pixel) avant de dépenser quoi que ce soit
**Blocage:** Pas de tracking de conversion en place ; **pas encore lancé côté ads payantes**

### État actuel
Rien de lancé côté publicité payante. En parallèle, une action manuelle est en cours côté utilisateur, hors de toute automatisation du dépôt : **envoi d'invitations Instagram** (inviter des contacts à suivre le compte) pour faire grossir l'audience avant d'envisager de la pub payante — pas de suivi chiffré dans ce dépôt.

### À faire
- Tracking de conversion (UTM / pixel) pour savoir si les clics se transforment en abonnés — prérequis avant toute dépense.
- Éventuel budget test de 5-10 €/jour sur Meta Ads Manager (Instagram + Facebook), ciblage par centres d'intérêt (« actualité », « géopolitique », 15-35 ans, France), pointant directement vers `newsletter.html` plutôt que le site en général.
- Pistes de distribution **gratuite** listées le même jour, non faites : soumission du site à Google Actualités (fondations déjà posées, voir B104), annuaire [DataNewsletters](https://www.datanewsletters.com/inscription-annuaire-newsletters), [Feedspot](https://rss.feedspot.com/) et Flipboard pour `feed.xml` (voir aussi B013, qui prépare un flux propre pour ces soumissions).

### Décisions
- **Meta plutôt que X Ads pour démarrer** : jugé plus mature et moins cher au clic.
- Pointer les annonces vers `newsletter.html`, pas vers le site en général.

### Historique
- **2026-08-10** — Discussion complète : budget test, ciblage, destination, prérequis tracking, pistes gratuites, et action manuelle d'invitations Instagram déjà en cours côté utilisateur.

---

## B013 — Flux RSS dérivé, propre pour les vrais lecteurs RSS

**Statut:** À FAIRE
**Priorité:** P3
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Scoper le script (nom de fichier, fréquence de génération, où le lier depuis le site) — aucune urgence
**Blocage:** Aucun

### État actuel
`feed.xml` **ne valide pas** au W3C Feed Validator (vérifié le 15 août) : erreur critique répétée sur chaque item (« Invalid character in a URI ») parce que `<comments>` contient le texte complet du post social (accents, retours à la ligne, emojis) au lieu d'une URL, comme l'exige la spec RSS 2.0. Cause : `{{comments}}` est le champ que **tous les modules Make** (Telegram/X/Facebook/Instagram/LinkedIn/Bluesky, sur les 3 flux) utilisent pour le texte du post — un lecteur RSS strict rejette ça, Make s'en moque complètement. Avertissements secondaires : `style="max-width..."` inline dans le HTML de `<description>` (signalé « potentiellement dangereux » par le validateur), et pas de `<atom:link rel="self">`. Aucun flux dérivé n'existe.

### À faire
- Écrire un script séparé (même esprit que `scripts/social/generate_*.py`) qui **lit** `feed.xml` (lecture seule, jamais d'écriture dessus) et génère un flux dérivé propre : `<comments>` retiré ou remplacé par une vraie URL, `<atom:link rel="self">` ajouté, warning `style` nettoyé si besoin.
- Destiné aux vrais lecteurs RSS et à la soumission Feedspot/DataNewsletters/Flipboard (voir B012).
- Scoper : nom de fichier, fréquence de génération, emplacement du lien sur le site.

### Décisions
- **Décision du 15 août : ne jamais toucher `feed.xml`/`feed-pub.xml`/`feed-suivi.xml` pour corriger ça** — ce sont les 3 flux dont dépend tout le pipeline Make ; le risque de casser des automatisations qui marchent dépasse largement le bénéfice d'une conformité RSS que personne n'exploite aujourd'hui en tant qu'abonné réel.

### Historique
- **2026-08-15** — Constat de non-validation vérifié via le W3C Feed Validator, cause identifiée, décision de ne pas toucher aux flux de production, piste du flux dérivé retenue.

---

## B014 — Bluesky comme canal de diffusion

**Statut:** FAIT
**Priorité:** P1 (à l'origine, avec Threads/Mastodon)
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Bluesky est branché sur les **3 circuits** (Daily, RSS SUIVI, RSS PUB) via le **module Make natif** (`Olivier's Bluesky connection`, compte `scenario-actu.bsky.social`) : modules 80 (Daily), 85 (RSS SUIVI), 83 (RSS PUB). Chaîne à 3 modules par branche pour la photo : `http:DownloadFile` → `bluesky:uploadMedia` → `bluesky:createAPost`. Les 3 branches ont été vérifiées cohérentes dans l'export final avant resynchronisation de `assets/make/scenario-daily.blueprint.json`.

### À faire
- Rien.

### Décisions
- **Module natif Make plutôt que Buffer** — contrairement à la supposition initiale du 15 août, qui pensait devoir passer par Buffer faute de module natif trouvé.
- **Limite de 300 caractères** sur le champ `Text` : le texte quotidien (module 80) réutilise la formule courte déjà éprouvée pour X (`{{4.title}}` + tagline fixe + CTA), jamais `{{4.comments}}` complet qui dépasserait la limite la plupart des jours. La branche RSS PUB (module 83) utilise en revanche `{{58.comments}}` complet (eyebrow + message + attribution + CTA) — safe ici car le contenu « pub » est conçu court par nature (voir `docs/pub-messages.md`).
- **Photo : upload en 2 temps, pas une simple URL.** L'API Bluesky (protocole AT) exige d'uploader l'image comme un « blob » séparé avant de l'attacher : `http:DownloadFile` (récupère le fichier depuis `{{X.enclosures[].url}}`) → `bluesky:uploadMedia` (renvoie un CID/`blob.ref`) → `bluesky:createAPost` (`embed.$type: app.bsky.embed.images`, référence le blob). Testé d'abord avec `embed.$type: app.bsky.embed.external` (simple lien avec URL/titre/description, sans upload) — **confirmé par l'utilisateur que ça n'affiche aucune vignette** quand l'URL pointe directement sur un fichier image plutôt qu'une page HTML (pas de balises `og:image` à scraper) ; abandonné au profit du vrai upload.
- **Lien cliquable : « facets », pas d'auto-détection d'URL.** Une URL en texte brut reste du texte inerte sur Bluesky — il faut un facet (`app.bsky.richtext.facet#link`) associant un sous-texte (`keyword`) à une URL cible (`feature.uri`). **Convention retenue : le mot « ici »** dans le texte (ex. « 📖 L'article est ici ») sert d'ancre cliquable plutôt que d'afficher l'URL brute — plus propre visuellement que le lien nu utilisé sur X/Facebook.

### Historique
- **2026-08-15 (idée, critère)** — Bluesky retenu avec Threads et Mastodon parce que son format colle **déjà** à ce que produit le pipeline (texte court + lien + image carrée) : zéro nouveau format de contenu à inventer (voir B015/B016).
- **2026-08-15 [FAIT]** — Branché sur les 3 circuits via le module natif.
- **2026-08-15 (3 problèmes trouvés et corrigés, relecture du blueprint, 2 allers-retours)** :
  1. Module 85 (RSS SUIVI) : le texte ne contenait pas le mot « ici » alors que son facet le cherchait — lien resté non cliquable jusqu'à correction du texte.
  2. Module 83 (RSS PUB) : utilisait par erreur la tagline de la branche Daily (« Scénario : chaque jour, un sujet d'actu décrypté en 3 scénarios chiffrés ») au lieu de `{{58.comments}}` — contenu hors sujet pour un post « pub » (perdait l'eyebrow/attribution/CTA propres à chaque entrée). Corrigé.
  3. Module orphelin (id 77, premier essai en `embed.external`) resté dans le blueprint après le passage à `embed.images` — signalé par Make lui-même (« not connected to the flow »), sans impact fonctionnel mais supprimé pour la propreté du scénario.

---

## B015 — Mastodon comme canal de diffusion

**Statut:** À FAIRE
**Priorité:** P1 à l'origine, mais explicitement « un cran en dessous de Threads » — priorité réelle à confirmer maintenant que Threads est fait
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Vérifier l'existence d'un module Mastodon natif dans la barre de recherche des apps Make ; sinon Buffer en repli si Buffer supporte le réseau et qu'il reste de la place sur le plan gratuit
**Blocage:** Aucun ; attend que l'utilisateur veuille avancer

### État actuel
Toujours en attente, rien d'implémenté. Même logique et même format que Bluesky (B014), audience plus réduite mais technophile/engagée.

### À faire
- Même méthode que pour Bluesky : module natif si disponible, sinon Buffer en repli (sous réserve de la limite de 3 connecteurs gratuits, voir B011).

### Décisions
- Priorité un cran en dessous de Threads (B003).

### Historique
- **2026-08-15** — Retenu comme piste P1 avec Threads et Bluesky, sur le critère « format déjà compatible avec ce que produit le pipeline » (texte court + lien + image carrée), contrairement à la vidéo (voir B017).

---

## B016 — Réseaux sociaux écartés (Pinterest, Reddit, Discord, YouTube)

**Statut:** ABANDONNÉ
**Priorité:** —
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune — ne pas reproposer sans nouvel élément
**Blocage:** —

### État actuel
Écartés lors du passage du 15 août sur les canaux supplémentaires, pour mauvais fit avec le sujet (actu/géopolitique quotidienne, pas de pipeline vidéo).

### À faire
- Rien.

### Décisions
- **Pinterest** : visuel evergreen, pas de l'actu.
- **Reddit** : pas un canal de diffusion automatisable proprement — soumission communautaire avec règles anti-spam strictes, risque de ban si posté automatiquement. (À ne pas confondre avec le « Reddit ciblé » évoqué comme piste de netlinking humain, voir B067.)
- **Discord / YouTube** : chantiers différents (communauté à modérer / vidéo à produire), hors du périmètre « quasi gratuit à ajouter ».

### Historique
- **2026-08-15** — Écartés dans le même passage que la sélection Threads/Bluesky/Mastodon.

---

## B017 — Générer les posts « pub » en Reel plutôt qu'en image statique (et TikTok)

**Statut:** BLOQUÉ
**Priorité:** P2
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Ajouter une étape de génération vidéo (ex. léger zoom/pan sur `assets/social/pub/{date}.png`, 4-6 secondes, avec ou sans musique, export mp4) en amont de `generate_pub_image.py` — prérequis de tout le reste
**Blocage:** **Contrainte API vérifiée le 15 août** : l'Instagram Content Publishing API exige `media_type=REELS` + un vrai `video_url` (mp4/mov) — aucun moyen de publier un Reel à partir d'une simple image via l'API. TikTok a la même contrainte de base (plateforme 100 % vidéo native)

### État actuel
Bloqué sur l'absence de brique de génération vidéo. Motivation d'origine : reach nettement supérieur aux posts statiques sur Instagram (et de plus en plus sur Facebook). TikTok rejoint ce chantier plutôt que d'être une piste séparée, pour la même raison technique. Pas encore scopé en détail (outil de rendu vidéo à choisir, durée, musique ou silence, adaptation TikTok).

### À faire
- Étape de génération vidéo en amont, puis brancher le module Make natif **Instagram for Business → « Create a reel post »**.
- Pour TikTok : vérifier l'existence de son module natif dans Make (pas fait).
- **TikTok demande en plus une vraie adaptation éditoriale** (format rapide/punchy, souvent une voix ou une personnalité à l'écran) — plus qu'un nouveau canal, un nouveau format de contenu à concevoir, à ne pas sous-estimer même une fois la brique vidéo résolue.

### Décisions
- La conversion « photo → reel » visible dans l'app Instagram se fait côté app, pas via l'API/Make : elle n'est donc pas une option.

### Historique
- **2026-08-15** — Idée, contrainte API vérifiée, TikTok rattaché au même chantier.

---

## B018 — Giveaway « abonne-toi à la newsletter = tirage au sort »

**Statut:** STANDBY
**Priorité:** P3
**Dernière MAJ:** 2026-08-10
**Prochaine action:** Reprendre une fois quelques dizaines/centaines d'abonnés atteints
**Blocage:** Base d'abonnés trop faible pour que l'effet réseau d'un giveaway existe

### État actuel
**Écarté pour l'instant.** Objectif initial : faire croître la base newsletter (notée alors comme MailerLite, **1 seul abonné**) via un jeu-concours simple. Avec une base aussi faible, l'effet réseau (partages, viralité) est quasi nul — priorité d'abord à la distribution sur les canaux existants (site, Telegram, réseaux) pour bâtir une vraie base avant d'investir dans un lot. Mécanique du jeu (règles, page d'inscription, tirage) pas encore conçue.

### À faire
- Concevoir la mécanique (règles, page d'inscription, tirage) le jour où la base le justifie.

### Décisions
- Pistes de lot déjà discutées, du moins cher au plus engageant : goodies Scénario (sticker/mug) ; accès « premium » gratuit à vie si le site se monétise un jour ; un livre géopolitique marquant ; un an d'abonnement à un média de référence (Le Monde, Courrier International...) ; une carte cadeau généraliste.

### Historique
- **2026-08-10** — Idée, écartée le jour même pour cause de base trop faible.

---

## B019 — Boutons de partage sur chaque édition (+ icônes)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Le partage est une ligne discrète `.share-inline` juste sous `.pubdate` (haut de page), avec des icônes SVG inline fines (X, Facebook, LinkedIn, WhatsApp, Telegram, copier le lien) — pas de texte ni de logos couleur officiels des plateformes. Style repris de `.sources-note` des pages de suivi (texte gold, soulignement pointillé, pas de gros boutons). 100 % statique/générique : les liens sont construits côté client en JS à partir de l'URL et du `<h1>`, donc **aucune donnée à générer par la routine quotidienne** — reproduit automatiquement avec le reste du gabarit. Le bloc du bas garde son titre d'origine « Vote avant de connaître le résultat » et ne contient plus que « Rejoindre le canal Telegram ».

### À faire
- Rien.

### Décisions
- Position discrète juste sous le titre (décision du 4 août), pas de gros boutons en bas de page.
- Icônes SVG inline fines plutôt que les logos couleur officiels.

### Historique
- **2026-08-04 [FAIT]** — Boutons de partage (X, LinkedIn, WhatsApp, copier le lien) ajoutés sur chaque édition (`index.html`, section `.share-block`, juste avant le footer). Testé desktop + mobile via Playwright avant publication. S'applique à partir de l'édition suivante (les archives déjà publiées restent figées).
- **2026-08-04 (même jour) — fusion avec `.telegram-promo`** : retour utilisateur (deux sections quasi identiques l'une sous l'autre) — un seul bloc « Rejoindre et faire circuler », bouton Telegram en premier suivi des boutons de partage ; CSS `.telegram-promo` obsolète retiré.
- **2026-08-04 (même jour) — déplacé une seconde fois** : retour utilisateur (boutons tout en bas = besoin de scroller, moins accessible) — passage à la ligne discrète `.share-inline` sous `.pubdate`.
- **2026-08-05 → 08 [FAIT, non daté précisément]** — Icônes SVG inline ajoutées, inspirées d'un exemple brief.eco vu le 5 août. Cette entrée était restée non cochée par erreur alors que le travail avait déjà été fait ; repéré le 8 août en vérifiant l'état réel du code plutôt que de se fier au backlog seul.

---

## B020 — X (Twitter) comme canal de diffusion

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
X est diffusé via **Buffer** (gratuit : 3 canaux, 10 posts programmés par canal, largement suffisant pour 1 post/jour), Buffer gérant lui-même sa propre app développeur X — aucune clé API à fournir. Module Make natif **Buffer → « Create a status update »** (module 14 pour le Daily), ajouté comme 3e sortie du Router existant (même déclencheur RSS `feed.xml`). `Text` = `Title` + une phrase fixe de contexte (« Scénario : chaque jour, un sujet d'actu décrypté en 3 scénarios chiffrés ») + « Lire l'article : » + `URL`. **X reste sur Buffer** même après la migration d'Instagram/Facebook vers les modules natifs le 15 août : pas de solution native depuis le retrait de l'app X de Make.

### À faire
- Rien.

### Décisions
- **Jamais la `Description`/`Comments` complète** dans le post X : largement au-dessus des 280 caractères certains jours — vérifié sur les 10 dernières éditions au 6 août, **8 sur 10 auraient dépassé la limite rien qu'avec Titre + Comments**.
- **Buffer plutôt que l'API X directe** (voir historique).
- X exclu du passage à `{{4.source.title}}` (« L'essentiel ») le 11 août : ~700-750 caractères, très au-dessus de 280 — l'utilisateur gère ce module lui-même dans Make (voir B023).

### Historique
- **2026-08-06 (plan initial abandonné)** — La connexion directe Make ↔ API X via un compte développeur a été tentée puis abandonnée : Make a supprimé son app native « X (Twitter) » le **3 avril 2025** (API X passée payante), et la reconstruction manuelle en HTTP OAuth 2.0 + PKCE dans Make (Authorize/Token URI, `code_challenge`/`code_verifier`, Client ID/Secret du compte développeur X) a buté sur des échecs de connexion répétés (« Accounts verify failed », « Something went wrong ») malgré une config conforme à la doc officielle Make — **cause exacte non identifiée**, abandonné après plusieurs tentatives.
- **2026-08-06 [FAIT et vérifié]** — Solution Buffer retenue et branchée.
- **2026-08-08** — Image ajoutée au post X du circuit Daily (voir B021).
- **2026-08-15** — Confirmé que X reste sur Buffer, contrairement à Instagram/Facebook passés en natif (voir B024/B025).

---

## B021 — Image Instagram attachée aux posts X et Facebook (circuit Daily)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Modules 14 (X) et 32 (Facebook) du circuit Daily utilisent le même mapping que la branche Instagram : `useMedia: true`, `media.picture` = `{{4.enclosures[].url}}`.

### À faire
- Rien sur ce périmètre. Le circuit RSS SUIVI a été traité séparément le 12 août (voir B035).

### Décisions
- **LinkedIn volontairement exclu** de ce lot (retour utilisateur) : le module LinkedIn poste en **Media Type = Article** (carte de lien cliquable, image OG du site récupérée automatiquement) ; passer en Image ferait perdre cette carte cliquable, jugé moins bon pour driver du trafic vers le site. *(Décision inversée le 11 août, voir B022.)*
- **Pas fait sur le circuit RSS SUIVI** à ce moment-là (modules 24/33, toujours `useMedia: false`) : `feed-suivi.xml` ne portait pas de tag `<enclosure>` à cette date, rien à mapper — pas demandé, laissé tel quel.

### Historique
- **2026-08-08 [FAIT]** — Confirmé via le blueprint Make ré-exporté par l'utilisateur le 8 août, qui a aussi capturé au passage le fix `filterDateFrom` (fenêtre glissante `addDays(now; -1)`) du module 30, resté en attente de ré-export depuis sa correction — `assets/make/scenario-daily.blueprint.json` mis à jour avec ce blueprint (voir B118).

---

## B022 — LinkedIn : passage au post Image natif (`CreateCompanyImagePost`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune sur la branche Daily
**Blocage:** Aucun

### État actuel
Sur la branche LinkedIn du circuit Daily, le duo module 52 (`http:DownloadFile`) + module 7 (`linkedin:CreateTextShare`, type Article) est remplacé par un **module unique `linkedin:CreateCompanyImagePost` (id 53)** : `method: "link"` (upload par URL, le module télécharge lui-même), `url: {{4.enclosures[].url}}` (même champ que Twitter/Instagram/Facebook), `organization: urn:li:organization:136694258`. Le lien de l'article est en **toute première ligne** du texte du post. Blueprint ré-exporté et validé le 11 août.

### À faire
- Rien sur la branche Daily. La branche RSS SUIVI a été traitée le 12 août (voir B035).

### Décisions
- **Décision du 8 août inversée** : grande photo native plutôt que carte de lien cliquable. Compromis assumé — le lien reste cliquable dans le texte du post, mais il n'y a plus de carte de prévisualisation à côté.
- **Toujours « Create a Company Image Post »**, jamais « Create a User Image Post » (qui poste en tant que profil personnel).
- **Lien en première ligne** : sur un post Image natif, contrairement à l'Article, le lien n'est cliquable que dans le texte — s'il arrive après le titre et le contexte, il finit caché derrière le « …voir plus » de LinkedIn. `content` = `"👉 Lire l'analyse complète : {{4.url}}{{newline}}{{newline}}{{4.title}}{{newline}}{{newline}}{{4.comments}}{{newline}}"` (auparavant l'accroche « 🔥 Nouvelle édition Scénario, à lire 👇 » ouvrait le post et le lien arrivait en dernier).

### Historique
- **2026-08-11 (diagnostic en 3 étapes)** — Repéré : un post LinkedIn réel de l'édition du jour n'affichait aucune photo (carte de lien Article sans vignette, malgré un montage binaire déjà en place, `http:DownloadFile` id 52 → `linkedin:CreateTextShare` id 7, `media.thumbnail.data` mappé).
  1. D'abord attribué à un bug de déploiement du site ce jour-là (site indisponible au moment où LinkedIn scanne l'URL) — cause réelle mais partielle.
  2. Un second post de test (site de nouveau opérationnel) a bien affiché une image, mais **en petite vignette carrée**, jamais en grande bannière — ce qui a orienté à tort vers une hypothèse de format d'image (carré 1080×1080 vs paysage 1.91:1).
  3. **Cause réelle, précisée par l'utilisateur** : pas un problème de format d'image mais de **type de post**. `CreateTextShare` en `type: ARTICLE` ne peut poster qu'une carte de lien (vignette toujours petite, quelle que soit l'image fournie) — jamais une grande image native. Il faut un module LinkedIn différent, pas une option du module Article.
- **2026-08-11 (erreur intermédiaire)** — L'utilisateur, en configurant lui-même le module, avait d'abord choisi **« Create a User Image Post »** (erreur API « Member permissions must be used when using person as owner ») au lieu de **« Create a Company Image Post »**, cohérent avec tous les autres modules du scénario. Corrigé.
- **2026-08-11 (réordonnancement du texte, même jour)** — Lien déplacé en première ligne, titre et contexte repoussés en dessous, configuré directement dans Make par l'utilisateur ; `assets/make/scenario-daily.blueprint.json` mis à jour pour rester synchronisé.
- **2026-08-11** — Noté à l'époque : **pas encore fait sur la branche RSS SUIVI** (module 22, toujours en Article/vignette vide), qui bloquait de toute façon sur l'absence d'`<enclosure>` dans `feed-suivi.xml` — traité le 12 août (B035).

---

## B023 — Teaser des posts sociaux : `{{4.comments}}` vs `{{4.source.title}}` (« L'essentiel »)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
**Décision finale (11 août)** : `source` (« L'essentiel ») sur **Instagram (module 34) et LinkedIn (module 53)** ; `comments` (question ouverte, sans le %) uniquement sur **Telegram (module 8) et Facebook (module 32)**. La branche RSS SUIVI n'est pas concernée (modules 23/24/33/22, toujours sur `{{30.comments}}`, non demandé). X/Twitter exclu. `assets/make/scenario-daily.blueprint.json` à jour.

### À faire
- Rien.

### Décisions
- **Critère retenu : « boucle de curiosité vs lien qui fonctionne vraiment »**, puis affiné en « valeur pour la majorité qui ne cliquera pas ».
  - Sur **Instagram**, le lien « en bio » pointe vers l'index du site (l'édition du jour courant), pas vers l'article précis du post — cassé par construction pour quiconque consulte un post après le jour J (usage courant : scroller un profil). Mieux vaut un post autonome qui arrête le scroll (`source`) qu'une question ouverte poussant vers un clic cassé.
  - Sur **LinkedIn** (lien direct fonctionnel), le réflexe dominant reste le scroll : la minorité vraiment intéressée cliquera de toute façon (le lien est en tête du post, visible sans dépasser le « …voir plus »), le reste défile. Le post doit donc apporter de la valeur à cette majorité — même logique qu'Instagram.
  - **Telegram et Facebook** gardent `comments` : lien direct cliquable vers l'article précis (`{{4.url}}`, valide quel que soit le jour de lecture), la boucle de curiosité fonctionne vraiment.
- **X/Twitter volontairement exclu** : « L'essentiel » fait ~700-750 caractères selon les jours, très au-dessus des 280 de X (le module 14 n'utilisait déjà pas `{{4.comments}}`, juste un tagline fixe générique) — l'utilisateur gère ce module lui-même dans Make plutôt que de risquer un échec de publication.

### Historique
- **2026-08-11 (bascule initiale, retour utilisateur)** — `<comments>` dans `feed.xml` ne porte que la question brute du jour ; `<source>` est censé porter « L'essentiel » — un résumé autonome et chiffré (issue la plus probable avec son %, signal concret à surveiller), **conçu justement pour ce genre d'usage** (« Autonome, lisible seul... partage, extrait », `docs/routine-prompt.md`). Jugé bien plus percutant comme teaser. Champ basculé sur `{{4.source.title}}` dans Telegram (8), Instagram (34), Facebook (32), LinkedIn (53).
- **2026-08-11 (bug trouvé au passage)** — Sur l'édition du 11 août, `<source>` contenait par erreur le texte de « Ce qu'on évalue » (`.stakes-text`, dont la place légitime est ailleurs : second paragraphe de la `<description>` de `feed.xml`) au lieu de « L'essentiel ». Vérifié sur les éditions du 8, 9 et 10 août : accroc isolé du 11, pas un bug systémique. Corrigé directement dans `feed.xml` (le `<source>` du 11 août contient le vrai texte « L'essentiel », sans les balises `<strong>`).
- **2026-08-11 (décision intermédiaire, même jour)** — `source` uniquement sur Instagram (34) ; `comments` repassé sur Telegram (8), Facebook (32), LinkedIn (53).
- **2026-08-11 (seconde révision, même jour, LinkedIn seulement)** — Retour utilisateur sur le réflexe de scroll : LinkedIn repasse sur `source`. **Décision finale** posée. Au passage, corrigé sur le module LinkedIn : un `/` parasite et un espace superflu introduits par erreur lors d'une réédition manuelle dans Make, retirés du texte de référence.

---

## B024 — Diffusion automatique sur Instagram (compte, Buffer puis module natif)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune. Point d'attention ouvert : si un run échoue un jour sur le format PNG, envisager une conversion JPEG
**Blocage:** Aucun

### État actuel
Instagram est publié par le **module Make natif 68** (`instagram-business:CreatePostPhoto`, `accountId` `17841439844206886`), via la connexion Facebook réutilisée (`Olivier's Facebook connection`), depuis le 15 août. Avant ça, la route passait par Buffer (module 34). La branche RSS SUIVI a son propre module Instagram (56) et la branche RSS PUB le module 64 (Buffer).

### À faire
- Rien. Surveiller uniquement le point PNG ci-dessous.

### Décisions
- **Point de vigilance Instagram, résolu en pratique** : l'API Content Publishing documente « JPEG only » (`PNG` refusé selon la doc officielle Meta, vérifiée le 15 août), or `assets/social/instagram/{date}.png` est bien un PNG et le module 68 pointe dessus tel quel (`{{4.enclosures[].url}}`) — **confirmé fonctionnel par l'utilisateur au run réel du 15 août**. Donc soit l'API est plus permissive que sa doc, soit il y a une conversion silencieuse côté Make/Meta. Pas de conversion JPEG ajoutée aux scripts, pas nécessaire tant que ça passe.
- **Buffer/Instagram met en file d'attente malgré `type: now`** : le 9 août, le post a été placé en file pour 21h09 au lieu d'être publié immédiatement — comportement Buffer/Instagram plus contraint que X/Facebook (créneau de file d'attente du canal, pas forcément lié à l'heure du scénario Make à 10h00). **Non résolu formellement** : publier manuellement via « Partager maintenant » dans Buffer si besoin d'un post immédiat, ou reconfigurer les créneaux de la file d'attente Instagram côté Buffer pour qu'ils tombent plus tôt. *(Devenu sans objet sur le circuit Daily depuis le passage au module natif le 15 août ; reste vrai pour les branches encore sur Buffer.)*

### Historique
- **2026-07-30 (état initial)** — Pipeline technique déjà prêt (cartes 1080×1080 via `tools/gen_single.js`/`gen_teaser.js`, `feed.xml`/`feed.json`) mais **jamais branché à un vrai compte Instagram** : pas de posting automatique, génération manuelle sans diffusion. Reste à faire noté alors : créer/activer le compte Instagram « Scénario », brancher un outil capable de lire `feed.xml`/`feed.json` avec enclosure image, puis suivre les statistiques (impressions, comptes touchés) pour juger du trafic généré vers `lesscenarios.fr`. Objectif commun avec LinkedIn noté le même jour : ces canaux ne servent à rien tant qu'ils n'ont pas d'audience — la priorité court terme est de poster régulièrement et de construire un minimum de réseau, pas seulement de brancher la technique.
- **2026-08-07 [FAIT]** — Module Make **Buffer → « INSTAGRAM »** (id 34) ajouté comme 5e sortie du Router principal du scénario Daily : `Text` = `Title` + `Comments` + « 👉 Lien en bio pour lire l'analyse complète » (pas de lien direct, Instagram ne rend pas les liens de légende cliquables), `useMedia: true`, `media.link`/`media.picture` = `{{4.enclosures[].url}}`. **Vérifié et validé le 7 août** : la syntaxe `enclosures[]` (crochets vides, plutôt que `enclosures[1]` vu dans l'interface Make au moment du mapping) résout bien vers le premier et seul élément du tableau une fois `feed.xml` alimenté par un vrai `<enclosure>` — confirmé par l'utilisateur.
- **2026-08-09 [FAIT] — bug corrigé : champ image vide sur le module Instagram (Buffer), empêchait la publication.** Repéré via le log d'exécution Make du 9 août (run 10h00) : dans le routeur du circuit Daily, les modules 32 (Facebook) et 34 (Instagram) n'avaient **aucune ligne d'opération** (juste initialisé/finalisé), contrairement aux autres modules — signe qu'ils n'étaient jamais réellement exécutés. Cause : le champ **« Link to an image »** du module Buffer Instagram (34) était vide, alors que le blueprint de référence l'attend mappé sur `{{4.enclosures[].url}}` — sans image, Instagram (qui exige un média, contrairement à Facebook) ne pouvait pas publier. Corrigé par l'utilisateur en remappant `Link`, `Title`, `Description` et `Link to an image` sur `4.Enclosures[]:URL` / `4.Title` / `4.Comments` — testé avec succès le jour même (post publié avec la bonne image composite du 9 août, titre et légende corrects).
- **2026-08-15 [FAIT] — migration Buffer → module natif** : module 68 (`instagram-business:CreatePostPhoto`), à la demande de l'utilisateur après avoir réussi la connexion directe.

---

## B025 — Diffusion automatique sur Facebook (Page « Scénario »)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Facebook est publié par le **module Make natif 70** (`facebook-pages:CreatePostWithPhotos`, `page_id` `1134876509719728`), via `Olivier's Facebook connection`, depuis le 15 août (avant : Buffer, module 32). La branche RSS SUIVI a son module Facebook (33) et la branche RSS PUB le module 71. Le scénario Weekly a aussi une branche Facebook (module 12, `profileIds` identique à celui du Daily, même format que ses branches Telegram/LinkedIn).

### À faire
- Rien.
- **Point de vigilance mineur non bloquant, non corrigé** : le champ `Text` du module 32 (édition quotidienne, version Buffer) contenait un unique retour à la ligne parasite avant `{{4.title}}` — un mélange entre la touche Entrée et la pastille `{{newline}}` du champ Make, malgré plusieurs allers-retours pour le nettoyer. Une ligne vide en trop à l'affichage, sans impact fonctionnel.

### Décisions
- Contrairement à X, Facebook n'a pas de limite de caractères contraignante : `Text` reprend le format riche façon LinkedIn plutôt que le format minimal de X — `Title` + `Comments` complet + lien, avec l'accroche « 🔥 Nouvelle édition Scénario, à lire 👇 » et la clôture « 👉 Lire l'analyse complète : `URL` ».
- **`CreatePostWithPhotos` plutôt que `CreatePost`** : pour poster une vraie photo au lieu d'une carte-lien.

### Historique
- **2026-08-07 [FAIT]** — Facebook ajouté via le même Buffer que X (aucune nouvelle app développeur à créer). La Page Facebook « Scénario » existait déjà, créée automatiquement par Meta lors du passage du compte Instagram dédié en compte pro (une Page Facebook ne peut pas exister sans profil admin — c'est le profil perso qui sert d'admin, la Page reste une entité publique séparée). Connectée à Buffer comme 2e canal (sur les 3 gratuits, X étant le 1er). Nouveau module Make natif **Buffer → « Create a status update »**, 4e sortie du Router existant (même déclencheur RSS `feed.xml`).
- **2026-08-07 (faux positif de test)** — Testé via « Run this module » : la fenêtre de test manuel de Make a renvoyé « Value is not a valid URL address » sur le champ `Comments` — **faux positif propre à la saisie de données de test**, dû au fait que la norme RSS 2.0 définit `<comments>` comme devant contenir une URL, alors que ce flux détourne le tag pour y mettre du texte libre. N'affecte pas le fonctionnement réel (ce même champ était déjà utilisé sans problème par la branche LinkedIn en production). **Contournement** : saisir une URL factice dans la fenêtre de test pour passer la validation.
- **2026-08-07 (même branche sur RSS SUIVI)** — Module 33 (mises à jour de sujets suivis) ajouté avec le même `profileIds`, donc les deux circuits publient sur la Page Facebook.
- **2026-08-15 [FAIT] — migration Buffer → natif, en deux itérations le même jour** : d'abord `facebook-pages:CreatePost` (champ `link`, publie un lien avec vignette), puis remplacé par `facebook-pages:CreatePostWithPhotos` (upload direct via `Photos` > `Use a photo URL`) — confirmé fonctionnel par l'utilisateur.
---

## B026 — Génération de l'image Instagram par édition

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Pipeline HTML/CSS + Playwright : `scripts/social/generate_instagram_image.py` + `scripts/social/instagram-template.html` (gabarit par défaut) et `scripts/social/instagram-photo-template.html` (variante avec photo, voir B027). Image carrée 1080×1080 avec le titre, une accroche courte `hook` sous le titre, et les 3 titres de scénarios (couleur + flèche par scénario), **sans pourcentages ni question**. Publiée via un tag RSS `<enclosure>` standard sur chaque `<item>` de `feed.xml`, lu nativement par le module RSS de Make (`enclosures`). La routine quotidienne génère l'image et la committe dans `assets/social/instagram/{AAAA-MM-JJ}.png` (voir `docs/routine-prompt.md`, étape technique 8). Chaque option de scénario est forcée sur une seule ligne (`white-space: nowrap` + `text-overflow: ellipsis` sur un `<span class="label">`).

### À faire
- Rien.

### Décisions
- **Pas de pourcentages sur l'image** (décision du 7 août, inchangée) : effet teaser vers le lien en bio.
- **Pas la question posée du site sur l'image** (7 août) : restait illisible sur mobile même en grossissant le texte plusieurs fois — le contexte reste porté par `<comments>`/la légende du post, pas par le visuel.
- **`hook` n'est jamais un extrait ou un copier-coller de la question posée** : une phrase distincte, écrite spécifiquement pour l'image, plafonnée à ~12 mots et une seule ligne à l'écran. C'est ce qui la distingue de la tentative rejetée le 7 août (la question posée fait souvent 30-45 mots).
- **Garde-fou de troncature** conservé malgré le retour en arrière sur les tailles : un label trop long tronque proprement avec `…` plutôt que de passer à la ligne et casser l'alignement avec la flèche. Filet de sécurité rarement déclenché en usage normal, pas la norme.

### Historique
- **2026-08-07 [FAIT]** — Pipeline créé, deux choix volontaires posés (pas de pourcentages, pas de question). Routine quotidienne mise à jour en conséquence. Route Buffer → Instagram branchée sur le scénario Daily (voir B024).
- **2026-08-11 [FAIT] — accroche courte (`hook`) réintroduite sous le titre, sans reproduire l'échec du 7 août.** Constat de l'utilisateur sur la publication du 11 août : Instagram est un usage très rapide, personne ne lit la légende ni ne clique le lien en bio, donc le visuel seul (titre + 3 scénarios sans contexte) reste trop abstrait pour comprendre l'enjeu au premier regard. Testé avant validation par rendu réel recadré à la taille d'affichage mobile (~350px de large dans le fil Instagram, pas seulement le PNG 1080×1080 plein format) — lisible sans problème à cette taille. Ajouté aux deux gabarits (`instagram-photo-template.html` : sous le titre, `.hook` 36px doré ; `instagram-template.html` : même principe à 44px, cohérent avec les tailles plus grandes de ce gabarit) et au script (nouveau champ `hook` du JSON, erreur explicite si absent alors que le gabarit l'attend). Documenté dans `docs/routine-prompt.md`, étape technique 8.
- **2026-08-11 [FAIT] — rééquilibrage des tailles de texte sur le gabarit avec photo**, retour utilisateur juste après l'ajout de l'accroche. Trois allers-retours : le titre paraissait trop discret (ratio titre/masthead de seulement 1,4× sur ce gabarit contre 1,8× sur le gabarit sans photo — la hiérarchie visuelle ne mettait pas assez en avant l'élément censé accrocher le regard) ; puis les 3 options de scénario paraissaient trop petites une fois le titre agrandi à 96px ; puis retour final demandant une taille plus petite pour limiter le recours au tronquage et réduire un peu le titre. **Valeurs finales** : titre 80px→88px, texte des options 29px→31px, flèches 32px→34px. Vérifié par rendu réel (titre court du jour + un label de scénario volontairement bien trop long). Même garde-fou de troncature ajouté au gabarit sans photo par cohérence, sans changer ses tailles de police (déjà plus grandes : 40px/44px).

---

## B027 — Image du sujet par photo libre de droits (Pexels, Pixabay dormant)

**Statut:** FAIT
**Priorité:** P1
**Dernière MAJ:** 2026-08-19
**Prochaine action:** Aucune. Si Pexels redevient inaccessible durablement, réactiver Pixabay (`--source pixabay`, déjà codé et testé)
**Blocage:** Aucun — blocage réseau `images.pexels.com` constaté intermittent, pas permanent

### État actuel
**Pexels est la seule source active par défaut** de `fetch_topic_image.py`, via API officielle uniquement. En cas d'échec Pexels (recherche ou tous les téléchargements), la routine principale retombe **directement** sur la photo par défaut du registre (`assets/social/pub-photos/{registre}.jpg`) — même repli que pour la vignette d'archive et le point 9 de l'Inspecteur — plutôt que de publier sans image. **« Ceinture et bretelles »** : la routine principale applique ce repli en premier (`docs/routine-prompt.md`, étape « Image du sujet », point 4) ; le point 9 de l'Inspecteur (`docs/routine-inspection-prompt.md`) reste en filet de sécurité redondant. **Pixabay reste dormant** : implémentation complète et testée (`--source pixabay`, `PIXABAY_KEY`), gardée au cas où, mais plus appelée automatiquement. Une photo retenue alimente `og:image`/`twitter:image`/le champ `image` du JSON-LD (au lieu de `og-image-v2.png`), l'image Instagram composite, et le corps de l'article (voir B076).

### À faire
- Rien de bloquant. *Note de cohérence à vérifier* : une ligne du 9 août listait encore comme « reste à faire une fois testé » le branchement du fichier obtenu dans `feed.xml` (`<enclosure>`) et dans les meta `og:image`/`twitter:image`/JSON-LD `image`, « à faire à la main la première fois » — alors que le même jour la routine automatique était décrite comme mettant déjà à jour ces valeurs. Contradiction interne du backlog d'origine, probablement résolue par l'automatisation du 9 août.

### Décisions
- **Principe non négociable posé par l'utilisateur : zéro risque.** Contrainte directe avec la décision du 1er août (« Photo dans les éditions », écartée pour risque de droit d'auteur, voir B111) — même risque ici, potentiellement pire (posts sociaux publics).
- **Sources limitées aux banques explicitement libres de droits, usage commercial autorisé sans ambiguïté** : **Pexels** retenu en premier, **API officielle uniquement, jamais de scraping** (irait contre leurs conditions d'utilisation, donc un risque même minime). **Wikimedia Commons écarté** (licences mixtes, plus de risque de mal filtrer). **Unsplash** gardé en option pour une éventuelle deuxième source.
- **Mots-clés** : thématiques génériques, de préférence en anglais (catalogue plus riche), français courant accepté en repli — **jamais un nom propre, une marque ou un acronyme isolé** (ex. « Suno », « IA »), qui ne matche aucun tag et sort des résultats hors-sujet ; **jamais le nom d'une personne réelle**, pour ne jamais laisser une photo générique suggérer qu'elle représente un individu précis.
- **Revue visuelle obligatoire avant tout usage** (regarder les candidats) — si rien de pertinent, ne rien utiliser et garder le visuel généré habituel. Reste vrai en routine automatique/sans supervision : c'est l'agent qui exécute la routine qui fait cette revue à ce moment-là, pas un humain en direct — mais « jamais un choix mécanique sur le premier résultat, jamais forcer une photo médiocre » reste non négociable. *(À noter : le prototype OpenRouter de septembre assume explicitement l'inverse, voir B002.)*
- **Recherche sans filtre `orientation`** (bug du 9 août : `orientation=square` écartait une bonne partie du catalogue avant même le classement par pertinence) — le format carré est appliqué après coup au téléchargement, via les paramètres d'image du CDN Pexels (`square_crop_url()`, généralisée en `crop_url(url, w, h)` le 10 août).
- **Décision finale du 19 août : retour à Pexels comme seule source active, pas de bascule automatique vers Pixabay.**
- **Clés API en variables d'environnement, jamais dans le dépôt** (public sur GitHub) : `PEXELS_API_KEY` (compte développeur créé le 8 août), `PIXABAY_KEY` (nom sans suffixe `_API`, utilisé tel quel dans le script).
- **Conditions Pixabay relues avant intégration** : cache 24h obligatoire par requête, pas de requêtes automatisées en masse (« systematic mass downloads not allowed ») — compatible avec 1 recherche/jour max.

### Historique
- **2026-08-08** — Compte développeur Pexels créé par l'utilisateur, clé stockée en variable d'environnement côté Claude Code Remote.
- **2026-08-09 [FAIT] — scripts et garde-fous** : `scripts/social/fetch_topic_image.py` télécharge plusieurs candidats (jamais un choix automatique) dans un dossier temporaire, avec une fiche `credits.json` (photographe, lien Pexels, requête) pour traçabilité, même si la licence Pexels n'exige pas d'attribution ; `scripts/social/use_topic_image.py` ne fait que committer le candidat déjà choisi vers `assets/social/topic-images/{date}.jpg` + provenance.
- **2026-08-09 [FAIT] — incrustation titre + scénarios sur la photo** (retour utilisateur), `scripts/social/instagram-photo-template.html` : au lieu d'une photo nue, le rendu reprend l'identité visuelle du template habituel (logo, titre en gros, 3 scénarios dans un encart noir avec le code couleur vert/bleu/rouge) mais avec la vraie photo en fond plutôt que le dégradé uni, dégradés noirs en haut et en bas pour garder le texte lisible. `generate_instagram_image.py --photo {chemin}` gère l'incrustation (photo encodée en data URI, injectée via `__PHOTO_SRC__`) — **strictement rétrocompatible**, le comportement par défaut sans `--photo` reste identique au pixel près.
- **2026-08-09 [FAIT] — branché sur la routine quotidienne automatique** (`docs/routine-prompt.md`, étape technique 8) : tentative de photo Pexels avant de générer l'image Instagram, repli silencieux sur le visuel généré si rien ne convient — jamais bloquant pour la publication.
- **2026-08-09** — Blocage réseau documenté sur `images.pexels.com` depuis cet environnement.
- **2026-08-10** — Étendu avec un second recadrage 16:9 de la même photo pour le corps de l'article (voir B076).
- **2026-08-19 (matin)** — Échec Pexels en routine : 3 timeouts réseau consécutifs, publication sans photo, repli manuel sur la banque de secours (voir `docs/inspection-log.md`, entrée du 19 août). Idée de l'utilisateur : « j'ai l'impression que c'est mieux que Pexels » (à propos de Pixabay).
- **2026-08-19 (faisabilité Pixabay testée)** — Un premier test sans clé valide avait donné un **faux négatif** (403 sur des URLs génériques/non authentifiées, à tort attribué au même blocage réseau que Pexels). Avec une vraie clé fournie par l'utilisateur : recherche (`pixabay.com/api/`) et téléchargement (`pixabay.com/get/..._640.jpg`, `cdn.pixabay.com`) fonctionnent, HTTP 200, vrais JPEG. **Différence clé** : ces domaines ne sont pas bloqués par la politique d'egress de cet environnement, contrairement à `images.pexels.com` — cause probable des échecs répétés en routine. Clé de test utilisée transitoirement en variable shell, jamais commitée (vérifié après coup : absente de tout fichier suivi par git), malgré son caractère « public » précisé par l'utilisateur.
- **2026-08-19 (décision de rôle, puis inversée le même jour)** — D'abord tranché « remplacement, pas filet de secours » : Pixabay en source par défaut (`--source pixabay`), Pexels dormant. **Implémentation** : `fetch_topic_image.py` et `use_topic_image.py` refactorés avec une branche par source. Différences techniques gérées : pas de recadrage à la volée par URL côté Pixabay (contrairement au CDN Pexels) → recadrage carré 1080×1080 et large 1600×900 faits **localement avec Pillow** (`square_crop_local()`/`wide_crop_local()`) depuis un `candidate-N-raw.jpg` conservé par `fetch_topic_image.py` (évite un second téléchargement) ; compte Pixabay standard (pas de « full API access » approuvé) → image la plus grande = `largeImageURL`, plafonnée à 1280px sur son plus grand côté, donc léger upscale pour le 1600×900, masqué en grande partie par le dégradé sombre `.article-image-scrim` ; fiche de provenance adaptée (`source: "pixabay"|"pexels"` dans `credits.json`, `pageURL`/`user`/`user_id` côté Pixabay au lieu de `pexels_url`/`photographer`).
- **2026-08-19 (test éditorial réel Pixabay, échec)** — Mots-clés « cybersecurity election hacking digital », 5 candidats : pipeline technique validé de bout en bout (recherche → téléchargement → recadrage carré), mais **aucun des 5 candidats utilisable** — photomontages stock clichetés (cadenas flottants, texte « CYBER SECURITY » incrusté, mains désincarnées touchant un hologramme) ou visages reconnaissables. Catalogue Pixabay visiblement plus chargé en stock clicheté que Pexels sur ce type de requête ; règle de rejet existante (§ « Regarder chaque candidat ») adaptée dans `docs/routine-prompt.md`. Aucun remplacement de l'édition du 19 août (déjà illustrée par la photo Assemblée nationale fournie manuellement par l'utilisateur) — confirme que la revue humaine/agent reste indispensable, encore plus avec Pixabay.
- **2026-08-19 (deuxième test Pixabay, échec)** — Retour utilisateur : préférer des mots-clés « politique » à « sécurité ». Mots-clés « french government politics election », 5 candidats : **les 5 étaient allemands** (Bundestag/Reichstag, urne et bulletin en allemand « Kommunalwahl », drapeau européen sur un bâtiment non identifié), aucun français. Catalogue visiblement biaisé vers du contenu allemand sur des requêtes politiques génériques en anglais (probable surreprésentation de contributeurs germanophones). **Enseignement retenu** : sur un sujet franco-français, préférer des mots-clés qui nomment un symbole français identifiable (« french parliament », « french flag government », « paris landmark government ») plutôt que des mots-clés génériques — et vérifier le drapeau/la langue visible sur chaque candidat, pas seulement la pertinence thématique de surface.
- **2026-08-19 (après-midi, retest Pexels)** — Recherche (`api.pexels.com`) et téléchargement (`images.pexels.com`, avec et sans paramètres de query) ont fonctionné à chaque essai (3/3, avec le vrai code de `fetch_topic_image.py --source pexels`, pas juste `curl`). Catalogue nettement mieux ciblé : « french national assembly building paris » a renvoyé en tête de vraies photos de l'Assemblée nationale/Palais Bourbon (le même bâtiment que la photo fournie manuellement, sous un autre angle). **Le blocage du 9 août sur `images.pexels.com` n'est donc pas permanent — plutôt intermittent** (cause exacte non identifiée : throttling ponctuel côté Pexels/Cloudflare ? variation de la politique d'egress selon les sessions ? — seulement le constat empirique d'un échec le matin puis 3 succès l'après-midi).
- **2026-08-19 (décision finale)** — Retour à Pexels par défaut, repli direct sur la photo du registre, Pixabay dormant.

---

## B028 — Image Instagram pour le récap hebdomadaire

**Statut:** ABANDONNÉ
**Priorité:** —
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune
**Blocage:** —

### État actuel
Écarté le 8 août. `feed-weekly.xml` reste sans `<enclosure>`, pas de route Buffer/Instagram sur ce scénario Make.

### À faire
- Rien.

### Décisions
- Le gabarit existant (titre + 3 scénarios d'**un seul** sujet) ne colle pas au format weekly (7 sujets différents) : demanderait une vraie refonte visuelle pour un gain d'engagement plus faible (1×/semaine vs 1×/jour).
- Le weekly a déjà une distribution sociale sans image dédiée (Telegram/LinkedIn/X via Buffer, ajoutée le 6 août — voir B110).
- *À ne pas confondre avec* les vignettes Instagram **des éditions quotidiennes** affichées **dans la page** du récap hebdo, qui ont bien été faites le 11 août (voir B050).

### Historique
- **2026-08-08** — Envisagé un temps, abandonné après discussion.

---

## B029 — Abonnement quotidienne + hebdo en une seule fois (metadata Buttondown)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-07
**Prochaine action:** Aucune. Cas non testé restant : se désabonner d'une seule formule en resoumettant le formulaire
**Blocage:** Aucun

### État actuel
Un seul formulaire sur `newsletter.html` (section « S'abonner », juste après le hero, avant les deux blocs explicatifs quotidienne/hebdo), avec deux cases à cocher : `<input type="checkbox" name="metadata__quotidien" value="oui" checked>` et `<input type="checkbox" name="metadata__hebdo" value="oui">`. « Quotidienne » pré-coché par défaut (format historique/principal), « Hebdo » à cocher explicitement. Les deux Automations RSS-to-email filtrent sur `metadata.quotidien == "oui"` / `metadata.hebdo == "oui"`, et les abonnés existants ont été migrés — **bug entièrement réglé, formulaire, Automations et base d'abonnés alignés de bout en bout**.

### À faire
- **Point de vigilance non vérifié** : une case décochée n'envoie rien du tout (pas de `metadata__hebdo=non`, juste l'absence du champ) — donc si un abonné qui avait déjà `metadata__hebdo=oui` resoumet le formulaire avec seulement « Quotidienne » coché, il n'est pas garanti que Buttondown efface l'ancienne valeur (un champ omis peut être ignoré plutôt qu'interprété comme « à vider », selon leur implémentation). Pour l'usage principal (première inscription, ou ajouter une deuxième formule) ça fonctionne très bien ; le cas « se désabonner d'une seule formule » reste à tester/confirmer.

### Décisions
- **Deux clés metadata différentes** (`quotidien` et `hebdo`) au lieu d'une seule clé à valeur unique (`subscription_type`) : cocher les deux soumet `metadata__quotidien=oui&metadata__hebdo=oui` en une seule requête, et chaque clé est indépendante côté Buttondown, aucune ne peut écraser l'autre. HTML gère nativement les cases décochées (absentes du POST), aucun JS requis.

### Historique
- **2026-08-07 (bug trouvé)** — Les deux formulaires séparés de `newsletter.html` utilisaient `<input type="hidden" name="metadata__subscription_type" value="...">` — un champ **metadata** Buttondown à valeur unique par abonné. Un même email qui s'inscrivait d'abord à la quotidienne (`metadata__subscription_type=quotidien`) puis à l'hebdo (`=hebdo`) voyait la seconde valeur écraser la première, alors que la page promettait explicitement de pouvoir s'abonner aux deux.
- **2026-08-07 [FAIT] — fix appliqué** : un seul formulaire, deux cases à cocher, deux clés metadata.
- **2026-08-07 [FAIT, côté Buttondown]** — Les deux Automations RSS-to-email configurées pour filtrer sur les nouvelles clés, confirmé par l'utilisateur.
- **2026-08-07 [FAIT]** — Migration des abonnés existants qui n'avaient que l'ancien `metadata.subscription_type` vers `metadata.quotidien`/`metadata.hebdo`, confirmée par l'utilisateur.
- **2026-08-08** — La rubrique « À vérifier » du backlog d'origine est devenue vide à cette date : son dernier point ouvert, le filtrage Buttondown quotidien/hebdo, est résolu par ce ticket.

---

## B030 — Widget Telegram embarqué sur le site

**Statut:** ABANDONNÉ
**Priorité:** P2 à l'origine
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune ; le lien « Rejoindre le canal Telegram » reste la seule option sur `newsletter.html`
**Blocage:** Telegram bloque l'affichage de `t.me/s/*` en iframe depuis un site tiers

### État actuel
Tenté puis retiré immédiatement le 8 août. Essayé via `<iframe src="https://t.me/s/scenario_fr">`, la page publique du canal — supposée faite pour ce genre d'intégration d'après plusieurs tutoriels tiers. **Confirmé en prod par l'utilisateur : « t.me n'autorise pas la connexion »** — Telegram envoie un en-tête (`X-Frame-Options` ou CSP `frame-ancestors`) qui bloque l'iframe. Retiré immédiatement (mieux vaut rien qu'une icône d'erreur visible à chaque visiteur).

### À faire
- Rien. Alternatives connues pour une éventuelle prochaine tentative, aucune aussi simple que l'idée de départ (voir Décisions).

### Décisions
- Le vrai widget officiel Telegram (`telegram-widget.js`, `data-telegram-post="canal/id"`) n'affiche **qu'un seul post fixe par son ID**, pas un flux des derniers posts en direct — il faudrait choisir 1-3 posts à la main et mettre à jour l'ID régulièrement (perd l'aspect « automatique »).
- Services tiers (SociableKit, Elfsight, Common Ninja...) : proxient le contenu Telegram sur leur propre domaine pour contourner le blocage, mais payants/limités en gratuit — contredit l'exigence « statique/gratuit » du projet.

### Historique
- **2026-08-08** — Tenté, bloqué, retiré, alternatives listées.

---

## B031 — Groupe de discussion Telegram lié au canal

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-04
**Prochaine action:** Prévoir une présence de modération humaine occasionnelle une fois que le groupe aura du trafic
**Blocage:** Aucun

### État actuel
Jusqu'au 4 août le canal était en diffusion pure, aucune interaction possible côté lecteur. Un groupe dédié « Scenario - Discussion » a été créé et lié au canal `@scenario_fr` via Telegram (Gérer le canal → Discussion → Add), **100 % côté app Telegram, rien à toucher côté code/routine**. Chaque post affiche désormais un compteur de commentaires qui renvoie vers un fil dédié dans ce groupe.

### À faire
- Modération humaine occasionnelle quand le groupe aura du trafic — **coût récurrent**, contrairement aux autres tâches de ce backlog qui sont ponctuelles.

### Décisions
- Vérification faite via la prévisualisation web publique `t.me/s/scenario_fr` plutôt que l'API bot (plus simple, pas besoin de token).

### Historique
- **2026-08-04 [FAIT]** — Groupe créé et lié. **Point à noter** : la liaison ne s'applique qu'aux posts publiés *après* le lien — pas de rétroactivité automatique confirmée sur les posts antérieurs au 4 août, contrairement à ce qui était supposé au départ.

---

## B032 — Teaser du registre du lendemain sur l'édition

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-04
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
« 📅 Demain : 🇫🇷 actualité française » sous les boutons de partage — `index.html`, `#tomorrow-teaser`. Calculé 100 % côté client en JS à partir de la date du jour + 1 (heure de Paris).

### À faire
- Rien.

### Décisions
- **Correction d'estimation** : contrairement à ce qui était noté au départ, ça ne nécessite **pas** de toucher la routine — la grille des registres est fixe par jour de semaine (lundi géopolitique, mardi carte blanche...), donc calculable côté client, exactement comme les boutons de partage et le temps de lecture.

### Historique
- **2026-08-04 [FAIT]** — Implémenté et testé avec Playwright.
- *Note* : le mapping JS des jours a été modifié deux fois le 12 août (voir B070 et B071), sans retrofit sur les archives déjà publiées.

---

## B033 — Brief audio quotidien (TTS)

**Statut:** À FAIRE
**Priorité:** P3
**Dernière MAJ:** 2026-08-10
**Prochaine action:** À explorer si le reste du backlog P1/P2 est traité — pas urgent
**Blocage:** Aucun

### État actuel
Idée non chiffrée, issue du brainstorm « out of the box » demandé par l'utilisateur le 10 août. Le format (question + 3 scénarios + probabilités) se prête bien à un résumé audio très court (60-90 secondes), généré automatiquement par synthèse vocale et distribué en `<enclosure>` audio dans un flux — même mécanisme que celui déjà utilisé pour les images dans `feed.xml`, juste un autre type de fichier. Ouvrirait un canal (trajet, assistant vocal) que peu de petits médias exploitent.

### À faire
- Choisir un outil TTS (coût, qualité de voix française).
- Écrire le script de génération.
- Décider où l'héberger / le référencer.

### Décisions
- Aucune.

### Historique
- **2026-08-10** — Idée notée (brainstorm « out of the box »).
- **2026-08-20** — Réapparue dans un audit LLM externe (voir B065) ; non redupliquée, renvoi vers cette entrée.

---

## B034 — Image en tête de la newsletter Buttondown

**Statut:** EN TEST
**Priorité:** P3
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Vérifier passivement sur l'édition du 12 août (premier item réellement neuf) si l'image apparaît dans le vrai email envoyé ; si l'aperçu Buttondown lui-même ne montre rien, l'utilisateur contactera le support Buttondown
**Blocage:** Impossible de tester sans risque tant qu'un item réellement neuf n'a pas été envoyé ; aucun résultat consigné après le 11 août dans ce backlog — **statut réel à confirmer**

### État actuel
Techniquement en place, **jamais vérifié en conditions réelles**. Deux méthodes appliquées, les deux sans aucun affichage : (1) balise `<img>` en tête du CDATA de `<description>` dans `feed.xml` (voir `docs/routine-prompt.md`, étape technique 8), pointant vers la même URL que l'`<enclosure>` Instagram ; (2) tag `{{ item.enclosure }}` dans le **template RSS-to-email** dédié. Les deux donnant exactement le même résultat nul (aucune trace, pas même une icône cassée), l'hypothèse de départ est renforcée : cause commune en amont (item déjà traité par Buttondown avant les deux correctifs), pas un problème de syntaxe.

### À faire
- Vérification passive à la prochaine édition réellement nouvelle.
- Si toujours absente malgré un item neuf, revoir l'hypothèse : sanitizer HTML côté Buttondown qui retirerait les balises `<img>` du contenu RSS, ou restriction sur les domaines d'images autorisés.

### Décisions
- **Ne pas fabriquer un faux item pour forcer un test** : cela aurait envoyé un vrai email de test aux vrais abonnés — écarté pour ce risque.
- **Bonne variable : `{{ item.enclosure }}`** (l'URL directement, pas un objet — `item.enclosure.url` n'existe pas, d'où l'échec du tout premier test).
- **Bon emplacement : le template RSS-to-email dédié** (écran distinct, propre au flux), pas l'éditeur du corps d'un email ponctuel testé initialement.

### Historique
- **2026-08-11 (matin)** — Balise `<img>` ajoutée dans le CDATA. Impossible de tester : l'item du jour (`guid scenario-2026-08-11`) avait déjà été traité et envoyé par Buttondown avant l'ajout — modifier le contenu d'un item déjà traité ne déclenche pas de nouvel envoi, Buttondown semblant se fier au `<guid>` pour détecter la nouveauté, pas au contenu présent dans le flux à l'instant T. Piste alors non vérifiable depuis cet environnement, `docs.buttondown.com` et `buttondown.com` étant bloqués par le réseau.
- **2026-08-11 (après-midi)** — `docs.buttondown.com` exceptionnellement accessible depuis la session : doc officielle consultée, deux corrections apportées (variable et emplacement). Correctif appliqué par l'utilisateur au bon endroit avec la bonne syntaxe — **toujours rien affiché**. **Confirmé par l'utilisateur** : l'édition du 11 août était bien déjà partie avant les deux essais.

---

## B035 — Image sur les posts du circuit RSS SUIVI (`feed-suivi.xml`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-12
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Le circuit RSS SUIVI est entièrement câblé (image + texte) sur les 4 réseaux, aligné avec le circuit Daily. Côté flux : `<enclosure>` présente sur les items de `feed-suivi.xml`, pointant vers `assets/social/topic-images/suivi-{sujet}.jpg` (taille réelle des fichiers, jamais inventée) ; `docs/routine-detection-prompt.md` mis à jour pour que les prochaines mises à jour incluent systématiquement cette balise. Côté Make : module LinkedIn 22 (`CreateTextShare`) remplacé par le module **54** (`CreateCompanyImagePost`, `method: link`, même recette que le module 53 du Daily) ; modules Facebook (33) et X/Twitter (24) passés en `useMedia: true` avec `{{30.enclosures[].url}}` ; nouveau module Instagram (**56**, même profil que le module 34) ajouté. Blueprint resynchronisé dans `assets/make/scenario-daily.blueprint.json`.

### À faire
- Rien.

### Décisions
- **Réutiliser la photo dédiée de la page de suivi** (`assets/social/topic-images/suivi-{sujet}[.jpg/-wide.jpg]`, voir B114) plutôt que l'image de l'édition d'origine (`assets/social/instagram/{date d'origine}.png`) — décision du 11 août révisée le 12 août : le plan initial supposait qu'une image Instagram de l'édition d'origine existe toujours, ce qui est faux pour les deux suivis d'alors (la génération d'image Instagram n'existe que depuis le **7 août**, et Spider-Man (18 juillet) comme FIFA (6 août) sont antérieurs). Un seul visuel par sujet suivi plutôt que deux qui pourraient diverger, et déjà visible sur la page elle-même.

### Historique
- **2026-08-11 (trou structurel repéré)** — En vérifiant le blueprint ré-exporté : le module LinkedIn de la branche RSS SUIVI (id 22) tentait de mapper `media.title`/`media.description` mais laissait `media.thumbnail: {}` vide, sans aucun module en amont pour aller chercher une image — contrairement à la branche quotidienne passée à `CreateCompanyImagePost` (voir B022). Résultat : **tous** les posts LinkedIn « 🔄 Un sujet suivi vient d'être mis à jour » partaient sans photo, systématiquement. Cause racine : `feed-suivi.xml` ne portait aucun `<enclosure>` (confirmé le 8 août : « pas demandé, laissé tel quel »).
- **2026-08-12 [FAIT côté dépôt]** — `<enclosure>` ajoutée aux deux items existants de `feed-suivi.xml` ; gabarit d'item mis à jour ; `docs/routine-detection-prompt.md` mis à jour.
- **2026-08-12 [FAIT côté utilisateur dans Make.com, clôturé]** — Modules 54/33/24/56 comme décrit ci-dessus, confirmé via le blueprint ré-exporté.
- **2026-08-12 — 3 erreurs de texte repérées dans cet export, corrigées (2 dans un second export, 1 dans un troisième)** :
  1. ✅ **Module 54 (LinkedIn RSS SUIVI)** : le lien `{{30.url}}` était en 2ᵉ ligne, derrière l'accroche — recréait le bug de troncature LinkedIn corrigé sur le module 53 (lien caché derrière « …voir plus » s'il n'est pas sur la toute première ligne d'un post Image). Remonté en première ligne, confirmé dans le second export.
  2. ✅ **Module 53 (LinkedIn Daily)** : `/` littéral parasite juste avant `{{4.source.title}}` retiré, confirmé dans le second export. Bonus : `{{4.author}}` (toujours vide, aucune balise `<author>` dans `feed.xml`) a aussi disparu du module 32 (Facebook Daily).
  3. ✅ **Module 56 (Instagram RSS SUIVI)** : `text` et `media.description` passés de `{{30.source.title}}` (champ inexistant — `feed-suivi.xml` n'a jamais porté de balise `<source>`, contrairement à `feed.xml`) à `{{30.comments}}`, comme les modules 23/24/33. Confirmé dans un 3ᵉ export.

---

## B036 — Fenêtre de dates « hier uniquement » sur les modules RSS de Make

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune (le fix était à appliquer à la main dans Make sur les modules 30 et 58 ; seul le champ `Date to` change)
**Blocage:** Aucun

### État actuel
Sur les deux modules `rss:ActionReadArticles` (RSS SUIVI id **30**, RSS PUB id **58**) : `filterDateFrom` = `{{parseDate(formatDate(addDays(now; -1); "YYYY-MM-DD"); "YYYY-MM-DD")}}` (minuit hier) et `filterDateTo` = `{{parseDate(formatDate(now; "YYYY-MM-DD"); "YYYY-MM-DD")}}` (minuit aujourd'hui) — soit exactement les 24h de « hier » en entier.

### À faire
- Rien.

### Décisions
- **C'est la fenêtre de dates qui empêche la republication** : ces modules n'ont pas de mémoire entre deux exécutions (contrairement à un trigger « Watch »).
- **Repli « hier + aujourd'hui » testé mais écarté** : avec « Maximum number of returned items » = 1, un item resterait éligible sur 2 exécutions consécutives.

### Historique
- **2026-08-15 [FAIT puis CASSÉ par le même changement]** — Généralisation de la fenêtre « hier uniquement » : `filterDateFrom` **et** `filterDateTo` mis à la **même** formule (les deux bornes sur la veille).
- **2026-08-15 (bug)** — Les deux champs avec la même formule donnent la **même valeur exacte** (minuit hier, à la milliseconde près) : un intervalle de largeur nulle, pas une journée. Comme la comparaison porte sur un vrai datetime et que le `pubDate` réel d'un item RSS a toujours une heure (ex. `20:00:00 +0200`, jamais `00:00:00`), **aucun item ne pouvait matcher** : le filtre bloquait silencieusement tout, sur RSS SUIVI comme RSS PUB. Repéré via le module inspector Make (les deux champs affichaient très visiblement la formule identique), **pas** via un item manquant en sortie — modules bien « stoppés » (0 item), pas en erreur.
- **2026-08-15 (fix)** — `filterDateTo` seul passe de `addDays(now; -1)` à `now` (on retire juste le `-1`), ce qui restaure l'effet voulu (filtre anti-répétition sur la veille) sans revenir à l'ancien souci de fenêtre glissante ouverte (voir B118 pour l'historique de cette fenêtre glissante).

---

## B037 — Branche « RSS PUB » dans le scénario Make Daily

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
6e branche du Router principal du scénario Daily (après un délai de 120s, module **57**) : lit `feed-pub.xml` (module **58**, fenêtre « hier uniquement », voir B036) et distribue vers **X (Buffer, module 61), Facebook (`facebook-pages:CreatePostWithPhotos`, module 71), LinkedIn (natif, module 63) et Instagram (Buffer, module 64)** — plus Bluesky (module 83, voir B014) et Threads (module 255, voir B003) ajoutés ensuite. **Pas de branche Telegram** pour cette catégorie. Les 4 branches d'origine sont programmées **~6h après le déclenchement** (`dateScheduled`/`date` = `{{addHours(now; 6)}}` sur les modules 61/64/71 + Publish date natif pour Facebook). Blueprint resynchronisé (3 exports successifs le 15 août, le dernier fait foi).

### À faire
- Rien.

### Décisions
- **Pas de Telegram sur les posts « pub »** — cohérent avec `docs/routine-pub-prompt.md`, qui ne mentionne jamais Telegram pour cette catégorie.
- **Publication décalée de 6h** pour éviter que le post « pub » (quand il y en a un) n'arrive groupé avec le post quotidien à la même heure — objectif direct de la discussion du 15 août sur l'étalement des publications.

### Historique
- **2026-08-15 [FAIT]** — Branche créée. `feed-pub.xml` a donc désormais un vrai canal de diffusion automatisé, ce qui n'était pas le cas jusque-là (le fichier existait mais rien ne le consommait).
- **2026-08-15 (coquille corrigée)** — Le module 71 (Facebook) était resté à `addHours(now; 3)` (copié depuis la branche RSS SUIVI) au lieu de `6` comme ses voisins X/Instagram — repéré à la relecture du blueprint, corrigé côté Make et confirmé dans l'export suivant.

---

## B038 — Bug du bouton notifications : faux positif OneSignal

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Question laissée à l'utilisateur, **pas encore tranchée** : faut-il corriger le même bug dans les 3 archives déjà publiées (`archives/2026-08-19.html`, `2026-08-20.html`, `2026-08-21.html`) malgré la règle « jamais remodifiée après publication » ?
**Blocage:** Aucun

### État actuel
Corrigé dans `index.html` (page vivante, écrasée chaque matin — le correctif se propage donc automatiquement aux prochaines éditions). **Confirmé résolu par l'utilisateur** après un test réel (vidage des données de l'app + nouvelle acceptation de la permission → notification de test bien reçue). `updateBtn()` vérifie désormais `PushSubscription.optedIn` en premier ; si la permission est accordée mais l'abonnement absent, il appelle lui-même `PushSubscription.optIn()` sans redemander la permission (label « Finalisation de l'abonnement… » pendant l'opération) ; un listener `PushSubscription.addEventListener("change", updateBtn)` a été ajouté en plus du `permissionChange` déjà présent.

### À faire
- Trancher le cas des 3 archives publiées avec le bug (correctif technique, donc discutable comme exception à la règle des archives figées).

### Décisions
- Corriger uniquement `index.html` : la propagation se fait d'elle-même via la recopie quotidienne du gabarit.

### Historique
- **2026-08-21 (symptôme)** — Retour utilisateur : « j'ai rien reçu ce matin ». Le bouton se verrouillait sur un faux positif (« Notifications activées ✓ ») sans jamais créer d'abonnement OneSignal réel.
- **2026-08-21 (diagnostic par élimination)** — `docs/notif-log.md` montrait l'envoi du jour rejeté par l'API OneSignal (`All included players are not subscribed`, 0 abonné malgré 2 players enregistrés) ; côté utilisateur, permission navigateur bien accordée (vérifié pas à pas : Android Chrome, réglages du site, réglages Android) sans que ça change quoi que ce soit côté OneSignal.
- **2026-08-21 (cause)** — Dans `index.html`, la fonction `updateBtn()` du bloc `OneSignalDeferred` ne vérifiait que `OneSignal.Notifications.permission` (permission **navigateur**) pour afficher « ✓ activées » et désactiver le bouton — jamais `OneSignal.User.PushSubscription.optedIn` (abonnement **OneSignal** réel, qui nécessite un appel explicite à `PushSubscription.optIn()`). Un utilisateur ayant accordé la permission autrement que via un clic sur ce bouton précis (ex. directement dans les réglages du navigateur, comme ici) se retrouvait avec un bouton verrouillé en faux « ✓ », sans abonnement créé, sans moyen de relancer puisque le bouton était désactivé.
- **2026-08-21 [FAIT]** — Correctif appliqué et confirmé résolu.
---

## B039 — Temps de lecture estimé sous le titre

**Statut:** EN COURS
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-04
**Prochaine action:** Synchroniser manuellement le prompt de la routine quotidienne réelle pour le volet email (voir B108) — pas encore fait côté trigger réel au moment de l'écriture de l'entrée d'origine
**Blocage:** Dépend de la synchronisation manuelle du prompt (B108)

### État actuel
Deux volets :
- **Site : fait et en ligne.** 100 % client (`index.html`, même script que `.pubdate`) — compte les mots de `.dek`/`.why`/`dd`, 200 mots/minute, arrondi, minimum 1 min. Aucune sync routine nécessaire.
- **Email (`feed.xml`) : la même valeur doit apparaître dans la description envoyée par Buttondown.** Texte statique dans un email, donc calculée par la routine (`docs/routine-prompt.md`, commande `grep`+`wc -w` sur `archives/{date}.html`, même méthode que le JS du site pour que les deux chiffres correspondent toujours). **Nécessite la synchronisation manuelle de la routine quotidienne réelle** — statut réel à confirmer aujourd'hui.

### À faire
- Confirmer/effectuer la synchronisation du prompt live pour le volet email.

### Décisions
- Même méthode de comptage des deux côtés (200 mots/min) pour que le chiffre du site et celui de l'email ne divergent jamais.

### Historique
- **2026-08-04 [FAIT côté site]** — Implémenté, en ligne. Volet email documenté dans le prompt mais pas encore synchronisé côté trigger réel.

---

## B040 — Sommaire ancré en haut de chaque édition

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune. Suite prévue par l'utilisateur mais **pas encore faite** : fusionner les sections Lexique et Sources elles-mêmes
**Blocage:** Aucun

### État actuel
`nav.toc`, juste après les boutons de partage, avec **3 tags définitifs** : `Scénarios` / `L'essentiel` / `Référence`. Padding/gap/taille resserrés pour que les 3 tags tiennent sur une ligne à 390px de large (mobile). Ajouté à `index.html` + `archives/2026-08-08.html`, et à `docs/routine-prompt.md` pour reproduction automatique chaque jour (bloc fixe, jamais de contenu variable). Vérifié visuellement (desktop + mobile 390px) + clic testé via Playwright.

### À faire
- Fusion des sections Lexique et Sources (prévue par l'utilisateur, pas encore faite).

### Décisions
- **Contexte retiré** du sommaire : redondant, juste en dessous du sommaire.
- **Lexique et Sources fusionnés en un seul tag « Référence »**, qui pointe vers `#lexique`, le premier des deux.

### Historique
- **2026-08-08 [FAIT]** — Passé par plusieurs versions le même jour : d'abord 3 ancres (Contexte/Scénarios/Sources), puis Lexique ajouté (oublié dans la première passe), puis Essentiel (5 ancres au total), **puis simplifié en fin de journée à 3 tags** sur retour utilisateur. La version à 5 tags avait déjà le problème de tenue sur une ligne en mobile avant même la simplification.

---

## B041 — Bloc de synthèse « L'essentiel »

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-12
**Prochaine action:** Aucune. Le **nom** « L'essentiel » reste ouvert à ajustement par l'utilisateur
**Blocage:** Aucun

### État actuel
Bloc après les 3 scénarios (`div.cards`), dans `index.html` + les archives à partir du 8 août + `feed.xml`. Contenu : 3-4 phrases en **3 temps distincts et dans cet ordre — problématique / contexte / conclusion** (issue la plus probable + signal concret à surveiller pour basculer vers une autre). Le même texte est repris dans `feed.xml`, dans la balise `<source url="{lien de l'édition}">`, en texte brut. Depuis le 12 août, `.essentiel-box` est découpée en plusieurs `<p class="essentiel-text">` (un par item), et un paragraphe France Impact y a été ajouté (voir B089). Reproduction documentée dans `docs/routine-prompt.md`.

### À faire
- Rien de bloquant ; éventuel renommage du bloc.

### Décisions
- **Placé en bas, après les 3 scénarios, pas en haut** : moins redondant avec `question-box`/`stakes-box` qui font déjà ce travail de cadrage en haut de page, et comble un vrai vide qui n'existait pas (rien ne reliait les 3 scénarios entre eux après lecture).
- **Jamais une répétition des paragraphes `why` des cartes.**
- **Jamais les labels bruts « favorable »/« stable »/« dégradé » dans ce bloc** (corrigé le 8 août, retour utilisateur) : le lecteur ne connaît pas forcément ce que chaque label recouvre pour ce sujet précis, contrairement à quelqu'un qui vient de lire les 3 cartes. Décrire l'issue en langage concret (ex. « le rebond se maintient sur un rythme soutenu » plutôt que « le scénario stable »).
- **Le bloc doit être autonome**, lisible sans avoir lu le reste de l'article (partage, extrait) : d'où la phrase de contexte/problématique en ouverture, et le passage de « 2-3 phrases » à « 3-4 phrases ».
- **Toujours nommer précisément le sujet** dans la phrase de contexte, ne jamais présumer que le lecteur a lu le reste de la page (un sujet vague repéré au premier essai : « la fréquentation » sans préciser de quoi).
- **Libellé « L'essentiel » plutôt que « Conclusion »**, jugé trop tranché pour un site qui pèse 3 issues sans en affirmer une.
- **Balise `<source>` plutôt que `<essentiel>`** dans `feed.xml` (retour utilisateur) : besoin d'une balise normée exploitable dans Make, `<essentiel>` (inventée) risquait de ne pas apparaître au mapping. `<source>` existe dans le spec RSS 2.0 (normalement le flux d'origine d'un item republié), est inutilisée ailleurs dans ce flux, et est détournée ici avec son attribut `url` obligatoire rempli. Le champ « Summary » visible côté Make n'était pas une option valable : juste un alias généré à partir de `<description>`, pas un champ indépendant.

### Historique
- **2026-08-08 (idée)** — Suggérée par un retour externe (« résumé 1 minute en haut d'article »), discutée avec l'utilisateur et **déplacée en bas**.
- **2026-08-08 (corrigé le même jour)** — Interdiction des labels bruts.
- **2026-08-08 (complété le même jour)** — Exigence d'autonomie du bloc, passage à 3-4 phrases.
- **2026-08-08 (retouché une 3ᵉ fois le même jour)** — Structure en 3 temps imposée ; règle de nommage explicite du sujet.
- **2026-08-08 (ajout dans `feed.xml`)** — Même texte en brut dans l'`<item>` du jour, « disponible pour un usage futur côté Make.com », demande explicite de l'utilisateur (« on ne sait jamais »), pas encore branché sur un module à ce moment-là. Balise `<essentiel>` remplacée le même jour par `<source url=...>`.
- **2026-08-11** — Le champ `<source>` devient le teaser de plusieurs posts sociaux (voir B023).
- **2026-08-12** — Découpage en plusieurs `<p class="essentiel-text">` et ajout du paragraphe France Impact (voir B089).
- *Note* : la reproduction quotidienne nécessite le copier-coller manuel habituel dans la routine live (`trig_0176spj7P7E9fyTs1XBkQBWF`, voir B108).

---

## B042 — Page glossaire (`glossaire.html`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-05
**Prochaine action:** Aucune (volet « développer le glossaire » traité en B140)
**Blocage:** Aucun

### État actuel
`glossaire.html` agrège tous les termes des lexiques d'édition au même endroit : recherche texte, filtre par domaine (réutilise la colonne « Domaine » de `docs/tags.md`, mêmes puces de filtre que `archives.html`), tri alphabétique, et un lien « Vu dans : {édition} → » vers l'édition d'origine de chaque terme. Lié à la routine via une **étape 6ter** (`docs/routine-prompt.md`) : purement mécanique, copie conditionnelle du terme+définition déjà rédigés pour le lexique du jour vers `glossaire.html` s'il n'y est pas déjà — aucune nouvelle rédaction, aucun jugement éditorial ajouté. Mentionné avec un lien dans `le-projet.html` (section « Vocabulaire »), référencé dans `sitemap.xml`, et **ajouté au menu principal** de toutes les pages (retour utilisateur le jour même) entre « Archives » et « Le projet ». Testé (recherche, filtre, rendu mobile) via Playwright.

### À faire
- Rien.

### Décisions
- En creusant le sujet, une bonne partie du travail existait déjà sans être documentée : chaque édition a son propre petit lexique en bas de page (`.lex-ref`, `<dl class="glossary">`) avec renvois cliquables depuis le texte, mécanisme déjà décrit dans `docs/routine-prompt.md` avant ce jour. Ce qui manquait était l'agrégation.

### Historique
- **2026-08-05 [FAIT]** — Inspiré d'un exemple brief.eco (lien « Glossaire » dans son footer email). **Rétro-rempli une fois** (script Python ponctuel, pas conservé) à partir des 13 éditions déjà publiées : **77 termes récupérés**, y compris ceux des éditions antérieures au système `.lex-ref` (format `<dt>` sans `id`, slug regénéré depuis le terme).

---

## B043 — Recherche en texte intégral sur `archives.html`

**Statut:** À FAIRE
**Priorité:** P3
**Dernière MAJ:** 2026-08 (non daté précisément)
**Prochaine action:** Aucune planifiée
**Blocage:** Touche la routine quotidienne (plus lourd, plus fragile vu la difficulté de synchronisation déjà rencontrée — voir B108)

### État actuel
La recherche actuelle ne porte a priori que sur les titres/tags, pas le contenu complet des éditions. Pas implémenté.

### À faire
- Générer un index de recherche à la publication — donc toucher la routine quotidienne.

### Décisions
- Aucune.

### Historique
- Entrée notée en P3 dans le backlog d'origine, sans date précise.

---

## B044 — Navigation « édition suivante » en bas de chaque archive

**Statut:** À DÉCIDER
**Priorité:** P3
**Dernière MAJ:** 2026-08 (non daté précisément)
**Prochaine action:** Trancher entre les deux options avant d'implémenter
**Blocage:** Conflit avec la règle « une archive ne se modifie jamais »

### État actuel
Pas implémenté. Le lien « précédente » est toujours facile (le jour d'avant est connu au moment de publier), mais « suivante » obligerait à retoucher l'archive de la veille une fois figée.

### À faire
- Trancher : soit seulement un lien « précédente » (moins complet), soit accepter une exception à la règle des archives figées pour ce cas précis.

### Décisions
- Aucune.

### Historique
- Entrée notée en P3 dans le backlog d'origine, sans date précise.

---

## B045 — Graphiques de séries chiffrées dans le contexte de l'édition

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-08-10
**Prochaine action:** Livrer une v1 simple, bornée aux **indices/indicateurs cotés** déjà cités avec plusieurs valeurs dans le contexte
**Blocage:** Aucun

### État actuel
Pas implémenté. Aujourd'hui le contexte (`.dek`) est uniquement du texte + `indicator-strip` (1-2 chiffres isolés) — pas de vraie visualisation de tendance, alors que ce genre de comparaison apparaît déjà régulièrement en prose (ex. l'édition du 8 août citait 156,79 M / 174,52 M / le plateau 2023-2024 à 181 M — une vraie série chiffrée, racontée en phrase au lieu d'être montrée).

### À faire
- Généraliser le principe déjà utilisé sur le site en un **graphique en barres** (plus adapté que des courbes pour des comparaisons ponctuelles type « par an ») dans le gabarit `index.html`, que la routine alimenterait juste avec un petit tableau `[{label, value}, ...]` — toute la génération SVG restant dans une fonction JS réutilisable.

### Décisions
- **Ne pas réinventer un système** : le site a déjà deux précédents de graphiques SVG générés en JS à partir d'un petit tableau de données — les jauges `.gauge` (arc de cercle par scénario) et surtout `renderEvoChart()` dans `suivi/_gabarit.html`, qui lit un tableau `evoData` et calcule tout le SVG lui-même, sans que la routine ait à faire le moindre calcul de coordonnées.
- **Ne pas rendre ça systématique chaque jour** : seulement quand le contexte contient une vraie série chiffrée comparable (plusieurs points dans le temps ou plusieurs catégories). `indicator-strip` reste approprié pour 1-2 chiffres isolés. Même logique de jugement que pour « L'essentiel » : un outil de plus, pas une case à cocher.
- **Déclencheur précisé le 10 août (retour utilisateur)** : le cas le plus net n'est pas n'importe quelle série chiffrée, c'est un **indice ou indicateur coté suivi dans le temps** — Brent, CAC 40, taux directeur d'une banque centrale, taux de change, inflation — déjà cité avec plusieurs valeurs dans le contexte. Avantage pratique : ses valeurs successives sont déjà extraites et vérifiées pour la rédaction du `.dek`, donc pas de recherche supplémentaire pour construire le tableau. **Bon premier périmètre pour une v1** avant d'élargir.

### Historique
- **2026-08-08** — Idée issue d'un retour externe (revue de Geok).
- **2026-08-10** — Déclencheur précisé, avec l'exemple réel de l'édition du 10 août citant le **Brent** à « 72 dollars en juin, plus de 100 dollars le 23 juillet, environ 84 dollars début août, contre 69 dollars en moyenne sur 2025 ».
- *Voir aussi* B064 : le graphique en escalier pour série historique longue, réalisé le 21 août, est un composant différent (autre type de série, autres critères de déclenchement).

---

## B046 — Cohérence des KPI entre `indicator-strip` et les 3 cartes

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Exactement **2 KPI fixes**, identiques dans les 3 cartes et déjà vus dans `indicator-strip`, au format visuel `.evo-current`/`.evo-arrow`/`.evo-prev` réutilisé du graphique d'évolution des pages de suivi (plus scannable qu'une phrase, utile vu que le lecteur est déjà à ~60 % de la page). Appliqué à `index.html` et `archives/2026-08-08.html` (commit `d5d88d9`), documenté dans `docs/routine-prompt.md`.

### À faire
- Rien.

### Décisions
- Ne plus laisser chaque carte inventer son propre tableau de bord.

### Historique
- **2026-08-08 [FAIT]** — Analyse approfondie demandée par l'utilisateur (« réfléchit deep » sur le fait que les indicateurs des 3 cartes ne semblaient pas cohérents avec les KPI mentionnés plus haut dans l'article). **Bug trouvé** : le 3e indicateur de chaque carte « Indicateurs touchés » était différent d'un scénario à l'autre (chacun sa propre statistique, jamais réutilisée ailleurs) — le lecteur avait l'impression que chaque carte inventait son propre tableau de bord.

---

## B047 — Lisibilité des 3 cartes de scénarios

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-09-02
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Deux passes appliquées. **Structure (8 août)** : le disclaimer « Ordres de grandeur indicatifs, pas des prévisions garanties » est factorisé en une seule footnote sous les 3 cartes (`<p class="indicators-note">`), avec un lien « En savoir plus sur notre méthode » vers `le-projet.html`, sans mention de l'IA ; le paragraphe `why` est scindé en 2 `<p class="why">` consécutifs (le récit factuel, puis la comparaison de probabilité isolée visuellement par un léger séparateur en pointillés). **Tailles et repères visuels (2 septembre)** : `.card .why` 0.92rem → **1.05rem**, `.france-line` 0.88rem → 0.95rem, jauge 108×64 → 132×78px, trait 10px → 12px, pourcentage central 1.35rem → 1.7rem et en couleur `--accent` (au lieu du blanc neutre), `h3` 1.2rem → 1.28rem, plus un filet de couleur de 4px en tête de chaque carte (`border-top`, `--accent`). Aucun changement structurel (mêmes classes, mêmes gabarits `card-head`/`card-body`).

### À faire
- Rien.

### Décisions
- **Diagnostic du 2 septembre** : `.card .why` était plus petit (0.92rem) que le texte de contexte `.dek` juste au-dessus (1.1rem) — le lecteur arrivait aux cartes, le contenu qu'elles existent pour porter, et le texte rétrécissait.
- Filet de couleur en tête de carte pour que favorable/stable/dégradé se distinguent d'un coup d'œil, avant même de lire le mot-repère — même logique que le filet de `.france-line` posé le 17 août (voir B089).
- **Pas de retrofit sur les archives antérieures** (design non rétroactif), conformément à la règle générale.
- Rien à changer dans `docs/routine-prompt.md` au-delà des valeurs déjà recopiées avec le `<style>` chaque matin.

### Historique
- **2026-08-08 [FAIT, 1ʳᵉ passe]** — Deux changements demandés par l'utilisateur à la suite de l'analyse des KPI (voir B046) : « il faut que ça soit plus facile à lire, plus agréable ». Le disclaimer était répété une fois par carte (3 fois au total, en dernier `<li>` de chaque liste d'indicateurs) — pur bruit répétitif, factorisé. Le paragraphe `why` était un seul bloc de 100-180 mots avec la comparaison de probabilité noyée à la fin — mur de texte difficile à parcourir, d'autant que le lecteur y arrive à ~60 % de la page. Appliqué à `index.html` et `archives/2026-08-08.html`, vérifié visuellement (desktop + mobile) via Playwright, documenté dans `docs/routine-prompt.md`.
- **2026-09-02 [FAIT, 2ᵉ passe]** — Retour utilisateur : « la lecture des scénarios est difficile, c'est pas visuel, trop petit ». La passe du 8 août avait traité la structure du texte, pas la taille ni le repère visuel. Vérifié via Playwright (desktop 1280px et mobile 390px). Appliqué à `index.html`, `archives/2026-09-02.html`, `en/index.html` et `en/archives/2026-09-02.html` (édition du jour dans les deux langues).

---

## B048 — Retrait de la ligne `.ai-disclosure` du footer

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
La ligne « 🤖 Recherche et rédaction assistées par l'intelligence artificielle. En savoir plus sur notre méthode → » est retirée de `index.html` et `archives/2026-08-08.html` (paragraphe + CSS associé). **Pas retirée des 15 autres archives déjà publiées**, qui n'ont pas la nouvelle footnote et n'ont donc pas ce doublon (archives figées, pas de raison de les toucher).

### À faire
- Rien.

### Décisions
- Devenue redondante avec la footnote `.indicators-note` ajoutée juste au-dessus le même jour (même lien « En savoir plus sur notre méthode → » vers `le-projet.html`, qui contient de toute façon la mention complète de l'IA dans sa section « Qui fait Scénario »).
- **Rien à changer dans `docs/routine-prompt.md`** : cette ligne n'était jamais mentionnée explicitement dans le prompt, juste héritée du gabarit `index.html` recopié tel quel — sa suppression du gabarit suffit à ce qu'elle disparaisse des prochaines éditions.
- *À ne pas confondre avec* l'obligation de transparence IA elle-même, qui reste en place (voir B125).

### Historique
- **2026-08-08 [FAIT]** — Retrait sur retour utilisateur.

---

## B049 — Bande `.top-updates` : rendre visibles le dernier suivi et le dernier récap hebdo

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Une bande `.top-updates` juste sous la nav (avant le hero), toujours visible sans scroll, avec deux liens texte discrets (même style que les liens `.dek` : gold + soulignement pointillé, pas de pill/bordure) : `🔄 Sujet révisé →` et `🗓️ Récap de la semaine →`.
- Le lien **« Sujet révisé »** est **générique et durable** : il pointe vers `archives.html?tag=revise`. Mécanisme : un tag non thématique `data-tag="revise"` (« Sujet révisé ») ajouté sur les entrées `archives.html` qui portent déjà un `.suivi-badge` (même logique que le tag spécial `hebdo`, capté automatiquement par le JS de filtrage — aucune modif JS nécessaire côté tags) ; un petit script lit `?tag=revise` au chargement d'`archives.html` et applique le filtre + le tri « Dernière mise à jour ». Ce lien pointe donc **toujours** vers le sujet réellement le plus récemment révisé, sans jamais devoir être remis à jour sur `index.html`. Seul entretien requis : ajouter le tag `revise` sur l'entrée concernée au moment de publier une nouvelle version de suivi — geste déjà nécessaire pour poser le `.suivi-badge`.
- Le lien **« Récap de la semaine »** est automatisé depuis le 11 août : la routine hebdo (`trig_01FwX1Q3xsLCMwAZt4WviUA6`, voir `docs/routine-hebdo-prompt.md`) remplace uniquement l'attribut `href` par la page tout juste publiée, `index.html` ajouté à l'étape 5 (git add + push).

### À faire
- Rien. **Piste pour aller plus loin, non demandée** : appliquer au lien hebdo la même approche générique (tag + filtre) que pour `revise` si ça devient gênant — pas nécessaire tant que le rythme reste hebdomadaire. Un oubli ne peut de toute façon produire qu'un lien vers l'avant-dernier récap, jamais un lien cassé.

### Décisions
- Version « pill » initiale abandonnée le soir même (retour utilisateur : trop lourde visuellement) au profit de deux liens texte discrets.
- Lien « Sujet révisé » générique plutôt que pointant vers une page `suivi/{sujet}.html` précise.

### Historique
- **2026-08-08 (constat)** — Un sujet suivi mis à jour (badge 🔄 sur `archives.html`) n'était signalé nulle part sur `index.html` : un visiteur régulier n'avait aucun moyen de le savoir sans déjà connaître le mécanisme et aller chercher le filtre.
- **2026-08-09 [FAIT]** — Implémenté, étendu le même jour (retour utilisateur) au dernier récap hebdomadaire, avec le même besoin de visibilité ; allégé une première fois le même soir. Testé visuellement desktop + mobile (Playwright). Lien « Sujet révisé » rendu générique (idée utilisateur).
- **2026-08-11 [FAIT]** — Lien « Récap de la semaine » automatisé : resté manuel jusque-là, un oubli lors de la publication manuelle du rattrapage du 9 août avait laissé le lien pointer vers l'avant-dernier récap (27 juillet-2 août), repéré par l'utilisateur.

---

## B050 — Vignettes Instagram sur le récap hebdo (grille 2 colonnes + accordéon)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Chaque jour du récap est une `.day-card` dans une grille 2 colonnes (`.week-grid`, repasse à 1 colonne sous 620px). L'image Instagram du jour (1080×1080, déjà générée quotidiennement, voir B026) est affichée en pleine largeur de la carte (`aspect-ratio:1/1`, cliquable vers l'archive) : comme elle contient déjà le titre + les 3 options de scénario sans les pourcentages, elle tient lieu de résumé visuel complet sans texte additionnel. Un bouton « Voir le détail ▾ » ouvre un accordéon (même mécanique CSS `grid-template-rows: 0fr → 1fr` que `.entry-scenarios` sur `archives.html`, dupliquée en local dans chaque carte) révélant la question exacte, les 3 pourcentages et le lien « Lire l'édition → ». **Résultat mesuré sur `hebdo/2026-08-09.html` : hauteur totale de page repliée réduite de ~26 %** par rapport à la V1 (vignette simple), malgré des images bien plus grandes.

### À faire
- Rien.

### Décisions
- **Limite connue, acceptée** : dans la grille 2 colonnes, si une carte se déplie et sa voisine reste repliée, la rangée CSS Grid garde la hauteur de la plus haute — un peu de vide apparaît à côté de la carte repliée. Comportement standard de CSS Grid (pas un vrai masonry), rien de cassé.
- **Image par défaut** (`assets/social/instagram/default.png`, générée une fois via Playwright — logo + baseline « Le futur en 3 scénarios » sur le fond dégradé habituel, sans titre puisque générique) utilisée quand l'image réelle d'un jour manque. Le champ `alt` de l'`<img>` reste toujours le vrai titre du jour même quand l'image est générique, pour l'accessibilité.
- **Rétrofit exceptionnel assumé** : contrairement à la règle « une page hebdo publiée n'est jamais retouchée » (réservée aux changements de contenu éditorial, jamais aux évolutions de présentation), l'utilisateur a explicitement demandé de rétrofiter la page en ligne (`hebdo/2026-08-09.html` + son fragment) plutôt que d'attendre le prochain récap — c'est cette page qui est visible depuis le lien `.top-updates`. `hebdo/2026-08-02.html` (semaine précédente, plus visible nulle part) n'a pas été touché.
- **CSS + JS dupliqués à trois endroits qui doivent rester synchronisés** : `hebdo/2026-08-09.html` (page figée) ; `archives.html` (le fragment hebdo y est injecté dynamiquement dans `.entry-scenarios-inner`, donc `archives.html` porte sa propre copie du CSS `.week-grid`/`.day-card*` et un gestionnaire de clic délégué sur `document` pour `.day-card-toggle`, puisque ces boutons n'existent pas encore au moment où le script s'exécute) ; `docs/routine-hebdo-prompt.md` (instructions + exemples HTML mis à jour pour que la routine du 16 août génère directement ce format — trigger `meta_mcp`, synchronisé via `update_trigger` le jour même).

### Historique
- **2026-08-11 — trois allers-retours sur la même idée de départ** (« mettre l'image de chaque jour, discret, sans allonger la page ») :
  1. Petite vignette carrée (84px) accolée au texte de chaque `.day-block` (image à gauche, texte à droite, `display:flex`). Fonctionnait mais jugé « trop petit vu en plus gros » — rollback demandé vers une vraie mise en page en colonnes.
  2. Vignette agrandie à 160px (110px mobile), toujours accolée au texte de chaque jour empilé verticalement. Meilleur, mais l'utilisateur a proposé une idée différente en cours de route : « que les images qui contiennent le titre etc [...] deux jours par ligne [...] et on clique sur un bouton qui ouvre en accordéon ».
  3. **Design retenu** : grille 2 colonnes + accordéon par carte.
- **2026-08-11 (cas concret de l'image par défaut)** — Les éditions du 3 au 6 août datent d'avant l'existence de la génération d'image Instagram (ajoutée le 7 août), donc `hebdo/2026-08-09.html` (qui couvre le 3-9 août) a 4 jours sur 7 avec l'image par défaut et 3 avec la vraie image — mélange assumé, temporaire par nature (toutes les semaines à partir du 16 août ont 7 vraies images).
- **2026-08-11 (vérification)** — Rendu Playwright desktop/mobile sur les trois fichiers, accordéon imbriqué testé dans le contexte réel de `archives.html` (clic sur « Les 7 jours ▾ » puis sur « Voir le détail » à l'intérieur du fragment chargé), aucune image cassée.

---

## B051 — « Signaux à surveiller » par scénario

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-08-10
**Prochaine action:** Chiffrer : emplacement dans la carte, longueur, cohérence avec les indicateurs déjà présents pour ne pas dupliquer
**Blocage:** Aucun

### État actuel
Pas implémenté. Aujourd'hui chaque carte a des « Indicateurs touchés » (des chiffres déjà mesurés), mais pas de liste explicite et falsifiable écrite au moment de la publication du type « voici ce qui confirmerait ce scénario précis » — différent des pages `suivi/{sujet}.html`, qui réestiment après coup sans grille de lecture pré-écrite.

### À faire
- Chiffrer et implémenter.

### Décisions
- **Intérêt concret, pas cosmétique** : donnerait à la routine de re-vérification matinale (l'Inspecteur, B077) et à la veille hebdo (`docs/routine-detection-prompt.md`, B123) des critères écrits d'avance à vérifier, plutôt que de réestimer à l'aveugle à chaque passage.

### Historique
- **2026-08-10** — Idée issue d'une revue externe ChatGPT du site, filtrée (voir B052 pour le tri de cette revue). Exemple donné pour l'édition du 10 août (Ormuz/croissance) : scénario favorable → réouverture du détroit, Brent < 75 $ ; scénario dégradé → nouvelles attaques, Brent > 120 $.

---

## B052 — Faire comprendre Scénario à un premier visiteur (bandeau d'accueil)

**Statut:** FAIT
**Priorité:** P2 à l'origine (accroche masthead)
**Dernière MAJ:** 2026-08-28
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Un vrai bandeau d'accueil `.intro-banner` avec un texte retravaillé (« L'actu, oui. Et après ? ») et **le logo du site en grand** — le tronc qui se sépare en 3 flèches vert/bleu/terracotta étant déjà, par construction, la représentation visuelle des 3 scénarios. Visible **une seule fois par navigateur** (localStorage, clé partagée par tout le site : vu une fois n'importe où, jamais revu ailleurs), fermeture manuelle possible. `.edition` sorti de `.masthead-right` vers une seconde ligne sous le logo (conservé des itérations précédentes, jamais remis en cause). Déployé sur `index.html`, `archives.html` et les 36 `archives/*.html` existantes — **pas** sur `glossaire.html`/`le-projet.html`/`suivi/`/`hebdo/`. Détail technique dans `docs/routine-prompt.md` (étape technique 3).

### À faire
- Rien.

### Décisions
- **Explicitement pas retenu** : refondre `index.html` en vraie page marketing séparée (hero, « comment ça marche », CTA) — `index.html` **est** l'édition du jour par principe assumé du site ; une vitrine séparée casserait ça pour un gain déjà largement couvert par `le-projet.html` et `archives.html`.
- **Rétrofit assumé sur les archives existantes** : élément de structure, pas de contenu éditorial figé — contrairement aux tickets éditoriaux de l'audit du 27 août (voir B134).
- Portée volontairement plus restreinte que l'accroche texte abandonnée à l'étape 1 (qui, elle, avait couvert 59 pages).

### Historique
- **2026-08-10 (P2, idée d'origine)** — Un primo-visiteur découvre le principe « 1 question → 3 scénarios chiffrés » en lisant l'article du jour, rien ne l'explique avant. Ajouter une phrase courte sous « Scénario » dans le masthead résoudrait ça à faible coût, sans reconstruire la page d'accueil. **Note sur la source de cette idée** : revue complète d'un tiers (ChatGPT) sur le site, challengée avant d'en retenir quoi que ce soit — la majorité de ses propositions (« créer » un logo 1→3, des catégories, un vote Telegram avant résultat, une page « avions-nous raison ») redécouvraient des fonctionnalités déjà en prod (logo actuel, `docs/tags.md`, sondage Telegram natif `sendPoll` sur `@scenario_fr`, pages `suivi/`) — signe qu'elle n'avait exploré que la home + un article. Une proposition (afficher le scénario central tout en haut, avant le contexte) a été explicitement **écartée** : contraire à la tension « deviner avant de savoir » déjà cultivée par le site (bloc « Vote avant de connaître le résultat » + sondage Telegram automatique, justement pensés pour que le lecteur parie avant de lire la résolution).
- **2026-08-28 [FAIT] — trois itérations en session, chacune sur retour utilisateur direct** (déclencheur : « on aime un appart dans les 20 premières secondes sinon on zappe à jamais », un premier visiteur atterrissant sur l'édition du jour ne comprend pas ce qu'est Scénario sans cliquer sur « Le projet ») :
  1. Accroche texte discrète dans le masthead (`.brand-tagline`), à droite du logo/wordmark, reprenant mot pour mot la description du flux RSS — jugée trop faible (« bof c'est moyen non ? »), **retirée le même jour** des 59 pages où elle avait été déployée.
  2. Remplacée par un vrai bandeau d'accueil (`.intro-banner`) — bien plus visible, texte retravaillé (« soit cool mais pro » → « L'actu, oui. Et après ? »), avec 3 pastilles textuelles « Favorable / Stable / Dégradé ».
  3. Pastilles retirées à leur tour (retour utilisateur : « tu répètes », déjà dit une ligne plus bas par les vraies cartes de l'article) et remplacées par le logo du site en grand.
---

## B053 — Prompt de la routine quotidienne allégé de 42 %

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune (la version allégée doit être collée manuellement dans la routine live, voir B108)
**Blocage:** Aucun

### État actuel
`docs/routine-prompt.md` reste la version complète de référence ; c'est une **version allégée** (sans le texte explicatif du haut du fichier ni les dates de correction) qui est collée dans la routine live (`http_api`, toujours copier-coller manuel, pas d'`update_trigger` possible). Résultat : **~17k → ~10k tokens (−42 %)**, vérifié bloc de code HTML/XML par bloc de code HTML/XML (22 blocs au total après la passe du 11 août) pour garantir qu'aucun format ni règle structurelle n'a été perdu.

### À faire
- Rien.

### Décisions
- **Ce qui est retiré du prompt live, gardé ici** : toutes les dates, « retour utilisateur : … » et exemples avant/après purement justificatifs — en ne gardant que la règle opérationnelle finale (format HTML/XML exact, conditions, et les exemples qui enseignent une **calibration**, comme « la taxe cale » → « la taxe reste bloquée », ceux-là gardés). Cet historique était de toute façon déjà dupliqué dans ce backlog.
- **Modèle de la routine (Sonnet) volontairement inchangé** : passer à un modèle moins cher a été écarté — tâche de jugement éditorial non supervisée, publication directe sans relecture humaine, risque de réintroduire des défauts d'écriture déjà corrigés plusieurs fois. Seul le prompt a été optimisé, pas le modèle.
- Existence d'un fichier de rollback : `docs/routine-prompt-rollback-2026-08-11.md`.

### Historique
- **2026-08-09 [FAIT, 1ʳᵉ passe]** — Demandé par l'utilisateur pour réduire le coût en tokens (~17k tokens auparavant, sans aucun cache d'un jour à l'autre puisque la routine repart d'un conteneur neuf chaque matin — donc facturé en entier tous les jours). `docs/routine-prompt.md` gardait, pour chaque correction ajoutée au fil des semaines, son historique complet — utile pour un humain qui relit le fichier, pas nécessaire à l'agent qui exécute la routine (qui a besoin de la règle finale, pas du récit).
- **2026-08-11 [FAIT, complété]** — La première passe avait été construite avant l'ajout de la bande `.top-updates` (B049), de l'exception `.dek-list` (B057) et de l'image dans le corps de l'article (B076) ; un rebase l'a révélé (conflit contre `main`, qui avait avancé entre-temps). La passe corrigée réintègre les trois règles, toujours vérifiée bloc de code par bloc de code (22 blocs) contre la version complète.

---

## B054 — Mettre davantage en avant les sujets suivis sur `archives.html`

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-08-29
**Prochaine action:** Comparer plusieurs variantes visuelles avant de choisir — ne pas se contenter d'un seul essai
**Blocage:** Aucun

### État actuel
Le `.suivi-badge` existant (voir B049) fait déjà le travail fonctionnel (repérer et filtrer les sujets révisés), mais reste visuellement discret — un petit pill texte + emoji 🔄, au même niveau que le reste de la carte d'archive, qui ne saute pas aux yeux dans la liste. Aucune piste tranchée.

### À faire
Pistes à explorer au moment de traiter ce ticket (aucune tranchée) :
- Une icône dédiée plus dessinée (SVG, cohérente avec le reste des icônes du site) plutôt que l'emoji 🔄 actuel.
- Un repère visuel sur la carte elle-même (ex. un liseré/pastille de coin) en plus du badge texte, pour qu'un sujet suivi se distingue au premier coup d'œil sans avoir à lire le badge.
- Ou un simple traitement graphique plus marqué du badge existant (icône plus grande, meilleur contraste) sans toucher à sa taille de police ni à sa couleur dominante.

### Décisions
- **Consigne explicite de l'utilisateur pour le calibrage : pas une grosse couleur, pas un énorme badge** — juste quelque chose d'assez visuel, porté par une icône, sans que ça devienne criard ou lourd dans la liste.
- Méthode : comparer plusieurs variantes visuelles, comme pour le format des cartes de scénarios le 28 août.

### Historique
- **2026-08-29** — Ticket ouvert sur retour utilisateur.

---

## B055 — Mémoriser la langue de lecture choisie par le lecteur (FR/EN)

**Statut:** À FAIRE
**Priorité:** P3 (validée P3 le 30 août 2026)
**Dernière MAJ:** 2026-08-30
**Prochaine action:** Aucune planifiée — utilité réelle encore faible tant que la couverture EN est limitée
**Blocage:** Le vrai coût est le déploiement sur toutes les pages d'un site statique, pas la logique

### État actuel
Pas implémenté. **À ne pas confondre avec la détection automatique de langue navigateur, explicitement écartée le 29 août** (`docs/strategie-anglais.md` § « UX de bascule entre langues » : « pas de détection de langue navigateur, pas de redirection automatique — le bouton offre un accès direct, jamais un choix imposé ») — cette règle vise un nouveau visiteur qu'on redirigerait de force sans qu'il ait rien demandé, le français devant rester la langue par défaut. Ce ticket est différent : mémoriser un choix **explicite** déjà fait par le lecteur (clic sur `.masthead-lang-btn`), pour le réappliquer aux visites suivantes — compatible avec la règle du 29 août, ne la remet pas en cause.

### À faire
- **Approche envisagée** : même mécanisme `localStorage` déjà utilisé ailleurs sur le site (`scenario_intro_seen` pour le bandeau d'accueil, la clé de dismissal du bandeau PWA) — un petit script partagé (même famille que `assets/pwa-install.js`) qui (1) au clic sur `.masthead-lang-btn`, enregistre la langue choisie avant de suivre le lien ; (2) à chaque chargement de page, si une préférence est enregistrée et diffère de `document.documentElement.lang`, cherche `.masthead-lang-btn` dans la page et redirige vers son `href` s'il existe — **ne rien faire sinon**. Ce dernier point évite d'avoir à maintenir une table de correspondance FR/EN : les pages sans équivalent anglais (glossaire, suivi, hebdo, pages légales) sont ignorées automatiquement puisqu'elles n'ont pas ce bouton.
- **Déploiement** : le site est statique (pas de template partagé côté serveur), donc le script doit être ajouté sur toutes les pages — une passe rétroactive sur l'existant, puis une ligne de plus dans le gabarit recopié chaque jour par `docs/routine-prompt.md`/`docs/routine-en-prompt.md`.

### Décisions
- **Répond au cas PWA soulevé par l'utilisateur** (« quand il ouvre l'appli, ça ouvre en anglais ou français ») : le site a deux manifestes distincts (`manifest.webmanifest` racine pour le FR, `en/manifest.webmanifest` pour l'EN), donc l'icône ajoutée à l'écran d'accueil ouvre toujours la même langue de départ quelle que soit la préférence. Comme ce script tournerait après ce premier chargement, il rebondirait automatiquement vers la langue préférée à chaque ouverture, y compris pour une app installée depuis l'autre langue.
- **Limite à connaître au moment de dépriorer ou de reprendre** : au 30 août, seules 2 éditions avaient une version anglaise (29 et 30 août) — utilité réelle faible tant que la traduction n'a pas rattrapé plus d'archives, même si le mécanisme n'a besoin d'aucune table de correspondance pour rester valable ensuite.

### Historique
- **2026-08-30** — Idée et validation P3 le même jour (retour utilisateur).

---

## B056 — Basculer du site statique « à la main » vers un fonctionnement type CMS

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée — **OUVERT le 31 août 2026, pas de direction tranchée**
**Dernière MAJ:** 2026-08-31
**Prochaine action:** Dans une session dédiée : clarifier laquelle des deux directions correspond au besoin réel (qui édite le contenu — toujours l'IA via Git, ou potentiellement un humain via une interface web ?) **avant** d'évaluer des outils spécifiques
**Blocage:** Décision explicite de l'utilisateur de ne pas trancher la direction sans avoir creusé davantage

### État actuel
**Rien commencé, volontairement.** Frictions structurelles du site statique apparues concrètement : le nav commun (`.topnav`) est dupliqué dans **76 fichiers HTML** (aucun template partagé — un changement de nav = 76 fichiers à retoucher un par un, ou une incohérence assumée entre anciennes et nouvelles pages, vécu en direct sur le chantier « menu déroulant Archives » du même jour, voir B137) ; le `<style>` CSS complet est copié-collé dans chaque page (~350 à ~900 lignes selon la page) ; et un script SEO (`scripts/seo/generate_theme_pages.py`) doit parser le HTML d'`archives.html` par regex faute de source de données structurée.

### À faire
- Choisir entre les deux directions, puis évaluer les outils.

### Décisions
- **Deux directions très différentes selon ce que « CMS » veut dire ici**, discutées mais pas choisies :
  - **Générateur de site statique** (type Eleventy/Astro/Hugo) : contenu toujours en fichiers Git (Markdown/JSON), mais avec de vrais templates réutilisables (un seul fichier de nav, un seul layout) au lieu de dupliquer le HTML partout. Un build régénère tout le site en HTML statique — garde le workflow actuel (routine/IA édite des fichiers, commit Git, hébergement gratuit GitHub Pages inchangé), migration envisageable progressivement, page par page.
  - **Vrai CMS** (headless type Sanity/Contentful, ou classique type WordPress) : base de données + interface web d'édition. Implique un hébergement différent (probablement payant) et une refonte complète de la routine de publication actuelle, qui repose entièrement sur des fichiers Git versionnés — pas une migration progressive mais un basculement global.
- Une bascule d'architecture n'est pas quelque chose à improviser dans une session déjà chargée d'autres changements.

### Historique
- **2026-08-31** — Ouvert sur retour utilisateur après une session où les frictions sont apparues concrètement.

---

## B057 — Copie intégrale du `<style>` du gabarit (`.list-box` / `.dek-list`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-14
**Prochaine action:** Aucune — à rouvrir si le symptôme revient malgré la règle
**Blocage:** Aucun

### État actuel
Problème considéré résolu. Règle explicite en place à l'étape technique 2 de `docs/routine-prompt.md` : **recopier le `<style>` intégralement, jamais au prorata de ce que le contenu du jour utilise**. Pas de garde-fou automatique supplémentaire jugé nécessaire pour l'instant.

### À faire
- Rien.

### Décisions
- Pas de garde-fou automatique ajouté : la règle écrite suffit tant que le symptôme ne revient pas.

### Historique
- **2026-08-10 et 2026-08-11 (symptôme)** — La classe `.dek-list` avait disparu du `<style>` d'`index.html` ces deux jours-là (deux jours sans liste dans le contexte), avant de réapparaître le 12. Contexte complet dans la section « Encart liste (`.list-box`) » de `docs/ARCHITECTURE.md`.
- **2026-08-12 (correctif)** — Règle explicite ajoutée à l'étape technique 2 de `docs/routine-prompt.md`.
- **2026-08-14 [FAIT — vérification sur 2 jours]** — Sur les deux éditions publiées depuis le correctif (`archives/2026-08-13.html`, `archives/2026-08-14.html`, ni l'une ni l'autre n'utilisant `.list-box` dans son contenu) : `.list-box` (10 occurrences) et `.dek-list` (4 occurrences) présentes intégralement dans les deux `<style>`, identiques à `index.html` — aucune régression, la règle tient sur 2 jours consécutifs.

---

## B058 — Optimisation d'`archives.html` (fragments chargés à la demande)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-04
**Prochaine action:** Aucune (le grossissement du fichier unique reste traité séparément, voir B061)
**Blocage:** Aucun

### État actuel
Le bloc dépliable de chaque entrée vit dans un fichier séparé `archives/fragments/{AAAA-MM-JJ}.html`, chargé via `fetch()` uniquement quand le lecteur clique sur « Scénarios » (et mis en cache côté DOM ensuite, `data-loaded` sur `.entry-scenarios`) — l'entrée dans la liste principale reste donc légère, quel que soit le nombre d'éditions accumulées. Les 12 éditions déjà publiées ont été migrées vers ce format (script Python ponctuel, pas conservé). `docs/routine-prompt.md` (étape 6) mis à jour. Testé (recherche, filtres, tri, chargement de fragment) via Playwright.

### À faire
- Rien.

### Décisions
- **Au passage (même retour utilisateur)** : ajout du pourcentage de chaque scénario (déjà calculé côté édition, simplement recopié) à côté de la flèche dans les fragments ; et design moins touffu — les tags thématiques secondaires perdent leur pastille pleine au profit d'un style texte souligné pointillé (comme les liens de sources), seul le tag de registre principal garde le badge plein.

### Historique
- **2026-08-04 (constat, retour utilisateur)** — Chaque jour, l'étape 6 de la routine insérait une nouvelle `<li class="entry">` en tête de liste, jamais retirée, avec le HTML complet du bloc dépliable des 3 scénarios inliné pour chaque entrée (pas juste un résumé) — à 12 entrées le fichier faisait déjà ~1000 lignes, un problème de fond de perf/maintenance à l'échelle d'une année de publication.
- **2026-08-04 [FAIT]** — Chargement différé en JS implémenté.

---

## B059 — Lien Instagram (@scenarios.actu) dans le bloc « Suivez-nous » du footer

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-07
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Lien ajouté, même style que les icônes existantes (Telegram/LinkedIn/X/Facebook). Ordre des icônes uniformisé partout : **Telegram, LinkedIn, X, Facebook, Instagram**. Ajouté sur les 16 pages statiques concernées (archives publiées, `contact.html`, `glossaire.html`, `le-projet.html`, `newsletter.html`, `hebdo/2026-08-02.html`, gabarits de suivi...).

### À faire
- Rien.

### Décisions
- `index.html` étant le gabarit recopié tel quel par la routine quotidienne, les futures éditions l'héritent automatiquement — **aucune modification de `docs/routine-prompt.md` nécessaire**.

### Historique
- **2026-08-07 [FAIT]** — Ajout du lien. **Bug préexistant repéré et corrigé au passage** : `archives/2026-08-07.html` n'avait pas encore le lien Facebook (figée avant son ajout plus tôt dans la journée).

---

## B060 — Site figé en silence par un bug de build Jekyll (`.nojekyll`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune — **le risque est neutralisé définitivement** par `.nojekyll`
**Blocage:** Aucun

### État actuel
Fichier `.nojekyll` ajouté à la racine : désactive complètement le traitement Jekyll/Liquid, cohérent avec le principe déjà documenté (« servis tels quels »). Déploiement suivant confirmé réussi (`pages build and deployment`, conclusion `success` vérifiée via l'API GitHub Actions) et pages vérifiées en ligne par l'utilisateur.

### À faire
- Rien. **Précaution à garder** : éviter à l'avenir de coller du texte brut ressemblant à `{% %}`/`{{ }}` dans les fichiers `.md` du dépôt.

### Décisions
- Désactiver Jekyll entièrement plutôt que d'échapper le texte au cas par cas.

### Historique
- **2026-08-11 (découverte)** — Repéré en creusant un 404 sur les deux nouvelles pages de redirection Buttondown (voir B106) : GitHub Pages exécutait par défaut son build Jekyll classique sur ce dépôt (jamais désactivé jusque-là, alors que le site est purement statique). Ce build passe **tous les `.md` du dépôt** dans le moteur Liquid, y compris `docs/ARCHITECTURE.md` : le paragraphe décrivant en prose la syntaxe Buttondown `{% if item.enclosure %}` a été interprété comme un vrai tag Liquid jamais refermé par un `{% endif %}`, provoquant une `Liquid::SyntaxError` fatale à chaque build.
- **2026-08-11 (conséquence passée inaperçue)** — Tout déploiement échouait silencieusement depuis le commit ayant introduit ce paragraphe (~11h37) : plusieurs pushes suivants, dont l'ajout des deux pages de redirection Buttondown, sont restés invisibles en ligne, le site public restant figé sur le dernier build réussi (~1h).
- **2026-08-11 [FAIT]** — `.nojekyll` ajouté, déploiement vérifié.

---

## B061 — Découpage d'`archives.html` par année

**Statut:** À FAIRE
**Priorité:** P2 — **à faire avant fin 2026**
**Dernière MAJ:** 2026-08-04
**Prochaine action:** Trancher les 3 points d'implémentation ci-dessous
**Blocage:** Aucun

### État actuel
Pas fait. La solution du 4 août (fragments à la demande, B058) règle le poids téléchargé par visite, mais pas le fait qu'`archives.html` reste un fichier unique qui grossit indéfiniment (une ligne de plus par jour, jamais retirée), ni le coût d'indexation JS (recherche/filtres/tri) qui reste `O(n)` sur toutes les entrées à chaque chargement — pas gênant aujourd'hui, mais pas illimité.

### À faire
- **À trancher avant implémentation** : URL de chaque année (`archives.html?annee=2025` ou fichiers séparés) ; comportement du sélecteur (rechargement de page vs fetch) ; impact sur l'étape 6 de la routine (écrire dans le fichier de l'année en cours, créer un nouveau fichier au changement d'année).

### Décisions
- **Direction retenue (retour utilisateur, 4 août)** : filtrer par année avec l'année en cours sélectionnée par défaut ; changer d'année charge la liste de cette année-là (un fichier par année, ex. `archives-2025.html`, `archives-2026.html`) plutôt qu'un unique fichier contenant tout. Reprend le filtre « Année » déjà présent dans l'UI (aujourd'hui un simple filtre d'affichage sur un seul fichier) pour en faire un vrai changement de page/fichier.

### Historique
- **2026-08-04** — Ticket ouvert avec sa direction, dans la foulée de l'optimisation par fragments.

---

## B062 — Données ouvertes / API publique (`feed.json` documenté comme flux stable)

**Statut:** À FAIRE
**Priorité:** P3
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Trancher la garantie de stabilité du schéma, et si `feed.json` convient tel quel ou mérite un format dédié
**Blocage:** Partage un prérequis commun avec B092 (calibration) et B142 (score historique) : un export structuré scénario ↔ résultat réel constaté, qui n'existe pas encore

### État actuel
`feed.json` existe déjà en JSON structuré (question, scénarios, probabilités), généré chaque jour. **Le travail restant est de le documenter comme flux public stable, pas de le construire** : schéma figé, page dédiée « Données ouvertes » avec un exemple et les règles de compatibilité. Coût quasi nul (la donnée existe déjà), bon capital de sérieux/goodwill, peu de médias de cette taille le font.

### À faire
- Décider de la garantie de stabilité du schéma dans le temps (breaking changes = casse les intégrations tierces).
- Décider si `feed.json` actuel (pensé pour Make/webhook) convient tel quel ou mérite un format dédié plus propre.
- Page dédiée « Données ouvertes ».

### Décisions
- **Une « base publique des scénarios » consultable** (proposée dans le backlog externe du 27 août) est le même chantier à un stade antérieur — **un jalon de cette même entrée, pas un ticket séparé**.

### Historique
- **2026-08-10** — Idée notée (brainstorm « out of the box »).
- **2026-08-27** — Rattachée à l'audit externe : classée « déjà en place, à ne pas refaire » côté construction ; la « base publique des scénarios » y est rattachée comme jalon.

---

## B063 — Identifier nommément l'auteur (byline + JSON-LD `Person`)

**Statut:** STANDBY
**Priorité:** P3 — « à revoir plus tard, pas maintenant »
**Dernière MAJ:** 2026-08-31
**Prochaine action:** **Ne pas relancer de son propre chef** — attendre un retour utilisateur explicite avant de rouvrir ce chantier
**Blocage:** Décision utilisateur : pas sûr que ce soit une bonne idée de s'identifier à ce stade

### État actuel
`author` = `Organization` partout, aucun byline, nom mentionné seulement dans `le-projet.html` (section « Qui fait Scénario »), sans lien externe — voir `docs/routine-prompt.md` pour la note explicite de non-réintroduction sans feu vert.

### À faire
- Rien sans feu vert. Si le sujet revient, réévaluer les 5 risques identifiés (voir Décisions).

### Décisions
- **Retiré entièrement le 31 août**, le jour même de sa mise en place, après une question directe de l'utilisateur sur les risques.
- **Risques identifiés à l'époque, à réévaluer si le sujet revient** : (1) le lien direct entre l'employeur actuel (finance/data/assurance, déjà mentionné dans `le-projet.html`) et le site devient traçable via LinkedIn ; (2) le site couvre géopolitique/politique française au quotidien — un nom + LinkedIn expose personnellement à la critique/au contact direct, contrairement à une marque anonyme ; (3) la mention explicite de l'usage de l'IA (`le-projet.html`) combinée à un nom réel crée un point de friction spécifique ; (4) une fois indexé par Google et des agrégateurs schema.org tiers, difficile à effacer partout même après retrait du site ; (5) perte du tampon de marque en cas d'erreur factuelle ou de scénario qui vieillit mal.

### Historique
- **2026-08-31 (essayé puis retiré le jour même)** — `author` avait été passé d'`Organization` (« Scénario ») à `Person` nommée (Olivier Bertrand, `jobTitle`, `sameAs` LinkedIn) sur les **46 pages** (39 archives FR + 5 EN + `index.html`/`en/index.html`), avec un byline visible « Par Olivier Bertrand — Directeur éditorial et technique » sous `.edition` — geste SEO E-E-A-T (Google valorise un auteur réel identifié). Retiré entièrement le même jour.
- *À ne pas confondre avec* B128 (« Identité du fondateur »), qui porte sur le manque de photo et de 1ʳᵉ personne dans `le-projet.html`, pas sur le balisage d'auteur.

---

## B064 — Graphique en escalier pour série historique longue (composant réutilisable)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Aucune — composant disponible, à n'utiliser que sous ses 3 critères
**Blocage:** Aucun

### État actuel
La recette complète (critères de déclenchement, format, gabarit CSS/SVG/JS, vérification) est documentée dans `docs/routine-prompt.md` juste après la section `.comprendre-box`, pour qu'une future édition puisse le reprendre sans repartir de zéro. **CSS pas ajouté au gabarit de base** (contrairement à `.comprendre-box`) : utilisé trop rarement pour ça — à copier depuis `index.html`/`archives/2026-08-21.html` le jour où c'est pertinent.

### À faire
- Rien.

### Décisions
- **Strictement optionnel et sous 3 critères cumulatifs** (retour utilisateur : « pas systématiquement mais quand c'est utile ») : source fiable et complète ; 8-10+ points réels sur 10+ ans ; série qui éclaire directement la question du jour. **Pas un composant à caser systématiquement.**

### Historique
- **2026-08-21 [FAIT]** — Première utilisation : Horloge de l'Apocalypse depuis 1947 sur l'édition « Le Grand Filtre » (`.dc-chart-box`). Plutôt que de laisser ce composant en one-shot, industrialisé en composant réutilisable documenté.

---

## B065 — Guide pédagogique (`guide-pedagogique.html`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-20
**Prochaine action:** Aucune — **pas ajoutée au menu `.topnav`**, à revoir si le besoin de visibilité se confirme
**Blocage:** Aucun

### État actuel
Page ajoutée, même gabarit visuel que `le-projet.html` (mêmes tokens CSS, mêmes fonts, même nav/footer/bloc « Nous suivre ») : 4 étapes de lecture d'une édition, rappel condensé de ce qu'est une probabilité (renvoi vers `le-projet.html#probabilite`), pistes d'exercice concrètes pour une classe (débat structuré 3 groupes, vérification a posteriori via une page de suivi, transposition de la méthode à un sujet du programme). Reliée depuis `le-projet.html` (section « Pour qui », nouveau `.cross-link`) et ajoutée à `sitemap.xml` (priority 0.4, changefreq monthly). Accessible par lien direct seulement (comme `mentions-legales.html`, `confirmez-votre-email.html`), **pas depuis le nav principal**.

### À faire
- Éventuellement l'ajouter au nav si le besoin de visibilité se confirme — ce qui demanderait de mettre à jour le gabarit généré chaque jour.

### Décisions
- **Pas ajoutée au menu `.topnav` commun** : ce nav est dupliqué dans toutes les pages y compris les archives figées (jamais remodifiées après publication) et probablement encodé dans le prompt de routine — l'y ajouter demanderait de toucher `docs/routine-prompt.md` sans validation explicite, pas fait ici.
- **Prérequis naturel** avant de démarcher des établissements (voir B066).

### Historique
- **2026-08-20 [FAIT]** — Suite à un retour d'audit fait par un LLM externe, soumis par l'utilisateur. **Comparaison faite point par point avec l'état réel du dépôt avant d'agir** : plusieurs suggestions étaient déjà en place (jauges de probabilité, graphiques d'évolution dans `suivi/`, recherche/filtres sur `archives.html`/`glossaire.html`, tests mobile systématiques via Playwright, point d'entrée SEO anglophone) ; une (commentaires/comptes utilisateurs/likes sur le site) rejoignait une idée déjà **écartée** (voir B094) et n'a pas été reproposée. Une piste — guide pratique « comment lire un scénario / s'en servir en classe » — répondait à un vrai manque : `le-projet.html` explique la mission et la méthode mais ne donne pas de méthode actionnable pour un usage en classe (HGGSP/SES), public déjà identifié comme cible.
- **2026-08-20** — Autres idées du même audit notées mais pas implémentées faute de décision utilisateur sur la priorité : partenariats éducatifs formels (B066), audit SEO régulier (B068), newsletter enrichie (B069). Deux autres pistes du même feedback existaient déjà ailleurs et n'ont pas été redupliquées : brief audio quotidien TTS (B033) et déclinaison papier/abonnement premium (B009).

---

## B066 — Partenariats éducatifs formels

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-08-20
**Prochaine action:** Rien à démarcher avant d'avoir le guide pédagogique — prérequis désormais rempli (B065, fait le 20 août)
**Blocage:** Aucun ; pas de décision utilisateur sur la priorité

### État actuel
Rien de construit. Idée : nouer des partenariats avec des établissements scolaires/universitaires pour intégrer Scénario comme ressource pédagogique officielle.

### À faire
- Tout reste à faire.

### Décisions
- Le guide pédagogique (B065) est un **prérequis naturel** avant de démarcher qui que ce soit.

### Historique
- **2026-08-20** — Noté parmi les idées de l'audit LLM externe non implémentées.
- **2026-09-03** — Rendu partiellement actionnable via le ticket netlinking (B067), qui liste nommément des associations d'enseignants comme cibles.

---

## B067 — Netlinking / « SEO passif » : contacter personnes et communautés

**Statut:** EN COURS
**Priorité:** P2
**Dernière MAJ:** 2026-09-03
**Prochaine action:** Étape (3) : relire/adapter chaque message dans `docs/strategie-netlinking.md`, puis envoyer depuis l'identité du site (Olivier Bertrand, `contact.html`) — en commençant par le Tier 1
**Blocage:** Aucun techniquement. **Statut : liste + messages prêts, aucun envoi fait.**

### État actuel
Étapes (1) liste de cibles et (2) messages-types **faites le 3 septembre** — voir `docs/strategie-netlinking.md` : **11 cibles nommées et vérifiées** (recherche web), classées par facilité d'obtention :
- **Tier 1** : 4 blogs perso HGGSP (décision d'une seule personne).
- **Tier 2** : 3 associations — APHG, APSES, Les Clionautes/Clio-Lycée (portée plus large mais décision collective).
- **Tier 3** : Géoconfluences ENS Lyon et CLEMI (autorité SEO forte mais institutionnels/lents).

Plus **2 messages-types** (version blog individuel, version association). **Reddit non vérifié** : aucun subreddit francophone pertinent confirmé depuis cette session (outil de recherche peu fiable sur Reddit, accès direct bloqué) — à vérifier soi-même sur reddit.com, **jamais deviner un nom de sub**.

### À faire
- Étape (3) : envoi des messages, **toujours un geste humain, jamais automatisé depuis une routine ou une session non supervisée**.
- Vérifier les subreddits francophones pertinents.

### Décisions
- **Objectif** : des backlinks (autorité de domaine, condition déjà identifiée pour l'indexation Google Actualités) obtenus par contact humain plutôt que par du contenu additionnel — d'où « passif » : une fois le lien posé, il continue de compter sans entretien, contrairement à la production quotidienne d'articles.
- Commencer par le Tier 1 (gains rapides) avant de solliciter les associations.

### Historique
- **2026-08-21 (diagnostic d'origine)** — « Le vrai levier reste les liens externes, pas plus de balises » : domaine jeune, zéro backlink (voir B068).
- **2026-09-03 (demande explicite)** — Ticket ouvert, rendant actionnable ce qui était noté séparément à deux endroits du backlog sans avoir jamais été construit : le diagnostic du 21 août et l'item « Partenariats éducatifs formels » (B066). Cibles déjà repérées mais jamais listées nommément avant : profs HGGSP/SES (public déjà positionné sur `le-projet.html` § « Pour qui » et `guide-pedagogique.html`) ; « Reddit ciblé » (mentionné le 21 août, jamais précisé) ; pistes non encore discutées avec l'utilisateur : associations professionnelles d'enseignants (APHG, APSES), sites d'éducation aux médias (CLEMI).
- **2026-09-03 [FAIT]** — Étapes (1) et (2) livrées dans `docs/strategie-netlinking.md`.

---

## B068 — Audit SEO : passe du 21 août et process récurrent

**Statut:** EN COURS
**Priorité:** P2
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Définir un process d'audit SEO récurrent (aucun n'existe à ce jour au-delà des balises meta systématiques par page)
**Blocage:** Le vrai levier restant est les backlinks (B067), pas la technique

### État actuel
Les deux lacunes techniques trouvées le 21 août sont corrigées. **Aucun process d'audit récurrent n'est identifié dans le dépôt** au-delà des balises meta déjà systématiques par page. Diagnostic de fond posé le 21 août : le domaine n'apparaissait dans aucune recherche (`site:lesscenarios.fr` et le nom de domaine entre guillemets, testés via WebSearch, zéro résultat) — problème d'**indexation/confiance d'un domaine encore jeune** (moins d'un mois, aucun backlink externe), cohérent avec le 0 clic/0 impression déjà constaté le 15 août sur Search Console (voir B104), **pas un problème de configuration technique cassée**.

### À faire
- Mettre en place un process d'audit SEO régulier.
- Volet historique jamais traité, noté très tôt dans le backlog : « amélioration de la recherche/découvrabilité et réflexion SEO plus poussée » — jugé peu coûteux à l'époque, le contenu étant déjà bien structuré (titres clairs, meta descriptions par page).

### Décisions
- **Le vrai levier à ce stade reste les liens externes (backlinks), pas plus de balises** — évoqué dans la même conversation que la croissance d'audience (contact profs SES/HGGSP, Reddit ciblé...), les deux sujets se recoupent (B067).

### Historique
- **2026-08-20** — « Audit SEO régulier » noté parmi les idées de l'audit LLM externe non implémentées (voir B065).
- **2026-08-21 (audit déclenché par un retour utilisateur : « je recherche sur Google et je ne remonte jamais »)** — Deux vraies lacunes techniques trouvées et corrigées, malgré le travail SEO déjà fait par ailleurs (Search Console, sitemap, `NewsArticle`, Publisher Center — voir B103/B104) :
  - **Aucune balise `<link rel="canonical">` nulle part sur le site** (seul `og:url` existait, qui sert au partage social, pas à l'indexation). Ajoutée sur `index.html`, les 28 archives et les pages statiques vivantes (voir `docs/routine-prompt.md`, nouveau paragraphe après l'étape technique 3bis, pour la règle de reproduction quotidienne). **`index.html` pointe vers l'archive du jour** (pas vers lui-même) puisque son contenu n'est qu'un miroir temporaire.
  - **Meta description trop longue** (184 caractères sur l'édition du 20 août, tronquée par Google au-delà de ~155-160) — raccourcie pour cette édition, règle de longueur ajoutée à la routine pour les prochaines.

---

## B069 — Newsletter enrichie (Q&A avec le créateur, aperçus des sujets à venir)

**Statut:** À FAIRE
**Priorité:** P3
**Dernière MAJ:** 2026-08-20
**Prochaine action:** Aucune planifiée
**Blocage:** Pas de décision utilisateur sur la priorité

### État actuel
Rien de construit. Idée : aller au-delà de l'édition quotidienne déjà envoyée via Buttondown (`newsletter.html`) — Q&A avec le créateur, aperçus des sujets à venir.

### À faire
- Tout.

### Décisions
- Aucune.

### Historique
- **2026-08-20** — Notée parmi les idées de l'audit LLM externe non implémentées (voir B065).
- *Note de recoupement* : un aperçu des sujets à venir existe désormais côté interne (bloc « Agenda de la semaine » du dashboard, voir B148), mais pas côté newsletter.
---

## B070 — Restructuration des registres du week-end (culture / économie & finance mondiale)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-12
**Prochaine action:** Resynchroniser à la main le prompt du trigger live avec `docs/routine-prompt.md` (voir B108) — point non résolu au moment de l'écriture
**Blocage:** Synchronisation manuelle du prompt (B108)

### État actuel
Samedi = registre **`culture`** (fusion culture française + culture internationale), dimanche = nouveau registre **`économie & finance mondiale`** *(puis permuté avec Sport le même jour, voir B071)*, lundi redevient un registre géopolitique plus resserré (conflits, diplomatie, rapports de force entre États).

### À faire
- Confirmer la resynchronisation du prompt live.

### Décisions
- **Fusion culture française + culture internationale** : la frontière France/international était souvent artificielle (Ubisoft est français mais mondial, Netflix est international mais touche les abonnés français).
- **Règle de classement pour un sujet à cheval** (guerre commerciale, tarifs douaniers…) : l'enjeu central est un rapport de force entre États → géopolitique/lundi ; l'enjeu central est un indicateur chiffré ou un marché → économie/dimanche. Deux cas tranchés en exemple : « Guerre commerciale USA-Chine » reste en géopolitique (framing État contre État) ; « Droits de douane de Trump » part en économie (contenu réel = batailles judiciaires et recettes tarifaires, pas un rapport de force diplomatique).
- **Tags historiques jamais retaggés rétroactivement** : `culture-francaise`/`culture-internationale` marqués historiques dans `docs/tags.md`, conformément à la règle déjà en place.
- **Non modifié, volontairement** : les archives déjà publiées (`archives/*.html`), les récaps hebdo déjà publiés (`hebdo/*.html`, `feed-weekly.xml`) et le rollback `docs/routine-prompt-rollback-2026-08-11.md` gardent leurs anciens libellés (« culture française », « culture internationale », « géopolitique international ») — enregistrements historiques exacts de ce qui a été publié à l'époque.

### Historique
- **2026-08-12 (constats croisés, retour utilisateur)** — (1) `sujets-prioritaires.md` montrait samedi (culture française) et dimanche (culture internationale) quasi vides (1 et 3 sujets restants), alors que lundi (géopolitique/international) débordait avec **17 sujets en attente**, dont la moitié purement économiques (inflation, taux, dette, marchés, dollar, or, bitcoin, pétrole…) mélangés aux vrais sujets géopolitiques (Ukraine, Taïwan, Iran, guerre commerciale) dans un seul slot hebdomadaire.
- **2026-08-12 [FAIT] — fichiers modifiés** : `sujets-prioritaires.md` (sections renommées/scindées/fusionnées, **80 sujets répartis à l'identique, aucun perdu**) ; `docs/tags.md` §1 (nouveaux tags `culture`/`economie-mondiale`) ; `archives.html` (`registreCanonicalOrder` étendu aux deux nouveaux tags, les deux tags historiques restent en fin de liste pour que le filtre continue de fonctionner sur les vieilles éditions) ; `docs/routine-prompt.md` (grille de l'étape 1, mapping des tons — dimanche rejoint lundi/mercredi côté sobriété plutôt que jeudi/samedi) ; `index.html` (script « Demain : {registre} », mapping JS des jours) ; `le-projet.html` (grille publique `.rhythm-grid`, visible des lecteurs).
- **2026-08-12 (point non résolu)** — Le trigger live de la routine quotidienne (`trig_0176spj7P7E9fyTs1XBkQBWF`) tourne sur un prompt figé stocké côté Claude Code Remote, à resynchroniser à la main ; la session n'a pas les droits `update_trigger` sur ce trigger (créé via `http_api`, pas par un agent) — voir B108.

---

## B071 — Permutation Sport ↔ Économie & finance mondiale (jeudi / dimanche)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-12
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
**Sport le dimanche, Économie & finance mondiale le jeudi.** Culture (samedi) inchangée. Mapping des tons : jeudi rejoint lundi/mercredi côté sobriété, dimanche rejoint samedi côté ton enlevé.

### À faire
- Rien.

### Décisions
- Principe : « plus logique de mettre des sujets plus légers le week-end » (retour utilisateur).
- **Urgence assumée le jour même** : le 13 août (lendemain) tombait un jeudi, donc le nouveau mapping devait être effectif avant la prochaine exécution de la routine (7h Paris) — d'où le **texte donné à l'utilisateur pour collage manuel dans le trigger live**.
- **Non modifié, volontairement** : les 20 archives déjà publiées gardent leur ancien mapping JS « Demain : {registre} » — widget calculé côté client à partir de la date réelle du visiteur, techniquement daté sur les vieilles pages, mais jamais mis à jour rétroactivement par choix déjà établi.

### Historique
- **2026-08-12 [FAIT]** — Repris juste après la restructuration B070, sur le même principe. **Fichiers modifiés** : `docs/routine-prompt.md` (grille de l'étape 1 + mapping des tons) ; `sujets-prioritaires.md` (en-têtes de section `## Sport` et `## Économie & finance mondiale` seulement — le contenu des sujets reste dans sa section, aucun sujet déplacé) ; `docs/tags.md` (notes sur `sport-economie` et le registre `sport`, jour mis à jour) ; `index.html` + `archives/2026-08-12.html` (mapping JS des jours, indices 0 et 4 permutés) ; `le-projet.html` (grille publique `.rhythm-grid`).

---

## B072 — Pondération France Impact par registre (poids asymétrique)

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-12
**Prochaine action:** Reprendre la discussion — principe proposé, jamais implémenté
**Blocage:** Discussion en cours, pas de décision

### État actuel
**Pas implémenté.** Principe proposé le 12 août : « l'ascenseur descend vite, l'escalier remonte lentement » — poids asymétrique **−1,5/+1** pour géopolitique/économie/actualité française, **±1** pour le reste.

### À faire
- Trancher et, le cas échéant, implémenter.

### Décisions
- Le principe reste valable tel quel après la permutation Sport/Économie du 12 août (B071) : **la règle est associée au nom du registre, pas au jour de la semaine**, donc aucun ajustement nécessaire de ce côté-là.
- Distincte de la pondération par `kind` (B073), qui agit sur le poids de chaque **carte**, pas sur le score final par sujet.

### Historique
- **2026-08-12** — Principe proposé et discuté, noté comme « discussion en cours, pas encore implémentée ».
- **2026-08-13** — Le dicton de trader « on descend par l'ascenseur, on remonte par l'escalier » a été ajouté comme `citation-12` dans `docs/pub-messages.md`, en écho explicite à cette idée non implémentée (voir B078).

---

## B073 — Pondération France Impact par `kind` de scénario (0,5 sur la carte stable)

**Statut:** STANDBY
**Priorité:** P3 — « on verra plus tard » (retour utilisateur)
**Dernière MAJ:** 2026-09-02
**Prochaine action:** Relire l'avis critique ci-dessous **avant d'implémenter quoi que ce soit** ; explorer plutôt la contre-proposition (indicateur de dispersion séparé)
**Blocage:** Avis technique défavorable rendu à l'utilisateur, pas encore rediscuté

### État actuel
**Pas implémenté.** Proposition : pondérer 0,5 la carte stable et 1 les cartes favorable/dégradé dans `compute_france_esperance()` (sur `_JUDGMENT_VALUE`/le poids de chaque **carte**, pas sur le score final par sujet) — pour « alléger le centre et donner plus de poids aux queues de distribution ».

### À faire
- Rediscuter avec l'utilisateur à la lumière de l'avis ci-dessous.

### Décisions
- **Avis rendu à l'utilisateur avant l'ajout au backlog, à relire avant toute implémentation** : le `kind` (favorable/stable/dégradé) est une **étiquette structurelle fixe** (une carte de chaque par édition), pas une position dans la distribution de probabilité — rien ne garantit que la carte « stable » soit la moins probable des trois un jour donné.
  - **Contre-exemple chiffré avec l'édition du 2 septembre** (Pesticides interdits, favorable 25 % / stable 45 % / dégradé 30 %, jugements +1/−1/−1) : espérance actuelle = **−0,50** (« assez négatif ») ; avec le poids 0,5 sur stable = **−0,275** (« plutôt défavorable ») — le score s'**adoucit** au lieu de s'accentuer, parce que « stable » portait justement le plus gros poids de probabilité ce jour-là. L'effet du poids dépend donc de quelle carte est la plus probable le jour J, pas d'un vrai signal de queue de distribution : **risque d'artefact plutôt que de biais choisi.**
  - Recasserait aussi l'étalonnage `FRANCE_ESPERANCE_SCALE` (déjà resserré une fois le 20 août) puisque l'amplitude atteignable change selon les jours.
  - Réintroduirait une dépendance au `kind` du même genre que celle **retirée** le 17 août sur la valeur France de « stable » (voir B089) — un poids par `kind` remettrait sur le poids ce qu'on vient d'ôter de la valeur.
- **Contre-proposition avancée, à explorer à la place** : ne pas toucher à l'espérance elle-même (qui reste une vraie espérance pondérée, honnête) mais ajouter un **indicateur de dispersion/désaccord séparé** entre les 3 scénarios, si le vrai besoin est de distinguer un pronostic tranché d'un pronostic mou — jamais en truquant le calcul existant avec un poids sans lien garanti avec les vraies queues de la distribution. Fait aussi écho au biais « risque de queue » déjà noté comme accepté-mais-non-résolu à la création de France Impact (12 août, voir B089).

### Historique
- **2026-09-02** — Ajouté au backlog sur retour utilisateur, avec l'avis critique et la contre-proposition consignés avant l'ajout.

---

## B074 — `le-projet.html` : le rôle technique porte sur la méthode, pas juste le site

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-07
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Phrase reformulée : « il conçoit et fiabilise la méthode quantitative qui structure les scénarios — probabilités, indicateurs, critères de bascule — ainsi que la gestion du site qui les diffuse. » Rôle éditorial (choix des sujets, vérification, ton) inchangé juste après.

### À faire
- Rien.

### Décisions
- La partie la plus substantielle du travail est la **méthode quantitative des scénarios** (probabilités, indicateurs, critères de bascule), le site n'en étant que le vecteur de diffusion.

### Historique
- **2026-08-07 [FAIT]** — Retour utilisateur : la phrase d'origine (« il conçoit et veille au bon fonctionnement du site ») sous-vendait le travail réel.

---

## B075 — Images de partage par édition

**Statut:** ABANDONNÉ
**Priorité:** —
**Dernière MAJ:** 2026-08-04
**Prochaine action:** Aucune — **décision ferme, ne pas reproposer**
**Blocage:** —

### État actuel
Écarté définitivement le 4 août : risque deepfake sur des sujets impliquant de vraies personnes.

### À faire
- Rien.

### Décisions
- **Décision ferme, ne pas reproposer.**
- *À distinguer de* l'image du sujet par photo libre de droits (B027), retenue plus tard justement parce qu'elle élimine ce risque (mots-clés génériques, jamais de personne réelle, revue visuelle obligatoire).

### Historique
- **2026-08-04** — Écarté définitivement.

---

## B076 — Image dans le corps de l'article (`figure.article-image`)

**Statut:** FAIT
**Priorité:** P1 (passée en P1 puis implémentée le jour même)
**Dernière MAJ:** 2026-08-10
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Bloc `<figure class="article-image">` inséré entre le sommaire (`.toc`) et le `.question-box`, avec une légende discrète en dessous (« **Photo d'illustration.** Photo : {photographe} / Pexels ↗ », style repris de `.sources-note`). `alt` réutilise la description déjà écrite pour `og:image:alt` (aucune rédaction en double). Contenue dans la largeur de la colonne (`.wrap`, 920px), pas plein écran, cohérent avec l'esprit typographique du site. Habillage : fondu noir en dégradé CSS en haut de la photo (`.article-image-scrim`, même teinte `--ink`) + masthead logo et wordmark « Scéna**rio** » en haut à gauche (réutilise `assets/logo.svg`) — **du vrai texte en overlay CSS, pas une image composite pré-rendue** comme pour Instagram, donc pas de nouvelle étape de génération, toujours la même photo `-wide.jpg`. Le style vit entièrement dans le `<style>` du gabarit `index.html`, recopié tel quel chaque matin (étape technique 3) : aucune valeur codée en dur dans `docs/routine-prompt.md`, seulement la classe `.article-image-masthead`.

### À faire
- Rien.

### Décisions
- **Piste initiale abandonnée en cours de route** : la première proposition (illustration générique/abstraite par registre, générée une fois et réutilisée) rouvrait sans le savoir un débat déjà tranché le 1er août (voir B111) — une illustration IA abstraite y avait déjà été envisagée puis écartée, pour une raison de cohérence de design (introduire un élément visuel non maîtrisé), pas seulement de risque.
- **Solution retenue : réutiliser tel quel le pipeline Pexels déjà construit le 8-9 août** (B027) plutôt qu'en inventer un nouveau — la photo du jour y est déjà sourcée avec zéro risque et déjà commitée chaque jour dans `assets/social/topic-images/{date}.jpg`, mais n'était utilisée que pour les meta `og:image`/`twitter:image` et le post Instagram, jamais visible par un lecteur du site. **Le seul vrai manque était la restitution, pas le sourcing.**
- **Titre en overlay essayé puis retiré le jour même** (retour utilisateur) : redondant avec le `<h1>` réel juste au-dessus — n'apportait qu'une répétition visuelle, et était déjà marqué `aria-hidden` donc jamais lu par un lecteur d'écran. Le fondu du bas de la photo a été retiré avec lui (plus nécessaire sans texte à faire ressortir) ; seul le fondu du haut reste, pour le masthead.
- **« Photo d'illustration. » en tête de légende, systématique et non négociable** (retour utilisateur, question posée sur la pertinence de la photo pour Google Actualités/le partage). Constat : la recherche Pexels se fait par mots-clés thématiques génériques, jamais le lieu/la scène exacte du sujet (principe non négociable du zéro-risque deepfake), donc la photo n'est presque jamais littéralement l'événement ou le lieu de l'article — concrètement le 10 août, une photo du détroit du **Bosphore** pour un article sur le détroit d'**Ormuz** (deux détroits différents, l'un en Turquie, l'autre entre l'Iran et la péninsule arabique). Pas un mensonge (légende/alt restent factuellement exacts sur ce qu'est la photo) mais une ambiguïté possible pour un lecteur pressé — évitée par cette mention, désormais **jamais retirée ni reformulée** dans `docs/routine-prompt.md`.
- **Règle des archives précisée** : « une archive ne se modifie jamais » (`docs/routine-prompt.md`, étape 10) protège les archives **datées d'un jour antérieur** — pas l'archive du jour même, produite par la même exécution de routine qu'`index.html` quelques heures plus tôt. Contrairement aux boutons de partage du 4 août (appliqués à partir de l'édition suivante, sur une archive déjà ancienne), ici `archives/2026-08-10.html` aurait sinon perdu la photo dès le lendemain matin (`index.html` écrasé par la routine, l'archive restant la seule trace permanente de cette édition).
- **Pas de coût récurrent supplémentaire** : un seul appel HTTP de plus par jour (le recadrage large), zéro nouvelle revue humaine/agent, zéro nouvelle dépendance.

### Historique
- **2026-08-10 (idée)** — Retour utilisateur : apporterait plus d'adoption. Passée en P1 et implémentée le jour même.
- **2026-08-10 [FAIT] — ajouts techniques** : `scripts/social/fetch_topic_image.py` (`square_crop_url()` généralisée en `crop_url(url, w, h)` ; `original_url` — URL source Pexels — ajoutée à `credits.json` pour permettre un second recadrage plus tard sans nouvelle recherche) ; `scripts/social/use_topic_image.py` (télécharge en plus un recadrage **16:9, 1600×900** de la même photo déjà validée vers `assets/social/topic-images/{date}-wide.jpg` — pas de nouvelle revue visuelle nécessaire, c'est un recrop, pas un nouveau candidat ; silencieusement absent si `original_url` manque ou si le téléchargement échoue, jamais bloquant) ; gabarit (`index.html`, `docs/routine-prompt.md` étape technique 8).
- **2026-08-10 (habillage et ajustements le jour même)** — Habillage inspiré de la carte Instagram (`scripts/social/instagram-photo-template.html`). Taille du logo/wordmark ajustée deux fois (trop petit, puis un peu trop gros) avant de se stabiliser. Masthead resserré dans le coin (`top: 22px`/`left: 24px` → `top: 10px`/`left: 12px`). Testé desktop + mobile via Playwright avant chaque publication.
- **2026-08-10 (appliqué à l'édition du jour)** — Sujet Ormuz/croissance mondiale, la photo déjà retenue par la routine ce matin-là (un pétrolier vu du ciel dans le Bosphore) collant bien au sujet : `index.html` **et `archives/2026-08-10.html`** mis à jour avec la vraie photo (CSS + bloc HTML, chemins ajustés en `../assets/...` depuis l'archive). **Décision initiale corrigée en cours de session** (retour utilisateur : l'archive avait été oubliée).

---

## B077 — Routine « Inspecteur » de re-vérification matinale

**Statut:** EN COURS
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-13
**Prochaine action:** **La routine principale doit être avancée à 6h Paris** — à faire manuellement par l'utilisateur dans l'interface Claude Code Remote (`update_trigger` refusé sur ce trigger, voir B108). Une fois fait, rapprocher l'Inspecteur de 8h à 7h Paris (`update_trigger` fonctionne pour lui)
**Blocage:** Dépend d'un geste utilisateur hors session sur le trigger de la routine principale

### État actuel
Prompt rédigé (`docs/routine-inspection-prompt.md`), journal créé (`docs/inspection-log.md`), **trigger créé le 13 août** : `trig_015wbeqHwALMg3EsUaZcRoWp`, via `create_trigger` (`created_via: meta_mcp`, donc `update_trigger` utilisable directement, contrairement au trigger principal). Session fraîche à chaque déclenchement (`create_new_session_on_fire`), prompt volontairement court qui renvoie vers `docs/routine-inspection-prompt.md` comme source de vérité plutôt que de dupliquer le texte dans le trigger (éviter la dérive du trigger principal, où deux copies doivent être resynchronisées à la main). **Horaire provisoire : `0 6 * * *` UTC = 8h Paris**, pas 7h comme prévu initialement (retour utilisateur du 13 août : « tu le mets à 8h Paris time pour l'instant »), le temps que la routine principale soit avancée à 6h Paris. Pas de connecteurs MCP attachés (Gmail/Calendar/Drive/MailerLite) : seulement les outils de base (Bash/Read/Write/Edit/WebFetch). *(Horaire ensuite fixé à 7h Paris / `0 5 * * *` UTC dans le planning global du 14 août — voir B087.)*

### À faire
- Avancer la routine principale à 6h Paris (geste utilisateur), puis rapprocher l'Inspecteur.
- **Lacune n° 4, non traitée, moins urgente** : pas de limite explicite sur le nombre de corrections « mécaniques » (points 1-7) par édition, alors que le point 8 (clarté) en a une (3 max) — à rouvrir si l'usage réel montre qu'une édition accumule beaucoup de petits correctifs le même jour.

### Décisions
- **Objectif reformulé le 12 août : améliorer l'accuracy des articles, jamais retoucher un choix éditorial** (scénario, probabilité, angle).
- **Horaire cible : routine principale à 6h00 Paris, Inspecteur à 7h00 Paris** (1h d'écart — à confirmer empiriquement une fois la durée réelle de la routine principale observée sur quelques jours).
- **Deux niveaux de correction, tranchés le 12 août** :
  - **Corrigé seul, sans demander** (mécanique, sans ambiguïté) : CSS tronqué ; désync `index.html`/archive du jour ; `data-france-impact`/`data-kind` qui ne correspond pas au texte adjacent ; incohérence numérique interne non ambiguë (majorité claire, ex. « 9 » à 3 endroits contre « 10 » à un seul) ; label brut oublié dans L'essentiel ; « Notre évaluation » raccourci. **Plus, ajout du même jour (retour utilisateur) : réécriture de phrases pour la clarté/pédagogie**, avec des garde-fous stricts — jamais de perte de chiffre/date/nom/lien de causalité, jamais de suppression d'information, uniquement la forme, chaque réécriture journalée en avant/après complet (seule catégorie qui touche à la formulation, donc la plus auditable).
  - **Signalé seulement, jamais corrigé seul** : probabilités qui ne somment pas à 100 % ; incohérence numérique ambiguë ; écart entre un chiffre cité et sa source déjà citée (la source a pu changer depuis la rédaction) ; terme de lexique orphelin — tout ce qui touche à un choix éditorial même indirectement.
- **Vérification des chiffres contre les sources** (question ouverte de l'utilisateur : « doit-on ouvrir les sources web et vérifier ? ») : oui, mais **bornée aux sources déjà citées** dans la `<section class="sources">` de l'article — jamais une nouvelle recherche sur le sujet. **3 à 5 chiffres les plus structurants seulement**, pas chaque virgule. Source injoignable = signalé « non re-vérifiable », jamais bloquant.
- **Économie de tokens** (retour utilisateur : « l'idée n'est pas de défoncer nos tokens ») : le vrai levier n'est pas de réduire le nombre de vérifications mais de **remplacer la lecture/raisonnement LLM par des outils déterministes** (`grep`/`diff`/script Python court) partout où c'est possible — sur les 8 points de « Corrigé seul », **6 ne demandent aucun jugement** (CSS manquant, désync index/archive, attribut incohérent, incohérence numérique non ambiguë, label brut, « France Impact » raccourci) : un motif ou un diff suffit. Seuls **2 points** (clarté/pédagogie, chiffres contre sources) demandent une vraie lecture LLM. **Plafonds explicites : 3 réécritures de clarté maximum par édition, 5 appels WebFetch maximum** pour la vérification des chiffres.
- **Limite honnête actée** : si les posts sociaux et la newsletter partent peu après la publication de 6h (via `feed.xml`), ils sont déjà envoyés au moment où l'Inspecteur passe — une correction ne peut rattraper que le site, pas ce qui a déjà circulé.
- **Journal séparé** : `docs/inspection-log.md`, une entrée par passage même sans rien à signaler — volontairement distinct de ce backlog pour ne pas noyer le journal éditorial dans du contrôle qualité quotidien.

### Historique
- **2026-08-10** — Idée.
- **2026-08-12 [FAIT — prompt rédigé, trigger pas encore créé]** — Détaillée et rédigée sur retour utilisateur. Fichiers créés : `docs/routine-inspection-prompt.md` (structure calquée sur `docs/routine-detection-prompt.md`) et `docs/inspection-log.md` (squelette).
- **2026-08-12 (soir) — relecture critique du prompt : 4 lacunes soulevées, 3 corrigées** :
  1. **Référence CSS trop vague** pour le groupe `.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag` — « recopier depuis la dernière archive qui la contient » est risqué car ce groupe a changé de forme **cinq fois dans la même soirée** ; une archive même récente peut contenir une version dépassée. **Corrigé** : le bloc CSS canonique de ce groupe est recopié texte pour texte directement dans `docs/routine-inspection-prompt.md`, à tenir à jour manuellement (même discipline que `docs/routine-prompt.md`) — les autres classes surveillées (`.essentiel-box`, `.list-box*`...), stables depuis longtemps, restent sur la règle « recopier depuis la dernière archive ».
  2. **Incohérence numérique : la règle ne vérifiait que le chiffre, pas le fait.** Repéré via un exemple réel de la soirée (`archives/2026-08-09.html`, article Musique IA) : « 9 milliards » (Sony seul contre Suno) et « 13,5 milliards » (Sony + Universal combinés contre Suno + Udio, sommés dans le texte lui-même) — ce n'était pas une erreur, mais une règle naïve sur la seule correspondance de chiffres aurait pu « corriger » un article juste. **Corrigé** : le point 4 exige de confirmer même fait/même périmètre/même opération avant toute comparaison, avec cet exemple réel écrit dans le prompt pour fixer le seuil.
  3. **Aucune auto-vérification après une correction, avant de commiter.** Toute la soirée, chaque édition manuelle avait été suivie d'un contrôle (balise HTML équilibrée, souvent une capture Playwright) — le prompt ne l'imposait pas à l'Inspecteur sur ses propres corrections. **Corrigé** : nouvelle section obligatoire — balance des balises + re-vérification de la sync index/archive après chaque correctif, plus une capture Playwright ciblée pour les correctifs touchant la mise en page (point 1 CSS) uniquement ; tout échec de vérification annule le correctif (`git checkout`) et bascule l'entrée en « signalé pour revue humaine » plutôt que de commiter quelque chose de non validé.
  4. **(Non traitée)** Pas de plafond sur les corrections mécaniques.
- **2026-08-13 [FAIT]** — Trigger créé, horaire provisoire à 8h Paris.

---

## B078 — Routine « pub » hebdomadaire (manifeste, citations, engagement)

**Statut:** EN COURS — **routine live depuis le 14 août**
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Décider si `citation-13` (Einstein, retirée le 13 août) doit être vérifiée sérieusement puis réintégrée (voir B085) — **rien d'autre ne bloque, la routine est live**
**Blocage:** Aucun

### État actuel
Routine autonome qui publie un post « pub » organique sur Instagram/Facebook/LinkedIn (et les autres réseaux via la branche RSS PUB, voir B037) à partir d'un nouveau flux dédié `feed-pub.xml`. Prompt : `docs/routine-pub-prompt.md`. Banque de contenu : `docs/pub-messages.md`. Trigger : `trig_01A1XU5Kpc4QWzApjZPqcKpj` (créé le 13 août, `created_via: meta_mcp`, donc `update_trigger` utilisable directement). Catégorie choisie par une **table jour → catégorie fixe** (voir B086). Distincte de la piste « pub payante » (B012) : ici du contenu organique récurrent, aucun budget publicitaire.

### À faire
- Trancher `citation-13` (B085).
- **Décision laissée à l'utilisateur** : retirer ou non les 2 citations repérées comme moins « positives » en ton (Voltaire, Héraclite), gardées avec un CTA compensatoire.
- **Décision laissée à l'utilisateur** : `citation-11` (slogan réel de la Française des Jeux, « 100 % des gagnants ont tenté leur chance », assumé comme slogan et non déguisé en citation) — sujet sensible jeu d'argent, à retirer si ça pose problème en relecture.

### Décisions
- **Objectif** : combler l'absence de tout contenu qui parle du projet lui-même entre deux éditions — **rétention** de la communauté déjà abonnée, pas acquisition.
- **Décision de principe importante : la routine ne génère/n'invente jamais un message ni une citation elle-même au moment de l'exécution** — risque de citation mal attribuée ou inventée par un LLM, déjà identifié en concevant l'Inspecteur (B077). Elle pioche uniquement dans la liste curée, en rotation. **Seule exception** : la catégorie `futur` (B083), autorisée à chercher un nouveau fait à chaque tour avec source vérifiée.
- **Cadence** : 1×/semaine en croisière, plus fréquente au lancement — piloté uniquement par le cron du trigger, **aucune logique de fréquence dans le prompt lui-même**.
- **Règle transversale « dénominateur commun » engageant/positif/orienté croissance (13 août)** : chaque entrée, toutes catégories confondues, doit se terminer par un CTA qui pousse à agir (abonnement, commentaire) — pas rester un rappel d'identité passif ; le ton reste positif/curieux même sur un sujet sérieux (retraites, climat), **jamais alarmiste**. CTA ajouté/renforcé sur toutes les entrées existantes (manifeste → « Abonne-toi, c'est gratuit » ; citations → CTA d'abonnement ajouté à toutes ; chiffres/futurs → CTA reformulé pour inviter explicitement à commenter plutôt qu'une question purement rhétorique).
- **Ton (13 août) : « moins IA style, plus naturel »** — le même « Abonne-toi, c'est gratuit » recopié presque identique sur 6+ entrées manifeste/citations a été varié en formulations propres à chaque entrée. **Vigilance à garder pour toute future entrée** : éviter la construction trop symétrique/générique typique d'un texte généré, préférer une formulation qui sonnerait bien dite à voix haute.
- **Nettoyage du 13 août : toutes les entrées non confirmées retirées** (retour utilisateur : « enlève les trucs qui sont pas confirmé ») plutôt que de les laisser traîner en attente de vérification — **16 entrées retirées** : `manifeste-05/06` (affirmations sur le modèle économique), `citation-04/09/10` (Anatole France, Bernanos, Bergson — attribution non confirmée), `citation-13` (Einstein), `chiffre-01/02/03` (retraites, population 2050, +1,5 °C), `futur-01` à `futur-07`.

### Historique
- **2026-08-13 (conception)** — Cadence tranchée : 1×/semaine, toutes les plateformes (Instagram/Facebook/LinkedIn), via un nouveau flux RSS dédié que l'utilisateur capturera dans Make comme les autres. Banque de contenu `docs/pub-messages.md` créée : liste fermée et curée à la main, **6 messages manifeste + 6 citations** au départ (brouillon), dont 2 manifestes et 2 citations marqués `[à confirmer]`/`[attribution à vérifier]`.
- **2026-08-13 [FAIT]** — `feed-pub.xml` créé (scaffold, aucun item) et `docs/routine-pub-prompt.md` rédigé : garde-fou anti-doublon 20h, choix déterministe catégorie/entrée/photo, génération image, construction de l'item, résumé final avec crédit en clair.
- **2026-08-13 (2 catégories supplémentaires, retour utilisateur)** — La banque passe de 2 à 4 sections : **Questions à la communauté** (B081) et **Le saviez-vous** (B082). Rotation alors : cycle fixe manifeste → citation → question → chiffre → manifeste…, déduit de l'historique déjà publié dans `feed-pub.xml` (pas de fichier d'état séparé).
- **2026-08-13 (5e catégorie)** — **Grands futurs** (B083). Cycle étendu à 5.
- **2026-08-13 (enrichissement, retour utilisateur, 4 ajouts)** :
  1. Manifeste : `manifeste-07`, message dédié à l'inscription newsletter (canal distinct de « s'abonner » sur les réseaux) — « 100 % réalisable, jamais de science-fiction ».
  2. Citations : 2 dictons populaires plutôt que des citations d'auteur — `citation-11` (slogan Française des Jeux) et `citation-12` (« on descend par l'ascenseur, on remonte par l'escalier », dicton de trader, pas d'auteur nommé — écho à la pondération asymétrique du France Impact, B072).
  3. Grands futurs : 3 nouvelles entrées `futur-05/06/07` côté **grands risques du siècle** (climat, IA, pandémie) en plus des 4 côté inventions.
  4. Questions : `question-01` (proposer un sujet) **retiré** — retour utilisateur : « on n'en sait rien, les gens scrollent », une question qui demande de construire une idée ne marche pas dans un feed. Remplacé par `question-04` (« le vrai risque pour la société dans 10 ans »), qui demande un avis plutôt qu'une proposition. Variante « quel est ton rêve » écartée par l'utilisateur lui-même comme trop convenue.
- **2026-08-13 [FAIT] — trigger créé** : `trig_01A1XU5Kpc4QWzApjZPqcKpj`, cron `0 16 * * 2,5` UTC = **mardi et vendredi 18h Paris** (2×/semaine, cadence de lancement choisie par l'utilisateur, à ramener à 1×/semaine plus tard si besoin). Session fraîche à chaque déclenchement, même principe que l'Inspecteur : prompt court renvoyant vers `docs/routine-pub-prompt.md`. Premier passage prévu vendredi 14 août.
- **2026-08-14** — Trigger passé à 5×/semaine (voir B086), puis déplacé à 2h Paris (voir B087).

---

## B079 — Gabarits d'image des posts pub (V1→V4 hybride, V5 stat)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Aucune (le recadrage photo reste ouvert, voir B001)
**Blocage:** Aucun

### État actuel
**Gabarit principal : `scripts/social/pub-template-v4-hybride.html`** (V4 hybride, tranché le 13 août), étendu de 2 à 5 couleurs d'accent — une par catégorie : or (manifeste), bleu (citation), vert (question), orange (chiffre), violet `--futur: #9b7fc0` (grands futurs) — les trois premières reprenant les teintes `--favorable`/`--stable`/`--degrade` déjà utilisées partout ailleurs sur le site. **Gabarit dédié à la catégorie chiffre : `scripts/social/pub-template-v5-stat.html`** (sans photo à l'origine, chiffre dominant). Génération : `scripts/social/generate_pub_image.py`. Toutes les entrées existantes de `docs/pub-messages.md` (champs `stat`/`message`/`attribution`/`cta`) restent valables sans réécriture.

### À faire
- Rien.

### Décisions
- **Photo de fond + fondu noir + mot-clé en doré** (`**mot**` dans le JSON) plutôt qu'un fond uni comme envisagé au départ (retour utilisateur).
- **Refonte du 21 août sur V5-stat** : `.stat` (chiffre géant seul) et `.message` fusionnés en un seul `.headline` — la phrase d'origine, avec le chiffre surligné en gras/orange dans son flux naturel (testé d'abord en `display:block` isolé, abandonné car ça laissait des mots orphelins avant le chiffre). `.attribution`/`.cta` retirés du HTML : ils restent dans la légende du post (`<comments>` de `feed-pub.xml`, `docs/routine-pub-prompt.md` étape 4) — rien n'est perdu côté lecteur, l'image gagne en impact. `.content` passé de `justify-content:center` à `flex-end` (texte poussé en bas, la photo respire en haut) et `.scrim` renforcé sur le tiers bas (0.84-0.97 au lieu de 0.58-0.9 sur toute la hauteur).
- **Surlignage automatique du chiffre** : `generate_pub_image.py` cherche `stat` tel quel dans le texte de `message` et l'entoure de `**` avant formatage si l'entrée ne l'a pas déjà marqué à la main — l'auteur d'une entrée `chiffre` n'a plus besoin d'ajouter ce marquage.
- **Couleur du chiffre géant éclaircie (17 août)** : `--stat` passe de `#bd6248` (terracotta assez sombre, qui se noyait dans le fond sombre du gabarit, surtout sur les photos claires où peu de scrim est visible derrière le chiffre) à **`#ff8b5e`** (corail plus lumineux) — contraste WCAG contre un fond sombre passé de **4.4:1 à ~8:1**. Changé dans `pub-template-v5-stat.html` (`--stat`, seul gabarit qui rend réellement la catégorie `chiffre`) et, par cohérence, dans `pub-template-v4-hybride.html` (`--degrade`, même couleur documentée comme identique dans le commentaire du gabarit v5, même si ce template ne rend plus `chiffre` depuis le 15 août).
- **Correction appliquée aux 4 premiers gabarits** : l'URL `lesscenarios.fr` du footer ne doit pas passer en capitales (`text-transform:lowercase` sur `.footer .url` seulement, le tagline garde les majuscules).
- `generate_pub_image.py` : champ optionnel `stat` (placeholder `__STAT__`), rétrocompatible — les autres gabarits n'ont pas ce placeholder, le `.replace()` ne fait rien sur eux.

### Historique
- **2026-08-13 — 4 pistes explorées** (`scripts/social/pub-template-v{1..4}-*.html`) :
  - **V1 sobre** : photo à peine suggérée (voile 86 %), liseré de couleur.
  - **V2 carte** : dégradé plus travaillé, cadre fin façon `.essentiel-box`, grand guillemet doré en filigrane pour les citations.
  - **V3 poster** : voile plus léger, teinte duotone couleur, typographie plus grande, masthead réduit à l'icône seule.
  - **V4 hybride** (cadre+guillemet de V2 + typo/teinte de V3), proposé pour trancher une hésitation explicite de l'utilisateur entre V2 et V3.
- **2026-08-13 (tranché)** — V4 retenu comme gabarit définitif, étendu à 4 puis 5 couleurs d'accent.
- **2026-08-14 [FAIT]** — `pub-template-v5-stat.html` créé pour la catégorie chiffre : nouveau gabarit **sans photo**, chiffre en très grand (accent orange, même couleur « chiffre » déjà réservée dans V4), phrase de contexte en dessous. Choix motivé : le chiffre doit être l'élément visuel dominant, pas noyé dans un texte sur une photo.
- **2026-08-17 [FAIT]** — Couleur du chiffre éclaircie après retour utilisateur sur le premier post publié un lundi (`chiffre-2026-08-17`) ; l'image déjà publiée ce jour-là (`assets/social/pub/2026-08-17.png`) a été régénérée avec la nouvelle couleur et recommittée.
- **2026-08-21 [FAIT]** — Refonte du gabarit V5 après analyse comparative avec des comptes concurrents (posts « chiffre choc » sur Instagram) : le gabarit empilait **6 blocs de texte** (pastille, chiffre géant seul, phrase complète qui répétait le même chiffre, attribution, CTA, tagline) contre 2-3 chez les comptes qui performent — et affichait **deux fois le même chiffre** (bloc `.stat` géant + `.hl` dans `.message`).

---

## B080 — Source et crédit de la photo des posts pub

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-13
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
La routine pub **réutilise une photo déjà choisie à la main cette semaine-là pour un article quotidien** (`assets/social/topic-images/{date}.jpg` + son `.json`), avec repli sur la banque de secours pré-validée (B084) si aucune photo n'a été choisie cette semaine-là. **Aucun appel Pexels en direct par cette routine.** Côté crédit : le photographe n'apparaît **jamais dans le texte visible du post** — l'utilisateur l'ajoute lui-même en commentaire du post une fois publié ; la routine consigne le photographe/lien Pexels dans un commentaire HTML invisible (`<!-- credit: ... -->`) en fin de `<description>` du flux, et le redonne en clair dans son résumé final de session pour que l'utilisateur puisse le recopier.

### À faire
- Rien.

### Décisions
- **Conflit identifié le 13 août** (question explicite : « qui choisit l'image ? ») avec la règle non négociable de `fetch_topic_image.py` (« ne choisit JAMAIS automatiquement une image finale [...] la sélection reste toujours un geste humain/en session ») — une routine hebdomadaire autonome ne peut pas chercher et choisir seule sur Pexels sans validation. **Résolu par la réutilisation d'une photo déjà validée**, déjà liée à l'actualité réelle de la semaine.
- **Crédit hors de l'image et hors du texte visible** : décision affinée le 13 août. Auparavant prévu en fin de `<description>` en clair, sur le modèle des légendes sous les photos d'articles (« Photographe / Pexels ») — puisqu'il n'y a pas de page web dédiée à ce post, contrairement aux articles et pages suivi/hebdo.

### Historique
- **2026-08-13 (tranché)** — Source de la photo : réutilisation d'une photo déjà choisie à la main.
- **2026-08-13 (crédit, première version)** — À reporter dans le `<description>` de l'item de `feed-pub.xml`, en fin de texte.
- **2026-08-13 (crédit, précisé le même jour)** — Jamais dans le texte visible du post ; commentaire HTML invisible + rappel en clair dans le résumé de session.

---

## B081 — Catégorie pub « Questions à la communauté »

**Statut:** STANDBY
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-14
**Prochaine action:** Réactiver en la remettant dans la table jour → catégorie si l'utilisateur le souhaite
**Blocage:** Catégorie dormante, volontairement absente de la table jour → catégorie

### État actuel
**Catégorie dormante, pas supprimée** : ses entrées restent dans `docs/pub-messages.md` (section 3), mais elle est volontairement absente de la table jour → catégorie depuis le 14 août (voir B086). Rien ne la publie donc aujourd'hui.

### À faire
- Rien tant qu'elle n'est pas réactivée.

### Décisions
- Vocation : engagement pur, **pas de fait à vérifier** — notamment pour solliciter des idées de sujets pour le mardi « carte blanche ».
- `question-01` (proposer un sujet) retiré le 13 août (retour utilisateur : « on n'en sait rien, les gens scrollent ») et remplacé par `question-04` (« le vrai risque pour la société dans 10 ans »), qui demande un avis plutôt qu'une proposition.

### Historique
- **2026-08-13** — Créée comme 3e section de `docs/pub-messages.md`.
- **2026-08-14** — Sortie de la rotation : absente de la table jour → catégorie, traitée comme dormante.

---

## B082 — Catégorie pub « Le saviez-vous » (chiffre)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Aucune — catégorie active, alimentée automatiquement par extraction depuis les archives
**Blocage:** Aucun

### État actuel
Catégorie active et **auto-alimentée** : elle **extrait un chiffre déjà publié et déjà vérifié** (sources croisées, relecture) directement depuis `archives/*.html` — jamais une génération ou un calcul par la routine, seulement une citation verbatim d'un fait ayant déjà passé le processus éditorial du site. Mécanisme décrit dans `docs/pub-messages.md` section 5 : scan des éditions des ~30 derniers jours, chiffres mis en `<strong>` dans `.dek`/`.essentiel-text`, exclusion des éditions trop récentes (<24h) ou déjà citées, recopie mot pour mot. Section volontairement vide au lancement (pas bloquant, le scan la réalimente à chaque tour). Rendue par `pub-template-v5-stat.html` (B079). Occupe 4 jours sur 7 dans la table jour → catégorie depuis le 21 août (lundi, mercredi, jeudi, samedi — voir B086).

### À faire
- Rien.

### Décisions
- **Différence clé avec la version retirée le 13 août** : l'ancienne liste demandait à l'utilisateur de fournir des chiffres pré-vérifiés un par un (jamais réamorcée, donc **bloquante**). La nouvelle version extrait depuis les archives — ce qui élimine le risque de fait inventé par un LLM, déjà identifié comme raison de retrait de plusieurs entrées le 13 août (`citation-04/09/10`, `chiffre-01/02/03`).
- **Décisions prises avec l'utilisateur le 14 août (3 questions, 3 réponses)** :
  - **Source** : éditions quotidiennes uniquement (`archives/*.html`), jamais les pages de suivi ni le récap hebdo — le contenu le plus dense en chiffres vérifiés, le plus simple à scanner.
  - **Gabarit** : nouveau template dédié plutôt que réutiliser `pub-template-v4-hybride.html`.
  - **Rotation** : 5e catégorie dans le cycle existant, pas un rythme séparé — garde une cadence de publication prévisible.
- Version d'origine (13 août) : un chiffre simple, toujours prolongé par une question prospective à 10 ans (ex. financement des retraites), **toutes les entrées marquées `[chiffre à vérifier]`** au moment de la rédaction (ordres de grandeur de mémoire, pas revérifiés) — aucune ne devait passer en rotation avant vérification sur une source primaire, la crédibilité du site reposant justement sur la justesse des chiffres.

### Historique
- **2026-08-13 (créée)** — 4e section de `docs/pub-messages.md`, alimentée à la main.
- **2026-08-13 (vidée par le nettoyage)** — `chiffre-01/02/03` retirés (retraites, population 2050, +1,5 °C) avec les autres entrées non confirmées. **Conséquence : section bloquante** — pas de mécanisme de recherche à la volée pour cette catégorie (contrairement à `futur`), elle ne publierait rien tant que personne n'y ajoute une entrée vérifiée à la main. `docs/routine-pub-prompt.md` la traite comme n'importe quelle catégorie sans entrée disponible : passée, signalée, jamais bloquante pour le reste du cycle.
- **2026-08-13 (retirée entièrement)** — Retour utilisateur : « on enlève la section chiffres on a assez pour démarrer ». Section supprimée de `docs/pub-messages.md`, cycle réduit à 4 catégories (`manifeste → citation → question → futur`), toutes les références mises à jour dans `docs/routine-pub-prompt.md`. « Grands futurs » renumérotée section 4 (`rotation D`). Réintroductible plus tard.
- **2026-08-14 [FAIT] — réintégrée avec un mécanisme différent** — Retour utilisateur : des pubs automatiques qui reprennent un fait/chiffre fort déjà publié dans une édition (ex. un bilan chiffré d'une canicule), pas une liste à approvisionner à la main. Implémenté : `pub-template-v5-stat.html`, champ `stat` dans `generate_pub_image.py`, section 5 de `docs/pub-messages.md`, et `docs/routine-pub-prompt.md` (cycle à 5 catégories, nouveau point 7 dans l'étape 1 avec la procédure d'extraction complète, étape 2 « photo » sautée pour cette catégorie, étape 3 avec la commande dédiée, table des liens étape 4 mise à jour — `chiffre` → l'édition source elle-même, **seule catégorie sans page de destination fixe**).
- **2026-08-21** — Reprend les jours de `futur` mis en pause : jeudi passe sur `chiffre` (voir B083/B086).

---

## B083 — Catégorie pub « Grands futurs » (futur)

**Statut:** STANDBY
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Réactivable à tout moment si l'utilisateur redonne un jour à `futur` dans la table jour → catégorie
**Blocage:** **Mise en pause le 21 août** (retour utilisateur direct : abandon de « Grand futur » pour l'instant)

### État actuel
**Catégorie dormante, pas supprimée** : le mécanisme de recherche à la volée (étape 1, point 6 de `docs/routine-pub-prompt.md`) et les entrées déjà présentes dans `docs/pub-messages.md` (section 4) restent en place, prêts à être réactivés. Jeudi, son dernier jour, est repassé sur `chiffre`.

### À faire
- Rien tant qu'elle n'est pas réactivée.

### Décisions
- **Objet** : inventions/technologies réelles déjà en développement qui pourraient changer le quotidien (voiture autonome, fusion nucléaire, longévité, informatique quantique...), et grands risques du siècle (climat, IA, pandémie).
- **Règle non négociable : toujours au conditionnel** (« pourrait », jamais « sera »/« va révolutionner ») — même exigence épistémique que le reste du site (une probabilité n'est jamais une certitude).
- **Vigilance particulière sur le survol technologique (« hype »)** : un secteur avec un long historique d'annonces « dans 10 ans » jamais tenues (quantique, fusion...) — exiger un vrai jalon concret déjà atteint, pas seulement une promesse marketing. Et vigilance dans les deux sens : **ni hype ni alarmisme**.
- **Seule catégorie autorisée à chercher à la volée (13 août)** — retour utilisateur direct : « je ferai pas une liste ferme sinon ça tourne et c'est boring ». Contrairement aux 4 autres catégories (banque curée, jamais de génération par la routine), `futur` peut chercher un nouveau fait à chaque tour (**WebFetch, 3 appels max, uniquement 1 fois sur 5 dans le cycle**). Garde-fous : toujours une vraie source vérifiée avant d'écrire (jamais une invention libre), repli sur la liste existante si la recherche ne trouve rien de solide, nouvelle entrée toujours ajoutée avec sa source (URL) dans `docs/pub-messages.md` — la banque grandit organiquement plutôt que de tourner en boucle sur un stock figé. **Seule catégorie de toute la routine pub où une vraie recherche LLM est nécessaire** — accepté comme coût raisonnable vu que ça ne se déclenche qu'1 fois sur 5, et que le risque (mauvais fait publié en post social) est bien plus faible que sur l'Inspecteur, qui édite le site lui-même.
- **Règle ajoutée au prompt** : si un lecteur qui suit un peu l'actualité tech/science hausse les épaules (« ça, je le savais déjà »), l'entrée est à refaire.
- **Une section vide au départ est son état normal, pas une anomalie** — contrairement à la catégorie chiffre dans sa version du 13 août.

### Historique
- **2026-08-13 (créée)** — 5e catégorie ; cycle de rotation étendu à 5 ; 5e couleur d'accent ajoutée au gabarit V4, violet (`--futur: #9b7fc0`), pour ne pas se marcher sur les 4 couleurs déjà prises. Toutes les entrées marquées `[à vérifier]`, même discipline que la section chiffres.
- **2026-08-13 (réécriture complète)** — Retour utilisateur : « pas de trucs bateau, pas besoin d'écrire des trucs que tout le monde sait ». Les 7 entrées initiales (voiture autonome, fusion en général, longévité en général, quantique en général, climat « risque n°1 », IA « hors de contrôle », pandémie générique) jugées trop génériques/déjà connues. Remplacées par des faits **précis, datés, spécifiques** : le premier gain net de fusion (déc. 2022, NIF), la bio-impression de tissus vivants, les interfaces cerveau-machine déjà testées sur des patients réels, les vaccins ARNm anti-cancer en essai, des IA prises à tricher lors de tests contrôlés, le retrait d'assureurs américains des zones à risque climatique, la surveillance de virus zoonotiques (« maladie X » de l'OMS).
- **2026-08-13 (mécanisme changé dans la foulée)** — Plus une liste fermée pour cette catégorie : recherche à la volée autorisée.
- **2026-08-13 (vidée par le nettoyage)** — `futur-01` à `futur-07` retirées, remplacées par de simples exemples de calibrage dans la prose, plus des entrées prêtes à publier. **Pas bloquant** : c'est justement la catégorie conçue pour repartir de zéro et se réapprovisionner elle-même.
- **2026-08-21** — Mise en pause, traitée comme `question` (dormante, pas supprimée). Mis à jour : `docs/routine-pub-prompt.md` (en-tête + étape 1, point 2 et l'exception `futur` de la section « Économie de tokens »), `docs/pub-messages.md` (section 4 + « Règle de rotation »).

---

## B084 — Banque de secours de photos pour les posts pub

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-13
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
`assets/social/pub-photos/` : **un paysage par registre (7 photos Pexels)**, recherchées et proposées en session, **validées par l'utilisateur avant commit — jamais un choix automatique**. Crédits dans `assets/social/pub-photos/credits.json`. Sert aussi de repli à la routine quotidienne pour l'image du sujet (voir B027) et au point 9 de l'Inspecteur.

### À faire
- Rien.

### Décisions
- **Premier jet écarté par l'utilisateur** : « des paysages plus beaux, ça fait rêver, pas des ordis/tours » — bureau de labo, gros plan de journal, tours de Paris la nuit jugés pas assez « dreamy ».
- **Deuxième jet retenu, uniquement des paysages** : Europe la nuit vue de l'espace (géopolitique), route ouverte vers l'horizon (carte blanche), Alpes au coucher de soleil (actualité française), porte-conteneurs sur la mer dorée (économie mondiale), aurore boréale (sciences), amphithéâtre antique au soleil couchant (culture), coureurs en silhouette au coucher de soleil (sport).

### Historique
- **2026-08-13 [FAIT]** — Banque constituée en deux jets.

---

## B085 — `citation-13` (Einstein) : vérifier sérieusement avant toute réintégration

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-13
**Prochaine action:** Décider si la citation doit être vérifiée sérieusement puis réintégrée — c'est le seul reste à faire du chantier routine pub (B078)
**Blocage:** Attribution non vérifiée

### État actuel
Retirée de `docs/pub-messages.md` le 13 août, **malgré la demande explicite de l'utilisateur de l'ajouter plus tôt dans la journée**. Motif : son statut de citation la plus fréquemment mal attribuée à Einstein en ligne reste inchangé. Citation concernée : « Dieu qui se promène incognito ».

### À faire
- Vraie vérification d'attribution, puis réintégration si le résultat le permet.

### Décisions
- À ré-ajouter **seulement après** une vraie vérification, si souhaité.

### Historique
- **2026-08-13** — Ajoutée sur demande, puis retirée le même jour avec les autres entrées non confirmées.

---

## B086 — Sélection de la catégorie pub : table jour → catégorie

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Table explicite jour → catégorie (état au 21 août) :

| Jour | Catégorie |
|---|---|
| Dimanche | `manifeste` |
| Lundi | `chiffre` |
| Mardi | `citation` |
| Mercredi | `chiffre` |
| Jeudi | `chiffre` |
| Vendredi | `manifeste` |
| Samedi | `chiffre` |

`question` et `futur` sont volontairement absentes (catégories dormantes, voir B081/B083).

### À faire
- Rien.

### Décisions
- **Table explicite plutôt qu'un cycle qui avance** (14 août, retour utilisateur : « voici le calendrier systématique, tu ne pourras pas te perdre ») : l'ancien mécanisme (déduire la catégorie suivante à partir du dernier `<guid>` publié dans `feed-pub.xml`, puis avancer d'un cran dans un cycle fixe) marchait mais restait une inférence à chaque exécution, donc un point de fragilité évitable. Même principe que le calendrier des éditions quotidiennes (`docs/routine-prompt.md`).
- **Un jour de calendrier par jour de trigger** : aucun jour de la table n'est orphelin de déclenchement, et inversement.

### Historique
- **2026-08-14 [FAIT]** — Table créée avec 5 jours (Dimanche `manifeste`, Mardi `citation`, Jeudi `futur`, Vendredi `manifeste`, Samedi `chiffre`) et le trigger « Scénario — Pub hebdo » passé le même jour à **5×/semaine** (`0 16 * * 0,2,4,5,6` UTC — dimanche, mardi, jeudi, vendredi, samedi). Mis à jour : `docs/routine-pub-prompt.md` (étape 1, point 2), `docs/pub-messages.md` (section « Règle de rotation »).
- **2026-08-21 [FAIT]** — Jeudi passe de `futur` à `chiffre` (mise en pause de `futur`, B083). *(La table publiée le 21 août comporte 7 jours, dont lundi et mercredi sur `chiffre` — évolution non détaillée ailleurs dans le backlog d'origine.)*

---

## B087 — Planning horaire des routines automatiques

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-14
**Prochaine action:** Aucune côté planning. Reste lié : avancer la routine Daily à 6h Paris demandait un geste utilisateur (voir B077/B108) — au 14 août, Daily figure à 6h dans le planning
**Blocage:** Aucun

### État actuel
Planning, toutes routines Scénario confondues :

| Heure Paris | Routine | Trigger | Cron UTC |
|---|---|---|---|
| 0h00 | Détection sujets à suivre | `trig_01BYYviSQge2CDcYkzBbYcjT` | `0 0 * * 1,4,5,6` |
| 2h00 | Pub hebdo | `trig_01A1XU5Kpc4QWzApjZPqcKpj` | `0 2 * * 0,2,4,5,6` |
| 6h00 | Daily (routine éditoriale principale) | `trig_0176spj7P7E9fyTs1XBkQBWF` | `0 4 * * *` *(inchangé)* |
| 7h00 | Inspecteur | `trig_015wbeqHwALMg3EsUaZcRoWp` | `0 5 * * *` |

Autres triggers connus, hors de ce tableau : routine hebdo `trig_01SE6daCsV38jPUXf82DC7TF` (dimanche 14h Paris, voir B107) — un autre identifiant, `trig_01FwX1Q3xsLCMwAZt4WviUA6`, est également cité comme celui de la routine hebdo dans ce backlog (voir B049) ; **incohérence non résolue dans la source**. Routine « Scénario — Audience », hebdomadaire (voir B148).

### À faire
- Rien.

### Décisions
- **Motif** : retour utilisateur direct — « est-ce que la routine pub etc peuvent tourner la nuit pour ventiler la charge ». Avant ce changement, Pub hebdo et Détection tournaient toutes les deux en soirée (18h et 20h Paris), proches l'une de l'autre et de la fin de journée ; Daily (6h) et Inspecteur (6h50) restaient groupées le matin.
- **Ordre choisi** pour garder un espacement régulier (2h entre chaque) tout en respectant les deux ancres demandées par l'utilisateur (Daily 6h, Inspecteur 7h) et en gardant les mêmes jours de la semaine qu'avant pour Pub et Détection (seule l'heure change).

### Historique
- **2026-08-14 [FAIT]** — Nouveau planning appliqué. Mis à jour : `docs/routine-pub-prompt.md`, `docs/routine-detection-prompt.md`, `docs/routine-inspection-prompt.md` (en-têtes).
---

## B088 — Heatmap « Le monde en ce moment » par domaine

**Statut:** À FAIRE
**Priorité:** P2
**Dernière MAJ:** 2026-08-12
**Prochaine action:** Trancher le mode de génération : job mensuel dédié (nouveau trigger Claude Code Remote) vs page 100 % JS qui recalcule à la volée depuis les pages déjà publiées
**Blocage:** Aucun techniquement — la formule et l'attribut machine-lisible existent déjà (voir B089)

### État actuel
**Toujours pas implémentée en tant que heatmap.** La méthode de calcul est entièrement posée, et la formule elle-même a été reprise et implémentée **par article** le 12 août (voir B089, « France Impact »), ce qui prépare le terrain sans construire ce chantier.

### À faire
- Trancher le mode de génération (job mensuel vs page JS).
- Construire l'agrégation par domaine et l'affichage.

### Décisions
- **Question recentrée** : partie d'une simple agrégation de jauges, l'idée a été recentrée sur une question plus précise et plus utile — **ce domaine (géopolitique, économie, tech...) est-il en ce moment plutôt favorable ou défavorable pour la France ?** Un score par domaine, mis à jour **mensuellement** (pas besoin de fraîcheur quotidienne pour une vue d'ensemble).
- **Méthode de calcul retenue (espérance mathématique, pas un simple choix de case)** :
  1. Chaque carte de scénario se termine, en pratique, par une phrase fixe — vérifié sur l'édition du 10 août, les 3 cartes finissent bien par exactement l'une de ces 3 formes : *« → Plutôt favorable pour la France. »* / *« → Neutre pour la France. »* / *« → Plutôt défavorable pour la France. »* Habitude de rédaction déjà là, **pas encore imposée formellement** dans `docs/routine-prompt.md` à l'époque — à corriger : rendre cette formule de clôture obligatoire, toujours l'une des 3, plus un attribut machine-lisible `data-france-impact="favorable|neutre|defavorable"` sur `.france-line` pour ne pas avoir à reparser du texte libre au moment du calcul mensuel. *(Fait le 12 août, puis `neutre`/`stable` retiré des valeurs possibles le 17 août — voir B089.)*
  2. Valeur par scénario : Favorable = +1, Neutre = 0, Défavorable = −1. *(Devenue strictement binaire +1/−1 le 17 août.)*
  3. **Score du sujet = Σ (probabilité du scénario × valeur France de ce scénario)** — une vraie espérance, pas juste la valeur du scénario le plus probable. Exemple réel avec l'édition du 10 août (20 % favorable / 55 % stable-neutre / 25 % dégradé-défavorable) : `(0,20×+1) + (0,55×0) + (0,25×−1) = −0,05` — proche de zéro, légèrement négatif, cohérent avec « surtout stable, avec un risque de queue ».
  4. **Score du domaine = moyenne des scores de tous les sujets actifs de ce domaine** (suivis actifs + éditions récentes sans suivi dédié) — la moyenne redevient pertinente maintenant que le score par sujet est un nombre continu entre −1 et +1, pas une catégorie (**piste initiale « prendre le plus récent » abandonnée pour cette raison**).
  5. Affichage : un score par domaine sur une échelle continue, coloré (rouge vers −1, gris vers 0, vert vers +1) — **pas de matrice à deux axes** (Monde vs France envisagé un temps, simplifié : uniquement l'angle France, plus lisible et plus utile).
- **Recombine des données déjà publiées** (probabilités déjà calculées, ligne France déjà écrite) : le seul vrai ajout était la formalisation de la formule de clôture + l'attribut machine-lisible, pas un nouveau pipeline de recherche.

### Historique
- **2026-08-10** — Idée (brainstorm « out of the box »), méthode affinée en discussion le jour même.
- **2026-08-12** — La formule est reprise et implémentée par article (B089) ; la heatmap par domaine reste à faire.

---

## B089 — France Impact (ex « Δ France ») — indice de sens pondéré pour la France

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-17
**Prochaine action:** Aucune. Deux points laissés ouverts : `feed.xml` du 17 août non corrigé (à trancher séparément si besoin) ; badge non implémenté sur le gabarit Instagram par défaut
**Blocage:** Aucun

### État actuel
Indice affiché dans le bloc « L'essentiel » de chaque édition, calculé par la formule d'espérance `score = Σ probabilité × valeur` (voir B088), **valeur France strictement binaire (+1 favorable / −1 dégradé, jamais 0)** depuis le 17 août, jugée indépendamment pour chaque scénario. `data-france-impact` n'accepte plus que `favorable|degrade`. Nom visible : **« France Impact »**, phrase visible : **« Notre évaluation de l'impact pour la France : {mot}. »** — jamais raccourcie. Le chiffre brut n'est jamais montré au lecteur, seuls le mot et la jauge le sont. Échelle : sens toujours signé + intensité — `|score| < 0,30` → « léger », `0,30-0,50` → « assez », `≥ 0,50` → « très » (ex. « léger négatif », « assez positif »). Sur la page : jauge en arc continu `.delta-france`/`.delta-gauge*` (dégradé SVG rouge→or→vert, repère positionné par script via `data-score` sur `.delta-gauge-marker`), mot du sens affiché **à la fois** dans la jauge (`.delta-gauge-word`, en flux normal sous l'arc) **et** coloré dans la phrase (`<span class="delta-word">`, couleur via `data-kind`), plus un petit drapeau 3 bandes devant la phrase. Sur l'image Instagram : badge « France Impact » avec drapeau en icône de label, **échelle fixe à 6 étoiles** remplies cumulativement de gauche à droite (1 = très défavorable … 6 = très favorable), **couleur uniforme selon le sens du jour** (rouge `_DEGRADE_HEX` si négatif, vert `_FAVORABLE_HEX` si positif, jamais mélangées), et une légende « Notre évaluation » entre les étoiles et le mot en gros. Les identifiants internes (`delta-france`, `delta-gauge*`, `build_delta_badge()`...) gardent « delta », seul le texte visible a changé.

### À faire
- **`feed.xml` du 17 août non corrigé** (texte dupliqué dans `<source>`, probablement déjà consommé par les canaux sociaux/newsletter du matin au moment de la correction) — à trancher séparément si besoin.
- **Badge implémenté uniquement sur `instagram-photo-template.html`, pas sur le gabarit par défaut** (`instagram-template.html`, celui de la routine automatique) : testé, le budget vertical/horizontal du gabarit par défaut est déjà tendu par le titre (1-3 lignes selon le jour), risque de chevauchement non vérifié. Cohérent avec le statut déjà manuel/optionnel de `--photo` — la routine quotidienne automatique n'est pas affectée.
- **Limite connue et assumée, pas résolue** : aucun garde-fou technique contre les biais méthodologiques (au-delà de la règle écrite dans `docs/routine-prompt.md`) — « de la documentation, pas du code, ne protège pas d'un oubli » (point soulevé par l'utilisateur).

### Décisions
- **Appliqué par article**, pas par domaine — demande explicite de l'utilisateur le 12 août (« je veux un truc super simple »).
- **Nom** : « Δ France » (delta) retenu initialement ; « Boussole France » rejeté (« trop bateau ») ; alternatives écartées : « Le Poids France » (plus parlant mais moins distinctif), « La Jauge France » (confusion possible avec les jauges existantes par scénario). **Renommé « France Impact » le même jour**, après un brainstorm de l'utilisateur avec ChatGPT sur le visuel de la carte image.
- **Échelle, décidée après calibrage sur les 5 éditions qui avaient déjà « L'essentiel » (8-12 août)** : un premier seuil à ±0,3 ne différenciait rien (les 5 scores réels tombaient tous entre +0,05 et −0,20) — **seuil resserré à ±0,10**, et **pas de case « neutre »** (retour utilisateur : jugée non informative), remplacée par un sens toujours signé + une intensité.
- **Limite méthodologique posée par l'utilisateur et actée avant l'implémentation** : le score compare valablement le *sens et l'ampleur pondérés* entre sujets (deux scores proches = deux sujets qui penchent pareil), mais **ne mesure jamais l'enjeu réel** — un −0,15 sur un dossier économique n'est pas « aussi grave » qu'un −0,15 sur un conflit géopolitique. **Jamais de classement ni de « pire score du mois » construit à partir de ce seul chiffre.**
- **Biais discutés et acceptés en connaissance de cause** : la formule est symétrique (+1/−1) alors que gains et pertes réels ne le sont pas forcément (risque de queue) ; la classification favorable/stable/dégradé de chaque scénario reste un jugement éditorial, le chiffre lui donne une précision qu'elle n'a pas vraiment.
- **Correction du 17 août — la valeur France de « stable » n'était pas censée être 0 par défaut** : deux questions différentes, à ne plus confondre — la **nature du scénario** (favorable/stable/dégradé) dit *où va* la situation ; la **valeur France** dit si l'état qui en résulte est bon ou mauvais pour la France. **Un statu quo qui maintient un coût déjà là n'est jamais neutre.**
- **Pas de retrofit** sur les archives antérieures au 17 août pour le score comme pour le repère visuel ; l'édition du 12 août avait servi de test réel, sans retrofit sur les archives 8-11 août.
- **Découpage de `.essentiel-box`** en plusieurs `<p class="essentiel-text">` (un par item : problématique / contexte / conclusion / signal à surveiller) au lieu d'un seul bloc — demande utilisateur explicite (« il faut découper en paragraphe »).
- **`data-france-impact` plutôt que du parsing de texte libre** : calcul fiable — le texte des `.france-line` varie beaucoup d'une édition à l'autre, vérifié sur les 20 archives, **55 sur 105 ne suivaient pas une formule figée**.
- **Couleurs SVG toujours en hex fixe** (`_FAVORABLE_HEX`/`_DEGRADE_HEX`), pas en `var(--x)` : un attribut `fill="var(--x)"` sur un `<path>` généré côté serveur ne se résout pas de façon fiable hors d'un attribut `style` — bug testé et évité.

### Historique
- **2026-08-12 [FAIT]** — Implémenté : `index.html` (CSS `.delta-france`/`.delta-gauge*`, jauge en arc continu, même géométrie que les jauges `.gauge` par scénario ; `.essentiel-box` découpée ; `data-france-impact="favorable|stable|degrade"` sur chaque `.france-line`). Appliqué à l'édition du 12 août (score réel : 20/45/35 → **−0,15** → « léger négatif »). `feed.xml` : même texte dans `<source>`, découpé en paragraphes séparés par de vrais doubles retours à la ligne (pas de `<br>`, aucune balise XML ajoutée — structure du flux inchangée comme demandé) + paragraphe Δ France ajouté à la fin — **corrige au passage l'illisibilité des légendes Instagram/LinkedIn/Facebook** qui reprenaient `{{4.source.title}}` en un seul bloc de 700+ caractères. `docs/routine-prompt.md` : étape 3 réécrite avec le gabarit HTML complet, la méthode de calcul, l'échelle, la portée (jamais de classement), et le format `<source>` en paragraphes.
- **2026-08-12 — badge sur l'image Instagram, demande utilisateur (« ça apporterait du sens et de l'accroche »)** : `__DELTA_BADGE__` ajouté à `scripts/social/generate_instagram_image.py` (champ optionnel `data["delta"] = {"direction": "positif|negatif", "label": "..."}`, repli silencieux si absent, même logique que `--photo`). **Treize itérations visuelles, sur retours utilisateur successifs le même jour** :
  1. Pastille texte + bordure fine — jugée « pauvre ».
  2. Disque tricolore avec flèche découpée dedans (masque SVG), en bas à gauche — visuel jugé bon, mais mauvais emplacement, « pas moderne ».
  3. Triangle tricolore en haut à droite (coin libre, le masthead occupe le haut à gauche) : `clip-path: polygon(100% 0, 100% 100%, 0 0)` sur un dégradé diagonal bleu/blanc/rouge, grosse flèche ▲/▼ à l'intérieur + petit texte « Δ France ». **Retour utilisateur : trop « drapeau », évoque une esthétique identitaire (« France d'abord ») non désirée — même discret par la taille, le drapeau plein cadre reste trop connoté.**
  4. Marque discrète sans imagerie nationale — abandon total du drapeau, petit anneau fin (~60px) avec flèche ▲/▼ pleine, couleur `--favorable`/`--degrade`, texte « Δ France » en petit dessous. **Retour utilisateur : trop petit, « pas très professionnel ».**
  5. Carte, même recette que `.essentiel-box`/`.list-box` (fond surface semi-opaque, bordure fine, ombre légère) — reprend l'anneau + flèche de l'itération 4 mais dans un vrai conteneur avec le mot affiché en grand à côté (Fraunces, gras, couleur accent). **Retour positif sur la carte, mais ré-ouvert le jour même** après un brainstorm avec ChatGPT sur un système d'étoiles d'intensité + un petit drapeau.
  6. « France Impact » — drapeau en icône de label + 3 étoiles d'intensité pleines/vides (une seule couleur à la fois, côté favorable ou dégradé). **Retour utilisateur : seules 3 étoiles ne montrent qu'un seul côté à la fois — « l'échelle doit toujours être la même quelle que soit la situation ».** *(Contrat JSON figé à partir d'ici : `data["delta"]` porte `direction`/`intensity` (1-3)/`label`.)*
  7. Échelle fixe à 6 étoiles avec une seule étoile visée + flèche qui pointe dessus (les 5 autres grises). **Retour utilisateur : mauvaise lecture — « ici c'est très positif, tout doit être coché, tu dois avoir les six ».** L'utilisateur voulait un remplissage **cumulatif**.
  8. Remplissage cumulatif de gauche à droite sur une position 1-6 unique — les étoiles `1..position` pleines, le reste gris, plus de flèche isolée. Mais couleur figée par index (0-2 rouge, 3-5 vert) : un score « léger favorable » (position 4) affichait 3 étoiles rouges + 1 verte. **Retour utilisateur : pas de mélange — toutes rouges si négatif, toutes vertes si favorable.**
  9. **[retenu]** Couleur des étoiles pleines = **sens du jour**, pas la position. La position 1-6 détermine toujours **combien** d'étoiles sont pleines, mais leur couleur est uniforme. `_delta_scale_positions()` calcule les coordonnées x — un écart d'abord un peu plus large entre l'étoile 3 et l'étoile 4, **retiré le jour même** (retour utilisateur : « pas besoin »), espacement régulier sur les 6 depuis.
  10. **[retenu]** Mécanisme confirmé (6 étoiles, 1-3 dégradé / 4-6 favorable) + **clarification du message : « notre évaluation », pas un fait.** Retour utilisateur : ambiguïté sur ce que « France Impact : léger négatif » affirme — est-ce la question posée par le sujet qui est favorable/défavorable, ou l'appréciation de la rédaction ? Corrigé à 3 endroits en même temps : **page + feed** (la phrase passe de « France Impact : {mot}. » à « **Notre évaluation de l'impact pour la France : {mot}.** », jamais raccourci en retour, règle explicite ajoutée à `docs/routine-prompt.md`) ; **image** (légende « Notre évaluation » en petites capitales, discrète, ajoutée entre les étoiles et le mot en gros — le nom « France Impact » reste en haut pour identifier l'axe mesuré, la légende clarifie que ce qui suit est une appréciation, pas une mesure). Le mécanisme des étoiles lui-même n'a pas changé — confirmé correct par l'utilisateur, seule la clarté du message était à retravailler.
  11. **[retenu]** Bugs d'affichage repérés sur la page réelle (capture d'écran fournie par l'utilisateur) + petit drapeau ajouté sur la page. Trois corrections sur `.delta-france`/`.delta-gauge*` dans `index.html` :
      - **Mot du repère (« LÉGER NÉGATIF ») débordant de la jauge** — il vivait en légende sous l'arc dans le flux normal, ce qui le faisait déborder de la boîte de 108px. Repositionné en `position: absolute` **dans le creux de l'arc** (même principe que `.gauge-num` des cartes) — d'abord élargi avec un offset négatif (ce qui aggravait le débordement, corrigé), puis réduit en taille de police pour tenir sur une seule ligne.
      - **Colonne de texte trop étroite à certaines largeurs d'écran** (capture utilisateur avec police système agrandie — le seuil fixe `@media (max-width: 480px)` ne se déclenchait pas dans ce cas, le texte se retrouvait compressé mot par mot à côté de la jauge). Remplacé par `.delta-france{ flex-wrap: wrap }` + `.delta-text{ flex: 1 1 220px; min-width: 220px }` — le texte repasse sous la jauge dès qu'il manque de place, quelle que soit la cause (largeur d'écran, zoom, taille de police système), plus robuste qu'un seuil fixe. Testé à 390/500/600/900px.
      - **Petit drapeau ajouté devant « Notre évaluation... »** dans le paragraphe (suggestion utilisateur, même drapeau 3 bandes que sur l'image) — cohérence visuelle page/image.
      **Répercuté sur `archives/2026-08-12.html`** (pas seulement `index.html`) suite à une question directe de l'utilisateur (« tu le mets sur index et archive du jour ? ») : l'archive du jour datait de ce matin, avant l'ajout de France Impact **et** de `.list-box` (chantier des sorties cinéma, même journée) — les deux CSS étaient absentes, ainsi que la mise à jour de la grille des registres (dimanche/lundi/samedi). **Resynchronisé chirurgicalement** (CSS, attributs `data-france-impact`, bloc essentiel, JS, objet `registres`) plutôt que de réécrire le fichier depuis `index.html`, pour ne pas casser les chemins relatifs `../` propres à `archives/` — diff final vérifié : ne restent que les différences légitimes (canonical/OG, nav `aria-current`, lien `.dek` sans préfixe `archives/`).
  12. Mot du sens retiré de la jauge, coloré directement dans la phrase — retour utilisateur : « léger négatif » apparaissait deux fois (légende sous la jauge + dans la phrase), redondant. `.delta-gauge-word` supprimé, mot déplacé en `<span class="delta-word">` coloré via `data-kind`. **Retour utilisateur, le jour même : reconsidéré — « tu peux pas mettre léger négatif à l'intérieur de la jauge sur 2 lignes ? »**
  13. **[retenu]** Le mot revient dans la jauge, **en plus** du mot coloré dans la phrase — les deux, pas l'un ou l'autre. `.delta-gauge-word` réintroduit, mais cette fois **en flux normal sous l'arc** (plus en `position: absolute`) avec `.delta-gauge` élargi à 78px de hauteur (64px pour l'arc + place réservée pour le mot) — wrap naturel sur autant de lignes que nécessaire dans les 108px de large, jamais de `nowrap` ni d'offset négatif (les deux avaient causé les débordements précédents). Répercuté sur `archives/2026-08-12.html` et `docs/routine-prompt.md` en même temps qu'`index.html`, comme pour l'itération 11.
- **2026-08-17 [FAIT] — biais corrigé sur la valeur France de « stable ».** Un des biais « acceptés en connaissance de cause » s'est concrètement matérialisé : l'édition du 17 août (détroit d'Ormuz) classait son scénario stable « Neutre pour la France » alors que son propre texte disait « facture énergétique élevée » — la valeur France avait été déduite mécaniquement de la nature du scénario (stable → 0) au lieu d'être jugée sur l'état réel décrit. Retour utilisateur direct, avec l'exemple du jour à l'appui. **Formule changée** (valeur binaire), `data-france-impact` restreint. Mis à jour : `docs/routine-prompt.md` (étape 3, règle complète + cet exemple), `docs/methodologie-probabilites.md` (renvoi). **Corrigé rétroactivement sur `index.html` et `archives/2026-08-17.html`** (seul cas concerné) : score **−0,45 (« assez négatif ») → −0,80 (« très négatif »)**, `.france-line` du scénario stable passée en `data-france-impact="degrade"` / « Plutôt défavorable pour la France. »
- **2026-08-17 — repère visuel favorable/défavorable ajouté sur `.france-line`** (même jour), retour utilisateur : la classification devait « rester pro et discret mais voyant rapidement », pas seulement lisible dans le texte. Filet de couleur à gauche du bloc + flèche colorée dans la phrase (`↑`/`↓` remplaçant le `→` générique), tous deux pilotés par `data-france-impact` — **aucun emoji** (cohérent avec le refus des emoji sur les scénarios, 14 août), **pas de nouvelle classe CSS** : la flèche réutilise `.evo-arrow.is-up`/`.is-down`, déjà en place pour les indicateurs chiffrés. Appliqué sur `index.html` et `archives/2026-08-17.html`, gabarit documenté dans `docs/routine-prompt.md`.
- **2026-08-20** — `FRANCE_ESPERANCE_SCALE` resserré une fois (mentionné le 2 septembre comme antériorité, voir B073).

---

## B090 — Carte de pari partageable, sans backend

**Statut:** À FAIRE
**Priorité:** P3
**Dernière MAJ:** 2026-08-10
**Prochaine action:** Chiffrer le design de la carte et le calcul de la date de clôture
**Blocage:** Aucun

### État actuel
Pas chiffré. Idée : une URL du type `parier.html?edition=2026-08-10&choix=stable` générant une carte « j'ai parié sur Stable, reviens le {date de clôture} pour voir si j'avais raison » — état encodé entièrement dans l'URL (query string), aucune base de données, compatible avec le principe zéro-backend du site. Transforme un lecteur passif en participant avec une raison concrète de revenir, et crée un objet naturellement partageable. Joue sur la même mécanique « deviner avant de savoir » déjà au cœur du site (vote Telegram).

### À faire
- Design de la carte (probablement même moteur HTML/CSS→capture que les cartes Instagram).
- Calcul de la date de clôture (**pas toujours définie** pour un sujet suivi).

### Décisions
- Aucune.

### Historique
- **2026-08-10** — Idée (brainstorm « out of the box »).

---

## B091 — Confronter les probabilités à un vrai marché de prédiction

**Statut:** À FAIRE
**Priorité:** P3
**Dernière MAJ:** 2026-08-10
**Prochaine action:** Aucune planifiée
**Blocage:** Aucun

### État actuel
Pas implémenté. Idée : quand un marché liquide existe sur le sujet du jour (Polymarket, Metaculus, Kalshi...), ajouter une ligne du type « Le marché de prédiction {nom} donne {X} % — nous {Y} %. » Validation externe, différenciant.

### À faire
- Tout.

### Décisions
- **Explicitement opportuniste, jamais systématique** : ne marche que pour certains sujets (géopolitique, financier surtout) ; **pas de recherche supplémentaire imposée à la routine du matin** si rien de pertinent n'existe — même logique de repli silencieux que pour la photo Pexels du sujet (B027).

### Historique
- **2026-08-10** — Idée (même brainstorm).

---

## B092 — Page de calibration (« avions-nous raison, au global »)

**Statut:** BLOQUÉ
**Priorité:** P3
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Revisiter dans plusieurs mois, une fois que `suivi/` aura accumulé assez de cas résolus
**Blocage:** **Volume** — pas encore assez de clôtures pour que la statistique ait un sens. Vérifié le 27 août : **aucun suivi n'a encore été clôturé** (`docs/sujets-a-suivre.md` ne liste qu'une clôture visée, en septembre 2026, pas encore atteinte). Partage aussi le prérequis « export structuré scénario ↔ résultat réel » avec B142 et B062

### État actuel
Bloqué par le volume, pas par l'absence d'idée. Au 27 août : le dépôt a 6 semaines d'existence (35 éditions depuis le 18 juillet, 7 suivis actifs), zéro suivi clôturé.

### À faire
- Construire la vraie **courbe de calibration** façon prévisionnistes sérieux : parmi tous les scénarios résolus (pages `suivi/` clôturées), regrouper par tranche de probabilité annoncée (ex. « 70-80 % ») et montrer le taux de réalisation réel observé dans cette tranche.

### Décisions
- **Différent d'une simple statistique « X % de bons scénarios »**, déjà écartée comme trop simpliste dans la revue du 10 août (voir B052).
- Transparence que quasiment aucun média ne pratique, cohérente avec l'identité méthodologique du site.
- Sera une future brique du dashboard interne (voir B148/B149) le jour où le prérequis est levé, **pas un chantier séparé**.

### Historique
- **2026-08-10** — Idée (même brainstorm).
- **2026-08-27** — Rattachée à l'audit externe, classée « bloqué par le volume », vérification du nombre de clôtures faite.
- **2026-09-02** — Reclassée dans le dashboard comme KPI « niveau 4 : pas encore possible, déjà connu du backlog ».

---

## B093 — Arabie saoudite / sport — dossier ouvert (à surveiller)

**Statut:** FAIT (à confirmer)
**Priorité:** Non chiffrée — dossier ouvert, pas une tâche
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Vérifier l'état réel du suivi : le fichier `suivi/arabie-saoudite-sport.html` est cité comme existant au 15 août, alors que l'entrée d'origine du 3 août le présentait comme « candidat mis en attente » — **statut incertain, à confirmer**
**Blocage:** Aucun

### État actuel
Entrée d'origine (3 août) : candidat à une première page de suivi (retrait du financement LIV Golf par le PIF, tension avec l'investissement massif dans le football), **mis en attente volontairement** pour accumuler plus de développements avant de lancer une première page. La routine hebdo de veille (« Détection sujets à suivre », B123) devait le re-signaler si ça bougeait. **Mais** une page `suivi/arabie-saoudite-sport.html` est citée le 15 août comme existante et corrigée rétroactivement (voir B115), donc le suivi a bien été lancé entre-temps — cet épisode n'est pas journalisé dans le backlog d'origine.

### À faire
- Confirmer l'état du suivi et, si besoin, clore ce dossier au profit du ticket de suivi normal.

### Décisions
- Mise en attente volontaire le 3 août plutôt qu'un lancement immédiat.

### Historique
- **2026-08-03** — Dossier ouvert, mis en attente volontairement.
- **2026-08-15** — `suivi/arabie-saoudite-sport.html` et son item `feed-suivi.xml` corrigés rétroactivement pour appliquer la règle « ouvrir par le fait concret » (voir B115) : « 🎯 LIV Golf trouve un nouvel investisseur, +20 points (45 %) » plutôt que « 🎯 Le retrait se fait proprement, +20 points (45 %) » — la page existe donc à cette date.

---

## B094 — Idées explicitement écartées (ne pas reproposer sans nouvel élément)

**Statut:** ABANDONNÉ
**Priorité:** —
**Dernière MAJ:** 2026-08-09
**Prochaine action:** Aucune — registre de référence, à consulter avant de reproposer une idée
**Blocage:** —

### État actuel
Liste de référence des idées écartées, conservée pour mémoire. **Ne pas reproposer sans nouvel élément.**

### À faire
- Rien.

### Décisions
- **Fil d'actualité scrollable façon LinkedIn/Instagram** : pas assez de densité avec 1 édition/jour, sans réel gain vs `archives.html`.
- **Comptes utilisateurs, likes, commentaires sur le site** : coût backend/modération/RGPD trop élevé vs bénéfice ; l'interaction sociale reste sur Telegram. *(Ressorti dans l'audit LLM du 20 août, non reproposé — voir B065.)*
- **WhatsApp Channels** : pas d'API officielle gratuite, seulement des services tiers payants et non garantis par Meta. *(Voir aussi B011 pour la piste WhatsApp Business Cloud API, elle, toujours ouverte.)*
- **Dépôt GitHub privé ou dossier privé séparé pour les docs internes** : coût opérationnel (routine à synchroniser sur deux dépôts) jugé disproportionné vu qu'aucun contenu n'est réellement sensible. *(Précédent invoqué le 2 septembre dans le choix du support du dashboard, voir B148 — avec la nuance que des chiffres d'abonnés/dons sont une catégorie de donnée un peu différente des notes éditoriales internes.)*
- **Remplacer la question posée (`.day-context`) par le texte « L'essentiel » dans le récap hebdomadaire (`hebdo/*.html`)** — proposé et écarté le 9 août : la conclusion de « L'essentiel » ferait doublon avec la liste des 3 scénarios juste en dessous (gagnant déjà en gras via `.is-winner`) ; question gardée, elle sépare proprement la mise en tension (question ouverte) de la résolution (scénarios). **Piste alternative notée si le besoin revient** : reprendre seulement la dernière phrase de « L'essentiel » (l'issue probable + le signal à surveiller), pas le bloc complet.

### Historique
- Liste constituée au fil des décisions, dernière entrée datée du 9 août.

---

## B095 — Emails de la newsletter qui arrivaient en spam

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07-31
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Corrigé le 30 juillet, **confirmé fonctionnel le 31 juillet** : l'édition du jour envoyée correctement depuis `contact@lesscenarios.fr`.

### À faire
- Rien (la réputation d'expéditeur continue de s'améliorer naturellement).

### Décisions
- **Domaine d'envoi dédié `newsletter.lesscenarios.fr`** connecté à Buttondown en **Managed setup** (DNS délégué via 2 enregistrements NS ajoutés côté OVH) — Buttondown gère depuis l'authentification complète (SPF, DKIM, DMARC) de ce sous-domaine.
- **Reply-to configuré vers `scenariocontact75@gmail.com`**, pour que les réponses des lecteurs arrivent réellement quelque part (l'adresse d'envoi elle-même ne reçoit aucun courrier entrant).

### Historique
- **2026-07-30 (constat)** — Premier envoi réel automatisé : plusieurs abonnés recevaient l'édition dans leurs indésirables plutôt qu'en boîte de réception.
- **2026-07-30 [FAIT]** — Corrections appliquées. Réputation d'expéditeur encore neuve (compte tout juste créé), s'améliorant naturellement avec le temps et les ouvertures/clics.
- **2026-07-31** — Confirmé fonctionnel.

---

## B096 — Pipeline Make LinkedIn (RSS `feed.xml` → post LinkedIn)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07-31
**Prochaine action:** Aucune. **Le scénario Make doit rester activé** pour continuer à tourner
**Blocage:** Aucun

### État actuel
Scénario Make : module **RSS** (« Watch RSS feed items », URL `https://lesscenarios.fr/feed.xml`, 1 item max, déclenché **« From now on »** pour ne traiter que les futures éditions, jamais l'historique) → module **LinkedIn « Create a Company Text Post »**, posté sur la **Page LinkedIn « Scenario »** (pas le profil personnel « Les Scenarios », non utilisé pour cet automatisme). Plan Make gratuit, ~30-60 opérations/mois avec une vérification 1×/jour à 10h Paris. *(Ce module a depuis été remplacé par un post Image natif, voir B022.)*

### À faire
- Rien.

### Décisions
- **Make.com plutôt que l'intégration native Buttondown** : l'auto-partage Buttondown ne fonctionne qu'avec un profil **personnel**, pas une Page Entreprise (confirmé via `docs.buttondown.com/linkedin`) — et, cause identifiée le 31 juillet par le support Buttondown (Anita), connecter l'intégration ne suffit pas : il faut configurer une **Automation** dédiée (`buttondown.com/automations`), fonctionnalité réservée au plan **Standard (26 $/mois, jugé trop cher pour ce besoin)**.
- **Vérification 1×/jour plutôt qu'un intervalle court** : Make compte une opération à **chaque vérification**, même sans nouvel item — un polling toutes les 15 min aurait consommé ~1440 opérations/mois, largement au-dessus du quota gratuit de 1000.
- **Contenu du post** : une simple phrase fixe d'intro (« 🔥 Nouvelle édition Scénario, à lire 👇 ») — le reste de l'info est porté par la carte Article, pas la peine de dupliquer titre/lien dans le texte. **Media Type = Article**, avec `Link → URL` = champ `URL` du flux, `Link → Title` = champ `Title`, `Link → Description` = champ `Comments`. Thumbnail laissé vide (LinkedIn récupère l'image Open Graph du site automatiquement).
- **Le champ `Description` brut du flux RSS n'est jamais utilisé directement** : pensé pour l'email, il contient des `<br>` non interprétés par LinkedIn et une invitation à répondre à un email qui n'a pas de sens hors contexte email.
- **Détournement du champ `<comments>`** : le module RSS générique de Make ne reconnaît que les champs standards RSS 2.0 + deux extensions prédéfinies (Google Merchant Center, iTunes) — impossible d'exposer un champ personnalisé arbitraire (testé : un `<scenario:teaser>` avec namespace dédié, **jamais détecté par Make**). Solution : détourner le champ standard `<comments>` (prévu pour un lien vers une page de commentaires) pour y mettre en texte brut la question posée du jour — Make le reconnaît nativement, aucune config supplémentaire. Voir `docs/routine-prompt.md`, étape technique 8.
- **Règle éditoriale de l'étape 2 : la question posée est rédigée une seule fois puis réutilisée mot pour mot** dans l'encart du site, `<comments>`/`<description>` de `feed.xml`, et le teaser Telegram — jamais reformulée différemment d'un endroit à l'autre. Les 4 items déjà publiés au 31 juillet ont été corrigés a posteriori dans `feed.xml` (leur `<comments>` avait dérivé de la vraie question affichée sur le site).
- **Autre règle : le h1 (titre) et la question posée ne doivent jamais être une simple reformulation l'un de l'autre** — constaté sur l'édition du 27 juillet (Iran/USA) où les deux étaient quasi identiques, redondant une fois affichés l'un après l'autre sur LinkedIn.
- **Piège de test à connaître** : la fonction « Rerun/Replay » de l'historique Make **rejoue les données figées au moment de la capture initiale** — si le champ `comments` n'existait pas encore dans `feed.xml` à ce moment-là, le replay l'affiche vide même après correction du flux et de la config. Seul un **vrai nouveau passage RSS** (nouvel item jamais vu) reflète la configuration actuelle. Un flux de test jetable (`feed-test.xml`, supprimé après usage) a servi à valider ça sans attendre le lendemain ni polluer la vraie newsletter.
- Erreur `LinkedIn Content is a duplicate` rencontrée pendant les tests : normale, LinkedIn refuse de reposter un contenu de test identique plusieurs fois — sans rapport avec la config.

### Historique
- **2026-07-30 (reprise en main)** — Constat que rien n'était vraiment actif côté LinkedIn/Instagram. Solution d'abord retenue : profil personnel renommé « Les Scenarios » (Suresnes, Île-de-France), connecté à l'intégration Buttondown, avec un résumé (« About ») réécrit expliquant la genèse et le principe du projet.
- **2026-07-31 (test)** — Envoi du jour : **toujours pas de post créé automatiquement**. Cause identifiée le même jour par le support Buttondown.
- **2026-07-31 [FAIT]** — Solution Make.com retenue et fonctionnelle.
- **2026-08-06** — X (Twitter) ajouté via Buffer sur le même scénario (voir B020).
- **2026-08-11** — Le module LinkedIn du Daily passe en post Image natif (voir B022).

---

## B097 — Identité visuelle de la Page LinkedIn « Scenario »

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07-31
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Page LinkedIn « Scenario » (id `136694258`) habillée, gratuitement (généré en HTML/CSS + capture Playwright, sans outil de design payant), en reprenant fidèlement les couleurs/polices du site (Fraunces + JetBrains Mono, `--gold`, `--favorable`/`--stable`/`--degrade`) et le mark existant (`assets/logo.svg`, le tronc doré qui se divise en trois flèches) :
- Bannière 1128×191.
- Logo carré 300×300 (spec officielle LinkedIn), basé sur le mark existant.
- Texte « Vue d'ensemble » (About, 2000 caractères max) rédigé dans la même voix que `le-projet.html` (aucune ligne éditoriale, sources croisées, Olivier Bertrand).
- **Lien « LinkedIn ↗ » ajouté au footer des 5 pages vivantes** (`index.html`, `archives.html`, `le-projet.html`, `contact.html`, `newsletter.html`), juste à côté du lien Telegram, vers `linkedin.com/company/136694258/`.

### À faire
- Rien.

### Décisions
- Contenu de la bannière volontairement recentré avec de vraies marges : le premier essai était trop proche des bords et empiétait sur la zone où le logo rond de la page se superpose en bas à gauche.
- Comme pour Telegram, le lien de footer fait partie du gabarit recopié chaque matin par la routine — **aucune instruction supplémentaire nécessaire dans `docs/routine-prompt.md`**. **Non ajouté aux pages `archives/*.html` figées**, cohérent avec le choix déjà fait pour Telegram.

### Historique
- **2026-07-31 [FAIT]** — Identité visuelle et lien de footer.

---

## B098 — Faire porter le sondage Telegram sur le sujet du lendemain

**Statut:** À FAIRE
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07-31
**Prochaine action:** Aucune planifiée — **pas systématiquement applicable en l'état**
**Blocage:** La routine ne connaît le sujet du lendemain à l'avance que les jours où il est déjà pré-cadré dans `sujets-prioritaires.md` (avec ses 3 scénarios), pas les jours d'auto-sélection dynamique

### État actuel
Idée notée le 31 juillet, pas implémentée. Objectif : créer un effet d'attente (« reviens demain voir si tu avais raison ») au lieu d'un vote juste avant la révélation immédiate des probabilités.

### À faire
- Trouver comment gérer les jours d'auto-sélection dynamique, ou n'appliquer la mécanique que les jours pré-cadrés.

### Décisions
- Aucune.

### Historique
- **2026-07-31** — Idée notée avec son frein principal.

---

## B099 — Canal Telegram : création, panne d'egress, bascule sur Make

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-01
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Canal public `@scenario_fr`, bot `@scenario_fr_bot` créé via BotFather et ajouté comme administrateur (droit « Publier des messages »). **Pipeline opérationnel via Make**, jamais en appel direct depuis une session : deux modules ajoutés à la suite du RSS dans le même scénario Make que LinkedIn :
- **Telegram Bot → « Send a Text Message »** : `Chat ID` = `@scenario_fr`, `Text` = `Title` + `Comments` + lien `URL`, connexion créée avec le token du bot (`TELEGRAM_BOT_TOKEN`, collé une fois dans Make).
- **Telegram Bot → « Make an API Call »** (pas de module natif « Create a Poll » dans le connecteur Telegram de Make, malgré ce que l'API Telegram permet) : `URL Method` = `sendPoll`, `Method` = `POST`, `Body Type` = Map Body, avec un **Body composé à la main** :
  `{"chat_id": "@scenario_fr", "question": "À ton avis, quel scénario l'emporte ?", "options": ["{{category}}"], "is_anonymous": true}`

Promotion du canal aussi ajoutée dans le template email (`feed.xml`, voir `docs/routine-prompt.md` étape technique 8) : une mention Telegram avant l'invitation à répondre, pour que les abonnés email découvrent le canal sans passer par `newsletter.html`. **Encart dédié sur `index.html`** (section `.telegram-promo`, entre Sources et le footer) : bouton à bordure — volontairement moins marquant qu'un bouton plein — puisque c'est la page la plus visitée du site. *(Ce bloc a été fusionné avec les boutons de partage le 4 août, voir B019.)*

### À faire
- Rien.

### Décisions
- **Ne jamais appeler l'API Telegram directement depuis une session** : `api.telegram.org` est **bloqué par la politique réseau (egress)** de l'environnement Claude Code Remote utilisé par le trigger « Scénario » — confirmé en reproduisant l'appel : `CONNECT api.telegram.org:443` → `403 Forbidden` côté proxy, « policy denial », indépendamment du bon paramétrage de `TELEGRAM_BOT_TOKEN`. L'appel API part donc depuis l'infrastructure de Make, non soumise à cette restriction.
- **Une seule balise `<category>` par item dans `feed.xml`**, contenant déjà les 3 titres séparés par `","` (guillemet-virgule-guillemet) — voir `docs/routine-prompt.md`, étape technique 8. Il suffit alors d'entourer la pastille de guillemets et crochets **tapés à la main** dans le Body (`["`+pastille+`"]`) pour obtenir un tableau JSON valide, **sans aucune fonction Make**.
  - **Piège découvert en configurant `options`** : Make **ne récupère qu'une seule occurrence** d'un champ RSS répété (`<category>` mis 3 fois dans le même item) au lieu d'un tableau de 3 — confirmé avec un flux de test 100 % frais, donc pas un souci de cache. Insérer directement le champ tableau (`Categories[]`) brut dans le JSON du Body ne fonctionne pas non plus : Make le sérialise en texte simple séparé par des virgules, pas en tableau JSON valide (`can't parse options JSON object`), et la fonction `split()` de Make donne le même résultat une fois insérée dans ce champ texte (pas de sérialisation JSON automatique des tableaux dans le Body « Map Body »).
- Flux de test jetable (`feed-test.xml`, supprimé après usage, comme pour LinkedIn) utilisé pour valider chaque itération sans polluer le vrai flux ni attendre le lendemain.

### Historique
- **2026-07-31** — Canal et bot créés. Test manuel d'envoi réussi (`sendMessage` + `sendPoll` via l'API Telegram, appelée à la main par l'utilisateur — pas depuis une session Claude Code Remote).
- **2026-08-01 (panne découverte)** — La routine avait été configurée pour appeler l'API Telegram directement en `curl` depuis sa propre session (ancienne étape technique 9). Résultat : **aucun message n'est jamais parti, silencieusement**. La consigne de ne jamais bloquer la publication principale en cas d'échec masquait le problème : l'édition partait normalement, seul le Telegram échouait en silence.
- **2026-08-01 [FAIT et vérifié]** — Bascule sur Make.com, exactement comme pour LinkedIn. L'ancienne étape `curl` retirée de `docs/routine-prompt.md` (étape technique 9 réécrite) : la routine n'a plus rien à faire pour Telegram.

---

## B100 — Soumission du canal Telegram aux annuaires

**Statut:** EN COURS
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07-31
**Prochaine action:** Envoyer manuellement l'email de proposition déjà préparé pour **ActuZones** (actuzones@proton.me)
**Blocage:** Aucun

### État actuel
- **TGStat** (tgstat.com, catégorie France / français / News and media) : **soumis le 31 juillet**.
- **ActuZones** : email de proposition **préparé**, à envoyer manuellement.
- **Lien Telegram** (lientelegram.com, fiche indexée Google) et **Annuaire Telegram France** (telegramfrance.com) : identifiés, **pas encore soumis**.

### À faire
- Envoyer l'email ActuZones.
- Soumettre aux deux autres annuaires identifiés.

### Décisions
- Objectif : rendre le canal découvrable en dehors du site.

### Historique
- **2026-07-31** — TGStat soumis, ActuZones préparé, 2 autres annuaires identifiés.

---

## B101 — Équilibre entre l'encart Telegram et le formulaire email sur `newsletter.html`

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07-31
**Prochaine action:** Trancher s'il faut rééquilibrer `newsletter.html`
**Blocage:** Sujet pas encore tranché

### État actuel
L'encart Telegram sur `newsletter.html` (bordure + bouton plein) est visuellement **plus marquant** que le formulaire email juste au-dessus, avec un risque de **cannibaliser** les inscriptions email (canal gratuit et sans engagement vs formulaire email) plutôt que de les compléter. Pas tranché.

### À faire
- Décider s'il faut rééquilibrer `newsletter.html` en conséquence.

### Décisions
- **Garder l'email comme canal principal** (liste possédée, indépendante d'une plateforme tierce) et traiter Telegram comme **option secondaire complémentaire**.
- **Rester volontairement discret** (lien simple, pas d'encart) si un ajout est fait sur `index.html`.

### Historique
- **2026-07-31** — Point de vigilance soulevé, décision de principe posée, arbitrage visuel laissé ouvert.

---

## B102 — Nom de domaine dédié

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07 (non daté précisément)
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
`lesscenarios.fr` acheté et configuré (DNS chez OVH, voir aussi B095 pour la délégation du sous-domaine d'envoi).

### À faire
- Rien.

### Décisions
- Aucune à consigner.

### Historique
- **2026-07** — Fait.

---

## B103 — SEO de base : `robots.txt`, `sitemap.xml`, Google Search Console

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-07-30
**Prochaine action:** Aucune (les lacunes canonical/meta description ont été traitées le 21 août, voir B068)
**Blocage:** Aucun

### État actuel
`robots.txt` (autorise tout, pointe vers le sitemap) et `sitemap.xml` (toutes les pages vivantes + toutes les archives) à la racine. `sitemap.xml` est mis à jour chaque jour par la routine (nouvelle entrée d'archive + `lastmod` rafraîchi), voir `docs/routine-prompt.md` étape technique 7. **Google Search Console : fait le 30 juillet 2026** — propriété du domaine `lesscenarios.fr` vérifiée, sitemap soumis. *(`robots.txt` a ensuite reçu un `Disallow: /dashboard.html`, voir B148.)*

### À faire
- Rien.

### Décisions
- Aucune à consigner.

### Historique
- **2026-07-30** — Search Console vérifiée, sitemap soumis.
---

## B104 — Données structurées `NewsArticle` et éligibilité Google Actualités

**Statut:** EN TEST
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-21
**Prochaine action:** **Prochain check : 15 septembre 2026** (1 mois jour pour jour après la vérification du 15 août, demande explicite de l'utilisateur) — même filtre Search Console (Type de recherche : Actualités). Si toujours à 0 à cette date, creuser une cause technique plus profonde plutôt que d'attendre encore
**Blocage:** **Toujours aucune apparition dans Google Actualités au 15 août** (0 clic, 0 impression sur 3 mois). Pas de rappel automatisé posé pour le 15 septembre — repère à surveiller manuellement

### État actuel
Toute la partie technique est en place et validée ; il ne manque que le résultat. `NewsArticle` (JSON-LD) présent dans le `<head>` d'`index.html` et de chaque archive ; publication déclarée sur Google Publisher Center ; **Rich Results Test validé le 8 août** (`NewsArticle` détecté comme « 1 élément valide », aucune erreur ni élément invalide, capture Search Console fournie par l'utilisateur). **Mais** : Search Console, rapport Performances filtré « Type de recherche : Actualités », fenêtre 3 mois (28/07 au 13/08) → **0 clic, 0 impression** sur toute la période, y compris depuis la config Publisher Center du 7 août (J+8 au moment du check). Pas forcément alarmant — Google annonce lui-même un délai « généralement plusieurs semaines » — mais c'est la première vérification factuelle depuis la mise en place.

### À faire
- Check du 15 septembre 2026.
- Si toujours 0 : creuser fréquence de crawl, `robots.txt`, sitemap news, volume de contenu jugé insuffisant par Google.
- *Note sur l'absence de rappel automatisé* : les outils de planification disponibles dans la session d'alors (cron/wakeup) ne tenaient pas au-delà de 7 jours, contrairement aux triggers persistants type « Scénario — Pub hebdo » gérés hors session.

### Décisions
- **Depuis 2019, Google n'a plus de « soumission » avec validation humaine pour Google News** — inclusion automatique si le site est crawlable et respecte les règles de contenu (déjà largement le cas : auteur identifié, dates claires, transparence IA, pages légales). Le manque technique principal identifié était l'absence de données structurées `NewsArticle`, le signal principal que Google utilise pour distinguer un article d'actualité d'une page web classique.
- **Logo carré PNG, pas SVG**, pour `publisher.logo` : Google déconseille le SVG pour ce champ.

### Historique
- **2026-08-07 [FAIT]** — Ajout du bloc `<script type="application/ld+json">` (headline, description, image, `datePublished`/`dateModified`, auteur, éditeur) dans le `<head>` d'`index.html` et de chaque archive — schéma exact et règles de reproduction quotidienne dans `docs/routine-prompt.md` (nouveau paragraphe après l'étape technique 3bis). Nouveau logo carré `assets/logo-512.png` (512×512, fond blanc, généré via Playwright depuis `assets/logo.svg`). Appliqué rétroactivement aux 3 dernières archives qui avaient déjà des balises `<head>` correctes par édition (05, 06, 07 août).
- **2026-08-07 [FAIT] — bug préexistant corrigé rétroactivement sur les 12 archives du 18 juillet au 4 août inclus** (pas 10 comme d'abord estimé — recompté en travaillant dessus). Avant correction : tagline générique dans `<title>`/`meta description` (« Scénario — L'actualité en trois hypothèses/scénarios chiffrés »), et pour les 10 plus anciennes (18 juillet au 2 août), **aucune balise Open Graph/Twitter Card du tout** — pas juste un contenu générique, les balises étaient absentes. Le fix du 4 août (étape technique 3bis) n'avait en réalité commencé à s'appliquer qu'à partir de l'édition du 5 août. **Reconstruit pour les 12** : titre réel, meta description (question posée extraite du corps de la page — ou rédigée à partir du `dek` pour les 2 toutes premières éditions, 18 et 25 juillet, qui datent d'avant l'existence du bloc « question posée » dédié), bloc Open Graph/Twitter complet aligné sur le gabarit actuel, `article:author`/`article:published_time`, et JSON-LD `NewsArticle`. **Dates de publication** : 8 des 12 confirmées par le `pubDate` réel encore présent dans `feed.xml` (27, 29, 30, 31 juillet, 1er, 2, 3, 4 août) ; les 4 autres (18, 25, 26, 28 juillet, absentes de `feed.xml`) n'ont **pas de trace fiable de l'heure réelle de publication** — estimées à 07:15:00 (heure standard du site), approximation raisonnable mais non garantie exacte à la minute près.
- **2026-08-07 [FAIT côté utilisateur]** — Publication ajoutée sur Google Publisher Center (`lesscenarios.fr`, Nom = « Scénario », France, français) + logos carrés fournis en fond blanc et fond noir (512 et 1000px : `assets/logo-512.png`/`logo-1000.png` et leurs variantes `-black`), générés via Playwright depuis `assets/logo.svg`. *(Avant cela, noté comme « reste à faire côté utilisateur » : ne se fait pas via API/session, nécessite le compte Google personnel.)*
- **2026-08-08 [FAIT]** — Rich Results Test validé. Reste disponible si Publisher Center demande une étape de configuration supplémentaire (sections, etc.), sinon ce point est clos.
- **2026-08-15 [VÉRIFIÉ]** — Toujours aucune apparition dans Google Actualités, repère du 15 septembre posé.
- **2026-08-21** — Audit SEO déclenché par « je recherche sur Google et je ne remonte jamais » : diagnostic d'indexation d'un domaine jeune sans backlink, cohérent avec ce 0 clic/0 impression (voir B068).

---

## B105 — Mentions légales et politique de confidentialité

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08 (non daté précisément ; section IA ajoutée le 1er août)
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Deux pages dédiées (`mentions-legales.html`, `politique-de-confidentialite.html`), liées depuis le footer des 5 pages vivantes. Éditeur identifié (Olivier Bertrand), hébergeur GitHub Pages précisé, et les trois cas de collecte de données détaillés simplement : newsletter (Buttondown), formulaire de contact (FormSubmit), mesure d'audience (GoatCounter, anonyme, sans cookie donc **pas de bandeau de consentement nécessaire**). Une section « Intelligence artificielle et transparence » a été ajoutée le 1er août (voir B125).

### À faire
- Rien. *(Traduction anglaise : question ouverte, voir B007.)*

### Décisions
- GoatCounter anonyme et sans cookie → pas de bandeau de consentement.

### Historique
- **2026-08 (non daté)** — Pages créées.
- **2026-08-01** — Section IA ajoutée (B125).

---

## B106 — Newsletter par email (Buttondown, RSS-to-email)

**Statut:** FAIT (« presque terminé » dans le backlog d'origine)
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune. *(Migration vers OneSignal envisagée à terme, voir B004.)*
**Blocage:** Aucun

### État actuel
Outil : **Buttondown**, compte payant, plan Basic ~9 $/mois — **nécessaire pour le RSS-to-email**, pas disponible en gratuit contrairement à ce qu'indiquaient plusieurs sources tierces, vérifié en pratique. Forfait payé jusqu'au 29 juillet 2027 (voir B004). Branché directement sur `feed.xml`, déjà généré chaque jour. `newsletter.html` (page d'inscription, style du site, formulaire Buttondown standard) + lien « Newsletter » dans le menu de toutes les pages vivantes ; design (couleurs/polices) aligné à la charte du site sur les pages web et email Buttondown ; connexion RSS-to-email configurée (« Send an email », déclenchement à chaque nouvel item, template « Rich ») ; mise à jour quotidienne de `feed.xml` dans le prompt de la routine (étape technique 7). Deux pages de redirection dédiées depuis le 11 août : `confirmez-votre-email.html` et `bienvenue.html`.

### À faire
- Rien.

### Décisions
- **Pages de redirection dédiées (11 août)** au lieu des pages génériques : Réglages Buttondown → Subscribing → Redirects — « After subscribing » (avant confirmation) pointait vers `newsletter.html`, « After confirming » (inscription validée) vers la page d'accueil. Remplacés par deux pages dédiées, même gabarit visuel que le reste du site, **`noindex`** (pages transactionnelles) : `confirmez-votre-email.html` (invite à vérifier la boîte mail/les spams, bonus Telegram en attendant) et `bienvenue.html` (confirme l'inscription active, ce qui va être reçu, CTA vers l'édition du jour).

### Historique
- **2026-07-31 (vérifié sur un envoi réel)** — Template d'email propre (un seul bloc d'intro « Rich », pas de doublon), objet/Subject correct (reprend le h1 du jour), retours à la ligne bien interprétés, liens de désinscription/gestion d'abonnement présents. Email de test réel reçu et vérifié bout en bout (édition du 31 juillet, 08h01). Le prompt de la routine est aussi tenu à jour dans le trigger réel au fil des sessions (dernière synchronisation vérifiée le 31 juillet, 16h36).
- **2026-08-07** — Passage à un formulaire unique avec deux metadata séparées (voir B029).
- **2026-08-11 [FAIT]** — Pages de redirection dédiées. **Déploiement d'abord bloqué par le bug Jekyll** (voir B060) — vérifié en ligne par l'utilisateur une fois `.nojekyll` poussé. Champs Buttondown mis à jour par l'utilisateur avec les deux nouvelles URLs.

---

## B107 — Newsletter hebdomadaire « On refait le scénario de la semaine » + routine hebdo

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-09
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Flux RSS séparé `feed-weekly.xml` (racine du dépôt), **totalement indépendant de `feed.xml`** — un abonné à la quotidienne ne reçoit jamais l'hebdo, et inversement, sauf inscription explicite aux deux (voir B029). Une **Routine automatique** tourne **chaque dimanche à 14h Paris**, sans validation manuelle (choix de l'utilisateur, cohérent avec l'automatisation complète du site) ; l'Automation Buttondown côté RSS-to-email envoie l'email le dimanche soir, l'écart de quelques heures laissant une marge confortable. Prompt documenté dans `docs/routine-hebdo-prompt.md` depuis le 9 août — trigger `trig_01SE6daCsV38jPUXf82DC7TF` (créé via `meta_mcp`, directement éditable via `update_trigger`, pas besoin du cycle copier-coller manuel de la routine quotidienne). *(Un autre identifiant, `trig_01FwX1Q3xsLCMwAZt4WviUA6`, est cité ailleurs dans le backlog comme celui de la routine hebdo — incohérence non résolue dans la source, voir B087.)*

### À faire
- Rien.

### Décisions
- **Nom choisi pour éviter le plagiat** d'un concurrent qui utilise « on rembobine » — même idée (revenir sur la semaine), formulation différente, dans l'esprit de la marque (« refaire le scénario » ~ « refaire le match »).
- **Étapes de la routine** :
  1. Vérifier qu'un récap n'a pas déjà été publié cette semaine (dernier `<pubDate>` de `feed-weekly.xml`).
  2. Relire les 7 dernières entrées du « Journal des sujets publiés » (`docs/sujets-a-suivre.md`), lundi à dimanche de la semaine calendaire.
  3. Ouvrir chaque archive correspondante pour en extraire la matière du récap (h1, question, scénario le plus probable) — **jamais se contenter du seul titre du journal, trop court pour un vrai résumé**.
  4. Rédiger le récap dans un **ton fluide et naturel, mais rigoureux — jamais familier ni « cute »**.
  5. Insérer un nouvel `<item>` en haut de `feed-weekly.xml` (historique conservé, comme `feed.xml`), commit et push direct sur `main`.
- **Règle de vocabulaire (correction du 3 août)** : **toujours le vocabulaire exact déjà établi sur le site** — « le scénario stable/favorable/dégradé », « jugé le plus probable », le pourcentage exact, le nom du scénario tel qu'écrit dans son `<h3>` — **jamais une reformulation de convenance**. Chaque sujet précise aussi le **registre du jour** (repris de l'eyebrow de l'archive, ex. « Lundi, géopolitique international ») pour ancrer le sujet. Un lien cliquable vers chaque archive citée, **jamais un jour mentionné sans son lien**.
- **Tag `<comments>` (6 août)** : ajouté pour la même raison que sur `feed.xml` — séparer un texte court réutilisable (aperçu, réseau social) du HTML complet de `<description>`, sans avoir à le parser. Porte la phrase d'ouverture/conclusion de semaine rédigée à l'étape 3, en texte brut — identique au premier paragraphe de la `<description>` mais sans les balises `<br>`. **Appliqué rétroactivement à l'item déjà publié (2 août).**

### Historique
- **2026-08-03 [FAIT]** — Ajoutée sur demande explicite de l'utilisateur : certains lecteurs préfèrent un récap hebdomadaire plutôt que de suivre la quotidienne.
- **2026-08-03 (correction du ton)** — Le tout premier exemple (basé sur la semaine du 27 juillet) partait sur un ton trop familier (« Salut 👋 ») et une paraphrase vague et creuse (« on ne tranche pas encore » pour désigner le scénario stable) — retour utilisateur immédiat, corrigé aussitôt dans l'exemple et dans le prompt.
- **2026-08-06** — Tag `<comments>` ajouté ; page dédiée `hebdo/{date}.html` créée (voir B109) ; relais social ajouté (voir B110).
- **2026-08-09** — `docs/routine-hebdo-prompt.md` créé : ce fichier miroir n'existait pas encore alors que la routine tournait déjà depuis plusieurs semaines — trou comblé après un retour utilisateur qui redonnait le correctif du 6 août pour vérification, l'occasion de s'apercevoir qu'aucune copie de référence n'existait.
- **2026-08-11** — La routine hebdo se charge désormais de mettre à jour le lien « Récap de la semaine » sur `index.html` (voir B049).
- **2026-08-27** — Confirmé « déjà en place » par l'audit externe : le récap existe depuis le 2 août et est déjà lié depuis la bande `.top-updates` de chaque édition.

---

## B108 — Synchronisation manuelle du prompt de la routine quotidienne (trigger `http_api`)

**Statut:** BLOQUÉ
**Priorité:** Non chiffrée — contrainte structurelle, pas un chantier
**Dernière MAJ:** 2026-08-11
**Prochaine action:** Aucune côté session. À chaque correction de `docs/routine-prompt.md` : signaler que c'est fait, l'utilisateur va chercher le fichier sur GitHub et fait le copier-coller lui-même
**Blocage:** **`update_trigger` est refusé sur `trig_0176spj7P7E9fyTs1XBkQBWF`** (`created_via: http_api`, créé hors session) : « this routine was created via http_api, not by an agent ». Une session ne peut qu'y lire son contenu (`list_triggers`) ou la désactiver, jamais réécrire son prompt

### État actuel
Contrainte permanente : le trigger de la routine éditoriale quotidienne tourne sur un prompt figé stocké côté Claude Code Remote, qui doit être recopié à la main par l'utilisateur depuis `docs/routine-prompt.md`. **Deux copies existent donc et peuvent dériver.** Contrairement à l'hebdo, la détection, l'Inspecteur et la pub (tous `created_via: meta_mcp`, donc éditables directement via `update_trigger`).

### À faire
- Rien de structurel n'est prévu. Chaque ticket touchant au prompt quotidien dépend de ce geste manuel (voir B039, B070, B071, B077, entre autres).

### Décisions
- **Dans `docs/routine-prompt.md`, seul le texte après la ligne `---` est le prompt réellement envoyé à la routine live** — tout ce qui précède (titre, explication du fichier, mentions « version allégée depuis le 9 août », lien vers le fichier de rollback) est de la documentation à l'usage d'un humain, jamais collé dans le trigger. *(Précision du 11 août.)*
- **Convention adoptée le 11 août** (demande explicite de l'utilisateur, par souci d'économie) : la session met à jour `docs/routine-prompt.md` directement sur GitHub (`main`) et signale juste que c'est fait — c'est à l'utilisateur d'aller chercher le fichier sur GitHub et de faire le copier-coller. **Ne plus envoyer de fichier texte séparé pour ça** (ancienne pratique du 8 août : plusieurs fichiers `routine-quotidienne-allegee*.txt` envoyés un par un à chaque correction, source de confusion sur la version réellement à jour).
- En cas d'urgence (ex. permutation des registres du 12 août, B071), le texte est donné directement à l'utilisateur pour collage immédiat.

### Historique
- **2026-08-03 (constat)** — Une tentative concrète a révélé que la routine quotidienne, contrairement à l'hebdo, n'est pas modifiable via `update_trigger`. **Une note antérieure du backlog affirmait par erreur que les deux étaient modifiables ; corrigé après vérification.**
- **2026-08-11** — Marche à suivre et convention précisées.

---

## B109 — Page dédiée par récap hebdo (`hebdo/{AAAA-MM-JJ}.html`) + découverte sur le site

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-06
**Prochaine action:** Aucune. **Toujours pas d'entrée dans le menu principal** (prématuré, un seul récap existant au moment de la décision)
**Blocage:** Aucun

### État actuel
Une page figée par semaine, `hebdo/{AAAA-MM-JJ}.html` (date = le dimanche du récap), qui ne bouge plus une fois publiée — symétrique aux éditions quotidiennes. Reprend le contenu de l'`<item>` de `feed-weekly.xml`, mis en page avec le même système visuel que le reste du site (mêmes variables CSS, polices, masthead/nav/footer identiques à `archives.html`) ; classes : `.day-block`, `.day-context`, `.scenario-list`/`.scenario-row`, `.week-conclusion`. Pour chacun des 7 jours : eyebrow (registre), titre lié à l'archive complète, la question posée du jour (`.day-context`, reprise de `.question-text` de l'archive citée — sert de contexte, « ce qu'on évalue »), puis les 3 scénarios en liste compacte (flèche + pourcentage + libellé, le plus probable en gras via `.is-winner`). Une conclusion de semaine tout en bas. Le `<link>` de l'`<item>` RSS pointe vers cette page précise (plus `archives.html` en générique).

**Découverte sur le site** : le récap est une **entrée comme les autres** dans le fil `#entries` d'`archives.html`, positionnée chronologiquement juste après l'entrée de l'édition quotidienne du dimanche correspondant (classe `entry-weekly` en plus de `entry`), avec un badge « Récap de la semaine » (`<button class="tag entry-weekly-badge" data-tag="hebdo">` — réutilise le système de tags existant, apparaît donc aussi comme puce de filtre cliquable : **c'est ce qui permet de retrouver l'historique complet des récaps hebdo** en un clic, sans liste dédiée qui grossit à part) et un accordéon **« Les 7 jours ▾ »** (au lieu de « Scénarios ▾ ») qui charge en lazy-load `hebdo/fragments/{date}.html` — même mécanique que `archives/fragments/{date}.html`, un fragment par semaine (uniquement les 7 `.day-block` + `.week-conclusion`, sans masthead/nav/footer). Le lien du titre de l'entrée pointe vers la page dédiée `hebdo/{date}.html` (utile pour le partage réseaux sociaux — un lien stable, pas juste un aperçu inline). Entrée ajoutée dans `sitemap.xml` (`changefreq: never` comme les archives quotidiennes, `priority: 0.5`).

### À faire
- Rien.

### Décisions
- **Revient sur la décision du 3 août** (pas de page dédiée) : retour utilisateur du 6 août — besoin d'un lien stable à partager sur les réseaux, pas juste l'email/RSS.
- **Liste compacte plutôt que grille à cartes bordées** : premier jet en grille jugé « trop lourd » par l'utilisateur.
- **Découverte : deux itérations le 6 août.** Premier essai : section « Récaps hebdo » séparée en haut de `archives.html`, liste à part. Retour utilisateur : grossirait indéfiniment au fil des semaines et repousserait la liste des éditions quotidiennes de plus en plus bas — **pas tenable à long terme**. Remplacé par l'intégration directe dans le fil `#entries`.
- **La routine quotidienne (7h00) n'a besoin d'aucune adaptation** : elle insère toujours sa nouvelle entrée en tête de `#entries`, sans se soucier du contenu plus bas dans la liste — aucune collision possible avec l'entrée hebdo positionnée ailleurs dans le fil.

### Historique
- **2026-08-03** — Décision initiale : pas de page dédiée.
- **2026-08-06 [FAIT]** — Page dédiée + découverte dans `archives.html`.
- **2026-08-11** — Vignettes Instagram et grille 2 colonnes ajoutées à la page hebdo (voir B050).

---

## B110 — Relais social du récap hebdo (scénario Make « Scenario Weekly »)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-07
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Un scénario Make dédié (« Scenario Weekly : RSS -> Réseaux Sociaux »), séparé de « Daily », tourne sur `feed-weekly.xml` — même structure que « Daily » : RSS « Watch » (1 item max) → Router → LinkedIn « Create a Company Text Post » / Telegram « Send a Text Message » / Buffer « Create a status update » (X), plus une branche Facebook ajoutée entre-temps (module 12, `profileIds` identique au Daily, voir B025). Textes adaptés au format hebdo (`Title` + `Comments` + « Lire le récap ici/complet » + `URL`). Sauvegarde complète : `assets/make/scenario-weekly.blueprint.json`.

### À faire
- Rien.

### Décisions
- **Revient sur la décision du 3 août** (pas de relais social pour le hebdo).
- **Pas d'invitation à voter / sondage Telegram**, contrairement à « Daily » — pas de sens pour un récap.
- **2 scénarios Make actifs au total** (« Daily » fusionné + « Weekly ») pour rester sur le plan gratuit, limité à 2 scénarios actifs simultanément (voir B118).

### Historique
- **2026-08-06 [FAIT]** — Scénario Weekly créé.
- **2026-08-07** — Branche Facebook ajoutée (voir B025).

---

## B111 — Photo dans les éditions (première discussion)

**Statut:** ABANDONNÉ
**Priorité:** —
**Dernière MAJ:** 2026-08-01
**Prochaine action:** Aucune — mais voir B027/B076, qui ont résolu le besoin autrement
**Blocage:** —

### État actuel
Idée écartée le 1er août. **Deux raisons distinctes, à ne pas confondre** : (1) impossible d'utiliser une vraie photo de presse trouvée pendant la recherche (droit d'auteur, republication non autorisée), et générer une image IA « réaliste » est risqué vu que les sujets impliquent souvent de vraies personnes (chefs d'État, dirigeants, sportifs...) — problème de désinformation/deepfake pour un site qui se veut rigoureux factuellement ; (2) une illustration abstraite générée par IA (pas photoréaliste, dans les couleurs de la marque) restait une option plus sûre, mais **écartée aussi** pour ne pas introduire un élément visuel non maîtrisé et casser la cohérence typographique du site (aucune photo nulle part à l'époque).

### À faire
- Rien.

### Décisions
- Les deux raisons ci-dessus ont été réinvoquées le 10 août pour écarter une piste d'illustration générique par registre (voir B076), et la contrainte de droit d'auteur est la raison directe du principe « zéro risque » de B027.

### Historique
- **2026-08-01** — Discuté puis volontairement abandonné, aucune action prévue à l'époque.
- **2026-08-08/09** — Le besoin est finalement couvert autrement : photos libres de droits Pexels, mots-clés génériques, jamais de personne réelle (B027).

---

## B112 — Pages de suivi par sujet (`suivi/{sujet}.html`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune — mécanique en place, 7 pages `suivi/*.html` existaient au 27 août
**Blocage:** Aucun

### État actuel
Une page par sujet suivi, `suivi/{sujet}.html`, **distincte de l'archive d'origine** (qui ne bouge jamais). N'existe pas tant qu'aucune mise à jour n'a été demandée. Déclenchement **entièrement manuel** (voir Décisions). À la première demande, la page se crée avec **deux entrées d'un coup** : (1) rappel de l'édition d'origine — résumé des 3 scénarios et lequel était jugé le plus probable, avec lien vers l'archive figée ; (2) la mise à jour du jour — ré-évaluation des 3 scénarios à la lumière de ce qui s'est passé depuis, conclusion claire comparée à l'entrée précédente. Chaque demande suivante ajoute une **nouvelle entrée en dessous**, jamais une réécriture des précédentes (v0, v1, v2...).

**Découverte** : pas de nouvel onglet dans le menu principal (prématuré tant qu'il n'existe que 2-3 sujets suivis). À la place : un badge sur la ligne concernée dans `archives.html` (`🔄 Suivi mis à jour le {date} →`, avec la date de dernière mise à jour plutôt que la date de publication) ; et un toggle de tri ajouté aux filtres existants d'`archives.html` (« Date de publication » / « Dernière mise à jour ») — en mode « dernière mise à jour », un sujet ancien mais récemment mis à jour remonte en haut, mélangé aux éditions du jour, en réutilisant le JS de recherche/filtre déjà en place.

**`suivi/_gabarit.html` est LE gabarit** (fichier dédié, jamais publié ni lié depuis le site, avec des `{PLACEHOLDER}` explicites et un commentaire d'avertissement en tête) — à réutiliser tel quel pour chaque nouveau sujet : copier ce fichier vers `suivi/{sujet}.html`, puis remplacer chaque placeholder. **Ne jamais repartir d'un autre fichier `suivi/*.html` existant ni improviser une nouvelle structure.** `suivi/spiderman-marvel.html` reste le premier exemple réel rempli, utile pour voir le rendu final, mais **`_gabarit.html` est la source à copier**, pas lui.

### À faire
- Rien sur la mécanique. Volets traités séparément : B113 (date de la puce), B114 (image), B115 (règles de rédaction), B116/B117 (clôture), B118 (annonce sociale), B119 (image du post), B120 (graphique d'évolution), B121 (accordéon), B122 (journal), B123 (détection), B124 (vitrine des clôturés), B127 (réécriture éditoriale des versions publiées).

### Décisions
- **Besoin identifié** : certains sujets (budget 2027, Iran-USA, méga-feux...) ont un enjeu qui dure bien au-delà de leur édition d'origine, mais les archives sont figées définitivement — donc aucun mécanisme pour montrer comment un scénario évolue dans le temps.
- **Déclenchement entièrement manuel** : l'utilisateur donne le « go » (ex. « mets à jour le sujet Budget 2027 ») ; jamais automatique dans la routine quotidienne, jamais une entrée systématique pour chaque édition — volontairement réservé à une poignée de sujets à enjeu durable, choisis à la main, **pour ne pas se retrouver à gérer un deuxième site**. *(Nuancé le 8 août par l'auto-publication encadrée de la routine de détection, voir B123.)*
- **On additionne, on ne remplace pas** : même logique que les archives.
- **`docs/routine-prompt.md` et le trigger automatique ne changent jamais pour ça** — le suivi reste déclenché seulement par une demande explicite de l'utilisateur en session.

### Historique
- **2026-08-01 [FAIT] — premier cas réel construit** : `suivi/spiderman-marvel.html`, suite de l'édition du 18 juillet (« Spider-Man contre Avengers : qui va sauver le box-office Marvel ? »). V0 reprend les 3 scénarios d'origine (favorable 25 %, stable 45 % jugé le plus probable, dégradé 30 %). V1 (1er août) intègre les vrais résultats de la sortie de Spider-Man : Brand New Day le 31 juillet (**72 M$ de previews, record ; ouverture projetée 260-330 M$, 2ᵉ meilleur démarrage de tous les temps**), qui dépasse le haut de la fourchette du scénario favorable — avec une conclusion honnête précisant que Doomsday (sortie en décembre) reste une inconnue, donc rien n'est encore tranché. Badge + tri par fraîcheur branchés sur `archives.html` et vérifiés visuellement (desktop + mobile).
- **2026-08-08 [FAIT] — deuxième cas réel** : `suivi/fifa-infantino.html`, suite de l'édition du 6 août (« FIFA : la présidence d'Infantino vacille »), déclenché par un sujet remonté par la routine de détection du soir plutôt que par une demande spontanée. V0 reprend les 3 scénarios d'origine (favorable 20 %, stable 45 % jugé le plus probable, dégradé 35 %). V1 (8 août) intègre les développements réels des 7-8 août — UEFA confirmant avoir « perdu confiance », FIFPRO dénonçant un « abus de pouvoir présidentiel », le scandale du paiement UEFA à une ex-employée, et surtout l'appui public de la CAF (unanime), de l'Argentine et du Mexique à Infantino — avec une conclusion qui nomme le scénario le plus volatil (favorable, −10 points) tout en distinguant ce qui relève de la rhétorique (durcissement du ton UEFA, dégradé +5) de ce qui relève d'un fait structurant pour le vote (bloc de **111 voix** désormais confirmé publiquement, stable +5). Badge + tri branchés sur `archives.html`, entrée « Suivis actifs » ajoutée dans `docs/sujets-a-suivre.md`, item ajouté dans `feed-suivi.xml`, tout vérifié visuellement (desktop + mobile).
- **2026-08-27** — L'audit externe confirme le mécanisme « V0 → V1 → V2 » comme **déjà en place** : blocs `.version`, tag/date/titre, repliables (voir B127 pour le travail éditorial restant).

---

## B113 — Date affichée sur la puce `.entry-date` d'une entrée révisée

**Statut:** FAIT (règle en place ; application ambiguë, à confirmer)
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-22
**Prochaine action:** Vérifier que toutes les entrées révisées d'`archives.html` portent bien `data-pub-date` et la date de mise à jour dans leur puce — la formulation d'origine ne dit pas si le rattrapage a été fait sur l'ensemble des entrées existantes
**Blocage:** Aucun

### État actuel
**Règle** : la puce `.entry-date` d'une entrée révisée affiche la **date de la dernière mise à jour**, pas la date de publication d'origine — même valeur que celle du badge juste en dessous (redondance volontaire, la puce est ce qu'on voit en premier). Pour ne pas casser le tri « Date de publication » ni le filtre par année (qui lisent tous les deux `.entry-date` par défaut), l'attribut `data-pub-date="{AAAA-MM-JJ d'origine}"` est ajouté sur le `<li class="entry">` — le JS d'`archives.html` s'en sert comme vraie date de publication dès qu'il est présent, indépendamment de ce qu'affiche la puce.

Concrètement, à chaque mise à jour d'un badge existant (ou à sa toute première création) :
`<li class="entry" data-last-update="{AAAA-MM-JJ du jour}" data-pub-date="{AAAA-MM-JJ de l'édition d'origine}">`, puis `<span class="entry-date">{JJ.MM.AAAA du jour}</span>` (au lieu de la date de publication).
**Exemple de référence** : `suivi/spiderman-marvel.html` / l'entrée du 18.07.2026 dans `archives.html`.

### À faire
- Confirmer la couverture sur les entrées révisées existantes.

### Décisions
- Redondance puce/badge volontaire.
- `data-pub-date` pour préserver tri et filtre par année.

### Historique
- **2026-08-22 (retour utilisateur)** — La puce `.entry-date` en tête d'entrée affichait toujours la date de publication, ce qui donnait l'impression qu'un sujet révisé n'avait « pas été mis à jour » au premier coup d'œil, même avec le badge juste en dessous.

---

## B114 — Image d'illustration des pages de suivi (à la création uniquement)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-12
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Même process que l'image Pexels des éditions quotidiennes (B027/B076), mais appliqué **une seule fois, à la création de la page (V0)** — jamais régénérée aux mises à jour suivantes (V1, V2...), pour éviter qu'un sujet suivi sur plusieurs mois accumule une galerie de photos disparates. Étapes, **seulement quand une page `suivi/{sujet}.html` n'existe pas encore** :
1. Construire 1 à 3 mots-clés thématiques génériques (même règle que pour l'édition quotidienne — jamais le titre recopié tel quel, jamais un nom propre isolé).
2. `python3 scripts/social/fetch_topic_image.py "{mots-clés}" --count 5 --out /tmp/topic-image-candidates` puis choisir le meilleur candidat à l'œil (mêmes garde-fous : écarter tout visage reconnaissable, tout candidat hors-sujet).
3. `python3 scripts/social/use_topic_image.py {candidat choisi} --date suivi-{sujet} --credits /tmp/topic-image-candidates/credits.json` — utiliser **`suivi-{sujet}` (pas une date)** comme identifiant, pour que les fichiers atterrissent sous `assets/social/topic-images/suivi-{sujet}.jpg` / `-wide.jpg` / `.json`, **jamais en collision** avec les images datées des éditions quotidiennes.
4. Insérer le bloc `<figure class="article-image">` déjà présent dans `suivi/_gabarit.html` (CSS et HTML identiques à `index.html`, chemins relatifs adaptés avec `../`), remplir `alt`/`{photographe}`/`{pexels_url}` à partir de la fiche de provenance JSON.
5. **Si aucun candidat ne convient (ou si le script échoue), retirer le bloc `<figure class="article-image">` entièrement** — jamais bloquant pour la création de la page, exactement comme pour l'édition quotidienne.

Sur une page qui existe déjà (ajout d'une V1, V2...), **ne jamais retoucher l'image en place** — elle reste celle choisie à la création, même si le sujet a beaucoup évolué depuis.

### À faire
- Rien.

### Décisions
- Une seule image par sujet suivi, fixée à la création. Elle sert aussi de base à l'image du post social de chaque mise à jour (voir B119).

### Historique
- **2026-08-12 [AJOUTÉ]** — Process posé sur retour utilisateur.

---

## B115 — Règles de rédaction d'une mise à jour de suivi

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-15
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Processus manuel, hors routine, dont les règles sont stabilisées :
- L'utilisateur donne le sujet à mettre à jour en session ; retrouver l'édition d'origine dans `archives/` ; si aucune page `suivi/{sujet}.html` n'existe, la créer depuis `suivi/_gabarit.html` avec V0 + V1 (et l'image, voir B114) ; si elle existe, ajouter uniquement une nouvelle version en dessous, jamais réécrire les précédentes.
- **Vérifier les faits par une vraie recherche** (même rigueur que pour une édition normale, sources croisées).
- **Donner une nouvelle estimation chiffrée des 3 scénarios**, présentée comme des cartes `.mini-scenarios` (même format que V0, pas un design différent), chacune avec une ligne d'évolution bien visible : le **nouveau %** en gros (`.evo-current`), une flèche colorée (`.evo-arrow` — verte `is-up` si ça monte, rouge `is-down` si ça descend, grise `is-flat` si inchangé), et l'ancien % entre parenthèses en petit (`.evo-prev`, ex. « (vs. 25% en V0) ») — **toujours comparé à la version immédiatement précédente**, jamais systématiquement V0 (V2 se compare à V1, V3 à V2, etc.). Un commentaire court par scénario explique pourquoi il monte/descend/reste stable.
- **L'intro de chaque mise à jour doit rester un seul paragraphe concis**, comme celui de V0 — pas plusieurs paragraphes détaillés ; le détail factuel spécifique à chaque scénario va dans son propre commentaire de carte.
- **Ordre du bloc obligatoirement identique à V0** : intro → cartes `.mini-scenarios` → bloc `.conclusion` (label + **une seule phrase**, jamais un gros paragraphe après la grille). **Ne pas dupliquer la conclusion** en un « headline » avant les cartes ET un paragraphe après — un seul emplacement, après la grille, exactement comme V0.
- **La conclusion doit nommer explicitement le scénario le plus volatil** : citer le scénario qui bouge le plus avec son écart exact en points (ex. « favorable : 25 % → 45 %, +20 points »), expliquer en une phrase le fait concret qui l'explique (ex. le succès du film, pas juste « les choses évoluent »), puis la nuance/incertitude restante s'il y en a une. **Le lecteur doit comprendre la volatilité réelle de la mise à jour en une seule lecture.**
- Puis : mettre à jour le badge et la date sur `archives.html` (voir B113) ; mettre à jour ou créer l'entrée dans la section « Suivis actifs » de `docs/sujets-a-suivre.md` (dernière vérification, prochaine échéance connue) ; ajouter un item dans `feed-suivi.xml` (voir B118) ; vérifier visuellement avant de pousser.

### À faire
- Rien.

### Décisions
- **Format des cartes remplacé le 1er août** : l'essai précédent en barres `.pct-compare` a été jugé pas assez lisible/scannable par rapport à V0, abandonné.
- **Jamais l'étiquette de catégorie brute (favorable/stable/dégradé) seule en tête de phrase, sans dire ce qu'elle recouvre concrètement** (ajouté le 14 août — cas réel : « ⏳ Stable en forte hausse, +20 points (45 %) » jugé incompréhensible, « stable *quoi* ? »). « Favorable »/« dégradé » passent presque toujours (le sens général — bonne/mauvaise nouvelle — se devine), mais « stable » ne dit jamais de quoi il s'agit : toujours remplacer l'étiquette par le titre concret du scénario (celui déjà écrit dans sa `.mini-scenario-title`, ex. « Le procès traîne, le deal reste gelé »), pas le nom de la catégorie interne.
- **Le titre du scénario lui-même ne doit pas non plus ouvrir la phrase** (affiné le 15 août — cas réel : « 🎯 Le retrait se fait proprement, +20 points (45 %) » jugé tout aussi incompréhensible en tête que l'étiquette brute : la règle du 14 août évitait « stable » seul, mais un titre de scénario reformulé reste souvent trop abstrait hors contexte de sa carte). **Toujours ouvrir la phrase par le fait concret** — l'événement réel qui explique le mouvement (ex. « LIV Golf a trouvé un nouvel investisseur principal ») — puis seulement ensuite nommer le scénario concerné et son écart en points, jamais l'inverse.
- **Périmètre de ces deux règles** : la page **ET** `<comments>`/`<description>` de `feed-suivi.xml` (et donc l'image générée par `generate_suivi_image.py`, qui réutilise ce même texte tel quel) — dans les deux cas, un lecteur qui n'a jamais ouvert la page doit comprendre en une seule phrase *pourquoi* il y a une mise à jour. Les titres de `.mini-scenario-title` sur les cartes individuelles restent inchangés : ces règles ne valent que pour la phrase de conclusion/verdict.

### Historique
- **2026-08-01** — Format des cartes, ordre du bloc et exigence de nommer le scénario le plus volatil ajoutés après retours utilisateur (l'ordre initial avait la conclusion *avant* les cartes, l'inverse de V0).
- **2026-08-14** — Règle « jamais l'étiquette brute en tête de phrase », **corrigée rétroactivement sur `suivi/warner-paramount.html`** et l'item correspondant de `feed-suivi.xml` le jour même.
- **2026-08-15** — Règle affinée « ouvrir par le fait concret », **corrigée rétroactivement sur `suivi/arabie-saoudite-sport.html`** et son item de `feed-suivi.xml` le jour même : « 🎯 LIV Golf trouve un nouvel investisseur, +20 points (45 %) » plutôt que « 🎯 Le retrait se fait proprement, +20 points (45 %) ».

---

## B116 — Clôture d'un sujet suivi (« VF — Résolu »)

**Statut:** FAIT (décision et mécanique) — **aucune clôture réelle au 27 août**
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune. La première clôture visée est datée de septembre 2026 dans `docs/sujets-a-suivre.md`
**Blocage:** Aucun

### État actuel
Pas un nouveau système, un **état final** sur les pages de suivi existantes : la dernière version devient définitive. Cette version finale suit le même format que les autres (cartes `.mini-scenarios`, comparaison à la version précédente), mais son titre de version est explicitement marqué **« VF — Résolu »** (au lieu de « V2 », « V3 »...) et son texte d'intro doit rappeler en une phrase ce qui avait été prédit en V0 (quel scénario était jugé le plus probable, à quel %) avant de dire ce qui s'est réellement passé — **le contraste prédiction/réalité doit être lisible sans avoir à remonter voir V0 soi-même**. Badge changé sur `archives.html` et sur la page elle-même : `✅ Résolu le {date}` à la place de `🔄 Suivi mis à jour le {date}`. Une fois clôturé, le sujet sort de la section « Suivis actifs » de `docs/sujets-a-suivre.md` (plus besoin de le repasser en revue à chaque passage de la routine de détection) — **mais la page `suivi/{sujet}.html` reste en ligne en permanence, comme une archive, jamais supprimée**. Vérifié le 27 août : **aucun suivi n'a encore été clôturé.**

### À faire
- Rien de structurel.

### Décisions
- **Condition de clôture : un fait réel, vérifié et sourcé, confirme clairement lequel des 3 scénarios s'est réalisé** — jamais le seul franchissement d'un seuil de probabilité interne (**idée écartée après discussion** : une probabilité élevée reste notre propre confiance, pas un fait vérifié ; clôturer dessus risquerait de figer un verdict juste avant un retournement, et s'apparente à de l'auto-évaluation). Un seuil franchi (≥ 80 % ou ≤ 20 % sur un scénario) ou une échéance connue atteinte servent de **déclencheur pour aller vérifier**, pas de critère de clôture en eux-mêmes.
- **Processus toujours entièrement manuel** : comme pour toute mise à jour de suivi, la clôture n'est jamais automatique — la routine de détection peut la **signaler** comme probable (🏁, point 2bis de son prompt), la décision et la rédaction restent celles de l'utilisateur en session. **Vrai même pour le sujet retenu par l'auto-publication** (B123) : seule la mise à jour normale est concernée par l'automatisation, jamais le passage en « VF — Résolu ».
- **Pas de page d'index dédiée (« track record ») pour l'instant** — trop tôt vu le faible nombre de sujets suivis (voir B124).

### Historique
- **2026-08-08 (décidée)** — Réflexion menée avec l'utilisateur sur un « track record » (mesurer si les scénarios publiés se réalisent vraiment) : plutôt que construire une page/base séparée, un sujet suivi peut simplement se clôturer.
- **2026-08-27** — Vérification : aucune clôture atteinte, `docs/sujets-a-suivre.md` ne liste qu'une clôture visée en septembre 2026.

---

## B117 — Préciser le déclencheur idéal de clôture d'un suivi

**Statut:** À FAIRE
**Priorité:** P1 (passée en P1 le 8 août)
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Retravailler la règle ensemble avant de l'ajouter au prompt de la routine de détection
**Blocage:** Discussion à reprendre

### État actuel
**Pas encore intégré au prompt de la routine de détection.** L'utilisateur propose que la clôture soit idéalement déclenchée quand **un événement concret déjà nommé dans la définition d'un des 3 scénarios se réalise** (ex. une démission, une motion de défiance effectivement déposée...) — un événement qui, de fait, ferait techniquement passer ce scénario à ~100 %.

### À faire
- Retravailler et intégrer dans `docs/routine-detection-prompt.md`.

### Décisions
- **Cohérent avec la règle déjà posée** (B116 : fait réel requis, jamais un seuil de probabilité interne) : ça ne la change pas, ça **précise ce qui compte comme « fait réel »** — pas n'importe quel développement notable, mais spécifiquement un des événements-jalons déjà écrits dans les scénarios eux-mêmes.

### Historique
- **2026-08-08** — Piste notée et passée en P1 le même jour.

---

## B118 — Annonce des mises à jour de suivi sur Telegram/LinkedIn (`feed-suivi.xml`)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-08
**Prochaine action:** Aucune. **Limite résiduelle assumée** : risque de doublon si une mise à jour est publiée avant l'heure de passage du scénario le jour même
**Blocage:** Aucun

### État actuel
Flux RSS séparé `feed-suivi.xml` (racine du dépôt), **volontairement distinct de `feed.xml`** pour ne **jamais déclencher d'email newsletter** pour une mise à jour de suivi — l'utilisateur n'a demandé que Telegram et LinkedIn (puis les autres réseaux ont suivi, voir B035). Consommé par une **4e branche du Router** du scénario Make « Daily » (module « Retrieve RSS feed items », id 30, avec son propre sous-Router). Format d'un item (mêmes conventions que `feed.xml` : `<comments>` porte la phrase courte, `<description>` le CDATA complet avec un lien final) :

```xml
<item>
  <title>{Sujet} : un scénario a bougé</title>
  <link>https://lesscenarios.fr/suivi/{sujet}.html#version-content-v{N}</link>
  <guid isPermaLink="false">scenario-suivi-{sujet}-v{N}</guid>
  <pubDate>{date de la mise à jour au format RFC-822}</pubDate>
  <comments>{verdict court de la conclusion, la phrase déjà écrite dans la page}</comments>
  <enclosure url="https://lesscenarios.fr/assets/social/suivi/{sujet}-v{N}.png" length="{taille réelle en octets}" type="image/png"/>
  <description><![CDATA[{même phrase}<br><br>{1-2 phrases : ce qui explique le mouvement}<br><br>Voir la mise à jour complète, scénario par scénario 👉 <a href="{lien vers la version}">lesscenarios.fr/suivi/{sujet}.html</a>]]></description>
</item>
```

Ajouter le nouvel item **en haut** du flux (comme `feed.xml`/`archives.html`), **ne jamais supprimer les précédents**.

### À faire
- Rien. **Solution plus lourde envisageable plus tard** si des doublons sont effectivement constatés en pratique : un Data Store mémorisant les `guid` déjà postés, immunisé à tout problème de fenêtre temporelle.

### Décisions
- **RSS plutôt qu'un webhook direct** : cohérent avec la solution déjà validée pour `feed.xml` (Make **poll** le flux, aucun appel sortant requis depuis la session — évite de retomber sur le blocage réseau déjà rencontré avec `api.telegram.org`, voir B099).
- **Modules dédiés (2 août)** : **Telegram Bot → « Send a Text Message »** (connexion « Scenario » réutilisée) : `Chat ID` = `@scenario_fr`, `Text` = `Title` + `Comments` + **« 👉 Voir la mise à jour complète : »** + `URL` — reprise du module de `feed.xml`, avec cette seule phrase de clôture changée (« Lire les 3 scénarios chiffrés » n'a pas de sens pour une réévaluation, pas une nouvelle prédiction). **LinkedIn → « Create a Company Text Post »** (connexion « Olivier's LinkedIn... », Page « Scenario », réutilisées) : `Content` = **« 🔄 Un sujet suivi vient d'être mis à jour 👇 »** + `Title` + `Comments` + `URL` — reprise du module de `feed.xml`, avec cette seule phrase d'intro changée (au lieu de « 🔥 Nouvelle édition Scénario, à lire 👇 »).
- **Pas de sondage (`sendPoll`) pour ce flux** : contrairement à une édition du jour, une mise à jour de suivi annonce un résultat déjà connu (les nouvelles probabilités), pas la peine de faire voter avant.
- **Fusion dans le scénario « Daily » le 6 août** (retour utilisateur) : le plan gratuit Make est limité à **2 scénarios actifs simultanément**, et l'ajout de Buffer/X avait fait passer le compte à 3. Le module RSS dédié à `feed-suivi.xml` a été **remplacé par un module « Retrieve RSS feed items »** (action normale, pas un déclencheur — contrairement à « Watch », elle peut être placée n'importe où dans un scénario, pas seulement en premier module) et rattaché comme 4e branche du Router du scénario « Daily », avec son propre sous-Router vers LinkedIn/Telegram/Buffer. Résultat : 2 scénarios actifs au total (« Daily » fusionné + « Weekly »).
- **Fréquence d'origine (scénario séparé) : 1×/jour, 18h heure de Paris** — volontairement décalée des 10h du scénario `feed.xml`, pour distinguer facilement les deux dans l'historique Make en cas de debug. Largement suffisant vu que les mises à jour de suivi sont rares et manuelles (pas de déclenchement « push » possible avec un flux RSS statique, donc polling à basse fréquence pour rester très en dessous du quota gratuit Make de 1000 opérations/mois).
- **Limite résiduelle assumée, non corrigée** : la fenêtre de 2 jours peut provoquer un **doublon** (pas un silence, contrairement à l'ancienne version) si une mise à jour est publiée **avant** l'heure de passage du scénario le jour même — elle tomberait dans la fenêtre glissante deux exécutions de suite. Risque jugé faible et accepté en connaissance de cause (mises à jour rares, manuelles).

### Historique
- **2026-08-02 [FAIT et vérifié]** — Flux créé sur demande explicite de l'utilisateur ; second scénario Make (« Scenario update topic : RSS -> LinkedIn/Telegram ») construit par duplication des modules LinkedIn/Telegram existants puis réglage des textes propres à une annonce de mise à jour. Module RSS « Watch RSS feed items », URL `https://lesscenarios.fr/feed-suivi.xml`, 1 item max. **Premier item réel ajouté le 2 août, rétroactivement, pour la mise à jour V1 de Spider-Man (1er août).** Test réel effectué avec cet item : envoi confirmé sur Telegram et LinkedIn.
- **2026-08-06** — Fusion dans le scénario « Daily ». Détail technique et texte exact des modules : `assets/make/scenario-daily.blueprint.json` (dernier export à jour au 8 août — **à ré-exporter et remplacer si le scénario est modifié par la suite, pas de synchronisation automatique**).
- **2026-08-08 [FAIT] — bug de répétition corrigé.** « Retrieve RSS feed items » n'a pas de mémoire des items déjà vus (contrairement à « Watch » sur `feed.xml`), donc à chaque exécution du scénario « Daily » (1×/jour) il renvoyait le dernier item de `feed-suivi.xml` **qu'il ait déjà été traité ou non**, ce qui repostait la même mise à jour tous les jours tant qu'aucune nouvelle n'était publiée. **Fix** : champ `filterDateFrom` du module 30, jusque-là vide, rempli avec `{{parseDate(formatDate(addDays(now; -1); "YYYY-MM-DD"); "YYYY-MM-DD")}}` (= hier à minuit, recalculé à chaque exécution), ne retenant que les items publiés dans les dernières ~24-48h glissantes. Une première version comparait à « aujourd'hui » plutôt qu'« hier » — **écartée après retour utilisateur** : une mise à jour publiée en fin de journée, après le passage quotidien du scénario (~7h00), n'aurait alors jamais été reprise (le lendemain, « aujourd'hui » ne correspond plus à sa date de publication). **Testé et vérifié le 8 août** : sur l'item Spider-Man déjà présent (`pubDate` du 1er août), `Date from` calculé à `7 août 2026 00:00` — la fenêtre l'exclut bien puisqu'il date de plus d'une semaine, confirmant que le filtre fonctionne.
- **2026-08-08** — `assets/make/scenario-daily.blueprint.json` réexporté par l'utilisateur et mis à jour dans le dépôt : reflète ce fix ainsi que l'ajout de l'image sur les posts X/Facebook (B021).
- **2026-08-12** — `<enclosure>` ajoutée au format d'item (voir B035).
- **2026-08-15** — Fenêtre de dates généralisée puis corrigée (voir B036).

---

## B119 — Image composée des posts de mise à jour de suivi

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-14
**Prochaine action:** Aucune (le recadrage de la photo de fond reste ouvert, voir B001)
**Blocage:** Aucun

### État actuel
À chaque nouvelle version publiée (V1, V2...), générer une image composée avec `scripts/social/generate_suivi_image.py` + `scripts/social/suivi-template.html` (logo — même taille que le daily — + pastille « 🔄 Suivi mis à jour » + titre du sujet + la conclusion, sur la photo `suivi-{sujet}.jpg` déjà en place, **jamais retouchée elle-même**) :

```
python3 scripts/social/generate_suivi_image.py \
  --data {json temporaire avec "topic" et "conclusion"} \
  --output assets/social/suivi/{sujet}-v{N}.png \
  --template scripts/social/suivi-template.html \
  --photo assets/social/topic-images/suivi-{sujet}.jpg
```

### À faire
- Rien.

### Décisions
- **Motif** : retour utilisateur — une simple photo Pexels sans rien dessus n'était « pas clean ».
- **`"conclusion"` = reprendre tel quel le texte déjà mis dans `<comments>`** (voir B115 : jamais mener avec la seule étiquette de catégorie).
- **Un fichier PNG par version** (`-v{N}.png`, jamais écrasé) plutôt qu'un seul fichier réutilisé, pour garder l'historique des visuels aligné sur l'historique des versions.
- **`{taille réelle en octets}`** de l'`<enclosure>` = taille de ce PNG généré (`stat -c%s`), **jamais une valeur inventée**.
- **Si la photo source (`suivi-{sujet}.jpg`) n'existe pas pour ce sujet, omettre `<enclosure>` entièrement** — jamais bloquant pour publier l'item.

### Historique
- **2026-08-14 [MIS À JOUR]** — L'image n'est plus la photo brute.
---

## B120 — Graphique d'évolution des pages de suivi

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-01
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Graphique **fixe (non repliable, choix volontaire** — le mettre dans l'accordéon irait à l'encontre de son but d'aperçu immédiat), affiché juste après l'intro de la page et **avant** « V0 — Point de départ ». Courbes lissées (Catmull-Rom → Bézier cubique), une par scénario (vert/bleu/rouge, mêmes couleurs que le reste du site), légère zone de dégradé sous la courbe favorable, points + % en Fraunces gras sur le dernier point. **N'apparaît qu'à partir de 2 versions** (`evoData.length < 2` → pas de rendu) : un seul point ne montre aucune évolution. **Généré en JS pur (pas de librairie externe), avec tout le rendu enveloppé dans un `try/catch`** : si les données sont mal formées (faute de frappe en éditant `evoData` à la main), le graphique se masque silencieusement au lieu de casser le reste de la page. Données à éditer : le tableau `evoData` en bas de page (`{ label: "V2", date: "...", favorable: X, stable: Y, degrade: Z }` — une ligne par version, ajouter simplement la ligne suivante).

### À faire
- Rien.

### Décisions
- `try/catch` ajouté par précaution — risque jugé faible (pas de dépendance réseau, pas de build) mais ces données sont éditées à la main à chaque mise à jour.
- `evoData` sert aussi de point de comparaison à la routine de détection (voir B123).

### Historique
- **2026-08-01 [FAIT]** — Ajouté.

---

## B121 — Anciennes versions de suivi repliées par défaut (accordéon)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-01
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Chaque bloc `.version` a un bouton `.version-toggle` ; seule la **dernière version** (la plus récente, toujours en bas du DOM) reste dépliée à l'arrivée sur la page — les précédentes sont repliées (tag + date visibles, contenu masqué jusqu'au clic). Même mécanique CSS/JS que l'accordéon des scénarios sur `archives.html` (`grid-template-rows` 0fr/1fr + classe `is-expanded`), **rien de nouveau inventé**. Pour un nouveau V2/V3..., dupliquer un bloc `.version.is-update` du gabarit et changer son `id` (`version-content-v2`, etc.) — le JS détecte automatiquement le dernier bloc du DOM et le déplie, aucune autre configuration nécessaire.

### À faire
- Rien.

### Décisions
- Ajouté après retour utilisateur : sans ça, la page devient un pavé à faire défiler dès la 3ᵉ ou 4ᵉ mise à jour d'un même sujet.

### Historique
- **2026-08-01 [FAIT]** — Ajouté.

---

## B122 — Journal quotidien auto-alimenté des sujets publiés

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-01
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Depuis le 1er août, l'étape 6bis de `docs/routine-prompt.md` fait écrire par la routine éditoriale **quotidienne** une ligne par édition (date + titre + lien) tout en haut de la section « Journal des sujets publiés » de `docs/sujets-a-suivre.md` — **sans aucun jugement de sa part sur l'intérêt du sujet**, juste un journal brut, même logique que `archives.html`. Le reste du fichier (section « Suivis actifs ») reste tenu à la main.

### À faire
- Rien.

### Décisions
- Journal brut, aucun jugement éditorial ; il sert de matière première à la routine hebdo (B107) et à la routine de détection (B123).

### Historique
- **2026-08-01 [FAIT]** — Ajouté.

---

## B123 — Routine de détection des sujets à mettre à jour

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-14
**Prochaine action:** Aucune. Deux points à confirmer empiriquement : le silence de l'email les jours « RAS » (logique « noteworthy » décidée côté plateforme) ; et la piste B117 (déclencheur idéal de clôture) reste à intégrer
**Blocage:** Aucun

### État actuel
Une Routine dédiée (`trig_01BYYviSQge2CDcYkzBbYcjT`, **lundi/jeudi/vendredi/samedi, 0h UTC ≈ 2h Paris** — déplacée du soir à la nuit le 14 août, voir B087), distincte de la routine éditoriale, relit `docs/sujets-a-suivre.md` : les « Suivis actifs » **systématiquement**, et le « Journal des sujets publiés » **limité aux 30 derniers jours**. Pour chaque « Suivi actif », elle **réestime chiffre à l'appui** la probabilité de chaque scénario (même sérieux méthodologique qu'une édition normale), la compare à la dernière version publiée (`evoData` de `suivi/{sujet}.html`), et marque **⚠️ seuil franchi** si l'écart atteint **≥ 20 points** sur au moins un scénario, ou qu'un événement rend un scénario clairement caduc/résolu. Pour les entrées du journal (pas encore de page dédiée), le jugement reste qualitatif — pas de probabilité de référence à comparer. Prompt : `docs/routine-detection-prompt.md` (trigger `created_via: meta_mcp`, directement éditable via `update_trigger`, pas besoin du cycle copier-coller manuel de B108). Notification par email native (`notifications: {email: true}`), session neuve à chaque déclenchement (`create_new_session_on_fire: true`). **Auto-publication encadrée** d'au plus un sujet par passage (voir Décisions).

### À faire
- Confirmer empiriquement le comportement de l'email les jours sans rien à signaler.
- Intégrer la précision du déclencheur de clôture (B117).

### Décisions
- **Fenêtre de 30 jours sur le journal, volontairement bornée** : au-delà, un sujet qui n'a pas justifié de suivi dans le mois suivant sa publication n'en a probablement pas besoin rétroactivement ; et sans cette borne, le journal grossissant d'une ligne par jour, la recherche deviendrait de plus en plus lourde au fil des mois/années.
- **Cadence** : d'abord passée en quotidien le 1er août, puis ramenée à lundi/jeudi/vendredi **par précaution sur la consommation** (pas de visibilité précise sur le coût en tokens d'un passage quotidien, l'utilisateur a préféré rester prudent tant que ce n'est pas confirmé), puis samedi ajouté juste après — **4×/semaine au final**.
- **Seuil chiffré ≥ 20 points** depuis le 7 août, au lieu d'un simple jugement qualitatif (« il y a du neuf ou pas »).
- **Auto-publication : décision du 7 août inversée le 8 août, avec garde-fous.** Jusqu'au 8 août la routine ne créait et ne modifiait **jamais** automatiquement une page `suivi/*.html` ni `sujets-a-suivre.md` : c'était toujours un rapport de veille, le « go » restant une décision manuelle. Une première demande d'auto-publication au-delà du seuil avait été **refusée côté conception le 7 août**, pour deux raisons : (a) réévaluer un seuil chiffré à chaque passage ne garantit pas d'écarter le bruit (une estimation peut varier un peu sans vrai fait nouveau) ; (b) le rôle éditorial du site suppose un passage humain avant publication.
  **Revenu sur cette décision le 8 août, à la lumière d'un cas réel** : le jour même, la page FIFA/Infantino avait été créée manuellement alors que l'écart réel (−10 points sur le scénario favorable) restait **sous** le seuil de 20 points et que l'édition d'origine datait de seulement **2 jours** — un exemple concret du bruit que le seuil chiffré seul ne suffit pas à écarter, exactement l'objection (a). Plutôt qu'abandonner l'idée, l'utilisateur a proposé un garde-fou supplémentaire : **auto-publier au plus un seul sujet par passage** (le plus crédible, jamais tous les sujets éligibles), et **jamais un sujet dont le point de référence (dernière version publiée, ou édition d'origine si pas encore de page de suivi) a moins de 10 jours** — pour laisser un développement se confirmer avant d'y réagir, plutôt que de publier sur un pic de bruit médiatique du jour même. Avec cette règle, le cas FIFA du 8 août n'aurait de toute façon pas été auto-publié (**double filtre** : écart sous 20 points ET référence à 2 jours). L'objection (b) reste vraie en soi, mais l'utilisateur **accepte explicitement le compromis** : vérification a posteriori plutôt qu'a priori, avec rollback git en filet de sécurité si une auto-publication s'avère fausse.
- **La clôture (🏁, point 2bis du prompt) reste dans tous les cas une décision manuelle** (voir B116).
- **Notification par email (7 août)** : avant cette date, la routine tournait attachée à la session principale (`persist_session`) pour garder le contexte du site, et son rapport arrivait comme message dans cette même conversation. Recréée le 7 août en **session neuve à chaque déclenchement**, seul mode qui permette la notification email native des Routines : la session neuve n'a plus besoin de contexte de conversation puisque tout ce qu'il lui faut est déjà dans le dépôt (`docs/sujets-a-suivre.md`, pages `suivi/*.html`). Le prompt demande explicitement de répondre uniquement « RAS aujourd'hui. » et de s'arrêter là quand rien n'est notable, pour que l'email reste silencieux les jours sans rien à signaler — **comportement non garanti à 100 %**, la logique de « noteworthy » étant décidée côté plateforme, pas par la routine.
- **Documenter les révisions importantes (« +20 points parce que… ») : déjà couvert** — tout écart ≥ 20 points déclenche le marqueur ⚠️ seuil franchi, publié avec les chiffres avant/après. Rien à construire, juste continuer à l'appliquer (confirmé le 27 août face à l'audit externe).
- **Exigence ajoutée le 27 août** : l'obligation de nommer le fait (ou son absence) s'applique désormais aux 3 `mini-scenario-text` de chaque nouvelle version, pas seulement à la conclusion (voir B130).

### Historique
- **2026-08-01 [FAIT]** — Routine créée.
- **2026-08-07** — Seuil chiffré + notification email ; auto-publication refusée.
- **2026-08-08** — `docs/routine-detection-prompt.md` créé, sur le même principe que `docs/routine-prompt.md` ; auto-publication acceptée avec double garde-fou.
- **2026-08-14** — Déplacée à 2h Paris (B087).
- **2026-08-27** — Exigence « pourquoi cette probabilité » étendue aux 3 textes de scénario (B130).

---

## B124 — Vitrine des suivis clôturés (« Scénario à l'épreuve du temps » / track record)

**Statut:** BLOQUÉ
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Attendre que `suivi/` accumule de vrais cas clôturés avant de construire quoi que ce soit
**Blocage:** **Volume** — vérifié le 27 août : aucun suivi clôturé, une vitrine n'aurait rien à montrer. Même prérequis que B092 (calibration) et B142 (score historique)

### État actuel
Pas de page d'index dédiée. Le mécanisme de fond existe déjà : **une page `suivi/` clôturée raconte exactement ça** (V0 → … → clôture avec le fait qui tranche, voir B116) — ce qui manque, c'est une **vitrine** qui les rassemble, distincte de « Suivis actifs ».

### À faire
- Construire la vitrine quand il y aura des clôtures.

### Décisions
- **Décision du 8 août** : pas de page d'index « track record » pour l'instant, trop tôt vu le faible nombre de sujets suivis — à reconsidérer une fois plusieurs sujets réellement résolus.
- **2026-08-27** : le ticket externe « Scénario à l'épreuve du temps » est le même chantier, rattaché ici (rattrapé le 27 août, oublié dans la première passe de l'audit).

### Historique
- **2026-08-08** — Décision de ne pas faire de page d'index pour l'instant.
- **2026-08-27** — Rattaché à l'audit externe, classé « bloqué par le volume ».

---

## B125 — Transparence IA (article 50 du règlement européen sur l'IA)

**Statut:** FAIT
**Priorité:** Non chiffrée — obligation applicable à partir du 2 août 2026
**Dernière MAJ:** 2026-08-04
**Prochaine action:** Aucune — à rouvrir si le sujet devient sensible ou si le volume d'audience change significativement
**Blocage:** Aucun

### État actuel
- **Mention au footer de chaque édition** (`index.html`, et donc chaque `archives/AAAA-MM-JJ.html` future puisque la routine recopie ce gabarit tel quel — même mécanisme que les liens Telegram/LinkedIn, aucune instruction supplémentaire nécessaire dans `docs/routine-prompt.md`) : « 🤖 Recherche et rédaction assistées par l'intelligence artificielle. En savoir plus sur notre méthode → » (lien vers `le-projet.html`), juste après le caveat existant sur les probabilités. *(Cette ligne précise, `.ai-disclosure`, a été retirée du footer le 8 août comme redondante avec la footnote `.indicators-note` qui porte le même lien — voir B048 ; la mention complète de l'IA vit dans `le-projet.html` et `mentions-legales.html`.)*
- **Ajoutée rétroactivement aux 9 archives déjà publiées** (18 juillet au 1er août).
- **Section dédiée dans `mentions-legales.html`** (« Intelligence artificielle et transparence », entre « L'éditeur » et « L'hébergeur ») : cite l'article 50, explique que chaque édition est produite par IA à partir de sources vérifiées sous la responsabilité éditoriale d'Olivier Bertrand, renvoie vers `le-projet.html` pour le détail du processus.
- **Pas de mention IA sur LinkedIn/Telegram/email.**

### À faire
- Rien.

### Décisions
- **L'exemption jugée trop fragile pour s'appuyer dessus** : l'article 50(4) impose de signaler clairement un contenu texte généré par IA sur un sujet d'intérêt public, **sauf** exemption pour un contenu ayant subi une vraie relecture éditoriale humaine substantielle (pas une simple approbation de forme) sous la responsabilité d'une personne identifiée. Vu que la routine publie chaque édition en autonomie complète, sans validation humaine séparée avant mise en ligne, cette exemption est jugée trop fragile — **décision de toujours afficher la mention** plutôt que de tenter de revendiquer l'exemption.
- **Rétroactivité assumée comme exception** au principe « une archive ne se modifie jamais », au même titre que la correction du bilan pompiers : justifiée parce que l'obligation légale porte sur le contenu déjà en ligne au 2 août, pas seulement sur le contenu futur.
- **Formulation volontairement factuelle** (ce qui est fait), **jamais une revendication de conformité totale certifiée** — le sujet reste juridiquement nuancé.
- **Pas de mention IA sur les canaux sociaux/email (tranché le 4 août)** : ces canaux ne publient qu'un titre, un teaser et une question, qui pointent vers l'article — pas le contenu de fond lui-même. La divulgation vit là où le lecteur rencontre vraiment le texte généré. Décision aussi motivée par la **proportionnalité** : une mention « IA » sur chaque post finirait par ressembler à du bruit plutôt qu'à de l'info utile. **Pas un avis juridique certifié** (ni l'utilisateur ni Claude ne sont juristes).

### Historique
- **2026-08-01** — Ajouté (footer + rétroactif + mentions légales).
- **2026-08-04** — Question des canaux sociaux tranchée.
- **2026-08-08** — La ligne `.ai-disclosure` du footer retirée comme doublon (B048), sans remettre en cause la transparence elle-même.

---

## B126 — Audit externe du 27 août : cadrage et mapping de priorités

**Statut:** FAIT (référence, pas une tâche)
**Priorité:** —
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune — entrée de contexte pour comprendre la provenance des tickets B127 à B135
**Blocage:** —

### État actuel
L'utilisateur a soumis un backlog de **23 tickets** (priorités P0→P3) produit ailleurs. Comparé point par point à l'état réel du dépôt avant d'agir, même méthode que l'audit LLM du 20 août (B065). Plusieurs tickets recoupaient des idées ou fonctionnalités déjà présentes ; les tickets réellement nouveaux ont été retenus.

### À faire
- Rien.

### Décisions
- **Mapping de priorité** : l'échelle externe va de P0 (le plus urgent) à P3 ; le backlog consolidé reprend la même échelle P0→P3 que l'audit d'origine pour ces tickets — contrairement à `ARCHITECTURE.md`, qui va de P1 à P3. Pas de conversion nécessaire.
- **Tickets classés « déjà en place, à ne pas refaire »** (et leur ticket de rattachement ici) : mécanisme V0→V1→V2 (B112, travail éditorial restant en B127) ; récap hebdomadaire (B107/B109) ; vote communautaire / affichage des résultats (B141) ; mesure de calibration (B092) ; données ouvertes / API publique (B062) ; identité du fondateur (B128, le manque réel étant visuel et de ton) ; documenter les révisions importantes « +20 points parce que… » (B123, rattrapé le 27 août car oublié dans la première passe).
- **Ticket classé « bloqué par le volume »** : « Scénario à l'épreuve du temps » (B124, rattrapé le 27 août).
- **Contradiction à lever avant de prioriser le participatif** — le backlog externe propose de « renforcer » le vote communautaire et de « renforcer le mardi participatif ». Le sondage Telegram natif est documenté comme fonctionnant **très bien techniquement mais touchant une fraction minime du lectorat** : ce n'est donc pas un mécanisme cassé à réparer, contrairement à ce qu'un retour antérieur isolé pouvait laisser penser (`docs/routine-prompt.md`, exclusion de Telegram du bloc de notifications compact, faute de portée suffisante). « Mardi participatif », en revanche, **n'existe nulle part** dans le code ni dans `docs/routine-prompt.md` — le mardi est aujourd'hui le registre « libre, plus fort enjeu/incertitude ». **Le verbe juste est « créer », pas « renforcer »** — et ça ne devrait être cadré qu'une fois le vote sur site tranché (voir B141).

### Historique
- **2026-08-27** — Audit reçu, comparé au dépôt, trié.

---

## B127 — Réécriture éditoriale des versions de suivi déjà publiées (V0 → V1 → V2)

**Statut:** À FAIRE
**Priorité:** Non chiffrée (issue de l'audit du 27 août)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Reprendre le texte des versions déjà publiées (7 pages `suivi/*.html`) pour qu'il raconte explicitement *ce qu'on pensait → ce qui a changé → ce qu'on pense maintenant*
**Blocage:** Aucun

### État actuel
**Le travail restant est éditorial, pas technique** : le mécanisme existe déjà dans `suivi/_gabarit.html` (blocs `.version`, tag/date/titre, repliables — voir B112/B121). Ce qui manque, c'est que le texte des versions déjà publiées raconte explicitement la trajectoire, pas juste un constat factuel.

### À faire
- Repasser sur les 7 pages `suivi/*.html` existantes.

### Décisions
- Aucune de plus. Les règles de rédaction applicables sont celles de B115 et B130.

### Historique
- **2026-08-27** — Identifié dans l'audit externe.

---

## B128 — Identité du fondateur : photo et 1ʳᵉ personne

**Statut:** À FAIRE
**Priorité:** Non chiffrée (issue de l'audit du 27 août)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune planifiée
**Blocage:** Aucun

### État actuel
Le texte existe déjà (`le-projet.html`, section « Qui fait Scénario » — nom, double casquette technique/éditoriale). **Le manque réel est visuel (aucune photo) et de ton (peu de 1ʳᵉ personne)**, pas un chantier de création.

### À faire
- Ajouter une photo et/ou retravailler le ton.

### Décisions
- *À ne pas confondre avec* B063 (byline + JSON-LD `Person`), retiré le 31 août pour des raisons d'exposition personnelle — les deux sujets se recoupent et devraient être arbitrés ensemble.

### Historique
- **2026-08-27** — Identifié dans l'audit externe.

---

## B129 — Clarifier « probabilité à l'instant T »

**Statut:** FAIT
**Priorité:** P0 (audit du 27 août)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Rendu visible directement sous les 3 scénarios de chaque édition, pas seulement dans `le-projet.html` : le disclaimer fixe `.indicators-note` (`docs/routine-prompt.md`) dit désormais explicitement que les probabilités sont « estimées avec l'information disponible à la publication et réévaluées si la situation change ». Appliqué rétroactivement à l'édition du 27 août (`index.html` + `archives/2026-08-27.html`).

### À faire
- Rien.

### Décisions
- Ne s'applique qu'à partir de l'édition du 27 août (voir B134).

### Historique
- **2026-08-27 [FAIT]**.

---

## B130 — Ajouter « Pourquoi cette probabilité ? »

**Statut:** FAIT
**Priorité:** P0 (audit du 27 août)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
La logique existait déjà en grande partie dans `suivi/_gabarit.html` (chaque `mini-scenario-text` doit dire pourquoi un scénario monte/descend/reste stable ; la conclusion doit nommer le fait qui explique le plus gros mouvement) — **mais seulement dans les commentaires HTML du gabarit, jamais explicité dans le texte de la routine elle-même**. Ajouté dans `docs/routine-detection-prompt.md` : l'exigence de nommer le fait (ou son absence) s'applique désormais **aux 3 `mini-scenario-text` de chaque nouvelle version**, pas seulement à la conclusion.

### À faire
- Rien.

### Décisions
- Aucune de plus.

### Historique
- **2026-08-27 [FAIT]**.

---

## B131 — Distinguer Faits / Analyse / Scénarios sur la page

**Statut:** FAIT
**Priorité:** P0 (audit du 27 août)
**Dernière MAJ:** 2026-08-28
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Un kicker `<p class="section-label">Les faits</p>` ajouté **une seule fois**, juste après `question-box` et avant le premier `.dek` — réutilise la classe déjà stylée, **zéro CSS nouvelle, pas de re-architecture**. Documenté dans `docs/routine-prompt.md` (étape technique 3). Appliqué à l'édition du 28 août (`index.html` + `archives/2026-08-28.html`).

### À faire
- Rien.

### Décisions
- La séparation existait déjà implicitement dans la structure (`.dek` = faits/contexte, `.comprendre-box` = analyse, cartes = scénarios) mais sans étiquetage explicite. **Seul le récit factuel n'avait aucun kicker** : `.comprendre-box` a déjà « Comprendre », les cartes ont déjà `p.section-label` « Favorable, stable ou dégradé » + l'ancre `#scenarios` du sommaire.
- **Non repris sur les éditions antérieures**, même logique que les autres tickets de cet audit (voir B134).

### Historique
- **2026-08-28 [FAIT]**.

---

## B132 — Étendre le balisage Question/Faits/Scénarios à la newsletter

**Statut:** FAIT
**Priorité:** Non chiffrée (extension directe de B131)
**Dernière MAJ:** 2026-08-28
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
La `<description>` de `feed.xml` est restructurée en **3 blocs labellisés** : « La question posée : », « Les faits : » (nouveau — 2ᵉ paragraphe de « L'essentiel » repris mot pour mot, **remplace `.stakes-text` jugée redondante ici**), « Les 3 scénarios : » (+ émoji couleur 🟢/🔵/🔴 par ligne, même code que `<category>`). Détail dans `docs/routine-prompt.md`, étape technique 8.

### À faire
- Rien. *(Cette structure servira de base au contenu de l'email OneSignal si la migration a lieu, voir B004.)*

### Décisions
- Retour utilisateur : « la lecture doit être plus simple ». Avant, la Description enchaînait question, `.stakes-text` et 3 titres de scénarios sans aucune étiquette ni fait chiffré.
- **Appliqué à partir de l'édition du 29 août** — l'email du 28 août était déjà envoyé au moment de ce ticket, et **`feed.xml` n'est jamais retouché sur un item déjà consommé**.

### Historique
- **2026-08-28 [FAIT]**.
- **2026-09-02** — Une note de `feed.xml`/étape technique 3bis affirmait encore que « Ce qu'on évalue » servait de second paragraphe de la `<description>`, périmé depuis ce retrait du 28 août ; corrigé à cette occasion (voir B147).

---

## B133 — Renforcer « Notre méthode » sur `le-projet.html`

**Statut:** FAIT
**Priorité:** P0 (audit du 27 août)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
`le-projet.html` avait déjà une section méthode (« Les probabilités affichées ne sortent pas d'un tirage au hasard... ») avec ses 4 axes en liste — ajouté un **paragraphe de clôture** qui explicite que c'est un **jugement structuré, pas un algorithme**, pour ne jamais laisser croire à une précision scientifique que les faits du jour ne permettent pas.

### À faire
- Rien.

### Décisions
- Aucune de plus.

### Historique
- **2026-08-27 [FAIT]**.

---

## B134 — Rattrapage historique des tickets éditoriaux de l'audit

**Statut:** ABANDONNÉ
**Priorité:** —
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune — **ne pas rouvrir ce chantier sans nouveau retour explicite**
**Blocage:** —

### État actuel
**Tranché le 27 août, retour utilisateur : « non ».** Les 4 tickets concernés (probabilité à l'instant T, pourquoi cette probabilité, méthode, CTA newsletter — B129/B130/B133/B135) s'appliquent seulement à partir de l'édition du 27 août : **les 34 éditions précédentes ne sont pas reprises.**

### À faire
- Rien.

### Décisions
- **Assumé comme décision, pas comme un oubli** — l'avant/après entre archives anciennes et nouvelles reste cohérent avec la règle générale « archives figées, jamais remodifiées après publication ».
- *Exceptions déjà admises ailleurs, pour mémoire* : la transparence IA (B125, obligation légale) et le bandeau d'accueil `.intro-banner` (B052, élément de structure et non de contenu éditorial).

### Historique
- **2026-08-27** — Tranché.

---

## B135 — CTA newsletter (wording)

**Statut:** FAIT
**Priorité:** Non chiffrée (audit du 27 août — sorti d'un ticket groupé, traité seul, « wording only, zéro coût »)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
`.follow-inline-text` (bloc compact réutilisé chaque édition, `docs/routine-prompt.md`) reformulé en impératif : **« Ne rate pas la prochaine édition : »** au lieu de « Reste informé de la prochaine édition : ». Un sous-titre ajouté à `newsletter.html` (gratuit / sans spam / résiliable en un clic), qui manquait sous le h1. Appliqué rétroactivement à l'édition du 27 août.

### À faire
- Rien.

### Décisions
- Traité seul parce que sans coût, contrairement au reste du ticket groupé.

### Historique
- **2026-08-27 [FAIT]**.

---

## B136 — Pages thématiques `themes/*.html` et maillage interne

**Statut:** FAIT
**Priorité:** P1 (volet de l'audit du 27 août)
**Dernière MAJ:** 2026-08-31
**Prochaine action:** Aucune. Geste **hebdomadaire** documenté : régénérer les pages via le script (pas une étape quotidienne)
**Blocage:** Aucun

### État actuel
**6 pages statiques crawlables sous `themes/{slug}.html`**, une par « domaine » de `docs/tags.md` §2 (regroupement déjà utilisé par le panneau « Détail par domaine » d'`archives.html`), chacune listant avec un vrai lien `<a>` tous les articles du domaine — **c'est ça le maillage interne**. Générées par `scripts/seo/generate_theme_pages.py` (idempotent). Domaines retenus (seuls ceux avec ≥ 8 articles) : Économie & entreprises, International, Sciences & environnement, Culture & divertissement, Politique & institutions, Tech & numérique. **`Société` et `Sport & argent` exclus**, trop peu d'articles (contenu « thin »). Les 6 URLs sont dans `sitemap.xml`. **Les 6 pages sont volontairement orphelines** : aucun lien interne ne pointe vers elles depuis le site, seul `sitemap.xml` les signale à Google — sauf via le menu déroulant « Archives ▾ » des nouvelles pages (voir B137). Pages en français uniquement, pas de `en/themes/` (voir B139).

### À faire
- Rien. Volet « titres SEO » du ticket d'origine toujours ouvert : voir B140.

### Décisions
- **Motif** : le filtre `archives.html?tag=X` ne produit **aucune URL crawlable** par Google (JS pur, même adresse).
- **Ressorti de la routine quotidienne le jour même** (retour utilisateur : « il faut alléger nos routines ») : d'abord branché en étape 7ter, puis transformé en **geste hebdomadaire documenté** dans `docs/routine-prompt.md` — aucun effet visible côté lecteur ou Google à un décalage de quelques jours.
- **Bloc « Explorer par thème » sur `archives.html` : ajouté le 31 août, retiré le jour même** (retour utilisateur). Sans amélioration UX dessus (pas de teaser/vignette, juste une liste titre+date — voir la décision « pas d'usine à gaz » du même jour) et vu que ces pages restent hors de la lecture quotidienne, le bandeau donnait **l'illusion d'une intégration dans le parcours utilisateur sans l'être vraiment** — retiré pour rester honnête.
- **Compromis assumé de l'orphelinat** : ces pages gagnent moins d'autorité de liens internes qu'avec le bandeau (une page vers laquelle personne ne lie en interne se positionne généralement moins bien), mais restent utiles pour le maillage **sortant** (chaque page thématique continue de lier vers les articles qu'elle liste) et comme point d'entrée si un lecteur arrive dessus depuis une recherche Google.
- **Lien discret dans le footer d'`archives.html` : essayé le 31 août, retiré le jour même** — retour utilisateur : « illogique et dirty », revert complet (voir PR #26).
- **Point de départ déjà favorable, pas de construction ex nihilo** (constat de l'audit) : glossaire déjà alimenté chaque jour (étape 6ter, B042), tags fermés dans `docs/tags.md` réutilisables, filtre `archives.html?tag=X` déjà en place comme brique de départ.

### Historique
- **2026-08-27** — Ticket P1 de l'audit (titres SEO / glossaire / pages thématiques / maillage interne) : « tickets valides, effort raisonnable mais pas du texte seul (page/template à construire) ».
- **2026-08-31 [FAIT]** — Les 6 pages créées ; bloc « Explorer par thème » ajouté puis retiré ; lien footer essayé puis reverté ; génération sortie de la routine quotidienne.

---

## B137 — Menu déroulant « Archives ▾ » dans le nav commun

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-31
**Prochaine action:** Aucune — les pages déjà publiées gardent l'ancien lien simple jusqu'à nouvel ordre
**Blocage:** Aucun

### État actuel
« Archives » devient le déclencheur d'un panneau qui se déplie juste en dessous du nav, avec **8 liens** : Toutes les archives, les 6 domaines (voir B136), Récap de la semaine. Vérifié par capture d'écran (Playwright, desktop + mobile 390px) que le panneau n'est pas coupé par le défilement horizontal de `.topnav .wrap`. Documenté dans `docs/routine-prompt.md` (étape technique 2) comme **exception explicite à « ne jamais changer la structure du gabarit »**. **Portée volontairement limitée aux nouvelles pages** (retour utilisateur : pas de rétrofit des 76 pages déjà publiées) — le dropdown apparaît à partir de l'édition suivante.

### À faire
- Rien.

### Décisions
- **Changement de comportement assumé** : « Archives » ne mène plus directement à `archives.html` en un clic (il faut ouvrir le panneau, « Toutes les archives → » en est le premier item) — **accepté par l'utilisateur** en échange d'un vrai point d'entrée vers les pages thématiques.
- Retenu à la place du lien discret en footer, jugé « illogique et dirty » (B136).

### Historique
- **2026-08-31 [FAIT]** — Retour utilisateur formulé comme une réflexion à voix haute pendant la session.
- **2026-08-31** — Ce chantier est l'exemple concret qui a nourri le ticket CMS (B056) : 76 fichiers HTML à retoucher un par un pour un changement de nav.

---

## B138 — Rôle et avenir d'`archives.html` lui-même

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-31
**Prochaine action:** Le jour où le sujet revient, partir de la **liste de fonctions à préserver** ci-dessous, pas seulement de la question de nav
**Blocage:** Question ouverte, volontairement pas tranchée sur le moment

### État actuel
Question posée par l'utilisateur en repensant à l'accès aux thèmes : « le fichier archive, il doit donc plus exister ? » — **pas de réponse improvisée sur le moment, volontairement.**

### À faire
- Trancher, le cas échéant.

### Décisions
- **Éléments à remettre sur la table** : `archives.html` n'est pas qu'une entrée de nav, c'est une page à part entière avec recherche, filtre par année, tri (date de publication / dernière mise à jour), filtre « Sujet révisé » (`?tag=revise`, **dont dépend l'icône du masthead sur toutes les pages du site**), vignettes, accordéon « Scénarios ▾ » — **rien de tout ça n'est couvert par les 6 pages thématiques ni par le récap hebdo**. Une restructuration ou fusion éventuelle devrait donc partir de cette liste de fonctions à préserver.

### Historique
- **2026-08-31** — Question ouverte consignée.

---

## B139 — Pages thématiques en anglais (`en/themes/`)

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-08-31
**Prochaine action:** **À revisiter au plus tôt le 15 septembre 2026**, en même temps que le check Google Actualités posé sur `en/` — et à retraiter **ensemble** avec « traduire plus d'articles » (B008), pas l'un sans l'autre
**Blocage:** Volume d'articles traduits trop faible par domaine

### État actuel
**Pas retenu pour l'instant.** Vérifié avant de trancher : sur les 5 articles déjà traduits (`en/archives/`), la répartition par domaine est bien trop pauvre pour justifier une page — **Culture & divertissement : 4, Économie & entreprises : 2, International : 1, les 3 autres domaines à 0** — on retomberait exactement dans le contenu « thin » évité côté français avec le seuil ≥ 8 (voir B136).

### À faire
- Revisiter le 15 septembre 2026.

### Décisions
- Cohérent aussi avec `docs/strategie-anglais.md` : pages statiques secondaires non traduites tant que l'audience anglaise n'est pas confirmée.

### Historique
- **2026-08-31** — Question posée, vérifiée, non retenue pour l'instant, avec un repère de calendrier.

---

## B140 — Optimiser les titres SEO et développer le glossaire

**Statut:** À FAIRE
**Priorité:** P1 (volets restants du ticket P1 de l'audit du 27 août)
**Dernière MAJ:** 2026-08-31
**Prochaine action:** Traiter le volet « titres SEO », explicitement resté ouvert le 31 août
**Blocage:** Aucun

### État actuel
Les volets « pages thématiques » et « maillage interne » du ticket P1 d'origine sont faits (B136/B137). **Le volet « titres SEO » est toujours ouvert** (pas traité le 31 août). Le volet « développer le glossaire » part d'une base déjà solide : glossaire alimenté chaque jour par l'étape 6ter de `docs/routine-prompt.md` (B042).

### À faire
- Optimiser les titres SEO.
- Développer le glossaire au-delà de son alimentation automatique quotidienne.

### Décisions
- Aucune de plus.

### Historique
- **2026-08-27** — Ticket P1 groupé de l'audit externe.
- **2026-08-31** — Deux volets livrés, ce volet explicitement laissé ouvert.

---

## B141 — Vote sur site, puis « mardi participatif »

**Statut:** STANDBY
**Priorité:** P2 → **dépriorisé le 27 août** (retour utilisateur : « pas urgent ça »)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** **Ne pas relancer de son propre chef**, attendre un nouveau retour explicite. Quand ça redevient prioritaire : trancher d'abord le point ouvert du 26 août (afficher un pourcentage en direct ou non), implémenter le vote sur site, **puis seulement** cadrer un « mardi participatif »
**Blocage:** Dépriorisé ; un point de conception reste ouvert

### État actuel
Reste ouvert mais plus sur la liste des prochains chantiers. Le mécanisme envisagé est déjà posé : **clic → événement GoatCounter côté client, zéro backend**. Le point non tranché : **afficher ou non un pourcentage en direct**. Le sondage Telegram natif (`sendPoll` sur `@scenario_fr`, voir B099) fonctionne très bien techniquement mais touche une fraction minime du lectorat : ce n'est pas un mécanisme cassé à réparer.

### À faire
- Trancher l'affichage d'un pourcentage en direct.
- Implémenter le vote sur site.
- Puis **créer** (pas « renforcer ») un mardi participatif — il n'existe nulle part dans le code ni dans `docs/routine-prompt.md` ; le mardi est aujourd'hui le registre « libre, plus fort enjeu/incertitude ».

### Décisions
- **Séquence imposée** : vote sur site d'abord, mardi participatif ensuite, puisqu'un mardi participatif en dépendrait probablement.
- Zéro backend, cohérent avec le principe du site.

### Historique
- **2026-08-26** — Entrée d'origine (« Faire remonter le vote quotidien sur le site en plus de Telegram ») : mécanisme et point ouvert posés. *Note de traçabilité : cette entrée du 26 août est référencée à plusieurs endroits comme étant « plus haut dans ce backlog » mais ne s'y trouve pas — son texte complet vit probablement dans `docs/ARCHITECTURE.md`.*
- **2026-08-27** — Dépriorisé ; contradiction du backlog externe levée (voir B126).

---

## B142 — Score historique de Scénario

**Statut:** BLOQUÉ
**Priorité:** P3 (audit du 27 août)
**Dernière MAJ:** 2026-09-02
**Prochaine action:** Documenter le prérequis commun aux trois tickets plutôt que de lancer trois chantiers indépendants
**Blocage:** **Un export structuré scénario ↔ résultat réel constaté**, qui n'existe pas encore et conditionne aussi B092 (calibration) et B062 (données ouvertes)

### État actuel
Nouveau par rapport à l'existant (la calibration du 10 août mesure la justesse globale, pas un score de suivi dans le temps) — mais dépend du même préalable.

### À faire
- Construire (ou définir) l'export structuré scénario ↔ résultat réel.

### Décisions
- **À traiter comme un prérequis commun à trois tickets** (B142, B092, B062), pas trois chantiers indépendants.
- Sera une future brique du dashboard interne (B149, KPI niveau 4).

### Historique
- **2026-08-27** — Retenu comme ticket nouveau de l'audit.
- **2026-09-02** — Classé « niveau 4 : pas encore possible » dans la pré-analyse du dashboard.

---

## B143 — Créer « Nos erreurs / enseignements »

**Statut:** À FAIRE
**Priorité:** P1/P2 (audit du 27 août — rattrapé le 27 août, oublié dans la première passe, aucune trace ailleurs dans le dépôt)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Cadrer le contenu — aucune piste de contenu encore identifiée dans le dépôt tel qu'il est
**Blocage:** Aucun (et, contrairement à la calibration, **pas de prérequis de volume**)

### État actuel
Aucun équivalent existant, contrairement à la plupart des autres tickets de cet audit. Idée : une page ou section qui assume les scénarios où l'estimation s'est trompée et ce que ça a changé dans la méthode.

### À faire
- Cadrer avant de lancer.

### Décisions
- **Sert la même crédibilité que la calibration (B092) mais n'a pas son prérequis de volume** : une erreur peut être documentée dès qu'elle est constatée sur un suivi révisé — `suivi/` marque déjà **⚠️ seuil franchi** quand une estimation bouge fort (B123) ; cette page raconterait ***pourquoi*** on s'était trompé, pas seulement ***que*** l'estimation a changé.

### Historique
- **2026-08-27** — Retenu comme ticket nouveau de l'audit.

---

## B144 — Créer une boucle réseaux → site → newsletter

**Statut:** À FAIRE
**Priorité:** P2 (audit du 27 août — rattrapé le 27 août, oublié dans la première passe)
**Dernière MAJ:** 2026-08-27
**Prochaine action:** Ajouter une ligne d'appel newsletter dans le gabarit de légende déjà utilisé pour Telegram/Instagram (piste la moins chère)
**Blocage:** Aucun

### État actuel
**Vérifié le 27 août** : aucun des canaux sociaux automatisés (Telegram, Instagram, LinkedIn, Facebook, Bluesky, X — pipeline Make.com, voir B003/B014/B020/B022/B024/B025/B037) ne mentionne la newsletter dans ses légendes/teasers, **seulement un lien vers l'article**.

### À faire
- Ajouter l'appel newsletter dans les légendes — même bloc que le rappel `.follow-inline` du site, juste reformulé pour un post social.

### Décisions
- **Objectif** : transformer les réseaux en acquisition d'abonnés, pas seulement en diffusion de lecture.
- **Piste la moins chère retenue** : modifier le gabarit de légende existant plutôt que construire un nouveau canal.

### Historique
- **2026-08-27** — Retenu comme ticket nouveau de l'audit.

---

## B145 — Titres de scénarios : toujours littéraux, jamais une image ambiguë

**Statut:** FAIT
**Priorité:** Non chiffrée (audit du 27 août)
**Dernière MAJ:** 2026-08-28
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
Règle renforcée à l'étape 4 de `docs/routine-prompt.md` : **4 catégories à écarter avec exemples avant/après** — métaphores de guerre/nature, portes figurées, idiomes tronqués, personnification d'un objet abstrait. Exemples réels retrouvés dans les archives : « Le front s'enterre pour l'hiver », « La porte reste entrouverte », « [Le dossier] sort de l'ornière », « La loi patiente ». Plus un **test rapide avant validation** : « un lecteur qui ne lit que ce titre, seul, comprendrait-il ce qui se passe ? » **Non repris sur les titres déjà publiés** — s'applique aux éditions à partir du 28 août.

### À faire
- Rien.

### Décisions
- La règle « la taxe cale » existait déjà (section Style de `docs/routine-prompt.md`) mais restait un exemple isolé, pas un test systématique pour les `<h3>` des cartes.

### Historique
- **2026-08-28 [FAIT]** — Retour utilisateur : « les titres manquent de clarté, tu utilises toujours des images qui créent une ambiguïté non voulue » — choisir les 3 titres « de façon claire et pragmatique ».

---

## B146 — Français naturel partout, pas seulement sur les encarts Comprendre

**Statut:** FAIT
**Priorité:** Non chiffrée (audit du 27 août)
**Dernière MAJ:** 2026-08-28
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
La règle anti-« IA » du 21 août (`docs/routine-prompt.md`, Style) ne couvrait que deux pièges précis vus sur un encart Comprendre (négation abrupte après une affirmation, source nuancée durcie en claim absolu) — **étendue à toute phrase de l'édition**, avec 3 nouveaux symptômes à repérer : subordonnée enchâssée au milieu d'une phrase plutôt qu'un ordre naturel ; connecteurs lourds empilés (« de fait », « il convient de noter que »...) ; formulation en creux/double négation là où l'affirmation directe est plus claire. Même test que pour les titres de scénario (B145) : **« je dirais ça comme ça, à voix haute, dans une conversation normale ? »**

### À faire
- Rien.

### Décisions
- Aucune de plus.

### Historique
- **2026-08-28 [FAIT]** — Retour utilisateur : « les tournures doivent être en français naturel, pas de style IA, parfois tournure tordue ».

---

## B147 — « Ce qu'on évalue » restructuré en 3 branches étiquetées

**Statut:** FAIT
**Priorité:** Non chiffrée (audit du 27 août)
**Dernière MAJ:** 2026-09-02
**Prochaine action:** Aucune
**Blocage:** Aucun

### État actuel
`<ul class="stakes-branches">` remplace le `<p class="stakes-text">` : une ligne par branche, chacune ouverte par un `<span class="stakes-tag">` coloré (Favorable/Stable/Dégradé, **même code couleur que `.kind-tag` sur les cartes juste en dessous**) — le rapprochement entre une branche et sa carte se fait désormais d'un coup d'œil. Le texte de chaque branche passe de la forme interrogative à une **phrase déclarative courte** (« L'Anses résiste et refuse... » plutôt que « Est-ce que l'Anses résiste et refuse... ? »). **`.stakes-text` reste défini en CSS** (compatibilité des archives publiées avant cette date, où il est toujours utilisé) **mais ne doit plus être utilisé pour une nouvelle édition.** Même périmètre d'application que B047 : édition du jour, FR + EN, pas les archives antérieures.

### À faire
- Rien.

### Décisions
- **Motif** : l'encart existait déjà et portait bien les 3 branches favorable/stable/dégradé, mais enchaînées dans un seul paragraphe sous forme de questions — **le lien entre chaque sous-question et son scénario n'était porté que par l'ordre de lecture**, invisible pour qui ne connaît pas déjà la convention du site.
- **Déclaratif plutôt qu'interrogatif** : le mot-repère qui ouvre la ligne dit déjà qu'il s'agit d'une branche, la question n'ajoutait rien — plus simple, conformément au retour utilisateur.
- **Correction collatérale** : une note de `feed.xml`/étape technique 3bis affirmait encore que « Ce qu'on évalue » servait de second paragraphe de la `<description>`, **périmé depuis le retrait du 28 août** (B132) et jamais reporté à cet endroit — corrigé au passage.

### Historique
- **2026-09-02 [FAIT]** — Retour utilisateur le même jour : « ce qu'on évalue n'est pas clair, il doit être plus pédagogique, expliquer ce qu'on dit en favorable/stable/dégradé, être plus clair et surtout simple ». `docs/routine-prompt.md` mis à jour (étape 3 : nouveau gabarit HTML + explication du changement ; règle de style correspondante).
---

## B148 — Dashboard de pilotage interne (`dashboard.html`)

**Statut:** FAIT (V1 livrée le 2 septembre, affinée jusqu'au 3 septembre)
**Priorité:** P2 à l'origine
**Dernière MAJ:** 2026-09-03
**Prochaine action:** Aucune. Suites traitées séparément : B149 (KPI niveaux 2-3), B151 (migration vers un GitHub Action)
**Blocage:** Aucun

### État actuel
`dashboard.html` à la racine du dépôt — **non lié depuis la nav**, `<meta name="robots" content="noindex, nofollow">`, exclu de `robots.txt` (`Disallow: /dashboard.html`), **jamais ajouté à `sitemap.xml`**. Accès par **code comparé à un hash SHA-256 embarqué dans la page** (jamais le code en clair dans le dépôt — voir le commentaire CSS `.gate` dans le fichier), code mémorisé en `localStorage` après une première saisie réussie. Code en vigueur depuis le 3 septembre : `renard-brasier-granit-75` (l'ancien `-63` a été révoqué). Une **icône cadenas** dans `.masthead-right` d'`index.html` y donne accès (« Accès privé »), reproduite chaque matin par la routine. Un lien « ← Retour au site » est présent dans les deux états (porte verrouillée et page déverrouillée). Régénéré à chaque passage de la routine hebdomadaire « Scénario — Audience » (`docs/routine-audience-prompt.md`, étape 3bis), en réutilisant les données déjà récupérées pour `#audience` — **pas d'appel API supplémentaire**. Le code d'accès n'est ni régénéré ni recommuniqué par cette routine.

**Contenu** : 5 cartes KPI (lectures cumulées ; **7 derniers jours glissants** + delta ; **30 derniers jours glissants** + delta ; cadence de publication ; moyenne par édition), graphique hebdomadaire non cumulé `#weekly-svg` (le vrai signal, buckets **semaines ISO lundi → dimanche**, premier ET dernier bucket marqués partiels), graphique cumulé `#cumul-svg` repris de `le-projet.html` (repère de fond, étiquette de fin « 424 lectures · 41 éditions »), top 5 / flop 5 des éditions par lectures, « Lectures par domaine », « Agenda de la semaine » (cartes `.agenda-card`, fenêtre lundi → dimanche) + « semaine d'après » (`.agenda-later-list`), « Suivis actifs — prochaines échéances », « Autonomie par registre ».

### À faire
- Rien sur la V1.

### Décisions
- **Constat de départ, corrigé dans le dashboard lui-même — pas seulement y ajouter des métriques** : le graphique `#audience` (cumul de lectures) est **par construction toujours croissant** — une courbe cumulative ne peut jamais montrer un ralentissement, seulement des paliers plus ou moins pentus, difficiles à lire à l'œil. Pour répondre à la vraie question posée (« ça avance ou pas ? »), le dashboard priorise des séries **non cumulatives** (lectures de la semaine, delta semaine sur semaine), le cumulatif gardant sa place comme repère de fond.
- **Où vit le dashboard : option 2 retenue** (« une page cachée ou privée via password sur le site », retour utilisateur du 2 septembre). Les trois options étaient : *étendre `le-projet.html`* — **écarté d'instinct** : cette page a un rôle de preuve sociale pour le **lecteur** (un chiffre, une courbe, minimal et propre), pas d'outil de pilotage interne ; y afficher publiquement un nombre d'abonnés newsletter aujourd'hui minuscule (« 3 pelés ») desservirait la crédibilité que la page cherche à construire ; *nouvelle page statique non liée depuis la nav*, régénérée par une routine hebdomadaire — même mécanisme que `#audience`, cohérent avec le principe zéro-backend et avec un précédent déjà posé (« dépôt GitHub privé... écarté, aucun contenu n'est réellement sensible », B094), avec la réserve que la page reste servie publiquement par GitHub Pages (juste non indexée/non linkée), une catégorie de donnée un peu différente des notes éditoriales internes ; *Artifact Claude privé* — zéro trace dans le dépôt public, zéro risque d'exposer un chiffre interne, mais un mécanisme de mise à jour différent du reste du site (pas de précédent).
- **Avertissement explicite laissé dans le fichier, à ne jamais nettoyer** : cette protection est une **dissuasion, pas une vraie sécurité** — le contenu reste techniquement présent dans le HTML envoyé au navigateur (site 100 % statique, zéro backend), donc quelqu'un qui lirait le code source contournerait la porte. Suffisant contre un passage accidentel, pas contre une donnée vraiment sensible.
- **Changement de modèle de protection assumé le 3 septembre, pas une régression** : jusque-là, l'absence de tout lien visible dans le HTML public était une couche de dissuasion en plus du code d'accès ; avec l'icône posée sur chaque édition, la page est à un clic depuis le site public, **seul le code d'accès protège encore le contenu**. Signalé à l'utilisateur avant d'implémenter, décision maintenue.
- **KPI niveau 1 uniquement pour la V1**, comme proposé dans la pré-analyse — phasage explicitement validé pour juger vite si le format répond au besoin avant d'investir dans les intégrations plus lourdes.
- **Fenêtres glissantes plutôt que semaines calendaires fixes** pour les cartes (évite la redondance avec le graphique hebdomadaire à buckets fixes, qui garde son rôle de tendance multi-semaines). Contrainte explicite de l'utilisateur pour ces affinages : « ça ne doit pas nous coûter une blinde » → **zéro appel GoatCounter supplémentaire**.
- **Bloc « Agenda de la semaine » explicitement présenté comme un aperçu de l'ordre actuel, pas un calendrier garanti** — la routine quotidienne peut réordonner ou insérer une priorité absolue.
- **Convention lundi → dimanche** pour l'agenda comme pour le graphique hebdomadaire : le renouvellement de la file (`sujets-prioritaires.md`) se fait le lundi.
- **Ne jamais retirer le fix bfcache** (écouteur `pageshow` + vidage des conteneurs avant re-rendu) lors des régénérations hebdomadaires — mise en garde explicite dans `docs/routine-audience-prompt.md`.

### Historique
- **2026-09-02 (demande + pré-analyse)** — Retour utilisateur direct, à la suite de la mise à jour manuelle du graphique d'audience de `le-projet.html` le même jour : envie d'un tableau de bord regroupant ce graphique **et** d'autres KPI, pour juger de la progression du projet dans son ensemble. Pré-analyse demandée avant tout chantier, avec les **KPI candidats classés par coût réel de mise en œuvre** (à ne pas sous-estimer : chaque plateforme sociale a sa propre API/auth, ce n'est pas une ligne de config par réseau) :
  1. **Déjà exploitable immédiatement, aucune nouvelle intégration** : lectures par semaine/jour (delta du cumul déjà récupéré, pas seulement le total) ; **visiteurs uniques** (`count_unique` de l'API GoatCounter, jamais exploité jusqu'ici — à ne pas confondre avec `count`, volontairement seul utilisé pour le compteur public « Lu X fois », voir `docs/ARCHITECTURE.md`) ; trafic total du site, pages fonctionnelles comprises (écarté pour la vitrine *publique* du 21 août parce que ça mélangeait avec les vraies lectures d'article — **non pertinent ici, un dashboard interne peut et doit regarder `contact.html`/`newsletter.html` aussi**) ; cadence de publication réelle (calculable depuis `archives/` et l'historique Git, zéro API externe) ; classement des éditions par lectures (le compteur par article existe déjà, juste jamais agrégé en top/flop) ; répartition par thème/registre (tags déjà posés).
  2. **Exploitable avec un peu de travail** : nombre d'abonnés newsletter — dépend du calendrier de la migration Buttondown → OneSignal (B004) ; **ne pas dupliquer ce chantier, juste piocher dedans une fois fait**.
  3. **Nouvelle intégration par plateforme, effort réel** : abonnés X/Bluesky/LinkedIn/Facebook/Instagram/Telegram (6 API différentes, 6 authentifications différentes) ; montant/nombre de dons Buy Me a Coffee. **Ne pas viser les 6 réseaux d'un coup — commencer par 1-2** (Bluesky et Telegram ont les API les plus simples).
  4. **Pas encore possible, déjà connu du backlog** : calibration (B092) et score historique (B142), tous deux bloqués par le volume de suivis clôturés — **à relier comme future brique du même dashboard le jour où ce prérequis est levé, pas un chantier séparé**.
- **2026-09-02 [FAIT] — V1 livrée le jour même**, avec en plus un besoin signalé en cours de route et non anticipé dans la pré-analyse : « préparer le calendrier et les sujets prévisionnels aussi » → blocs « Semaine à venir » (prochain sujet en tête de chaque registre de `sujets-prioritaires.md`) et « Suivis actifs — prochaines échéances » (les 7 suivis de `docs/sujets-a-suivre.md`, triés par date connue la plus proche, liens directs vers chaque page `suivi/`).
- **2026-09-02 (vrai bug trouvé et corrigé à la vérification Playwright)** — `[hidden]{ display:none !important; }` manquant : sans cette règle, la feuille de style auteur (`.gate{display:flex}`) l'emportait sur le `display:none` par défaut du navigateur pour `[hidden]`, et **la porte restait affichée à l'écran alors même que `gate.hidden === true` en JS** (confirmé par inspection directe du DOM).
- **2026-09-02 (chiffres du jour)** — **+65 % de lectures cette semaine vs la précédente, elle-même +87 % vs celle d'avant** — tendance en accélération, premier vrai signal quantifié côté « ça avance ».
- **2026-09-02 (même soir) [FAIT] — trois affinages** : (a) KPI en fenêtres glissantes — « 7 derniers jours » et « 30 derniers jours », ce dernier nouveau (**≈ 94 % du cumul total sur les 30 derniers jours** — pas encore de comparaison aux 30 j précédents, il faut 60 jours d'historique, on n'en a que 36) ; (b) **« Lectures par domaine »**, nouveau bloc : `data-domain` déjà posé sur chaque ligne d'`archives.html` (voir `docs/tags.md`), joint aux lectures déjà filtrées par article — aucune nouvelle donnée, juste un regroupement différent du même total, trié par moyenne par édition (**Sciences & environnement en tête à 15,5 ; Tech & numérique dernier à 7,7 — mais seulement 3 éditions sur ce domaine, échantillon à interpréter avec prudence**) ; (c) « Semaine à venir » devient **« Agenda de la semaine »**, cartes visuelles (`.agenda-card`, une grille) plutôt qu'un tableau.
- **2026-09-02 (repéré au moment de pousser sur `main`)** — `docs/sujets-a-suivre.md` avait été mis à jour entre-temps par la routine quotidienne (nouveau suivi actif, « Big Tech face à la justice », jugement attendu sous 30 jours) : le tableau « Suivis actifs » a été réordonné avant publication pour ne pas livrer une donnée périmée dès le premier jour. `docs/routine-audience-prompt.md` mis à jour (étape 3bis étendue).
- **2026-09-03 [FAIT] — icône d'accès dans `.masthead-right`** : retour utilisateur « met un petit icone en haut a droite pour y accéder ». Icône barres (`.masthead-notif-btn`, même style que les autres boutons de la ligne — cloche, impression, « Sujet révisé », « Récap de la semaine »), pointant vers `dashboard.html`. Appliqué **uniquement à `index.html`**, donc reproduit automatiquement chaque matin. **Essai initial sur `archives/2026-09-02.html` annulé avant de pousser** : commencé pendant que cette page était encore l'édition du jour, mais la routine quotidienne a publié l'édition du 3 septembre entre-temps — la page était devenue une archive figée au moment de committer, retiré pour respecter la règle « jamais remodifiée après publication ». **Pas ajouté sur les pages EN** (dashboard entièrement en français, usage interne).
- **2026-09-03 [FAIT] — icône revue en cadenas** : retour utilisateur — l'icône barres ne disait pas assez clairement « accès privé » et ne signalait pas le curseur au survol. `aria-label`/`title` passés de « Tableau de bord » à « Accès privé » (le curseur pointer était déjà hérité du style de bouton). `archives/2026-09-03.html` — créée par la routine avant que l'icône n'existe sur `index.html` ce matin-là — n'avait jamais hérité de l'icône : ajoutée directement dans sa version finale (cadenas), sans repasser par la version intermédiaire.
- **2026-09-03 [FAIT] — rotation du code d'accès** : retour utilisateur explicite (`renard-brasier-granit-63` → `renard-brasier-granit-75`) — hash SHA-256 recalculé et remplacé, ancien code vérifié révoqué et nouveau code vérifié fonctionnel avant de considérer la demande faite.
- **2026-09-03 [FAIT] — bouton retour + nombre cumulé d'éditions** : retour utilisateur urgent (coincé dans l'app sans moyen de revenir au site). Lien « ← Retour au site » (`.dash-back`, vers `index.html`) ajouté en premier enfant de l'écran de porte (`.gate-box`) **et** de l'en-tête déverrouillé (`.dash-header`). Étiquette de fin de courbe du graphique cumulatif complétée : « 424 lectures » → « **424 lectures · 41 éditions** » — distingue le nombre de jours de suivi du nombre réel d'éditions publiées, les deux compteurs n'avançant pas au même rythme (jours sans publication, ou plusieurs publications le même jour).
- **2026-09-03 [FAIT] — correctif graphiques vides après retour arrière (bug bfcache)** : retour utilisateur avec capture d'écran — après avoir quitté le dashboard déverrouillé puis y être revenu, la page restait déverrouillée (code non redemandé) mais les graphiques et tableaux s'affichaient **vides** (conteneurs et titres présents, contenu absent). Diagnostic : restauration depuis le **bfcache** du navigateur/webview, le JS de rendu ne se rejoue pas tout seul. **Fix** : écouteur `pageshow` avec `event.persisted` relançant `renderCharts()` **uniquement** lors d'une restauration bfcache (jamais à un chargement normal), combiné à un **vidage systématique des conteneurs** en tête de `renderWeekly()`, `renderCumul()` et `fill()` (tableaux) pour que ce second rendu ne duplique jamais le contenu. Vérifié via Playwright (déclenchement manuel d'un `pageshow` avec `persisted:true`) : nombre d'éléments enfants identique avant/après, ni duplication ni vide.
- **2026-09-03 [FAIT] — agenda recalé lundi → dimanche + aperçu « semaine d'après »** : retour utilisateur — le renouvellement de la file se fait le lundi, l'agenda devait donc montrer une semaine complète à venir plutôt qu'une fenêtre « aujourd'hui + 6 jours » qui dérive au fil de la semaine et finit par mordre sur la semaine suivante sans le dire. Les 7 cartes réordonnées sur la fenêtre **lundi 7 → dimanche 13 septembre** (premier sujet non coché de chaque registre, une fois l'édition du jour même — jeudi 3, Marchés financiers — cochée). Nouveau bloc compact `.agenda-later-list` : pour chaque registre, le **2ᵉ** sujet en attente. **Carte blanche et Culture n'ont chacune qu'un seul sujet encore en réserve** — indiqué explicitement (« rien en réserve après … », classe `.agenda-later-empty`) plutôt que de laisser la ligne vide ou de l'omettre. `docs/routine-audience-prompt.md` (étape 3bis) étendu : convention lundi → dimanche explicitée, nouveau bloc documenté (2ᵉ `- [ ]` non coché par registre, texte intégral de l'accroche).
- **2026-09-03 [FAIT] — graphique « Lectures par semaine » recalé sur de vraies semaines calendaires** : retour utilisateur — « est-ce que tu fais bien les éditions du lundi au dimanche ? je trouve bizarre d'avoir que 24 sur cette semaine encore inachevée ». **Diagnostic confirmé** : les buckets de `#weekly-svg` étaient calés sur le jour de lancement du site (mercredi 29 juillet), donc des semaines mercredi→mardi et non lundi→dimanche — la dernière barre affichait « 24 », qui ne comptait en réalité que le seul mercredi 2 septembre, pas les jours déjà écoulés (lundi 31 août, mardi 1er septembre) de la vraie semaine en cours. Recalculé à partir des lectures quotidiennes (déduites par différence de la série cumulative déjà en mémoire, **aucun appel API supplémentaire**) puis regroupé par semaine ISO réelle : **la semaine en cours passe de 24 à 76 lectures** (31 août-2 septembre, 3 des 7 jours). Premier ET dernier bucket désormais tous deux marqués partiels (`is-partial`) — le premier avec le libellé « **(lancement)** » plutôt que « (en cours) », puisque son incomplétude vient de l'absence de données avant le 29 juillet. `docs/routine-audience-prompt.md` mis à jour avec l'algorithme exact (dérivation quotidienne + regroupement ISO).
- **2026-09-03 [FAIT] — tableau « Autonomie par registre »** : sujets non cochés de `sujets-prioritaires.md` par section, semaines d'autonomie déduites (1 registre consommé/semaine). Retour utilisateur : « avons des pb sur certains domaines manque de sujet ? », après quoi le tableau ad hoc partagé en réponse a été jugé assez utile pour vivre dans le dashboard. Seuils fixes déterministes : **dégradé ≤ 4 non cochés, stable 5-10, favorable 11+**, couleurs `var(--degrade/stable/favorable)` déjà utilisées ailleurs. **Repéré ce jour-là : mardi (carte blanche) à 1 sujet, géopolitique à 3 ; les deux renfloués le jour même** (13 nouveaux sujets géopolitique après tri critique d'un lot de 21 idées, voir le journal de `sujets-prioritaires.md`). `docs/routine-audience-prompt.md` étendu : relit `sujets-prioritaires.md` déjà chargé pour l'agenda, aucune donnée supplémentaire à aller chercher.

---

## B149 — KPI de niveaux 2-3 du dashboard (abonnés newsletter, réseaux sociaux, dons)

**Statut:** À FAIRE
**Priorité:** P2 (suite de B148)
**Dernière MAJ:** 2026-09-03
**Prochaine action:** Aucune planifiée. Si le niveau 3 est retenu, commencer par 1-2 réseaux (Bluesky et Telegram ont les API les plus simples)
**Blocage:** Le KPI « abonnés newsletter » dépend du calendrier de la migration Buttondown → OneSignal (B004, en standby jusqu'en 2027) ; les KPI niveau 4 (calibration B092, score historique B142) sont bloqués par le volume de suivis clôturés

### État actuel
**Rien fait dans la V1** : la V1 ne contient que les KPI de niveau 1 (voir B148). Le classement par coût est inchangé depuis la pré-analyse du 2 septembre.

### À faire
- **Niveau 2** : nombre d'abonnés newsletter — **ne pas dupliquer le chantier B004**, juste piocher dedans une fois fait.
- **Niveau 3** : abonnés X/Bluesky/LinkedIn/Facebook/Instagram/Telegram (6 API et 6 authentifications différentes) ; montant/nombre de dons Buy Me a Coffee.
- **Niveau 4** : calibration et score historique, à relier comme briques du même dashboard le jour où le prérequis de volume est levé.

### Décisions
- **Ne pas viser les 6 réseaux d'un coup.**
- Chaque plateforme sociale a sa propre API/auth : **ce n'est pas une ligne de config par réseau**.

### Historique
- **2026-09-02** — Classement par coût posé dans la pré-analyse.
- **2026-09-03** — Confirmé inchangé : aucune intégration supplémentaire ajoutée dans les passages du 2-3 septembre.

---

## B150 — Lectures par édition sur `archives.html` (`reads.json` via GitHub Action)

**Statut:** FAIT
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-09-03
**Prochaine action:** Aucune. **Cette routine hebdomadaire ne doit plus jamais toucher `reads.json`** — seul le dashboard reste de son ressort
**Blocage:** Aucun

### État actuel
Sorti entièrement du périmètre Claude Code vers un GitHub Action dédié : `.github/workflows/reads.yml` (cron **horaire** + `workflow_dispatch` pour test manuel) + `scripts/seo/update_reads_json.py`, token `GOATCOUNTER_TOKEN` en **secret GitHub Actions** (jamais dans ce dépôt public). Régénère `assets/data/reads.json`, consommé côté client par `archives.html` (`scripts/seo/generate_archives_table.py`) : colonne « Lectures » + barre horizontale (largeur relative au max de lectures de la page, **plancher 4 %** pour rester visible) + **badge 🔥** sur l'édition la plus lue. `docs/routine-audience-prompt.md` (étape 3ter) modifié en conséquence.

### À faire
- Rien.

### Décisions
- **Motif du passage en GitHub Action** : tâche purement mécanique (appel API GoatCounter + agrégation par édition, **aucun jugement éditorial**), et la cadence hebdomadaire de la routine Claude Code ne convenait pas — retours utilisateur : « ça se met pas à jour tous les jours ? » et « tu peux pas faire une fonction dynamique ? ».

### Historique
- **2026-09-03 (demande)** — « met le nombre de lecture sur la page archive ». D'abord livré **dans** cette routine, **puis retiré le même jour** au profit du GitHub Action.
- **2026-09-03 (tests réels le jour même)** — **1er run échoué** (bug `git pull --rebase` avec index sale, ordre commit/pull inversé) ; **2e run réussi** (36 éditions, 451 lectures cumulées, poussé sur `main` par `scenario-reads-bot`).

---

## B151 — Migrer le reste du dashboard et le graphique `#audience` vers un GitHub Action

**Statut:** À DÉCIDER
**Priorité:** Non chiffrée
**Dernière MAJ:** 2026-09-03
**Prochaine action:** Valider le plan avec l'utilisateur ; suggestion de découpage : commencer par KPI + top/flop + « Lectures par domaine », qui réutilisent déjà `reads.json` sans rien inventer, avant de s'attaquer aux graphiques SVG
**Blocage:** **Plan proposé le 3 septembre, pas encore implémenté, pas encore validé avec l'utilisateur**

### État actuel
La routine « Scénario — Audience » reste hebdomadaire et coûte une session Claude Code à chaque passage, pour un travail lui aussi largement mécanique. Suite logique du chantier `reads.json` (B150) ; retour utilisateur : « il faudra connecter à notre dashboard pour t'éviter de mettre à jour ? »

### À faire
- **Ce qui migrerait sans trop de difficulté** (arithmétique/agrégation pure, comme `reads.json`) : les 5 cartes KPI (lectures cumulées, 7 j/30 j glissants + deltas, cadence de publication, moyenne par édition) ; le tableau top/flop (trivial une fois `reads.json` disponible — plus besoin de rappeler GoatCounter) ; « Lectures par domaine » (jointure `data-domain` d'`archives.html` + `reads.json`, déjà les deux sur disque) ; « Suivis actifs » (lecture de `docs/sujets-a-suivre.md`, extraction de texte déterministe) ; « Agenda de la semaine »/« Semaine d'après » (premier et second `- [ ]` non coché par registre dans `sujets-prioritaires.md`, **avec une règle de troncature de titre à fixer** pour les cartes).
- **Ce qui demande plus de soin** : les deux graphiques SVG (`#weekly-svg` barres, `#cumul-svg` courbe, plus la même série pour `#audience` sur `le-projet.html`) — actuellement **écrits à la main par une session Claude Code à chaque passage, donc jamais formalisés en code générique** ; un script Python devrait reproduire fidèlement le bucketing ISO lundi→dimanche, les barres partielles (`is-partial`, premier ET dernier bucket), le choix des `xLabels`/`yMax`, et surtout **ne jamais toucher au fix bfcache déjà en place** (écouteur `pageshow` + vidage des conteneurs avant re-rendu, voir B148) — celui-là reste dans le HTML/JS statique, pas dans les données régénérées.

### Décisions
- **Non tranché** : cadence du nouveau Action (`reads.json` tourne toutes les heures, mais `#audience` est **public** sur `le-projet.html` — peut-être pas besoin d'une fraîcheur horaire côté vitrine, à voir avec l'utilisateur) ; migration en un seul chantier ou par étapes.
- **Hors sujet, aucune raison d'y toucher** : le code d'accès du dashboard (hash SHA-256) et sa logique de porte.

### Historique
- **2026-09-03** — Plan proposé, non validé.

## B152 — Répartition des modèles OpenRouter par tâche (Opus / Sonnet / DeepSeek)

**Statut:** FAIT
**Priorité:** —
**Dernière MAJ:** 2026-09-18
**Prochaine action:** Surveiller le coût OpenRouter et la qualité des sorties dans les prochains jours
**Blocage:** Aucun

### État actuel
Trois scripts OpenRouter ont changé de modèle par défaut le 18 septembre 2026 :
- `generate_fallback_brief.py` (recherche quotidienne — tourne tous les jours tant que le trigger CCR reste désactivé, voir B004/routine-prompt.md) : passé de Sonnet 5 à **Opus** (`anthropic/claude-opus-5`) — c'est l'étape la plus proche d'un vrai jugement éditorial (choix du sujet, sources, anti-doublon) du pipeline, et elle tourne quotidiennement.
- `generate_hot_topics.py` (candidats « sujets chauds » ajoutés à `sujets-prioritaires.md`, jamais publiés directement, toujours filtrés par une relecture humaine) : passé à **DeepSeek** (`deepseek/deepseek-v4-flash`), pour financer une partie du surcoût d'Opus.
- `generate_suivi_update.py` (mise à jour **publiée** des pages de suivi) : brièvement passé à DeepSeek le même jour, puis **revenu à Sonnet 5** — ce script réestime réellement les 3 scénarios et écrit le texte publié, pas un simple tri (voir Historique).

Doc de référence complète (les 11 workflows GitHub Actions, leur fréquence, leur modèle, les incidents réels déjà rencontrés par modèle) : `docs/modeles-openrouter.md`.

### À faire
- Surveiller le coût OpenRouter (dashboard `#audience`) et la qualité des briefs Opus / des mises à jour de suivi Sonnet dans les prochains jours.
- Le dashboard de coût OpenRouter reste global au compte, sans ventilation par modèle/workflow — impossible de mesurer objectivement l'effet réel de cette bascule sans y ajouter un suivi par script (piste notée dans le doc lié ci-dessus).
- Réévaluer si le trigger CCR de recherche est un jour réactivé (le repli Opus tournerait alors beaucoup moins souvent, changeant le calcul de coût).

### Décisions
- Critère retenu pour choisir un modèle par script : le volume de jugement éditorial et de rédaction **réellement publiée**, pas la fréquence seule — un script qui écrit du contenu publié (suivi) reste sur un modèle robuste même si son volume est plus faible qu'un script de simple repérage de candidats (hot-topics).
- `call_openrouter()` (dans `generate_daily_edition.py`, partagé par plusieurs scripts) désactive désormais le raisonnement pour `anthropic/*` **et** `deepseek/*` (avant : `anthropic/*` seul) — nécessaire pour que `generate_hot_topics.py` tourne correctement sur DeepSeek sans reproduire le bug « contenu vide » déjà vu avec un modèle à raisonnement obligatoire.

### Historique
- **2026-09-18** — Doc préparé recensant les 11 workflows GitHub Actions, leur fréquence, leur modèle par défaut et les incidents réels déjà rencontrés par modèle (Sonnet qui bloque 16 min sans le flag reasoning-off — voir B002 ; GPT-5 qui renvoie un contenu vide si son raisonnement obligatoire mange tout le `max_tokens` — voir l'historique du récap hebdo ; DeepSeek qui tronque sur du texte long, cause du passage de la traduction EN sur Sonnet 5).
- **2026-09-18** — Première proposition : basculer recherche + détection + hot-topics sur Opus. Retour utilisateur : augmente le coût total sans rien compenser.
- **2026-09-18** — Proposition corrigée, pensée cost-neutre : Opus sur la recherche seule, financé par DeepSeek sur `detection.yml` et `hot-topics.yml`. Implémentée (import `DEFAULT_MODEL` remplacé par une constante dédiée dans chacun des 3 scripts).
- **2026-09-18** — Erreur repérée par l'utilisateur (« Détection il ne génère pas l'édition de mise à jour ? ») : `generate_suivi_update.py` ne fait pas du tri, il réestime les scénarios et écrit la mise à jour réellement publiée — downgrade DeepSeek inadapté, revenu à Sonnet 5. Seul `generate_hot_topics.py` reste sur DeepSeek pour financer partiellement Opus — l'équilibre coût n'est donc plus strictement neutre, mais le choix de modèle correspond maintenant à ce que chaque script fait réellement.
- **2026-09-18** — Question posée : GPT-5 plutôt que DeepSeek sur `hot-topics.yml` ? Écarté : GPT-5 coûte plus cher (raisonnement obligatoire non désactivable, `max_tokens` à relever comme sur le hebdo) pour un enjeu qualité faible ici (candidats non publiés, filtrés par l'utilisateur) — aurait mangé l'économie qui finance Opus. DeepSeek confirmé sur ce script.
- **2026-09-18** — Doc de référence rapatrié depuis l'Artifact claude.ai vers un vrai fichier versionné, `docs/modeles-openrouter.md` (retour utilisateur : nom "Artifact" ne veut rien dire) — mis à jour pour refléter l'état final (Opus recherche / Sonnet détection / DeepSeek hot-topics et pub).
