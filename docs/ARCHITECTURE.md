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

Idées et tâches ouvertes, consolidées ici pour ne pas avoir à les
retrouver éparpillées dans le reste du document. Mise à jour au 11 août.
Priorités P1 (fort impact, faible coût) à P3 (utile mais plus lourd ou
moins prioritaire).

**Distribution / automatisation**
- **[FAIT le 9 août] Image de pub Instagram "Suis @scenarios.actu"
  finalisée.** Base : `assets/social/instagram-ads/follow-cta-v1.png`
  (gabarit maison, identique visuellement aux posts quotidiens). Deux
  premiers résultats du 8 août écartés (vocabulaire des scénarios
  renommé sur l'un, chiffre parasite dans le fond sur l'autre — voir
  historique dans le diff, plus la peine de le détailler ici). **Repris
  le 9 août** une fois les crédits IA renouvelés, avec un nouveau
  concept demandé par l'utilisateur : une route qui se sépare en trois
  (verte/bleue/rouge, tronc doré) plutôt qu'un simple fond texturé —
  reprend visuellement le tronc/branches du logo du site. Prompt
  construit avec les mêmes garde-fous stricts que les tentatives
  précédentes (aucune modification du texte, aucun chiffre/texte
  inventé) + la nouvelle direction créative. Résultat validé, deux
  formats sauvegardés :
  - `assets/social/instagram-ads/follow-cta-v2-square.png` (1:1, 1254×1254)
  - `assets/social/instagram-ads/follow-cta-v2-4x5.png` (4:5, 1122×1402 — format demandé en second, généralement préférable sur le fil Instagram pour l'espace vertical)
  - `assets/social/instagram-ads/follow-cta-v3-4x5.png` (4:5, 1122×1402 —
    variante envoyée juste après avec un léger semis d'étoiles en fond ;
    pas un doublon exact du v2-4x5, à comparer avant de choisir laquelle
    utiliser).

  **Point de vigilance mineur, non corrigé (présent sur les deux
  versions 4:5)** : le rayon doré central passe juste derrière
  "LESSCENARIOS.FR" en bas — reste lisible mais contraste réduit à cet
  endroit précis (texte doré sur lueur dorée). Pas bloquant, à améliorer
  si besoin d'une future itération (baisser l'intensité du rayon à cette
  hauteur).
  Diffusion pas encore branchée (image prête, pas encore poussée en pub
  Meta/Instagram par l'utilisateur).

  **Retiré le 9 août : la phrase "👉 Suis @scenarios.actu".** Retour
  utilisateur : l'image doit être réutilisable sur plusieurs plateformes
  (Instagram, X...) qui n'ont pas le même identifiant de compte — un CTA
  avec un handle spécifique n'a donc plus sa place sur ce visuel
  générique. **Pas régénéré via l'outil IA** (économise des crédits) :
  retiré directement en local par interpolation verticale simple
  (script Python ponctuel, pas conservé) — pour chaque colonne de
  pixels, la bande contenant le texte est remplacée par un dégradé
  entre la ligne juste au-dessus et celle juste en dessous, ce qui se
  fond naturellement dans la lueur de la route en arrière-plan. Fichiers
  renommés en conséquence (`follow-cta-*` ne convenait plus) :
  - `assets/social/instagram-ads/brand-teaser-square.png` (1:1)
  - `assets/social/instagram-ads/brand-teaser-4x5-v2.png` (4:5, base v2)
  - `assets/social/instagram-ads/brand-teaser-4x5-v3.png` (4:5, base v3
    avec étoiles)

  **Piège rencontré et corrigé** : la bande de texte n'est pas à la même
  hauteur d'un fichier à l'autre (généré indépendamment par l'outil IA
  externe à chaque fois) — appliquer la bande détectée sur le fichier v3
  (y≈1019-1047) au fichier v2 (texte en réalité à y≈967-991) a d'abord
  produit un résultat raté (texte à moitié effacé, effet de stries). Fix :
  détecter la bande de texte **séparément pour chaque fichier**
  (recherche des pixels de la couleur dorée du texte, `#cf9d4c` avec
  tolérance) avant de choisir la zone à interpoler. Les 3 fichiers
  originaux `follow-cta-v2-*`/`v3-4x5.png` (avec la phrase) restent aussi
  dans le dépôt, au cas où une version avec CTA spécifique Instagram soit
  utile un jour.
- **P2 — WhatsApp comme canal de distribution supplémentaire.** Buffer
  limite à 3 connecteurs gratuits (déjà pris par X, Facebook,
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
- **P2 — Stratégie de pub payante (Meta/Instagram, X), discutée le 10
  août.** Pistes évoquées : petit budget test (5-10 €/jour) sur Meta Ads
  Manager (Instagram + Facebook), ciblage par centres d'intérêt
  ("actualité", "géopolitique", 15-35 ans, France), pointant directement
  vers `newsletter.html` plutôt que le site en général — Meta jugé plus
  mature/moins cher au clic que X Ads pour démarrer. Nécessite un vrai
  tracking de conversion (UTM / pixel) avant de dépenser, pour savoir si
  les clics se transforment en abonnés. **Pas encore lancé côté ads
  payantes.** En parallèle, pistes de distribution gratuite listées le
  même jour : soumission du site à Google Actualités (fondations déjà
  posées, voir schéma NewsArticle plus bas dans ce backlog), annuaire
  [DataNewsletters](https://www.datanewsletters.com/inscription-annuaire-newsletters),
  [Feedspot](https://rss.feedspot.com/) et Flipboard pour `feed.xml`.
  **Action manuelle déjà en cours côté utilisateur, en dehors de toute
  automatisation du dépôt** : envoi d'invitations Instagram (inviter des
  contacts à suivre le compte) pour faire grossir l'audience avant
  d'envisager de la pub payante — pas de suivi chiffré dans ce dépôt,
  démarche manuelle côté utilisateur.
- **P3 — Giveaway "abonne-toi à la newsletter = tirage au sort", idée du
  10 août.** Objectif : faire croître la base newsletter (MailerLite,
  **1 seul abonné actuellement**) via un jeu-concours simple. **Écarté
  pour l'instant** : avec une base aussi faible, l'effet réseau d'un
  giveaway (partages, viralité) est quasi nul — priorité d'abord à la
  distribution sur les canaux existants (site, Telegram, réseaux) pour
  bâtir une vraie base avant d'investir dans un lot. À reprendre une
  fois quelques dizaines/centaines d'abonnés atteints. Pistes de lot
  déjà discutées, du moins cher au plus engageant : goodies Scénario
  (sticker/mug), accès "premium" gratuit à vie si le site se monétise un
  jour, un livre géopolitique marquant, un an d'abonnement à un média de
  référence (Le Monde, Courrier International...), ou une carte cadeau
  généraliste. Mécanique du jeu (règles, page d'inscription, tirage) pas
  encore conçue.
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
- **[FAIT le 8 août] Image Instagram attachée aux posts X et Facebook**
  (circuit Daily). Modules 14 (X) et 32 (Facebook), même mapping que la
  branche Instagram : `useMedia: true`, `media.picture` =
  `{{4.enclosures[].url}}`. **LinkedIn volontairement exclu** (retour
  utilisateur) : le module LinkedIn poste en **Media Type = Article**
  (carte de lien cliquable, image OG du site récupérée automatiquement)
  plutôt qu'une image uploadée — passer en Image ferait perdre cette
  carte cliquable, jugé moins bon pour driver du trafic vers le site.
  **Pas fait sur le circuit RSS SUIVI** (modules 24/33, toujours
  `useMedia: false`) : `feed-suivi.xml` ne porte pas de tag `<enclosure>`
  à ce jour, rien à mapper — pas demandé, laissé tel quel. Confirmé via
  le blueprint Make ré-exporté par l'utilisateur le 8 août, qui a aussi
  capturé au passage le fix `filterDateFrom` (fenêtre glissante
  `addDays(now; -1)`) du module 30, resté en attente de ré-export depuis
  sa correction — `assets/make/scenario-daily.blueprint.json` mis à jour
  avec ce blueprint.
- **[FAIT le 11 août] Décision du 8 août inversée : LinkedIn a maintenant
  une vraie image, en abandonnant le format Article au profit d'un post
  Image natif.** Repéré le 11 août : un post LinkedIn réel de l'édition
  du jour n'affichait aucune photo (carte de lien Article sans vignette,
  malgré un montage binaire déjà en place — module `http:DownloadFile` id
  52 → module `linkedin:CreateTextShare` id 7, `media.thumbnail.data`
  mappé). Diagnostic en plusieurs étapes avec l'utilisateur :
  1. D'abord attribué à un bug de déploiement du site ce jour-là (site
     indisponible au moment où LinkedIn scanne l'URL) — cause réelle mais
     partielle.
  2. Un second post de test (site de nouveau opérationnel) a bien affiché
     une image, mais **en petite vignette carrée**, jamais en grande
     bannière — ce qui a orienté à tort vers une hypothèse de format
     d'image (carré 1080×1080 vs paysage 1.91:1 attendu par LinkedIn pour
     les grandes cartes).
  3. **Cause réelle, précisée par l'utilisateur** : pas un problème de
     format d'image, mais de **type de post**. Le module `CreateTextShare`
     en `type: ARTICLE` ne peut poster qu'une carte de lien (avec vignette
     toujours petite, quelle que soit l'image fournie) — jamais une
     grande image native dans le fil. Pour une vraie grande photo, il
     faut un module LinkedIn différent, pas une option du module Article.

  **Solution appliquée** : remplacement complet, sur la branche LinkedIn
  du circuit Daily, du duo module 52 (`http:DownloadFile`) + module 7
  (`linkedin:CreateTextShare`, type Article) par un **nouveau module
  unique, `linkedin:CreateCompanyImagePost` (id 53)** :
  - `method: "link"` — upload par URL directement, plus besoin du module
    HTTP intermédiaire (le module Image Post télécharge lui-même).
  - `url: {{4.enclosures[].url}}` — même champ que Twitter/Instagram/
    Facebook.
  - `organization: urn:li:organization:136694258` — même page qu'avant.
  - `content` : même texte qu'avant (titre + accroche + lien vers
    l'article) — le lien reste cliquable dans le texte du post, mais il
    n'y a plus de carte de prévisualisation à côté (compromis assumé :
    grande photo native, contre carte de lien cliquable perdue — inverse
    du choix du 8 août, qui privilégiait alors la carte cliquable).
  Erreur intermédiaire rencontrée et corrigée par l'utilisateur en
  configurant lui-même le module : avait d'abord choisi **"Create a User
  Image Post"** (poste en tant que profil personnel, erreur API "Member
  permissions must be used when using person as owner") au lieu de
  **"Create a Company Image Post"** (poste sur la page entreprise,
  cohérent avec tous les autres modules du scénario). Blueprint Make
  ré-exporté et validé le 11 août, `assets/make/scenario-daily.blueprint.json`
  mis à jour en conséquence. **Pas encore fait sur la branche RSS SUIVI**
  (module 22, toujours en Article/vignette vide) — voir entrée backlog
  dédiée plus bas, qui bloque de toute façon sur l'absence d'`<enclosure>`
  dans `feed-suivi.xml`.
  **Réordonnancement du texte du post, même jour** (retour utilisateur) :
  sur un post Image natif, contrairement à l'Article, le lien vers
  l'article n'est cliquable que dans le texte — donc s'il arrive après le
  titre et le contexte, il finit caché derrière le "…voir plus" de
  LinkedIn. Lien déplacé en toute première ligne, titre et contexte
  repoussés en dessous — l'utilisateur a configuré directement dans Make
  : `content` = `"👉 Lire l'analyse complète : {{4.url}}{{newline}}
  {{newline}}{{4.title}}{{newline}}{{newline}}{{4.comments}}{{newline}}"`
  (auparavant l'accroche "🔥 Nouvelle édition Scénario, à lire 👇" ouvrait
  le post et le lien arrivait en dernier). Mis à jour dans
  `assets/make/scenario-daily.blueprint.json` pour rester synchronisé
  avec la config réelle du module.
- **[FAIT le 11 août] Teaser des posts sociaux (circuit Daily) : bascule
  de `{{4.comments}}` vers `{{4.source.title}}` ("L'essentiel"), retour
  utilisateur.** `<comments>` dans `feed.xml` ne porte que la question
  brute du jour ; `<source>` est censé porter "L'essentiel" (voir plus
  haut, §UX du 8 août) — un résumé autonome et chiffré (issue la plus
  probable avec son %, signal concret à surveiller), **conçu justement
  pour ce genre d'usage** ("Autonome, lisible seul... partage, extrait",
  `docs/routine-prompt.md`). Bien plus percutant comme teaser.
  **Bug trouvé au passage** : sur l'édition du 11 août, `<source>`
  contenait par erreur le texte de "Ce qu'on évalue" (`.stakes-text`,
  qui a sa place légitime ailleurs — second paragraphe de la
  `<description>` de `feed.xml`) au lieu de "L'essentiel". Vérifié sur
  les éditions du 8, 9 et 10 août : uniquement un accroc isolé du 11,
  pas un bug systémique de la routine — corrigé directement dans
  `feed.xml` (le `<source>` du 11 août contient maintenant le vrai texte
  "L'essentiel" de la page, sans les balises `<strong>`).
  **Champ basculé sur `{{4.source.title}}`** dans les modules Telegram
  (id 8), Instagram (id 34), Facebook (id 32) et LinkedIn (id 53) du
  circuit Daily — uniquement, pas la branche RSS SUIVI (modules 23/24/
  33/22, toujours sur `{{30.comments}}`, non demandé). **X/Twitter
  volontairement exclu** : "L'essentiel" fait ~700-750 caractères selon
  les jours, très au-dessus de la limite de 280 caractères de X (le
  module 14 n'utilisait déjà pas `{{4.comments}}`, juste un tagline fixe
  générique) — l'utilisateur gère ce module lui-même directement dans
  Make plutôt que de risquer un échec de publication.
  **Revu le même jour, par plateforme, sur le critère « boucle de
  curiosité vs lien qui fonctionne vraiment »** : `source` (L'essentiel)
  donne déjà l'issue probable et son % dans le post — ça satisfait la
  curiosité sur place, ce qui n'incite au clic que si ce clic mène
  vraiment quelque part. Or **le lien "en bio" d'Instagram pointe vers
  l'index du site (l'édition du jour courant), pas vers l'article
  précis du post** — cassé par construction pour quiconque consulte un
  post après le jour J (usage courant sur Instagram : scroller un
  profil). Sur Instagram, un clic ne marchant pas de toute façon passé
  le jour J, mieux vaut un post autonome qui arrête le scroll
  (`source`) plutôt qu'une question ouverte qui pousse vers un clic
  cassé. **Telegram, Facebook et LinkedIn ont un lien direct, cliquable,
  qui pointe vers l'article précis** (`{{4.url}}`, valide quel que soit
  le jour de lecture) — là, la boucle de curiosité fonctionne vraiment :
  `comments` (question ouverte, sans le %) pousse à un clic qui mène
  quelque part. **Décision intermédiaire : `source` uniquement sur
  Instagram (id 34) ; `comments` repassé sur Telegram (id 8), Facebook
  (id 32) et LinkedIn (id 53).**
  **Revu une seconde fois le 11 août, LinkedIn seulement** : retour
  utilisateur — même sur LinkedIn (lien qui fonctionne), le réflexe
  dominant reste le scroll, pas le clic ; la minorité vraiment
  intéressée cliquera de toute façon (le lien est en tête du post,
  visible sans dépasser le "…voir plus"), le reste continue à faire
  défiler. Mieux vaut donc que le post lui-même apporte de la valeur
  pour cette majorité qui ne cliquera pas — même logique qu'Instagram.
  **Décision finale : `source` sur Instagram (id 34) et LinkedIn
  (id 53) ; `comments` uniquement sur Telegram (id 8) et Facebook
  (id 32).** Au passage, corrigé sur le module LinkedIn : un `/` parasite
  et un espace superflu introduits par erreur lors d'une réédition
  manuelle dans Make, retirés du texte de référence.
  `assets/make/scenario-daily.blueprint.json` mis à jour en conséquence.
- **[FAIT le 9 août] Bug trouvé et corrigé : champ image vide sur le
  module Instagram (Buffer), empêchait la publication.** Repéré via le
  log d'exécution Make du 9 août (run 10h00) : dans le routeur du
  circuit Daily, les modules 32 (Facebook) et 34 (Instagram) n'avaient
  **aucune ligne d'opération** (juste initialisé/finalisé), contrairement
  aux autres modules — signe qu'ils n'étaient jamais réellement exécutés
  ce matin-là. Cause trouvée en ouvrant la config du module Buffer
  Instagram (34) : le champ **« Link to an image »** était vide, alors
  que le blueprint de référence l'attend mappé sur `{{4.enclosures[].url}}`
  — sans image, Instagram (qui exige un média, contrairement à Facebook)
  ne pouvait pas publier. Corrigé par l'utilisateur en remappant `Link`,
  `Title`, `Description` et `Link to an image` sur `4.Enclosures[]:URL` /
  `4.Title` / `4.Comments` — testé avec succès le jour même (post
  Instagram publié avec la bonne image composite du 9 août, titre et
  légende corrects).
  **Point d'attention à garder en tête, pas encore résolu formellement** :
  même avec `type: now` côté Make, Buffer a placé le post en **file
  d'attente pour 21h09** au lieu de le publier immédiatement — un
  comportement Buffer/Instagram plus contraint que X/Facebook (créneau
  de file d'attente du canal, pas forcément lié à l'heure du scénario
  Make à 10h00). À publier manuellement via "Partager maintenant" dans
  Buffer si besoin d'un post immédiat, ou reconfigurer les créneaux de la
  file d'attente Instagram côté Buffer pour qu'ils tombent plus tôt dans
  la journée.
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

  **[FAIT le 11 août] Accroche courte (`hook`) réintroduite sous le
  titre — sans reproduire l'échec du 7 août.** Constat de l'utilisateur
  sur la publication du 11 août : Instagram est un usage très rapide,
  personne ne lit la légende ni ne va cliquer le lien en bio, donc le
  visuel seul (titre + 3 scénarios sans contexte) reste trop abstrait
  pour comprendre l'enjeu au premier regard. Le 7 août, une tentative
  d'ajouter la question posée du site directement sur l'image avait été
  retirée le jour même car illisible sur mobile, même agrandie — mais la
  question posée fait souvent 30-45 mots (une phrase complète), bien
  trop pour tenir sur une image déjà occupée par titre + 3 scénarios.
  **La différence cette fois : `hook` n'est jamais un extrait ou un
  copier-coller de la question posée, mais une phrase distincte, écrite
  spécifiquement pour l'image, plafonnée à ~12 mots et une seule ligne
  à l'écran.** Testé avant validation par rendu réel recadré à la taille
  d'affichage mobile (~350px de large dans le fil Instagram, pas
  seulement le PNG 1080×1080 plein format) — lisible sans problème à
  cette taille, contrairement à la tentative du 7 août. Ajouté aux deux
  gabarits (`instagram-photo-template.html` : sous le titre, `.hook`
  36px doré ; `instagram-template.html` : même principe à 44px, cohérent
  avec les tailles plus grandes de ce gabarit) et au script
  `generate_instagram_image.py` (nouveau champ `hook` du JSON, erreur
  explicite si absent alors que le gabarit l'attend). Documenté dans
  `docs/routine-prompt.md`, étape technique 8. Les pourcentages restent
  volontairement absents de l'image (effet teaser vers le lien en bio,
  décision du 7 août inchangée) — seul le choix "pas de question" a été
  révisé, avec une solution différente de celle rejetée à l'époque.

  **[FAIT le 11 août] Rééquilibrage des tailles de texte sur le gabarit
  avec photo, retour utilisateur juste après l'ajout de l'accroche.**
  Trois allers-retours successifs : le titre paraissait trop discret
  (ratio titre/masthead de seulement 1,4× sur ce gabarit, contre 1,8×
  sur le gabarit sans photo — la hiérarchie visuelle ne mettait pas
  assez en avant l'élément censé accrocher le regard en premier), puis
  les 3 options de scénario paraissaient trop petites une fois le titre
  agrandi à 96px, puis retour final demandant de revenir sur une taille
  plus petite pour limiter le recours au tronquage et de réduire un peu
  le titre. Valeurs finales retenues après vérification par rendu réel
  (titre court d'aujourd'hui + un label de scénario volontairement bien
  trop long, pour confirmer que le garde-fou de troncature reste un
  filet de sécurité rarement déclenché en usage normal plutôt que la
  norme) : titre 80px→88px, texte des options 29px→31px, flèches
  32px→34px. **Garde-fou ajouté à cette occasion** (repéré comme risque
  avant même d'être demandé, et conservé malgré le retour en arrière sur
  les tailles) : chaque option de scénario est maintenant forcée sur une
  seule ligne (`white-space: nowrap` + `text-overflow: ellipsis` sur un
  nouveau `<span class="label">` dans `generate_instagram_image.py`) —
  un label trop long tronque proprement avec `…` plutôt que de passer à
  la ligne et casser l'alignement avec la flèche. Testé avec un label
  délibérément bien trop long pour confirmer le comportement, et avec le
  contenu réel du jour pour confirmer qu'aux tailles finales retenues,
  un label normal tient sur une ligne sans jamais avoir besoin du
  tronquage. Même garde-fou ajouté au gabarit sans photo par cohérence,
  sans changer ses tailles de police (déjà plus grandes : 40px/44px).
- **P1 — Image custom par sujet (Pexels), testée le 9 août puis branchée
  sur la routine automatique le même jour.** Idée de l'utilisateur :
  remplacer le visuel généré (titre + 3 scénarios) par une vraie photo
  libre de droits liée au thème du jour, quand une bonne correspond, à
  la fois pour l'image des posts sociaux (Instagram/X/Facebook) et pour
  l'image de partage OG/Twitter Card (aujourd'hui statique,
  `og-image-v2.png`) — sinon garder le visuel généré actuel en repli.

  **Principe non négociable, explicitement posé par l'utilisateur : zéro
  risque.** Contrainte directe avec la décision du 1er août ("Photo dans
  les éditions", écartée pour risque de droit d'auteur) — même risque
  ici, potentiellement pire (posts sociaux publics). Résolu en limitant
  la source à des banques **explicitement libres de droits, usage
  commercial autorisé sans ambiguïté** : **Pexels** retenu en premier
  (API officielle uniquement, jamais de scraping — irait contre leurs
  conditions d'utilisation, donc un risque même minime). Wikimedia
  Commons volontairement écarté pour l'instant (licences mixtes sur la
  plateforme, plus de risque de mal filtrer qu'avec Pexels/Unsplash qui
  n'hébergent que du contenu déjà autorisé). Unsplash gardé en option
  pour plus tard si besoin d'une deuxième source.

  **Compte développeur Pexels créé par l'utilisateur le 8 août**, clé
  API stockée en **variable d'environnement** (`PEXELS_API_KEY`) côté
  Claude Code Remote — jamais dans le dépôt (public sur GitHub).

  **Garde-fous construits dans les scripts** (`scripts/social/
  fetch_topic_image.py` + `scripts/social/use_topic_image.py`) :
  - Recherche par **mots-clés thématiques génériques**, de préférence en
    anglais (catalogue Pexels plus riche), français courant accepté en
    repli — **jamais un nom propre, une marque ou un acronyme isolé**
    (ex. "Suno", "IA"), qui ne matche aucun tag Pexels et sort des
    résultats hors-sujet ; **jamais le nom d'une personne réelle** — pour
    ne jamais laisser une photo générique suggérer qu'elle représente un
    individu précis.
  - `fetch_topic_image.py` télécharge plusieurs candidats (jamais un
    choix automatique) dans un dossier temporaire, avec une fiche
    `credits.json` (photographe, lien Pexels, requête) pour traçabilité,
    même si la licence Pexels n'exige pas d'attribution. Recherche sans
    filtre `orientation` (bug trouvé le 9 août : le forcer sur
    `orientation=square` écartait une bonne partie du catalogue avant
    même le classement par pertinence) — le format carré est appliqué
    après coup, au téléchargement, via les paramètres d'image du CDN
    Pexels (`square_crop_url()`).
  - Revue visuelle obligatoire avant tout usage (regarder les candidats,
    Read tool) — si rien de pertinent, ne rien utiliser, garder le
    visuel généré habituel. Reste vrai même en routine automatique/sans
    supervision : c'est l'agent qui exécute la routine qui fait cette
    revue à ce moment-là, pas un humain en direct — mais le principe
    "jamais un choix mécanique sur le premier résultat, jamais forcer
    une photo médiocre" reste non négociable.
  - `use_topic_image.py` ne fait que committer le candidat déjà choisi
    vers `assets/social/topic-images/{date}.jpg` + provenance — geste
    toujours volontaire, jamais automatique en amont de cette revue.

  **Incrustation titre + scénarios sur la photo (ajouté le 9 août,
  retour utilisateur), `scripts/social/instagram-photo-template.html`** :
  au lieu d'une photo nue, le rendu final reprend l'identité visuelle du
  template généré habituel (logo, titre en gros, 3 scénarios dans un
  encart noir avec le code couleur habituel vert/bleu/rouge) mais avec
  la vraie photo en fond plutôt que le dégradé uni, dégradés noirs en
  haut et en bas de l'image pour garder tout le texte lisible.
  `generate_instagram_image.py --photo {chemin}` gère l'incrustation
  (photo encodée en data URI, injectée dans le template via
  `__PHOTO_SRC__`) — strictement rétrocompatible, le comportement par
  défaut (sans `--photo`) reste identique au pixel près à avant le
  9 août.

  **Branché sur la routine quotidienne automatique le 9 août**
  (`docs/routine-prompt.md`, étape technique 8) : la routine tente
  désormais une photo Pexels avant de générer l'image Instagram, et
  retombe silencieusement sur le visuel généré habituel si rien ne
  convient (aucun candidat pertinent, ou `fetch_topic_image.py` en
  échec) — jamais bloquant pour la publication du jour. Si une photo est
  retenue, `og:image`/`twitter:image`/le champ `image` du JSON-LD sont
  aussi mis à jour vers cette image composite (1080×1080) au lieu de
  l'image générique statique `og-image-v2.png`.

  **Reste à faire une fois testé** : brancher le fichier obtenu dans
  `feed.xml` (`<enclosure>`) et les meta `og:image`/`twitter:image`/
  JSON-LD `image` de l'édition du jour (remplace la valeur utilisée
  aujourd'hui pour l'image générée) — pas encore automatisé, à faire à
  la main la première fois pour valider le rendu avant d'envisager
  d'intégrer ça dans la routine.

  **Étendu le 10 août** avec un second recadrage 16:9 de la même photo
  (pour l'affichage dans le corps de l'article, pas juste le social/OG)
  — voir l'entrée dédiée « [FAIT le 10 août] Image dans le corps de
  l'article » plus haut dans ce backlog pour le détail.
- **Image Instagram pour le récap hebdomadaire — écarté le 8 août.**
  Envisagé un temps (voir plus haut : pipeline daily), abandonné après
  discussion : le gabarit existant (titre + 3 scénarios d'**un seul**
  sujet) ne colle pas au format weekly (7 sujets différents), demanderait
  une vraie refonte visuelle pour un gain d'engagement plus faible
  (1x/semaine vs 1x/jour) — et le weekly a déjà une distribution sociale
  sans image dédiée (Telegram/LinkedIn/X via Buffer, ajoutée le 6 août).
  `feed-weekly.xml` reste donc sans `<enclosure>`, pas de route
  Buffer/Instagram sur ce scénario Make.
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

  **Troisième variante proposée le 8 août, comparée aux deux
  précédentes** : traduire l'édition complète chaque jour + un
  sélecteur de langue (drapeau FR/EN) sur le site, sans routine séparée
  ni nouvelle sélection de sujets. Coût jugé **plus élevé que la
  variante légère**, pas plus faible malgré une apparente simplicité :
  traduire toute une édition (contexte + 3 cartes + indicateurs +
  lexique + sources) avec la même rigueur terminologique revient
  quasiment à doubler la rédaction quotidienne, et double la surface à
  maintenir à chaque futur ajustement du gabarit (JSON-LD, sommaire,
  "L'essentiel", balises `feed.xml`... tout ce qui a été touché le
  8 août aurait dû l'être deux fois). Les questions d'architecture
  restent aussi entières (sous-dossier/sous-domaine/toggle). Recommandé
  par l'utilisateur : si un jour une distribution anglophone est
  vraiment lancée, commencer par la variante légère pour tester
  l'intérêt réel avant d'investir dans un site bilingue complet.

  **Compromis recommandé, proposé le 8 août — réutiliser "L'essentiel"
  plutôt que traduire l'édition entière.** Idée née de la discussion sur
  l'architecture ("pas clair pour moi", demande explicite d'un compromis
  simple archi/token/besoin) : traduire uniquement le bloc "L'essentiel"
  (3-4 phrases, déjà rédigé chaque jour pour une autre raison) plutôt que
  toute l'édition. Concrètement :
  - **Coût** : marginal — une fraction du texte d'une édition complète,
    pas un doublement de la rédaction quotidienne.
  - **Architecture** : reste dans le paradigme statique actuel, un
    sous-dossier `en/` avec une simple page listant les "L'essentiel" du
    jour et des précédents en anglais, chacun lié vers l'édition
    française complète ("Read the full analysis (in French)"). Pas de
    gabarit à dupliquer, pas de JSON-LD/sommaire à traduire.
  - **Besoin couvert** : un vrai point d'entrée anglophone (SEO, partage
    X) sans prétendre à un site bilingue complet — le lecteur qui veut
    aller plus loin retombe sur le français, où la traduction passive du
    navigateur (déjà en place, gratuite) prend le relais si besoin.
  - Remplacerait la variante légère du 7 août (feed-en.xml → X
    uniquement) par quelque chose de plus visible sur le site lui-même,
    sans en augmenter le coût.
  **Toujours en P3, aucun développement commencé — juste la piste la
  plus claire identifiée à ce jour si le sujet est repris.**

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
- **P3 — Brief audio quotidien (TTS), idée du 10 août (brainstorm "out
  of the box" demandé par l'utilisateur).** Le format (question + 3
  scénarios + probabilités) se prête bien à un résumé audio très court
  (60-90 secondes), généré automatiquement par synthèse vocale et
  distribué en `<enclosure>` audio dans un flux — même mécanisme déjà
  utilisé pour les images (`feed.xml`), juste un autre type de fichier.
  Ouvre un canal (trajet, assistant vocal) que peu de petits médias
  exploitent. Pas chiffré : choix d'un outil TTS (coût, qualité voix
  française), script de génération, où l'héberger/le référencer. Pas
  urgent, à explorer si le reste du backlog P1/P2 est traité.
- **P3 — Image en tête de la newsletter Buttondown, implémentée le 11
  août mais non testable pour l'instant.** Balise `<img>` déjà ajoutée en
  tête du CDATA de `<description>` dans `feed.xml` (voir
  `docs/routine-prompt.md`, étape technique 8) — pointe vers la même URL
  que l'`<enclosure>` Instagram. Techniquement en place, mais **jamais
  vérifiée en conditions réelles** : impossible de tester sans risque le
  11 août, l'item du jour (`guid scenario-2026-08-11`) ayant déjà été
  traité et envoyé par Buttondown avant l'ajout de la balise — modifier
  le contenu d'un item déjà traité ne déclenche pas de nouvel envoi côté
  Buttondown, qui semble se fier au `<guid>` pour détecter la nouveauté,
  pas au contenu réellement présent dans le flux à l'instant T. Fabriquer
  un faux item pour forcer un test aurait envoyé un vrai email de test
  aux vrais abonnés — écarté pour ce risque. **À vérifier passivement** à
  la prochaine édition (le 12 août normalement) : regarder si l'image
  apparaît bien dans le vrai email envoyé ce jour-là. Si toujours absente
  malgré un item réellement nouveau, revoir l'hypothèse (peut-être un
  sanitizer HTML côté Buttondown qui retire les balises `<img>` du
  contenu RSS, ou une restriction sur les domaines d'images autorisés —
  pas vérifiable depuis cet environnement, `docs.buttondown.com` et
  `buttondown.com` étant bloqués par le réseau).
  **Mise à jour le 11 août, après-midi** : `docs.buttondown.com`
  exceptionnellement accessible depuis cette session — doc officielle
  consultée directement. Deux corrections à la piste ci-dessus : (1) la
  bonne variable est `{{ item.enclosure }}` (l'URL directement, pas un
  objet — `item.enclosure.url` n'existe pas, d'où l'échec du tout premier
  test) ; (2) le bon endroit pour ce tag est le **template RSS-to-email**
  dédié (écran distinct, propre au flux), pas l'éditeur du corps d'un
  email ponctuel testé initialement. Correctif appliqué au bon endroit
  avec la bonne syntaxe par l'utilisateur — **toujours rien affiché**,
  même résultat que l'essai `<img>` dans le CDATA de `<description>`.
  Les deux méthodes donnant exactement le même résultat nul (aucune
  trace, pas même une icône cassée) renforce l'hypothèse de départ :
  cause commune en amont (item déjà traité par Buttondown avant les deux
  correctifs), pas un problème de syntaxe. **Confirmé par l'utilisateur**
  : l'édition du 11 août était bien déjà partie avant les deux essais.
  Plan retenu, inchangé : attendre l'item réellement neuf du 12 août pour
  un vrai test ; si l'aperçu Buttondown lui-même ne montre rien non plus,
  l'utilisateur contactera directement le support Buttondown plutôt que
  de continuer à deviner de l'extérieur du compte.
- **[MOITIÉ FAITE le 12 août] Image sur les posts LinkedIn "sujet suivi"
  (`feed-suivi.xml`), repéré le 11 août en vérifiant le blueprint Make
  ré-exporté par l'utilisateur.** Le module LinkedIn de la branche RSS
  SUIVI (id 22) tente de mapper `media.title`/`media.description` mais
  laisse `media.thumbnail: {}` vide, sans aucun module en amont pour
  aller chercher une image — contrairement à la branche quotidienne, qui
  poste maintenant une vraie image via `linkedin:CreateCompanyImagePost`
  (module 53, voir l'entrée dédiée plus haut). Résultat : tous les posts
  LinkedIn "🔄 Un sujet suivi vient d'être mis à jour" partent sans photo,
  systématiquement (pas un incident ponctuel — un vrai trou structurel).
  Cause racine : `feed-suivi.xml` ne porte aucun tag `<enclosure>` à ce
  jour (confirmé le 8 août, déjà noté plus haut — "pas demandé, laissé
  tel quel").

  **Décision du 11 août révisée le 12 août.** Le plan initial (réutiliser
  l'image de l'édition d'origine, `assets/social/instagram/{date
  d'origine}.png`) supposait qu'une telle image existe toujours — faux
  pour les deux suivis actuels : la génération d'image Instagram n'existe
  que depuis le **7 août**, et Spider-Man (18 juillet) comme FIFA
  (6 août) sont tous les deux antérieurs, donc sans image d'origine à
  réutiliser. Entre-temps (12 août), chaque page de suivi a reçu sa
  **propre** image Pexels dédiée (`assets/social/topic-images/suivi-
  {sujet}[.jpg/-wide.jpg]`, voir plus haut section « Pages de suivi par
  sujet ») — devenue de fait la seule image disponible pour ces deux
  sujets, et la plus cohérente à réutiliser ici (déjà visible sur la page
  elle-même, un seul visuel par sujet suivi plutôt que deux qui
  pourraient diverger).

  **Fait le 12 août** : `<enclosure>` ajoutée aux deux items existants de
  `feed-suivi.xml`, pointant vers `suivi-{sujet}.jpg` (taille réelle des
  fichiers, pas inventée) ; gabarit d'item mis à jour dans la section
  « Annonce des mises à jour sur Telegram/LinkedIn » ci-dessous ;
  `docs/routine-detection-prompt.md` mis à jour pour que les prochaines
  mises à jour de suivi incluent systématiquement cette balise.

  **[FAIT le 12 août, clôturé] Fait côté utilisateur dans Make.com** :
  module LinkedIn 22 (`CreateTextShare`) remplacé par le module 54
  (`CreateCompanyImagePost`, `method: link`), même recette que le module
  53 de la branche quotidienne ; modules Facebook (33) et X/Twitter (24)
  passés en `useMedia: true` avec `{{30.enclosures[].url}}` ; nouveau
  module Instagram (56, même profil que le module 34) ajouté sur la
  branche RSS SUIVI. Confirmé via le blueprint ré-exporté par
  l'utilisateur le 12 août, resynchronisé dans
  `assets/make/scenario-daily.blueprint.json`. Le circuit RSS SUIVI est
  donc désormais câblé pour l'image sur les 4 réseaux, plus de trou
  structurel.

  **[FAIT le 15 août] Fenêtre de dates du module RSS SUIVI (id 30)
  resserrée à "hier uniquement"** — `filterDateFrom` =
  `{{parseDate(formatDate(addDays(now; -1); "YYYY-MM-DD"); "YYYY-MM-DD")}}`,
  `filterDateTo` laissé vide. Choix motivé : ce module n'a pas de mémoire
  entre deux exécutions (contrairement à un trigger "Watch"), donc c'est
  la fenêtre de dates elle-même qui doit empêcher qu'un même item de
  `feed-suivi.xml` soit republié sur les réseaux deux jours de suite
  (repli "hier + aujourd'hui" testé mais écarté : avec "Maximum number
  of returned items" = 1, un item resterait éligible sur 2 exécutions
  consécutives). Confirmé et resynchronisé dans
  `assets/make/scenario-daily.blueprint.json`.

  **3 erreurs de texte repérées dans cet export, corrigées à 2/3 dans un
  second export le 12 août** :
  - ✅ **[FAIT] Module 54 (LinkedIn RSS SUIVI)** : le lien `{{30.url}}`
    était en 2ᵉ ligne, derrière l'accroche — recréait le bug de
    troncature LinkedIn corrigé le 8 août sur le module 53 (lien caché
    derrière "…voir plus" s'il n'est pas sur la toute première ligne d'un
    post Image). Remonté en première ligne, confirmé dans le second
    export.
  - ✅ **[FAIT] Module 53 (LinkedIn Daily)** : `/` littéral parasite
    juste avant `{{4.source.title}}` retiré, confirmé dans le second
    export. Bonus au passage : `{{4.author}}` (toujours vide, aucune
    balise `<author>` dans `feed.xml`) a aussi disparu du module 32
    (Facebook Daily), qui ne le portait plus besoin de signaler.
  - ✅ **[FAIT le 12 août] Module 56 (Instagram RSS SUIVI)** : `text` et
    `media.description` passés de `{{30.source.title}}` (champ inexistant
    — `feed-suivi.xml` n'a jamais porté de balise `<source>`,
    contrairement à `feed.xml`) à `{{30.comments}}`, comme les modules
    23/24/33. Confirmé dans un 3ᵉ export le 12 août.

  **Les 3 erreurs de ce lot sont maintenant corrigées.** Circuit RSS
  SUIVI entièrement câblé (image + texte) sur les 4 réseaux, aligné avec
  le circuit Daily.

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
- **[FAIT le 8 août] Sommaire ancré**, en haut de chaque édition —
  `nav.toc`, juste après les boutons de partage. Passé par plusieurs
  versions le même jour : d'abord 3 ancres (Contexte/Scénarios/Sources),
  puis Lexique ajouté (oublié dans la première passe) puis Essentiel
  (5 ancres au total), **puis simplifié en fin de journée à 3 tags
  définitifs** sur retour utilisateur : `Scénarios` / `L'essentiel` /
  `Référence` — Contexte retiré (redondant, juste en dessous du
  sommaire), Lexique et Sources fusionnés en un seul tag "Référence"
  (pointe vers `#lexique`, le premier des deux — fusion des sections
  elles-mêmes prévue plus tard par l'utilisateur, pas encore faite).
  Padding/gap/taille resserrés pour que les 3 tags tiennent sur une
  ligne à 390px de large (mobile) — la version à 5 tags avait déjà ce
  problème avant même la simplification. Ajouté à `index.html` +
  `archives/2026-08-08.html`, et à `docs/routine-prompt.md` pour
  reproduction automatique chaque jour (bloc fixe, jamais de contenu
  variable). Vérifié visuellement (desktop + mobile 390px) + clic testé
  via Playwright.
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

  **Complété le 8 août, encore le même jour** : le bloc doit être
  **autonome**, lisible sans avoir lu le reste de l'article (partage,
  extrait...) — ajout d'une phrase de contexte/problématique en
  ouverture, avant l'issue probable et le signal à surveiller. Passe de
  "2-3 phrases" à "3-4 phrases" en conséquence.

  **Retouché une 3e fois le 8 août, retour utilisateur** : la structure
  n'était pas assez marquée (partait trop vite sur la conclusion) —
  imposé 3 temps distincts et dans cet ordre : problématique / contexte
  / conclusion (issue probable + signal). Et un sujet vague repéré dans
  le premier essai ("la fréquentation" sans préciser de quoi) — toujours
  nommer précisément le sujet dans la phrase de contexte, ne jamais
  présumer que le lecteur a déjà lu le reste de la page.

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
- **[FAIT, non daté précisément — repéré et corrigé le 8 août] Icônes
  pour les boutons de partage** — inspiré d'un exemple brief.eco vu le
  5 août. `.share-inline` utilise déjà des icônes SVG inline fines
  (X, Facebook, LinkedIn, WhatsApp, Telegram, copier le lien), pas de
  texte ni de logos couleur officiels des plateformes — position
  discrète juste sous le titre, conforme à la décision du 4 août. Cette
  entrée était restée non cochée par erreur alors que le travail avait
  déjà été fait entre le 5 et le 8 août ; repéré en vérifiant l'état
  réel du code plutôt que de se fier au backlog seul.
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
- **P2 — Graphiques injectés dans le contexte de l'édition, idée du 8
  août (retour externe, revue de Geok).** Aujourd'hui le contexte
  (`.dek`) est uniquement du texte + `indicator-strip` (1-2 chiffres
  isolés) — pas de vraie visualisation de tendance (ex. fréquentation
  ou part de marché sur plusieurs années), alors que ce genre de
  comparaison apparaît déjà régulièrement dans les paragraphes en prose
  (ex. l'édition du 8 août citait 156,79 M / 174,52 M / le plateau
  2023-2024 à 181 M — une vraie série chiffrée, racontée en phrase au
  lieu d'être montrée).

  **Comment faire, sans réinventer un système** : le site a déjà deux
  précédents de graphiques SVG générés dynamiquement en JS à partir d'un
  petit tableau de données — les jauges `.gauge` (arc de cercle par
  scénario) et surtout le graphique d'évolution des pages de suivi
  (`renderEvoChart()` dans `suivi/_gabarit.html`, qui lit un tableau
  `evoData` et calcule tout le SVG lui-même, sans que la routine ait à
  faire le moindre calcul de coordonnées). La piste la plus simple :
  généraliser ce même principe en un **graphique en barres** (plus
  adapté que des courbes pour des comparaisons ponctuelles type "par
  an") dans le gabarit `index.html`, que la routine alimenterait juste
  avec un petit tableau `[{label, value}, ...]` — toute la génération
  SVG resterait dans une fonction JS réutilisable, comme aujourd'hui.

  **Point de jugement à ne pas oublier** : ne pas rendre ça systématique
  chaque jour — seulement quand le contexte contient une vraie série
  chiffrée comparable (plusieurs points dans le temps ou plusieurs
  catégories), pas forcer un graphique là où 1-2 chiffres isolés
  suffisent (`indicator-strip` reste approprié pour ce cas). Même logique
  de jugement que pour "L'essentiel" : un outil de plus, pas une case à
  cocher automatiquement. Pas encore implémenté.

  **Déclencheur précisé le 10 août (retour utilisateur)** : le cas le
  plus net n'est pas n'importe quelle série chiffrée, c'est un **indice
  ou indicateur coté suivi dans le temps** — Brent, CAC 40, taux
  directeur d'une banque centrale, taux de change, inflation, etc. —
  déjà cité avec plusieurs valeurs dans le contexte de l'édition.
  Exemple concret déjà publié : l'édition du 10 août cite le **Brent**
  à « 72 dollars en juin, plus de 100 dollars le 23 juillet, environ 84
  dollars début août, contre 69 dollars en moyenne sur 2025 » —
  exactement le genre de série qui gagnerait à être montrée en graphique
  plutôt que racontée en phrase. Un indice coté a un avantage pratique
  sur une série chiffrée générique : ses valeurs successives sont déjà
  extraites et vérifiées pour la rédaction du `.dek` (pas de recherche
  supplémentaire pour construire le tableau `[{label, value}, ...]`),
  donc un bon premier périmètre pour livrer une v1 simple avant
  d'envisager d'élargir à d'autres types de séries chiffrées.

- **[FAIT le 8 août] Cohérence des KPI entre `indicator-strip` et les 3
  cartes, après une analyse approfondie demandée par l'utilisateur**
  ("réfléchit deep" sur le fait que les indicateurs des 3 cartes ne
  semblaient pas cohérents avec les KPI mentionnés plus haut dans
  l'article). Bug trouvé : le 3e indicateur de chaque carte "Indicateurs
  touchés" était différent d'un scénario à l'autre (chacun sa propre
  statistique, jamais réutilisée ailleurs) — le lecteur avait
  l'impression que chaque carte inventait son propre tableau de bord.
  Corrigé : exactement 2 KPI fixes, identiques dans les 3 cartes et déjà
  vus dans `indicator-strip`, au format visuel `.evo-current`/
  `.evo-arrow`/`.evo-prev` réutilisé du graphique d'évolution des pages
  de suivi (plus scannable qu'une phrase, utile vu que le lecteur est
  déjà à ~60% de la page). Appliqué à `index.html` et
  `archives/2026-08-08.html` (commit `d5d88d9`), documenté dans
  `docs/routine-prompt.md` pour les prochaines éditions.

- **[FAIT le 8 août] Lisibilité des 3 cartes de scénarios**, deux
  changements demandés par l'utilisateur à la suite de l'analyse
  ci-dessus ("il faut que ça soit plus facile à lire, plus agréable") :
  - Le disclaimer "Ordres de grandeur indicatifs, pas des prévisions
    garanties" était répété une fois par carte (3 fois au total, en
    dernier `<li>` de chaque liste d'indicateurs) — pur bruit répétitif.
    Factorisé en une seule footnote sous les 3 cartes
    (`<p class="indicators-note">`), avec un lien "En savoir plus sur
    notre méthode" vers `le-projet.html`, sans mention de l'IA.
  - Le paragraphe `why` de chaque carte était un seul bloc de 100-180
    mots, avec la comparaison de probabilité aux deux autres scénarios
    noyée à la fin — mur de texte difficile à parcourir, d'autant que le
    lecteur y arrive déjà à ~60% de la page. Scindé en 2 `<p class="why">`
    consécutifs : le récit factuel, puis la comparaison de probabilité
    isolée visuellement (léger séparateur en pointillés).

  Les deux changements sont appliqués à `index.html` et
  `archives/2026-08-08.html`, vérifiés visuellement (desktop + mobile)
  via Playwright, et documentés dans `docs/routine-prompt.md` pour que
  les prochaines éditions reproduisent directement ce format.
- **[FAIT le 8 août] Retire la ligne `.ai-disclosure` du footer**
  ("🤖 Recherche et rédaction assistées par l'intelligence artificielle.
  En savoir plus sur notre méthode →"), retour utilisateur : devenue
  redondante avec la footnote `.indicators-note` ajoutée juste au-dessus
  le même jour (même lien "En savoir plus sur notre méthode →" vers
  `le-projet.html`, qui contient de toute façon la mention complète de
  l'IA dans sa section "Qui fait Scénario"). Retiré de `index.html` et
  `archives/2026-08-08.html` (paragraphe + CSS associé) — **pas retiré
  des 15 autres archives déjà publiées**, qui n'ont pas la nouvelle
  footnote et n'ont donc pas ce doublon (archives figées, pas de raison
  de les toucher). Rien à changer dans `docs/routine-prompt.md` : cette
  ligne n'était jamais mentionnée explicitement dans le prompt, juste
  héritée du gabarit `index.html` recopié tel quel — sa suppression du
  gabarit suffit à ce qu'elle disparaisse des prochaines éditions.
- **[FAIT le 9 août] Rendre visible le dernier sujet de suivi mis à jour
  et le dernier récap hebdo, sans avoir à aller sur `archives.html`.**
  Constat de l'utilisateur le 8 août : un sujet suivi mis à jour (badge
  🔄 sur `archives.html`) n'était signalé nulle part sur `index.html` —
  un visiteur régulier n'avait aucun moyen de le savoir sans déjà
  connaître le mécanisme et aller chercher le filtre. Étendu le 9 août
  (retour utilisateur) au dernier récap hebdomadaire, avec le même
  besoin de visibilité.

  **Implémenté, allégé une première fois le même soir** (retour
  utilisateur : version pill initiale trop lourde visuellement) : une
  bande `.top-updates` juste sous la nav (avant le hero), toujours
  visible sans scroll — deux liens texte discrets (même style que les
  liens `.dek`, gold + soulignement pointillé, pas de pill/bordure) :
  `🔄 Sujet révisé →` et `🗓️ Récap de la semaine →`. Testé visuellement
  desktop + mobile (Playwright) avant publication.

  **Lien "Sujet révisé" rendu générique et durable** (idée utilisateur,
  9 août) — pointe vers `archives.html?tag=revise` plutôt que vers une
  page `suivi/{sujet}.html` précise. Mécanisme : un nouveau tag non
  thématique `data-tag="revise"` (« Sujet révisé »), ajouté sur les
  entrées `archives.html` qui portent déjà un `.suivi-badge` (même
  logique que le tag spécial `hebdo` existant, capté automatiquement par
  le JS de filtrage — aucune modif JS nécessaire côté tags). Un petit
  script lit `?tag=revise` dans l'URL au chargement d'`archives.html` et
  applique automatiquement le filtre + le tri "Dernière mise à jour" —
  donc ce lien pointe **toujours** vers le sujet réellement le plus
  récemment révisé, sans jamais avoir besoin d'être remis à jour sur
  `index.html`. Le seul entretien requis : ajouter le tag `revise` sur
  l'entrée concernée dans `archives.html` au moment de publier une
  nouvelle version de suivi — un geste déjà nécessaire pour poser le
  `.suivi-badge` lui-même, donc pas de travail supplémentaire.

  **[FAIT le 11 août] Lien "Récap de la semaine" désormais automatisé.**
  Resté manuel jusqu'ici (à mettre à jour à la main sur `index.html` vers
  le dernier `hebdo/{date}.html`) — un oubli lors de la publication
  manuelle du rattrapage du 9 août a laissé le lien pointer vers
  l'avant-dernier récap (27 juillet-2 août), repéré par l'utilisateur.
  La routine hebdo (`trig_01FwX1Q3xsLCMwAZt4WviUA6`, voir
  `docs/routine-hebdo-prompt.md`) inclut maintenant une étape dédiée :
  remplacer uniquement l'attribut `href` du lien `🗓️ Récap de la semaine
  →` par la page tout juste publiée, `index.html` ajouté à l'étape 5
  (git add + push). Toujours pas de lien cassé possible en cas d'oubli
  futur — juste un lien vers l'avant-dernier récap. **Piste pour aller
  plus loin, non demandée mais cohérente avec le mécanisme "revise"** :
  appliquer la même approche générique (tag + filtre) si ça devient
  gênant — pas fait, pas nécessaire tant que le rythme reste hebdomadaire.

  **[FAIT le 11 août] Vignettes Instagram sur le récap hebdo, grille 2
  colonnes + accordéon.** Trois allers-retours de retour utilisateur sur
  la même idée de départ ("mettre l'image de chaque jour, discret, sans
  allonger la page") :
  1. Premier essai : petite vignette carrée (84px) accolée au texte de
     chaque `.day-block` (image à gauche, texte à droite, `display:flex`
     sur le bloc). Fonctionnait mais jugé "trop petit vu en plus gros" —
     rollback demandé vers une vraie mise en page en colonnes.
  2. Deuxième essai : vignette agrandie à 160px (110px mobile), toujours
     accolée au texte de chaque jour empilé verticalement. Meilleur, mais
     l'utilisateur a proposé une idée différente en cours de route : "que
     les images qui contiennent le titre etc [...] deux jours par ligne
     [...] et on clique sur un bouton qui ouvre en accordéon".
  3. **Design retenu** : chaque jour devient une `.day-card` affichée
     dans une grille 2 colonnes (`.week-grid`, repasse à 1 colonne sous
     620px). L'image Instagram du jour (1080×1080, déjà générée
     quotidiennement — voir `scripts/social/generate_instagram_image.py`)
     est affichée en pleine largeur de la carte (`aspect-ratio:1/1`,
     cliquable vers l'archive) : comme cette image contient déjà le
     titre + les 3 options de scénario (sans les pourcentages, teaser
     volontaire — décision du 7 août), elle tient lieu de résumé visuel
     complet sans texte additionnel. Un bouton "Voir le détail ▾" ouvre
     un accordéon (même mécanique CSS `grid-template-rows: 0fr → 1fr`
     que `.entry-scenarios` sur `archives.html`, juste dupliquée en local
     à l'intérieur de chaque carte) révélant la question exacte, les 3
     pourcentages et le lien "Lire l'édition →" — l'information qui
     manque volontairement à l'image. Résultat mesuré sur la page
     `hebdo/2026-08-09.html` : hauteur totale de page repliée réduite de
     ~26 % par rapport à la V1 (vignette simple), malgré des images bien
     plus grandes visuellement.
  Limite connue, acceptée : dans la grille 2 colonnes, si une carte se
  déplie et sa voisine sur la même rangée reste repliée, la rangée CSS
  Grid garde la hauteur de la plus haute — un peu de vide apparaît à
  côté de la carte repliée. Comportement standard de CSS Grid (pas un
  vrai masonry), rien de cassé, juste pas parfaitement compact dans ce
  cas précis.

  **Image par défaut** (`assets/social/instagram/default.png`, generée
  une fois via Playwright — logo + baseline "Le futur en 3 scénarios"
  sur le fond dégradé habituel, sans titre puisque générique) : utilisée
  quand l'image réelle d'un jour manque. Cas concret le 11 août : les
  éditions du 3 au 6 août datent d'avant l'existence de la génération
  d'image Instagram (ajoutée le 7 août), donc `hebdo/2026-08-09.html`
  (qui couvre le 3-9 août) a 4 jours sur 7 avec l'image par défaut et 3
  avec la vraie image du jour — mélange assumé, temporaire par nature
  (toutes les semaines à partir du 16 août auront 7 vraies images,
  puisque la routine quotidienne génère déjà cette image pour chaque
  édition). Le champ `alt` de l'`<img>` reste toujours le vrai titre du
  jour même quand l'image est générique, pour l'accessibilité.

  **Portée de la retouche** : contrairement à la règle habituelle "une
  page hebdo publiée n'est jamais retouchée" (réservée aux changements de
  contenu éditorial, jamais aux évolutions de présentation), l'utilisateur
  a explicitement demandé de rétrofiter la page actuellement en ligne
  (`hebdo/2026-08-09.html` + son fragment) plutôt que d'attendre le
  prochain récap — c'est cette page qui est en fait visible depuis le
  lien `.top-updates` de `index.html`. `hebdo/2026-08-02.html` (semaine
  précédente, plus visible nulle part) n'a pas été touché.

  **Implémentation** : CSS + JS de la grille dupliqués à trois endroits
  qui doivent rester synchronisés — `hebdo/2026-08-09.html` (page figée),
  `archives.html` (car le fragment hebdo y est injecté dynamiquement dans
  `.entry-scenarios-inner`, donc `archives.html` porte sa propre copie du
  CSS `.week-grid`/`.day-card*` et un gestionnaire de clic délégué sur
  `document` pour `.day-card-toggle`, puisque ces boutons n'existent pas
  encore au moment où le script s'exécute), et `docs/routine-hebdo-
  prompt.md` (instructions + exemples HTML mis à jour pour que la routine
  du 16 août génère directement ce format — trigger `meta_mcp`, synchronisé
  via `update_trigger` le jour même). Vérifié sans bug : rendu Playwright
  desktop/mobile sur les trois fichiers, accordéon imbriqué testé dans le
  contexte réel de `archives.html` (clic sur "Les 7 jours ▾" puis sur
  "Voir le détail" à l'intérieur du fragment chargé), aucune image cassée.
- **P2 — « Signaux à surveiller » par scénario, idée du 10 août (retour
  d'une revue externe ChatGPT sur le site, filtrée — voir plus bas
  pourquoi la majorité de cette revue ne retenait rien de neuf).**
  Aujourd'hui chaque carte a des "Indicateurs touchés" (des chiffres
  déjà mesurés), mais pas de liste explicite et falsifiable écrite au
  moment de la publication du type "voici ce qui confirmerait ce
  scénario précis" — différent des pages `suivi/{sujet}.html`, qui
  réestiment après coup sans grille de lecture pré-écrite. Exemple pour
  l'édition du 10 août (Ormuz/croissance) : scénario favorable →
  réouverture du détroit, Brent < 75 $ ; scénario dégradé → nouvelles
  attaques, Brent > 120 $. Intérêt concret, pas juste cosmétique :
  donnerait à la routine de re-vérification matinale (voir plus haut,
  idée du 10 août) et à la veille hebdo (`docs/routine-detection-
  prompt.md`) des critères écrits d'avance à vérifier, plutôt que de
  réestimer à l'aveugle à chaque passage. Pas encore chiffré (emplacement
  dans la carte, longueur, cohérence avec les indicateurs déjà présents
  pour ne pas dupliquer).
- **P2 — Phrase d'accroche du concept sous le masthead, idée du 10
  août (même origine).** Un primo-visiteur découvre aujourd'hui le
  principe "1 question → 3 scénarios chiffrés" en lisant l'article du
  jour — rien ne l'explique avant. Ajouter une phrase courte sous
  "Scénario" dans le masthead (`index.html`, avant le premier article)
  résoudrait ça à faible coût, sans reconstruire la page d'accueil.
  **Explicitement pas retenu en revanche** : refondre `index.html` en
  vraie page marketing séparée (hero, "comment ça marche", CTA) —
  `index.html` **est** l'édition du jour par principe assumé du site,
  une vitrine séparée casserait ça pour un gain déjà largement couvert
  par `le-projet.html` (page "À propos" existante) et `archives.html`
  (liste + filtres déjà en place).

  **Note sur la source de ces deux idées** : revue complète d'un tiers
  (ChatGPT) sur le site, challengée avant d'en retenir quoi que ce soit
  — la majorité de ses propositions ("créer" un logo 1→3, des
  catégories, un vote Telegram avant résultat, une page "avions-nous
  raison") redécouvraient des fonctionnalités déjà en prod (logo
  actuel, `docs/tags.md`, sondage Telegram natif `sendPoll` sur
  `@scenario_fr`, pages `suivi/`) — signe qu'elle n'avait exploré que la
  home + un article, pas le reste du site. Une proposition (afficher le
  scénario central tout en haut, avant le contexte) a été explicitement
  écartée : contraire à la tension "deviner avant de savoir" déjà
  cultivée par le site (bloc "Vote avant de connaître le résultat" +
  sondage Telegram automatique, justement pensés pour que le lecteur
  parie avant de lire la résolution).
- **[FAIT le 9 août, complété le 11 août] Prompt de la routine
  quotidienne allégé de 42%**, demandé par l'utilisateur pour réduire le
  coût en tokens (~17k tokens auparavant, sans aucun cache d'un jour à
  l'autre puisque la routine repart d'un conteneur neuf chaque matin —
  donc facturé en entier tous les jours). `docs/routine-prompt.md`
  gardait, pour chaque correction ajoutée au fil des semaines, son
  historique complet ("erreur corrigée le X, retour utilisateur : …",
  exemple avant/après détaillé) — utile pour un humain qui relit le
  fichier, mais pas nécessaire à l'agent qui exécute la routine chaque
  jour (qui a besoin de la règle finale, pas du récit). Cet historique
  était de toute façon déjà dupliqué dans ce document. **Retiré du
  prompt live, gardé ici** : toutes les dates/"retour utilisateur"/
  exemples avant-après purement justificatifs retirés du texte envoyé à
  la routine, en ne gardant que la règle opérationnelle finale (format
  HTML/XML exact, conditions, exemples qui enseignent une calibration
  comme "la taxe cale" → "la taxe reste bloquée", ceux-là gardés).
  Résultat : ~17k → ~10k tokens (-42%), vérifié bloc de code HTML/XML par
  bloc de code HTML/XML pour garantir qu'aucun format ni règle
  structurelle n'a été perdu. `docs/routine-prompt.md` reste la version
  complète comme toujours ; c'est la version allégée (sans le texte
  explicatif du haut du fichier ni les dates de correction) qui est
  collée dans la routine live (`http_api`, toujours copier-coller
  manuel, pas d'`update_trigger` possible). **Modèle de la routine
  (Sonnet) volontairement inchangé** — passer à un modèle moins cher a
  été écarté (tâche de jugement éditorial non supervisée, publication
  directe sans relecture humaine, risque de réintroduire des défauts
  d'écriture déjà corrigés plusieurs fois cette session) ; seul le
  prompt a été optimisé, pas le modèle. **Complété le 11 août** : la
  première passe (9 août) avait été construite avant l'ajout de la bande
  `.top-updates`, de l'exception `.dek-list` et de l'image dans le corps
  de l'article (les trois entrées juste au-dessus) — un rebase l'a
  révélé (conflit contre `main`, qui avait avancé entre-temps), la
  passe corrigée réintègre les trois règles, toujours vérifiée bloc de
  code par bloc de code (22 blocs au total désormais) contre la version
  complète de `docs/routine-prompt.md`.

**Technique**
- **[FAIT le 14 août] `.list-box` survit à la copie quotidienne du
  gabarit sur une édition qui n'en a pas besoin — confirmé sur 2 jours.**
  Contexte complet dans la section « Encart liste (`.list-box`) » plus
  haut dans ce document : la classe équivalente `.dek-list` avait disparu
  du `<style>` d'`index.html` les 10 et 11 août (deux jours sans liste
  dans le contexte), avant de réapparaître le 12. Correctif appliqué le
  12 août : règle explicite ajoutée à l'étape technique 2 de
  `docs/routine-prompt.md` (recopier le `<style>` intégralement, jamais au
  prorata de ce que le contenu du jour utilise). **Vérification faite le
  14 août** sur les deux éditions publiées depuis le correctif
  (`archives/2026-08-13.html`, `archives/2026-08-14.html`, ni l'une ni
  l'autre n'utilisant `.list-box` dans son contenu) : `.list-box` (10
  occurrences) et `.dek-list` (4 occurrences) présentes intégralement dans
  les deux `<style>`, identiques à `index.html` — aucune régression, la
  règle du 12 août tient sur 2 jours consécutifs. Problème considéré
  résolu ; pas de garde-fou automatique supplémentaire nécessaire pour
  l'instant (à rouvrir si le symptôme revient malgré cette règle).
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
- **[FAIT le 7 août] Lien Instagram (@scenarios.actu) dans le bloc
  "Suivez-nous" du footer**, même style que les icônes existantes
  (Telegram/LinkedIn/X/Facebook). `index.html` étant le gabarit recopié
  tel quel par la routine quotidienne, les futures éditions l'héritent
  automatiquement — aucune modification de `docs/routine-prompt.md`
  nécessaire. Ajouté sur les 16 pages statiques concernées (archives
  publiées, `contact.html`, `glossaire.html`, `le-projet.html`,
  `newsletter.html`, `hebdo/2026-08-02.html`, gabarits de suivi...).
  **Au passage, bug préexistant repéré et corrigé** :
  `archives/2026-08-07.html` n'avait pas encore le lien Facebook (figée
  avant son ajout plus tôt dans la journée) — ordre des icônes uniformisé
  partout : Telegram, LinkedIn, X, Facebook, Instagram.
- **[FAIT le 11 août] Site figé en silence ~1h par un bug de build Jekyll —
  `.nojekyll` ajouté.** Repéré en creusant un 404 sur les deux nouvelles
  pages de redirection Buttondown (voir « Distribution / automatisation »
  plus bas) : GitHub Pages exécutait par défaut son build Jekyll classique
  sur ce dépôt (jamais désactivé jusque-là, alors que le site est
  purement statique — voir « Aperçu »). Ce build passe **tous les `.md` du
  dépôt** dans le moteur Liquid, y compris `docs/ARCHITECTURE.md` : le
  paragraphe décrivant en prose la syntaxe Buttondown `{% if item.enclosure
  %}` (plus bas dans ce même backlog) a été interprété comme un vrai tag
  Liquid jamais refermé par un `{% endif %}`, provoquant une
  `Liquid::SyntaxError` fatale à chaque build.
  **Conséquence passée inaperçue un moment** : tout déploiement échouait
  silencieusement depuis le commit ayant introduit ce paragraphe (~11h37) —
  plusieurs pushes suivants, dont l'ajout des deux pages de redirection
  Buttondown, sont restés invisibles en ligne, le site public restant figé
  sur le dernier build réussi. **Fix : fichier `.nojekyll` ajouté à la
  racine** — désactive complètement le traitement Jekyll/Liquid, cohérent
  avec le principe déjà documenté (« servis tels quels »). Déploiement
  suivant confirmé réussi (`pages build and deployment`, conclusion
  `success` vérifiée via l'API GitHub Actions) et pages vérifiées en ligne
  par l'utilisateur. **Le risque est neutralisé définitivement** par
  `.nojekyll`, mais éviter par prudence, à l'avenir, de coller du texte
  brut ressemblant à `{% %}`/`{{ }}` dans les fichiers `.md` du dépôt.
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
- **P3 — Données ouvertes / API publique, idée du 10 août (brainstorm
  "out of the box").** `feed.json` existe déjà en JSON structuré
  (question, scénarios, probabilités) chaque jour — le documenter comme
  un flux public **stable** (schéma figé, page dédiée "Données
  ouvertes" avec un exemple et les règles de compatibilité) permettrait
  à des tiers (chercheurs, devs, dashboards) de le réutiliser sans rien
  demander. Coût quasi nul (la donnée existe déjà), bon capital de
  sérieux/goodwill, peu de médias de cette taille le font. À trancher :
  garantie de stabilité du schéma dans le temps (breaking changes =
  casse les intégrations tierces), et si `feed.json` actuel (pensé pour
  Make/webhook) convient tel quel ou mérite un format dédié plus propre.

**Contenu**
- **[FAIT le 12 août] Restructuration des registres du week-end (retour
  utilisateur).** Deux constats croisés le même jour : (1) `sujets-prioritaires.md`
  montrait samedi (culture française) et dimanche (culture internationale)
  quasi vides (1 et 3 sujets restants), alors que lundi (géopolitique/international)
  débordait avec 17 sujets en attente, dont la moitié purement économiques
  (inflation, taux, dette, marchés, dollar, or, bitcoin, pétrole…) mélangés aux
  vrais sujets géopolitiques (Ukraine, Taïwan, Iran, guerre commerciale) dans un
  seul slot hebdomadaire. Décision : fusionner culture française + culture
  internationale en un seul registre **`culture`** (samedi) — la frontière
  France/international était de toute façon souvent artificielle (Ubisoft est
  français mais mondial, Netflix est international mais touche les abonnés
  français) — et utiliser la case libérée pour un nouveau registre
  **`économie & finance mondiale`** (dimanche), qui récupère les sujets
  économiques auparavant tassés sous lundi. Lundi redevient un registre
  géopolitique plus resserré (conflits, diplomatie, rapports de force entre
  États).

  **Règle de classement pour un sujet à cheval sur les deux** (guerre
  commerciale, tarifs douaniers…) : l'enjeu central est un rapport de force
  entre États → géopolitique/lundi ; l'enjeu central est un indicateur chiffré
  ou un marché → économie/dimanche. Deux cas tranchés à titre d'exemple lors de
  la restructuration : "Guerre commerciale USA-Chine" reste en géopolitique
  (framing État contre État) ; "Droits de douane de Trump" part en économie
  (contenu réel = batailles judiciaires et recettes tarifaires, pas un rapport
  de force diplomatique).

  **Fichiers modifiés** : `sujets-prioritaires.md` (sections renommées/scindées/
  fusionnées, 80 sujets répartis à l'identique, aucun perdu) ; `docs/tags.md`
  §1 (nouveaux tags `culture`/`economie-mondiale`, `culture-francaise`/
  `culture-internationale` marqués historiques — **jamais retaggées
  rétroactivement**, conformément à la règle déjà en place dans ce fichier) ;
  `archives.html` (`registreCanonicalOrder` étendu aux deux nouveaux tags, les
  deux tags historiques restent en fin de liste pour que le filtre continue de
  fonctionner sur les vieilles éditions) ; `docs/routine-prompt.md` (grille de
  l'étape 1, mapping des tons — dimanche rejoint désormais lundi/mercredi côté
  sobriété plutôt que jeudi/samedi) ; `index.html` (script "Demain : {registre}",
  mapping JS des jours) ; `le-projet.html` (grille publique `.rhythm-grid`,
  visible des lecteurs).

  **Non modifié, volontairement** : les archives déjà publiées
  (`archives/*.html`), les récaps hebdo déjà publiés (`hebdo/*.html`,
  `feed-weekly.xml`) et le rollback `docs/routine-prompt-rollback-2026-08-11.md`
  gardent leurs anciens libellés de registre ("culture française", "culture
  internationale", "géopolitique international") — ce sont des enregistrements
  historiques exacts de ce qui a été publié à l'époque, jamais retouchés
  rétroactivement (même principe que pour les tags).

  **Point non résolu** : le trigger live de la routine quotidienne
  (`trig_0176spj7P7E9fyTs1XBkQBWF`) tourne sur un prompt figé, stocké côté
  Claude Code Remote, qui doit être resynchronisé à la main avec
  `docs/routine-prompt.md` après cette édition (voir l'entrée backlog
  "Technique" sur `.list-box` du 12 août pour le même problème de
  synchronisation, déjà rencontré une fois ce jour-là) — la session n'a pas les
  droits `update_trigger` sur ce trigger (créé via `http_api`, pas par un
  agent).

- **[FAIT le 12 août, même jour] Sport et Économie & finance mondiale
  permutés entre jeudi et dimanche (retour utilisateur).** Repris juste
  après la restructuration ci-dessus, sur le même principe : "plus
  logique de mettre des sujets plus légers le week-end". **Sport passe de
  jeudi à dimanche, Économie & finance mondiale de dimanche à jeudi** —
  Culture (samedi) inchangée. Urgent le jour même : le 13 août (lendemain)
  tombe un jeudi, donc le nouveau mapping doit être effectif avant la
  prochaine exécution de la routine (7h Paris).

  **Fichiers modifiés, même liste que la restructuration précédente** :
  `docs/routine-prompt.md` (grille de l'étape 1 — Jeudi devient économie,
  Dimanche devient sport ; mapping des tons — jeudi rejoint lundi/mercredi
  côté sobriété, dimanche rejoint samedi côté ton enlevé ; **texte donné à
  l'utilisateur pour collage manuel dans le trigger live, urgence
  oblige**) ; `sujets-prioritaires.md` (en-têtes de section `## Sport` et
  `## Économie & finance mondiale` seulement — le contenu des sujets
  reste dans sa section, aucun sujet déplacé) ; `docs/tags.md` (notes sur
  `sport-economie` et le registre `sport`, jour mis à jour) ; `index.html`
  + `archives/2026-08-12.html` (script "Demain : {registre}", mapping JS
  des jours — indices 0 et 4 permutés) ; `le-projet.html` (grille publique
  `.rhythm-grid`).

  **Non modifié, volontairement** : les 20 archives déjà publiées
  gardent leur ancien mapping JS "Demain : {registre}" (déjà le cas pour
  la restructuration samedi/dimanche du même jour — voir juste au-dessus,
  même raisonnement : widget calculé côté client à partir de la date
  réelle du visiteur, techniquement daté sur les vieilles pages, mais
  jamais mis à jour rétroactivement par choix déjà établi).

  **Pondération France Impact par registre (discussion en cours, pas
  encore implémentée)** : le principe proposé le même jour ("ascenseur
  descend vite, escalier remonte lentement" — poids asymétrique −1,5/+1
  pour géopolitique/économie/actualité française, ±1 pour le reste) reste
  valable tel quel après cette permutation — la règle est associée au
  **nom du registre**, pas au jour de la semaine, donc aucun ajustement
  nécessaire de ce côté-là.

- **[FAIT le 7 août] `le-projet.html` : le rôle technique porte sur la
  méthode, pas juste le site.** Retour utilisateur : la phrase décrivant
  le rôle technique d'Olivier Bertrand ("il conçoit et veille au bon
  fonctionnement du site") sous-vendait le travail réel — la partie la
  plus substantielle est la **méthode quantitative des scénarios**
  (probabilités, indicateurs, critères de bascule), le site n'en étant
  que le vecteur de diffusion. Reformulé : "il conçoit et fiabilise la
  méthode quantitative qui structure les scénarios — probabilités,
  indicateurs, critères de bascule — ainsi que la gestion du site qui
  les diffuse." Rôle éditorial (choix des sujets, vérification, ton)
  inchangé juste après.
- **Images de partage par édition** — **écarté définitivement le 4 août**
  (risque deepfake sur des sujets impliquant de vraies personnes, décision
  ferme, ne pas reproposer).
- **[FAIT le 10 août] Image dans le corps de l'article.** Idée du 10 août
  (retour utilisateur : apporterait plus d'adoption), passée en P1 puis
  implémentée le jour même. **Piste initiale abandonnée en cours de
  route** : la première proposition (illustration générique/abstraite
  par registre, générée une fois et réutilisée) rouvrait sans le savoir
  un débat déjà tranché le 1er août (« Photo dans les éditions », voir
  plus bas) — une illustration IA abstraite y avait déjà été envisagée
  puis écartée, pour une raison de cohérence de design (introduire un
  élément visuel non maîtrisé), pas seulement de risque.

  **Solution retenue : réutiliser tel quel le pipeline Pexels déjà
  construit le 8-9 août** (voir plus bas, entrée « Image custom par
  sujet (Pexels) ») plutôt qu'en inventer un nouveau — la photo du jour
  y est déjà sourcée avec zéro risque (mots-clés thématiques génériques,
  jamais de personne réelle, revue visuelle obligatoire avant usage,
  repli silencieux si rien ne convient) et déjà commitée chaque jour
  dans `assets/social/topic-images/{date}.jpg`, mais seulement utilisée
  jusqu'ici pour les meta `og:image`/`twitter:image` et le post
  Instagram — jamais visible par un lecteur du site. Le seul vrai
  manque était donc la restitution, pas le sourcing.

  **Ajouté le 10 août** :
  - `scripts/social/fetch_topic_image.py` : `square_crop_url()` généralisée
    en `crop_url(url, w, h)` ; `original_url` (URL source Pexels) ajoutée
    à `credits.json` pour permettre un second recadrage plus tard sans
    nouvelle recherche.
  - `scripts/social/use_topic_image.py` : télécharge en plus un recadrage
    **16:9 (1600×900)** de la même photo déjà validée, vers
    `assets/social/topic-images/{date}-wide.jpg` — pas de nouvelle revue
    visuelle nécessaire (c'est un recrop, pas un nouveau candidat) ;
    silencieusement absent si `original_url` manque ou si le
    téléchargement échoue, jamais bloquant.
  - Gabarit (`index.html`, `docs/routine-prompt.md` étape technique 8) :
    bloc `<figure class="article-image">` inséré entre le sommaire
    (`.toc`) et le `.question-box`, légende discrète en dessous
    (« Photo : {photographe} / Pexels ↗ », style repris de
    `.sources-note`) — `alt` réutilise la description déjà écrite pour
    `og:image:alt`, aucune rédaction en double. Contenue dans la largeur
    de la colonne (`.wrap`, 920px), pas plein écran, cohérent avec
    l'esprit typographique du site. **Habillage repris le 10 août sur
    demande utilisateur, inspiré de la carte Instagram** (voir
    `scripts/social/instagram-photo-template.html`) : fondu noir en
    dégradé CSS en haut de la photo (`.article-image-scrim`, même teinte
    `--ink`), masthead logo + wordmark « Scéna**rio** » en haut à gauche
    (réutilise `assets/logo.svg`, déjà utilisé dans l'en-tête du site) —
    **du vrai texte en overlay CSS, pas une image composite pré-rendue**
    comme pour Instagram (pas de nouvelle étape de génération/script,
    toujours la même photo `-wide.jpg`). Taille du logo/wordmark ajustée
    deux fois le jour même (trop petit, puis un peu trop gros) avant de
    se stabiliser. **Titre en overlay essayé puis retiré le jour même**
    (retour utilisateur) : redondant avec le `<h1>` réel juste au-dessus
    sur la page — n'apportait qu'une répétition visuelle, déjà marqué
    `aria-hidden` donc jamais lu par un lecteur d'écran de toute façon ;
    le fondu du bas de la photo a été retiré avec lui (plus nécessaire
    sans texte à faire ressortir), seul le fondu du haut reste, pour le
    masthead. **Masthead resserré dans le coin le jour même** (retour
    utilisateur, `top: 22px`/`left: 24px` → `top: 10px`/`left: 12px`) —
    aucune valeur codée en dur dans `docs/routine-prompt.md`, seulement
    la classe `.article-image-masthead` : le style vit entièrement dans
    le `<style>` du gabarit `index.html`, recopié tel quel chaque matin
    (étape technique 3), donc ce réglage se reproduit automatiquement
    sans rien à changer dans le prompt. Testé desktop + mobile via
    Playwright avant chaque
    publication.
  - **Appliqué à l'édition du jour** (10 août, sujet Ormuz/croissance
    mondiale — la photo déjà retenue par la routine ce matin-là, un
    pétrolier vu du ciel dans le Bosphore, colle bien au sujet) :
    `index.html` **et `archives/2026-08-10.html`** mis à jour avec la
    vraie photo (CSS + bloc HTML, chemins ajustés en `../assets/...`
    depuis l'archive). **Décision initiale corrigée en cours de
    session** (retour utilisateur, l'archive avait été oubliée) : la
    règle « une archive ne se modifie jamais »
    (`docs/routine-prompt.md`, étape 10) protège les archives **datées
    d'un jour antérieur** — pas l'archive du jour même, produite par la
    même exécution de routine qu'`index.html` quelques heures plus tôt.
    Contrairement aux boutons de partage du 4 août (appliqués à partir
    de la prochaine édition, sur une archive déjà ancienne), ici
    l'archive du 10 août aurait sinon perdu la photo dès le lendemain
    matin (`index.html` écrasé par la routine, seule
    `archives/2026-08-10.html` restant comme trace permanente de cette
    édition) — pas le comportement voulu pour du contenu produit le
    jour même.
  - Pas de coût récurrent supplémentaire : un seul appel HTTP de plus par
    jour (le recadrage large), zéro nouvelle revue humaine/agent, zéro
    nouvelle dépendance.
  - **« Photo d'illustration. » ajouté en tête de légende le jour même**
    (retour utilisateur, question posée sur la pertinence de la photo
    pour Google Actualités/le partage). Constat : la recherche Pexels se
    fait par mots-clés thématiques génériques (jamais le lieu/la scène
    exacte du sujet — voir docstring de `fetch_topic_image.py`, principe
    non négociable pour le zéro-risque deepfake), donc la photo retenue
    n'est presque jamais littéralement l'événement/le lieu de l'article
    — concrètement le 10 août, une photo du détroit du **Bosphore**
    utilisée pour un article sur le détroit d'**Ormuz** (deux détroits
    différents, l'un en Turquie, l'autre entre l'Iran et la péninsule
    arabique). Pas un mensonge (légende/alt restent factuellement
    exacts sur ce qu'est la photo), mais une ambiguïté possible pour un
    lecteur pressé qui suppose que l'image illustre littéralement le
    fait relaté — évitée avec cette mention, systématique et non
    négociable dans `docs/routine-prompt.md` désormais (jamais retirée
    ni reformulée), cohérente avec l'exigence de rigueur factuelle du
    site. Appliqué à `index.html` et `archives/2026-08-10.html`.
- **[FAIT le 12 août, prompt rédigé — trigger pas encore créé] Routine
  « Inspecteur » de re-vérification matinale, idée du 10 août, détaillée
  et rédigée le 12 août (retour utilisateur).** Objectif reformulé plus
  précisément le 12 août : **améliorer l'accuracy** des articles, jamais
  retoucher un choix éditorial (scénario, probabilité, angle). Horaire
  tranché : **routine principale avancée à 6h00 Paris, Inspecteur à
  7h00 Paris** (1h d'écart — à confirmer empiriquement une fois la durée
  réelle de la routine principale observée sur quelques jours).

  **Deux niveaux de correction, tranchés le 12 août** :
  - **Corrigé seul, sans demander** (mécanique, sans ambiguïté) : CSS
    tronqué, désync `index.html`/archive du jour, `data-france-impact`/
    `data-kind` qui ne correspond pas au texte adjacent, incohérence
    numérique interne non ambiguë (majorité claire, ex. "9" à 3 endroits
    contre "10" à un seul), label brut oublié dans L'essentiel, "Notre
    évaluation" raccourci. **Plus, ajout du même jour (retour
    utilisateur) : réécriture de phrases pour la clarté/pédagogie**, avec
    des garde-fous stricts — jamais de perte de chiffre/date/nom/lien de
    causalité, jamais de suppression d'information, uniquement la forme,
    chaque réécriture journalée en avant/après complet (seule catégorie
    de correction qui touche à la formulation, donc la plus auditable).
  - **Signalé seulement, jamais corrigé seul** : probabilités qui ne
    somment pas à 100 %, incohérence numérique ambiguë, écart entre un
    chiffre cité et sa source déjà citée (la source a pu changer depuis
    la rédaction), terme de lexique orphelin — tout ce qui touche à un
    choix éditorial même indirectement.

  **Vérification des chiffres contre les sources, tranchée le 12 août**
  (question ouverte de l'utilisateur : "doit-on ouvrir les sources web et
  vérifier ?") : oui, mais **bornée aux sources déjà citées** dans la
  section `<section class="sources">` de l'article — jamais une nouvelle
  recherche sur le sujet. 3 à 5 chiffres les plus structurants seulement,
  pas chaque virgule. Source injoignable = signalé "non re-vérifiable",
  jamais bloquant.

  **Économie de tokens, ajoutée le 12 août (retour utilisateur : "l'idée
  n'est pas de défoncer nos tokens").** Le vrai levier n'est pas de
  réduire le nombre de vérifications mais de **remplacer la lecture/
  raisonnement LLM par des outils déterministes** (`grep`/`diff`/script
  Python court) partout où c'est possible : sur les 8 points de la
  section "Corrigé seul", **6 ne demandent aucun jugement** (CSS
  manquant, désync index/archive, attribut incohérent, incohérence
  numérique non ambiguë, label brut, "France Impact" raccourci) — un
  motif ou un diff suffit à les détecter, pas la peine de charger le
  fichier entier dans le contexte du modèle pour ça. Seuls **2 points**
  (clarté/pédagogie, chiffres contre sources) demandent une vraie lecture
  LLM. Plafonds explicites ajoutés pour ces deux points précis : **3
  réécritures de clarté maximum par édition**, **5 appels WebFetch
  maximum** pour la vérification des chiffres.

  **Limite honnête actée** : si les posts sociaux et la newsletter
  partent peu après la publication de 6h (via `feed.xml`), ils sont déjà
  envoyés au moment où l'Inspecteur passe à 7h — une correction ne peut
  rattraper que le site, pas ce qui a déjà circulé.

  **Journal séparé** : `docs/inspection-log.md`, une entrée par passage
  même sans rien à signaler — volontairement distinct de ce fichier pour
  ne pas noyer le journal éditorial dans du contrôle qualité quotidien.

  **Fichiers créés le 12 août** : `docs/routine-inspection-prompt.md`
  (prompt complet, structure calquée sur `docs/routine-detection-
  prompt.md`) et `docs/inspection-log.md` (squelette).

  **Relecture critique du prompt, même soir (12 août) — 4 lacunes
  soulevées, 3 corrigées dans le fichier** (la 4ᵉ, moins prioritaire,
  reste ouverte) :
  1. **Référence CSS trop vague** pour le groupe `.delta-france`/
     `.delta-gauge*`/`.delta-word`/`.delta-flag` — "recopier depuis la
     dernière archive qui la contient" est risqué car ce groupe précis a
     changé de forme **cinq fois dans la même soirée** ; une archive même
     récente peut contenir une version dépassée. Corrigé : le bloc CSS
     canonique de ce groupe est maintenant recopié texte pour texte
     directement dans `docs/routine-inspection-prompt.md`, à tenir à jour
     manuellement (même discipline que `docs/routine-prompt.md`) — les
     autres classes surveillées (`.essentiel-box`, `.list-box*`, etc.),
     stables depuis longtemps, restent sur la règle "recopier depuis la
     dernière archive".
  2. **Incohérence numérique : la règle ne vérifiait que le chiffre, pas
     le fait.** Repéré via un exemple réel de la soirée même
     (`archives/2026-08-09.html`, article Musique IA) : "9 milliards"
     (Sony seul contre Suno) et "13,5 milliards" (Sony + Universal
     combinés contre Suno + Udio, sommés dans le texte lui-même) —
     ce n'était pas une erreur, mais une règle naïve sur la seule
     correspondance de chiffres aurait pu "corriger" un article juste.
     Corrigé : le point 4 exige maintenant de confirmer même fait/même
     périmètre/même opération avant toute comparaison, avec cet exemple
     réel écrit dans le prompt pour fixer le seuil.
  3. **Aucune auto-vérification après une correction, avant de commiter.**
     Toute la soirée, chaque édition manuelle a été suivie d'un contrôle
     (balise HTML équilibrée, souvent une capture Playwright) avant d'être
     poussée — le prompt ne l'imposait pas à l'Inspecteur sur ses propres
     corrections. Corrigé : nouvelle section obligatoire — balance des
     balises + re-vérification de la sync index/archive après chaque
     correctif, plus une capture Playwright ciblée pour les correctifs
     touchant la mise en page (point 1 CSS) uniquement ; tout échec de
     vérification annule le correctif (`git checkout`) et bascule
     l'entrée en "signalé pour revue humaine" plutôt que de commiter
     quelque chose de non validé.
  4. **(Non traitée, moins urgente)** Pas de limite explicite sur le
     nombre de corrections "mécaniques" (points 1-7) par édition, alors
     que le point 8 (clarté) en a une (3 max) — à rouvrir si l'usage
     réel montre qu'une édition accumule beaucoup de petits correctifs
     le même jour.

  **Trigger créé le 13 août** : `trig_015wbeqHwALMg3EsUaZcRoWp`, via
  `create_trigger` (`created_via: meta_mcp`) donc `update_trigger`
  utilisable directement pour lui, contrairement au trigger principal.
  Session fraîche à chaque déclenchement (`create_new_session_on_fire`),
  prompt volontairement court : renvoie vers `docs/routine-inspection-
  prompt.md` comme source de vérité plutôt que de dupliquer le texte dans
  le trigger lui-même (éviter le même problème de dérive que le trigger
  principal, où deux copies existent et doivent être resynchronisées à la
  main). **Horaire provisoire : `0 6 * * *` UTC = 8h Paris**, pas 7h comme
  prévu initialement (retour utilisateur du 13 août : "tu le mets à 8h
  Paris time pour l'instant") — le temps que la routine principale soit
  avancée à 6h Paris ; rapprocher l'Inspecteur à 7h une fois ce
  rapprochement fait, pour revenir à 1h d'écart. Pas de connecteurs MCP
  attachés (Gmail/Calendar/Drive/MailerLite) : l'Inspecteur n'en a pas
  besoin, seulement des outils de base (Bash/Read/Write/Edit/WebFetch).

  **Reste à faire** : **la routine principale doit être avancée à 6h
  Paris** — hors de portée de cette session (`update_trigger` refusé sur
  ce trigger précis, créé via `http_api` — voir plus haut) : à faire
  manuellement par l'utilisateur dans l'interface Claude Code Remote. Une
  fois fait, rapprocher aussi l'Inspecteur de 8h à 7h Paris (celui-là,
  `update_trigger` fonctionne).
- **[EN COURS, idée et conception du 13 août] Routine "pub" hebdomadaire —
  rappel d'identité (manifeste) et citations sur le hasard/l'incertitude.**
  Distincte de la piste "pub payante" ci-dessus (P2, Meta Ads) : ici,
  contenu organique récurrent, pas de budget publicitaire. Objectif :
  combler l'absence de tout contenu qui parle du projet lui-même entre
  deux éditions — rétention de la communauté déjà abonnée, pas
  acquisition. **Cadence tranchée : 1x/semaine, toutes les plateformes**
  (Instagram/Facebook/LinkedIn), via un nouveau flux RSS dédié que
  l'utilisateur capturera dans Make comme les autres flux existants.

  **Banque de contenu** : `docs/pub-messages.md`, liste fermée et curée à
  la main (6 messages manifeste + 6 citations pour l'instant, brouillon).
  **Décision de principe importante** : la routine ne génère/n'invente
  **jamais** un message ni une citation elle-même au moment de l'exécution
  — risque de citation mal attribuée ou inventée par un LLM, déjà identifié
  en concevant l'Inspecteur (voir plus haut). Elle pioche uniquement dans
  cette liste, en rotation. 2 messages manifeste et 2 citations sont
  marqués `[à confirmer]`/`[attribution à vérifier]`, pas encore validés.

  **Gabarit visuel — 4 pistes explorées le 13 août** (voir
  `scripts/social/pub-template-v{1..4}-*.html` +
  `scripts/social/generate_pub_image.py`), photo de fond + fondu noir +
  mot-clé en doré (`**mot**` dans le JSON) plutôt qu'un fond uni comme
  envisagé au départ (retour utilisateur) :
  - V1 sobre : photo à peine suggérée (voile 86%), liseré de couleur.
  - V2 carte : dégradé plus travaillé, cadre fin façon `.essentiel-box`,
    grand guillemet doré en filigrane pour les citations.
  - V3 poster : voile plus léger, teinte duotone couleur, typographie
    plus grande, masthead réduit à l'icône seule.
  - V4 hybride (cadre+guillemet de V2 + typo/teinte de V3), proposé pour
    trancher une hésitation explicite de l'utilisateur entre V2 et V3.
  **Pas encore de choix final arrêté.** Correction appliquée aux 4 :
  l'URL `lesscenarios.fr` du footer ne doit pas passer en capitales
  (`text-transform:lowercase` sur `.footer .url` seulement, le tagline
  garde les majuscules).

  **Source de la photo, tranchée le 13 août (question explicite : "qui
  choisit l'image ?").** Conflit identifié avec la règle non négociable
  de `fetch_topic_image.py` ("ne choisit JAMAIS automatiquement une image
  finale [...] la sélection reste toujours un geste humain/en session") —
  une routine hebdomadaire autonome ne peut pas chercher et choisir seule
  sur Pexels sans validation. **Résolu : la routine réutilise une photo
  déjà choisie à la main cette semaine-là pour un article quotidien**
  (`assets/social/topic-images/{date}.jpg` + `.json` associé, déjà
  validée par l'utilisateur, déjà liée à l'actualité réelle de la
  semaine) — avec repli sur une petite banque de secours pré-validée si
  aucune photo n'a été choisie cette semaine-là (banque pas encore
  constituée). Aucun appel Pexels en direct par cette routine.

  **Crédit photo dans le feed** : puisque la photo est réutilisée depuis
  `assets/social/topic-images/`, le nom du photographe est déjà connu
  (champ `photographer` du `.json` associé, aucun nouvel appel Pexels
  nécessaire) — à reporter dans le `<description>` de l'item du nouveau
  flux (`feed-pub.xml`, pas encore créé), en fin de texte, sur le modèle
  des légendes déjà utilisées sous les photos d'articles ("Photographe /
  Pexels"). Pas de page web dédiée à ce post (contrairement aux articles
  et pages suivi/hebdo) donc le crédit doit vivre directement dans le
  texte du post, pas en légende sur une page.

  **Gabarit tranché le 13 août : V4 (hybride)** —
  `scripts/social/pub-template-v4-hybride.html` devient le gabarit
  définitif, étendu de 2 à 4 couleurs d'accent (une par catégorie, voir
  ci-dessous) : or (manifeste), bleu (citation), vert (question),
  orange (chiffre) — mêmes teintes que `--favorable`/`--stable`/
  `--degrade` déjà utilisées partout ailleurs sur le site.

  **2 catégories supplémentaires ajoutées le 13 août (retour
  utilisateur)**, la banque `docs/pub-messages.md` passe de 2 à 4
  sections :
  - **Questions à la communauté** : engagement pur, pas de fait à
    vérifier — notamment pour solliciter des idées de sujets pour le
    mardi "carte blanche".
  - **Le saviez-vous** : un chiffre simple, toujours prolongé par une
    question prospective à 10 ans (ex. financement des retraites). Même
    discipline que les citations, en plus stricte : **toutes les entrées
    sont marquées `[chiffre à vérifier]`** au moment de la rédaction
    (ordres de grandeur de mémoire, pas revérifiés) — aucune ne doit
    passer en rotation avant vérification sur une source primaire, la
    crédibilité du site reposant justement sur la justesse des chiffres.
  Rotation : cycle fixe manifeste → citation → question → chiffre →
  manifeste..., déduit de l'historique déjà publié dans `feed-pub.xml`
  (pas de fichier d'état séparé) — voir `docs/routine-pub-prompt.md`.

  **Crédit photo, précisé le 13 août : jamais dans le texte visible du
  post.** L'utilisateur l'ajoutera lui-même en commentaire du post une
  fois publié. La routine consigne quand même le photographe/lien Pexels
  dans un commentaire HTML invisible (`<!-- credit: ... -->`) en fin de
  `<description>` du flux, et le redonne en clair dans son résumé final
  de session pour que l'utilisateur puisse le recopier facilement.

  **Fréquence** : 1x/semaine en croisière, plus fréquente au lancement
  (pas de chiffre arrêté) — piloté uniquement par le cron du trigger,
  aucune logique de fréquence dans le prompt lui-même.

  **[FAIT le 13 août] `feed-pub.xml` créé** (scaffold, aucun item encore)
  et **`docs/routine-pub-prompt.md` rédigé** (étapes : garde-fou
  anti-doublon 20h, choix déterministe catégorie/entrée/photo, génération
  image, construction de l'item, résumé final avec crédit en clair).

  **5e catégorie ajoutée le 13 août : Grands futurs** — inventions/
  technologies réelles déjà en développement qui pourraient changer le
  quotidien (voiture autonome, fusion nucléaire, longévité, informatique
  quantique...). **Règle non négociable : toujours au conditionnel**
  ("pourrait", jamais "sera"/"va révolutionner") — même exigence
  épistémique que le reste du site (une probabilité n'est jamais une
  certitude). Vigilance particulière sur le survol technologique
  ("hype") : un secteur avec un long historique d'annonces "dans 10 ans"
  jamais tenues (quantique, fusion...) — exiger un vrai jalon concret
  déjà atteint, pas seulement une promesse marketing. Toutes les entrées
  marquées `[à vérifier]`, même discipline que la section chiffres.
  Cycle de rotation étendu à 5 : manifeste → citation → question →
  chiffre → futur → manifeste... 5e couleur d'accent ajoutée au gabarit
  V4, violet (`--futur: #9b7fc0`), pour ne pas se marcher sur les 4
  couleurs déjà prises par les autres catégories.

  **Règle transversale ajoutée le 13 août : "dénominateur commun"
  engageant/positif/orienté croissance.** Chaque entrée, toutes
  catégories confondues, doit se terminer par un CTA qui pousse à agir
  (abonnement, commentaire) — pas rester un simple rappel d'identité
  passif ; le ton reste positif/curieux même sur un sujet sérieux
  (retraites, climat), jamais alarmiste. CTA ajouté/renforcé sur toutes
  les entrées existantes (manifeste → "Abonne-toi, c'est gratuit" ;
  citations → CTA d'abonnement ajouté à toutes ; chiffres/futurs → CTA
  reformulé pour inviter explicitement à commenter plutôt qu'une question
  purement rhétorique). 2 citations (Voltaire, Héraclite) repérées comme
  moins "positives" en ton — gardées avec CTA compensatoire, décision de
  les retirer ou non laissée à l'utilisateur.

  **Enrichissement du 13 août (retour utilisateur), 3 ajouts** :
  1. Manifeste : `manifeste-07`, message dédié à l'inscription newsletter
     (canal distinct de "s'abonner" sur les réseaux) — "100% réalisable,
     jamais de science-fiction".
  2. Citations : 2 dictons populaires plutôt que des citations d'auteur —
     `citation-11` (slogan réel de la Française des Jeux, "100% des
     gagnants ont tenté leur chance", assumé comme slogan et non déguisé
     en citation ; sujet sensible jeu d'argent, à retirer si ça pose
     problème en relecture) et `citation-12` ("on descend par l'ascenseur,
     on remonte par l'escalier", dicton de trader, pas d'auteur nommé —
     fait écho à l'idée de pondération asymétrique du France Impact,
     encore non implémentée, voir plus haut dans ce backlog).
  3. Grands futurs : 3 nouvelles entrées `futur-05/06/07` côté **grands
     risques du siècle** (climat, IA, pandémie) en plus des 4 déjà
     existantes côté inventions — même catégorie/rotation, même règle du
     conditionnel obligatoire, et vigilance dans les deux sens (ni hype
     ni alarmisme, voir "Dénominateur commun").
  4. Questions : `question-01` (proposer un sujet) retiré — retour
     utilisateur : "on n'en sait rien, les gens scrollent", une question
     qui demande de construire une idée ne marche pas dans un feed.
     Remplacé par `question-04` ("le vrai risque pour la société dans 10
     ans"), qui demande un avis plutôt qu'une proposition. Variante "quel
     est ton rêve" écartée par l'utilisateur lui-même comme trop convenue.

  **Ton, retour utilisateur du 13 août : "moins IA style, plus naturel".**
  Passe de nettoyage sur les CTA les plus répétitifs — le même "Abonne-toi,
  c'est gratuit" recopié presque identique sur 6+ entrées manifeste/
  citations, varié en formulations plus naturelles et propres à chaque
  entrée plutôt qu'un gabarit recopié. Vigilance à garder pour toute
  future entrée : éviter la construction trop symétrique/générique typique
  d'un texte généré, préférer une formulation qui sonnerait bien dite à
  voix haute.

  **[FAIT le 13 août] Banque de secours de photos constituée** —
  `assets/social/pub-photos/`, un paysage par registre (7 photos Pexels,
  recherchées et proposées en session, validées par l'utilisateur avant
  commit — jamais un choix automatique). **Premier jet écarté par
  l'utilisateur** : "des paysages plus beaux, ça fait rêver, pas des
  ordis/tours" — bureau de labo, gros plan de journal, tours de Paris la
  nuit jugés pas assez "dreamy". Deuxième jet, uniquement des paysages :
  Europe la nuit vue de l'espace (géopolitique), route ouverte vers
  l'horizon (carte blanche), Alpes au coucher de soleil (actualité
  française), porte-conteneurs sur la mer dorée (économie mondiale),
  aurore boréale (sciences), amphithéâtre antique au soleil couchant
  (culture), coureurs en silhouette au coucher de soleil (sport) —
  validé. Crédits dans `assets/social/pub-photos/credits.json`.

  **Grands futurs, réécriture complète le 13 août** (retour utilisateur :
  "pas de trucs bateau, pas besoin d'écrire des trucs que tout le monde
  sait") — les 7 entrées initiales (voiture autonome, fusion en général,
  longévité en général, quantique en général, climat "risque n°1", IA
  "hors de contrôle", pandémie générique) jugées trop génériques/déjà
  connues. Remplacées par des faits **précis, datés, spécifiques** : le
  premier gain net de fusion (déc. 2022, NIF), la bio-impression de
  tissus vivants, les interfaces cerveau-machine déjà testées sur des
  patients réels, les vaccins ARNm anti-cancer en essai, des IA prises à
  tricher lors de tests contrôlés, le retrait d'assureurs américains des
  zones à risque climatique, la surveillance de virus zoonotiques
  ("maladie X" de l'OMS). Règle ajoutée au prompt : si un lecteur qui
  suit un peu l'actualité tech/science hausse les épaules ("ça, je le
  savais déjà"), l'entrée est à refaire.

  **Mécanisme changé le 13 août, dans la foulée : plus une liste fermée
  pour cette catégorie précise.** Retour utilisateur direct : "je ferai
  pas une liste ferme sinon ça tourne et c'est boring". Contrairement aux
  4 autres catégories (banque curée, jamais de génération par la
  routine — risque de citation/chiffre inventé déjà établi), la catégorie
  `futur` peut désormais **chercher un nouveau fait à chaque tour**
  (WebFetch, 3 appels max, uniquement 1 fois sur 5 dans le cycle) plutôt
  que de piocher uniquement dans un stock fixe. Garde-fous : toujours une
  vraie source vérifiée avant d'écrire (jamais une invention libre comme
  le reste des 4 catégories), repli sur la liste existante si la
  recherche ne trouve rien de solide, nouvelle entrée toujours ajoutée
  avec sa source (URL) dans `docs/pub-messages.md` — la banque grandit
  organiquement dans le temps plutôt que de tourner en boucle sur un
  stock figé. Seule catégorie de toute la routine "pub" où une vraie
  recherche LLM est nécessaire — accepté comme coût raisonnable vu que ça
  ne se déclenche qu'1 fois sur 5, et que le risque (mauvais fait publié
  en post social) est bien plus faible que sur l'Inspecteur, qui édite le
  site lui-même.

  **[FAIT le 13 août] Nettoyage : toutes les entrées non confirmées
  retirées** (retour utilisateur : "enlève les trucs qui sont pas
  confirmé"), plutôt que de les laisser trainer en attente de
  vérification. 16 entrées retirées : `manifeste-05/06` (affirmations sur
  le modèle économique), `citation-04/09/10` (Anatole France, Bernanos,
  Bergson — attribution non confirmée), `citation-13` (Einstein "Dieu qui
  se promène incognito" — retirée malgré la demande explicite de
  l'utilisateur de l'ajouter plus tôt dans la journée, son statut de
  citation la plus fréquemment mal attribuée à Einstein en ligne restant
  inchangé ; à ré-ajouter seulement après une vraie vérification si
  souhaité), `chiffre-01/02/03` (retraites, population 2050, +1,5°C),
  `futur-01` à `futur-07` (les 7 entrées, remplacées par de simples
  exemples de calibrage dans la prose, plus des entrées prêtes à
  publier).

  **Conséquence directe : 2 catégories vides.**
  - **Section 4 (chiffres) : bloquante.** Pas de mécanisme de recherche à
    la volée pour cette catégorie (contrairement à "futur") — elle ne
    publiera rien tant que personne n'y ajoute une entrée vérifiée à la
    main. `docs/routine-pub-prompt.md` la traite comme n'importe quelle
    catégorie sans entrée disponible : passée, signalée, jamais bloquant
    pour le reste du cycle.
  - **Section 5 (grands futurs) : pas bloquante.** C'est justement la
    catégorie conçue le jour même pour repartir de zéro et se
    réapprovisionner elle-même via recherche (voir plus haut) — une
    section vide au départ est son état normal, pas une anomalie.

  **[FAIT le 13 août] Catégorie "Le saviez-vous" (chiffres) retirée
  entièrement** — retour utilisateur : "on enlève la section chiffres on
  a assez pour démarrer". Section supprimée de `docs/pub-messages.md`,
  cycle de rotation réduit à 4 catégories (`manifeste → citation →
  question → futur`), toutes les références dans `docs/routine-pub-
  prompt.md` mises à jour (liste des catégories, cycle, lien par
  catégorie). Renumérotée : "Grands futurs" devient la section 4
  (`rotation D`), plus la section 5. Réintroductible plus tard si
  l'utilisateur réapprovisionne une liste de chiffres vérifiés — pas
  supprimé du concept, juste absent du cycle actif pour l'instant.

  **[FAIT le 14 août] Catégorie "Le saviez-vous" (chiffres) réintégrée,
  avec un mécanisme différent de la version retirée le 13 août** — retour
  utilisateur : des pubs automatiques qui reprennent un fait/chiffre fort
  déjà publié dans une édition (ex. un bilan chiffré d'une canicule), pas
  une liste à approvisionner à la main. **Différence clé avec la version
  retirée** : l'ancienne liste demandait à l'utilisateur de fournir des
  chiffres pré-vérifiés un par un (jamais réamorcée, bloquante). La
  nouvelle version **extrait un chiffre déjà publié et déjà vérifié**
  (sources croisées, relecture) directement depuis `archives/*.html` —
  jamais une génération ou un calcul par la routine, seulement une
  citation verbatim d'un fait qui a déjà passé le processus éditorial du
  site. Ça élimine le risque de fait inventé par un LLM déjà identifié
  comme raison de retrait de plusieurs entrées le 13 août
  (`citation-04/09/10`, `chiffre-01/02/03`).

  Décisions prises avec l'utilisateur (3 questions posées, 3 réponses) :
  - **Source** : éditions quotidiennes uniquement (`archives/*.html`),
    jamais les pages de suivi ni le récap hebdo — le contenu le plus
    dense en chiffres vérifiés, le plus simple à scanner.
  - **Gabarit** : nouveau template dédié plutôt que réutiliser
    `pub-template-v4-hybride.html` — le chiffre doit être l'élément
    visuel dominant, pas noyé dans un texte sur une photo.
  - **Rotation** : 5e catégorie dans le cycle existant (`manifeste →
    citation → question → futur → chiffre → manifeste...`), pas un
    rythme séparé — garde une cadence de publication prévisible plutôt
    que d'ajouter une fréquence à gérer en plus.

  Implémenté :
  - `scripts/social/pub-template-v5-stat.html` — nouveau gabarit sans
    photo, chiffre en très grand (accent orange, même couleur "chiffre"
    déjà réservée dans `pub-template-v4-hybride.html`), phrase de
    contexte en dessous.
  - `scripts/social/generate_pub_image.py` — ajoute un champ optionnel
    `stat` (placeholder `__STAT__`), rétrocompatible : les autres
    gabarits n'ont pas ce placeholder, le `.replace()` ne fait rien sur
    eux.
  - `docs/pub-messages.md`, nouvelle section 5 : décrit le mécanisme
    d'extraction (scan des éditions des ~30 derniers jours, chiffres mis
    en `<strong>` dans `.dek`/`.essentiel-text`, exclusion des éditions
    trop récentes <24h ou déjà citées, recopie mot pour mot) plutôt
    qu'une liste fermée — section volontairement vide au lancement,
    comme "Grands futurs" le 13 août (pas bloquant, le scan la
    réalimente à chaque tour).
  - `docs/routine-pub-prompt.md` : cycle mis à jour partout (5
    catégories), nouveau point 7 dans l'étape 1 (procédure d'extraction
    complète), étape 2 (photo) sautée pour cette catégorie, étape 3
    (génération) avec la commande dédiée, table des liens étape 4 mise à
    jour (`chiffre` → l'édition source elle-même, seule catégorie sans
    page de destination fixe).

  **[FAIT le 14 août] Sélection de la catégorie : cycle qui avance
  remplacé par une table jour → catégorie fixe.** Retour utilisateur
  direct : "voici le calendrier systématique, tu ne pourras pas te
  perdre" — l'ancien mécanisme (déduire la catégorie suivante à partir du
  dernier `<guid>` publié dans `feed-pub.xml`, puis avancer d'un cran
  dans un cycle fixe) marchait, mais restait une inférence à chaque
  exécution, donc un point de fragilité évitable. Remplacé par une table
  explicite (même principe que le calendrier des éditions quotidiennes,
  `docs/routine-prompt.md`) :

  | Jour | Catégorie |
  |---|---|
  | Dimanche | `manifeste` |
  | Mardi | `citation` |
  | Jeudi | `futur` |
  | Vendredi | `manifeste` |
  | Samedi | `chiffre` |

  **`question` volontairement absente de cette table** — catégorie
  dormante, pas supprimée (ses entrées restent dans `docs/pub-
  messages.md`, section 3). Le trigger "Scénario — Pub hebdo" est passé
  le même jour à 5x/semaine (`0 16 * * 0,2,4,5,6` UTC — dimanche, mardi,
  jeudi, vendredi, samedi), un jour de calendrier par jour de trigger,
  aucun jour de la table n'est orphelin de déclenchement et
  inversement. Mis à jour : `docs/routine-pub-prompt.md` (étape 1, point
  2), `docs/pub-messages.md` (section "Règle de rotation").

  **[FAIT le 14 août] Routines déplacées à la nuit pour ventiler la
  charge.** Retour utilisateur direct : "est-ce que la routine pub etc
  peuvent tourner la nuit pour ventiler la charge". Avant ce changement,
  Pub hebdo et Détection tournaient toutes les deux en soirée (18h et
  20h Paris), proches l'une de l'autre et de la fin de journée ; Daily
  (6h) et Inspecteur (6h50) restaient groupées le matin. Nouveau
  planning, toutes routines Scénario confondues :

  | Heure Paris | Routine | Trigger | Cron UTC |
  |---|---|---|---|
  | 0h00 | Détection sujets à suivre | `trig_01BYYviSQge2CDcYkzBbYcjT` | `0 0 * * 1,4,5,6` |
  | 2h00 | Pub hebdo | `trig_01A1XU5Kpc4QWzApjZPqcKpj` | `0 2 * * 0,2,4,5,6` |
  | 6h00 | Daily (routine éditoriale principale) | `trig_0176spj7P7E9fyTs1XBkQBWF` | `0 4 * * *` *(inchangé)* |
  | 7h00 | Inspecteur | `trig_015wbeqHwALMg3EsUaZcRoWp` | `0 5 * * *` |

  Ordre choisi pour garder un espacement régulier (2h entre chaque) tout
  en respectant les deux ancres demandées par l'utilisateur (Daily 6h,
  Inspecteur 7h) et en gardant les mêmes jours de la semaine qu'avant
  pour Pub et Détection (seule l'heure change). Mis à jour :
  `docs/routine-pub-prompt.md`, `docs/routine-detection-prompt.md`,
  `docs/routine-inspection-prompt.md` (en-têtes).

  **[FAIT le 13 août] Trigger créé** : `trig_01A1XU5Kpc4QWzApjZPqcKpj`,
  cron `0 16 * * 2,5` UTC = **mardi et vendredi 18h Paris** (2x/semaine,
  cadence de lancement choisie par l'utilisateur, à ramener à 1x/semaine
  plus tard si besoin via `update_trigger` — utilisable directement,
  `created_via: meta_mcp`). Session fraîche à chaque déclenchement, même
  principe que l'Inspecteur : prompt court qui renvoie vers
  `docs/routine-pub-prompt.md` comme source de vérité. Premier passage
  prévu vendredi 14 août.

  **Reste à faire** : décider si `citation-13` (Einstein, retirée plus
  tôt le même jour) doit être vérifiée sérieusement puis réintégrée —
  rien d'autre ne bloque, la routine est live.
- **P2 — Heatmap "Le monde en ce moment" par domaine, idée du 10 août
  (brainstorm "out of the box"), méthode affinée en discussion le jour
  même.** Partie d'une simple agrégation de jauges, recentrée sur une
  question plus précise et plus utile : **ce domaine (géopolitique,
  économie, tech...) est-il en ce moment plutôt favorable ou
  défavorable pour la France ?** — un score par domaine, mis à jour
  **mensuellement** (pas besoin de fraîcheur quotidienne pour une vue
  d'ensemble).

  **Méthode de calcul retenue (espérance mathématique, pas un simple
  choix de case)** :
  1. Chaque carte de scénario (favorable/stable/dégradé) se termine
     déjà, en pratique, par une phrase fixe — vérifié sur l'édition du
     10 août, les 3 cartes finissent bien par exactement l'une de ces
     3 formes : *"→ Plutôt favorable pour la France."* / *"→ Neutre
     pour la France."* / *"→ Plutôt défavorable pour la France."* —
     une habitude de rédaction déjà là, **pas encore imposée
     formellement** dans `docs/routine-prompt.md` (à corriger : rendre
     cette formule de clôture obligatoire, toujours l'une des 3, plus
     un attribut machine-lisible `data-france-impact="favorable|
     neutre|defavorable"` sur le `.france-line` pour ne pas avoir à
     reparser du texte libre au moment du calcul mensuel).
  2. Valeur par scénario : Favorable = +1, Neutre = 0, Défavorable = −1.
  3. **Score du sujet = Σ (probabilité du scénario × valeur France de
     ce scénario)** — une vraie espérance, pas juste la valeur du
     scénario le plus probable. Exemple réel avec l'édition du 10 août
     (20 % favorable / 55 % stable-neutre / 25 % dégradé-défavorable) :
     `(0,20×+1) + (0,55×0) + (0,25×−1) = −0,05` — proche de zéro,
     légèrement négatif, cohérent avec "surtout stable, avec un risque
     de queue".
  4. **Score du domaine = moyenne des scores de tous les sujets actifs
     de ce domaine** (suivis actifs + éditions récentes sans suivi
     dédié) — la moyenne redevient pertinente maintenant que le score
     par sujet est un nombre continu entre −1 et +1, pas une catégorie
     (piste initiale "prendre le plus récent" abandonnée pour cette
     raison).
  5. Affichage : un score par domaine sur une échelle continue, coloré
     (rouge vers −1, gris vers 0, vert vers +1) — pas de matrice à deux
     axes (Monde vs France envisagé un temps, simplifié : uniquement
     l'angle France, plus lisible et plus utile).

  Recombine des données déjà publiées (probabilités déjà calculées,
  ligne France déjà écrite) — le seul vrai ajout est la formalisation
  de la formule de clôture + l'attribut machine-lisible, pas un nouveau
  pipeline de recherche. À trancher avant implémentation : génération
  par un job mensuel dédié (nouveau trigger Claude Code Remote,
  fréquence mensuelle) vs page 100% JS qui recalcule à la volée à
  partir des pages déjà publiées. **Toujours pas implémenté en tant que
  heatmap** (le job mensuel ci-dessus reste à trancher), mais la formule
  elle-même a été reprise et implémentée par article le 12 août — voir
  entrée « Δ France » juste en dessous, qui prépare le terrain pour ce
  chantier sans le construire.

- **[FAIT le 12 août] Δ France — indice de sens pondéré pour la France,
  ajouté dans « L'essentiel ».** Reprend telle quelle la formule
  ci-dessus (espérance mathématique : `score = Σ probabilité × valeur`,
  valeur = +1 favorable / 0 stable / −1 dégradé), appliquée par article
  plutôt que par domaine — demande explicite de l'utilisateur le 12 août
  ("je veux un truc super simple"), après plusieurs allers-retours sur
  le nom et l'échelle.

  **Nom retenu initialement : « Δ France »** (delta). "Boussole France"
  rejeté par l'utilisateur ("trop bateau"). Alternatives écartées : "Le
  Poids France" (plus parlant mais moins distinctif), "La Jauge France"
  (confusion possible avec les jauges déjà existantes par scénario).
  **Renommé « France Impact » le même jour**, après un brainstorm de
  l'utilisateur avec ChatGPT sur le visuel de la carte image (voir
  itération 6 plus bas) — repris partout pour rester cohérent entre la
  page, `feed.xml` et l'image (`index.html`, `feed.xml`,
  `docs/routine-prompt.md` mis à jour). Les identifiants internes
  (`delta-france`, `delta-gauge*`, `build_delta_badge()`...) gardent
  "delta" en interne, seul le texte visible par le lecteur change.

  **Échelle, décidée après calibrage sur les 5 éditions qui avaient déjà
  "L'essentiel" (8-12 août)** : un premier seuil à ±0,3 ne différenciait
  rien (les 5 scores réels tombaient tous entre +0,05 et −0,20, aucun ne
  dépassait ±0,3) —**seuil resserré à ±0,10**, et **retour utilisateur :
  pas de case "neutre"** (jugée non informative), remplacée par un sens
  toujours signé + une intensité : `|score| < 0,30` → léger,
  `0,30-0,50` → assez, `≥ 0,50` → très (ex. « léger négatif », « assez
  positif »). Le chiffre brut n'est jamais montré au lecteur, seuls le
  mot et la jauge le sont.

  **Limite méthodologique explicitement posée par l'utilisateur et
  actée avant l'implémentation** (échange du 12 août) : le score compare
  valablement le *sens et l'ampleur pondérés* entre sujets (deux scores
  proches = deux sujets qui penchent pareil), mais **ne mesure jamais
  l'enjeu réel** — un −0,15 sur un dossier économique n'est pas "aussi
  grave" qu'un −0,15 sur un conflit géopolitique. **Jamais de classement
  ou de "pire score du mois" construit à partir de ce seul chiffre.**
  Biais supplémentaires discutés et acceptés en connaissance de cause :
  la formule est symétrique (+1/−1) alors que gains et pertes réels ne
  le sont pas forcément (risque de queue) ; la classification
  favorable/stable/dégradé de chaque scénario reste un jugement
  éditorial, le chiffre lui donne une précision qu'elle n'a pas
  vraiment. Pas de garde-fou technique contre ces biais (au-delà de la
  règle écrite dans `docs/routine-prompt.md`) — **limite connue et
  assumée, pas résolue : de la documentation, pas du code, ne protège
  pas d'un oubli** (point soulevé par l'utilisateur).

  **Implémentation** :
  - `index.html` : CSS `.delta-france`/`.delta-gauge*` (jauge en arc
    continu, dégradé SVG rouge→or→vert, repère positionné par script
    via `data-score` sur `.delta-gauge-marker`, même géométrie que les
    jauges `.gauge` par scénario) ; `.essentiel-box` découpée en
    plusieurs `<p class="essentiel-text">` (un par item : problématique
    / contexte / conclusion / signal à surveiller) au lieu d'un seul
    bloc — demande utilisateur explicite ("il faut découper en
    paragraphe") ; `data-france-impact="favorable|stable|degrade"`
    ajouté sur chaque `.france-line` (calcul fiable, pas de parsing de
    texte libre — le texte des `.france-line` varie beaucoup d'une
    édition à l'autre, vérifié sur les 20 archives, 55 sur 105 ne
    suivaient pas une formule figée). Appliqué à l'édition du 12 août
    (score réel : 20/45/35 → −0,15 → « léger négatif »), pas de retrofit
    sur les archives déjà figées (8-11 août) — seule l'édition du jour,
    pas encore archivée au moment du calibrage, a servi de test réel.
  - `feed.xml` : même texte dans `<source>`, découpé en paragraphes
    séparés par de vrais doubles retours à la ligne (pas de `<br>`,
    aucune balise XML ajoutée — structure du flux inchangée comme
    demandé) + paragraphe Δ France ajouté à la fin. Corrige au passage
    l'illisibilité des légendes Instagram/LinkedIn/Facebook qui
    reprenaient `{{4.source.title}}` en un seul bloc de 700+ caractères.
  - `docs/routine-prompt.md` : étape 3 réécrite avec le gabarit HTML
    complet, la méthode de calcul, l'échelle, la portée (jamais de
    classement), et le format `<source>` en paragraphes.
  - **Badge sur l'image Instagram, demande utilisateur ("ça apporterait
    du sens et de l'accroche")** : `__DELTA_BADGE__` ajouté à
    `scripts/social/generate_instagram_image.py` (champ optionnel
    `data["delta"] = {"direction": "positif|negatif", "label": "..."}`,
    repli silencieux si absent, même logique que `--photo`). **Trois
    itérations visuelles le même jour, sur retours utilisateur
    successifs** :
    1. Pastille texte + bordure fine — jugée "pauvre".
    2. Disque tricolore avec flèche découpée dedans (masque SVG),
       positionné en bas à gauche — visuel jugé bon, mais retour
       utilisateur : mauvais emplacement, "pas moderne".
    3. Triangle tricolore en haut à droite (coin libre, le masthead
       occupe le haut à gauche) : `clip-path: polygon(100% 0, 100% 100%,
       0 0)` sur un dégradé diagonal bleu/blanc/rouge, grosse flèche ▲/▼
       à l'intérieur + petit texte "Δ France". **Retour utilisateur :
       trop "drapeau", évoque une esthétique identitaire ("France
       d'abord") non désirée — même en étant discret par la taille, le
       drapeau plein cadre reste trop connoté.**
    4. Marque discrète, sans imagerie nationale — abandon total du
       drapeau, petit anneau fin (~60px) avec flèche ▲/▼ pleine, couleur
       `--favorable`/`--degrade`, juste le texte "Δ France" en petit en
       dessous. **Retour utilisateur : trop petit, "pas très
       professionnel".**
    5. Carte, même recette que `.essentiel-box`/`.list-box` (fond
       surface semi-opaque, bordure fine, ombre légère) — reprend
       l'anneau + flèche de l'itération 4 (toujours aucune imagerie
       nationale, mêmes couleurs favorable/dégradé déjà utilisées
       ailleurs) mais dans un vrai conteneur avec le mot affiché en
       grand à côté (Fraunces, gras, couleur accent) plutôt que seul en
       petit texte flottant. **Retour utilisateur, positif sur la
       carte, mais ré-ouvert le jour même** après un brainstorm avec
       ChatGPT sur un système d'étoiles d'intensité + un petit drapeau.
    6. « France Impact » — drapeau en icône de label + 3 étoiles
       d'intensité pleines/vides (une seule couleur à la fois, côté
       favorable ou dégradé). **Retour utilisateur, le jour même :
       seules 3 étoiles ne montrent qu'un seul côté à la fois —
       "l'échelle doit toujours être la même quelle que soit la
       situation".**
    7. Échelle fixe à 6 étoiles avec une seule étoile visée + flèche qui
       pointe dessus (les 5 autres restent grises). **Retour
       utilisateur, le jour même : mauvaise lecture — "ici c'est très
       positif, tout doit être coché, tu dois avoir les six".**
       L'utilisateur voulait un remplissage **cumulatif**, pas une seule
       étoile isolée.
    8. Remplissage cumulatif de gauche à droite, sur une position 1-6
       unique — les étoiles `1..position` sont pleines, le reste gris,
       plus de flèche isolée. Mais couleur figée par index (0-2 rouge,
       3-5 vert) : un score "léger favorable" (position 4) affichait
       3 étoiles rouges + 1 verte. **Retour utilisateur, le jour même :
       pas de mélange — toutes rouges si négatif, toutes vertes si
       favorable.**
    9. **[FAIT, retenu] Couleur des étoiles pleines = sens du jour, pas
       la position.** Corrige l'itération 8 : la position 1-6 (calculée
       pareil : 1 = très défavorable ... 6 = très favorable) détermine
       toujours **combien** d'étoiles sont pleines, mais leur couleur est
       désormais uniforme — rouge (`_DEGRADE_HEX`) si `direction ==
       "negatif"`, vert (`_FAVORABLE_HEX`) si `"positif"`, jamais les
       deux mélangées sur un même score. `_delta_scale_positions()`
       calcule toujours les coordonnées x — écart d'abord un peu plus
       large entre l'étoile 3 et l'étoile 4, **retiré le jour même**
       (retour utilisateur : "pas besoin"), espacement régulier sur les
       6 depuis. Couleurs SVG toujours en hex fixe (`_FAVORABLE_HEX`/
       `_DEGRADE_HEX`), pas en `var(--x)` — un attribut `fill="var(--x)"`
       sur un `<path>` généré côté serveur ne se résout pas de façon
       fiable hors d'un attribut `style`, bug testé et évité. Contrat
       JSON inchangé depuis l'itération 6 : `data["delta"]` porte
       `direction`/`intensity` (1-3)/`label`.
    10. **[FAIT, retenu] Mécanisme confirmé (6 étoiles, 1-3 dégradé /
        4-6 favorable) + clarification du message : "notre évaluation",
        pas un fait.** Retour utilisateur, le jour même : ambiguïté sur
        ce que "France Impact : léger négatif" affirme — est-ce la
        question posée par le sujet qui est favorable/défavorable, ou
        l'appréciation de la rédaction ? Corrigé à 3 endroits en même
        temps, pour rester cohérent :
        - **Page + feed** : la phrase passe de "France Impact : {mot}."
          à **"Notre évaluation de l'impact pour la France : {mot}."**
          — jamais raccourci en retour, `docs/routine-prompt.md` mis à
          jour avec une règle explicite dessus.
        - **Image** : une légende **"Notre évaluation"** (petites
          capitales, discrète) ajoutée entre les étoiles et le mot en
          gros — le nom "France Impact" reste en haut (identifie l'axe
          mesuré), la légende clarifie que ce qui suit est une
          appréciation, pas une mesure.
        Le mécanisme des étoiles lui-même (échelle 1-6, 1-3 dégradé/4-6
        favorable, couleur uniforme par sens) n'a pas changé — confirmé
        par l'utilisateur comme correct, seule la clarté du message
        autour était à retravailler.
    11. **[FAIT, retenu] Bugs d'affichage repérés sur la page réelle
        (capture d'écran fournie par l'utilisateur) + petit drapeau
        ajouté sur la page.** Trois corrections successives sur
        `.delta-france`/`.delta-gauge*` dans `index.html` :
        - **Mot du repère ("LÉGER NÉGATIF") débordant de la jauge** —
          il vivait en légende sous l'arc dans le flux normal, ce qui le
          faisait déborder de la boîte de 108px. Repositionné en
          `position: absolute` **dans le creux de l'arc lui-même**
          (même principe que `.gauge-num` des cartes de scénario) —
          d'abord élargi avec un offset négatif (aggravait le
          débordement, corrigé), puis réduit en taille de police pour
          tenir sur une seule ligne sans déborder.
        - **Colonne de texte trop étroite à certaines largeurs d'écran**
          (capture utilisateur avec police système agrandie — le seuil
          fixe `@media (max-width: 480px)` ne se déclenchait pas dans ce
          cas précis, le texte se retrouvait compressé mot par mot à
          côté de la jauge). Remplacé par `.delta-france{ flex-wrap:
          wrap }` + `.delta-text{ flex: 1 1 220px; min-width: 220px }` —
          le texte repasse sous la jauge dès qu'il manque de place,
          quelle que soit la cause (largeur d'écran, zoom, taille de
          police système), plus robuste qu'un seuil fixe. Testé à
          390/500/600/900px.
        - **Petit drapeau ajouté devant "Notre évaluation..."** dans le
          paragraphe (suggestion utilisateur, même drapeau 3 bandes que
          sur l'image) — cohérence visuelle page/image.
        **Répercuté sur `archives/2026-08-12.html`** (pas seulement
        `index.html`) suite à une question directe de l'utilisateur
        ("tu le mets sur index et archive du jour ?") : l'archive du
        jour datait de ce matin, avant l'ajout de France Impact **et**
        de `.list-box` (chantier des sorties cinéma, même journée) —
        les deux CSS étaient absentes, ainsi que la mise à jour de la
        grille des registres (dimanche/lundi/samedi). Resynchronisé
        chirurgicalement (CSS, attributs `data-france-impact`, bloc
        essentiel, JS, objet `registres`) plutôt que de réécrire le
        fichier depuis `index.html`, pour ne pas casser les chemins
        relatifs `../` propres à `archives/` — diff final vérifié : ne
        restent que les différences légitimes (canonical/OG, nav
        `aria-current`, lien `.dek` sans préfixe `archives/`).
    12. Mot du sens retiré de la jauge, coloré directement dans la
        phrase. Retour utilisateur : "léger négatif" apparaissait deux
        fois (légende sous la jauge + dans la phrase), redondant.
        `.delta-gauge-word` supprimé, mot déplacé en `<span
        class="delta-word">` coloré via `data-kind` sur `.delta-france`.
        **Retour utilisateur, le jour même : reconsidéré — "tu peux pas
        mettre léger négatif à l'intérieur de la jauge sur 2 lignes ?"**
    13. **[FAIT, retenu] Le mot revient dans la jauge, en plus du mot
        coloré dans la phrase — les deux, pas l'un ou l'autre.**
        `.delta-gauge-word` réintroduit, mais cette fois **en flux
        normal sous l'arc** (plus en `position: absolute`) avec
        `.delta-gauge` élargi à 78px de hauteur (64px pour l'arc + place
        réservée pour le mot) — wrap naturel sur autant de lignes que
        nécessaire dans les 108px de large, jamais de `nowrap` ni
        d'offset négatif (les deux avaient causé les débordements des
        itérations précédentes). Le `<span class="delta-word">` coloré
        dans la phrase reste inchangé. Répercuté sur
        `archives/2026-08-12.html` et `docs/routine-prompt.md` en même
        temps qu'`index.html`, comme pour l'itération 11.
    **Implémenté uniquement sur `instagram-photo-template.html`, pas sur
    le gabarit par défaut** (`instagram-template.html`, celui de la
    routine automatique) : testé, le budget vertical/horizontal du
    gabarit par défaut est déjà tendu par le titre (1-3 lignes selon le
    jour), risque de chevauchement non vérifié pour ce gabarit-là.
    Cohérent avec le statut déjà manuel/optionnel de `--photo` — la
    routine quotidienne automatique n'est pas affectée.
- **P3 — Carte de pari partageable, sans backend, idée du 10 août
  (même brainstorm).** Une URL du type
  `parier.html?edition=2026-08-10&choix=stable` générant une carte
  "j'ai parié sur Stable, reviens le {date de clôture} pour voir si
  j'avais raison" — état encodé entièrement dans l'URL (query string),
  aucune base de données, compatible avec le principe zéro-backend du
  site. Transforme un lecteur passif en participant avec une raison
  concrète de revenir, et un objet naturellement partageable. Joue sur
  la même mécanique "deviner avant de savoir" déjà au cœur du site
  (vote Telegram). Pas chiffré : design de la carte (probablement même
  moteur HTML/CSS→capture que les cartes Instagram), calcul de la date
  de clôture (pas toujours définie pour un sujet suivi).
- **P3 — Confronter à un vrai marché de prédiction (Polymarket,
  Metaculus, Kalshi...), idée du 10 août (même brainstorm).** Quand un
  marché liquide existe sur le sujet du jour, ajouter une ligne du type
  "Le marché de prédiction {nom} donne {X}% — nous {Y}%." Validation
  externe, différenciant. **Explicitement opportuniste, jamais
  systématique** : ne marche que pour certains sujets (géopolitique,
  financier surtout), pas de recherche supplémentaire imposée à la
  routine du matin si rien de pertinent n'existe — même logique de
  repli silencieux que pour la photo Pexels du sujet (voir plus haut).
- **P3 — Page de calibration ("avions-nous raison, au global"), idée du
  10 août (même brainstorm).** Différent d'une simple statistique
  "X% de bons scénarios" (déjà écartée comme trop simpliste dans la
  revue du 10 août, voir plus haut section UX) : une vraie **courbe de
  calibration** façon prévisionnistes sérieux — parmi tous les
  scénarios résolus (pages `suivi/` clôturées), regrouper par tranche
  de probabilité annoncée (ex. "70-80%") et montrer le taux de
  réalisation réel observé dans cette tranche. Transparence que
  quasiment aucun média ne pratique, cohérent avec l'identité
  méthodologique du site. **Bloqué par le volume** : pas encore assez
  de clôtures pour que la statistique ait un sens — à revisiter dans
  plusieurs mois, une fois `suivi/` accumulé assez de cas résolus.

**À surveiller (pas une tâche, un dossier ouvert)**
- **Arabie saoudite / sport** — candidat à une première page de suivi
  (retrait du financement LIV Golf par le PIF, tension avec l'investissement
  massif dans le football), mis en attente volontairement le 3 août pour
  accumuler plus de développements avant de lancer une première page. La
  routine hebdo de veille (« Détection sujets à suivre ») le re-signalera
  si ça bouge.

**À vérifier**
- *(vide au 8 août — le dernier point ouvert ici, le filtrage Buttondown
  quotidien/hebdo, est résolu depuis le passage aux metadata
  `quotidien`/`hebdo` séparées le 7 août, confirmé par l'utilisateur ;
  voir plus bas, section Newsletter.)*

**Idées explicitement écartées** (pour mémoire, ne pas reproposer sans
nouvel élément) : fil d'actualité scrollable façon LinkedIn/Instagram
(pas assez de densité avec 1 édition/jour, sans réel gain vs
`archives.html`) ; comptes utilisateurs, likes, commentaires sur site
(coût backend/modération/RGPD trop élevé vs bénéfice, l'interaction
sociale reste sur Telegram) ; WhatsApp Channels (pas d'API officielle
gratuite) ; dépôt GitHub privé ou dossier privé séparé pour les docs
internes (coût opérationnel — routine à synchroniser sur deux dépôts —
jugé disproportionné vu qu'aucun contenu n'est réellement sensible) ;
remplacer la question posée (`.day-context`) par le texte "L'essentiel"
dans le récap hebdomadaire (`hebdo/*.html`) — proposé et écarté le
9 août, la conclusion de "L'essentiel" ferait doublon avec la liste des
3 scénarios juste en dessous (gagnant déjà en gras via `.is-winner`) ;
question gardée, elle sépare proprement la mise en tension (question
ouverte) de la résolution (scénarios). Piste alternative notée si le
besoin revient : reprendre seulement la dernière phrase de "L'essentiel"
(l'issue probable + le signal à surveiller), pas le bloc complet.

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
    Buttondown standard) + lien « Newsletter » dans le menu de toutes les
    pages vivantes ; compte Buttondown créé et passé en payant ; design
    (couleurs/polices) aligné à la charte du site sur les pages web et email
    Buttondown ; connexion RSS-to-email configurée (« Send an email »,
    déclenchement à chaque nouvel item, template « Rich ») ; mise à jour
    quotidienne de `feed.xml` ajoutée au prompt de la routine (étape
    technique 7).
  - ✅ **[FAIT le 11 août] Pages de redirection dédiées, au lieu des pages
    génériques utilisées jusque-là.** Réglages Buttondown → Subscribing →
    Redirects : « After subscribing » (avant confirmation) pointait vers
    `newsletter.html`, « After confirming » (inscription validée) vers la
    page d'accueil. Remplacés par deux pages dédiées, même gabarit visuel
    que le reste du site, `noindex` (pages transactionnelles) :
    `confirmez-votre-email.html` (invite à vérifier la boîte mail/les
    spams, bonus Telegram en attendant) et `bienvenue.html` (confirme
    l'inscription active, ce qui va être reçu, CTA vers l'édition du jour).
    Déploiement d'abord bloqué par le bug Jekyll (voir backlog
    « Technique ») — vérifié en ligne par l'utilisateur une fois `.nojekyll`
    poussé. Champs Buttondown mis à jour par l'utilisateur avec les deux
    nouvelles URLs.
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
  **Précision du 11 août sur la marche à suivre pour ce copier-coller
  manuel** : dans `docs/routine-prompt.md`, seul le texte **après** la
  ligne `---` est le prompt réellement envoyé à la routine live — tout ce
  qui précède (titre, explication du fichier, mentions "version allégée
  depuis le 9 août", lien vers le fichier de rollback) est de la
  documentation à l'usage d'un humain qui lit le fichier, jamais collé
  dans le trigger. **Convention adoptée le 11 août** (demande explicite
  de l'utilisateur, par souci d'économie) : la session met à jour
  `docs/routine-prompt.md` directement sur GitHub (`main`) et signale
  juste que c'est fait — c'est à l'utilisateur d'aller chercher le
  fichier lui-même sur GitHub et de faire le copier-coller. Ne plus
  envoyer de fichier texte séparé pour ça (ancienne pratique de ce
  8 août : plusieurs fichiers `routine-quotidienne-allegee*.txt` envoyés
  un par un à chaque correction, source de confusion sur la version
  réellement à jour).

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

  **Tag `<comments>` ajouté le 6 août** (retour utilisateur), pour la
  même raison que sur `feed.xml` : séparer un texte court réutilisable
  (aperçu, réseau social) du HTML complet de `<description>`, sans avoir
  à le parser. Porte la phrase d'ouverture/conclusion de semaine rédigée
  à l'étape 3, en texte brut — identique au premier paragraphe de la
  `<description>` mais sans les balises `<br>`. Appliqué rétroactivement
  à l'item déjà publié (2 août).

  **Prompt de cette routine documenté dans un fichier dédié depuis le
  9 août** : `docs/routine-hebdo-prompt.md`, même principe que
  `docs/routine-prompt.md`/`docs/routine-detection-prompt.md` — trigger
  `trig_01SE6daCsV38jPUXf82DC7TF` (créé via `meta_mcp`, directement
  éditable via `update_trigger`, pas besoin du cycle copier-coller
  manuel de la routine éditoriale quotidienne). Ce fichier miroir
  n'existait pas encore alors que la routine tournait déjà depuis
  plusieurs semaines — trou comblé après un retour utilisateur qui
  redonnait ce correctif du 6 août pour vérification, l'occasion de
  s'apercevoir qu'aucune copie de référence n'existait.

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

  **La routine quotidienne (7h00) n'a besoin d'aucune adaptation** : elle
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
  `metadata.hebdo == "oui"` — confirmé par l'utilisateur. **[FAIT le
  7 août]** la migration des abonnés existants (ancien
  `metadata.subscription_type`) vers les nouvelles clés est également
  confirmée (voir note complète plus haut dans le backlog) — plus rien
  en attente côté Buttondown sur ce point.
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

  **[AJOUTÉ le 12 août] Image d'illustration, à la création de la page
  uniquement.** Retour utilisateur : même process que l'image Pexels des
  éditions quotidiennes (voir « Générer et attacher l'image Instagram » /
  « Image dans le corps de l'article » dans `docs/routine-prompt.md`), mais
  appliqué **une seule fois, à la création de la page** (V0) — jamais
  régénérée aux mises à jour suivantes (V1, V2...), pour éviter qu'un sujet
  suivi sur plusieurs mois accumule une galerie de photos disparates. Étapes,
  seulement quand une page `suivi/{sujet}.html` **n'existe pas encore** :
  1. Construire 1 à 3 mots-clés thématiques génériques (même règle que pour
     l'édition quotidienne — jamais le titre recopié tel quel, jamais un nom
     propre isolé).
  2. `python3 scripts/social/fetch_topic_image.py "{mots-clés}" --count 5 --out /tmp/topic-image-candidates`
     puis choisir le meilleur candidat à l'œil (mêmes garde-fous : écarter
     tout visage reconnaissable, tout candidat hors-sujet).
  3. `python3 scripts/social/use_topic_image.py {candidat choisi} --date suivi-{sujet} --credits /tmp/topic-image-candidates/credits.json`
     — utiliser `suivi-{sujet}` (pas une date) comme identifiant, pour que les
     fichiers atterrissent sous `assets/social/topic-images/suivi-{sujet}.jpg`
     / `-wide.jpg` / `.json`, jamais en collision avec les images datées des
     éditions quotidiennes.
  4. Insérer le bloc `<figure class="article-image">` déjà présent dans
     `suivi/_gabarit.html` (CSS et HTML identiques à `index.html`, chemins
     relatifs adaptés avec `../`), remplir `alt`/`{photographe}`/`{pexels_url}`
     à partir de la fiche de provenance JSON.
  5. **Si aucun candidat ne convient (ou si le script échoue), retirer le bloc
     `<figure class="article-image">` entièrement** — jamais bloquant pour la
     création de la page, exactement comme pour l'édition quotidienne.

  Sur une page qui existe déjà (ajout d'une V1, V2...), ne jamais retoucher
  l'image en place — elle reste celle choisie à la création, même si le sujet
  a beaucoup évolué depuis.

  **Marche à suivre pour une mise à jour** (processus manuel, hors
  routine) : l'utilisateur donne le sujet à mettre à jour dans une
  session ; retrouver l'édition d'origine dans `archives/` ; si aucune
  page `suivi/{sujet}.html` n'existe encore, la créer à partir de
  `suivi/_gabarit.html` avec V0 (rappel de l'édition d'origine) + V1
  (première mise à jour) — **et l'image d'illustration si applicable, voir
  ci-dessus** ; si elle existe déjà, ajouter uniquement une
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

  **Jamais l'étiquette de catégorie brute (favorable/stable/dégradé)
  seule en tête de phrase, sans dire ce qu'elle recouvre concrètement**
  (ajouté le 14 août après retour utilisateur — cas réel :
  "⏳ Stable en forte hausse, +20 points (45%)" jugé incompréhensible,
  "stable *quoi* ?"). "Favorable"/"dégradé" passent presque toujours
  (le sens général — bonne/mauvaise nouvelle — se devine), mais
  "stable" ne dit jamais de quoi il s'agit : toujours remplacer
  l'étiquette par le titre concret du scénario (celui déjà écrit dans
  sa carte `.mini-scenario-title`, ex. "Le procès traîne, le deal
  reste gelé"), pas le nom de la catégorie interne. Corrigé rétro-
  activement sur `suivi/warner-paramount.html` et l'item correspondant
  de `feed-suivi.xml` le jour même. Vaut pour la conclusion sur la page
  ET pour `<comments>`/`<description>` de `feed-suivi.xml` (et donc
  pour l'image générée par `generate_suivi_image.py`, qui réutilise ce
  même texte tel quel) — dans les deux cas, un lecteur qui n'a jamais
  ouvert la page doit comprendre en une seule phrase *pourquoi* il y a
  une mise à jour, sans avoir à deviner ce que "stable" signifie pour
  ce sujet précis.

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

  **P1 — Piste à approfondir plus tard (notée le 8 août, passée en P1
  le 8 août, discussion à reprendre) : préciser le déclencheur idéal de
  clôture.** L'utilisateur
  propose que la clôture soit idéalement déclenchée quand **un événement
  concret déjà nommé dans la définition d'un des 3 scénarios se
  réalise** (ex. une démission, une motion de défiance effectivement
  déposée...) — un événement qui, de fait, ferait techniquement passer
  ce scénario à ~100%. Cohérent avec la règle déjà posée ci-dessus (fait
  réel requis, jamais un seuil de probabilité interne) : ça ne la
  change pas, ça précise ce qui compte comme "fait réel" — pas
  n'importe quel développement notable, mais spécifiquement un des
  événements-jalons déjà écrits dans les scénarios eux-mêmes. Pas encore
  intégré au prompt de la routine de détection ; à retravailler ensemble
  avant de l'ajouter.

  **Deuxième cas réel construit le 8 août** : `suivi/fifa-infantino.html`,
  suite de l'édition du 6 août ("FIFA : la présidence d'Infantino
  vacille"), déclenché par un sujet remonté par la routine de détection
  du soir (voir plus bas) plutôt que par une demande spontanée. V0 reprend
  les 3 scénarios d'origine (favorable 20%, stable 45% jugé le plus
  probable, dégradé 35%). V1 (8 août) intègre les développements réels
  des 7-8 août — UEFA confirmant avoir « perdu confiance », FIFPRO
  dénonçant un « abus de pouvoir présidentiel », le scandale du paiement
  UEFA à une ex-employée, et surtout l'appui public de la CAF (unanime),
  de l'Argentine et du Mexique à Infantino — avec une conclusion qui
  nomme le scénario le plus volatil (favorable, -10 points) tout en
  distinguant ce qui relève de la rhétorique (durcissement du ton UEFA,
  dégradé +5) de ce qui relève d'un fait structurant pour le vote
  (bloc de 111 voix désormais confirmé publiquement, stable +5). Badge +
  tri par fraîcheur branchés sur `archives.html`, entrée « Suivis actifs »
  ajoutée dans `docs/sujets-a-suivre.md`, item ajouté dans
  `feed-suivi.xml`, tout vérifié visuellement (desktop + mobile).

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
    <comments>{verdict court de la conclusion, la phrase déjà écrite dans la page}</comments>
    <enclosure url="https://lesscenarios.fr/assets/social/suivi/{sujet}-v{N}.png" length="{taille réelle en octets}" type="image/png"/>
    <description><![CDATA[{même phrase}<br><br>{1-2 phrases : ce qui explique le mouvement}<br><br>Voir la mise à jour complète, scénario par scénario 👉 <a href="{lien vers la version}">lesscenarios.fr/suivi/{sujet}.html</a>]]></description>
  </item>
  ```
  **`<enclosure>` ajoutée le 12 août** — voir l'entrée backlog dédiée
  (« Image sur les posts LinkedIn "sujet suivi" ») pour le détail complet
  et la partie Make.com restant à faire côté utilisateur.

  **[MIS À JOUR le 14 août] L'image n'est plus la photo brute.** Retour
  utilisateur : une simple photo Pexels sans rien dessus n'était "pas
  clean". Désormais, à chaque nouvelle version publiée (V1, V2...),
  générer une image composée avec `scripts/social/generate_suivi_image.py`
  + `scripts/social/suivi-template.html` (logo — même taille que le
  daily — + pastille "🔄 Suivi mis à jour" + titre du sujet + la
  conclusion, sur la photo `suivi-{sujet}.jpg` déjà en place, jamais
  retouchée elle-même) :
  ```
  python3 scripts/social/generate_suivi_image.py \
    --data {json temporaire avec "topic" et "conclusion"} \
    --output assets/social/suivi/{sujet}-v{N}.png \
    --template scripts/social/suivi-template.html \
    --photo assets/social/topic-images/suivi-{sujet}.jpg
  ```
  `"conclusion"` = reprendre **tel quel** le texte déjà mis dans
  `<comments>` (voir règle juste en dessous — jamais mener avec la seule
  étiquette de catégorie). Un fichier PNG par version (`-v{N}.png`,
  jamais écrasé) plutôt qu'un seul fichier réutilisé, pour garder
  l'historique des visuels alignés sur l'historique des versions.
  `{taille réelle en octets}` = taille de ce PNG généré (`stat -c%s`),
  jamais une valeur inventée. Si la photo source
  (`suivi-{sujet}.jpg`) n'existe pas pour ce sujet, omettre `<enclosure>`
  entièrement — jamais bloquant pour publier l'item, exactement comme
  avant.

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
  scénario, `assets/make/scenario-daily.blueprint.json` (dernier export
  à jour au 8 août — à ré-exporter et remplacer si le scénario est
  modifié par la suite, pas de synchronisation automatique).

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
  après le passage quotidien du scénario (~7h00), n'aurait alors jamais
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
  - **[FAIT le 8 août]** `assets/make/scenario-daily.blueprint.json`
    réexporté par l'utilisateur et mis à jour dans le dépôt — reflète ce
    fix ainsi que l'ajout de l'image sur les posts X/Facebook (voir
    backlog en tête de ce document).
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
  (`trig_01BYYviSQge2CDcYkzBbYcjT`, **lundi/jeudi/vendredi/samedi, 0h UTC
  ~2h Paris (la nuit — déplacée du soir le 14 août, voir plus bas)**,
  distincte de la routine éditoriale) relit
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

  **Ne créait et ne modifiait jamais automatiquement une page
  `suivi/*.html`, ni `sujets-a-suivre.md`, jusqu'au 8 août** : c'était
  jusque-là toujours un rapport de veille, jamais une publication — le
  "go" restait une décision manuelle de l'utilisateur, donnée ensuite
  dans la session principale du site. Ce point n'avait pas changé le
  7 août malgré une première demande d'auto-publication au-delà du
  seuil : refusé côté conception à ce moment-là, parce que réévaluer un
  seuil chiffré à chaque passage ne garantit pas d'écarter le bruit (une
  estimation peut varier un peu sans vrai fait nouveau), et parce que le
  rôle éditorial du site suppose un passage humain avant publication.

  **Revenu sur cette décision le 8 août, à la lumière d'un cas réel.**
  Le jour même, la page de suivi FIFA/Infantino avait été créée
  manuellement (voir plus haut) alors que l'écart réel (-10 points sur
  le scénario favorable) restait sous le seuil de 20 points et que
  l'édition d'origine datait de seulement 2 jours — un exemple concret
  du bruit que le seuil chiffré seul ne suffit pas à écarter, exactement
  l'objection soulevée le 7 août. Plutôt qu'abandonner l'idée
  d'auto-publication, l'utilisateur a proposé un garde-fou supplémentaire
  qui répond directement à cette objection : **auto-publier au plus un
  seul sujet par passage** (le plus crédible, jamais tous les sujets
  éligibles), **jamais un sujet dont le point de référence (dernière
  version publiée, ou édition d'origine si pas encore de page de suivi)
  a moins de 10 jours** — pour laisser un développement se confirmer
  avant d'y réagir, plutôt que de publier sur un pic de bruit médiatique
  du jour même. Avec cette règle, le cas FIFA du 8 août n'aurait de
  toute façon pas été auto-publié (double filtre : écart sous 20 points
  ET référence à 2 jours). Deuxième objection du 7 août (le rôle
  éditorial suppose un passage humain avant publication) : reste vraie
  en soi, mais l'utilisateur accepte explicitement le compromis —
  vérification a posteriori plutôt qu'a priori, avec rollback git en
  filet de sécurité si une auto-publication s'avère fausse.

  **La clôture (🏁, voir point 2bis du prompt) reste dans tous les cas
  une décision manuelle**, même pour le sujet retenu pour
  l'auto-publication — seule la mise à jour normale (nouvelle version
  ou nouvelle page) est concernée par l'automatisation, jamais le
  passage d'un sujet en "VF — Résolu". Cohérent avec la règle posée le
  8 août sur la clôture elle-même (fait vérifié requis, jamais un
  franchissement de seuil interne, pour éviter l'auto-évaluation).

  **Prompt de cette routine documenté dans un fichier dédié depuis le
  8 août** : `docs/routine-detection-prompt.md`, sur le même principe
  que `docs/routine-prompt.md` pour la routine éditoriale quotidienne —
  sauf que ce trigger (`created_via: meta_mcp`) est directement éditable
  via `update_trigger`, pas besoin du cycle copier-coller manuel requis
  pour la routine quotidienne (`created_via: http_api`).

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
