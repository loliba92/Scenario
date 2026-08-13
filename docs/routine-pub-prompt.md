# Prompt de la routine « Scénario — Pub hebdo »

Ce fichier est la copie de référence du prompt envoyé par la routine "pub"
(Claude Code Remote, trigger **« Scénario — Pub hebdo »**, `{id à
compléter une fois le trigger créé}`). Créé par un agent
(`create_trigger`), donc directement éditable via `update_trigger` — ce
fichier reste la source de vérité lisible par un humain : le mettre à jour
dans la foulée de tout changement.

**Objectif : rappeler l'identité du projet et faire réagir la communauté**
entre deux éditions quotidiennes — jamais un sujet d'actualité (ça reste le
rôle de `feed.xml`). Contenu organique, pas de budget publicitaire (à ne
pas confondre avec la piste "pub payante" listée séparément dans
`docs/ARCHITECTURE.md`).

**Cadence : 1x/semaine en croisière, plus fréquente au lancement.** Pas de
logique de fréquence dans ce prompt — la cadence réelle est pilotée
uniquement par le cron du trigger, ajusté à la main par l'utilisateur.
Cette routine n'a qu'une règle de sécurité (étape 0) pour éviter un doublon
si elle est déclenchée deux fois trop rapprochées.

**Économie de tokens** — même logique que `docs/routine-inspection-
prompt.md` : le choix de la catégorie, de l'entrée et de la photo (étapes
1 à 3) est **entièrement déterministe** (lecture de fichiers + petits
scripts, aucun jugement éditorial requis) — ne pas "réfléchir" dessus,
suivre la procédure telle quelle. Le seul endroit qui demande un peu de
jugement est la rédaction du texte du post final (étape 5), et encore :
il recopie du texte déjà écrit, il ne compose rien depuis zéro.
**Exception : la catégorie `futur`** (étape 1, point 6) peut demander une
vraie recherche (WebFetch, 3 appels max, uniquement quand c'est son tour
dans le cycle — 1 fois sur 5) — volontaire, pour éviter qu'une liste figée
devienne prévisible, voir la justification dans cette section.

---

**La cible du push est toujours `main`, sans exception.**

**Avant de commencer : `git pull origin main`.**

## Étape 0 — Garde-fou anti-doublon

Lire le `<pubDate>` du premier `<item>` de `feed-pub.xml` (le plus récent,
toujours en tête). S'il date de moins de 20h, s'arrêter proprement sans
rien publier — protège contre un double déclenchement rapproché, sans
verrouiller une cadence figée (contrairement à `docs/routine-hebdo-
prompt.md` qui vérifie "cette semaine civile" : ici la fréquence peut
changer, un simple délai minimal suffit).

## Étape 1 — Déterminer la catégorie et l'entrée

1. Lister tous les `<guid>` de `feed-pub.xml`, format `scenario-pub-
   {id-entrée}` (ex. `scenario-pub-manifeste-03`) — le préfixe avant le
   premier tiret après "pub-" donne la catégorie (`manifeste`, `citation`,
   `question`, `chiffre`, `futur`).
2. **Catégorie du jour** : cycle fixe `manifeste → citation → question →
   chiffre → futur → manifeste...`. Prendre la catégorie du `<guid>` le
   plus récent (premier `<item>`), avancer d'un cran dans le cycle. Si
   `feed-pub.xml` n'a encore aucun item, commencer par `manifeste`.
3. Dans `docs/pub-messages.md`, section de cette catégorie : lister les
   entrées dans l'ordre où elles apparaissent, **en écartant celles encore
   marquées `[à confirmer]` / `[attribution à vérifier]` / `[chiffre à
   vérifier]` / `[à vérifier]`** — ne jamais publier une entrée non
   validée, quel que soit son tour dans la rotation. Pour la catégorie
   `futur` en particulier, vérifier aussi que le texte recopié est bien
   **au conditionnel** ("pourrait", "devrait" — jamais "sera", "va
   révolutionner") : une entrée à l'indicatif/futur simple ne doit jamais
   être publiée telle quelle, même si elle n'est plus marquée `[à
   vérifier]` (erreur de relecture possible lors de la validation).
4. Parmi les entrées restantes de cette catégorie : trouver l'id du
   dernier `<guid>` publié dans cette catégorie (peut remonter à plusieurs
   items en arrière dans `feed-pub.xml`, puisque les catégories
   alternent). L'entrée à publier aujourd'hui est **la suivante dans
   l'ordre du fichier après celle-là** (retour au début de la liste si on
   était sur la dernière) — jamais répéter avant d'avoir fait le tour
   complet de la catégorie. Si la catégorie n'a jamais été publiée, prendre
   la première entrée de la liste.
5. **Si toutes les entrées d'une catégorie sont encore marquées comme non
   validées** (aucune disponible) : passer à la catégorie suivante du
   cycle pour cette exécution, et le signaler dans le résumé final —
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
     section 5) — et rédigé **au conditionnel** pour tout ce qui n'est
     pas encore arrivé. Si trouvé et vérifié : l'ajouter en tant que
     nouvelle entrée à la fin de la section 5 de `docs/pub-messages.md`
     (id suivant non utilisé, `futur-{N}`), **avec sa source (URL) en
     plus de l'`attribution`** habituelle, dans le même commit que la
     publication du post. Utiliser cette entrée pour le post du jour.
   - **b) Repli sur la liste existante.** Si la recherche ne trouve rien
     d'assez solide dans le budget de 3 appels, ou si le sujet trouvé
     ressemble trop à une entrée déjà publiée récemment : reprendre une
     entrée déjà en liste (même logique de rotation que les autres
     catégories, étape 4 ci-dessus) plutôt que de bloquer ou de publier
     un fait mal vérifié.
   - Dans les deux cas, jamais de fait inventé sans source — la seule
     différence avec les 4 autres catégories est que la source peut être
     trouvée au moment de la publication plutôt qu'être uniquement
     pré-validée en session.

## Étape 2 — Choisir la photo (jamais de recherche Pexels en direct)

**Règle non négociable, héritée de `scripts/social/fetch_topic_image.py`** :
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

```
python3 scripts/social/generate_pub_image.py \
  --data {json temporaire avec eyebrow/message/attribution/cta de l'entrée choisie, "accent": "{catégorie}"} \
  --output assets/social/pub/{AAAA-MM-JJ}.png \
  --template scripts/social/pub-template-v4-hybride.html \
  --photo {photo choisie à l'étape 2}
```

`eyebrow`/`message`/`attribution`/`cta` sont recopiés **tels quels** depuis
`docs/pub-messages.md` — jamais reformulés, jamais traduits, jamais
"améliorés" à la volée.

## Étape 4 — Construire l'item `feed-pub.xml`

Ajouter en tête (le plus récent en premier, jamais réordonner les items
existants) :

```xml
<item>
  <title>{message de l'entrée, \n remplacés par un espace, ** retirés, tronqué proprement si besoin}</title>
  <link>{lien selon la catégorie, voir ci-dessous}</link>
  <guid isPermaLink="false">scenario-pub-{id-entrée}-{AAAA-MM-JJ}</guid>
  <pubDate>{date/heure actuelles, format RFC 822, fuseau Europe/Paris}</pubDate>
  <comments>{eyebrow}\n\n{message sans **}{, \n\nattribution si présente}</comments>
  <enclosure url="https://lesscenarios.fr/assets/social/pub/{AAAA-MM-JJ}.png" length="{taille réelle du fichier}" type="image/png"/>
  <description><![CDATA[{même contenu que <comments>, mise en forme <br> au lieu de \n}{cta si présent}<!-- credit: {photographer} — {pexels_url} -->]]></description>
</item>
```

**Lien selon la catégorie** : `manifeste` → `https://lesscenarios.fr/le-
projet.html`, `citation`/`chiffre`/`futur` → `https://lesscenarios.fr/`,
`question` → `https://lesscenarios.fr/contact.html`.

**Le crédit photo n'apparaît JAMAIS dans le texte visible du post**
(ni `<comments>`, ni le texte lisible de `<description>`) — décision
utilisateur du 13 août : le crédit est ajouté à la main par l'utilisateur
en commentaire du post une fois publié, pas par cette routine. Le
commentaire HTML `<!-- credit: ... -->` en fin de `<description>` sert
uniquement à ce que la routine (et l'utilisateur, en lisant le flux) sache
quelle photo/quel photographe a été utilisé — invisible dans un lecteur
RSS ou sur les réseaux, jamais affiché publiquement par ce mécanisme.

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

Commit avec un message préfixé `[pub]`, push sur `main`.
