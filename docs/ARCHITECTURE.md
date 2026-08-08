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

## Backlog

Idées et tâches ouvertes, consolidées ici pour ne pas avoir à les
retrouver éparpillées dans le reste du document. Mise à jour au 4 août.
Priorités P1 (fort impact, faible coût) à P3 (utile mais plus lourd ou
moins prioritaire).

**Distribution / automatisation**
- **P1 — Finaliser l'image de pub Instagram "Suis @scenarios.actu", en pause le 8 août faute de crédits IA.**
  Base : `assets/social/instagram-ads/follow-cta-v1.png` (gabarit maison,
  identique visuellement aux posts quotidiens), envoyée à l'utilisateur
  avec un prompt pour l'améliorer via un outil IA photo externe (fond
  plus premium, effet "flux de données"). Deux résultats reçus le 8 août,
  tous deux avec des défauts à corriger avant utilisation :
  - Version avec bullets "Gratuit"/"Sans pub"/pourcentages : **à écarter
    telle quelle** — renomme "Stable" en "Scénario central" et "Dégradé"
    en "Scénario défavorable" (casse le vocabulaire du site, toujours
    Favorable/Stable/Dégradé), et affiche des pourcentages 35/45/20
    inventés par l'IA, sans rapport avec de vraies données.
  - Version plus sobre (garde Favorable/Stable/Dégradé intacts) : plus
    proche du bon résultat, mais un chiffre parasite illisible traîne
    dans le fond (artefact IA) — à régénérer en précisant explicitement
    "no numbers, no extra text in the background". Contient aussi une
    ligne ajoutée "Gratuit et sans pub" non présente dans l'original, à
    valider ou retirer.
  **Repris le [date à compléter] une fois les crédits IA renouvelés** —
  utilisateur à relancer explicitely, il n'a plus de crédits le 8 août.
  Buffer limite à 3 connecteurs gratuits (déjà pris par X, Facebook,
  Instagram) — passer par un 4e connecteur Buffer serait payant. Option
  écartée : créer un second compte Buffer gratuit avec une autre adresse
  email pour contourner la limite — risque réel de détection (même site
  `lesscenarios.fr`, mêmes réseaux sociaux liés, probablement même
  appareil/IP) et de suspension des comptes liés, ce qui casserait aussi
  X/Facebook/Instagram qui tournent déjà bien ; non recommandé, écarté
  après discussion. **Piste retenue à explorer** : brancher WhatsApp
  directement dans Make.com via son module natif **WhatsApp Business
  Cloud API** (comme Telegram/LinkedIn aujourd'hui), sans passer par
  Buffer du tout — nécessite un compte WhatsApp Business + accès à l'API
  Cloud Meta (gratuit jusqu'à un certain volume de messages). Pas encore
  configuré, à reprendre quand l'utilisateur veut avancer dessus.
- **[FAIT le 4 août] Boutons de partage** (X, LinkedIn, WhatsApp, copier
  le lien) sur chaque édition — `index.html`, section `.share-block`,
  juste avant le footer. 100 % statique/générique : les liens sont
  construits côté client en JS à partir de l'URL et du `<h1>` de la page,
  donc **aucune donnée à générer par la routine quotidienne** — elle sera
  reproduite automatiquement comme le reste du gabarit (structure/CSS),
  sans avoir besoin de synchroniser le prompt de la routine réelle.
  Testé desktop + mobile via Playwright avant publication. S'applique à
  partir de la prochaine édition (les archives déjà publiées restent
  figées). **Fusionné avec l'ancien bloc `.telegram-promo`** le même jour
  (retour utilisateur : deux sections quasi identiques l'une sous
  l'autre) — un seul bloc "Rejoindre et faire circuler", bouton Telegram
  en premier suivi des boutons de partage ; CSS `.telegram-promo`
  obsolète retiré. **Déplacé une seconde fois le même jour** (retour
  utilisateur : boutons tout en bas de page = besoin de scroller, moins
  accessible) — le partage est maintenant une ligne discrète juste sous
  `.pubdate` (haut de page), style `.share-inline` repris de `.sources-note`
  des pages de suivi (texte gold, soulignement pointillé, pas de gros
  boutons). Le bloc du bas reprend son titre d'origine "Vote avant de
  connaître le résultat" et ne garde que "Rejoindre le canal Telegram".
- **X (Twitter) comme canal supplémentaire — fait et vérifié le 6 août,
  mais pas par la voie prévue.** Le plan initial (connexion directe
  Make ↔ API X via un compte développeur) a été tenté puis abandonné :
  Make a supprimé son app native "X (Twitter)" le 3 avril 2025 (API X
  passée payante), et la reconstruction manuelle en HTTP OAuth 2.0 +
  PKCE dans Make (Authorize/Token URI, code_challenge/code_verifier,
  Client ID/Secret du compte développeur X) a buté sur des échecs de
  connexion répétés ("Accounts verify failed", "Something went wrong")
  malgré une config conforme à la doc officielle Make — cause exacte non
  identifiée, abandonné après plusieurs tentatives. **Solution retenue :
  Buffer**, gratuit (3 canaux, 10 posts programmés par canal, largement
  suffisant pour 1 post/jour), qui gère lui-même sa propre app développeur
  X — aucune clé API à fournir. Module Make natif **Buffer → "Create a
  status update"**, ajouté comme 3e sortie du Router existant (même
  déclencheur RSS `feed.xml`), `Text` = `Title` + une phrase fixe de
  contexte ("Scénario : chaque jour, un sujet d'actu décrypté en 3
  scénarios chiffrés") + "Lire l'article :" + `URL` — jamais la
  `Description`/`Comments` complète, largement au-dessus des 280
  caractères de X certains jours (vérifié sur les 10 dernières éditions :
  8 sur 10 auraient dépassé la limite rien qu'avec Titre + Comments).
  Voir aussi la sauvegarde du scénario Make complet plus bas.
- **[FAIT le 7 août] Facebook comme canal supplémentaire**, via le même
  Buffer que X (aucune nouvelle app développeur à créer). La Page
  Facebook "Scénario" existait déjà, créée automatiquement par Meta lors
  du passage du compte Instagram dédié en compte pro (une Page Facebook
  ne peut pas exister sans profil admin — c'est le profil perso qui sert
  d'admin, la Page reste une entité publique séparée). Connectée à Buffer
  comme 2e canal (sur les 3 gratuits, X étant le 1er). Nouveau module
  Make natif **Buffer → "Create a status update"**, 4e sortie du Router
  existant (même déclencheur RSS `feed.xml`). Contrairement à X, Facebook
  n'a pas de limite de caractères contraignante : `Text` reprend donc le
  format riche façon LinkedIn plutôt que le format minimal de X —
  `Title` + `Comments` complet + lien, avec l'accroche "🔥 Nouvelle
  édition Scénario, à lire 👇" et la formule de clôture "👉 Lire l'analyse
  complète : `URL`". Testé via "Run this module" dans Make : la fenêtre
  de test manuel de Make a renvoyé une erreur "Value is not a valid URL
  address" sur le champ `Comments` — **faux positif propre à la saisie de
  données de test**, dû au fait que la norme RSS 2.0 définit `<comments>`
  comme devant contenir une URL (page de commentaires), alors que ce flux
  détourne le tag pour y mettre du texte libre ; n'affecte pas le
  fonctionnement réel, ce même champ étant déjà utilisé sans problème par
  la branche LinkedIn en production. Contournement : saisir une URL
  factice dans la fenêtre de test pour passer la validation. **Même
  branche ajoutée sur la sous-route "RSS SUIVI"** (module 33, mises à
  jour de sujets suivis) avec le même `profileIds`, donc les deux
  circuits (édition quotidienne et suivi) publient sur la Page Facebook.
  **Point de vigilance mineur non bloquant** : le champ `Text` du module
  32 (édition quotidienne) contient un unique retour à la ligne parasite
  avant `{{4.title}}` (un mélange entre la touche Entrée et la pastille
  `{{newline}}` du champ Make, malgré plusieurs allers-retours pour le
  nettoyer) — une ligne vide en trop à l'affichage, sans impact
  fonctionnel. Blueprint à jour sauvegardé dans
  `assets/make/scenario-daily.blueprint.json`.
- **[FAIT le 7 août] Image Instagram générée par édition** — pipeline
  HTML/CSS + Playwright (`scripts/social/generate_instagram_image.py` +
  `scripts/social/instagram-template.html`), image carrée 1080×1080 avec
  le titre et les 3 titres de scénarios (couleur + flèche par scénario),
  **sans pourcentages ni question/contexte** — deux choix volontaires du
  7 août : pas de pourcentages (effet teaser vers le lien en bio) et pas
  de question (retour utilisateur : restait illisible sur mobile même en
  grossissant le texte plusieurs fois) — le contexte reste porté par
  `<comments>`/la légende du post, pas par le visuel. Publiée via un tag
  RSS `<enclosure>` standard ajouté à chaque `<item>` de `feed.xml`, lu
  nativement par le module RSS de Make (`enclosures`), branché sur une
  route Buffer → Instagram du scénario Daily. Routine quotidienne mise à
  jour en conséquence (génère l'image, la committe dans
  `assets/social/instagram/{AAAA-MM-JJ}.png`, ajoute l'`<enclosure>` —
  voir `docs/routine-prompt.md`). Module Make **Buffer → "INSTAGRAM"**
  (id 34) ajouté comme 5e sortie du Router principal du scénario Daily,
  `Text` = `Title` + `Comments` + "👉 Lien en bio pour lire l'analyse
  complète" (pas de lien direct, Instagram ne rend pas les liens de
  légende cliquables), `useMedia: true`, `media.link`/`media.picture` =
  `{{4.enclosures[].url}}`. **[Vérifié et validé le 7 août]** : la
  syntaxe `enclosures[]` (crochets vides, plutôt que `enclosures[1]`
  index explicite vu dans l'interface Make au moment du mapping) résout
  bien vers le premier (et seul) élément du tableau une fois `feed.xml`
  alimenté par un vrai `<enclosure>` généré par la routine — confirmé par
  l'utilisateur, plus un point de vigilance. **Weekly a aussi gagné une
  branche Facebook** (module 12, `profileIds` identique à celui du Daily)
  entre-temps, pas documentée en détail ici — même format que la branche
  Telegram/LinkedIn existante du scénario Weekly.
- **P2 — Même pipeline d'image pour le récap hebdomadaire.** Le scénario
  Make Weekly n'a pas encore d'image dédiée (`feed-weekly.xml` sans
  `<enclosure>`, pas de route Buffer/Instagram sur ce scénario). Le
  script/template devraient être largement réutilisables tels quels — à
  trancher surtout le contenu affiché vu que le weekly porte sur 7 sujets
  et pas 3 scénarios d'un seul sujet (image récap titre+date seule ? une
  sélection des 7 sujets ? format encore à définir). Pas commencé.
- **[FAIT le 7 août] Bug corrigé + UX simplifiée : abonnement
  quotidienne + hebdo en une seule fois.** Trouvé le même jour : les deux
  formulaires séparés de `newsletter.html` utilisaient
  `<input type="hidden" name="metadata__subscription_type" value="...">`
  — un champ **metadata** Buttondown, à valeur unique par abonné. Un
  même email qui s'inscrivait d'abord à la quotidienne
  (`metadata__subscription_type=quotidien`) puis à l'hebdo
  (`=hebdo`) voyait la seconde valeur écraser la première, alors que la
  page promettait explicitement de pouvoir s'abonner aux deux.

  **Fix appliqué** : un seul formulaire (section "S'abonner", juste après
  le hero, avant les deux blocs explicatifs quotidienne/hebdo), avec deux
  cases à cocher — `<input type="checkbox" name="metadata__quotidien"
  value="oui" checked>` et `<input type="checkbox" name="metadata__hebdo"
  value="oui">` — plutôt que deux formulaires distincts avec un champ
  email chacun et un seul champ `metadata__subscription_type` partagé.
  Le point clé du fix : ce sont désormais **deux clés metadata
  différentes** (`quotidien` et `hebdo`) au lieu d'une seule clé
  (`subscription_type`) à valeur unique — donc cocher les deux soumet
  `metadata__quotidien=oui&metadata__hebdo=oui` en une seule requête, et
  chaque clé est indépendante côté Buttondown, aucune ne peut écraser
  l'autre. HTML gère nativement les cases décochées (simplement absentes
  du POST), aucun JS requis. "Quotidienne" pré-coché par défaut (format
  historique/principal), "Hebdo" à cocher explicitement.

  **Point de vigilance non vérifié cette session** : une case décochée
  n'envoie rien du tout (pas de `metadata__hebdo=non`, juste l'absence du
  champ) — donc si un abonné qui avait déjà `metadata__hebdo=oui`
  resoumet le formulaire avec seulement "Quotidienne" coché, il n'est pas
  garanti que Buttondown efface l'ancienne valeur `hebdo=oui` (un champ
  omis dans une requête peut être ignoré plutôt qu'interprété comme "à
  vider", selon leur implémentation). Pour l'usage principal (première
  inscription, ou ajouter une deuxième formule) ça fonctionne très bien ;
  le cas "se désabonner d'une seule formule en resoumettant le
  formulaire" reste à tester/confirmer.

  **[FAIT le 7 août, côté Buttondown]** les deux Automations RSS-to-email
  (quotidienne et hebdo) sont configurées pour filtrer sur
  `metadata.quotidien == "oui"` / `metadata.hebdo == "oui"` — confirmé
  par l'utilisateur. Le nouveau formulaire (deux metadata séparées) et le
  filtre des Automations sont maintenant alignés de bout en bout.

  **[FAIT le 7 août]** migration des abonnés existants qui n'avaient que
  l'ancien `metadata.subscription_type` vers les nouvelles clés
  `metadata.quotidien`/`metadata.hebdo` — confirmée par l'utilisateur. Le
  bug d'abonnement simultané quotidien+hebdo est donc entièrement réglé,
  formulaire, Automations et base d'abonnés existante alignés.
- **P3 — Version anglaise du site, idée du 7 août, à reprendre dans
  quelques mois.** Garder la version française telle quelle (pas de
  remplacement) et ajouter une version anglaise en parallèle, avec sa
  propre routine dédiée pour la production (traduction et/ou rédaction
  directe en anglais — à trancher le moment venu). Rien de tranché à ce
  stade : ni l'architecture (sous-dossier `en/` ? sous-domaine ? champ de
  langue par édition ?), ni si la routine anglaise republie les mêmes
  sujets que la française ou en sélectionne d'autres, ni le rythme de
  publication.

  **Variante plus légère envisagée le même jour** (pas de site anglais
  complet, juste une distribution anglophone) : ajouter à la routine
  principale une traduction du titre + du commentaire de chaque édition,
  publiée dans un nouveau `feed-en.xml` séparé de `feed.xml`, branché
  côté Make sur une route Buffer dédiée qui poste **uniquement sur X**
  (pas Telegram/LinkedIn/Facebook/Instagram) — parce que l'audience X est
  jugée nettement plus anglophone que le reste des canaux. Pas de
  nouvelles pages HTML anglaises dans cette variante, juste un post X en
  anglais en plus du post français existant.

  **Les deux options restent explicitement mises de côté par
  l'utilisateur pour être rediscutées plus tard — ne rien commencer sans
  un go explicite**, y compris la variante légère malgré son coût
  d'implémentation plus faible.

  **Points à réfléchir avant de lancer quoi que ce soit (ajoutés le 7
  août, sur demande explicite de l'utilisateur — "tout doit être pensé
  d'abord")** :
  - **Précision et cohérence de la traduction** : les termes récurrents du
    site (favorable/stable/dégradé, "scénario", les formulations types du
    caveat probabilités, etc.) doivent être traduits de façon strictement
    identique à chaque édition — envisager un **glossaire de référence**
    (fichier dédié, ex. `docs/glossaire-en.md`) que la routine anglaise
    consulterait systématiquement, plutôt que de laisser chaque traduction
    réinventer sa propre formulation.
  - **Archives** : décider si la traduction s'applique seulement aux
    éditions futures, ou s'il faut aussi traduire rétroactivement les
    archives françaises existantes (`archives/*.html`) — et si oui,
    lesquelles et avec quelle méthode de contrôle qualité vu le volume.
  - **Pages légales en anglais** : si une vraie version anglaise du site
    voit le jour (pas juste la variante "posts X"), `politique-de-
    confidentialite.html` et les mentions légales doivent avoir un
    équivalent anglais tout aussi rigoureux — pas une simple traduction
    automatique vu la sensibilité RGPD/juridique de ce contenu.
  - Plus généralement, ne pas sous-estimer la variante "légère" (feed-en
    vers X) sur ce point : même un simple post traduit doit rester
    juridiquement/factuellement aussi rigoureux que l'édition française
    d'origine, pas une traduction approximative.
- **P2 — Widget Telegram embarqué : tenté et abandonné le 8 août,
  Telegram bloque l'iframe.** Essayé via `<iframe src="https://t.me/s/
  scenario_fr">`, la page publique du canal — supposée faite pour ce
  genre d'intégration d'après plusieurs tutoriels tiers trouvés en
  recherche. **Confirmé en prod par l'utilisateur : "t.me n'autorise pas
  la connexion"** — Telegram envoie un en-tête (`X-Frame-Options` ou CSP
  `frame-ancestors`) qui bloque l'affichage de `t.me/s/*` en iframe
  depuis un site tiers. Retiré immédiatement (mieux vaut rien qu'une
  icône d'erreur visible à chaque visiteur).

  **Alternatives pour une prochaine tentative, aucune n'est aussi simple
  que l'idée de départ** :
  - Le vrai widget officiel Telegram (`telegram-widget.js`,
    `data-telegram-post="canal/id"`) n'affiche **qu'un seul post fixe
    par son ID**, pas un flux des derniers posts en direct — il
    faudrait choisir 1-3 posts à la main et mettre à jour l'ID
    régulièrement (perd l'aspect "automatique").
  - Services tiers (SociableKit, Elfsight, Common Ninja...) : proxient
    le contenu Telegram sur leur propre domaine pour contourner le
    blocage, mais payants/limités en gratuit — contredit l'exigence
    "statique/gratuit" de ce backlog à l'origine.
  - Non retenu pour l'instant : le lien "Rejoindre le canal Telegram"
    existant reste la seule option côté `newsletter.html`.
- **[FAIT le 4 août] Groupe de discussion Telegram lié au canal** — jusque
  là le canal était en diffusion pure, aucune interaction possible côté
  lecteur. Un groupe dédié "Scenario - Discussion" a été créé et lié au
  canal `@scenario_fr` via Telegram (Gérer le canal → Discussion → Add),
  100% côté app Telegram, rien à toucher côté code/routine. Chaque post
  affiche désormais un compteur de commentaires qui renvoie vers un fil
  dédié dans ce groupe. **Point à noter :** la liaison ne s'applique qu'aux
  posts publiés *après* le lien — pas de rétroactivité automatique
  confirmée sur les posts antérieurs au 4 août, contrairement à ce qui
  était supposé au départ. Vérifié via la prévisualisation web publique
  `t.me/s/scenario_fr` plutôt que l'API bot (plus simple, pas besoin de
  token). Nécessite une présence de modération humaine occasionnelle une
  fois que le groupe aura du trafic (pas un coût ponctuel comme le reste
  de cette liste, un coût récurrent).
- **[FAIT le 4 août] Teaser du registre du lendemain** ("📅 Demain : 🇫🇷
  actualité française") sous les boutons de partage — `index.html`,
  `#tomorrow-teaser`. **Correction d'estimation** : contrairement à ce qui
  était noté ici, ça ne nécessite **pas** de toucher la routine — la
  grille des registres est fixe par jour de semaine (lundi géopolitique,
  mardi carte blanche...), donc calculable 100 % côté client en JS à
  partir de la date du jour + 1 (heure de Paris), exactement comme les
  boutons de partage et le temps de lecture. Testé avec Playwright.

**UX**
- **[FAIT le 4 août] Temps de lecture estimé** sous le titre de chaque
  édition. Deux volets :
  - **Site** : 100 % client (`index.html`, même script que `.pubdate`) —
    compte les mots de `.dek`/`.why`/`dd`, 200 mots/minute, arrondi,
    minimum 1 min. Aucune sync routine nécessaire, déjà en ligne.
  - **Email (`feed.xml`)** : la même valeur doit apparaître dans la
    description envoyée par Buttondown — texte statique dans un email,
    donc calculée par la routine (`docs/routine-prompt.md`, commande
    `grep`+`wc -w` sur `archives/{date}.html`, même méthode que le JS du
    site pour que les deux chiffres correspondent toujours). **Nécessite
    la synchronisation manuelle de la routine quotidienne réelle**
    (comme pour les corrections précédentes) — pas encore fait côté
    trigger réel au moment d'écrire cette ligne.
- **[FAIT le 8 août] Sommaire ancré** (Contexte / Scénarios / Essentiel /
  Lexique / Sources) en haut de chaque édition — `nav.toc`, juste après
  les boutons de partage. Ancres `id` sur les 5 éléments, dans l'ordre
  réel de la page (`.hero`, `.scenarios`, `.essentiel-box`, `.lexique`,
  `.sources` — Lexique puis Essentiel ajoutés après coup, oubliés dans
  la première passe ; l'`id` d'Essentiel va directement sur
  `.essentiel-box`, pas sur `section.scenarios` qui l'englobe, pour
  sauter précisément dessus), défilement fluide natif déjà en place.
  Ajouté à `index.html` + `archives/2026-08-08.html`, et à
  `docs/routine-prompt.md` pour reproduction automatique chaque jour
  (bloc fixe, jamais de contenu variable). Vérifié visuellement + clic
  testé via Playwright.
- **[FAIT le 8 août] Bloc de synthèse « L'essentiel », après les 3
  scénarios.** Idée initiale (« résumé 1 minute en haut d'article »)
  suggérée par un retour externe (voir revue du 8 août plus haut) —
  discutée avec l'utilisateur et déplacée **en bas**, après `div.cards`,
  plutôt qu'en haut : moins redondant avec `question-box`/`stakes-box`
  qui font déjà ce travail de cadrage en haut de page, et comble un vrai
  vide qui n'existait pas (rien ne reliait les 3 scénarios entre eux
  après lecture). Contenu : 2-3 phrases décrivant l'issue la plus
  probable + un signal concret à surveiller pour basculer vers une
  autre — jamais une répétition des paragraphes `why` des cartes.
  Libellé « L'essentiel » retenu plutôt que « Conclusion » (jugé trop
  tranché pour un site qui pèse 3 issues sans en affirmer une), **nom
  encore ouvert à ajustement par l'utilisateur**.

  **Corrigé le 8 août même jour, retour utilisateur** : ne jamais
  écrire les labels bruts "favorable"/"stable"/"dégradé" dans ce
  bloc — le lecteur ne connaît pas forcément ce que chaque label
  recouvre pour ce sujet précis (contrairement à quelqu'un qui vient de
  lire les 3 cartes en détail juste au-dessus). Décrire l'issue en
  langage concret à la place (ex. "le rebond se maintient sur un rythme
  soutenu" plutôt que "le scénario stable").

  **Aussi ajouté le 8 août : le même texte dans `feed.xml`**, dans
  l'`<item>` du jour (texte brut, sans balisage HTML) — disponible pour
  un usage futur côté Make.com, demande explicite de l'utilisateur
  ("on ne sait jamais"), pas encore branché sur un module particulier.
  **Balise `<essentiel>` (inventée) remplacée le même jour par
  `<source url="{lien de l'édition}">`** — retour utilisateur : besoin
  d'une balise normée exploitable dans Make, `<essentiel>` n'existant
  pas dans le spec RSS 2.0 risquait de ne pas apparaître au mapping.
  `<source>` existe dans le spec (normalement le flux d'origine d'un
  item republié), inutilisée ailleurs dans ce flux, détournée ici avec
  son attribut `url` obligatoire rempli. Le champ "Summary" visible côté
  Make n'était pas une option valable : juste un alias généré à partir
  de `<description>`, pas un champ indépendant.

  Ajouté à `index.html` + `archives/2026-08-08.html` + `feed.xml` +
  `docs/routine-prompt.md` (reproduction quotidienne — nécessite le
  copier-coller manuel habituel dans la routine live,
  `trig_0176spj7P7E9fyTs1XBkQBWF`).
- **P2 — Icônes pour les boutons de partage** — inspiré d'un exemple
  brief.eco vu le 5 août (retour utilisateur : "pas l'idée de recopier,
  mais j'aime bien les icônes"), remplacer le texte "X, Facebook,
  LinkedIn..." de `.share-inline` par de petites icônes (glyphes fins,
  cohérents avec le style du site — pas les logos couleur officiels des
  plateformes). Attention à ne pas revenir sur la décision du 4 août
  (position discrète juste sous le titre, pas de gros boutons) : des
  icônes compactes dans la même ligne, pas un nouveau bloc imposant.
  Effort modéré (SVG inline ou police d'icônes + CSS), reste 100% dans le
  gabarit statique. Pas encore implémenté.
- **[FAIT le 5 août] Glossaire** — inspiré du même exemple brief.eco (lien
  "Glossaire" dans son footer email). En creusant le sujet, une bonne
  partie du travail existait déjà sans que ce soit documenté ici : chaque
  édition a son propre petit lexique en bas de page (`.lex-ref`, `<dl
  class="glossary">`), avec des renvois cliquables depuis le texte —
  mécanisme déjà décrit dans `docs/routine-prompt.md` avant ce jour.
  Ce qui manquait, et qui est fait maintenant : une page `glossaire.html`
  qui agrège tous ces termes au même endroit — recherche texte, filtre par
  domaine (réutilise la colonne « Domaine » de `docs/tags.md`, mêmes
  puces de filtre que `archives.html`), tri alphabétique, et un lien
  « Vu dans : {édition} → » vers l'édition d'origine de chaque terme.
  **Rétro-rempli une fois** (script Python ponctuel, pas conservé) à
  partir des 13 éditions déjà publiées — 77 termes récupérés, y compris
  ceux des éditions antérieures au système `.lex-ref` (format `<dt>` sans
  `id`, slug regénéré depuis le terme). **Lié à la routine** via une
  nouvelle étape 6ter (`docs/routine-prompt.md`) : purement mécanique,
  copie conditionnelle du terme+définition déjà rédigés pour le lexique
  du jour vers `glossaire.html` s'il n'y est pas déjà — aucune nouvelle
  rédaction, aucun jugement éditorial ajouté. Mentionné avec un lien dans
  `le-projet.html` (section « Vocabulaire »), référencé dans
  `sitemap.xml`, et **ajouté au menu principal** de toutes les pages
  (retour utilisateur le jour même) entre "Archives" et "Le projet".
  Testé (recherche, filtre, rendu mobile) via Playwright avant
  publication.
- **P3 — Recherche en texte intégral** sur `archives.html` (la recherche
  actuelle ne porte a priori que sur titres/tags, pas le contenu complet
  des éditions) — demande de générer un index de recherche à la
  publication, donc touche la routine quotidienne (plus lourd, plus
  fragile vu la difficulté de synchronisation déjà rencontrée). Pas
  encore implémenté.
- **P3 — Navigation "édition suivante"** en bas de chaque archive — le
  lien "précédente" est toujours facile (le jour d'avant est connu au
  moment de publier), mais "suivante" obligerait à retoucher l'archive de
  la veille une fois figée, ce qui va à l'encontre de la règle "une
  archive ne se modifie jamais". À trancher avant d'implémenter : soit
  seulement un lien "précédente" (moins complet), soit accepter une
  exception à la règle des archives figées pour ce cas précis.

**Technique**
- **[FAIT le 4 août] Optimisation de `archives.html`** — repéré le 4 août
  (retour utilisateur) : chaque jour, l'étape 6 de la routine insérait une
  nouvelle `<li class="entry">` en tête de liste, jamais retirée, avec le
  HTML complet du bloc dépliable des 3 scénarios inliné pour chaque entrée
  (pas juste un résumé) — à 12 entrées le fichier faisait déjà ~1000
  lignes, un problème de fond de perf/maintenance à l'échelle d'une année
  de publication. **Solution retenue : chargement différé en JS.** Le bloc
  dépliable de chaque entrée sort de `archives.html` vers un petit fichier
  séparé `archives/fragments/{AAAA-MM-JJ}.html`, chargé via `fetch()`
  uniquement quand le lecteur clique sur "Scénarios" (et mis en cache côté
  DOM ensuite, `data-loaded` sur `.entry-scenarios`) — l'entrée dans la
  liste principale reste donc légère, quel que soit le nombre d'éditions
  accumulées. Les 12 éditions déjà publiées ont été migrées vers ce format
  (script Python ponctuel, pas conservé). **Au passage** (même retour
  utilisateur) : ajout du pourcentage de chaque scénario (déjà calculé
  côté édition, simplement recopié) à côté de la flèche dans les
  fragments ; et design moins touffu — les tags thématiques secondaires
  perdent leur pastille pleine au profit d'un style texte souligné
  pointillé (comme les liens de sources), seul le tag de registre
  principal garde le badge plein. `docs/routine-prompt.md` (étape 6) mis à
  jour pour ce nouveau format. Testé (recherche, filtres, tri, chargement
  de fragment) via Playwright avant publication.
- **P2 — Découpage de `archives.html` par année, à faire avant fin 2026** —
  la solution du 4 août (fragments à la demande) règle le poids téléchargé
  par visite, mais pas le fait que `archives.html` reste un fichier unique
  qui grossit indéfiniment (une ligne de plus par jour, jamais retirée) ni
  le coût d'indexation JS (recherche/filtres/tri) qui reste `O(n)` sur
  toutes les entrées à chaque chargement — pas gênant aujourd'hui, mais pas
  illimité. **Direction retenue (retour utilisateur, 4 août) :** filtrer
  par année avec l'année en cours sélectionnée par défaut ; changer d'année
  charge la liste de cette année-là (un fichier par année, ex.
  `archives-2025.html`, `archives-2026.html`...) plutôt qu'un unique
  fichier qui contient tout. Reprend le filtre "Année" déjà présent dans
  l'UI actuelle (aujourd'hui un simple filtre d'affichage sur un seul
  fichier) pour en faire un vrai changement de page/fichier. À trancher
  avant implémentation : URL de chaque année (`archives.html?annee=2025`
  ou fichiers séparés), comportement du sélecteur (rechargement de page vs
  fetch), et impact sur l'étape 6 de la routine (écrire dans le fichier de
  l'année en cours, créer un nouveau fichier au changement d'année).

**Contenu**
- **Images de partage par édition** — **écarté définitivement le 4 août**
  (risque deepfake sur des sujets impliquant de vraies personnes, décision
  ferme, ne pas reproposer).

**À surveiller (pas une tâche, un dossier ouvert)**
- **Arabie saoudite / sport** — candidat à une première page de suivi
  (retrait du financement LIV Golf par le PIF, tension avec l'investissement
  massif dans le football), mis en attente volontairement le 3 août pour
  accumuler plus de développements avant de lancer une première page. La
  routine hebdo de veille (« Détection sujets à suivre ») le re-signalera
  si ça bouge.

**À vérifier**
- **Config Buttondown de l'hebdo** : l'envoi du dimanche soir fonctionne
  (confirmé par l'utilisateur), mais le filtrage précis par tag `hebdo`
  côté Automation Buttondown n'a jamais été confirmé explicitement dans
  cette doc — à valider que les abonnés de la quotidienne ne reçoivent
  pas aussi l'hebdo par erreur (et inversement).

**Idées explicitement écartées** (pour mémoire, ne pas reproposer sans
nouvel élément) : fil d'actualité scrollable façon LinkedIn/Instagram
(pas assez de densité avec 1 édition/jour, sans réel gain vs
`archives.html`) ; comptes utilisateurs, likes, commentaires sur site
(coût backend/modération/RGPD trop élevé vs bénéfice, l'interaction
sociale reste sur Telegram) ; WhatsApp Channels (pas d'API officielle
gratuite) ; dépôt GitHub privé ou dossier privé séparé pour les docs
internes (coût opérationnel — routine à synchroniser sur deux dépôts —
jugé disproportionné vu qu'aucun contenu n'est réellement sensible).

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
    - **X (Twitter) ajouté le 6 août, via Buffer plutôt que l'API X
      directe** — voir la section dédiée dans le backlog plus haut pour le
      détail de ce qui a été tenté puis abandonné côté API X, et
      `assets/make/scenario-daily.blueprint.json` pour la config exacte
      du module Buffer.
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
- **[FAIT le 7 août] Données structurées `NewsArticle` (JSON-LD), pour
  l'éligibilité Google Actualités.** Depuis 2019 Google n'a plus de
  "soumission" avec validation humaine pour Google News — inclusion
  automatique si le site est crawlable et respecte les règles de contenu
  (déjà largement le cas : auteur identifié, dates claires, transparence
  IA, pages légales). Le manque technique principal identifié : aucune
  page n'avait de données structurées `NewsArticle`, le signal principal
  que Google utilise pour distinguer un article d'actualité d'une page
  web classique. Ajouté :
  - Bloc `<script type="application/ld+json">` dans le `<head>` de
    `index.html` et de chaque archive (headline, description, image,
    `datePublished`/`dateModified`, auteur, éditeur) — voir le schéma
    exact et les règles de reproduction quotidienne dans
    `docs/routine-prompt.md` (nouveau paragraphe après l'étape technique
    3bis).
  - Nouveau logo carré `assets/logo-512.png` (512×512, fond blanc, généré
    via Playwright à partir de `assets/logo.svg`) pour le champ
    `publisher.logo` — Google déconseille le SVG pour ce champ.
  - Appliqué rétroactivement aux 3 dernières archives qui avaient déjà des
    balises `<head>` correctes par édition (05, 06, 07 août).

  **[FAIT le 7 août] Bug préexistant corrigé rétroactivement sur les 12
  archives du 18 juillet au 4 août inclus** (pas 10 comme d'abord estimé —
  recompté en travaillant dessus). Avant correction : tagline générique
  dans `<title>`/`meta description` ("Scénario — L'actualité en trois
  hypothèses/scénarios chiffrés"), et pour les 10 plus anciennes (18
  juillet au 2 août), **aucune balise Open Graph/Twitter Card du tout** —
  pas juste un contenu générique, les balises étaient absentes. Le fix du
  4 août (étape technique 3bis de `docs/routine-prompt.md`) n'avait en
  réalité commencé à s'appliquer qu'à partir de l'édition du 5 août, pas
  rétroactivement.

  Reconstruit pour les 12 : titre réel, meta description (question posée
  extraite du corps de la page — ou rédigée à partir du `dek` pour les 2
  toutes premières éditions, 18 et 25 juillet, qui datent d'avant
  l'existence du bloc "question posée" dédié), bloc Open Graph/Twitter
  complet aligné sur le gabarit actuel, `article:author`/
  `article:published_time`, et JSON-LD `NewsArticle`. **Dates de
  publication** : 8 des 12 confirmées par le `pubDate` réel encore présent
  dans `feed.xml` (27, 29, 30, 31 juillet, 1er, 2, 3, 4 août) ; les 4
  autres (18, 25, 26, 28 juillet, absentes de `feed.xml`) n'ont pas de
  trace fiable de l'heure réelle de publication — estimées à 07:15:00
  (heure standard du site), une approximation raisonnable mais non
  garantie exacte à la minute près.
  - **Reste à faire côté utilisateur** : créer/configurer un compte
    **Google Publisher Center** pour `lesscenarios.fr` (déclaration de la
    publication — nom, sections, logo) — ne se fait pas via API/session,
    nécessite le compte Google personnel de l'utilisateur. Pas de délai
    garanti pour l'apparition dans Google Actualités/Discover une fois
    la partie technique en place, généralement plusieurs semaines.
  - **[FAIT le 7 août]** Publication ajoutée sur Google Publisher Center
    par l'utilisateur (`lesscenarios.fr`, Nom = « Scénario », France,
    français) + logos carrés fournis en fond blanc et fond noir (512 et
    1000px, `assets/logo-512.png`/`logo-1000.png` et leurs variantes
    `-black`), générés via Playwright à partir de `assets/logo.svg`.
  - **[FAIT le 8 août] Rich Results Test validé** : `NewsArticle` détecté
    comme "1 élément valide" sur `lesscenarios.fr`, aucune erreur ni
    élément invalide signalé (capture Search Console fournie par
    l'utilisateur). Reste disponible si Publisher Center demande une
    étape de configuration supplémentaire (sections, etc.), sinon ce
    point est clos.
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
  **nouvelle Routine automatique** (créée par une session via `create_trigger`,
  donc modifiable directement via `update_trigger`) tourne **chaque dimanche
  à 14h Paris**, sans validation manuelle (choix de l'utilisateur, cohérent
  avec l'automatisation complète du site). **Précision du 3 août, après une
  tentative concrète** : la routine quotidienne, elle, **n'est pas**
  modifiable directement via `update_trigger` — créée via `http_api` (hors
  session), l'outil refuse explicitement toute mise à jour dessus (« this
  routine was created via http_api, not by an agent »). Une session ne peut
  qu'y lire son contenu (`list_triggers`) ou la désactiver, jamais réécrire
  son prompt. Toute correction du prompt quotidien doit donc être recopiée
  à la main par l'utilisateur depuis `docs/routine-prompt.md` vers la
  routine réelle — contrairement à l'hebdo, entièrement autonome de ce
  côté-là. (Une note antérieure de ce fichier affirmait par erreur que les
  deux étaient modifiables directement ; corrigé après vérification.)
  L'Automation Buttondown côté RSS-to-email envoie l'email le dimanche
  soir : l'écart de quelques heures laisse une marge confortable
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

  **Page dédiée ajoutée le 6 août** (retour utilisateur : besoin d'un lien
  stable à partager sur les réseaux, pas juste l'email/RSS). Revient sur la
  décision du 3 août ci-dessous. **Mécanique retenue**, symétrique aux
  éditions quotidiennes : une page figée par semaine, `hebdo/{AAAA-MM-JJ}.html`
  (date = le dimanche du récap), qui ne bouge plus une fois publiée. Reprend
  le même contenu que l'`<item>` de `feed-weekly.xml`, mis en page avec le
  même système visuel que le reste du site (mêmes variables CSS, polices,
  masthead/nav/footer identiques à `archives.html`) — voir le fichier lui-même
  pour le détail exact des classes (`.day-block`, `.day-context`,
  `.scenario-list`/`.scenario-row`, `.week-conclusion`). Pour chacun des 7
  jours : eyebrow (registre), titre lié à l'archive complète, la question
  posée du jour (`.day-context`, reprise de `.question-text` de l'archive
  citée — sert de contexte, "ce qu'on évalue"), puis les 3 scénarios en
  liste compacte (flèche + pourcentage + libellé, le plus probable en gras
  via `.is-winner` plutôt qu'un encadré — **premier jet en grille à cartes
  bordées jugé "trop lourd" par l'utilisateur, remplacé par cette liste plus
  légère**). Une conclusion de semaine tout en bas. `<link>` de l'`<item>`
  RSS pointe désormais vers cette page précise (plus `archives.html` en
  générique).

  **Découverte sur le site — deux itérations le 6 août.** Premier essai :
  section "Récaps hebdo" séparée en haut de `archives.html`, liste à part
  des éditions quotidiennes. Retour utilisateur : grossirait indéfiniment au
  fil des semaines et repousserait la liste des éditions quotidiennes de
  plus en plus bas — pas tenable à long terme. Remplacé par une intégration
  directe dans le fil `#entries` : le récap devient une **entrée comme les
  autres**, positionnée chronologiquement juste après l'entrée de l'édition
  quotidienne du dimanche correspondant (classe `entry-weekly` en plus de
  `entry`), avec un badge "Récap de la semaine" (`<button class="tag
  entry-weekly-badge" data-tag="hebdo">` — réutilise le système de tags
  existant, apparaît donc aussi comme puce de filtre cliquable : **c'est ce
  qui permet de retrouver l'historique complet des récaps hebdo** en un
  clic, sans liste dédiée qui grossit à part) et un accordéon **"Les 7
  jours ▾"** (au lieu de "Scénarios ▾") qui charge en lazy-load
  `hebdo/fragments/{date}.html` — même mécanique que
  `archives/fragments/{date}.html`, un fragment séparé par semaine
  (uniquement les 7 `.day-block` + `.week-conclusion`, sans
  masthead/nav/footer) pour ne pas alourdir `archives.html`. Le lien du
  titre de l'entrée continue de pointer vers la page dédiée
  `hebdo/{date}.html` (toujours utile pour le partage réseaux sociaux — un
  lien stable, pas juste un aperçu inline). Toujours **pas d'entrée dans le
  menu principal** (prématuré, un seul récap existant pour l'instant).
  Entrée ajoutée aussi dans `sitemap.xml` (`changefreq: never`, comme les
  archives quotidiennes, `priority: 0.5`).

  **La routine quotidienne (7h15) n'a besoin d'aucune adaptation** : elle
  insère toujours sa nouvelle entrée en tête de `#entries`, sans se soucier
  du contenu plus bas dans la liste — aucune collision possible avec
  l'entrée hebdo positionnée ailleurs dans le fil.

  **Revenu sur la décision du 3 août — relais Telegram/LinkedIn/X ajouté
  le 6 août.** Un scénario Make dédié ("Scenario Weekly : RSS -> Réseaux
  Sociaux"), séparé de "Daily", tourne sur `feed-weekly.xml` — même
  structure que "Daily" : RSS "Watch" (1 item max) → Router → LinkedIn
  "Create a Company Text Post" / Telegram "Send a Text Message" / Buffer
  "Create a status update" (X). Textes adaptés au format hebdo (`Title` +
  `Comments` + "Lire le récap ici/complet" + `URL`, pas d'invitation à
  voter/sondage Telegram contrairement à "Daily" — pas de sens pour un
  récap). Sauvegarde complète : `assets/make/scenario-weekly.blueprint.json`.

  **Côté Buttondown [FAIT le 7 août]** : un seul formulaire sur
  `newsletter.html` depuis le 7 août (voir « Bug corrigé + UX simplifiée »
  plus haut dans le backlog), deux cases à cocher — deux clés `metadata`
  séparées et indépendantes (`metadata__quotidien=oui` /
  `metadata__hebdo=oui`) plutôt qu'un seul champ
  `metadata__subscription_type` partagé qui s'écrasait. Les deux
  Automations RSS-to-email (dont celle branchée sur `feed-weekly.xml`)
  sont configurées et filtrent bien sur `metadata.quotidien == "oui"` /
  `metadata.hebdo == "oui"` — confirmé par l'utilisateur. Reste à migrer
  les abonnés existants qui n'ont que l'ancien
  `metadata.subscription_type` (voir note complète plus haut dans le
  backlog).
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

  **Clôture d'un sujet suivi, décidée le 8 août — pas un nouveau
  système, un état final sur celui-ci.** Réflexion menée avec
  l'utilisateur sur un « track record » (mesurer si les scénarios
  publiés se réalisent vraiment) : plutôt que construire une page/base
  séparée, un sujet suivi peut simplement se **clôturer** — sa dernière
  version devient définitive.

  - **Condition de clôture : un fait réel, vérifié et sourcé, confirme
    clairement lequel des 3 scénarios s'est réalisé** — jamais le seul
    franchissement d'un seuil de probabilité interne (idée écartée après
    discussion : une probabilité élevée reste notre propre confiance, pas
    un fait vérifié ; clôturer dessus risquerait de figer un verdict
    juste avant un retournement, et s'apparente à de l'auto-évaluation).
    Un seuil de probabilité franchi (≥ 80% ou ≤ 20% sur un scénario) ou
    une échéance connue atteinte servent de **déclencheur pour aller
    vérifier**, pas de critère de clôture en eux-mêmes.
  - Cette version finale suit le même format que les autres (cartes
    `.mini-scenarios`, comparaison à la version précédente), mais son
    titre de version est explicitement marqué **« VF — Résolu »**
    (au lieu de « V2 », « V3»...) et son texte d'intro doit rappeler en
    une phrase ce qui avait été prédit en V0 (quel scénario était jugé
    le plus probable, à quel %) avant de dire ce qui s'est réellement
    passé — le contraste prédiction/réalité doit être lisible sans avoir
    à remonter voir V0 soi-même.
  - **Badge changé sur `archives.html` et sur la page elle-même** :
    `✅ Résolu le {date}` à la place de `🔄 Suivi mis à jour le {date}`.
  - **Une fois clôturé, le sujet sort de la section « Suivis actifs »**
    de `docs/sujets-a-suivre.md` (plus besoin de le repasser en revue à
    chaque passage de la routine de détection) — mais la page
    `suivi/{sujet}.html` elle-même reste en ligne en permanence, comme
    une archive, jamais supprimée.
  - **Processus toujours entièrement manuel** : comme pour toute mise à
    jour de suivi, la clôture n'est jamais automatique — la routine de
    détection (voir plus bas) peut la **signaler** comme probable, la
    décision et la rédaction restent celles de l'utilisateur en session.
  - Pas de page d'index dédiée ("track record") pour l'instant — trop tôt
    vu le faible nombre de sujets suivis actuellement. À reconsidérer une
    fois plusieurs sujets réellement résolus (voir aussi la section
    Backlog en tête de ce document).

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

  **Fusionné dans le scénario "Daily" le 6 août** (retour utilisateur :
  le plan gratuit Make est limité à 2 scénarios actifs simultanément, et
  l'ajout de Buffer/X avait fait passer le compte à 3). Le module RSS
  dédié à `feed-suivi.xml` a été **remplacé par un module "Retrieve RSS
  feed items"** (action normale, pas un déclencheur — contrairement à
  "Watch", elle peut être placée n'importe où dans un scénario, pas
  seulement en premier module) et rattaché comme **4e branche du Router**
  du scénario "Daily" existant, avec son propre sous-Router vers
  LinkedIn/Telegram/Buffer. Résultat : 2 scénarios actifs au total
  ("Daily" fusionné + "Weekly"), reste sur le plan gratuit Make. Détail
  technique et texte exact des modules : voir la sauvegarde JSON du
  scénario, `assets/make/scenario-daily.blueprint.json` (exportée le
  6 août, à ré-exporter et remplacer si le scénario est modifié par la
  suite — pas de synchronisation automatique).

  **[FAIT le 8 août] Bug de répétition corrigé** — "Retrieve RSS feed
  items" n'a pas de mémoire des items déjà vus (contrairement à "Watch"
  sur `feed.xml`), donc à chaque exécution du scénario "Daily" (1x/jour)
  il renvoyait le dernier item de `feed-suivi.xml` **qu'il ait déjà été
  traité ou non**, ce qui repostait la même mise à jour de suivi tous les
  jours tant qu'aucune nouvelle n'était publiée.

  **Fix appliqué** : champ `filterDateFrom` du module 30 (RSS SUIVI),
  jusque-là vide, rempli avec une formule dynamique qui ne retient que les
  items publiés dans les dernières ~24-48h glissantes :
  ```
  {{parseDate(formatDate(addDays(now; -1); "YYYY-MM-DD"); "YYYY-MM-DD")}}
  ```
  (= hier à minuit, recalculé à chaque exécution). Une première version de
  l'idée comparait à "aujourd'hui" plutôt que "hier" — écartée après
  retour utilisateur : une mise à jour de suivi publiée en fin de journée,
  après le passage quotidien du scénario (~7h15), n'aurait alors jamais
  été reprise (le lendemain, "aujourd'hui" ne correspond plus à sa date de
  publication). La fenêtre glissante sur 2 jours corrige ce cas.

  **Testé et vérifié le 8 août** : sur l'item Spider-Man déjà présent
  (`pubDate` du 1er août), `Date from` calculé à `7 août 2026 00:00` — la
  fenêtre de 24-48h l'exclut bien puisqu'il date de plus d'une semaine,
  confirmant que le filtre fonctionne.

  **Limite résiduelle assumée, non corrigée** : la fenêtre de 2 jours peut
  provoquer un **doublon** (pas un silence, contrairement à l'ancienne
  version) si une mise à jour est publiée **avant** l'heure de passage du
  scénario le jour même — elle tomberait alors dans la fenêtre glissante
  deux exécutions de suite. Risque jugé faible et accepté en connaissance
  de cause (mises à jour de suivi rares, manuelles) plutôt que de mettre
  en place la solution plus lourde (Data Store mémorisant les `guid` déjà
  postés, immunisée à tout problème de fenêtre temporelle) — envisageable
  plus tard si des doublons sont effectivement constatés en pratique.
  - **Reste à faire** : réexporter `assets/make/scenario-daily.blueprint.json`
    pour refléter ce changement (pas fait automatiquement, l'utilisateur
    doit le réexporter depuis Make après modification).
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
  août, passée en seuil chiffré + email le 7 août.** Une Routine dédiée
  (`trig_01BYYviSQge2CDcYkzBbYcjT`, **lundi/jeudi/vendredi/samedi, 18h
  UTC ~20h Paris (le soir, pour ne pas se superposer à la routine
  éditoriale du matin et étaler la charge)**, distincte de la routine
  éditoriale) relit
  `docs/sujets-a-suivre.md` : les « Suivis actifs » systématiquement, et
  le « Journal des sujets publiés » **limité aux 30 derniers jours** —
  au-delà, un sujet qui n'a pas justifié de suivi dans le mois qui suit sa
  publication n'en a probablement pas besoin rétroactivement (fenêtre
  volontairement bornée : sans ça, le journal grossissant indéfiniment
  d'une ligne par jour, la recherche deviendrait de plus en plus lourde au
  fil des mois/années). D'abord passée en quotidien le même jour, puis
  ramenée à lundi/jeudi/vendredi par précaution sur la consommation — pas
  de visibilité précise sur le coût en tokens d'un passage quotidien,
  l'utilisateur a préféré rester prudent tant que ce n'est pas confirmé —
  puis samedi ajouté juste après (4x/semaine au final).

  Pour chaque « Suivi actif », depuis le 7 août la routine ne se contente
  plus d'un jugement qualitatif ("il y a du neuf ou pas") : elle **réestime
  chiffre à l'appui** la probabilité de chaque scénario (même sérieux
  méthodologique qu'une édition normale), la compare à la dernière version
  publiée (`evoData` de `suivi/{sujet}.html`), et marque **⚠️ seuil
  franchi** si l'écart atteint **≥ 20 points** sur au moins un scénario,
  ou qu'un événement rend un scénario clairement caduc/résolu. Pour les
  entrées du journal (pas encore de page dédiée), le jugement reste
  qualitatif — pas de probabilité de référence à comparer.

  **Ne crée et ne modifie jamais automatiquement une page `suivi/*.html`,
  ni le fichier `sujets-a-suivre.md` lui-même** : c'est toujours un
  rapport de veille, jamais une publication — le "go" reste une décision
  manuelle de l'utilisateur, donnée ensuite dans la session principale du
  site. Ce point n'a pas changé le 7 août malgré la demande initiale d'une
  possible auto-publication au-delà du seuil : refusé côté conception,
  discuté avec l'utilisateur, parce que réévaluer un seuil chiffré à
  chaque passage ne garantit pas d'écarter le bruit (une estimation peut
  varier un peu sans vrai fait nouveau), et parce que le rôle éditorial du
  site ("il choisit les sujets, encadre la vérification et tranche le
  ton", voir `le-projet.html`) suppose justement un passage humain avant
  publication.

  **Notification par email, ajoutée le 7 août.** Avant cette date, la
  routine tournait attachée à la session principale (`persist_session`),
  pour garder le contexte du site — son rapport arrivait comme message
  dans cette même conversation. Recréée le 7 août en mode **session neuve
  à chaque déclenchement** (`create_new_session_on_fire: true`), seul mode
  qui permette la notification par email native des Routines
  (`notifications: {email: true}`) : la session neuve n'a plus besoin de
  contexte de conversation puisque tout ce qu'il lui faut est déjà dans le
  dépôt (`docs/sujets-a-suivre.md`, pages `suivi/*.html`). Le prompt
  demande explicitement de répondre uniquement "RAS aujourd'hui." et de
  s'arrêter là quand rien n'est notable, pour que l'email de notification
  (généré côté plateforme selon si le run est jugé "noteworthy") reste
  silencieux les jours sans rien à signaler — comportement non garanti à
  100 %, la logique de "noteworthy" étant décidée côté plateforme, pas par
  la routine elle-même ; à confirmer empiriquement dans les jours qui
  suivent.

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
  - **Question tranchée le 4 août : pas de mention IA sur LinkedIn/Telegram/
    email, volontairement.** Ces canaux ne publient qu'un titre, un teaser
    et une question, qui pointent vers l'article — pas le contenu de fond
    lui-même. La divulgation vit là où le lecteur rencontre vraiment le
    texte généré (l'article, déjà couvert ci-dessus), pas sur chaque
    fragment promotionnel qui y mène. Décision aussi motivée par la
    proportionnalité : une mention "IA" sur chaque post finirait par
    ressembler à du bruit plutôt qu'à de l'info utile. Pas un avis
    juridique certifié (ni l'utilisateur ni Claude ne sont juristes) —
    à rouvrir si le sujet devient sensible ou si le volume d'audience
    change significativement.
