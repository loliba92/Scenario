# Banque de messages — routine "pub" hebdomadaire

Liste fermée et curée à la main, dans le même esprit que `docs/tags.md` ou
`sujets-prioritaires.md` : la routine hebdomadaire (`docs/routine-pub-
prompt.md`) **pioche dans cette liste en rotation, elle n'invente jamais un
message ni une citation elle-même** — voir la justification dans
`docs/ARCHITECTURE.md` (risque de citation mal attribuée ou inventée par un
LLM, déjà identifié pendant la conception de cette routine).

**Statut : brouillon, pas encore validé pour publication.** Points à
trancher avant de mettre cette liste en service :
1. Les lignes marquées `[à confirmer]` dans la section Manifeste font une
   affirmation sur le modèle économique (pas de sponsor, etc.) que je ne
   peux pas vérifier moi-même — à valider ou reformuler avant usage.
2. Les citations marquées `[attribution à vérifier]` dans la section
   Citations ont une attribution courante mais pas 100 % certaine — à
   vérifier une source primaire avant publication, ou à retirer.
3. **Toutes les entrées de la section 4 (Le saviez-vous) sont marquées
   `[chiffre à vérifier]`** — ordres de grandeur retenus de mémoire, pas
   revérifiés sur la source primaire au moment de la rédaction. Vu que
   toute la crédibilité du site repose sur la justesse des chiffres,
   **aucune ne doit passer en rotation sans une vérification par une
   vraie source (WebFetch ou lecture manuelle) au moins une fois** —
   après quoi le chiffre est figé (même règle que pour une citation :
   on ne le revérifie pas à chaque utilisation, juste avant sa première
   mise en rotation).

## Dénominateur commun (règle du 13 août)

Quelle que soit la catégorie, chaque entrée doit être **engageante,
positive dans le ton, et orientée croissance** (gagner des
abonnés/auditeurs) — pas seulement un rappel d'identité passif. Concrètement :
- **Toujours un CTA qui pousse à agir**, pas juste "lesscenarios.fr" en
  signature : s'abonner, commenter, réagir. Un chiffre ou une citation qui
  se termine sans inviter de réaction rate la moitié de l'objectif.
- **Le ton reste positif/curieux même sur un sujet sérieux** (retraites,
  climat...) — jamais alarmiste. La question qui suit un chiffre doit
  donner envie de répondre, pas juste constater un problème.
- Ça ne change rien à la rigueur déjà en place (jamais de fait inventé,
  toujours au conditionnel pour les "grands futurs", etc.) — seulement la
  façon dont chaque message se termine et invite à réagir.

**2 citations existantes repérées comme moins alignées avec "positif"**
(`citation-05`, Voltaire — ton plutôt désabusé ; `citation-06`, Héraclite —
mélancolique) : gardées pour l'instant, CTA ajouté pour les rendre plus
engageantes, mais à toi de dire si tu préfères les retirer/remplacer par
des citations plus toniques.

## Format d'une entrée

```
### {id unique, court, jamais réutilisé même si l'entrée est retirée}
- eyebrow: {texte affiché en haut de l'image, MAJUSCULES}
- message: {texte principal, \n autorisé pour forcer un saut de ligne, **mot** pour surligner en doré}
- attribution: {optionnel, citations : "— Auteur" / chiffres : "— Source, année"}
- cta: {optionnel, ligne d'appel à l'action sous le message}
```

## 1. Manifeste — pourquoi Scénario (rotation A)

Objectif : rappeler ce qui différencie le projet et convertir en abonné —
pas juste de la rétention passive (voir "Dénominateur commun" ci-dessus) —
jamais un ton commercial pour autant, la même sobriété que le reste du
site.

### manifeste-01
- eyebrow: POURQUOI SCÉNARIO
- message: Gratuit. Indépendant.\nNi de gauche ni de droite.
- cta: 👉 Abonne-toi, c'est gratuit

*Reprend mot pour mot la ligne éditoriale de `le-projet.html` : "ne défend
aucune ligne, ni de gauche ni de droite, aucun parti pris."*

### manifeste-02
- eyebrow: POURQUOI SCÉNARIO
- message: On ne prédit pas l'avenir.\nOn chiffre l'incertitude.
- cta: 👉 Abonne-toi, c'est gratuit

*Reprend l'idée de `le-projet.html` : "des métiers où l'on chiffre
l'incertitude plutôt que de deviner un seul avenir."*

### manifeste-03
- eyebrow: POURQUOI SCÉNARIO
- message: Une probabilité n'est jamais gravée dans le marbre.\nQuand les faits changent, elle change.
- cta: 👉 Abonne-toi, suis chaque mise à jour

*Reprend `le-projet.html` : "Un pourcentage donné dans une édition n'est
pas une vérité gravée dans le marbre [...]. Quand la situation évolue,
l'estimation doit évoluer avec elle."*

### manifeste-04
- eyebrow: POURQUOI SCÉNARIO
- message: Pas de tirage au hasard.\nUne méthode, appliquée à chaque édition.
- cta: 👉 Abonne-toi, c'est gratuit

*Reprend `le-projet.html` : "chaque estimation s'appuie sur une méthode
propriétaire, appliquée systématiquement à chaque édition."*

### manifeste-05 `[à confirmer]`
- eyebrow: POURQUOI SCÉNARIO
- message: Aucune pub. Aucun sponsor.\nJuste trois scénarios chiffrés.
- cta: 👉 Abonne-toi, c'est gratuit

*Affirmation sur le modèle économique — à confirmer avant usage (aucune
mention équivalente déjà publiée ailleurs sur le site à recopier).*

### manifeste-06 `[à confirmer]`
- eyebrow: POURQUOI SCÉNARIO
- message: Gratuit, sans compte à créer.\nLe lien en bio suffit.
- cta: 👉 Abonne-toi, c'est gratuit

*"Sans compte à créer" — à confirmer que c'est bien exact (pas de zone
membre sur le site à ma connaissance, mais à vérifier avant publication).*

## 2. Citations — le hasard et l'incertitude (rotation B)

Objectif : varier le feed avec du contenu plus léger/partageable, en lien
thématique avec le projet, sans ton commercial — mais toujours avec un CTA
qui invite à s'abonner ou réagir (voir "Dénominateur commun" ci-dessus).

### citation-01
- eyebrow: UNE CITATION
- message: « Le hasard ne favorise que les esprits préparés. »
- attribution: — Louis Pasteur
- cta: 👉 Abonne-toi, prépare-toi chaque jour

*Source solide : formule d'une conférence de Pasteur à l'université de
Lille, 1854, très largement documentée.*

### citation-02
- eyebrow: UNE CITATION
- message: « Il y a des choses qui dépendent de nous,\net d'autres qui n'en dépendent pas. »
- attribution: — Épictète
- cta: 👉 Abonne-toi, concentre-toi sur ce qui compte

*Source solide : ouverture du Manuel d'Épictète.*

### citation-03
- eyebrow: UNE CITATION
- message: « La théorie des probabilités n'est, au fond,\nque le bon sens réduit au calcul. »
- attribution: — Pierre-Simon de Laplace
- cta: 👉 Abonne-toi, c'est gratuit

*Source solide : Essai philosophique sur les probabilités, 1814.*

### citation-04 `[attribution à vérifier]`
- eyebrow: UNE CITATION
- message: « Le hasard, c'est peut-être le pseudonyme\nde Dieu quand il ne veut pas signer. »
- attribution: — Anatole France
- cta: 👉 Abonne-toi, c'est gratuit

*Attribution courante (Le Jardin d'Épicure, 1894) mais à vérifier sur une
édition de référence avant publication — formule très reprise, parfois de
façon approximative.*

### citation-05 `[attribution à vérifier]`
- eyebrow: UNE CITATION
- message: « Le doute n'est pas une condition agréable,\nmais la certitude est absurde. »
- attribution: — Voltaire
- cta: 👉 Abonne-toi, on t'aide à y voir clair

*Attribution très répandue mais disputée par certains chercheurs (parfois
présentée comme une paraphrase plutôt qu'une citation exacte d'un texte
identifié) — à vérifier ou à retirer avant publication. Ton plutôt
désabusé — moins "positif" au sens de la règle du 13 août, gardée pour
l'instant, CTA ajouté pour compenser.*

### citation-06
- eyebrow: UNE CITATION
- message: « On ne se baigne jamais deux fois\ndans le même fleuve. »
- attribution: — Héraclite
- cta: 👉 Abonne-toi, suis ce qui change

*Fragment antique, formulation reconstituée (normal pour un fragment
présocratique transmis indirectement) — thème de l'impermanence/incertitude,
pas du hasard au sens strict, mais reste pertinent pour la ligne éditoriale.
Ton plutôt mélancolique — moins "positif" au sens de la règle du 13 août,
gardée pour l'instant, CTA ajouté pour compenser.*

## 3. Questions à la communauté (rotation C)

Objectif : faire réagir, pas informer — engagement direct, notamment pour
alimenter le mardi "carte blanche" (sujet libre suggéré par les lecteurs).
Jamais de chiffre ni de citation ici, juste une question ouverte.

### question-01
- eyebrow: À VOUS DE JOUER
- message: Quel sujet libre voudrais-tu voir décrypté\nen 3 scénarios mardi prochain ?
- cta: 👉 Dis-le en commentaire

*Sollicite directement des idées pour le registre "carte blanche" du
mardi — voir `docs/routine-prompt.md`, Étape 1.*

### question-02
- eyebrow: À VOUS DE JOUER
- message: Une question qui te trotte dans la tête\net dont tu voudrais 3 scénarios chiffrés ?
- cta: 👉 On lit tous les commentaires

*Variante plus ouverte de question-01, pas limitée au mardi.*

### question-03
- eyebrow: À VOUS DE JOUER
- message: Parmi les 3 scénarios de la semaine,\nlequel t'a le plus surpris ?
- cta: 👉 Dis-nous lequel

*Réagit sur du contenu déjà publié plutôt que de solliciter une nouvelle
idée — variante utile pour ne pas répéter le même type de question à
chaque publication.*

## 4. Le saviez-vous — chiffres et projection à 10 ans (rotation D)

Objectif : un chiffre simple et concret, toujours prolongé par une
question ouverte sur ce que ça implique dans 10 ans — jamais un chiffre
seul sans mise en perspective.

### chiffre-01 `[chiffre à vérifier]`
- eyebrow: LE SAVIEZ-VOUS ?
- message: En 1960, la France comptait plus de **4 actifs**\npour 1 retraité. Aujourd'hui, un peu moins de 2.
- cta: 👉 Ta solution pour dans 10 ans ? Dis-le en commentaire

*Ordre de grandeur courant (données historiques type INSEE/COR) — chiffre
exact et année précise à vérifier sur une source primaire avant mise en
rotation, voir point 3 ci-dessus.*

### chiffre-02 `[chiffre à vérifier]`
- eyebrow: LE SAVIEZ-VOUS ?
- message: La population mondiale devrait franchir\nles **9,7 milliards** d'habitants vers 2050.
- cta: 👉 Ton pronostic pour dans 10 ans, en commentaire ?

*Ordre de grandeur ONU (World Population Prospects) — à vérifier sur la
publication la plus récente avant mise en rotation.*

### chiffre-03 `[chiffre à vérifier]`
- eyebrow: LE SAVIEZ-VOUS ?
- message: Le seuil des **+1,5°C** de réchauffement\npourrait être franchi dès le début des années 2030.
- cta: 👉 Où on en sera dans 10 ans ? Ton avis en commentaire

*Ordre de grandeur GIEC — à vérifier sur le dernier rapport avant mise en
rotation (les projections évoluent d'un rapport à l'autre).*

## 5. Grands futurs — les inventions qui pourraient changer le quotidien (rotation E)

Objectif : projeter, jamais affirmer. Des technologies réelles, déjà en
développement ou en test — pas de science-fiction, pas d'invention
imaginaire — mais dont l'arrivée et l'impact restent incertains.

**Règle non négociable : toujours au conditionnel.** Jamais "la voiture
n'aura plus besoin de toi", toujours "la voiture pourrait ne plus avoir
besoin de toi" — même exigence que le reste du site (une probabilité
n'est jamais une certitude). Une entrée rédigée à l'indicatif/futur simple
("sera", "va révolutionner", "changera") doit être reformulée avant
d'entrer dans cette liste, jamais publiée telle quelle.

**Vigilance particulière sur le survol technologique ("hype").** Ce
secteur (quantique, fusion, IA, longévité...) a un long historique
d'annonces "dans 10 ans" jamais tenues — vérifier que la technologie
citée a un vrai jalon concret déjà atteint (essai clinique en cours,
prototype fonctionnel, calendrier annoncé par un acteur sérieux), pas
seulement un concept ou une promesse marketing. **Toutes les entrées sont
marquées `[à vérifier]`** au moment de la rédaction, même discipline que
la section 4 : à sourcer avant la première mise en rotation.

### futur-01 `[à vérifier]`
- eyebrow: GRAND FUTUR
- message: Dans 10 ans, la voiture pourrait\nne plus jamais avoir besoin de toi au volant.
- cta: 👉 Prêt à lâcher le volant ? Dis-le en commentaire

*Conduite autonome (niveaux 4/5) — déjà des services réels limités
(robotaxis) dans quelques villes ; généralisation et calendrier réel à
vérifier avant mise en rotation.*

### futur-02 `[à vérifier]`
- eyebrow: GRAND FUTUR
- message: Et si l'énergie devenait presque illimitée ?\nPlusieurs projets de fusion nucléaire visent une première électricité commerciale d'ici les années 2030.
- cta: 👉 On y sera dans 10 ans ? Ton avis en commentaire

*Fusion nucléaire — jalons réels (ITER et projets privés) mais calendrier
historiquement optimiste dans ce secteur ; vérifier l'état d'avancement
le plus récent avant mise en rotation.*

### futur-03 `[à vérifier]`
- eyebrow: GRAND FUTUR
- message: Des chercheurs pensent qu'on pourrait bientôt\nralentir le vieillissement biologique, pas seulement le soigner.
- cta: 👉 Toi, tu ferais quoi de 10 ans de plus ? Dis-le en commentaire

*Recherche sur la longévité (essais en cours sur plusieurs molécules) —
encore au stade expérimental, formulation "des chercheurs pensent"
volontairement prudente ; vérifier l'état des essais avant mise en
rotation.*

### futur-04 `[à vérifier]`
- eyebrow: GRAND FUTUR
- message: L'ordinateur quantique pourrait un jour résoudre\nen minutes des calculs impossibles pour un supercalculateur classique.
- cta: 👉 Tu l'utiliserais pour quoi, toi ? Dis-le en commentaire

*Informatique quantique — progrès réels mais usages pratiques encore
limités à des cas de niche ; vérifier qu'aucune annonce trop optimiste
ne s'est glissée dans la formulation avant mise en rotation.*

## Règle de rotation

La routine avance dans chaque liste (Manifeste, Citations, Questions,
Chiffres, Grands futurs) indépendamment, dans l'ordre où les entrées
apparaissent ci-dessus, sans répéter avant d'avoir fait le tour de la
liste entière — voir `docs/routine-pub-prompt.md` pour le mécanisme exact
(déduit de l'historique déjà publié dans `feed-pub.xml`, pas de fichier
d'état séparé). Faire tourner les 5 catégories dans cet ordre fixe
(Manifeste → Citation → Question → Chiffre → Grand futur → Manifeste...)
plutôt que de les mélanger au hasard, pour garder un rythme reconnaissable.

**Fréquence.** Cadence de croisière : 1 publication/semaine. **Au
lancement, fréquence volontairement plus élevée** (décision utilisateur du
13 août, pas de chiffre arrêté) le temps de construire l'habitude —
ajustée à la main via `update_trigger` sur le trigger "Scénario — Pub
hebdo", pas un mécanisme automatique dans la routine elle-même.

**Ajouter une entrée** : lui donner un id qui ne sera jamais réutilisé,
même après suppression (traçabilité de l'historique de rotation). Ne
jamais modifier le texte d'une entrée déjà publiée au moins une fois —
en créer une nouvelle à la place, pour que l'historique de ce qui a été
réellement montré reste exact.
