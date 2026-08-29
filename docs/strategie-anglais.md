# Scénario en version anglaise — avis et stratégie

Note de cadrage rédigée en réponse à la question : « faut-il une version
anglaise de Scénario, et si oui, avec quelle stratégie ? » — motivée par
l'hypothèse (retour utilisateur, 29 août) qu'une version anglaise pourrait
multiplier le lectorat par 10.

## Réponse courte

Oui, mais en MVP volontairement restreint : **traduction FR→EN de l'édition
du jour uniquement**, pas une rédaction indépendante en anglais. Pas de
nouvelle recherche, pas de nouveaux scénarios, pas de nouvelle évaluation
des probabilités — l'anglais reprend exactement le contenu déjà tranché en
français (chiffres, probabilités, titres de scénarios, France Impact),
uniquement reformulé dans une autre langue. Ce choix minimise la charge
éditoriale ajoutée (pas de second travail de recherche/rédaction quotidien)
tout en testant l'hypothèse d'audience avant d'investir dans un pipeline
éditorial anglais autonome.

## Décisions actées (29 août 2026)

- **Mécanisme** : traduction, pas duplication du travail éditorial. La
  version anglaise n'existe que parce que la version française existe déjà
  — elle est produite après elle, à partir d'elle, jamais en parallèle.
- **Arborescence — revue le 29 août, retour utilisateur** (« j'aurais mis
  plutôt dans le folder en, plus facile à s'y retrouver [...] tout ce qui
  est anglais dans le folder en mais même structure même nom de folder que
  le fr, pour juste avoir "en" à ajouter dans l'adresse ») : tout le
  contenu anglais vit **sous `en/`**, avec exactement les mêmes noms de
  dossiers que côté français — `en/index.html` (édition du jour, miroir de
  `index.html`) et `en/archives/AAAA-MM-JJ.html` (archive, miroir de
  `archives/AAAA-MM-JJ.html`). L'adresse d'une page anglaise est donc
  toujours celle de son équivalent français avec `en/` ajouté juste après
  le domaine (ex. `lesscenarios.fr/archives/2026-08-29.html` →
  `lesscenarios.fr/en/archives/2026-08-29.html`), jamais un nom de dossier
  différent (l'ancien `archive-en/` à la racine, essai initial du 29 août,
  a été abandonné pour cette raison). Conséquence sur les chemins relatifs
  : `en/archives/` est un niveau **plus profond** que `en/` (comme
  `archives/` l'est par rapport à la racine côté français) — un fichier
  dans `en/archives/` remonte donc de deux crans (`../../assets/...`,
  `../../glossaire.html`...) là où `en/index.html` n'en remonte qu'un
  (`../assets/...`), exactement la même règle de profondeur que
  `archives/AAAA-MM-JJ.html` vs `index.html` côté français.
- **Flux RSS dédié** : `en/feed.xml`, même structure que `feed.xml`
  (channel + un `<item>` par édition traduite), `<language>en</language>`,
  liens pointant vers `en/archives/`. Flux séparé plutôt qu\'un `<language>`
  mixte dans `feed.xml` — un lecteur abonné au flux anglais ne doit jamais
  recevoir un item en français, et inversement.
- **`sitemap.xml`** : `en/` référencé comme page vivante
  (`changefreq: daily`, priorité 0.9 — juste sous la home FR), chaque
  `en/archives/AAAA-MM-JJ.html` en `changefreq: never` comme son équivalent
  français.
- **Pages statiques non traduites pour l'instant** (glossaire, le-projet,
  archives.html, newsletter, contact, mentions légales...) : tous les liens
  de nav secondaires depuis `en/index.html` (Glossary, About, Newsletter,
  Contact, Updated topic, Weekly recap, mentions légales/politique de
  confidentialité) pointent vers leurs pages françaises existantes. Un
  lecteur anglophone qui clique dessus retombe sur du français — limite
  connue et acceptée du MVP, pas un bug. Prochaine itération si l'audience
  anglaise confirme l'hypothèse : traduire au moins `le-projet.html` et
  `glossaire.html`, les deux pages qui expliquent ce qu'est le site.
- **Image sociale non retraitée** : `en/index.html` réutilise l'image
  Instagram déjà générée pour l'édition française du jour
  (`assets/social/instagram/AAAA-MM-JJ.png`), qui peut porter du texte en
  français si le visuel en contient. Acceptable pour un MVP texte — à
  revoir si un jour une variante anglaise de la chaîne de génération
  d'images sociales est envisagée (hors scope actuel).
- **`localStorage` du bandeau d'accueil partagé entre FR et EN.** La clé
  `scenario_intro_seen` (voir `docs/routine-prompt.md`) n'est pas dupliquée
  par langue : un lecteur qui a déjà vu le bandeau en français ne le
  reverra pas en anglais s'il visite `en/` depuis le même navigateur, et
  réciproquement. Comportement jugé acceptable — les deux publics ont peu
  de chances de se recouper, et dupliquer la clé aurait ajouté de la
  complexité pour un cas limite.
- **Canonical / Open Graph / JSON-LD** : `en/index.html` pointe vers
  `en/archives/AAAA-MM-JJ.html` (canonical) et `https://lesscenarios.fr/en/`
  (`og:url`, `@id`), exactement le même schéma que la version française
  (`index.html` → `archives/AAAA-MM-JJ.html` / `https://lesscenarios.fr/`).
  `og:locale`/`inLanguage` passés à `en_US`/`en-US`.

## Ce qui n'est PAS fait à ce stade (hors scope du MVP)

- Pas de traduction rétroactive des éditions passées — seule l'édition du
  jour de bascule (29 août 2026) a été traduite pour valider le pipeline.
- **Pas de glossaire en anglais — confirmé explicitement par l'utilisateur
  le 29 août** (« on n'a pas pensé au glossaire en anglais pour l'instant
  on ne fait pas le glossaire en anglais »). `glossaire.html` n'est pas
  traduit ; le lien « Glossary » de `en/index.html` continue de pointer
  vers la page française. Ne pas improviser de traduction ad hoc des
  termes du lexique ailleurs sur le site anglais.
- Pas de compte Telegram/X/Instagram anglophone dédié, pas de diffusion
  Make.com vers des canaux anglais — la diffusion reste à définir une fois
  le format validé (voir « Prochaine étape »).
- Pas de traduction des pages `suivi/*.html` elles-mêmes, `hebdo/`,
  `glossaire.html`, `le-projet.html` — seules les **annonces** de mise à
  jour (`en/feed-suivi.xml`) sont traduites depuis le 29 août, pas les
  pages de suivi vers lesquelles elles renvoient (voir section suivante).
  **`hebdo/` (récap de la semaine) — question posée et tranchée le 29
  août** : reste en français pour l'instant, décision explicite (pas un
  oubli). Le bouton « Weekly recap » sur les pages EN continue de pointer
  vers le récap français. Deux raisons : (1) ce n'est pas couvert par la
  règle de cascade des articles cités (§ « Extension le même jour »
  ci-dessus, qui ne porte que sur `archives/AAAA-MM-JJ.html`) — l'étendre
  serait un élargissement de scope, pas une application de la règle déjà
  actée ; (2) c'est un objet **récurrent** (chaque semaine), pas un
  article ponctuel à traduire une fois — l'engagement de charge éditoriale
  est d'une autre nature que les 3 articles déjà traduits. À revoir, comme
  le reste, une fois un vrai signal de trafic sur `en/`.
  **Suite le même jour** : retour utilisateur, veut qu'on le fasse « si tu
  le fais en 5 minutes tu fais now » — évalué et jugé pas assez rapide
  pour être improvisé sans casser le rythme du reste (voir le ticket
  dédié dans `docs/BACKLOG.md` pour le scope détaillé et l'estimation).
  Passé en ticket backlog structuré plutôt que fait à la volée.
- Pas de version anglaise du compte OneSignal (le bouton de notification
  reste branché sur le même `appId`, donc sur la même liste d'abonnés que
  la version française).

## Extension du 29 août : posts pub et mises à jour de suivi

Suite directe du MVP ci-dessus, même jour, retour utilisateur : « les pub
il faudrait aussi faire feed-pub-en avec la même image mais traduit en
anglais [...] et les mise à jour pareil je pense avec un feed adapté en
anglais ». Même principe que l'édition quotidienne (traduction, jamais
rédaction indépendante) étendu aux deux routines auxiliaires :

- **`en/feed-pub.xml`** — miroir anglais de `feed-pub.xml`. Chaque post
  (manifeste/citation/question/futur/chiffre) est traduit, et son image
  régénérée avec **la même photo** que la version française mais un
  gabarit anglais dédié (`scripts/social/pub-template-v{N}-*-en.html`,
  simple copie du gabarit français avec le bandeau bas de page traduit —
  aucune autre différence). Images stockées dans
  `en/assets/social/pub/`. Procédure : `docs/routine-en-prompt.md` §
  « Traduction des posts pub ».
- **`en/feed-suivi.xml`** — miroir anglais de `feed-suivi.xml` (annonces
  de mise à jour, pas les pages `suivi/*.html` elles-mêmes — voir
  ci-dessus). Même logique : image régénérée avec la même photo source et
  un gabarit anglais dédié (`scripts/social/suivi-template-en.html`),
  stockée dans `en/assets/social/suivi/`. Le lien de l'item continue de
  pointer vers la page de suivi française (non traduite) — limite connue,
  cohérente avec le reste du MVP.
- **Première paire d'items traduits** (29 août, validation du mécanisme) :
  le post « chiffre » du jour (quota chinois de films, `feed-pub.xml`) et
  la mise à jour Arabie saoudite/sport V2 (`feed-suivi.xml`).

**Réarborescence sous `en/`, même jour (voir « Arborescence » plus haut).**
Ces deux flux et leurs images ont été créés une première fois à la racine
(`feed-pub-en.xml`/`feed-suivi-en.xml`, `assets/social/pub-en/`/
`assets/social/suivi-en/`), puis déplacés le jour même sous `en/`
(`en/feed-pub.xml`/`en/feed-suivi.xml`, `en/assets/social/pub/`/
`en/assets/social/suivi/`) pour rester cohérents avec la règle « tout
l'anglais sous `en/`, mêmes noms de dossiers que le français ». Toute
référence à l'ancien emplacement dans l'historique de ce dépôt est
obsolète.

## Routine de production — première version (29 août)

Pas encore une routine automatisée dédiée exécutée par un cron séparé —
documentée en détail dans `docs/routine-en-prompt.md`, qui décrit l'étape
de traduction ajoutée à la suite de la routine quotidienne française
existante (`docs/routine-prompt.md`). Le principe reste : traduire, jamais
rerédiger indépendamment ; jamais publier l'anglais avant que le français
soit validé et publié.

## UX de bascule entre langues — ajouté le 29 août 2026

Retour utilisateur : « il manque des trucs sur l'ux pour bien gérer
français et anglais, français reste le prioritaire et défaut ». Première
brique posée le jour même : un bouton `EN`/`FR` dans le masthead
(`.masthead-lang-btn`, voir `docs/routine-en-prompt.md` § « Étape 4bis »)
sur les quatre pages de l'édition traduite du jour, plus des balises
`hreflang` (`fr`/`en`/`x-default` → toujours la version française) dans
le `<head>` des quatre mêmes pages. **Français reste explicitement la
langue par défaut** : pas de détection de langue navigateur, pas de
redirection automatique — le bouton offre un accès direct, jamais un
choix imposé.

**Extension le même jour : traduction en cascade des articles cités.**
Retour utilisateur : « les liens qui font référence à nos précédents
articles doivent aussi pointer sur la version anglaise si elle existe, du
coup il faudrait générer la version anglaise dans archive des articles
que tu mentionnes dans l'édition du jour ». Règle actée : un lien de
l'édition du jour vers une édition passée (`archives/AAAA-MM-JJ.html`)
pointe désormais toujours vers l'équivalent `en/archives/AAAA-MM-JJ.html`
— traduit à la volée s'il ne l'était pas encore, jamais laissé pointer
vers le français par défaut. Un seul niveau de cascade (les liens internes
de l'article ainsi traduit vers une *troisième* édition restent en
français pour cette fois, voir `docs/routine-en-prompt.md` § « Étape
1bis »). Deux éditions passées traduites ce jour-là pour valider le
mécanisme (toutes deux citées par l'édition du 29 août) :
- `archives/2026-08-08.html` (« Le cinéma reprend des couleurs » → « French
  Cinema Bounces Back ») — gabarit plus ancien (avant le masthead moderne
  du 21 août), traduit et retrofité avec le bouton de langue en CSS
  minimal ad hoc plutôt qu'en rétrofitant tout le masthead.
- `archives/2026-08-22.html` (« Hollywood décroche en Chine » → « Hollywood
  Is Losing China »).

**Question ouverte, posée par l'utilisateur le 29 août, pas encore
tranchée** : traduire aussi `le-projet.html` et les pages légales
(`mentions-legales.html`, `politique-de-confidentialite.html`) en
anglais, avec un bouton de bascule FR/EN dessus. Pas commencé — deux
raisons de ne pas se lancer sans un go explicite :
- **Sensibilité RGPD/juridique** des pages légales, déjà relevée dans une
  discussion antérieure sur le sujet (voir `docs/BACKLOG.md`, ticket
  anglais du 7 août archivé) : une traduction automatique de ce contenu
  précis n'est pas un simple exercice de style, une imprécision peut avoir
  une vraie conséquence juridique — mérite une relecture dédiée, pas le
  même traitement que le contenu éditorial.
- **`glossaire.html` reste explicitement hors scope** (voir plus haut) —
  `le-projet.html` cite et s'appuie sur des termes du glossaire par
  endroits ; le traduire sans le glossaire peut laisser des renvois
  bancals à vérifier au cas par cas.
Si l'utilisateur confirme vouloir avancer là-dessus : traiter dans une
session dédiée, `le-projet.html` en premier (page la plus lue, explique le
site), les deux pages légales ensuite avec une relecture spécifique,
jamais les trois en un seul passage automatique.

## Prochaine étape (pas encore commencée)

- Mesurer l'audience réelle sur `en/` et `en/feed.xml` sur plusieurs
  semaines avant d'investir davantage (traduire les pages statiques,
  ouvrir des canaux sociaux dédiés).
- Si l'hypothèse se confirme : traduire `le-projet.html` en priorité
  (page qui explique le site à un nouveau lecteur) — voir la question
  ouverte juste au-dessus pour les pages légales, et le glossaire qui
  reste hors scope. Envisager des comptes sociaux anglophones dédiés
  seulement après.
- Revoir la question de l'image sociale (texte en dur en français) si la
  diffusion sociale anglophone démarre.

## Stratégie réseaux sociaux — analyse du 29 août 2026

Retour utilisateur : « il faut réfléchir à la stratégie anglaise sur les
réseaux sociaux, dois-je créer un nouveau compte, fais la liste des
réseaux où on est et analyse chacun ». État des lieux (tous les comptes
actuels sont mono-langue, français) :

| Réseau | Constat | Recommandation |
|---|---|---|
| Telegram (@scenario_fr) | Le nom du canal signale « FR », pas de segmentation par langue possible dans un même canal | Nouveau canal dédié **seulement si** `en/feed.xml` montre une vraie traction — mélanger casserait l'expérience des abonnés FR actuels |
| X (@scenario_fr) | Portée la plus internationale des 6 réseaux, tolère bien le bilingue sur un même compte | **Tester sur le compte existant d'abord** — poster le lien EN de temps en temps, coût quasi nul, premier signal d'engagement avant tout nouveau handle |
| Bluesky | Petite audience mais historiquement plus anglophone | Même logique que X, tester sur le compte existant |
| LinkedIn (page entreprise) | Audience pro multilingue, posts plus unitaires qu'un flux identitaire | Tester sur la page existante |
| Facebook | Audience proche des abonnés FR existants, pas de stratégie payante ciblée EN | Priorité basse |
| Instagram (@scenarios.actu) | **Le plus coûteux à adapter** : le texte des visuels (pub/suivi) est incrusté dans l'image, pas un sous-titre séparé — la brique technique existe déjà (gabarits `-en.html`, voir extension du 29 août) mais pas branchée à un compte dédié | À revoir seulement après validation de la demande |
| Newsletter (Buttondown) | Une seule liste FR, segmenter coûte une Automation supplémentaire | À traiter dans la même fenêtre que la migration OneSignal (standby jusqu'à avril 2027, voir `docs/BACKLOG.md`) |
| Push OneSignal | ⚠️ **Point découvert en répondant à cette question** : le bouton notifications sur `en/index.html` utilise le même `appId`/segment que le site français — un lecteur anglophone abonné depuis `en/` reçoit des notifications **en français**. Angle mort du MVP, pas un choix voulu. | Documenté ici ; vraie solution = segments/tags OneSignal par langue, chantier séparé, pas commencé |

**Recommandation d'ensemble : ne créer aucun nouveau compte pour
l'instant.** La chaîne déjà en place (`en/feed.xml` → Make.com, une fois
branché) suffit à mesurer une vraie demande sans coût de gestion
supplémentaire. Les deux gestes à coût quasi nul et utiles dès
maintenant : tester des posts EN ponctuels sur X et Bluesky depuis les
comptes existants, et traiter le trou OneSignal ci-dessus comme une
limite documentée. Tout le reste (canal Telegram dédié, compte Instagram
EN, liste newsletter séparée) attend un vrai signal de trafic sur `en/`.

## À éviter

- Ne jamais laisser la version anglaise dériver du contenu français validé
  (nouveaux chiffres, nouvelle probabilité, nouvelle formulation de
  scénario) — elle doit rester une traduction fidèle, jamais une deuxième
  rédaction éditoriale indépendante avec le risque de décorrélation que ça
  implique.
- Ne jamais publier l'édition anglaise avant l'édition française
  correspondante — l'anglais est un dérivé, pas une source.
- Ne pas dupliquer l'effort de recherche ou de relecture éditoriale : la
  vérification de fond (chiffres, sources) est déjà faite côté français,
  la traduction ne doit vérifier que la fidélité du sens, pas repartir de
  zéro.
