# Prompt de la routine « Scénario — Traduction EN »

**Pas encore un trigger dédié séparé** (contrairement à `docs/routine-
pub-prompt.md` ou `docs/routine-hebdo-prompt.md`) — cette étape s'exécute
**à la suite de la routine quotidienne française** (`docs/routine-
prompt.md`), une fois l'édition du jour validée et publiée sur `main`,
jamais avant ni en parallèle. Ce fichier est la copie de référence de cette
étape, créée le 29 août 2026 (première édition traduite :
« Cinéma mondial : peut-il survivre au streaming ? », 2026-08-29). Voir
`docs/strategie-anglais.md` pour le cadrage stratégique complet (pourquoi
une traduction et pas une rédaction indépendante, ce qui est hors scope).

**Étendu le 29 août 2026 aux deux routines auxiliaires** — retour
utilisateur : « les pub il faudrait aussi faire feed-pub-en... et les mise
à jour pareil ». Ce fichier couvre donc trois miroirs anglais distincts,
chacun appelé depuis la routine française correspondante :
1. **Édition quotidienne** (ci-dessous) — appelée depuis `docs/routine-
   prompt.md`, étape 13.
2. **Posts pub** (§ « Traduction des posts pub » en bas de ce fichier) —
   appelée depuis `docs/routine-pub-prompt.md`, étape 4bis.
3. **Mises à jour de suivi** (§ « Traduction des mises à jour de suivi »
   en bas de ce fichier) — appelée depuis `docs/routine-detection-
   prompt.md`, point 4.

**Explicitement hors scope, confirmé le 29 août 2026 : pas de glossaire en
anglais.** Retour utilisateur direct : « on n'a pas pensé au glossaire en
anglais pour l'instant on ne fait pas le glossaire en anglais » — ne pas
traduire `glossaire.html`, ni improviser une traduction ad hoc des termes
du lexique dans les pages traduites. `en/index.html` continue de pointer
son lien « Glossary » vers la page française existante (`../glossaire.
html`), comme documenté dans `docs/strategie-anglais.md`.

**Principe non négociable : traduire, jamais rerédiger.** Cette routine ne
fait aucune recherche, ne choisit aucun nouveau chiffre, ne réévalue aucune
probabilité et n'invente aucun titre de scénario — elle reprend
intégralement le contenu déjà validé de l'édition française du jour
(`index.html`) et le reformule en anglais naturel, phrase par phrase,
section par section. Si un fait semble à vérifier ou à préciser, ce n'est
jamais le rôle de cette étape : le contenu français est déjà la source de
vérité, validée par la routine principale.

**Économie de tokens** : contrairement à `docs/routine-inspection-
prompt.md`, cette étape n'est pas déterministe — elle demande un vrai
jugement de traduction (formulation naturelle, pas de calque mot à mot,
respecter les règles de titres de scénarios déjà en vigueur côté français —
voir `docs/routine-prompt.md`, étape 4). Mais elle reste bornée : aucune
recherche externe, aucun WebFetch, uniquement de la lecture/écriture de
fichiers locaux.

**[AJOUTÉ le 29 août] Garde-fou : mieux vaut sauter l'anglais du jour
qu'en publier une version cassée ou à moitié faite.** Cette étape
compte désormais beaucoup de sous-étapes (traduction complète, cascade
vers les articles cités, badge `archives.html`, bouton de langue +
`hreflang` sur 4 fichiers minimum, image sociale régénérée, item
`feed.xml`) — plus qu'une simple traduction ponctuelle. **Étape 8 fait
exprès un seul commit final** : tant qu'il n'a pas lieu, rien n'est
publié, donc s'arrêter en cours de route sans committer est déjà sûr en
soi, pas seulement un pis-aller. En conséquence :
- Si le budget (temps, tokens) semble insuffisant pour finir
  proprement toutes les étapes 1 à 8 (traduction + cascade éventuelle +
  validations), **s'arrêter sans committer plutôt que de pousser un
  résultat partiel** — jamais un `en/index.html` sans son
  `en/archives/AAAA-MM-JJ.html`, jamais un bouton de langue sans sa
  cible, jamais une balise `hreflang` posée sur un seul des quatre
  fichiers attendus.
- **Cascade (étape 1bis) : plafonnée à 1 édition passée par jour.** Si
  l'édition du jour cite plus d'une édition non encore traduite,
  traduire seulement la première rencontrée dans le corps du texte,
  laisser les autres liens tels quels vers le français pour cette fois
  (elles seront traduites le jour où elles seront citées seules, ou
  directement dans une session dédiée) — et le signaler dans le résumé
  final (étape 9). Ne jamais laisser le volume de cascade dicter un
  travail bâclé sur l'édition du jour elle-même.
- Dans les deux cas, le signaler clairement dans le résumé remonté à
  l'utilisateur (étape 9, ou l'équivalent du jour si l'étape n'a même
  pas pu démarrer) — jamais silencieux sur un jour sans traduction.

---

**La cible du push est toujours `main`, sans exception** — mêmes règles que
`docs/routine-prompt.md` (fetch + rebase si des commits concurrents sont
arrivés entre-temps, jamais de force-push).

**Avant de commencer : vérifier que l'édition française du jour est bien
publiée sur `main`** (`index.html` à jour, commit de la routine principale
déjà poussé). Ne jamais traduire une édition qui n'est pas encore sur
`main` — l'anglais est toujours un second temps, jamais en parallèle du
premier.

## Étape 1 — Créer `en/index.html`

1. Copier `index.html` vers `en/index.html` tel quel (structure, CSS, JS
   inchangés — seul le contenu textuel change).
2. Corriger tous les chemins relatifs devenus faux d'un niveau
   (`en/` est un dossier de premier niveau, comme `index.html` à la
   racine, mais un cran plus profond) : préfixer `../` devant tous les
   liens vers `assets/`, et toutes les pages du premier niveau
   (`archives.html`, `glossaire.html`, `le-projet.html`,
   `newsletter.html`, `contact.html`, `mentions-legales.html`,
   `politique-de-confidentialite.html`), ainsi que les liens internes de
   l'article vers `archives/AAAA-MM-JJ.html`, `suivi/*.html`,
   `hebdo/AAAA-MM-JJ.html`. Ne pas toucher aux URLs absolues
   (`https://...`) ni aux ancres internes (`#scenarios`, `#essentiel`...).
   **Exception : `manifest.webmanifest`** — ne pas pointer vers celui de
   la racine (nom/description en français) mais vers `en/manifest.
   webmanifest` (créé le 29 août, nom/description en anglais, `lang:
   "en"`, `start_url`/`id`: `/en/`) : depuis `en/index.html`, `href=
   "manifest.webmanifest"` (même dossier) ; depuis `en/archives/AAAA-MM-
   JJ.html`, `href="../manifest.webmanifest"` (un cran au-dessus, comme
   pour `en/index.html`).

## Étape 1bis — Traduire aussi les articles référencés [AJOUTÉ le 29 août
2026]

Retour utilisateur : « les liens qui font référence à nos précédents
articles doivent aussi pointer sur la version anglaise si elle existe, du
coup il faudrait générer la version anglaise dans archive des articles
que tu mentionnes dans l'édition du jour ». Règle : **un lien vers une
autre édition (`archives/AAAA-MM-JJ.html`) ne doit jamais rester pointé
vers le français si l'article visé est traduit — et doit être traduit
lui-même s'il ne l'est pas encore et qu'il est cité par l'édition du
jour.**

1. **Repérer tous les liens internes vers `archives/AAAA-MM-JJ.html`**
   dans le corps de `index.html` (pas `suivi/*.html` ni
   `hebdo/AAAA-MM-JJ.html` — ces pages restent hors scope, voir
   `docs/strategie-anglais.md`).
2. **Pour chaque édition citée, vérifier si `en/archives/AAAA-MM-JJ.html`
   existe déjà.** Si oui, passer directement au point 4.
3. **Si elle n'existe pas encore : la traduire d'abord**, en suivant
   exactement les étapes 1 à 8 de ce document appliquées à cette
   édition passée plutôt qu'à l'édition du jour (copier `archives/AAAA-
   MM-JJ.html` vers `en/archives/AAAA-MM-JJ.html`, corriger les chemins
   pour son niveau de profondeur — voir étape 4 plus bas, traduire tout
   le contenu, ajouter le bouton de bascule de langue + `hreflang` sur
   les deux fichiers FR et EN, ajouter l'entrée `sitemap.xml`). **Ne pas
   suivre récursivement les liens internes de cet article traduit vers
   une troisième édition** — un seul niveau de traduction déclenchée par
   citation, pas une chaîne sans fin ; si cet article cité en cite
   lui-même un autre, laisser ce lien tel quel vers le français pour
   cette fois (à traiter, le cas échéant, le jour où cette édition plus
   ancienne est elle-même citée directement par une nouvelle traduction).
   **Plafond : 1 édition passée traduite par cascade et par jour** (voir
   le garde-fou en tête de ce fichier) — si plusieurs éditions non
   traduites sont citées le même jour, ne traduire que la première
   rencontrée dans le corps du texte, laisser les autres liens vers le
   français, et le signaler dans le résumé final (étape 9).
4. **Réécrire le lien dans `en/index.html` (et dans `en/archives/AAAA-
   MM-JJ.html` une fois créé à l'étape 4 ci-dessous) pour qu'il pointe
   vers `en/archives/{date citée}.html`.** Comme les deux fichiers
   vivent dans le même dossier `en/archives/`, le lien entre eux est un
   simple nom de fichier sans préfixe (`{date}.html`) — jamais un chemin
   relatif vers le français. Depuis `en/index.html` (un niveau
   au-dessus), le lien est `archives/{date}.html` (descend dans le
   sous-dossier, pas de `../`).
5. **Mettre à jour aussi tout flux qui cite cette édition** —
   `en/feed-pub.xml` en particulier (catégorie `chiffre`, voir
   `docs/routine-pub-prompt.md`) peut déjà contenir un `<link>` vers la
   version française d'une édition qui vient d'être traduite : le
   remplacer par l'équivalent `en/archives/...` dans ce cas.
6. **[AJOUTÉ le 29 août] Ajouter le badge `EN` sur `archives.html`**
   pour toute édition traduite (celle du jour comme celle(s) traduites
   par cascade à l'étape 3) — jamais de bouton de bascule générique sur
   cette page elle-même (voir `docs/strategie-anglais.md` § « Audit UX
   du parcours anglais » pour le raisonnement complet) :
   ```html
   <a class="entry-lang-badge" href="en/archives/{AAAA-MM-JJ}.html" aria-label="Read this edition in English" title="Read this edition in English">EN</a>
   ```
   À insérer juste après `<a class="entry-title" href="archives/{AAAA-
   MM-JJ}.html">...</a>` de l'entrée correspondante, dans `.entry-main`.
   La classe CSS `.entry-lang-badge` est déjà dans le `<style>` de
   `archives.html` (ajoutée le 29 août) — ne jamais utiliser `.tag` pour
   ce badge, même visuellement proche : le JS de filtre de la page
   indexe `.tag`/`data-tag` sur chaque entrée, un badge sans `data-tag`
   sous cette classe casserait le filtre (tag fantôme « undefined »).
   L'accordéon « Scénarios ▾ » de l'entrée n'est jamais traduit, quel
   que soit l'article — voir la même justification.
7. **[AJOUTÉ le 29 août] Régénérer l'image sociale en anglais** — sinon
   `og:image`/`twitter:image` de la page EN affichent l'image du jour
   avec du texte français incrusté (repéré par l'utilisateur en
   partageant un lien sur X). Ne jamais réutiliser l'image française
   telle quelle.
   ```
   python3 scripts/social/generate_instagram_image.py \
     --data {json temporaire, title/context/scenario[].label traduits} \
     --output en/assets/social/instagram/{AAAA-MM-JJ}.png \
     --template scripts/social/instagram-photo-template-en.html \
     --photo assets/social/topic-images/{AAAA-MM-JJ}.jpg \
     --lang en
   ```
   `title`/`context`/les 3 `label` viennent du JSON, traduits comme le
   reste de l'article — jamais mot à mot si le résultat déborde du
   cadre (l'anglais est souvent plus long que le français à sens égal,
   vérifier le rendu et raccourcir si un label est coupé). `--lang en`
   pilote uniquement les libellés internes au script (Favorable/Stable/
   Degraded, "Our assessment" du badge France Impact) — jamais utiliser
   `--template` sans son suffixe `-en.html` (bandeau « Sujet du jour »/
   tagline resteraient en français, ce ne sont pas des `__PLACEHOLDER__`
   pilotés par le JSON). Utiliser `instagram-template-en.html` (fond
   dégradé uni) plutôt que la variante `-photo` seulement si l'édition
   française d'origine n'utilisait pas `--photo` non plus. Mettre à jour
   `og:image`/`og:image:width`/`og:image:height`/`twitter:image`/le
   `image` du JSON-LD sur `en/index.html` et `en/archives/AAAA-MM-JJ.
   html`, ainsi que l'`<enclosure>`/`<img src>` de `en/feed.xml` (taille
   réelle du nouveau fichier, pas celle de l'image française).
   **`og:image:alt` reste inchangé** (déjà traduit à l'étape 2, décrit la
   photo elle-même, pas le texte incrusté). Si l'édition traduite est
   plus ancienne et utilisait une image générique plutôt qu'une carte
   par article (ex. `assets/social/og-image-v2.png`, sans script de
   génération connu) : ne pas en fabriquer une version anglaise à la
   volée — signaler dans le résumé final, limite connue documentée dans
   `docs/strategie-anglais.md`.

## Étape 2 — Traduire le contenu

Parcourir `en/index.html` section par section (balises `<head>` puis corps
de page) et traduire **tout texte visible ou destiné à l'utilisateur**,
dans cet ordre :

1. **`<head>`** : `<title>`, `<meta name="description">`, tous les
   `<meta property="og:*">` et `<meta name="twitter:*">` (title,
   description, image:alt), `og:locale` → `en_US`, le bloc JSON-LD
   (`headline`, `description`, `inLanguage` → `en-US`).
   - `<link rel="canonical">` → pointe vers l'archive anglaise du jour,
     `https://lesscenarios.fr/en/archives/AAAA-MM-JJ.html` (jamais vers
     `en/index.html` lui-même — même logique que la version française,
     dont le canonical d'`index.html` pointe vers `archives/AAAA-MM-JJ.html`).
   - `og:url` et le `@id` du JSON-LD → `https://lesscenarios.fr/en/`
     (l'équivalent anglais de la home, pas l'archive — même logique que la
     version française, dont `og:url`/`@id` sur `index.html` pointent vers
     `https://lesscenarios.fr/`).
2. **Masthead / nav** : la ligne édition (« Édition du... » →
   « Edition of... »), les labels de nav (Accueil → Home, Glossaire →
   Glossary, Le projet → About, Nous suivre → Follow us, Soutenir →
   Support us, Sujet révisé → Updated topic, Récap de la semaine → Weekly
   recap), tous les `aria-label`/`title` des boutons (notifications,
   impression, partage).
   - **Les liens de ces pages restent vers leurs URLs françaises**
     (`../glossaire.html`, `../le-projet.html`, `../archives.html?tag=
     revise`, `../hebdo/...`) — ces pages n'ont pas encore de version
     anglaise, voir `docs/strategie-anglais.md`. Traduire uniquement le
     libellé affiché, jamais le lien lui-même.
3. **Bandeau d'accueil** (`.intro-banner`) : accroche et texte, `aria-
   label` du bouton de fermeture.
4. **Hero** : eyebrow (jour + registre), `<h1>`, `.pubdate` (texte
   affiché par défaut, même si un script le regénère ensuite — voir point
   7 ci-dessous), légende de la photo (`.article-image-caption`,
   `alt` de l'image), `.question-box` (label + texte), sommaire (`.toc`).
5. **Corps de l'article** : tous les `.dek`, `.list-box` (label, items,
   pied), `.comprendre-box` (label, lead, texte), `.indicator-strip`
   (labels + valeurs, convertir `Md$` → `B`/`$`, virgule décimale
   française → point décimal anglais), `.dc-chart-box` (label, lead,
   `aria-label` du SVG, légende).
6. **Section scénarios** : `.stakes-box`, et pour chacune des 3 cartes —
   `.kind-tag` (Dégradé → Degraded, Favorable et Stable restent
   identiques), `.gauge-word` (Probable → Likely, Peu probable →
   Unlikely), **le titre `<h3>` du scénario** (appliquer la même règle de
   clarté que la version française — voir `docs/routine-prompt.md`, étape
   4 : titre littéral et pragmatique, jamais une image ou une métaphore
   ambiguë, traduire le sens du titre français plutôt que le transposer
   mot à mot si le résultat sonnerait mécanique), les deux paragraphes
   `.why`, `.field-label`/`.field-name`/valeurs des indicateurs, et
   `.france-line` (label « Concrètement en France » → « The France
   angle », texte).
7. **`.essentiel-box`** : label, les 4 paragraphes, `.delta-gauge-word`,
   le paragraphe `.delta-text` (dont le mot coloré `.delta-word`).
8. **Lexique** (`.lexique`) : label de section, titre, les définitions
   (`<dt>`/`<dd>`), lien vers le glossaire (texte traduit, lien conservé
   vers `../glossaire.html`).
9. **Sources** : label de section — **les titres d'articles source
   restent tels quels** (déjà en anglais dans la version française pour
   des sources anglophones, ou dans leur langue d'origine).
10. **Bloc « Nous suivre »** et **footer** : tous les libellés visibles,
    les liens externes (réseaux sociaux, Buy Me a Coffee) restent
    identiques (mêmes comptes, pas de version anglaise séparée).

## Étape 3 — Traduire les chaînes visibles dans le JavaScript

Certaines chaînes affichées à l'utilisateur sont générées par les
`<script>` en bas de page plutôt qu'écrites en dur dans le HTML — à
traduire aussi, sans quoi la page bascule en français au chargement même
après l'étape 2 :

- Le regex qui relit la ligne édition pour en déduire la date affichée
  (`/Édition du\s+(.+?)\s+·/` → `/Edition of\s+(.+?)\s+·/`) et le préfixe
  « Publié le » → « Published ».
- Le texte du temps de lecture (« ~X min de lecture » → « ~X min read »)
  et du compteur de lectures (« Lu X fois » → « Read X times »,
  `toLocaleString("fr-FR")` → `toLocaleString("en-US")`).
- La table des registres du lendemain (`registres`, jours 0-6) et le
  préfixe « 📅 Demain : » → « 📅 Tomorrow: ».
- Le script de partage : la détection de page archive doit chercher
  `/en/archives/` (pas `/archives/`) dans `location.pathname`, et l'URL de
  repli construite doit pointer vers
  `https://lesscenarios.fr/en/archives/AAAA-MM-JJ.html`. Les textes « Lien copié »/« Copier le lien » →
  « Link copied »/« Copy link ».
- Les libellés du graphique en escalier (`Md$` → `$...B`, les deux
  légendes de points « record pré-pandémie » et « (prévision), encore
  loin de... »).
- Tous les messages d'état du bouton de notifications OneSignal
  (Activation…, Notifications activées ✓, Erreur, Refusé, Finalisation de
  l'abonnement…, Erreur d'initialisation).

Les commentaires de code (`//`, `/* */`) peuvent rester en français —
invisibles pour le lecteur, pas de valeur à les traduire systématiquement.

## Étape 4 — Créer `en/archives/AAAA-MM-JJ.html`

**Toute l'arborescence anglaise vit sous `en/`, mêmes noms de dossiers
qu'en français** (retour utilisateur du 29 août : « tout ce qui est
anglais dans le folder en, mais même structure même nom de folder que le
fr, pour juste avoir "en" à ajouter dans l'adresse ») — jamais un dossier
séparé à la racine comme l'ancien `archive-en/` (essai initial, abandonné
le jour même). `en/archives/` est donc **un niveau plus profond que
`en/`**, exactement comme `archives/` l'est par rapport à la racine côté
français.

Copier `en/index.html` (une fois traduit et validé) vers
`en/archives/AAAA-MM-JJ.html`, puis corriger les chemins relatifs pour ce
cran de profondeur supplémentaire (même logique que l'étape 1, point 2,
mais un `../` de plus partout : `../assets/...` → `../../assets/...`,
`../glossaire.html` → `../../glossaire.html`, etc.), à l'exception du lien
« Home » du topnav qui reste à un seul `../` (`../index.html` — depuis
`en/archives/`, `en/index.html` n'est qu'un cran au-dessus, pas deux).
Puis, comme côté français :

1. `canonical`, `og:url` et le `@id` JSON-LD → l'URL de cette archive
   elle-même, `https://lesscenarios.fr/en/archives/AAAA-MM-JJ.html`
   (remplace la version « home » posée à l'étape 2).
2. Le lien « Home » du topnav → `../index.html` (au lieu de `index.html`,
   qui pointait vers lui-même sur la page du jour) — garder
   `aria-current="page"` dessus, même si ce n'est plus littéralement la
   page courante (même choix que la version française).
3. Le script de partage (voir étape 3 ci-dessus) : la détection de page
   archive doit chercher `/en/archives/` dans `location.pathname`
   (cohérent avec l'étape 3, pas `/archive-en/`).

## Étape 4bis — Bouton de bascule de langue + `hreflang` [AJOUTÉ le 29
août 2026]

Retour utilisateur : « il manque des trucs sur l'ux pour bien gérer
français et anglais, français reste le prioritaire et défaut » — deux
liens de bascule ajoutés à chaque édition traduite, jamais un simple lien
vers l'accueil de l'autre langue. **Français reste la langue par défaut du
site** : ce bouton n'existe que pour offrir un accès direct, jamais pour
rediriger automatiquement un visiteur (pas de détection de langue
navigateur, pas de redirection).

1. **Ajouter `.masthead-lang-btn` dans `<div class="masthead-right">`,
   avant le bouton notifications**, sur les **quatre** fichiers de
   l'édition du jour (les deux français, retouchés rétroactivement — ils
   ont été publiés avant que la traduction existe — et les deux anglais,
   déjà en cours de création à cette étape) :
   - `index.html` (racine) → lien vers `en/archives/{AAAA-MM-JJ}.html`,
     libellé `EN`, `aria-label`/`title` = « Read this edition in English ».
   - `archives/{AAAA-MM-JJ}.html` → lien vers
     `../en/archives/{AAAA-MM-JJ}.html`, même libellé/attributs.
   - `en/index.html` → lien vers `../index.html` (l'accueil français),
     libellé `FR`, `aria-label`/`title` = « Lire en français ».
   - `en/archives/{AAAA-MM-JJ}.html` → lien vers
     `../../archives/{AAAA-MM-JJ}.html`, même libellé/attributs.
   La classe CSS `.masthead-lang-btn` est déjà dans le `<style>` des
   quatre fichiers (voir `docs/routine-prompt.md`, section « Ligne
   `.masthead-right` ») — ne jamais la re-déclarer, seulement ajouter le
   lien `<a>` lui-même s'il manque encore. Depuis le 29 août,
   `.masthead-right` contient aussi un séparateur `.masthead-divider` et
   les liens "Sujet révisé"/"Récap de la semaine" (ex-bande
   `.top-updates`, supprimée ce jour-là) : `.masthead-lang-btn` reste le
   tout premier enfant, avant la cloche notifications — ne rien changer
   à l'ordre des éléments qui suivent.
2. **Ajouter les balises `hreflang` dans `<head>`, juste après
   `<link rel="canonical">`**, sur les mêmes quatre fichiers :
   ```html
   <link rel="alternate" hreflang="fr" href="https://lesscenarios.fr/archives/{AAAA-MM-JJ}.html">
   <link rel="alternate" hreflang="en" href="https://lesscenarios.fr/en/archives/{AAAA-MM-JJ}.html">
   <link rel="alternate" hreflang="x-default" href="https://lesscenarios.fr/archives/{AAAA-MM-JJ}.html">
   ```
   Même trio sur les quatre fichiers (`index.html`/`archives/...` côté
   français, `en/index.html`/`en/archives/...` côté anglais) — seul l'ordre
   des deux premières lignes change selon la langue du fichier (celle du
   fichier courant en premier n'a pas d'importance pour le SEO, mais reste
   la convention adoptée le 29 août pour la lisibilité). `x-default`
   pointe toujours vers la version française — **français reste la langue
   par défaut du site**, jamais l'anglaise.
3. **Vérifier l'équilibrage des balises** sur les quatre fichiers après
   modification (même garde-fou qu'à l'étape 7 plus bas), puis valider
   visuellement le masthead des quatre pages (capture Playwright ciblée
   sur `header.masthead` suffit, pas besoin de la page entière).

**Jours sans traduction (routine EN sautée ce jour-là)** : ne jamais
ajouter ce bouton ni ces balises sur les pages françaises du jour — un
lien vers une page anglaise qui n'existe pas casserait la navigation.
Cette étape ne s'exécute que lorsque les étapes 1 à 4 ci-dessus ont
effectivement produit une traduction ce jour-là.

## Étape 5 — Ajouter l'item à `en/feed.xml`

Même structure que `feed.xml` (voir `docs/routine-prompt.md`, étape
technique 8, pour le détail du format 3 blocs), traduite :

```xml
<item>
  <title>{titre anglais}</title>
  <link>https://lesscenarios.fr/en/archives/AAAA-MM-JJ.html</link>
  <guid isPermaLink="false">scenario-en-AAAA-MM-JJ</guid>
  <pubDate>{même date/heure que l'item correspondant de feed.xml}</pubDate>
  <comments>{question-text traduite}</comments>
  <category>🟢 {titre scénario 1}","🔵 {titre scénario 2}","🔴 {titre scénario 3}</category>
  <enclosure url="https://lesscenarios.fr/en/assets/social/instagram/AAAA-MM-JJ.png" length="{taille réelle du fichier EN généré à l'étape 1bis point 7 — jamais celle de l'image française}" type="image/png"/>
  <description><![CDATA[{<img src="https://lesscenarios.fr/en/assets/social/instagram/AAAA-MM-JJ.png" ...> même image, + The question/The facts/The 3 scenarios, CTA traduits}]]></description>
  <source url="https://lesscenarios.fr/en/archives/AAAA-MM-JJ.html">{texte de L'essentiel traduit, mêmes 4 paragraphes}</source>
</item>
```

Ajouter l'item en tête (le plus récent en premier), jamais réordonner les
items existants. **Valider le XML avant tout commit** — même garde-fou que
`docs/routine-pub-prompt.md` (étape 4) : un CDATA mal fermé fait
disparaître silencieusement tout ce qui suit pour un parseur strict.

## Étape 6 — Mettre à jour `sitemap.xml`

Mettre à jour le `<lastmod>` de l'entrée `https://lesscenarios.fr/en/` à
la date du jour, et ajouter une nouvelle entrée pour
`https://lesscenarios.fr/en/archives/AAAA-MM-JJ.html`
(`changefreq: never`, `priority: 0.6` — mêmes valeurs que les entrées
`archives/AAAA-MM-JJ.html`).

## Étape 7 — Valider avant de committer

1. **Vérifier qu'aucun texte visible en français ne subsiste** dans
   `en/index.html` et `en/archives/AAAA-MM-JJ.html` — chercher les
   caractères accentués français (`àâäéèêëïîôöùûüç...`) en dehors des
   commentaires de code, du nom de marque « Scénario » (jamais traduit,
   reste la marque du site dans les deux langues) et des noms propres
   (ex. « Pathé »).
2. **Vérifier l'équilibrage des balises** (`div`, `section`, `article`,
   `header`, `footer`, `nav`, `script`, `style`, `p`, `span`, titres) —
   même nombre d'ouvertures que de fermetures.
3. **Vérification visuelle** : servir le dossier en local
   (`python3 -m http.server`) et prendre une capture Playwright des deux
   pages (`en/index.html`, `en/archives/AAAA-MM-JJ.html`) — utiliser
   `wait_until="domcontentloaded"` plutôt que `networkidle` (les CDN
   externes — OneSignal, Google Fonts, goatcounter — ne sont pas
   joignables depuis l'environnement d'exécution et bloqueraient
   `networkidle` indéfiniment).

## Étape 8 — Commit et push

Un seul commit couvrant `en/index.html`, `en/archives/AAAA-MM-JJ.html`,
`en/feed.xml`, `sitemap.xml`, **et les retouches rétroactives de l'étape
4bis sur `index.html`/`archives/AAAA-MM-JJ.html`** (préfixe `[en]`), après
`git fetch origin main` + rebase si des commits concurrents sont arrivés
entre-temps — mêmes règles que les autres routines de ce projet. Toujours
après le commit de l'édition française du jour, jamais avant, jamais dans
le même commit (même si ce commit-ci modifie aussi les deux fichiers
français, ce sont des ajouts ciblés — bouton + `hreflang` —, jamais une
réédition du contenu déjà publié).

**Si l'étape 1bis a traduit une ou plusieurs éditions passées** (article
cité par l'édition du jour, pas encore traduit) : inclure dans le même
commit `en/archives/{date citée}.html` pour chacune, la retouche
rétroactive de `archives/{date citée}.html` (bouton + `hreflang`), et
toute entrée `en/feed-pub.xml`/`sitemap.xml` mise à jour en conséquence
(étape 1bis, points 4-5). Toujours un seul commit `[en]` pour l'ensemble
de la traduction du jour, articles cités compris — jamais un commit par
article traduit.

## Étape 9 — Résumé final

Toujours terminer par un message court et explicite : édition traduite
(titre + date), fichiers créés/modifiés, et tout écart signalé pendant la
traduction (ex. une expression française sans équivalent direct, un choix
de formulation ambigu tranché à la volée) — pour que l'utilisateur puisse
relire ces points en particulier plutôt que la traduction complète.

---

## Traduction des posts pub

Appelée depuis `docs/routine-pub-prompt.md`, étape 4bis, une fois l'item
français ajouté à `feed-pub.xml`. Même principe non négociable qu'en tête
de ce fichier : traduire les champs déjà rédigés, jamais en composer de
nouveaux.

1. **Traduire les champs texte** de l'entrée utilisée
   (`eyebrow`/`message`/`attribution`/`cta`, et `stat` pour la catégorie
   `chiffre` — le chiffre lui-même ne change jamais, seule son unité si
   nécessaire). Le `message` garde son balisage `**mot**` (mise en
   évidence) exactement aux mêmes endroits sémantiques que la version
   française, pas nécessairement à la même position littérale dans la
   phrase (l'ordre des mots change en anglais).
2. **Gabarit anglais dédié, jamais le gabarit français.** Chaque template
   `scripts/social/pub-template-v{N}-*.html` a un jumeau `-en.html` (ex.
   `pub-template-v5-stat-en.html`) — copie exacte sauf le bandeau bas de
   page « Le futur en 3 scénarios » → « The future in 3 scenarios »,
   seule chaîne du template non passée en paramètre. Si un nouveau
   gabarit `pub-template-vN-*.html` est créé côté français sans jumeau
   `-en.html` : le dupliquer avec cette même unique traduction avant de
   l'utiliser ici, jamais improviser une image sans l'équivalent anglais
   du bandeau.
3. **Régénérer l'image, même photo, gabarit anglais** :
   ```
   python3 scripts/social/generate_pub_image.py \
     --data {json temporaire, champs traduits} \
     --output en/assets/social/pub/{AAAA-MM-JJ}.png \
     --template scripts/social/pub-template-v{N}-*-en.html \
     --photo {exactement la même photo qu'à l'étape 2/3 de la routine française}
   ```
4. **Ajouter l'item à `en/feed-pub.xml`** — même structure que l'item
   français ajouté à `feed-pub.xml` (voir `docs/routine-pub-prompt.md`,
   étape 4, pour le détail complet du format), traduit :
   - `<guid>` = `scenario-pub-en-{id-entrée}-{AAAA-MM-JJ}`.
   - `<link>` : même règle par catégorie que la version française — la
     page cible n'a pour l'instant presque jamais d'équivalent anglais
     (seule exception à ce jour : la catégorie `chiffre`, si jamais elle
     cite l'édition du 29 août ou une édition future traduite, doit
     pointer vers `en/archives/{AAAA-MM-JJ}.html` plutôt que
     `archives/{AAAA-MM-JJ}.html`) — sinon garder le lien français tel
     quel, jamais un lien inventé.
   - `<enclosure>` vers `https://lesscenarios.fr/en/assets/social/pub/
     {AAAA-MM-JJ}.png`, taille réelle du fichier généré à l'étape 3.
   - Le commentaire de crédit photo (`<!-- credit: ... -->`) reste
     identique — même photographe, même photo.
5. **Valider le XML avant de committer** — même garde-fou que
   `docs/routine-pub-prompt.md`, étape 4 (CDATA mal fermé = item suivant
   avalé silencieusement).

## Traduction des mises à jour de suivi

Appelée depuis `docs/routine-detection-prompt.md`, point 4, une fois
l'item français ajouté à `feed-suivi.xml`. Même principe non négociable :
traduire le topic/la conclusion/le paragraphe de contexte déjà rédigés,
jamais réévaluer les scénarios ou reformuler le fond.

1. **Traduire** `topic` (titre du sujet suivi) et `conclusion` (la phrase
   qui démarre par le fait concret, jamais par l'étiquette de catégorie
   brute ni le titre du scénario seul — même règle que la version
   française, voir `docs/routine-detection-prompt.md` point 4) — et, pour
   `en/feed-suivi.xml`, le paragraphe de contexte complet de la
   `<description>`.
2. **Gabarit anglais dédié** : `scripts/social/suivi-template-en.html`,
   jumeau de `suivi-template.html` avec deux chaînes traduites en dur
   (bandeau bas de page identique aux gabarits pub, et le tag « 🔄 Suivi
   mis à jour » → « 🔄 Update »).
3. **Régénérer l'image, même photo source, gabarit anglais** :
   ```
   python3 scripts/social/generate_suivi_image.py \
     --data {topic+conclusion traduits} \
     --output en/assets/social/suivi/{sujet}-v{N}.png \
     --template scripts/social/suivi-template-en.html \
     --photo assets/social/topic-images/suivi-{sujet}.jpg
   ```
   Si la routine française a omis `<enclosure>` faute de photo source
   (voir `docs/routine-detection-prompt.md` point 52) : omettre aussi
   l'image et l'`<enclosure>` côté anglais, jamais improviser une autre
   photo.
4. **Ajouter l'item à `en/feed-suivi.xml`** — même structure que l'item
   français, traduite :
   - `<guid>` = `scenario-suivi-en-{sujet}-v{N}`.
   - `<link>` : reste vers la page `suivi/{sujet}.html` française (ancre
     `#version-content-v{N}` incluse) — ces pages ne sont pas traduites,
     voir `docs/strategie-anglais.md`. Un lecteur anglophone qui clique
     retombe sur du français, limite connue et acceptée du MVP.
   - `<enclosure>` vers `https://lesscenarios.fr/en/assets/social/suivi/
     {sujet}-v{N}.png` (si générée à l'étape 3).
5. **Valider le XML avant de committer**, même garde-fou qu'ailleurs dans
   ce fichier.
