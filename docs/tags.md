# Tags — liste de référence

Ce fichier pilote les tags utilisés pour classifier les articles. Avant d'ajouter des
tags à une nouvelle entrée, **consulter cette liste et réutiliser un tag existant chaque
fois que le sujet y rentre raisonnablement** — n'en créer un nouveau qu'en dernier
recours (voir règle en bas de page).

But : un tag ne rend service au lecteur que s'il regroupe plusieurs articles. Une
liste fermée, réutilisée d'édition en édition, vaut mieux qu'un mot inventé à chaque
fois qui ne filtre jamais rien.

## Classification thématique (système unifié)

À partir de septembre 2026, la classification passe à un système unifié en une seule
couche : les **6 domaines thématiques** qui structurent la navigation (pages thématiques,
dropdown menu). Le tag de « registre » (géopolitique, sport, culture…) est supprimé.

Chaque article doit avoir exactement **un domaine** enregistré dans la balise
`<meta name="domain" content="...">` (voir `docs/routine-prompt.md`, Étape technique 2).

## Domaines thématiques (liste fermée)

Liste fermée, à réutiliser en priorité. Classée par grands domaines pour trouver
rapidement le bon tag — l'ordre du tableau n'a pas d'autre signification.

| Domaine | Slug | Tags thématiques |
|---|---|---|
| Économie & entreprises | `economie-entreprises` | `economie`, `entreprises`, `emploi` |
| Politique & institutions | `politique-institutions` | `politique`, `justice` |
| International | `international` | `diplomatie`, `defense`, `immigration` |
| Sciences & environnement | `sciences-environnement` | `energie`, `climat`, `sante`, `espace` |
| Tech & numérique | `tech-numerique` | `intelligence-artificielle`, `numerique` |
| Culture & divertissement | `culture-divertissement` | `cinema`, `musique`, `jeux-video`, `litterature`, `medias` |

Les tags thématiques ci-dessus restent disponibles pour classification granulaire future,
mais **chaque article doit avoir un domaine principal** enregistré via
`<meta name="domain" content="...">`. Les domaines structurent la navigation et l'archivage.

## Règle pour assigner un domaine

Pour chaque **nouvel article**, assigner exactement **un domaine** en ajoutant la
balise `<meta name="domain" content="{slug}">` dans le `<head>` (voir
`docs/routine-prompt.md`, Étape technique 2).

Si le sujet touche plusieurs domaines (ex. une loi économique affectant le travail) :
choisir le domaine **principal** — celui qui domine l'angle de l'article. Favoriser
la clarté sur la précision.

## Historique

Le 2 août 2026, à la création de cette liste, les 9 entrées déjà publiées dans
`archives.html` ont été normalisées une seule fois pour repartir sur une base
propre : `streaming` → `medias` (édition du 2 août), `moyen-orient` → `diplomatie`
(édition du 27 juillet). `societe` (édition du 28 juillet) a été gardé tel quel et
intégré à la liste ci-dessus plutôt que remplacé, le thème étant assez récurrent
pour mériter son propre tag.

Le 9 septembre 2026, restructuration majeure : suppression du système de registre
(géopolitique, sport, culture, etc.), remplacé par un classement unifié sur les 6
domaines thématiques. Archives.html passe de tableau filtrable (JS) à tableau statique
auto-généré depuis les métadonnées d'article. Les 39 articles existants sont backfillés
avec domaine metadata. Les anciens registres restent conservés pour compatibilité
historique avec les articles déjà publiés (voir section « Anciens registres » ci-dessus).
