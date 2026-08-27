# Backlog produit / éditorial — Scénario

Backlog produit (confiance/méthode, SEO, participatif, mesure), tenu à
part du backlog technique de `docs/ARCHITECTURE.md` (section « Backlog »)
pour ne pas mélanger les deux sources. **Règle de non-duplication** :
quand un ticket ici recoupe une entrée déjà documentée dans
`docs/ARCHITECTURE.md`, on y renvoie par son intitulé plutôt que de
recopier son contenu — la source de vérité pour cette entrée reste
`ARCHITECTURE.md`, jamais copiée ici en double.

## Audit externe du 27 août

Comparé point par point à l'état réel du dépôt avant d'agir, même méthode
que l'audit LLM du 20 août documenté dans `docs/ARCHITECTURE.md` (section
Backlog → Contenu). L'utilisateur a soumis un backlog de 23 tickets
(priorités P0→P3) produit ailleurs. **Mapping de priorité** : l'échelle
externe va de P0 (le plus urgent) à P3 ; ce backlog-ci reprend la même
échelle P0→P3 que l'audit d'origine (contrairement à `ARCHITECTURE.md` qui
va de P1 à P3 — pas de conversion nécessaire ici puisque ce fichier est
dédié à cet audit). Plusieurs tickets recoupaient déjà des idées ou
fonctionnalités présentes dans ce dépôt, listées ci-dessous pour éviter de
les refaire à neuf ; les tickets réellement nouveaux sont retenus ensuite.

### Déjà en place, à ne pas refaire

- **« V0 → V1 → V2 »** (raconter l'évolution d'un sujet suivi) : le
  mécanisme existe déjà dans `suivi/_gabarit.html` (blocs `.version`,
  tag/date/titre, repliables). Le travail restant est éditorial, pas
  technique : reprendre le texte des versions déjà publiées (7 pages
  `suivi/*.html`) pour qu'il raconte explicitement *ce qu'on pensait → ce
  qui a changé → ce qu'on pense maintenant*, pas juste un constat
  factuel.
- **Récap hebdomadaire** : existe déjà (`hebdo/`, une page par semaine
  depuis le 2 août), déjà linké depuis la bande `.top-updates` de chaque
  édition (« Récap de la semaine »).
- **Vote communautaire / affichage des résultats** : déjà en réflexion
  active côté technique — voir dans `docs/ARCHITECTURE.md` l'entrée
  « Faire remonter le vote quotidien sur le site en plus de Telegram,
  idée du 26 août » (section Backlog → Contenu). Mécanisme (clic →
  événement GoatCounter côté client, zéro backend) et point non tranché
  (afficher ou non un pourcentage en direct) déjà posés là-bas. Reprendre
  ce fil plutôt qu'en ouvrir un nouveau ici.
- **Mesure de calibration** : déjà loggée dans `docs/ARCHITECTURE.md`,
  entrée « Page de calibration ("avions-nous raison, au global"), idée du
  10 août » — explicitement **bloquée par le volume de suivis résolus**,
  pas par l'absence d'idée. Le dépôt a 6 semaines d'existence (35
  éditions depuis le 18 juillet, 7 suivis actifs) : à revisiter dans
  plusieurs mois, pas un chantier à lancer maintenant.
- **Données ouvertes / API publique** : déjà loggée dans
  `docs/ARCHITECTURE.md`, section Technique, entrée « Données ouvertes /
  API publique, idée du 10 août ». `feed.json` existe déjà en JSON
  structuré ; le travail restant est de le documenter comme flux stable,
  pas de le construire. Une « base publique des scénarios » consultable
  (proposée dans le backlog externe) est le même chantier à un stade
  antérieur — un jalon de cette même entrée, pas un ticket séparé.
- **Identité du fondateur** : le texte existe déjà (`le-projet.html`,
  section « Qui fait Scénario » — nom, double casquette
  technique/éditoriale). Le manque réel est visuel (aucune photo) et de
  ton (peu de 1ʳᵉ personne), pas un chantier de création.

### Contradiction à lever avant de prioriser le participatif

Le backlog externe propose de « renforcer » le vote communautaire et de
« renforcer le mardi participatif ». Le sondage Telegram natif est
documenté (`docs/ARCHITECTURE.md`, entrée du 26 août) comme fonctionnant
très bien techniquement mais touchant une fraction minime du lectorat —
ce n'est donc pas un mécanisme cassé à réparer, contrairement à ce qu'un
retour antérieur isolé pouvait laisser penser (`docs/routine-prompt.md`,
exclusion de Telegram du bloc de notifications compact, faute de portée
suffisante). « Mardi participatif », en revanche, n'existe nulle part
dans le code ni dans `docs/routine-prompt.md` — le mardi est aujourd'hui
le registre « libre, plus fort enjeu/incertitude ». Le verbe juste est
« créer », pas « renforcer » — et ça ne devrait être cadré qu'une fois le
vote sur site du 26 août tranché (pourcentage en direct ou non), puisqu'un
mardi participatif en dépendrait probablement.

### Tickets réellement nouveaux, retenus

- **P0 — Clarifier « probabilité à l'instant T ».** Rendre visible, au
  niveau de l'édition elle-même (pas seulement dans `le-projet.html`),
  que les probabilités reflètent l'information disponible à la
  publication et sont vouées à être réévaluées — pas une prédiction
  figée. `le-projet.html` porte déjà un caveat proche (« Chaque édition
  reste figée à sa date de publication ») : l'adapter plutôt que
  réinventer une formulation.
- **P0 — Ajouter « Pourquoi cette probabilité ? ».** Rendre plus
  visibles, notamment sur les pages `suivi/`, les facteurs qui font
  monter/baisser un scénario d'une version à l'autre — la logique existe
  déjà au niveau de chaque édition (`why`, comparaison explicite entre
  les 3 scénarios, `docs/routine-prompt.md` étape 5) mais n'est pas
  systématiquement reprise lors d'une révision `suivi/`.
- **P0 — Distinguer Faits / Analyse / Scénarios.** La séparation existe
  déjà implicitement dans la structure (`.dek` = faits/contexte,
  `.comprendre-box` = analyse, cartes = scénarios) mais sans étiquetage
  explicite. Point de vigilance à l'exécution : ne pas dupliquer les
  `.section-label` déjà nombreux (« Favorable, stable ou dégradé »,
  « Pour ceux qui découvrent le sujet »...) — un balisage léger plutôt
  qu'une re-architecture de la mise en page.
- **P0 — Renforcer « Notre méthode ».** `le-projet.html` a déjà une
  section méthode (« Les probabilités affichées ne sortent pas d'un
  tirage au hasard... ») — préciser/étoffer, pas créer.
- **P0/P1 — Rattrapage historique, ticket ajouté ici (absent du backlog
  externe).** Les 4 tickets ci-dessus ne précisent pas s'ils s'appliquent
  aux futures éditions seulement ou aussi aux 35 déjà publiées. Décision
  à prendre avant de lancer : sans rattrapage, le site aura un
  avant/après visible pendant des mois (archives figées, jamais
  remodifiées après publication).
- **P1 — Optimiser les titres SEO / développer le glossaire / pages
  thématiques / maillage interne / CTA newsletter.** Tickets valides,
  effort raisonnable. Point de départ déjà favorable, pas de
  construction ex nihilo : glossaire déjà alimenté chaque jour (étape
  6ter de `docs/routine-prompt.md`), tags fermés dans `docs/tags.md`
  réutilisables pour des pages thématiques, filtre
  `archives.html?tag=X` déjà en place comme brique de départ pour le
  maillage.
- **P2 (préalable), puis P2 — Vote sur site, puis mardi participatif.**
  Trancher d'abord le point ouvert de l'entrée du 26 août dans
  `docs/ARCHITECTURE.md` (pourcentage en direct ou non), implémenter le
  vote sur site, **puis seulement** cadrer un « mardi participatif »
  (créer, pas renforcer) une fois ce socle posé.
- **P3 — Score historique de Scénario.** Nouveau par rapport à l'existant
  (la calibration du 10 août mesure la justesse globale, pas un score de
  suivi dans le temps) — mais dépend du même préalable qu'elle : un
  export structuré scénario ↔ résultat réel constaté, qui n'existe pas
  encore et qui conditionne aussi bien ce ticket que la calibration et
  les données ouvertes. À documenter comme un prérequis commun aux
  trois, pas trois chantiers indépendants.
