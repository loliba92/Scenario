# Rapport Search Console

Site `sc-domain:lesscenarios.fr` · données Google du 2026-09-19 au 2026-10-16 · synchronisé le 2026-10-19 (les chiffres de Google ont ~3 jours de retard).

**Verdict : CRITIQUE** — 7 éditions de plus de 7 jours sont inconnues de Google (sur 33 pages inspectées). Demander l'indexation dans Search Console, vérifier un lien interne depuis une page déjà indexée, patienter si la page a moins de 7 jours.

## Chiffres (28 jours)

- 2 clics, 294 impressions, taux de clic 0,7 %, position moyenne 8,7.
- Pages indexées : 21 sur 33 inspectées ; éditions inconnues de Google : 9 (dont 7 de plus de 7 jours).
- Requêtes : 4 (dont 2 avec le nom du site).
- Tendance (14 jours, jusqu'au 2026-10-16) : impressions 139 contre 155, clics 0 contre 2.

## À résoudre — critique

- 7 éditions de plus de 7 jours sont inconnues de Google (sur 33 pages inspectées). **Action** : Demander l'indexation dans Search Console, vérifier un lien interne depuis une page déjà indexée, patienter si la page a moins de 7 jours. **Agent à envoyer** : seo-technical + seo-sitemap. **Mission** : Diagnostiquer pourquoi ces éditions restent inconnues de Google : profondeur de clics depuis l'accueil, liens internes vers les éditions récentes, structure et dates du plan du site, robots.txt, vitesse. Rendre un plan correctif chiffré, classé par impact.

## À résoudre — important

- Le site apparaît (position moyenne 8,7) mais est très peu cliqué (0,7 %). **Action** : Retravailler les titres et descriptions des pages les plus vues. **Agent à envoyer** : seo-content. **Mission** : Proposer de nouveaux titres (≤ 59 caractères) et descriptions (100–160) plus incitatifs pour les pages les plus vues, dans le ton sobre de Scénario ; ne rien promettre.
- Éditions en français : 1 titres coupés. **Action** : Corriger via les générateurs (voir .claude/seo-routage.md). **Mission** : Correction directe dans les générateurs (generate_seo_head.py, translate_daily.py), puis régénération et tests.
- Éditions en anglais : 1 titres coupés. **Action** : Corriger via les générateurs (voir .claude/seo-routage.md). **Mission** : Correction directe dans les générateurs (generate_seo_head.py, translate_daily.py), puis régénération et tests.

## À surveiller

- Seulement 4 requêtes enregistrées. **Action** : Trop peu pour piloter par mots-clés : viser d'abord l'indexation des éditions. **Agent à envoyer** : seo-cluster. **Mission** : Proposer des axes thématiques (matières, sujets récurrents) et un maillage interne pour élargir les requêtes, sans produire de pages en série.
- Pages en première page de Google sans aucun clic : `/`, `/en/archives/2026-08-08.html`, `/en/archives/2026-09-11.html`, `/en/archives/2026-09-13.html`, `/en/archives/2026-09-15.html`. **Action** : Titre ou description à rendre plus incitatif. **Agent à envoyer** : seo-content. **Mission** : Réécrire titre et description de ces pages (liste dans le rapport), puis vérifier la cohérence avec le contenu.
- L'adresse `/index.html` apparaît dans Google en plus de `/`. **Action** : Vérifier la balise canonique de l'accueil. **Agent à envoyer** : seo-technical. **Mission** : Vérifier la canonique de l'accueil, les redirections et les liens internes qui pointent vers /index.html.
- 1 page : Google connaît l'adresse mais ne l'a pas encore explorée ou retenue (`/en/archives/2026-10-18.html`). **Action** : Renforcer les liens internes vers la page, enrichir son contenu, demander l'indexation. **Agent à envoyer** : seo-content. **Mission** : Comprendre pourquoi Google retient ou écarte ces pages (profondeur, unicité, qualité perçue) et proposer des améliorations de contenu et de liens internes.
- 2 pages : Google a lu la page et a décidé de ne pas l'indexer (qualité ou doublon perçu) (`/archives/2026-10-10.html`, `/en/archives/2026-10-13.html`). **Action** : Apporter de la valeur propre (analyse, chiffres, sources) et vérifier les doublons. **Agent à envoyer** : seo-content. **Mission** : Comprendre pourquoi Google retient ou écarte ces pages (profondeur, unicité, qualité perçue) et proposer des améliorations de contenu et de liens internes.

## Ce qui fonctionne

- Google affiche le site en position moyenne 8,7 (première page) sur 294 impressions.
- 6 pages principales indexées : `/`, `/archives.html`, `/le-projet.html`, `/sources.html`, `/glossaire.html`, `/en/`.
- 15 éditions indexées par Google.
- Plan du site `/sitemap.xml` lu par Google sans erreur (181 adresses envoyées).
- Plan du site `/sitemap-news.xml` lu par Google sans erreur (4 adresses envoyées).

## Ce qui ne fonctionne pas

- Presque aucune visite venue de Google : 2 clics en 28 jours.
- Découverte trop lente : 7 éditions publiées depuis plus d’une semaine ne sont pas connues de Google.

## Ce que seul le propriétaire peut faire

- Dans Search Console, collez l'adresse de l'édition du jour dans la barre du haut, puis « Demander une indexation » (quota limité par jour) ; répétez pour les éditions inconnues les plus récentes.
- Relisez les recommandations des agents avant de valider tout changement de titres ou de contenu.

## Conclusions des agents — 16 octobre 2026 : titres coupés sur les éditions du 13 au 16 octobre

**Verdict** : Le problème « éditions inconnues de Google » est le même que celui conclu le 11 octobre : aucun blocage technique, Google explore rarement ce jeune site, et les correctifs de maillage sont déjà en place. Aucun nouvel audit n'a été lancé, les données n'ayant pas changé de nature ; il faut attendre le contrôle du 25 octobre. En revanche, une vraie cause nouvelle a été trouvée et corrigée : le générateur coupait les titres des éditions récentes en plein milieu d'une phrase.
**Agents** : gsc-expert (lecture des conclusions et du rapport, sans nouvel appel).

- [Corrigé] **Titres coupés par « … » sur 6 pages (éditions du 13 au 16 octobre, 4 en français, 2 en anglais)** (certain (code lu, pages relues)) — generate_seo_head.py coupait le titre proposé (presque toujours plus long que 59 caractères) alors que le h1 de l'édition est déjà un titre court et complet. Résultat : « …ou cette peur… », « …peut-il tenir sans… ». **Action** : Fait : le générateur prend désormais le h1 entier quand le titre proposé est trop long (avec la marque jusqu'à 59 caractères, sans la marque jusqu'à 70), et ne coupe qu'en dernier recours. 2 tests ajoutés. Titres, og:title et twitter:title corrigés sur les 6 pages (seules ces balises ont changé, vérifié ligne à ligne). Les titres anglais viennent de la traduction du titre français, donc les prochains seront corrects.
- [Corrigé] **Description anglaise trop courte (édition du 12 octobre, 84 caractères)** (certain) — La description était la question traduite, sans le complément habituel. **Action** : Fait : complément ajouté (146 caractères) dans description, og et twitter uniquement. Toutes les éditions en français et en anglais sont maintenant dans la norme (titre sans coupure, description de 100 à 160 caractères).
- [Corrigé] **Pages anglaises déclarées en français** (certain) — La balise « language » restait à fr-FR sur les pages anglaises (la langue du document et le JSON-LD étaient déjà en anglais). **Action** : Fait : translate_daily.py la passe à en-US pour les prochaines éditions, et l'édition anglaise du jour est corrigée. Les anciennes éditions anglaises, figées, ne sont pas touchées (impact faible).
- [Vous] **10 éditions de plus de 7 jours inconnues de Google** (mesuré, cause déjà établie le 11 octobre) — Exploration rare d'un site jeune et peu cité ; correctifs de maillage déjà faits (bloc « Les éditions du mois », liens précédente/suivante). Aucun nouvel élément depuis le 11 octobre. **Action** : Rien de nouveau à corriger dans le site. Les demandes d'indexation dans Search Console restent à faire par vous (voir ci-dessous).

À faire par le propriétaire :
- Dans Search Console, demander l'indexation de /archives.html en priorité, puis de l'édition du jour et d'une dizaine d'éditions récentes par jour.
- Demander aussi l'indexation de /guide-pedagogique.html, seule page principale encore « détectée, non indexée ».

Ce que l'on ne sait pas encore :
- Si les titres complets font monter le taux de clic : trop peu de données (299 impressions sur 28 jours) pour conclure avant plusieurs semaines.
- Les liens « édition précédente » des pages déjà publiées affichent encore l'ancien titre coupé (pages figées, non modifiées).

Prochain contrôle : 2026-10-25.

## Conclusions des agents — 12 octobre 2026 : peu de clics malgré une première page

**Verdict** : Le site apparaît en position moyenne 9,1 mais n'obtient que 4 clics sur 291 impressions. Le classement n'est pas en cause : c'est l'aperçu dans Google qui n'incitait pas à cliquer. Les balises des trois pages vivantes et des 10 éditions les plus vues sont réécrites ; reste à mesurer l'effet.
**Agents** : seo-content.

- [Corrigé] **Les pages les plus vues sont des éditions anglaises passées** (certain (mesuré)) — Sur les 13 pages les plus vues, 9 sont des éditions anglaises et 1 une édition française, toutes passées et figées. Elles sont en position 5 à 7,5 avec 0 clic ; la page cinéma du 8 août a 82 impressions sans aucun clic. **Action** : Fait le 12 octobre, sur accord du propriétaire : titres, descriptions, og et twitter de ces 10 éditions réécrits (9 anglaises, 1 française), sans toucher à rien d'autre (vérifié ligne à ligne). Dates du plan du site inchangées.
- [À faire] **Les descriptions reprennent la question du titre** (certain (code lu)) — generate_seo_head.py renvoie la question posée telle quelle si elle tient en 160 caractères : la description répète le titre, sans chiffre clé ni mention des trois scénarios. Le titre est un simple extrait du sujet. **Action** : Pour les prochaines éditions : description = un fait ou un chiffre, puis « trois scénarios » et la fourchette des issues, avec des fins variées pour éviter des métadonnées en série ; contrôler titre et description après traduction dans translate_daily.py.
- [Corrigé] **Accueil, Le projet et Newsletter : balises peu parlantes** (certain) — « Le projet » et « Newsletter » ne disaient pas ce que la page apporte ; la page Newsletter est en position 52 et son titre ne contenait aucun mot de la requête « scénarios email ». **Action** : Fait : nouveaux titres et descriptions (titre ≤ 61 caractères avec la marque, description 133 à 138), repris dans le générateur de l'accueil.

À faire par le propriétaire :
- Vérifier dans Search Console, à partir du 26 octobre, si le taux de clic de l'accueil, du projet et de la newsletter évolue.

Ce que l'on ne sait pas encore :
- Quel effet auront ces nouveaux titres sur le taux de clic : aucune garantie, et 291 impressions sur 28 jours sont un échantillon très faible.
- Si la page Newsletter peut monter au-dessus de la position 52 : elle vise une requête rare.

Prochain contrôle : 2026-10-26.

## Conclusions des agents — 11 octobre 2026 : des éditions récentes inconnues de Google

**Verdict** : Pas de blocage technique : Google explore rarement ce site jeune et peu cité, et il n'a pas relu la page Éditions depuis le 30 août. Les corrections de maillage et de balises sont faites ; le reste dépend de demandes d'indexation et du temps (mesurer à partir du 25 octobre).
**Agents** : gsc-expert, seo-technical, seo-sitemap.

- [Écarté] **Aucun blocage technique** (quasi certain) — robots.txt, noindex, canoniques, hreflang et données de page sont corrects ; les éditions indexées ont les mêmes réglages que celles qui ne le sont pas. **Action** : Rien à corriger de ce côté.
- [Vous] **Google explore rarement le site** (probable (forte)) — Dernière exploration d'une édition : 28 septembre. La page Éditions, qui liste tout, n'a pas été relue depuis le 30 août. Site jeune (quelques mois), très peu de liens venant d'ailleurs. **Action** : Demander l'indexation dans Search Console, d'abord de /archives.html puis des éditions les plus récentes (voir « À faire par vous »).
- [Vous] **Les éditions anglaises sont connues de Google, pas encore explorées** (certain (mesuré le 11 octobre)) — Sur les 6 dernières éditions anglaises inspectées, 5 sont « détectées, actuellement non indexées » et 1 (7 octobre) est indexée ; l'accueil anglais est indexé. Contrairement aux éditions françaises, Google connaît donc ces adresses (sans doute par le plan du site et les liens entre langues) mais ne les a pas encore lues. **Action** : Rien à corriger dans le site. Après /archives.html, une demande d'indexation de /en/archives/2026-10-11.html peut aider.
- [Corrigé] **L'accueil ne reliait que 10 éditions** (certain) — Les éditions de plus de 10 jours n'étaient accessibles que par la page Éditions, rarement explorée. **Action** : Fait : nouveau bloc « Les éditions du mois » sur l'accueil, avec un vrai lien HTML vers chaque édition des 30 derniers jours (21 éditions de plus). Ajouté aussi au générateur de l'accueil, donc il se maintient chaque jour.
- [Corrigé] **Pas de lien entre éditions avant le 10 octobre** (certain) — Les liens « précédente / suivante » n'existaient pas avant le 10 octobre. **Action** : Déjà en place depuis le 10 octobre. Effet attendu après la prochaine exploration par Google (une à trois semaines, sans garantie).
- [Corrigé] **Dates du plan du site trop uniformes** (certain) — J'avais mis la date du 11 octobre sur 58 éditions après la retouche de leurs balises : 65 pages portaient la même date, ce qui affaiblit ce champ pour Google, et les pages indiquaient une autre date que le plan. **Action** : Fait : chaque édition a retrouvé sa date de publication, cohérente avec la date inscrite dans la page. Un des agents préférait aligner les pages sur le 11 octobre ; j'ai retenu la solution qui ne touche pas au contenu des éditions figées. Règle à garder : ne pas faire bouger cette date pour une simple retouche de balises.
- [Corrigé] **Plan Actualités mal purgé** (certain) — La purge à 48 heures exactes laissait survivre une entrée de quelques secondes ; le script anglais ne pouvait pas purger les entrées françaises ; le fuseau horaire était fixé à +02:00 (faux à partir du 25 octobre). **Action** : Fait : seuil de 46 heures, purge qui reconnaît toutes les entrées, vrai fuseau Europe/Paris, 3 tests. L'absence de l'édition anglaise du 9 octobre dans ce plan reste à expliquer (journal du workflow du 9 octobre).
- [Corrigé] **Données structurées invalides sur 22 éditions de septembre** (certain) — Des valeurs étaient entourées de &#39; au lieu de guillemets, et des apostrophes mal codées : Google ignorait ces blocs ou lisait des signes parasites. **Action** : Fait : 22 fichiers réparés, uniquement à l'intérieur de leurs blocs de données structurées ; vérifié que rien d'autre n'a changé et qu'aucun bloc invalide ne subsiste sur 225.
- [Corrigé] **Descriptions coupées par « … »** (certain) — Le générateur coupait les questions longues en plein milieu. **Action** : Fait : générateur corrigé (phrases complètes ou titre + complément), 7 éditions françaises réparées, 8 tests.
- [Corrigé] **L'échantillon inspecté ne contenait que des pages françaises** (certain) — Les pages les plus vues sont pourtant anglaises (7 sur 8). **Action** : Fait : l'accueil anglais et les 6 dernières éditions anglaises sont maintenant inspectés chaque jour. Le compteur d'adresses du plan Actualités du rapport est aussi corrigé (5 et non 10).
- [Corrigé] **Liens internes vers /index.html** (certain) — Des menus pointent vers index.html alors que la canonique de l'accueil est « / » : Google voit deux adresses. **Action** : Fait le 11 octobre (PR 344) : menus des pages vivantes, gabarit de l'accueil et générateurs pointent vers « / ». Éditions passées non touchées.
- [À faire] **Pages anglaises déclarées en français** (certain) — Une balise de langue indique fr-FR sur les pages anglaises. **Action** : Corriger dans scripts/en/translate_daily.py pour les prochaines éditions (impact faible).
- [Écarté] **changefreq et priority du plan du site** (certain) — Google ignore ces deux champs. **Action** : Aucun gain à les retirer ; on les laisse.

À faire par le propriétaire :
- Dans Search Console, demander l'indexation de /archives.html en priorité : c'est la page qui lie les 15 éditions inconnues.
- Puis, à raison d'une dizaine par jour, des éditions du 4, 3, 2 et 1er octobre, puis du 30, 29, 24 et 23 septembre.
- Ouvrir Paramètres puis « Statistiques sur l'exploration » : nombre de requêtes par jour depuis le 20 septembre, part d'erreurs, temps de réponse. C'est le seul moyen d'écarter un problème d'hébergement autour du 28 septembre.
- Inspecter /archives/2026-09-28.html et lire « Page de provenance » : vous saurez par quel chemin Google a trouvé les éditions indexées.
- Partager publiquement chaque édition (réseaux, newsletter) : quelques liens venant d'ailleurs aident plus que tout réglage. IndexNow ne prévient pas Google.

Ce que l'on ne sait pas encore :
- À quelle fréquence Google est passé sur l'accueil entre le 28 septembre et le 7 octobre.
- Si une erreur du serveur a eu lieu autour du 28 septembre.
- Comment Google a découvert les 5 éditions indexées (plan du site, accueil ou demande manuelle).

Prochain contrôle : 25 octobre 2026 (ne rien conclure avant).

## Requêtes principales

- « scénarios email » : 0 clic(s), 7 impression(s), position 89,6
- « les scénarios » : 0 clic(s), 4 impression(s), position 27,8
- « ceutat » : 0 clic(s), 1 impression(s), position 8
- « las dos últimas » : 0 clic(s), 1 impression(s), position 4

## Pages les plus vues

- `/en/archives/2026-08-08.html` : 81 impressions, 0 clic(s), position 7,0
- `/en/archives/2026-09-21.html` : 30 impressions, 0 clic(s), position 6,9
- `/en/archives/2026-09-30.html` : 29 impressions, 0 clic(s), position 4,8
- `/en/archives/2026-09-13.html` : 23 impressions, 0 clic(s), position 4,8
- `/en/archives/2026-08-30.html` : 15 impressions, 1 clic(s), position 4
- `/en/archives/2026-09-15.html` : 15 impressions, 0 clic(s), position 6,6
- `/en/archives/2026-09-20.html` : 14 impressions, 0 clic(s), position 9,3
- `/le-projet.html` : 13 impressions, 1 clic(s), position 13,3

## Indexation page par page

- `/` : ok
- `/archives.html` : ok
- `/guide-pedagogique.html` : inconnue (Google ne reconnaît pas cette URL)
- `/le-projet.html` : ok
- `/sources.html` : ok
- `/glossaire.html` : ok
- `/en/` : ok
- `/archives/2026-10-18.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 1 j
- `/archives/2026-10-17.html` : ok, publiée il y a 2 j
- `/archives/2026-10-16.html` : ok, publiée il y a 3 j
- `/archives/2026-10-15.html` : ok, publiée il y a 4 j
- `/archives/2026-10-14.html` : ok, publiée il y a 5 j
- `/archives/2026-10-13.html` : ok, publiée il y a 6 j
- `/archives/2026-10-12.html` : ok, publiée il y a 7 j
- `/archives/2026-10-11.html` : ok, publiée il y a 8 j
- `/archives/2026-10-10.html` : exploree (Explorée, actuellement non indexée), publiée il y a 9 j
- `/archives/2026-10-09.html` : ok, publiée il y a 10 j
- `/archives/2026-10-08.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 11 j
- `/archives/2026-10-07.html` : ok, publiée il y a 12 j
- `/archives/2026-10-06.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 13 j
- `/archives/2026-10-05.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 14 j
- `/archives/2026-10-04.html` : ok, publiée il y a 15 j
- `/archives/2026-10-03.html` : ok, publiée il y a 16 j
- `/archives/2026-10-02.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 17 j
- `/archives/2026-10-01.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 18 j
- `/archives/2026-09-30.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 19 j
- `/archives/2026-09-29.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 20 j
- `/en/archives/2026-10-18.html` : decouverte (Détectée, actuellement non indexée), publiée il y a 1 j
- `/en/archives/2026-10-17.html` : ok, publiée il y a 2 j
- `/en/archives/2026-10-16.html` : ok, publiée il y a 3 j
- `/en/archives/2026-10-15.html` : ok, publiée il y a 4 j
- `/en/archives/2026-10-13.html` : exploree (Explorée, actuellement non indexée), publiée il y a 6 j
- `/en/archives/2026-10-12.html` : ok, publiée il y a 7 j

Le compteur « indexées » des plans du site n'est pas fiable : l'inspection page par page fait foi.
