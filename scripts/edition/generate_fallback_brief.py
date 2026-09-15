"""
Repli automatique de la recherche (Étapes 0 à 3bis point 1 de
docs/routine-prompt.md) via OpenRouter — ajouté le 15 septembre 2026,
retour utilisateur explicite : « j'ai trop de pb de token, Claude Code se
bloque et tout le process se bloque ». Jusqu'ici, quand le trigger Claude
Code Remote « Scénario — recherche & brief quotidien » ne produisait pas
`editorial-briefs/{date}.json` à temps (blocage, limite de tokens, panne),
post-edition.yml échouait sèchement (« Brief introuvable ») et AUCUNE
édition ne sortait ce jour-là — pas de filet.

Ce script n'est JAMAIS le chemin principal : la routine Claude Code
Remote reste prioritaire (recherche interactive, WebSearch natif, accès
direct au dépôt). Ce n'est qu'une assurance, déclenchée uniquement quand
le brief du jour n'existe toujours pas au moment où post-edition.yml se
réveille (voir .github/workflows/post-edition.yml) — jamais en
concurrence avec une exécution CCR encore en cours (le vrai brief, une
fois committé sur `main`, prime toujours).

Mécanique :
  1. Rassemble tout le contexte nécessaire depuis le dépôt déjà checkouté
     (sujets-prioritaires.md, docs/sujets-a-suivre.md, les dernières
     éditions d'archives.html pour l'anti-doublon, le schéma exact du
     brief) — le modèle n'a PAS d'accès fichier, seulement la recherche
     web, donc tout ce contexte local doit être injecté dans le prompt.
  2. Un seul appel OpenRouter, avec le server tool `openrouter:web_search`
     (le modèle décide lui-même combien de recherches faire et sur quoi,
     exécutées côté OpenRouter — jamais de cycle tool_calls à gérer ici,
     voir call_openrouter()) — les RÈGLES ÉDITORIALES elles-mêmes sont
     extraites telles quelles de docs/routine-prompt.md (jamais dupliquées
     ici : une seule source de vérité, qui reste modifiable sans jamais
     toucher ce script).
  3. Valide la réponse avec generate_daily_edition.validate_brief() — les
     mêmes règles que pour un brief humain/CCR, aucun passe-droit. Un seul
     retry (même discipline que le reste du pipeline, MAX_RETRIES=1) avec
     le détail des erreurs renvoyé au modèle.
  4. Écrit `editorial-briefs/{date}.json` directement au vrai chemin (pas
     de bac à sable ici : un seul fichier, contrairement à
     generate_post_edition.py qui en écrit beaucoup d'interdépendants) —
     AUCUN commit/push : le workflow appelant s'en charge, exactement
     comme le fait déjà generate_post_edition.py --publish.

Usage :
    export OPENROUTER_API_KEY=sk-or-v1-...
    python3 generate_fallback_brief.py --date 2026-09-15
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from generate_daily_edition import (
    DEFAULT_MODEL,
    GenerationError,
    InvalidModelJSON,
    MAX_RETRIES,
    call_openrouter,
    validate_brief,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ROUTINE_PROMPT_PATH = REPO_ROOT / "docs" / "routine-prompt.md"
BRIEF_FORMAT_PATH = REPO_ROOT / "docs" / "routine-brief-format.md"
SUJETS_PRIORITAIRES_PATH = REPO_ROOT / "sujets-prioritaires.md"
SUJETS_A_SUIVRE_PATH = REPO_ROOT / "docs" / "sujets-a-suivre.md"
ARCHIVES_HTML_PATH = REPO_ROOT / "archives.html"
BRIEFS_DIR = REPO_ROOT / "editorial-briefs"

_RECHERCHE_START_MARKER = "## STATUT ACTUEL"
_RECHERCHE_END_MARKER = "## ⚠️ RÉFÉRENCE ÉDITORIALE HISTORIQUE"

_JOURS_FR = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def extract_recherche_instructions():
    """Extrait la portion active (recherche-only, Étapes 0 à 3bis) de
    docs/routine-prompt.md — jamais recopiée/reformulée ici, pour qu'une
    modification des règles éditoriales (fait par ailleurs, pour la
    routine CCR) se répercute automatiquement sur ce repli sans jamais
    avoir à le maintenir en double. Échoue fort si les deux marqueurs
    disparaissent (signal qu'une restructuration du fichier a cassé cette
    extraction, mieux vaut un crash net qu'un prompt silencieusement
    tronqué)."""
    text = ROUTINE_PROMPT_PATH.read_text(encoding="utf-8")
    start = text.index(_RECHERCHE_START_MARKER)
    end = text.index(_RECHERCHE_END_MARKER, start)
    return text[start:end].strip()


def extract_brief_format_doc():
    return BRIEF_FORMAT_PATH.read_text(encoding="utf-8").strip()


def read_optional(path):
    return path.read_text(encoding="utf-8").strip() if path.exists() else "(fichier absent ou vide)"


def extract_priority_queue(path=SUJETS_PRIORITAIRES_PATH):
    """sujets-prioritaires.md fait plus de 100 Ko (dizaines de sujets déjà
    traités, chacun avec son commentaire de recherche complet, jamais
    purgés) — mais l'Étape 0 n'a jamais besoin que du PREMIER sujet non
    coché de chaque section (« elle prend le premier sujet non coché »,
    voir l'intro du fichier), jamais de la file entière. Ne garde que le
    texte d'intro + chaque titre de section + son premier `- [ ]`, avec le
    commentaire de recherche qui l'accompagne s'il y en a un — réduit le
    prompt d'un facteur ~15 sans perdre l'information dont Étape 0 se sert
    réellement."""
    if not path.exists():
        return "(fichier absent ou vide)"
    import re

    text = path.read_text(encoding="utf-8")
    head, *sections = re.split(r"\n(?=## )", text)
    out = [head.split("\n---\n")[0].strip()]
    for sec in sections:
        title_line, _, body = sec.partition("\n")
        m = re.search(r"^- \[ \] .*?(?=\n- \[|\Z)", body, re.S | re.M)
        out.append(title_line + "\n" + (m.group(0).strip() if m else "(rien de non coché dans cette section)"))
    return "\n\n".join(out)


def summarize_recent_archives(limit=20):
    """Extrait (date, domaine, titre, question) des `limit` dernières
    éditions d'archives.html — jamais un aller-retour BeautifulSoup sur
    tout le fichier (lecture seule ici, mais même discipline de robustesse
    par regex que generate_archives_table.py sur ce type de fichier).
    Sert de base à l'anti-doublon (Étape 0bis) : le modèle n'a pas accès
    au dépôt, donc ce résumé compact est sa seule fenêtre sur les éditions
    déjà publiées."""
    import re

    text = ARCHIVES_HTML_PATH.read_text(encoding="utf-8")
    row_re = re.compile(
        r'<tr data-domain="([^"]*)"[^>]*data-date="([^"]*)"[^>]*>.*?'
        r'<a href="archives/[^"]*\.html" title="([^"]*)">([^<]*)</a>',
        re.S,
    )
    rows = []
    for m in row_re.finditer(text):
        domain, date, question, title = m.groups()
        rows.append(f"- {date} ({domain}) — {title} : {question}")
        if len(rows) >= limit:
            break
    return "\n".join(rows) if rows else "(aucune édition trouvée dans archives.html)"


def build_prompt(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    jour = _JOURS_FR[dt.weekday()]

    return f"""Tu remplaces EXCEPTIONNELLEMENT la routine de recherche éditoriale
habituelle (Claude Code Remote) pour « Scénario », un site quotidien de
scénarios chiffrés — uniquement parce qu'elle n'a pas pu produire le
brief du jour à temps (blocage technique). Applique EXACTEMENT les mêmes
règles éditoriales qu'elle, reproduites ci-dessous telles quelles, extraites
de docs/routine-prompt.md.

**Ce que tu dois produire, et RIEN d'autre** : le JSON du brief éditorial
du jour (schéma exact plus bas), pour la date {date_str} ({jour}). Toute
mention dans le texte ci-dessous de committer sur git, de déclencher un
pipeline GitHub Actions, ou de t'arrêter après un résumé ne te concerne
PAS — tu n'as accès à rien de tout ça, un script séparé s'en charge après
toi. Ignore ces instructions, produis uniquement le JSON final.

**Tu n'as PAS accès au dépôt Git ni à ses fichiers** — tout le contexte
nécessaire (sujets prioritaires, suivis actifs, éditions récentes pour
l'anti-doublon) est fourni intégralement ci-dessous. Tu as en revanche un
outil de recherche web réel : utilise-le autant de fois que nécessaire,
pour la sélection du sujet comme pour la vérification factuelle — jamais
une affirmation ou un chiffre depuis ta seule mémoire sans recherche
récente qui le confirme.

=== RÈGLES ÉDITORIALES (docs/routine-prompt.md, extrait textuel) ===
{extract_recherche_instructions()}

=== SCHÉMA EXACT DU BRIEF À PRODUIRE (docs/routine-brief-format.md) ===
{extract_brief_format_doc()}

=== sujets-prioritaires.md (racine du dépôt — Étape 0, seulement le 1er sujet non coché de chaque section, voir cette règle dans le fichier lui-même) ===
{extract_priority_queue()}

=== docs/sujets-a-suivre.md (suivis actifs + anti-doublon) ===
{read_optional(SUJETS_A_SUIVRE_PATH)}

=== Éditions récentes, les {20} dernières (archives.html — anti-doublon Étape 0bis) ===
{summarize_recent_archives()}

=== Contexte du jour ===
Date : {date_str} ({jour})

Réponds UNIQUEMENT avec le JSON du brief — aucun texte avant ni après,
aucune balise markdown autour, un objet JSON valide et rien d'autre.
"""


def generate_fallback_brief(date_str, model, api_key, timeout=480):
    prompt = build_prompt(date_str)
    tools = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 6}}]

    last_errors = None
    for attempt in range(MAX_RETRIES + 1):
        this_prompt = prompt
        if attempt > 0:
            this_prompt += (
                "\n\n=== CORRECTIONS REQUISES (essai précédent invalide) ===\n"
                + "\n".join(f"- {e}" for e in last_errors)
                + "\nRenvoie le JSON complet du brief, corrigé."
            )
        try:
            brief, usage = call_openrouter(
                this_prompt, model, api_key,
                temperature=0.4, max_tokens=12000, timeout=timeout, tools=tools,
            )
        except InvalidModelJSON as e:
            print(f"[fallback-brief] essai {attempt + 1} : JSON invalide — {e}", file=sys.stderr)
            last_errors = [f"réponse non-JSON : {e}"]
            continue

        errors = validate_brief(brief)
        if not errors:
            return brief, usage
        print(f"[fallback-brief] essai {attempt + 1} : brief invalide :", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        last_errors = errors

    raise GenerationError(
        f"brief de repli invalide après {MAX_RETRIES + 1} essai(s), rien n'est écrit :\n  - "
        + "\n  - ".join(last_errors)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="date du brief à produire, AAAA-MM-JJ")
    parser.add_argument("--model", default=None, help="modèle OpenRouter (défaut : DEFAULT_MODEL/variable OPENROUTER_MODEL)")
    parser.add_argument("--timeout", type=int, default=480, help="délai max de l'appel OpenRouter, en secondes (défaut 480 — plusieurs recherches web côté serveur peuvent prendre du temps)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise GenerationError("OPENROUTER_API_KEY manquant dans l'environnement")

    model = args.model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL
    print(f"[fallback-brief] génération du brief du {args.date} — modèle {model}", file=sys.stderr)

    brief, usage = generate_fallback_brief(args.date, model, api_key, timeout=args.timeout)

    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BRIEFS_DIR / f"{args.date}.json"
    out_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[fallback-brief] brief écrit : {out_path} (sujet : {brief.get('sujet', {}).get('titre_propose', '?')})", file=sys.stderr)
    print(f"[fallback-brief] coût ≈ {usage.get('cost', '?')} $ (modèle {usage.get('model', model)})", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except (GenerationError, InvalidModelJSON) as e:
        print(f"[fallback-brief] ERREUR : {e}", file=sys.stderr)
        sys.exit(1)
