# Banque de messages — routine "pub" hebdomadaire

Liste fermée et curée à la main, dans le même esprit que `docs/tags.md` ou
`sujets-prioritaires.md` : la routine hebdomadaire (`docs/routine-pub-
prompt.md`) **pioche dans cette liste en rotation, elle n'invente jamais un
message ni une citation elle-même** — voir la justification dans
`docs/ARCHITECTURE.md` (risque de citation mal attribuée ou inventée par un
LLM, déjà identifié pendant la conception de cette routine).

**Statut : brouillon, pas encore validé pour publication.** Deux points à
trancher avant de mettre cette liste en service :
1. Les lignes marquées `[à confirmer]` dans la section Manifeste font une
   affirmation sur le modèle économique (pas de sponsor, etc.) que je ne
   peux pas vérifier moi-même — à valider ou reformuler avant usage.
2. Les citations marquées `[attribution à vérifier]` dans la section
   Citations ont une attribution courante mais pas 100 % certaine — à
   vérifier une source primaire avant publication, ou à retirer.

## Format d'une entrée

```
### {id unique, court, jamais réutilisé même si l'entrée est retirée}
- eyebrow: {texte affiché en haut de l'image, MAJUSCULES}
- message: {texte principal, \n autorisé pour forcer un saut de ligne}
- attribution: {optionnel, uniquement pour les citations, ex. "— Louis Pasteur"}
- cta: {optionnel, ligne d'appel à l'action sous le message}
```

## 1. Manifeste — pourquoi Scénario (rotation A)

Objectif : rappeler ce qui différencie le projet, pour la rétention de la
communauté déjà abonnée — jamais un ton commercial, la même sobriété que le
reste du site.

### manifeste-01
- eyebrow: POURQUOI SCÉNARIO
- message: Gratuit. Indépendant.\nNi de gauche ni de droite.
- cta: 👉 lesscenarios.fr

*Reprend mot pour mot la ligne éditoriale de `le-projet.html` : "ne défend
aucune ligne, ni de gauche ni de droite, aucun parti pris."*

### manifeste-02
- eyebrow: POURQUOI SCÉNARIO
- message: On ne prédit pas l'avenir.\nOn chiffre l'incertitude.
- cta: 👉 lesscenarios.fr

*Reprend l'idée de `le-projet.html` : "des métiers où l'on chiffre
l'incertitude plutôt que de deviner un seul avenir."*

### manifeste-03
- eyebrow: POURQUOI SCÉNARIO
- message: Une probabilité n'est jamais gravée dans le marbre.\nQuand les faits changent, elle change.
- cta: 👉 Suivi mis à jour dès qu'un scénario bouge

*Reprend `le-projet.html` : "Un pourcentage donné dans une édition n'est
pas une vérité gravée dans le marbre [...]. Quand la situation évolue,
l'estimation doit évoluer avec elle."*

### manifeste-04
- eyebrow: POURQUOI SCÉNARIO
- message: Pas de tirage au hasard.\nUne méthode, appliquée à chaque édition.
- cta: 👉 lesscenarios.fr

*Reprend `le-projet.html` : "chaque estimation s'appuie sur une méthode
propriétaire, appliquée systématiquement à chaque édition."*

### manifeste-05 `[à confirmer]`
- eyebrow: POURQUOI SCÉNARIO
- message: Aucune pub. Aucun sponsor.\nJuste trois scénarios chiffrés.
- cta: 👉 lesscenarios.fr

*Affirmation sur le modèle économique — à confirmer avant usage (aucune
mention équivalente déjà publiée ailleurs sur le site à recopier).*

### manifeste-06 `[à confirmer]`
- eyebrow: POURQUOI SCÉNARIO
- message: Gratuit, sans compte à créer.\nLe lien en bio suffit.
- cta: 👉 lesscenarios.fr

*"Sans compte à créer" — à confirmer que c'est bien exact (pas de zone
membre sur le site à ma connaissance, mais à vérifier avant publication).*

## 2. Citations — le hasard et l'incertitude (rotation B)

Objectif : varier le feed avec du contenu plus léger/partageable, en lien
thématique avec le projet, sans ton commercial du tout.

### citation-01
- eyebrow: UNE CITATION
- message: « Le hasard ne favorise que les esprits préparés. »
- attribution: — Louis Pasteur

*Source solide : formule d'une conférence de Pasteur à l'université de
Lille, 1854, très largement documentée.*

### citation-02
- eyebrow: UNE CITATION
- message: « Il y a des choses qui dépendent de nous,\net d'autres qui n'en dépendent pas. »
- attribution: — Épictète

*Source solide : ouverture du Manuel d'Épictète.*

### citation-03
- eyebrow: UNE CITATION
- message: « La théorie des probabilités n'est, au fond,\nque le bon sens réduit au calcul. »
- attribution: — Pierre-Simon de Laplace

*Source solide : Essai philosophique sur les probabilités, 1814.*

### citation-04 `[attribution à vérifier]`
- eyebrow: UNE CITATION
- message: « Le hasard, c'est peut-être le pseudonyme\nde Dieu quand il ne veut pas signer. »
- attribution: — Anatole France

*Attribution courante (Le Jardin d'Épicure, 1894) mais à vérifier sur une
édition de référence avant publication — formule très reprise, parfois de
façon approximative.*

### citation-05 `[attribution à vérifier]`
- eyebrow: UNE CITATION
- message: « Le doute n'est pas une condition agréable,\nmais la certitude est absurde. »
- attribution: — Voltaire

*Attribution très répandue mais disputée par certains chercheurs (parfois
présentée comme une paraphrase plutôt qu'une citation exacte d'un texte
identifié) — à vérifier ou à retirer avant publication.*

### citation-06
- eyebrow: UNE CITATION
- message: « On ne se baigne jamais deux fois\ndans le même fleuve. »
- attribution: — Héraclite

*Fragment antique, formulation reconstituée (normal pour un fragment
présocratique transmis indirectement) — thème de l'impermanence/incertitude,
pas du hasard au sens strict, mais reste pertinent pour la ligne éditoriale.*

## Règle de rotation

La routine avance dans chaque liste (Manifeste, Citations) indépendamment,
dans l'ordre où les entrées apparaissent ci-dessus, sans répéter avant
d'avoir fait le tour de la liste entière — voir `docs/routine-pub-prompt.md`
pour le mécanisme exact (état de rotation stocké où et comment). Alterner
les deux catégories une semaine sur deux plutôt que de les mélanger au
hasard, pour garder un rythme reconnaissable.

**Ajouter une entrée** : lui donner un id qui ne sera jamais réutilisé,
même après suppression (traçabilité de l'historique de rotation). Ne
jamais modifier le texte d'une entrée déjà publiée au moins une fois —
en créer une nouvelle à la place, pour que l'historique de ce qui a été
réellement montré reste exact.
