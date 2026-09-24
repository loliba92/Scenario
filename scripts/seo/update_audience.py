#!/usr/bin/env python3
"""
Met à jour les données d'audience de `le-projet.html` (section
`#audience`) et de `dashboard.html` (KPI, graphiques, agenda éditorial,
autonomie par registre) à partir de l'API GoatCounter — remplace la
routine Claude Code hebdomadaire "Scénario — Audience"
(docs/routine-audience-prompt.md), tâche purement mécanique (appel API +
arithmétique + remplissage de gabarit, aucun jugement éditorial réel
requis) qui n'a jamais eu besoin d'une session Claude Code. Même
justification et même schéma que `scripts/seo/update_reads_json.py`
(déplacé le 3 septembre 2026 pour la même raison) — cette fois pour
l'ensemble du dashboard plutôt que la seule colonne "Lectures".

Historique (12 septembre 2026) : à la demande de l'utilisateur, le
tableau top/flop, "Lectures par domaine" et "Suivis actifs" ont été
retirés de `dashboard.html` avant cette bascule (périmètre réduit aux
KPI/graphiques GoatCounter + agenda éditorial + autonomie par registre)
— voir le commit qui a retiré ces blocs. Une fois ce script validé en
conditions réelles, la routine Claude Code "Scénario — Audience" doit
être supprimée (son trigger Claude Code Remote), pour éviter un
double-écrasement des mêmes fichiers.

Le token GoatCounter (lecture seule) est lu depuis GOATCOUNTER_TOKEN —
le même secret GitHub Actions que celui déjà utilisé par
update_reads_json.py/.github/workflows/reads.yml, aucun nouveau secret
à créer.

Portée volontairement pas 100% mécanique sur un seul point : le titre
court de chaque carte "Agenda de la semaine" est une troncature
heuristique de l'accroche de `sujets-prioritaires.md` (coupe à la
première "?"/". " dans une fenêtre raisonnable, sinon troncature dure
avec "…") plutôt qu'une vraie reformulation éditoriale — acceptable ici
car ce dashboard est un usage strictement interne (voir
docs/routine-audience-prompt.md), pas un texte publié aux lecteurs.

Usage (en local, pour tester) :
    GOATCOUNTER_TOKEN=xxx python3 scripts/seo/update_audience.py [--dry-run]
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_reads_json import PATH_RE, START_DATE, fetch_hits  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LE_PROJET = ROOT / "le-projet.html"
DASHBOARD = ROOT / "dashboard.html"
SUJETS_PRIORITAIRES = ROOT / "sujets-prioritaires.md"
ARCHIVES_DIR = ROOT / "archives"
OPENROUTER_COST_HISTORY = ROOT / "assets" / "data" / "openrouter-cost.json"

PARIS = ZoneInfo("Europe/Paris")

MONTHS_SHORT = ["janv.", "févr.", "mars", "avr.", "mai", "juin",
                "juil.", "août", "sept.", "oct.", "nov.", "déc."]
MONTHS_FULL = ["janvier", "février", "mars", "avril", "mai", "juin",
               "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
DAYS_SHORT = ["Lun.", "Mar.", "Mer.", "Jeu.", "Ven.", "Sam.", "Dim."]

# Les 7 registres hebdomadaires, dans l'ordre du calendrier (lundi->dimanche)
# — nom de section dans sujets-prioritaires.md, nom court affiché sur les
# cartes/tableaux du dashboard. Exclut volontairement "🔥 Priorité absolue"
# (file d'urgence opportuniste, pas un registre consommé une fois/semaine
# — voir docs/routine-audience-prompt.md).
REGISTRES = [
    ("Géopolitique — lundi", "Géopolitique"),
    ("Mardi — carte blanche aux lecteurs (tous registres au choix)", "Carte blanche"),
    ("Actualité & politique française — mercredi", "Actu. française"),
    ("Économie & finance mondiale — jeudi", "Économie &amp; finance"),
    ("Sciences — vendredi (climat & écologie, espace, IA, médecine, énergie…)", "Sciences"),
    ("Culture — samedi", "Culture"),
    ("Sport — dimanche", "Sport"),
]


OPENROUTER_CREDITS_URL = "https://openrouter.ai/api/v1/credits"
OPENROUTER_KEY_URL = "https://openrouter.ai/api/v1/key"


def _fetch_openrouter_json(url, api_key):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def fetch_openrouter_cost(api_key):
    """Coûts OpenRouter (tout le compte) — demandé le 17 septembre 2026 :
    « dans le dashboard il faudrait ajouter les coûts de openrouter ».
    Jamais bloquant (None si absent/en échec — ce n'est qu'un KPI de
    plus, pas une donnée dont dépend le reste du dashboard). Deux
    endpoints :
    - /credits : solde total (total_usage/total_credits), pour le coût
      cumulé et le solde restant.
    - /key : usage_daily/usage_weekly/usage_monthly déjà calculés côté
      OpenRouter — inspecté en conditions réelles le 17 septembre 2026
      (voir logs du run qui a suivi le diagnostic) avant de construire
      quoi que ce soit dessus. Aucun des deux n'expose de nombre de
      requêtes, seulement des montants en dollars — un KPI "requêtes/jour"
      demanderait un comptage local par script, hors de portée ici."""
    if not api_key:
        return None
    try:
        credits_payload = _fetch_openrouter_json(OPENROUTER_CREDITS_URL, api_key)
        key_payload = _fetch_openrouter_json(OPENROUTER_KEY_URL, api_key)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
        print(f"[audience] avertissement : coût OpenRouter indisponible ({e}).", file=sys.stderr)
        return None
    credits_data = credits_payload.get("data") or {}
    key_data = key_payload.get("data") or {}
    if "total_usage" not in credits_data or "total_credits" not in credits_data:
        print(f"[audience] avertissement : réponse OpenRouter /credits inattendue : {credits_payload!r}", file=sys.stderr)
        return None
    return {
        "total_usage": credits_data["total_usage"],
        "total_credits": credits_data["total_credits"],
        "usage_daily": key_data.get("usage_daily"),
        "usage_weekly": key_data.get("usage_weekly"),
        "usage_monthly": key_data.get("usage_monthly"),
    }


def update_openrouter_history(today_iso, total_usage):
    """Historique minimal (juste total_usage par date). Le seul chiffre
    qu'aucun endpoint OpenRouter ne donne directement est "hier"
    (usage_daily de /key ne couvre qu'aujourd'hui) — un snapshot
    quotidien suffit à le dériver. Une entrée par date (écrase si déjà
    présente aujourd'hui — plusieurs runs le même jour ne dupliquent
    jamais), jamais réordonné, jamais une entrée passée modifiée."""
    if OPENROUTER_COST_HISTORY.exists():
        history = json.loads(OPENROUTER_COST_HISTORY.read_text(encoding="utf-8"))
    else:
        history = []
    history = [h for h in history if h["date"] != today_iso]
    history.append({"date": today_iso, "total_usage": total_usage})
    history.sort(key=lambda h: h["date"])
    OPENROUTER_COST_HISTORY.parent.mkdir(parents=True, exist_ok=True)
    OPENROUTER_COST_HISTORY.write_text(
        json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    return history


def compute_cost_yesterday(history):
    """Coût de la veille = écart entre les deux derniers relevés
    disponibles — jamais supposé être exactement le jour précédent si un
    run a été raté (cron en échec) : c'est le coût depuis le relevé
    précédent DISPONIBLE, quelle que soit la date exacte."""
    if len(history) < 2:
        return None
    dates_sorted = sorted(h["date"] for h in history)
    by_date = {h["date"]: h["total_usage"] for h in history}
    d_now, d_prev = dates_sorted[-1], dates_sorted[-2]
    return {"value": by_date[d_now] - by_date[d_prev], "date": d_now, "since": d_prev}


def compute_cost_today(history, today_iso):
    """Coût d'aujourd'hui = écart entre aujourd'hui et hier dans l'historique.
    Même logique que compute_cost_yesterday pour assurer la cohérence :
    jamais usage_daily de l'API qui grossit au fil de la journée et reste
    incomplet jusqu'à minuit. Utilise l'historique qui contient les snapshots
    quotidiens, même si aujourd'hui n'est pas encore clos — c'est la valeur
    la plus fiable à ce stade.

    Bug corrigé le 24 septembre 2026 (retour utilisateur : "Aujourd'hui"
    affichait 1,51 $ alors que le coût réel du jour était 0.03 $, et 1,51
    était en fait le coût d'hier) : l'ancienne version utilisait usage_daily
    de l'API OpenRouter, qui change en temps réel et n'est jamais comparable
    à "hier" (journée close) ou aux autres jours. Passer à l'historique
    pour les deux rend la comparaison cohérente."""
    past = sorted((h for h in history if h["date"] <= today_iso), key=lambda h: h["date"])
    if len(past) < 2:
        return None
    # past[-1] est aujourd'hui (avec son total_usage courant),
    # past[-2] est hier — la différence est le coût d'aujourd'hui.
    return {"value": past[-1]["total_usage"] - past[-2]["total_usage"], "date": past[-1]["date"], "since": past[-2]["date"]}



def build_sparkline_svg(values, width=84, height=26):
    """Sparkline de tendance pour une carte KPI — contrat "stat tile" du
    skill dataviz : trait dans la teinte discrète (paper-dim), seul le
    dernier point (période courante) est accentué (gold). Jamais d'axe ni
    de grille — une carte KPI n'est pas un graphique, juste une forme.
    Chaîne vide si moins de 2 points (rien à tracer)."""
    if len(values) < 2:
        return ""
    vmin, vmax = min(values), max(values)
    span = (vmax - vmin) or 1
    n = len(values)
    pad = 3

    def x(i):
        return pad + (i / (n - 1)) * (width - 2 * pad)

    def y(v):
        return height - pad - ((v - vmin) / span) * (height - 2 * pad)

    pts = [(x(i), y(v)) for i, v in enumerate(values)]
    path = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    last_x, last_y = pts[-1]
    return (
        f'<svg class="kpi-spark" viewBox="0 0 {width} {height}" preserveAspectRatio="none" aria-hidden="true">'
        f'<path d="{path}" fill="none" stroke="var(--paper-dim)" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="2.4" fill="var(--gold)"/>'
        f"</svg>"
    )


def fmt_long(d):
    return f"{d.day} {MONTHS_FULL[d.month - 1]} {d.year}"


def fmt_card_day(d):
    return f"{DAYS_SHORT[d.weekday()]} {d.day} {MONTHS_SHORT[d.month - 1]}"


def fmt_range(start_d, end_d):
    """"du {début} au {fin}" — l'année n'est jamais répétée sur la
    première date d'une plage si les deux tombent la même année (même
    convention que l'original, ex. "du 30 juillet au 7 septembre 2026")."""
    if start_d.year == end_d.year:
        return f"{start_d.day} {MONTHS_FULL[start_d.month - 1]}", fmt_long(end_d)
    return fmt_long(start_d), fmt_long(end_d)


# ---------------------------------------------------------------------------
# GoatCounter : agrégation par jour calendaire (tous chemins /archives/
# confondus) — distinct de update_reads_json.py, qui agrège par édition
# (total à vie de CE chemin), pas par jour toutes éditions confondues.
# Voir docs/routine-audience-prompt.md, étape 2, pour la règle exacte.
# ---------------------------------------------------------------------------
def aggregate_per_day(payload):
    per_day = defaultdict(int)
    for hit in payload.get("hits", []):
        if not PATH_RE.match(hit.get("path", "")):
            continue
        for s in hit.get("stats", []):
            day = s.get("day")
            if day:
                per_day[day[:10]] += s.get("daily", 0)
    return dict(per_day)


def build_cumulative(per_day, start_iso, end_date):
    start = date.fromisoformat(start_iso)
    series = []
    cum = 0
    d = start
    while d <= end_date:
        cum += per_day.get(d.isoformat(), 0)
        series.append([d.isoformat(), cum])
        d += timedelta(days=1)
    return series


def pick_x_labels(series):
    """Première, dernière, 3 intermédiaires régulièrement espacées — jamais
    toutes les dates (voir docs/routine-prompt.md, règle du graphique en
    escalier, même principe appliqué ici)."""
    n = len(series)
    if n <= 5:
        return [d[0] for d in series]
    idxs = sorted({0, n - 1, round((n - 1) / 4), round((n - 1) / 2), round(3 * (n - 1) / 4)})
    return [series[i][0] for i in idxs]


def round_up_yaxis(value):
    """Palier rond immédiatement au-dessus (ex. 507 -> 550, 181 -> 200)."""
    if value <= 0:
        return 50
    step = 50 if value < 1000 else 100
    return ((value // step) + 1) * step


def build_weekly(per_day, start_iso, end_date):
    """Buckets calendaires lundi->dimanche — voir docs/routine-audience-
    prompt.md, étape 3bis, pour la convention exacte (corrigée le 3
    septembre 2026). Renvoie une liste de [lundi_iso, total, is_partial]."""
    start = date.fromisoformat(start_iso)
    monday = start - timedelta(days=start.weekday())
    weeks = []
    m = monday
    while m <= end_date:
        week_end = m + timedelta(days=6)
        total = 0
        d = m
        while d <= min(week_end, end_date):
            if d >= start:
                total += per_day.get(d.isoformat(), 0)
            d += timedelta(days=1)
        is_partial = (m < start) or (week_end > end_date)
        weeks.append([m.isoformat(), total, is_partial])
        m += timedelta(days=7)
    return weeks


# ---------------------------------------------------------------------------
# KPI : lectures cumulées, 7j/30j glissants, cadence de publication,
# moyenne par édition — voir docs/routine-audience-prompt.md, étape 3bis.
# ---------------------------------------------------------------------------
def sum_window(per_day, end_date, days, start_floor):
    total = 0
    d = end_date - timedelta(days=days - 1)
    while d <= end_date:
        if d >= start_floor:
            total += per_day.get(d.isoformat(), 0)
        d += timedelta(days=1)
    return total


def compute_cadence(archive_dates, reference_date):
    """Jours consécutifs sans interruption dans archives/*.html, en
    repartant de la dernière rupture calendaire — jamais une date de
    départ figée (voir docs/routine-audience-prompt.md).

    Ancré sur la DERNIÈRE ÉDITION CONNUE, pas sur `reference_date`
    (aujourd'hui) : ce script tourne désormais chaque jour, parfois avant
    que l'édition du jour ne soit publiée — ça ne doit jamais compter
    comme une rupture. En revanche, un vrai trou de plusieurs jours entre
    la dernière édition et aujourd'hui (site réellement arrêté) doit
    apparaître comme une rupture, jamais comme une cadence qui continue
    silencieusement de grossir. Renvoie (cadence_days, depuis, en_retard)."""
    if not archive_dates:
        return 0, reference_date, False
    dates_set = set(archive_dates)
    last_edition = max(archive_dates)
    is_stale = (reference_date - last_edition).days > 1
    cursor = last_edition
    while (cursor - timedelta(days=1)) in dates_set:
        cursor -= timedelta(days=1)
    cadence_days = (last_edition - cursor).days + 1
    return cadence_days, cursor, is_stale


def get_archive_dates():
    dates = []
    for f in ARCHIVES_DIR.glob("????-??-??.html"):
        try:
            dates.append(date.fromisoformat(f.stem))
        except ValueError:
            continue
    return sorted(dates)


def compute_kpis(per_day, cumulative, end_date, archive_dates):
    start = date.fromisoformat(START_DATE)
    total = cumulative[-1][1] if cumulative else 0

    last7 = sum_window(per_day, end_date, 7, start)
    prev7 = sum_window(per_day, end_date - timedelta(days=7), 7, start)
    delta7 = last7 - prev7

    days_tracked = (end_date - start).days + 1
    last30 = sum_window(per_day, end_date, 30, start)
    share30 = round(100 * last30 / total) if total else 0
    has_60d = days_tracked >= 60
    prev30 = sum_window(per_day, end_date - timedelta(days=30), 30, start) if has_60d else None

    cadence_days, cadence_since, cadence_stale = compute_cadence(archive_dates, end_date)

    tracked_editions = [d for d in archive_dates if d >= start]
    avg_per_edition = round(total / len(tracked_editions), 1) if tracked_editions else 0

    # Moyenne/édition sur des fenêtres plus courtes (demandé le 17
    # septembre 2026 : « il faut 13,8 all year, mais ajoute sur la
    # semaine, sur le dernier mois ») — même fenêtre inclusive que
    # sum_window (end_date - (jours-1) à end_date), None tant qu'aucune
    # édition n'est tombée dans la fenêtre (jamais une division par zéro
    # déguisée en 0).
    editions_7d = [d for d in archive_dates if end_date - timedelta(days=6) <= d <= end_date]
    avg_per_edition_7d = round(last7 / len(editions_7d), 1) if editions_7d else None
    editions_30d = [d for d in archive_dates if end_date - timedelta(days=29) <= d <= end_date]
    avg_per_edition_30d = round(last30 / len(editions_30d), 1) if editions_30d else None

    return {
        "total": total,
        "last7": last7,
        "delta7": delta7,
        "days_tracked": days_tracked,
        "last30": last30,
        "share30": share30,
        "prev30": prev30,
        "cadence_days": cadence_days,
        "cadence_since": cadence_since,
        "cadence_stale": cadence_stale,
        "tracked_editions": len(tracked_editions),
        "avg_per_edition": avg_per_edition,
        "avg_per_edition_7d": avg_per_edition_7d,
        "avg_per_edition_30d": avg_per_edition_30d,
    }


# ---------------------------------------------------------------------------
# sujets-prioritaires.md : agenda (semaine à venir + semaine d'après) et
# autonomie par registre (nombre de sujets non cochés). Reference_date doit
# toujours être un lundi (voir docs/routine-audience-prompt.md, "toujours
# afficher le prochain lundi au prochain dimanche").
# ---------------------------------------------------------------------------
def parse_section(md_text, heading):
    pattern = re.compile(
        r"^## " + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)",
        re.M | re.S,
    )
    m = pattern.search(md_text)
    return m.group(1) if m else ""


def unchecked_items(section_text):
    items = []
    for line in section_text.splitlines():
        m = re.match(r"^- \[ \] (.+)$", line.strip())
        if m:
            items.append(m.group(1).strip())
    return items


def strip_trailing_tag(full_text):
    """Retire le tag [entre crochets] final d'une entrée de
    sujets-prioritaires.md (ex. "... [géopolitique]") — catégorisation
    interne, jamais affichée telle quelle sur le dashboard."""
    return re.sub(r"\s*\[[^\]]+\]\s*$", "", full_text).strip()


def short_title(full_text, max_len=70):
    """Troncature heuristique pour une carte d'agenda (usage interne
    seulement, voir docstring du module) : coupe au premier "?" ou ". "
    trouvé dans une fenêtre raisonnable, sinon troncature dure sur un
    mot entier avec "…"."""
    text = strip_trailing_tag(full_text)
    window = text[: max_len + 20]
    qmark = window.find("?")
    if 0 < qmark <= max_len + 15:
        return html.escape(text[: qmark + 1], quote=False)
    dot = window.find(". ")
    if 0 < dot <= max_len:
        return html.escape(text[: dot + 1], quote=False)
    if len(text) <= max_len:
        return html.escape(text, quote=False)
    cut = text[:max_len].rsplit(" ", 1)[0].rstrip(",;:.")
    return html.escape(f"{cut}…", quote=False)


def build_agenda(md_text, next_monday):
    cards = []
    later = []
    priority_line = None

    priority_section = parse_section(md_text, "🔥 Priorité absolue (n'importe quel jour, avant tout le reste)")
    priority_pending = unchecked_items(priority_section)
    if priority_pending:
        priority_line = f"🔥 Priorité absolue : {short_title(priority_pending[0], max_len=90)}"
    else:
        priority_line = "🔥 Priorité absolue : aucun sujet en file d'urgence actuellement — la routine suit l'ordre normal des registres ci-dessus."

    for i, (heading, label) in enumerate(REGISTRES):
        section = parse_section(md_text, heading)
        pending = unchecked_items(section)
        day = next_monday + timedelta(days=i)
        if pending:
            cards.append({"day": fmt_card_day(day), "registre": label, "topic": short_title(pending[0])})
        else:
            cards.append({"day": fmt_card_day(day), "registre": label, "topic": "(section vide — auto-sélection le jour même)"})
        if len(pending) >= 2:
            later.append({"label": label, "text": html.escape(strip_trailing_tag(pending[1]), quote=False), "empty": False})
        else:
            later.append({"label": label, "text": "rien en réserve après le sujet de la semaine — dépend des prochains ajouts", "empty": True})

    return cards, later, priority_line


def build_autonomy_table(md_text):
    rows = []
    for heading, label in REGISTRES:
        section = parse_section(md_text, heading)
        n = len(unchecked_items(section))
        if n == 0:
            text, color = "épuisée", "var(--degrade)"
        elif n == 1:
            text, color = "⚠️ épuisée la semaine prochaine", "var(--degrade)"
        elif n <= 4:
            text, color = f"⚠️ ~{n} semaines", "var(--degrade)"
        elif n <= 10:
            text, color = f"~{n} semaines", "var(--stable)"
        else:
            text, color = "confortable", "var(--favorable)"
        rows.append({"label": label, "n": n, "text": text, "color": color, "degrade": n <= 4})
    rows.sort(key=lambda r: r["n"])
    return rows


# ---------------------------------------------------------------------------
# Écriture des fichiers HTML.
# ---------------------------------------------------------------------------
def replace_js_array(script_text, var_name, new_literal):
    pattern = re.compile(
        r"(var\s+" + re.escape(var_name) + r"\s*=\s*)(\[.*?\]);",
        re.S,
    )
    if not pattern.search(script_text):
        raise RuntimeError(f"variable JS introuvable : {var_name}")
    return pattern.sub(lambda m: m.group(1) + new_literal + ";", script_text, count=1)


def js_array_literal(series, indent="      ", per_line=3):
    """Formaté 3 par ligne comme l'original (voir le <script> #audience-svg
    déjà en place) — un diff git lisible plutôt qu'un seul très long bloc
    sur une ligne, même contenu."""
    items = [f"['{d}', {v}]" for d, v in series]
    lines = [", ".join(items[i:i + per_line]) + ("," if i + per_line < len(items) else "")
             for i in range(0, len(items), per_line)]
    body = ("\n" + indent).join(lines)
    return f"[\n{indent}{body}\n{indent[:-2]}]"


def update_le_projet(cumulative, x_labels, y_max, kpis, end_date):
    html = LE_PROJET.read_text(encoding="utf-8")

    intro_re = re.compile(
        r"(<strong>)[\d\xa0.,]+( lectures d'éditions cumulées</strong> au )[^,]+(,)",
    )
    html, n = intro_re.subn(
        rf"\g<1>{kpis['total']}\g<2>{fmt_long(end_date)}\g<3>", html, count=1,
    )
    if n != 1:
        raise RuntimeError("le-projet.html : phrase d'intro #audience introuvable")

    range_start, range_end = fmt_range(date.fromisoformat(cumulative[0][0]), end_date)
    lead_re = re.compile(r'(<p class="dc-chart-lead">Nombre total de lectures d\'éditions depuis le lancement, du ).*?( au ).*?(\.</p>)')
    html, n = lead_re.subn(
        rf"\g<1>{range_start}\g<2>{range_end}\g<3>", html, count=1,
    )
    if n != 1:
        raise RuntimeError("le-projet.html : dc-chart-lead introuvable")

    # Texte figé depuis le passage de la routine Audience à un rythme
    # quotidien (12 septembre 2026) — jamais corrigé ici avant ce jour-là,
    # contrairement à dashboard.html (voir update_dashboard() plus bas) :
    # le-projet.html continuait à dire "chaque semaine" alors que le
    # GitHub Action tourne chaque jour. Idempotent (.count() == 0 une fois
    # déjà corrigé, pas une erreur) pour que les prochains passages n'y
    # touchent plus une fois la phrase mise à "chaque jour".
    STALE_INTRO = (
        "mesurées sans cookie ni profilage (<a href=\"https://www.goatcounter.com/\" "
        "target=\"_blank\" rel=\"noopener noreferrer\">GoatCounter</a>), mises à jour chaque semaine."
    )
    if html.count(STALE_INTRO) > 1:
        raise RuntimeError("le-projet.html : phrase 'mises à jour chaque semaine' trouvée en double")
    html = html.replace(STALE_INTRO, STALE_INTRO.replace("chaque semaine", "chaque jour"))

    STALE_CAPTION = "mis à jour chaque semaine par une routine automatisée."
    if html.count(STALE_CAPTION) > 1:
        raise RuntimeError("le-projet.html : phrase 'mis à jour chaque semaine par une routine automatisée' trouvée en double")
    html = html.replace(STALE_CAPTION, "mis à jour chaque jour par un GitHub Action.")

    aria_re = re.compile(r'(aria-label="Courbe de croissance des lectures cumulées d\'éditions, de )\d+( le ).*?( à )\d+( le ).*?(")')
    first_date = date.fromisoformat(cumulative[0][0])
    html, n = aria_re.subn(
        rf"\g<1>{cumulative[0][1]}\g<2>{fmt_long(first_date)}\g<3>{kpis['total']}\g<4>{fmt_long(end_date)}\g<5>",
        html, count=1,
    )
    if n != 1:
        raise RuntimeError("le-projet.html : aria-label #audience-svg introuvable")

    script_m = re.search(r"(<script>\s*\n\s*// Lectures cumulées.*?)(</script>)", html, re.S)
    if not script_m:
        raise RuntimeError("le-projet.html : bloc <script> #audience introuvable")
    script_text = script_m.group(1)
    script_text = replace_js_array(script_text, "data", js_array_literal(cumulative))
    labels_literal = "[" + ", ".join(f"'{d}'" for d in x_labels) + "]"
    script_text = replace_js_array(script_text, "xLabels", labels_literal)
    script_text = re.sub(
        r"var yMax = \d+;(?:[^\n]*)",
        f"var yMax = {y_max}; // palier rond au-dessus du dernier cumul ({kpis['total']})",
        script_text, count=1,
    )
    html = html[: script_m.start(1)] + script_text + html[script_m.end(1):]

    LE_PROJET.write_text(html, encoding="utf-8")


def update_dashboard(cumulative, weekly, kpis, end_date, agenda_cards, agenda_later, priority_line, autonomy_rows, current_monday, openrouter=None, cost_yesterday=None, cost_today=None):
    html = DASHBOARD.read_text(encoding="utf-8")

    html = re.sub(
        r'(<p class="dash-meta">Données au ).*?( — mesure d\'audience GoatCounter, mise à jour ).*?(\.</p>)',
        rf"\g<1>{fmt_long(end_date)}\g<2>chaque jour par un GitHub Action\g<3>",
        html, count=1,
    )

    html = re.sub(
        r"(Prochain sujet en tête de chaque registre dans <code>sujets-prioritaires\.md</code>, à date du )[^.]+(\.)",
        rf"\g<1>{fmt_long(end_date)}\g<2>", html, count=1,
    )
    html = re.sub(
        r"(Nombre de sujets en attente \(non cochés\) par section de <code>sujets-prioritaires\.md</code>, à date du )[^.]+(\.)",
        rf"\g<1>{fmt_long(end_date)}\g<2>", html, count=1,
    )
    html = html.replace(
        "Régénéré chaque semaine par la routine « Scénario — Audience », comme le reste du dashboard.",
        "Régénéré chaque jour par un GitHub Action, comme le reste du dashboard.",
    )
    later_start = current_monday + timedelta(days=7)
    later_end = later_start + timedelta(days=6)
    later_range = (
        f"{later_start.day}–{later_end.day} {MONTHS_SHORT[later_end.month - 1]}"
        if later_start.month == later_end.month
        else f"{later_start.day} {MONTHS_SHORT[later_start.month - 1]}–{later_end.day} {MONTHS_SHORT[later_end.month - 1]}"
    )
    html = re.sub(
        r"(<strong>Semaine d'après \().*?(\)</strong>)",
        rf"\g<1>{later_range}\g<2>", html, count=1,
    )

    kpi_values = {
        "cumul": (str(kpis["total"]), f"depuis le {fmt_long(date.fromisoformat(START_DATE))}"),
        "sub_class": "is-up" if kpis["delta7"] > 0 else ("is-down" if kpis["delta7"] < 0 else ""),
    }
    delta_sign = "↑ +" if kpis["delta7"] > 0 else ("↓ " if kpis["delta7"] < 0 else "→ ")
    delta_text = f"{delta_sign}{kpis['delta7']} vs les 7 jours précédents ({kpis['last7'] - kpis['delta7']})"

    if kpis["prev30"] is not None:
        d30 = kpis["last30"] - kpis["prev30"]
        sign30 = "↑ +" if d30 > 0 else ("↓ " if d30 < 0 else "→ ")
        sub30 = f"≈ {kpis['share30']} % des lectures totales — {sign30}{d30} vs les 30 jours précédents ({kpis['prev30']})"
    else:
        sub30 = (f"≈ {kpis['share30']} % des lectures totales — comparaison au 30j précédents pas encore "
                 f"possible ({kpis['days_tracked']} jours d'historique, il en faut 60)")

    replacements = [
        (r'(<p class="kpi-label">Lectures d\'éditions cumulées</p>\s*<div class="kpi-value-row">\s*<div class="kpi-value">)\d+(</div>.*?</div>\s*<p class="kpi-sub">)depuis le [^<]+(</p>)',
         rf"\g<1>{kpis['total']}\g<2>depuis le {fmt_long(date.fromisoformat(START_DATE))}\g<3>"),
        (r'(<p class="kpi-label">7 derniers jours \(glissant\)</p>\s*<div class="kpi-value-row">\s*<div class="kpi-value">)\d+(</div>.*?</div>\s*<p class="kpi-sub)[^"]*("[^>]*>)[^<]+(</p>)',
         rf"\g<1>{kpis['last7']}\g<2> {kpi_values['sub_class']}\g<3>{delta_text}\g<4>"),
        (r'(<p class="kpi-label">30 derniers jours \(glissant\)</p>\s*<div class="kpi-value">)\d+(</div>\s*<p class="kpi-sub">)[^<]+(</p>)',
         rf"\g<1>{kpis['last30']}\g<2>{sub30}\g<3>"),
        (r'(share30-fill" style="width:)\d+(%)',
         rf"\g<1>{max(0, min(100, kpis['share30']))}\g<2>"),
        (r'(<p class="kpi-label">Moyenne par édition</p>\s*<div class="kpi-value">)[^<]+(</div>\s*<p class="kpi-sub">)[^<]+(</p>)',
         rf"\g<1>{str(kpis['avg_per_edition']).replace('.', ',')}\g<2>lectures/édition, sur les {kpis['tracked_editions']} éditions trackées depuis le {fmt_long(date.fromisoformat(START_DATE))}\g<3>"),
    ]

    spark_cumul = build_sparkline_svg([v for _, v in cumulative[-14:]])
    replacements.append((
        r'(<span class="kpi-spark-wrap-cumul">)(?:(?!</span>).)*(</span>)',
        lambda m: m.group(1) + spark_cumul + m.group(2),
    ))
    spark_week = build_sparkline_svg([v for _, v, _ in weekly[-10:]])
    replacements.append((
        r'(<span class="kpi-spark-wrap-week">)(?:(?!</span>).)*(</span>)',
        lambda m: m.group(1) + spark_week + m.group(2),
    ))

    avg_week = kpis.get("avg_per_edition_7d")
    replacements.append((
        r'(<strong class="avg-week">)[^<]+(</strong>)',
        rf"\g<1>{str(avg_week).replace('.', ',') if avg_week is not None else '—'}\g<2>",
    ))
    avg_month = kpis.get("avg_per_edition_30d")
    replacements.append((
        r'(<strong class="avg-month">)[^<]+(</strong>)',
        rf"\g<1>{str(avg_month).replace('.', ',') if avg_month is not None else '—'}\g<2>",
    ))

    def fmt_usd(v):
        return "— $" if v is None else f"{v:.2f}".replace(".", ",") + " $"

    if openrouter:
        cumul_val = fmt_usd(openrouter["total_usage"])
        remaining = openrouter["total_credits"] - openrouter["total_usage"]
        cumul_sub = f"solde restant : {fmt_usd(remaining)} — au {fmt_long(end_date)}"
    else:
        cumul_val, cumul_sub = "— $", "solde restant : — $ — non disponible"
    replacements.append((
        r'(<p class="kpi-label">Coût OpenRouter cumulé</p>\s*<div class="kpi-value">)[^<]+(</div>\s*<p class="kpi-sub">)[^<]+(</p>)',
        rf"\g<1>{cumul_val}\g<2>{cumul_sub}\g<3>",
    ))

    replacements.append((r'(<strong class="cost-today">)[^<]+(</strong>)',
                          rf"\g<1>{fmt_usd(cost_today['value'] if cost_today else None)}\g<2>"))
    replacements.append((r'(<strong class="cost-yesterday">)[^<]+(</strong>)',
                          rf"\g<1>{fmt_usd(cost_yesterday['value'] if cost_yesterday else None)}\g<2>"))
    replacements.append((r'(<strong class="cost-week">)[^<]+(</strong>)',
                          rf"\g<1>{fmt_usd((openrouter or {}).get('usage_weekly'))}\g<2>"))
    replacements.append((r'(<strong class="cost-month">)[^<]+(</strong>)',
                          rf"\g<1>{fmt_usd((openrouter or {}).get('usage_monthly'))}\g<2>"))

    for pattern, repl in replacements:
        html, n = re.subn(pattern, repl, html, count=1, flags=re.S)
        if n != 1:
            raise RuntimeError(f"dashboard.html : bloc KPI introuvable pour le pattern {pattern[:60]}...")

    # #weekly-svg : dernières ~12 semaines suffisent (graphique, pas un
    # historique complet) — même esprit que xLabels côté #cumul-svg,
    # jamais tout afficher si la série s'allonge.
    weekly_recent = weekly[-12:] if len(weekly) > 12 else weekly
    weekly_literal = "[" + ",\n      ".join(f"['{d}', {v}]" for d, v, _p in weekly_recent) + "\n    ]"
    weekly_last = weekly_recent[-1]
    weekly_aria = (
        f"Lectures d'éditions par semaine, de {weekly_recent[0][1]} la semaine du {fmt_long(date.fromisoformat(weekly_recent[0][0]))} "
        f"à {weekly[-2][1] if len(weekly) > 1 else weekly_last[1]} la semaine précédente, "
        # Précise la date d'arrêt (jamais juste "semaine en cours X lectures")
        # depuis le retour utilisateur du 12 septembre 2026 ("on est le 12
        # septembre pas le 7") — la date du lundi de la semaine en cours se
        # lisait comme la date d'arrêt des données, pas comme un début de
        # période encore ouverte.
        f"semaine en cours {weekly_last[1]} lectures, jusqu'au {fmt_long(end_date)}"
    )
    html, n = re.subn(
        r'(<svg id="weekly-svg"[^>]*aria-label=")[^"]*(")',
        rf"\g<1>{weekly_aria}\g<2>", html, count=1,
    )
    if n != 1:
        raise RuntimeError("dashboard.html : aria-label #weekly-svg introuvable")

    total_editions = len([d for d in get_archive_dates()])
    cumul_aria = (
        f"Courbe de croissance des lectures cumulées d'éditions, de {cumulative[0][1]} le {fmt_long(date.fromisoformat(cumulative[0][0]))} "
        f"à {kpis['total']} le {fmt_long(end_date)} — {total_editions} éditions publiées au total depuis le lancement"
    )
    html, n = re.subn(
        r'(<svg id="cumul-svg"[^>]*aria-label=")[^"]*(")',
        rf"\g<1>{cumul_aria}\g<2>", html, count=1,
    )
    if n != 1:
        raise RuntimeError("dashboard.html : aria-label #cumul-svg introuvable")

    script_m = re.search(r"(<script>\s*\(function \(\) \{.*?)(</script>)", html, re.S)
    if not script_m:
        raise RuntimeError("dashboard.html : bloc <script> principal introuvable")
    script_text = script_m.group(1)
    script_text = replace_js_array(script_text, "weekly", weekly_literal)
    script_text = replace_js_array(script_text, "data", js_array_literal(cumulative))
    script_text = re.sub(
        r"(var totalEditions = )\d+(;)",
        rf"\g<1>{total_editions}\g<2>", script_text, count=1,
    )
    html = html[: script_m.start(1)] + script_text + html[script_m.end(1):]

    # Autonomie par registre
    rows_html = "\n".join(
        f'          <tr><td>{r["label"]}</td><td class="num">{r["n"]}</td>'
        f'<td class="echeance" style="color:{r["color"]}">{r["text"]}</td></tr>'
        for r in autonomy_rows
    )
    html, n = re.subn(
        r'(<span class="chart-label">Autonomie par registre.*?<tbody>).*?(</tbody>)',
        lambda m: m.group(1) + "\n" + rows_html + "\n        " + m.group(2),
        html, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("dashboard.html : tbody Autonomie par registre introuvable")

    degrade = [r for r in autonomy_rows if r["degrade"]]
    if degrade:
        names = ", ".join(f'{r["label"]} ({r["text"]})' for r in degrade)
        autonomy_note = (
            f"{names} : relayer les suggestions des lecteurs "
            f'(<a href="mailto:scenariocontact75@gmail.com" style="color:var(--paper-dim)">scenariocontact75@gmail.com</a>) '
            f"reste le moyen normal de réalimenter ce(s) registre(s)."
        )
    else:
        autonomy_note = "Aucun registre en tension actuellement — tous à 5 sujets non cochés ou plus."
    html, n = re.subn(
        r'(Autonomie par registre — sujets non cochés</span>.*?<p class="kpi-sub" style="margin-top:12px;">).*?(</p>)',
        lambda m: m.group(1) + autonomy_note + m.group(2),
        html, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("dashboard.html : note Autonomie par registre introuvable")

    # Agenda de la semaine + Semaine d'après
    cards_html = "\n".join(
        f'        <div class="agenda-card">\n'
        f'          <p class="agenda-day">{c["day"]}</p>\n'
        f'          <p class="agenda-registre">{c["registre"]}</p>\n'
        f'          <p class="agenda-topic">{c["topic"]}</p>\n'
        f"        </div>"
        for c in agenda_cards
    )
    html, n = re.subn(
        r'(<div class="agenda-grid">).*?(</div>\s*<p class="kpi-sub" style="margin-top:12px;">)',
        lambda m: m.group(1) + "\n" + cards_html + "\n      " + m.group(2),
        html, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("dashboard.html : agenda-grid introuvable")

    html, n = re.subn(
        r'(<p class="kpi-sub" style="margin-top:12px;">).*?(</p>\s*<p class="chart-lead" style="margin-top:18px;">)',
        lambda m: m.group(1) + priority_line + m.group(2),
        html, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("dashboard.html : ligne priorité absolue introuvable")

    later_html = "\n".join(
        (f'        <li><span class="agenda-later-tag">{it["label"]}</span>'
         f'<span class="agenda-later-empty">{it["text"]}</span></li>')
        if it["empty"] else
        (f'        <li><span class="agenda-later-tag">{it["label"]}</span>{it["text"]}</li>')
        for it in agenda_later
    )
    html, n = re.subn(
        r'(<ul class="agenda-later-list">).*?(</ul>)',
        lambda m: m.group(1) + "\n" + later_html + "\n      " + m.group(2),
        html, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("dashboard.html : agenda-later-list introuvable")

    DASHBOARD.write_text(html, encoding="utf-8")


def check_js_syntax(path):
    script = subprocess.run(
        ["node", "-e", f"""
const fs = require('fs');
const html = fs.readFileSync('{path}', 'utf-8');
const matches = [...html.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)];
for (const m of matches) {{ new Function(m[1]); }}
console.log('OK');
"""],
        capture_output=True, text=True,
    )
    if script.returncode != 0 or "OK" not in script.stdout:
        raise RuntimeError(f"JS invalide dans {path} :\n{script.stderr}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    import os
    token = os.environ.get("GOATCOUNTER_TOKEN")
    if not token:
        print("ERREUR : GOATCOUNTER_TOKEN absent de l'environnement.", file=sys.stderr)
        return 1

    payload = fetch_hits(token)
    per_day = aggregate_per_day(payload)
    if not per_day:
        print("ERREUR : aucune lecture agrégée — fichiers non modifiés.", file=sys.stderr)
        return 1

    now_paris = datetime.now(PARIS)
    end_date = now_paris.date()
    # Si aucune donnée pour aujourd'hui/hier (routine lancée très tôt,
    # données GoatCounter pas encore arrivées), reculer d'un jour plutôt
    # que d'afficher un "aujourd'hui" à 0 lectures trompeur.
    if end_date.isoformat() not in per_day and (end_date - timedelta(days=1)).isoformat() not in per_day:
        pass  # jours à 0 gérés naturellement par build_cumulative/sum_window

    cumulative = build_cumulative(per_day, START_DATE, end_date)
    x_labels = pick_x_labels(cumulative)
    y_max = round_up_yaxis(cumulative[-1][1])
    weekly = build_weekly(per_day, START_DATE, end_date)
    archive_dates = get_archive_dates()
    kpis = compute_kpis(per_day, cumulative, end_date, archive_dates)

    md_text = SUJETS_PRIORITAIRES.read_text(encoding="utf-8")
    # Ancre sur le lundi de la semaine EN COURS (pas "le prochain lundi") :
    # contrairement à l'ancienne routine hebdomadaire qui ne tournait que
    # le lundi (d'où "le prochain lundi" = toujours dans le futur proche),
    # ce script tourne maintenant chaque jour — la semaine affichée doit
    # donc toujours être celle où "aujourd'hui" se trouve réellement.
    current_monday = now_paris.date() - timedelta(days=now_paris.date().weekday())
    agenda_cards, agenda_later, priority_line = build_agenda(md_text, current_monday)
    autonomy_rows = build_autonomy_table(md_text)

    print(f"Total cumulé : {kpis['total']} lectures au {fmt_long(end_date)} "
          f"(delta 7j : {kpis['delta7']:+d}).")

    # Coût OpenRouter — jamais bloquant (voir fetch_openrouter_cost) : un
    # échec ici ne doit jamais empêcher la mise à jour du reste du
    # dashboard, qui fonctionnait très bien avant cet ajout.
    openrouter = fetch_openrouter_cost(os.environ.get("OPENROUTER_API_KEY"))
    cost_yesterday = None
    cost_today = None
    if openrouter and not args.dry_run:
        history = update_openrouter_history(end_date.isoformat(), openrouter["total_usage"])
        cost_yesterday = compute_cost_yesterday(history)
        cost_today = compute_cost_today(history, end_date.isoformat())
    elif openrouter:
        print(f"Coût OpenRouter cumulé : {openrouter['total_usage']:.2f} $ "
              f"(solde restant : {openrouter['total_credits'] - openrouter['total_usage']:.2f} $).")

    if args.dry_run:
        print("--dry-run : rien écrit sur disque.")
        return 0

    update_le_projet(cumulative, x_labels, y_max, kpis, end_date)
    update_dashboard(cumulative, weekly, kpis, end_date, agenda_cards, agenda_later, priority_line, autonomy_rows, current_monday, openrouter, cost_yesterday, cost_today)
    check_js_syntax(LE_PROJET)
    check_js_syntax(DASHBOARD)

    print("le-projet.html et dashboard.html mis à jour.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
