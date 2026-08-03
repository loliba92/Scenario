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
est **FormSubmit** (formulaire de contact) — voir plus bas.

## Structure des fichiers

```
index.html              L'édition du JOUR, et seulement elle. Écrasée chaque matin.
archives.html           Liste de toutes les éditions passées (recherche + filtres client-side + résumé dépliable des 3 scénarios par édition).
archives/AAAA-MM-JJ.html Copie figée de chaque édition passée. Jamais remodifiée après publication.
le-projet.html          Page « À propos » : mission, méthode, rythme des 7 jours.
newsletter.html         Page d'inscription à la newsletter quotidienne (Buttondown).
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

## Automatisation éditoriale (la routine quotidienne)

Une **routine planifiée** (Claude Code Remote, nommée « Scénario »,
`trig_0176spj7P7E9fyTs1XBkQBWF`) se déclenche chaque jour à **7h15 heure de
Paris** (`15 5 * * *` en UTC — ⚠️ à ajuster de ±1h lors des changements
d'heure hiver/été, le cron ne s'ajuste pas tout seul).

Elle exécute le prompt archivé dans `docs/routine-prompt.md` : sélection du
sujet (étape 0 → file prioritaire, sinon auto-sélection par registre),
recherche et vérification factuelle (2 sources croisées minimum), rédaction,
remplissage du gabarit, écrasement d'`index.html`, création de l'archive
figée, mise à jour d'`archives.html`, puis `git commit` + `git push` direct
sur `main` (pas de pull request).

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

## Image de partage (Open Graph / Twitter Card)

`assets/social/og-image.png` (1672×941, généré par IA puis retouché à la main)
est l'image affichée en aperçu quand un lien Scénario est partagé sur
Slack, WhatsApp, X/Twitter, iMessage, etc. Statique et identique sur toutes
les pages — contrairement aux cartes Instagram, elle ne change pas chaque
jour.

Les balises `og:*` et `twitter:*` sont posées dans le `<head>` des 5 pages
vivantes (`index.html`, `archives.html`, `le-projet.html`, `contact.html`,
`newsletter.html`), chacune avec son propre `og:title`/`og:description`
repris du `<title>`/`<meta name="description">` de la page, mais la même
image partout. Ces balises font partie du gabarit préservé par la routine
quotidienne (elles ne changent jamais, comme le `<title>` et la description) —
aucune instruction supplémentaire nécessaire dans `docs/routine-prompt.md`.

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

## Ce qui reste à faire (suivi)

Voir les échanges de session pour le détail, mais en résumé :
- **Emails de la newsletter qui arrivent en spam — corrigé le 30 juillet.**
  Constaté le 30 juillet (premier envoi réel automatisé) : plusieurs abonnés
  recevaient l'édition dans leurs indésirables plutôt qu'en boîte de
  réception. Corrections apportées :
  - Domaine d'envoi dédié `newsletter.lesscenarios.fr` connecté à Buttondown
    en **Managed setup** (DNS délégué via 2 enregistrements NS ajoutés côté
    OVH) — Buttondown gère depuis l'authentification complète (SPF, DKIM,
    DMARC) de ce sous-domaine.
  - **Reply-to** configuré vers `scenariocontact75@gmail.com`, pour que les
    réponses des lecteurs arrivent réellement quelque part (l'adresse
    d'envoi elle-même ne reçoit aucun courrier entrant).
  - Réputation d'expéditeur encore neuve (compte tout juste créé) — continue
    de s'améliorer naturellement avec le temps et les ouvertures/clics des
    abonnés, indépendamment de ce qui précède.
  - **Confirmé fonctionnel le 31 juillet** : l'édition du jour envoyée
    correctement depuis `contact@lesscenarios.fr`.
- **LinkedIn et Instagram — à configurer correctement pour générer du trafic.**
  Reprise en main le 30 juillet, après constat que rien n'était vraiment
  actif :
  - **LinkedIn** : l'intégration native Buttondown (auto-partage à chaque
    envoi) ne fonctionne qu'avec un profil **personnel**, pas une Page
    Entreprise (confirmé via `docs.buttondown.com/linkedin`). Solution
    retenue : profil personnel renommé "Les Scenarios" (Suresnes,
    Île-de-France), connecté à l'intégration Buttondown, avec un résumé
    ("About") réécrit expliquant la genèse et le principe du projet.
    **Testé le 31 juillet (envoi du jour) : toujours pas de post créé
    automatiquement.** **Cause identifiée le 31 juillet (réponse du support
    Buttondown, Anita)** : connecter l'intégration LinkedIn ne suffit pas à
    déclencher l'auto-partage — il faut configurer une **Automation**
    dédiée (`buttondown.com/automations`), fonctionnalité réservée au plan
    **Standard** (26 $/mois, jugé trop cher pour ce besoin).
    **Solution retenue et fonctionnelle depuis le 31 juillet : Make.com**
    (plan gratuit, ~30-60 opérations/mois avec une vérification 1x/jour à
    10h Paris plutôt qu'un intervalle court — un polling toutes les 15 min
    aurait consommé ~1440 opérations/mois, largement au-dessus du quota
    gratuit de 1000 : Make compte une opération à **chaque vérification**,
    même sans nouvel item).

    **Scénario Make final** : module **RSS** ("Watch RSS feed items", URL
    `https://lesscenarios.fr/feed.xml`, 1 item max, déclenché **"From now
    on"** pour ne traiter que les futures éditions, jamais l'historique) →
    module **LinkedIn "Create a Company Text Post"**, posté sur la **Page
    LinkedIn "Scenario"** (pas le profil personnel "Les Scenarios", non
    utilisé pour cet automatisme) :
    - **Content** : une simple phrase fixe d'intro ("🔥 Nouvelle édition
      Scénario, à lire 👇") — le reste de l'info est porté par la carte Article
      ci-dessous, pas la peine de dupliquer titre/lien dans le texte.
    - **Media Type = Article**, avec **Link → URL** = champ `URL` du flux,
      **Link → Title** = champ `Title`, **Link → Description** = champ
      `Comments` (voir plus bas). Thumbnail laissé vide (LinkedIn récupère
      l'image Open Graph du site automatiquement).
    - Le champ `Description` brut du flux RSS n'est **jamais** utilisé
      directement (pensé pour l'email : contient des `<br>` non interprétés
      par LinkedIn et une invitation à répondre à un email qui n'a pas de
      sens hors contexte email).
    - **Point d'attention Make découvert en session** : le module RSS
      générique ne reconnaît que les champs standards RSS 2.0 + deux
      extensions prédéfinies (Google Merchant Center, iTunes) — impossible
      d'exposer un champ personnalisé arbitraire (on a testé un
      `<scenario:teaser>` avec namespace dédié : jamais détecté par Make).
      Solution : détourner le champ standard **`<comments>`** (prévu à
      l'origine pour un lien vers une page de commentaires) pour y mettre
      en texte brut la question posée du jour — Make le reconnaît nativement,
      aucune config supplémentaire. Voir `docs/routine-prompt.md`, étape
      technique 8, et la nouvelle règle éditoriale de l'étape 2 : **la
      question posée est rédigée une seule fois puis réutilisée mot pour
      mot** dans l'encart du site, `<comments>`/`<description>` de
      `feed.xml`, et le teaser Telegram — jamais reformulée différemment
      d'un endroit à l'autre. Les 4 items déjà publiés au 31 juillet ont été
      corrigés a posteriori dans `feed.xml` pour respecter cette règle
      (leur `<comments>` avait dérivé de la vraie question affichée sur le
      site).
    - Autre règle ajoutée : **le h1 (titre) et la question posée ne
      doivent jamais être une simple reformulation l'un de l'autre** —
      constaté sur l'édition du 27 juillet (Iran/USA) où les deux étaient
      quasi identiques, redondant une fois affichés l'un après l'autre sur
      LinkedIn.
    - **Piège de test à connaître** : la fonction "Rerun/Replay" de
      l'historique Make **rejoue les données figées au moment de la
      capture initiale** — si le champ `comments` n'existait pas encore
      dans `feed.xml` à ce moment-là, le replay l'affiche vide même après
      correction du flux et de la config. Seul un **vrai nouveau passage
      RSS** (nouvel item jamais vu) reflète la configuration actuelle. Un
      flux de test jetable (`feed-test.xml`, supprimé après usage) a servi
      à valider ça sans attendre le lendemain ni polluer la vraie newsletter.
    - Le scénario Make doit rester **activé** pour continuer à tourner
      automatiquement.
    - **Idée notée le 31 juillet, pas encore implémentée** : faire porter
      le sondage Telegram sur le sujet du **lendemain** plutôt que sur
      celui du jour même, pour créer un effet d'attente ("reviens demain
      voir si tu avais raison") au lieu d'un vote juste avant la révélation
      immédiate des probabilités. Frein principal : la routine ne connaît
      le sujet du lendemain à l'avance que les jours où il est déjà
      pré-cadré dans `sujets-prioritaires.md` (avec ses 3 scénarios), pas
      les jours d'auto-sélection dynamique — donc pas systématiquement
      applicable en l'état.
    - **Idée notée le 31 juillet, pas encore implémentée** : ajouter X
      (Twitter) comme canal supplémentaire, toujours via Make.com, sur le
      même principe que LinkedIn (même module RSS `feed.xml` en entrée).
      Différences à anticiper avant de configurer : (1) connexion X dans
      Make nécessite un compte développeur X (gratuit, "Free tier", ~500
      posts/mois — largement suffisant pour 1 post/jour), contrairement à
      LinkedIn qui se connecte directement avec le compte perso ; (2) limite
      de 280 caractères impose un format court dédié (titre + lien, sans la
      description longue utilisée pour LinkedIn) ; (3) pour économiser les
      opérations Make (quota gratuit 1000/mois), privilégier un seul
      scénario avec deux sorties (LinkedIn + X) branchées sur le même
      déclencheur RSS plutôt que dupliquer la lecture du flux.
  - **Identité visuelle de la Page LinkedIn "Scenario"** (id `136694258`)
    faite le 31 juillet, gratuitement (généré en HTML/CSS + capture
    Playwright, sans outil de design payant), en reprenant fidèlement les
    couleurs/polices du site (Fraunces + JetBrains Mono, `--gold`,
    `--favorable`/`--stable`/`--degrade`) et le mark existant
    (`assets/logo.svg`, le tronc doré qui se divise en trois flèches) :
    - Bannière 1128×191, contenu volontairement recentré avec de vraies
      marges (le premier essai était trop proche des bords et empiétait
      sur la zone où le logo rond de la page se superpose en bas à gauche).
    - Logo carré (300×300, spec officielle LinkedIn) basé sur le mark
      existant du site.
    - Texte de la section "Vue d'ensemble" (About, 2000 caractères max)
      rédigé dans la même voix que `le-projet.html` (aucune ligne
      éditoriale, sources croisées, Olivier Bertrand).
    - **Lien "LinkedIn ↗" ajouté au footer des 5 pages vivantes**
      (`index.html`, `archives.html`, `le-projet.html`, `contact.html`,
      `newsletter.html`), juste à côté du lien Telegram, vers
      `linkedin.com/company/136694258/`. Comme pour Telegram, ce lien fait
      partie du gabarit recopié chaque matin par la routine — aucune
      instruction supplémentaire nécessaire dans `docs/routine-prompt.md`
      pour le préserver. Non ajouté aux pages `archives/*.html` figées,
      cohérent avec le choix déjà fait pour Telegram.
- **Telegram — canal créé le 31 juillet.**
  Canal public `@scenario_fr`, bot `@scenario_fr_bot` créé via BotFather et
  ajouté comme administrateur (droit "Publier des messages"). Test manuel
  d'envoi réussi le 31 juillet (`sendMessage` + `sendPoll` via l'API
  Telegram, appelée à la main par l'utilisateur — pas depuis une session
  Claude Code Remote).
  **Panne découverte le 1er août** : la routine avait été configurée pour
  appeler l'API Telegram directement en `curl` depuis sa propre session
  (ancienne étape technique 9). Résultat : **aucun message n'est jamais
  parti**, silencieusement — `api.telegram.org` s'est révélé **bloqué par
  la politique réseau (egress) de l'environnement Claude Code Remote**
  utilisé par le trigger « Scénario » (confirmé en reproduisant l'appel :
  `CONNECT api.telegram.org:443` → `403 Forbidden` côté proxy de
  l'environnement, "policy denial"), et ce indépendamment du bon
  paramétrage de `TELEGRAM_BOT_TOKEN`. La consigne de ne jamais bloquer la
  publication principale en cas d'échec masquait le problème : l'édition
  partait normalement, seul le Telegram échouait en silence.
  **Solution retenue le 1er août : basculer sur Make.com**, exactement
  comme pour LinkedIn (voir plus haut) — modules natifs **"Telegram Bot"**
  (Send a Text Message + Create a Poll), branchés sur le même module RSS
  `feed.xml` déjà utilisé pour LinkedIn (un seul scénario Make, deux
  sorties). L'appel API part alors depuis l'infrastructure de Make, non
  soumise à la restriction réseau de l'environnement Claude Code Remote.
  L'ancienne étape `curl` a été retirée de `docs/routine-prompt.md` (étape
  technique 9 réécrite) : la routine n'a plus rien à faire pour Telegram,
  Make s'en charge dès qu'un nouvel item apparaît dans `feed.xml`.
  **Fait et vérifié le 1er août — pipeline Telegram opérationnel via Make.**
  Deux modules ajoutés à la suite du RSS dans le même scénario Make que
  LinkedIn :
  - **Telegram Bot → "Send a Text Message"** : `Chat ID` = `@scenario_fr`,
    `Text` = `Title` + `Comments` + lien `URL`, connexion créée avec le
    token du bot (`TELEGRAM_BOT_TOKEN`, collé une fois dans Make — pas de
    problème réseau côté Make, contrairement à cette session).
  - **Telegram Bot → "Make an API Call"** (pas de module natif "Create a
    Poll" dans le connecteur Telegram de Make, malgré ce que l'API
    Telegram permet) : `URL Method` = `sendPoll`, `Method` = `POST`,
    `Body Type` = Map Body, avec un **Body composé à la main** :
    `{"chat_id": "@scenario_fr", "question": "À ton avis, quel scénario l'emporte ?", "options": ["{{category}}"], "is_anonymous": true}`.
  - **Piège découvert en configurant `options`** : Make **ne récupère
    qu'une seule occurrence** d'un champ RSS répété (`<category>` mis 3
    fois dans le même item) au lieu d'un tableau de 3 — confirmé avec un
    flux de test 100% frais, donc pas un souci de cache. Insérer
    directement le champ tableau (`Categories[]`) brut dans le JSON du
    Body ne fonctionne pas non plus : Make le sérialise en texte simple
    séparé par des virgules, pas en tableau JSON valide (`can't parse
    options JSON object`), et la fonction `split()` de Make donne le même
    résultat une fois insérée dans ce champ texte (pas de sérialisation
    JSON automatique des tableaux dans le Body "Map Body"). **Solution
    retenue** : une seule balise `<category>` par item dans `feed.xml`,
    contenant déjà les 3 titres séparés par `","` (guillemet-virgule-
    guillemet) — voir `docs/routine-prompt.md`, étape technique 8. Il
    suffit alors d'entourer la pastille de guillemets et crochets **tapés
    à la main** dans le Body (`["`+pastille+`"]`) pour obtenir un tableau
    JSON valide, sans aucune fonction Make. Flux de test jetable
    (`feed-test.xml`, supprimé après usage, comme pour LinkedIn) utilisé
    pour valider chaque itération sans polluer le vrai flux ni attendre le
    lendemain.
  - Erreur `LinkedIn Content is a duplicate` rencontrée pendant les tests :
    normal, LinkedIn refuse de reposter un contenu de test identique
    plusieurs fois — sans rapport avec la config, LinkedIn fonctionne déjà
    avec du vrai contenu quotidien.
  WhatsApp Channels a été écarté pour l'instant (pas d'API officielle
  gratuite, seulement des services tiers payants et non garantis par Meta).
  Promotion du canal aussi ajoutée dans le template email (`feed.xml`,
  voir `docs/routine-prompt.md` étape technique 8) : une mention Telegram
  avant l'invitation à répondre, pour que les abonnés email découvrent le
  canal sans passer par `newsletter.html`.
  **Canal soumis à l'annuaire TGStat** (tgstat.com, catégorie France /
  français / News and media) le 31 juillet, pour être découvrable en
  dehors du site. Email de proposition préparé pour l'annuaire **ActuZones**
  (actuzones@proton.me) — à envoyer manuellement. Deux autres annuaires
  identifiés mais pas encore soumis : Lien Telegram (lientelegram.com,
  fiche indexée Google) et Annuaire Telegram France (telegramfrance.com).
  **Encart dédié ajouté sur `index.html`** (section `.telegram-promo`,
  entre Sources et le footer) : bouton à bordure — volontairement moins
  marquant qu'un bouton plein — puisque c'est la page la plus visitée du
  site. Comme le lien du footer, cette section fait partie du gabarit
  `index.html` recopié chaque matin, aucune instruction supplémentaire
  nécessaire dans `docs/routine-prompt.md`.
  **Point de vigilance soulevé le 31 juillet** : l'encart Telegram sur
  `newsletter.html` (bordure + bouton plein) est visuellement plus marquant
  que le formulaire email juste au-dessus, avec un risque de cannibaliser
  les inscriptions email (canal gratuit et sans engagement vs formulaire
  email) plutôt que de les compléter. Décision : garder l'email comme
  canal principal (liste possédée, indépendante d'une plateforme tierce)
  et traiter Telegram comme option secondaire complémentaire — sujet pas
  encore tranché sur s'il faut rééquilibrer `newsletter.html` en
  conséquence, et rester volontairement discret (lien simple, pas
  d'encart) si un ajout est fait sur `index.html`.
  - **Instagram** : pipeline technique déjà prêt (cartes 1080×1080 via
    `tools/gen_single.js`/`gen_teaser.js`, `feed.xml`/`feed.json`, voir
    section dédiée plus haut) mais **jamais branché à un vrai compte
    Instagram** — pas de posting automatique en place à ce jour, génération
    manuelle sans diffusion. **Reste à faire** : créer/activer le compte
    Instagram "Scénario", brancher un outil d'automatisation (ex. Make,
    Buffer, ou tout outil capable de lire `feed.xml`/`feed.json` avec
    enclosure image) pour poster automatiquement la carte du jour, puis
    suivre les mêmes statistiques (impressions, comptes touchés) pour
    juger si ça génère du trafic vers `lesscenarios.fr`.
  - Objectif commun : ces deux canaux ne servent à rien tant qu'ils n'ont
    pas d'audience — la priorité court terme est de poster régulièrement et
    de construire un minimum de réseau, pas seulement de brancher la
    technique.
- Nom de domaine dédié : **fait** — `lesscenarios.fr` acheté et configuré
  (voir plus haut).
- **SEO de base — fait.** `robots.txt` (autorise tout, pointe vers le
  sitemap) et `sitemap.xml` (toutes les pages vivantes + toutes les archives)
  ajoutés à la racine. `sitemap.xml` est maintenant mis à jour chaque jour
  par la routine (nouvelle entrée d'archive + `lastmod` rafraîchi), voir
  `docs/routine-prompt.md` étape technique 7. **Google Search Console —
  fait** (30 juillet 2026) : propriété du domaine `lesscenarios.fr`
  vérifiée, sitemap soumis.
- Amélioration de la recherche/découvrabilité et réflexion SEO plus poussée
  (contenu déjà bien structuré pour ça — titres clairs, meta descriptions par
  page — donc peu de travail supplémentaire nécessaire ici).
- **Mentions légales + politique de confidentialité** — fait. Deux pages
  dédiées (`mentions-legales.html`, `politique-de-confidentialite.html`),
  liées depuis le footer des 5 pages vivantes. Éditeur identifié (Olivier
  Bertrand), hébergeur GitHub Pages précisé, et les trois cas de collecte de
  données détaillés simplement : newsletter (Buttondown), formulaire de
  contact (FormSubmit), mesure d'audience (GoatCounter, anonyme, sans cookie
  donc pas de bandeau de consentement nécessaire).
- **Newsletter par email — presque terminé.** Outil choisi : **Buttondown**
  (compte payant, plan Basic ~9$/mois — nécessaire pour le RSS-to-email, pas
  disponible en gratuit contrairement à ce qu'indiquaient plusieurs sources
  tierces, vérifié en pratique). Branché directement sur `feed.xml`, déjà
  généré chaque jour (texte seul, voir plus haut).
  - ✅ Fait : `newsletter.html` (page d'inscription, style du site, formulaire
    Buttondown standard, redirections configurées pour rester sur le site) +
    lien « Newsletter » dans le menu de toutes les pages vivantes ; compte
    Buttondown créé et passé en payant ; design (couleurs/polices) aligné à la
    charte du site sur les pages web et email Buttondown ; connexion RSS-to-email
    configurée (« Send an email », déclenchement à chaque nouvel item, template
    « Rich ») ; mise à jour quotidienne de `feed.xml` ajoutée au prompt de la
    routine (étape technique 7).
  - ✅ **Fait, vérifié le 31 juillet sur un envoi réel** : template d'email
    propre (un seul bloc d'intro « Rich », pas de doublon), objet/Subject
    correct (reprend le h1 du jour), retours à la ligne bien interprétés,
    liens de désinscription/gestion d'abonnement présents. Email de test
    réel reçu et vérifié bout en bout (édition du 31 juillet, 08h01). Le
    prompt de la routine est aussi tenu à jour dans le trigger réel au fil
    des sessions (dernière synchronisation vérifiée le 31 juillet, 16h36).
- **Newsletter hebdomadaire « On refait le scénario de la semaine » — ajoutée le 3 août.**
  Demande explicite de l'utilisateur : certains lecteurs préfèrent un récap
  hebdomadaire plutôt que de suivre la quotidienne. Nom choisi pour éviter le
  plagiat d'un concurrent qui utilise "on rembobine" — même idée (revenir sur
  la semaine), formulation différente, dans l'esprit de la marque
  ("refaire le scénario" ~ "refaire le match").

  **Mécanique** : flux RSS séparé, `feed-weekly.xml` (racine du dépôt),
  totalement indépendant de `feed.xml` — un abonné à la quotidienne ne reçoit
  jamais l'hebdo, et inversement, sauf inscription explicite aux deux. Une
  **nouvelle Routine automatique** (créée par une session, donc modifiable
  directement via `update_trigger` — contrairement au trigger quotidien créé
  hors session) tourne **chaque dimanche à 14h Paris**, sans validation
  manuelle (choix de l'utilisateur, cohérent avec l'automatisation complète
  du site). L'Automation Buttondown côté RSS-to-email envoie l'email le
  dimanche soir : l'écart de quelques heures laisse une marge confortable
  entre la publication du récap dans `feed-weekly.xml` et l'envoi réel :
  1. Vérifie qu'un récap n'a pas déjà été publié cette semaine (dernier
     `<pubDate>` de `feed-weekly.xml`).
  2. Relit les 7 dernières entrées du « Journal des sujets publiés »
     (`docs/sujets-a-suivre.md`), lundi à dimanche de la semaine calendaire.
  3. Ouvre chaque archive correspondante pour en extraire la matière du
     récap (h1, question, scénario le plus probable) — jamais se contenter
     du seul titre du journal, trop court pour un vrai résumé.
  4. Rédige le récap dans un **ton fluide et naturel, mais rigoureux —
     jamais familier ni "cute"**. **Correction du 3 août** : le tout
     premier exemple (basé sur la semaine du 27 juillet) partait sur un ton
     trop familier ("Salut 👋") et une paraphrase vague et creuse ("on ne
     tranche pas encore" pour désigner le scénario stable) — retour
     utilisateur immédiat, corrigé aussitôt dans l'exemple et dans le
     prompt de la routine. Règle retenue : **toujours le vocabulaire exact
     déjà établi sur le site** — "le scénario stable/favorable/dégradé",
     "jugé le plus probable", le pourcentage exact, le nom du scénario tel
     qu'écrit dans son `<h3>` — jamais une reformulation de convenance.
     Chaque sujet précise aussi le **registre du jour** (repris de
     l'eyebrow de l'archive, ex. "Lundi, géopolitique international") pour
     ancrer le sujet. Un lien cliquable vers chaque archive citée, jamais
     un jour mentionné sans son lien.
  5. Insère un nouvel `<item>` en haut de `feed-weekly.xml` (historique
     conservé, comme `feed.xml`), commit et push direct sur `main`.

  **Pas de page dédiée sur le site** (décision du 3 août, pour démarrer
  simple) : le contenu vit uniquement dans le flux RSS et l'email — aucune
  page `hebdo.html` ni archive figée par semaine, contrairement aux
  éditions quotidiennes. Réévaluable plus tard si le format prend.

  **Pas de relais Telegram/LinkedIn** (décision du 3 août) : contrairement à
  `feed-suivi.xml`, ce flux reste strictement newsletter email — pas de
  second scénario Make à créer pour celui-ci.

  **Côté Buttondown** (configuration à faire par l'utilisateur, hors
  session) : deux inscriptions séparées sur `newsletter.html`, chacune avec
  son propre formulaire vers `https://buttondown.com/api/emails/embed-subscribe/scenario`
  — celui de l'hebdo ajoute un champ cadré `<input type="hidden" name="tag" value="hebdo">`
  pour taguer l'abonné côté Buttondown. Il reste à créer, côté Buttondown,
  une **Automation RSS-to-email** branchée sur `feed-weekly.xml` et filtrée
  pour n'envoyer qu'aux abonnés portant le tag `hebdo` (à vérifier/adapter
  selon les options réellement disponibles dans l'interface Buttondown —
  non testé, cette session n'a pas accès à Buttondown).
- **Photo dans les éditions — idée écartée le 1er août.** Discuté puis
  volontairement abandonné : impossible d'utiliser une vraie photo de presse
  trouvée pendant la recherche (droit d'auteur, republication non autorisée),
  et générer une image IA "réaliste" est risqué vu que les sujets impliquent
  souvent de vraies personnes (chefs d'État, dirigeants, sportifs...) —
  problème de désinformation/deepfake pour un site qui se veut rigoureux
  factuellement. Une illustration abstraite générée par IA (pas
  photoréaliste, dans les couleurs de la marque) restait une option plus
  sûre, mais écartée aussi pour ne pas introduire un élément visuel non
  maîtrisé et casser la cohérence typographique actuelle du site (aucune
  photo nulle part aujourd'hui). Aucune action prévue pour l'instant.
- **Pages de suivi par sujet — implémenté et testé le 1er août avec un
  premier vrai cas d'usage.** Besoin identifié : certains sujets (budget
  2027, Iran-USA, méga-feux...) ont un enjeu qui dure bien au-delà de leur
  édition d'origine, mais les archives sont figées définitivement (aucune
  édition n'est jamais remodifiée) — donc aucun mécanisme actuel pour
  montrer comment un scénario évolue dans le temps.

  **Mécanique retenue** :
  - Une nouvelle page par sujet suivi, `suivi/{sujet}.html`, **distincte**
    de l'archive d'origine (qui ne bouge jamais). N'existe pas tant
    qu'aucune mise à jour n'a été demandée.
  - Déclenchement **entièrement manuel** : l'utilisateur donne le "go"
    (ex. « mets à jour le sujet Budget 2027 ») ; jamais automatique dans la
    routine quotidienne, jamais une entrée systématique pour chaque
    édition — volontairement réservé à une poignée de sujets à enjeu
    durable, choisis à la main, pour ne pas se retrouver à gérer un
    deuxième site.
  - À la première demande, la page se crée avec **deux entrées d'un
    coup** : (1) rappel de l'édition d'origine — résumé des 3 scénarios et
    lequel était jugé le plus probable, avec lien vers l'archive figée ;
    (2) la mise à jour du jour — ré-évaluation des 3 scénarios à la
    lumière de ce qui s'est passé depuis, conclusion claire comparée à
    l'entrée précédente.
  - Chaque demande suivante ajoute une **nouvelle entrée en dessous**,
    jamais une réécriture des précédentes (même logique que les
    archives : on additionne, on ne remplace pas) — v0, v1, v2... jusqu'à
    autant de mises à jour que nécessaire.

  **Découverte** : pas de nouvel onglet dans le menu principal pour
  l'instant (prématuré tant qu'il n'existe que 2-3 sujets suivis). À la
  place :
  - Un badge sur la ligne concernée dans `archives.html` (la liste
    vivante, jamais la page individuelle figée) : `🔄 Suivi mis à jour le
    {date} →`, avec la date de dernière mise à jour plutôt que la date de
    publication.
  - Un toggle de tri ajouté aux filtres existants de `archives.html`
    (« Date de publication » / « Dernière mise à jour ») : en mode
    « dernière mise à jour », un sujet ancien mais récemment mis à jour
    remonte en haut, mélangé aux éditions du jour — réutilise le JS de
    recherche/filtre déjà en place, pas de nouvelle mécanique à inventer.

  **Premier cas réel construit le 1er août** : `suivi/spiderman-marvel.html`,
  suite de l'édition du 18 juillet ("Spider-Man contre Avengers : qui va
  sauver le box-office Marvel ?"). V0 reprend les 3 scénarios d'origine
  (favorable 25%, stable 45% jugé le plus probable, dégradé 30%). V1
  (1er août) intègre les vrais résultats de la sortie de Spider-Man : Brand
  New Day le 31 juillet (72 M$ de previews, record ; ouverture projetée
  260-330 M$, 2ᵉ meilleur démarrage de tous les temps), qui dépasse le haut
  de la fourchette du scénario favorable — avec une conclusion honnête
  précisant que Doomsday (sortie en décembre) reste une inconnue, donc rien
  n'est encore tranché sur l'ensemble du sujet. Badge + tri par fraîcheur
  branchés sur `archives.html` et vérifiés visuellement (desktop + mobile).

  **`suivi/_gabarit.html` est LE gabarit** (fichier dédié, jamais publié
  ni lié depuis le site, avec des `{PLACEHOLDER}` explicites et un
  commentaire d'avertissement en tête) — à réutiliser tel quel pour chaque
  nouveau sujet suivi : copier ce fichier vers `suivi/{sujet}.html`, puis
  remplacer chaque placeholder par le vrai contenu. Ne jamais repartir
  d'un autre fichier `suivi/*.html` existant ni improviser une nouvelle
  structure. `suivi/spiderman-marvel.html` reste le premier exemple réel
  rempli à partir de ce gabarit, utile pour voir le rendu final, mais
  **`_gabarit.html` est la source à copier**, pas lui.

  **Marche à suivre pour une mise à jour** (processus manuel, hors
  routine) : l'utilisateur donne le sujet à mettre à jour dans une
  session ; retrouver l'édition d'origine dans `archives/` ; si aucune
  page `suivi/{sujet}.html` n'existe encore, la créer à partir de
  `suivi/_gabarit.html` avec V0 (rappel de l'édition d'origine) + V1
  (première mise à jour) ; si elle existe déjà, ajouter uniquement une
  nouvelle version en dessous, jamais réécrire les précédentes ; vérifier
  les faits par une vraie recherche (même rigueur que pour une édition
  normale, sources croisées) ; **donner une nouvelle estimation chiffrée
  des 3 scénarios, présentée comme des cartes `.mini-scenarios` (même
  format que V0, pas un design différent)**, chacune avec une ligne
  d'évolution bien visible : le **nouveau %** en gros (`.evo-current`),
  une flèche colorée (`.evo-arrow` — verte `is-up` si ça monte, rouge
  `is-down` si ça descend, grise `is-flat` si inchangé), et l'ancien %
  entre parenthèses en petit (`.evo-prev`, ex. "(vs. 25% en V0)") —
  **toujours comparé à la version immédiatement précédente**, jamais
  systématiquement V0 (V2 se compare à V1, V3 à V2, etc.). Un commentaire
  court par scénario explique pourquoi il monte/descend/reste stable.
  Format remplacé le 1er août (l'essai précédent en barres `.pct-compare`
  a été jugé pas assez lisible/scannable par rapport à V0, abandonné).
  **L'intro de chaque mise à jour doit rester un seul paragraphe concis**,
  comme celui de V0 — pas plusieurs paragraphes détaillés, le détail
  factuel spécifique à chaque scénario va dans son propre commentaire de
  carte, pas dans l'intro générale.

  **Ordre du bloc obligatoirement identique à V0** (corrigé le 1er août
  après retour utilisateur — l'ordre initial avait la conclusion *avant*
  les cartes, l'inverse de V0) : intro → cartes `.mini-scenarios` → bloc
  `.conclusion` (label + **une seule phrase**, jamais un gros paragraphe
  après la grille). Ne pas dupliquer la conclusion en un "headline" avant
  les cartes ET un paragraphe après — un seul emplacement, après la
  grille, exactement comme V0.

  **La conclusion doit nommer explicitement le scénario le plus volatil**
  (ajouté le 1er août après retour utilisateur — une conclusion vague ne
  suffit pas) : citer le scénario qui bouge le plus avec son écart exact
  en points (ex. "favorable : 25% → 45%, +20 points"), expliquer en une
  phrase le fait concret qui l'explique (ex. le succès du film,
  pas juste "les choses évoluent"), puis la nuance/incertitude restante
  s'il y en a une. Le lecteur doit comprendre la volatilité réelle de la
  mise à jour en une seule lecture.

  Mettre à jour le badge et la date sur `archives.html` ; mettre à jour
  aussi l'entrée correspondante (ou la créer) dans la section « Suivis
  actifs » de `docs/sujets-a-suivre.md` (dernière vérification, prochaine
  échéance connue) ; ajouter aussi un item dans `feed-suivi.xml` (voir
  section « Annonce des mises à jour sur Telegram/LinkedIn » ci-dessous)
  pour que Make.com relaie l'annonce ; vérifier visuellement avant de
  pousser.

  **Annonce des mises à jour sur Telegram/LinkedIn, ajoutée le 2 août.**
  Demande explicite de l'utilisateur : quand une page de suivi reçoit une
  nouvelle version (V1, V2…), l'annoncer aussi sur Telegram et LinkedIn —
  pas seulement sur le site. Mécanisme choisi : un **flux RSS séparé**,
  `feed-suivi.xml` (racine du dépôt), volontairement distinct de
  `feed.xml` (celui des éditions quotidiennes, qui alimente aussi la
  newsletter Buttondown) pour ne **jamais déclencher d'email newsletter**
  pour une mise à jour de suivi — l'utilisateur n'a demandé que Telegram
  et LinkedIn. RSS plutôt qu'un webhook direct : cohérent avec la solution
  déjà validée pour `feed.xml` (Make **poll** le flux, aucun appel sortant
  requis depuis cette session — évite de retomber sur le blocage réseau
  déjà rencontré avec `api.telegram.org` en appel direct, voir plus bas).

  Format d'un item (mêmes conventions que `feed.xml` : `<comments>` porte
  la phrase courte, `<description>` le CDATA complet avec un lien final) :
  ```xml
  <item>
    <title>{Sujet} : un scénario a bougé</title>
    <link>https://lesscenarios.fr/suivi/{sujet}.html#version-content-v{N}</link>
    <guid isPermaLink="false">scenario-suivi-{sujet}-v{N}</guid>
    <pubDate>{date de la mise à jour au format RFC-822}</pubDate>
    <comments>{emoji} {verdict court de la conclusion, la phrase déjà écrite dans la page}</comments>
    <description><![CDATA[{emoji} {même phrase}<br><br>{1-2 phrases : ce qui explique le mouvement}<br><br>Voir la mise à jour complète, scénario par scénario 👉 <a href="{lien vers la version}">lesscenarios.fr/suivi/{sujet}.html</a>]]></description>
  </item>
  ```
  Ajouter le nouvel item **en haut** du flux (comme `feed.xml`/`archives.html`), ne jamais supprimer les précédents. Premier item réel ajouté le 2 août, rétroactivement, pour la mise à jour V1 de Spider-Man (1er août).

  **Fait et vérifié le 2 août — scénario Make créé, testé, opérationnel.**
  Second scénario Make ("Scenario update topic : RSS -> LinkedIn/Telegram"),
  séparé de celui de `feed.xml`, construit par duplication des modules
  LinkedIn/Telegram existants puis réglage des textes propres à une
  annonce de mise à jour (pas une nouvelle édition) :
  - Module **RSS "Watch RSS feed items"**, URL `https://lesscenarios.fr/feed-suivi.xml`, 1 item max.
  - **Fréquence : 1x/jour, 18h heure de Paris** — volontairement décalée
    des 10h du scénario `feed.xml`, pour distinguer facilement les deux
    dans l'historique Make en cas de debug. Largement suffisant vu que les
    mises à jour de suivi sont rares et manuelles (voir plus haut :
    pas de déclenchement "push" possible avec un flux RSS statique, donc
    polling à basse fréquence pour rester très en dessous du quota
    gratuit Make de 1000 opérations/mois).
  - Module **Telegram Bot → "Send a Text Message"** (connexion "Scenario"
    déjà existante, réutilisée) : `Chat ID` = `@scenario_fr`, `Text` =
    `Title` + `Comments` + **« 👉 Voir la mise à jour complète : »** + `URL`
    — reprise du module de `feed.xml`, avec cette seule phrase de clôture
    changée (« Lire les 3 scénarios chiffrés » n'a pas de sens pour une
    réévaluation, pas une nouvelle prédiction).
  - Module **LinkedIn → "Create a Company Text Post"** (connexion "Olivier's
    LinkedIn...", Page "Scenario", déjà existantes, réutilisées) : `Content`
    = **« 🔄 Un sujet suivi vient d'être mis à jour 👇 »** + `Title` +
    `Comments` + `URL` — reprise du module de `feed.xml`, avec cette
    seule phrase d'intro changée (au lieu de « 🔥 Nouvelle édition
    Scénario, à lire 👇 »).
  - **Pas de sondage (`sendPoll`) pour ce flux** : contrairement à une
    édition du jour, une mise à jour de suivi annonce un résultat déjà
    connu (les nouvelles probabilités), pas la peine de faire voter avant.
  - Test réel effectué avec l'item Spider-Man V1 déjà présent dans
    `feed-suivi.xml` : envoi confirmé sur Telegram et LinkedIn.

  **Graphique d'évolution ajouté le 1er août**, fixe (non-repliable, choix
  volontaire — le mettre dans l'accordéon irait à l'encontre de son but
  d'aperçu immédiat), affiché juste après l'intro de la page et **avant**
  "V0 — Point de départ". Courbes lissées (Catmull-Rom → Bézier cubique),
  une par scénario (vert/bleu/rouge, mêmes couleurs que le reste du site),
  légère zone de dégradé sous la courbe favorable, points + % en Fraunces
  gras sur le dernier point. **N'apparaît qu'à partir de 2 versions**
  (`evoData.length < 2` → pas de rendu) : un seul point ne montre aucune
  évolution, pas la peine de l'afficher pour un sujet jamais mis à jour.
  **Généré en JS pur (pas de librairie externe), avec tout le rendu
  enveloppé dans un `try/catch`** : si les données sont mal formées (faute
  de frappe en éditant le tableau `evoData` à la main), le graphique se
  masque silencieusement au lieu de casser le reste de la page — risque
  jugé faible (pas de dépendance réseau, pas de build) mais protection
  ajoutée par précaution vu que ces données sont éditées à la main à
  chaque mise à jour. Données à éditer : le tableau `evoData` en bas de
  page (`{ label: "V2", date: "...", favorable: X, stable: Y, degrade: Z }`
  — une ligne par version, ajouter simplement la ligne suivante).

  **Journal quotidien auto-alimenté, ajouté le 1er août.** Depuis cette
  date, l'étape 6bis de `docs/routine-prompt.md` fait écrire par la
  routine éditoriale **quotidienne** une ligne par édition (date + titre +
  lien) tout en haut de la section « Journal des sujets publiés » de
  `docs/sujets-a-suivre.md` — sans aucun jugement de sa part sur l'intérêt
  du sujet, juste un journal brut, même logique que `archives.html`. Le
  reste du fichier (section « Suivis actifs ») reste tenu à la main.

  **Détection automatique des sujets à mettre à jour, ajoutée le 1er
  août.** Une Routine dédiée (`trig_...`, hebdomadaire, distincte de la
  routine éditoriale quotidienne) relit `docs/sujets-a-suivre.md` : les
  « Suivis actifs » systématiquement, et le « Journal des sujets publiés »
  **limité aux 30 derniers jours** — au-delà, un sujet qui n'a pas justifié
  de suivi dans le mois qui suit sa publication n'en a probablement pas
  besoin rétroactivement (fenêtre volontairement bornée : sans ça, le
  journal grossissant indéfiniment d'une ligne par jour, la recherche
  hebdomadaire deviendrait de plus en plus lourde au fil des mois/années).
  Fait une recherche rapide sur les sujets retenus, et **propose** une
  short-list de sujets qui semblent mériter une page de suivi ou une mise
  à jour, avec le fait déclencheur. **Ne crée et ne modifie jamais
  automatiquement une page `suivi/*.html`, ni le fichier
  `sujets-a-suivre.md` lui-même** : c'est un rapport, le "go" reste
  toujours une décision manuelle de l'utilisateur. La routine fire dans la
  session en cours (pas une session neuve), pour garder le contexte
  complet du site — son rapport arrive donc comme message dans cette même
  conversation, pas par email (choix confirmé le 1er août : la continuité
  de contexte a été préférée à la notification automatique).

  **Anciennes versions repliées par défaut (accordéon), ajouté le 1er
  août.** Chaque bloc `.version` a un bouton `.version-toggle` ; seule la
  **dernière version** (la plus récente, toujours en bas du DOM) reste
  dépliée à l'arrivée sur la page — les précédentes sont repliées (tag +
  date visibles, contenu masqué jusqu'au clic). Ajouté après retour
  utilisateur : sans ça, la page devient un pavé à faire défiler dès la
   3ᵉ ou 4ᵉ mise à jour d'un même sujet. Même mécanique CSS/JS que
  l'accordéon des scénarios sur `archives.html` (`grid-template-rows`
  0fr/1fr + classe `is-expanded`), rien de nouveau inventé. Pour un
  nouveau V2/V3..., dupliquer un bloc `.version.is-update` du gabarit et
  changer son `id` (`version-content-v2`, etc.) — le JS détecte
  automatiquement le dernier bloc du DOM et le déplie, aucune autre
  configuration nécessaire.
  **`docs/routine-prompt.md` et le trigger automatique ne changent
  jamais pour ça** — le suivi reste entièrement manuel, déclenché
  seulement par une demande explicite de l'utilisateur en session.
- **Transparence IA (article 50 du règlement européen sur l'IA) — ajouté
  le 1er août, obligation applicable à partir du 2 août 2026.** L'article
  50(4) impose de signaler clairement un contenu texte généré par IA sur
  un sujet d'intérêt public, sauf exemption pour un contenu ayant subi une
  vraie relecture éditoriale humaine substantielle (pas une simple
  approbation de forme) sous la responsabilité d'une personne identifiée.
  Vu que la routine publie chaque édition en autonomie complète, sans
  validation humaine séparée avant mise en ligne, cette exemption est
  jugée trop fragile pour s'appuyer dessus — décision prise de toujours
  afficher la mention de transparence plutôt que de tenter de revendiquer
  l'exemption.
  - **Mention ajoutée au footer de chaque édition** (`index.html`, et donc
    aussi chaque `archives/AAAA-MM-JJ.html` future puisque la routine
    recopie ce gabarit tel quel — même mécanisme que les liens
    Telegram/LinkedIn, aucune instruction supplémentaire nécessaire dans
    `docs/routine-prompt.md`) : `🤖 Recherche et rédaction assistées par
    l'intelligence artificielle. En savoir plus sur notre méthode →`
    (lien vers `le-projet.html`), juste après le caveat existant sur les
    probabilités.
  - **Ajouté rétroactivement aux 9 archives déjà publiées** (18 juillet
    au 1er août) — exception au principe "une archive ne se modifie
    jamais", au même titre que la correction du bilan pompiers : justifiée
    ici parce que l'obligation légale porte sur le contenu déjà en ligne
    au 2 août, pas seulement sur le contenu futur.
  - **Section dédiée ajoutée à `mentions-legales.html`** ("Intelligence
    artificielle et transparence", entre "L'éditeur" et "L'hébergeur") :
    cite l'article 50, explique que chaque édition est produite par IA à
    partir de sources vérifiées sous la responsabilité éditoriale
    d'Olivier Bertrand, renvoie vers `le-projet.html` pour le détail du
    processus. Formulation volontairement factuelle (ce qui est fait),
    **jamais une revendication de conformité totale certifiée** — le sujet
    reste juridiquement nuancé (voir l'analyse de l'exemption ci-dessus).
