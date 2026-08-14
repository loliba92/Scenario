# Journal de l'inspecteur

Une entrée par passage de la routine « Scénario — Inspecteur »
(`docs/routine-inspection-prompt.md`), même quand tout est conforme —
jamais de passage silencieux sans trace. La plus récente en tête.

---

## 2026-08-14 — L'addition de l'été / Le rattrapage à moitié / La panne budgétaire
**Vérifié** : cohérence interne (probabilités 25+45+30=100 %, `data-france-
impact`/`data-kind` vs texte `.france-line` pour les 3 cartes, présence des
classes CSS attendues dans `<style>` — dont `.delta-france`/`.delta-gauge*`/
`.delta-word`/`.delta-flag`, bloc identique à la version canonique de
`docs/routine-inspection-prompt.md` — et intégrité du dégradé SVG à 3 stops
avec `data-score`), sync `index.html` vs `archives/2026-08-14.html` (`diff`
complet — seuls écarts : chemins relatifs `archives/` vs direct, canonical/
`og:url`/`mainEntityOfPage`, `aria-current`, tous légitimes), lexique (3
`.lex-ref` ↔ 3 entrées, aucun terme orphelin dans un sens ou l'autre),
incohérence numérique interne (5 764 morts vs le record 6 969 de l'été 2022
cité en comparaison — deux faits différents, pas une incohérence ; aucune
autre occurrence isolée d'un chiffre par ailleurs répété 3+ fois), style des
paragraphes `.dek`/`.why`/`.essentiel-text` (plusieurs phrases de 40-55 mots
mais structure par coordination/liste, pas d'empilement de subordonnées
gênant, sigles PNACC/Fonds vert déjà `.lex-ref`, aucune rupture de registre
— `grep` `\bton \|\bta \|\btu \b` ne remonte que le `.share-block`,
exception légitime), formulation "Notre évaluation de l'impact pour la
France" intacte (jamais raccourcie en "France Impact :"), 3 chiffres
vérifiés contre sources (voir détail ci-dessous).
**Corrigé automatiquement** : label brut "stable" utilisé pour nommer le
scénario dans la phrase France Impact de `.essentiel-text` (`index.html`,
`archives/2026-08-14.html`, `feed.xml`) — exactement l'anti-exemple donné
par le prompt principal lui-même (`docs/routine-prompt.md` : mauvais « le
scénario stable (45%) reste le plus probable »), et l'édition du 13 août
avait évité ce même piège sur sa propre phrase équivalente ("le scénario
central" plutôt que "le scénario stable"). Correction minimale : suppression
du seul mot fautif, la reformulation concrète déjà présente dans la phrase
("un rattrapage timide sans rupture nette") reste intacte, aucun chiffre ni
fait touché. Avant : « mais c'est bien le scénario stable (45 %), un
rattrapage timide sans rupture nette, qui reste de loin le plus probable des
trois. » Après : « mais c'est bien le scénario (45 %), un rattrapage timide
sans rupture nette, qui reste de loin le plus probable des trois. »
**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
aucune — plusieurs phrases dépassaient 40 mots mais aucune jugée assez
gênante pour justifier une réécriture (voir "Vérifié" ci-dessus).
**Auto-vérification** : balises HTML équilibrées (script `html.parser`) sur
`index.html` et `archives/2026-08-14.html` — OK, aucune balise non fermée ni
mal imbriquée. Diff `index.html` vs `archives/2026-08-14.html` rejoué après
correctif — toujours synchronisés (mêmes écarts légitimes qu'avant
correctif, rien de nouveau). Correctif hors point 1 (texte uniquement) :
pas de capture Playwright nécessaire.
**Signalé pour revue humaine** :
- Source Météo-France (bilan climatique juin 2026, citée en bas de page)
  injoignable — `WebFetch` renvoie une erreur HTTP 503. Non re-vérifiable
  ce passage-ci ; à retenter au prochain passage plutôt que de chercher une
  source de remplacement.
- Les 3 autres chiffres structurants vérifiés (Santé publique France :
  5 764 morts en excès, +36 % — exact ; ministère de la Transition
  écologique via L'EnerGeek : 10-15 Md€ de facture été — exact ;
  Maire-info : Fonds vert 2,5 Md€ en 2024, ~840 M€ en 2026 (proche des 837
  M€ cités, écart d'arrondi source), 1 Md€ promis en 2027 — exact)
  correspondent tous à l'article, rien à signaler sur ces trois-là.
- Ce passage a probablement lieu après le départ des posts sociaux du
  matin (`feed.xml`) — la correction ci-dessus corrige le site pour les
  lecteurs suivants mais ne peut plus rattraper ce qui a déjà circulé sur
  Telegram/Instagram/Facebook/LinkedIn avec l'ancienne formulation.

---

## 2026-08-13 (correctif a posteriori, signalé par l'utilisateur) — La détente pétrolière / Le statu quo tendu / La rechute inflationniste
**Contexte** : hors passage automatique de la routine — l'utilisateur a signalé
en conversation que le 1er `.dek` de l'article (juste après `.question-text`)
contenait un registre bizarre, en rupture avec le reste du site : tutoiement
direct du lecteur ("ton argent") et une tournure jugée peu naturelle
("avait fini par refluer"). Vérifié que ce `.dek` est le seul endroit du
site à basculer en tutoiement (grep sur `\bton \|\bta \|\btu \b` — le seul
autre "tu" du site est dans le bloc Telegram, `.share-block`, où l'adresse
directe est volontaire). Réécriture forme uniquement : aucun chiffre, aucune
date, aucun nom propre, aucun lien de cause à effet modifié.
**Corrigé automatiquement** : `index.html` et `archives/2026-08-13.html`
(les deux, resynchronisés).
**Réécritures de clarté** (avant/après complet) :
- Avant : « L'inflation, c'est la hausse générale des prix : quand elle
  grimpe, ton argent achète moins qu'avant — un café, un plein d'essence,
  un loyer. Après le pic de 2022-2023, elle avait fini par refluer presque
  partout dans le monde, et les banques centrales pensaient avoir gagné la
  partie. Mi-2026, la tendance s'est brutalement inversée : la guerre entre
  les États-Unis et l'Iran, qui dure depuis le 28 février 2026, a rouvert
  le dossier en faisant flamber le prix du pétrole. »
  Après : « L'inflation, c'est la hausse générale des prix : quand elle
  grimpe, le pouvoir d'achat baisse — un café, un plein d'essence, un loyer
  coûtent plus cher qu'avant. Après le pic de 2022-2023, elle était
  retombée presque partout dans le monde, et les banques centrales
  pensaient avoir gagné la partie. Mi-2026, la tendance s'est brutalement
  inversée : la guerre entre les États-Unis et l'Iran, qui dure depuis le
  28 février 2026, a rouvert le dossier en faisant flamber le prix du
  pétrole. »
**Auto-vérification** : balises HTML équilibrées (script `html.parser`) sur
les deux fichiers modifiés — OK. Diff `index.html` vs
`archives/2026-08-13.html` rejoué après correctif — toujours synchronisés
(seules différences : chemins relatifs `../`, canonical/OG/nav, légitimes).
**Signalé pour revue humaine** : rien de nouveau (voir entrées des passages
automatiques ci-dessous pour le signalement sources non re-vérifiables,
toujours valable).

---

## 2026-08-13 (2e passage) — La détente pétrolière / Le statu quo tendu / La rechute inflationniste
**Second déclenchement du trigger le même jour** — `index.html`,
`archives/2026-08-13.html` et ce journal n'ont pas bougé depuis le passage
précédent (`git diff` vide entre le commit `fc5898e` et l'état de départ de
ce passage) : même édition, contenu strictement identique. Re-vérification
complète effectuée quand même (outils déterministes, coût marginal) plutôt
que de se fier au journal précédent sans contrôle.
**Vérifié** : classes CSS attendues présentes dans `<style>` (dont
`.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag`, aucune classe
utilisée dans le corps manquante à l'appel), sync `index.html` vs
`archives/2026-08-13.html` (`diff` complet — seuls écarts : chemins `../`,
`canonical`/`og:url`/`mainEntityOfPage`, `aria-current` — tous légitimes),
`data-france-impact`/`data-kind` cohérents avec le texte `.france-line`
adjacent pour les 3 cartes, probabilités 25+45+30=100 %, lexique (4
`.lex-ref` ↔ 4 entrées, aucun terme orphelin), label brut
favorable/stable/dégradé absent de `.essentiel-text`, formulation "Notre
évaluation de l'impact pour la France" intacte. Style des paragraphes
`.dek`/`.why`/`.essentiel-text` non ré-examiné en détail par lecture LLM
(contenu identique au passage précédent, déjà jugé sans phrase à
retravailler). Nouvelle tentative de `WebFetch` sur 2 des 4 sources
(Franceinfo, CNBC) pour voir si l'accès réseau avait changé depuis le
passage précédent.
**Corrigé automatiquement** : rien.
**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
aucune.
**Signalé pour revue humaine** : sources toujours non re-vérifiables —
`WebFetch` renvoie encore `EGRESS_BLOCKED` sur Franceinfo et CNBC (même
politique réseau que le passage précédent, pas un problème ponctuel) ; arrêt
après 2 tentatives plutôt que d'épuiser les 4 restantes pour un résultat
déjà établi. Al Jazeera et Euronews non retentés ce passage-ci pour la même
raison. À revérifier lors d'un prochain passage si l'accès réseau le
permet.

---

## 2026-08-13 — La détente pétrolière / Le statu quo tendu / La rechute inflationniste
**Vérifié** : cohérence interne (probabilités 25+45+30=100 %, `data-france-
impact`/`data-kind` vs texte `.france-line`, présence des classes CSS
attendues dans `<style>` dont `.delta-france`/`.delta-gauge*`/`.delta-word`/
`.delta-flag` et intégrité du dégradé SVG à 3 stops, sync `index.html` vs
`archives/2026-08-13.html`), lexique (4 `.lex-ref` ↔ 4 entrées, aucun terme
orphelin dans un sens ou l'autre), label brut favorable/stable/dégradé
absent de `.essentiel-text`, formulation "Notre évaluation de l'impact pour
la France" intacte (jamais raccourcie en "France Impact :"), style des
paragraphes `.dek`/`.why`/`.essentiel-text` (aucune phrase jugée assez
gênante pour justifier une réécriture), 0 chiffre vérifié contre source
(voir signalement ci-dessous).
**Corrigé automatiquement** : rien.
**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
aucune.
**Signalé pour revue humaine** : les 4 sources citées en bas de page
(Franceinfo, CNBC, Al Jazeera, Euronews) sont non re-vérifiables depuis cet
environnement d'exécution — `WebFetch` renvoie `EGRESS_BLOCKED` (politique
réseau de la session, pas un lien mort côté site) pour les quatre domaines.
Aucun chiffre n'a donc pu être comparé à sa source ce passage-ci ; à
revérifier lors d'un prochain passage si l'accès réseau le permet.

---
