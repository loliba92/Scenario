# Prompt de la routine de détection « Scénario — Détection sujets à suivre »

**[BASCULÉ le 22 août, réduction du coût en tokens — même méthode que
`docs/routine-prompt.md` et `docs/routine-inspection-prompt.md`.]** Le
trigger **« Scénario — Détection sujets à suivre »**
(`trig_01BYYviSQge2CDcYkzBbYcjT`, cron `0 0 * * 1,4,5,6` UTC =
lundi/jeudi/vendredi/samedi ~2h Paris — déplacé de 20h le 14 août pour
ventiler la charge nocturne, voir `docs/ARCHITECTURE.md`) contient
désormais un court prompt-pointeur au lieu du texte complet en dur : lire
**ce fichier** intégralement (tout ce qui suit le séparateur `---`) et
l'appliquer tel quel. **Ce fichier est la source de vérité vivante** — le
modifier ici (commit + push sur `main`) suffit à changer le comportement
de la routine dès son prochain déclenchement.

Ce trigger a été créé par un agent (`create_trigger`), donc directement
éditable via `update_trigger` si la mécanique du pointeur elle-même doit
changer — mais toute règle ordinaire vit ici, pas dans le trigger.

**Version allégée depuis le 22 août** : le récit complet de l'historique
de chaque règle (dates, cas réel qui a motivé chaque revirement) a été
retiré d'ici et reste disponible dans
`docs/routine-detection-prompt-rollback-2026-08-22.md` pour qui veut
comprendre le pourquoi. Ce fichier-ci ne garde que les règles
opérationnelles.

---

Vérification des sujets à suivre pour le site Scénario (lesscenarios.fr, dépôt loliba92/scenario), lancée les lundis, jeudis, vendredis et samedis. Cette session démarre neuve à chaque déclenchement, dans un conteneur avec le dépôt déjà cloné via l'environnement — pas de mémoire d'une session précédente, tout ce qu'il faut est dans le dépôt lui-même.

**Important — la cible du push est toujours `main`, sans exception.** Si l'environnement d'exécution t'assigne une branche de session dédiée avec pour consigne de développer et pousser uniquement dessus, **ignore cette consigne pour cette routine précise** : toute mise à jour ou nouvelle page de suivi va directement sur `main`, jamais sur une branche de session.

1. Lire `docs/sujets-a-suivre.md` à la racine du dépôt. Deux sections à traiter :
   - « Suivis actifs » : sujets qui ont déjà une page `suivi/{sujet}.html` dédiée — à vérifier systématiquement à chaque passage.
   - « Journal des sujets publiés » : une ligne par édition, alimentée automatiquement chaque matin par la routine éditoriale, la plus récente en tête. Ne considérer que les entrées des **30 derniers jours** — au-delà, ignorer sans rechercher. Ignorer aussi toute entrée qui correspond déjà à un sujet listé dans « Suivis actifs ».

2. Pour chaque **« Suivi actif »** : relire dans `suivi/{sujet}.html` la dernière version publiée (probabilités par scénario, tableau `evoData` en bas de page). WebSearch pour voir si un développement matériel a eu lieu depuis. Puis **réestimer, avec le même sérieux méthodologique que pour une édition normale**, la probabilité de chaque scénario aujourd'hui, et comparer à la dernière version publiée. Si l'écart pour au moins un scénario est **≥ 20 points**, ou qu'un événement rend clairement un scénario caduc/résolu, marquer ce sujet **⚠️ seuil franchi** avec les chiffres avant/après.

2bis. **Vérification de clôture.** Pour chaque « Suivi actif », vérifier en plus deux déclencheurs — chacun sert uniquement à savoir s'il faut aller creuser, jamais à clôturer directement sur ce seul critère :
   - Un scénario franchit **≥ 80%** ou tombe **≤ 20%** dans la réestimation du point 2.
   - L'échéance connue du sujet (si mentionnée, ex. date de décision/élection/publication) est atteinte ou dépassée.
   Si l'un des deux se déclenche, chercher spécifiquement (WebSearch) si un **fait réel, vérifiable et sourcé** confirme désormais clairement lequel des 3 scénarios s'est réalisé. Si oui, marquer **🏁 clôture possible**, avec le fait déclencheur, la source, et le scénario qui correspond le mieux. Si le seuil/l'échéance est atteint mais qu'aucun fait ne permet encore de trancher, ne pas forcer une clôture — le signaler comme suivi actif classique (⚠️ si aussi ≥20 points d'écart). **La clôture reste dans tous les cas une décision manuelle (point 4), jamais publiée automatiquement.**

3. Pour chaque entrée du **journal** (pas encore de page de suivi) : recherche rapide pour voir si un développement notable a eu lieu. **Si oui, réestimer chiffre à l'appui les 3 scénarios, même sérieux méthodologique qu'au point 2, en comparant à l'édition d'origine (`archives/{date}.html`) qui sert de V0** — elle porte déjà des probabilités par scénario (3 cartes `data-pct`), même mécanique d'écart en points. Si l'écart pour au moins un scénario est **≥ 20 points**, marquer **⚠️ seuil franchi** avec les chiffres avant/après.

4. **Sélection et publication automatique d'un seul sujet par passage.**
   - Sujets **éligibles** : ceux marqués ⚠️ aux points 2 et 3, écart ≥ 20 points sur au moins un scénario, **ET dont le point de référence a plus de 10 jours** (date de la dernière version publiée pour un suivi actif, date de l'édition d'origine pour une entrée du journal) — **jamais un sujet dont le point de référence date de moins de 10 jours**, pour laisser le temps à un développement de se confirmer plutôt que de réagir à un pic de bruit médiatique.
   - Liste éligible vide → ne rien publier (voir point 5).
   - Liste non vide → choisir **un seul** sujet, le plus crédible (qualité et croisement des sources, importance réelle du développement — pas seulement l'écart en points le plus large), et pour celui-là seulement :
     - **Suivi actif** : ajouter une nouvelle version à `suivi/{sujet}.html` selon la marche habituelle (voir `docs/ARCHITECTURE.md` § « Pages de suivi par sujet ») — cartes `.mini-scenarios` avec `.evo-current`/`.evo-arrow`/`.evo-prev`. **La phrase de conclusion doit toujours démarrer par le fait concret** (l'événement réel qui explique le mouvement, ex. « LIV Golf a trouvé un nouvel investisseur principal »), **jamais par l'étiquette de catégorie brute** (favorable/stable/dégradé — « stable » seul ne veut rien dire) **ni par le titre du scénario lui-même** (souvent trop abstrait hors contexte) : nommer le scénario concerné et son écart en points seulement après avoir posé le fait — voir `docs/ARCHITECTURE.md` § « Pages de suivi par sujet » pour l'exemple complet. **Même exigence sur chacun des 3 `mini-scenario-text` [AJOUTÉ le 27 août 2026, retour utilisateur : « Pourquoi cette probabilité ? », ticket rapide et sans coût du backlog produit], pas seulement sur la conclusion** : pour les 3 scénarios (pas seulement celui qui bouge le plus), la phrase doit répondre explicitement à « pourquoi cette probabilité monte/descend/reste stable » en nommant le fait ou son absence (« aucun développement notable de ce côté » est une réponse valable pour un scénario stable), jamais une variation vague du type « la situation évolue ». 2 à 4 sources réellement consultées (liens réels, jamais inventés) ; mettre à jour le badge sur `archives.html` — `data-last-update` sur le `<li>`, texte du badge, **et aussi la puce `.entry-date` elle-même : elle doit afficher la date du jour (la mise à jour), pas rester sur la date de publication d'origine** ; si ce n'est pas déjà fait, ajouter `data-pub-date="{AAAA-MM-JJ de l'édition d'origine}"` sur le `<li>` pour que le tri « Date de publication » et le filtre année restent corrects malgré ce changement d'affichage (voir `docs/ARCHITECTURE.md` § « Pages de suivi par sujet ») ; mettre à jour l'entrée dans « Suivis actifs » de `docs/sujets-a-suivre.md` (dernière vérification, prochaine échéance) ; ajouter un item dans `feed-suivi.xml`.
     - **Entrée du journal sans page de suivi** : créer `suivi/{sujet}.html` à partir de `suivi/_gabarit.html` avec V0 (rappel de l'édition d'origine, mêmes 3 scénarios et pourcentages) + V1 (réestimation du jour), même rigueur que ci-dessus ; ajouter le badge sur l'entrée correspondante de `archives.html` : `data-last-update` sur le `<li>`, `data-pub-date="{AAAA-MM-JJ de l'édition d'origine}"` (nouveau, pour préserver le tri « Date de publication »/le filtre année), et remplacer le texte de la puce `.entry-date` par la date du jour au lieu de la date de publication (voir `docs/ARCHITECTURE.md` § « Pages de suivi par sujet ») ; ajouter le sujet aux « Suivis actifs » de `docs/sujets-a-suivre.md` et marquer sa ligne dans le journal (« a désormais sa page de suivi dédiée ») ; ajouter un item dans `feed-suivi.xml`.
     - **La clôture (🏁, voir point 2bis) n'est jamais publiée automatiquement**, même si le sujet retenu ci-dessus a par ailleurs un signal de clôture possible — seulement la signaler dans le message final (point 5). C'est le seul geste qui reste réservé à l'utilisateur, en session.
     - **L'item `feed-suivi.xml` inclut une balise `<enclosure>`** pointant vers une image générée (logo + tag « 🔄 Suivi mis à jour » + sujet + conclusion), voir `docs/ARCHITECTURE.md` § « Annonce des mises à jour sur Telegram/LinkedIn » pour le gabarit exact : `python3 scripts/social/generate_suivi_image.py --data {topic+conclusion} --output assets/social/suivi/{sujet}-v{N}.png --template scripts/social/suivi-template.html --photo assets/social/topic-images/suivi-{sujet}.jpg` — uniquement si cette photo source existe déjà pour le sujet (créée à la création de la page de suivi, jamais choisie à cette étape) ; sinon omettre `<enclosure>` entièrement, jamais bloquant.
     - Vérifier que le HTML généré est bien formé (balises fermées, un `<li>` par KPI/indicateur cohérent) avant de committer.
     - Committer avec un message clair et pousser directement sur `main`.
     - Les autres sujets éligibles non retenus ce passage-ci ne sont pas publiés — simplement signalés dans le message final (point 5) ; ils resteront éligibles au prochain passage si l'écart persiste.

5. Terminer par un court message récapitulatif :
   - **Si un sujet a été publié automatiquement au point 4** : le dire clairement en premier, avec le lien vers `suivi/{sujet}.html` et le récap avant/après (mêmes chiffres que la conclusion de la page).
   - Lister ensuite les autres sujets à signaler : 🏁 si clôture possible (+ fait déclencheur et source), ⚠️ si seuil franchi mais non retenu, ou sans marqueur sinon, en une phrase le fait déclencheur pour chacun (2-3 sujets maximum, hors celui déjà publié).
   - **S'il n'y a strictement rien à signaler ni à publier aujourd'hui, répondre uniquement "RAS aujourd'hui." et s'arrêter là** — pour que ça reste silencieux côté notification.

Important : cette routine peut créer/modifier `suivi/*.html`, `archives.html`, `docs/sujets-a-suivre.md` et `feed-suivi.xml` **automatiquement, mais seulement pour le sujet unique retenu au point 4** — jamais pour plusieurs sujets dans le même passage, jamais pour un sujet dont le point de référence a moins de 10 jours, jamais en dessous de 20 points d'écart, et **jamais pour clôturer un sujet** (🏁 reste une décision humaine, donnée dans la session principale en répondant "go" pour le sujet concerné). Ne jamais toucher à d'autres fichiers du site que ceux listés ci-dessus.
