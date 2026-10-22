"""Écrit le texte parlé d'un épisode à UNE voix, à partir d'une édition publiée (style validé le 3 octobre 2026).

Le propriétaire a rejeté le dialogue à deux voix (trop « IA », trop de chiffres). Le texte attendu : une question, les
faits qui la posent, le problème de fond, les trois scénarios dans l'ensemble, l'impact pour la France, ce qu'on
surveillera. Aucun tableau d'indicateurs. Rien qui ne figure pas dans l'article (garde-fou sur les nombres).
La fermeture est écrite par le script, jamais par le modèle.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from fractions import Fraction
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_podcast as gp  # noqa: E402

MOTS_MIN, MOTS_MAX = 420, 1000  # 3 à 7 minutes de lecture (« mieux vaut plus que moins », 6 octobre 2026 ; 720 mots au départ)
SEPARATEUR = "---"
MOTS_PHRASE_MAX, MOTS_PHRASE_MOYENNE = 32, 20   # pédagogie : phrases courtes à l'oral (textes validés : moyenne 13-15, maximum 28)
# Sept accueils (plus chaleureux depuis le 10 octobre 2026 : « Comment allez-vous ? ») et sept fermetures, écrits à l'avance (jamais par le modèle) : on en tire un par jour pour que l'épisode
# ne sonne pas toujours pareil. Règles communes : vouvoiement, « évolutions » seulement dans l'accueil, phrases courtes.
# Les fermetures changent seulement au début : la fin est un rituel fixe (RITUEL), pour que la devise devienne celle du site. Le tirage dépend de la date (voir _rangs) : il se refait à l'identique si l'on
# régénère un épisode.
OUVERTURES = (
    "Bonjour, comment allez-vous ? Installez-vous : bienvenue sur Scénario. Comme chaque jour, une question d'actualité et ses trois évolutions possibles.",
    "Bonjour, et merci d'être là. Comment allez-vous ? Bienvenue sur Scénario : comme chaque jour, une question d'actualité, trois évolutions possibles.",
    "Bonjour, ou bonsoir, selon le moment où vous nous écoutez. J'espère que vous allez bien. Bienvenue sur Scénario : une question, trois évolutions possibles.",
    "Bienvenue sur Scénario. Prenez un moment pour vous, installez-vous. Comme chaque jour, une question d'actualité, et trois évolutions possibles.",
    "Bonjour à toutes et à tous, comment allez-vous ? Vous écoutez Scénario : ensemble, nous regardons trois évolutions possibles d'une question d'actualité.",
    "Bienvenue sur Scénario, et merci de nous accorder quelques minutes. Comment allez-vous ? Comme chaque jour, une question d'actualité, trois évolutions possibles.",
    "Bonjour, et bienvenue sur Scénario. Si vous avez un instant, installez-vous : une question d'actualité, trois évolutions possibles, et le temps de comprendre.",
)
RITUEL = ("Rien n'est écrit à l'avance. La suite, c'est à vous de l'écrire. "
          "Prenez soin de vous, et à demain pour un nouveau scénario.")   # devise du site, dite chaque jour mot pour mot : « Rien n'est écrit à l'avance ». Réécrit le 14 octobre 2026 après écoute : l'ancienne fin (« Prenez soin de vous. Rien n'est écrit à l'avance, ne l'oubliez pas. La suite, c'est à vous de l'écrire. À demain… ») ne coulait pas (adieu au milieu, rappel puis invitation sans lien). Ordre voulu : constat, invitation, adieu. « ne l'oubliez pas » (idée du 7 octobre) retiré à cette occasion.
FERMETURES = tuple(debut + "\n\n" + RITUEL for debut in (   # lues d'un seul tenant (une seule voix, un seul ton), avec la devise dans un paragraphe à part
    "Merci d'avoir passé ce moment avec nous : l'édition complète vous attend sur lesscenarios.fr.",
    "Voilà, c'est la fin de ce rendez-vous : merci de votre confiance, elle compte beaucoup pour nous, et tout est sur lesscenarios.fr.",
    "Merci de nous avoir écoutés : si le sujet vous a donné envie d'aller plus loin, tout est sur lesscenarios.fr.",
    "C'est tout pour aujourd'hui : merci pour votre attention, et retrouvez les sources sur lesscenarios.fr.",
    "Merci de votre écoute : si vous en avez envie, parlez-en autour de vous, une question à plusieurs, c'est toujours plus riche, et retrouvez tout sur lesscenarios.fr.",
    "Nous nous arrêtons ici : merci de nous accorder votre temps, cela nous touche, et retrouvez tout sur lesscenarios.fr.",
    "Voilà qui conclut cette édition : merci d'être restés jusqu'au bout, l'édition complète est sur lesscenarios.fr.",
))
OUVERTURE = OUVERTURES[0]   # accueil par défaut (tests, repli)
FERMETURE = FERMETURES[0]


def _rangs(date_str: str | None) -> tuple[int, int]:
    """(rang de l'accueil, rang de la fermeture) pour une date AAAA-MM-JJ.

    L'accueil avance d'un cran par jour : les sept sont joués chaque semaine, sans répétition d'un jour à l'autre.
    La fermeture avance de trois crans par jour (elle ne suit donc pas l'ordre de l'accueil) et d'un cran de plus à
    chaque semaine : jamais deux fois la même d'affilée, les sept reviennent régulièrement, et le couple accueil +
    fermeture change d'une semaine à l'autre."""
    try:
        n = date.fromisoformat((date_str or "")[:10]).toordinal()
    except ValueError:
        return 0, 0
    return n % 7, (3 * n + n // 7) % 7


def ouverture(date_str: str | None = None) -> str:
    return OUVERTURES[_rangs(date_str)[0]]


def fermeture(date_str: str | None = None) -> str:
    return FERMETURES[_rangs(date_str)[1]]


EXEMPLE = (Path(__file__).resolve().parents[2] / "podcast" / "textes" / "2026-10-03.txt")


def construire_prompt(ed: dict, remarques: list[str] | None = None) -> str:
    exemple = EXEMPLE.read_text(encoding="utf-8").strip() if EXEMPLE.exists() else ""
    lexique = "\n".join(f"- {x['terme']} : {x['definition']}" for x in ed.get("lexique") or []) or "(aucun terme dans cette édition)"
    probas = probabilites_edition(ed)
    bloc_probas = ""
    if probas:
        bloc_probas = ("\n- PROBABILITÉS : dis-les EXACTEMENT ainsi, mot pour mot, sans jamais les arrondir ni les changer (leur somme fait 100 %) : "
                       + " ; ".join(f"scénario {r} ({t}) : « {fraction_parlee(p)} »"
                                    for r, t, p in zip(("un", "deux", "trois"), ("favorable", "stable", "dégradé"), probas))
                       + ". Pour deux scénarios réunis, dis la somme exacte : "
                       + ", ".join(f"« {fraction_parlee(a + b)} »" for a, b in combinations(probas, 2)) + " (dans l'ordre un+deux, un+trois, deux+trois). "
                       "N'emploie aucune autre formule du type « une chance sur N ».")
    suite = ("\n\nTa version précédente a été refusée pour ces raisons, corrige-les :\n- " + "\n- ".join(remarques)) if remarques else ""
    return f"""Tu écris le texte parlé d'un court podcast quotidien du site d'actualité Scénario (lesscenarios.fr), à partir de l'édition du {gp.date_longue(ed['date'])} ci-dessous. Une seule voix, chaleureuse, qui parle à un ami curieux : un ton décontracté et naturel, comme on raconte l'actualité à quelqu'un qu'on apprécie.

RÈGLES ABSOLUES
- N'ajoute AUCUN fait, chiffre, nom, date ni exemple qui ne figure pas dans l'article (seule exception : l'image du quotidien décrite dans la partie 3, sans chiffre ni nom propre).
- Registre : décontracté mais jamais péjoratif, ni vulgaire, ni moqueur envers des personnes, des équipes, des pays ou des groupes. Aucun gros mot, aucun mot familier agressif ou dévalorisant (pas de « gueule », « merde », « débile », « nul », « pourri », etc.). Reste bienveillant et nuancé.
- PÉDAGOGIE (règle d'or : l'auditeur ne connaît pas le sujet et ne peut pas revenir en arrière) :
  · une idée par phrase, des phrases de 15 mots en moyenne, jamais plus de 25 ;
  · chaque sigle, institution, lieu peu connu ou terme technique est expliqué en quelques mots dès sa première apparition (« le Top 14, le championnat français de rugby ») ; les termes du LEXIQUE ci-dessous sont obligatoires : explique-les avec des mots du quotidien, en une courte phrase, sans recopier la définition ; fais de même pour tout autre mot qu'un lycéen ne connaîtrait pas ;
  · jamais de sigle de quatre lettres ou plus prononcé comme un code (« OSNMA », « GLONASS »…) : donne son nom en mots (« le système antifraude de Galileo », « le système russe »). Les sigles courts et connus (GPS, UE, ONU) sont permis, expliqués à la première mention ;
  · une seule cause par phrase : jamais « …, ce qui …, ce qui … ». Découpe la chaîne en phrases séparées, dans l'ordre où les choses arrivent ;
  · quand le sujet est technique, ouvre la partie 3 par UNE image du quotidien (sans chiffre ni nom propre) qui fait comprendre le mécanisme, par exemple « crier pour couvrir la voix de quelqu'un » ;
  · pas de mots abstraits (« dynamique », « enjeux », « paradigme », « gouvernance », « trajectoire ») : dis ce qu'ils désignent ;
  · les trois scénarios gardent leur nom, c'est notre marque : « premier scénario », « deuxième scénario », « troisième scénario », chacun annoncé par une phrase simple avant son détail (le mot « évolutions » n'est utilisé que dans la phrase d'accueil, ajoutée par le script) ;
  · après la partie 3 et après la partie 4, une phrase qui redit l'idée en mots simples, introduite par « En clair, » ou « Autrement dit, », sans répéter les chiffres ;
  · une comparaison ou un exemple concret par grande partie quand l'article en fournit un (jamais inventé).
- VIE À L'ORAL (une voix de synthèse lit chaque phrase sur le même rythme : c'est à toi de créer le relief, sans jamais dépasser les limites de longueur ci-dessus) :
  · alterne : après deux ou trois phrases moyennes, une phrase très courte (3 à 6 mots) qui marque un temps (« Et c'est là que tout se joue. », « Rien de plus simple. ») ;
  · pose une vraie question à l'auditeur au début de chaque grande partie (« Que se passe-t-il alors ? », « Pourquoi est-ce si difficile ? »), puis réponds-y ;
  · une ou deux tournures de la parole courante par partie (« Eh bien », « Justement », « Voilà le point », « Regardez ») ; jamais plus, jamais familières ;
  · un ton propre à chaque scénario : le premier, plus léger et encourageant ; le deuxième, posé et nuancé ; le troisième, plus grave, sur des phrases plus lentes ;
  · mets une pause à l'endroit où l'on respire : un point plutôt qu'une virgule avant une idée nouvelle, un tiret ou deux-points avant la chute d'une explication ;
  · jamais de points de suspension, de majuscules d'insistance, ni de point d'exclamation (la voix les lit mal).
- Du langage parlé : phrases courtes, tournures naturelles, pas de liste, pas de Markdown, pas d'adresse web.
- Pas de tableau d'indicateurs : ne récite pas les indicateurs chiffrés des scénarios. Garde peu de chiffres : ceux qui font comprendre le sujet, et les probabilités des scénarios, TOUJOURS dites en fractions parlées : « une chance sur quatre » pour 25 %, « une chance sur deux » pour 50 %, « trois chances sur quatre » pour 75 %, « une chance sur trois », « une chance sur cinq », « une chance sur dix ». JAMAIS « pour cent » ni le signe %, même si l'article donne des pourcentages. Ne les arrondis JAMAIS : les trois probabilités des scénarios doivent faire 100 % ensemble (voir PROBABILITÉS ci-dessous).{bloc_probas}
- Ne dis jamais « selon l'article », ne parle ni de toi ni de l'intelligence artificielle. Pas de « bonjour » ni de « bienvenue » ni d'au revoir : le script ajoute l'accueil avant ton texte et la fermeture après. Ton texte commence par la MISE EN SITUATION (voir STRUCTURE).

STRUCTURE (entre {MOTS_MIN} et {MOTS_MAX} mots, soit 3 à 7 minutes ; vise environ 850 mots : l'épisode idéal dure 6 à 8 minutes, la mise en situation et la phrase finale comptent dans ce total)
1. La mise en situation, puis la question du jour. D'abord UNE ou DEUX phrases très courtes qui placent l'auditeur dans une scène de sa vie liée au sujet, à la deuxième personne (« Imaginez… », « Vous… »), concrète et sans chiffre ni nom propre, pour qu'il se sente concerné avant de réfléchir (par exemple, pour la pénurie de médecins : « Imaginez : vous êtes malade, vous appelez votre médecin, et personne ne peut vous recevoir. » ; pour la hausse des prix : « Vous remplissez votre caddie, et à la caisse, la note vous surprend. »). La scène est présentée comme imaginée, jamais comme un fait réel, et ne dit rien de faux sur le sujet. Ensuite, la question du jour, en une ou deux phrases. Ton chaleureux, humain, jamais dramatique.
2. Ce que l'on sait : les faits qui posent la question, avec un ou deux exemples concrets.
3. Le fond du problème : à quoi cherche-t-on à répondre, et pourquoi la réponse n'est pas évidente.
4. Les trois scénarios, un par un : le plus optimiste (favorable), le plus probable (stable, dis-le clairement), le plus sombre (dégradé), chacun avec sa probabilité, en trois ou quatre phrases courtes : l'idée centrale, puis ce que cela change concrètement pour les gens (un vol retardé, une coupure de courant…), jamais le mécanisme technique ni un nom de technologie.
5. L'impact pour la France, en deux ou trois phrases.
6. Ce qu'on surveillera pour savoir lequel se réalise.
7. La dernière phrase, seule dans un court paragraphe, qui enchaîne directement sur la fermeture : UNE seule phrase simple, dite d'un seul souffle (une virgule au plus), qui commence par « La prochaine fois que vous… » ou « Quand vous… » et ramène le sujet à un geste de la vie de l'auditeur, avec chaleur. Pas de tournure double comme « Dans votre quotidien, la prochaine fois que… ». Elle ne tranche pas et ne donne aucun chiffre : rien n'est écrit à l'avance. Elle ne dit ni « merci » ni « à demain » : le script ajoute la fermeture.

EXEMPLE DE STYLE ATTENDU (autre édition, ne reprends AUCUN de ses faits ; il commence directement par la question, alors que ton texte, lui, commence par la mise en situation) :
{exemple}

LEXIQUE (termes à expliquer en mots simples à leur première mention, voir PÉDAGOGIE) :
{lexique}

ARTICLE
{gp.texte_source(ed)}{suite}

SÉPARATEURS : entre les grandes parties (1 | 2 | 3 | 4 | 5 | 6 ci-dessus), écris une ligne qui contient uniquement trois tirets (---). Un jingle musical y sera placé. Pas d'autre séparateur ; à l'intérieur d'une partie, les paragraphes sont séparés par une ligne vide.

Réponds UNIQUEMENT avec un JSON : {{"texte": "le texte parlé, parties séparées par une ligne ---"}}"""


MOTS_PARTIE_MIN = 100   # une partie plus courte est jointe à la précédente (pas de jingle ni d'appel de voix pour 30 mots)


def regrouper(parts: list[str], minimum: int = MOTS_PARTIE_MIN) -> list[str]:
    """Regroupe les parties trop courtes (10 octobre 2026). La première (l'accroche : mise en situation et question)
    et la dernière (la fermeture, sous laquelle la musique est plus présente) restent seules ; les autres parties de
    moins de `minimum` mots sont jointes à la précédente. Moins de jingles (9 faisaient 1 min 20 de musique) et moins
    d'appels de voix : une petite partie lue seule est celle dont le ton varie le plus."""
    if len(parts) <= 2:
        return list(parts)
    premier, *milieu, dernier = parts
    sortie: list[str] = []
    for p in milieu:
        if sortie and len(p.split()) < minimum:
            sortie[-1] = sortie[-1] + "\n\n" + p
        else:
            sortie.append(p)
    return [premier, *sortie, dernier]


def avec_fermeture(parts: list[str], date_str: str | None = None) -> list[str]:
    """Garantit que l'épisode se termine par la fermeture et la devise (16 octobre 2026).

    Incident : le texte du 16 octobre, déposé dans le dépôt sans sa fermeture, s'arrêtait sur une seule phrase, sans
    « Rien n'est écrit à l'avance » ni au revoir. Le texte généré par le script contient déjà la fermeture (voir
    generer) ; un texte écrit à la main, lui, peut l'oublier. Si la dernière partie ne contient pas la devise, la
    fermeture du jour est ajoutée comme dernière partie."""
    if parts and not re.search(r"écrit à l['’]avance", parts[-1], re.I):
        return [*parts, fermeture(date_str)]
    return list(parts)


def joindre_conclusion(parts: list[str], maximum: int = 60) -> list[str]:
    """Le dernier paragraphe du texte (la phrase qui ramène à la vie de l'auditeur) et la fermeture forment UN seul bloc,
    lu d'un seul appel de voix (22 octobre 2026).

    Retour du propriétaire : « on dirait plusieurs voix, plusieurs tons, très décousu ». Mesuré sur l'épisode du 22 octobre :
    la conclusion était lue en plusieurs appels (introduction, deux phrases de la devise, adieu), chacun avec sa propre
    hauteur de voix (186 à 219 Hz contre 188 pour le corps) et son propre volume. Un seul appel garde une voix et un ton
    constants (mesure : 175 à 205 Hz). Une consigne d'émotion ne peut pas être ajoutée au texte (la voix la lirait à voix
    haute, voir generate_podcast.synthese_unique) : le ton vient du texte et de sa ponctuation.

    Le paragraphe est pris à la fin de l'avant-dernière partie (`regrouper` a pu l'y joindre) ; ce qui reste de cette partie
    est conservé. Rien n'est joint sans devise dans la dernière partie, avec moins de trois parties (l'accroche reste
    seule), ou si ce paragraphe dépasse `maximum` mots."""
    if len(parts) < 3 or not re.search(r"écrit à l['’]avance", parts[-1], re.I):
        return list(parts)
    *debut_partie, dernier = parts[-2].split("\n\n")
    if len(dernier.split()) > maximum:
        return list(parts)
    reste = "\n\n".join(debut_partie).strip()
    return [*parts[:-2], *([reste] if reste else []), dernier + "\n\n" + parts[-1]]


def parties(texte: str) -> list[str]:
    """Le texte découpé aux lignes « --- » (parties vides ignorées)."""
    return [p.strip() for p in re.split(r"(?m)^\s*---\s*$", texte) if p.strip()]


# Mots vulgaires ou péjoratifs refusés par le contrôle (le texte est alors réécrit).
# « match nul » est un résultat sportif (édition du 18 octobre 2026), pas une insulte : seul « nul » employé seul est refusé.
MOTS_INTERDITS = (r"\b(gueules?|merdes?|merdique|putain|bordel|con|cons|conne|connes|connard\w*|salop\w*|enfoir\w*|"
                  r"débiles?|crétins?|idiot\w*|imbéciles?|stupides?|(?<!match )(?<!matchs )(?<!matches )nuls?|pourri\w*|dégueu\w*|foutre|foutu\w*|"
                  r"bouffons?|minables?|ridicules?|pathétiques?|ringard\w*|naze\w*|chiant\w*|crevard\w*)\b")


# Sigles de quatre lettres ou plus qui se disent comme des mots (les autres sont refusés : « O-S-N-M-A » ne dit rien à l'oreille).
SIGLES_PRONONCES = {"OTAN", "NASA", "UNESCO", "OPEP", "FIFA", "UEFA", "INSEE", "SMIC", "NATO", "ARENH"}


_UNITES = ("zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze", "treize",
           "quatorze", "quinze", "seize")
_DIZAINES = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def en_lettres(n: int) -> str:
    """Nombre de 0 à 100 écrit en toutes lettres (« soixante et onze », « quatre-vingt-dix-sept »)."""
    if n < 17:
        return _UNITES[n]
    if n < 20:
        return "dix-" + _UNITES[n - 10]
    if n == 100:
        return "cent"
    if n < 70:
        d, u = divmod(n, 10)
        return _DIZAINES[d] if u == 0 else _DIZAINES[d] + (" et un" if u == 1 else "-" + _UNITES[u])
    if n < 80:
        return "soixante et onze" if n == 71 else "soixante-" + en_lettres(n - 60)
    return "quatre-vingts" if n == 80 else "quatre-vingt-" + en_lettres(n - 80)


# Fractions que l'oreille saisit tout de suite (en %). Une probabilité qui n'en fait pas partie est dite par rapport à la plus proche.
_FRACTIONS_SIMPLES = {10: (1, 10), 20: (1, 5), 25: (1, 4), 30: (3, 10), 33: (1, 3), 40: (2, 5), 50: (1, 2),
                      60: (3, 5), 67: (2, 3), 70: (7, 10), 75: (3, 4), 80: (4, 5), 90: (9, 10)}


def _chances(num: int, den: int) -> str:
    return f"{'une chance' if num == 1 else en_lettres(num) + ' chances'} sur {en_lettres(den)}"


def fraction_parlee(pct: int) -> str:
    """Probabilité dite à l'oreille sans jamais être arrondie en silence.

    25 → « une chance sur quatre », 30 → « trois chances sur dix » ; 45 → « un peu moins d'une chance sur deux »,
    55 → « un peu plus d'une chance sur deux ». Décidé le 7 octobre 2026 : 45 % avait été dit « une chance sur deux »
    (50 %) et les trois probabilités annoncées faisaient 105 % ; « neuf chances sur vingt » est exact mais difficile à
    suivre à l'oreille, d'où cette formule. Les valeurs sont calculées ici, jamais choisies par le modèle."""
    pct = int(pct)
    f = Fraction(pct, 100)
    if f.denominator in (2, 4, 5, 10):
        return _chances(f.numerator, f.denominator)
    proche = min(_FRACTIONS_SIMPLES, key=lambda v: (abs(v - pct), _FRACTIONS_SIMPLES[v][1]))   # à égalité, la plus simple : 45 et 55 → « une chance sur deux »
    num, den = _FRACTIONS_SIMPLES[proche]
    comparatif = "un peu moins" if pct < proche else "un peu plus"
    chances = _chances(num, den)
    return f"{comparatif} d'{chances}" if num == 1 else f"{comparatif} de {chances}"


def probabilites_edition(ed: dict) -> list[int]:
    """Probabilités (en %) des trois scénarios de l'édition, dans l'ordre ; liste vide si elles sont absentes ou incohérentes."""
    try:
        valeurs = [int(str(sc["probabilite"]).strip().rstrip("%")) for sc in ed.get("scenarios") or []]
    except (KeyError, ValueError):
        return []
    return valeurs if len(valeurs) == 3 and all(0 < v < 100 for v in valeurs) else []


def phrases_probabilites_autorisees(probas: list[int]) -> list[str]:
    """Les trois probabilités, plus la somme de deux scénarios (« les deux scénarios les plus sombres ensemble »)."""
    return [fraction_parlee(p) for p in probas] + [fraction_parlee(a + b) for a, b in combinations(probas, 2)]


def controle_probabilites(texte: str, probas: list[int]) -> list[str]:
    """Chaque scénario doit citer SA probabilité exacte ; toute autre « chance(s) sur » est refusée (arrondi, invention)."""
    if not probas:
        return []
    bas = re.sub(r"\s+", " ", texte.lower().replace("’", "'"))
    problemes = [f"dis la probabilité du scénario {rang} EXACTEMENT : « {fraction_parlee(p)} » (soit {p} %), sans l'arrondir"
                 for rang, p in zip(("un", "deux", "trois"), probas) if fraction_parlee(p) not in bas]
    for phrase in sorted(set(phrases_probabilites_autorisees(probas)), key=len, reverse=True):
        bas = bas.replace(phrase, " ")
    for m in re.finditer(r"(?:[\wéèêû-]+ ){0,2}chances? sur [\wéèêû-]+", bas):
        problemes.append(f"probabilité inexacte « {m.group(0).strip()} » : les trois scénarios font {probas[0]} %, {probas[1]} %, {probas[2]} % ; "
                         "dis exactement " + ", ".join(f"« {fraction_parlee(p)} »" for p in probas)
                         + " (deux scénarios ensemble : la somme exacte, ex. « " + fraction_parlee(probas[1] + probas[2]) + " »)")
    return problemes


def phrases_brutes(texte: str) -> list[str]:
    return [p for p in re.split(r"(?<=[.!?])\s+|\n+", texte) if p.strip()]


MOTS_MAX_DERNIER_ESSAI, MOTS_CIBLE = 1100, 850   # dernier essai : jusqu'à 1100 mots ; consigne de raccourcissement : viser 850 mots
MOTS_PHRASE_MAX_DERNIER_ESSAI = 40   # dernier essai : une phrase un peu longue (33 à 40 mots) ne doit pas faire perdre l'épisode du jour


# Mots qui peuvent apparaître sans être dans l'article : la marque, et des noms communs très courants écrits avec une majuscule.
TERMES_LIBRES = {"scenario", "france", "francais", "francaise", "francaises", "europe", "europeen", "europeenne", "etat", "etats"}


def _sans_accents(t: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def termes_hors_article(texte: str, source: str) -> list[str]:
    """Sigles et noms propres du texte qui ne figurent pas dans l'article (10 octobre 2026 : « NFT », absent de l'édition).

    Règle du propriétaire : s'appuyer sur l'édition, ne rien inventer. Sont contrôlés : les sigles en majuscules (2 à 6 lettres)
    et les mots à majuscule au milieu d'une phrase (précédés d'un mot en minuscules), sans tenir compte des accents."""
    connus = set(re.findall(r"[a-z0-9]+", _sans_accents(source)))
    trouves: dict[str, None] = {}
    for m in re.finditer(r"\b[A-ZÉÈÀ]{2,6}\b", texte):
        if _sans_accents(m.group(0)) not in connus:
            trouves[m.group(0)] = None
    for m in re.finditer(r"(?<=[a-zàâçéèêëîïôûùüÿ,;] )([A-ZÉÈÀ][A-Za-zÀ-ÿ'’-]{2,})", texte):
        mot = m.group(1)
        base = _sans_accents(mot)
        morceaux = re.findall(r"[a-z0-9]+", base)   # « Franche-Comté » : chaque morceau est cherché dans l'article
        if base in TERMES_LIBRES or all(x in connus or re.sub(r"s$", "", x) in connus or x in TERMES_LIBRES for x in morceaux):
            continue
        trouves[mot] = None
    return list(trouves)


def verifier(texte: str, source: str, dernier_essai: bool = False, probas: list[int] | None = None) -> list[str]:
    problemes = []
    texte = "\n\n".join(parties(texte))  # les lignes --- ne sont ni des mots ni du Markdown
    mots = len(texte.split())
    maxi = MOTS_MAX_DERNIER_ESSAI if dernier_essai else MOTS_MAX
    if mots > maxi:
        problemes.append(f"{mots} mots : trop long de {mots - MOTS_MAX} mots (maximum {MOTS_MAX}). Réécris plus court, vise environ {MOTS_CIBLE} mots : "
                         "garde les trois scénarios et l'idée principale, supprime les détails secondaires et les chiffres en trop")
    elif mots < MOTS_MIN:
        problemes.append(f"{mots} mots (attendu entre {MOTS_MIN} et {MOTS_MAX})")
    if "**" in texte or "http" in texte or re.search(r"^\s*[-*•]", texte, re.M):
        problemes.append("pas de Markdown, de liste ni d'adresse web")
    if re.search(r"\b(bonjour|bienvenue|au revoir)\b", texte, re.I):
        problemes.append("ni bonjour, ni bienvenue, ni au revoir")
    if not re.search(r"\b(vous|votre|vos)\b", " ".join(texte.split()[-45:]), re.I):
        problemes.append("termine par une phrase chaleureuse à la deuxième personne qui ramène le sujet à la vie de l'auditeur "
                         "(« La prochaine fois que vous… »), sans « merci » ni « à demain » : le script ajoute la fermeture")
    if not re.search(r"\b(imaginez|imaginons|vous|votre|vos|pensez|supposez)\b", " ".join(texte.split()[:45]), re.I):
        problemes.append("commence par une mise en situation : une ou deux phrases courtes à la deuxième personne (« Imaginez : vous… ») "
                         "qui placent l'auditeur dans une scène de sa vie liée au sujet, avant la question du jour")
    for phrase in re.split(r"(?<=[.!?])\s+", texte):   # un pourcentage de probabilité est refusé ; un chiffre factuel reste permis
        if re.search(r"pour\s*cent|%", phrase, re.I) and re.search(r"chance|probab|sc[ée]nario|trajectoire|optimiste|sombre", phrase, re.I):
            problemes.append("dis les probabilités en fractions (« une chance sur quatre »), pas en pourcentage")
            break
    if re.search(MOTS_INTERDITS, texte, re.I):
        problemes.append("registre : aucun mot vulgaire ni péjoratif")
    phrases = [p for p in re.split(r"(?<=[.!?;:])\s+|\n+", texte) if len(p.split()) > 2]
    if phrases:
        limite = MOTS_PHRASE_MAX_DERNIER_ESSAI if dernier_essai else MOTS_PHRASE_MAX
        trop_longues = [p for p in phrases if len(p.split()) > limite]
        moyenne = sum(len(p.split()) for p in phrases) / len(phrases)
        if trop_longues or moyenne > MOTS_PHRASE_MOYENNE:
            cites = " | ".join("« " + " ".join(p.split()[:14]) + "… »" for p in trop_longues[:3])
            problemes.append(f"phrases trop longues pour l'oral (maximum {limite} mots, moyenne {MOTS_PHRASE_MOYENNE} ; "
                             f"{len(trop_longues)} trop longue(s), moyenne actuelle {moyenne:.0f})"
                             + (f", à couper en deux : {cites}" if cites else "") + " : une idée par phrase")
    if len(re.findall(r"sc[ée]narios?", texte, re.I)) < 2:
        problemes.append("nomme les trois « scénarios » avec ce mot (c'est la marque : « premier scénario », etc.)")
    if re.search(r"indicateurs?", texte, re.I):
        problemes.append("ne parle pas des indicateurs")
    sigles = sorted({m for m in re.findall(r"\b[A-ZÉ]{4,}\b", texte) if m not in SIGLES_PRONONCES})
    if sigles:
        problemes.append("sigle(s) épelé(s) à l'oral : " + ", ".join(sigles) + " : n'écris pas le sigle, décris-le en mots avec ce que dit l'article "
                         "(« le système antifraude de Galileo » pour OSNMA ; « l'instrument européen de prêts pour la défense » pour SAFE)")
    if any(len(re.findall(r"\bce qui\b", ph, re.I)) >= 2 for ph in phrases_brutes(texte)):
        problemes.append("phrase en chaîne (« …, ce qui …, ce qui … ») : une seule cause par phrase")
    if not re.search(r"\b(en clair|autrement dit|en d'autres termes|en deux mots)\b", texte, re.I):
        problemes.append("ajoute une phrase de reformulation (« En clair, … ») après la partie dense")
    inventes = termes_hors_article(texte, source)
    if inventes:
        problemes.append("termes absents de l'article (rien ne doit être inventé, appuie-toi uniquement sur l'édition) : "
                         + ", ".join(inventes) + " : supprime-les ou remplace-les par ce que dit l'article")
    problemes += controle_probabilites(texte, probas or [])
    connus = gp.nombres(source)
    inconnus = sorted(n for n in gp.nombres(texte) if n not in connus and not (n.isdigit() and int(n) <= 10))
    if inconnus:
        problemes.append("nombres absents de l'article : " + ", ".join(inconnus))
    return problemes


def source_controlee(ed: dict) -> str:
    """Texte source + date de l'édition, pour le contrôle des nombres et des noms.

    L'année de l'édition (« 2026 ») n'est pas dans le texte source mais le modèle l'écrit légitimement : sans elle, elle était refusée
    comme « nombre absent de l'article » (12 octobre 2026 : huit essais refusés, aucun épisode)."""
    source = gp.texte_source(ed)
    if ed.get("date"):
        source += f"\nDATE DE L'ÉDITION : {gp.date_longue(ed['date'])}"
    return source


def generer(ed: dict, modele: str, cle: str, essais: int = 4) -> str:
    import enrich_sujets as en  # relais de modèles gratuits

    source = source_controlee(ed)
    remarques: list[str] = []
    for n in range(1, essais + 1):
        resultat, _ = en._appeler_avec_reprises(construire_prompt(ed, remarques or None), modele, cle,
                                                temperature=0.6, max_tokens=12000, timeout=300)
        texte = re.sub(r"\n{3,}", "\n\n", str((resultat or {}).get("texte", "")).strip())
        remarques = verifier(texte, source, dernier_essai=(n == essais), probas=probabilites_edition(ed))
        print(f"  essai {n}/{essais} : {len(texte.split())} mots, {'conforme' if not remarques else '; '.join(remarques)}", flush=True)
        if not remarques:
            nb = len(parties(texte))
            if nb < 3:
                print(f"  ATTENTION : {nb} partie(s) seulement (séparateurs --- attendus) : peu ou pas de jingles.", flush=True)
            return texte + "\n\n" + SEPARATEUR + "\n\n" + fermeture(ed.get("date"))
    raise gp.PodcastError("texte refusé par le garde-fou : " + "; ".join(remarques))
