# Rapport Search Console

Site `sc-domain:lesscenarios.fr` · données Google du 2026-09-11 au 2026-10-08 · synchronisé le 2026-10-11 (les chiffres de Google ont ~3 jours de retard).

**Verdict : CRITIQUE** — 7 éditions de plus de 7 jours sont inconnues de Google (sur 26 pages inspectées). Demander l'indexation dans Search Console, vérifier un lien interne depuis une page déjà indexée, patienter si la page a moins de 7 jours.

## Chiffres (28 jours)

- 4 clics, 286 impressions, taux de clic 1,4 %, position moyenne 9,1.
- Pages indexées : 10 sur 26 inspectées ; éditions inconnues de Google : 15 (dont 7 de plus de 7 jours).
- Requêtes : 6 (dont 2 avec le nom du site).
- Tendance (14 jours, jusqu'au 2026-10-08) : impressions 161 contre 125, clics 0 contre 4.

## À résoudre — critique

- 7 éditions de plus de 7 jours sont inconnues de Google (sur 26 pages inspectées). **Action** : Demander l'indexation dans Search Console, vérifier un lien interne depuis une page déjà indexée, patienter si la page a moins de 7 jours. **Agent à envoyer** : seo-technical + seo-sitemap. **Mission** : Diagnostiquer pourquoi ces éditions restent inconnues de Google : profondeur de clics depuis l'accueil, liens internes vers les éditions récentes, structure et dates du plan du site, robots.txt, vitesse. Rendre un plan correctif chiffré, classé par impact.

## À résoudre — important

- Le site apparaît (position moyenne 9,1) mais est très peu cliqué (1,4 %). **Action** : Retravailler les titres et descriptions des pages les plus vues. **Agent à envoyer** : seo-content. **Mission** : Proposer de nouveaux titres (≤ 59 caractères) et descriptions (100–160) plus incitatifs pour les pages les plus vues, dans le ton sobre de Scénario ; ne rien promettre.
- 1 page : Google connaît l'adresse mais ne l'a pas encore explorée ou retenue (`/guide-pedagogique.html`). **Action** : Renforcer les liens internes vers la page, enrichir son contenu, demander l'indexation. **Agent à envoyer** : seo-content. **Mission** : Comprendre pourquoi Google retient ou écarte ces pages (profondeur, unicité, qualité perçue) et proposer des améliorations de contenu et de liens internes.
- Éditions en français : 7 descriptions hors norme. **Action** : Corriger via les générateurs (voir .claude/seo-routage.md). **Mission** : Correction directe dans les générateurs (generate_seo_head.py, translate_daily.py), puis régénération et tests.

## À surveiller

- Seulement 6 requêtes enregistrées. **Action** : Trop peu pour piloter par mots-clés : viser d'abord l'indexation des éditions. **Agent à envoyer** : seo-cluster. **Mission** : Proposer des axes thématiques (matières, sujets récurrents) et un maillage interne pour élargir les requêtes, sans produire de pages en série.
- Pages en première page de Google sans aucun clic : `/`, `/en/archives/2026-08-08.html`, `/en/archives/2026-09-11.html`, `/en/archives/2026-09-13.html`, `/en/archives/2026-09-15.html`. **Action** : Titre ou description à rendre plus incitatif. **Agent à envoyer** : seo-content. **Mission** : Réécrire titre et description de ces pages (liste dans le rapport), puis vérifier la cohérence avec le contenu.
- L'adresse `/index.html` apparaît dans Google en plus de `/`. **Action** : Vérifier la balise canonique de l'accueil. **Agent à envoyer** : seo-technical. **Mission** : Vérifier la canonique de l'accueil, les redirections et les liens internes qui pointent vers /index.html.

## Ce qui fonctionne

- Visibilité en hausse : 161 impressions sur les 14 derniers jours contre 125 avant.
- Google affiche le site en position moyenne 9,1 (première page) sur 286 impressions.
- 5 pages principales indexées : `/`, `/archives.html`, `/le-projet.html`, `/sources.html`, `/glossaire.html`.
- 5 éditions indexées par Google.
- Plan du site `/sitemap.xml` lu par Google sans erreur (162 adresses envoyées).
- Plan du site `/sitemap-news.xml` lu par Google sans erreur (10 adresses envoyées).
- Balises des 48 éditions en anglais conformes : titres sans coupure, descriptions de 100 à 160 caractères, un seul titre principal, canonique présente, toutes dans le plan du site.

## Ce qui ne fonctionne pas

- Presque aucune visite venue de Google : 4 clics en 28 jours.
- Découverte trop lente : 7 éditions publiées depuis plus d’une semaine ne sont pas connues de Google.
- Page principale non indexée : `/guide-pedagogique.html`.

## Ce que seul le propriétaire peut faire

- Dans Search Console, collez l'adresse de l'édition du jour dans la barre du haut, puis « Demander une indexation » (quota limité par jour) ; répétez pour les éditions inconnues les plus récentes.
- Faites de même pour les pages principales « détectées, non indexées » (guide pédagogique, par exemple).
- Relisez les recommandations des agents avant de valider tout changement de titres ou de contenu.

## Requêtes principales

- « scénarios email » : 0 clic(s), 8 impression(s), position 88,1
- « ceutat » : 0 clic(s), 1 impression(s), position 8
- « las dos últimas » : 0 clic(s), 1 impression(s), position 4
- « les scénarios » : 0 clic(s), 1 impression(s), position 47
- « n'importe quoi » : 0 clic(s), 1 impression(s), position 1
- « oui » : 0 clic(s), 1 impression(s), position 1

## Pages les plus vues

- `/en/archives/2026-08-08.html` : 81 impressions, 0 clic(s), position 7,0
- `/en/archives/2026-09-21.html` : 29 impressions, 0 clic(s), position 6,9
- `/en/archives/2026-09-13.html` : 23 impressions, 0 clic(s), position 5,6
- `/en/archives/2026-08-30.html` : 21 impressions, 1 clic(s), position 5,9
- `/en/archives/2026-09-15.html` : 16 impressions, 0 clic(s), position 7
- `/le-projet.html` : 15 impressions, 1 clic(s), position 8,7
- `/newsletter.html` : 14 impressions, 0 clic(s), position 52,2
- `/en/archives/2026-09-11.html` : 13 impressions, 0 clic(s), position 7,5

## Indexation page par page

- `/` : ok
- `/archives.html` : ok
- `/guide-pedagogique.html` : decouverte (Détectée, actuellement non indexée)
- `/le-projet.html` : ok
- `/sources.html` : ok
- `/glossaire.html` : ok
- `/archives/2026-10-11.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 0 j
- `/archives/2026-10-10.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 1 j
- `/archives/2026-10-09.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 2 j
- `/archives/2026-10-08.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 3 j
- `/archives/2026-10-07.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 4 j
- `/archives/2026-10-06.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 5 j
- `/archives/2026-10-05.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 6 j
- `/archives/2026-10-04.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 7 j
- `/archives/2026-10-03.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 8 j
- `/archives/2026-10-02.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 9 j
- `/archives/2026-10-01.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 10 j
- `/archives/2026-09-30.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 11 j
- `/archives/2026-09-29.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 12 j
- `/archives/2026-09-28.html` : ok, publiée il y a 13 j
- `/archives/2026-09-27.html` : ok, publiée il y a 14 j
- `/archives/2026-09-26.html` : ok, publiée il y a 15 j
- `/archives/2026-09-25.html` : ok, publiée il y a 16 j
- `/archives/2026-09-24.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 17 j
- `/archives/2026-09-23.html` : inconnue (Google ne reconnaît pas cette URL), publiée il y a 18 j
- `/archives/2026-09-22.html` : ok, publiée il y a 19 j

Le compteur « indexées » des plans du site n'est pas fiable : l'inspection page par page fait foi.
