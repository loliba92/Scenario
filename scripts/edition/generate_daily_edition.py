"""
Prototype (Phase 1) de la chaîne rédaction OpenRouter — voir le cahier des
charges validé dans la conversation qui a précédé ce script et
`docs/routine-redaction-prompt.md`/`docs/routine-brief-format.md`.

Ce script :
  1. charge un brief éditorial déjà vérifié (docs/routine-brief-format.md) ;
  2. appelle OpenRouter (modèle Claude Sonnet par défaut) avec le prompt de
     rédaction (docs/routine-redaction-prompt.md) ;
  3. valide strictement la réponse (jamais de confiance aveugle au
     modèle) ;
  4. construit le HTML final via scripts/edition/build_html.py (Python
     déterministe, le modèle ne produit jamais le HTML complet) ;
  5. écrit une sortie de test locale — AUCUN commit, AUCUN push, AUCUNE
     publication. Voir .github/workflows/edition.yml.

Usage :
    export OPENROUTER_API_KEY=sk-or-v1-...
    python3 scripts/edition/generate_daily_edition.py --brief editorial-briefs/{AAAA-MM-JJ}.json

    # Sans clé API, pour tester la mécanique (validations + templating)
    # avec une réponse de modèle déjà enregistrée (brief-exemple fictif,
    # jamais un vrai brief daté — voir scripts/edition/fixtures/) :
    python3 scripts/edition/generate_daily_edition.py --brief scripts/edition/fixtures/2026-09-20.json --dry-run
"""
import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

import build_html

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# Phase 2 déploiement optimisation coût (21 septembre 2026) :
# Google Gemini 3.7 Flash ($0.0222 vs $0.171 Sonnet = 87% réduction, JSON valide 100%)
# Testé le 21/09: seul modèle avec JSON valide parmi alternatives (Gemini, Nova, Qwen)
# Xiaomi MIMO v2.5 rejeté: qualité insuffisante, contenu tronqué
# NVIDIA Nemotron rejeté: JSON invalide pour rédaction
# Voir docs/alternatives-tests/ et scripts/edition/test-alternatives.py
DEFAULT_MODEL = "google/gemini-3.7-flash"  # Phase 2 production (qualité + validité garantie)
SONNET_5_BACKUP = "anthropic/claude-sonnet-5"  # Rollback si besoin
REDACTION_PROMPT_PATH = REPO_ROOT / "docs" / "routine-redaction-prompt.md"
MIN_WORDS = 1100
MIN_ESSENTIEL_WORDS = 110  # essentiel_box (4 paragraphes) — voir validate_content_schema()
# phrase_a_retenir — même plafond que l'ancien CHIFFRE_MAX_CHARS de
# scripts/pub/generate_daily_pub.py (gabarit d'image pub sans défilement,
# voir validate_content_schema()).
PHRASE_A_RETENIR_MAX_CHARS = 280
MAX_RETRIES = 2  # relevé de 1 à 2 le 17 septembre 2026 (incident réel : 2 essais
# consécutifs rejetés pour 2 raisons DIFFÉRENTES le même run — lexique non
# utilisé puis delta_france.word, ce 2e cas s'étant révélé être un vrai bug
# de validation, voir plus bas — mais rester avec une seule marge de retry
# expose à épuiser le budget sur un pur hasard éditorial, jamais un signe
# que le sujet est infaisable). Coût marginal : un essai de plus à ~0,11 $
# seulement dans le pire cas (2 rejets), jamais facturé si le 1er passe.


class GenerationError(Exception):
    pass


class InvalidModelJSON(GenerationError):
    """Levée uniquement quand la réponse du modèle n'est pas un JSON valide,
    même après tentative de réparation automatique (voir
    repair_unescaped_lexref_quotes()) — distincte de GenerationError levée
    pour une erreur réseau/timeout dans call_openrouter(), qui reste un
    échec net jamais retenté (voir sa docstring). Un JSON invalide, lui,
    rentre dans la même boucle de retry de validation que les autres
    erreurs de schéma dans main() : incident réel du 14 septembre 2026
    (run 34841534063) où le modèle recopiait le balisage `.lex-ref` du
    prompt avec des guillemets HTML non échappés dans un attribut
    (`class="lex-ref"`), cassant le parsing JSON — ce type d'erreur
    abandonnait alors tout l'essai au lieu de déclencher un 2e essai."""


# ---------------------------------------------------------------------------
# Récupération image Pexels (intégration preview)
# ---------------------------------------------------------------------------
def fetch_preview_image(image_keywords, timeout=25):
    """Récupère l'image Pexels pour la preview sans écrire d'assets.
    Retourne un dict photo {og_image_url, hero_image_url, alt, photographer, pexels_url}
    ou None si la récupération échoue (non-bloquant). Utilise fetch_topic_image.py
    pour la recherche, extrait le 1er candidat des credits.json.
    """
    if not image_keywords:
        return None

    fetch_script = REPO_ROOT / "scripts" / "social" / "fetch_topic_image.py"
    if not fetch_script.exists():
        print("[edition] fetch_topic_image.py introuvable", file=sys.stderr)
        return None

    candidates_dir = Path("/tmp/scenario-preview-image-candidates")
    candidates_dir.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [sys.executable, str(fetch_script), image_keywords, "--count", "1", "--out", str(candidates_dir)],
            check=True, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.CalledProcessError as e:
        print(f"[edition] fetch_topic_image.py échoué : {(e.stderr or '')[-300:]}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"[edition] fetch_topic_image.py délai dépassé ({timeout}s)", file=sys.stderr)
        return None

    credits_path = candidates_dir / "credits.json"
    if not credits_path.exists():
        print("[edition] aucun credits.json — pas d'image trouvée", file=sys.stderr)
        return None

    try:
        with open(credits_path, encoding="utf-8") as f:
            credits = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[edition] erreur lecture credits.json : {e}", file=sys.stderr)
        return None

    if not credits:
        print("[edition] credits.json vide", file=sys.stderr)
        return None

    chosen = credits[0]
    if chosen.get("source") != "pexels":
        print(f"[edition] candidat n'est pas de Pexels (source: {chosen.get('source')})", file=sys.stderr)
        return None

    original_url = chosen.get("original_url")
    if not original_url:
        print("[edition] original_url manquant dans les credits", file=sys.stderr)
        return None

    # Construire l'URL d'image carrée recadée (1080x1080) via Pexels CDN
    # Réutilise la logique de square_crop_url de fetch_topic_image.py
    from urllib.parse import urlencode
    sep = "&" if "?" in original_url else "?"
    og_image_url = f"{original_url}{sep}auto=compress&cs=tinysrgb&fit=crop&w=1080&h=1080&crop=bottom"

    return {
        "og_image_url": og_image_url,
        "hero_image_url": og_image_url,
        "alt": f"Illustration du sujet: {image_keywords}",
        "photographer": chosen.get("photographer", "Photographe Pexels"),
        "pexels_url": chosen.get("pexels_url", "https://www.pexels.com/"),
    }


# ---------------------------------------------------------------------------
# Chargement brief + prompt
# ---------------------------------------------------------------------------
def load_brief(path):
    with open(path, encoding="utf-8") as f:
        brief = json.load(f)
    errors = validate_brief(brief)
    if errors:
        raise GenerationError("Brief invalide :\n  - " + "\n  - ".join(errors))
    return brief


def validate_brief(brief):
    """Validations minimales du brief lui-même (voir docs/routine-brief-format.md
    § Règles de validité) — avant même d'appeler OpenRouter, pour ne pas
    payer un appel sur un brief cassé."""
    errors = []
    required_top = ["date", "registre", "sujet", "scenarios_prospectifs", "indicateurs_kpi", "sources"]
    for key in required_top:
        if key not in brief:
            errors.append(f"champ obligatoire manquant : {key}")
    if errors:
        return errors

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", brief["date"]):
        errors.append("date : format AAAA-MM-JJ attendu")

    question = brief.get("sujet", {}).get("question_posee", "")
    if not question:
        errors.append("sujet.question_posee manquant")
    elif len(question) > 200:
        errors.append(f"sujet.question_posee dépasse 200 caractères ({len(question)})")

    sp = brief.get("scenarios_prospectifs", {})
    for kind in ("favorable", "stable", "degrade"):
        if kind not in sp:
            errors.append(f"scenarios_prospectifs.{kind} manquant")
    if not errors:
        total = sum(sp[k].get("probabilite_suggeree", 0) for k in ("favorable", "stable", "degrade"))
        if abs(total - 100) > 10:
            errors.append(f"avertissement : somme des probabilités suggérées = {total} (écart > 10 points)")

    n_kpi = len(brief.get("indicateurs_kpi", []))
    if not (1 <= n_kpi <= 3):
        errors.append(f"indicateurs_kpi : {n_kpi} éléments (attendu 1 à 3)")

    if not brief.get("sources"):
        errors.append("sources : au moins 1 élément attendu")
    else:
        source_ids = {s["id"] for s in brief["sources"] if "id" in s}
        for fait in brief.get("faits_verifies", []):
            for sid in fait.get("sources", []):
                if sid not in source_ids:
                    errors.append(f"faits_verifies référence une source inconnue : {sid}")

    # Ajouté le 16 septembre 2026 (retour utilisateur : forcer 2 encarts
    # pédagogiques ne se justifie que sur un sujet réellement difficile —
    # sur un sujet déjà simple, ça pousse justement vers le contenu
    # artificiel que le garde-fou plus bas cherche à éviter). Note de 1
    # (évident) à 5 (sujet technique) : « est-ce qu'un lecteur français
    # sans connaissance préalable du domaine comprend ce sujet sans
    # effort ? ». Voir docs/routine-brief-format.md pour le barème complet.
    complexite = brief.get("sujet", {}).get("complexite")
    if not isinstance(complexite, int) or isinstance(complexite, bool) or not (1 <= complexite <= 5):
        errors.append(f"sujet.complexite : {complexite!r} (entier entre 1 et 5 requis)")

    # comprendre_box : le nombre requis dépend de sujet.complexite
    # ci-dessus. En dessous de 3/5, au moins 1 reste requis (jamais 0 —
    # c'est la règle posée le 16 septembre 2026 au matin) ; à partir de
    # 3/5, exactement 2 sont requis (retour utilisateur du même jour,
    # l'après-midi : « plus pédagogique » sur les sujets qui le
    # justifient) — voir docs/routine-prompt.md § Encart « Comprendre »
    # pour le garde-fou anti contenu artificiel (le compte est vérifié
    # ici, jamais la qualité du focus lui-même, qui reste un jugement
    # éditorial en amont de la recherche).
    n_comprendre = len(brief.get("encarts_decides", {}).get("comprendre_box") or [])
    if isinstance(complexite, int) and not isinstance(complexite, bool) and 1 <= complexite <= 5:
        if complexite >= 3:
            if n_comprendre != 2:
                errors.append(
                    f"encarts_decides.comprendre_box : {n_comprendre} élément(s) "
                    f"(exactement 2 requis, sujet complexité {complexite}/5)"
                )
        else:
            if n_comprendre < 1:
                errors.append(
                    f"encarts_decides.comprendre_box : {n_comprendre} élément(s) "
                    f"(au moins 1 requis même sur un sujet simple, complexité {complexite}/5)"
                )

    # Seul un "avertissement :" ne bloque pas la génération — tout le reste
    # est bloquant. Distinction volontairement explicite plutôt qu'un
    # simple len(errors) > 0, pour ne jamais élargir silencieusement ce
    # qui est bloquant en ajoutant une future vérification.
    blocking = [e for e in errors if not e.startswith("avertissement :")]
    warnings = [e for e in errors if e.startswith("avertissement :")]
    for w in warnings:
        print(f"[brief] {w}", file=sys.stderr)
    return blocking


def load_redaction_prompt():
    if not REDACTION_PROMPT_PATH.exists():
        raise GenerationError(f"prompt de rédaction introuvable : {REDACTION_PROMPT_PATH}")
    return REDACTION_PROMPT_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Texte complet des sources — retour utilisateur du 14 septembre 2026 :
# jusqu'ici, le modèle de rédaction ne recevait que le résumé (2-3 phrases)
# écrit par la routine de recherche, jamais l'article lui-même. Sur un
# sujet où les faits vérifiés sont peu nombreux, ça laisse peu de matière
# première à développer sans délayer — piste concrète pour les échecs de
# longueur observés (ex. brief Taïwan du jour, manque de 15 mots à peine
# sur un essai réel).
#
# Récupéré à la VOLÉE ici, à chaque appel de rédaction — jamais stocké
# dans editorial-briefs/{date}.json lui-même : le brief committé reste
# les résumés/faits déjà vérifiés par la recherche (contenu original,
# léger, pérenne). Le texte complet des articles tiers, lui, ne doit
# jamais vivre durablement dans un dépôt public (poids qui grossit à
# chaque édition, question de republication de contenu sous droits) —
# seulement une consommation éphémère comme matière première du modèle,
# jetée après l'appel, jamais commitée nulle part.
# ---------------------------------------------------------------------------
SOURCE_FETCH_USER_AGENT = "Scenario/1.0 (lesscenarios.fr; recherche éditoriale)"
SOURCE_FETCH_MAX_CHARS = 4000  # ~600-700 mots par source, budget volontairement plafonné (coût + bruit du prompt)


def fetch_source_full_text(url, timeout=12):
    """Récupère et extrait le texte principal d'un article source — best
    effort, ne lève jamais d'exception : retourne None sur tout échec
    (paywall, 404, timeout, blocage anti-bot, structure HTML sans
    <article>/<p> exploitable...), auquel cas l'appelant retombe sur le
    `summary` déjà présent dans le brief. Jamais bloquant pour la
    génération de l'édition — un article illisible ne doit jamais faire
    échouer toute la rédaction."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": SOURCE_FETCH_USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read()
    except Exception:
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
            tag.decompose()
        # <article> d'abord (structure sémantique la plus fiable) ; à
        # défaut, le conteneur avec le plus de texte cumulé dans ses <p>
        # directs — heuristique simple mais robuste sur la plupart des
        # sites d'actualité, jamais une vraie extraction "readability"
        # (pas de dépendance dédiée dans ce dépôt).
        container = soup.find("article")
        if container is None:
            candidates = soup.find_all(["div", "main", "section"])
            best, best_len = None, 0
            for c in candidates:
                text_len = sum(len(p.get_text(strip=True)) for p in c.find_all("p", recursive=False))
                if text_len > best_len:
                    best, best_len = c, text_len
            container = best or soup
        paragraphs = [
            p.get_text(" ", strip=True)
            for p in container.find_all("p")
            if len(p.get_text(strip=True)) > 40  # écarte légendes/mentions courtes, pas du vrai contenu
        ]
        text = "\n\n".join(paragraphs).strip()
        if len(text) < 200:  # trop court pour être une vraie extraction utile
            return None
        return text[:SOURCE_FETCH_MAX_CHARS]
    except Exception:
        return None


def enrich_sources_with_full_text(brief):
    """Mute brief["sources"] EN MÉMOIRE (jamais le fichier sur disque) —
    ajoute "texte_complet" à chaque source dont l'article a pu être
    récupéré, en plus de "summary" (jamais à la place : le modèle garde
    le résumé comme repère même quand le texte complet est aussi
    disponible). Log un résumé (N/M sources récupérées) pour rester
    observable depuis les logs GitHub Actions."""
    sources = brief.get("sources") or []
    fetched = 0
    for source in sources:
        url = source.get("url")
        if not url:
            continue
        text = fetch_source_full_text(url)
        if text:
            source["texte_complet"] = text
            fetched += 1
    if sources:
        print(f"[edition] sources : texte complet récupéré pour {fetched}/{len(sources)} — "
              "repli sur le résumé pour les autres", file=sys.stderr)


# ---------------------------------------------------------------------------
# Appel OpenRouter
# ---------------------------------------------------------------------------
def build_user_prompt(redaction_prompt, brief):
    return (
        redaction_prompt
        + "\n\n---\n\nBrief éditorial à rédiger (JSON) :\n\n"
        + json.dumps(brief, ensure_ascii=False, indent=2)
    )


def build_retry_reinforcement(errors):
    """Message de relance pour le 2e essai — placé en TÊTE du prompt (pas
    en fin, voir call_openrouter() pour l'incident qui a motivé ce choix),
    avec une instruction concrète plutôt qu'une simple liste d'erreurs à
    "corriger" (qui n'avait pas suffi : la 2e réponse était plus courte
    que la 1ère)."""
    length_errors = [e for e in errors if e.startswith("longueur estimée insuffisante")]
    apres_dek_index_errors = [e for e in errors if "apres_dek_index" in e]
    other_errors = [e for e in errors if e not in length_errors and e not in apres_dek_index_errors]

    parts = [
        "# CORRECTION OBLIGATOIRE AVANT TOUTE AUTRE CONSIGNE\n\n"
        "Une première réponse a déjà été rejetée par la validation automatique. "
        "Ignore toute tentation de raccourcir ou de simplifier — c'est l'inverse "
        "du problème constaté. Renvoie une réponse entièrement nouvelle qui "
        "corrige ce qui suit avant de reprendre le reste du prompt ci-dessous.\n\n"
    ]

    if length_errors:
        parts.append(
            f"**PROBLÈME PRINCIPAL, non négociable : {length_errors[0]}**\n\n"
            "Ce n'est pas un ajustement à la marge — la réponse précédente était "
            "nettement trop courte, et une réponse encore plus courte serait un "
            "nouvel échec. Vise 1300 à 1500 mots au total pour dek + why + lexique, "
            "PAS 1100 pile — une cible pile sur le minimum retombe presque toujours "
            "en dessous une fois comptée. Pour corriger, développe réellement le "
            "contenu, jamais en délayant les phrases existantes avec des mots creux :\n"
            "- `dek` : exactement 6 paragraphes complets, **chacun au moins 90 mots, "
            "idéalement 100 à 130**, couvrant chacun un aspect distinct du sujet "
            "(acteurs, chiffres, causes de fond, calendrier, enjeu, contexte "
            "international).\n"
            "- Chaque carte (`favorable`/`stable`/`degrade`) : 2 paragraphes "
            "`why` substantiels, **chacun au moins 90 mots, idéalement 100 à 130**.\n"
            "- Arithmétique de vérification avant de répondre : 6 × ~110 (dek) + "
            "6 × ~110 (why) + lexique (~100) ≈ 1420 mots — si ton brouillon "
            "interne est nettement en dessous, ajoute du contenu avant de renvoyer, "
            "ne renvoie jamais un brouillon dont tu sais qu'il est trop court.\n"
            "- Utilise systématiquement TOUS les faits chiffrés du brief, pas "
            "seulement les plus évidents — chaque fait du brief encore inutilisé "
            "est une occasion d'ajouter du contenu réel, jamais du remplissage "
            "stylistique.\n\n"
        )

    if apres_dek_index_errors:
        # Incident réel du 14 septembre 2026 (run 34851759911) : listé
        # uniquement dans "Autres erreurs" comme les autres erreurs de
        # schéma, cette erreur a quand même échoué 2 essais sur 2 — même
        # défaut que l'incident de longueur (une simple ligne dans une
        # liste ne suffit pas toujours) : traitement dédié, avec
        # l'exemple exact attendu plutôt qu'une description abstraite.
        parts.append(
            f"**ERREUR RÉCURRENTE, à corriger explicitement : {apres_dek_index_errors[0]}**\n\n"
            "Chaque élément de `comprendre_box` doit inclure le champ "
            "`\"apres_dek_index\": N` (entier), où N est l'index (0-based) du "
            "paragraphe de TON PROPRE tableau `dek` juste après lequel cet "
            "encart doit apparaître. Sans ce champ, l'encart n'apparaît nulle "
            "part dans la page finale, même s'il est par ailleurs bien rédigé. "
            "Exemple concret, pour un `dek` de 6 paragraphes où l'encart doit "
            "suivre le 2e paragraphe (index 1) :\n"
            '```json\n'
            '"comprendre_box": [{"lead": "...", "text": "...", "apres_dek_index": 1}]\n'
            '```\n'
            "Avant de renvoyer ta réponse, vérifie explicitement que chaque "
            "`comprendre_box` a bien ce champ, avec une valeur entière entre "
            "0 et `len(dek) - 1`.\n\n"
        )

    if other_errors:
        parts.append(
            "**Autres erreurs à corriger :**\n"
            + "\n".join(f"- {e}" for e in other_errors)
            + "\n\n"
        )

    parts.append("---\n\n")
    return "".join(parts)


def call_openrouter(prompt, model, api_key, temperature=0.45, max_tokens=12000, timeout=180, tools=None):
    """Incident réel du 14 septembre 2026 (premier vrai appel de test) :
    Claude Sonnet a tourné plus de 16 minutes sans jamais répondre, forçant
    une annulation manuelle du run — deux causes trouvées après coup :
    1. Le raisonnement étendu du modèle n'était pas désactivé (contrairement
       à translate_daily.py pour Deepseek, `"reasoning": {"enabled": False}`)
       — corrigé ci-dessous, même garde-fou.
    2. `urlopen(..., timeout=N)` ne borne QUE chaque lecture socket
       individuelle, jamais la durée totale de la requête — si le serveur
       renvoie des octets en filet continu, aucune lecture ne dépasse N
       secondes et l'appel peut ne jamais expirer.

    **Deuxième bug trouvé en testant CE correctif en conditions réelles** :
    une première version utilisait `concurrent.futures.ThreadPoolExecutor`
    en context manager — mais `ThreadPoolExecutor.__exit__` appelle
    `shutdown(wait=True)` même quand `future.result(timeout=...)` a déjà
    levé un TimeoutError, donc la sortie du bloc `with` attendait quand
    même la fin du thread bloqué : le timeout ne servait à rien. Corrigé
    avec un `threading.Thread(daemon=True)` classique et
    `Thread.join(timeout=...)`, qui borne réellement l'attente du thread
    appelant sans jamais attendre le thread daemon lui-même — celui-ci est
    tué net à la sortie du process, jamais rejoint."""
    body_dict = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        # "usage": {"include": True} : sans ce flag, OpenRouter ne renvoie
        # que prompt_tokens/completion_tokens dans `usage`, jamais `cost`
        # (voir docs OpenRouter — le coût est un ajout optionnel à la
        # réponse, pas renvoyé par défaut). Demandé explicitement ici pour
        # pouvoir logger un coût réel plutôt qu'un "?" permanent.
        "usage": {"include": True},
        "messages": [{"role": "user", "content": prompt}],
    }
    # `tools` (ajouté le 15 septembre 2026 pour generate_fallback_brief.py) :
    # ex. [{"type": "openrouter:web_search"}] — server tool OpenRouter, le
    # modèle décide lui-même quand et combien de fois chercher, exécuté
    # entièrement côté OpenRouter (jamais de cycle tool_calls/tool_results à
    # gérer ici, contrairement au function calling classique). `None` par
    # défaut : aucun changement de comportement pour generate_daily_edition.py,
    # qui n'en a jamais besoin (le brief lui fournit déjà tous les faits).
    if tools:
        body_dict["tools"] = tools
    # Incident réel du 14 septembre 2026 (test manuel, openai/gpt-5) :
    # "reasoning": {"enabled": False} envoyé sans condition faisait
    # échouer tout modèle qui impose son raisonnement interne (erreur
    # API explicite : "Reasoning is mandatory for this endpoint and
    # cannot be disabled"). Ce désactivateur avait été ajouté pour un
    # AUTRE incident réel, propre à Claude (Sonnet qui tournait plus de
    # 16 minutes sans répondre, raisonnement étendu jamais coupé) — donc
    # limité aux modèles Claude, où le problème d'origine a été observé,
    # plutôt qu'appliqué en aveugle à tout modèle passé via --model. Le
    # timeout global de cette fonction (parametre `timeout`, déjà en
    # place) reste le filet de sécurité générique pour tout modèle qui
    # traînerait en longueur, raisonnement ou non.
    # Élargi à deepseek/ le 18 septembre 2026 (bascule de
    # generate_suivi_update.py/generate_hot_topics.py sur DeepSeek) —
    # même garde-fou que generate_weekly_recap.py::call_openrouter_json(),
    # qui accepte déjà ce flag sans erreur sur ce modèle. openai/ reste
    # exclu : impose son raisonnement et refuse qu'on le désactive
    # ("Reasoning is mandatory for this endpoint and cannot be disabled").
    if "anthropic/" in model or "deepseek/" in model:
        body_dict["reasoning"] = {"enabled": False}
    body = json.dumps(body_dict).encode()
    req = urllib.request.Request(OPENROUTER_URL, method="POST", data=body, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })

    last_err = None
    for attempt in range(2):  # 1 essai + 1 retry réseau court, jamais plus (voir MAX_RETRIES pour le retry de validation, distinct)
        result_box = {}

        def worker():
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    result_box["data"] = json.loads(resp.read())
            except Exception as e:  # noqa: BLE001 — capturé puis re-levé dans le thread appelant
                result_box["error"] = e

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            # Thread toujours bloqué après `timeout` secondes — abandonné
            # sans être rejoint (daemon=True). Jamais réessayé
            # automatiquement (voir consigne « pas de retries agressifs ») :
            # un dépassement du délai global est un échec net, pas une
            # panne transitoire à retenter.
            raise GenerationError(
                f"appel OpenRouter sans réponse après {timeout}s (délai global dépassé) — "
                "arrêt forcé, vérifier le tableau de bord OpenRouter pour le coût réel "
                "déjà engagé sur cette tentative avant de relancer"
            )

        if "error" in result_box:
            e = result_box["error"]
            if isinstance(e, urllib.error.HTTPError):
                # Incident réel du 14 septembre 2026 (test manuel avec
                # openai/gpt-5) : un 400 Bad Request s'affichait comme
                # "HTTP Error 400: Bad Request", sans jamais lire le corps
                # de la réponse — qui contient pourtant le vrai message
                # d'erreur d'OpenRouter/du fournisseur (ex. un paramètre
                # non supporté par ce modèle précis). Lu et inclus ici,
                # une seule fois (le flux ne se relit pas deux fois).
                try:
                    detail = e.read().decode("utf-8", errors="replace")[:1000]
                except Exception:
                    detail = "(corps de la réponse illisible)"
                # Un 4xx est une erreur du CONTENU de la requête (modèle,
                # paramètre, format...) : la retenter à l'identique échoue
                # de la même façon à coup sûr, donc jamais de retry réseau
                # dessus — contrairement à une vraie panne réseau/5xx,
                # transitoire par nature, qui garde son retry court.
                if 400 <= e.code < 500:
                    raise GenerationError(
                        f"appel OpenRouter refusé (HTTP {e.code}, requête invalide, jamais retenté "
                        f"à l'identique) : {detail}"
                    )
                last_err = e
                if attempt == 0:
                    print(f"[openrouter] erreur serveur HTTP {e.code}, nouvel essai dans 3s : {detail}", file=sys.stderr)
                    time.sleep(3)
                    continue
                raise GenerationError(f"appel OpenRouter impossible après 2 essais (HTTP {last_err.code}) : {detail}")
            if isinstance(e, urllib.error.URLError):
                last_err = e
                if attempt == 0:
                    print(f"[openrouter] erreur réseau, nouvel essai dans 3s : {e}", file=sys.stderr)
                    time.sleep(3)
                    continue
                raise GenerationError(f"appel OpenRouter impossible après 2 essais : {last_err}")
            raise GenerationError(f"appel OpenRouter — erreur inattendue : {e}")

        data = result_box["data"]
        break

    # Capturé et loggé tout de suite, avant la validation du JSON de contenu
    # ci-dessous : l'appel a consommé des tokens/de l'argent côté OpenRouter
    # même si le contenu renvoyé s'avère invalide, donc cette info ne doit
    # jamais dépendre de la réussite du parsing qui suit. `usage.model` est
    # le modèle RÉELLEMENT utilisé (peut différer de `model` demandé en cas
    # de fallback/routage côté OpenRouter) — demandé explicitement pour le
    # log, distinct du modèle demandé dans l'argument `model`.
    usage = dict(data.get("usage") or {})
    usage["model"] = data.get("model", model)
    print(
        f"[openrouter] appel — modèle {usage['model']} · "
        f"tokens entrée {usage.get('prompt_tokens', '?')} · "
        f"tokens sortie {usage.get('completion_tokens', '?')} · "
        f"coût ≈ {usage.get('cost', '?')} $",
        file=sys.stderr,
    )

    if "choices" not in data:
        raise GenerationError(f"réponse OpenRouter sans 'choices' : {data}")
    content_str = data["choices"][0]["message"]["content"]
    stripped = strip_markdown_json_fence(content_str)
    try:
        content = json.loads(stripped)
    except json.JSONDecodeError:
        repaired = repair_unescaped_lexref_quotes(stripped)
        try:
            content = json.loads(repaired)
            print(
                "[openrouter] JSON réparé automatiquement (guillemets non échappés "
                "détectés dans un balisage .lex-ref) — voir repair_unescaped_lexref_quotes()",
                file=sys.stderr,
            )
        except json.JSONDecodeError as e:
            raise InvalidModelJSON(f"{e}\n{content_str[:2000]}")
    return content, usage


_LEXREF_UNESCAPED_RE = re.compile(
    r'<a class="lex-ref" href="#lex-([a-z0-9-]+)" aria-label="Voir la définition dans le lexique">\*</a>'
)


def repair_unescaped_lexref_quotes(text):
    """Répare l'échec le plus fréquent observé en conditions réelles côté
    modèle : recopier le balisage `.lex-ref` du prompt
    (docs/routine-redaction-prompt.md) avec ses guillemets HTML non
    échappés, alors qu'il est déjà à l'intérieur d'une chaîne JSON — ce
    qui casse le parsing (`Expecting ',' delimiter`) au premier `"` de
    `class="lex-ref"`. Motif volontairement strict (calqué sur le
    balisage exact demandé dans le prompt, `aria-label` inclus) : mieux
    vaut ne pas réparer un motif imprévu que réparer trop largement et
    introduire un JSON valide mais sémantiquement corrompu. Best-effort,
    jamais une garantie générale — un guillemet non échappé ailleurs
    dans la réponse fera quand même échouer le parsing et lèvera
    InvalidModelJSON, qui rentre alors dans le retry normal de main()."""
    return _LEXREF_UNESCAPED_RE.sub(
        lambda m: (
            '<a class=\\"lex-ref\\" href=\\"#lex-' + m.group(1)
            + '\\" aria-label=\\"Voir la définition dans le lexique\\">*</a>'
        ),
        text,
    )


_LEXREF_ANY_RE = re.compile(
    r'<a class="lex-ref" href="#lex-([a-z0-9-]+)" aria-label="Voir la définition dans le lexique">'
    r'((?:(?!</a>).)*)</a>'
)


def normalize_lex_ref_link_text(text):
    """Le prompt (docs/routine-redaction-prompt.md § « Terme technique →
    lexique ») demande un simple astérisque comme texte du lien .lex-ref,
    juste après le terme écrit en clair — mais le modèle enveloppe parfois
    le terme entier dans le lien au lieu de l'astérisque seul (observé en
    conditions réelles sur plusieurs éditions : "fusion nucléaire",
    "deutérium-tritium", "plasma", "tokamak" le 15 septembre 2026, "COFER",
    "CIPS", "Fed" le 17, "trêve tarifaire" le 21 — retour utilisateur du
    21 septembre, "les liens vers le glossaire ont un format bizarre").
    Non fiable à corriger par un retry payant (le modèle ne suit cette
    règle qu'environ 1 essai sur 2 dans les runs déjà observés) : réparé
    ici mécaniquement à la place — le terme ressort du lien en texte
    normal (sens et lisibilité inchangés), seul l'astérisque reste dans
    le lien, format identique à celui déjà correct la plupart du temps."""
    def repl(m):
        slug, inner = m.group(1), m.group(2)
        if inner == "*":
            return m.group(0)
        return (
            inner + '<a class="lex-ref" href="#lex-' + slug
            + '" aria-label="Voir la définition dans le lexique">*</a>'
        )
    return _LEXREF_ANY_RE.sub(repl, text)


def normalize_content_lex_ref(content):
    """Applique normalize_lex_ref_link_text() aux mêmes champs que ceux
    inspectés par validate_content_schema() pour la cohérence lex-ref <->
    lexique (dek, why des 3 cartes, comprendre_box[].text) — la seule
    liste de champs du schéma où ce balisage peut apparaître."""
    if isinstance(content.get("dek"), list):
        content["dek"] = [normalize_lex_ref_link_text(p) for p in content["dek"]]
    for k in ("favorable", "stable", "degrade"):
        card = (content.get("cards") or {}).get(k)
        if card and isinstance(card.get("why"), list):
            card["why"] = [normalize_lex_ref_link_text(p) for p in card["why"]]
    for box in content.get("comprendre_box") or []:
        if isinstance(box, dict) and isinstance(box.get("text"), str):
            box["text"] = normalize_lex_ref_link_text(box["text"])
    return content


def strip_markdown_json_fence(text):
    """Malgré `response_format: {"type": "json_object"}`, un premier vrai
    appel (14 septembre 2026) a montré Claude Sonnet envelopper sa réponse
    dans un bloc markdown ```json ... ``` — jamais garanti côté modèle,
    donc traité ici plutôt que supposé absent. Ne touche pas le texte si
    aucune barrière markdown n'est présente (cas nominal).

    Repli ajouté le 15 septembre 2026 (generate_fallback_brief.py, premier
    vrai test avec le server tool `openrouter:web_search`) : le modèle
    avait aussi renvoyé du texte de raisonnement libre AVANT le bloc
    ```json (« Je vais faire les recherches nécessaires... »), que le
    premier motif ci-dessus, ancré `^...$`, ne matchait pas — response_format
    json_object semble moins strictement garanti dès qu'un tool est utilisé.
    On cherche alors un bloc fenced n'importe où dans le texte, en prenant
    le DERNIER trouvé (le brief final, jamais un extrait de raisonnement
    intermédiaire qui ressemblerait à du JSON)."""
    stripped = text.strip()
    m = re.match(r"^```(?:json)?\s*\n(.*)\n```\s*$", stripped, re.S)
    if m:
        return m.group(1)
    matches = re.findall(r"```(?:json)?\s*\n(.*?)\n```", stripped, re.S)
    return matches[-1] if matches else stripped


def apply_apres_dek_index_fallback(content):
    """Filet de sécurité — incidents réels des 14-15 septembre 2026 (runs
    34851759911, 34858896901, 34859320491) : apres_dek_index manque à
    l'essai 1 dans 100 % des runs réels observés jusqu'ici, malgré la
    consigne explicite du prompt de base, son renforcement dédié en
    relance (build_retry_reinforcement()) et la checklist finale ajoutée
    dans docs/routine-redaction-prompt.md. Contrairement aux autres
    erreurs de validate_content_schema() (longueur, JSON invalide,
    lex-ref cassé...), qui touchent toutes à l'exactitude factuelle ou
    éditoriale du contenu et doivent donc rester strictement bloquantes,
    apres_dek_index n'est qu'un choix de PLACEMENT — n'importe quel
    index valide reste correct du point de vue du lecteur. Appelée
    uniquement en tout dernier recours par main() (voir son appel),
    quand c'est la SEULE erreur restante après le dernier essai : mute
    `content` en place avec un index par défaut raisonnable (milieu du
    tableau dek, jamais avant le 1er paragraphe, donc toujours valide),
    plutôt que de perdre un essai payant entier sur ce seul champ.
    Retourne True si au moins une correction a été appliquée."""
    dek_len = len(content.get("dek") or [])
    if dek_len == 0:
        return False
    default_index = dek_len // 2
    fixed_any = False
    for box in content.get("comprendre_box") or []:
        if not isinstance(box, dict):
            continue  # forme invalide, hors périmètre de ce filet — validate_content_schema() l'aura déjà signalé séparément
        apres = box.get("apres_dek_index")
        if not isinstance(apres, int) or isinstance(apres, bool) or not (0 <= apres < dek_len):
            box["apres_dek_index"] = default_index
            fixed_any = True
    return fixed_any


# ---------------------------------------------------------------------------
# Validation du contenu retourné par le modèle (avant construction HTML)
# ---------------------------------------------------------------------------
def validate_content_schema(content, brief):
    errors = []
    required = ["h1", "question_text", "section_title", "dek", "stakes_branches",
                "indicators", "cards", "essentiel_box", "delta_france",
                "phrase_a_retenir", "phrase_a_retenir_stat", "lexique",
                "sources_html", "meta"]
    for key in required:
        if key not in content or content[key] in (None, "", []):
            errors.append(f"champ manquant ou vide : {key}")
    if errors:
        return errors  # inutile de creuser plus loin si la forme de base manque

    if len(content["dek"]) < 3:
        errors.append(f"dek : {len(content['dek'])} paragraphes (minimum 3 attendu)")

    for kind in ("favorable", "stable", "degrade"):
        if kind not in content["stakes_branches"]:
            errors.append(f"stakes_branches.{kind} manquant")
        if kind not in content["cards"]:
            errors.append(f"cards.{kind} manquant")

    # Incident réel du 14 septembre 2026 (test mistralai/mistral-large-2512) :
    # AttributeError non gérée ("'int' object has no attribute 'get'"),
    # script interrompu net (crash, pas une erreur de validation normale) —
    # un modèle non calibré sur ce schéma peut renvoyer une forme
    # inattendue (ex. un élément de liste qui n'est pas un objet JSON).
    # Chaque boucle ci-dessous vérifie maintenant isinstance(..., dict)
    # avant d'appeler .get()/[...] dessus, pour transformer ce genre de
    # cas en erreur de validation classique (retryable) plutôt qu'un
    # crash qui perd tout l'essai sans message exploitable.
    if not errors and all(isinstance(content["cards"].get(k), dict) for k in ("favorable", "stable", "degrade")):
        pcts = [content["cards"][k]["pct"] for k in ("favorable", "stable", "degrade") if "pct" in content["cards"][k]]
        if len(pcts) == 3 and abs(sum(pcts) - 100) > 1:
            errors.append(f"somme des pct des 3 cartes = {sum(pcts)} (attendu 100)")
        # Retour utilisateur du 15 septembre 2026 : les 3 cartes ne
        # reprenaient chacune QU'UN SEUL des 2 KPI de .indicator-strip
        # (jamais détecté avant, faute de vérifier autre chose que "non
        # vide" sur indicateurs_touches) — la règle de docs/routine-prompt.md
        # § Cohérence des KPI ("2 KPI fixes... réutilisés identiques dans
        # les 3 cartes") n'était donc jamais réellement vérifiée. Vérifie
        # le NOMBRE seulement, jamais une correspondance exacte de libellé :
        # field_name est légitimement une version abrégée de indicators[].label
        # (ex. édition du 13 septembre, déjà publiée avant automatisation :
        # "Taux d'emprunt de la France à 10 ans (OAT)" en tête devient "Taux
        # d'emprunt à 10 ans (OAT)" dans les cartes) — imposer une égalité
        # stricte casserait ce cas légitime, déjà vérifié sur du contenu réel.
        n_expected_kpi = len(content.get("indicators") or [])
        for kind in ("favorable", "stable", "degrade"):
            card = content["cards"][kind]
            for f in ("pct", "gauge_word", "h3", "why", "indicateurs_touches", "france_line", "france_impact"):
                if f not in card or card[f] in (None, "", []):
                    errors.append(f"cards.{kind}.{f} manquant ou vide")
            if card.get("france_impact") not in ("favorable", "degrade"):
                errors.append(f"cards.{kind}.france_impact doit être 'favorable' ou 'degrade' (reçu : {card.get('france_impact')!r})")
            if len(card.get("why", [])) < 2:
                errors.append(f"cards.{kind}.why : {len(card.get('why', []))} paragraphes (2 attendus)")
            touches = card.get("indicateurs_touches")
            if n_expected_kpi and isinstance(touches, list) and len(touches) != n_expected_kpi:
                errors.append(
                    f"cards.{kind}.indicateurs_touches : {len(touches)} KPI évalué(s), "
                    f"{n_expected_kpi} attendus (les mêmes que .indicator-strip, dans chacune des 3 cartes)"
                )
    elif not errors:
        for kind in ("favorable", "stable", "degrade"):
            if not isinstance(content["cards"].get(kind), dict):
                errors.append(f"cards.{kind} : attendu un objet JSON, reçu {type(content['cards'].get(kind)).__name__}")

    if len(content["indicators"]) != len(brief.get("indicateurs_kpi", [])):
        errors.append(
            f"indicators : {len(content['indicators'])} éléments, brief en avait "
            f"{len(brief.get('indicateurs_kpi', []))}"
        )

    n_comprendre_brief = len(brief.get("encarts_decides", {}).get("comprendre_box") or [])
    n_comprendre_content = len(content.get("comprendre_box") or [])
    if n_comprendre_content != n_comprendre_brief:
        errors.append(
            f"comprendre_box : {n_comprendre_content} éléments produits, "
            f"{n_comprendre_brief} décidés dans le brief"
        )

    # apres_dek_index — incident réel du 14 septembre 2026 (run 34847218352,
    # test grandeur nature) : le modèle a produit un comprendre_box complet
    # (lead + text), qui a passé cette validation puisqu'elle ne vérifiait
    # que le NOMBRE d'éléments — mais build_html.py insère chaque
    # comprendre_box juste après content["dek"][apres_dek_index]
    # (build_hero()), un champ que le prompt ne demandait jusque-là jamais
    # au modèle. Résultat : l'encart existait dans le JSON validé mais
    # n'apparaissait nulle part dans le HTML final, sans qu'aucune
    # validation ne le détecte. Rendu obligatoire côté prompt (voir
    # docs/routine-redaction-prompt.md § comprendre_box) et vérifié ici.
    dek_len = len(content.get("dek") or [])
    for idx, box in enumerate(content.get("comprendre_box") or []):
        if not isinstance(box, dict):
            errors.append(f"comprendre_box[{idx}] : attendu un objet JSON, reçu {type(box).__name__} ({box!r})")
            continue
        apres = box.get("apres_dek_index")
        if not isinstance(apres, int) or isinstance(apres, bool) or not (0 <= apres < dek_len):
            errors.append(
                f"comprendre_box[{idx}].apres_dek_index manquant ou invalide "
                f"(reçu {apres!r}, attendu un entier entre 0 et {dek_len - 1}) — "
                "sans cet index l'encart n'est inséré nulle part dans le HTML final"
            )

    essentiel_box = content["essentiel_box"]
    if not isinstance(essentiel_box, list) or len(essentiel_box) != 4:
        errors.append(
            f"essentiel_box : "
            f"{len(essentiel_box) if isinstance(essentiel_box, list) else type(essentiel_box).__name__} "
            "(4 chaînes attendues)"
        )
    else:
        # Retour utilisateur du 15 septembre 2026 : « l'essentiel assez
        # léger » — comparé aux éditions de la routine manuelle (avant le
        # 14 septembre), qui tournaient entre 126 et 142 mots au total sur
        # ces 4 paragraphes, contre ~90 mots sur les premières éditions
        # automatisées (aucune contrainte de longueur n'existait ici avant
        # ce correctif, seulement un compte de 4 paragraphes). Seuil fixé
        # légèrement sous ce plancher historique observé, même mécanique
        # de retry que MIN_WORDS ci-dessus.
        essentiel_words = sum(len(p.split()) for p in essentiel_box if isinstance(p, str))
        if essentiel_words < MIN_ESSENTIEL_WORDS:
            errors.append(
                f"essentiel_box trop léger : {essentiel_words} mots au total sur les 4 "
                f"paragraphes (minimum {MIN_ESSENTIEL_WORDS}, manque {MIN_ESSENTIEL_WORDS - essentiel_words} mots) — "
                "développer chaque point avec un chiffre ou un fait concret précis, jamais juste raccourcir/paraphraser"
            )

    df = content["delta_france"]
    for f in ("kind", "score", "word", "text"):
        if f not in df:
            errors.append(f"delta_france.{f} manquant")
    if df.get("kind") not in ("positif", "negatif"):
        errors.append(f"delta_france.kind doit être 'positif' ou 'negatif' (reçu : {df.get('kind')!r})")

    # Bug réel du 14-15 septembre 2026 (retour utilisateur) : "word" ne
    # portait que l'intensité ("assez"), sans la polarité ("négatif") —
    # jauge illisible sur la page publiée (« Assez. » sans rien après).
    # "word" doit toujours contenir les deux : un mot d'intensité ET
    # l'adjectif de kind (voir docs/routine-redaction-prompt.md).
    word = (df.get("word") or "").strip().lower()
    if word:
        # Incident réel du 17 septembre 2026 : "légèrement négatif" rejeté
        # à tort ("légèrement" contient un è, "léger" un é — ce ne sont
        # pas les mêmes caractères Unicode, donc "léger in légèrement"
        # est FAUX malgré un mot parfaitement valide). Le modèle avait
        # raison, la validation avait un vrai trou. Formes explicites
        # plutôt qu'un stemming/normalisation d'accents plus général —
        # champ fermé, seules quelques inflexions réelles possibles ici.
        has_intensity = any(w in word for w in ("léger", "légère", "légèrement", "assez", "très"))
        polarity_adj = "négatif" if df.get("kind") == "negatif" else "positif"
        if not has_intensity or polarity_adj not in word:
            errors.append(
                f"delta_france.word incomplet ({df.get('word')!r}) : doit contenir un mot "
                f"d'intensité (léger/assez/très) ET la polarité ({polarity_adj}), ex. 'assez {polarity_adj}'"
            )

    # Même incident : "text" recommençait par la phrase d'intro déjà
    # affichée par le gabarit (« Notre évaluation de l'impact pour la
    # France : ... »), produisant un doublon visible à la publication.
    text = (df.get("text") or "").strip().lower()
    if text.startswith("notre évaluation") or text.startswith("notre évaluation de l'impact"):
        errors.append(
            f"delta_france.text répète la phrase d'intro déjà affichée par le gabarit "
            f"(reçu : {df.get('text')!r}) — text doit commencer directement par la justification"
        )

    # phrase_a_retenir / phrase_a_retenir_stat — ajouté le 19 septembre
    # 2026, remplace l'ancienne extraction a posteriori dans
    # scripts/pub/generate_daily_pub.py (extract_chiffre()) : la phrase
    # citée mot pour mot par le post "pub" du jour vient maintenant
    # directement d'ici, jamais re-extraite plus tard — voir
    # docs/routine-redaction-prompt.md pour la règle éditoriale complète.
    par = (content.get("phrase_a_retenir") or "").strip()
    par_stat = (content.get("phrase_a_retenir_stat") or "").strip()
    if len(par) > PHRASE_A_RETENIR_MAX_CHARS:
        errors.append(
            f"phrase_a_retenir : {len(par)} caractères (max {PHRASE_A_RETENIR_MAX_CHARS} — "
            "le gabarit de l'image pub n'a pas de défilement, un dépassement la rend illisible)"
        )
    if par_stat and par_stat not in par:
        errors.append(
            f"phrase_a_retenir_stat ({par_stat!r}) n'apparaît pas mot pour mot dans "
            f"phrase_a_retenir ({par!r})"
        )

    for idx, term in enumerate(content.get("lexique", [])):
        if not isinstance(term, dict):
            errors.append(f"lexique[{idx}] : attendu un objet JSON, reçu {type(term).__name__} ({term!r})")
            continue
        for f in ("slug", "terme", "definition"):
            if f not in term or not term[f]:
                errors.append(f"lexique : entrée incomplète (manque {f}) : {term}")

    # Cohérence lex-ref <-> lexique — vérifiée ici, sur le contenu, en plus
    # de validate_assembled_html() sur le HTML final (incident du 14
    # septembre 2026, run 34841291433 : terme "swap" défini au lexique mais
    # jamais référencé dans le texte, échec seulement détecté après la
    # boucle de retry, donc jamais corrigé automatiquement). Ici, un écart
    # rentre dans le même retry automatique que les autres erreurs de
    # schéma, avec le détail exact renvoyé au modèle au 2e essai.
    if not errors:
        lex_slugs = {t["slug"] for t in content.get("lexique", []) if t.get("slug")}
        referenced_text = " ".join(
            list(content.get("dek") or [])
            + [w for k in ("favorable", "stable", "degrade")
               for w in (content.get("cards", {}).get(k, {}).get("why") or [])]
            + [b.get("text", "") for b in (content.get("comprendre_box") or [])]
        )
        referenced_slugs = set(re.findall(r'href="#lex-([a-z0-9-]+)"', referenced_text))
        unused = lex_slugs - referenced_slugs
        broken = referenced_slugs - lex_slugs
        if unused:
            errors.append(
                f"lexique : termes définis mais jamais référencés via .lex-ref dans le texte : "
                f"{sorted(unused)} — soit les utiliser dans dek/why via <a class=\"lex-ref\" "
                f"href=\"#lex-{{slug}}\">, soit les retirer du lexique"
            )
        if broken:
            errors.append(
                f"lexique : .lex-ref pointant vers un terme absent du lexique : {sorted(broken)}"
            )

    # Placeholders résiduels — même garde-fou que la validation de forme
    # décrite dans l'audit (point E.1).
    flat_text = json.dumps(content, ensure_ascii=False)
    for pattern in (r"\bTODO\b", r"\{\{", r"\bXXX\b", r"lorem ipsum"):
        if re.search(pattern, flat_text, re.I):
            errors.append(f"placeholder résiduel détecté (motif {pattern!r}) dans la réponse du modèle")

    # Longueur — vérifiée ici, sur le contenu, en plus de
    # validate_assembled_html() sur le HTML final (incident du 14 septembre
    # 2026, run 34835807298 : 583 mots, aucun retry déclenché car ce
    # contrôle ne vivait jusque-là que dans validate_assembled_html(),
    # après la boucle de retry). Ici, un échec de longueur rentre dans le
    # même retry automatique (1 essai max) que les autres erreurs de
    # schéma, avec le nombre de mots manquants explicite dans le message
    # renvoyé au modèle au deuxième essai.
    word_count = estimate_word_count(content)
    if word_count < MIN_WORDS:
        errors.append(
            f"longueur estimée insuffisante : {word_count} mots dans dek + why + "
            f"lexique (minimum {MIN_WORDS}, manque {MIN_WORDS - word_count} mots) — "
            "développer le contexte et les why plutôt que délayer les phrases existantes"
        )

    return errors


def estimate_word_count(content):
    """Estimation du même comptage que validate_assembled_html()/le script
    déjà en place côté client (.dek, .why, dd) — mais calculée directement
    sur le JSON du modèle, avant construction du HTML, pour pouvoir
    déclencher un retry automatique en cas de contenu trop court.

    Incident réel du 14 septembre 2026 (2e occurrence, test
    mistralai/mistral-large-2512) : même crash AttributeError que dans
    validate_content_schema(), mais ICI — cette fonction est appelée
    AVANT la boucle lexique de validate_content_schema() qui vérifie
    déjà isinstance(term, dict), donc son propre garde-fou ne protège
    jamais cet appel plus précoce. Gardes ajoutées ici aussi, jamais
    supposer qu'un élément de liste fourni par le modèle est du bon
    type avant de l'avoir vérifié — même sur un chemin de code qui
    semblait déjà couvert ailleurs."""
    texts = [d for d in (content.get("dek") or []) if isinstance(d, str)]
    for kind in ("favorable", "stable", "degrade"):
        card = (content.get("cards") or {}).get(kind)
        if isinstance(card, dict):
            texts.extend(w for w in (card.get("why") or []) if isinstance(w, str))
    for term in content.get("lexique") or []:
        if isinstance(term, dict):
            texts.append(term.get("definition") or "")
    plain = re.sub(r"<[^>]+>", " ", " ".join(texts))
    return len(plain.split())


def validate_assembled_html(html_text, content):
    """Validation finale, sur le HTML réellement produit — indépendante du
    modèle, même si validate_content_schema() est déjà passée (voir
    section E de l'audit : deux niveaux de validation, jamais un seul)."""
    errors = []
    soup = BeautifulSoup(html_text, "html.parser")

    # Structure obligatoire du gabarit
    required_selectors = [
        (".question-box", 1), (".indicator-strip", 1), (".cards", 1),
        (".card", 3), (".lexique", 1), ("footer", 1), (".stakes-box", 1),
        (".essentiel-box", 1), (".sources-list", 1), (".retenir-box", 1),
    ]
    for sel, expected_count in required_selectors:
        found = len(soup.select(sel))
        if found != expected_count:
            errors.append(f"structure : {sel} trouvé {found} fois (attendu {expected_count})")

    # Filet de sécurité — incident du 14 septembre 2026 (run 34847218352,
    # test grandeur nature) : un comprendre_box complet, validé par
    # validate_content_schema() (bon nombre d'éléments), a été perdu
    # silencieusement dans le HTML final faute d'apres_dek_index exploitable
    # (voir ce contrôle plus haut). apres_dek_index est maintenant validé en
    # amont, mais ce comptage reste un filet indépendant — n'importe quel
    # futur bug de placement dans build_html.py (nouveau champ, nouvel
    # incident) fera échouer ici plutôt que de publier un encart manquant en
    # silence, même si validate_content_schema() est déjà passée.
    n_comprendre_content = len(content.get("comprendre_box") or [])
    n_comprendre_html = len(soup.select(".comprendre-box"))
    if n_comprendre_html != n_comprendre_content:
        errors.append(
            f"comprendre_box : {n_comprendre_content} élément(s) dans la réponse du modèle, "
            f"{n_comprendre_html} réellement présent(s) dans le HTML assemblé — "
            "au moins un encart a été perdu lors de la construction du HTML"
        )
    if content.get("list_box") and not soup.select(".list-box"):
        errors.append("list_box présent dans la réponse du modèle mais absent du HTML assemblé")

    # Seuil de mots — même sélecteur, même méthode que le script déjà en
    # place côté client (voir index.html, script de fin de page).
    content_els = soup.select(".dek, .why, dd")
    text = " ".join(el.get_text() for el in content_els)
    word_count = len(text.split())
    if word_count < MIN_WORDS:
        errors.append(f"longueur : {word_count} mots dans .dek/.why/dd (minimum {MIN_WORDS})")

    # Cohérence lex-ref <-> lexique : tout href="#lex-..." doit avoir un id
    # correspondant, et réciproquement chaque terme du lexique doit être
    # référencé au moins une fois dans le texte (règle explicite du prompt
    # de rédaction).
    lex_ids = {dt.get("id") for dt in soup.select(".lexique dt[id]")}
    referenced = set()
    for a in soup.select("a.lex-ref[href]"):
        href = a["href"].lstrip("#")
        referenced.add(href)
        if href not in lex_ids:
            errors.append(f"lex-ref cassé : href=#{href} sans entrée de lexique correspondante")
    unreferenced = lex_ids - referenced
    if unreferenced:
        errors.append(f"lexique : termes jamais référencés dans le texte : {sorted(unreferenced)}")

    # Cohérence numérique — avertissement seulement (voir décision G.4) :
    # chaque valeur d'indicateur doit réapparaître au moins une fois dans
    # le texte du contexte/des cartes.
    dek_why_text = " ".join(el.get_text() for el in soup.select(".dek, .why"))
    for ind in soup.select(".indicator-strip .indicator"):
        value = ind.select_one(".value")
        if not value:
            continue
        # Premier "nombre" du champ value (avant le premier espace après un
        # chiffre), heuristique simple, volontairement peu stricte.
        m = re.search(r"[\d,.]+", value.get_text())
        if m and m.group(0) not in dek_why_text:
            print(
                f"[avertissement] indicateur {m.group(0)!r} non retrouvé tel quel dans le texte "
                "(cohérence numérique — non bloquant, voir docs/routine-redaction-prompt.md)",
                file=sys.stderr,
            )

    # Placeholders résiduels dans le HTML final
    for pattern in (r"\bTODO\b", r"\{\{", r"\bXXX\b"):
        if re.search(pattern, html_text, re.I):
            errors.append(f"placeholder résiduel détecté dans le HTML final (motif {pattern!r})")

    return errors


# ---------------------------------------------------------------------------
# Mode --dry-run : réponse de modèle déjà enregistrée, aucun appel réseau
# ---------------------------------------------------------------------------
def load_dry_run_fixture(brief_date):
    fixture_path = REPO_ROOT / "scripts" / "edition" / "fixtures" / f"{brief_date}-dry-run.json"
    if not fixture_path.exists():
        raise GenerationError(
            f"--dry-run demandé mais aucune fixture trouvée : {fixture_path}\n"
            "Une fixture par date de brief de test doit être créée à la main "
            "(voir scripts/edition/fixtures/2026-09-20-dry-run.json)."
        )
    with open(fixture_path, encoding="utf-8") as f:
        return json.load(f), {"cost": 0.0, "prompt_tokens": 0, "completion_tokens": 0, "note": "dry-run, aucun appel réel"}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, help="chemin du fichier brief JSON")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--dry-run", action="store_true", help="utilise une fixture locale, aucun appel OpenRouter")
    parser.add_argument("--out", default=None, help="chemin de sortie (défaut : _prototype-out/{date}.html, jamais index.html)")
    args = parser.parse_args()

    brief = load_brief(args.brief)
    date_str = brief["date"]
    print(f"[edition] brief chargé : {args.brief} (date {date_str}, registre {brief['registre']})")

    # Jamais en --dry-run : effet de bord réseau réel (comme la photo
    # Pexels ailleurs dans le pipeline), et --dry-run utilise une fixture
    # figée dont le contenu ne dépend pas de ce brief de toute façon.
    if not args.dry_run:
        enrich_sources_with_full_text(brief)

    index_html_path = REPO_ROOT / "index.html"
    shell = build_html.extract_shell(index_html_path.read_text(encoding="utf-8"))
    print(f"[edition] gabarit extrait depuis index.html (édition courante N°{shell['edition_number']})")

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not args.dry_run and not api_key:
        raise GenerationError("OPENROUTER_API_KEY manquant dans l'environnement (ou utiliser --dry-run)")

    redaction_prompt = load_redaction_prompt()
    usage_total = {"cost": 0.0, "prompt_tokens": 0, "completion_tokens": 0}
    content = None
    errors = []
    attempts_history = []  # [(content, errors), ...] — voir repli "meilleur essai" plus bas
    used_best_effort_fallback = False

    for attempt in range(1 + MAX_RETRIES):
        if args.dry_run:
            content, usage = load_dry_run_fixture(date_str)
        else:
            prompt = build_user_prompt(redaction_prompt, brief)
            if attempt > 0:
                # Incident du 14 septembre 2026 (run 34838683152) : un simple
                # ajout de la liste d'erreurs en FIN de prompt (déjà long) n'a
                # pas suffi — le 2e essai était même plus court que le 1er
                # (863 mots contre 936, seuil 1100). Renforcement mis en tête
                # du prompt, isolé, avec une instruction concrète plutôt
                # qu'une simple liste d'erreurs à "corriger".
                prompt = build_retry_reinforcement(errors) + prompt
            try:
                content, usage = call_openrouter(prompt, args.model, api_key)
            except InvalidModelJSON as e:
                # Incident du 14 septembre 2026 (run 34841534063) : cette
                # erreur remontait jusqu'ici sans jamais passer par
                # validate_content_schema() ni par la logique de retry
                # ci-dessous — un JSON invalide faisait donc échouer tout
                # le script au 1er essai, sans jamais utiliser le retry
                # prévu. Traitée maintenant comme une erreur de validation
                # ordinaire : elle entre dans la même boucle.
                print(f"[edition] réponse du modèle invalide (essai {attempt + 1}) : {e}", file=sys.stderr)
                content = None
                errors = [
                    "la réponse précédente n'était pas un JSON syntaxiquement valide "
                    f"({e.args[0].splitlines()[0] if e.args else e}) — renvoie UNIQUEMENT l'objet JSON "
                    "demandé (rien avant, rien après), et échappe (\\\") tout guillemet double à "
                    "l'intérieur d'un attribut HTML (ex. class=\\\"lex-ref\\\", href=\\\"...\\\") "
                    "puisque tu es déjà à l'intérieur d'une chaîne JSON"
                ]
                if attempt == MAX_RETRIES:
                    raise GenerationError(
                        f"réponse du modèle jamais un JSON valide après {1 + MAX_RETRIES} essai(s), "
                        "rien n'est produit"
                    ) from e
                continue

        for k in ("cost", "prompt_tokens", "completion_tokens"):
            usage_total[k] = usage_total.get(k, 0) + (usage.get(k) or 0)
        if usage.get("model"):
            usage_total["model"] = usage["model"]

        content = normalize_content_lex_ref(content)
        errors = validate_content_schema(content, brief)
        attempts_history.append((content, errors))
        if not errors:
            break
        print(f"[edition] validation du contenu échouée (essai {attempt + 1}) :", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        if args.dry_run:
            break  # inutile de "réessayer" contre la même fixture figée

    if errors:
        # Filet de sécurité : si apres_dek_index est la SEULE erreur
        # restante après le dernier essai (aucune autre erreur de fond),
        # corriger directement plutôt que de tout rejeter — voir
        # apply_apres_dek_index_fallback(). Un contenu par ailleurs
        # invalide (longueur, JSON, lex-ref...) continue de faire
        # échouer le script normalement.
        non_apres_dek_errors = [e for e in errors if "apres_dek_index" not in e]
        if not non_apres_dek_errors and content is not None and apply_apres_dek_index_fallback(content):
            print(
                "[edition] apres_dek_index manquant/invalide après le dernier essai — "
                "filet de sécurité appliqué (index par défaut), voir apply_apres_dek_index_fallback()",
                file=sys.stderr,
            )
            errors = []
        elif attempts_history and not args.dry_run:
            # Repli ajouté le 20 septembre 2026, retour utilisateur explicite
            # (« on prend le max des 3 tentatives, tant pis ») : jusqu'ici,
            # 3 essais qui échouent tous la validation (même de peu — ex.
            # 74 mots sous le seuil, ou un phrase_a_retenir_stat pas tout à
            # fait mot pour mot) ne produisaient RIEN, alors que le meilleur
            # des 3 essais est souvent déjà quasi utilisable. Reprend l'essai
            # le plus proche de passer (le moins d'erreurs restantes) plutôt
            # que d'abandonner sec — jamais silencieux : les erreurs
            # ignorées restent loguées ci-dessous. Jamais en --dry-run
            # (inutile contre une fixture figée — voir check_fixtures.py,
            # qui doit rester strict sur celle-ci).
            content, errors = min(attempts_history, key=lambda pair: len(pair[1]))
            used_best_effort_fallback = True
            print(
                f"[edition] AUCUN essai n'a validé proprement après {1 + MAX_RETRIES} tentative(s) "
                f"— repli sur le meilleur essai ({len(errors)} erreur(s) résiduelle(s) acceptée(s)) :",
                file=sys.stderr,
            )
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            errors = []
        else:
            raise GenerationError(f"validation du contenu échouée après {1 + MAX_RETRIES} essai(s), rien n'est produit")

    # Tentative de récupération de l'image Pexels pour la preview
    # (non-bloquant : retombe sur image générique du gabarit si échec)
    image_keywords = brief.get("sujet", {}).get("image_keywords")
    photo = fetch_preview_image(image_keywords) if image_keywords and not args.dry_run else None
    if photo:
        print(f"[edition] image Pexels trouvée pour le preview (keywords: {image_keywords})")

    try:
        html_text, edition_number = build_html.assemble_index_html(shell, content, brief, date_str, photo=photo)
    except Exception as e:
        # Filet ultime pour le repli "meilleur essai" ci-dessus : un contenu
        # accepté malgré des erreurs résiduelles (longueur, stat...) reste
        # structurellement complet (les champs manquants font échouer
        # validate_content_schema() bien plus tôt, jamais tolérés par ce
        # repli), donc ceci ne devrait normalement jamais se déclencher —
        # mais un crash Python brut serait pire qu'une erreur de génération
        # propre si un cas non prévu survient malgré tout.
        raise GenerationError(f"assemblage HTML échoué sur le contenu retenu ({e}), rien n'est produit") from e

    html_errors = validate_assembled_html(html_text, content)
    if html_errors:
        print("[edition] validation du HTML assemblé échouée :", file=sys.stderr)
        for e in html_errors:
            print(f"  - {e}", file=sys.stderr)
        raise GenerationError("validation du HTML assemblé échouée, rien n'est écrit")

    out_path = Path(args.out) if args.out else REPO_ROOT / "_prototype-out" / f"{date_str}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_text, encoding="utf-8")

    # content.json validé — consommé par generate_post_edition.py (photo,
    # image Instagram, feed.xml, sitemap, archives.html), pour ne jamais
    # avoir à reparser le HTML déjà assemblé pour en extraire les mêmes
    # informations structurées. Même dossier/base que --out, extension
    # différente — jamais index.html ni un chemin réel du dépôt.
    content_path = out_path.with_suffix(".content.json")
    content_path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")

    if used_best_effort_fallback:
        print(f"[edition] ⚠ repli meilleur essai (validation non propre) — sortie de test écrite : {out_path}")
    else:
        print(f"[edition] validation OK — sortie de test écrite : {out_path}")
    print(f"[edition] contenu validé écrit : {content_path}")
    print(f"[edition] édition de test N°{edition_number}, {len(html_text)} caractères")
    print(
        f"[edition] usage OpenRouter (cumul de tous les essais) — "
        f"modèle {usage_total.get('model', args.model)} · "
        f"coût ≈ {usage_total.get('cost', '?')} $ · "
        f"tokens entrée {usage_total.get('prompt_tokens', '?')} · "
        f"tokens sortie {usage_total.get('completion_tokens', '?')}"
    )
    print("[edition] AUCUN commit, AUCUN push effectué — Phase 1 prototype (workflow_dispatch uniquement).")


if __name__ == "__main__":
    try:
        main()
    except GenerationError as e:
        print(f"[edition] ERREUR : {e}", file=sys.stderr)
        sys.exit(1)
