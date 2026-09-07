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

**La conclusion de semaine (réutilisée dans `<comments>` et `.week-conclusion`) doit être un vrai résumé substantiel, jamais une méta-statistique creuse — et depuis le 6 septembre, en liste à puces plutôt qu'en un seul paragraphe filé** [**CHANGÉ le 6 septembre 2026, retour utilisateur : « le résumé est trop narratif, mets des bullet »** — jusque-là, 3-4 faits étaient enchaînés à la suite dans une même phrase séparée par des points-virgules ; trop dense à scanner rapidement]. Interdit : toute phrase/puce qui se contente de compter/qualifier les scénarios (« le stable l'a emporté X fois sur 7 », « aucune bascule nette », « sept sujets, sept scénarios chiffrés » comme accroche) — ça décrit la structure du récap sans rien dire de concret sur la semaine. À la place, **une puce par fait concret et spécifique tiré des sujets de la semaine (3-4 puces), puis une phrase de clôture séparée qui tire un vrai fil conducteur si un lien réel existe** (ex. plusieurs dossiers bloqués sans dénouement, un thème géopolitique dominant, plusieurs sujets basculant vers le même type de scénario pour une raison de fond identifiable — jamais une coïncidence statistique présentée comme un constat). Exemple de bonne pratique (puces) : « Le budget 2027 reste suspendu à un probable 49.3. » / « L'Arabie saoudite envoie des signaux contradictoires sur le sport. » / « Les méga-feux se combattent encore au coup par coup sans plan structurel. » / « La musique IA continue de grignoter du terrain sans que la loi tranche. », suivi de la phrase de clôture séparée : « Le fil commun de la semaine : des tensions réelles, mais aucun dénouement net. » — chaque puce cite un fait précis propre à un sujet, pas juste son étiquette de scénario ; le « fil commun » final est justifié par ces faits, pas asséné en préambule. Si les 7 sujets n'ont vraiment aucun lien thématique réel, ne pas forcer un faux fil conducteur : lister quand même 3-4 faits marquants en puces, sans phrase de synthèse artificielle à la fin.

**Dans toutes les versions HTML de cette conclusion** (les `<li>` et la phrase de clôture dans la `<description>` CDATA de `feed-weekly.xml`, et le bloc `.week-conclusion.week-conclusion-lead` sur `hebdo/{date}.html` et son fragment), **mettre en `<strong>` 1 à 2 passages au maximum, tous éléments confondus (puces + phrase de clôture)** [**CHANGÉ le 27 août 2026, retour utilisateur : « tu as quasi tout mis en doré, remets en blanc » — seuil resserré de 4-6 à 1-2 ; passage aux puces le 6 septembre, seuil inchangé**]. Réserver le `<strong>` au fait le plus important de la semaine, ou deux si deux dossiers distincts le méritent vraiment — jamais une date, un chiffre ou un nom d'institution gras-ifié juste parce qu'il est présent dans une puce. La phrase de clôture (« Le fil commun de la semaine : … ») peut rester en `<strong>` comme repère de lecture rapide, mais compte alors comme l'un des 1-2 passages, pas en plus. Le CSS affiche ce `<strong>` **en doré** (`.week-conclusion strong{ color: var(--gold); font-weight: 600; }`, dans `hebdo/{date}.html` uniquement — **`archives.html` n'a plus ce CSS du tout depuis sa refonte en tableau**, voir l'étape 4 plus bas) — ne pas ajouter de couleur inline dans le HTML, la couleur vient du CSS partagé. But : que le lecteur qui scanne rapidement capte l'essentiel sans tout lire, même principe que le gras déjà utilisé dans les paragraphes « pourquoi » des cartes de scénario sur `archives/*.html` (mais doré ici plutôt que blanc, pour se distinguer visuellement comme un vrai résumé) — et même exigence de sobriété que ces mêmes paragraphes (« `<strong>` sur un seul fait clé par phrase, pas deux ou trois — sinon plus rien ne ressort visuellement », `docs/routine-prompt.md`). Ne jamais gras-ifier une puce entière en plus d'un autre passage déjà en gras ailleurs dans le bloc ; **exception : le `<comments>` du flux reste en texte brut sans aucun HTML** (donc sans `<strong>`, sans `<ul>`/`<li>` — les faits y sont séparés par « • » au lieu des points-virgules d'avant le 6 septembre), c'est la seule version de cette conclusion qui n'a ni gras ni liste.

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
  <comments>{conclusion de semaine rédigée à l'étape 3, texte brut sans HTML — les mêmes faits que les puces de la <description>, mais séparés par « • » au lieu de <li>, suivis de la phrase de clôture}</comments>
  <description><![CDATA[{phrase d'intro courte}<ul><li>{fait 1}</li><li>{fait 2}</li><li>{fait 3}</li>{éventuellement <li>{fait 4}</li>}</ul><strong>{phrase de clôture "Le fil commun de la semaine : ..."}</strong><br><br>{récap complet des 7 jours rédigé à l'étape 3, en HTML : <br><br> entre paragraphes, un <a href="https://lesscenarios.fr/archives/{AAAA-MM-JJ}.html">...</a> par sujet cité}]]></description>
</item>
```
**Pas de `<category>`** pour ce flux (pas de sondage Telegram sur l'hebdo). Le `<comments>` sert de texte court réutilisable (aperçu, réseau social). Le `<link>` de l'item pointe vers la page dédiée créée ci-dessous — jamais vers `archives.html` en générique.

**Créer `hebdo/{AAAA-MM-JJ du dimanche}.html`** — page figée, jamais retouchée une fois publiée. Copier exactement le gabarit HTML/CSS du dernier exemple publié, `hebdo/2026-09-06.html` **[gabarit changé le 6 septembre — CSS `.week-conclusion-bullets`/`.week-conclusion-thread` ajouté, voir ci-dessous ; structure par ailleurs identique au gabarit du 23 août]** : même masthead/nav/footer, mêmes variables CSS (`--ink`, `--surface`, `--gold`, `--favorable`/`--stable`/`--degrade`, polices Fraunces/Inter/JetBrains Mono), même largeur de colonne (760px). Ne jamais changer le CSS ni la structure — seulement le contenu texte. Dans `<section class="week"><div class="wrap">`, **le résumé vient en premier** (`.week-conclusion.week-conclusion-lead`, gabarit ci-dessous), **puis** `<div class="week-grid">` avec les 7 `.day-card` (même carte que le fragment ci-dessous) — voir `hebdo/2026-09-06.html` pour le HTML exact (structure, classes, meta `og:*`/`twitter:*`/`article:published_time`/`og:url` adaptées à la nouvelle date/titre). **Ajouter aussi le `<script>` en bas de page** (avant `</body>`) qui gère le clic sur `.day-card-toggle` — copier tel quel.

Chaque jour est une `.day-card` dans une grille 2 colonnes (`.week-grid`, 1 colonne sous 620px) : l'image Instagram du jour (déjà générée par la routine quotidienne dans `assets/social/instagram/{AAAA-MM-JJ}.png` — voir `docs/routine-prompt.md`) tient lieu de résumé visuel, avec un bouton « Voir le détail ▾ » qui déplie la question exacte + les 3 scénarios détaillés + lien vers l'archive. Utiliser `assets/social/instagram/default.png` (logo + baseline) uniquement si l'image d'un jour manque vraiment.

**Le résumé du haut de page** (« Conclusion de la semaine ») reprend le style de l'encart « L'essentiel » des éditions quotidiennes (`.essentiel-box` dans `archives/*.html`) : encart encadré (fond `--surface`, bordure `--gold`, coins arrondis), pas un simple paragraphe en bas de page comme avant le 23 août, et **en liste à puces depuis le 6 septembre** (voir étape 3) :
```html
<div class="week-conclusion week-conclusion-lead">
  <p class="week-conclusion-label">Conclusion de la semaine</p>
  <ul class="week-conclusion-bullets">
    <li>{fait 1 rédigé à l'étape 3}</li>
    <li>{fait 2}</li>
    <li>{fait 3}</li>
  </ul>
  <p class="week-conclusion-thread">{phrase de clôture "Le fil commun de la semaine : ..." — identique à la fin du <comments> du flux}</p>
</div>
```
Ce bloc vient **juste après `<div class="wrap">`, avant `<div class="week-grid">`** — jamais après, jamais en bas de page.

**Pour chaque scénario détaillé de chaque jour, réutiliser tel quel le contenu déjà écrit pour `archives/fragments/{AAAA-MM-JJ}.html`** (généré par la routine quotidienne — voir `docs/routine-prompt.md`) : les 3 `<div class="scenario-mini">` avec leur titre, pourcentage **et leur phrase `.scenario-mini-text` qui explique ce que signifie le scénario** — jamais juste un titre + un pourcentage sans explication. Ne pas réécrire ces phrases : copier-coller depuis le fragment archive du jour cité, il existe déjà pour chacune des 7 éditions de la semaine.

**Créer aussi `hebdo/fragments/{AAAA-MM-JJ du dimanche}.html`** — fragment séparé (même principe que `archives/fragments/{date}.html`). **`archives.html` ne le charge plus depuis sa refonte en tableau** (voir plus bas) : ce fichier est conservé pour la cohérence de la collection et une éventuelle réutilisation future, mais n'est actuellement consommé par aucune page du site — le seul point d'accès au récap depuis `archives.html` est le lien direct décrit plus bas. Contient, **dans cet ordre** : `<div class="week-conclusion week-conclusion-lead">` (résumé, gabarit ci-dessus) **en premier**, puis `<div class="week-grid">` avec les 7 `<div class="day-card">`, **sans** masthead/nav/footer (voir `hebdo/fragments/2026-08-23.html`) :
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

**Dans ce fragment, les liens `href`/`src` sont relatifs à la racine du site** (sans `../`) — différent de la page `hebdo/{date}.html` elle-même qui utilise `../archives/...` et `../assets/...`. Ne pas confondre. Plus de notion de « scénario gagnant » à marquer dans ce gabarit (pas d'`is-winner`) : les 3 scénarios sont affichés à plat avec leur pourcentage et leur explication, comme dans `.scenario-grid`/`.scenario-mini` sur les pages d'archives — le pourcentage suffit à repérer le plus probable. Les 7 cartes à la suite, lundi en premier.

**Ligne « Récap de la semaine » dans `archives.html` — automatique, rien à écrire à la main [RÉÉCRIT le 7 septembre 2026, retour utilisateur].** Historique court : `archives.html` avait été refondu en tableau (`<table class="archives-table" id="archives-table">`) sans que cette routine en soit informée, l'ancien système `<ul class="entries">`/`<li class="entry entry-weekly">` avait disparu, et une première tentative de correctif le 6 septembre (ligne `<tr class="row-weekly">` ajoutée « à la main » dans `archives.html`) n'a en réalité jamais tenu : le fichier est entièrement régénéré à chaque passage de `scripts/seo/generate_archives_table.py` (voir `docs/routine-prompt.md`, § « Pages thématiques et table d'archives »), qui ignorait tout des récaps hebdo — toute ligne ajoutée à la main y disparaît donc silencieusement au prochain passage du script. **Corrigé à la racine le 7 septembre** : le script lui-même détecte désormais chaque `hebdo/AAAA-MM-JJ.html` publié (fonction `discover_weekly_recaps()`, cherche le `<title>` de la page hebdo) et insère automatiquement une ligne `<tr class="week-recap-row"><td class="week-recap-cell" colspan="6">` (fond doré discret, lien direct vers `hebdo/{date}.html`) juste après la ligne `<tr data-date="{AAAA-MM-JJ du dimanche}">` de l'édition quotidienne de ce même dimanche — à chaque régénération, sans intervention manuelle.

**Pour que la ligne apparaisse tout de suite plutôt que d'attendre la prochaine régénération hebdomadaire normale** : juste après avoir créé `hebdo/{AAAA-MM-JJ du dimanche}.html` et son fragment ci-dessus, relancer `python3 scripts/seo/generate_archives_table.py` et inclure `archives.html` dans le commit de cette routine (même pattern que `docs/routine-en-prompt.md`, étape 6bis, pour le badge EN). **Ne jamais éditer `archives.html` à la main** — la ligne récap comme le reste de la page, y toucher directement ne survivrait pas à la prochaine régénération, exactement la panne du 6 septembre qui vient d'être corrigée.

**Ajouter une entrée dans `sitemap.xml`** pour la nouvelle page hebdo (même format que les entrées `archives/*.html` : `changefreq: never`, `priority: 0.5`, `<lastmod>` = date du dimanche) — l'insérer juste après l'entrée `archives/{AAAA-MM-JJ du dimanche}.html`.

**Mettre à jour DEUX endroits sur `index.html`** [**section réécrite le 6 septembre 2026** — l'ancienne bande `.top-updates` avec lien texte `🗓️ Récap de la semaine →` a depuis fusionné dans une rangée d'icônes du header, et un bandeau dédié a été ajouté] :
1. L'icône calendrier du header, `<a class="masthead-notif-btn" href="hebdo/{ancienne-date}.html" aria-label="Récap de la semaine" title="Récap de la semaine">` : remplacer uniquement `href` par `hebdo/{AAAA-MM-JJ du dimanche}.html`.
2. **Le bandeau `<div class="weekly-banner" id="weekly-banner" data-hebdo="{ancienne-date}" hidden>`** (juste après `</nav>`, avant `.intro-banner`) : mettre à jour `data-hebdo` (déclenche le réaffichage du bandeau à chaque nouveau récap, voir le JS en bas de page — comparaison de date en localStorage, pas un "vu une fois" comme `.intro-banner`), le `href` du lien `#weekly-banner-link` (`hebdo/{AAAA-MM-JJ du dimanche}.html`), et le texte `.weekly-banner-text` si sa formulation générique ne convient plus. **Trois remplacements ciblés au total (icône + data-hebdo + href du bandeau), rien d'autre** — ni le CSS, ni la structure, ni le lien voisin « Sujet révisé », ni `.intro-banner`.

## Étape 5 — Publication finale
`git add feed-weekly.xml hebdo/{AAAA-MM-JJ du dimanche}.html hebdo/fragments/{AAAA-MM-JJ du dimanche}.html archives.html sitemap.xml index.html`, `git commit` (message clair, date + aperçu), `git push origin main` — jamais sur une autre branche.

Termine par un court résumé (les 7 sujets couverts, ce qui a été publié).

**Ne jamais toucher** à `archives/*.html`, `feed.xml`, `sujets-prioritaires.md`, `docs/sujets-a-suivre.md`, ni aucun autre fichier hors de ceux listés à l'étape 5. Sur `index.html`, seules modifications autorisées : les trois remplacements ciblés décrits à l'étape 4 (icône masthead + `data-hebdo` + `href` du bandeau `weekly-banner`) — jamais toucher `.intro-banner` ni son JS. `archives.html` ne se régénère que via `python3 scripts/seo/generate_archives_table.py` (voir étape 4 ci-dessus) — jamais d'édition manuelle, la ligne récap comme le reste de la page. Ne jamais retoucher une page ou un fragment `hebdo/*` déjà publiés une semaine précédente.
