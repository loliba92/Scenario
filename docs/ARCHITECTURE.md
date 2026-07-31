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
    automatiquement** — l'intégration reste cassée malgré la connexion.
    **Reste à faire** : diagnostiquer pourquoi (reconnexion du compte
    LinkedIn côté Buttondown ? permission manquante ? délai de propagation
    plus long que prévu ?) ; en attendant, construire un minimum de
    réseau/abonnés sur ce profil (0 relation ≈ 0 diffusion, cf.
    "Découverte : 100 % dans le réseau, 1 membre touché" sur le premier
    post) ; réfléchir si la Page LinkedIn "Scénario" (Entreprise, existante
    mais manuelle, jamais utilisée) a un rôle à jouer en complément, ou si
    on l'abandonne pour se concentrer sur le profil personnel.
- **Telegram — canal créé le 31 juillet, automatisation branchée.**
  Canal public `@scenario_fr`, bot `@scenario_fr_bot` créé via BotFather et
  ajouté comme administrateur (droit "Publier des messages"). Test manuel
  d'envoi réussi (`sendMessage` + `sendPoll` via l'API Telegram). Étape
  ajoutée au prompt de la routine (voir `docs/routine-prompt.md`, étape
  technique 9) : poste un teaser + lien vers l'archive du jour, suivi d'un
  sondage natif (favorable/stable/dégradé) pour créer de l'engagement.
  **Fait le 31 juillet** : variable d'environnement `TELEGRAM_BOT_TOKEN`
  configurée côté environnement Claude Code Remote ("Default") utilisé par
  le trigger « Scénario » ; lien "Telegram ↗" ajouté au footer des 5 pages
  vivantes, et section dédiée "Suivre sur Telegram" sur `newsletter.html`
  pour que les visiteurs découvrent le canal. Comme pour les balises OG et
  GoatCounter, ce lien fait désormais partie du gabarit `index.html`
  recopié chaque matin — aucune instruction supplémentaire nécessaire dans
  `docs/routine-prompt.md` pour le préserver.
  **Reste à faire** : vérifier au prochain déclenchement (1er août) que le
  post + sondage partent bien automatiquement en conditions réelles.
  WhatsApp Channels a été écarté pour l'instant (pas d'API officielle
  gratuite, seulement des services tiers payants et non garantis par Meta).
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
  - ⏳ À faire : finaliser le template d'email (nettoyer les doublons du bloc
    « Rich », vérifier l'objet/Subject), envoyer un email de test réel pour
    valider le rendu bout en bout, puis coller la mise à jour de
    `docs/routine-prompt.md` dans le prompt réel de la routine (comme toujours,
    la doc n'est qu'une copie de référence).
