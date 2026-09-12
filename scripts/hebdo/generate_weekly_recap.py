#!/usr/bin/env python3
"""
Génère le récap hebdomadaire « On refait le scénario de la semaine » et le
publie dans feed-weekly.xml + hebdo/{date}.html + hebdo/fragments/{date}.html
+ sitemap.xml + index.html + archives.html (régénéré) — remplace la routine
Claude Code hebdomadaire « Scénario — On refait le scénario de la semaine »
(docs/routine-hebdo-prompt.md).

Comme scripts/pub/generate_daily_pub.py, l'essentiel de cette routine est
mécanique : retrouver les (jusqu'à) 7 éditions de la semaine dans
docs/sujets-a-suivre.md, relire leurs pages archives déjà publiées, et
reprendre TEL QUEL le texte des 3 scénarios déjà rédigé dans
archives/fragments/{date}.html (jamais réécrit — voir read_edition()).

Seule la rédaction du résumé hebdomadaire (3-4 faits marquants + un
éventuel « fil commun » réel, jamais forcé s'il n'existe pas) et des 1-2
phrases de contexte factuel par sujet demande un vrai jugement éditorial :
un seul appel OpenRouter, strictement contraint aux données déjà publiées
listées ci-dessus (jamais une recherche web, jamais un fait ajouté hors de
ces données — voir build_prompt()). Contrairement à la catégorie « chiffre »
de generate_daily_pub.py, il n'y a pas ici de garde-fou verbatim automatique
possible (la tâche est une synthèse, pas une extraction d'un segment
littéral) : la fiabilité vient du grounding strict du prompt, pas d'une
vérification post-hoc — même modèle de confiance que la session Claude Code
d'origine qu'il remplace.

IMPORTANT — conséquence réelle d'une exécution : feed-weekly.xml alimente
une Automation Buttondown (RSS-to-email) qui envoie le dimanche soir un
email récap aux abonnés hebdo. Moins immédiatement public qu'un post
Telegram/X/LinkedIn/Facebook/Instagram (scripts/pub/…), mais un envoi
d'email reste, comme lui, difficile à « retirer » une fois parti — valider
en conditions réelles avant d'activer un cron automatique sur
.github/workflows/hebdo.yml (workflow_dispatch pour l'instant).

Usage :
    python3 scripts/hebdo/generate_weekly_recap.py --dry-run
    OPENROUTER_API_KEY=xxx python3 scripts/hebdo/generate_weekly_recap.py
    # rattrapage/tests uniquement :
    python3 scripts/hebdo/generate_weekly_recap.py --date 2026-09-13 --dry-run
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
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SUJETS_A_SUIVRE = ROOT / "docs" / "sujets-a-suivre.md"
FEED_WEEKLY = ROOT / "feed-weekly.xml"
ARCHIVES_DIR = ROOT / "archives"
FRAGMENTS_DIR = ARCHIVES_DIR / "fragments"
HEBDO_DIR = ROOT / "hebdo"
HEBDO_FRAGMENTS_DIR = HEBDO_DIR / "fragments"
INDEX_HTML = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
GENERATE_ARCHIVES_TABLE = ROOT / "scripts" / "seo" / "generate_archives_table.py"

PARIS = ZoneInfo("Europe/Paris")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-v4-flash"

MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin",
             "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
NUM_WORDS_FR = {1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq", 6: "six", 7: "sept"}
KIND_FR = {"favorable": "favorable", "stable": "stable", "degrade": "dégradé"}


class HebdoError(Exception):
    pass


# ---------------------------------------------------------------------------
# Petits utilitaires (dates, HTML)
# ---------------------------------------------------------------------------
def fmt_day_month(d):
    return f"{d.day} {MONTHS_FR[d.month - 1]}"


def fmt_full(d):
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}"


def format_range(start, end):
    """« 31 août au 6 septembre 2026 » (année omise sur la première date si
    identique, comme scripts/seo/update_audience.py::fmt_range)."""
    if start.year == end.year:
        return f"{fmt_day_month(start)} au {fmt_full(end)}"
    return f"{fmt_full(start)} au {fmt_full(end)}"


def esc_text(s):
    """Échappe pour du contenu texte HTML (jamais les apostrophes — style
    du site, qui les laisse littérales dans le texte, voir archives/*.html)."""
    return html.escape(s or "", quote=False)


def esc_attr(s):
    """Échappe pour une valeur d'attribut HTML (title, alt, meta content...)."""
    return html.escape(s or "", quote=True)


def bold_to_html(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def inner_html(tag):
    return "".join(str(c) for c in tag.contents) if tag else ""


def strip_extra_bold(texts, max_total):
    """Ne garde que les `max_total` premiers passages **...** rencontrés
    dans l'ordre (bullets d'abord) ; au-delà, retire les ** sans retirer le
    texte — garde-fou pour la règle des 1-2 passages en gras maximum."""
    count = 0

    def cap(text):
        nonlocal count

        def repl(m):
            nonlocal count
            count += 1
            if count <= max_total:
                return f"**{m.group(1)}**"
            return m.group(1)

        return re.sub(r"\*\*(.+?)\*\*", repl, text)

    return [cap(t) for t in texts]


def check(n, label):
    if n != 1:
        raise HebdoError(f"remplacement '{label}' a matché {n} fois (attendu 1)")


def clamp_meta_description(text, limit=165):
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text.rfind(" ", 0, limit)
    return text[: cut if cut > 0 else limit].rstrip()


# ---------------------------------------------------------------------------
# Étape 1 — les (jusqu'à) 7 éditions de la semaine
# ---------------------------------------------------------------------------
JOURNAL_LINE_RE = re.compile(
    r"^- (\d{2})\.(\d{2})\.(\d{4}) — \[(.+?)\]\(\.\./archives/(\d{4}-\d{2}-\d{2})\.html\)"
)


def parse_journal_entries(md_text):
    """[(date, titre_court)] pour chaque ligne du « Journal des sujets
    publiés » de docs/sujets-a-suivre.md."""
    parts = md_text.split("## Journal des sujets publiés", 1)
    if len(parts) < 2:
        raise HebdoError("section 'Journal des sujets publiés' introuvable dans sujets-a-suivre.md")
    entries = []
    for line in parts[1].splitlines():
        m = JOURNAL_LINE_RE.match(line.strip())
        if not m:
            continue
        d = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        if d.isoformat() != m.group(5):
            continue  # date de la ligne et date de l'archive citée incohérentes : on ignore plutôt que deviner
        entries.append((d, m.group(4)))
    return entries


def week_editions(md_text, sunday):
    """Entrées du lundi au dimanche (inclus) de la semaine finissant à
    `sunday`, triées du lundi au dimanche — jamais plus de 7, jamais une
    entrée inventée si moins de 7 existent réellement."""
    monday = sunday - timedelta(days=6)
    entries = parse_journal_entries(md_text)
    week = [(d, title) for d, title in entries if monday <= d <= sunday]
    week.sort(key=lambda x: x[0])
    return week


# ---------------------------------------------------------------------------
# Étape 2 — lire chaque édition (archive + fragment déjà publiés)
# ---------------------------------------------------------------------------
SCENARIO_ARROW = {"favorable": "↑", "stable": "→", "degrade": "↓"}


def ensure_fragment(d, archive_soup, write=True):
    """archives/fragments/{date}.html est normalement créé par la routine
    éditoriale quotidienne (docs/routine-prompt.md, § « Le bloc dépliable
    des 3 scénarios ») — mais certaines éditions passées ne l'ont jamais eu
    (bug de la routine d'origine, pas de ce script). Plutôt que de faire
    échouer tout le récap hebdo pour un fichier manquant côté quotidien, on
    le reconstruit ici depuis l'archive elle-même — jamais par réécriture :
    seulement la 1re phrase, déjà publiée et déjà relue, de chaque
    paragraphe « pourquoi » de la carte. Écrit sur disque au passage, ce qui
    corrige aussi silencieusement le bouton « Voir les scénarios »
    d'archives.html pour cette édition (voir docs/routine-prompt.md, ligne
    citée plus haut)."""
    fragment_path = FRAGMENTS_DIR / f"{d.isoformat()}.html"
    minis = []
    for card in archive_soup.select(".cards .card"):
        kind = card.get("data-kind")
        h3 = card.select_one("h3")
        pct_num = card.select_one(".gauge-num")
        why = card.select_one(".why")
        if not (kind and h3 and pct_num and why):
            raise HebdoError(f"reconstruction du fragment {d.isoformat()} : carte incomplète ({kind})")
        pct = re.sub(r"\D", "", pct_num.get_text())
        first_sentence_m = re.match(r"(.+?[.!?])(\s|$)", why.get_text().strip())
        text = first_sentence_m.group(1) if first_sentence_m else why.get_text().strip()
        minis.append(
            f'  <div class="scenario-mini" data-kind="{kind}">\n'
            f'    <p class="scenario-mini-title"><span class="scenario-mini-arrow" aria-hidden="true">'
            f'{SCENARIO_ARROW.get(kind, "")}</span> <span class="scenario-mini-pct">{pct}%</span> '
            f'{esc_text(h3.get_text().strip())}</p>\n'
            f'    <p class="scenario-mini-text">{esc_text(text)}</p>\n'
            f'  </div>'
        )
    if len(minis) != 3:
        raise HebdoError(f"reconstruction du fragment {d.isoformat()} : {len(minis)} cartes trouvées (attendu 3)")
    fragment_html = '<div class="scenario-grid">\n' + "\n".join(minis) + '\n</div>\n'
    if write:
        fragment_path.write_text(fragment_html, encoding="utf-8")
        print(f"  (fragment manquant pour {d.isoformat()} — reconstruit depuis l'archive et sauvegardé)")
    else:
        print(f"  (fragment manquant pour {d.isoformat()} — reconstruit en mémoire, --dry-run : rien n'est écrit)")
    return fragment_html.strip()


def read_edition(d, write_missing_fragment=True):
    date_str = d.isoformat()
    archive_path = ARCHIVES_DIR / f"{date_str}.html"
    fragment_path = FRAGMENTS_DIR / f"{date_str}.html"
    if not archive_path.exists():
        raise HebdoError(f"archive manquante : {archive_path}")

    soup = BeautifulSoup(archive_path.read_text(encoding="utf-8"), "html.parser")
    h1 = soup.select_one("h1")
    eyebrow = soup.select_one(".eyebrow")
    question = soup.select_one(".question-text")
    if not (h1 and eyebrow and question):
        raise HebdoError(f"{archive_path} : h1/.eyebrow/.question-text manquant")

    if fragment_path.exists():
        fragment_text = fragment_path.read_text(encoding="utf-8").strip()
    else:
        fragment_text = ensure_fragment(d, soup, write=write_missing_fragment)
    fragment_soup = BeautifulSoup(fragment_text, "html.parser")
    scenario_grid = fragment_soup.select_one(".scenario-grid")
    if not scenario_grid:
        raise HebdoError(f"{fragment_path} : .scenario-grid introuvable")

    scenarios = {}
    for mini in fragment_soup.select(".scenario-mini"):
        kind = mini.get("data-kind")
        pct_tag = mini.select_one(".scenario-mini-pct")
        title_p = mini.select_one(".scenario-mini-title")
        text_p = mini.select_one(".scenario-mini-text")
        if not (kind and pct_tag and title_p and text_p):
            raise HebdoError(f"{fragment_path} : scenario-mini incomplet ({kind})")
        pct = int(re.sub(r"\D", "", pct_tag.get_text()) or "0")
        title_text = title_p.get_text()
        title_only = title_text.split("%", 1)[1].strip() if "%" in title_text else title_text.strip()
        scenarios[kind] = {"pct": pct, "title": title_only, "text": text_p.get_text().strip()}

    if set(scenarios) != {"favorable", "stable", "degrade"}:
        raise HebdoError(f"{fragment_path} : scénarios incomplets ({sorted(scenarios)})")

    winner_kind = max(scenarios, key=lambda k: scenarios[k]["pct"])

    return {
        "date": d,
        "date_str": date_str,
        "h1": h1.get_text().strip(),
        "eyebrow_html": inner_html(eyebrow),
        "eyebrow_text": eyebrow.get_text().strip(),
        "question": question.get_text().strip(),
        "scenarios": scenarios,
        "winner_kind": winner_kind,
        # str(scenario_grid), pas le fragment_text brut : certains fragments
        # portent aussi un <p class="fragment-question"> avant le
        # .scenario-grid (repris par archives.html pour son propre bouton
        # « Voir les scénarios ») — la question est déjà affichée séparément
        # dans le day-card (.day-card-context, voir day_card_html()), donc
        # on ne réutilise que le .scenario-grid lui-même, jamais tout le
        # fichier brut, pour ne pas la dupliquer.
        "scenario_grid_html": str(scenario_grid),
        "has_image": (ROOT / "assets" / "social" / "instagram" / f"{date_str}.png").exists(),
    }


# ---------------------------------------------------------------------------
# Étape 3 — rédaction (un seul appel OpenRouter, strictement grounded)
# ---------------------------------------------------------------------------
def call_openrouter_json(prompt, model, api_key, timeout=90):
    body = json.dumps({
        "model": model,
        "max_tokens": 3000,
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
        "reasoning": {"enabled": False},
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(OPENROUTER_URL, method="POST", data=body, headers={
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    if "choices" not in data:
        raise HebdoError(f"réponse OpenRouter sans 'choices' : {data}")
    content = data["choices"][0]["message"]["content"]
    return json.loads(content), data.get("usage", {})


def build_llm_input(editions):
    days = []
    for e in editions:
        w = e["scenarios"][e["winner_kind"]]
        days.append({
            "date": e["date_str"],
            "jour_registre": e["eyebrow_text"],
            "titre": e["h1"],
            "question": e["question"],
            "scenario_gagnant": KIND_FR[e["winner_kind"]],
            "pourcentage": w["pct"],
            "scenario_titre": w["title"],
            "scenario_texte": w["text"],
        })
    return days


def build_prompt(days):
    n = len(days)
    bullet_count = "un par sujet" if n < 3 else "3 à 4 (un par sujet si moins de 4 sujets au total)"
    return f"""Tu rédiges le récap hebdomadaire du site « Scénario » (lesscenarios.fr)
— « On refait le scénario de la semaine ». Voici les {n} sujets de la
semaine, dans l'ordre chronologique (lundi en premier). Pour chaque sujet :
la question posée, et le scénario déjà jugé le plus probable par l'édition
du jour (titre, pourcentage, explication déjà rédigée). Ce jugement et ce
pourcentage sont FIXES : ne les remets pas en cause, ne les modifie pas.

Sujets de la semaine (JSON) :
{json.dumps(days, ensure_ascii=False, indent=2)}

RÈGLE ABSOLUE : n'invente et n'ajoute AUCUN fait, chiffre, date ou nom
propre absent des données ci-dessus. Tu résumes/reformules, tu ne
recherches et n'imagines jamais une information nouvelle.

Tâche 1 — Conclusion de la semaine :
- "opening" : une phrase d'intro courte (jamais les dates de la semaine,
  déjà données ailleurs dans la page).
- "bullets" : {bullet_count} faits CONCRETS et SPÉCIFIQUES, chacun tiré
  d'un sujet différent — jamais une remarque sur la structure du récap
  elle-même (interdit : "le stable l'emporte X fois sur 7", "sept sujets,
  sept scénarios chiffrés" comme accroche). Un fait précis par puce, pas
  seulement l'étiquette du scénario.
- "thread" : UNE phrase qui tire un vrai fil conducteur SEULEMENT s'il
  existe réellement un lien de fond entre plusieurs sujets (même thème
  géopolitique, plusieurs dossiers bloqués sans dénouement, plusieurs
  bascules vers le même type de scénario pour une raison de fond
  identifiable) — jamais une coïncidence statistique présentée comme un
  constat. Si les sujets n'ont vraiment aucun lien réel, renvoie null :
  ne force jamais un faux fil conducteur. Si non-null, commence par
  "Le fil commun de la semaine : ". N'utilise PAS ** dans "thread" (il
  sera mis en gras en entier automatiquement, comme le veut le gabarit).
- Dans "opening"/"bullets" uniquement, tu peux entourer de **...** un
  passage court (1 passage la plupart des semaines, 2 maximum au total)
  correspondant au fait le plus important de la semaine — jamais une
  date ou un nom d'institution mis en gras juste parce qu'il est présent.
  N'en mets aucun si rien ne s'impose vraiment.
- "meta_description" : ~150-160 caractères, condensé factuel de l'opening
  et du fait le plus marquant, texte brut sans HTML, sans les dates.

Tâche 2 — pour CHAQUE sujet (même ordre, même "date" en clé) :
- "context" : 1 à 2 phrases factuelles et déclaratives (jamais une
  question) qui posent la situation, reformulées à partir de "question" —
  jamais une reprise mot pour mot.
- "explication" : une courte clause (sans point final), qui reprend
  l'idée de "scenario_texte" en la raccourcissant/paraphrasant — jamais
  un fait ajouté qui n'y figure pas.

Réponds avec un JSON unique, exactement :
{{
  "opening": "...",
  "bullets": ["...", "..."],
  "thread": "..." ou null,
  "meta_description": "...",
  "days": [
    {{"date": "AAAA-MM-JJ", "context": "...", "explication": "..."}}
  ]
}}
"""


# ---------------------------------------------------------------------------
# Étape 4 — assemblage (feed-weekly.xml, hebdo/{date}.html, fragment)
# ---------------------------------------------------------------------------
def build_day_paragraph(e, context, explanation):
    w = e["scenarios"][e["winner_kind"]]
    h1 = e["h1"]
    punct = "" if h1 and h1[-1] in "?!." else "."
    kind_fr = KIND_FR[e["winner_kind"]]
    context = context.strip()
    if context and context[-1] not in ".!?":
        context += "."
    explanation = explanation.strip().rstrip(".")
    link = f'https://lesscenarios.fr/archives/{e["date_str"]}.html'
    return (
        f'<strong>{e["eyebrow_html"]}</strong> — <a href="{link}">{esc_text(h1)}</a>{punct} '
        f'{esc_text(context)} Scénario {kind_fr} jugé le plus probable, à {w["pct"]}% : '
        f'{esc_text(w["title"])} — {esc_text(explanation)}.'
    )


def build_description_cdata(opening_html, bullets_html, thread_html, day_paragraphs):
    li = "".join(f"<li>{b}</li>" for b in bullets_html)
    out = f"{opening_html}<ul>{li}</ul>"
    if thread_html:
        out += f"<strong>{thread_html}</strong>"
    out += "<br><br>" + "<br><br>".join(day_paragraphs)
    out += "<br><br>Une question, une remarque ? Réponds directement à cet email."
    return out


def build_comments(opening_plain, bullets_plain, thread_plain):
    first = opening_plain.rstrip(":.").strip() + "."
    bullets_joined = " • ".join(b.rstrip(".").strip() + "." for b in bullets_plain)
    parts = [first, bullets_joined]
    if thread_plain:
        parts.append(thread_plain if thread_plain[-1:] in ".!?" else thread_plain + ".")
    return " ".join(parts)


def build_feed_item_xml(sunday, title, comments, description_cdata):
    date_str = sunday.isoformat()
    pub_date = datetime(sunday.year, sunday.month, sunday.day, 14, 0, 0, tzinfo=PARIS)
    link = f"https://lesscenarios.fr/hebdo/{date_str}.html"
    guid = f"scenario-hebdo-{date_str}"
    return (
        f"    <item>\n"
        f"      <title>{esc_attr(title)}</title>\n"
        f"      <link>{link}</link>\n"
        f"      <guid isPermaLink=\"false\">{guid}</guid>\n"
        f"      <pubDate>{pub_date.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>\n"
        f"      <comments>{esc_attr(comments)}</comments>\n"
        f"      <description><![CDATA[{description_cdata}]]></description>\n"
        f"    </item>\n"
    )


def insert_item(xml_text, item_xml):
    return xml_text.replace("<item>", item_xml.strip() + "\n    <item>", 1)


def validate_feed_xml(path):
    tree = ET.parse(path)
    items = tree.getroot().find("channel").findall("item")
    guids = [it.find("guid").text for it in items]
    if len(guids) != len(set(guids)):
        raise HebdoError(f"validate_feed_xml : guid en double dans {path}")
    return len(items)


def build_week_conclusion_lead_html(bullets_html, thread_html):
    li = "\n    ".join(f"<li>{b}</li>" for b in bullets_html)
    thread_p = (
        f'\n  <p class="week-conclusion-thread"><strong>{thread_html}</strong></p>'
        if thread_html else ""
    )
    return (
        '<div class="week-conclusion week-conclusion-lead">\n'
        '  <p class="week-conclusion-label">Conclusion de la semaine</p>\n'
        '  <ul class="week-conclusion-bullets">\n'
        f'    {li}\n'
        '  </ul>' + thread_p + '\n'
        '</div>'
    )


def day_card_html(e, prefix):
    date_str = e["date_str"]
    img_src = (f'{prefix}assets/social/instagram/{date_str}.png' if e["has_image"]
               else f'{prefix}assets/social/instagram/default.png')
    alt = esc_attr(e["h1"])
    archive_href = f'{prefix}archives/{date_str}.html'
    question_html = esc_text(f"❓ {e['question']}")
    return f'''<div class="day-card">
  <p class="day-card-eyebrow">{e["eyebrow_html"]}</p>
  <a class="day-card-image-link" href="{archive_href}">
    <img class="day-card-image" src="{img_src}" alt="{alt}" loading="lazy">
  </a>
  <button type="button" class="day-card-toggle" aria-expanded="false" aria-controls="detail-{date_str}">Voir le détail <span class="day-card-toggle-icon" aria-hidden="true">▾</span></button>
  <div class="day-card-detail" id="detail-{date_str}">
    <div class="day-card-detail-inner">
      <p class="day-card-context">{question_html}</p>
      {e["scenario_grid_html"]}
      <a class="day-link" href="{archive_href}">Lire l'édition →</a>
    </div>
  </div>
</div>'''


def latest_hebdo_template():
    """Le gabarit à copier est toujours le dernier hebdo/*.html publié (voir
    docs/routine-hebdo-prompt.md étape 4) — jamais un gabarit figé dans ce
    script, qui dériverait silencieusement du CSS/de la structure réels
    dès le prochain changement de gabarit humain."""
    candidates = sorted(
        p for p in HEBDO_DIR.glob("*.html")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.html", p.name)
    )
    if not candidates:
        raise HebdoError("aucun hebdo/*.html existant à utiliser comme gabarit")
    return candidates[-1]


def build_hebdo_page(template_path, sunday, title, dek, meta_description,
                      week_conclusion_html, week_grid_cards_html):
    text = template_path.read_text(encoding="utf-8")
    date_str = sunday.isoformat()
    full_title = f"{title} — Scénario"
    published_time = f"{date_str}T14:00:00+02:00"

    text, n = re.subn(r"<title>.*?</title>", f"<title>{esc_text(full_title)}</title>", text, count=1)
    check(n, "title")
    text, n = re.subn(r'<link rel="canonical" href="[^"]*">',
                       f'<link rel="canonical" href="https://lesscenarios.fr/hebdo/{date_str}.html">',
                       text, count=1)
    check(n, "canonical")
    text, n = re.subn(r'<meta name="description" content="[^"]*">',
                       f'<meta name="description" content="{esc_attr(meta_description)}">', text, count=1)
    check(n, "meta description")
    text, n = re.subn(r'<meta property="og:url" content="[^"]*">',
                       f'<meta property="og:url" content="https://lesscenarios.fr/hebdo/{date_str}.html">',
                       text, count=1)
    check(n, "og:url")
    text, n = re.subn(r'<meta property="og:title" content="[^"]*">',
                       f'<meta property="og:title" content="{esc_attr(full_title)}">', text, count=1)
    check(n, "og:title")
    text, n = re.subn(r'<meta property="og:description" content="[^"]*">',
                       f'<meta property="og:description" content="{esc_attr(meta_description)}">', text, count=1)
    check(n, "og:description")
    text, n = re.subn(r'<meta property="article:published_time" content="[^"]*">',
                       f'<meta property="article:published_time" content="{published_time}">', text, count=1)
    check(n, "article:published_time")
    text, n = re.subn(r'<meta name="twitter:title" content="[^"]*">',
                       f'<meta name="twitter:title" content="{esc_attr(full_title)}">', text, count=1)
    check(n, "twitter:title")
    text, n = re.subn(r'<meta name="twitter:description" content="[^"]*">',
                       f'<meta name="twitter:description" content="{esc_attr(meta_description)}">', text, count=1)
    check(n, "twitter:description")
    text, n = re.subn(r'<p class="dek">.*?</p>', f'<p class="dek">{esc_text(dek)}</p>', text, count=1)
    check(n, "dek")

    inner = week_conclusion_html + "\n\n" + f'<div class="week-grid">\n\n{week_grid_cards_html}\n\n</div>'
    text, n = re.subn(
        r'<div class="week-conclusion week-conclusion-lead">.*?</section>',
        inner + "\n  </div>\n</section>",
        text, count=1, flags=re.S,
    )
    check(n, "week-conclusion/week-grid")
    return text


# ---------------------------------------------------------------------------
# Étape 4bis — sitemap.xml / index.html / archives.html
# ---------------------------------------------------------------------------
def update_sitemap(sunday):
    text = SITEMAP.read_text(encoding="utf-8")
    date_str = sunday.isoformat()
    anchor_re = re.compile(
        rf'(<url>\s*<loc>https://lesscenarios\.fr/archives/{re.escape(date_str)}\.html</loc>\s*'
        rf'<lastmod>.*?</lastmod>\s*<changefreq>.*?</changefreq>\s*<priority>.*?</priority>\s*</url>\n)',
        re.S,
    )
    new_block = (
        f'  <url>\n'
        f'    <loc>https://lesscenarios.fr/hebdo/{date_str}.html</loc>\n'
        f'    <lastmod>{date_str}</lastmod>\n'
        f'    <changefreq>never</changefreq>\n'
        f'    <priority>0.5</priority>\n'
        f'  </url>\n'
    )
    new_text, n = anchor_re.subn(lambda m: m.group(1) + new_block, text, count=1)
    if n != 1:
        raise HebdoError(f"sitemap.xml : entrée archives/{date_str}.html introuvable, insertion abandonnée")
    return new_text


def update_index_html(sunday):
    text = INDEX_HTML.read_text(encoding="utf-8")
    date_str = sunday.isoformat()
    m = re.search(r'data-hebdo="(\d{4}-\d{2}-\d{2})"', text)
    if not m:
        raise HebdoError("index.html : attribut data-hebdo introuvable")
    old_date = m.group(1)
    if old_date == date_str:
        return text, False

    text, n1 = re.subn(
        rf'(<a class="masthead-notif-btn" href="hebdo/){re.escape(old_date)}(\.html" aria-label="Récap de la semaine")',
        rf'\g<1>{date_str}\g<2>', text, count=1,
    )
    text, n2 = re.subn(
        r'(<div class="weekly-banner" id="weekly-banner" data-hebdo=")\d{4}-\d{2}-\d{2}(")',
        rf'\g<1>{date_str}\g<2>', text, count=1,
    )
    text, n3 = re.subn(
        r'(<a class="weekly-banner-link" id="weekly-banner-link" href="hebdo/)\d{4}-\d{2}-\d{2}(\.html")',
        rf'\g<1>{date_str}\g<2>', text, count=1,
    )
    if (n1, n2, n3) != (1, 1, 1):
        raise HebdoError(f"index.html : remplacements inattendus ({n1},{n2},{n3}) — abandon plutôt que de deviner")
    return text, True


def regenerate_archives_table():
    result = subprocess.run(
        [sys.executable, str(GENERATE_ARCHIVES_TABLE)],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise HebdoError(f"generate_archives_table.py a échoué :\n{result.stdout}\n{result.stderr}")


# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--date", help="Dimanche ciblé (AAAA-MM-JJ) — tests/rattrapage uniquement, "
                                        "par défaut aujourd'hui à Paris.")
    parser.add_argument("--force-weekday", action="store_true",
                         help="Ignore la vérification 'doit être un dimanche' (tests uniquement).")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    sunday = date.fromisoformat(args.date) if args.date else datetime.now(PARIS).date()
    if sunday.weekday() != 6 and not args.force_weekday:
        print(f"{sunday.isoformat()} n'est pas un dimanche — rien à publier.", file=sys.stderr)
        return 1

    date_str = sunday.isoformat()
    monday = sunday - timedelta(days=6)

    if not FEED_WEEKLY.exists():
        raise HebdoError(f"{FEED_WEEKLY} introuvable")
    feed_text = FEED_WEEKLY.read_text(encoding="utf-8")

    m = re.search(r"<pubDate>(.*?)</pubDate>", feed_text)
    if m:
        try:
            existing = datetime.strptime(m.group(1), "%a, %d %b %Y %H:%M:%S %z").date()
        except ValueError:
            existing = None
        if existing == sunday:
            print(f"Un récap est déjà publié pour le {date_str} — rien à faire.")
            return 0

    md_text = SUJETS_A_SUIVRE.read_text(encoding="utf-8")
    week = week_editions(md_text, sunday)
    if not week:
        print(f"Aucune édition trouvée entre {monday.isoformat()} et {date_str}.", file=sys.stderr)
        return 1
    if len(week) < 7:
        print(f"Attention : seulement {len(week)}/7 éditions trouvées pour cette semaine.")

    editions = [read_edition(d, write_missing_fragment=not args.dry_run) for d, _ in week]
    print(f"{len(editions)} édition(s) retenue(s) : {', '.join(e['date_str'] for e in editions)}")

    llm_days = build_llm_input(editions)
    prompt = build_prompt(llm_days)
    result, usage = call_openrouter_json(prompt, args.model, api_key)
    cost = usage.get("cost", 0) or 0

    opening = (result.get("opening") or "").strip()
    bullets = [b.strip() for b in (result.get("bullets") or []) if b.strip()]
    thread = (result.get("thread") or "").strip() or None
    meta_description = clamp_meta_description(result.get("meta_description"))
    days_result = {d.get("date"): d for d in (result.get("days") or [])}

    if not opening or not bullets:
        raise HebdoError("réponse OpenRouter incomplète : 'opening'/'bullets' manquant(s)")

    max_bold = 1 if thread else 2
    bullets = strip_extra_bold(bullets, max_bold)
    bullets_plain = [b.replace("**", "") for b in bullets]
    thread_plain = thread.replace("**", "") if thread else None

    day_paragraphs = []
    for e in editions:
        d_res = days_result.get(e["date_str"])
        if not d_res or not d_res.get("context") or not d_res.get("explication"):
            raise HebdoError(f"réponse OpenRouter : contexte/explication manquant pour {e['date_str']}")
        day_paragraphs.append(build_day_paragraph(e, d_res["context"], d_res["explication"]))

    opening_html = bold_to_html(esc_text(opening))
    bullets_html = [bold_to_html(esc_text(b)) for b in bullets]
    thread_html = esc_text(thread_plain) if thread_plain else None

    date_range_title = format_range(monday, sunday)
    title = f"On refait le scénario de la semaine — {date_range_title}"
    n_word = NUM_WORDS_FR.get(len(editions), str(len(editions)))
    dek = f"{date_range_title} — {n_word} sujets, {n_word} fois trois scénarios chiffrés."

    print(f"\nTitre : {title}")
    print(f"Ouverture : {opening}")
    for b in bullets_plain:
        print(f"  - {b}")
    if thread_plain:
        print(f"Fil commun : {thread_plain}")
    print(f"Meta description ({len(meta_description)} caractères) : {meta_description}")
    print(f"Coût OpenRouter ≈ {cost} $.")

    if args.dry_run:
        print("--dry-run : aucun fichier modifié.")
        return 0

    week_conclusion_page = build_week_conclusion_lead_html(bullets_html, thread_html)
    day_cards_page = "\n\n".join(day_card_html(e, "../") for e in editions)
    day_cards_fragment = "\n\n".join(day_card_html(e, "") for e in editions)

    template_path = latest_hebdo_template()
    hebdo_html = build_hebdo_page(template_path, sunday, title, dek, meta_description,
                                   week_conclusion_page, day_cards_page)
    HEBDO_DIR.mkdir(parents=True, exist_ok=True)
    (HEBDO_DIR / f"{date_str}.html").write_text(hebdo_html, encoding="utf-8")

    fragment_html = week_conclusion_page + "\n\n" + f'<div class="week-grid">\n\n{day_cards_fragment}\n\n</div>\n'
    HEBDO_FRAGMENTS_DIR.mkdir(parents=True, exist_ok=True)
    (HEBDO_FRAGMENTS_DIR / f"{date_str}.html").write_text(fragment_html, encoding="utf-8")
    print(f"hebdo/{date_str}.html et hebdo/fragments/{date_str}.html créés.")

    description_cdata = build_description_cdata(opening_html, bullets_html, thread_html, day_paragraphs)
    comments = build_comments(opening, bullets_plain, thread_plain)
    item_xml = build_feed_item_xml(sunday, title, comments, description_cdata)
    new_feed_text = insert_item(feed_text, item_xml)
    FEED_WEEKLY.write_text(new_feed_text, encoding="utf-8")
    validate_feed_xml(FEED_WEEKLY)
    print("feed-weekly.xml : item ajouté et validé.")

    SITEMAP.write_text(update_sitemap(sunday), encoding="utf-8")
    print("sitemap.xml : entrée ajoutée.")

    new_index_text, changed = update_index_html(sunday)
    if changed:
        INDEX_HTML.write_text(new_index_text, encoding="utf-8")
        print("index.html : icône masthead + bandeau hebdo mis à jour.")

    regenerate_archives_table()
    print("archives.html : régénéré (ligne récap incluse).")

    print(f"\nRésumé : récap {date_str} publié — {len(editions)} sujets couverts "
          f"({', '.join(e['date_str'] for e in editions)}), coût OpenRouter ≈ {cost} $.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except HebdoError as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        sys.exit(1)
