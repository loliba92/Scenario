# Scénario en version papier — avis et stratégie

Note de cadrage rédigée en réponse à la question : « est-ce une bonne idée de
décliner Scénario en version papier, et si oui, avec quelle stratégie ? »

## Réponse courte

Oui, mais pas au sens d'un journal imprimé quotidien. Un objet papier a du
sens pour Scénario — à condition de partir d'un format hebdomadaire déjà
existant, de cibler d'abord le public déjà identifié (lycéens/profs), et de
tester gratuitement avant d'envisager un objet payant. Un quotidien papier
serait, en revanche, une mauvaise idée pour ce projet, pour des raisons
structurelles détaillées ci-dessous. **Cadence retenue pour l'objet payant,
si on y arrive (Phase 3) : trimestriel** (arbitré le 17 août) plutôt que
mensuel — voir le détail plus bas.

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

**Phase 0 — Cadrage (objectif du papier) — tranché le 17 août**
Le papier sert d'abord la **notoriété/développement de la marque**, pas le
revenu — le revenu (Phase 3) ne vient qu'une fois la base d'abonnés et la
légitimité construites. Conséquence directe sur la Phase 1 : ne pas
brûler la Phase 1 sur un simple test d'appétence, en faire un vrai levier de
croissance de la marque.

**Phase 1 — PDF hebdo, en freemium (pas en libre accès) — précisé le 17
août**
Transformer l'édition hebdo existante en PDF sobre (1–2 pages, charte
`--paper`/`--ink`/`--gold`), mais **réservé aux abonnés** — pas de
téléchargement public sans friction. L'inscription utilise l'infrastructure
déjà en place (formulaire newsletter Buttondown sur `newsletter.html`,
« 100 % gratuit, sans engagement ») : rester abonné à la lettre gratuite est
la seule condition pour recevoir le PDF, aucun nouvel outil à mettre en
place. Diffusion de l'appel sur les canaux déjà actifs (Telegram, LinkedIn),
avec un appel explicite aux enseignants HGGSP/SES déjà identifiés comme
public cible.

Ce choix sert directement l'objectif de marque tranché en Phase 0 : chaque
téléchargement de PDF devient une **inscription qualifiée** à la base
d'abonnés (l'actif qui sera réutilisé en Phase 3 pour vendre le Cahier
payant), pas juste un fichier diffusé dans le vide. Mesurer : nombre
d'inscriptions générées par l'appel PDF (pas juste des téléchargements),
taux de rétention de ces nouveaux abonnés, retours spontanés et demandes de
profs.

**Phase 2 — Kit pédagogique**
Si la Phase 1 accroche : une fiche imprimable par sujet (3 scénarios +
questions de réflexion pour la classe), coconçue avec 2–3 profs volontaires
qui testent en vrai. Rester gratuit à ce stade — l'objectif est la
légitimité et la base d'utilisateurs, pas encore le revenu.

**Phase 3 — Objet imprimé payant**
Si la demande est confirmée : pas un quotidien, mais un objet — **cadence
trimestriel arbitrée le 17 août** (plutôt que mensuel ou annuel) — « Cahier
Scénario » qui reprend les scénarios majeurs de la période et boucle la
promesse de suivi en revenant sur ce qui s'est réellement passé. Impression
à la demande (aucun stock à avancer), vendu en précommande/abonnement,
ciblant écoles/lycées en priorité et lecteurs engagés en second. C'est le
premier flux de revenu récurrent au-delà du don libre.

Le trimestriel a été préféré au mensuel pour une raison d'économie
d'expédition : sur un objet aussi léger (~40 pages), le port pèse presque
autant que l'impression, quelle que soit la quantité de contenu dans
l'enveloppe — grouper 3 mois de contenu (~100-120 pages) en un seul envoi
répartit ce coût fixe sur davantage de pages, au lieu de le payer 3 fois. Ça
correspond aussi mieux au rythme d'un lycée (période scolaire) qu'un envoi
mensuel.

**Prix indicatif retenu** (à confirmer une fois un vrai devis d'expédition
obtenu — voir « Repères de coûts » ci-dessous) : **12-15 € TTC le numéro,
~45-55 €/an en abonnement** pour un lecteur individuel ; tarif dégressif à
l'unité pour les commandes groupées lycée/CDI (meilleure économie
d'expédition sur un envoi groupé à une seule adresse).

**Brique technique — automatisation maison écartée, décision du 17 août.**
Le montage Steady/Stripe + Make.com + API Gelato/Pumbo envisagé plus haut
est abandonné en tant que solution **construite et maintenue par
l'utilisateur** : un bug de RPA sur le pipeline éditorial retarde au pire
une édition, alors qu'un bug sur ce pipeline-ci touche des abonnés qui ont
payé (mauvaise adresse, numéro non envoyé, double prélèvement) — un niveau
de risque opérationnel différent, à ne pas faire porter en solo sur une
automatisation maison. **Décision : déléguer** la chaîne abonnement +
impression + envoi à un prestataire externe plutôt que la construire et la
faire tourner soi-même. Deux pistes à évaluer avant de lancer la Phase 3 :

- **Un routeur/prestataire de fulfillment presse** (agence spécialisée
  abonnement + impression + mise sous pli + envoi, modèle courant pour la
  presse indépendante française) : on leur fournit le PDF chaque trimestre
  et la liste d'abonnés, ils gèrent l'impression et l'expédition de bout en
  bout — coût par exemplaire plus élevé qu'en DIY, mais aucune
  automatisation à maintenir.
- **Une plateforme d'abonnement avec intégration impression déjà
  maintenue par l'éditeur** (ex. Shopify + application officielle Gelato,
  plutôt qu'un scénario Make.com construit à la main) : réduit le risque en
  s'appuyant sur une intégration entretenue par un tiers plutôt qu'une
  automatisation propriétaire, sans aller jusqu'à un routeur complet.

**Risque de péremption des sujets sur 3 mois — soulevé le 17 août.** Un
sujet traité en semaine 1 du trimestre peut être tranché (ou dépassé) au
moment où le lecteur reçoit le cahier en semaine 12-13. Deux cas, deux
traitements :

- **Sujet résolu pendant le trimestre** : ce n'est pas un problème, c'est le
  format voulu — le cahier revient dessus en rétrospective (« voici les 3
  scénarios posés, voici ce qui s'est réellement passé »), qui boucle la
  promesse de suivi et sert d'argument de calibration/transparence.
- **Sujet encore ouvert en fin de trimestre** : ne jamais réimprimer les
  probabilités du jour de publication d'origine si elles sont datées de
  plusieurs semaines — reprendre la **dernière version réévaluée** (page de
  suivi) au moment du bouclage. Un sujet resté ouvert et jamais réévalué
  depuis sa publication d'origine est **écarté de la sélection finale**
  plutôt que republié avec une exactitude qu'on n'a plus — même exigence que
  celle déjà affichée sur le site (« jamais prétendre à une exactitude
  qu'aucune actualité en cours ne permet »).

**Conséquence sur le calendrier de fabrication** : la sélection des sujets
du numéro ne doit pas se figer au fil du trimestre, mais se faire dans les
**derniers jours avant l'envoi en impression** — un vrai bouclage de fin de
trimestre (comme un magazine classique), pas une compilation progressive
au fil de l'eau. Ça minimise le délai entre « dernière info connue » et
« réception par le lecteur ».

Conséquence sur le prix : la marge calculée plus haut (12-15 € TTC) supposait
une automatisation à coût quasi nul ; un prestataire de fulfillment prend
une commission ou un tarif au pli, à intégrer dans le prix final une fois un
devis obtenu — **à revoir avant de communiquer un prix définitif**.

## Focus thématique et identité « Les Cahiers de Scénario » — retour du 25 août 2026

**Question posée** : décliner le Cahier trimestriel avec un **focus thématique
tournant** (ex. un trimestre « Intelligence artificielle », un autre
« Sciences »...) plutôt qu'un simple compilateur chronologique toutes
rubriques confondues, avec de vraies photos pour en faire un objet éditorial
soigné.

**Avis retenu** : oui pour le focus thématique, mais **sans casser la cadence
trimestrielle déjà actée** (raison d'expédition — voir plus haut) ni la
diversité de lectorat. Formule proposée : chaque numéro met en avant **un
registre en fil rouge** (dossier principal + rétrospective) et garde 1-2
pages de consolidation pour les autres registres, pour ne pas perdre les
lecteurs qui ne suivent pas le registre du trimestre. Rythme de rotation
des registres (lequel en T1/T2/T3/T4) **pas encore tranché** — à faire une
fois la sélection de contenu du premier numéro cadrée (voir « Prochaine
étape » plus bas).

**Nom retenu pour l'objet** : **Les Cahiers de Scénario** (au pluriel,
collection) — remplace le nom de travail générique « Cahier Scénario » /
« Cahier trimestriel » utilisé plus haut dans ce document.

**Photos : Pexels, déjà en place, coût nul.** Pas de nouvel outil à
construire — `scripts/social/fetch_topic_image.py` (déjà utilisé pour les
visuels du site) sert de base : recherche par mots-clés thématiques
génériques, jamais de nom de personne réelle, choix humain systématique,
crédit photographe consigné. Licence Pexels compatible usage commercial/
impression, sans attribution obligatoire (mais fournie par bonne pratique).
Seul ajustement à prévoir le moment venu : exporter l'`original_url` en
haute résolution pour l'impression, plutôt que le recadrage carré
1080×1080 pensé pour Instagram.

**Maquette de validation** — deux planches A4 construites à partir d'un vrai
article déjà publié (« IA chinoise : cadeau ou piège ? », édition du 25 août
2026) et de sa photo Pexels déjà en place, sans rien inventer :
- **P.01 Couverture** — photo plein cadre (pas juste un bloc central),
  dégradé sombre progressif pour la lisibilité (assombri une deuxième fois
  le 25 août, retour utilisateur : le premier passage laissait le texte
  trop proche du bord clair de la photo — le noir descend maintenant plus
  tôt et devient opaque autour de 80 % de hauteur), titre + accroche + tags
  + **agenda numéroté et daté** (« Dans ce numéro ») ancré en bas de page.
  L'agenda liste les **vrais titres** des éditions déjà publiées dans ce
  registre thématique plutôt que des intitulés inventés pour remplir —
  voir point de volume ci-dessous.
- **P.02 Le dossier** — tient sur une seule page : image + texte + rail de
  statistiques + encart « Ce qu'on évalue » + les 3 scénarios chiffrés +
  **encart « L'essentiel » en bas**, qui reprend la synthèse déjà écrite
  pour l'édition originale. C'est ce bloc, avec son chiffre mis à jour
  (>60 % vs 45 % à la publication), qui joue le rôle de « mise à jour » du
  sujet sur une seule planche — pas une page de suivi séparée avec un
  historique V0/V1/V2 qui n'existe pas encore pour un sujet publié le jour
  même (une première tentative avait réutilisé une page de suivi existante
  sur un *autre* sujet, FIFA/Infantino, pour illustrer le mécanisme de
  rétrospective — écarté en retour utilisateur : casse la cohérence
  thématique du numéro).
- **Format retenu pour les encarts « Ce qu'on évalue » et « L'essentiel »**
  (validé le 25 août, après deux allers-retours) : **le même pour les
  deux** — fond `#ddd4bd` (dérivé du papier, discret) et bordure gauche or
  de 3px, jamais une boîte pleine bordure ni un fond encre/sombre. Un
  premier essai en fond encre (repris du site, où l'encart tranche sur un
  fond sombre) a été écarté : illisible/trop tranché sur une page papier
  claire. Un deuxième essai en ivoire clair dédié a aussi été écarté : trop
  jaune. La bonne réponse était plus simple — réutiliser tel quel le format
  déjà en place pour « Ce qu'on évalue » plutôt que d'en inventer un
  nouveau pour « L'essentiel ».
- Charte graphique = exactement celle du site (Fraunces/Inter/JetBrains
  Mono, `--ink`/`--paper`/`--gold`/`--favorable`/`--stable`/`--degrade`),
  aucune rupture graphique avec le digital.

**Règle éditoriale pour l'adaptation du texte au papier** (ajoutée le 25
août) : caser un article déjà écrit dans le gabarit A4 demande de couper
des phrases/paragraphes pour la place (voir P.02 ci-dessus) — **ne pas
trop retoucher le texte d'origine** (rester le plus proche possible des
phrases déjà écrites et validées pour l'édition digitale, pas une
réécriture), mais **toujours relire l'ensemble une fois les coupes faites**
pour vérifier que l'article coupé reste cohérent (pas de référence à une
phrase supprimée, pas de transition cassée entre deux paragraphes qui ne
se suivaient pas à l'origine). Une coupe individuellement correcte peut
rendre l'ensemble bancal une fois assemblé — la relecture porte sur
l'article complet, pas sur chaque coupe isolément.

**Exemple réel qui a motivé cette règle** (retour utilisateur, 25 août) :
le scénario « Dégradé » de P.02 mentionnait « le même schéma que Huawei et
la 5G il y a une décennie » — référence correcte dans l'article original,
où un paragraphe (coupé pour tenir sur une page) expliquait l'analogie.
Une fois ce paragraphe supprimé, la phrase restait dans la carte scénario
sans plus rien pour l'expliquer — incompréhensible pour qui n'a lu que le
papier. Corrigé en rendant la phrase autonome : « comme la 5G Huawei, qui
avait verrouillé des dizaines de pays avant que le risque ne soit mesuré »
— le contexte minimal nécessaire tient dans la phrase elle-même plutôt que
de dépendre d'un paragraphe qui a pu disparaître ailleurs sur la page.

Design **mis en pause ici, validé par l'utilisateur** — la suite n'est pas
un chantier visuel mais un chantier de **contenu** : voir « Prochaine
étape » ci-dessous.

**Prochaine étape (pas encore commencée)** : réfléchir à la sélection et à
la consolidation du contenu sur un trimestre entier, pas juste sur un seul
article de démonstration. Points à trancher :
- **Volume réel disponible — déjà mesuré le 25 août, pas juste théorique.**
  Scénario n'a qu'un mois d'existence : 37 éditions publiées au total, dont
  seulement **6 taguées « intelligence-artificielle »** (`archives.html`,
  `data-tag`) — pas encore les ~12-13/trimestre attendus en rythme de
  croisière (1 créneau/semaine par registre, voir `docs/tags.md`). La
  maquette de couverture assume cet écart plutôt que de le masquer :
  l'agenda affiche les 6 vrais titres avec une note explicite (« un
  trimestre complet en réunira une douzaine »). Point à retrancher une
  fois que le site aura tourné un trimestre plein : recompter, et
  rapprocher du gabarit ~100-120 pages visé en Phase 3 (compilation 3 mois
  toutes rubriques) pour voir combien de pages ça représente réellement
  une fois mis en forme (dossier + L'essentiel par sujet), et combien de
  place ça laisse aux 1-2 pages de consolidation des autres registres.
- **Critère de sélection/tri.** Tous les sujets du trimestre ne méritent pas
  forcément un dossier complet — sur quel critère trier (scénario tranché
  vs encore ouvert, richesse de la réévaluation, résonance déjà mesurée
  côté audience/réseaux) ?
- **Suivi au fil du trimestre plutôt qu'au bouclage.** Repérer les bons
  candidats de dossier au fur et à mesure des publications (liste courte
  tenue à jour) plutôt que de relire ~90 éditions à froid en fin de
  trimestre.
- **Sujets encore ouverts en fin de trimestre** : la règle déjà actée plus
  haut (reprendre la dernière version réévaluée, écarter si jamais
  réévalué depuis la publication d'origine) s'applique directement ici.
- **Ordre de rotation des registres** sur l'année (quel registre en fil
  rouge pour quel trimestre).

**État final de la maquette (session du 25 août, close ici pour la
soirée)** : https://claude.ai/code/artifact/d5e72207-faf4-4b9d-b0ed-24ccaa21e626
— 2 planches A4, nom « Les Cahiers de Scénario », toutes les décisions
ci-dessus appliquées. Design validé par l'utilisateur, **rien à reprendre
dessus par défaut** — ne pas relancer un travail visuel sans une demande
explicite. **Reprendre directement sur les 4 points de « Prochaine étape »
ci-dessus** (contenu, pas mise en page).



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
