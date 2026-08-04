# Méthodologie de détermination des probabilités — document interne

**Statut : usage interne uniquement.** Pas de lien depuis le site public, pas
d'annonce. Ce document vit dans le dépôt (comme `routine-prompt.md` ou
`ARCHITECTURE.md`), donc techniquement visible si le dépôt GitHub est public
et que quelqu'un va fouiller l'historique — mais il n'est référencé,
indexé ni promu nulle part. À traiter comme « pas caché, mais pas mis en
avant », en cohérence avec la façon dont le reste de la documentation
technique du site est déjà géré. Si un jour vous voulez le rendre public
(même en version résumée), on en reparle — pour l'instant, une version
très allégée en existe déjà sur `le-projet.html` (section « Favorable,
stable, dégradé : par rapport à quoi ? »), qui ne révèle rien de ce qui
suit en détail.

Ce document répond à une question simple : **quand une édition affiche
« 45 % / 30 % / 25 % », d'où viennent ces chiffres ?** Il n'y a pas de
formule mathématique cachée qui les recrache automatiquement — la méthode
est un **jugement structuré**, comparable dans l'esprit aux techniques
d'analyse utilisées en prévision géopolitique ou en renseignement
(« structured analytic techniques »), pas à un modèle statistique
entraîné sur des données. Ce document décrit précisément en quoi consiste
ce jugement, pour qu'il reste **cohérent d'une édition à l'autre**, même
si chaque édition est rédigée indépendamment.

---

## 1. Le cadre : pourquoi trois scénarios, pas une prédiction

Une prédiction unique masque l'incertitude réelle d'une situation en
cours. Trois scénarios — toujours dans le même ordre, favorable / stable /
dégradé — obligent à représenter explicitement l'éventail des issues
plausibles plutôt qu'à parier sur une seule. Les trois probabilités
s'additionnent toujours à 100 % : ce ne sont pas trois évaluations
indépendantes, mais un partage d'un même espace de certitude.

**Aucun scénario n'est jamais noté isolément.** La probabilité d'un
scénario n'a de sens que par comparaison aux deux autres — c'est un
jugement relatif (« lequel des trois est le plus solide, compte tenu de
ce qu'on sait aujourd'hui ? »), pas une note absolue attribuée en vase
clos.

## 2. Ce que mesure chaque scénario

Rappel (voir aussi `le-projet.html` pour la version publique) :

- **Favorable** : la tension ou l'incertitude au cœur de la question posée
  ce jour-là se résout plutôt bien.
- **Stable** : ni résolution ni aggravation nette — le statu quo se
  prolonge, avec un coût potentiel même sans rupture visible.
- **Dégradé** : la tension s'aggrave nettement.

Le sens concret de ces trois mots est redéfini **à chaque édition** dans
l'encart « Ce qu'on évalue » (`docs/routine-prompt.md`, étape 3) : une
phrase interrogative en trois branches explicites, une par scénario, qui
ancre la grille dans le sujet du jour plutôt que de rester une généralité
interchangeable. C'est cette phrase, pas les trois mots eux-mêmes, qui fait
le vrai travail de cadrage.

## 3. Le processus, étape par étape

### 3.1 — Vérification factuelle (avant tout jugement de probabilité)

Un jugement de probabilité mal informé ne vaut rien, donc la rigueur
factuelle vient en premier :

- **Recoupement d'au moins deux sources récentes et distinctes** pour
  chaque fait avancé, en particulier sur ce qui évolue vite.
- **Anti-péremption des données chiffrées** : un chiffre daté (palmarès,
  rapport annuel, classement) est un instantané, pas une photo de
  l'instant présent — vérifier explicitement si un développement plus
  récent l'a rendu obsolète avant de le citer comme situation actuelle.
- **Bilans cumulés, pas premier chiffre trouvé** : pour un total qui
  s'additionne au fil d'événements séparés (morts, incidents...),
  rechercher spécifiquement le total le plus large et le plus récent,
  croiser une troisième source en cas de désaccord entre deux chiffres.
- **Vérifier qu'une hypothèse prospective ne s'est pas déjà réalisée** :
  toute formulation du type « pourrait atteindre X d'ici [date] » doit
  être vérifiée — si l'événement a déjà eu lieu, ce n'est plus un
  scénario incertain, c'est un fait acquis, et le texte doit le refléter.

### 3.2 — Construction individuelle de chaque scénario

Pour chaque scénario (favorable, puis stable, puis dégradé) :

- Un **mécanisme concret** : ce qui se passerait réellement, pas une
  ambiance ou un sentiment général.
- Des **indicateurs chiffrés réellement pertinents** (économiques,
  sociaux, sectoriels — seulement ceux qui comptent pour ce sujet précis),
  avec une **fourchette d'évolution en %**, jamais juste une direction
  vague.
- Ces fourchettes sont **calibrées sur le niveau actuel réel de
  l'indicateur** et sur des **précédents comparables réels** — si aucun
  précédent fiable n'existe pour calibrer un chiffre, le dire
  explicitement plutôt que d'inventer un ordre de grandeur non fondé.
- Une **traduction concrète côté France** quand elle existe (prix,
  pouvoir d'achat, emploi...), toujours descriptive, jamais un conseil
  d'action.

### 3.3 — Attribution des probabilités : les facteurs pesés

Il n'y a pas de formule pondérée explicite (« 30 % source A + 20 % source
B... ») — c'est un jugement qualitatif informé par plusieurs axes,
évalués ensemble et comparés entre les trois scénarios :

1. **La dynamique actuelle (momentum)** : la situation est-elle déjà en
   train de se diriger vers l'un des trois scénarios au moment de la
   rédaction, ou tout reste-t-il réellement ouvert ?
2. **Les contraintes et incitatifs de chaque acteur en présence** :
   qu'est-ce que chaque partie a objectivement à gagner ou à perdre dans
   chaque issue ? Un scénario qui suppose qu'un acteur agisse contre son
   intérêt structurel évident est moins probable, sauf élément concret
   qui le justifie.
3. **Les précédents comparables et leur issue réelle** : quand une
   situation similaire s'est déjà produite (même mécanisme, contexte
   proche), comment s'est-elle résolue ? Un scénario qui s'écarte
   fortement du pattern historique observé demande une justification
   plus solide qu'un scénario qui le prolonge.
4. **Le degré de réversibilité de la situation actuelle** : certains
   développements (un accord signé, une loi votée, un seuil technique
   franchi) sont difficiles à défaire, ce qui pèse sur la probabilité des
   scénarios qui supposeraient un retour en arrière.
5. **Les échéances calendaires connues** : une décision institutionnelle
   prévue à date fixe (vote, sommet, deadline contractuelle) contraint
   fortement la fenêtre dans laquelle un scénario peut ou non se
   matérialiser.
6. **Le degré de consensus ou de divergence entre les sources
   consultées** : si les analystes/médias sérieux convergent largement
   vers une lecture de la situation, ça pèse sur l'estimation ; si les
   sources divergent fortement, l'incertitude doit rester élevée et se
   refléter dans des probabilités plus resserrées entre les trois
   scénarios (aucun n'écrase les deux autres).
7. **L'existence de mécanismes de sortie de crise déjà activés ou
   disponibles** (médiation en cours, clause de sauvegarde, précédent de
   compromis récent entre les mêmes acteurs) : leur présence tire vers le
   favorable/stable, leur absence tire vers le dégradé.

### 3.4 — Comparaison finale et cohérence interne

Une fois les trois scénarios rédigés indépendamment, relecture
systématique en les comparant :

- Est-ce que la somme fait bien 100 % ?
- Est-ce que chaque scénario répond sans ambiguïté à **sa** branche de la
  question « Ce qu'on évalue » — pas à une version édulcorée ou décalée ?
- Est-ce que l'écart entre les trois probabilités reflète honnêtement le
  niveau d'incertitude réel du sujet (un sujet très ouvert ne devrait
  jamais afficher un scénario à 80 % sauf raison solide) ?
- Est-ce qu'un chiffre cité dans un scénario contredit un chiffre cité
  ailleurs dans la même édition (contexte, indicateurs, lexique) ?

## 4. Les repères de probabilité (mot-clé associé)

| Plage | Mot-repère | Ce que ça signifie concrètement |
|---|---|---|
| 0–25 % | Peu probable | Possible mais irait à l'encontre de la dynamique actuelle, des incitatifs des acteurs, ou des précédents connus — demande un développement notable pour se réaliser. |
| 26–50 % | Probable | Une issue plausible et documentée, mais qui n'est pas la plus soutenue par les éléments disponibles aujourd'hui. |
| 51–75 % | Assez probable | L'issue la mieux soutenue par la dynamique actuelle et les précédents, sans être jouée d'avance — un développement contraire resterait plausible. |
| 76–100 % | Très probable | Peu de marge réaliste pour une autre issue à court terme, sauf choc externe non anticipé — réservé aux cas où la dynamique est déjà largement engagée. |

Ces plages ne sont **pas des seuils calculés** — elles servent de
garde-fou pour éviter la sur-confiance : un scénario ne devrait quasiment
jamais dépasser 75-80 % sur un sujet encore réellement incertain (sinon,
ce n'est probablement plus un « scénario », c'est déjà un fait établi, et
le sujet ne mérite peut-être pas l'exercice des trois scénarios).

## 5. Garde-fous et biais explicitement évités

- **Pas de biais de récence non vérifié** : un développement qui vient de
  tomber n'est pas automatiquement extrapolé comme tendance de fond —
  vérifier qu'il ne s'agit pas d'un pic isolé avant de lui donner un
  poids disproportionné.
- **Pas de scénario évalué en vase clos** : toujours comparatif aux deux
  autres (voir 3.4).
- **Pas de fausse précision** : les pourcentages sont arrondis à des
  valeurs qui restent lisibles comme des estimations (multiples de 5 en
  général), jamais un chiffre à la décimale près qui suggérerait une
  précision non fondée.
- **Pas de source unique** : un fait ou une tendance qui ne repose que
  sur une seule source, surtout si elle est partisane ou intéressée, ne
  doit pas déterminer à lui seul un scénario.
- **Pas de prise de position déguisée** : la probabilité reflète une
  estimation de ce qui est *susceptible* de se produire, jamais ce que
  l'auteur *souhaiterait* voir se produire. Le style reste factuel même
  dans les scénarios dégradés ou favorables les plus francs.

## 6. Ce que cette méthode n'est pas

Pour être honnête en interne (utile si un jour vous formulez une version
publique) :

- **Ce n'est pas un modèle statistique** entraîné sur des données
  historiques structurées — il n'y a pas de base de données de sujets
  passés notée et calibrée en continu.
- **Ce n'est pas un marché de prédiction** (pas de pool de votants, pas de
  cotes de marché agrégées).
- **Ce n'est pas un sondage** — les probabilités n'interrogent aucun
  panel, elles reflètent une analyse qualitative structurée d'informations
  vérifiées.
- **C'est un jugement d'analyse structuré et reproductible dans sa
  méthode**, pas dans son résultat exact : deux analystes suivant
  scrupuleusement le même processus sur le même sujet, au même moment,
  pourraient arriver à des pourcentages légèrement différents (35/40/25
  vs 30/45/25, par exemple) sans que l'un soit « faux » — la valeur de la
  méthode est de structurer le raisonnement et d'éviter les biais
  grossiers, pas de produire un chiffre unique objectivement vérifiable
  comme le serait une mesure physique.

## 7. Une version publique, si vous choisissez d'en publier une

Une formulation courte et honnête, sans révéler le détail ci-dessus,
pourrait être : *« Scénario s'appuie sur une méthode propriétaire qui
croise recoupement de sources récentes, comparaison avec des précédents
similaires, poids des intérêts et contraintes des acteurs en présence, et
cohérence d'ensemble entre les trois scénarios — jamais évalués
isolément. »* C'est exactement la phrase déjà publiée sur `le-projet.html`
(section « Favorable, stable, dégradé : par rapport à quoi ? ») — elle
donne du sens à la démarche sans exposer la mécanique fine décrite plus
haut.
