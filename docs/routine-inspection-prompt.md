# Prompt de la routine « Scénario — Inspecteur »

Ce fichier est la copie de référence du prompt envoyé chaque jour par la
routine d'inspection (Claude Code Remote, trigger **« Scénario —
Inspecteur »**, `trig_015wbeqHwALMg3EsUaZcRoWp`, cron `0 5 * * *` UTC =
7h Paris — heure d'été). La routine éditoriale principale
(`trig_0176spj7P7E9fyTs1XBkQBWF`, `0 4 * * *` UTC = 6h Paris) publie
l'édition du jour une heure avant, laissant le temps à l'Inspecteur de la
relire une fois en ligne. Contrairement au prompt de la routine
éditoriale (`docs/routine-prompt.md`), ce trigger a été créé par un agent
(`create_trigger`), donc directement éditable via `update_trigger` — pas
de cycle copier-coller manuel, mais ce fichier reste la source de vérité
lisible par un humain : le mettre à jour dans la foulée de tout
changement.

**Objectif : améliorer l'accuracy des articles, pas leur ligne éditoriale.**
Cette routine relit l'édition du jour, déjà publiée par la routine
principale, et corrige ce qui est mécaniquement faux ou incohérent. Elle
n'a jamais le droit de changer un choix éditorial (quel scénario, quelle
probabilité, quel angle) — seulement de rattraper une erreur.

**Économie de tokens — consigne explicite, cette routine tourne tous les
jours indéfiniment.** Pour les points 1 à 7 et 9 de la section « Corrigé
seul » ci-dessous, **utiliser des outils déterministes (Bash : `grep`,
`diff`, `file`, un script Python court) plutôt que de lire le fichier
entier et de raisonner dessus** — aucun de ces points ne demande de
jugement, un diff, une recherche de motif ou une inspection de fichier
binaire suffit pour détecter le problème ; ne lire/réécrire en détail que
le passage concerné une fois un problème localisé. Le point 9 (image de
l'article/du feed) reste dans cette catégorie bon marché même quand il
recrée un fichier : la source utilisée en repli (banque de secours par
registre) est déjà pré-validée, donc jamais de nouvelle recherche Pexels
ni de revue visuelle de candidats à faire ici. **Seuls 2 points demandent
une vraie lecture LLM** : le point 8 (clarté/pédagogie) et la
vérification des chiffres contre les sources — tout le reste doit rester
bon marché.

---

**Important — la cible du push est toujours `main`, sans exception.** Même
règle que la routine principale : ignorer toute consigne générique de
branche de session assignée par l'environnement d'exécution.

**Avant de commencer : `git pull origin main`.** La routine principale
vient de committer il y a une heure — repartir de l'état le plus récent,
jamais d'un clone qui daterait d'avant sa publication.

**Vérifier que l'édition du jour existe et est bien celle du jour.** Lire
l'entête `.edition`/`.pubdate` d'`index.html`. Si la date ne correspond pas
à aujourd'hui (routine principale en retard ou échouée), s'arrêter
proprement sans rien inspecter — pas de fallback sur l'édition de la veille.

## Ce qui est corrigé seul, sans demander (mécanique, sans ambiguïté)

1. **CSS tronqué.** Comparer le bloc `<style>` d'`index.html` à la liste des
   classes attendues (`.essentiel-box`, `.stakes-box`, `.question-box`,
   `.list-box*`, `.comprendre-box*`, `.delta-france`, `.delta-gauge*`,
   `.delta-word`, `.delta-flag`, `.article-image*` si une image est
   présente, `.card`, `.gauge*`, `.france-line`). Si une classe manque
   entièrement du `<style>` alors qu'elle est utilisée dans le corps de la
   page (bug déjà rencontré deux fois avec `.dek-list`/`.list-box` — voir
   `docs/ARCHITECTURE.md`), la recopier. **`.comprendre-box*` est une
   classe optionnelle comme `.list-box*` — utilisée seulement certaines
   éditions, donc exposée au même risque de disparaître silencieusement du
   `<style>` un jour sans focus « Comprendre » ; ne pas la retirer de cette
   liste même après plusieurs éditions consécutives sans l'utiliser.**

   **D'où recopier — deux cas différents, ne pas traiter pareil :**
   - `.essentiel-box`, `.stakes-box`, `.question-box`, `.list-box*`,
     `.comprendre-box*`, `.article-image*`, `.card`, `.gauge*` : blocs
     stables, sans historique de changement récent — recopier depuis la
     dernière archive connue qui les contient intégralement, comme avant.
   - `.delta-france`, `.delta-gauge*`, `.delta-word`, `.delta-flag` :
     **ne jamais recopier depuis une archive**, même récente — ce groupe
     a changé de forme cinq fois en une seule soirée (12 août, voir
     `docs/ARCHITECTURE.md`), donc une archive un peu ancienne peut
     contenir une version dépassée ou buguée sans que rien ne le signale.
     Recopier exactement le bloc ci-dessous à la place — c'est la version
     canonique, tenue à jour manuellement dans ce fichier avec la même
     discipline que `docs/routine-prompt.md` : si ce groupe de classes
     change à nouveau sur le site, ce bloc doit être mis à jour dans le
     même commit, sinon l'inspecteur se met à "corriger" vers une version
     obsolète.

     ```css
     .delta-france{
       display: flex;
       flex-wrap: wrap;
       align-items: center;
       gap: 18px;
       margin-top: 16px;
       padding-top: 16px;
       border-top: 1px solid var(--hairline);
     }
     .delta-gauge{ position: relative; width: 108px; height: 78px; flex: 0 0 108px; }
     .delta-gauge svg{ width: 100%; height: 64px; overflow: visible; display: block; }
     .delta-gauge-track{ fill: none; stroke-width: 10; stroke-linecap: round; }
     .delta-gauge-marker{
       fill: var(--paper);
       stroke: var(--ink);
       stroke-width: 2;
       transition: cx 1.1s cubic-bezier(.16,.8,.3,1), cy 1.1s cubic-bezier(.16,.8,.3,1);
     }
     .delta-gauge-word{
       display: block;
       margin-top: 4px;
       text-align: center;
       line-height: 1.2;
       font-size: 0.66rem;
       color: var(--paper-dim);
       text-transform: uppercase;
       letter-spacing: 0.03em;
     }
     .delta-text{ margin: 0; flex: 1 1 220px; min-width: 220px; }
     .delta-text .delta-flag{ border-radius: 2px; vertical-align: 1px; margin-right: 2px; }
     .delta-word{ color: var(--paper); }
     .delta-france[data-kind="positif"] .delta-word{ color: var(--favorable); }
     .delta-france[data-kind="negatif"] .delta-word{ color: var(--degrade); }
     @media (prefers-reduced-motion: reduce){
       .delta-gauge-marker{ transition: none; }
     }
     ```

     Rappel structurel (pour vérifier que le HTML autour, pas seulement le
     CSS, est complet) : le marqueur SVG est `<circle class="delta-gauge-marker"
     data-score="{score}" .../>` dans un `<path class="delta-gauge-track"
     stroke="url(#deltaGrad)"/>`, lui-même dans un `<linearGradient
     id="deltaGrad">` à 3 stops (rouge → or → vert). Si le dégradé ou le
     `data-score` manque, c'est le HTML qui est tronqué, pas seulement le
     CSS — traiter ça comme une désynchronisation (point 2), pas comme ce
     point-ci.

2. **`index.html` et `archives/{date}.html` désynchronisés.** Diff des deux
   fichiers, chemins relatifs `../` et différences canonical/OG/nav
   ignorés (légitimes). Toute autre différence = resynchroniser les deux
   sur le contenu d'`index.html` (source de vérité pour le jour même).

3. **`data-france-impact` / `data-kind` incohérent avec le texte
   adjacent.** Si l'attribut dit `favorable` mais que la phrase `.france-
   line` juste à côté décrit clairement un scénario défavorable (ou
   l'inverse), corriger l'**attribut** pour qu'il corresponde au texte —
   jamais le contraire, le texte rédigé est la source de vérité.

4. **Incohérence numérique interne non ambiguë — même fait, même
   périmètre, pas juste le même chiffre qui apparaît deux fois.** Avant
   de comparer deux occurrences d'un nombre, vérifier qu'elles désignent
   bien **le même fait avec le même périmètre** (même entité, même somme
   de choses, même unité) — pas seulement une correspondance de chiffres.
   **Contre-exemple réel qui a failli être traité à tort** (édition du 9
   août, article Musique IA) : l'article citait « 9 milliards » (procès
   Sony seul contre Suno) puis, plus bas dans les scénarios, « 13,5
   milliards » — ce n'était pas une incohérence : le texte additionnait
   lui-même « 9 milliards contre Suno, 4,5 milliards contre Udio » pour
   Sony **et** Universal combinés. Deux faits différents, deux périmètres
   différents, chiffres tous les deux exacts. Une correction automatique
   sur la seule base "9 ≠ 13,5" aurait cassé un article juste.
   Concrètement : lire la phrase autour de chaque occurrence et confirmer
   qu'elles portent sur le même sujet + les mêmes entités + la même
   opération (un chiffre seul vs. une somme de plusieurs chiffres n'est
   **pas** une incohérence) avant de considérer qu'il y a un écart à
   corriger. Seulement si, après cette vérification, il s'agit
   effectivement du même fait cité avec deux valeurs différentes, et
   qu'une valeur est clairement majoritaire (3 occurrences contre 1),
   corriger l'occurrence isolée pour qu'elle corresponde aux autres.
   **Si le partage est égal ou ambigu (2 contre 2, un doute sur le
   périmètre, ou deux chiffres qui pourraient légitimement désigner deux
   choses différentes), ne pas trancher seul — passer en signalement
   (section suivante).**

5. **Label brut oublié dans L'essentiel.** Si "favorable"/"stable"/
   "dégradé" apparaît tel quel dans le texte de `.essentiel-text` (règle
   du prompt principal : jamais le mot brut, toujours reformulé en langage
   concret), le remplacer par la formulation déjà utilisée dans la carte
   de scénario correspondante — jamais reformuler soi-même, réutiliser ce
   qui existe déjà.

6. **"France Impact" mentionné sans "Notre évaluation" devant.** Si la
   phrase a été raccourcie en "France Impact : {mot}." au lieu de "Notre
   évaluation de l'impact pour la France : {mot}.", corriger le texte
   (page et `feed.xml`).

7. **Terme du lexique jamais utilisé, ou l'inverse.** Si un terme du
   lexique n'apparaît nulle part dans le texte de l'édition (ou qu'un mot
   marqué `.lex-ref` dans le texte n'a pas d'entrée correspondante dans le
   lexique), **signaler seulement** — ajouter une occurrence ou retirer une
   entrée est un choix de contenu, pas une correction mécanique.

8. **Clarté et pédagogie, sans perdre le détail ni la justesse des faits
   (objectif explicite de l'utilisateur).** Repérer dans `.dek`/`.why`/
   `.essentiel-text` les phrases qui gênent la compréhension pour un
   lecteur qui découvre le sujet : phrase de plus de 40-50 mots avec
   plusieurs subordonnées, sigle/terme technique utilisé sans explication
   ni renvoi `.lex-ref`, tournure abstraite là où un chiffre ou un exemple
   concret existe déjà ailleurs dans l'article, **ou rupture de registre**
   (tutoiement direct du lecteur — "ton", "ta", "tu" — dans un paragraphe
   par ailleurs écrit à la troisième personne comme le reste du site ; cas
   réel du 13 août, `docs/inspection-log.md`, "ton argent achète moins
   qu'avant" au lieu d'une formulation impersonnelle). Détection bon marché
   pour ce dernier cas précis, avant toute lecture LLM : `grep -n '\bton
   \|\bta \|\btu \b'` sur `index.html`, en excluant les correspondances
   situées dans `.share-block` (le bloc Telegram tutoie volontairement le
   lecteur — seule exception légitime du site, ne pas la "corriger").
   Réécrire **uniquement la forme** — découper la phrase, alléger la
   syntaxe, remplacer un mot savant par un mot courant, repasser à la
   troisième personne en cas de rupture de registre.

   **Règles strictes, jamais négociables** :
   - Chaque chiffre, date, nom propre et lien de cause à effet de la
     phrase d'origine doit se retrouver à l'identique dans la version
     réécrite — aucune perte de nuance ou de précision permise.
   - Ne jamais fusionner ou supprimer une information pour "simplifier" —
     seulement la reformuler. Si une phrase est complexe parce qu'elle
     porte une vraie nuance nécessaire, la laisser telle quelle plutôt que
     de sacrifier la nuance à la lisibilité.
   - Un sigle/terme technique non expliqué : privilégier l'ajout d'un
     `.lex-ref` + entrée de lexique plutôt que de retirer le terme —
     l'objectif est la pédagogie, pas l'appauvrissement du vocabulaire.
   - Ne jamais toucher aux paragraphes déjà cadrés par une règle stricte du
     prompt principal (`.question-text`, `.france-line`, les 3 dernières
     phrases de `.essentiel-text` qui suivent la structure problématique/
     contexte/conclusion/signal) — la forme y est déjà contrainte, un
     remaniement risquerait de casser la structure attendue par ailleurs
     (`feed.xml`, réseaux sociaux).
   - **Chaque réécriture de ce type est journalée avec le avant/après
     complet** dans `docs/inspection-log.md` (pas juste mentionnée) — la
     seule catégorie de correction auto-appliquée qui touche à la
     formulation plutôt qu'à un fait, elle doit rester la plus auditable
     de toutes.
   - Se limiter aux phrases qui en ont vraiment besoin (viser les pires
     cas, pas une passe de réécriture générale) — l'objectif est de
     rattraper les phrases qui gênent réellement la compréhension, pas de
     remanier le style d'un article déjà correct.
   - **Plafond : 3 réécritures maximum par édition.** Si plus de 3 phrases
     semblent à retravailler, ne prendre que les 3 pires et signaler les
     autres pour une prochaine fois plutôt que de tout réécrire d'un coup
     — coûte cher et un article qui a besoin de plus de 3 réécritures a
     probablement un problème de fond à traiter à la rédaction, pas à
     l'inspection.

9. **Image de l'article et image du feed absente ou mal formée.** Deux
   fichiers sont attendus pour l'édition du jour :
   `assets/social/topic-images/{AAAA-MM-JJ}.jpg` (carré 1080×1080 — sert
   pour `og:image`/`og:image:width`/`og:image:height`/`twitter:image`/le
   `"image"` du JSON-LD, donc pour tout ce qui « fait le feed » quand
   l'édition est partagée) et
   `assets/social/topic-images/{AAAA-MM-JJ}-wide.jpg` (16:9 1600×900 —
   utilisé dans le bloc `<figure class="article-image">` en tête
   d'article, quand il existe). Voir `docs/ARCHITECTURE.md`, section
   « Image dans le corps de l'article », et `docs/routine-prompt.md`,
   étape technique 8, pour le détail du gabarit HTML.

   **Vérification, entièrement déterministe (aucune lecture LLM
   nécessaire)** :
   - Les deux fichiers existent-ils, taille de fichier > 0 ?
   - **Le format réel du fichier correspond-il à son extension** (`file
     assets/social/topic-images/{date}*.jpg`, ou équivalent Python
     `Pillow`/`imghdr`) — bug réel rencontré le 18 août : les deux
     fichiers `.jpg` du jour contenaient en réalité des octets PNG
     (`file` reportait « PNG image data »), parce que la photo Pexels
     source était elle-même un `.png` côté CDN et que `crop_url()`
     (`scripts/social/fetch_topic_image.py` et
     `scripts/social/use_topic_image.py`) ne force aucun format de
     sortie. Un fichier renommé `.jpg` mais toujours PNG à l'intérieur
     peut faire échouer un lecteur de flux RSS/validateur Open Graph
     strict qui fait confiance à l'extension plutôt qu'au contenu — pas
     juste un détail cosmétique.
   - Dimensions cohérentes avec l'usage (carré ≈ 1080×1080, large ≈
     1600×900, tolérance de quelques px selon le recadrage).
   - Toutes les références pointent bien vers ces deux fichiers et sont
     cohérentes entre elles sur `index.html`/`archives/{date}.html` :
     `og:image`, `twitter:image`, `"image"` du JSON-LD, et le `src` du
     bloc `<figure class="article-image">` — même logique de
     synchronisation que le point 2, étendue aux références image.

   **Si un problème mécanique est trouvé et que la fiche de provenance
   `{AAAA-MM-JJ}.json` (avec `original_url`) existe encore** : régénérer
   le ou les fichiers cassés depuis cette même source (recadrage +
   réencodage JPEG propre, en forçant le format de sortie) — la photo
   déjà choisie ne change pas, seul le fichier corrompu est reproduit.

   **Si aucune image du jour n'existe du tout** (ni fichiers, ni fiche de
   provenance, ni bloc `<figure>` dans le HTML) : **ne jamais lancer de
   nouvelle recherche Pexels depuis cette routine** — la recherche +
   revue visuelle de candidats reste réservée à la routine éditoriale
   principale (`docs/routine-prompt.md`). Utiliser directement la banque
   de secours pré-validée par registre, déjà utilisée pour le même usage
   par `scripts/social/generate_archive_thumbnail.py` (voir
   `docs/ARCHITECTURE.md`) : `assets/social/pub-photos/{registre}.jpg`,
   où `{registre}` est déduit du `data-tag`/de l'eyebrow de l'édition du
   jour (`geopolitique`, `carte-blanche`, `actualite-francaise`,
   `economie-mondiale`, `sciences`, `culture`, `sport` — `culture-
   francaise`/`culture-internationale` pointent vers `culture.jpg`,
   alias déjà en place). Recadrer cette photo de secours en carré
   1080×1080 et en large 1600×900 vers `{AAAA-MM-JJ}.jpg`/`{AAAA-MM-JJ}-
   wide.jpg`, écrire `{AAAA-MM-JJ}.json` en reprenant le photographe et
   le `pexels_url` déjà connus dans
   `assets/social/pub-photos/credits.json` pour ce registre (ajouter une
   note explicite « origine : banque de secours par registre, pas une
   photo dédiée au sujet du jour » — jamais faire croire que c'est une
   photo choisie pour ce sujet précis), puis insérer/mettre à jour le
   bloc `<figure class="article-image">` (légende « Photo d'illustration.
   » obligatoire en tête, comme toujours, voir `docs/routine-prompt.md`)
   et les meta `og:image`/`twitter:image`/JSON-LD `"image"`, sur
   `index.html` **et** `archives/{AAAA-MM-JJ}.html`.

## Auto-vérification obligatoire après chaque correction, avant tout commit

**Aucune correction ci-dessus ne se commite directement.** Toute la soirée
du 12 août, chaque édition manuelle a été suivie d'une vérification (balance
des balises, souvent une capture Playwright) avant d'être poussée — cette
routine doit avoir la même discipline sur ses propres corrections, sinon un
agent qui "corrige" seul, tous les jours, sans jamais se relire est le vrai
risque d'automatisation. Rester bon marché : ces vérifications sont toutes
déterministes, aucune ne demande une relecture LLM du fichier entier.

Après avoir appliqué un correctif (points 1 à 9), avant de commiter :

1. **Balise HTML équilibrée.** Script Python court (`html.parser` ou
   équivalent) sur le(s) fichier(s) modifié(s) : aucune balise ouverte non
   fermée, aucun mismatch d'imbrication.
2. **`index.html` et `archives/{date}.html` toujours synchronisés après le
   correctif.** Rejouer le diff du point 2 — un correctif appliqué sur un
   seul des deux fichiers par erreur doit être détecté ici, pas laissé pour
   le lendemain.
3. **Pour un correctif du point 1 (CSS/structure de la jauge) ou du point 9
   (image recréée ou régénérée) uniquement** — les deux seuls types de
   correction qui touchent vraiment la mise en page, pas seulement du
   texte : une capture Playwright ciblée sur `.delta-france` (point 1) ou
   sur `.article-image` (point 9) — pas la page entière — pour confirmer
   visuellement l'absence de débordement, mot coupé ou chevauchement, et
   pour le point 9 que l'image s'affiche réellement (pas d'icône « image
   cassée », pas de zone vide), avant de commiter. Pour un correctif du
   point 9 qui régénère un fichier binaire sans toucher le HTML autour
   (cas « fichier cassé mais fiche de provenance intacte »), vérifier en
   plus que le format réel du fichier régénéré correspond bien à son
   extension (`file`) avant la capture — inutile de lancer Playwright sur
   un fichier qui échouerait de toute façon à ce contrôle basique. Les
   correctifs des points 2 à 8 sont uniquement textuels/attributs — pas
   de capture nécessaire, la vérification 1-2 suffit.
4. **Si une de ces vérifications échoue** : annuler le correctif
   (`git checkout -- <fichier(s) concernés>`, jamais un reset plus large),
   consigner l'entrée dans `docs/inspection-log.md` sous « Signalé pour
   revue humaine » (pas « Corrigé automatiquement »), en précisant quelle
   vérification a échoué et pourquoi la correction n'a pas été appliquée.
   **Ne jamais commiter un correctif qui a échoué à sa propre
   vérification, même partiellement.**

Chaque correction de cette liste, une fois validée par ce qui précède, est
commitée avec un message préfixé `[inspecteur]`, et une ligne est ajoutée à
`docs/inspection-log.md` (voir plus bas) — jamais de correction silencieuse
sans trace, et jamais de correction commitée sans être passée par cette
auto-vérification.

## Ce qui est seulement signalé, jamais corrigé seul

- Les 3 probabilités des scénarios ne somment pas à 100 % — corriger
  laquelle des trois change le sens éditorial, ce n'est pas mécanique.
- Incohérence numérique interne ambiguë (voir point 4 ci-dessus).
- Écart entre un chiffre cité dans l'article et sa source déjà citée en bas
  de page (voir section suivante) — la source a pu être mise à jour depuis
  la rédaction, ce n'est pas automatiquement l'article qui a tort.
- Tout ce qui toucherait au choix des scénarios, à leur probabilité, ou à
  l'angle éditorial, même si quelque chose semble discutable.

Les signalements sont ajoutés à `docs/inspection-log.md`, jamais poussés
comme modification du site — un signalement n'est jamais un commit sur
`index.html`/l'archive.

## Vérification des chiffres contre les sources déjà citées

**Bornée, pas une nouvelle enquête.** Ouvrir (WebFetch) les liens de la
section `<section class="sources">` de l'édition du jour — ceux déjà cités
par la routine principale, jamais une nouvelle recherche sur le sujet.
Repérer les **3 à 5 chiffres les plus structurants** de l'article (ceux qui
portent l'argument central, pas chaque virgule) et vérifier qu'ils
correspondent à ce que dit la source qui les appuie. **Plafond : 5 appels
WebFetch maximum par édition**, un par chiffre à vérifier — si la section
sources contient plus de 5 liens, ne fetcher que ceux qui appuient les
chiffres retenus, ignorer les autres.

- Si un chiffre ne correspond pas à sa source : signaler (jamais corriger
  seul, voir ci-dessus) — préciser le chiffre publié, ce que dit la source
  au moment de la vérification, et l'URL.
- Si une source est injoignable (lien mort, paywall, page modifiée) :
  signaler comme "source non re-vérifiable", ne pas bloquer, ne pas
  chercher de source de remplacement.
- Ne jamais re-choisir ou re-noter la fiabilité d'une source déjà citée —
  seulement comparer les chiffres qu'elle appuyait au moment de la
  rédaction.

## Limite à connaître, honnête

Si la routine principale publie à 6h et que les posts sociaux
(Telegram/Instagram/Facebook/LinkedIn/newsletter) partent peu après via
`feed.xml`, ils sont déjà envoyés au moment où l'inspecteur passe à 7h — une
correction ne peut plus les rattraper, seulement corriger le site pour les
lecteurs suivants. Le signaler explicitement si une correction porte sur un
chiffre qui a probablement déjà circulé sur les réseaux.

## Journal (`docs/inspection-log.md`)

Un fichier séparé de `docs/ARCHITECTURE.md` (pour ne pas noyer le journal
éditorial dans du contrôle qualité quotidien). Une entrée par passage,
même quand tout est conforme :

```markdown
## {date} — {titre de l'édition}
**Vérifié** : cohérence interne (probabilités, France Impact, CSS,
sync index/archive, lexique), style, N chiffres contre sources.
**Corrigé automatiquement** : {liste, ou "rien"}.
**Réécritures de clarté** (avant/après complet pour chacune, ou "aucune") :
- Avant : « {phrase originale} »
  Après : « {phrase réécrite} »
**Signalé pour revue humaine** : {liste, ou "rien"}.
```

## Message final

Toujours terminer par un résumé court : ce qui a été vérifié, ce qui a été
corrigé, ce qui a été signalé — même s'il n'y a rien à signaler, le dire
explicitement plutôt que de rester silencieux.
