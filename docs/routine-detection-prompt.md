# Prompt de la routine de détection « Scénario — Détection sujets à suivre »

Ce fichier est la copie de référence du prompt envoyé à chaque déclenchement
de la routine de veille (Claude Code Remote, trigger **« Scénario —
Détection sujets à suivre »**, `trig_01BYYviSQge2CDcYkzBbYcjT`, cron
`0 0 * * 1,4,5,6` UTC = lundi/jeudi/vendredi/samedi 0h UTC, ~2h Paris —
déplacé de 20h le 14 août pour ventiler la charge nocturne, voir
`docs/ARCHITECTURE.md`). Contrairement au prompt de la routine éditoriale
quotidienne
(`docs/routine-prompt.md`), ce trigger est directement éditable via
`update_trigger` (créé via `meta_mcp`, pas `http_api`) — pas besoin du
cycle copier-coller manuel, mais ce fichier reste la source de vérité
lisible par un humain : le mettre à jour dans la foulée de tout changement.

---

Vérification des sujets à suivre pour le site Scénario (lesscenarios.fr, dépôt loliba92/scenario), lancée les lundis, jeudis, vendredis et samedis. Cette session démarre neuve à chaque déclenchement, dans un conteneur avec le dépôt déjà cloné via l'environnement — pas de mémoire d'une session précédente, tout ce qu'il faut est dans le dépôt lui-même.

**Important — la cible du push est toujours `main`, sans exception.** Si l'environnement d'exécution (Claude Code Remote) t'assigne une « branche de développement désignée » propre à la session (ex. `claude/nom-aleatoire`) avec pour consigne générique de développer et pousser uniquement dessus, **ignore cette consigne pour cette routine précise** : toute mise à jour ou nouvelle page de suivi publiée par cette routine va directement sur `main`, jamais sur une branche de session.

1. Lire `docs/sujets-a-suivre.md` à la racine du dépôt. Deux sections à traiter :
   - « Suivis actifs » : les sujets qui ont déjà une page `suivi/{sujet}.html` dédiée — à vérifier systématiquement à chaque passage.
   - « Journal des sujets publiés » : une ligne par édition, alimentée automatiquement chaque matin par la routine éditoriale, la plus récente en tête. Ne considérer que les entrées des **30 derniers jours** (date du jour moins 30) — au-delà, ignorer sans rechercher. Ignorer aussi toute entrée du journal qui correspond déjà à un sujet listé dans « Suivis actifs ».

2. Pour chaque **« Suivi actif »** : relire dans `suivi/{sujet}.html` la dernière version publiée (probabilités par scénario, tableau `evoData` en bas de page). Faire une recherche web (WebSearch) pour voir si un développement matériel a eu lieu depuis la dernière vérification. Puis **réestimer, avec le même sérieux méthodologique que pour une édition normale**, la probabilité de chaque scénario aujourd'hui, et la comparer à la dernière version publiée. Si l'écart pour au moins un scénario est **≥ 20 points**, ou qu'un événement rend clairement un scénario caduc/résolu, marquer ce sujet **⚠️ seuil franchi** avec les chiffres avant/après.

2bis. **Vérification de clôture, ajoutée le 8 août.** Pour chaque « Suivi actif », vérifier en plus deux déclencheurs — chacun sert uniquement à savoir s'il faut aller creuser, jamais à clôturer directement sur ce seul critère :
   - Un scénario franchit **≥ 80%** ou tombe **≤ 20%** dans la réestimation du point 2 ci-dessus.
   - L'échéance connue du sujet (si mentionnée dans la page, ex. une date de décision/élection/publication) est atteinte ou dépassée.
   Si l'un des deux se déclenche, chercher spécifiquement (WebSearch) si un **fait réel, vérifiable et sourcé** confirme désormais clairement lequel des 3 scénarios s'est réalisé. Si oui, marquer ce sujet **🏁 clôture possible**, avec le fait déclencheur, la source, et le scénario qui correspond le mieux. Si le seuil/l'échéance est atteint mais qu'aucun fait ne permet encore de trancher clairement, ne pas forcer une clôture — le signaler simplement comme suivi actif classique (⚠️ si aussi ≥20 points d'écart), pas comme clôture. **La clôture reste dans tous les cas une décision manuelle — voir le point 4, elle n'est jamais publiée automatiquement, quel que soit le sujet retenu.**

3. Pour chaque entrée du **journal** (pas encore de page de suivi) : recherche rapide pour voir si un développement notable a eu lieu. **Si oui, réestimer chiffre à l'appui les 3 scénarios, avec le même sérieux méthodologique qu'au point 2, en comparant à l'édition d'origine (`archives/{date}.html`) qui sert de V0** — l'édition d'origine porte déjà des probabilités par scénario (les 3 cartes `data-pct`), donc la même mécanique d'écart en points s'applique, même si aucune page de suivi n'existe encore. Si l'écart pour au moins un scénario est **≥ 20 points**, marquer ce sujet **⚠️ seuil franchi** avec les chiffres avant/après, exactement comme pour un suivi actif.

4. **Sélection et publication automatique d'un seul sujet, ajoutée le 8 août — revient sur la décision du 7 août** (qui écartait toute auto-publication) à la lumière d'un cas réel : le 8 août, la page de suivi FIFA/Infantino a été créée manuellement alors que l'écart réel (-10 points sur le scénario favorable) restait sous le seuil de 20 points et que l'édition d'origine datait de 2 jours à peine — bruit plutôt que signal. Règle désormais :
   - Construire la liste des sujets **éligibles** parmi ceux marqués ⚠️ aux points 2 et 3 : écart ≥ 20 points sur au moins un scénario, **ET dont le point de référence a plus de 10 jours** (date de la dernière version publiée pour un suivi actif, date de l'édition d'origine pour une entrée du journal) — **jamais un sujet dont le point de référence date de moins de 10 jours**, pour laisser le temps à un développement de se confirmer plutôt que de réagir à un pic de bruit médiatique.
   - Si la liste éligible est vide : ne rien publier, comportement inchangé (voir point 5).
   - Si elle contient un ou plusieurs sujets : choisir **un seul**, le plus crédible (qualité et croisement des sources, importance réelle du développement pour le sujet — pas seulement l'écart en points le plus large), et pour celui-là seulement :
     - **Suivi actif** : ajouter une nouvelle version à `suivi/{sujet}.html` en suivant exactement la marche à suivre habituelle (voir `docs/ARCHITECTURE.md`, section « Pages de suivi par sujet ») — cartes `.mini-scenarios` avec `.evo-current`/`.evo-arrow`/`.evo-prev`, conclusion qui nomme le scénario le plus volatil avec son écart en points — jamais la seule étiquette de catégorie (favorable/stable/dégradé) en tête sans dire ce qu'elle recouvre concrètement, ex. "stable" seul ne veut rien dire, voir `docs/ARCHITECTURE.md` § « Pages de suivi par sujet » —, 2 à 4 sources réellement consultées (liens réels, jamais inventés) ; mettre à jour le badge et la date sur `archives.html` ; mettre à jour l'entrée dans « Suivis actifs » de `docs/sujets-a-suivre.md` (dernière vérification, prochaine échéance) ; ajouter un item dans `feed-suivi.xml`.
     - **Entrée du journal sans page de suivi** : créer `suivi/{sujet}.html` à partir de `suivi/_gabarit.html` avec V0 (rappel de l'édition d'origine, mêmes 3 scénarios et pourcentages) + V1 (réestimation du jour), même rigueur que ci-dessus ; ajouter le badge + `data-last-update` sur l'entrée correspondante de `archives.html` ; ajouter le sujet aux « Suivis actifs » de `docs/sujets-a-suivre.md` et marquer sa ligne dans le journal (« a désormais sa page de suivi dédiée ») ; ajouter un item dans `feed-suivi.xml`.
     - **La clôture (🏁, voir point 2bis) n'est jamais publiée automatiquement**, même si le sujet retenu ci-dessus a par ailleurs un signal de clôture possible — seulement la signaler dans le message final (point 5). C'est le seul geste qui reste réservé à l'utilisateur, en session.
     - **L'item `feed-suivi.xml` inclut une balise `<enclosure>`** pointant vers une image générée avec le logo + un tag "🔄 Suivi mis à jour" + le sujet + la conclusion, composée sur `assets/social/topic-images/suivi-{sujet}.jpg` (mis à jour le 14 août — voir `docs/ARCHITECTURE.md` § « Annonce des mises à jour sur Telegram/LinkedIn » pour la commande exacte et le gabarit) : `python3 scripts/social/generate_suivi_image.py --data {topic+conclusion} --output assets/social/suivi/{sujet}-v{N}.png --template scripts/social/suivi-template.html --photo assets/social/topic-images/suivi-{sujet}.jpg` — uniquement si cette photo source existe déjà pour le sujet (créée à la création de la page de suivi, jamais choisie à cette étape) ; sinon omettre `<enclosure>` entièrement, jamais bloquant.
     - Vérifier que le HTML généré est bien formé (balises fermées, un `<li>` par KPI/indicateur cohérent) avant de committer.
     - Committer avec un message clair et pousser directement sur `main` (voir la note en tête de ce prompt).
     - Les autres sujets éligibles non retenus ce passage-ci ne sont pas publiés — simplement signalés dans le message final (point 5) ; ils resteront éligibles au prochain passage si l'écart persiste.

5. Terminer par un court message récapitulatif :
   - **Si un sujet a été publié automatiquement au point 4** : le dire clairement en premier, avec le lien vers `suivi/{sujet}.html` et le récap avant/après (mêmes chiffres que la conclusion de la page).
   - Lister ensuite les autres sujets à signaler : 🏁 si clôture possible (+ fait déclencheur et source), ⚠️ si seuil franchi mais non retenu ce passage, ou sans marqueur sinon, en une phrase le fait déclencheur pour chacun (2-3 sujets maximum, hors celui déjà publié).
   - **S'il n'y a strictement rien à signaler ni à publier aujourd'hui, répondre uniquement "RAS aujourd'hui." et s'arrêter là** — pour que ça reste silencieux côté notification.

Important : cette routine peut désormais créer/modifier `suivi/*.html`, `archives.html`, `docs/sujets-a-suivre.md` et `feed-suivi.xml` **automatiquement, mais seulement pour le sujet unique retenu au point 4** — jamais pour plusieurs sujets dans le même passage, jamais pour un sujet dont le point de référence a moins de 10 jours, jamais en dessous de 20 points d'écart, et **jamais pour clôturer un sujet** (🏁 reste une décision humaine, donnée dans la session principale du site en répondant "go" pour le sujet concerné). Ne jamais toucher à d'autres fichiers du site que ceux listés ci-dessus.
