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

## Prochaine étape (pas encore commencée)

- Mesurer l'audience réelle sur `en/` et `en/feed.xml` sur plusieurs
  semaines avant d'investir davantage (traduire les pages statiques,
  ouvrir des canaux sociaux dédiés).
- Si l'hypothèse se confirme : traduire `le-projet.html` et
  `glossaire.html` en priorité (ce sont les deux pages qui expliquent le
  site à un nouveau lecteur), puis seulement ensuite envisager des comptes
  sociaux anglophones dédiés.
- Revoir la question de l'image sociale (texte en dur en français) si la
  diffusion sociale anglophone démarre.

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
