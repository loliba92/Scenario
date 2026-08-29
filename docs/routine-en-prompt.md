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
   liens vers `assets/`, `manifest.webmanifest`, et toutes les pages du
   premier niveau (`archives.html`, `glossaire.html`, `le-projet.html`,
   `newsletter.html`, `contact.html`, `mentions-legales.html`,
   `politique-de-confidentialite.html`), ainsi que les liens internes de
   l'article vers `archives/AAAA-MM-JJ.html`, `suivi/*.html`,
   `hebdo/AAAA-MM-JJ.html`. Ne pas toucher aux URLs absolues
   (`https://...`) ni aux ancres internes (`#scenarios`, `#essentiel`...).

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
  <enclosure url="https://lesscenarios.fr/assets/social/instagram/AAAA-MM-JJ.png" length="{même taille que l'item FR}" type="image/png"/>
  <description><![CDATA[{image + La question posée/The question + Les faits/The facts + Les 3 scénarios/The 3 scenarios, CTA traduits}]]></description>
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
`en/feed.xml`, `sitemap.xml` (préfixe `[en]`), après `git fetch origin
main` + rebase si des commits concurrents sont arrivés entre-temps —
mêmes règles que les autres routines de ce projet. Toujours après le
commit de l'édition française du jour, jamais avant, jamais dans le même
commit.

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
