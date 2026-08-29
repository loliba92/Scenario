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
     `https://lesscenarios.fr/archive-en/AAAA-MM-JJ.html` (jamais vers
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
  `/archive-en/` (pas `/archives/`) dans `location.pathname`, et l'URL de
  repli construite doit pointer vers `https://lesscenarios.fr/archive-
  en/AAAA-MM-JJ.html`. Les textes « Lien copié »/« Copier le lien » →
  « Link copied »/« Copy link ».
- Les libellés du graphique en escalier (`Md$` → `$...B`, les deux
  légendes de points « record pré-pandémie » et « (prévision), encore
  loin de... »).
- Tous les messages d'état du bouton de notifications OneSignal
  (Activation…, Notifications activées ✓, Erreur, Refusé, Finalisation de
  l'abonnement…, Erreur d'initialisation).

Les commentaires de code (`//`, `/* */`) peuvent rester en français —
invisibles pour le lecteur, pas de valeur à les traduire systématiquement.

## Étape 4 — Créer `archive-en/AAAA-MM-JJ.html`

Copier `en/index.html` (une fois traduit et validé) vers
`archive-en/AAAA-MM-JJ.html`. `en/` et `archive-en/` sont tous deux des
dossiers de premier niveau (même profondeur) : **aucun chemin relatif ne
change** entre les deux fichiers, à trois exceptions près (même logique
que `archives/AAAA-MM-JJ.html` par rapport à `index.html` côté français) :

1. `canonical`, `og:url` et le `@id` JSON-LD → l'URL de cette archive
   elle-même, `https://lesscenarios.fr/archive-en/AAAA-MM-JJ.html`
   (remplace la version « home » posée à l'étape 2).
2. Le lien « Home » du topnav → `../en/index.html` (au lieu de
   `index.html`, qui pointait vers lui-même sur la page du jour) — garder
   `aria-current="page"` dessus, même si ce n'est plus littéralement la
   page courante (même choix que la version française).

## Étape 5 — Ajouter l'item à `feed-en.xml`

Même structure que `feed.xml` (voir `docs/routine-prompt.md`, étape
technique 8, pour le détail du format 3 blocs), traduite :

```xml
<item>
  <title>{titre anglais}</title>
  <link>https://lesscenarios.fr/archive-en/AAAA-MM-JJ.html</link>
  <guid isPermaLink="false">scenario-en-AAAA-MM-JJ</guid>
  <pubDate>{même date/heure que l'item correspondant de feed.xml}</pubDate>
  <comments>{question-text traduite}</comments>
  <category>🟢 {titre scénario 1}","🔵 {titre scénario 2}","🔴 {titre scénario 3}</category>
  <enclosure url="https://lesscenarios.fr/assets/social/instagram/AAAA-MM-JJ.png" length="{même taille que l'item FR}" type="image/png"/>
  <description><![CDATA[{image + La question posée/The question + Les faits/The facts + Les 3 scénarios/The 3 scenarios, CTA traduits}]]></description>
  <source url="https://lesscenarios.fr/archive-en/AAAA-MM-JJ.html">{texte de L'essentiel traduit, mêmes 4 paragraphes}</source>
</item>
```

Ajouter l'item en tête (le plus récent en premier), jamais réordonner les
items existants. **Valider le XML avant tout commit** — même garde-fou que
`docs/routine-pub-prompt.md` (étape 4) : un CDATA mal fermé fait
disparaître silencieusement tout ce qui suit pour un parseur strict.

## Étape 6 — Mettre à jour `sitemap.xml`

Mettre à jour le `<lastmod>` de l'entrée `https://lesscenarios.fr/en/` à
la date du jour, et ajouter une nouvelle entrée pour
`https://lesscenarios.fr/archive-en/AAAA-MM-JJ.html`
(`changefreq: never`, `priority: 0.6` — mêmes valeurs que les entrées
`archives/AAAA-MM-JJ.html`).

## Étape 7 — Valider avant de committer

1. **Vérifier qu'aucun texte visible en français ne subsiste** dans
   `en/index.html` et `archive-en/AAAA-MM-JJ.html` — chercher les
   caractères accentués français (`àâäéèêëïîôöùûüç...`) en dehors des
   commentaires de code, du nom de marque « Scénario » (jamais traduit,
   reste la marque du site dans les deux langues) et des noms propres
   (ex. « Pathé »).
2. **Vérifier l'équilibrage des balises** (`div`, `section`, `article`,
   `header`, `footer`, `nav`, `script`, `style`, `p`, `span`, titres) —
   même nombre d'ouvertures que de fermetures.
3. **Vérification visuelle** : servir le dossier en local
   (`python3 -m http.server`) et prendre une capture Playwright des deux
   pages (`en/index.html`, `archive-en/AAAA-MM-JJ.html`) — utiliser
   `wait_until="domcontentloaded"` plutôt que `networkidle` (les CDN
   externes — OneSignal, Google Fonts, goatcounter — ne sont pas
   joignables depuis l'environnement d'exécution et bloqueraient
   `networkidle` indéfiniment).

## Étape 8 — Commit et push

Un seul commit couvrant `en/index.html`, `archive-en/AAAA-MM-JJ.html`,
`feed-en.xml`, `sitemap.xml` (préfixe `[en]`), après `git fetch origin
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
