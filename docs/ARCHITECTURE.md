# Architecture — Scénario

Vue d'ensemble technique du site, pour s'y retrouver rapidement sans avoir à
tout redécouvrir à chaque fois.

## Aperçu

**Scénario** est un site d'actualité statique, publié gratuitement via
**GitHub Pages** à l'adresse https://loliba92.github.io/Scenario/. Une édition
est publiée chaque jour, produite automatiquement par une routine planifiée
(voir « Automatisation éditoriale » plus bas).

Aucun backend, aucune base de données : tout est fait de fichiers HTML/CSS/JS
statiques, servis tels quels par GitHub Pages. Le seul service externe utilisé
est **FormSubmit** (formulaire de contact) — voir plus bas.

## Structure des fichiers

```
index.html              L'édition du JOUR, et seulement elle. Écrasée chaque matin.
archives.html           Liste de toutes les éditions passées (recherche + filtres client-side).
archives/AAAA-MM-JJ.html Copie figée de chaque édition passée. Jamais remodifiée après publication.
le-projet.html          Page « À propos » : mission, méthode, rythme des 7 jours.
newsletter.html         Page d'inscription à la newsletter quotidienne (Buttondown).
contact.html            Formulaire de contact (FormSubmit) + appel à la carte blanche du mardi.
sujets-prioritaires.md  File d'attente éditoriale (voir plus bas).
assets/logo.svg          Logo (3 flèches divergentes = les 3 scénarios).
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

**État au 27 juillet 2026** : la génération des cartes n'est **pas encore
branchée dans la routine quotidienne** — c'est fait manuellement pour l'instant.
La publication Instagram automatique (Make + application Meta développeur, ou
alternative payante type Publer Professional) est en cours de mise en place —
voir la discussion et la décision à prendre dans le suivi de session.

## Formulaire de contact

`contact.html` utilise **FormSubmit** (service gratuit tiers, sans backend à
héberger) : le formulaire poste vers `formsubmit.co/<alias>`, qui relaie par
email. Envoi en **AJAX** (`fetch` vers `formsubmit.co/ajax/<alias>`) pour que
le visiteur reste sur `loliba92.github.io/Scenario` au lieu d'être redirigé
vers une page FormSubmit externe. Un lien `mailto:` reste en repli.
L'alias anonyme (plutôt que l'adresse email en clair) évite l'exposition aux
robots spammeurs.

## Ce qui reste à faire (suivi)

Voir les échanges de session pour le détail, mais en résumé :
- **Mesure d'audience** : voir qui visite le site, pour suivre les progrès dans
  le temps — nombre de visiteurs/jour, d'où ils viennent (Instagram, recherche
  Google, lien direct, autre site), quelles pages et éditions marchent le
  mieux, taux de retour. Deux options :
  - **Google Analytics (GA4)** — gratuit, le plus complet, mais demande un
    identifiant de mesure (`G-XXXXXXX`, à créer sur analytics.google.com) et,
    juridiquement, un bandeau de consentement cookies (RGPD) puisqu'il dépose
    des cookies de suivi.
  - **Alternative « respectueuse de la vie privée »** (Plausible, Fathom,
    GoatCounter…) — sans cookies, donc pas de bandeau de consentement requis,
    tableau de bord plus simple (visiteurs, provenance, pages vues) ; gratuit
    seulement chez GoatCounter, les autres sont payants (quelques €/mois) mais
    beaucoup plus légers à mettre en place que GA4.
  À trancher : gratuit + complet mais bandeau cookie (GA4), ou plus simple et
  sans bandeau mais souvent payant (alternatives).
- Automatisation Instagram bout-en-bout (Make + appli Meta, ou solution
  payante) — décision et mise en place à finaliser.
- Nom de domaine dédié (ex. lesscenarios.fr) avec redirection vers le site.
- Amélioration de la recherche/découvrabilité et réflexion SEO/promotion.
- **Newsletter par email — en cours.** Outil choisi : **Buttondown**, parce
  qu'il sait envoyer un email automatiquement à partir d'un flux **RSS**
  (fonctionnalité « RSS-to-email », incluse dans son plan gratuit jusqu'à 100
  abonnés, envois illimités) — on peut donc le brancher directement sur
  `feed.xml`, déjà généré chaque jour pour Instagram, **sans modifier la
  routine quotidienne** ni ajouter d'appel API.
  - ✅ Fait : `newsletter.html` (page d'inscription, style du site, formulaire
    Buttondown standard) + lien « Newsletter » dans le menu de toutes les
    pages vivantes.
  - ⏳ À faire : créer le compte Buttondown, remplacer le `VOTRE-USERNAME-BUTTONDOWN`
    dans l'attribut `action` du formulaire de `newsletter.html` par le vrai
    nom d'utilisateur, connecter Buttondown à `feed.xml` (RSS-to-email), et
    décider du contenu de l'email envoyé — reprendre le teaser d'Instagram
    (question + 3 scénarios sans les %, lien vers le site) ou passer à un
    format plus complet puisque l'abonné a déjà consenti (moins besoin de
    « forcer le clic » que sur les réseaux sociaux). `feed.xml` devra peut-être
    évoluer pour porter un contenu email dédié, distinct de la légende Instagram.
