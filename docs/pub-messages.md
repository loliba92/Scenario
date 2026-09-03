# Banque de messages — routine "pub" hebdomadaire

Liste fermée et curée à la main, dans le même esprit que `docs/tags.md` ou
`sujets-prioritaires.md` : la routine hebdomadaire (`docs/routine-pub-
prompt.md`) **pioche dans cette liste en rotation, elle n'invente jamais un
message ni une citation elle-même** — voir la justification dans
`docs/ARCHITECTURE.md` (risque de citation mal attribuée ou inventée par un
LLM, déjà identifié pendant la conception de cette routine).

**Statut au 13 août : validée pour démarrer.** 4 catégories actives
(Manifeste, Citations, Questions, Grands futurs) — toutes les entrées
encore incertaines ont été retirées plutôt que laissées en attente de
vérification (voir `docs/ARCHITECTURE.md`). La catégorie "Le saviez-vous"
(chiffres) a été retirée entièrement le 13 août, jugée pas indispensable
pour démarrer — à réintroduire plus tard si besoin, voir
`docs/ARCHITECTURE.md`.

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

*(Note du 13 août sur citation-05/citation-06 retirée le 14 août —
périmée : les deux ont depuis été retirées, voir la section Citations
ci-dessous.)*

## Format d'une entrée

```
### {id unique, court, jamais réutilisé même si l'entrée est retirée}
- eyebrow: {texte affiché en haut de l'image, MAJUSCULES}
- message: {texte principal, \n autorisé pour forcer un saut de ligne, **mot** pour surligner en doré}
- attribution: {optionnel, citations : "— Auteur" / chiffres : "— Source, année"}
- cta: {optionnel, ligne d'appel à l'action sous le message}
```

**Catégorie `chiffre` : `attribution`/`cta` ne s'affichent plus sur
l'image** depuis la refonte du 21 août du gabarit dédié
(`pub-template-v5-stat.html`) — toujours à renseigner dans l'entrée, ils
passent directement dans la légende du post (`<comments>` de
`feed-pub.xml`), pas perdus, juste pas dupliqués sur le visuel.

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

### manifeste-07
- eyebrow: LA NEWSLETTER
- message: Trois scénarios chiffrés dans ta boîte mail,\ntous les matins.
- cta: 👉 Inscris-toi, 100% réalisable, jamais de science-fiction

*Objectif spécifique : pousser l'inscription à la newsletter (canal
distinct de "s'abonner" sur les réseaux) — retour utilisateur du 13 août.
"100% réalisable" reprend l'esprit du site : des scénarios bornés par des
faits, jamais de spéculation gratuite.*

### manifeste-08
- eyebrow: LA SEMAINE SCÉNARIO
- message: Un jour, un regard différent.\nGéopolitique, économie, sciences, culture, sport...
- cta: 👉 Abonne-toi, découvre le programme complet

*Reprend le rythme hebdomadaire déjà publié sur `le-projet.html` ("Sept
éditions par semaine, chacune ancrée dans un domaine") — objectif :
montrer la diversité des sujets traités plutôt qu'un simple rappel
d'identité. Reste un aperçu représentatif, pas la liste exhaustive des 7
jours (dont le mardi "carte blanche aux lecteurs") : le gabarit texte
actuel (`pub-template-v4-hybride.html`) est pensé pour 1-2 lignes courtes,
pas un tableau à 7 lignes — le programme complet reste sur `le-projet.html`,
d'où le lien du CTA (catégorie manifeste → `le-projet.html`, voir
`docs/routine-pub-prompt.md`). Une vraie carte-grille avec les 7 jours
demanderait un nouveau gabarit sans photo de fond, hors du pipeline actuel
— à faire séparément si utile.*

### manifeste-09
- eyebrow: LES 3 SCÉNARIOS
- message: Rien n'est écrit à l'avance.\n**Favorable**, **stable**, **dégradé** : trois chemins possibles, jamais une prophétie.
- cta: 👉 Découvre comment on les définit

*Ajouté le 14 août, reformulé le 18 août (retour utilisateur : le
premier jet — "Trois issues chiffrées, jamais une prédiction unique" —
était trop clinique, demandait quelque chose de plus spirituel) — garde
le principe central de `le-projet.html` § « Les trois scénarios »
(jamais une prédiction unique, trois issues chiffrées et réévaluées dans
le temps) mais ouvre sur "rien n'est écrit à l'avance" et referme sur
"prophétie" plutôt que "prédiction", pour se démarquer de manifeste-02
("On ne prédit pas l'avenir. On chiffre l'incertitude.") déjà publié le
16 août avec un vocabulaire proche. Les définitions détaillées
(favorable = la tension se résout plutôt bien, stable = le statu quo se
prolonge, dégradé = la situation se détériore nettement) tiennent sur
la page elle-même, pas sur l'image — le gabarit pub n'a la place que
pour un teaser (voir manifeste-08, même logique). Le CTA renvoie vers
`le-projet.html` via le lien automatique de la catégorie manifeste
(voir `docs/routine-pub-prompt.md`).*

### manifeste-10
- eyebrow: À VOUS DE JOUER
- message: Une question qui te trotte dans la tête\net dont tu voudrais 3 scénarios chiffrés ?
- cta: 👉 On lit tous les commentaires

*Déplacée depuis la catégorie `question` (dormante) le 18 août, à la
demande de l'utilisateur — était `question-02`, voir la trace dans la
section 3 ci-dessous. Reste plus légère qu'une demande de sujet construit
(l'ancien `question-01`, retiré) : elle part de ce que le lecteur a déjà
en tête plutôt que de lui demander de réfléchir à un sujet. **Point
d'attention du déplacement** : le lien du post suit désormais la règle
de la catégorie `manifeste` (`le-projet.html`), pas celle de `question`
(`contact.html`) — le CTA "On lit tous les commentaires" invite à réagir
en commentaire sur le réseau social, ce qui reste cohérent même si le
clic renvoie vers la page projet plutôt que la page contact.*

### manifeste-11
- eyebrow: SOUTENEZ SCÉNARIO
- message: Partager Scénario autour de vous, c'est le plus simple des coups de pouce pour nous aider à grandir.
- cta: 👉 Soutenez-nous ici : buymeacoffee.com/scenario
- cta-image: 👉 Soutenez-nous — lien ci-dessous
- link: https://buymeacoffee.com/scenario

*Créée le 18 août comme catégorie séparée (`soutien`, samedi), repliée
le même jour dans `manifeste` à la demande de l'utilisateur — logique
attendue : pas de jour dédié, juste une entrée de plus dans la rotation
`manifeste` (dimanche/vendredi), au même titre que manifeste-01…10.
Adaptée d'un rappel Buy Me a Coffee reçu côté créateur ("Your fans are
waiting!..."), reformulée pour s'adresser au lecteur plutôt qu'au
créateur. **Champ `link` (nouveau, optionnel)** : override le lien par
défaut de la catégorie (`le-projet.html` pour `manifeste`) — sans lui,
ce post perdrait sa seule raison d'être (rediriger vers la page de don)
en renvoyant vers la page projet comme toutes les autres entrées
manifeste. Voir `docs/routine-pub-prompt.md`, étape 4, pour la règle
générale : si une entrée définit `link`, il prime sur le lien
automatique de sa catégorie.*

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
- cta: 👉 Abonne-toi, on fait le calcul pour toi

*Source solide : Essai philosophique sur les probabilités, 1814.*


### citation-05 `[retiré le 13 août]`
*Était : « Le doute n'est pas une condition agréable, mais la certitude
est absurde. » — Voltaire. Retiré : trop littéraire/abstrait pour "monsieur
tout le monde" (retour utilisateur du 13 août), en plus d'une attribution
disputée. Remplacé par citation-07/08/09/10 ci-dessous. Id jamais réutilisé
(voir "Règle de rotation"), gardé en trace ici plutôt que supprimé.*

### citation-06 `[retiré le 13 août]`
*Était : « On ne se baigne jamais deux fois dans le même fleuve. » —
Héraclite. Retiré : trop philosophique/mélancolique pour "monsieur tout le
monde" (retour utilisateur du 13 août). Remplacé par citation-07/08/09/10
ci-dessous. Id jamais réutilisé, gardé en trace ici plutôt que supprimé.*

### citation-07
- eyebrow: UNE CITATION
- message: « La fortune sourit aux audacieux. »
- attribution: — Proverbe latin
- cta: 👉 Abonne-toi, ose regarder plus loin

*Proche du vers de Virgile "Audentes Fortuna iuvat" (Énéide, X.284) — rendu
en proverbe latin plutôt qu'attribué nommément à Virgile, la formule
française circule surtout comme dicton, pas comme citation exacte d'un
texte précis. Simple, court, positif — bon fit "monsieur tout le monde".*

### citation-08
- eyebrow: UNE CITATION
- message: « Il y a plusieurs chemins\npour aller au sommet de la montagne. »
- attribution: — Proverbe chinois
- cta: 👉 Abonne-toi, explore les 3 chemins

*Attribuée à "la sagesse chinoise" comme beaucoup de proverbes de ce type
en circulation en Occident — origine textuelle précise non retracée,
présentée comme un dicton populaire plutôt qu'une citation d'auteur
identifié. Image simple et parlante, colle bien à l'idée des 3 scénarios.*


### citation-11
- eyebrow: UNE CITATION
- message: « 100 % des gagnants ont tenté leur chance. »
- attribution: — Slogan historique de la Française des Jeux
- cta: 👉 On a tenté la nôtre en lançant Scénario. Abonne-toi.

*Pas une citation d'auteur mais un slogan publicitaire réel (FDJ) —
assumé comme tel dans l'attribution plutôt que déguisé en citation. Sujet
sensible (loterie/jeu d'argent) : à utiliser au second degré sur le thème
du hasard, jamais comme une incitation à jouer — si ça pose un problème
en le relisant à froid, le retirer plutôt que le garder par principe.*

### citation-12
- eyebrow: UNE CITATION
- message: « On descend toujours par l'ascenseur,\net on remonte par l'escalier. »
- attribution: — dicton de trader
- cta: 👉 On te dit où en est la remontée. Abonne-toi.

*Dicton de salle de marché sur l'asymétrie chute rapide / reprise lente —
pas d'auteur précis identifiable, présenté comme un dicton plutôt qu'une
citation nominative pour rester honnête. Fait écho à l'idée de pondération
asymétrique du France Impact, encore à l'état de discussion dans
`docs/ARCHITECTURE.md` (pas implémentée).*


## 3. Questions à la communauté (rotation C)

Objectif : faire réagir, pas informer — engagement direct, notamment pour
alimenter le mardi "carte blanche" (sujet libre suggéré par les lecteurs).
Jamais de chiffre ni de citation ici, juste une question ouverte.

### question-01 `[retiré le 13 août]`
*Était : "Quel sujet libre voudrais-tu voir décrypté en 3 scénarios mardi
prochain ?" Retiré : retour utilisateur direct — "on n'en sait rien, les
gens scrollent", une question qui demande de proposer un sujet de zéro
ne marche pas dans un feed qu'on parcourt vite. Remplacé par question-04
ci-dessous, qui demande un avis plutôt qu'une idée à construire. Id
jamais réutilisé, gardé en trace ici.*

### question-02 `[déplacé vers manifeste-10 le 18 août]`
*Était : eyebrow "À VOUS DE JOUER", message "Une question qui te trotte
dans la tête, et dont tu voudrais 3 scénarios chiffrés ?", cta "On lit
tous les commentaires". Déplacé à la demande de l'utilisateur (18 août)
vers la catégorie `manifeste`, voir manifeste-10 en section 1 pour le
contenu actuel. Id jamais réutilisé, gardé en trace ici — la catégorie
`question` reste par ailleurs dormante (voir `docs/routine-pub-
prompt.md`).*

### question-03 `[retiré le 14 août]`
*Était : "Parmi les 3 scénarios de la semaine, lequel t'a le plus
surpris ?" Retiré : retour utilisateur direct — "ça veut rien dire",
question trop floue/abstraite pour un lecteur qui scrolle (aucun des 3
scénarios d'une semaine donnée n'est nommément rappelé, la question ne
tient pas seule dans un post). Id jamais réutilisé, gardé en trace ici.*

### question-04
- eyebrow: À VOUS DE JOUER
- message: Pour toi, c'est quoi le vrai risque\npour la société dans 10 ans ?
- cta: 👉 Dis-le en commentaire

*Demande un avis, pas une idée à construire — plus facile à répondre en
scrollant que question-01 (retiré). Retour utilisateur du 13 août ;
variante "quel est ton rêve" écartée par l'utilisateur lui-même comme
trop convenue.*

## 4. Grands futurs — inventions et grands risques du siècle (rotation D)

**Catégorie dormante depuis le 21 août** (retour utilisateur direct :
abandon pour l'instant, remplacée par "Le saviez-vous" le jeudi dans la
table de rotation ci-dessous) — pas supprimée, le mécanisme de recherche
et les entrées déjà présentes restent en place, prêtes à être réactivées
si l'utilisateur lui redonne un jour.

Objectif : projeter, jamais affirmer. Deux angles dans la même catégorie
— des inventions qui pourraient changer le quotidien et des grands
risques du siècle — des technologies ou des menaces réelles, déjà en
développement/déjà documentées, pas de science-fiction ni de
catastrophisme gratuit, mais dont l'arrivée et l'impact restent
incertains.

**Mécanisme différent des 4 autres catégories — pas une liste fermée qui
tourne en boucle** (retour utilisateur du 13 août : "je ferai pas une
liste ferme sinon ça tourne et c'est boring"). Les entrées ci-dessous
servent de **calibrage** (le niveau de précision/surprise attendu, voir
règle juste en dessous) plutôt que d'un stock fixe à épuiser avant de
répéter. Voir `docs/routine-pub-prompt.md` pour le mécanisme exact : à
chaque tour de cette catégorie, la routine peut soit reprendre une entrée
existante pas trop récemment utilisée, soit **chercher et rédiger un
nouveau fait, à condition de le vérifier par une vraie source (WebFetch)
avant de l'écrire** — jamais une invention libre comme pour les autres
catégories. Toute nouvelle entrée ajoutée porte sa source (URL) en plus
du texte, et reste soumise aux mêmes règles non négociables ci-dessous.

**Règle non négociable : toujours au conditionnel** pour tout ce qui
n'est pas encore arrivé. Jamais "la voiture n'aura plus besoin de toi",
toujours "la voiture pourrait ne plus avoir besoin de toi" — même
exigence que le reste du site (une probabilité n'est jamais une
certitude). Une entrée rédigée à l'indicatif/futur simple sur un fait pas
encore établi doit être reformulée avant d'entrer dans cette liste.

**Règle ajoutée le 13 août, retour utilisateur direct : "pas de trucs
bateau, pas besoin d'écrire des trucs que tout le monde sait".** Interdit
les catégories génériques trop connues pour surprendre qui que ce soit
("la voiture autonome", "le climat, risque n°1"...). À la place, un fait
**précis, daté, chiffré si possible** — un jalon déjà atteint ou une
découverte spécifique, pas un concept que tout le monde a déjà croisé
100 fois. Le test : si un lecteur qui suit un peu l'actualité tech/
science hausse les épaules en lisant "ça, je le savais déjà", l'entrée
est à refaire.

**Vigilance particulière sur le survol technologique ("hype").** Ce
secteur a un long historique d'annonces jamais tenues — vérifier que le
fait cité a un vrai jalon concret déjà atteint (essai clinique en cours,
prototype fonctionnel, publication scientifique, annonce d'un acteur
sérieux), pas seulement un concept ou une promesse marketing.

**Section vide depuis le 13 août** — les 7 entrées initiales retirées,
aucune vérifiée sur une vraie source (voir `docs/ARCHITECTURE.md`).
Contrairement à la section 4, ce n'est pas bloquant ici : le mécanisme de
recherche à la volée (voir plus haut et `docs/routine-pub-prompt.md`)
peut faire repartir cette catégorie de zéro. **Exemples de calibrage
seulement, jamais des entrées prêtes à publier** (niveau de précision/
surprise attendu, pas un texte à recopier tel quel) :
- "En 2022, un réacteur a produit pour la première fois plus d'énergie de
  fusion qu'il n'en avait reçu" plutôt que "la fusion nucléaire va
  changer l'énergie".
- "Des patients paralysés peuvent déjà déplacer un curseur d'ordinateur
  par la pensée grâce à une puce implantée" plutôt que "les interfaces
  cerveau-machine, c'est l'avenir".
- "Aux États-Unis, plusieurs assureurs ont déjà cessé de couvrir
  certaines zones inondables ou à risque incendie" plutôt que "le climat
  est le risque n°1 du siècle".

### futur-01
- eyebrow: GRAND FUTUR
- message: Depuis mai 2025, des camions **sans chauffeur**\nroulent déjà avec du fret entre Dallas et Houston.
- attribution: — Aurora Innovation, mai 2025
- cta: 👉 Abonne-toi, on suit ces bascules au quotidien
- source: https://aurora.tech/blog
- photo: `assets/social/topic-images/2026-08-19.jpg` (crédit : aslanbutlercontact,
  Pixabay — https://pixabay.com/users/aslanbutlercontact-1486943/), photo de
  rotation générique (pas liée au sujet du post, mécanisme normal des
  catégories hors `chiffre`, voir `docs/routine-pub-prompt.md`).

*Première entrée de cette catégorie depuis sa remise à zéro le 13 août —
trouvée le 20 août via WebFetch (1er appel : `en.wikipedia.org/wiki/
Aurora_Innovation`, qui synthétise plusieurs jalons datés ; 2e appel :
`aurora.tech/blog`, confirme l'annonce officielle "Aurora Begins
Commercial Driverless Trucking in Texas", 1er mai 2025 — jalon retenu
pour le message ; 3e appel : `ir.aurora.tech`, n'a rien apporté de plus
précis). Jalon déjà atteint (camions déjà en service commercial sans
chauffeur), donc rédigé à l'indicatif comme les exemples de calibrage
ci-dessus — pas une projection. Les chiffres plus précis vus sur
Wikipedia (nombre exact de camions, miles parcourus, objectif de fin
d'année) n'ont pas pu être recoupés sur une deuxième source primaire dans
le budget de 3 appels : volontairement laissés hors du message plutôt que
publiés sur une seule source tertiaire.*

## 5. Le saviez-vous — un chiffre qui marque (rotation E)

**Réintroduite le 14 août, à la demande de l'utilisateur, avec un
mécanisme différent de la version retirée le 13 août.** L'ancienne
version (voir `docs/ARCHITECTURE.md`) était une liste fermée à
approvisionner à la main, jamais réamorcée faute de temps. Cette fois :
**jamais un chiffre inventé ou recalculé — toujours extrait tel quel
d'une édition déjà publiée sur `lesscenarios.fr`, donc déjà vérifiée par
le processus éditorial normal (sources croisées, relecture) avant même
d'atterrir ici.** Ça élimine le risque qui avait fait retirer citation-04/
09/10 et chiffre-01/02/03 le 13 août (fait/citation mal attribué ou
inventé par un LLM) : on ne génère rien, on cite.

**Mécanisme (voir `docs/routine-pub-prompt.md` pour la procédure
exacte) :**
1. Scanner les éditions quotidiennes publiées dans les ~30 derniers jours
   (`archives/*.html`), jamais les pages de suivi ni le récap hebdo.
2. Repérer les phrases de `.dek` ou `.essentiel-text` contenant un
   chiffre mis en évidence (`<strong>`) — un pourcentage, un montant, un
   nombre de personnes, une date marquante, etc.
3. Écarter les éditions dont le chiffre a déjà servi dans un post
   "chiffre" précédent (déduit de `feed-pub.xml`, même logique que les
   autres catégories) et les éditions publiées il y a moins de 24h (leur
   laisser le temps d'un passage par la routine Inspecteur avant d'être
   citées ailleurs).
4. **Rester sur une seule édition par jour** (retour utilisateur du
   3 septembre : comparer plusieurs éditions à chaque tour risquerait de
   réutiliser le même vivier de chiffres d'un jour sur l'autre) — prendre
   l'édition candidate la plus récente, n'en changer que si elle n'a
   vraiment aucun chiffre exploitable. À l'intérieur de cette édition,
   choisir **la phrase qui porte l'information la plus importante de
   l'édition — pas forcément le chiffre le plus spectaculaire** (règle du
   14 août sur la simplicité, affinée le 3 septembre après un chiffre
   jugé secondaire et daté — voir `docs/routine-pub-prompt.md`, étape
   1.7.b/c, pour le détail et l'exemple) : le point clé que l'édition
   raconte vraiment, celui qu'un lecteur n'ayant lu que le titre
   retiendrait comme message principal. Un chiffre marquant qui exprime
   ce point clé est bienvenu (le gabarit en a besoin pour le champ
   `stat`), mais ce n'est qu'une conséquence du choix, jamais le critère
   de départ — ne pas préférer un chiffre secondaire juste parce qu'il
   sonne plus fort qu'un chiffre central mais plus sobre. La phrase doit
   rester compréhensible seule, sans avoir lu le reste de l'édition ;
   écarter les phrases à clauses multiples ou au jargon non expliqué. À
   égalité d'importance entre deux phrases de la même édition, préférer
   celle sans millésime qui la date (éviter "en {année passée}") — mais
   ne jamais écarter le point clé réel de l'édition au seul motif qu'il
   porte une date. Préférer `.essentiel-text` à `.dek` quand les deux ont
   un candidat valable — déjà écrit dans un registre plus simple.
5. Recopier **mot pour mot, jamais reformulée** (même discipline que les
   citations) — le chiffre extrait seul alimente le champ `stat`, les
   phrases retenues alimentent `message` (le texte affiché en légende,
   voir "Gabarit dédié" ci-dessous). **Jusqu'à 2-3 phrases, pas
   forcément une seule** (assoupli le 3 septembre avec la refonte du
   gabarit) : la phrase qui porte le fait retenu peut être suivie ou
   précédée d'1 à 2 phrases **contiguës** du même paragraphe source, pour
   donner un peu de contexte — jamais piochées ailleurs dans l'édition,
   jamais réordonnées, jamais reliées par un connecteur ajouté. Rester
   sous ~280 caractères au total, une seule idée par phrase. Si la phrase
   source est trop longue mais contient un segment autonome complet, on
   peut **ne garder que ce segment** (coupé à une virgule/point-virgule,
   avec majuscule initiale et point final ajoutés si besoin) — jamais un
   mot changé, déplacé ou ajouté, seulement raccourci. Détail complet
   dans `docs/routine-pub-prompt.md`, étape 1.7.c.
6. Journaliser l'entrée utilisée dans ce fichier après publication (id
   `chiffre-{AAAA-MM-JJ}`, jamais réutilisé), avec un lien vers l'édition
   source — même logique de traçabilité que les entrées `futur-{N}`.

**Format spécifique à cette catégorie** (s'ajoute au format standard) :
```
- stat: {le chiffre seul, tel qu'affiché dans l'édition source}
- source: {lien vers l'édition d'origine}
```
Le lien du post pointe vers l'édition source elle-même (pas
`le-projet.html` ni la page d'accueil) — contrairement aux autres
catégories, voir la table des liens dans `docs/routine-pub-prompt.md`.

**Gabarit dédié** : `scripts/social/pub-template-v5-stat.html` — la photo
de l'**édition source elle-même** occupe tout le cadre (changé le 15
août : auparavant fond uni sans photo, désormais `assets/social/topic-
images/{date de l'édition}.jpg`, voir `docs/routine-pub-prompt.md` étape
2 pour le mécanisme et le repli si cette image n'existe plus), avec une
légende (pastille + `message`, chiffre surligné en gras/orange
automatiquement dans son flux) ancrée en bas de l'image sur un dégradé
noir — style "Hugo Décrypte", refonte du 3 septembre qui remplace le
titre unique centré du 21 août. La légende peut désormais compter jusqu'à
2-3 phrases (voir point 5 ci-dessus), la photo reste visible sur son
tiers supérieur. Ne pas utiliser `pub-template-v4-hybride.html` pour
cette catégorie (le chiffre serait noyé dans le texte).

**Section vide au lancement** — comme "Grands futurs" le 13 août, ce
n'est pas bloquant : le mécanisme de scan alimente la catégorie à chaque
tour, pas de stock à préremplir.

### chiffre-2026-08-15
- eyebrow: LE SAVIEZ-VOUS
- stat: 24 %
- message: Le prix du pétrole a bondi de 24 % depuis février à cause du blocage du détroit d'Ormuz.
- attribution: — lesscenarios.fr, 13 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-13.html
- photo: `assets/social/topic-images/2026-08-13.jpg` (crédit : Zifeng
  Xiong — https://www.pexels.com/photo/cargo-ships-anchored-at-coastal-port-under-blue-sky-33284879/),
  photo de l'édition source elle-même — premier post à utiliser le
  mécanisme photo ajouté le 15 août.

*Extrait tel quel de `.essentiel-text` dans l'édition du 13 août
("Le prix du pétrole a bondi de 24 % depuis février à cause du blocage
du détroit d'Ormuz, et l'inflation américaine ressort déjà à 3,4 % sur
un an, loin de l'objectif de 2 % des banques centrales.") — segment
coupé à la première virgule (frontière naturelle avant "et"), point
final ajouté, aucun mot changé ni déplacé. Première entrée de cette
catégorie depuis sa réintroduction du 14 août.*

### chiffre-2026-08-17
- eyebrow: LE SAVIEZ-VOUS
- stat: 32-37 %
- message: Le Rassemblement national domine déjà les sondages du premier tour, entre 32 et 37 %.
- attribution: — lesscenarios.fr, 12 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-12.html
- photo: `assets/social/topic-images/2026-08-12.jpg` (crédit : Element5
  Digital — https://www.pexels.com/photo/person-dropping-paper-on-box-1550337/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.essentiel-text` dans l'édition du 12 août
("Le Rassemblement national domine déjà les sondages du premier tour,
entre 32 et 37 %, porté par une droite et une gauche toutes deux
divisées entre plusieurs prétendants qui refusent de s'unir.") — segment
coupé à la deuxième virgule (frontière naturelle avant "porté par"),
point final ajouté, aucun mot changé ni déplacé. Premier post publié un
lundi, cron passé quotidien le 17 août (voir `docs/routine-pub-
prompt.md`).*

### chiffre-2026-08-19
- eyebrow: LE SAVIEZ-VOUS
- stat: 3,0 %
- message: Le FMI a maintenu sa prévision de croissance mondiale pour 2026 à 3,0 % en juillet.
- attribution: — lesscenarios.fr, 10 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-10.html
- photo: `assets/social/topic-images/2026-08-10.jpg` (crédit : Julien
  Goettelmann — https://www.pexels.com/photo/aerial-view-of-cargo-ship-in-bosphorus-strait-28966472/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.essentiel-text` dans l'édition du 10 août
("Le FMI a maintenu sa prévision de croissance mondiale pour 2026 à
3,0 % en juillet, mais seulement grâce au boom des investissements dans
l'intelligence artificielle, qui compense un pétrole redevenu cher...")
— segment coupé à la première virgule (frontière naturelle avant "mais
seulement"), point final ajouté, aucun mot changé ni déplacé. Éditions
du 12 et 13 août déjà utilisées pour cette catégorie (chiffre-2026-08-17
et chiffre-2026-08-15) ; édition du 18 août écartée (moins de 24h) ;
éditions du 17 et 16 août candidates mais sans phrase autonome à un seul
chiffre assez simple (respectivement pétrole/Ormuz avec plusieurs
chiffres empilés, et rugby/commotions avec chiffres nécessitant du
contexte pour se comprendre seuls).*

### chiffre-2026-08-22
- eyebrow: LE SAVIEZ-VOUS
- stat: 5 764 décès en excès
- message: Rien que sur l'épisode du 17 juin au 2 juillet, Santé publique France a recensé au moins 5 764 décès en excès.
- attribution: — lesscenarios.fr, 14 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-14.html
- photo: `assets/social/topic-images/2026-08-14.jpg` (crédit : Fatih
  Turan — https://www.pexels.com/photo/a-city-during-sunset-12413177/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.dek` dans l'édition du 14 août ("Rien que sur
l'épisode du 17 juin au 2 juillet, Santé publique France a recensé au
moins 5 764 décès en excès, soit 36 % de morts en plus que d'habitude
sur la période — un chiffre qui approche déjà le record de l'été 2022
(6 969 morts), atteint ici en deux semaines à peine.") — segment coupé
à la première virgule (frontière naturelle avant "soit 36 %"), point
final ajouté, aucun mot changé ni déplacé ; édition sans
`.essentiel-text` exploitable en un seul chiffre (plusieurs stats
empilées : 10-15 milliards d'euros, 5 764 morts, budget divisé par
trois). Éditions du 10, 12 et 13 août déjà utilisées pour cette
catégorie ; édition du 21 août écartée (moins de 24h) ; édition du
4 août candidate solide sur le fond (bilan Gaza, 73 350 morts) mais
écartée faute de fichier `.jpg`/`.json` associé dans
`assets/social/topic-images/` (retour à l'étape 1.7a, voir
`docs/routine-pub-prompt.md` étape 2.2) ; édition du 6 août également
sans image associée.*

### chiffre-2026-08-24
- eyebrow: LE SAVIEZ-VOUS
- stat: 1 chance sur 6
- message: Le philosophe Toby Ord (Oxford) chiffre à environ 1 chance sur 6 le risque qu'une catastrophe mette fin à l'aventure humaine d'ici la fin du siècle.
- attribution: — lesscenarios.fr, 21 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-21.html
- photo: `assets/social/topic-images/2026-08-21.jpg` (crédit : Gabriel
  Mihalcea — https://www.pexels.com/photo/a-silhouette-of-an-observatory-under-a-starry-night-sky-12290473/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.essentiel-text` dans l'édition du 21 août
("Le philosophe Toby Ord (Oxford) chiffre à environ 1 chance sur 6 le
risque qu'une catastrophe mette fin à l'aventure humaine d'ici la fin
du siècle, avec l'intelligence artificielle non maîtrisée comme facteur
dominant (environ 1 sur 10), loin devant le nucléaire ou le climat pris
isolément.") — segment coupé à la première virgule (frontière naturelle
avant "avec l'intelligence artificielle"), point final ajouté, aucun
mot changé ni déplacé. Éditions du 10, 12, 13 et 14 août déjà utilisées
pour cette catégorie ; édition du 23 août écartée (moins de 24h).
Éditions du 15 au 22 août (hors 21) parcourues mais écartées faute de
phrase autonome à un seul chiffre assez simple (clauses multiples ou
chiffres empilés — Ormuz/pétrole, Fed/BCE, ingérence électorale,
box-office chinois...).*

### chiffre-2026-08-26
- eyebrow: LE SAVIEZ-VOUS
- stat: 376 missiles
- message: En juillet, la Russie a tiré 376 missiles sur l'Ukraine — un record depuis mai 2022.
- attribution: — lesscenarios.fr, 24 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-24.html
- photo: `assets/social/topic-images/2026-08-24.jpg` (crédit : Алесь
  Усцінаў — https://www.pexels.com/photo/demolished-residential-building-11734711/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.dek` dans l'édition du 24 août ("En juillet, la
Russie a tiré 376 missiles sur l'Ukraine — un record depuis mai 2022,
contre 288 en mars et 192 un an plus tôt.") — segment coupé à la
virgule avant "contre 288" (frontière naturelle, chiffres empilés
écartés), point final ajouté, aucun mot changé ni déplacé ; édition
sans `.essentiel-text` exploitable en un seul chiffre (45 % nécessite le
contexte du scénario, 80/20 % de l'évaluation d'impact nécessitent aussi
le contexte des trois scénarios). Éditions du 10, 12, 13, 14 et 21 août
déjà utilisées pour cette catégorie ; édition du 25 août écartée (moins
de 24h). Éditions du 15 au 23 août (hors 21) parcourues mais écartées
faute de phrase autonome à un seul chiffre assez simple (mêmes limites
que le tour précédent, plus 745 km²/627 km² empilés dans l'édition du
24 elle-même sur un autre paragraphe, et 57 % des Ukrainiens qui ne se
comprend qu'en connaissant le blocage sur le Donbas).*

### chiffre-2026-08-27
- eyebrow: LE SAVIEZ-VOUS
- stat: 60 %
- message: Les fournisseurs chinois représentent désormais plus de 60 % du trafic mondial de requêtes IA sur OpenRouter.
- attribution: — lesscenarios.fr, 25 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-25.html
- photo: `assets/social/topic-images/2026-08-25.jpg` (crédit : panumas
  nikhomkhai — https://www.pexels.com/photo/close-up-of-a-blue-server-rack-in-datacenter-37730211/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.essentiel-text` dans l'édition du 25 août ("Les
fournisseurs chinois représentent désormais plus de 60 % du trafic
mondial de requêtes IA sur OpenRouter (contre 45 % en avril 2026 et
moins de 2 % un an plus tôt), pendant que Washington accuse la start-up
chinoise Moonshot AI d'avoir siphonné un modèle américain pour
construire son propre modèle ouvert, Kimi K3.") — segment coupé avant
la parenthèse "(contre 45 %..." (frontière naturelle, chiffres
empilés écartés), point final ajouté, aucun mot changé ni déplacé.
Éditions du 10, 12, 13, 14, 21 et 24 août déjà utilisées pour cette
catégorie ; édition du 26 août écartée (moins de 24h, publiée la veille
à 06h30).*

### chiffre-2026-08-29
- eyebrow: LE SAVIEZ-VOUS
- stat: 34 par an
- message: Le quota chinois de films étrangers à partage de recettes reste fixé à 34 par an depuis 2015.
- attribution: — lesscenarios.fr, 22 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-22.html
- photo: `assets/social/topic-images/2026-08-22.jpg` (crédit : İNZİLE
  DAL — https://www.pexels.com/photo/photo-of-a-cinema-hall-14746411/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.essentiel-text` dans l'édition du 22 août ("Le
quota chinois de films étrangers à partage de recettes reste fixé à
34 par an depuis 2015 — un levier que Pékin peut resserrer du jour au
lendemain, comme annoncé dès avril 2025 en rétorsion aux droits de
douane de Trump — mais même sans lui, de moins en moins de films
américains ordinaires rapportent assez en Chine pour justifier le
détour.") — segment coupé au premier tiret (frontière naturelle avant
"un levier que Pékin..."), point final ajouté, aucun mot changé ni
déplacé ; édition sans chiffre exploitable plus simple par ailleurs
(40,6 % nécessite le contexte du semestre, 45 % celui du scénario).
Éditions du 10, 12, 13, 14, 21, 24 et 25 août déjà utilisées pour
cette catégorie ; édition du 28 août écartée (moins de 24h). Éditions
du 23, 26 et 27 août parcourues mais écartées faute de phrase autonome
à un seul chiffre assez simple (FIFA/48-64 équipes avec plusieurs
chiffres empilés ; retraites/COR avec plusieurs chiffres empilés ;
dette américaine avec plusieurs chiffres empilés et pronoms sans
antécédent hors contexte).*

### chiffre-2026-09-02
- eyebrow: LE SAVIEZ-VOUS
- stat: 21 %
- message: Les produits de la mer pèsent encore 21 % des exportations islandaises en 2024.
- attribution: — lesscenarios.fr, 31 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-31.html
- photo: `assets/social/topic-images/2026-08-31.jpg` (crédit : Jonathan
  Cooper — https://www.pexels.com/photo/cape-spear-battery-12505399/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.dek` dans l'édition du 31 août ("Le chiffre qui
explique ce refus : les produits de la mer pèsent encore 21 % des
exportations islandaises en 2024 — en baisse depuis 38,8 % en 2021,
mais toujours assez pour que Reykjavik refuse d'en perdre le
contrôle.") — segment coupé au premier tiret (frontière naturelle
avant "en baisse depuis 38,8 %..."), point final ajouté, aucun mot
changé ni déplacé ; ouverture de phrase ("Le chiffre qui explique ce
refus :") retirée car dépendante du contexte du référendum, pas du
segment retenu lui-même. Éditions du 10, 12, 13, 14, 21, 22, 24 et 25
août déjà utilisées pour cette catégorie ; édition du 1er septembre
écartée (moins de 24h). Première édition candidate parcourue (31 août)
avec plusieurs phrases à chiffre fort ; segment retenu préféré aux
alternatives de la même édition (394 000 habitants, sans sujet propre
une fois isolé ; 52,8 %/47,2 % du référendum, incompréhensible sans la
phrase précédente ; 1994/espace économique européen, valable mais
moins marquant) pour son impact narratif plus net (dépendance
économique qui explique le résultat du vote).*

*Extrait tel quel de `.essentiel-text` dans l'édition du 22 août ("Le
quota chinois de films étrangers à partage de recettes reste fixé à
34 par an depuis 2015 — un levier que Pékin peut resserrer du jour au
lendemain, comme annoncé dès avril 2025 en rétorsion aux droits de
douane de Trump — mais même sans lui, de moins en moins de films
américains ordinaires rapportent assez en Chine pour justifier le
détour.") — segment coupé au premier tiret (frontière naturelle avant
"un levier que Pékin..."), point final ajouté, aucun mot changé ni
déplacé ; édition sans chiffre exploitable plus simple par ailleurs
(40,6 % nécessite le contexte du semestre, 45 % celui du scénario).
Éditions du 10, 12, 13, 14, 21, 24 et 25 août déjà utilisées pour
cette catégorie ; édition du 28 août écartée (moins de 24h). Éditions
du 23, 26 et 27 août parcourues mais écartées faute de phrase autonome
à un seul chiffre assez simple (FIFA/48-64 équipes avec plusieurs
chiffres empilés ; retraites/COR avec plusieurs chiffres empilés ;
dette américaine avec plusieurs chiffres empilés et pronoms sans
antécédent hors contexte).*

### chiffre-2026-09-03
- eyebrow: LE SAVIEZ-VOUS
- stat: 7 millions
- message: Chaque jour, les utilisateurs de Suno génèrent environ 7 millions de chansons grâce à l'intelligence artificielle — de quoi recréer tout le catalogue de Spotify toutes les deux semaines.
- attribution: — lesscenarios.fr, 9 août 2026
- cta: 👉 Abonne-toi, un chiffre qui marque chaque jour
- source: https://lesscenarios.fr/archives/2026-08-09.html
- photo: `assets/social/topic-images/2026-08-09.jpg` (crédit : Anna
  Shvets — https://www.pexels.com/photo/black-vinyl-record-player-on-brown-wooden-table-5614105/),
  photo de l'édition source elle-même.

*Extrait tel quel de `.dek` dans l'édition du 9 août ("Chaque jour, les
utilisateurs de Suno génèrent environ 7 millions de chansons grâce à
l'intelligence artificielle — de quoi recréer tout le catalogue de
Spotify toutes les deux semaines."), astérisque de renvoi au lexique
sur "Suno" retiré (pure décoration HTML, même traitement que pour
"détroit d'Ormuz" dans chiffre-2026-08-15) ; aucun mot changé, déplacé
ni ajouté. Titre RSS tronqué au tiret (phrase complète jusqu'à
"...intelligence artificielle.") faute de quoi le `<title>` dépassait
nettement la longueur des titres déjà en place — le `message` complet,
lui, reste inchangé dans `<comments>`/`<description>`. Éditions du 10,
12, 13, 14, 21, 22, 24, 25 et 31 août déjà utilisées pour cette
catégorie ; édition du 2 septembre écartée (moins de 24h). Éditions du
23, 26 et 27 août déjà écartées précédemment (voir note sous
chiffre-2026-08-29). Première édition candidate parcourue cette fois
(1ᵉʳ septembre, présidentielle 2027) écartée faute de phrase à chiffre
unique et autonome (sondages 33-38 % dépendants du pronom "elle",
scénarios à 45/30/20 % empilés) ; édition du 9 août retenue ensuite
pour son chiffre à la fois simple, isolé et marquant.*

## 6. Soutenez Scénario — Buy Me a Coffee `[repliée dans manifeste le 18 août]`

*Créée le 18 août comme catégorie séparée (samedi), puis repliée le même
jour dans la catégorie `manifeste` à la demande de l'utilisateur — voir
`manifeste-11` en section 1. Le champ `cta-image` introduit ici (URL non
cliquable écrite sur l'image) reste documenté en étape 3 de
`docs/routine-pub-prompt.md`, désormais comme règle générale plutôt que
spécifique à cette catégorie retirée.*

## Règle de rotation

**Catégorie déterminée par le jour de la semaine, pas par un cycle qui
avance** (changement du 14 août, retour utilisateur direct : "voici le
calendrier systématique, tu ne pourras pas te perdre" — remplace
l'ancien mécanisme où la routine déduisait la catégorie suivante à
partir du dernier `<guid>` publié, jugé trop sujet à erreur). Table
complète et mécanisme dans `docs/routine-pub-prompt.md`, étape 1 :

| Jour | Catégorie |
|---|---|
| Dimanche | Manifeste |
| Lundi | Le saviez-vous |
| Mardi | Citation |
| Mercredi | Le saviez-vous |
| Jeudi | Le saviez-vous |
| Vendredi | Manifeste |
| Samedi | Le saviez-vous |

**21 août : "Grands futurs" mise en pause, jeudi repasse sur "Le
saviez-vous".** Retour utilisateur direct : abandon de "Grand futur" pour
l'instant. **"Questions" et "Grands futurs" ne sont dans aucun jour de
cette table — catégories dormantes**, pas supprimées : leurs entrées
(sections 3 et 4) restent en place, prêtes si l'utilisateur leur redonne
un créneau plus tard.

**"Soutien" (Buy Me a Coffee) n'a pas non plus de ligne dédiée** — testé
un temps sur samedi le 18 août, puis replié le même jour dans `Manifeste`
(entrée `manifeste-11`, section 1) à la demande de l'utilisateur : il
sort donc les dimanches/vendredis, quand c'est le tour de `manifeste`
dans sa propre rotation interne, pas selon un jour fixe à lui.

Dans chaque catégorie, la routine avance dans sa propre liste
indépendamment (l'ordre où les entrées apparaissent ci-dessus, sans
répéter avant d'avoir fait le tour) — ça, ça n'a pas changé, seule la
façon de déterminer *quelle* catégorie traiter aujourd'hui a été
remplacée. **Catégorie "Le saviez-vous" (chiffres) réintégrée le
14 août**, avec un mécanisme d'extraction (voir section 5 ci-dessus)
plutôt que la liste fermée retirée le 13 août — voir
`docs/ARCHITECTURE.md` pour l'historique de la décision.

**Fréquence.** Cadence de croisière visée : 1 publication/semaine. **Au
lancement, fréquence volontairement plus élevée** le temps de construire
l'habitude et pendant la période de croissance de la chaîne — ajustée à
la main via `update_trigger` sur le trigger "Scénario — Pub hebdo", pas
un mécanisme automatique dans la routine elle-même.
- 13 août : 2x/semaine (mardi, vendredi, 18h Paris).
- 14 août (1er ajustement) : passée à **4x/semaine** (dimanche, mardi,
  jeudi, vendredi, 18h Paris — `0 16 * * 0,2,4,5` UTC), retour
  utilisateur explicite pour pousser la visibilité pendant la croissance.
- 14 août (2e ajustement, même jour) : **samedi ajouté, 5x/semaine**
  (dimanche, mardi, jeudi, vendredi, samedi, 18h Paris —
  `0 16 * * 0,2,4,5,6` UTC), pour que le post du lendemain (15 août,
  samedi) tombe sur la catégorie `chiffre` fraîchement réintégrée — voir
  aussi le réordonnancement du cycle ci-dessus. À redescendre vers 1x/
  semaine une fois la phase de lancement passée, pas de date arrêtée.

**Ajouter une entrée** : lui donner un id qui ne sera jamais réutilisé,
même après suppression (traçabilité de l'historique de rotation). Ne
jamais modifier le texte d'une entrée déjà publiée au moins une fois —
en créer une nouvelle à la place, pour que l'historique de ce qui a été
réellement montré reste exact.
