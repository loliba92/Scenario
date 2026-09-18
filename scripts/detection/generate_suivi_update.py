#!/usr/bin/env python3
"""
Port OpenRouter de la routine Claude Code Remote « Scénario — Détection
sujets à suivre » (docs/routine-detection-prompt.md) — demandé le 17
septembre 2026 : « on prend claude code via open router, j'ai besoin de
faire ça pour réduire mes tokens » — même logique que `generate_
fallback_brief.py` pour la recherche/rédaction quotidienne : un modèle
Claude avec le server tool OpenRouter `openrouter:web_search` (recherche
web réelle, pas une extraction d'un texte déjà écrit comme `generate_
daily_pub.py`), facturé sur le compte OpenRouter plutôt que sur le
forfait Claude Code.

**Le jugement éditorial reste le même qu'avant** (voir docs/routine-
detection-prompt.md pour la version de référence, non modifiée) : recherche
réelle, réestimation sérieuse des 3 scénarios, sélection du sujet le plus
crédible — jamais mécanique comme `generate_daily_pub.py`. Le compromis
assumé ici : la qualité de recherche/jugement d'un modèle OpenRouter avec
plugin web_search est probablement un cran en dessous du WebSearch natif
de Claude Code — accepté explicitement par l'utilisateur en échange du
coût.

Garde-fous repris du reste du pipeline OpenRouter :
- Les pourcentages doivent sommer à 100 (tolérance d'arrondi ±1).
- Aucune clôture (🏁) n'est jamais publiée automatiquement — seulement
  signalée dans le résumé final (point 5 de la routine de référence).
- Un seul sujet publié par passage (point 4) — jamais plusieurs.
- Jamais un sujet dont le point de référence a moins de 10 jours.
- `--dry-run` : affiche ce qui serait fait, ne modifie/committe rien.

Ce script écrit les fichiers mais NE COMMIT PAS — comme `generate_daily_
pub.py`, c'est au workflow appelant de committer/pousser (voir
.github/workflows/detection.yml).

Usage :
    python3 scripts/detection/generate_suivi_update.py --dry-run
    OPENROUTER_API_KEY=xxx python3 scripts/detection/generate_suivi_update.py
"""
import argparse
import html
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "edition"))
from generate_daily_edition import (  # noqa: E402
    GenerationError,
    call_openrouter,
)

# Passé de DEFAULT_MODEL (anthropic/claude-sonnet-5) à DeepSeek le
# 18 septembre 2026 : détection de sujets à suivre = tri/classement,
# pas de rédaction fine — finance le passage d'Opus sur la recherche
# quotidienne (voir generate_fallback_brief.py).
DETECTION_MODEL = "deepseek/deepseek-v4-flash"

SUJETS_A_SUIVRE = ROOT / "docs" / "sujets-a-suivre.md"
ARCHIVES_DIR = ROOT / "archives"
SUIVI_DIR = ROOT / "suivi"
GABARIT_PATH = SUIVI_DIR / "_gabarit.html"
FEED_SUIVI = ROOT / "feed-suivi.xml"
EN_FEED_SUIVI = ROOT / "en" / "feed-suivi.xml"
TOPIC_IMAGES_DIR = ROOT / "assets" / "social" / "topic-images"
PARIS = ZoneInfo("Europe/Paris")

GAP_THRESHOLD = 20
MIN_REFERENCE_AGE_DAYS = 10
JOURNAL_WINDOW_DAYS = 30

KIND_ORDER = ["favorable", "stable", "degrade"]
KIND_LABEL = {"favorable": "Favorable", "stable": "Stable", "degrade": "Dégradé"}

MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin",
             "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_FR_SHORT = ["janv.", "févr.", "mars", "avril", "mai", "juin",
                    "juil.", "août", "sept.", "oct.", "nov.", "déc."]

# Regex large plutôt qu'exhaustive : couvre les blocs Unicode où vivent
# les émojis effectivement utilisés dans ce dépôt (🤝⚖️🔥📈📉🔄...).
EMOJI_RE = re.compile(
    r"^([\U0001F000-\U0001FAFF☀-➿️‍]+)\s*"
)


class DetectionError(Exception):
    pass


def fmt_date_long(d):
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}"


def fmt_date_short(d):
    return f"{d.day} {MONTHS_FR_SHORT[d.month - 1]}"


def parse_french_date(s):
    """'7 août 2026' -> date(2026, 8, 7)."""
    m = re.match(r"(\d{1,2})\s+(\w+)\.?\s+(\d{4})", s.strip())
    if not m:
        raise DetectionError(f"date française non reconnue : {s!r}")
    day, month_name, year = m.groups()
    month_name = month_name.lower()
    for i, name in enumerate(MONTHS_FR):
        if name.startswith(month_name[:4]):
            return date(int(year), i + 1, int(day))
    raise DetectionError(f"mois non reconnu dans {s!r}")


def split_emoji(title):
    m = EMOJI_RE.match(title)
    if m:
        return m.group(1), title[m.end():].strip()
    return "", title.strip()


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def slugify_fallback(text):
    """Utilisé seulement si le modèle ne renvoie pas de 'slug' exploitable."""
    n = unicodedata.normalize("NFKD", text)
    n = n.encode("ascii", "ignore").decode()
    n = re.sub(r"[^a-zA-Z0-9]+", "-", n).strip("-").lower()
    return n[:40] or "sujet"


# ---------------------------------------------------------------------------
# docs/sujets-a-suivre.md
# ---------------------------------------------------------------------------
def parse_active_suivis(md_text):
    """Liste des sujets de la section « Suivis actifs » : bullets '- **Titre**
    (édition du {date})' suivis de lignes indentées jusqu'au prochain '- **'."""
    m = re.search(r"^## Suivis actifs\s*$(.*?)(?=^---)", md_text, re.M | re.S)
    if not m:
        raise DetectionError("section 'Suivis actifs' introuvable dans sujets-a-suivre.md")
    body = m.group(1)
    entries = []
    for bm in re.finditer(
        r"^- \*\*(.+?)\*\* \(édition du ([^)]+)\)\n((?:  .*\n?)+)",
        body, re.M,
    ):
        title, origin_str, block = bm.groups()
        file_m = re.search(r"`suivi/([a-z0-9-]+)\.html`", block)
        if not file_m:
            continue
        entries.append({
            "title": title.strip(),
            "slug": file_m.group(1),
            "origin_date": parse_french_date(origin_str),
            "block": block,
        })
    return entries


def parse_journal(md_text, today):
    m = re.search(r"^## Journal des sujets publiés\s*$(.*)\Z", md_text, re.M | re.S)
    if not m:
        raise DetectionError("section 'Journal des sujets publiés' introuvable")
    entries = []
    for lm in re.finditer(
        r"^- (\d{2})\.(\d{2})\.(\d{4}) — \[(.+?)\]\(\.\./archives/(\d{4}-\d{2}-\d{2})\.html\)(.*)$",
        m.group(1), re.M,
    ):
        dd, mm, yyyy, title, date_iso, trailing = lm.groups()
        d = date.fromisoformat(date_iso)
        if (today - d).days > JOURNAL_WINDOW_DAYS:
            continue
        if "a désormais sa page de suivi dédiée" in trailing:
            continue
        entries.append({"title": title.strip(), "date": d})
    return entries


def update_active_suivi_entry(md_text, slug, origin_title, origin_date_str,
                               new_version_label, new_date, next_echeance_note):
    """Met à jour 'Dernière vérification' (et ajoute une ligne 'Prochaine
    échéance' si fournie) pour le bloc du sujet `slug` — jamais réécrire
    le reste du bloc (historique déjà publié)."""
    pattern = re.compile(
        r"(- \*\*" + re.escape(origin_title) + r"\*\* \(édition du " + re.escape(origin_date_str) +
        r"\)\n(?:  .*\n?)+?)(Dernière vérification : [^\n]+\.)\n",
        re.M,
    )
    replacement_tail = f"Dernière vérification : {fmt_date_long(new_date)} ({new_version_label}).\n"
    new_text, n = pattern.subn(lambda mo: mo.group(1) + replacement_tail, md_text, count=1)
    if n != 1:
        raise DetectionError(f"impossible de mettre à jour l'entrée 'Suivis actifs' pour {slug!r}")
    return new_text


def add_active_suivi_entry(md_text, entry_block):
    """Ajoute un nouveau bullet à la fin de la section 'Suivis actifs'
    (juste avant le '---' de fin de section)."""
    pattern = re.compile(r"(^## Suivis actifs\s*$.*?)(\n---\n)", re.M | re.S)
    m = pattern.search(md_text)
    if not m:
        raise DetectionError("section 'Suivis actifs' introuvable pour y ajouter une entrée")
    return md_text[:m.end(1)] + "\n" + entry_block + md_text[m.end(1):]


def mark_journal_entry_has_suivi(md_text, date_iso):
    pattern = re.compile(
        r"(^- \d{2}\.\d{2}\.\d{4} — \[.+?\]\(\.\./archives/" + re.escape(date_iso) + r"\.html\))(\n|$)",
        re.M,
    )
    new_text, n = pattern.subn(
        r"\1 — a désormais sa page de suivi dédiée, voir « Suivis actifs » ci-dessus.\2",
        md_text, count=1,
    )
    if n != 1:
        raise DetectionError(f"ligne journal introuvable pour {date_iso!r}")
    return new_text


# ---------------------------------------------------------------------------
# Lecture d'une édition source (archives/{date}.html) — 3 cartes de scénarios
# ---------------------------------------------------------------------------
def read_edition_scenarios(html_text):
    h1_m = re.search(r"<h1>(.*?)</h1>", html_text, re.S)
    h1 = strip_tags(h1_m.group(1)) if h1_m else ""
    stakes_m = re.search(r'<p class="stakes-text">(.*?)</p>', html_text, re.S)
    stakes = strip_tags(stakes_m.group(1)) if stakes_m else ""

    cards = []
    for chunk in re.split(r'(?=<article class="card")', html_text):
        if '<article class="card"' not in chunk:
            continue
        kind_m = re.search(r'data-kind="(\w+)"', chunk)
        pct_m = re.search(r'data-pct="(\d+)"', chunk)
        title_m = re.search(r"<h3>(.*?)</h3>", chunk, re.S)
        whys = re.findall(r'<p class="why">(.*?)</p>', chunk, re.S)
        if not (kind_m and pct_m and title_m):
            continue
        cards.append({
            "kind": kind_m.group(1),
            "pct": int(pct_m.group(1)),
            "title": strip_tags(title_m.group(1)),
            "why": " ".join(strip_tags(w) for w in whys),
        })
        if len(cards) == 3:
            break
    cards.sort(key=lambda c: KIND_ORDER.index(c["kind"]) if c["kind"] in KIND_ORDER else 9)
    return h1, stakes, cards


# ---------------------------------------------------------------------------
# Lecture de l'état actuel d'une page suivi/{sujet}.html
# ---------------------------------------------------------------------------
def read_suivi_state(html_text):
    h1_m = re.search(r"<h1>(.*?)</h1>", html_text, re.S)
    h1 = strip_tags(h1_m.group(1)) if h1_m else ""

    origin_m = re.search(r'<a class="origin-link" href="\.\./archives/(\d{4}-\d{2}-\d{2})\.html"', html_text)
    origin_date = date.fromisoformat(origin_m.group(1)) if origin_m else None

    evo_m = re.search(r"var evoData = (\[.*?\]);", html_text, re.S)
    evo_entries = []
    if evo_m:
        for em in re.finditer(
            r'\{\s*label:\s*"([^"]+)",\s*date:\s*"([^"]*)",\s*favorable:\s*(\d+),\s*stable:\s*(\d+),\s*degrade:\s*(\d+)\s*\}',
            evo_m.group(1),
        ):
            evo_entries.append({
                "label": em.group(1), "date": em.group(2),
                "favorable": int(em.group(3)), "stable": int(em.group(4)), "degrade": int(em.group(5)),
            })
    if not evo_entries:
        raise DetectionError("evoData vide/illisible dans la page suivi")

    version_count = len(re.findall(r'<div class="version(?:\s|">)', html_text))
    last_date_m = list(re.finditer(r'<span class="version-date">([^<]+)</span>', html_text))
    last_date_text = last_date_m[-1].group(1).strip() if last_date_m else evo_entries[-1]["date"]

    blocks = list(re.finditer(r'<div class="mini-scenarios">(.*?)<div class="conclusion">', html_text, re.S))
    if not blocks:
        raise DetectionError("aucun bloc mini-scenarios trouvé dans la page suivi")
    last_block = blocks[-1].group(1)
    titles = {}
    for chunk in re.split(r'(?=<div class="mini-scenario")', last_block):
        kind_m = re.search(r'data-kind="(\w+)"', chunk)
        title_m = re.search(r'<p class="mini-scenario-title">(.*?)</p>', chunk, re.S)
        if not (kind_m and title_m):
            continue
        raw = re.sub(r'<span class="mini-scenario-pct">.*?</span>', "", title_m.group(1))
        emoji, text = split_emoji(strip_tags(raw))
        titles[kind_m.group(1)] = {"emoji": emoji, "title": text}

    return {
        "h1": h1, "origin_date": origin_date, "evo_entries": evo_entries,
        "version_count": version_count, "last_date_text": last_date_text,
        "titles": titles,
    }


# ---------------------------------------------------------------------------
# Vérification structurelle CSS/HTML (point 1bis de la routine de référence)
# — port déterministe du snippet bash, aucune part de jugement ici.
# ---------------------------------------------------------------------------
def find_missing_css_classes(html_text):
    style_m = re.search(r"<style>(.*?)</style>", html_text, re.S)
    style = style_m.group(1) if style_m else ""
    used = set(re.findall(r'class="([^"]+)"', html_text))
    used = {c for group in used for c in group.split()}
    defined = set(re.findall(r"\.([a-zA-Z][a-zA-Z0-9_-]*)", style))
    return sorted(used - defined)


def autofix_missing_css(suivi_path, gabarit_text):
    text = suivi_path.read_text(encoding="utf-8")
    missing = find_missing_css_classes(text)
    if not missing:
        return False
    gabarit_style_m = re.search(r"<style>(.*?)</style>", gabarit_text, re.S)
    gabarit_style = gabarit_style_m.group(1) if gabarit_style_m else ""
    added_rules = []
    for cls in missing:
        # Cherche la règle (ou groupe de règles séparées par virgule) qui
        # définit .cls dans le gabarit — recopiée telle quelle, jamais
        # improvisée (voir docs/routine-detection-prompt.md, point 1bis).
        rule_m = re.search(
            r"(^[^{}\n]*\." + re.escape(cls) + r"[^{}\n]*\{[^}]*\})",
            gabarit_style, re.M,
        )
        if rule_m:
            added_rules.append("  " + rule_m.group(1).strip())
    if not added_rules:
        print(f"[detection] ATTENTION : classes manquantes sans règle retrouvable dans le gabarit "
              f"pour {suivi_path.name} : {missing} — non corrigé automatiquement, à examiner à la main.",
              file=sys.stderr)
        return False
    patched = text.replace("</style>", "\n  /* Ajouté automatiquement (point 1bis) — règle recopiée depuis _gabarit.html */\n"
                            + "\n".join(added_rules) + "\n</style>", 1)
    suivi_path.write_text(patched, encoding="utf-8")
    still_missing = find_missing_css_classes(patched)
    print(f"[detection] CSS corrigé sur {suivi_path.name} : {sorted(set(missing) - set(still_missing))}"
          + (f" (toujours manquant : {still_missing})" if still_missing else ""))
    return True


# ---------------------------------------------------------------------------
# Appel OpenRouter — recherche web réelle + réestimation.
# ---------------------------------------------------------------------------
def build_search_prompt(candidate):
    is_new = candidate["type"] == "journal"
    lines = [
        "Tu es le rédacteur du site d'actualité Scénario (lesscenarios.fr). "
        "Pour le sujet ci-dessous, cherche sur le web s'il y a eu un développement "
        "réel et notable depuis la date de référence, puis réestime les 3 scénarios "
        "avec le même sérieux méthodologique qu'une édition normale.",
        "",
        f"Sujet : {candidate['h1']}",
        f"Date de référence : {fmt_date_long(candidate['reference_date'])}",
        "",
        "Scénarios actuels (favorable / stable / dégradé) et leurs probabilités :",
    ]
    for kind in KIND_ORDER:
        s = candidate["scenarios"][kind]
        lines.append(f"- {kind} ({s['pct']}%) : {s['title']} — {s.get('why', '')}")
    if candidate.get("echeance_note"):
        lines.append(f"\nÉchéance connue mentionnée : {candidate['echeance_note']}")
    lines += [
        "",
        "Règles strictes :",
        "- Cherche des faits réels, datés, sourcés (2-4 sources, liens réels jamais inventés).",
        "- Si rien de notable n'a changé depuis la date de référence, renvoie has_development=false "
        "et arrête-toi là (ne remplis aucun autre champ).",
        "- Les 3 pourcentages doivent sommer à 100.",
        "- Chaque 'reasons' doit répondre explicitement à « pourquoi cette probabilité "
        "monte/descend/reste stable », en nommant le fait ou son absence — jamais une "
        "phrase vague du type « la situation évolue ».",
        "- 'conclusion_kind' = le scénario qui bouge le plus (le plus gros écart en points) ; "
        "'conclusion_text' explique pourquoi ce scénario précisément, sans répéter le "
        "pourcentage (je le formate moi-même).",
        "- 'social_sentence' = UNE phrase autonome pour un post court (réseaux sociaux) : "
        "le fait concret, sans pourcentage ni conclusion (je les ajoute après), style : "
        "« Donald Trump publie une carte plaçant l'Islande sous drapeau américain, sans "
        "réponse de Washington depuis ».",
        "- 'short_labels' = pour chacun des 3 scénarios, une courte formule en minuscules "
        "utilisable au milieu d'une phrase (ex. « la dépendance sans garantie renforcée »), "
        "jamais le titre complet ni une majuscule initiale.",
        "- closure_signal=true UNIQUEMENT si un scénario franchit ≥80% ou ≤20% ET qu'un fait "
        "réel et vérifiable confirme clairement lequel des 3 scénarios s'est réalisé — "
        "jamais publié automatiquement, seulement signalé (closure_note).",
    ]
    if is_new:
        lines += [
            "",
            "Ce sujet n'a pas encore de page de suivi dédiée — remplis EN PLUS :",
            "- 'slug' : identifiant court (1-3 mots, minuscules, tirets, sans accents), "
            "ex. 'islande', 'taux-marche-arriere', 'arabie-saoudite-sport'.",
            "- 'v0_intro' : 1 paragraphe condensé rappelant pourquoi le sujet posait question "
            "à l'origine (reformulation, pas un copier-coller du texte source).",
            "- 'v0_scenarios' : pour chacun des 3 scénarios, {emoji, text} — un émoji pertinent "
            "et 1-2 phrases condensées reprenant l'idée centrale du scénario d'origine.",
            "- 'v0_conclusion_kind' et 'v0_conclusion_text' : le scénario jugé le plus probable "
            "À L'ÉPOQUE (pas aujourd'hui) et pourquoi, en une phrase.",
        ]
    lines += [
        "",
        "Renvoie un unique objet JSON avec exactement les champs demandés "
        "(has_development, et si true : percentages, fact_paragraph, reasons, "
        "short_labels, conclusion_kind, conclusion_text, social_sentence, sources, "
        "closure_signal, closure_note" + (", slug, v0_intro, v0_scenarios, "
        "v0_conclusion_kind, v0_conclusion_text" if is_new else "") + ").",
    ]
    return "\n".join(lines)


def search_and_reestimate(candidate, model, api_key):
    tools = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 6}}]
    prompt = build_search_prompt(candidate)
    content, usage = call_openrouter(
        prompt, model, api_key, temperature=0.3, max_tokens=4000, timeout=150, tools=tools,
    )
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        raise GenerationError(f"réponse non-JSON pour {candidate['h1']!r} : {e}\n{content[:1500]}")

    if not result.get("has_development"):
        return None, usage

    pct = result.get("percentages") or {}
    try:
        pct = {k: int(round(float(pct[k]))) for k in KIND_ORDER}
    except (KeyError, TypeError, ValueError):
        raise GenerationError(f"percentages incomplet/invalide pour {candidate['h1']!r} : {pct!r}")
    total = sum(pct.values())
    if abs(total - 100) > 1:
        raise GenerationError(f"percentages ne somme pas à 100 (={total}) pour {candidate['h1']!r} : {pct!r}")
    if abs(total - 100) == 1:
        # Ajustement de l'arrondi sur le plus gros scénario — jamais sur le
        # choix éditorial, juste la contrainte arithmétique 100%.
        biggest = max(pct, key=pct.get)
        pct[biggest] += 100 - total

    if result.get("conclusion_kind") not in KIND_ORDER:
        raise GenerationError(f"conclusion_kind invalide pour {candidate['h1']!r} : {result.get('conclusion_kind')!r}")

    gap = max(abs(pct[k] - candidate["scenarios"][k]["pct"]) for k in KIND_ORDER)
    result["percentages"] = pct
    result["gap"] = gap
    return result, usage


def select_winner(eligible, model, api_key):
    """eligible: liste de (candidate, result). Choisit le sujet le plus
    crédible — pas seulement l'écart en points le plus large (point 4 de la
    routine de référence)."""
    if len(eligible) == 1:
        return eligible[0]
    lines = [
        "Plusieurs sujets sont éligibles à une mise à jour de page de suivi "
        "aujourd'hui. Choisis-en UN SEUL, le plus crédible (qualité/croisement "
        "des sources, importance réelle du développement — pas seulement "
        "l'écart en points le plus large).",
        "",
    ]
    for i, (cand, res) in enumerate(eligible):
        lines.append(f"{i}. {cand['h1']} — écart {res['gap']} points — {res['fact_paragraph']}")
    lines.append('\nRenvoie {"chosen_index": N}.')
    content, usage = call_openrouter(
        "\n".join(lines), model, api_key, temperature=0.2, max_tokens=200, timeout=60,
    )
    try:
        idx = json.loads(content)["chosen_index"]
        return eligible[int(idx)]
    except Exception:
        # Repli déterministe plutôt que planter sur un sujet par ailleurs
        # publiable — le plus gros écart, à défaut d'un choix qualitatif.
        print("[detection] sélection du sujet gagnant : réponse illisible, repli sur l'écart le plus large", file=sys.stderr)
        return max(eligible, key=lambda pair: pair[1]["gap"])


# ---------------------------------------------------------------------------
# Construction des blocs HTML.
# ---------------------------------------------------------------------------
def verb_for_delta(delta):
    if delta > 0:
        return "grimpe"
    if delta < 0:
        return "recule"
    return "reste stable"


def arrow_for_delta(delta):
    if delta > 0:
        return "is-up", "↑"
    if delta < 0:
        return "is-down", "↓"
    return "is-flat", "→"


UPDATE_BLOCK_TMPL = """    <div class="version is-update">
      <div class="version-head">
        <span class="version-tag">V{n} — Mise à jour</span>
        <span class="version-date">{date_maj}</span>
        <button type="button" class="version-toggle" aria-expanded="false" aria-controls="version-content-v{n}">Détails <span class="version-toggle-icon" aria-hidden="true">▾</span></button>
      </div>
      <div class="version-content" id="version-content-v{n}">
        <div class="version-content-inner">
        <p>{fact_paragraph}</p>
        <div class="mini-scenarios">
{scenario_cards}
        </div>
        <div class="conclusion">
          <span class="conclusion-label">Conclusion vs {prev_label}</span>
          <p><strong>{concl_emoji} {concl_verdict} ({concl_pct}%)</strong> — {concl_text}.</p>
        </div>
        <p class="sources-note">Sources : {sources_html}</p>
        </div>
      </div>
    </div>
"""

SCENARIO_CARD_UPDATE_TMPL = """          <div class="mini-scenario" data-kind="{kind}">
            <p class="mini-scenario-title">{emoji} {title}</p>
            <p class="mini-scenario-evolution"><span class="evo-current">{new}%</span> <span class="evo-arrow {arrow_class}">{arrow}</span> <span class="evo-prev">(vs. {prev}% en {prev_label})</span></p>
            <p class="mini-scenario-text">{reason}</p>
          </div>"""

SCENARIO_CARD_V0_TMPL = """            <div class="mini-scenario" data-kind="{kind}">
              <p class="mini-scenario-title">{emoji} {title} <span class="mini-scenario-pct">{pct}%</span></p>
              <p class="mini-scenario-text">{text}</p>
            </div>"""

V0_BLOCK_TMPL = """    <div class="version">
      <div class="version-head">
        <span class="version-tag">V0 — Point de départ</span>
        <span class="version-date">{date_origine}</span>
        <button type="button" class="version-toggle" aria-expanded="false" aria-controls="version-content-v0">Détails <span class="version-toggle-icon" aria-hidden="true">▾</span></button>
      </div>
      <div class="version-content" id="version-content-v0">
        <div class="version-content-inner">
        <h2 class="version-title">{titre_court}</h2>
        <div class="version-body">
          <p>{intro}</p>
          <div class="mini-scenarios">
{scenario_cards}
          </div>
          <div class="conclusion">
            <span class="conclusion-label">Scénario jugé le plus probable à l'époque</span>
            <p><strong>{concl_emoji} {concl_title} ({concl_pct}%)</strong> — {concl_text}.</p>
          </div>
        </div>
        </div>
      </div>
    </div>
"""


def build_update_block(version_n, date_maj, titles, prev_pcts, new_pcts, reasons,
                        fact_paragraph, conclusion_kind, conclusion_text, sources, prev_label):
    cards = []
    for kind in KIND_ORDER:
        arrow_class, arrow = arrow_for_delta(new_pcts[kind] - prev_pcts[kind])
        cards.append(SCENARIO_CARD_UPDATE_TMPL.format(
            kind=kind, emoji=titles[kind]["emoji"], title=titles[kind]["title"],
            new=new_pcts[kind], arrow_class=arrow_class, arrow=arrow,
            prev=prev_pcts[kind], prev_label=prev_label, reason=reasons[kind],
        ))
    delta = new_pcts[conclusion_kind] - prev_pcts[conclusion_kind]
    verdict = f"{KIND_LABEL[conclusion_kind]}, {'+' if delta >= 0 else ''}{delta} points"
    sources_html = ", ".join(
        f'<a href="{s["url"]}" target="_blank" rel="noopener noreferrer">{html.escape(s["name"])} ↗</a>'
        for s in sources
    )
    return UPDATE_BLOCK_TMPL.format(
        n=version_n, date_maj=date_maj, fact_paragraph=fact_paragraph,
        scenario_cards="\n".join(cards), prev_label=prev_label,
        concl_emoji=titles[conclusion_kind]["emoji"], concl_verdict=verdict,
        concl_pct=new_pcts[conclusion_kind], concl_text=conclusion_text,
        sources_html=sources_html,
    )


def build_v0_block(date_origine, titre_court, intro, pcts, v0_scenarios, conclusion_kind, conclusion_text):
    cards = []
    for kind in KIND_ORDER:
        cards.append(SCENARIO_CARD_V0_TMPL.format(
            kind=kind, emoji=v0_scenarios[kind]["emoji"], title=v0_scenarios[kind]["title"],
            pct=pcts[kind], text=v0_scenarios[kind]["text"],
        ))
    return V0_BLOCK_TMPL.format(
        date_origine=date_origine, titre_court=titre_court, intro=intro,
        scenario_cards="\n".join(cards),
        concl_emoji=v0_scenarios[conclusion_kind]["emoji"],
        concl_title=v0_scenarios[conclusion_kind]["title"],
        concl_pct=pcts[conclusion_kind], concl_text=conclusion_text,
    )


def insert_update_into_suivi(html_text, block_html, new_evo_entry):
    marker = "\n  </div>\n</section>\n\n<section class=\"follow-block\""
    if marker not in html_text:
        raise DetectionError("marqueur de fin de <section class=\"timeline\"> introuvable")
    html_text = html_text.replace(marker, "\n" + block_html + "\n  </div>\n</section>\n\n<section class=\"follow-block\"", 1)

    evo_m = re.search(r"(var evoData = \[\n)(.*?)(\n\s*\];)", html_text, re.S)
    if not evo_m:
        raise DetectionError("evoData introuvable pour insertion")
    new_line = (
        f'      {{ label: "{new_evo_entry["label"]}", date: "{new_evo_entry["date"]}", '
        f'favorable: {new_evo_entry["favorable"]}, stable: {new_evo_entry["stable"]}, '
        f'degrade: {new_evo_entry["degrade"]} }}'
    )
    body = evo_m.group(2).rstrip()
    if not body.endswith(","):
        body += ","
    new_body = body + "\n" + new_line
    html_text = html_text[:evo_m.start(2)] + new_body + html_text[evo_m.end(2):]
    return html_text


# ---------------------------------------------------------------------------
# Nouvelle page suivi/{slug}.html à partir du gabarit.
# ---------------------------------------------------------------------------
def create_new_suivi_page(slug, question, origin_date, origin_iso, v0_intro, v0_scenarios,
                           v0_pcts, v0_conclusion_kind, v0_conclusion_text, titre_court,
                           photo_meta):
    gabarit = GABARIT_PATH.read_text(encoding="utf-8")

    if photo_meta:
        figure_html = (
            '    <figure class="article-image">\n'
            '      <div class="article-image-photo-wrap">\n'
            f'        <img class="article-image-photo" src="../assets/social/topic-images/suivi-{slug}-wide.jpg" alt="{html.escape(photo_meta.get("alt", ""))}">\n'
            '        <div class="article-image-scrim"></div>\n'
            '        <div class="article-image-masthead">\n'
            '          <img class="article-image-logo" src="../assets/logo.svg" alt="">\n'
            '          <span class="article-image-wordmark">Scéna<span class="rio">rio</span></span>\n'
            '        </div>\n'
            '      </div>\n'
            f'      <figcaption class="article-image-caption">Photo d\'illustration. {html.escape(photo_meta.get("photographer", ""))} / <a href="{photo_meta.get("pexels_url", "")}" target="_blank" rel="noopener noreferrer">Pexels ↗</a></figcaption>\n'
            '    </figure>\n\n'
        )
        og_image = f"https://lesscenarios.fr/assets/social/topic-images/suivi-{slug}.jpg"
    else:
        figure_html = ""
        og_image = "https://lesscenarios.fr/assets/social/og-image-v2.png"

    v0_block = build_v0_block(
        fmt_date_long(origin_date), titre_court, v0_intro, v0_pcts, v0_scenarios,
        v0_conclusion_kind, v0_conclusion_text,
    )

    text = gabarit
    text = text.replace(
        "<title>Suivi — {TITRE DE LA QUESTION} — Scénario</title>",
        f"<title>Suivi — {html.escape(question)} — Scénario</title>",
    )
    text = text.replace(
        '<meta name="description" content="Suivi dans le temps de l\'édition du {DATE ORIGINE} sur {SUJET} — chaque mise à jour s\'ajoute à la précédente, rien n\'est réécrit.">',
        f'<meta name="description" content="Suivi dans le temps de l\'édition du {fmt_date_long(origin_date)} — chaque mise à jour s\'ajoute à la précédente, rien n\'est réécrit.">',
    )
    text = text.replace(
        '<meta property="og:url" content="https://lesscenarios.fr/suivi/{sujet}.html">',
        f'<meta property="og:url" content="https://lesscenarios.fr/suivi/{slug}.html">',
    )
    text = text.replace(
        '<meta property="og:title" content="Suivi — {TITRE DE LA QUESTION}">',
        f'<meta property="og:title" content="Suivi — {html.escape(question)}">',
    )
    text = text.replace(
        '<meta property="og:description" content="Suivi dans le temps de l\'édition du {DATE ORIGINE} — chaque mise à jour s\'ajoute à la précédente, rien n\'est réécrit.">',
        f'<meta property="og:description" content="Suivi dans le temps de l\'édition du {fmt_date_long(origin_date)} — chaque mise à jour s\'ajoute à la précédente, rien n\'est réécrit.">',
    )
    text = text.replace(
        '<meta property="og:image" content="https://lesscenarios.fr/assets/social/og-image-v2.png">',
        f'<meta property="og:image" content="{og_image}">',
    )
    text = text.replace(
        '<h1>{TITRE DE LA QUESTION, ex. "Sujet : où en est-on ?"}</h1>',
        f"<h1>{html.escape(question)}</h1>",
    )

    figure_block_m = re.search(
        r'    <figure class="article-image">.*?</figure>\n\n', gabarit, re.S,
    )
    if figure_block_m:
        text = text.replace(figure_block_m.group(0), figure_html, 1)

    text = text.replace(
        '<a class="origin-link" href="../archives/{AAAA-MM-JJ}.html">Voir l\'édition d\'origine du {DATE ORIGINE EN TOUTES LETTRES} →</a>',
        f'<a class="origin-link" href="../archives/{origin_iso}.html">Voir l\'édition d\'origine du {fmt_date_long(origin_date)} →</a>',
    )

    timeline_m = re.search(
        r'(<section class="timeline">\s*<div class="wrap">\n\n).*?(\n\n  </div>\n</section>)',
        text, re.S,
    )
    if not timeline_m:
        raise DetectionError("section timeline introuvable dans le gabarit")
    text = text[:timeline_m.start()] + timeline_m.group(1) + v0_block + timeline_m.group(2) + text[timeline_m.end():]

    text = re.sub(
        r"var evoData = \[.*?\];",
        "var evoData = [\n"
        f'      {{ label: "V0", date: "{fmt_date_short(origin_date)}", '
        f'favorable: {v0_pcts["favorable"]}, stable: {v0_pcts["stable"]}, degrade: {v0_pcts["degrade"]} }}\n'
        "    ];",
        text, count=1, flags=re.S,
    )

    out_path = SUIVI_DIR / f"{slug}.html"
    out_path.write_text(text, encoding="utf-8")
    return out_path


def setup_topic_image(slug, origin_iso):
    src_jpg = TOPIC_IMAGES_DIR / f"{origin_iso}.jpg"
    src_json = TOPIC_IMAGES_DIR / f"{origin_iso}.json"
    if not (src_jpg.exists() and src_json.exists()):
        return None
    meta = json.loads(src_json.read_text(encoding="utf-8"))
    dest = TOPIC_IMAGES_DIR / f"suivi-{slug}.jpg"
    dest_wide = TOPIC_IMAGES_DIR / f"suivi-{slug}-wide.jpg"
    dest.write_bytes(src_jpg.read_bytes())
    dest_wide.write_bytes(src_jpg.read_bytes())
    return {
        "photographer": meta.get("photographer", ""),
        "pexels_url": meta.get("pexels_url", ""),
        "alt": meta.get("alt", ""),
        "jpg_for_social": dest,
    }


# ---------------------------------------------------------------------------
# feed-suivi.xml (+ miroir EN traduit séparément, voir docs/routine-en-
# prompt.md § « Traduction des mises à jour de suivi » — laissé à faire à
# la main pour l'instant, voir résumé final).
# ---------------------------------------------------------------------------
def build_social_conclusion(emoji, social_sentence, title, pct, delta):
    verb = verb_for_delta(delta)
    sign = "+" if delta >= 0 else ""
    return f"{emoji} {social_sentence} : « {title} » {verb} à {pct}%, {sign}{delta} points."


def build_feed_item(guid, title, link, pub_date, comments, description, image_url=None, image_length=None):
    enclosure = (
        f'      <enclosure url="{image_url}" length="{image_length}" type="image/png"/>\n'
        if image_url else ""
    )
    return (
        f"    <item>\n"
        f"      <title>{html.escape(title)}</title>\n"
        f"      <link>{link}</link>\n"
        f'      <guid isPermaLink="false">{guid}</guid>\n'
        f"      <pubDate>{pub_date}</pubDate>\n"
        f"      <comments>{html.escape(comments)}</comments>\n"
        f"{enclosure}"
        f"      <description><![CDATA[{description}]]></description>\n"
        f"    </item>\n"
    )


def insert_feed_item(feed_path, item_xml):
    xml_text = feed_path.read_text(encoding="utf-8")
    now = datetime.now(PARIS)
    build_date = now.strftime("%a, %d %b %Y %H:%M:%S %z")
    xml_text = re.sub(r"<lastBuildDate>.*?</lastBuildDate>", f"<lastBuildDate>{build_date}</lastBuildDate>", xml_text, count=1)
    if "<item>" in xml_text:
        xml_text = xml_text.replace("<item>", item_xml.strip() + "\n    <item>", 1)
    else:
        xml_text = xml_text.replace("</channel>", item_xml + "  </channel>", 1)
    feed_path.write_text(xml_text, encoding="utf-8")


def generate_suivi_social_image(topic, conclusion, photo_path, output_path, en=False):
    import subprocess
    template = ROOT / "scripts" / "social" / ("suivi-template-en.html" if en else "suivi-template.html")
    data = {"topic": topic, "conclusion": conclusion}
    data_path = output_path.with_suffix(".data.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    try:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "social" / "generate_suivi_image.py"),
             "--data", str(data_path), "--output", str(output_path),
             "--template", str(template), "--photo", str(photo_path)],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as e:
        raise DetectionError(f"generate_suivi_image.py a échoué : {e.stdout}\n{e.stderr}")
    finally:
        data_path.unlink(missing_ok=True)
    return output_path.stat().st_size


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default=DETECTION_MODEL)
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    today = datetime.now(PARIS).date()
    changed_paths = []

    # Point 1bis — contrôle CSS/HTML sur TOUTES les pages de suivi, avant
    # toute recherche, exception à « un sujet par passage ».
    for f in sorted(SUIVI_DIR.glob("*.html")):
        if f.name == "_gabarit.html":
            continue
        if args.dry_run:
            missing = find_missing_css_classes(f.read_text(encoding="utf-8"))
            if missing:
                print(f"[dry-run] {f.name} : classes CSS manquantes {missing}")
            continue
        if autofix_missing_css(f, GABARIT_PATH.read_text(encoding="utf-8")):
            changed_paths.append(str(f.relative_to(ROOT)))

    md_text = SUJETS_A_SUIVRE.read_text(encoding="utf-8")
    active_suivis = parse_active_suivis(md_text)
    journal = parse_journal(md_text, today)
    active_slugs_titles = {e["title"] for e in active_suivis}
    journal = [j for j in journal if j["title"] not in active_slugs_titles]

    candidates = []
    for e in active_suivis:
        state = read_suivi_state((SUIVI_DIR / f"{e['slug']}.html").read_text(encoding="utf-8"))
        ref_date = state["evo_entries"][-1]["date"]  # texte court, non parsable fiablement -> utiliser origin/version_count comme repère d'âge
        # Repère d'âge fiable : la dernière ligne "Dernière vérification : {date longue} (VN)."
        dv_m = re.search(r"Dernière vérification : ([^()]+) \(V\d+\)\.", e["block"])
        reference_date = parse_french_date(dv_m.group(1)) if dv_m else e["origin_date"]
        prev_pcts = {k: state["evo_entries"][-1][k] for k in KIND_ORDER}
        candidates.append({
            "type": "suivi", "slug": e["slug"], "h1": state["h1"],
            "origin_date": state["origin_date"], "reference_date": reference_date,
            "scenarios": {k: {"pct": prev_pcts[k], "title": state["titles"][k]["title"], "why": ""} for k in KIND_ORDER},
            "titles": state["titles"], "prev_pcts": prev_pcts,
            "version_count": state["version_count"], "prev_label": state["evo_entries"][-1]["label"],
            "origin_title": e["title"],
        })
    for j in journal:
        archive_path = ARCHIVES_DIR / f"{j['date'].isoformat()}.html"
        if not archive_path.exists():
            continue
        h1, stakes, cards = read_edition_scenarios(archive_path.read_text(encoding="utf-8"))
        if len(cards) != 3:
            continue
        candidates.append({
            "type": "journal", "h1": h1, "origin_date": j["date"], "reference_date": j["date"],
            "scenarios": {c["kind"]: c for c in cards}, "stakes": stakes,
        })

    eligible = []
    signalled = []
    total_cost = 0.0
    for cand in candidates:
        age_days = (today - cand["reference_date"]).days
        if age_days <= MIN_REFERENCE_AGE_DAYS:
            continue  # jamais publiable ce passage-ci -> pas la peine de payer une recherche
        if args.dry_run:
            print(f"[dry-run] candidat interrogeable : {cand['h1']} (type={cand['type']}, âge={age_days}j)")
            continue
        try:
            result, usage = search_and_reestimate(cand, args.model, api_key)
        except GenerationError as e:
            print(f"[detection] échec recherche pour {cand['h1']!r} : {e}", file=sys.stderr)
            continue
        total_cost += usage.get("cost") or 0.0
        if result is None:
            continue
        if result.get("closure_signal"):
            signalled.append(("🏁", cand["h1"], result.get("closure_note", "")))
        if result["gap"] >= GAP_THRESHOLD:
            eligible.append((cand, result))
        else:
            signalled.append(("⚠️" if result["gap"] >= 10 else "", cand["h1"], f"écart {result['gap']} points, sous le seuil"))

    if args.dry_run:
        print(f"\n[dry-run] {len(candidates)} candidats, aucun appel OpenRouter effectué.")
        return 0

    if not eligible:
        print("RAS aujourd'hui." if not signalled else "Rien à publier aujourd'hui.")
        for marker, title, note in signalled:
            if marker:
                print(f"{marker} {title} — {note}")
        if changed_paths:
            print(f"\n[detection] correctifs CSS appliqués : {changed_paths}")
        return 0

    winner_cand, winner_result = select_winner(eligible, args.model, api_key)
    pct = winner_result["percentages"]
    conclusion_kind = winner_result["conclusion_kind"]
    sources = winner_result.get("sources") or []

    if winner_cand["type"] == "suivi":
        slug = winner_cand["slug"]
        suivi_path = SUIVI_DIR / f"{slug}.html"
        html_text = suivi_path.read_text(encoding="utf-8")
        version_n = winner_cand["version_count"]
        date_maj = fmt_date_long(today)
        block = build_update_block(
            version_n, date_maj, winner_cand["titles"], winner_cand["prev_pcts"], pct,
            winner_result["reasons"], winner_result["fact_paragraph"], conclusion_kind,
            winner_result["conclusion_text"], sources, winner_cand["prev_label"],
        )
        new_evo = {"label": f"V{version_n}", "date": fmt_date_short(today), **pct}
        new_html = insert_update_into_suivi(html_text, block, new_evo)
        suivi_path.write_text(new_html, encoding="utf-8")
        changed_paths.append(str(suivi_path.relative_to(ROOT)))

        md_text = SUJETS_A_SUIVRE.read_text(encoding="utf-8")
        md_text = update_active_suivi_entry(
            md_text, slug, winner_cand["origin_title"], fmt_date_long(winner_cand["origin_date"]),
            f"V{version_n}", today, None,
        )
        SUJETS_A_SUIVRE.write_text(md_text, encoding="utf-8")
        changed_paths.append(str(SUJETS_A_SUIVRE.relative_to(ROOT)))

        title_for_titles = winner_cand["titles"][conclusion_kind]["title"]
        emoji = winner_cand["titles"][conclusion_kind]["emoji"]
        link = f"https://lesscenarios.fr/suivi/{slug}.html#version-content-v{version_n}"
        delta = pct[conclusion_kind] - winner_cand["prev_pcts"][conclusion_kind]
        social = build_social_conclusion(emoji, winner_result["social_sentence"], title_for_titles, pct[conclusion_kind], delta)

        other_clauses = []
        for kind in KIND_ORDER:
            if kind == conclusion_kind:
                continue
            d = pct[kind] - winner_cand["prev_pcts"][kind]
            other_clauses.append(
                f"{winner_result['short_labels'][kind]} {verb_for_delta(d)} de {winner_cand['prev_pcts'][kind]}% à {pct[kind]}%"
            )
        description = (
            f"{social} — ce scénario {verb_for_delta(delta)} de {winner_cand['prev_pcts'][conclusion_kind]}% à "
            f"{pct[conclusion_kind]}%, tandis que " + " et ".join(other_clauses) + ".<br><br>"
            f"{winner_result['fact_paragraph']}<br><br>"
            f'Voir la mise à jour complète, scénario par scénario 👉 <a href="{link}">lesscenarios.fr/suivi/{slug}.html</a>'
        )
        pub_date = datetime.now(PARIS).strftime("%a, %d %b %Y %H:%M:%S %z")
        item = build_feed_item(
            f"scenario-suivi-{slug}-v{version_n}", f"{winner_cand['h1']}, un scénario a bougé",
            link, pub_date, social, description,
        )

        image_url = None
        photo_for_social = TOPIC_IMAGES_DIR / f"suivi-{slug}.jpg"
        if photo_for_social.exists():
            out_png = ROOT / "assets" / "social" / "suivi" / f"{slug}-v{version_n}.png"
            length = generate_suivi_social_image(winner_cand["h1"], social, photo_for_social, out_png)
            image_url = f"https://lesscenarios.fr/assets/social/suivi/{slug}-v{version_n}.png"
            item = build_feed_item(
                f"scenario-suivi-{slug}-v{version_n}", f"{winner_cand['h1']}, un scénario a bougé",
                link, pub_date, social, description, image_url, length,
            )
            changed_paths.append(str(out_png.relative_to(ROOT)))
        insert_feed_item(FEED_SUIVI, item)
        changed_paths.append(str(FEED_SUIVI.relative_to(ROOT)))

        print(f"Sujet publié : {winner_cand['h1']} — {slug} V{version_n}")
        print(f"  {social}")

    else:
        slug = (winner_result.get("slug") or "").strip() or slugify_fallback(winner_cand["h1"])
        if (SUIVI_DIR / f"{slug}.html").exists():
            slug = f"{slug}-2"
        origin_iso = winner_cand["origin_date"].isoformat()
        photo_meta = setup_topic_image(slug, origin_iso)
        v0_scenarios = winner_result["v0_scenarios"]

        out_path = create_new_suivi_page(
            slug, winner_cand["h1"], winner_cand["origin_date"], origin_iso,
            winner_result["v0_intro"], v0_scenarios, winner_cand["scenarios"],
            winner_result["v0_conclusion_kind"], winner_result["v0_conclusion_text"],
            f"Point de départ — {winner_cand['h1']}", photo_meta,
        )
        v0_pcts = {k: winner_cand["scenarios"][k]["pct"] for k in KIND_ORDER}
        titles_with_emoji = {k: {"emoji": v0_scenarios[k]["emoji"], "title": winner_cand["scenarios"][k]["title"]} for k in KIND_ORDER}
        block = build_update_block(
            1, fmt_date_long(today), titles_with_emoji, v0_pcts, pct,
            winner_result["reasons"], winner_result["fact_paragraph"], conclusion_kind,
            winner_result["conclusion_text"], sources, "V0",
        )
        html_text = out_path.read_text(encoding="utf-8")
        new_evo = {"label": "V1", "date": fmt_date_short(today), **pct}
        html_text = insert_update_into_suivi(html_text, block, new_evo)
        out_path.write_text(html_text, encoding="utf-8")
        changed_paths.append(str(out_path.relative_to(ROOT)))
        if photo_meta:
            changed_paths.append(str((TOPIC_IMAGES_DIR / f"suivi-{slug}.jpg").relative_to(ROOT)))
            changed_paths.append(str((TOPIC_IMAGES_DIR / f"suivi-{slug}-wide.jpg").relative_to(ROOT)))

        md_text = SUJETS_A_SUIVRE.read_text(encoding="utf-8")
        entry_block = (
            f"- **{winner_cand['h1']}** (édition du {fmt_date_long(winner_cand['origin_date'])})\n"
            f"  Suivi existant : `suivi/{slug}.html` (V0 + V1 au {fmt_date_long(today)}, publiée "
            f"automatiquement par la routine de détection OpenRouter — écart de "
            f"{pct[conclusion_kind] - v0_pcts[conclusion_kind]:+d} points sur le scénario {conclusion_kind}).\n"
            f"  {winner_result['fact_paragraph']}\n"
            f"  Dernière vérification : {fmt_date_long(today)} (V1).\n"
        )
        md_text = add_active_suivi_entry(md_text, entry_block)
        md_text = mark_journal_entry_has_suivi(md_text, origin_iso)
        SUJETS_A_SUIVRE.write_text(md_text, encoding="utf-8")
        changed_paths.append(str(SUJETS_A_SUIVRE.relative_to(ROOT)))

        title_for_titles = titles_with_emoji[conclusion_kind]["title"]
        emoji = titles_with_emoji[conclusion_kind]["emoji"]
        link = f"https://lesscenarios.fr/suivi/{slug}.html#version-content-v1"
        delta = pct[conclusion_kind] - v0_pcts[conclusion_kind]
        social = build_social_conclusion(emoji, winner_result["social_sentence"], title_for_titles, pct[conclusion_kind], delta)
        other_clauses = []
        for kind in KIND_ORDER:
            if kind == conclusion_kind:
                continue
            d = pct[kind] - v0_pcts[kind]
            other_clauses.append(f"{winner_result['short_labels'][kind]} {verb_for_delta(d)} de {v0_pcts[kind]}% à {pct[kind]}%")
        description = (
            f"{social} — ce scénario {verb_for_delta(delta)} de {v0_pcts[conclusion_kind]}% à {pct[conclusion_kind]}%, "
            f"tandis que " + " et ".join(other_clauses) + ".<br><br>"
            f"{winner_result['fact_paragraph']}<br><br>"
            f'Voir la mise à jour complète, scénario par scénario 👉 <a href="{link}">lesscenarios.fr/suivi/{slug}.html</a>'
        )
        pub_date = datetime.now(PARIS).strftime("%a, %d %b %Y %H:%M:%S %z")
        image_url = None
        if photo_meta:
            out_png = ROOT / "assets" / "social" / "suivi" / f"{slug}-v1.png"
            length = generate_suivi_social_image(winner_cand["h1"], social, photo_meta["jpg_for_social"], out_png)
            image_url = f"https://lesscenarios.fr/assets/social/suivi/{slug}-v1.png"
            changed_paths.append(str(out_png.relative_to(ROOT)))
        item = build_feed_item(
            f"scenario-suivi-{slug}-v1", f"{winner_cand['h1']}, un scénario a bougé",
            link, pub_date, social, description,
            image_url, length if image_url else None,
        )
        insert_feed_item(FEED_SUIVI, item)
        changed_paths.append(str(FEED_SUIVI.relative_to(ROOT)))

        print(f"Nouvelle page de suivi créée : {winner_cand['h1']} — suivi/{slug}.html")
        print(f"  {social}")
        print("  ATTENTION : miroir EN (en/feed-suivi.xml) non généré par ce script — "
              "voir docs/routine-en-prompt.md § « Traduction des mises à jour de suivi », à faire à la main ou en session Claude Code.")

    print(f"\nAutres sujets signalés (non retenus ce passage-ci) :")
    for marker, title, note in signalled:
        if marker:
            print(f"{marker} {title} — {note}")
    print(f"\nCoût OpenRouter total ≈ {total_cost:.4f} $ ({len(candidates)} candidats évalués).")
    print(f"Fichiers modifiés : {changed_paths}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
