# Scénario — instructions de travail

Site lesscenarios.fr : une édition par jour, un podcast quotidien (flux `podcast.xml`, diffusé sur Spotify).

## Façon de répondre au propriétaire
- Vouvoiement, ton naturel et pédagogique, sans familiarité ni gros mots, pas de style « IA ».
- Ne jamais nommer le sujet de l'édition du 2 octobre.

## Éditions
- Les éditions passées sont figées : on ne change que l'édition du jour et les futures.
  Les pages vivantes (accueil, Éditions, matières, projet, contact…) peuvent évoluer.
- `index.html` sert de modèle aux futures pages ; `preview.html` aussi pour les éditions.
- Ne pas refaire ni republier un épisode du podcast sans demande explicite (Spotify relit le flux).
- Je fusionne mes propres PR (branche de travail désignée par la session).

## Interface (UI) : vigilance obligatoire
Toute modification visuelle se vérifie à l'écran avant de la livrer, pas seulement dans le code :
1. Prendre une capture sur **ordinateur (≈ 1100 px)** et sur **téléphone (≈ 390 px)** (Playwright + Chromium installé).
2. Aucun mot coupé, aucun débordement horizontal, aucune tuile isolée sur une ligne.
3. Sur ordinateur, privilégier des ensembles compacts : les matières tiennent sur **une seule ligne**, la date et la matière sur la même ligne dans les cartes.
4. Cohérence : mêmes libellés, mêmes couleurs (doré pour les libellés de section), mêmes espacements d'une page à l'autre.
5. Une ancre ou un lien interne doit arriver au **début** de sa section (l'en-tête collant ne doit rien masquer).
6. Pas de doublons d'accès (ex. deux liens vers la même page dans un même bloc) ; une icône seule ne suffit pas si son sens n'est pas évident : ajouter un libellé.
7. Vérifier le résultat sur la page réelle générée (accueil, Éditions, édition du jour), puis relire le rendu avant de dire que c'est fait.

## Podcast
- Texte lu à l'oreille : phrases courtes, une idée par phrase, pas de sigles épelés, reformulation « En clair », devise finale « Rien n'est écrit à l'avance ».
- Longueur du texte : 420 à 1000 mots (« mieux vaut plus que moins »).
- Un épisode manquant le matin : lire le journal du workflow `podcast-quotidien.yml`, corriger la cause, relancer pour la date du jour.
