# Architecture — Scénario

Vue d'ensemble technique du site, pour s'y retrouver rapidement sans avoir à
tout redécouvrir à chaque fois.

## Aperçu

**Scénario** est un site d'actualité statique, publié gratuitement via
**GitHub Pages** à l'adresse https://lesscenarios.fr/. Une édition
est publiée chaque jour, produite automatiquement par une routine planifiée
(voir « Automatisation éditoriale » plus bas).

Aucun backend, aucune base de données : tout est fait de fichiers HTML/CSS/JS
statiques, servis tels quels par GitHub Pages. Le seul service externe utilisé
est **FormSubmit** (formulaire de contact) — voir plus bas. Fichier `.nojekyll`
à la racine (ajouté le 11 août, voir backlog « Technique ») : désactive
explicitement le build Jekyll par défaut de GitHub Pages, pour que ce principe
« servis tels quels » soit réellement garanti, pas juste supposé.

## Backlog

Le backlog (idées, tâches ouvertes, priorités P1-P3) a été déplacé dans un fichier dédié : voir [`docs/BACKLOG.md`](./BACKLOG.md).

## Structure des fichiers

```
index.html              L'édition du JOUR, et seulement elle. Écrasée chaque matin.
archives.html           Liste de toutes les éditions passées (recherche + filtres client-side + résumé dépliable des 3 scénarios par édition).
archives/AAAA-MM-JJ.html Copie figée de chaque édition passée. Jamais remodifiée après publication.
le-projet.html          Page « À propos » : mission, méthode, rythme des 7 jours.
newsletter.html         Page d'inscription à la newsletter quotidienne (Buttondown).
confirmez-votre-email.html  Redirection Buttondown "After subscribing" (avant clic sur le lien de confirmation), ajoutée le 11 août.
bienvenue.html          Redirection Buttondown "After confirming" (inscription validée), ajoutée le 11 août.
contact.html            Formulaire de contact (FormSubmit) + appel à la carte blanche du mardi.
mentions-legales.html   Éditeur, hébergeur, propriété intellectuelle.
politique-de-confidentialite.html  Données collectées (newsletter, contact, mesure d'audience), droits RGPD.
sujets-prioritaires.md  File d'attente éditoriale (voir plus bas).
assets/logo.svg          Logo (3 flèches divergentes = les 3 scénarios).
assets/social/           Image de partage (Open Graph / Twitter Card), statique.
assets/cards/            Images pour la publication Instagram (voir plus bas).
feed.xml / feed.json     Flux consommés par l'automatisation Instagram (voir plus bas).
docs/                    Cette documentation + le prompt de la routine éditoriale.
tools/                   Scripts Node de génération des cartes Instagram.
test/                    Fichier de brouillon/aperçu, non lié au site publié.
```

Chaque page HTML est **autonome** : le CSS est inline dans un `<style>` en tête
de fichier (pas de feuille de style partagée), pour que chaque page — y compris
les archives figées — reste indépendante et ne casse jamais si le design évolue
plus tard. **Ne jamais factoriser ce CSS** sans avoir conscience que ça romprait
cette garantie de stabilité des archives.

## Le gabarit d'édition (`index.html`)

Chaque édition suit une structure fixe (voir `docs/routine-prompt.md` pour le
détail éditorial complet) :
1. **Masthead** — logo, nom, numéro d'édition + date.
2. **Nav** — Accueil / Archives / Le projet / Contact.
3. **Hero** — eyebrow (registre du jour), titre, encart `.question-box`
   (« La question posée »), 4-6 paragraphes de contexte (`.dek`), et un
   `indicator-strip` (indicateurs chiffrés).
4. **Scénarios** — 3 cartes `.card[data-kind=favorable|stable|degrade]`, chacune
   avec une jauge SVG animée (`data-pct`), un mot-repère de probabilité, un titre
   + emoji, un paragraphe d'explication, des indicateurs chiffrés et une ligne
   « Concrètement en France ».
5. **Lexique** — définitions des termes techniques.
6. **Footer** — avertissement sur la nature indicative des probabilités.

Une date de publication (« Publié le … ») est affichée automatiquement sous le
titre : elle est **déduite en JS** de la ligne du bandeau, donc jamais à saisir
à la main.

### Encart liste (`.list-box`) — [AJOUTÉ le 12 août]

Composant CSS pour toute liste mise en avant dans le corps d'un article (top,
calendrier de sorties, classement...), ajouté au gabarit `index.html` à
l'occasion de l'édition du 8 août sur la fréquentation cinéma. **À réutiliser
systématiquement** dès qu'une liste mérite d'être détachée du texte courant —
ne pas revenir à de simples puces `<ul>` dans un `.dek` pour ce cas d'usage.

Même recette visuelle que `.essentiel-box` (fond `--surface`, bordure pleine
dorée, rayon 10px, label en JetBrains Mono majuscules) mais pensée pour des
items scannables plutôt qu'un paragraphe :

```html
<div class="list-box">
  <span class="list-box-label">🏆 Top 10 des entrées 2026, à ce jour</span>
  <ul class="list-box-items">
    <li>
      <span class="list-box-rank">01</span>
      <span class="list-box-body">
        <span class="list-box-title">Marsupilami</span>
        <span class="list-box-meta">6,11 millions d'entrées — sorti le 4 février</span>
      </span>
    </li>
    <!-- ... -->
  </ul>
  <p class="list-box-foot">Note optionnelle sous la liste (ex. classement encore mouvant).</p>
</div>
```

- `.list-box-rank` accepte soit un **numéro** (`01`, `02`...) pour un
  classement, soit un **emoji** pour une liste non ordonnée (calendrier de
  sorties, checklist...) — jamais les deux mélangés dans le même encart.
- `.list-box-title` porte le nom de l'item (film, chiffre, événement...),
  `.list-box-meta` la ligne de détail en dessous (date, source, contexte).
- `.list-box-foot`, optionnel, pour une précision qui s'applique à
  l'ensemble de la liste plutôt qu'à un item (ex. « classement encore
  mouvant, ces films sont encore en salles »).
- Remplace `.dek-list` (tiret doré, liste dense **dans** un paragraphe
  `.dek`, sans encadré) pour toute nouvelle liste — retour utilisateur du
  12 août : design jugé pas assez soigné/cohérent avec le reste du gabarit.
  `.dek-list` reste présent dans quelques éditions passées (9 et 12 août)
  mais ne doit plus être utilisé pour du nouveau contenu.

**Vérification post-ajout (12 août, retour utilisateur « routine copié
collé vérifie ») :** en comparant le `<style>` des archives 09→12 août,
`.dek-list` était bien présente et utilisée le 9, puis **absente du CSS**
(pas juste inutilisée) les 10 et 11 août, avant de réapparaître le 12 —
preuve concrète que le gabarit `index.html` ne recopie pas fiablement une
classe CSS un jour où le contenu ne s'en sert pas, malgré la consigne
« ne jamais changer le CSS ». Correctifs appliqués : règle explicite ajoutée
à l'étape technique 2 de `docs/routine-prompt.md` (recopier le `<style>`
intégralement, sans filtrer sur l'usage du jour) ; `.list-box` confirmée
présente dans le `index.html` courant (vérifié après ce commit). À
recontrôler après quelques éditions sans liste pour confirmer que la classe
survit désormais.

### Encart « Comprendre » (`.comprendre-box`) — [AJOUTÉ le 14 août]

Composant pour donner au lecteur **une** clé de lecture qui change sa
manière de voir le sujet — un mécanisme, une distinction ou une analogie,
jamais une définition (déjà le rôle du lexique). Ajouté à l'occasion de
l'édition du 14 août sur les canicules, pour porter l'idée que les
dépenses climatiques (Fonds vert, adaptation) fonctionnent comme une
économie de guerre : une dépense défensive qui maintient le niveau de vie
actuel plutôt qu'un investissement qui le fait progresser.

Même recette visuelle que `.question-box` (fond `--surface`, filet doré
3px à gauche, radius 4px — plus léger que la bordure pleine 10px de
`.essentiel-box`/`.list-box`, cohérent avec son rôle d'aparté ponctuel
dans le texte plutôt que de bloc de synthèse) :

```html
<div class="comprendre-box">
  <span class="comprendre-label">Comprendre</span>
  <p class="comprendre-lead">Ces dépenses ressemblent à une économie de guerre : elles ne rendent personne plus riche, elles évitent seulement de perdre ce qu'on a déjà.</p>
  <p class="comprendre-text">Climatiser un hôpital, renforcer un réseau électrique : ce n'est pas un investissement qui fait grandir l'économie, comme la formation ou la recherche. C'est une dépense défensive, qui maintient le niveau de vie actuel face à une menace qui, elle, s'aggrave chaque année. Reste que l'arbitrage budgétaire entre ces deux logiques — investir pour faire grandir l'économie, ou dépenser pour la protéger — est souvent difficile à trancher, faute de moyens pour financer les deux à la fois.</p>
</div>
```

- **Optionnel, un focus maximum par édition** — voir `docs/routine-prompt.md`
  pour les critères de sélection du focus et le format strict (lead ≤ 30
  mots, un seul paragraphe ≤ 70 mots). Ne pas en fabriquer un les jours où
  le sujet n'a pas de vrai point de confusion à éclaircir — même risque
  que `.list-box` plaqué sans vraie matrice.
- **Placement appris par l'usage, pas par la conception initiale** : la
  première version (édition du 14 août) avait été placée en fin de
  section, juste avant `indicator-strip`/le titre des scénarios — retour
  utilisateur : ça se lisait comme un ajout secondaire plutôt qu'une
  explication éclairant le texte. Déplacé dans le fil des `.dek`, juste
  après le paragraphe qui introduit le fait justifiant l'analogie. Toujours
  placer ainsi pour les prochaines éditions, pas en bout de bloc.
- **Classe optionnelle, même piège de troncature que `.list-box`/`.dek-list`**
  (voir plus haut) : ajoutée à la liste de classes vérifiées par la routine
  d'inspection (`docs/routine-inspection-prompt.md`, point 1) dès son
  introduction, pour ne pas revivre le même bug de disparition silencieuse
  du `<style>` un jour sans focus « Comprendre ».

### Vignette d'archive (`.entry-thumb`) — [AJOUTÉ le 14 août]

Chaque entrée de `archives.html` porte une petite photo carrée
(`assets/social/archive-thumbs/{date}.jpg`, 144px source, affichée à 56px
— 44px sous 560px), générée par
`scripts/social/generate_archive_thumbnail.py` :

```bash
python3 scripts/social/generate_archive_thumbnail.py --date {AAAA-MM-JJ} --registre {registre}
```

**Source de l'image, jamais une nouvelle recherche Pexels** — même
principe que `fetch_topic_image.py`/`routine-pub-prompt.md` :
1. `assets/social/topic-images/{date}.jpg` si l'édition a une photo de
   sujet retenue (17/22 éditions au 14 août).
2. Sinon `assets/social/pub-photos/{registre}.jpg` — la même banque de
   secours pré-validée qu'utilise déjà la routine Pub (un paysage par
   registre). `culture-francaise`/`culture-internationale` (tags
   historiques) retombent tous les deux sur `culture.jpg`.

Recadrage centré en carré (`ImageOps.fit`, Pillow), export JPEG qualité
72 : quelques Ko par vignette (116 Ko pour les 22 premières réunies) au
lieu des centaines de Ko/plusieurs Mo des sources.

**Disposition : au même niveau que le titre, sur la même ligne.**
`.entry` passe en `flex-direction: row` (`column` à l'origine, avant cet
ajout), `align-items: center` — `.entry-thumb` et un nouveau
`<div class="entry-body">` (qui regroupe `.entry-main` et
`.entry-scenarios`, auparavant enfants directs de `.entry`) sont deux
enfants côte à côte, l'image centrée verticalement sur toute la hauteur
du bloc texte. `alt=""` volontairement vide (le titre adjacent porte déjà
l'information).

**Un premier réglage l'avait empilée au-dessus du texte** (mauvaise
lecture d'un retour utilisateur ambigu — « tu ne peux pas aligner l'image
au texte sinon ça fait gros » lu comme *« ne l'aligne pas »* plutôt que
*« tu n'as pas réussi à l'aligner, et le résultat fait gros »*). Retour
utilisateur explicite juste après : « l'image doit être au même niveau »
— corrigé le 14 août, vérifié en layout réel (bounding box Playwright,
pas juste à l'œil) sur desktop et mobile (380px) avant de repousser.

**Backfill** : les 22 éditions existantes au 14 août ont été traitées en
une passe. 5 d'entre elles (06/08, 04/08, 27/07, 26/07, 18/07) n'avaient
pas de photo de sujet et utilisent la banque de secours par registre.

## Page Archives (`archives.html`)

Chaque entrée de la liste porte un bouton **« Scénarios »** qui déplie, au clic,
un résumé en 1-2 phrases des 3 scénarios de cette édition (favorable / stable /
dégradé), en colonnes sur desktop et empilés sur mobile. Objectif : donner un
aperçu du contenu sans obliger à ouvrir chaque archive. Accordéon en CSS pur
(`grid-template-rows` 0fr → 1fr), sans dépendance JS externe — le clic ne fait
que basculer une classe `is-expanded` sur l'entrée. Ce bloc est indépendant du
système de recherche/filtres (les deux cohabitent sans conflit).

**Pas d'emoji dans ce résumé** (contrairement aux `<h3>` des cartes de
l'édition complète, qui gardent chacun leur emoji propre) : avec plusieurs
éditions listées les unes sous les autres, des emojis différents à chaque
ligne donnaient un effet visuel chargé (« sapin de Noël »). À la place, une
flèche colorée fixe et cohérente sur toute la liste : `↑` vert (favorable),
`→` bleu (stable), `↓` rouge (dégradé) — couleur héritée de la variable CSS
`--accent` déjà posée par `data-kind` sur `.scenario-mini`.

Ajouté depuis la routine quotidienne (voir `docs/routine-prompt.md`, étape
technique 6) : chaque nouvelle édition doit inclure ce bloc dès sa publication,
pas seulement le titre et les tags.

## File éditoriale (`sujets-prioritaires.md`)

Pilote le choix du sujet du jour. Avant l'auto-sélection, la routine lit ce
fichier :
- une ligne non cochée sous **« 🔥 Priorité absolue »** passe avant tout, quel
  que soit le jour ;
- sinon, la première ligne non cochée de la section du **registre du jour**
  (lundi = géopolitique, mardi = carte blanche lecteurs, etc.) est utilisée ;
- une fois traité, le sujet est coché (`- [x]`) automatiquement.

Chaque ligne peut porter une **problématique + 3 scénarios pré-cadrés** en
commentaire HTML (`<!-- ... -->`), pour figer l'angle à l'avance sans que ça
s'affiche sur le site.

**Règle d'or**, rappelée en tête du fichier : tout sujet doit être une
problématique à **issue ouverte**, tranchable en 3 scénarios chiffrés — jamais
un trait permanent ou un fait déjà acquis.

## Règle emoji (ajoutée le 14 août, retour utilisateur)

Retour utilisateur direct : « ce que je n'aime pas ce sont les emojis, ça
manque de sérieux ». Décision, appliquée aux **futures** éditions/pages
uniquement — jamais retouchée rétroactivement sur les archives déjà
publiées (même logique que le changement de style des pastilles
`.kind-tag`, voir plus bas) :

- **Supprimés (décoratif, aucune fonction)** : l'emoji devant chaque
  `<h3>` de carte scénario (`docs/routine-prompt.md` étape 4) ; le ❓
  devant la question dans `.question-box` (le label « La question
  posée » suffit) ; l'emoji de repère dans `.list-box-rank` (toujours un
  numéro désormais) ; l'emoji d'ouverture du teaser dans `<comments>`/
  `<description>` de `feed.xml` et de `feed-suivi.xml`.
- **Gardés, usage volontairement restreint** : 👉 uniquement devant un
  vrai lien d'appel à l'action (s'abonner, lire l'article) — repère de
  navigation fonctionnel, pas une décoration.
- **Gardés, cas à part** : le code couleur 🟢/🔵/🔴 du `<category>` de
  `feed.xml` (options du sondage Telegram) — équivalent fonctionnel du
  point coloré `.kind-tag` sur le site, seul moyen de distinguer les 3
  options par couleur dans l'UI d'un sondage Telegram (pas de CSS
  possible) ; le tag "🔄 Suivi mis à jour" sur les images de suivi/pub
  (icône de badge, pas un emoji noyé dans une phrase — voir
  `scripts/social/suivi-template.html`).

`docs/routine-hebdo-prompt.md` avait déjà cette règle depuis le 3 août
(« pas d'emoji décoratif superflu, pas de "Salut 👋" ») — cohérent avec
le reste du site, pas un changement pour ce fichier-là.

## Automatisation éditoriale (la routine quotidienne)

Une **routine planifiée** (Claude Code Remote, nommée « Scénario »,
`trig_0176spj7P7E9fyTs1XBkQBWF`) se déclenche chaque jour à **7h00 heure de
Paris** (`0 5 * * *` en UTC — ⚠️ à ajuster de ±1h lors des changements
d'heure hiver/été, le cron ne s'ajuste pas tout seul). **Avancée de 7h15 à
7h00 le 10 août** (décision utilisateur).

Elle exécute le prompt archivé dans `docs/routine-prompt.md` : sélection du
sujet (étape 0 → file prioritaire, sinon auto-sélection par registre),
recherche et vérification factuelle (2 sources croisées minimum), rédaction,
remplissage du gabarit, écrasement d'`index.html`, création de l'archive
figée, mise à jour d'`archives.html`, puis `git commit` + `git push` direct
sur `main` (pas de pull request).

**Mode pointeur depuis le 14 août** (retour utilisateur : trop de
copier-coller manuel à chaque évolution du prompt). Jusque-là, le texte
complet de `docs/routine-prompt.md` était collé en dur dans le trigger —
toute évolution de la routine demandait un aller-retour manuel dans
l'interface Claude Code Remote, en plus du commit du fichier. Le trigger
contient désormais un court prompt fixe (~1 Ko, mêmes 5 étapes que le
prompt-pointeur de l'Inspecteur ci-dessous) qui se contente de faire
`git pull origin main` puis de lire et appliquer `docs/routine-prompt.md`
dans son intégralité. **`docs/routine-prompt.md` est donc la source de
vérité vivante** : un commit + push sur `main` suffit à changer le
comportement de la routine dès sa prochaine exécution, plus de
copier-coller après la bascule initiale.

**Limite vérifiée le 14 août** : `trig_0176spj7P7E9fyTs1XBkQBWF` a été créé
via l'API HTTP, pas par un agent (`create_trigger`) — `update_trigger` y
est refusé pour tout agent (message exact : *« this routine was created
via "http_api", not by an agent »*). La bascule initiale vers le mode
pointeur, et toute future modification du texte fixe du pointeur
lui-même (pas du contenu qu'il pointe), reste donc un geste manuel de
l'utilisateur dans l'interface — rare, puisque les règles éditoriales et
techniques ordinaires vivent désormais entièrement dans
`docs/routine-prompt.md`.

## Branches Git

- `main` — branche servie par GitHub Pages, toujours à jour.
- `claude/zen-hawking-m951cj` — branche de développement des sessions Claude
  Code. À chaque publication, `main` est **fast-forwardé** sur cette branche
  (jamais de merge divergent), donc les deux restent strictement identiques.

## Automatisation Instagram (cartes + flux)

**Objectif** : publier chaque jour un post Instagram qui tease l'édition
(question + 3 scénarios, sans les probabilités) et renvoie vers le site via le
lien en bio — sans jamais dévoiler les chiffres, pour inciter au clic.

- `tools/gen_single.js` — génère une carte unique 1080×1080 (HTML → capture
  Chromium headless) : question + 3 scénarios teasés + CTA « lien en bio,
  gratuit ». C'est la carte utilisée par l'automatisation (une seule image,
  compatible avec un flux RSS classique).
- `tools/gen_teaser.js` — variante en 3 cartes (carrousel : question / 3
  scénarios / CTA), pour une publication manuelle plus riche si besoin.
- `assets/cards/AAAA-MM-JJ/` — archive datée des cartes du jour.
- `assets/cards/latest/` — **URL fixes** (mêmes noms de fichiers chaque jour),
  écrasées quotidiennement. Utile pour brancher un outil externe une seule
  fois sans avoir à changer l'URL chaque jour.
- `feed.xml` — flux RSS (image en `<enclosure>`, légende en description),
  consommable par un outil d'automatisation pour poster sans intervention
  manuelle.
- `feed.json` — même contenu en JSON, pour un usage type Make/webhook.

**État au 29 juillet 2026** : la génération des **cartes image** n'est **pas
encore branchée dans la routine quotidienne** — c'est fait manuellement pour
l'instant, donc pas d'image dans `feed.xml` (`<enclosure>` absent). En
revanche, **la mise à jour texte de `feed.xml` fait maintenant partie du
prompt de la routine** (nouvel item ajouté chaque jour : titre, lien, date,
description au format teaser) — voir `docs/routine-prompt.md`, étape technique
7. Ce même flux alimente désormais la **newsletter** (Buttondown, RSS-to-email,
plan payant) en plus d'Instagram.

**[EN COURS le 11 août] Image visible dans la newsletter Buttondown —
deux tentatives, aucune concluante pour l'instant.** Constat de
l'utilisateur : rien ne garantissait que l'image Instagram (portée par
`<enclosure>` depuis le 7-9 août) s'affiche réellement dans l'email envoyé
par Buttondown — utile seulement à Make/Instagram jusque-là.

**Tentative 1 — éditeur du corps d'email.** Vérification d'abord tentée via
la documentation officielle Buttondown, bloquée depuis cet environnement à
ce moment-là (`docs.buttondown.com`/`buttondown.com` inaccessibles). Test
réel fait par l'utilisateur dans l'éditeur du corps d'un email ponctuel :
le tag `{% if item.enclosure %}` était déjà présent, vide, dans le gabarit
par défaut, mais coller `<img src="{{ item.enclosure.url }}">` dans ce
champ ne l'affichait pas — l'éditeur du corps d'un email est un champ de
texte enrichi qui affiche le HTML tapé à la main tel quel (texte littéral),
sans l'interpréter.

**Tentative 2 — `<img>` dans le CDATA de `<description>`.** Solution de
repli : balise `<img>` mise directement dans le CDATA de `<description>`
de `feed.xml`, en tout premier élément, même URL que l'`<enclosure>` de
l'`<item>` — ce chemin étant confirmé interprété comme HTML par Buttondown
(comme les `<br>` déjà présents). Documenté dans `docs/routine-prompt.md`,
étape technique 8.

**Correctif à la tentative 1, l'après-midi même** : `docs.buttondown.com`
exceptionnellement accessible depuis cette session — doc officielle
consultée directement. La vraie syntaxe est `{{ item.enclosure }}` (l'URL
directement, `item.enclosure.url` n'existe pas) et le bon endroit est le
**template RSS-to-email** dédié, un écran distinct de l'éditeur du corps
d'un email ponctuel testé en tentative 1. Réappliqué au bon endroit avec
la bonne syntaxe — **toujours rien affiché**, résultat identique à la
tentative 2.

**Diagnostic retenu : les deux tentatives ont probablement échoué pour la
même raison, indépendante de leur contenu.** L'édition du 11 août (`guid
scenario-2026-08-11`) avait déjà été traitée/envoyée par Buttondown avant
que l'une ou l'autre tentative n'existe — Buttondown semble se fier au
`<guid>` pour détecter la nouveauté d'un item, pas au contenu réellement
présent dans le flux à l'instant où on le relit. Modifier après coup le
contenu d'un item déjà vu n'a donc aucune chance de changer quoi que ce
soit à un envoi déjà parti. Ni la syntaxe du template ni l'approche CDATA
ne sont donc invalidées par ce test — juste non concluantes. Suivi complet
dans le backlog « Distribution / automatisation », entrée « Image en tête
de la newsletter Buttondown ».

## Image de partage (Open Graph / Twitter Card)

`assets/social/og-image-v2.png` (2508×1412) est l'image affichée en aperçu
quand un lien Scénario est partagé sur Slack, WhatsApp, X/Twitter,
LinkedIn, Facebook, iMessage, etc. Statique et identique sur toutes les
pages — contrairement aux cartes Instagram, elle ne change pas chaque jour.

**Refondue le 4 août** (retour utilisateur : l'ancienne version — photo IA
d'une route au coucher de soleil + légende en petit texte — devenait
illisible une fois réduite à la taille réelle d'une vignette de partage).
Nouvelle version en format "poster", construite en HTML/CSS et capturée via
Playwright (même méthode que la bannière LinkedIn, sans outil de design
payant) : logo (le tronc doré qui se divise en trois flèches, repris tel
quel de `assets/logo.svg`), wordmark "Scéna**rio**" en très grand, slogan
"L'avenir en 3 scénarios." et la légende Favorable/Stable/Dégradé avec les
mêmes flèches que le reste du site (↑/→/↓). Chaque itération vérifiée par
export en miniature 320px et 160px avant validation, pour s'assurer que le
texte reste lisible même tout petit — c'était justement le défaut de
l'ancienne version. Fichier aussi ~6x plus léger (1,7 Mo → ~260 Ko, aplats
de couleur plutôt qu'une photo). Source HTML de travail non conservée dans
le dépôt (fichier temporaire de session) — à refaire à l'identique si besoin
d'un futur ajustement, en repartant des couleurs/polices déjà documentées
dans ce fichier (`--gold`, `--favorable`/`--stable`/`--degrade`, Fraunces +
JetBrains Mono).

**Renommée `og-image.png` → `og-image-v2.png` le 6 août** (bug confirmé :
Telegram affichait encore une version très ancienne de l'image sur une
édition jamais partagée avant). Cause : certaines plateformes mettent en
cache l'URL de l'IMAGE elle-même, indépendamment de la page qui la
référence — tant que le nom de fichier ne change pas, une plateforme qui a
déjà vu cette URL une fois ne la re-télécharge jamais, même après une refonte
complète du visuel. Le contenu de l'image n'a pas changé lors de ce
renommage, seul le nom de fichier a changé (et les ~14 pages HTML qui le
référencent), pour forcer tous les caches plateforme à repartir de zéro.
**Règle à suivre pour tout futur remplacement visuel de cette image** :
toujours changer le nom de fichier (`v3`, `v4`, ...) en même temps que le
contenu, jamais réutiliser le même nom — sinon le même bug de cache se
reproduira. Limite connue : ce renommage ne corrige que les partages
FUTURS ; un lien déjà partagé (ex. un message Telegram déjà envoyé) garde
l'aperçu qu'il avait au moment du partage, il n'y a pas de correction
rétroactive possible côté Scénario (Facebook propose un « Sharing Debugger »
et LinkedIn un « Post Inspector » pour forcer un rafraîchissement au cas par
cas ; Telegram n'a pas d'équivalent public).

Les balises `og:*` et `twitter:*` sont posées dans le `<head>` des 5 pages
vivantes (`index.html`, `archives.html`, `le-projet.html`, `contact.html`,
`newsletter.html`), chacune avec son propre `og:title`/`og:description`
repris du `<title>`/`<meta name="description">` de la page, mais la même
image partout. **Correction du 4 août** : sur `index.html` (l'édition du
jour), ces balises doivent être mises à jour à chaque édition pour
refléter le sujet du jour — voir étape 3bis de `docs/routine-prompt.md`.
Une ancienne version de cette doc affirmait à tort que ces balises ne
changeaient jamais ; en pratique elles étaient restées au tagline
générique sur toutes les éditions jusqu'au bug découvert ce jour-là (carte
LinkedIn générique au lieu du titre réel). Sur les 4 autres pages vivantes
(pages fixes, pas d'édition quotidienne), les balises restent bien
statiques, aucune instruction de routine nécessaire pour elles.

**Piste future** : des images de partage spécifiques à chaque édition (avec
le titre du jour incrusté) seraient possibles en réutilisant le pipeline déjà
construit pour les cartes Instagram (`tools/gen_single.js`), mais ce n'est pas
fait — chaque édition partage aujourd'hui la même image générique.

## Formulaire de contact

`contact.html` utilise **FormSubmit** (service gratuit tiers, sans backend à
héberger) : le formulaire poste vers `formsubmit.co/<alias>`, qui relaie par
email. Envoi en **AJAX** (`fetch` vers `formsubmit.co/ajax/<alias>`) pour que
le visiteur reste sur `lesscenarios.fr` au lieu d'être redirigé
vers une page FormSubmit externe. Un lien `mailto:` reste en repli.
L'alias anonyme (plutôt que l'adresse email en clair) évite l'exposition aux
robots spammeurs.

## Mesure d'audience

**GoatCounter** (gratuit, sans cookies, donc pas de bandeau de consentement
RGPD requis) — compte `scenario` (scenariocontact75@gmail.com), tableau de
bord sur `scenario.goatcounter.com`. Le script de suivi est posé juste avant
`</body>` sur les 5 pages vivantes (`index.html`, `archives.html`,
`le-projet.html`, `newsletter.html`, `contact.html`) :

```html
<script data-goatcounter="https://scenario.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
```

Comme la routine quotidienne recopie `index.html` comme gabarit chaque matin,
ce script se retrouve automatiquement dans chaque nouvelle édition — même
mécanisme que les balises Open Graph, aucune instruction supplémentaire
nécessaire dans `docs/routine-prompt.md`. Les archives déjà publiées avant
cet ajout n'ont pas été modifiées (changement d'infrastructure mineur, pas
crucial rétroactivement).

**[FAIT le 21 août] Compteur de lecture par article ("Lu X fois"), demande
utilisateur directe.** Idée initiale : Google Search Console — écartée
après réflexion (ne compte que les clics venant de la recherche Google,
pas Telegram/newsletter/réseaux qui sont les principaux canaux du site ;
décalage de plusieurs jours ; aucun accès API disponible dans la session).
**GoatCounter, déjà en place pour la mesure d'audience générale (voir
ci-dessus), a un mécanisme fait pour exactement ce besoin** : un compteur
public par chemin, `https://scenario.goatcounter.com/counter/{chemin}.json`
→ `{"count": "...", "count_unique": "..."}`, utilisable directement en JS
côté client, sans clé API, cohérent avec le principe zéro-backend du site.
Ce compteur public est **désactivé par défaut** (403 *"Need to enable the
'allow using the visitor counter' setting"*) — activé manuellement par
l'utilisateur le 21 août dans `scenario.goatcounter.com` → Settings, testé
et confirmé fonctionnel après coup (ex. `archives/2026-08-18.html` → 2
lectures au moment du test).

**Implémentation** : le script existant qui construit `.pubdate` (déjà
présent sur chaque édition — voir le mécanisme "Publié le {date} · ~{N}
min de lecture" documenté dans `docs/routine-prompt.md` de facto via le
gabarit, pas une instruction écrite séparément) reçoit un second appel
`fetch` asynchrone qui va chercher `{count}` sur le chemin exact de la
page courante et l'ajoute en troisième segment, même séparateur (" · ") :
"Publié le 17 août 2026 · ~4 min de lecture · Lu 2 fois". Rien affiché si
la requête échoue ou si `count` vaut 0 (page trop récente, pas encore de
visite) — pas de "Lu 0 fois" trompeur sur une édition qui vient de
sortir. Utilise `count` (nombre total de vues), pas `count_unique`
(visiteurs uniques) : plus proche du sens littéral "lu X fois". Appliqué
à `index.html` et aux 26 archives existantes au moment de l'ajout (deux
variantes de script legacy selon l'ancienneté de la page — voir
historique du "temps de lecture" — les deux ont reçu le même ajout), puis
complété sur les 3 archives publiées sur `main` entre-temps
(2026-08-19/20/21) au moment du merge. Comme pour le script de suivi
GoatCounter lui-même, ce bloc fait partie du gabarit recopié chaque
matin : aucune instruction supplémentaire nécessaire dans
`docs/routine-prompt.md` pour que les futures éditions l'aient
automatiquement. **Périmètre volontairement limité aux éditions
quotidiennes** (`index.html`/`archives/*.html`) — pas étendu à
`suivi/*.html` ni `hebdo/*.html`, structure de page différente, à faire
séparément si le besoin se confirme.

**Correction le 21 août, même jour — biais `index.html` vs
`archives/{date}.html`, repéré par l'utilisateur.** La version initiale
utilisait `location.pathname` pour construire le chemin interrogé —
correct sur une page d'archive (chemin stable, propre à cet article),
mais faux sur `index.html` : ce chemin (`/` ou `/index.html`) est
**le même tous les jours**, donc son compteur GoatCounter cumule le
trafic de la page d'accueil depuis le tout début du site, pas seulement
celui de l'édition du jour — testé : 121 vues sur `/` contre 105 sur
`/index.html`, deux chemins déjà distincts entre eux, et aucun des deux
propre à un seul article. **Première piste envisagée et rejetée** :
sommer les 3 compteurs (`/`, `index.html`, `archives/{date}.html`) —
rejetée par l'utilisateur avant implémentation, à raison : ça aurait
additionné l'historique complet de la page d'accueil (tous les articles
jamais publiés) au compteur d'un seul article, une **sur-estimation**
massive plutôt qu'une correction. **Solution retenue** : chaque page du
site porte déjà une balise `<link rel="canonical" href="https://
lesscenarios.fr/archives/{date}.html">` pointant vers l'URL permanente de
l'article — y compris `index.html`, dont le canonical pointe vers
l'archive du jour, pas vers lui-même. Le script lit ce chemin canonique
plutôt que `location.pathname` (repli sur `location.pathname` uniquement
si la balise est absente, cas qui ne devrait jamais arriver vu qu'elle
est déjà systématique sur le site). Résultat : `index.html` et
`archives/{date}.html` affichent désormais toujours le même chiffre,
celui de l'URL permanente de l'article — reste un léger sous-comptage du
trafic homepage/bookmark direct (non rattrapable rétroactivement, l'API
GoatCounter ne donne qu'un total cumulé par chemin, pas de répartition
par date), mais plus aucune pollution croisée entre articles. Corrigé
sur les 30 fichiers concernés (`index.html` + 29 archives) avant même le
premier passage en production de la version bugguée.

**[FAIT le 21 août] Graphique de croissance de l'audience sur
`le-projet.html`, demande utilisateur directe.** Nouvelle section
`#audience`, juste avant le bloc "Nous suivre" (preuve de croissance
concrète juste au-dessus de l'appel à s'abonner) — courbe en escalier des
lectures d'éditions cumulées depuis le lancement, réutilisant le composant
`.dc-chart-box` (voir `docs/routine-prompt.md`, section "Horloge de
l'Apocalypse") en **variante "favorable"** (bordure/couleur vertes plutôt
que `--degrade`, la série est positive ici, pas alarmante).

**Périmètre : lectures d'éditions uniquement, pas le trafic total du
site.** Décidé avec l'utilisateur après avoir vérifié les deux options : le
total site (`/api/v0/stats/total`) mélange les pages fonctionnelles
(contact, inscription newsletter, `le-projet.html` lui-même) avec les
vraies lectures d'articles — moins honnête que ce que la section prétend
montrer ("l'audience qui lit Scénario"). Calcul : chemins `/api/v0/paths`
filtrés sur `^/archives/(\d{4}-\d{2}-\d{2})\.html(\?.*)?$`, variantes avec
query string (ex. `?trk=feed_main-feed-card_...`, ajoutée par certains
liens entrants) regroupées avec le chemin propre du même article plutôt que
comptées séparément — sinon sous-comptage silencieux, même famille de biais
que celui corrigé plus haut sur `index.html`.

**Source des données : l'API authentifiée GoatCounter, pas le compteur
public.** Le compteur public utilisé pour le "Lu X fois" par article (voir
plus haut) ne donne qu'un total cumulé instantané, sans historique — inutile
pour reconstruire une courbe dans le temps. L'utilisateur a généré un token
API (lecture seule, `[Username] → API` sur `scenario.goatcounter.com` — pas
sous "Paramètres" comme deviné à tort deux fois de suite avant vérification
via la doc officielle, https://www.goatcounter.com/help/api). **Le token
n'est stocké nulle part dans ce dépôt** (public, servi par GitHub Pages) :
il vit uniquement dans le prompt du trigger CCR "Scénario — Audience",
configuration privée côté Claude Code Remote. Testé en direct avant
implémentation : historique réel disponible depuis le tout premier hit du
site, 2026-07-29 — pas besoin d'attendre des semaines pour une courbe
parlante, `/api/v0/stats/hits` donne un vrai cumul jour par jour depuis le
lancement (1 lecture le 30 juillet → 181 le 21 août, premier jeu de
données utilisé).

**Nouvelle routine hebdomadaire** — trigger "Scénario — Audience", prompt
de référence `docs/routine-audience-prompt.md` (même principe que les
autres routines : fichier public = toute la logique, sauf le token,
uniquement dans la config privée du trigger). Régénère le tableau `data`/
`xLabels` du script `#audience-svg` et le texte associé (chiffre en gras,
`.dc-chart-lead`, `aria-label`, label du dernier point) à chaque passage —
ne touche jamais au CSS ni à la structure de la section. Vérification
visuelle Playwright recommandée à chaque passage (composant déjà en place,
mais un chevauchement de labels reste possible si la série s'accélère).

## Ce qui reste à faire (suivi)

Cette section a été déplacée dans [`docs/BACKLOG.md`](./BACKLOG.md), à la suite du Backlog.
