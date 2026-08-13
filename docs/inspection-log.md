# Journal de l'inspecteur

Une entrée par passage de la routine « Scénario — Inspecteur »
(`docs/routine-inspection-prompt.md`), même quand tout est conforme —
jamais de passage silencieux sans trace. La plus récente en tête.

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
