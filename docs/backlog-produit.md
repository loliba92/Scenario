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

- **[FAIT le 27 août] P0 — Clarifier « probabilité à l'instant T ».**
  Rendu visible directement sous les 3 scénarios de chaque édition, pas
  seulement dans `le-projet.html` : le disclaimer fixe `.indicators-note`
  (`docs/routine-prompt.md`) dit désormais explicitement que les
  probabilités sont « estimées avec l'information disponible à la
  publication et réévaluées si la situation change ». Appliqué
  rétroactivement à l'édition du 27 août (`index.html` +
  `archives/2026-08-27.html`).
- **[FAIT le 27 août] P0 — Ajouter « Pourquoi cette probabilité ? ».**
  La logique existait déjà en grande partie dans `suivi/_gabarit.html`
  (chaque `mini-scenario-text` doit dire pourquoi un scénario
  monte/descend/reste stable, la conclusion doit nommer le fait qui
  explique le plus gros mouvement) — mais seulement dans les commentaires
  HTML du gabarit, jamais explicité dans le texte de la routine elle-même.
  Ajouté dans `docs/routine-detection-prompt.md` : l'exigence de nommer
  le fait (ou son absence) s'applique désormais aux 3 `mini-scenario-text`
  de chaque nouvelle version, pas seulement à la conclusion.
- **P0 — Distinguer Faits / Analyse / Scénarios.** La séparation existe
  déjà implicitement dans la structure (`.dek` = faits/contexte,
  `.comprendre-box` = analyse, cartes = scénarios) mais sans étiquetage
  explicite. Point de vigilance à l'exécution : ne pas dupliquer les
  `.section-label` déjà nombreux (« Favorable, stable ou dégradé »,
  « Pour ceux qui découvrent le sujet »...) — un balisage léger plutôt
  qu'une re-architecture de la mise en page.
- **[FAIT le 27 août] P0 — Renforcer « Notre méthode ».** `le-projet.html`
  avait déjà une section méthode (« Les probabilités affichées ne
  sortent pas d'un tirage au hasard... ») avec ses 4 axes en liste — ajouté
  un paragraphe de clôture qui explicite que c'est un jugement structuré,
  pas un algorithme, pour ne jamais laisser croire à une précision
  scientifique que les faits du jour ne permettent pas.
- **P0/P1 — Rattrapage historique, ticket ajouté ici (absent du backlog
  externe).** Les 4 tickets ci-dessus ne précisent pas s'ils s'appliquent
  aux futures éditions seulement ou aussi aux 35 déjà publiées. Décision
  à prendre avant de lancer : sans rattrapage, le site aura un
  avant/après visible pendant des mois (archives figées, jamais
  remodifiées après publication).
- **[FAIT le 27 août] CTA newsletter — sorti du ticket groupé ci-dessous,
  traité seul (wording only, zéro coût).** `.follow-inline-text` (bloc
  compact réutilisé chaque édition, `docs/routine-prompt.md`) reformulé
  en impératif : « Ne rate pas la prochaine édition : » au lieu de
  « Reste informé de la prochaine édition : ». Ajouté un sous-titre à
  `newsletter.html` (gratuit/sans spam/résiliable en un clic) qui
  manquait sous le h1. Appliqué rétroactivement à l'édition du 27 août.
- **P1 — Optimiser les titres SEO / développer le glossaire / pages
  thématiques / maillage interne.** Tickets valides, effort raisonnable
  mais pas du texte seul (page/template à construire). Point de départ
  déjà favorable, pas de construction ex nihilo : glossaire déjà
  alimenté chaque jour (étape
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

## Déclinaison papier — « Les Cahiers de Scénario »

Objectif produit distinct de l'audit du 27 août, mais à garder visible
dans ce même backlog consolidé. Stratégie complète et phasage (PDF hebdo
freemium → kit pédagogique → objet imprimé payant trimestriel) déjà
tranchés et documentés dans `docs/strategie-papier.md` — ne pas la
recopier ici, ce fichier reste la source de vérité. Entrée backlog
correspondante : `docs/ARCHITECTURE.md`, section Distribution /
automatisation, « P3 — Déclinaison papier de Scénario, idée du 17
août ».

**Maquette déjà réalisée (25 août), à ne pas refaire.** Une maquette de
mise en page 2 pages A4 — « Les Cahiers de Scénario » — existe déjà comme
Artifact publié (non versionné dans ce dépôt git) :
https://claude.ai/code/artifact/d5e72207-faf4-4b9d-b0ed-24ccaa21e626.
Couverture plein cadre + page article, contenu réel du site (chiffres,
scénarios, « L'essentiel », vraie photo Pexels déjà utilisée sur le
site — rien d'inventé), calibrée A4 210×297mm et imprimable directement
(Ctrl/Cmd+P). Sert à juger du ton d'un numéro payant à focus thématique
tournant — exemple pris pour la maquette : « IA chinoise : cadeau ou
piège ? ». **Prochaine étape si on avance sur cet objectif** : partir de
cette maquette pour la Phase 1 de `docs/strategie-papier.md` (PDF hebdo
freemium, réservé aux abonnés newsletter), pas repartir d'une page
blanche.
