# Scénario en version papier — avis et stratégie

Note de cadrage rédigée en réponse à la question : « est-ce une bonne idée de
décliner Scénario en version papier, et si oui, avec quelle stratégie ? »

## Réponse courte

Oui, mais pas au sens d'un journal imprimé quotidien. Un objet papier a du
sens pour Scénario — à condition de partir d'un format hebdomadaire déjà
existant, de cibler d'abord le public déjà identifié (lycéens/profs), et de
tester gratuitement avant d'envisager un objet payant. Un quotidien papier
serait, en revanche, une mauvaise idée pour ce projet, pour des raisons
structurelles détaillées ci-dessous.

## Pourquoi pas un quotidien papier

- **Portage solo.** Scénario tourne aujourd'hui sur un pipeline d'édition
  quotidien piloté par une seule personne, avec l'appui de l'IA pour la
  recherche et la rédaction (cf. `docs/routine-pub-prompt.md`,
  `docs/routine-hebdo-prompt.md`). Ajouter une mise en page, une impression et
  une diffusion physique quotidiennes multiplie la charge opérationnelle sans
  aide supplémentaire en vue.
- **Le mécanisme central du projet est la réévaluation, pas la fixité.** La
  promesse de Scénario (cf. `le-projet.html`, section « Le suivi ») est que
  « une probabilité, ça se réévalue » : les pages de suivi mettent à jour un
  sujet quand l'actualité bouge. Un papier imprimé fige une estimation au jour
  J — il va structurellement à l'encontre de ce qui différencie le projet.
- **Aucune infrastructure de diffusion physique existante.** Pas de kiosque,
  pas d'abonnement postal, pas de budget impression — le lancer d'un coup
  serait un pari coûteux et non testé.

## Pourquoi un « papier » ponctuel a, lui, du sens

- **Le format hebdo existe déjà.** La section `hebdo/` compile chaque semaine
  les éditions publiées — c'est une synthèse déjà « figée » par nature, donc
  un candidat naturel à l'export imprimable, sans rien changer au
  fonctionnement quotidien.
- **Le public cible est déjà défini et colle au format papier.** La section
  « Pour qui » de `le-projet.html` cite explicitement les lycéens, étudiants
  (HGGSP, SES) et leurs professeurs — un public qui, en classe, utilise
  encore beaucoup de supports imprimables/projetables. C'est un usage réel,
  pas une nostalgie du papier.
- **L'identité visuelle évoque déjà le papier.** La charte du site utilise un
  jeton `--paper: #ece7da` (ton crème) comme couleur de texte principale sur
  fond sombre — la déclinaison imprimée n'est pas une rupture graphique.
- **Le modèle financier actuel est fragile.** Scénario ne vit d'aucune
  publicité ni d'aucun partenariat (cf. `le-projet.html`), uniquement d'un don
  libre via Buy Me a Coffee. Un objet papier premium (payant, à la demande)
  serait le premier vrai levier de revenu récurrent, sans toucher à la
  gratuité de l'édition quotidienne — ligne éditoriale à préserver.

## Stratégie proposée (par étapes, risque croissant)

**Phase 0 — Cadrage (objectif du papier)**
Trancher en amont si le papier sert d'abord la notoriété/pédagogie ou d'abord
un revenu. Les deux sont compatibles, mais l'ordre des priorités change la
conception du premier jet.

**Phase 1 — PDF hebdo imprimable, gratuit**
Transformer l'édition hebdo existante en PDF sobre (1–2 pages, charte
`--paper`/`--ink`/`--gold`), diffusé gratuitement sur les canaux déjà en
place (Telegram, LinkedIn, newsletter), avec un appel explicite aux
enseignants HGGSP/SES déjà identifiés comme public cible. Mesurer :
téléchargements, retours spontanés, demandes de profs.

**Phase 2 — Kit pédagogique**
Si la Phase 1 accroche : une fiche imprimable par sujet (3 scénarios +
questions de réflexion pour la classe), coconçue avec 2–3 profs volontaires
qui testent en vrai. Rester gratuit à ce stade — l'objectif est la
légitimité et la base d'utilisateurs, pas encore le revenu.

**Phase 3 — Objet imprimé payant**
Si la demande est confirmée : pas un quotidien, mais un objet trimestriel ou
annuel (« Cahier Scénario ») qui reprend les scénarios majeurs de la période
et boucle la promesse de suivi en revenant sur ce qui s'est réellement passé.
Impression à la demande (aucun stock à avancer), vendu en précommande,
ciblant écoles/lycées en priorité et lecteurs engagés en second. C'est le
premier flux de revenu récurrent au-delà du don libre.

## Repères de coûts (indicatif)

- **Devis Gelato**, brochure cousue ~40 pages (format papier discuté pour un
  cahier mensuel) : coût d'impression unitaire **≈ 7,55 € HT en tarif promo,
  sinon ≈ 11 € HT hors promo**. Hors frais d'expédition, hors marge de vente.
  À reconfirmer une fois le nombre de pages et le tirage réellement arrêtés
  (ce chiffre ne vaut que pour la fourchette ~40 pages évoquée en Phase 3) —
  noté ici comme ordre de grandeur, pas comme devis final.

## À éviter

- Lancer un objet payant avant d'avoir testé gratuitement la demande.
- Sous-traiter la mise en page/rédaction du papier à un tiers sans garder la
  main éditoriale — la rigueur des sources est l'actif principal du projet.
- Tout format qui fige une probabilité sans le lien vers la page de suivi
  correspondante : le papier doit renvoyer vers le numérique pour rester
  cohérent avec la promesse de réévaluation.
