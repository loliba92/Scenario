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

### question-02
- eyebrow: À VOUS DE JOUER
- message: Une question qui te trotte dans la tête\net dont tu voudrais 3 scénarios chiffrés ?
- cta: 👉 On lit tous les commentaires

*Reste plus légère qu'une demande de sujet construit (question-01,
retiré) : elle part de ce que le lecteur a déjà en tête plutôt que de lui
demander de réfléchir à un sujet.*

### question-03
- eyebrow: À VOUS DE JOUER
- message: Parmi les 3 scénarios de la semaine,\nlequel t'a le plus surpris ?
- cta: 👉 Dis-nous lequel

*Réagit sur du contenu déjà publié plutôt que de solliciter une nouvelle
idée — variante utile pour ne pas répéter le même type de question à
chaque publication.*

### question-04
- eyebrow: À VOUS DE JOUER
- message: Pour toi, c'est quoi le vrai risque\npour la société dans 10 ans ?
- cta: 👉 Dis-le en commentaire

*Demande un avis, pas une idée à construire — plus facile à répondre en
scrollant que question-01 (retiré). Retour utilisateur du 13 août ;
variante "quel est ton rêve" écartée par l'utilisateur lui-même comme
trop convenue.*

## 4. Grands futurs — inventions et grands risques du siècle (rotation D)

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

## Règle de rotation

La routine avance dans chaque liste (Manifeste, Citations, Questions,
Grands futurs) indépendamment, dans l'ordre où les entrées apparaissent
ci-dessus, sans répéter avant d'avoir fait le tour de la liste entière —
voir `docs/routine-pub-prompt.md` pour le mécanisme exact (déduit de
l'historique déjà publié dans `feed-pub.xml`, pas de fichier d'état
séparé). Faire tourner les 4 catégories dans cet ordre fixe (Manifeste →
Citation → Question → Grand futur → Manifeste...) plutôt que de les
mélanger au hasard, pour garder un rythme reconnaissable. **Catégorie
"Le saviez-vous" (chiffres) retirée le 13 août**, jugée pas indispensable
pour démarrer — à réintroduire dans le cycle si l'utilisateur la
réapprovisionne un jour, voir `docs/ARCHITECTURE.md`.

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
