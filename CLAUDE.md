# Scénario — instructions de travail

Site lesscenarios.fr : une édition par jour, un podcast quotidien (flux `podcast.xml`, diffusé sur Spotify).

## Façon de répondre au propriétaire
- Vouvoiement, ton naturel et pédagogique, sans familiarité ni gros mots, pas de style « IA ».
- Ne jamais nommer le sujet de l'édition du 2 octobre.

## Choix des modèles d'IA : décision objective
- Claude est développé par Anthropic : pour écarter tout conflit d'intérêt, aucun modèle Claude n'est proposé en premier par défaut, ni favorisé à qualité égale.
- Tout choix ou changement de modèle (texte, voix, recherche) repose sur des critères vérifiables, présentés dans cet ordre :
  1. le prix réel, calculé à partir des journaux OpenRouter (pas de tarif recopié de mémoire) ;
  2. la qualité mesurée sur la tâche réelle (même texte, mêmes contrôles du code), pas sur une réputation ;
  3. la fiabilité (taux d'échec, nombre de reprises, quota, stabilité du fournisseur).
- Comparer au moins trois modèles de fournisseurs différents, et indiquer ce qui n'a pas été testé.
- Rappeler l'origine d'un modèle (fournisseur) quand c'est utile, et signaler toute incertitude sur un chiffre.

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

## Modèles (OpenRouter)
- Modèle par défaut de toute tâche automatisée nouvelle : **DeepSeek** (`deepseek/deepseek-v4-flash`) ou **Gemini** (`google/gemini-3.7-flash`). Jamais Claude (Sonnet ou autre) par défaut : seulement si le propriétaire le demande explicitement.
- Changer le modèle d'une tâche est une décision du propriétaire : proposer, ne pas décider. Chaque modèle et sa raison sont notés dans `docs/modeles-openrouter.md`.
- Jamais Claude Sonnet : aucune tâche automatique n'en utilise par défaut (état vérifié dans le code le 10 novembre 2026, tableau dans `docs/modeles-openrouter.md`). Ne jamais en remettre, ni dans un script, ni dans un workflow, ni dans la variable de dépôt `OPENROUTER_MODEL`.
- Vérification des résultats de `a-venir.json` : recherche sur DeepSeek, confirmation sur Gemini (voir `docs/a-venir.md`).

## SEO
- Toute demande autour du référencement (titres, balises, Google, citation par les IA, trafic, indexation) : lire d'abord `.claude/seo-routage.md`. Il indique quel module (`.claude/skills/`) ou quel agent (`.claude/agents/`) appeler, dans quel ordre, et où corriger.
- Les agents SEO peuvent être lancés sans redemander pour une demande SEO (autorisation durable du propriétaire). Mesurer d'abord (SEOmatic, gratuit) ; Semrush est payant : ne pas l'utiliser sans demande.
- Search Console : `data/gsc/rapport.md` (mis à jour chaque jour, aussi en page privée `seo.html` et carte du tableau de bord) liste les problèmes avec l'agent à envoyer et sa mission. Problème critique ou important : envoyer ces agents sans redemander (`gsc-expert` d'abord pour les données et la connexion), corriger dans le périmètre, rendre compte. Procédure complète : `.claude/seo-routage.md`.
