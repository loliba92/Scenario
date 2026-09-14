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
    python3 scripts/edition/generate_daily_edition.py --brief editorial-briefs/2026-09-20.json

    # Sans clé API, pour tester la mécanique (validations + templating)
    # avec une réponse de modèle déjà enregistrée :
    python3 scripts/edition/generate_daily_edition.py --brief editorial-briefs/2026-09-20.json --dry-run
"""
import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

import build_html

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-sonnet-5"
REDACTION_PROMPT_PATH = REPO_ROOT / "docs" / "routine-redaction-prompt.md"
MIN_WORDS = 1100
MAX_RETRIES = 1  # 1 nouvel essai max en cas d'échec de validation — jamais plus (coût maîtrisé)


class GenerationError(Exception):
    pass


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

    n_comprendre = len(brief.get("encarts_decides", {}).get("comprendre_box") or [])
    if n_comprendre > 2:
        errors.append(f"encarts_decides.comprendre_box : {n_comprendre} éléments (max 2)")

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
# Appel OpenRouter
# ---------------------------------------------------------------------------
def build_user_prompt(redaction_prompt, brief):
    return (
        redaction_prompt
        + "\n\n---\n\nBrief éditorial à rédiger (JSON) :\n\n"
        + json.dumps(brief, ensure_ascii=False, indent=2)
    )


def _do_openrouter_request(req, socket_timeout):
    with urllib.request.urlopen(req, timeout=socket_timeout) as resp:
        return json.loads(resp.read())


def call_openrouter(prompt, model, api_key, temperature=0.45, max_tokens=12000, timeout=180):
    """Incident réel du 14 septembre 2026 (premier vrai appel de test) :
    Claude Sonnet a tourné plus de 16 minutes sans jamais répondre, forçant
    une annulation manuelle du run — deux causes trouvées après coup :
    1. Le raisonnement étendu du modèle n'était pas désactivé (contrairement
       à translate_daily.py pour Deepseek, `"reasoning": {"enabled": False}`)
       — corrigé ci-dessous, même garde-fou.
    2. `urlopen(..., timeout=N)` ne borne QUE chaque lecture socket
       individuelle, jamais la durée totale de la requête — si le serveur
       renvoie des octets en filet continu, aucune lecture ne dépasse N
       secondes et l'appel peut ne jamais expirer. Corrigé en exécutant la
       requête dans un thread et en bornant l'attente globale avec
       `future.result(timeout=...)` : si le délai est dépassé, le script
       lève une erreur et sort — la fermeture du process coupe la
       connexion TCP sous-jacente, ce qui arrête la génération côté
       serveur au lieu de la laisser tourner indéfiniment en arrière-plan."""
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "reasoning": {"enabled": False},
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(OPENROUTER_URL, method="POST", data=body, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })

    last_err = None
    for attempt in range(2):  # 1 essai + 1 retry réseau court, jamais plus (voir MAX_RETRIES pour le retry de validation, distinct)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_do_openrouter_request, req, timeout)
            try:
                data = future.result(timeout=timeout)
                break
            except concurrent.futures.TimeoutError:
                # Jamais réessayé automatiquement (voir consigne « pas de
                # retries agressifs ») — un dépassement du délai global est
                # un échec net, pas une panne transitoire à retenter.
                raise GenerationError(
                    f"appel OpenRouter sans réponse après {timeout}s (délai global dépassé) — "
                    "arrêt forcé, vérifier le tableau de bord OpenRouter pour le coût réel "
                    "déjà engagé sur cette tentative avant de relancer"
                )
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                last_err = e
                if attempt == 0:
                    print(f"[openrouter] erreur réseau, nouvel essai dans 3s : {e}", file=sys.stderr)
                    time.sleep(3)
                else:
                    raise GenerationError(f"appel OpenRouter impossible après 2 essais : {last_err}")

    if "choices" not in data:
        raise GenerationError(f"réponse OpenRouter sans 'choices' : {data}")
    content_str = data["choices"][0]["message"]["content"]
    try:
        content = json.loads(content_str)
    except json.JSONDecodeError as e:
        raise GenerationError(f"réponse du modèle n'est pas un JSON valide : {e}\n{content_str[:2000]}")
    usage = data.get("usage", {})
    return content, usage


# ---------------------------------------------------------------------------
# Validation du contenu retourné par le modèle (avant construction HTML)
# ---------------------------------------------------------------------------
def validate_content_schema(content, brief):
    errors = []
    required = ["h1", "question_text", "section_title", "dek", "stakes_branches",
                "indicators", "cards", "essentiel_box", "delta_france", "lexique",
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

    if not errors:
        pcts = [content["cards"][k]["pct"] for k in ("favorable", "stable", "degrade")]
        if abs(sum(pcts) - 100) > 1:
            errors.append(f"somme des pct des 3 cartes = {sum(pcts)} (attendu 100)")
        for kind in ("favorable", "stable", "degrade"):
            card = content["cards"][kind]
            for f in ("pct", "gauge_word", "h3", "why", "indicateurs_touches", "france_line", "france_impact"):
                if f not in card or card[f] in (None, "", []):
                    errors.append(f"cards.{kind}.{f} manquant ou vide")
            if card.get("france_impact") not in ("favorable", "degrade"):
                errors.append(f"cards.{kind}.france_impact doit être 'favorable' ou 'degrade' (reçu : {card.get('france_impact')!r})")
            if len(card.get("why", [])) < 2:
                errors.append(f"cards.{kind}.why : {len(card.get('why', []))} paragraphes (2 attendus)")

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

    if len(content["essentiel_box"]) != 4:
        errors.append(f"essentiel_box : {len(content['essentiel_box'])} paragraphes (4 attendus)")

    df = content["delta_france"]
    for f in ("kind", "score", "word", "text"):
        if f not in df:
            errors.append(f"delta_france.{f} manquant")
    if df.get("kind") not in ("positif", "negatif"):
        errors.append(f"delta_france.kind doit être 'positif' ou 'negatif' (reçu : {df.get('kind')!r})")

    for term in content.get("lexique", []):
        for f in ("slug", "terme", "definition"):
            if f not in term or not term[f]:
                errors.append(f"lexique : entrée incomplète (manque {f}) : {term}")

    # Placeholders résiduels — même garde-fou que la validation de forme
    # décrite dans l'audit (point E.1).
    flat_text = json.dumps(content, ensure_ascii=False)
    for pattern in (r"\bTODO\b", r"\{\{", r"\bXXX\b", r"lorem ipsum"):
        if re.search(pattern, flat_text, re.I):
            errors.append(f"placeholder résiduel détecté (motif {pattern!r}) dans la réponse du modèle")

    return errors


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
        (".essentiel-box", 1), (".sources-list", 1),
    ]
    for sel, expected_count in required_selectors:
        found = len(soup.select(sel))
        if found != expected_count:
            errors.append(f"structure : {sel} trouvé {found} fois (attendu {expected_count})")

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

    for attempt in range(1 + MAX_RETRIES):
        if args.dry_run:
            content, usage = load_dry_run_fixture(date_str)
        else:
            prompt = build_user_prompt(redaction_prompt, brief)
            if attempt > 0:
                prompt += (
                    "\n\nATTENTION — ta réponse précédente a échoué la validation pour les raisons "
                    f"suivantes, corrige-les précisément avant de renvoyer : {errors}"
                )
            content, usage = call_openrouter(prompt, args.model, api_key)
        for k in ("cost", "prompt_tokens", "completion_tokens"):
            usage_total[k] = usage_total.get(k, 0) + (usage.get(k) or 0)

        errors = validate_content_schema(content, brief)
        if not errors:
            break
        print(f"[edition] validation du contenu échouée (essai {attempt + 1}) :", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        if args.dry_run:
            break  # inutile de "réessayer" contre la même fixture figée

    if errors:
        raise GenerationError(f"validation du contenu échouée après {1 + MAX_RETRIES} essai(s), rien n'est produit")

    html_text, edition_number = build_html.assemble_index_html(shell, content, brief, date_str)

    html_errors = validate_assembled_html(html_text, content)
    if html_errors:
        print("[edition] validation du HTML assemblé échouée :", file=sys.stderr)
        for e in html_errors:
            print(f"  - {e}", file=sys.stderr)
        raise GenerationError("validation du HTML assemblé échouée, rien n'est écrit")

    out_path = Path(args.out) if args.out else REPO_ROOT / "_prototype-out" / f"{date_str}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_text, encoding="utf-8")

    print(f"[edition] validation OK — sortie de test écrite : {out_path}")
    print(f"[edition] édition de test N°{edition_number}, {len(html_text)} caractères")
    print(
        f"[edition] usage OpenRouter — modèle {args.model} · "
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
