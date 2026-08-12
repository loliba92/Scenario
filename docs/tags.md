# Tags — liste de référence

Ce fichier pilote les tags utilisés dans `archives.html` (boutons `.tag` sous chaque
entrée). Avant d'ajouter des tags à une nouvelle entrée, **consulter cette liste et
réutiliser un tag existant chaque fois que le sujet y rentre raisonnablement** —
n'en créer un nouveau qu'en dernier recours (voir règle en bas de page).

But : un tag ne rend service au lecteur que s'il regroupe plusieurs articles. Une
liste fermée, réutilisée d'édition en édition, vaut mieux qu'un mot inventé à chaque
fois qui ne filtre jamais rien.

## 1. Tag de registre (toujours le premier, un seul, jamais inventé)

Fixé par le jour de publication — voir `docs/routine-prompt.md`, Étape 1.

| `data-tag` | Libellé |
|---|---|
| `geopolitique` | Géopolitique |
| `carte-blanche` | Carte blanche |
| `actualite-francaise` | Actualité française |
| `sport` | Sport |
| `sciences` | Sciences |
| `culture` | Culture |
| `economie-mondiale` | Économie mondiale |

**Tags historiques, à ne plus utiliser pour une nouvelle édition** — conservés
uniquement pour que le filtre d'`archives.html` continue à fonctionner sur les
éditions déjà publiées avec l'ancien registre (jamais retaggées
rétroactivement, voir « Historique » en bas de page) :

| `data-tag` | Libellé | Utilisé jusqu'au |
|---|---|---|
| `culture-francaise` | Culture française | 12 août 2026 |
| `culture-internationale` | Culture internationale | 12 août 2026 |

**Restructuration du 12 août 2026 (retour utilisateur).** Deux changements
liés : (1) `culture-francaise` (samedi) et `culture-internationale` (dimanche)
fusionnent en un seul registre `culture` (samedi) — la frontière
France/international était souvent artificielle, et les deux files étaient
clairsemées ; (2) la case libérée par cette fusion sert à un nouveau registre
`economie-mondiale` (dimanche), séparé de `geopolitique` (lundi) qui mélangeait
jusque-là géopolitique dure et économie mondiale dans un seul slot surchargé.
Voir `sujets-prioritaires.md` (section « Géopolitique — lundi ») pour la règle
de classement des sujets à cheval sur les deux (guerres commerciales, tarifs
douaniers…), et `docs/ARCHITECTURE.md` pour le détail de la décision.

## 2. Tags thématiques (1 à 2 en plus du tag de registre)

Liste fermée, à réutiliser en priorité. Classée par grands domaines pour trouver
rapidement le bon tag — l'ordre du tableau n'a pas d'autre signification.

| `data-tag` | Libellé | Domaine |
|---|---|---|
| `economie` | Économie | Économie & entreprises |
| `entreprises` | Entreprises | Économie & entreprises |
| `emploi` | Emploi | Économie & entreprises |
| `politique` | Politique | Politique & institutions |
| `justice` | Justice | Politique & institutions |
| `diplomatie` | Diplomatie | International |
| `defense` | Défense & sécurité | International |
| `immigration` | Immigration | International |
| `energie` | Énergie | Sciences & environnement |
| `climat` | Climat | Sciences & environnement |
| `sante` | Santé | Sciences & environnement |
| `espace` | Espace | Sciences & environnement |
| `intelligence-artificielle` | Intelligence artificielle | Tech & numérique |
| `numerique` | Numérique | Tech & numérique |
| `cinema` | Cinéma | Culture & divertissement |
| `musique` | Musique | Culture & divertissement |
| `jeux-video` | Jeux vidéo | Culture & divertissement |
| `litterature` | Littérature | Culture & divertissement |
| `medias` | Médias | Culture & divertissement |
| `sport-economie` | Sport & argent | Sport (hors registre du jeudi) |
| `societe` | Société | Société |

Note : `sport` existe déjà comme tag de registre (jeudi). Un sujet sportif traité un
autre jour (ex. mardi carte blanche) prend `sport-economie` comme tag thématique
plutôt que de réutiliser `sport`, pour ne pas mélanger les deux usages dans le
filtre.

## Règle de dernier recours

Si vraiment aucun tag de la liste ci-dessus ne convient au sujet du jour :
1. En créer un nouveau, sobre et générique (pas trop spécifique à l'édition du
   jour — un tag doit pouvoir resservir).
2. L'ajouter aussitôt à ce fichier (section 2, avec son domaine), dans le même
   commit que l'édition.
3. Ne jamais créer deux tags différents pour la même idée à quelques semaines
   d'écart (ex. ne pas avoir à la fois `streaming` et `medias` pour la même chose) :
   avant de créer, vérifier si un tag existant de la liste couvre déjà l'idée en
   restant un peu plus large.

## Historique

Le 2 août 2026, à la création de cette liste, les 9 entrées déjà publiées dans
`archives.html` ont été normalisées une seule fois pour repartir sur une base
propre : `streaming` → `medias` (édition du 2 août), `moyen-orient` → `diplomatie`
(édition du 27 juillet). `societe` (édition du 28 juillet) a été gardé tel quel et
intégré à la liste ci-dessus plutôt que remplacé, le thème étant assez récurrent
pour mériter son propre tag.

**Ce fut une normalisation ponctuelle, pas une nouvelle règle.** À partir de
maintenant, les entrées `archives.html` redeviennent figées comme le veut la
routine (« ne jamais supprimer ni modifier les entrées déjà présentes ») : un tag
mal choisi sur une future édition ne sera plus corrigé rétroactivement, d'où
l'intérêt de bien choisir dans la liste fermée dès la publication.
