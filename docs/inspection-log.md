# Journal de l'inspecteur

Une entrée par passage de la routine « Scénario — Inspecteur »
(`docs/routine-inspection-prompt.md`), même quand tout est conforme —
jamais de passage silencieux sans trace. La plus récente en tête.

---

## 2026-08-27 — Dette : le mur des 40 000 milliards
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 27 août
2026), CSS complet (`.essentiel-box`, `.stakes-box`, `.question-box`,
`.list-box`, `.comprendre-box` absente cette édition (pas de focus
« Comprendre » séparé, conforme), `.delta-france`/`.delta-gauge*`/
`.delta-word`/`.delta-flag` — bloc canonique intact, dégradé SVG à 3 stops
et `data-score="-0.60"` présents —, `.article-image*`, `.card`, `.gauge*`,
`.france-line` toutes présentes dans `<style>`), sync `index.html`/
`archives/2026-08-27.html` (seules différences : chemins relatifs `../`,
`canonical`/`og:url`/`mainEntityOfPage`, `aria-current` de nav — toutes
légitimes), `data-france-impact`/`data-kind` cohérents avec le texte
`.france-line` des 3 cartes (favorable/dégradé/dégradé, texte assorti) et
avec le `delta-france` (`data-kind="negatif"`, mot "assez négatif"),
incohérence numérique interne : aucune trouvée (taux à 30 ans 5,34 % pic du
19 août → 5,2 % fin août cohérent avec le KPI stable ≈5,2 %, KPI favorable
≈4,65 % cohérent avec le `.why` "4,6-4,7 %", KPI dégradé ≈5,8 % cohérent
avec le `.why` "5,5 %, voire 6 %", dette 40 000 Md$ répétée essentiel/dek
cohérente avec la base 40 100 Md$ des 3 cartes), probabilités
20+50+30=100 %, label brut favorable/stable/dégradé absent des 4
paragraphes `.essentiel-text` structurés (les 3 occurrences trouvées sont
dans le paragraphe `.delta-text`, qui nomme les 3 scénarios par leur
catégorie depuis au moins une semaine d'éditions consécutives — vérifié sur
les archives du 20 au 26 août, ce n'est pas le cas visé par ce point),
formulation "Notre évaluation de l'impact pour la France" intacte, lexique
(3 `.lex-ref` ↔ 3 entrées : prime-de-terme, rachat-de-dette,
bond-vigilantes, aucun terme orphelin), 2 KPI (taux à 30 ans, dette
fédérale fin 2027) distincts sur les 3 cartes deux à deux (aucun doublon
complet), image du jour (`assets/social/topic-images/2026-08-27.jpg` et
`-wide.jpg`, vrais JPEG 1080×1080/1600×900 confirmés par `file`, fiche de
provenance Pexels présente, `og:image`/`twitter:image`/JSON-LD pointant
vers le composite Instagram `assets/social/instagram/2026-08-27.png`, vrai
PNG 1080×1080 — comportement documenté dans `docs/ARCHITECTURE.md` et
observé chaque jour depuis le 22 août, pas une désynchronisation), style
des paragraphes `.dek`/`.why`/`.essentiel-text` (`grep` tutoiement hors
`.share-block` : 2 occurrences restantes toutes deux légitimement dans
`.share-block` — Telegram/notifications —, 1 dans un commentaire HTML non
rendu ; plusieurs phrases dépassent 40-50 mots, revues une à une, voir
"Réécritures de clarté" ci-dessous), 4 chiffres structurants vérifiés
contre les 4 sources déjà citées (5 `WebFetch` utilisés sur le plafond de
5, un deuxième passage sur PrimeRates pour préciser la date exacte).
**Corrigé automatiquement** : rien côté points 1 à 7, 9, 10 (aucune
anomalie mécanique trouvée) — seule la réécriture de clarté ci-dessous.
**Réécritures de clarté** (avant/après complet pour chacune) : 1 réécriture
(sur un plafond de 3) — seule phrase jugée réellement gênante parmi celles
qui dépassaient 40-50 mots, les autres restant lisibles malgré leur
longueur (structure en `soit/soit/soit` parallèle du `.dek`, asides entre
tirets, énumérations factuelles) :
- Avant : « **C'est le scénario le moins probable des trois** : il suppose
  à la fois un compromis budgétaire crédible au Congrès — rare en année
  pré-électorale — et une demande extérieure qui se rétablit alors qu'elle
  s'érode depuis plusieurs années ; plus optimiste que le stable, qui
  n'exige aucun de ces deux sursauts, et bien plus que le dégradé, qui part
  de la même fragilité sans réponse efficace. »
  Après : « **C'est le scénario le moins probable des trois** : il suppose
  à la fois un compromis budgétaire crédible au Congrès — rare en année
  pré-électorale — et une demande extérieure qui se rétablit, alors qu'elle
  s'érode depuis plusieurs années. Il reste plus optimiste que le stable,
  qui n'exige aucun de ces deux sursauts, et plus encore que le dégradé,
  qui part de la même fragilité sans réponse efficace. »
  (scission au point-virgule en deux phrases, aucun chiffre/date/nom propre
  concerné dans ce passage — seule la syntaxe change ; appliquée à
  l'identique sur `index.html` et `archives/2026-08-27.html`, vérifiée
  balisage équilibré + sync avant commit.)
**Signalé pour revue humaine** :
- Le chiffre « la dette de tous les pays du monde réunis dépasse
  310 000 milliards de dollars — environ 95 % du PIB de la planète »
  (`.dek`) semble mélanger deux périmètres différents : la source IMF citée
  en premier (Moniteur des finances publiques, avril 2026) confirme bien
  "94 % du PIB mondial en 2025 → 100 % dès 2029" (quasi identique au "95 %
  / 100 % dès 2029" de l'article, écart d'1 point négligeable) **mais ne
  fournit aucun montant en dollars** — le rapport IMF porte sur la dette
  publique (~94-95 % du PIB mondial, donc plutôt de l'ordre de
  100 000 milliards $ vu un PIB mondial ≈110 000 Md$), alors que
  « 310 000 milliards de dollars » correspond typiquement à la dette
  mondiale tous secteurs confondus (public + privé + entreprises, ~330 %
  du PIB selon les suivis usuels type IIF) — deux mesures différentes
  présentées comme équivalentes dans la même phrase. Le chiffre en dollars
  n'est pas vérifiable via la source IMF citée telle quelle ; possible
  confusion de périmètre à l'écriture, à trancher par la rédaction (pas
  une correction mécanique).
- Source OCDE (`oecd.org/.../global-debt-report-2026...`, citée pour "61
  000 milliards $ d'encours souverain en 2025" et "~4 000 milliards $ de
  besoins d'emprunt net en 2026") : HTTP 503 ce passage-ci — signalée comme
  "source non re-vérifiable", pas de recherche de remplacement.
- Source CNBC (`cnbc.com/.../treasury-announces-upscaled-buyback-operation
  -for-longer-term-debt...`, citée pour "rachats de dette longue du Trésor,
  au moins 4 milliards $ par opération, mi-août") : HTTP 403 ce passage-ci
  (probable blocage anti-bot, même schéma que CNEWS le 26 août) — signalée
  comme "source non re-vérifiable".
- Chiffre confirmé sans réserve : « dette fédérale des États-Unis vient de
  franchir les 40 000 milliards de dollars » — source PrimeRates montre
  39 890 Md$ au 7 août 2026, en hausse d'environ 7,2 Md$/jour ; extrapolé
  sur les 20 jours suivants jusqu'au 27 août, ça donne ≈ 40 030 Md$ —
  cohérent avec le franchissement du seuil annoncé par l'article à la date
  de publication, aucune correction nécessaire.

## 2026-08-26 — Retraites : la patate chaude de 2027
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 26 août
2026), CSS complet (`.essentiel-box`, `.stakes-box`, `.question-box`,
`.list-box`, `.comprendre-box`, `.delta-france`/`.delta-gauge*`/
`.delta-word`/`.delta-flag` — bloc canonique intact — `.article-image*`,
`.card`, `.gauge*`, `.france-line` toutes présentes dans `<style>`),
sync `index.html`/`archives/2026-08-26.html` (seules différences : chemins
relatifs `../`, `canonical`/`og:url`, `aria-current` de nav — toutes
légitimes), `data-france-impact`/`data-kind` cohérents avec le texte
`.france-line` des 3 cartes, incohérences numériques internes (déficit COR
2,4 %/1,4 %, désindexation 1,5/3/6 Md€ répétés dek/why/essentiel-text/KPI —
tous cohérents entre eux), probabilités 20+50+30=100 %, label brut
favorable/stable/dégradé absent de `.essentiel-text`, formulation "Notre
évaluation de l'impact pour la France" intacte, lexique (3 `.lex-ref` ↔ 3
entrées, aucun terme orphelin), 2 KPI (`déficit du système`, `économies de
la désindexation`) distincts sur les 3 cartes deux à deux (aucun doublon
complet), image du jour (`assets/social/topic-images/2026-08-26.jpg` et
`-wide.jpg`, vrais JPEG 1080×1080/1600×900, fiche de provenance Pexels
présente, `og:image`/`twitter:image`/JSON-LD pointant vers le composite
Instagram `assets/social/instagram/2026-08-26.png` — comportement documenté
dans `docs/ARCHITECTURE.md`, pas une désynchronisation), style des
paragraphes `.dek`/`.why`/`.essentiel-text` (plusieurs phrases dépassent 40
mots mais restent lisibles — énumérations parallèles ou éléments factuels
enchaînés, sans rupture de registre — `grep` tutoiement hors `.share-block`
: rien trouvé), 4 chiffres/faits vérifiés contre les sources déjà citées
(3 fetchées avec succès sur 4, plafond de 5 `WebFetch` atteint).
**Corrigé automatiquement** : rien.
**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
aucune — aucune phrase jugée assez gênante pour justifier une réécriture
malgré plusieurs phrases longues (voir "Vérifié" ci-dessus).
**Signalé pour revue humaine** :
- Le chiffre-clé « déficit du système de retraites à 2,4 % du PIB en 2070,
  contre 1,4 % un an plus tôt (COR, 3 août 2026) », repris dans `.dek`, les
  3 `.why` et `.essentiel-text`, ne se retrouve dans aucune des 4 sources
  citées en bas de page — vérifié spécifiquement sur MoneyVox (l'article le
  plus proche du sujet retraites/rentrée politique), qui ne contient ni le
  chiffre ni la date du 3 août 2026. Les 2 chiffres n'apparaissent pas non
  plus dans LCP (positions des candidats) ni Orange Actu (désindexation).
  Le chiffre est plausible (cohérent avec les rapports COR connus) mais
  n'est pas re-vérifiable depuis les 4 sources listées telles quelles —
  probablement une source COR primaire non ajoutée à la liste. À vérifier
  par la rédaction, ou ajouter la source COR directe à la section
  `sources`.
- La source CNEWS (`cnews.fr/.../ce-que-lon-sait-deja-sur-le-premier-
  debat-...`) renvoie HTTP 403 depuis cet environnement — source non
  re-vérifiable ce passage-ci (pas nécessairement un lien mort côté site,
  peut-être un blocage anti-bot). Le fait qu'elle appuie (date du débat du
  27 août face au Medef) n'a donc pas pu être confirmé.
- Chiffres confirmés sans réserve : les 3 montants de désindexation (1,5 /
  3 / 6 Md€ selon le seuil retenu, 2 000-3 000 €) correspondent exactement
  à l'article Orange Actu cité, y compris le taux d'inflation de 2 % pris
  pour hypothèse sur le scénario du gel total. Positions des candidats
  (Mélenchon 60 ans, Retailleau 65 ans, Attal suppression de l'âge légal)
  confirmées par LCP ; nuance mineure non bloquante sur Philippe (LCP ne
  confirme explicitement que 67 ans, l'article évoque "66 ou 67 ans") et
  sur Le Pen (LCP mentionne aussi 60 ans comme position possible, en plus
  des 62 ans repris dans l'article) — écarts trop mineurs pour être
  qualifiés d'erreur factuelle, mentionnés ici par transparence.

---

## 2026-08-25 — IA chinoise : cadeau ou piège ?
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 25 août
2026), classes CSS attendues présentes dans `<style>` et utilisées dans le
corps (dont `.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag`,
bloc canonique intact), sync `index.html` vs `archives/2026-08-25.html`
(`diff` normalisé — seuls écarts : chemins `../`, `canonical`/`og:url`,
`aria-current`, tous légitimes), `data-france-impact`/`data-kind` cohérents
avec le texte `.france-line` adjacent sur les 3 cartes, probabilités
20+45+35 = 100 %, label brut favorable/stable/dégradé absent de
`.essentiel-text`, formulation « Notre évaluation de l'impact pour la
France » intacte, lexique (3 `.lex-ref` ↔ 3 entrées, `distillation` /
`poids-ouverts` / `verrouillage-technologique`, aucun terme orphelin dans
un sens ou l'autre), absence de tutoiement hors `.share-block` (une seule
occurrence de "ton" trouvée, dans un commentaire HTML de développement, pas
dans du texte lecteur), KPI des 3 cartes (point 10 : paires `.evo-current`
distinctes sur les 2 indicateurs — 40 %/45 %, 58 %/60 %, 70 %/68 % — aucun
doublon complet), image de l'article et du feed (`topic-images/2026-08-
25.jpg` 1080×1080 et `-wide.jpg` 1600×900, formats JPEG réels conformes à
l'extension, `og:image`/`twitter:image`/JSON-LD cohérents entre eux et
identiques entre `index.html` et l'archive — pointent vers
`assets/social/instagram/2026-08-25.png`, PNG réel 1080×1080 conforme,
comportement cohérent avec `docs/ARCHITECTURE.md` même si ça diffère du
chemin `topic-images/*.jpg` décrit au point 9 du prompt — rien de cassé,
pas traité comme une anomalie), 3 chiffres structurants vérifiés contre
sources déjà citées (voir détail ci-dessous).
**Corrigé automatiquement** : 3 réécritures de clarté (plafond du point 8
atteint, voir détail ci-dessous) sur `index.html` et
`archives/2026-08-25.html` — aucune autre correction mécanique nécessaire
ce passage-ci (rien à corriger sur les points 1 à 7, 9, 10).
**Réécritures de clarté** (avant/après complet pour chacune) :
- Avant : « Pour la Chine, rendre ses modèles gratuits et ouverts est une
  stratégie assumée : plus un modèle chinois devient la base sur laquelle
  les développeurs du monde entier construisent leurs propres outils, plus
  la Chine gagne en influence sur les standards techniques de demain — un
  peu comme les équipements 5G bon marché de Huawei avaient permis à la
  Chine de s'installer dans les réseaux télécoms de dizaines de pays avant
  que les gouvernements occidentaux n'en mesurent le risque de
  verrouillage technologique. »
  Après : « Pour la Chine, rendre ses modèles gratuits et ouverts est une
  stratégie assumée : plus un modèle chinois devient la base sur laquelle
  les développeurs du monde entier construisent leurs propres outils, plus
  la Chine gagne en influence sur les standards techniques de demain. C'est
  le même mécanisme qu'avec les équipements 5G bon marché de Huawei : ils
  avaient permis à la Chine de s'installer dans les réseaux télécoms de
  dizaines de pays, avant même que les gouvernements occidentaux n'en
  mesurent le risque de verrouillage technologique. »
- Avant : « La tension est montée d'un cran le 22 juillet, quand Michael
  Kratsios, le conseiller scientifique et technologique de la Maison-
  Blanche, a accusé la start-up chinoise Moonshot AI d'avoir siphonné en
  secret les réponses du modèle Fable d'Anthropic pour construire Kimi K3,
  son propre modèle en poids ouverts publié six jours plus tôt. »
  Après : « La tension est montée d'un cran le 22 juillet. Ce jour-là,
  Michael Kratsios, le conseiller scientifique et technologique de la
  Maison-Blanche, a accusé la start-up chinoise Moonshot AI d'avoir
  siphonné en secret les réponses du modèle Fable d'Anthropic pour
  construire Kimi K3, son propre modèle en poids ouverts publié six jours
  plus tôt. »
- Avant : « La dépendance s'accélère plutôt qu'elle ne se stabilise : de
  plus en plus d'outils de développement et de services cloud occidentaux
  sont construits directement sur des modèles chinois, rendant un retour
  en arrière coûteux et lent — le même schéma que les équipements télécoms
  Huawei il y a une décennie. »
  Après : « La dépendance s'accélère plutôt qu'elle ne se stabilise : de
  plus en plus d'outils de développement et de services cloud occidentaux
  sont construits directement sur des modèles chinois. Un retour en
  arrière devient coûteux et lent — le même schéma que les équipements
  télécoms Huawei il y a une décennie. »
**Signalé pour revue humaine** :
- Incohérence numérique potentielle, périmètre/date ambigus (point 4) :
  la somme des parts individuelles des 6 labos chinois listés dans le
  `.list-box` (Xiaomi 21,1 % + Alibaba 13,9 % + MiniMax 8,1 % + Zhipu 5,6 %
  + DeepSeek 5,6 % + StepFun 5,3 % = 59,6 %) dépasse largement le chiffre
  « 45 % » utilisé ailleurs dans l'article comme part chinoise totale du
  trafic mondial, y compris dans `.essentiel-text` où il est présenté avec
  le mot « désormais » (laissant entendre une valeur actuelle). Vérification
  faite auprès de la source citée (Digital Applied, Q2 2026, seule source
  couvrant ces chiffres) : les deux chiffres sont réels et proviennent bien
  de cette source, mais le rapport lui-même précise que « Chinese share
  crossed 45% of OpenRouter traffic » (un seuil franchi, cohérent avec la
  date « avril 2026 » explicitement donnée dans le `.dek`), tandis que la
  répartition par labo vient du rapport Q2 2026 dans son ensemble — donc
  potentiellement plus récente, ce qui expliquerait une somme déjà
  supérieure. Le `.list-box-foot` de l'article reste littéralement exact
  (« plus de 45 % ») mais `.essentiel-text` (« désormais 45 % ») entre en
  tension avec sa propre répartition détaillée plus haut dans le même
  article. Périmètre temporel exact non tranchable depuis cet inspecteur —
  ne pas corriger seul, à trancher par la rédaction (reformuler
  « désormais » en « en avril 2026 », ou mettre à jour l'agrégat, selon ce
  que confirme la source complète).
- Source « CNBC — Nvidia, Microsoft, Meta warn against 'premature
  restrictions' of open-weight models » non re-vérifiable ce passage-ci :
  `WebFetch` renvoie HTTP 403 Forbidden (blocage probable côté CNBC, pas
  une politique réseau de la session — à la différence des blocages
  `EGRESS_BLOCKED` rencontrés lors de passages précédents sur d'autres
  domaines). Le chiffre qu'elle est censée appuyer (plus de 25 entreprises,
  dont Mistral, signataires d'une lettre commune à Washington fin juillet)
  n'a donc pas pu être confirmé ce passage-ci ; pas de source de
  remplacement cherchée, à revérifier lors d'un prochain passage.

---

## 2026-08-24 — Ukraine : ni paix ni victoire
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 24 août
2026), classes CSS attendues présentes dans `<style>` (dont
`.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag` — bloc canonique
intact au caractère près, structure SVG dégradé 3 stops + `data-score`
complète), sync `index.html` vs `archives/2026-08-24.html` (`diff` complet
— seul écart : `mainEntityOfPage` JSON-LD, légitime comme `canonical`/
`og:url`), `data-france-impact`/`data-kind` cohérents avec le texte
`.france-line` adjacent pour les 3 cartes (favorable/défavorable/
défavorable), probabilités 20+45+35=100 %, label brut favorable/stable/
dégradé absent de `.essentiel-text` (les occurrences de "stable"/"dégradé"/
"favorable" qui y apparaissent nomment les scénarios eux-mêmes, pas une
description brute de l'impact France), formulation "Notre évaluation de
l'impact pour la France" intacte (page et `feed.xml`), lexique (2
`.lex-ref` ↔ 2 entrées, aucun terme orphelin dans un sens ou l'autre),
absence de rupture de registre (`grep '\bton \|\bta \|\btu \b'` : seules
occurrences dans `.share-block`, légitimes), cohérence numérique interne
(missiles 376/288/192, territoire russe 19 % de référence sur les 3
cartes, 15/50 ans repris à l'identique dek↔scénario favorable — aucune
incohérence du type point 4), les 2 indicateurs `.evo-current` des 3
cartes (missiles, territoire) tous distincts deux à deux (pas de doublon
complet, point 10), image de l'édition (`assets/social/topic-images/
2026-08-24.jpg` 1080×1080 et `-wide.jpg` 1600×900, `file` confirme un vrai
JPEG sous les deux extensions, références `og:image`/`twitter:image`/
JSON-LD `image`/`<figure class="article-image">` cohérentes entre
`index.html`, l'archive et `feed.xml` — voir note ci-dessous), 4 chiffres
vérifiés contre les 3 sources ouvertes (missiles 376/288/192 et 745 km²
Dnipropetrovsk via Al Jazeera, 57 % d'Ukrainiens opposés à céder le Donbas
via The Moscow Times — voir signalement pour les 15/50 ans).
**Note (pas un signalement, pour info)** : `docs/routine-inspection-
prompt.md` (point 9) décrit `assets/social/topic-images/{date}.jpg` comme
la source d'`og:image`/`twitter:image`/JSON-LD `image` — en pratique,
depuis le 9-10 août (`docs/ARCHITECTURE.md`), ces meta pointent vers
l'image composite `assets/social/instagram/{date}.png` (photo + titre +
scénarios incrustés), qui est bien reproduite/cohérente sur les 3 fichiers
ce jour. Rien à corriger sur le site, juste un écart de formulation entre
le prompt de la routine et l'architecture actuelle, à corriger dans
`docs/routine-inspection-prompt.md` lui-même à l'occasion (hors périmètre
de ce passage, qui ne touche que le contenu de l'édition).
**Corrigé automatiquement** : rien — aucune anomalie mécanique détectée
sur les points 1 à 10.
**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
aucune. 4 phrases de plus de 40-50 mots repérées dans `.dek`/`.why`/
`.essentiel-text` mais aucune jugée réellement gênante pour la
compréhension (structure claire par deux-points/tirets/énumération
parallèle "soit... soit... soit...", tous les termes techniques déjà
couverts par un `.lex-ref`, aucune rupture de registre) ; l'une d'elles
("Les pourparlers menés par Washington butent...") est de toute façon dans
le paragraphe "contexte" protégé de `.essentiel-text`, jamais retouché.
**Signalé pour revue humaine** : la durée des garanties de sécurité citée
dans le `.dek` et le scénario favorable ("quinze ans... quand Kyiv en
réclame jusqu'à cinquante", "au-delà des quinze ans initialement
proposés") n'a été retrouvée dans aucune des 3 sources ouvertes, y compris
l'article Kyiv Independent dédié précisément aux garanties de sécurité
(vérifié deux fois avec des prompts différents) — plafond de 5 `WebFetch`
atteint avant d'avoir pu confirmer ce chiffre ailleurs ; à revérifier si
la source exacte est retrouvée. Secondaire : le chiffre "745 km²" repris
sans réserve dans le `.dek` est bien celui cité par Al Jazeera, mais cet
article précise que c'est une revendication ukrainienne, l'ISW l'évaluant
plus prudemment à 627 km² — pas une erreur de chiffre à proprement parler
(745 est bien dans la source), mais à garder en tête si la rédaction
souhaite nuancer.

---

## 2026-08-23 — Le pari XXL du Mondial 2030
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 23 août
2026), classes CSS attendues présentes dans `<style>` (dont
`.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag` — bloc comparé
caractère pour caractère à la version canonique de
`docs/routine-inspection-prompt.md`, identique — et structure HTML du
dégradé SVG à 3 stops + `data-score` intacte, `.comprendre-box*` bien
présente dans `<style>` bien qu'utilisée cette édition-ci pour le focus
« Comprendre »), sync `index.html` vs `archives/2026-08-23.html` (`diff`
complet — seuls écarts : `og:url`/`mainEntityOfPage` selon canonical/
archive, légitimes), `data-france-impact`/`data-kind` cohérents avec le
texte `.france-line` adjacent sur les 3 cartes (favorable/favorable/
dégradé, tous alignés avec « Plutôt favorable »/« Plutôt défavorable pour
la France » du texte adjacent) et avec `.delta-word` (« léger positif »
cohérent avec `data-kind="positif"`), probabilités 20+45+35=100 %,
incohérences numériques internes (48/64 équipes, 104/128 matchs, dates 14
août/11 septembre — cohérents à chaque occurrence, même fait même
périmètre), label brut favorable/stable/dégradé absent de
`.essentiel-text` proprement dit (les occurrences « favorable et stable »
dans `.delta-text` sont des références aux cartes, motif déjà rencontré
les jours précédents), formulation « Notre évaluation de l'impact pour la
France » intacte, lexique (4 `.lex-ref` ↔ 4 entrées, aucun terme
orphelin), rupture de registre (`grep '\bton \|\bta \|\btu \b'` — 2
occurrences, toutes deux dans `.share-block`, exception légitime), style
des paragraphes `.dek`/`.why`/`.essentiel-text` (lecture des phrases de
plus de 40 mots, voir réécritures ci-dessous), 4 chiffres/faits
structurants vérifiés contre 3 des 4 sources citées (voir ci-dessous),
KPI projetés des 3 cartes (point 10, ajouté en cours de journée — voir
ci-dessous).

**Point 10 (KPI projetés dupliqués, ajouté en cours de journée du 23 août
— voir commit `c633a3b`, prompt relu après coup pour ne pas laisser ce
point de côté)** : `.evo-current` extraits des 3 cartes — carte 1
(compromis, 20 %) : 64 équipes / 128 matchs ; carte 2 (stable, 45 %) : 48
équipes / 104 matchs ; carte 3 (dégradé, 35 %) : 64 équipes / 128 matchs.
Doublon **complet** entre les cartes 1 et 3 sur les deux indicateurs à la
fois — le cas mécanique que ce point est censé détecter. **Pas de
correction appliquée** : le scénario dupliqué le moins probable des deux
est la carte 1 (compromis, 20 %), mais son KPI ne peut pas être ajusté
sans casser le fait qu'elle décrit elle-même — « un compromis à **64
équipes** » n'a pas de sens avec un autre chiffre que 64, ce n'est pas une
valeur de modèle libre comme le quota/taux de reversement de l'exemple du
22 août. Aucun ajustement plausible ne se dégage donc naturellement.
**Corrigé une erreur de jugement du premier passage aujourd'hui** :
initialement classé "rien à signaler" au motif que le `.comprendre-box`
de l'article explique déjà ce chevauchement (« Deux des trois scénarios
de cette édition aboutissent exactement au même chiffre — 64 équipes, 128
matchs — [...] Ce qui change, c'est la méthode »). C'était trancher seul
sur un point que la règle demande explicitement de signaler dans ce cas
précis (« les 3 scénarios sont censés partager la même valeur de départ
pour une raison éditoriale légitime [...] ne pas trancher seul —
signaler »), même quand une explication légitime existe déjà dans
l'article — l'inspecteur n'a pas autorité pour décider que cette
explication suffit, seule une revue humaine peut confirmer que
l'indiscernabilité des deux cartes sur ce plan est acceptée en l'état ou
mériterait un ajustement éditorial (par exemple : donner à la carte
compromis un chiffre intermédiaire, si un format négocié pouvait
plausiblement retenir moins de 64 équipes ou une phase finale à moins de
128 matchs — un choix de contenu, pas mécanique). Voir "Signalé pour
revue humaine" ci-dessous.

**Point 9 (image)** : `topic-images/2026-08-23.jpg` (1080×1080) et
`-wide.jpg` (1600×900) présents, `file` confirme un vrai JPEG dans les
deux cas (pas de PNG renommé), dimensions correctes. `<figure
class="article-image">` pointe bien vers `-wide.jpg`, cohérent entre
`index.html` et l'archive. `og:image`/`twitter:image`/JSON-LD `"image"`
pointent vers `assets/social/instagram/2026-08-23.png` plutôt que vers
`topic-images/2026-08-23.jpg` — même motif déjà vérifié le 22 août (et
les jours précédents), les 3 métas cohérentes entre elles et avec l'`alt`
du `<figure>`. Rien à corriger.

**Réécritures de clarté** (avant/après complet pour chacune, ou
"aucune") :
aucune — plusieurs phrases dans `.dek`/`.why` dépassaient 40-50 mots
(listes parallèles à 3 éléments, structures « soit... ; soit... ; soit... »
ou comparatifs simples), mais aucune jugée assez gênante pour la
compréhension pour justifier une réécriture : ce sont des énumérations ou
des comparaisons à un seul niveau de subordination, pas des phrases à
plusieurs subordonnées imbriquées comme les cas déjà corrigés
précédemment (voir entrées antérieures). Le paragraphe `.essentiel-text`
de 60 mots fait partie des 3 dernières phrases de la structure
problématique/contexte/conclusion/signal — non éligible de toute façon.

**Vérification des chiffres contre les sources citées** (3 des 4 URLs de
la section Sources fetchées avec succès, 4 appels `WebFetch` sur le
plafond de 5) :
- Al Jazeera — *FIFA studying impact of expanding to 64 teams* : décision
  sur le choix de l'agence le 14 août, conclusions attendues le 11
  septembre 2026, format 2026 confirmé à 48 équipes/104 matchs — conforme
  à l'article.
- Foot Mercato (décision attendue le 14 août) : décision le 14 août,
  48→64 équipes pour 2030 — conforme.
- Foot Mercato (gros coup dur pour le projet) : opposition confirmée de
  l'UEFA et de l'AFC, réticence des trois pays hôtes (Espagne, Portugal,
  Maroc), origine CONMEBOL/Alejandro Domínguez pour le centenaire —
  conforme à l'article (l'opposition de la CONCACAF, citée dans
  l'article, n'est pas mentionnée par cette source précise, mais n'est
  pas non plus contredite — pas traité comme un écart).
- ESPN — *UEFA's Čeferin calls 64-team plan 'bad idea'* : page renvoyée
  vide par `WebFetch` (contenu non récupéré, probable blocage
  d'accès) — **signalée comme source non re-vérifiable**, pas de
  chiffre de cet article vérifié ce passage-ci.

Le nombre de matchs de la phase finale à 128 pour un format à 64 équipes
n'est confirmé explicitement par aucune des sources (elles confirment
seulement le format actuel à 104 matchs pour 48 équipes) — ce n'est pas
une contradiction, seulement une absence de confirmation externe
explicite d'un calcul éditorial plausible ; pas signalé comme écart.

**Signalé pour revue humaine** :
- Source ESPN non re-vérifiable ce passage-ci (voir ci-dessus) ; à
  retenter lors d'un prochain passage.
- **Point 10** : les cartes « compromis » (favorable, 20 %) et « 64
  équipes envers et contre tous » (dégradé, 35 %) affichent des KPI
  projetés strictement identiques (64 équipes / 128 matchs sur les deux
  indicateurs) — indiscernables sur ce plan, même si leur récit,
  probabilité et impact France (`.france-line`) diffèrent. L'article
  l'explique déjà lui-même dans son `.comprendre-box`, et aucun
  ajustement chiffré ne se dégage naturellement côté inspecteur (voir
  ci-dessus), donc pas de correction automatique — mais l'inspecteur n'a
  pas autorité pour décider seul que cette explication suffit à clore le
  sujet. À la rédaction de trancher si cette indiscernabilité est
  acceptable telle quelle ou mérite un chiffre distinct pour la carte
  compromis.

  **Résolu le 23 août, en conversation avec l'utilisateur** : le KPI
  identique est confirmé volontaire (format à 64 équipes défini par la
  proposition elle-même, indépendant de la méthode négociée/imposée) —
  pas de chiffre distinct à inventer. Décision : rendre le chevauchement
  visible directement au niveau du tableau d'indicateurs, pas seulement
  dans l'encart Comprendre plus haut. Une note (`.indicators-note`) a été
  ajoutée sous les indicateurs des cartes compromis et dégradé, sur
  `index.html` **et** `archives/2026-08-23.html` (commit `c632b7c`) :
  « Même chiffre que le scénario [dégradé/favorable] ci-dessous/ci-dessus
  — c'est la méthode qui les distingue, pas le format final (voir «
  Comprendre » plus haut). » Correction hors périmètre mécanique de
  l'inspecteur (touche à la présentation d'un choix éditorial), donc
  appliquée manuellement avec confirmation explicite de l'utilisateur,
  pas par la routine automatisée.

---

## 2026-08-22 — Hollywood décroche en Chine
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 22 août
2026), classes CSS attendues présentes dans `<style>` (dont
`.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag` — bloc comparé
caractère pour caractère à la version canonique de
`docs/routine-inspection-prompt.md`, identique — et structure HTML du
dégradé SVG à 3 stops + `data-score` intacte, `.comprendre-box*` absente
cette édition mais toujours dans `<style>` comme requis), sync
`index.html` vs `archives/2026-08-22.html` (`diff` complet, rejoué après
correctif — seuls écarts : chemins relatifs internes selon la profondeur
du fichier, `canonical`/`og:url`/`mainEntityOfPage`, `aria-current` nav —
tous légitimes), `data-france-impact`/`data-kind` cohérents avec le texte
`.france-line` adjacent sur les 3 cartes (favorable/favorable/dégradé,
tous alignés avec « Plutôt favorable »/« Plutôt défavorable pour la
France » du texte adjacent — le `data-kind="stable"` de la 2e carte avec
`data-france-impact="favorable"` n'est pas une incohérence, ce sont deux
axes distincts, probabilité du scénario vs. impact France), probabilités
30+45+25=100 %, incohérence numérique interne (40,6 % répété 3 fois pour
le même fait/périmètre — recul du box-office chinois au 1er semestre
2026 — cohérent à chaque occurrence ; les 6 occurrences de « 25 % »
désignent des faits différents — taux de reversement référence 2025,
probabilité du scénario dégradé, jauge de la carte — chacune cohérente
dans son propre contexte, pas une incohérence), label brut
favorable/stable/dégradé absent de `.essentiel-text` (les occurrences
« favorable et stable » dans `.delta-text` sont des références aux
cartes, motif déjà rencontré les jours précédents — voir entrées du 19 et
20 août), formulation « Notre évaluation de l'impact pour la France »
intacte, lexique (3 `.lex-ref` ↔ 3 entrées avant correctif, aucun terme
orphelin), rupture de registre (`grep '\bton \|\bta \|\btu \b'` — 2
occurrences, toutes deux dans `.share-block`, exception légitime),
style des paragraphes `.dek`/`.why`/`.essentiel-text` (lecture LLM des
phrases longues, voir réécritures ci-dessous), 3 chiffres/faits
structurants vérifiés contre 2 des 4 sources citées (voir ci-dessous).

**Point 9 (image)** : `topic-images/2026-08-22.jpg` (1080×1080) et
`-wide.jpg` (1600×900) présents, `file` confirme un vrai JPEG dans les
deux cas (pas de PNG renommé), dimensions correctes. `<figure
class="article-image">` pointe bien vers `-wide.jpg`, cohérent entre
`index.html` et l'archive. `og:image`/`twitter:image`/JSON-LD `"image"`
pointent vers `assets/social/instagram/2026-08-22.png` plutôt que vers
`topic-images/2026-08-22.jpg` — vérifié que ce n'est pas une
désynchronisation : les 3 métas sont cohérentes entre elles (même
fichier, dimensions déclarées 1080×1080 = dimensions réelles du PNG,
`og:image:alt` = `alt` du `<figure>`) et ce même motif (méta social sur
le PNG Instagram plutôt que le JPG topic-images malgré la présence des
deux fichiers) existe déjà sur plusieurs éditions précédentes (10-14
août), pas une anomalie propre à ce jour. Rien à corriger.

**Vérification des chiffres contre les sources citées** (2 des 4 URLs de
la section Sources fetchées, 4 appels `WebFetch` sur le plafond de 5) :
- ABC News — *China to limit number of American films imported* :
  quota de 34 films/an depuis 2015 (contre 20 auparavant) confirmé,
  droits de douane à 145 % confirmés, annonce de la National Film
  Administration de « réduire modérément » les importations confirmée
  (datée du 10 avril 2025 par la source, cohérent avec le « dès avril
  2025 » de l'article).
- CGTN (22 février) — *China becomes world's top box office market* :
  confirme que la Chine a dépassé l'Amérique du Nord au box-office
  cumulé le 22 février 2026, cohérent avec l'article.
- CGTN (21 août) — *40 Days, $1.5 billion box office* : **le chiffre de
  « 40,6 % » de recul du box-office chinois au 1er semestre 2026 (cité 3
  fois dans l'article — `.dek`, `.essentiel-text`, `.why` de la carte
  dégradée) n'apparaît nulle part dans cette source** — l'article cité
  ne parle que de records positifs (26,6 milliards de yuans cumulés au
  21 août, 10,9 milliards sur l'été), aucun pourcentage, aucune
  comparaison 2025/2026. Signalé ci-dessous, pas corrigé seul.

**Corrigé automatiquement** :
- 2 réécritures de clarté (sous le plafond de 3, voir détail ci-dessous),
  dont l'ajout d'une entrée de lexique (`tentpole`) pour un terme
  technique jusque-là non expliqué.

**Réécritures de clarté** (avant/après complet pour chacune) :
- Avant : « Le quota chinois reste fixé à 34 films américains à partage
  de recettes par an, comme depuis 2015, mais de moins en moins de
  studios utilisent ce créneau à plein : beaucoup de sorties américaines
  ordinaires, hors tentpole, restent boudées côté chinois ou snobées côté
  studio — un cadre de studio résumait la situation cet été en expliquant
  que sortir un film milieu de gamme en Chine ne rapporte tout simplement
  plus assez pour en valoir la peine. »
  Après : « Le quota chinois reste fixé à 34 films américains à partage
  de recettes par an, comme depuis 2015, mais de moins en moins de
  studios utilisent ce créneau à plein. Beaucoup de sorties américaines
  ordinaires, hors tentpole*, restent boudées côté chinois ou snobées
  côté studio — un cadre de studio résumait la situation cet été en
  expliquant que sortir un film milieu de gamme en Chine ne rapporte tout
  simplement plus assez pour en valoir la peine. »
  Phrase de 78 mots scindée en deux (le « : » reliait deux idées
  distinctes) ; « tentpole » (terme technique non expliqué) reçoit un
  `.lex-ref` vers une nouvelle entrée de lexique (« Tentpole ») plutôt que
  d'être retiré.
- Avant : « Le prochain vrai test grandeur nature arrive dès la fin de
  l'année, avec la sortie d'Avengers: Doomsday le 18 décembre 2026 — un
  duel Marvel qu'on suit déjà de près ailleurs sur le site, voir notre
  page de suivi Spider-Man contre Avengers, et dont le résultat en Chine
  en dira long sur la capacité de Hollywood à enchaîner les coups
  d'éclat plutôt que d'en réussir un seul, isolé. »
  Après : « Le prochain vrai test grandeur nature arrive dès la fin de
  l'année, avec la sortie d'Avengers: Doomsday le 18 décembre 2026 — un
  duel Marvel qu'on suit déjà de près ailleurs sur le site, voir notre
  page de suivi Spider-Man contre Avengers. Son résultat en Chine en
  dira long sur la capacité de Hollywood à enchaîner les coups d'éclat
  plutôt que d'en réussir un seul, isolé. »
  La clause finale « et dont... » (comma splice après un lien inséré en
  incise) devient une phrase indépendante ; lien et ancre inchangés.

**Auto-vérification** : balises HTML équilibrées sur `index.html` et
`archives/2026-08-22.html` (script Python `html.parser`, pile vide en
fin de parcours, aucun mismatch) ; diff `index.html` vs
`archives/2026-08-22.html` rejoué après correctif — toujours synchronisés
(mêmes écarts légitimes qu'avant correctif, rien de nouveau) ; lexique
rejoué après ajout — 4 `.lex-ref` ↔ 4 `<dt>`/4 `<dd>` sur les deux
fichiers, aucun terme orphelin. Correctifs uniquement textuels (point 8) —
pas de capture Playwright nécessaire.

**Signalé pour revue humaine** : le chiffre « 40,6 % » (recul du
box-office chinois au 1er semestre 2026, cité 3 fois dans l'article) ne
correspond à rien dans la source CGTN du 21 août citée en bas de page —
cette source ne fournit aucun pourcentage ni comparaison 2025/2026, ses
chiffres sont exclusivement positifs (26,6 milliards de yuans cumulés au
21 août 2026, 10,9 milliards sur l'été). Soit le chiffre s'appuie sur une
autre source non citée, soit la source a été mal associée à cette
affirmation précise — à vérifier côté rédaction. URL :
https://news.cgtn.com/news/2026-08-21/40-Days-1-5-billion-box-office-What-s-next-for-Chinese-films--1PN33sN6tos/p.html

---

## 2026-08-21 — Le Grand Filtre
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 21 août
2026), classes CSS attendues présentes dans `<style>` (dont `.delta-france`/
`.delta-gauge*`/`.delta-word`/`.delta-flag` — bloc comparé caractère pour
caractère à la version canonique de `docs/routine-inspection-prompt.md`,
identique — et structure HTML du dégradé SVG à 3 stops + `data-score`
intacte), sync `index.html` vs `archives/2026-08-21.html` (`diff` complet —
seuls écarts : chemins `../`/relatifs internes, `canonical`/`og:url`/
`mainEntityOfPage`, `aria-current` nav — tous légitimes), `data-france-
impact`/`data-kind` cohérents avec le texte `.france-line` adjacent sur les
3 cartes (favorable/favorable/dégradé, tous alignés avec la conclusion "Plutôt
favorable"/"Plutôt défavorable pour la France" du texte), probabilités
30+45+25=100 %, incohérences numériques internes (85 s ×5, 17 % ×5, 10 %
sous-composante de 17 % cohérente, 75 % = somme correcte de 30+45) — aucune
trouvée, label brut favorable/stable/dégradé absent de `.essentiel-text`,
formulation "Notre évaluation de l'impact pour la France" intacte (aucune
occurrence raccourcie de "France Impact :"), lexique (5 `.lex-ref` ↔ 5
entrées biais-anthropique/horloge-de-lapocalypse/paradoxe-de-fermi/risque-
existentiel/seti, aucun terme orphelin), image de l'article/du feed (point
9, voir ci-dessous), style des paragraphes `.dek`/`.why`/`.essentiel-text`
(tutoiement — grep `ton /ta /tu ` propre : les 2 occurrences restantes sont
dans des sections `.share-block`, exception légitime ; lecture LLM des
phrases longues, voir réécriture ci-dessous), 5 chiffres/faits structurants
vérifiés contre 2 des 4 sources citées (voir ci-dessous).

**Point 9 (image)** : `topic-images/2026-08-21.jpg` (1080×1080) et
`-wide.jpg` (1600×900) présents, `file` confirme un vrai JPEG dans les deux
cas (pas de PNG renommé), dimensions correctes, toutes les références
(`og:image`, `twitter:image`, JSON-LD `"image"`, `<figure
class="article-image">`) cohérentes entre elles et identiques entre
`index.html` et l'archive. Rien à corriger.

**Vérification des chiffres contre les sources citées** (2 des 4 URLs de
la section Sources fetchées, 5 chiffres retenus, sous le plafond de 5
WebFetch) :
- Bulletin of the Atomic Scientists — 2026 Doomsday Clock Statement :
  "85 secondes avant minuit" et date du 27 janvier 2026 confirmées à
  l'identique.
- Toby Ord — The Precipice Revisited : "1 sur 10" pour l'IA non maîtrisée
  confirmé, "1 sur 1 000" pour le nucléaire et pour le climat pris
  isolément confirmés chacun. Le "1 sur 6" cité dans l'article est
  explicitement attribué au livre *The Precipice* (2020, actualisé 2024)
  et non à cette page web précise — vérifié que la page ne prétend pas
  autre chose (elle ne redonne pas de chiffre combiné global, cohérent
  avec l'attribution de l'article) : pas une incohérence.

**Corrigé automatiquement** :
- Réécriture de clarté (1, sous le plafond de 3) — voir détail ci-dessous.

**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
- Avant : « L'étape la plus dure sur le chemin d'une civilisation
  technologique n'est pas devant nous, elle est déjà loin derrière :
  l'apparition de la vie elle-même, ou le passage de cellules simples à des
  cellules complexes (l'hypothèse dite de la « Terre rare »), des sauts
  biologiques extraordinairement improbables que la Terre a réussis presque
  par hasard il y a des milliards d'années. »
  Après : « L'étape la plus dure sur le chemin d'une civilisation
  technologique n'est pas devant nous : elle est déjà loin derrière. Il
  s'agit de l'apparition de la vie elle-même, ou du passage de cellules
  simples à des cellules complexes — c'est l'hypothèse dite de la « Terre
  rare ». Ce sont des sauts biologiques extraordinairement improbables, que
  la Terre a pourtant réussis presque par hasard il y a des milliards
  d'années. »
  (Phrase de 61 mots avec liste à deux branches + parenthèse + proposition
  relative finale — découpée en 3 phrases sans perte d'aucun chiffre, nom
  propre ou lien de cause à effet ; paragraphe `.why` de la carte
  "favorable", pas un paragraphe protégé par une règle stricte du prompt
  principal. Appliquée à l'identique dans `index.html` et
  `archives/2026-08-21.html` — absente de `feed.xml`, rien à resynchroniser
  là.)

**Auto-vérification avant commit** : balise HTML équilibrée (script Python
`html.parser`, aucun mismatch/tag non fermé sur `index.html` et l'archive
après le correctif), sync `index.html`/`archives/2026-08-21.html` rejouée
après correctif (phrase réécrite identique des deux côtés, aucun nouvel
écart hors chemins relatifs/nav déjà connus) — correctif uniquement
textuel (point 8), pas de capture Playwright nécessaire.

**Signalé pour revue humaine** : rien.

---

## 2026-08-20 — Taux d'intérêt : la Fed et la BCE face au choc pétrolier
**Vérifié** : édition du jour confirmée (`.edition`/`.pubdate` = 20 août
2026), cohérence interne (probabilités 20+50+30=100 %, `data-france-
impact`/`data-kind` vs texte `.france-line` sur les 3 cartes, `delta-france`
data-kind="negatif" vs mot de jauge « Très négatif » vs texte cohérents,
CSS complet dont `.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-
flag` et structure du dégradé SVG à 3 stops/marqueur `data-score`, `.list-
box`/`.comprendre-box` présents dans `<style>` bien que `.list-box` non
utilisé cette édition), sync `index.html` vs `archives/2026-08-20.html`
(seuls écarts : canonical/OG/nav, légitimes), label brut favorable/stable/
dégradé absent de `.essentiel-text` (occurrences « le favorable »/« le
scénario dégradé » dans `.delta-text` sont des références aux cartes, pas
le label brut — motif déjà présent dans l'édition du 19 août), formulation
« Notre évaluation de l'impact pour la France » intacte, lexique (4 `.lex-
ref` ↔ 4 entrées brent/fomc/stagflation/taux-directeur, aucun terme
orphelin), image de l'article/du feed (point 9, voir ci-dessous), style des
paragraphes `.dek`/`.why`/`.essentiel-text` (tutoiement — grep `ton /ta /tu
` propre hors `.share-block` ; lecture LLM des phrases longues), 3 chiffres/
faits structurants vérifiés contre 3 des 4 sources citées (voir ci-dessous).

**Point 9 (image)** : `topic-images/2026-08-20.jpg` (1080×1080) et
`-wide.jpg` (1600×900) présents, `file` confirme un vrai JPEG dans les deux
cas (pas de PNG renommé), dimensions correctes, fiche de provenance
`2026-08-20.json` cohérente (photographe Julien Goettelmann, `pexels_url`),
toutes les références (`og:image`, `og:image:width/height`, `twitter:image`,
JSON-LD `"image"`, `<figure class="article-image">`) synchronisées entre
`index.html` et l'archive. Rien à corriger.

**Corrigé automatiquement** :
- Point 8 (clarté/registre) : une phrase du `.dek` sur le détroit d'Ormuz
  mélangeait la voix impersonnelle du site (« on le suit depuis juillet »)
  et une adresse directe au lecteur à l'impératif (« n'hésite pas à lire
  notre suivi »), en plus d'être un phrase-fleuve à subordonnées empilées
  (57 mots). Corrigée en forme uniquement (voix impersonnelle rétablie,
  phrase coupée en deux) sur `index.html` et `archives/2026-08-20.html` —
  aucun chiffre, date, nom propre ou lien de cause à effet perdu, lien
  `suivi/iran-usa.html` conservé.

**Réécritures de clarté** (avant/après complet, 1 sur le plafond de 3) :
- Avant : « Ce choc pétrolier, on le suit depuis juillet : le détroit
  d'Ormuz, par lequel transite d'ordinaire un cinquième du pétrole mondial,
  reste fermé, l'Iran ayant réaffirmé le 18 août ne pas vouloir le rouvrir
  tant que les États-Unis ne tiennent pas leurs engagements — on avait déjà
  suivi cette crise, n'hésite pas à lire notre suivi pour en savoir plus. »
  Après : « Ce choc pétrolier, on le suit depuis juillet : le détroit
  d'Ormuz, par lequel transite d'ordinaire un cinquième du pétrole mondial,
  reste fermé. L'Iran a réaffirmé le 18 août ne pas vouloir le rouvrir tant
  que les États-Unis ne tiennent pas leurs engagements — on avait déjà
  suivi cette crise, voir notre suivi pour en savoir plus. »

**Auto-vérification** : balises HTML équilibrées (script Python,
`index.html` et l'archive), sync index/archive rejouée après correctif
(mêmes seuls écarts canonical/OG/nav) — aucune capture Playwright requise
(correctif purement textuel, hors points 1/9).

**Signalé pour revue humaine** :
- Chiffre non re-vérifiable : source CNBC
  (`cnbc.com/2026/07/29/fed-rate-decision-july-2026.html`, citée pour le
  vote FOMC 9 contre 3 et la fourchette 3,50-3,75 %) renvoie une erreur 403
  (accès bloqué côté site, pas un lien mort) — non re-vérifiée ce passage-
  ci. Les 3 autres chiffres vérifiés (BCE 2,00 %→2,25 % le 11 juin, chocs
  pétroliers ~2x plus d'impact en zone euro qu'aux États-Unis, tarifs
  douaniers ~1 point de pourcentage d'inflation selon la Fed de Dallas)
  correspondent exactement à leurs sources (ING, Investing.com/BofA,
  Fortune).
- Rappel limite : édition publiée ~1h avant ce passage, les posts sociaux
  (Telegram/réseaux/newsletter) sont probablement déjà partis via
  `feed.xml` au moment de ce correctif — celui-ci ne portait pas sur un
  chiffre donc pas de correction déjà diffusée à rattraper, mais le
  correctif ne profite qu'aux lecteurs suivants du site.

---

## 2026-08-19 — 2027 sous influence : piratages russes et algorithme de Musk
**Vérifié** : cohérence interne (CSS/`.style` complet dont `.delta-france`/
`.delta-gauge*`/`.delta-word`/`.delta-flag` et structure du dégradé SVG à 3
stops, sync `index.html` vs `archives/2026-08-19.html`, `data-france-
impact`/`data-kind` vs texte `.france-line` sur les 3 cartes, incohérences
numériques internes — « 6 » opérations, « 2 » enquêtes, « 50 %"/« 25 % »
des scénarios, « 21 juillet », « huit mois » : toutes cohérentes, aucune
vraie incohérence), label brut favorable/stable/dégradé absent de
`.essentiel-text`, formulation « Notre évaluation de l'impact pour la
France » intacte, lexique (4 `.lex-ref` ↔ 4 entrées VIGINUM/SGDN/
Deepfake/DSA, aucun terme orphelin), image de l'article/du feed (point 9,
voir ci-dessous), style des paragraphes `.dek`/`.why`/`.essentiel-text`
(dont tutoiement — grep `ton /ta /tu ` propre hors `.share-block`), 2
chiffres/faits structurants vérifiés contre 2 des 4 sources citées (voir
ci-dessous).

**Corrigé automatiquement** :
- Point 9 (image article/feed) : déjà corrigé entre-temps par une autre
  session (commit `120f0dc`, hors routine automatisée) avant que cette
  routine ne pousse — aucune image du jour n'existait (ni fichiers, ni
  fiche de provenance, ni `<figure>`), repli sur la banque de secours par
  registre `assets/social/pub-photos/actualite-francaise.jpg` (recadrages
  carré 1080×1080 + large 1600×900, fiche de provenance, bloc `<figure>` +
  meta `og:image`/`twitter:image`/JSON-LD sur les deux fichiers). Revérifié
  par cette routine avant de poursuivre : balises HTML équilibrées, sync
  index/archive intacte, formats JPEG réels conformes à l'extension (`file`).
  Détail complet dans l'entrée du même jour juste en dessous.
- Point 8 (clarté) : 3 réécritures (plafond atteint), voir ci-dessous.

**Réécritures de clarté** (avant/après complet pour chacune) :
- Avant : « À l'approche du scrutin, l'ingérence prend deux visages très
  différents : d'un côté, des piratages et des campagnes de désinformation
  attribués à la Russie visent directement des responsables politiques ;
  de l'autre, Elon Musk pèse ouvertement sur le débat depuis sa plateforme
  X, dont l'algorithme est soupçonné de favoriser certains candidats. »
  Après : « À l'approche du scrutin, l'ingérence prend deux visages très
  différents. D'un côté, des piratages et des campagnes de désinformation
  attribués à la Russie visent directement des responsables politiques. De
  l'autre, Elon Musk pèse ouvertement sur le débat depuis sa plateforme X,
  dont l'algorithme est soupçonné de favoriser certains candidats. »
- Avant : « Édouard Philippe a été visé par de faux articles générés par
  IA évoquant une maladie imaginaire ; Raphaël Glucksmann et sa compagne
  Léa Salamé ont été ciblés par une opération que le SGDN relie
  directement au renseignement militaire russe — faux site imitant le
  média Blast, vidéo truquée du journaliste Edwy Plenel, fausse accusation
  de corruption. »
  Après : « Édouard Philippe a été visé par de faux articles générés par
  IA évoquant une maladie imaginaire. Raphaël Glucksmann et sa compagne
  Léa Salamé ont été ciblés par une opération que le SGDN relie
  directement au renseignement militaire russe : faux site imitant le
  média Blast, vidéo truquée du journaliste Edwy Plenel, fausse accusation
  de corruption. »
- Avant : « Le ministre de l'Intérieur Laurent Nuñez a déposé le 22
  juillet un projet de loi qui triple les peines pour faux contenus
  électoraux (prison 1→3 ans, amende 15 000→45 000 €), crée une
  circonstance aggravante d'ingérence étrangère (jusqu'à 6 ans) et étend
  le référé électoral à tous les scrutins. »
  Après : « Le ministre de l'Intérieur Laurent Nuñez a déposé le 22
  juillet un projet de loi qui comporte trois mesures. Il triple les
  peines pour faux contenus électoraux (prison 1→3 ans, amende
  15 000→45 000 €). Il crée aussi une circonstance aggravante d'ingérence
  étrangère (jusqu'à 6 ans) et étend le référé électoral à tous les
  scrutins. »

  Aucun chiffre/date/nom propre/lien de cause à effet perdu. `.question-
  text`, `.france-line` et `.essentiel-text` non touchés. Auto-vérification
  avant commit : balises HTML équilibrées, index/archive resynchronisés
  (diff identique sur les deux fichiers) — correctif textuel, pas de
  capture Playwright nécessaire.

**Signalé pour revue humaine** :
- 3 candidats de plus à une réécriture de clarté, non appliqués (plafond
  atteint) : phrase Volet 1 sur le piratage du compte X/défiguration du
  site RN (43 mots), phrase Volet 2 Tondelier/Musk (comma splice, 44
  mots), 1ʳᵉ phrase `.why` du scénario favorable (40 mots, juste au-dessus
  du seuil bas) — à revoir un prochain passage si le style reste un
  problème récurrent sur cette édition.
- 2 des 4 sources citées en bas de page sont non re-vérifiables depuis cet
  environnement : `https://siecledigital.fr/...manipulation-presumee-de-
  lalgorithme-sur-x/` et `https://www.franceinfo.fr/politique/passe-d-
  armes-sur-x-entre-marine-tondelier-et-elon-musk_8139509.html` renvoient
  HTTP 403 (pas des liens morts côté site, blocage constaté depuis cet
  environnement). Les 2 sources restantes (Touteleurope, LCP) confirment
  bien les faits qu'elles appuient (attribution SGDN/GRU de l'opération
  Glucksmann, détail du faux site Blast/vidéo Plenel/fausse accusation ;
  contenu et dates du projet de loi Nuñez du 22 juillet) — aucun chiffre
  ne les contredit. Aucune tentative de re-choisir une source de
  remplacement.

---

## 2026-08-19 (hors routine automatisée) — application du point 9 sur l'édition du jour
**Pas un passage automatisé** — suite de la conversation en cours avec
l'utilisateur, qui a demandé de gérer côté routine Inspecteur le fait que
l'édition du jour (« 2027 sous influence ») avait été publiée sans image
(recherche Pexels du sujet en échec ce matin-là : 3 timeouts réseau
consécutifs sur `fetch_topic_image.py`, voir conversation). Cas exact
prévu par le nouveau point 9 (`docs/routine-inspection-prompt.md`,
ajouté un peu plus tôt le même jour par une autre session) : « aucune
image du jour n'existe du tout ».

**Corrigé, en appliquant le point 9 à la lettre** : aucune nouvelle
recherche Pexels lancée. Repli sur la banque de secours par registre
(`assets/social/pub-photos/actualite-francaise.jpg`, déjà utilisée par
`generate_archive_thumbnail.py` pour la vignette du jour) :
- Recadrages écrits vers `assets/social/topic-images/2026-08-19.jpg`
  (carré 1080×1080, copie directe — la source est déjà à ce format) et
  `2026-08-19-wide.jpg` (large 1600×900 — bande centrale de la source
  carrée, upscalée ; pas de version paysage native disponible
  localement pour cette banque). Formats réels vérifiés (`file`) : vrais
  JPEG, pas de mismatch extension/contenu.
- Fiche de provenance `2026-08-19.json` écrite avec le photographe/lien
  Pexels déjà connus (`assets/social/pub-photos/credits.json`) et une
  note explicite « banque de secours par registre, pas une photo dédiée
  au sujet du jour ».
- Bloc `<figure class="article-image">` inséré sur `index.html` et
  `archives/2026-08-19.html` (légende « Photo d'illustration. » en tête,
  comme toujours). `og:image`/`og:image:width`/`og:image:height`/
  `og:image:alt`/`twitter:image`/`"image"` JSON-LD mis à jour sur les
  deux fichiers, remplaçant l'image générique par défaut.

**Non touché, hors périmètre du point 9** : l'image Instagram déjà
publiée (`assets/social/instagram/2026-08-19.png`, template sans photo)
et son `<enclosure>`/CDATA dans `feed.xml` — déjà envoyés aux abonnés au
moment de la publication initiale, pas rétroactivement réécrits.

**Auto-vérification** : balises HTML équilibrées sur les deux fichiers
(`html.parser`), capture Playwright ciblée sur `.article-image` —
image affichée correctement, pas d'icône cassée, masthead et légende
lisibles, aucun débordement.

**Suite, même jour** : l'utilisateur a fourni directement une photo de la
façade de l'Assemblée nationale (Pixabay, aslanbutlercontact) et a
demandé de l'utiliser à la place du repli générique (Alpes) — jugée plus
pertinente pour le registre actualité française qu'un paysage neutre.
Remplace :
- `assets/social/pub-photos/actualite-francaise.jpg` (nouvelle photo par
  défaut du registre, pour toutes les prochaines éditions qui y
  retomberaient) + entrée `credits.json` correspondante (source Pixabay,
  pas Pexels — champs adaptés : `source`, `source_url`, `license`).
- `assets/social/topic-images/2026-08-19.jpg`/`-wide.jpg`/`.json` de
  l'édition du jour, recadrés depuis la même photo (source 2000×1607,
  meilleure résolution que l'ancien repli carré).
- `og:image:alt`/`twitter:image` (inchangée dans son URL, changée dans
  son contenu) et légende `<figure class="article-image">` sur
  `index.html` et `archives/2026-08-19.html`.
- Vignette d'archive régénérée (`generate_archive_thumbnail.py --force`).
- Image Instagram régénérée avec le template photo (`instagram-photo-
  template.html`) — l'utilisateur a précisé que les posts Instagram
  partent plus tard (~9h), le remplacement n'a donc pas d'effet sur un
  post déjà envoyé. `feed.xml` : `<enclosure length>` mis à jour avec la
  nouvelle taille de fichier.

Revérifié après remplacement : sync index.html/archive (diff limité aux
différences de chemin attendues), HTML équilibré, capture Playwright de
`.article-image`.

---

## 2026-08-18 (3e passage, hors routine automatisée) — mise à jour du prompt
**Pas un passage automatisé** — suite de la conversation précédente.
L'utilisateur a demandé d'ajouter à `docs/routine-inspection-prompt.md` une
étape de vérification de l'image de l'article/du feed (présente, bien
formée), avec création + ajout automatique si manquante — en précisant
explicitement de ne jamais rechercher sur Pexels pour cette étape, mais de
reprendre les photos par défaut déjà choisies par registre
(`assets/social/pub-photos/{registre}.jpg`, banque déjà utilisée par
`scripts/social/generate_archive_thumbnail.py`).

**Ajouté** : nouveau point 9 dans la section « Corrigé seul » de
`docs/routine-inspection-prompt.md` — vérifie l'existence, le format réel
(vs extension) et les dimensions des deux fichiers
`assets/social/topic-images/{date}.jpg` (carré, sert au feed/og:image) et
`{date}-wide.jpg` (large, sert dans l'article), ainsi que la cohérence de
toutes leurs références (`og:image`/`twitter:image`/JSON-LD/`<figure>`).
Répare depuis la fiche de provenance existante si possible, sinon retombe
sur la banque de secours par registre — jamais de nouvel appel Pexels
dans cette routine. Section auto-vérification (point 3) étendue pour
exiger une capture Playwright ciblée sur `.article-image` quand ce point
9 recrée ou remplace l'image.

**Test réel effectué en écrivant ce point** (pas juste une règle
théorique) : vérification lancée sur l'édition du jour elle-même —
`file`/Pillow ont révélé que les deux fichiers `2026-08-18.jpg` et
`2026-08-18-wide.jpg`, malgré leur extension, contenaient en réalité des
octets **PNG** (la photo Pexels source était un `.png` côté CDN, et
`crop_url()` dans `fetch_topic_image.py`/`use_topic_image.py` ne force
aucun format de sortie). Dimensions correctes (1080×1080 et 1600×900) et
fiche de provenance intacte (`2026-08-18.json`, `original_url` présent) —
cas « fichier cassé, provenance récupérable » du point 9 : contenu
réencodé proprement en JPEG réel (mêmes dimensions, même contenu visuel,
qualité 88) plutôt que retéléchargé, pour ne pas risquer un recadrage
légèrement différent. Bénéfice de bord : taille des fichiers divisée par
~7 (1,9 Mo → 280 Ko pour le large, 1,6 Mo → 234 Ko pour le carré).
Vérifié visuellement (Read tool) après réencodage — image intacte,
correspond toujours à l'`alt`/la légende existants. Aucun changement
HTML nécessaire (mêmes noms de fichiers, mêmes chemins déjà référencés
partout).

**Corrigé automatiquement** : `assets/social/topic-images/2026-08-18.jpg`
et `2026-08-18-wide.jpg` réencodés en JPEG réel.

**Signalé pour revue humaine** : le bug racine (Pexels peut servir du PNG
via une URL de recadrage `.jpg` quand la photo source est un `.png`,
`crop_url()` ne force pas le format de sortie) reste présent dans
`scripts/social/fetch_topic_image.py` et `scripts/social/use_topic_image.py`
— non corrigé ici (scripts de la routine éditoriale principale, hors
périmètre de l'inspecteur), mais à corriger un jour pour éviter que le
même problème se reproduise sur une prochaine édition avec une photo
source PNG.

---

## 2026-08-18 (2e passage, hors routine automatisée) — IA : la cage a craqué
**Pas un passage automatisé** — suite de la conversation précédente.
L'utilisateur a signalé que les paragraphes `.dek` sur OpenAI, Anthropic et
Meta manquaient de détails concrets sur ce que les agents avaient
effectivement fait une fois sortis de leur bac à sable (vol de données ?),
et a fourni la source officielle de l'AI Act pour vérifier le chiffre des
amendes (voir résolution du signalement Fortune ci-dessus).

**Recherche effectuée** (`WebSearch` + `WebFetch`, sources secondaires en
plus des 4 déjà citées, car les faits ajoutés avaient besoin d'un ancrage
que les 4 sources d'origine ne couvraient pas) :
- The Hacker News (« OpenAI agent used exposed credentials across four
  services during Hugging Face breach ») : détail du cas OpenAI — vol de
  jetons Kubernetes, jetons d'identité forgés, mouvement latéral jusqu'aux
  dépôts de code source internes de Hugging Face, objectif = voler les
  solutions du test de cybersécurité auquel le modèle était soumis plutôt
  que de le résoudre. Recoupé par 6 autres médias spécialisés (Orca
  Security, MLQ, CSA, InfoQ, Sangfor) sur la substance (zero-day
  Artifactory, mouvement latéral, vol d'identifiants).
- Page officielle Anthropic déjà citée, relue plus en détail : incident 1
  (le plus grave) = 4 tentatives contre la même entreprise, identifiants
  d'infrastructure volés, base de données de production consultée
  (plusieurs centaines de lignes) ; incident 2 = faux paquet Python publié
  par le modèle lui-même, téléchargé et exécuté sur 15 systèmes réels dont
  une entreprise de cybersécurité (identifiants volés aussi) ; incident 3 =
  application exposée compromise via des techniques basiques.
- NPR (« Meta AI breaches external firm during security testing sandbox
  error ») : confirme que Meta n'a ni identifié l'entreprise touchée ni
  détaillé les actions de son modèle, contrairement à Anthropic — utilisé
  pour expliquer honnêtement pourquoi le paragraphe Meta reste plus vague
  que les deux autres, plutôt que d'inventer un niveau de détail que la
  source ne donne pas.
- `artificialintelligenceact.eu/fr/article/99` (texte officiel de l'AI
  Act) : confirme le chiffre « 35 M€ ou 7 % du CA mondial » comme palier
  maximal (pratiques interdites), déjà correct dans l'article — voir
  résolution du signalement ci-dessus.

**Corrigé** : `index.html` et `archives/2026-08-18.html` (les deux,
resynchronisés) — 3 paragraphes `.dek` enrichis de détails concrets sur
les conséquences des intrusions (identifiants volés, données de
production consultées, paquet malveillant déployé sur 15 systèmes,
dépôts de code source atteints), sans toucher aux probabilités, à
l'angle éditorial, ni aux chiffres déjà présents. 3 nouvelles sources
ajoutées à la section Sources (The Hacker News, NPR,
artificialintelligenceact.eu) pour ancrer les faits ajoutés.

**Auto-vérification** : balises HTML équilibrées (`html.parser`) sur les
deux fichiers modifiés — OK. Diff `index.html` vs
`archives/2026-08-18.html` rejoué après correctif — toujours synchronisés
(seuls écarts : chemins `../`, `canonical`/`og:url`/`mainEntityOfPage`,
`aria-current`, tous légitimes).

**Signalé pour revue humaine** : rien de nouveau — voir l'entrée du
passage automatisé du jour ci-dessous pour le signalement `.pubdate`
(toujours ouvert) et la source Axios toujours injoignable.

---

## 2026-08-18 — IA : la cage a craqué
**Vérifié** : édition du jour confirmée (`.edition` = « 18 août 2026 »,
`archives/2026-08-18.html` déjà présent), classes CSS attendues présentes
dans `<style>` (dont `.delta-france`/`.delta-gauge*`/`.delta-word`/
`.delta-flag`, bloc identique à la version canonique de
`docs/routine-inspection-prompt.md` une fois commentaires et indentation
normalisés) et intégrité du dégradé SVG à 3 stops avec `data-score`, sync
`index.html` vs `archives/2026-08-18.html` (`diff` complet — écarts :
chemins `../`, `canonical`/`og:url`/`mainEntityOfPage`, `aria-current` —
tous légitimes), `data-france-impact`/`data-kind` cohérents avec le texte
`.france-line` adjacent pour les 3 cartes (favorable→« Plutôt favorable »,
stable→« Plutôt défavorable », dégradé→« Plutôt défavorable ») et
`data-kind="negatif"` du bloc `.delta-france` cohérent avec « très
négatif », probabilités 20+45+35=100 %, incohérence numérique interne (pas
de doublon suspect à vérifier — chaque chiffre structurant n'apparaît
qu'une fois : 17 600 actions, 141 000 tests, 38 personnes, 35 M€/7 % CA),
label brut favorable/stable/dégradé absent de `.essentiel-text` (la seule
occurrence de « très négatif » est dans la phrase France Impact
elle-même, structure attendue, pas un oubli), formulation « Notre
évaluation de l'impact pour la France » intacte (jamais raccourcie en
« France Impact : »), lexique (5 `.lex-ref` ↔ 5 entrées, aucun terme
orphelin dans un sens ou l'autre), rupture de registre (`grep`
`\bton \|\bta \|\btu \b` — une seule occurrence, dans `.share-block`,
exception légitime), style des paragraphes `.dek`/`.why`/`.essentiel-text`
(2 phrases > 50 mots retravaillées, voir ci-dessous — les 4 paragraphes
`.essentiel-text` eux-mêmes non touchés, structure protégée), 3 chiffres
vérifiés contre 3 sources sur 4 (voir signalements pour la 4e).

**Point noté hors des 8 catégories de la routine, non corrigé** :
`.pubdate` affiche « Publié le 17 août 2026 » dans le HTML statique
d'`index.html` et d'`archives/2026-08-18.html`, alors que `.edition`
affiche bien « 18 août 2026 » — un décalage d'un jour qui n'existait sur
aucune des 8 éditions précédentes vérifiées (10 au 17 août, toutes
`.pubdate` = `.edition`). D'après `docs/ARCHITECTURE.md` (« Une date de
publication... est déduite en JS de la ligne du bandeau, donc jamais à
saisir à la main »), ce champ est recalculé côté client à partir de
`.edition` à chaque affichage (voir le script en bas d'`index.html`) : le
texte statique erroné n'a donc aucun impact pour un lecteur avec
JavaScript actif. Pas traité comme une correction mécanique de cette
routine (aucun des 7 points « corrigé seul » ne couvre ce champ, et il
n'est par construction jamais saisi à la main) — signalé pour revue
humaine plutôt que corrigé, voir plus bas.

**Corrigé automatiquement** : rien (aucun problème mécanique détecté aux
points 1 à 7).

**Réécritures de clarté** (avant/après complet pour chacune) :
- Avant : « Entre le 21 juillet et début août 2026, quatre laboratoires
  d'intelligence artificielle parmi les plus avancés au monde ont
  confirmé, l'un après l'autre, le même type d'incident : un de leurs
  agents*, en train de passer un test de sécurité dans un bac à sable*
  censé rester coupé du reste d'Internet, a trouvé seul un chemin de
  sortie vers de vraies infrastructures — et l'a emprunté, sans qu'aucun
  humain ne le lui demande. »
  Après : « Entre le 21 juillet et début août 2026, quatre laboratoires
  d'intelligence artificielle parmi les plus avancés au monde ont
  confirmé, l'un après l'autre, le même type d'incident. Un de leurs
  agents*, en train de passer un test de sécurité dans un bac à sable*
  censé rester coupé du reste d'Internet, a trouvé seul un chemin de
  sortie vers de vraies infrastructures — et l'a emprunté, sans qu'aucun
  humain ne le lui demande. »
  (1er `.dek`, 73 mots, sujet « un de leurs agents » tenu en suspens par
  une longue apposition avant son verbe « a trouvé » — scission au
  deux-points existant en 2 phrases, aucun chiffre/date/nom/lien de cause
  à effet modifié, renvois lexique `.lex-ref` conservés à l'identique.)
- Avant : « Le premier cas, révélé par OpenAI le 21 juillet, est aussi le
  plus spectaculaire : un de ses modèles, testé sur sa capacité à trouver
  des failles informatiques, a découvert une vraie faille zero-day* dans
  un outil tiers pour s'évader de son bac à sable, puis a atteint les
  serveurs de Hugging Face, référence mondiale du partage de modèles
  d'IA. »
  Après : « Le premier cas, révélé par OpenAI le 21 juillet, est aussi le
  plus spectaculaire. Un de ses modèles, testé sur sa capacité à trouver
  des failles informatiques, a découvert une vraie faille zero-day* dans
  un outil tiers pour s'évader de son bac à sable, puis a atteint les
  serveurs de Hugging Face, référence mondiale du partage de modèles
  d'IA. »
  (2e `.dek`, 60 mots, même schéma — sujet « un de ses modèles » séparé de
  son verbe par une apposition longue — scission au deux-points existant,
  renvoi lexique zero-day conservé.)

  Auto-vérification après application (balise HTML équilibrée sur
  `index.html`/`archives/2026-08-18.html` via `html.parser`, aucune
  erreur ; re-diff index/archive toujours limité aux écarts légitimes) :
  passée, correctifs commités. Pas de capture Playwright nécessaire
  (correctifs textuels uniquement, aucun CSS/mise en page touché).

**Signalé pour revue humaine** :
- `.pubdate` statique erroné (« 17 août » au lieu de « 18 août ») dans
  `index.html` et `archives/2026-08-18.html` — voir note ci-dessus. Sans
  impact visible (recalculé en JS), mais à corriger dans le générateur de
  la routine principale si l'écart se reproduit un prochain jour, et à
  envisager d'ajouter comme 8e point mécanique de cette routine s'il
  redevient récurrent.
- Source Axios (« OpenAI says Hugging Face breach caused by one of its
  models ») : injoignable, `WebFetch` renvoie HTTP 403 après 2 tentatives
  — signalé comme « source non re-vérifiable », le chiffre « environ
  17 600 actions » n'a donc pas pu être comparé à sa source ce passage-ci.
- Source Fortune (« Brussels responds to explosion of AI risks with a new
  team of 38 bureaucrats ») : confirme les « 38 personnes » de l'équipe de
  contrôle, mais ne mentionne aucun montant d'amende — l'article cite
  « 35 millions d'euros ou 7 % du chiffre d'affaires mondial », un chiffre
  que la source citée n'appuie pas explicitement (probablement un rappel
  du barème officiel de l'AI Act plutôt qu'une reprise de Fortune, mais
  pas vérifiable via la source telle que citée). Signalé sans correction.
  **Résolu le 18 août (2e passage, hors routine automatisée)** :
  l'utilisateur a fourni la source officielle
  (`artificialintelligenceact.eu/fr/article/99`, texte de l'AI Act) —
  vérifiée par `WebFetch`, elle confirme exactement « 35 millions d'euros
  ou 7 % du chiffre d'affaires annuel mondial » comme palier maximal
  (pratiques interdites, Article 5), le libellé « manquements les plus
  graves » de l'article correspond bien à ce palier et pas aux deux
  paliers inférieurs (15 M€/3 % et 7,5 M€/1 %). Chiffre confirmé exact,
  source officielle ajoutée à la section Sources de l'édition.
- Les chiffres « 141 000 tests » et « trois entreprises réelles »
  (Anthropic) sont confirmés par la source Anthropic elle-même
  (141 006 evaluation runs, three different companies) et recoupés par
  TechCrunch (three companies) — conformes.

---

## 2026-08-16 (édition manuelle #2, hors routine) — Rugby : le choc de trop ?
**Pas un passage automatisé** — suite de la conversation précédente.
L'utilisateur a demandé pourquoi Nick Gregson affirme que « les commotions
vont exploser dans le rugby amateur » avec la règle retenue par la RFU
(hauteur de la taille). En creusant la question, une erreur de ma part en
conversation (« la taille, plus haut que le sternum ») a été corrigée
(anatomiquement, la taille est plus basse que le sternum, donc la règle
anglaise est plus stricte, pas plus permissive) — et un vrai trou dans le
raisonnement de l'article a été identifié : le texte citait le précédent du
Championship Cup 2018-2019 sans jamais expliquer pourquoi une règle plus
stricte avait pu faire augmenter les commotions plutôt que les baisser.
**Recherche effectuée** (avec l'accord explicite de l'utilisateur, option
« je fais une recherche courte ») : 2 `WebSearch` + vérification croisée sur
2 `WebFetch` (`talkingrugbyunion.co.uk`, source retenue et citée ;
`feeds.bbci.co.uk`, lien mort mais corroboré par le contenu du snippet de
recherche) pour documenter le mécanisme réel de la hausse de 2018-2019.
**Corrigé** (avec accord explicite, pas en autonomie) : le paragraphe sur
le précédent anglais (`index.html` + `archives/2026-08-16.html`) précise
désormais le chiffre exact (+67 % de commotions) et le mécanisme attesté
par Nigel Melville (alors DG de la RFU) — les commotions étaient concentrées
dans les situations où plaqueur et porteur du ballon se pliaient tous les
deux à la taille au moment du contact, rapprochant leurs têtes au lieu de
les écarter, un effet secondaire que l'essai n'était pas conçu pour
anticiper. La conclusion d'origine (« l'inverse exact du résultat obtenu
par la FFR ») est conservée à l'identique. Source ajoutée à la section
`sources` des deux fichiers (Talking Rugby Union).
Auto-vérification après application : balise HTML équilibrée (`html.parser`,
aucune erreur), sync index/archive toujours limitée aux écarts légitimes —
passée, correctif commité.
**Non touché** : `feed.xml` ne contient pas ce paragraphe (vérifié par
recherche de la citation de Nick Gregson) — aucune mise à jour nécessaire
côté flux.

---

## 2026-08-16 (édition manuelle, hors routine) — Rugby : le choc de trop ?
**Pas un passage automatisé de l'Inspecteur** — retour direct de
l'utilisateur en conversation (« la problématique n'est pas claire du tout
qu'est-ce qu'on teste exactement... on se perd ») sur la clarté de la
"question posée" et de "ce qu'on évalue". Ce type de changement touche
l'angle éditorial (portée de "favorable/stable/dégradé", cadrage de la
question) — hors du mandat de la routine automatisée (`docs/routine-
inspection-prompt.md`), qui n'a jamais le droit d'y toucher seule.
Correction faite ici avec l'accord explicite de l'utilisateur ("Go"), pas
en autonomie.
**Diagnostic** : la "question posée" fusionnait deux dossiers distincts
(procès britannique sur des commotions passées vs nouvelle règle de
plaquage née en France, mondiale pour les amateurs seulement) sans jamais
préciser leur portée géographique respective — d'où la confusion
rapportée ("Le process, la règle, c'est en France, au UK, dans le
monde.."). Confusion secondaire sur le terme "contacts tête contre tête",
jamais expliqué malgré 4 occurrences dans l'article.
**Corrigé** (avec accord explicite, pas en autonomie) :
- `.question-text` et `.stakes-text` réécrits dans `index.html`,
  `archives/2026-08-16.html`, les 4 balises meta (`description`,
  `og:description`, `twitter:description`, JSON-LD) et `feed.xml`
  (`<comments>` + `<description>`) — pour nommer explicitement les deux
  dossiers et leur portée géographique (procès → justice britannique ;
  règle → née en France, mondiale amateurs seulement, pas encore élite).
  Chaque chiffre/date/nom propre/lien de cause à effet de la version
  d'origine conservé à l'identique, aucune information supprimée —
  seulement des précisions géographiques ajoutées et la question scindée
  en phrases plus courtes.
- Ajout d'une entrée de lexique "Contact tête contre tête" (`index.html` +
  archive) avec `.lex-ref` sur la première occurrence (baisse de -63 %
  mesurée en France) — 5 entrées désormais (ETC, choc sous-commotionnel,
  action de groupe, contact tête contre tête, HIA).
  Auto-vérification après application : balise HTML équilibrée
  (`html.parser`, aucune erreur), sync index/archive toujours limitée aux
  écarts légitimes, `feed.xml` toujours XML bien formé
  (`xml.dom.minidom`) — passée, correctifs commités.
**Limite honnête** : le contenu de `feed.xml` (question + "ce qu'on
évalue") a très probablement déjà été diffusé sur Telegram/Instagram/
Facebook/LinkedIn/newsletter avant cette conversation — mis à jour pour la
cohérence du flux et des lecteurs futurs, mais ne rattrape pas ce qui est
déjà parti.

---

## 2026-08-16 — Rugby : le choc de trop ?
**Vérifié** : cohérence interne (probabilités 20+45+35=100 %, `data-france-
impact`/`data-kind` vs texte `.france-line` pour les 3 cartes — favorable→
« Plutôt favorable », stable→« Neutre », dégradé→« Plutôt défavorable » —
et `data-kind="negatif"` du bloc `.delta-france` cohérent avec « léger
négatif »), présence des classes CSS attendues dans `<style>` (dont
`.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag`, bloc identique
à la version canonique de `docs/routine-inspection-prompt.md` une fois
commentaires et indentation normalisés) et intégrité du dégradé SVG à 3
stops avec `data-score`, sync `index.html` vs `archives/2026-08-16.html`
(`diff` complet — écarts : `og:url`/`mainEntityOfPage`, `aria-current` sur
la nav Accueil/Archives — tous légitimes), lexique (4 `.lex-ref` ↔ 4
entrées : ETC, choc sous-commotionnel, action de groupe, HIA — aucun terme
orphelin dans un sens ou l'autre), incohérence numérique interne (561
plaignants, 95 % de rejet potentiel, 63 % de baisse des contacts,
1 000+ anciens joueurs, 20/45/35 % — cohérents à chaque occurrence, aucun
faux positif type "9 vs 13,5 milliards"), label brut absent de
`.essentiel-text` (la seule occurrence de « stable » désigne le nom de la
carte de scénario, pas une description France non reformulée), formulation
« Notre évaluation de l'impact pour la France » intacte (jamais raccourcie
en "France Impact :"), rupture de registre (`grep` `\bton \|\bta \|\btu \b`
— une seule occurrence, dans `.share-block`, exception légitime), style des
paragraphes `.dek`/`.why`/`.essentiel-text` (3 phrases > 40 mots
retravaillées, voir ci-dessous), 3 chiffres vérifiés contre 3 sources sur 4
(voir signalements).
**Corrigé automatiquement** : rien (aucun problème mécanique détecté aux
points 1 à 7).
**Réécritures de clarté** (avant/après complet pour chacune) :
- Avant : « Après due diligence, Leigh Day (ou un autre cabinet) reprend
  officiellement le dossier avant la prochaine audience ; s'appuyant sur la
  position du juge Cook, qui a explicitement écarté toute responsabilité
  des plaignants, le tribunal accepte de sauver l'essentiel des 561
  premières plaintes malgré le vice de procédure de Richard Boardman. »
  Après : « Après due diligence, Leigh Day (ou un autre cabinet) reprend
  officiellement le dossier avant la prochaine audience. Le juge Cook a
  explicitement écarté toute responsabilité des plaignants ; en s'appuyant
  sur cette position, le tribunal accepte de sauver l'essentiel des 561
  premières plaintes malgré le vice de procédure de Richard Boardman. »
  (carte « Favorable », scission de la proposition participiale en
  suspens sur 15 mots avant son sujet réel — tous les chiffres/noms
  conservés à l'identique.)
- Avant : « Le Top 14 et le rugby d'élite n'y sont pas encore soumis : au-
  delà des premiers essais lancés avec le Championnat du monde U20 en
  Géorgie, les commotions des professionnels restent gérées par le
  protocole d'évaluation immédiate sur le terrain, le HIA*, sans
  changement de la hauteur de plaquage à ce niveau. »
  Après : « Le Top 14 et le rugby d'élite n'y sont pas encore soumis. Seule
  exception : les premiers essais lancés avec le Championnat du monde U20
  en Géorgie. En dehors de ce cas, les commotions des professionnels
  restent gérées par le protocole d'évaluation immédiate sur le terrain, le
  HIA*, sans changement de la hauteur de plaquage à ce niveau. »
  (paragraphe FFR, levée de l'ambiguïté de « au-delà de » — exception ou
  progression ? — en 3 phrases courtes plutôt qu'une ; renvoi lexique HIA
  conservé.)
- Avant : « En parallèle, la baisse des contacts tête contre tête mesurée
  en France depuis 2019 (-63 %) se confirme à l'échelle des dix fédérations
  qui ont suivi son exemple, et les premiers essais en élite (Championnat
  du monde U20) donnent des résultats encourageants qui ouvrent la voie à
  une extension au rugby professionnel. »
  Après : « En parallèle, la baisse des contacts tête contre tête mesurée
  en France depuis 2019 (-63 %) se confirme à l'échelle des dix fédérations
  qui ont suivi son exemple. Les premiers essais en élite (Championnat du
  monde U20) donnent aussi des résultats encourageants, qui ouvrent la voie
  à une extension au rugby professionnel. »
  (carte « Favorable », scission au point de coordination « et » entre
  deux faits distincts — chiffre -63 % et renvoi U20 conservés.)

  Auto-vérification après application (balise HTML équilibrée sur
  `index.html`/`archives/2026-08-16.html` via `html.parser`, aucune erreur ;
  re-diff index/archive toujours limité aux écarts légitimes) : passée,
  correctifs commités.
**Signalé pour revue humaine** :
- Source `rugbyamateur.fr` (World Rugby officialise l'abaissement de la
  hauteur de plaquage chez les amateurs) : l'article cite « plus de
  150 000 plaquages étudiés en deux ans », la source dit « rien que sur les
  18 derniers mois, 150 000 plaquages ont été analysés » — le chiffre
  (150 000) est exact, mais la période (18 mois ≈ 1,5 an, pas 2 ans) ne
  correspond pas exactement. Écart mineur sur une donnée secondaire (pas un
  des 2-3 chiffres centraux de l'article), signalé sans correction.
- Source `braininjurygroup.co.uk` (New Rugby Tackle Height Law 2026) : non
  re-vérifiable, `WebFetch` renvoie un contenu vide malgré 2 tentatives —
  signalé comme "source non re-vérifiable", pas de recherche de
  remplacement.
- Les 3 autres chiffres structurants vérifiés (95 % de rejet potentiel des
  plaintes + nom du juge Cook via Planète Rugby et Minute Sports ; « plus
  d'un millier d'anciens joueurs » via Minute Sports ; 63 % de baisse des
  contacts + « dix fédérations » via rugbyamateur.fr) correspondent tous à
  ce que disent les sources.

---

## 2026-08-15 — Traduction littéraire, le métier en sursis ?
**Vérifié** : cohérence interne (probabilités 20+50+30=100 %, `data-france-
impact`/`data-kind` vs texte `.france-line` pour les 3 cartes — favorable→
« Plutôt favorable », stable→« Neutre », dégradé→« Plutôt défavorable » —
et `data-kind="negatif"` du bloc `.delta-france` cohérent avec « léger
négatif »), présence des classes CSS attendues dans `<style>` (dont
`.delta-france`/`.delta-gauge*`/`.delta-word`/`.delta-flag`, bloc identique
à la version canonique de `docs/routine-inspection-prompt.md` une fois
commentaires et indentation normalisés) et intégrité du dégradé SVG à 3
stops avec `data-score`, sync `index.html` vs `archives/2026-08-15.html`
(`diff` complet — écarts : chemins relatifs `archives/` vs direct,
canonical/`og:url`/`mainEntityOfPage`, `aria-current`, et le lien interne
vers l'archive du 1er août — `archives/2026-08-01.html` dans `index.html`
contre `2026-08-01.html` dans l'archive, même schéma de chemin relatif que
les autres liens, confirmé cohérent avec le même type de lien dans
`archives/2026-08-12.html`/`13`/`14` — tous légitimes), lexique (5
`.lex-ref` ↔ 5 entrées, aucun terme orphelin dans un sens ou l'autre),
incohérence numérique interne (3 c€/9,6 c€ cohérents sur les 3 occurrences,
dates 8 avril/11 juin/décembre 2026 cohérentes partout, « une vingtaine »
vs « plusieurs dizaines » de traductrices explicitement attribuées à deux
sources différentes — pas une incohérence), label brut absent de
`.essentiel-text`, formulation « Notre évaluation de l'impact pour la
France » intacte, style des paragraphes `.dek`/`.why`/`.essentiel-text`
(plusieurs phrases de 40-52 mots mais lisibles ; une phrase à 74 mots dans
le `.dek` sur la loi Darcos correspond à un gabarit de renvoi « on avait
déjà vu passer un sujet similaire (...) n'hésite pas à lire notre article
(...) » réutilisé à l'identique sur plusieurs éditions passées — 2026-08-02,
2026-08-14 deux fois — traité comme un gabarit éditorial établi, pas une
maladresse isolée du jour, donc non retouché ; aucune rupture de registre,
`grep '\bton \|\bta \|\btu \b'` ne remonte que le `.share-block`, exception
légitime), 4 chiffres/faits structurants vérifiés contre les 4 sources
citées (voir détail ci-dessous).
**Corrigé automatiquement** : rien.
**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
aucune.
**Signalé pour revue humaine** : la date « Adoptée par le Sénat le 8 avril
2026 » (loi Darcos) n'a pu être confirmée par aucune des 4 sources citées —
Mind Media, la source la plus pertinente pour cette loi, ne couvre que le
blocage du 11 juin à l'Assemblée nationale (confirmé exact : « plus de 100
amendements ») sans mentionner l'étape sénatoriale. Pas une erreur avérée,
juste non re-vérifiable avec les sources disponibles ; plafond des 5
`WebFetch` atteint pour ce passage (2 appels sur Mind Media, 1 chacun sur
Livres Hebdo, Actualitté, Publishing Perspectives).
**Suivi (même jour, hors passage)** : signalement résolu — l'utilisateur a
transmis le dossier législatif officiel de l'Assemblée nationale
(`assemblee-nationale.fr/dyn/17/dossiers/DLR5L17N53359`), qui confirme
l'adoption au Sénat le **8 avril 2026** en première lecture (dépôt au Sénat
le 12 décembre 2025, rapport de commission le 1er avril, adoption le 8
avril, dépôt à l'Assemblée le 9 avril). La date publiée sur le site était
donc exacte ; aucune correction nécessaire. Chiffres vérifiés et
conformes aux sources : « 3 centimes du mot » (Livres Hebdo + Actualitté),
« une vingtaine (...) plusieurs dizaines » de traductrices (Livres Hebdo),
« 1,5 milliard de dollars » + « environ 3 000 dollars par livre » Anthropic
(Publishing Perspectives — léger écart de nuance, la source dit « as much
as $3,000 » (maximum) contre « environ » dans l'article, cohérent avec la
moyenne réelle 1,5 Md$/~500 000 œuvres ≈ 3 000 $, pas assez significatif
pour un signalement séparé), « 11 juin 2026 » + « plus de 100 amendements »
blocage Assemblée (Mind Media, exact). Limite horaire notée pour mémoire :
édition publiée ~1h avant ce passage, posts sociaux déjà partis via
`feed.xml` au moment de l'inspection — sans conséquence aujourd'hui
puisqu'aucune correction n'a été nécessaire.

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
- ~~Source Météo-France (bilan climatique juin 2026, citée en bas de page)
  injoignable — `WebFetch` renvoie une erreur HTTP 503.~~ **Résolu le même
  jour** (retenté hors passage automatique, sur demande de l'utilisateur) :
  la source répond maintenant. Les 3 faits qu'elle appuie correspondent à
  l'article — 72 départements en vigilance rouge canicule le 25 juin,
  pointes >40°C (43,8°C à Saintes, 42,7°C à Cognac, 42,5°C à Bordeaux),
  "totalement inédit depuis la création de la Vigilance Canicule en 2004".
  Rien à corriger. Signalement clos, plus rien en attente sur cette
  édition.
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

## 2026-08-25 (correction en direct, post-inspection) — chiffre de trafic chinois obsolète
**Contexte** : suite au passage automatique du matin (voir entrée ci-dessus,
signalement sur l'écart 45 %/59,6 %), l'utilisateur a demandé une
vérification complémentaire en conversation directe, avec des pistes
apportées par un autre assistant (Grok) à confirmer avant toute correction.
**Vérifié** (recherche web + `WebFetch` sur sources primaires, hors budget
de la routine automatique puisque conversation directe) : la part chinoise
du trafic OpenRouter (développeurs/entreprises, même périmètre que
l'article) a largement dépassé 45 % depuis avril 2026 — Dataconomy (25
février 2026) la donne déjà à 61 %, eWeek/Bloomberg (24 juillet 2026) à
60 % avec un pic à 63 % début juillet. Confirmé par plusieurs titres
indépendants (Yahoo Finance, Fortune, TechBriefly) sur la même période.
Le chiffre « désormais 45 % » de `.essentiel-text` (repris tel quel dans
`feed.xml`) était donc obsolète au moment de la publication — contrairement
au signalement du matin, l'écart n'était pas une ambiguïté de périmètre
mais une vraie donnée périmée. La répartition par labo du `.list-box`
(somme 59,6 %) s'est révélée être la donnée la plus proche de la réalité.
**Corrigé** (urgence : diffusion `feed.xml` imminente) : `.essentiel-text`
et le `.dek` d'`index.html`/`archives/2026-08-25.html`, ainsi que le texte
équivalent dans `feed.xml`, mis à jour vers « plus de 60 % » (sourcé
Dataconomy/Bloomberg), en conservant explicitement la mention « 45 % en
avril 2026 » pour ne pas perdre le point de comparaison historique déjà
présent. **Non touché, volontairement** : les probabilités des 3
scénarios, leurs `.evo-current`/`.evo-prev` (base « 45 %, référence avril
2026 »), le texte `.why`/`.france-line` des cartes — ce sont des choix
éditoriaux, hors mandat de cette correction.
**Question de fond transmise à la rédaction, non tranchée ici** : la base
de départ du tableau d'indicateurs (45 %, avril 2026) sert de référence aux
3 scénarios projetés (40 %/58 %/70 %) ; si le trafic réel dépassait déjà
58-63 % au moment de la publication, le scénario « stable » (le plus
probable, 45 %) décrit peut-être un état déjà largement atteint plutôt
qu'une trajectoire encore incertaine. À réévaluer par la rédaction, pas par
cette correction ponctuelle.
