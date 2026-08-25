# Prompt de la routine « Scénario — Pub hebdo »

Ce fichier est la copie de référence du prompt envoyé par la routine "pub"
(Claude Code Remote, trigger **« Scénario — Pub hebdo »**,
`trig_01A1XU5Kpc4QWzApjZPqcKpj`, cron **quotidien** (`0 2 * * *` UTC =
4h Paris heure d'été) depuis le 17 août — l'utilisateur est passé de 5
jours/semaine à tous les jours, voir `docs/ARCHITECTURE.md`). Créé par un
agent (`create_trigger`), donc directement éditable via `update_trigger`
— ce fichier reste la source de vérité lisible par un humain : le mettre
à jour dans la foulée de tout changement.

**17 août : cron passé à quotidien par l'utilisateur** (résout la note
précédente sur lundi, qui restait dormant faute de déclenchement — ce
n'est plus le cas). Table jour → catégorie complétée en conséquence
(mercredi ajouté) et repli explicite ajouté pour tout jour qui y
manquerait quand même (voir point 2 ci-dessous) : consigne utilisateur du
17 août, remplace l'ancien réflexe "s'arrêter et signaler" par défaut sur
`chiffre` plutôt que de bloquer la routine.

**21 août : catégorie `futur` mise en pause, remplacée par `chiffre` le
jeudi.** Retour utilisateur direct : abandon de "Grand futur" pour
l'instant. Table jour → catégorie mise à jour (point 2 ci-dessous) —
`futur` n'est plus assignée à aucun jour, même traitement que `question`
(catégorie dormante, pas supprimée : le mécanisme de recherche du point 6
et les entrées déjà présentes dans `docs/pub-messages.md` section 4
restent en place, prêts à être réactivés plus tard).

**Objectif : rappeler l'identité du projet et faire réagir la communauté**
entre deux éditions quotidiennes — jamais un sujet d'actualité (ça reste le
rôle de `feed.xml`). Contenu organique, pas de budget publicitaire (à ne
pas confondre avec la piste "pub payante" listée séparément dans
`docs/ARCHITECTURE.md`).

**Cadence : quotidienne depuis le 17 août** (auparavant 1x/semaine en
croisière, plus fréquente au lancement). Pas de logique de fréquence dans
ce prompt — la cadence réelle est pilotée uniquement par le cron du
trigger, ajusté à la main par l'utilisateur. Ancien garde-fou anti-doublon
(20h minimum entre deux publications) retiré le 15 août à la demande de
l'utilisateur — la routine publie désormais à chaque déclenchement, sans
vérifier l'écart avec la dernière publication.

**Économie de tokens** — même logique que `docs/routine-inspection-
prompt.md` : le choix de la catégorie, de l'entrée et de la photo (étapes
1 à 3) est **entièrement déterministe** (lecture de fichiers + petits
scripts, aucun jugement éditorial requis) — ne pas "réfléchir" dessus,
suivre la procédure telle quelle. Le seul endroit qui demande un peu de
jugement est la rédaction du texte du post final (étape 5), et encore :
il recopie du texte déjà écrit, il ne compose rien depuis zéro.
**Exception : la catégorie `futur`** (étape 1, point 6) peut demander une
vraie recherche (WebFetch, 3 appels max, uniquement quand c'est son tour
dans le cycle) — volontaire, pour éviter qu'une liste figée devienne
prévisible, voir la justification dans cette section. **Catégorie
dormante depuis le 21 août** (voir note en tête de fichier) : ce point
reste décrit ici pour le jour où elle sera réactivée, mais ne se
déclenche plus en pratique tant que `futur` n'a pas de jour dans la
table du point 2.

---

**La cible du push est toujours `main`, sans exception** — même si
l'environnement d'exécution assigne une autre branche de session par
défaut (ex. `claude/xxx`) : y committer n'est pas une alternative, `main`
reste la seule cible de contenu.

**Avant de commencer : `git pull origin main`.**

**Après le push sur `main` (étape 5) : pousser aussi la branche de
session locale vers son propre remote** (`git push -u origin
{nom-de-la-branche-de-session}`), pour satisfaire le stop hook local qui
signale les commits non poussés sur cette branche — ajouté le 15 août
après un retour utilisateur ("assure-toi que ce sera fait la prochaine
fois"). C'est un simple miroir de suivi, jamais une pull request, et ça
ne change rien à la cible réelle (`main`, déjà à jour à ce stade).

## Étape 1 — Déterminer la catégorie et l'entrée

1. Lister tous les `<guid>` de `feed-pub.xml`, format `scenario-pub-
   {id-entrée}` (ex. `scenario-pub-manifeste-03`) — le préfixe avant le
   premier tiret après "pub-" donne la catégorie (`manifeste`, `citation`,
   `question`, `futur`, `chiffre`).
2. **Catégorie du jour : table jour → catégorie fixe** (remplace
   l'ancien mécanisme "cycle qui avance d'un cran", retour utilisateur du
   14 août — trop de risque de se tromper en déduisant la catégorie du
   dernier item publié). Déterminer le jour de la semaine **à l'heure de
   Paris** au moment du déclenchement, puis :

   | Jour | Catégorie |
   |---|---|
   | Dimanche | `manifeste` |
   | Lundi | `chiffre` |
   | Mardi | `citation` |
   | Mercredi | `chiffre` |
   | Jeudi | `chiffre` |
   | Vendredi | `manifeste` |
   | Samedi | `chiffre` |

   **18 août — catégorie "soutien" (Buy Me a Coffee) testée un temps sur
   samedi, puis repliée dans `manifeste`** (retour utilisateur direct :
   pas de jour dédié, juste une entrée de plus dans la rotation
   `manifeste`) — voir `manifeste-11` dans `docs/pub-messages.md`. Samedi
   redevient donc `chiffre` comme avant le 18 août. **1 seul post/jour,
   sans exception** — reste vrai en général : n'ajouter aucune catégorie
   en plus de celle du jour (leçon du 18 août : une première tentative
   avait publié 2 items le même jour et cassé l'automatisation réseaux
   sociaux, qui ne traite qu'1 post/jour).

   **`question` et `futur` ne sont pas dans cette table — catégories
   dormantes**, pas supprimées : leurs entrées restent dans `docs/pub-
   messages.md` (sections 3 et 4), à réactiver si l'utilisateur leur
   redonne un jour (`futur` retirée de la table le 21 août, jeudi
   reprend désormais `chiffre` — voir la note en tête de fichier). **Si
   la routine se déclenche malgré tout un jour absent de cette table**
   (nouveau jour de la semaine ajouté au cron sans que cette table soit
   mise à jour) :
   consigne du 17 août, remplace l'ancien réflexe "s'arrêter et signaler"
   — **utiliser `chiffre` par défaut** pour ce jour plutôt que de bloquer
   la routine, et le mentionner quand même dans le résumé final (étape 5)
   pour que l'écart de doc soit visible et corrigé.
3. Dans `docs/pub-messages.md`, section de cette catégorie : lister les
   entrées dans l'ordre où elles apparaissent, **en écartant celles encore
   marquées `[à confirmer]` / `[attribution à vérifier]` / `[à
   vérifier]`** — ne jamais publier une entrée non validée, quel que soit
   son tour dans la rotation. Pour la catégorie `futur` en particulier,
   vérifier aussi que le texte recopié est bien
   **au conditionnel** ("pourrait", "devrait" — jamais "sera", "va
   révolutionner") : une entrée à l'indicatif/futur simple ne doit jamais
   être publiée telle quelle, même si elle n'est plus marquée `[à
   vérifier]` (erreur de relecture possible lors de la validation). Comme
   `futur`, la catégorie `chiffre` n'est pas une simple liste à parcourir
   — passer directement au point 7 ci-dessous pour son mécanisme propre.
4. Parmi les entrées restantes de cette catégorie : trouver l'id du
   dernier `<guid>` publié dans cette catégorie (peut remonter à plusieurs
   items en arrière dans `feed-pub.xml`, puisque les catégories
   alternent). L'entrée à publier aujourd'hui est **la suivante dans
   l'ordre du fichier après celle-là** (retour au début de la liste si on
   était sur la dernière) — jamais répéter avant d'avoir fait le tour
   complet de la catégorie. Si la catégorie n'a jamais été publiée, prendre
   la première entrée de la liste.
5. **Si toutes les entrées d'une catégorie sont encore marquées comme non
   validées, ou si la section est vide** (aucune disponible) : passer à
   la catégorie suivante du cycle pour cette exécution, et le signaler
   dans le résumé final —
   jamais bloquer toute la routine pour ça, jamais publier une entrée non
   validée pour combler.
6. **Cas particulier de la catégorie `futur` — pas une simple rotation
   fermée** (retour utilisateur du 13 août : une liste qui tourne en
   boucle devient vite prévisible pour cette catégorie précise). Deux
   options, dans cet ordre de préférence :
   - **a) Rechercher et rédiger un nouveau fait.** WebFetch une source
     fiable (media scientifique/économique sérieux, organisme officiel,
     publication de recherche — jamais un blog ou un site non identifié),
     **3 appels WebFetch maximum** pour cette étape. Le fait doit être
     **précis, daté, spécifique** — jamais une généralité déjà connue
     (voir la règle "pas de trucs bateau" dans `docs/pub-messages.md`,
     section 4) — et rédigé **au conditionnel** pour tout ce qui n'est
     pas encore arrivé. Si trouvé et vérifié : l'ajouter en tant que
     nouvelle entrée à la fin de la section 4 de `docs/pub-messages.md`
     (id suivant non utilisé, `futur-{N}`), **avec sa source (URL) en
     plus de l'`attribution`** habituelle, dans le même commit que la
     publication du post. Utiliser cette entrée pour le post du jour.
   - **b) Repli sur la liste existante.** Si la recherche ne trouve rien
     d'assez solide dans le budget de 3 appels, ou si le sujet trouvé
     ressemble trop à une entrée déjà publiée récemment : reprendre une
     entrée déjà en liste (même logique de rotation que les autres
     catégories, étape 4 ci-dessus) plutôt que de bloquer ou de publier
     un fait mal vérifié. **Au 13 août, la section 4 de `docs/pub-
     messages.md` est vide** (entrées initiales retirées, aucune
     vérifiée) — ce repli n'est donc pas disponible tant qu'au moins une
     entrée n'a pas été ajoutée par l'option a). Si la recherche échoue
     et qu'aucun repli n'existe : passer à la catégorie suivante du cycle
     pour cette exécution et le signaler dans le résumé final (même
     traitement que l'étape 1, point 5, pour les autres catégories).
   - Dans les deux cas, jamais de fait inventé sans source — la seule
     différence avec les 4 autres catégories est que la source peut être
     trouvée au moment de la publication plutôt qu'être uniquement
     pré-validée en session.
7. **Cas particulier de la catégorie `chiffre` — extraction, jamais
   génération** (réintroduite le 14 août, voir `docs/pub-messages.md`
   section 5 pour le détail complet). Contrairement à `futur`, aucune
   recherche externe : le chiffre vient toujours d'une édition déjà
   publiée sur le site, donc déjà vérifiée par le processus éditorial
   normal.
   - **a) Lister les éditions récentes.** Parcourir `archives/*.html` des
     ~30 derniers jours, en excluant celles publiées il y a moins de 24h
     (laisser le temps d'un passage Inspecteur avant réutilisation) et
     celles dont un chiffre a déjà servi dans un post `chiffre` précédent
     (déduit des `<link>` déjà présents dans les items `scenario-pub-
     chiffre-*` de `feed-pub.xml`).
   - **b) Repérer les phrases à chiffre fort.** Dans les paragraphes
     `.dek` et `.essentiel-text` de chaque édition candidate, chercher les
     phrases contenant un `<strong>` autour d'un chiffre (%, montant,
     nombre de personnes, date marquante...). Écarter les chiffres
     purement techniques sans impact narratif (ex. un simple numéro
     d'article de loi) — privilégier ceux qui frappent (pertes humaines,
     ampleur financière, record historique...). **Préférer `.essentiel-
     text` à `.dek`** quand les deux ont un candidat valable : c'est déjà
     la version résumée/simplifiée de l'édition, donc plus proche du ton
     recherché ici.
   - **c) Choisir simple, court, pédagogique — et recopier tel quel.**
     Retenue **pas seulement la plus marquante, mais celle qui se
     comprend seule, en une lecture, sans connaître le reste de
     l'édition** (règle explicite du 14 août : "les phrases doivent être
     simples, assez courtes et pédagogiques"). Écarter les phrases à
     clauses multiples, jargon non expliqué, ou qui empilent plusieurs
     chiffres à la fois — une seule idée, un seul chiffre, une phrase
     qu'on comprend en scrollant. Si la phrase candidate est trop longue
     mais contient un segment autonome et complet (ex. une proposition
     séparée par une virgule qui a son sens toute seule), il est permis
     de **ne garder que ce segment** — jamais reformulé, jamais un mot
     changé ou ajouté, seulement raccourci à une frontière naturelle
     (virgule, point-virgule), avec au besoin une majuscule initiale et
     un point final ajoutés pour qu'il se lise comme une phrase complète.
     **Le chiffre lui-même n'est jamais recalculé ni arrondi
     différemment.** Extraire le chiffre seul pour le champ `stat`,
     garder la phrase (ou le segment) retenu pour `message`.
   - **d) Journaliser.** Ajouter l'entrée utilisée à la fin de la
     section 5 de `docs/pub-messages.md` (id `chiffre-{AAAA-MM-JJ}`,
     jamais réutilisé), avec le lien vers l'édition source, dans le même
     commit que la publication du post.
   - **e) Si aucune édition candidate n'a de chiffre exploitable** (rare) :
     passer à la catégorie suivante du cycle pour cette exécution, même
     traitement que l'étape 1, point 5.

## Étape 2 — Choisir la photo (jamais de recherche Pexels en direct)

**Catégorie `chiffre` : mécanisme dédié, pas la rotation ci-dessous**
(changé le 15 août, retour utilisateur — le fond doit être la photo de
l'édition dont le chiffre est extrait, pas une photo de banque
générique sans rapport direct). `pub-template-v5-stat.html` utilise
désormais une photo :
1. Chemin déterministe : `assets/social/topic-images/{date de l'édition
   source, AAAA-MM-JJ}.jpg`, avec son `.json` associé pour le crédit
   (`photographer`, `pexels_url`) — la même image que celle déjà
   utilisée par l'édition elle-même sur le site, jamais une recherche
   ou un autre choix.
2. Si cette édition n'a pas (ou plus) de fichier `.jpg`/`.json`
   correspondant dans `assets/social/topic-images/` (rare, les images
   les plus anciennes peuvent avoir été purgées) : revenir à l'étape 1,
   point 7a, et écarter cette édition candidate au profit de la
   suivante qui a bien son image associée. Si aucune édition candidate
   sur les ~30 jours n'a de `.jpg`/`.json` associé : replier sur la
   règle générale ci-dessous (points 1-2) comme pour les autres
   catégories plutôt que de bloquer.
3. Passer directement à l'étape 3 avec cette photo (jamais l'étape 2,
   points 1-2 ci-dessous, sauf repli du point 2 ci-dessus).

**Règle non négociable, héritée de `scripts/social/fetch_topic_image.py`**
(catégories `manifeste`/`citation`/`question`/`futur`, et repli `chiffre`
ci-dessus) :
cette routine ne cherche et ne choisit jamais une photo sur Pexels
elle-même. Elle réutilise uniquement une image déjà validée par un humain.

1. Regarder `assets/social/topic-images/` : parmi les fichiers `{date}.jpg`
   des 7 derniers jours qui ont un `.json` associé (photographe connu),
   préférer celui qui n'a pas déjà servi à un post `feed-pub.xml` récent
   (grep les commentaires HTML `<!-- credit: -->` du flux, voir étape 4).
   Si tous ont déjà servi, réutiliser quand même le plus récent — mieux
   qu'aucune image.
2. Si aucune photo n'existe dans les 7 derniers jours : utiliser la
   banque de secours pré-validée, `assets/social/pub-photos/` — un
   paysage par registre (`geopolitique.jpg`, `carte-blanche.jpg`,
   `actualite-francaise.jpg`, `economie-mondiale.jpg`, `sciences.jpg`,
   `culture.jpg`, `sport.jpg`), crédits dans le `credits.json` du même
   dossier (liste d'objets `file`/`photographer`/`pexels_url`, même
   format que `assets/social/topic-images/`). Prendre celle qui
   correspond au registre du jour de publication (voir la grille
   `docs/routine-prompt.md`, Étape 1, pour associer le jour de la
   semaine au registre) — si le jour ne tombe sur aucun registre fixe
   (cas rare), prendre la photo du registre le moins utilisé récemment
   dans `feed-pub.xml`. Si même cette banque de secours est vide ou
   introuvable, s'arrêter sans publier et le signaler dans le résumé
   final plutôt que de publier sans image ou d'improviser une recherche
   Pexels.
3. Noter le chemin de la photo choisie et le contenu de son `.json`
   (`photographer`, `pexels_url`) pour l'étape 4.

## Étape 3 — Générer l'image

Pour les catégories `manifeste`/`citation`/`question`/`futur` :
```
python3 scripts/social/generate_pub_image.py \
  --data {json temporaire avec eyebrow/message/attribution/cta de l'entrée choisie, "accent": "{catégorie}"} \
  --output assets/social/pub/{AAAA-MM-JJ}.png \
  --template scripts/social/pub-template-v4-hybride.html \
  --photo {photo choisie à l'étape 2}
```

Pour la catégorie `chiffre` — gabarit dédié, `--photo` = photo de
l'édition source (étape 2 ci-dessus, jamais une autre photo) :
```
python3 scripts/social/generate_pub_image.py \
  --data {json temporaire avec eyebrow/stat/message/attribution/cta de l'entrée extraite} \
  --output assets/social/pub/{AAAA-MM-JJ}.png \
  --template scripts/social/pub-template-v5-stat.html \
  --photo assets/social/topic-images/{date de l'édition source}.jpg
```

`eyebrow`/`message`/`attribution`/`cta` (et `stat` pour la catégorie
`chiffre`) sont recopiés **tels quels** depuis `docs/pub-messages.md` —
jamais reformulés, jamais traduits, jamais "améliorés" à la volée.

**Principe à respecter : jamais d'URL écrite en dur sur l'image**
(retour utilisateur du 18 août, entrée `manifeste-11` "Soutenez
Scénario") — une image PNG
n'est pas cliquable, une URL affichée dessus est donc inutile voire
trompeuse (elle donne l'impression d'un lien alors qu'il faut la
retaper à la main). Si le `cta` d'une entrée contient une URL, utiliser
pour l'image le champ `cta-image` de cette entrée s'il existe (variante
sans URL, voir `docs/pub-messages.md` section 6 pour l'exemple), et
garder `cta` (avec l'URL) pour `<comments>`/`<description>` à l'étape 4
— c'est là, dans le texte du post sous l'image, que l'URL est cliquable
ou copiable. Sans `cta-image` disponible pour une entrée qui en aurait
besoin, ne pas en improviser un à la volée : signaler le manque dans le
résumé final plutôt que d'écrire une URL sur l'image.

## Étape 4 — Construire l'item `feed-pub.xml`

**Mettre à jour `<lastBuildDate>` du `<channel>`** (juste après
`<language>`) avec la date/heure actuelles, même format RFC 822 que les
`<pubDate>` — à chaque publication, sans exception, même règle que
l'ajout d'item ci-dessous.

Ajouter en tête (le plus récent en premier, jamais réordonner les items
existants) :

```xml
<item>
  <title>{message de l'entrée, \n remplacés par un espace, ** retirés, tronqué proprement si besoin}</title>
  <link>{lien selon la catégorie, voir ci-dessous}</link>
  <guid isPermaLink="false">scenario-pub-{id-entrée}-{AAAA-MM-JJ}</guid>
  <pubDate>{date/heure actuelles, format RFC 822, fuseau Europe/Paris}</pubDate>
  <comments>{eyebrow}\n\n{message sans **}{, \n\nattribution si présente}{\n\ncta si présent}</comments>
  <enclosure url="https://lesscenarios.fr/assets/social/pub/{AAAA-MM-JJ}.png" length="{taille réelle du fichier}" type="image/png"/>
  <description><![CDATA[{même contenu que <comments>, mise en forme <br> au lieu de \n}<!-- credit: {photographer} — {pexels_url} -->]]></description>
</item>
```

**Le CTA doit être dans `<comments>`, pas seulement dans `<description>`**
(corrigé le 13 août, bug repéré en relisant le blueprint Make de
l'utilisateur) — les 4 modules réseaux (Twitter/Facebook/LinkedIn/
Instagram) utilisent tous `{{comments}}` pour le texte du post, jamais
`{{description}}`. Un CTA absent de `<comments>` ne serait donc **jamais
posté nulle part**, alors que le CTA est justement l'élément central de
la règle "dénominateur commun" (voir `docs/pub-messages.md`) — sans lui,
chaque post perd sa raison d'être orientée croissance.

**Lien selon la catégorie** : `manifeste` → `https://lesscenarios.fr/le-
projet.html`, `citation`/`futur` → `https://lesscenarios.fr/`,
`question` → `https://lesscenarios.fr/contact.html`, `chiffre` → l'URL de
l'édition source elle-même (ex. `https://lesscenarios.fr/archives/2026-
08-10.html`) — seule catégorie qui ne renvoie pas vers une page fixe,
puisque chaque post cite une édition différente.

**Exception : champ `link` sur une entrée précise, dans
`docs/pub-messages.md`** (ajouté le 18 août, `manifeste-11`) — quand une
entrée a besoin de pointer ailleurs que le lien par défaut de sa
catégorie (ex. une entrée `manifeste` qui doit renvoyer vers
`buymeacoffee.com/scenario` plutôt que `le-projet.html`), ce champ
optionnel prime sur la règle générale ci-dessus. Vérifier sa présence
avant d'appliquer le lien par défaut de la catégorie ; l'utiliser tel
quel, jamais reformulé.

**Le crédit photo n'apparaît JAMAIS dans le texte visible du post**
(ni `<comments>`, ni le texte lisible de `<description>`) — décision
utilisateur du 13 août : le crédit est ajouté à la main par l'utilisateur
en commentaire du post une fois publié, pas par cette routine. Le
commentaire HTML `<!-- credit: ... -->` en fin de `<description>` sert
uniquement à ce que la routine (et l'utilisateur, en lisant le flux) sache
quelle photo/quel photographe a été utilisé — invisible dans un lecteur
RSS ou sur les réseaux, jamais affiché publiquement par ce mécanisme.

**Garde-fou obligatoire : valider le XML avant tout commit** (ajouté le
25 août — incident réel : l'item `citation-03` du 25 août avait été
écrit avec un CDATA non fermé sur `<description>` — `]]>` manquant
avant `</description>`. Ce genre d'erreur ne casse pas le XML au sens
strict — `xmllint --noout` ne remonte aucune erreur, un CDATA mal fermé
reste syntaxiquement valide, juste mal "scopé" — mais un CDATA ouvert
avale tout le texte qui suit, y compris l'`<item>` entier suivant, qui
disparaît alors pour tout parseur XML strict, dont celui utilisé par
Make côté automatisation réseaux sociaux : l'édition suivante n'était
donc jamais postée, sans qu'aucune erreur ne soit visible dans le
fichier lui-même. Repéré seulement parce que l'utilisateur a remarqué
l'absence d'un item dans Make.**

Après avoir écrit le nouvel item (et avant `git add`/`git commit`),
valider systématiquement avec ce script (jamais sauter cette étape,
même si la modification semble triviale) :

```python
import xml.etree.ElementTree as ET
tree = ET.parse("feed-pub.xml")
items = tree.getroot().find("channel").findall("item")
assert len(items) == {nombre d'items avant ajout} + 1, f"attendu {n+1}, trouvé {len(items)}"
# vérifier que le nouvel item ne contient pas le texte d'un autre item
# (signe d'un CDATA/tag mal fermé qui aurait tout avalé)
guids = [it.find("guid").text for it in items]
assert len(guids) == len(set(guids)), "guid en double"
print("OK —", len(items), "items, tous distincts")
```

Si l'assertion échoue (nombre d'items inattendu, ou contenu d'un item
qui déborde visiblement sur le suivant en le lisant) : **ne pas
committer**, chercher la balise mal fermée (`]]>` manquant sur une
`<description>` en CDATA est la cause la plus probable, vue l'incident
du 25 août) et corriger avant de relancer la validation. Un
`xmllint --noout feed-pub.xml` qui passe **ne suffit pas** à lui seul —
il ne détecte pas ce type d'erreur, voir l'incident ci-dessus.

## Étape 5 — Résumé final

Toujours terminer par un message court et explicite :
- Catégorie et entrée publiées (id).
- Photo utilisée + **le nom du photographe et le lien Pexels, en clair,
  pour que l'utilisateur puisse le recopier en commentaire du post** —
  c'est le seul endroit où cette information doit apparaître en texte
  visible dans la réponse de la routine.
- Si une catégorie a été sautée faute d'entrée validée (étape 1.5), ou si
  la routine s'est arrêtée faute de photo (étape 2.2), le dire
  explicitement plutôt que de rester silencieux.

Commit avec un message préfixé `[pub]`, push sur `main`, puis pousser la
branche de session locale vers son propre remote (voir la note en tête
de fichier) — dans cet ordre, `main` reste la cible de contenu, la
branche de session n'est qu'un miroir.
