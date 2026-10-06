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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_podcast as gp  # noqa: E402

MOTS_MIN, MOTS_MAX = 420, 720  # 3 à 5 minutes de lecture
SEPARATEUR = "---"
MOTS_PHRASE_MAX, MOTS_PHRASE_MOYENNE = 32, 20   # pédagogie : phrases courtes à l'oral (textes validés : moyenne 13-15, maximum 28)
# Sept accueils et sept fermetures, écrits à l'avance (jamais par le modèle) : on en tire un par jour pour que l'épisode
# ne sonne pas toujours pareil. Règles communes : vouvoiement, « évolutions » seulement dans l'accueil, phrases courtes.
# Les fermetures changent seulement au début : la fin est un rituel fixe (RITUEL), pour que la devise devienne celle du site. Le tirage dépend de la date (voir _rangs) : il se refait à l'identique si l'on
# régénère un épisode.
OUVERTURES = (
    "Bienvenue sur Scénario. Chaque jour, une question d'actualité, et trois évolutions possibles. On y va !",
    "Bonjour, et bienvenue sur Scénario. Une question d'actualité, trois évolutions possibles. Voyons cela ensemble.",
    "Vous écoutez Scénario. Chaque jour, une question d'actualité, et trois évolutions possibles. C'est parti.",
    "Bienvenue sur Scénario, le rendez-vous quotidien d'une question d'actualité et de ses trois évolutions possibles. Commençons.",
    "Bonjour à toutes et à tous, bienvenue sur Scénario. Aujourd'hui encore, une question d'actualité, et trois évolutions possibles. Allons-y.",
    "Scénario, c'est une question d'actualité par jour, et trois évolutions possibles. Bienvenue, installez-vous : on commence.",
    "Bienvenue sur Scénario. Prenez un moment avec nous : une question d'actualité, trois évolutions possibles. Allons-y.",
)
RITUEL = "Prenez soin de vous. Rien n'est écrit à l'avance. À demain, pour un nouveau scénario."   # devise du site, dite chaque jour mot pour mot : « Rien n'est écrit à l'avance. »
FERMETURES = tuple(debut + " " + RITUEL for debut in (
    "Voilà pour aujourd'hui. Merci de nous avoir écoutés. L'édition complète est sur lesscenarios.fr.",
    "C'est tout pour aujourd'hui. Merci d'avoir été avec nous. Tout est sur lesscenarios.fr.",
    "Voilà qui conclut cette édition. Merci de votre attention. L'édition complète est sur lesscenarios.fr.",
    "Merci d'avoir été là. Si le sujet vous a donné envie d'aller plus loin, tout est sur lesscenarios.fr.",
    "Nous nous arrêtons ici. Merci de votre confiance. Retrouvez tout sur lesscenarios.fr.",
    "C'est la fin de cet épisode. Merci de nous avoir suivis. Les sources sont sur lesscenarios.fr.",
    "Merci de votre écoute, et belle journée à vous. L'édition complète est sur lesscenarios.fr.",
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
- Du langage parlé : phrases courtes, tournures naturelles, pas de liste, pas de Markdown, pas d'adresse web.
- Pas de tableau d'indicateurs : ne récite pas les indicateurs chiffrés des scénarios. Garde peu de chiffres : ceux qui font comprendre le sujet, et les probabilités des scénarios, TOUJOURS dites en fractions parlées : « une chance sur quatre » pour 25 %, « une chance sur deux » pour 50 %, « trois chances sur quatre » pour 75 %, « une chance sur trois », « une chance sur cinq », « une chance sur dix ». JAMAIS « pour cent » ni le signe %, même si l'article donne des pourcentages ; arrondis à la fraction la plus proche.
- Ne dis jamais « selon l'article », ne parle ni de toi ni de l'intelligence artificielle. Pas de « bonjour » ni de « bienvenue » ni d'au revoir : commence directement par la question, le script ajoute la fermeture.

STRUCTURE (entre {MOTS_MIN} et {MOTS_MAX} mots, soit 3 à 5 minutes)
1. La question du jour, en une ou deux phrases.
2. Ce que l'on sait : les faits qui posent la question, avec un ou deux exemples concrets.
3. Le fond du problème : à quoi cherche-t-on à répondre, et pourquoi la réponse n'est pas évidente.
4. Les trois scénarios, un par un : le plus optimiste (favorable), le plus probable (stable, dis-le clairement), le plus sombre (dégradé), chacun avec sa probabilité, en trois ou quatre phrases courtes : l'idée centrale, puis ce que cela change concrètement pour les gens (un vol retardé, une coupure de courant…), jamais le mécanisme technique ni un nom de technologie.
5. L'impact pour la France, en deux ou trois phrases.
6. Ce qu'on surveillera pour savoir lequel se réalise.

EXEMPLE DE STYLE ATTENDU (autre édition, ne reprends AUCUN de ses faits) :
{exemple}

LEXIQUE (termes à expliquer en mots simples à leur première mention, voir PÉDAGOGIE) :
{lexique}

ARTICLE
{gp.texte_source(ed)}{suite}

SÉPARATEURS : entre les grandes parties (1 | 2 | 3 | 4 | 5 | 6 ci-dessus), écris une ligne qui contient uniquement trois tirets (---). Un jingle musical y sera placé. Pas d'autre séparateur ; à l'intérieur d'une partie, les paragraphes sont séparés par une ligne vide.

Réponds UNIQUEMENT avec un JSON : {{"texte": "le texte parlé, parties séparées par une ligne ---"}}"""


def parties(texte: str) -> list[str]:
    """Le texte découpé aux lignes « --- » (parties vides ignorées)."""
    return [p.strip() for p in re.split(r"(?m)^\s*---\s*$", texte) if p.strip()]


# Mots vulgaires ou péjoratifs refusés par le contrôle (le texte est alors réécrit).
MOTS_INTERDITS = (r"\b(gueules?|merdes?|merdique|putain|bordel|con|cons|conne|connes|connard\w*|salop\w*|enfoir\w*|"
                  r"débiles?|crétins?|idiot\w*|imbéciles?|stupides?|nul|nuls|pourri\w*|dégueu\w*|foutre|foutu\w*|"
                  r"bouffons?|minables?|ridicules?|pathétiques?|ringard\w*|naze\w*|chiant\w*|crevard\w*)\b")


# Sigles de quatre lettres ou plus qui se disent comme des mots (les autres sont refusés : « O-S-N-M-A » ne dit rien à l'oreille).
SIGLES_PRONONCES = {"OTAN", "NASA", "UNESCO", "OPEP", "FIFA", "UEFA", "INSEE", "SMIC", "NATO", "ARENH"}


def phrases_brutes(texte: str) -> list[str]:
    return [p for p in re.split(r"(?<=[.!?])\s+|\n+", texte) if p.strip()]


MOTS_MAX_DERNIER_ESSAI, MOTS_CIBLE = 800, 620   # dernier essai : jusqu'à ~5 min 40 s ; consigne de raccourcissement : viser 620 mots
MOTS_PHRASE_MAX_DERNIER_ESSAI = 40   # dernier essai : une phrase un peu longue (33 à 40 mots) ne doit pas faire perdre l'épisode du jour


def verifier(texte: str, source: str, dernier_essai: bool = False) -> list[str]:
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
        problemes.append("sigle(s) épelé(s) à l'oral : " + ", ".join(sigles) + " : donne leur nom en mots (« le système antifraude de Galileo »)")
    if any(len(re.findall(r"\bce qui\b", ph, re.I)) >= 2 for ph in phrases_brutes(texte)):
        problemes.append("phrase en chaîne (« …, ce qui …, ce qui … ») : une seule cause par phrase")
    if not re.search(r"\b(en clair|autrement dit|en d'autres termes|en deux mots)\b", texte, re.I):
        problemes.append("ajoute une phrase de reformulation (« En clair, … ») après la partie dense")
    connus = gp.nombres(source)
    inconnus = sorted(n for n in gp.nombres(texte) if n not in connus and not (n.isdigit() and int(n) <= 10))
    if inconnus:
        problemes.append("nombres absents de l'article : " + ", ".join(inconnus))
    return problemes


def generer(ed: dict, modele: str, cle: str, essais: int = 4) -> str:
    import enrich_sujets as en  # relais de modèles gratuits

    source = gp.texte_source(ed)
    remarques: list[str] = []
    for n in range(1, essais + 1):
        resultat, _ = en._appeler_avec_reprises(construire_prompt(ed, remarques or None), modele, cle,
                                                temperature=0.6, max_tokens=12000, timeout=300)
        texte = re.sub(r"\n{3,}", "\n\n", str((resultat or {}).get("texte", "")).strip())
        remarques = verifier(texte, source, dernier_essai=(n == essais))
        print(f"  essai {n}/{essais} : {len(texte.split())} mots, {'conforme' if not remarques else '; '.join(remarques)}", flush=True)
        if not remarques:
            nb = len(parties(texte))
            if nb < 3:
                print(f"  ATTENTION : {nb} partie(s) seulement (séparateurs --- attendus) : peu ou pas de jingles.", flush=True)
            return texte + "\n\n" + SEPARATEUR + "\n\n" + fermeture(ed.get("date"))
    raise gp.PodcastError("texte refusé par le garde-fou : " + "; ".join(remarques))
