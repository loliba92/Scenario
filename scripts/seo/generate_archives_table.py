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
    max-width: 1200px;
    margin: 32px auto;
    border-collapse: collapse;
    font-size: 0.90rem;
    line-height: 1.6;
    background: var(--surface);
    border: 1px solid var(--hairline);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .archives-table thead {
    background: linear-gradient(135deg, var(--surface-2) 0%, var(--surface) 100%);
    border-bottom: 2px solid var(--gold);
  }

  .archives-table th {
    padding: 14px 12px;
    text-align: center;
    font-weight: 700;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.70rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--gold);
  }

  .archives-table th:first-child,
  .archives-table th:nth-child(2),
  .archives-table th:nth-child(3) {
    text-align: left;
  }

  .archives-table tbody tr {
    border-bottom: 1px solid var(--hairline);
    transition: background 0.2s ease;
  }

  .archives-table tbody tr:last-child {
    border-bottom: none;
  }

  .archives-table tbody tr:hover {
    background: var(--surface-2);
  }

  .archives-table td {
    padding: 12px;
    vertical-align: middle;
  }

  .archives-table .col-date {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--gold);
    white-space: nowrap;
    flex-shrink: 0;
    letter-spacing: 0.02em;
    text-align: center;
  }

  .archives-table .col-domain {
    font-size: 0.75rem;
    font-family: "JetBrains Mono", monospace;
    font-weight: 600;
    color: var(--gold);
    white-space: nowrap;
    flex-shrink: 0;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    text-align: center;
  }

  .archives-table .col-title {
    min-width: 280px;
  }

  .archives-table .col-title a {
    color: var(--gold);
    text-decoration: none;
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: 0.95rem;
    transition: color 0.2s ease;
  }

  .archives-table .col-title a:hover {
    color: var(--paper);
    text-decoration: underline;
  }

  .archives-table .lang-badge {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.65rem;
    margin-left: 8px;
    color: var(--paper-dim);
    text-decoration: none;
    border: 1px solid var(--paper-dim);
    padding: 3px 7px;
    border-radius: 3px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.2s ease;
  }

  .archives-table .lang-badge:hover {
    color: var(--gold);
    border-color: var(--gold);
    background: rgba(218, 165, 32, 0.08);
  }

  .archives-table .col-eval {
    text-align: center;
  }

  .archives-table .eval-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.75rem;
    font-family: "JetBrains Mono", monospace;
    white-space: nowrap;
  }

  .archives-table .eval-badge.eval-favorable {
    background: rgba(94, 156, 120, 0.12);
    color: #5e9c78;
    border: 1px solid rgba(94, 156, 120, 0.3);
  }

  .archives-table .eval-badge.eval-stable {
    background: rgba(111, 143, 174, 0.12);
    color: #6f8fae;
    border: 1px solid rgba(111, 143, 174, 0.3);
  }

  .archives-table .eval-badge.eval-degrade {
    background: rgba(189, 98, 72, 0.12);
    color: #bd6248;
    border: 1px solid rgba(189, 98, 72, 0.3);
  }

  .archives-table .eval-label {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .archives-table .eval-pct {
    font-weight: 700;
    font-size: 0.75rem;
  }

  .archives-table .col-france {
    text-align: center;
  }

  .archives-table .france-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.75rem;
    font-family: "JetBrains Mono", monospace;
    white-space: nowrap;
  }

  .archives-table .france-badge.france-favorable {
    background: rgba(94, 156, 120, 0.12);
    color: #5e9c78;
    border: 1px solid rgba(94, 156, 120, 0.3);
  }

  .archives-table .france-badge.france-stable {
    background: rgba(111, 143, 174, 0.12);
    color: #6f8fae;
    border: 1px solid rgba(111, 143, 174, 0.3);
  }

  .archives-table .france-badge.france-degrade {
    background: rgba(189, 98, 72, 0.12);
    color: #bd6248;
    border: 1px solid rgba(189, 98, 72, 0.3);
  }

  @media (max-width: 1200px) {
    .archives-table {
      font-size: 0.85rem;
    }
    .archives-table th,
    .archives-table td {
      padding: 10px 10px;
    }
  }

  @media (max-width: 768px) {
    .archives-table {
      font-size: 0.80rem;
      margin: 20px auto;
    }
    .archives-table th,
    .archives-table td {
      padding: 8px;
    }
    .archives-table th:nth-child(4),
    .archives-table td:nth-child(4) {
      display: none;
    }
    .archives-table .eval-badge,
    .archives-table .france-badge {
      flex-direction: column;
      gap: 2px;
      padding: 5px 10px;
      font-size: 0.70rem;
    }
  }

  @media (max-width: 480px) {
    .archives-table {
      font-size: 0.75rem;
      margin: 16px auto;
    }
    .archives-table th,
    .archives-table td {
      padding: 6px;
    }
    .archives-table .col-title a {
      font-size: 0.85rem;
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


def extract_france_judgment(france_text):
    """Extrait le jugement France Impact (Favorable/Dégradé/Stable) du texte complet.

    Exemple:
      "↓ Plutôt défavorable pour la France" → "Dégradé"
      "↑ Plutôt favorable pour la France" → "Favorable"
      "→ Impact stable pour la France" → "Stable"
    """
    if not france_text:
        return None

    # Normalise le texte
    text_lower = france_text.lower()

    # Détecte le jugement
    if "favorable" in text_lower:
        return "Favorable"
    elif "défavorable" in text_lower:
        return "Dégradé"
    elif "stable" in text_lower:
        return "Stable"

    return None


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

    # Extrait le scénario le plus probable
    best_scenario = get_most_probable_scenario(scenarios)
    kind, pct = best_scenario if best_scenario[0] else (None, None)

    # Extrait france_impact du scénario le plus probable
    france_impact = extract_france_impact(text, kind) if kind else None

    return {
        "iso_date": iso_date,
        "title": title,
        "question": question,
        "scenario_kind": kind,
        "scenario_pct": pct,
        "france_impact": france_impact,
        "domain": domain,
    }


def format_date_display(iso_date):
    """Convertit AAAA-MM-JJ en JJ.MM.AAAA."""
    parts = iso_date.split("-")
    return f"{parts[2]}.{parts[1]}.{parts[0]}"


def get_scenario_label(kind):
    """Retourne le label lisible du scénario."""
    labels = {
        "favorable": "Favorable",
        "stable": "Stable",
        "degrade": "Dégradé",
    }
    return labels.get(kind, kind)


def render_table_row(article):
    """Rend une ligne du tableau avec 5 colonnes: Date | Domaine | Titre | Notre scénario | Quel impact pour la France."""
    domain_label = DOMAIN_LABELS.get(article["domain"], article["domain"])

    # Notre scénario : badge de couleur + % SEULEMENT (pas de texte du scénario)
    kind = article["scenario_kind"]
    pct = article["scenario_pct"]

    if kind and pct:
        scenario_label = get_scenario_label(kind)
        # Badge de couleur avec SEULEMENT le label et le pourcentage
        eval_html = f'''<span class="eval-badge eval-{kind}" data-kind="{kind}">
      <span class="eval-label">{scenario_label}</span>
      <span class="eval-pct">{pct}%</span>
    </span>'''
    else:
        eval_html = "<span class=\"eval-badge\">?</span>"

    # France Impact : badge de couleur avec SEULEMENT le jugement (pas le texte complet)
    france_text = article["france_impact"]
    france_judgment = extract_france_judgment(france_text)

    if france_judgment:
        # Mappe le jugement à une classe CSS compatible
        judgment_kind = france_judgment.lower()
        if judgment_kind == "favorable":
            judgment_class = "france-favorable"
        elif judgment_kind == "dégradé":
            judgment_class = "france-degrade"
        else:
            judgment_class = "france-stable"
        france_html = f'<span class="france-badge {judgment_class}">{france_judgment}</span>'
    else:
        france_html = "<span class=\"france-badge\">?</span>"

    # Lien EN (toujours ajouter le badge)
    en_link = f' <a href="en/archives/{article["iso_date"]}.html" title="Read in English" class="lang-badge">EN</a>'

    # Ordre simplifiée : Date | Domaine | Titre | Notre scénario | Quel impact pour la France
    return f"""    <tr>
      <td class="col-date">{format_date_display(article["iso_date"])}</td>
      <td class="col-domain">{domain_label}</td>
      <td class="col-title"><a href="archives/{article["iso_date"]}.html">{html.escape(article["title"])}</a>{en_link}</td>
      <td class="col-eval">{eval_html}</td>
      <td class="col-france">{france_html}</td>
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
        <th style="width: 140px;">Domaine</th>
        <th style="flex: 1; min-width: 300px;">Titre</th>
        <th style="width: 140px;">Notre scénario</th>
        <th style="width: 140px;">Quel impact pour la France</th>
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
    <p class="dek">{len(articles)} éditions de Scénario — chacune analyse un sujet d'actualité avec 3 scénarios chiffrés : favorable, stable, dégradé. Cliquez sur le titre pour voir l'analyse complète.</p>
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
