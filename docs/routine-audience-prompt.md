# Prompt de la routine « Scénario — Audience »

Ce fichier est la copie de référence du prompt envoyé par la routine "audience"
(Claude Code Remote, trigger **« Scénario — Audience »**, cron **hebdomadaire**).
Créée le 21 août à la demande de l'utilisateur, pour maintenir à jour le
graphique de croissance de l'audience sur `le-projet.html` (section
`#audience`, composant `.dc-chart-box` réutilisé en variante "favorable").

**Objectif** : montrer que l'audience grandit, avec de vrais chiffres —
cohérent avec l'identité du site ("on chiffre plutôt qu'on affirme"). Voir
`docs/ARCHITECTURE.md`, section "Mesure d'audience", pour l'historique complet
de la décision (pourquoi Search Console a été écarté, pourquoi le calcul se
limite aux éditions et pas au trafic total du site).

**Le token API GoatCounter (lecture seule) n'est jamais dans ce fichier ni
ailleurs dans le dépôt** — le dépôt est public (servi tel quel par GitHub
Pages), un secret commité y resterait visible pour toujours dans l'historique
git. Le token est fourni uniquement dans le prompt du trigger lui-même
(configuration privée côté Claude Code Remote, `job_config`, jamais
synchronisée vers GitHub). **Si le token doit être régénéré** (rotation,
fuite suspectée) : mettre à jour uniquement le trigger via `update_trigger`,
jamais un fichier de ce dépôt.

**La cible du push est toujours `main`, sans exception** — même règle que les
autres routines Scénario, même si l'environnement d'exécution assigne une
autre branche de session par défaut.

## Étape 1 — Récupérer les données

Appeler l'API GoatCounter, `GET https://scenario.goatcounter.com/api/v0/stats/hits`,
avec :
- `start=2026-07-29` — date du tout premier hit enregistré sur le site
  (constante connue, jamais à redécouvrir dynamiquement).
- `end` = **demain**, pas aujourd'hui — vérifié empiriquement le 21 août :
  `end` égal à la date du jour omettait les hits du jour lui-même dans la
  réponse ; `end` = date du jour + 2 jours les incluait de façon fiable.
  Utiliser `end` = date du jour (Paris) + 2 jours pour rester marge.
- `limit=200` — largement suffisant, le site a moins de 100 chemins trackés
  au 21 août.

En-tête `Authorization: Bearer {token}` (fourni dans le prompt du trigger,
voir ci-dessus) et `Content-Type: application/json`.

## Étape 2 — Agréger

Parmi les chemins retournés (`hits[].path`), **ne garder que ceux qui
correspondent à `^/archives/(\d{4}-\d{2}-\d{2})\.html(\?.*)?$`** — regrouper
les variantes avec query string (ex. `?trk=feed_main-feed-card_...`, ajoutée
par certains liens entrants) avec le chemin propre du même article, jamais
les compter comme un article à part. Ignorer tous les autres chemins (page
d'accueil `/` et `/index.html`, `archives.html`, `le-projet.html`, `contact.html`,
`newsletter.html`, `suivi/*`, `hebdo/*`...) — **seules les éditions
quotidiennes comptent pour ce graphique**, même périmètre que le compteur de
lecture par article (voir `docs/ARCHITECTURE.md`).

Pour chaque chemin retenu, sommer par jour calendaire (`stats[].day` /
`stats[].daily` dans la réponse) — additionner tous les articles ensemble
pour obtenir un total de lectures d'éditions par jour, tous articles
confondus, pas un total par article. Construire ensuite le **cumul** : somme
courante jour après jour, du plus ancien au plus récent, en incluant les
jours à 0 (ex. le tout premier jour du site) pour que la courbe démarre
proprement à zéro.

## Étape 3 — Mettre à jour `le-projet.html`

Dans le `<script>` situé juste après le script de suivi GoatCounter
(`data-goatcounter=...`) et juste avant `assets/pwa-install.js` :

- Remplacer le tableau `data` (paires `[date ISO, cumul]`) par la nouvelle
  série complète.
- Remplacer `xLabels` par une sélection de ~5 dates réparties sur toute la
  période — toujours la première et la dernière date de la série, 3
  intermédiaires à peu près régulièrement espacées. Ne jamais afficher tous
  les jours sur l'axe X, ça surcharge (même règle que le graphique de
  l'Horloge de l'Apocalypse, voir `docs/routine-prompt.md`).
- `yMax` : palier rond immédiatement au-dessus du dernier cumul (ex. 200 pour
  un cumul de 181, 250 pour un cumul de 210...).

Mettre à jour aussi le texte autour du graphique, dans la section
`#audience` :
- Le chiffre en gras du paragraphe d'intro : "**{N} lectures d'éditions
  cumulées** depuis le lancement, au {date la plus récente}".
- `.dc-chart-lead` : "Nombre total de lectures d'éditions depuis le
  lancement, du {date début} au {date fin}."
- Le `aria-label` du `<svg id="audience-svg">` : reprendre le point de départ
  et le point d'arrivée exacts de la série.
- Le label du dernier point sur le graphique (`{N} au {date}`, jamais
  "aujourd'hui" — ce chiffre n'est mis à jour qu'une fois par semaine, pas en
  direct, donc jamais présenté comme temps réel).

**Ne jamais changer le CSS, la structure HTML de la section, ni son
emplacement sur la page** (juste avant `#nous-suivre`) — seules les données
et le texte qui en dépend changent d'une exécution à l'autre.

## Étape 3bis — Mettre à jour `dashboard.html` [AJOUTÉ le 2 septembre]

Page interne créée le 2 septembre (retour utilisateur : vouloir un tableau
de bord regroupant le graphique d'audience et d'autres KPI, plus la file
d'attente éditoriale — voir `docs/BACKLOG.md`, entrée « Dashboard de
pilotage interne »). **Non liée depuis la nav, `noindex`, exclue de
`robots.txt`/`sitemap.xml`**, protégée par un code d'accès (comparé à un
hash SHA-256 embarqué dans la page — jamais le code en clair dans ce
fichier ni ailleurs dans le dépôt, même logique que le token GoatCounter).
**Le code d'accès n'est pas dans ce prompt** : il vit uniquement dans la
mémoire de l'utilisateur (donné une fois au moment de la création, jamais
recommuniqué automatiquement) — cette routine ne le régénère jamais, elle
ne fait que mettre à jour le contenu affiché *après* déverrouillage.

Réutiliser telles quelles les données déjà récupérées à l'étape 1
(`per_day`, cumul construit à l'étape 2) pour régénérer, dans le
`<script>` de `dashboard.html` — **aucun appel API supplémentaire pour
tout ce qui suit, uniquement de l'arithmétique sur les données déjà en
mémoire** (contrainte explicite de l'utilisateur, 2 septembre : « ça ne
doit pas nous coûter une blinde ») :
- Les 5 cartes KPI (`.kpi-grid`) : lectures cumulées ; **7 derniers jours
  glissants** (somme des 7 derniers jours calendaires disponibles, pas un
  bucket fixe) et son delta vs les 7 jours glissants précédents (même
  fenêtre décalée d'une semaine) ; **30 derniers jours glissants**, avec
  la part que ça représente du cumul total — comparaison au 30j glissants
  précédents seulement possible une fois 60 jours d'historique atteints
  (avant ça, l'indiquer explicitement plutôt que d'inventer un delta) ;
  cadence de publication (jours consécutifs sans interruption depuis la
  dernière rupture détectée dans `archives/*.html` — recalculer, ne pas
  supposer que le 25 juillet reste la bonne date de départ indéfiniment) ;
  moyenne par édition.
- Le graphique `#weekly-svg` (`var weekly`) : buckets **calendaires lundi →
  dimanche** [convention corrigée le 3 septembre 2026, retour utilisateur :
  « je trouve bizarre d'avoir que 24 sur cette semaine encore inachevée »
  — les buckets étaient jusque-là calés sur le jour de lancement du site
  (mercredi 29 juillet), donc mercredi→mardi au lieu de lundi→dimanche,
  ce qui faisait paraître la dernière barre anormalement basse puisqu'elle
  ne comptait qu'un seul jour écoulé de la vraie semaine calendaire].
  Recalculer à partir des lectures **quotidiennes** (dérivées par
  différence consécutive de la série cumulative `data` de `#cumul-svg`,
  voir juste en dessous — pas besoin d'un nouvel appel API, seulement de
  l'arithmétique sur une série déjà en mémoire), puis regrouper ces
  lectures quotidiennes par semaine ISO (lundi au dimanche). **Premier ET
  dernier bucket toujours traités comme partiels** (`is-partial`,
  libellé `(lancement)` sur le premier et `(en cours)` sur le dernier) :
  le premier parce que le suivi GoatCounter démarre un mercredi (pas de
  données avant le 29 juillet), le dernier parce que la semaine
  calendaire en cours à la date de la routine (le lundi) n'est presque
  jamais terminée. Un bucket intermédiaire n'est jamais partiel — s'il
  couvre exactement lundi à dimanche avec des données pour les 7 jours,
  pas de `is-partial` dessus. Distinct des KPI glissants ci-dessus
  (buckets calendaires fixes vs fenêtre glissante) — les deux se
  complètent, ne pas les fusionner ni en retirer un au profit de l'autre.
- Le graphique `#cumul-svg` (`var data`) : même série que `le-projet.html`,
  recopiée telle quelle (pas besoin de la recalculer deux fois — construite
  une fois à l'étape 2, réutilisée aux deux endroits).
- Le tableau top/flop (`renderTables`) : 5 meilleures et 5 moins bonnes
  éditions par lectures cumulées, sur les chemins déjà filtrés à l'étape 2.

Régénérer aussi le contenu **statique** (pas dans le `<script>`, dans le
HTML directement) des trois derniers blocs :
- **« Lectures par domaine »** : lire `archives.html` (attribut
  `data-domain` de chaque `<tr>`, déjà présent, aucune nouvelle donnée à
  produire), joindre par date aux lectures cumulées déjà filtrées à
  l'étape 2 (mêmes chemins `archives/{date}.html`), sommer par domaine.
  Trier par **moyenne par édition**, pas par total (un domaine avec peu
  d'éditions ne doit pas paraître faible juste faute d'échantillon).
- **« Agenda de la semaine »** (cartes `.agenda-card`, pas un tableau) :
  relire `sujets-prioritaires.md`, prendre pour chaque section de
  registre (lundi Géopolitique, mardi Carte blanche, mercredi Actu
  française, jeudi Économie, vendredi Sciences, samedi Culture, dimanche
  Sport) le premier `- [ ]` non coché — titre raccourci à une ligne
  courte pour la carte, pas le texte intégral de `sujets-prioritaires.md`.
  **Fenêtre lundi → dimanche** [convention ajoutée le 3 septembre, retour
  utilisateur] : toujours afficher le **prochain lundi au prochain
  dimanche** (jamais un « aujourd'hui + 6 jours » qui dérive au fil de la
  semaine), puisque cette routine tourne le lundi — la fenêtre affichée
  est donc systématiquement la semaine à venir dans son intégralité,
  jamais une semaine à moitié entamée. Rappeler que ce n'est qu'un
  aperçu de l'ordre actuel, pas une garantie (la routine quotidienne peut
  réordonner/insérer une priorité absolue entre-temps). Mettre aussi à
  jour la ligne « Priorité absolue » (vide ou premier sujet non coché de
  cette section).
- **« Semaine d'après »** (liste `.agenda-later-list`, sous l'agenda
  principal) [ajouté le 3 septembre, retour utilisateur : « donner
  rapidement les sujets prévisionnels de la semaine après »] : pour
  chaque registre, le **2ᵉ** `- [ ]` non coché (celui qui suit le sujet
  déjà placé dans l'agenda ci-dessus) — une ligne par registre, texte
  intégral de l'accroche (pas besoin de raccourcir, ce n'est pas dans une
  carte). Un registre qui n'a plus qu'un seul sujet en attente (ex. Carte
  blanche, Culture selon l'état de la file) → l'indiquer explicitement
  avec `.agenda-later-empty` (« rien en réserve après … »), jamais laisser
  la ligne vide ou l'omettre silencieusement.
- **« Autonomie par registre »** [ajouté le 3 septembre 2026, tableau
  créé manuellement le même jour puis intégré à cette routine dans la
  foulée pour qu'il ne devienne pas obsolète] : relire
  `sujets-prioritaires.md` (déjà lu pour « Agenda de la semaine »
  ci-dessus, aucune lecture supplémentaire) et compter les lignes
  `- [ ]` (non cochées) de chacun des 7 registres hebdomadaires — les
  sections `## Géopolitique — lundi`, `## Mardi — carte blanche aux
  lecteurs...`, `## Actualité & politique française — mercredi`,
  `## Économie & finance mondiale — jeudi`, `## Sciences — vendredi...`,
  `## Culture — samedi`, `## Sport — dimanche`. **Ne jamais compter la
  section `## 🔥 Priorité absolue`** : elle n'est pas consommée une fois
  par semaine comme les 7 autres, c'est une file d'urgence opportuniste,
  hors de ce calcul.

  Chaque registre n'étant consommé qu'**une fois par semaine** (cadence
  quotidienne à 7 registres fixes), le nombre de semaines d'autonomie
  est **strictement égal** au nombre de sujets non cochés — aucun calcul
  supplémentaire. Trier le tableau par autonomie **croissante** (le
  registre le plus en tension en premier), pas par jour de la semaine :
  le but du tableau est de repérer vite ce qui manque, pas de suivre le
  calendrier.

  Statut et couleur — seuils fixes, appliquer tel quel, aucun jugement
  éditorial requis (même logique "économie de tokens" que le reste de
  cette routine) :
  | Non cochés | Texte | Couleur |
  |---|---|---|
  | 0 | `épuisée` | `var(--degrade)` |
  | 1 | `⚠️ épuisée la semaine prochaine` | `var(--degrade)` |
  | 2 à 4 | `⚠️ ~{N} semaines` | `var(--degrade)` |
  | 5 à 10 | `~{N} semaines` | `var(--stable)` |
  | 11 et plus | `confortable` | `var(--favorable)` |

  Reconstruire entièrement le `<tbody>` de ce tableau (une `<tr>` par
  registre, colonnes Registre / Non cochés / Autonomie) selon ces
  règles. Mettre aussi à jour la phrase `.kpi-sub` juste en dessous :
  nommer explicitement le ou les registres actuellement en `dégradé`
  (0 à 4 non cochés) et leur date d'épuisement approximative ; si aucun
  registre n'est en dégradé, le dire explicitement plutôt que de
  garder une ancienne phrase d'alerte périmée.
- **« Suivis actifs »** : relire `docs/sujets-a-suivre.md`, section
  « Suivis actifs », reprendre la ligne « Prochaine échéance connue » de
  chacun des suivis existants, trier par date la plus proche (« pas de
  date fixe » toujours en bas).

**Ne jamais changer le CSS ni la structure HTML de `dashboard.html`**
(porte d'accès, grille de KPI, disposition des graphiques) — même règle
que pour `#audience` sur `le-projet.html`, seules les données et le texte
qui en dépend changent d'une exécution à l'autre. En particulier, **ne
jamais retirer l'écouteur `pageshow`** ajouté le 3 septembre juste après
la vérification du hash au chargement (`if (ev.persisted...) renderCharts();`)
ni le vidage des conteneurs en tête de `renderWeekly()`/`renderCumul()`/
`fill()` (`svg.innerHTML = ''`/`tbody.innerHTML = ''`) : c'est le fix d'un
bug réel remonté par l'utilisateur (graphiques vides après restauration
depuis le bfcache du navigateur/webview), pas du code à nettoyer.

## Étape 3ter — Écrire `assets/data/reads.json` (lectures par édition sur `archives.html`)
[AJOUTÉ le 3 septembre 2026, retour utilisateur : « mettre le nombre de
lecture sur la page archive »]

`archives.html` affiche une colonne « Lectures » par édition (chemin
`archives/{AAAA-MM-JJ}.html`) et un badge 🔥 sur l'édition la plus lue —
voir `scripts/seo/generate_archives_table.py`, variable `reads_script`.
**Ce script ne connaît jamais le nombre de lectures lui-même** : il se
contente d'écrire une colonne vide (`—`) et un petit JS qui va chercher
les vraies valeurs dans `assets/data/reads.json` au chargement de la
page. C'est cette routine-ci qui écrit ce fichier, chaque semaine :

- **Aucun appel API supplémentaire** : réutiliser les lectures cumulées
  par chemin déjà calculées à l'étape 2 (`per_day` agrégé par article),
  la même donnée qui alimente le tableau top/flop de `dashboard.html`
  juste au-dessus — seulement, ici, **toutes les éditions, pas
  seulement les 5 meilleures/5 moins bonnes**.
- Format : objet JSON plat, une clé par date ISO, valeur = lectures
  cumulées depuis le lancement —
  `{"AAAA-MM-JJ": N, "AAAA-MM-JJ": N, ...}`. Remplacer le fichier en
  entier à chaque exécution (pas de fusion incrémentale à gérer :
  toutes les données viennent du même appel GoatCounter de l'étape 1).
- Valider le JSON (`python3 -c "import json;
  json.load(open('assets/data/reads.json'))"`) avant de committer.
- **`generate_archives_table.py` (domaines/tags) et cette routine
  (lectures) ne se marchent jamais dessus** : le premier ne touche
  jamais `reads.json`, la seconde ne touche jamais `archives.html`
  directement — la colonne se remplit uniquement côté client au
  chargement de la page, quel que soit l'ordre dans lequel les deux
  scripts tournent dans la semaine.
- **Amorçage du 3 septembre** : `reads.json` a été créé manuellement ce
  jour-là avec seulement 10 valeurs connues (le top 5 / flop 5 alors
  affiché sur `dashboard.html`) — cette routine le remplace
  intégralement dès son premier passage suivant, aucune action
  particulière à prévoir pour "compléter" les valeurs manquantes.

## Étape 4 — Vérification et publication

Vérifier la syntaxe des `<script>` modifiés (`node --check`) avant de
committer — `le-projet.html` et `dashboard.html`. Une vérification visuelle
(Playwright, `executablePath: '/opt/pw-browsers/chromium'`, capture de la
section `#audience` **et** de `dashboard.html` déverrouillé) est
recommandée à chaque passage — le composant ne change pas de structure d'une
semaine à l'autre, mais une régression silencieuse (chevauchement de labels
sur une série qui s'accélère, par exemple) resterait invisible sans capture.

`git add le-projet.html dashboard.html assets/data/reads.json`, commit
avec un message clair (`[audience] mise à jour du {date} — {N} lectures
cumulées`), `git push origin main` directement — jamais sur une autre
branche.

## Étape 5 — Résumé final

Toujours terminer par : le nouveau total cumulé, la date de la donnée la plus
récente, et le delta depuis la dernière mise à jour connue (comparer au
dernier total committé si visible dans l'historique git, sinon simplement
donner le nouveau total).
