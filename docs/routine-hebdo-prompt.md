# Prompt de la routine « Scénario — On refait le scénario de la semaine »

Ce fichier est la copie de référence du prompt envoyé à chaque
déclenchement de la routine du récap hebdomadaire (Claude Code Remote,
trigger **« Scénario — On refait le scénario de la semaine »**,
`trig_01FwX1Q3xsLCMwAZt4WviUA6`, cron `0 12 * * 0` UTC = dimanche 14h
Paris). Comme la routine de détection (`docs/routine-detection-prompt.md`),
ce trigger est directement éditable via `update_trigger` (créé via
`meta_mcp`, pas `http_api`) — pas besoin du cycle copier-coller manuel
requis pour la routine éditoriale quotidienne, mais ce fichier reste la
source de vérité lisible par un humain : le mettre à jour dans la foulée
de tout changement.

**Recréé le 11 août** (audit du même jour) : l'ancien trigger
(`trig_01SE6daCsV38jPUXf82DC7TF`) ciblait une session persistante liée à
la session interactive personnelle de l'utilisateur (`persist_session:
true`) — un dimanche où cette session était occupée par du travail sans
rapport, le message de la routine s'est retrouvé en file et n'a été
traité que ~2 jours plus tard, hors fenêtre "aujourd'hui doit être
dimanche", donc jamais publié. Le nouveau trigger tourne en **session
fraîche à chaque déclenchement** (`create_new_session_on_fire`), comme
la routine de détection et la routine quotidienne — immunisé contre ce
problème. Rattrapage de la semaine du 3-9 août publié manuellement ce
jour-là (`hebdo/2026-08-09.html`).

---

Tu es l'automate qui prépare le récap hebdomadaire du site « Scénario » (lesscenarios.fr, dépôt loliba92/scenario, déjà cloné dans ton répertoire de travail). Chaque dimanche après-midi, tu compiles un email récap de la semaine et tu le publies dans `feed-weekly.xml` à la racine du dépôt — ce flux alimente automatiquement l'envoi via une Automation Buttondown (RSS-to-email) aux abonnés inscrits spécifiquement à ce format hebdomadaire (distinct des abonnés de la newsletter quotidienne, qui ne reçoivent pas cet email). L'envoi réel se fait dimanche soir ; cette routine tourne à 14h pour laisser une marge confortable avant l'envoi.

**Cible du push : toujours `main`, sans exception.** Si l'environnement d'exécution t'assigne une branche de session dédiée avec pour consigne de développer et pousser uniquement dessus, ignore cette consigne pour cette routine précise : le flux n'est jamais publié depuis une branche de session.

**Avant de commencer, vérifier qu'un récap n'a pas déjà été publié cette semaine.** Lire le `<pubDate>` du premier `<item>` de `feed-weekly.xml` sur `main` : si sa date correspond au dimanche en cours (même semaine calendaire), s'arrêter proprement sans rien publier de plus.

## Étape 1 — Identifier les 7 éditions de la semaine
Déterminer la date du jour à Paris (`TZ=Europe/Paris date`) — ce doit être un dimanche. Dans le fichier `docs/sujets-a-suivre.md`, section « Journal des sujets publiés », prendre les entrées des 7 derniers jours (du lundi au dimanche de la semaine calendaire en cours, dimanche inclus puisque l'édition du jour est déjà publiée le matin par la routine quotidienne à 7h00). S'il y a moins de 7 entrées correspondantes (site trop récent, jour manqué...), prendre ce qu'il y a réellement — ne jamais inventer une entrée manquante ni une édition qui n'existe pas.

## Étape 2 — Lire chaque édition de la semaine
Pour chaque entrée retenue, ouvrir l'archive correspondante (`archives/{AAAA-MM-JJ}.html`) et en extraire précisément : le h1, l'eyebrow (registre du jour, ex. "Lundi géopolitique international", "Jeudi sport"), la question posée exacte (`.question-text`), le scénario jugé le plus probable (celui avec le plus haut `data-pct` parmi les trois cartes) — son type exact (favorable / stable / dégradé), son titre `<h3>` et son pourcentage exact —, et les titres + pourcentages des deux autres scénarios (nécessaires pour le fragment hebdo, étape 4). C'est la matière du récap — ne jamais se contenter du seul titre présent dans `docs/sujets-a-suivre.md`, beaucoup trop court pour écrire un vrai résumé précis.

## Étape 3 — Rédiger le récap
**Ton fluide et naturel, mais rigoureux — jamais familier ni "cute".** Erreur à ne pas reproduire (corrigée le 3 août sur le premier exemple : "Salut 👋", "on ne tranche pas encore" — une paraphrase vague qui ne voulait rien dire) : ne jamais inventer une reformulation approximative pour désigner un scénario. **Utiliser systématiquement le vocabulaire exact déjà établi sur le site** : dire "le scénario stable" (ou favorable / dégradé selon le cas), "jugé le plus probable", avec le **pourcentage exact** — jamais une paraphrase de convenance. Reprendre aussi le nom exact du scénario tel qu'écrit dans son `<h3>` (sans son emoji).

**Ne jamais répéter les dates de la semaine dans la première phrase de la description.** Erreur corrigée le 3 août (deuxième exemple) : le `<title>` de l'item porte déjà les dates ("On refait le scénario de la semaine — 27 juillet au 2 août 2026"), et la description commençait quand même par "Le récap de la semaine du 27 juillet au 2 août..." — une pure redondance visible dans l'email, le titre juste au-dessus disant déjà la même chose. La première phrase de la description doit aller directement au contenu sans réintroduire les dates ni le mot "récap de la semaine du...".

**La phrase d'ouverture (= conclusion de semaine, réutilisée telle quelle dans `<comments>` et dans `.week-conclusion`) doit être un vrai résumé substantiel, jamais une méta-statistique creuse.** Erreur corrigée le 6 août, retour utilisateur direct ("très IA style, tu ne dis rien du tout, ça n'apporte rien au lecteur") sur le tout premier exemple publié : "Sept sujets, sept fois trois scénarios chiffrés. Sur l'ensemble de la semaine, le scénario stable a été jugé le plus probable dans les sept cas — aucune bascule nette vers le favorable ou le dégradé." — techniquement vrai, mais ça ne fait que décrire la structure du récap (compter les scénarios stables) sans rien dire de concret sur la semaine elle-même. **Interdit : toute phrase qui se contente de compter/qualifier les scénarios ("le stable l'a emporté X fois sur 7", "aucune bascule nette", "sept sujets, sept scénarios chiffrés" comme accroche).** À la place, **nommer 3-4 faits concrets et spécifiques tirés des sujets de la semaine, et en tirer un vrai fil conducteur si un lien réel existe** (ex. plusieurs dossiers bloqués sans dénouement, un thème géopolitique qui domine, plusieurs sujets qui basculent vers le même type de scénario pour une raison de fond identifiable — jamais une coïncidence statistique présentée comme un constat). Exemple retenu après correction : "Cette semaine, aucun des sept dossiers n'a vraiment basculé : le budget 2027 reste suspendu à un probable 49.3, l'Arabie saoudite envoie des signaux contradictoires sur le sport, les méga-feux se combattent encore au coup par coup sans plan structurel, la musique IA continue de grignoter du terrain sans que la loi tranche. Le fil commun de la semaine : des tensions réelles, mais aucun dénouement net." — cite des faits précis et propres à chaque sujet, pas juste leur étiquette de scénario, et le "fil commun" final est justifié par ces faits, pas asséné en préambule. Si, une semaine donnée, les 7 sujets n'ont vraiment aucun lien thématique réel entre eux, ne pas forcer un faux fil conducteur : décrire quand même 3-4 faits marquants concrets de la semaine, sans phrase de synthèse artificielle à la fin.

Structure par sujet : **{Jour}, {registre exact de l'eyebrow}** — lien vers le titre, puis 1-2 phrases de contexte factuel, puis "scénario {favorable/stable/dégradé} jugé le plus probable, à {X}% : {nom du scénario et ce qu'il signifie}." Ordre chronologique, lundi en premier, les 7 jours à la suite. **Toujours un lien cliquable vers l'archive complète** — jamais un jour mentionné sans son lien.

Une phrase de clôture sobre invitant à répondre à l'email (distincte de la phrase d'ouverture/conclusion de semaine). Pas d'emoji décoratif superflu, pas de "Salut 👋" ni de formule qui fait "essayer d'être sympa" — la simplicité et la précision suffisent à rendre le texte agréable à lire.

Pour les meta descriptions de la page HTML (balises `description`/`og:description`/`twitter:description`, étape 4), utiliser une version condensée de cette même phrase d'ouverture (viser ~150-160 caractères, garder les faits les plus parlants, pas juste une troncature brute) — voir `hebdo/2026-08-09.html` pour l'exemple de référence le plus récent.

## Étape 3bis — Générer l'image du récap (og:image)

**Ajouté le 18 août** (retour utilisateur : le récap hebdo utilisait jusque-là l'image générique `og-image-v2.png`, jamais dédiée à la semaine). Générer l'image carrée avec `scripts/social/generate_hebdo_image.py` :
```
python3 scripts/social/generate_hebdo_image.py \
    --data data.json \
    --output assets/social/hebdo/{AAAA-MM-JJ du dimanche}.png
```
avec `data.json` :
```json
{
  "weekrange": "{ex. \"3 → 9 août\"}",
  "message": "{la version condensée ~150-160 caractères déjà rédigée juste au-dessus}",
  "cta": "👉 Lire le récap complet"
}
```
**La photo de fond et le gabarit sont fixés en dur dans le script** (`assets/social/hebdo-bg.jpg`, toujours la même — voir `assets/social/hebdo-photo-credit.json` pour le crédit) : contrairement aux images par sujet/pub, il n'y a rien à choisir ni à faire vérifier chaque semaine, juste fournir le texte de la semaine. Ne jamais changer cette photo sans un retour explicite de l'utilisateur en ce sens.

## Étape 4 — Publier dans feed-weekly.xml, créer la page hebdo/{date}.html et son fragment

Insérer un nouvel `<item>` tout en haut du flux (juste après les champs `<title>`/`<link>`/`<description>`/`<language>` du `<channel>`), **avant** les items précédents — ne jamais les supprimer, l'historique reste complet comme pour `feed.xml` :
```xml
<item>
  <title>On refait le scénario de la semaine — {date de début, ex. "3 août"} au {date de fin, ex. "9 août 2026"}</title>
  <link>https://lesscenarios.fr/hebdo/{AAAA-MM-JJ du dimanche}.html</link>
  <guid isPermaLink="false">scenario-hebdo-{AAAA-MM-JJ du dimanche}</guid>
  <pubDate>{date du dimanche, format RFC-822, ex. Sun, 09 Aug 2026 14:00:00 +0200}</pubDate>
  <comments>{la phrase d'ouverture/conclusion de semaine rédigée à l'étape 3, en texte brut, sans HTML — identique au premier paragraphe de la <description> ci-dessous mais sans balises <br>}</comments>
  <description><![CDATA[{récap complet rédigé à l'étape 3, en HTML : <br><br> entre paragraphes, un <a href="https://lesscenarios.fr/archives/{AAAA-MM-JJ}.html">...</a> par sujet cité}]]></description>
</item>
```
**Pas de `<category>`** pour ce flux (pas de sondage Telegram associé à l'hebdo — `<category>` sert uniquement aux 3 options de sondage sur `feed.xml`). Le `<comments>` sert de texte court réutilisable (ex. aperçu, réseau social) sans avoir à parser le HTML de la `<description>` — même logique que sur `feed.xml`. Le `<link>` de l'item pointe vers la page dédiée créée ci-dessous — jamais vers `archives.html` en générique.

**Créer `hebdo/{AAAA-MM-JJ du dimanche}.html`** — une page figée, jamais retouchée une fois publiée (même logique que `archives/{date}.html`, jamais une réécriture d'une page hebdo d'une semaine précédente). Copier exactement le gabarit HTML/CSS du dernier exemple publié, `hebdo/2026-08-09.html` : même masthead, même nav (Accueil/Archives/Glossaire/Le projet/Newsletter/Contact, chemins relatifs `../`), même footer, mêmes variables CSS (`--ink`, `--surface`, `--gold`, `--favorable`/`--stable`/`--degrade`, polices Fraunces/Inter/JetBrains Mono), même largeur de colonne (760px). Ne jamais changer le CSS ni la structure générale — seulement le contenu texte. Cette page contient, pour chacun des 7 jours (dans `<section class="week"><div class="wrap">`), la même carte `.day-card` que celle décrite ci-dessous pour le fragment, à l'intérieur d'une `<div class="week-grid">`, plus un `.week-conclusion` en bas — voir `hebdo/2026-08-09.html` pour le HTML exact à reproduire tel quel (structure, classes, balises meta `og:*`/`twitter:*`/`article:published_time`/`og:url`, adaptées à la nouvelle date/titre). **Exception depuis le 18 août** : `og:image`/`twitter:image` (et `og:image:width`/`og:image:height`) ne pointent plus vers `og-image-v2.png` — remplacer par `https://lesscenarios.fr/assets/social/hebdo/{AAAA-MM-JJ du dimanche}.png` généré à l'étape 3bis, largeur/hauteur 1080×1080. **Ajouter aussi le petit `<script>` en bas de page** (juste avant `</body>`) qui gère le clic sur `.day-card-toggle` — copier tel quel depuis `hebdo/2026-08-09.html`.

**[Grille avec vignettes + accordéon, ajouté le 11 août, retour utilisateur : "l'image pour chaque jour possible, discret, sans allonger la page" puis "une colonne images / une colonne texte" puis "deux jours par ligne, accordéon pour le détail".]** Chaque jour est une `.day-card` affichée dans une grille 2 colonnes (`.week-grid`, 1 colonne en dessous de 620px) : l'image Instagram du jour (qui contient déjà le titre + les 3 options — voir `scripts/social/generate_instagram_image.py`) tient lieu de résumé visuel, avec un bouton "Voir le détail ▾" qui déplie la question exacte + les pourcentages + le lien vers l'archive (ces informations ne sont pas dans l'image, volontairement — voir `docs/ARCHITECTURE.md`). Comme la routine quotidienne génère déjà `assets/social/instagram/{AAAA-MM-JJ}.png` pour chaque édition (voir `docs/routine-prompt.md`), les 7 jours de la semaine ont normalement tous une image réelle — utiliser `assets/social/instagram/default.png` (image générique, juste le logo + la baseline) uniquement si l'image d'un jour particulier manque vraiment (ex. génération ratée ce jour-là).

**Créer aussi `hebdo/fragments/{AAAA-MM-JJ du dimanche}.html`** — un fragment séparé (même principe que `archives/fragments/{date}.html`), chargé en lazy-load par `archives.html` quand on clique sur "Les 7 jours ▾" de l'entrée hebdo (voir ci-dessous). Contient uniquement `<div class="week-grid">` avec les 7 `<div class="day-card">` + le `<div class="week-conclusion">` final après la fermeture de `.week-grid`, **sans** le masthead/nav/footer (juste le contenu, comme `hebdo/fragments/2026-08-09.html` déjà publié — copier sa structure exacte) :
```html
<div class="day-card">
  <p class="day-card-eyebrow">{Jour}, {registre exact de l'eyebrow}</p>
  <a class="day-card-image-link" href="archives/{AAAA-MM-JJ}.html">
    <img class="day-card-image" src="assets/social/instagram/{AAAA-MM-JJ}.png" alt="{h1 exact de l'édition}" loading="lazy">
  </a>
  <button type="button" class="day-card-toggle" aria-expanded="false" aria-controls="detail-{AAAA-MM-JJ}">Voir le détail <span class="day-card-toggle-icon" aria-hidden="true">▾</span></button>
  <div class="day-card-detail" id="detail-{AAAA-MM-JJ}">
    <div class="day-card-detail-inner">
      <p class="day-card-context">{`.question-text` exacte de l'archive citée, avec son ❓ de tête}</p>
      <div class="scenario-list">
        <p class="scenario-row{ is-winner si c'est le plus probable}" data-kind="favorable"><span class="scenario-arrow" aria-hidden="true">↑</span><span class="scenario-pct">{X}%</span><span class="scenario-label">{titre exact de la carte favorable}</span></p>
        <p class="scenario-row{ is-winner si c'est le plus probable}" data-kind="stable"><span class="scenario-arrow" aria-hidden="true">→</span><span class="scenario-pct">{X}%</span><span class="scenario-label">{titre exact de la carte stable}</span></p>
        <p class="scenario-row{ is-winner si c'est le plus probable}" data-kind="degrade"><span class="scenario-arrow" aria-hidden="true">↓</span><span class="scenario-pct">{X}%</span><span class="scenario-label">{titre exact de la carte dégradé}</span></p>
      </div>
      <a class="day-link" href="archives/{AAAA-MM-JJ}.html">Lire l'édition →</a>
    </div>
  </div>
</div>
```
Si l'image du jour manque (cas exceptionnel, voir ci-dessus), remplacer uniquement le bloc `<a class="day-card-image-link">...</a>` par `src="assets/social/instagram/default.png"` — le reste de la carte (eyebrow, bouton, détail) ne change pas.

**Attention : dans ce fragment, les liens `href`/`src` sont relatifs à la racine du site** (`archives/{AAAA-MM-JJ}.html`, `assets/social/instagram/{AAAA-MM-JJ}.png`, sans `../`) — différent de la page `hebdo/{date}.html` elle-même qui utilise `../archives/...` et `../assets/...` (elle est dans un sous-dossier). Ne pas confondre les deux. **`is-winner` va uniquement sur le `<p class="scenario-row">` du scénario au plus haut pourcentage** (jamais deux à la fois, jamais aucun). Les 7 cartes à la suite à l'intérieur de `<div class="week-grid">`, lundi en premier. Après la fermeture de `.week-grid` :
```html
<div class="week-conclusion">
  <p class="week-conclusion-label">Conclusion de la semaine</p>
  <p>{la phrase d'ouverture rédigée à l'étape 3 — identique au <comments> du flux}</p>
</div>
```
**`archives.html` porte déjà tout le CSS et le JS nécessaires** pour afficher ce fragment correctement une fois injecté (classes `.week-grid`/`.day-card*`, délégation de clic sur `.day-card-toggle` — voir `docs/ARCHITECTURE.md`) : rien à modifier dans `archives.html` en dehors de la nouvelle `<li class="entry entry-weekly">` décrite plus bas.

**Ajouter une nouvelle entrée dans `archives.html`**, à l'intérieur de `<ul class="entries" id="entries">`. **Positionnement : l'entrée hebdo va TOUJOURS juste EN DESSOUS de l'entrée de l'édition quotidienne de CE dimanche** (celle-ci est déjà publiée depuis le matin même par la routine quotidienne de 7h00, donc déjà en tête de liste au moment où cette routine hebdo s'exécute à 14h — le lundi suivant n'existe pas encore). Concrètement : repérer le `<li class="entry">` dont `<span class="entry-date">` correspond à la date du jour (le dimanche), et insérer le nouveau `<li class="entry entry-weekly">` juste après le `</li>` fermant de cette entrée-là :
```html
<li class="entry entry-weekly">
  <div class="entry-main">
    <span class="entry-date">{JJ.MM.AAAA du dimanche}</span>
    <a class="entry-title" href="hebdo/{AAAA-MM-JJ du dimanche}.html">On refait le scénario de la semaine — {date de début} au {date de fin}</a>
    <div class="entry-tags">
      <button type="button" class="tag entry-weekly-badge" data-tag="hebdo">Récap de la semaine</button>
    </div>
    <button type="button" class="entry-toggle" aria-expanded="false" aria-controls="scenarios-hebdo-{AAAA-MM-JJ du dimanche}">Les 7 jours <span class="entry-toggle-icon" aria-hidden="true">▾</span></button>
  </div>
  <div class="entry-scenarios" id="scenarios-hebdo-{AAAA-MM-JJ du dimanche}" data-fragment="hebdo/fragments/{AAAA-MM-JJ du dimanche}.html">
    <div class="entry-scenarios-inner"></div>
  </div>
</li>
```
Le `data-tag="hebdo"` est important : il alimente automatiquement la puce de filtre "Récap de la semaine" déjà présente sur le site (système générique, rien d'autre à faire) — c'est ce qui permet de retrouver l'historique de tous les récaps hebdo publiés. Ne jamais toucher aux autres entrées de la liste (`.entry` sans la classe `entry-weekly`), ni aux filtres/JS.

**Ajouter aussi une entrée dans `sitemap.xml`** pour la nouvelle page hebdo (même format que les entrées `archives/*.html` existantes : `changefreq: never`, `priority: 0.5`, `<lastmod>` = date du dimanche).

**Mettre à jour le lien "Récap de la semaine" sur `index.html`** (ajouté le 11 août, suite à un oubli constaté par l'utilisateur — le lien était resté sur l'avant-dernier récap après une publication manuelle). Dans la bande `.top-updates` juste sous la nav (voir `docs/ARCHITECTURE.md`), il y a un unique lien `<a class="update-link" href="hebdo/{ancienne-date}.html">🗓️ Récap de la semaine →</a>` : remplacer uniquement la valeur de son attribut `href` par `hebdo/{AAAA-MM-JJ du dimanche}.html`, la page tout juste publiée. **Un seul remplacement de chaîne, rien d'autre sur `index.html`** — ni le lien voisin "🔄 Sujet révisé →" (générique, toujours à jour tout seul, jamais à toucher ici), ni le CSS, ni la structure, ni aucun contenu éditorial.

## Étape 5 — Publication finale
`git add feed-weekly.xml hebdo/{AAAA-MM-JJ du dimanche}.html hebdo/fragments/{AAAA-MM-JJ du dimanche}.html archives.html sitemap.xml index.html assets/social/hebdo/{AAAA-MM-JJ du dimanche}.png`, `git commit` (message clair avec la date et un aperçu du contenu), `git push origin main` directement — jamais sur une autre branche.

Termine par un court résumé (les 7 sujets couverts, ce qui a été publié) pour que l'historique de cette exécution reste lisible.

**Ne jamais toucher** à `archives/*.html`, `feed.xml`, `sujets-prioritaires.md`, `docs/sujets-a-suivre.md`, ni aucun autre fichier du site en dehors de ceux listés à l'étape 5. **La seule modification autorisée sur `index.html`** est le remplacement de l'attribut `href` décrit à l'étape 4 — jamais le CSS, la structure, le contenu éditorial (hero, cartes, lexique...), ni le lien "Sujet révisé" voisin. Dans `archives.html`, ajouter uniquement la nouvelle `<li class="entry entry-weekly">` décrite ci-dessus — jamais modifier une entrée existante, jamais toucher aux filtres/JS. Ne jamais retoucher une page ou un fragment `hebdo/*` déjà publiés une semaine précédente — chaque semaine obtient sa propre page et son propre fragment, jamais une réécriture, exactement comme les archives quotidiennes.
