# Rapport Search Console

Site `sc-domain:lesscenarios.fr` · données Google du 2026-10-19 au 2026-11-15 · synchronisé le 2026-11-18 (les chiffres de Google ont ~3 jours de retard).

**Verdict : MOYEN** — Le site apparaît (position moyenne 10,8) mais est très peu cliqué (1,0 %).

## Chiffres (28 jours)

- 4 clics, 394 impressions, taux de clic 1,0 %, position moyenne 10,8.
- Pages indexées : 31 sur 33 inspectées ; éditions inconnues de Google : 1 (dont 0 de plus de 7 jours).
- Requêtes : 21 (dont 5 avec le nom du site).
- Tendance (14 jours, jusqu'au 2026-11-15) : impressions 150 contre 244, clics 2 contre 2.

## À résoudre — critique

- Rien.

## À résoudre — important

- Le site apparaît (position moyenne 10,8) mais est très peu cliqué (1,0 %). **Action** : Retravailler les titres et descriptions des pages les plus vues. **Agent à envoyer** : seo-content. **Mission** : Proposer de nouveaux titres (≤ 59 caractères) et descriptions (100–160) plus incitatifs pour les pages les plus vues, dans le ton sobre de Scénario ; ne rien promettre.
- Éditions en anglais : 1 descriptions hors norme. **Action** : Corriger via les générateurs (voir .claude/seo-routage.md). **Mission** : Correction directe dans les générateurs (generate_seo_head.py, translate_daily.py), puis régénération et tests.

## À surveiller

- Pages en première page de Google sans aucun clic : `/en/archives/2026-09-13.html`, `/en/archives/2026-09-24.html`, `/en/archives/2026-09-26.html`, `/en/archives/2026-10-17.html`. **Action** : Titre ou description à rendre plus incitatif. **Agent à envoyer** : seo-content. **Mission** : Réécrire titre et description de ces pages (liste dans le rapport), puis vérifier la cohérence avec le contenu.
- L'adresse `/index.html` apparaît dans Google en plus de `/`. **Action** : Vérifier la balise canonique de l'accueil. **Agent à envoyer** : seo-technical. **Mission** : Vérifier la canonique de l'accueil, les redirections et les liens internes qui pointent vers /index.html.
- 1 page : Google connaît l'adresse mais ne l'a pas encore explorée ou retenue (`/en/archives/2026-11-18.html`). **Action** : Renforcer les liens internes vers la page, enrichir son contenu, demander l'indexation. **Agent à envoyer** : seo-content. **Mission** : Comprendre pourquoi Google retient ou écarte ces pages (profondeur, unicité, qualité perçue) et proposer des améliorations de contenu et de liens internes.

## Ce qui fonctionne

- 7 pages principales indexées : `/`, `/archives.html`, `/guide-pedagogique.html`, `/le-projet.html`, `/sources.html`, `/glossaire.html`.
- 24 éditions indexées par Google.
- Plan du site `/sitemap.xml` lu par Google sans erreur (241 adresses envoyées).
- Plan du site `/sitemap-news.xml` lu par Google sans erreur (4 adresses envoyées).
- Balises des 118 éditions en français conformes : titres sans coupure, descriptions de 100 à 160 caractères, un seul titre principal, canonique présente, toutes dans le plan du site.

## Ce qui ne fonctionne pas

- Presque aucune visite venue de Google : 4 clics en 28 jours.
- Visibilité en baisse : 150 impressions sur 14 jours contre 244 avant.

## Ce que seul le propriétaire peut faire

- Dans Search Console, collez l'adresse de l'édition du jour dans la barre du haut, puis « Demander une indexation » (quota limité par jour) ; répétez pour les éditions inconnues les plus récentes.
- Relisez les recommandations des agents avant de valider tout changement de titres ou de contenu.

## Conclusions des agents — 16 novembre 2026 : traduction anglaise en panne depuis le 11 novembre ; français toujours peu exploré

**Verdict** : Les éditions françaises de plus de 7 jours restent inconnues de Google (12 sur 33 pages inspectées), alors que les éditions anglaises sont indexées le jour même : le maillage, le plan du site et les balises sont pourtant identiques, donc attendre ne suffit plus. Une panne du site a de plus été trouvée et corrigée : la traduction anglaise échouait chaque jour depuis le 11 novembre.
**Agents** : g, s, c, -, e, x, p, e, r, t, ,,  , s, e, o, -, t, e, c, h, n, i, c, a, l, ,,  , s, e, o, -, c, o, n, t, e, n, t, ..

- [Corrigé] **Traduction anglaise en échec du 11 au 16 novembre (6 éditions anglaises manquantes)** (certain (journal du workflow lu, correctif testé)) — Les liens de langue (hreflang) ajoutés au bloc /en/ du plan du site se trouvaient entre <loc> et <lastmod> ; le script de traduction ne retrouvait plus ce bloc et s'arrêtait avant d'enregistrer. Conséquences : plus de page anglaise, liens de langue des éditions françaises du 11 au 16 novembre vers des pages absentes, bouton EN renvoyant à l'accueil anglais. **Action** : Fait (PR 491) : l'expression tolère ces liens, test ajouté, traduction relancée pour l'édition du jour. Les éditions anglaises du 11 au 15 novembre ne sont pas rattrapées : voir « à décider ».
- [Corrigé] **Six descriptions de moins de 100 caractères (1 FR, 5 EN)** (certain (code lu, pages mesurées)) — La question seule servait de description ; la traduction anglaise, plus courte, tombait sous 100 caractères sans contrôle. **Action** : Fait (PR 492) : les deux générateurs complètent une description trop courte ; les 6 pages corrigées (description, og, twitter, données structurées ; texte visible inchangé, vérifié ligne à ligne).
- [Vous] **Éditions françaises inconnues de Google (12 de plus de 7 jours : du 27 octobre au 8 novembre sauf le 3)** (mesuré ; cause probable, non prouvée) — Rien ne bloque côté site (robots, canoniques, plan du site lu sans erreur, liens à un clic de l'accueil). Google semble explorer l'anglais en priorité. /archives.html n'a pas été relue depuis le 21 octobre. **Action** : Seul le propriétaire peut agir : demandes d'indexation, lecture de « Page de provenance » dans Search Console, liens venant d'autres sites.
- [À faire] **/guide-pedagogique.html « détectée, non indexée »** (moyenne) — Contenu qui recoupe fortement le-projet.html, exemple fictif, aucun lien depuis archives.html, titre peu parlant. **Action** : Page vivante, modifiable : exemple réel (budget 2027), liste d'éditions pour la classe, titre « Lire une probabilité et un scénario : guide pour la classe ». Non fait ce jour (réécriture de contenu : à valider).
- [Vous] **Liens de langue incomplets sur 12 éditions de septembre (13 au 24)** (certain (relu par l'agent)) — 12 éditions anglaises n'ont pas la balise hreflang vers elles-mêmes ; l'édition française du 13 septembre ne déclare pas sa version anglaise. Le plan du site est complet. **Action** : Éditions figées : ces balises sortent de l'exception autorisée. À décider par le propriétaire.
- [À faire] **Liens vers /index.html dans les gabarits hebdo et suivi** (certain) — hebdo/*.html et suivi/_gabarit.html pointent encore vers ../index.html ; la canonique de l'accueil est correcte, donc impact faible. **Action** : Non fait ce jour (origine du gabarit hebdomadaire à confirmer).
- [Écarté] **Titres des trois pages anglaises sans clic (13 et 24 septembre, 17 octobre)** (faible (72 impressions)) — Trop peu de données pour conclure ; la première est déjà réécrite le 12 octobre. **Action** : Rien à changer maintenant ; propositions de l'agent conservées pour un prochain contrôle.

À faire par le propriétaire :
- Dans Search Console, demander l'indexation de /archives.html (non relue depuis le 21 octobre), puis de quelques éditions françaises récentes par jour (en commençant par le 8 novembre), puis de /guide-pedagogique.html.
- Inspecter /en/archives/2026-11-10.html et lire « Pages de provenance » : cela dira comment Google découvre l'anglais et pas le français.
- Décider du rattrapage des éditions anglaises du 11 au 15 novembre (nouvelles pages ; liens de langue à ajouter sur les éditions françaises correspondantes).
- Décider d'ajouter les liens de langue manquants sur les éditions de septembre (13 au 24).
- Partager publiquement des éditions françaises : quelques liens extérieurs pèsent plus que tout réglage.

Ce que l'on ne sait pas encore :
- Pourquoi Google découvre l'anglais en quelques heures et le français non.
- Si les demandes d'indexation recommandées en octobre ont été faites.
- L'effet des titres réécrits le 12 octobre : 4 clics sur 426 impressions, trop peu pour conclure.

Prochain contrôle : 2026-11-23.

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

## Requêtes principales

- « viralité organique dirigée » : 0 clic(s), 16 impression(s), position 15
- « france peripheral neuropathy market » : 0 clic(s), 10 impression(s), position 57,8
- « les scénarios » : 0 clic(s), 9 impression(s), position 18,8
- « scénarios email » : 0 clic(s), 7 impression(s), position 70,1
- « scénarios » : 0 clic(s), 5 impression(s), position 25,6
- « how do healthcare deserts affect access to medical care? in 2026 » : 0 clic(s), 2 impression(s), position 6
- « "budget 2027" "49.3" censure lecornu » : 0 clic(s), 1 impression(s), position 3
- « 10 nations rugby » : 0 clic(s), 1 impression(s), position 67

## Pages les plus vues

- `/en/archives/2026-10-07.html` : 49 impressions, 1 clic(s), position 4,7
- `/le-projet.html` : 30 impressions, 0 clic(s), position 13,8
- `/` : 22 impressions, 1 clic(s), position 3,8
- `/en/archives/2026-08-08.html` : 22 impressions, 1 clic(s), position 7,5
- `/archives/2026-10-03.html` : 19 impressions, 0 clic(s), position 13,7
- `/en/archives/2026-09-26.html` : 19 impressions, 0 clic(s), position 9,3
- `/en/archives/2026-10-17.html` : 18 impressions, 0 clic(s), position 6,3
- `/en/archives/2026-09-13.html` : 17 impressions, 0 clic(s), position 4,1

## Indexation page par page

- `/` : ok
- `/archives.html` : ok
- `/guide-pedagogique.html` : ok
- `/le-projet.html` : ok
- `/sources.html` : ok
- `/glossaire.html` : ok
- `/en/` : ok
- `/archives/2026-11-18.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 0 j
- `/archives/2026-11-17.html` : ok, publiée il y a 1 j
- `/archives/2026-11-16.html` : ok, publiée il y a 2 j
- `/archives/2026-11-15.html` : ok, publiée il y a 3 j
- `/archives/2026-11-14.html` : ok, publiée il y a 4 j
- `/archives/2026-11-13.html` : ok, publiée il y a 5 j
- `/archives/2026-11-12.html` : ok, publiée il y a 6 j
- `/archives/2026-11-11.html` : ok, publiée il y a 7 j
- `/archives/2026-11-10.html` : ok, publiée il y a 8 j
- `/archives/2026-11-09.html` : ok, publiée il y a 9 j
- `/archives/2026-11-08.html` : ok, publiée il y a 10 j
- `/archives/2026-11-07.html` : ok, publiée il y a 11 j
- `/archives/2026-11-06.html` : ok, publiée il y a 12 j
- `/archives/2026-11-05.html` : ok, publiée il y a 13 j
- `/archives/2026-11-04.html` : ok, publiée il y a 14 j
- `/archives/2026-11-03.html` : ok, publiée il y a 15 j
- `/archives/2026-11-02.html` : ok, publiée il y a 16 j
- `/archives/2026-11-01.html` : ok, publiée il y a 17 j
- `/archives/2026-10-31.html` : ok, publiée il y a 18 j
- `/archives/2026-10-30.html` : ok, publiée il y a 19 j
- `/en/archives/2026-11-18.html` : decouverte (Détectée, actuellement non indexée), publiée il y a 0 j
- `/en/archives/2026-11-17.html` : ok, publiée il y a 1 j
- `/en/archives/2026-11-16.html` : ok, publiée il y a 2 j
- `/en/archives/2026-11-10.html` : ok, publiée il y a 8 j
- `/en/archives/2026-11-09.html` : ok, publiée il y a 9 j
- `/en/archives/2026-11-08.html` : ok, publiée il y a 10 j

Le compteur « indexées » des plans du site n'est pas fiable : l'inspection page par page fait foi.
