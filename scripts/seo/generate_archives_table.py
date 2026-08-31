#!/usr/bin/env python3
"""Génère une nouvelle archives.html avec tableau auto-construit à partir des données d'articles.

Ce script remplace le manuel archives.html par un tableau structuré:
  Date | Titre | Problématique | Évaluation | France Impact | Domaine

Idempotent — peut être relancé après chaque nouvel article pour mettre à jour le tableau.
"""
import re
import html
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
ARCHIVES_DIR = ROOT / "archives"
FRAGMENTS_DIR = ROOT / "archives" / "fragments"
GLOSSAIRE_HTML = ROOT / "glossaire.html"
ARCHIVES_HTML = ROOT / "archives.html"
SITE_URL = "https://lesscenarios.fr"
TODAY = datetime.now().isoformat()

# Domaine labels
DOMAIN_LABELS = {
    "economie-entreprises": "Économie & entreprises",
    "politique-institutions": "Politique & institutions",
    "international": "International",
    "sciences-environnement": "Sciences & environnement",
    "tech-numerique": "Tech & numérique",
    "culture-divertissement": "Culture & divertissement",
}

# CSS pour le tableau
ARCHIVES_TABLE_CSS = """
  /* ---- Archives table (scripts/seo/generate_archives_table.py) ---- */
  .archives-table {
    width: 100%;
    border-collapse: collapse;
    margin: 32px 0;
    font-size: 0.90rem;
    line-height: 1.5;
  }

  .archives-table thead {
    background: var(--surface);
    border-bottom: 2px solid var(--gold);
  }

  .archives-table th {
    padding: 12px;
    text-align: left;
    font-weight: 600;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--gold);
  }

  .archives-table tbody tr {
    border-bottom: 1px solid var(--hairline);
  }

  .archives-table tbody tr:hover {
    background: var(--surface-2);
  }

  .archives-table td {
    padding: 10px 12px;
    vertical-align: top;
  }

  .archives-table .col-date {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.80rem;
    color: var(--paper-dim);
    white-space: nowrap;
    flex-shrink: 0;
  }

  .archives-table .col-title {
    min-width: 200px;
  }

  .archives-table .col-title a {
    color: var(--gold);
    text-decoration: none;
    font-family: "Fraunces", serif;
    font-weight: 600;
  }

  .archives-table .col-title a:hover {
    text-decoration: underline;
    color: var(--paper);
  }

  .archives-table .lang-badge {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.70rem;
    margin-left: 8px;
    color: var(--paper-dim);
    text-decoration: none;
    border: 1px solid var(--paper-dim);
    padding: 2px 6px;
    border-radius: 2px;
  }

  .archives-table .lang-badge:hover {
    color: var(--paper);
    border-color: var(--paper);
  }

  .archives-table .col-question {
    font-size: 0.88rem;
    color: var(--paper);
    font-style: italic;
    min-width: 300px;
  }

  .archives-table .col-eval {
    font-size: 0.88rem;
    color: var(--paper);
    min-width: 250px;
  }

  .archives-table .eval-pct {
    font-family: "JetBrains Mono", monospace;
    font-weight: 600;
    color: var(--gold);
    margin-right: 6px;
  }

  .archives-table .col-france {
    font-size: 0.88rem;
    color: var(--paper);
    min-width: 300px;
  }

  .archives-table .col-scenarios {
    font-size: 0.86rem;
    color: var(--paper);
    min-width: 350px;
  }

  .archives-table .scenario-short {
    margin: 6px 0;
    line-height: 1.4;
  }

  .archives-table .scenario-short:first-child {
    margin-top: 0;
  }

  .archives-table .scenario-short:last-child {
    margin-bottom: 0;
  }

  .archives-table .col-domain {
    font-size: 0.80rem;
    font-family: "JetBrains Mono", monospace;
    color: var(--paper-dim);
    white-space: nowrap;
    flex-shrink: 0;
  }

  @media (max-width: 1200px) {
    .archives-table {
      font-size: 0.85rem;
    }
    .archives-table th,
    .archives-table td {
      padding: 8px 10px;
    }
  }

  @media (max-width: 768px) {
    .archives-table {
      font-size: 0.80rem;
    }
    .archives-table th,
    .archives-table td {
      padding: 6px 8px;
    }
    .archives-table .col-question,
    .archives-table .col-france {
      display: none;
    }
  }
"""


def extract_title(text):
    """Extrait le titre de la balise <title>."""
    m = re.search(r"<title>([^<]+) — Scénario</title>", text)
    return html.unescape(m.group(1)) if m else None


def extract_question(text):
    """Extrait la problématique du bloc .question-text."""
    m = re.search(r'<p class="question-text">([^<]+)</p>', text)
    if m:
        return html.unescape(m.group(1))
    return None


def extract_scenarios(text):
    """Extrait les scénarios avec leurs pourcentages et france-impact."""
    scenarios = []
    for card_match in re.finditer(
        r'<article class="card" data-kind="([^"]+)"[^>]*>(.*?)</article>', text, re.DOTALL
    ):
        kind = card_match.group(1)
        card_content = card_match.group(2)

        pct_m = re.search(r'<div class="gauge-num">(\d+)%</div>', card_content)
        percentage = int(pct_m.group(1)) if pct_m else 0

        # Extrait aussi la france-impact de ce scénario
        france_m = re.search(
            r'<div class="france-line"[^>]*>.*?<span class="field-label">Concrètement en France</span>\s*([^<]+)',
            card_content,
            re.DOTALL,
        )
        france_impact = html.unescape(france_m.group(1).strip()) if france_m else None

        scenarios.append((kind, percentage, france_impact))

    return scenarios


def extract_france_impact(text, most_probable_kind):
    """Extrait la donnée France Impact du scénario le plus probable."""
    # Cherche le card correspondant au kind le plus probable
    pattern = rf'<article class="card" data-kind="{re.escape(most_probable_kind)}"[^>]*>(.*?)</article>'
    card_m = re.search(pattern, text, re.DOTALL)
    if not card_m:
        return None

    card_content = card_m.group(1)
    france_m = re.search(
        r'<div class="france-line"[^>]*>.*?<span class="field-label">Concrètement en France</span>\s*([^<]+)',
        card_content,
        re.DOTALL,
    )
    if france_m:
        # Extrait juste la première phrase, avant l'emoji
        text = france_m.group(1).strip()
        # Enlève l'emoji et le texte qui suit
        text = re.sub(r'\s*[↑↓]\s*.*', '', text)
        return html.unescape(text)
    return None


def extract_domain(text):
    """Extrait le domaine de la meta tag."""
    m = re.search(r'<meta name="domain" content="([^"]+)">', text)
    if m:
        return m.group(1)
    return None


def extract_scenario_texts(iso_date):
    """Extrait les 3 phrases courtes des scénarios du fragment."""
    fragment_path = FRAGMENTS_DIR / f"{iso_date}.html"
    if not fragment_path.exists():
        return None, None, None

    text = fragment_path.read_text(encoding="utf-8")
    # Extrait les 3 scenario-mini-text
    matches = re.findall(r'<p class="scenario-mini-text">([^<]+)</p>', text)

    if len(matches) >= 3:
        return (
            html.unescape(matches[0]),
            html.unescape(matches[1]),
            html.unescape(matches[2])
        )
    return None, None, None


def get_most_probable_scenario(scenarios):
    """Retourne le scénario avec le pourcentage le plus élevé."""
    if not scenarios:
        return (None, None, None)
    best = max(scenarios, key=lambda x: x[1])
    return best[:2]  # Retourne juste (kind, pct), pas france_impact


def parse_article(file_path):
    """Parse un fichier d'article."""
    text = file_path.read_text(encoding="utf-8")

    iso_date = file_path.stem
    title = extract_title(text)
    question = extract_question(text)
    scenarios = extract_scenarios(text)
    domain = extract_domain(text)

    # Extrait le scénario le plus probable (avec titre)
    if scenarios:
        best = max(scenarios, key=lambda x: x[1])
        kind, pct, scenario_title = best
    else:
        kind, pct, scenario_title = None, None, None

    # Extrait france_impact du scénario le plus probable
    france_impact = extract_france_impact(text, kind) if kind else None

    # Extrait les 3 phrases courtes des scénarios depuis le fragment
    scenario_text_1, scenario_text_2, scenario_text_3 = extract_scenario_texts(iso_date)

    return {
        "iso_date": iso_date,
        "title": title,
        "question": question,
        "scenario_kind": kind,
        "scenario_pct": pct,
        "scenario_title": scenario_title,
        "france_impact": france_impact,
        "domain": domain,
        "scenario_text_1": scenario_text_1,
        "scenario_text_2": scenario_text_2,
        "scenario_text_3": scenario_text_3,
    }


def format_date_display(iso_date):
    """Convertit AAAA-MM-JJ en JJ.MM.AAAA."""
    parts = iso_date.split("-")
    return f"{parts[2]}.{parts[1]}.{parts[0]}"


def render_table_row(article):
    """Rend une ligne du tableau."""
    domain_label = DOMAIN_LABELS.get(article["domain"], article["domain"])

    # Problématique : texte complet, pas tronqué
    question_html = (
        html.escape(article["question"])
        if article["question"]
        else "(question non trouvée)"
    )

    # Évaluation : titre complet du scénario + %
    scenario_title = html.escape(article["scenario_title"]) if article["scenario_title"] else "?"
    eval_html = (
        f'<span class="eval-pct">{article["scenario_pct"]}%</span> {scenario_title}'
        if article["scenario_pct"] and article["scenario_title"]
        else "?"
    )

    # France Impact : texte complet, pas tronqué
    france_html = (
        html.escape(article["france_impact"])
        if article["france_impact"]
        else "(impact non trouvé)"
    )

    # Lien EN (toujours ajouter le badge)
    en_link = f' <a href="en/archives/{article["iso_date"]}.html" title="Read in English" class="lang-badge">EN</a>'

    # Les 3 phrases courtes des scénarios
    scenarios_html = ""
    if article["scenario_text_1"] or article["scenario_text_2"] or article["scenario_text_3"]:
        scenarios_html = """
      <div class="col-scenarios">
        <p class="scenario-short">🟢 """ + html.escape(article["scenario_text_1"]) + """</p>
        <p class="scenario-short">🔵 """ + html.escape(article["scenario_text_2"]) + """</p>
        <p class="scenario-short">🔴 """ + html.escape(article["scenario_text_3"]) + """</p>
      </div>"""

    return f"""    <tr>
      <td class="col-date">{format_date_display(article["iso_date"])}</td>
      <td class="col-title"><a href="archives/{article["iso_date"]}.html">{html.escape(article["title"])}</a>{en_link}</td>
      <td class="col-question">{question_html}</td>
      <td class="col-eval">{eval_html}</td>
      <td class="col-france">{france_html}</td>
      <td class="col-scenarios">{scenarios_html.strip() if scenarios_html else "(scénarios non trouvés)"}</td>
      <td class="col-domain">{domain_label}</td>
    </tr>"""


def extract_block(text, start_marker, end_marker, include_end=True):
    """Extrait un bloc HTML."""
    start = text.index(start_marker)
    end = text.index(end_marker, start) + (len(end_marker) if include_end else 0)
    return text[start:end]


def build_shared_pieces():
    """Extrait les blocs réutilisables de glossaire.html."""
    text = GLOSSAIRE_HTML.read_text(encoding="utf-8")
    style_block = extract_block(text, "<style>", "</style>")
    masthead_nav = extract_block(text, '<header class="masthead">', "</nav>")
    follow_footer = extract_block(text, '<section class="follow-block" id="nous-suivre">', "</footer>")
    tail_scripts = extract_block(
        text,
        '<script data-goatcounter="https://scenario.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>',
        "</html>",
    )
    return style_block, masthead_nav, follow_footer, tail_scripts


def render_page(articles, style_block, masthead_nav, follow_footer, tail_scripts):
    """Rend la page archives.html complète."""
    title = "Archives — Scénario"
    description = f"Archives complètes de Scénario : {len(articles)} éditions avec chacune 3 scénarios chiffrés (favorable, stable, dégradé)."
    url = f"{SITE_URL}/archives.html"

    # Rend le tableau
    rows_html = "\n".join(render_table_row(article) for article in articles)
    table_html = f"""  <table class="archives-table">
    <thead>
      <tr>
        <th style="width: 80px;">Date</th>
        <th style="width: 250px;">Titre</th>
        <th style="width: 300px;">Problématique</th>
        <th style="width: 120px;">Évaluation</th>
        <th style="width: 250px;">France Impact</th>
        <th style="width: 350px;">Les 3 scénarios</th>
        <th style="width: 150px;">Domaine</th>
      </tr>
    </thead>
    <tbody>
{rows_html}
    </tbody>
  </table>"""

    json_ld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": {html.escape(title)!r},
  "description": {html.escape(description)!r},
  "url": {url!r},
  "isPartOf": {{ "@type": "WebSite", "name": "Scénario", "url": "{SITE_URL}/" }}
}}
</script>'''.replace("'", '"')

    # Injecte le CSS dans le style block
    style_block = style_block.replace("</style>", ARCHIVES_TABLE_CSS + "</style>")

    head = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="assets/logo.svg">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#10151c">
<link rel="apple-touch-icon" href="assets/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Scénario">
<link rel="stylesheet" href="assets/pwa-install.css">
<meta name="description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Scénario">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE_URL}/assets/social/og-image-v2.png">
<meta property="og:image:width" content="2508">
<meta property="og:image:height" content="1412">
<meta property="og:image:alt" content="Scénario — trois scénarios chiffrés pour chaque actualité : favorable, stable, dégradé.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/assets/social/og-image-v2.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
{style_block}
{json_ld}
</head>
"""

    body = f"""<body>

{masthead_nav}

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Archives</p>
    <h1>Toutes les éditions</h1>
    <p class="dek">Retrouvez toutes nos analyses de l'actualité avec 3 scénarios chiffrés : favorable, stable, dégradé. Cliquez sur le titre pour voir l'analyse complète.</p>
  </div>
</section>

<section class="listing">
  <div class="wrap">
{table_html}
    <p style="margin-top:28px"><a href="index.html" style="color:var(--gold);text-decoration:none">← Retour à l'accueil</a></p>
  </div>
</section>

{follow_footer}

{tail_scripts}
"""
    return head + body


def main():
    """Génère archives.html."""
    print(f"Parsing {len(list(ARCHIVES_DIR.glob('*.html')))} articles...")

    articles = []
    for file_path in sorted(ARCHIVES_DIR.glob("*.html"), reverse=True):
        data = parse_article(file_path)
        articles.append(data)

    print(f"✓ Parsed {len(articles)} articles")

    # Charge les blocs réutilisables
    style_block, masthead_nav, follow_footer, tail_scripts = build_shared_pieces()

    # Génère la page
    page = render_page(articles, style_block, masthead_nav, follow_footer, tail_scripts)

    # Écrit le fichier
    ARCHIVES_HTML.write_text(page, encoding="utf-8")
    print(f"✓ Generated {ARCHIVES_HTML.name}")


if __name__ == "__main__":
    main()
