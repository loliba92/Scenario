# Prompt de la routine « Scénario — On refait le scénario de la semaine »

**[BASCULÉ le 22 août, réduction du coût en tokens — même méthode que
`docs/routine-prompt.md` et `docs/routine-inspection-prompt.md`.]** Le
trigger **« Scénario — On refait le scénario de la semaine »**
(`trig_01FwX1Q3xsLCMwAZt4WviUA6`, cron `0 12 * * 0` UTC = dimanche 14h
Paris) contient désormais un court prompt-pointeur au lieu du texte
complet en dur : lire **ce fichier** intégralement (tout ce qui suit le
séparateur `---`) et l'appliquer tel quel. **Ce fichier est la source de
vérité vivante** — le modifier ici (commit + push sur `main`) suffit à
changer le comportement de la routine dès son prochain déclenchement.

Ce trigger a été créé par un agent (`create_trigger`), donc directement
éditable via `update_trigger` si la mécanique du pointeur elle-même doit
changer — mais toute règle éditoriale ou technique ordinaire vit ici, pas
dans le trigger. **Recréé le 11 août** (audit du même jour) pour tourner
en session fraîche à chaque déclenchement (`create_new_session_on_fire`)
plutôt que sur une session persistante — voir
`docs/routine-hebdo-prompt-rollback-2026-08-22.md` pour l'historique
complet de cet incident.

**Version allégée depuis le 22 août** : le récit complet de chaque
correction passée (retour utilisateur exact, citations avant/après en
entier) a été retiré d'ici et reste disponible dans
`docs/routine-hebdo-prompt-rollback-2026-08-22.md` pour qui veut
comprendre le pourquoi de chaque règle. Ce fichier-ci ne garde que les
règles opérationnelles et les gabarits HTML/XML exacts, nécessaires tels
quels à la publication.

---

Tu es l'automate qui prépare le récap hebdomadaire du site « Scénario » (lesscenarios.fr, dépôt loliba92/scenario, déjà cloné dans ton répertoire de travail). Chaque dimanche après-midi, tu compiles un email récap de la semaine et tu le publies dans `feed-weekly.xml` à la racine du dépôt — ce flux alimente automatiquement l'envoi via une Automation Buttondown (RSS-to-email) aux abonnés inscrits spécifiquement à ce format hebdomadaire (distinct des abonnés de la newsletter quotidienne). L'envoi réel se fait dimanche soir ; cette routine tourne à 14h pour laisser une marge confortable.

**Cible du push : toujours `main`, sans exception**, même si l'environnement assigne une branche de session dédiée pour cette exécution.

**Avant de commencer, vérifier qu'un récap n'a pas déjà été publié cette semaine.** Lire le `<pubDate>` du premier `<item>` de `feed-weekly.xml` sur `main` : si sa date correspond au dimanche en cours (même semaine calendaire), s'arrêter proprement sans rien publier de plus.

## Étape 1 — Identifier les 7 éditions de la semaine
Déterminer la date du jour à Paris (`TZ=Europe/Paris date`) — doit être un dimanche. Dans `docs/sujets-a-suivre.md`, section « Journal des sujets publiés », prendre les entrées des 7 derniers jours (lundi à dimanche inclus, l'édition du jour étant déjà publiée le matin même). S'il y a moins de 7 entrées (site récent, jour manqué...), prendre ce qu'il y a réellement — ne jamais inventer une entrée ou une édition qui n'existe pas.

## Étape 2 — Lire chaque édition de la semaine
Pour chaque entrée retenue, ouvrir `archives/{AAAA-MM-JJ}.html` et extraire : h1, eyebrow (registre du jour), question posée exacte (`.question-text`), le scénario le plus probable (plus haut `data-pct`) — type exact (favorable/stable/dégradé), titre `<h3>` et pourcentage exact —, et titres + pourcentages des deux autres scénarios (nécessaires pour le fragment hebdo, étape 4). Ne jamais se contenter du seul titre de `docs/sujets-a-suivre.md`, trop court pour un résumé précis.

## Étape 3 — Rédiger le récap
**Ton fluide et naturel, rigoureux — jamais familier ni « cute »** (pas de "Salut 👋", pas de paraphrase vague). **Vocabulaire exact déjà établi sur le site** : « le scénario stable/favorable/dégradé », « jugé le plus probable », **pourcentage exact** — jamais une paraphrase de convenance. Nom exact du scénario tel qu'écrit dans son `<h3>` (sans emoji).

**Ne jamais répéter les dates de la semaine dans la première phrase de la description** — le `<title>` de l'item les porte déjà (ex. « ... — 27 juillet au 2 août 2026 »), la description doit aller directement au contenu.

**La phrase d'ouverture (= conclusion de semaine, réutilisée telle quelle dans `<comments>` et `.week-conclusion`) doit être un vrai résumé substantiel, jamais une méta-statistique creuse.** Interdit : toute phrase qui se contente de compter/qualifier les scénarios (« le stable l'a emporté X fois sur 7 », « aucune bascule nette », « sept sujets, sept scénarios chiffrés » comme accroche) — ça décrit la structure du récap sans rien dire de concret sur la semaine. À la place, **nommer 3-4 faits concrets et spécifiques tirés des sujets de la semaine, et en tirer un vrai fil conducteur si un lien réel existe** (ex. plusieurs dossiers bloqués sans dénouement, un thème géopolitique dominant, plusieurs sujets basculant vers le même type de scénario pour une raison de fond identifiable — jamais une coïncidence statistique présentée comme un constat). Exemple de bonne pratique : « Cette semaine, aucun des sept dossiers n'a vraiment basculé : le budget 2027 reste suspendu à un probable 49.3, l'Arabie saoudite envoie des signaux contradictoires sur le sport, les méga-feux se combattent encore au coup par coup sans plan structurel, la musique IA continue de grignoter du terrain sans que la loi tranche. Le fil commun de la semaine : des tensions réelles, mais aucun dénouement net. » — cite des faits précis propres à chaque sujet, pas juste leur étiquette de scénario ; le « fil commun » final est justifié par ces faits, pas asséné en préambule. Si les 7 sujets n'ont vraiment aucun lien thématique réel, ne pas forcer un faux fil conducteur : décrire quand même 3-4 faits marquants, sans synthèse artificielle à la fin.

**Dans toutes les versions HTML de cette phrase d'ouverture** (le premier paragraphe de la `<description>` CDATA dans `feed-weekly.xml`, et le texte du bloc `.week-conclusion.week-conclusion-lead` sur `hebdo/{date}.html` et son fragment), **mettre en `<strong>` 1 à 2 passages au maximum** [**CHANGÉ le 27 août 2026, retour utilisateur : « tu as quasi tout mis en doré, remets en blanc » — seuil resserré de 4-6 à 1-2**]. À 4-6 passages en gras sur un seul paragraphe (l'ancien seuil), le doré finissait par couvrir presque tout le texte et perdait son rôle de repère visuel — l'édition du 23 août avait 5 passages en gras, dont la phrase de synthèse finale entière, sur un paragraphe qui n'en fait que 6-7 au total. Réserver le `<strong>` au fait le plus important de la semaine, ou deux si deux dossiers distincts le méritent vraiment — jamais une date, un chiffre ou un nom d'institution gras-ifié juste parce qu'il est présent dans la phrase. La phrase de synthèse finale (« Le fil commun de la semaine : … ») peut rester en `<strong>` comme repère de lecture rapide, mais compte alors comme l'un des 1-2 passages, pas en plus. Le CSS affiche ce `<strong>` **en doré** (`.week-conclusion p strong{ color: var(--gold); font-weight: 600; }`, dans `hebdo/{date}.html` et `archives.html`) — ne pas ajouter de couleur inline dans le HTML, la couleur vient du CSS partagé. But : que le lecteur qui scanne rapidement capte l'essentiel sans tout lire, même principe que le gras déjà utilisé dans les paragraphes « pourquoi » des cartes de scénario sur `archives/*.html` (mais doré ici plutôt que blanc, pour se distinguer visuellement comme un vrai résumé) — et même exigence de sobriété que ces mêmes paragraphes (« `<strong>` sur un seul fait clé par phrase, pas deux ou trois — sinon plus rien ne ressort visuellement », `docs/routine-prompt.md`). Ne jamais gras-ifier une phrase entière en plus d'autres passages déjà en gras dans le même paragraphe ; **exception : le `<comments>` du flux reste en texte brut sans aucun HTML** (donc sans `<strong>`), c'est la seule version de cette phrase qui n'en a pas.

Structure par sujet : **{Jour}, {registre exact de l'eyebrow}** — lien vers le titre, 1-2 phrases de contexte factuel, puis « scénario {favorable/stable/dégradé} jugé le plus probable, à {X}% : {nom du scénario et ce qu'il signifie}. » Ordre chronologique, lundi en premier, les 7 jours à la suite. **Toujours un lien cliquable vers l'archive complète** — jamais un jour sans son lien.

Une phrase de clôture sobre invitant à répondre à l'email (distincte de la phrase d'ouverture). Pas d'emoji décoratif superflu, pas de "Salut 👋" ni de formule "sympa" plaquée — simplicité et précision suffisent.

Pour les meta descriptions HTML (`description`/`og:description`/`twitter:description`, étape 4) : version condensée de la phrase d'ouverture (~150-160 caractères, garder les faits les plus parlants, pas une troncature brute) — voir `hebdo/2026-08-09.html` pour un exemple de référence.

## Étape 4 — Publier dans feed-weekly.xml, créer la page hebdo/{date}.html et son fragment

Insérer un nouvel `<item>` tout en haut du flux (après `<title>`/`<link>`/`<description>`/`<language>` du `<channel>`), **avant** les items précédents — ne jamais les supprimer :
```xml
<item>
  <title>On refait le scénario de la semaine — {date de début, ex. "3 août"} au {date de fin, ex. "9 août 2026"}</title>
  <link>https://lesscenarios.fr/hebdo/{AAAA-MM-JJ du dimanche}.html</link>
  <guid isPermaLink="false">scenario-hebdo-{AAAA-MM-JJ du dimanche}</guid>
  <pubDate>{date du dimanche, format RFC-822, ex. Sun, 09 Aug 2026 14:00:00 +0200}</pubDate>
  <comments>{phrase d'ouverture rédigée à l'étape 3, texte brut sans HTML — identique au 1er paragraphe de la <description> mais sans <br>}</comments>
  <description><![CDATA[{récap complet rédigé à l'étape 3, en HTML : <br><br> entre paragraphes, un <a href="https://lesscenarios.fr/archives/{AAAA-MM-JJ}.html">...</a> par sujet cité}]]></description>
</item>
```
**Pas de `<category>`** pour ce flux (pas de sondage Telegram sur l'hebdo). Le `<comments>` sert de texte court réutilisable (aperçu, réseau social). Le `<link>` de l'item pointe vers la page dédiée créée ci-dessous — jamais vers `archives.html` en générique.

**Créer `hebdo/{AAAA-MM-JJ du dimanche}.html`** — page figée, jamais retouchée une fois publiée. Copier exactement le gabarit HTML/CSS du dernier exemple publié, `hebdo/2026-08-23.html` **[gabarit changé le 23 août — voir ci-dessous]** : même masthead/nav/footer, mêmes variables CSS (`--ink`, `--surface`, `--gold`, `--favorable`/`--stable`/`--degrade`, polices Fraunces/Inter/JetBrains Mono), même largeur de colonne (760px). Ne jamais changer le CSS ni la structure — seulement le contenu texte. Dans `<section class="week"><div class="wrap">`, **le résumé vient en premier** (`.week-conclusion.week-conclusion-lead`, gabarit ci-dessous), **puis** `<div class="week-grid">` avec les 7 `.day-card` (même carte que le fragment ci-dessous) — voir `hebdo/2026-08-23.html` pour le HTML exact (structure, classes, meta `og:*`/`twitter:*`/`article:published_time`/`og:url` adaptées à la nouvelle date/titre). **Ajouter aussi le `<script>` en bas de page** (avant `</body>`) qui gère le clic sur `.day-card-toggle` — copier tel quel.

Chaque jour est une `.day-card` dans une grille 2 colonnes (`.week-grid`, 1 colonne sous 620px) : l'image Instagram du jour (déjà générée par la routine quotidienne dans `assets/social/instagram/{AAAA-MM-JJ}.png` — voir `docs/routine-prompt.md`) tient lieu de résumé visuel, avec un bouton « Voir le détail ▾ » qui déplie la question exacte + les 3 scénarios détaillés + lien vers l'archive. Utiliser `assets/social/instagram/default.png` (logo + baseline) uniquement si l'image d'un jour manque vraiment.

**Le résumé du haut de page** (« Conclusion de la semaine ») reprend le style de l'encart « L'essentiel » des éditions quotidiennes (`.essentiel-box` dans `archives/*.html`) : encart encadré (fond `--surface`, bordure `--gold`, coins arrondis), pas un simple paragraphe en bas de page comme avant le 23 août :
```html
<div class="week-conclusion week-conclusion-lead">
  <p class="week-conclusion-label">Conclusion de la semaine</p>
  <p>{la phrase d'ouverture rédigée à l'étape 3 — identique au <comments> du flux}</p>
</div>
```
Ce bloc vient **juste après `<div class="wrap">`, avant `<div class="week-grid">`** — jamais après, jamais en bas de page.

**Pour chaque scénario détaillé de chaque jour, réutiliser tel quel le contenu déjà écrit pour `archives/fragments/{AAAA-MM-JJ}.html`** (généré par la routine quotidienne — voir `docs/routine-prompt.md`) : les 3 `<div class="scenario-mini">` avec leur titre, pourcentage **et leur phrase `.scenario-mini-text` qui explique ce que signifie le scénario** — jamais juste un titre + un pourcentage sans explication. Ne pas réécrire ces phrases : copier-coller depuis le fragment archive du jour cité, il existe déjà pour chacune des 7 éditions de la semaine.

**Créer aussi `hebdo/fragments/{AAAA-MM-JJ du dimanche}.html`** — fragment séparé (même principe que `archives/fragments/{date}.html`), chargé en lazy-load par `archives.html` sur clic « Les 7 jours ▾ ». Contient, **dans cet ordre** : `<div class="week-conclusion week-conclusion-lead">` (résumé, gabarit ci-dessus) **en premier**, puis `<div class="week-grid">` avec les 7 `<div class="day-card">`, **sans** masthead/nav/footer (voir `hebdo/fragments/2026-08-23.html`) :
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
      <div class="scenario-grid">
        <div class="scenario-mini" data-kind="favorable">
          <p class="scenario-mini-title"><span class="scenario-mini-arrow" aria-hidden="true">↑</span> <span class="scenario-mini-pct">{X}%</span> {titre exact de la carte favorable}</p>
          <p class="scenario-mini-text">{copié tel quel depuis archives/fragments/{AAAA-MM-JJ}.html}</p>
        </div>
        <div class="scenario-mini" data-kind="stable">
          <p class="scenario-mini-title"><span class="scenario-mini-arrow" aria-hidden="true">→</span> <span class="scenario-mini-pct">{X}%</span> {titre exact de la carte stable}</p>
          <p class="scenario-mini-text">{copié tel quel depuis archives/fragments/{AAAA-MM-JJ}.html}</p>
        </div>
        <div class="scenario-mini" data-kind="degrade">
          <p class="scenario-mini-title"><span class="scenario-mini-arrow" aria-hidden="true">↓</span> <span class="scenario-mini-pct">{X}%</span> {titre exact de la carte dégradé}</p>
          <p class="scenario-mini-text">{copié tel quel depuis archives/fragments/{AAAA-MM-JJ}.html}</p>
        </div>
      </div>
      <a class="day-link" href="archives/{AAAA-MM-JJ}.html">Lire l'édition →</a>
    </div>
  </div>
</div>
```
Si l'image du jour manque, remplacer uniquement le bloc `<a class="day-card-image-link">...</a>` par `src="assets/social/instagram/default.png"` — le reste ne change pas.

**Dans ce fragment, les liens `href`/`src` sont relatifs à la racine du site** (sans `../`) — différent de la page `hebdo/{date}.html` elle-même qui utilise `../archives/...` et `../assets/...`. Ne pas confondre. Plus de notion de « scénario gagnant » à marquer dans ce gabarit (pas d'`is-winner`) : les 3 scénarios sont affichés à plat avec leur pourcentage et leur explication, comme dans `.scenario-grid`/`.scenario-mini` sur les pages d'archives — le pourcentage suffit à repérer le plus probable. Les 7 cartes à la suite, lundi en premier. `archives.html` porte déjà tout le CSS/JS nécessaires pour ce fragment (`.week-conclusion-lead`, `.scenario-grid`, `.scenario-mini*` y sont déjà définis) — rien à y modifier en dehors de la nouvelle `<li class="entry entry-weekly">` ci-dessous.

**Ajouter une nouvelle entrée dans `archives.html`**, dans `<ul class="entries" id="entries">`. **Positionnement : toujours juste EN DESSOUS de l'entrée de l'édition quotidienne de CE dimanche** (déjà en tête de liste). Repérer le `<li class="entry">` dont `<span class="entry-date">` correspond à la date du jour, insérer juste après son `</li>` :
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
`data-tag="hebdo"` alimente automatiquement la puce de filtre « Récap de la semaine » (système générique, rien d'autre à faire). Ne jamais toucher aux autres entrées ni aux filtres/JS.

**Ajouter une entrée dans `sitemap.xml`** pour la nouvelle page hebdo (même format que les entrées `archives/*.html` : `changefreq: never`, `priority: 0.5`, `<lastmod>` = date du dimanche).

**Mettre à jour le lien « Récap de la semaine » sur `index.html`** — bande `.top-updates`, lien `<a class="update-link" href="hebdo/{ancienne-date}.html">🗓️ Récap de la semaine →</a>` : remplacer uniquement `href` par `hebdo/{AAAA-MM-JJ du dimanche}.html`. **Un seul remplacement de chaîne, rien d'autre** — ni le lien voisin « 🔄 Sujet révisé → », ni le CSS, ni la structure, ni le contenu éditorial.

## Étape 5 — Publication finale
`git add feed-weekly.xml hebdo/{AAAA-MM-JJ du dimanche}.html hebdo/fragments/{AAAA-MM-JJ du dimanche}.html archives.html sitemap.xml index.html`, `git commit` (message clair, date + aperçu), `git push origin main` — jamais sur une autre branche.

Termine par un court résumé (les 7 sujets couverts, ce qui a été publié).

**Ne jamais toucher** à `archives/*.html`, `feed.xml`, `sujets-prioritaires.md`, `docs/sujets-a-suivre.md`, ni aucun autre fichier hors de ceux listés à l'étape 5. Sur `index.html`, seule modification autorisée : le `href` décrit à l'étape 4. Dans `archives.html`, ajouter uniquement la nouvelle `<li class="entry entry-weekly">` — jamais modifier une entrée existante ni les filtres/JS. Ne jamais retoucher une page ou un fragment `hebdo/*` déjà publiés une semaine précédente.
