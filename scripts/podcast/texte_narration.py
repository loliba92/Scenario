"""Écrit le texte parlé d'un épisode à UNE voix, à partir d'une édition publiée (style validé le 3 octobre 2026).

Le propriétaire a rejeté le dialogue à deux voix (trop « IA », trop de chiffres). Le texte attendu : une question, les
faits qui la posent, le problème de fond, les trois scénarios dans l'ensemble, l'impact pour la France, ce qu'on
surveillera. Aucun tableau d'indicateurs. Rien qui ne figure pas dans l'article (garde-fou sur les nombres).
La fermeture est écrite par le script, jamais par le modèle.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_podcast as gp  # noqa: E402

MOTS_MIN, MOTS_MAX = 420, 720  # 3 à 5 minutes de lecture
SEPARATEUR = "---"
OUVERTURE = ("Bienvenue sur Scénario. Chaque jour, une actualité, une question, "
             "et trois façons dont les choses peuvent tourner. On y va.")
FERMETURE = "Voilà pour aujourd'hui. L'édition complète est sur lesscenarios.fr. À demain, pour un nouveau scénario."
EXEMPLE = (Path(__file__).resolve().parents[2] / "podcast" / "textes" / "2026-10-03.txt")


def construire_prompt(ed: dict, remarques: list[str] | None = None) -> str:
    exemple = EXEMPLE.read_text(encoding="utf-8").strip() if EXEMPLE.exists() else ""
    suite = ("\n\nTa version précédente a été refusée pour ces raisons, corrige-les :\n- " + "\n- ".join(remarques)) if remarques else ""
    return f"""Tu écris le texte parlé d'un court podcast quotidien du site d'actualité Scénario (lesscenarios.fr), à partir de l'édition du {gp.date_longue(ed['date'])} ci-dessous. Une seule voix, chaleureuse, qui parle à un ami curieux.

RÈGLES ABSOLUES
- N'ajoute AUCUN fait, chiffre, nom, date ni exemple qui ne figure pas dans l'article.
- Du langage parlé : phrases courtes, tournures naturelles, pas de liste, pas de Markdown, pas d'adresse web.
- Pas de tableau d'indicateurs : ne récite pas les indicateurs chiffrés des scénarios. Garde peu de chiffres : ceux qui font comprendre le sujet, et les probabilités des scénarios (dis « environ une chance sur trois », « une chance sur deux », « une chance sur cinq » ou « 30 pour cent », au choix).
- Ne dis jamais « selon l'article », ne parle ni de toi ni de l'intelligence artificielle. Pas de « bonjour » ni de « bienvenue » ni d'au revoir : commence directement par la question, le script ajoute la fermeture.

STRUCTURE (entre {MOTS_MIN} et {MOTS_MAX} mots, soit 3 à 5 minutes)
1. La question du jour, en une ou deux phrases.
2. Ce que l'on sait : les faits qui posent la question, avec un ou deux exemples concrets.
3. Le fond du problème : à quoi cherche-t-on à répondre, et pourquoi la réponse n'est pas évidente.
4. Les trois scénarios, un par un, dans l'ensemble : le plus optimiste (favorable), le plus probable (stable, dis-le clairement), le plus sombre (dégradé), chacun avec sa probabilité et l'idée centrale, sans détail chiffré.
5. L'impact pour la France, en deux ou trois phrases.
6. Ce qu'on surveillera pour savoir lequel se réalise.

EXEMPLE DE STYLE ATTENDU (autre édition, ne reprends AUCUN de ses faits) :
{exemple}

ARTICLE
{gp.texte_source(ed)}{suite}

SÉPARATEURS : entre les grandes parties (1 | 2 | 3 | 4 | 5 | 6 ci-dessus), écris une ligne qui contient uniquement trois tirets (---). Un jingle musical y sera placé. Pas d'autre séparateur ; à l'intérieur d'une partie, les paragraphes sont séparés par une ligne vide.

Réponds UNIQUEMENT avec un JSON : {{"texte": "le texte parlé, parties séparées par une ligne ---"}}"""


def parties(texte: str) -> list[str]:
    """Le texte découpé aux lignes « --- » (parties vides ignorées)."""
    return [p.strip() for p in re.split(r"(?m)^\s*---\s*$", texte) if p.strip()]


def verifier(texte: str, source: str) -> list[str]:
    problemes = []
    texte = "\n\n".join(parties(texte))  # les lignes --- ne sont ni des mots ni du Markdown
    mots = len(texte.split())
    if not MOTS_MIN <= mots <= MOTS_MAX:
        problemes.append(f"{mots} mots (attendu entre {MOTS_MIN} et {MOTS_MAX})")
    if "**" in texte or "http" in texte or re.search(r"^\s*[-*•]", texte, re.M):
        problemes.append("pas de Markdown, de liste ni d'adresse web")
    if re.search(r"\b(bonjour|bienvenue|au revoir)\b", texte, re.I):
        problemes.append("ni bonjour, ni bienvenue, ni au revoir")
    if re.search(r"indicateurs?", texte, re.I):
        problemes.append("ne parle pas des indicateurs")
    connus = gp.nombres(source)
    inconnus = sorted(n for n in gp.nombres(texte) if n not in connus and not (n.isdigit() and int(n) <= 10))
    if inconnus:
        problemes.append("nombres absents de l'article : " + ", ".join(inconnus))
    return problemes


def generer(ed: dict, modele: str, cle: str, essais: int = 3) -> str:
    import enrich_sujets as en  # relais de modèles gratuits

    source = gp.texte_source(ed)
    remarques: list[str] = []
    for n in range(1, essais + 1):
        resultat, _ = en._appeler_avec_reprises(construire_prompt(ed, remarques or None), modele, cle,
                                                temperature=0.6, max_tokens=12000, timeout=300)
        texte = re.sub(r"\n{3,}", "\n\n", str((resultat or {}).get("texte", "")).strip())
        remarques = verifier(texte, source)
        print(f"  essai {n}/{essais} : {len(texte.split())} mots, {'conforme' if not remarques else '; '.join(remarques)}", flush=True)
        if not remarques:
            nb = len(parties(texte))
            if nb < 3:
                print(f"  ATTENTION : {nb} partie(s) seulement (séparateurs --- attendus) : peu ou pas de jingles.", flush=True)
            return texte + "\n\n" + SEPARATEUR + "\n\n" + FERMETURE
    raise gp.PodcastError("texte refusé par le garde-fou : " + "; ".join(remarques))
