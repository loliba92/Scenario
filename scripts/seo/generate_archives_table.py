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
    table-layout: fixed;
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
    color: var(--paper-dim);
    white-space: nowrap;
    flex-shrink: 0;
    letter-spacing: 0.02em;
    text-align: center;
  }

  .archives-table .col-domain {
    font-size: 0.72rem;
    font-family: "JetBrains Mono", monospace;
    font-weight: 600;
    color: var(--paper-dim);
    white-space: normal;
    line-height: 1.35;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    text-align: center;
  }

  .archives-table .col-title {
    overflow-wrap: break-word;
  }

  /* Titre + lien EN alignés dans un même flex row, TOUJOURS sur une seule
     ligne (nowrap) : EN reste collé au titre au lieu de passer dessous.
     Le titre rétrécit (flex-shrink + min-width:0) pour laisser la place à
     EN plutôt que de le pousser en dessous (le titre a besoin de
     display:-webkit-box pour son clamp 2 lignes, donc on isole ça sur le <a>
     et on gère l'alignement au niveau du wrapper) */
  .archives-table .title-row {
    display: flex;
    align-items: baseline;
    gap: 8px;
    flex-wrap: nowrap;
  }

  .archives-table .col-title a:first-child {
    color: var(--gold);
    text-decoration: none;
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: 0.95rem;
    transition: color 0.2s ease;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    flex: 1 1 auto;
    min-width: 0;
  }

  .archives-table .col-title a:first-child:hover {
    color: var(--paper);
    text-decoration: underline;
  }

  /* Lien EN : simple texte discret + petite flèche, pas un badge encadré */
  .archives-table .lang-link {
    display: inline-flex;
    align-items: baseline;
    gap: 2px;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.65rem;
    color: var(--paper-dim);
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 0.04em;
    flex-shrink: 0;
    align-self: flex-start;
    transition: color 0.2s ease;
  }

  .archives-table .lang-link:hover {
    color: var(--gold);
    text-decoration: underline;
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

  /* Notre scénario : badge fond plein (donnée principale du site) */
  .archives-table .eval-badge.eval-favorable {
    background: #5e9c78;
    color: #10151c;
    border: 1px solid #5e9c78;
  }

  .archives-table .eval-badge.eval-stable {
    background: #6f8fae;
    color: #10151c;
    border: 1px solid #6f8fae;
  }

  .archives-table .eval-badge.eval-degrade {
    background: #bd6248;
    color: #10151c;
    border: 1px solid #bd6248;
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
    text-align: center;
    padding: 6px 10px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.68rem;
    font-family: "JetBrains Mono", monospace;
    line-height: 1.3;
    /* Labels plus longs ("Nettement défavorable") : on autorise le retour à
       la ligne plutôt que de forcer un débordement (contrairement au badge
       "Notre scénario" dont les labels courts restent sur une ligne). */
    white-space: normal;
    max-width: 100%;
  }

  /* Impact France : badge contour léger (donnée secondaire, pour se distinguer
     visuellement du badge "Notre scénario" en fond plein juste à côté), avec
     un dégradé d'intensité sur 7 niveaux qui reflète l'espérance pondérée des
     3 scénarios (voir FRANCE_ESPERANCE_SCALE) : extrêmement → très → plutôt →
     neutre → plutôt → très → extrêmement. */
  .archives-table .france-badge.esp-favorable-extreme {
    background: #5e9c78;
    color: #10151c;
    border: 1.5px solid #5e9c78;
  }

  .archives-table .france-badge.esp-favorable-fort {
    background: rgba(94, 156, 120, 0.16);
    color: #5e9c78;
    border: 1.5px solid #5e9c78;
  }

  .archives-table .france-badge.esp-favorable {
    background: transparent;
    color: #5e9c78;
    border: 1.5px solid rgba(94, 156, 120, 0.5);
  }

  .archives-table .france-badge.esp-neutre {
    background: transparent;
    color: #6f8fae;
    border: 1.5px solid rgba(111, 143, 174, 0.5);
  }

  .archives-table .france-badge.esp-degrade {
    background: transparent;
    color: #bd6248;
    border: 1.5px solid rgba(189, 98, 72, 0.5);
  }

  .archives-table .france-badge.esp-degrade-fort {
    background: rgba(189, 98, 72, 0.16);
    color: #bd6248;
    border: 1.5px solid #bd6248;
  }

  .archives-table .france-badge.esp-degrade-extreme {
    background: #bd6248;
    color: #10151c;
    border: 1.5px solid #bd6248;
  }

  @media (max-width: 1200px) and (min-width: 769px) {
    .archives-table {
      font-size: 0.85rem;
    }
    .archives-table th,
    .archives-table td {
      padding: 10px 10px;
    }
  }

  /* ---- Mobile (<768px) : vue carte empilée ----
     Une table à 5 colonnes ne tient pas sur un écran de téléphone : on bascule
     chaque ligne en carte verticale (titre en haut, méta, puis les 2 badges
     en ligne label/valeur). thead est masqué, l'ordre est piloté par `order`. */
  @media (max-width: 768px) {
    .archives-table {
      max-width: 100%;
      margin: 20px auto;
      box-shadow: none;
      font-size: 0.85rem;
    }

    .archives-table thead {
      display: none;
    }

    .archives-table,
    .archives-table tbody {
      display: block;
      width: 100%;
    }

    .archives-table tr {
      display: flex;
      flex-direction: column;
      padding: 16px;
      border-bottom: 1px solid var(--hairline);
    }

    .archives-table tr:last-child {
      border-bottom: none;
    }

    .archives-table td {
      padding: 0;
      border: none;
      text-align: left;
    }

    .archives-table .col-title {
      order: 1;
      padding-bottom: 8px;
    }

    .archives-table .col-date {
      order: 2;
      text-align: left;
      font-size: 0.72rem;
    }

    .archives-table .col-domain {
      order: 3;
      text-align: left;
      font-size: 0.68rem;
      margin-bottom: 10px;
    }

    .archives-table .col-eval,
    .archives-table .col-france {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-top: 1px solid var(--hairline);
      text-align: left;
    }

    .archives-table .col-eval { order: 4; }
    .archives-table .col-france { order: 5; }

    .archives-table .col-eval::before,
    .archives-table .col-france::before {
      content: attr(data-label);
      font-family: "JetBrains Mono", monospace;
      font-size: 0.62rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--paper-dim);
    }
  }

  @media (max-width: 480px) {
    .archives-table {
      margin: 16px auto;
    }
    .archives-table tr {
      padding: 14px;
    }
    .archives-table .col-title a:first-child {
      font-size: 0.88rem;
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


def _extract_card_judgment(card_content):
    """Extrait le jugement France Impact (favorable/stable/degrade) d'UN card de scénario.

    Lit d'abord l'attribut data-france-impact="..." posé sur la div .france-line
    dans le HTML source (articles récents) — plus robuste que de parser le texte,
    où "favorable" est un sous-mot de "défavorable". Pour les articles plus anciens
    qui n'ont pas cet attribut, retombe sur un parsing du jugement en toutes lettres
    ("Plutôt favorable" / "Neutre" / "Plutôt défavorable"), en testant "défavorable"
    avant "favorable" pour éviter le piège du sous-mot.
    """
    # 1) Attribut data-france-impact (articles récents, fiable)
    attr_m = re.search(r'<div class="france-line" data-france-impact="([^"]+)"', card_content)
    if attr_m:
        return attr_m.group(1)  # "favorable" | "stable" | "degrade"

    # 2) Fallback texte (articles anciens sans l'attribut)
    france_m = re.search(
        r'<div class="france-line"[^>]*>.*?<span class="field-label">Concrètement en France</span>\s*(.*?)</div>',
        card_content,
        re.DOTALL,
    )
    if not france_m:
        return None
    france_text = re.sub(r'<[^>]+>', '', france_m.group(1)).lower()
    if "défavorable" in france_text:
        return "degrade"
    if "favorable" in france_text:
        return "favorable"
    return "stable"  # "Neutre pour la France" et autres formulations stables


def extract_scenarios(text):
    """Extrait les 3 scénarios avec leur pourcentage et leur jugement France Impact respectif.

    Important : le jugement France Impact d'un card est indépendant de son "kind"
    (ex. le scénario "stable" peut très bien avoir un impact France jugé "degrade") —
    c'est justement ce qui permet de calculer une espérance pondérée plus bas.
    """
    scenarios = []
    for card_match in re.finditer(
        r'<article class="card" data-kind="([^"]+)"[^>]*>(.*?)</article>', text, re.DOTALL
    ):
        kind = card_match.group(1)
        card_content = card_match.group(2)

        pct_m = re.search(r'<div class="gauge-num">(\d+)%</div>', card_content)
        percentage = int(pct_m.group(1)) if pct_m else 0

        judgment = _extract_card_judgment(card_content)

        scenarios.append((kind, percentage, judgment))

    return scenarios


# Valeur numérique de chaque jugement pour le calcul de l'espérance pondérée
_JUDGMENT_VALUE = {"favorable": 1, "stable": 0, "degrade": -1}


def compute_france_esperance(scenarios):
    """Calcule l'espérance (valeur pondérée par les probabilités) de l'impact France.

    Chacun des 3 scénarios a un pourcentage (probabilité) et un jugement France Impact
    propre (favorable=+1, stable=0, degrade=-1). L'espérance = Σ(pct_i/100 × valeur_i),
    un score continu dans [-1, 1] — plus fidèle que de ne retenir que le jugement du
    seul scénario le plus probable, qui ignore les deux autres.
    """
    if not scenarios:
        return None
    return sum(
        (pct / 100) * _JUDGMENT_VALUE.get(judgment, 0)
        for _kind, pct, judgment in scenarios
        if judgment is not None
    )


# Barème officiel de l'espérance France Impact — SOURCE UNIQUE, documentée
# dans docs/routine-prompt.md (garder les deux synchronisés si ce barème change).
# Seuils décroissants ; le premier seuil <= value l'emporte.
FRANCE_ESPERANCE_SCALE = [
    (0.8, "Extrêmement favorable", "esp-favorable-extreme"),
    (0.4, "Très favorable", "esp-favorable-fort"),
    (0.15, "Plutôt favorable", "esp-favorable"),
    (-0.15, "Neutre", "esp-neutre"),
    (-0.4, "Plutôt défavorable", "esp-degrade"),
    (-0.8, "Très défavorable", "esp-degrade-fort"),
    (float("-inf"), "Extrêmement défavorable", "esp-degrade-extreme"),
]


def label_esperance(value):
    """Mappe l'espérance (float dans [-1, 1]) à un label nuancé + une classe CSS.

    Applique FRANCE_ESPERANCE_SCALE (7 niveaux symétriques : extrêmement / très /
    plutôt / neutre / plutôt / très / extrêmement).
    """
    if value is None:
        return None, None
    for threshold, label, css_class in FRANCE_ESPERANCE_SCALE:
        if value >= threshold:
            return label, css_class
    return None, None  # inatteignable : le dernier seuil est -inf


def extract_domain(text):
    """Extrait le domaine de la meta tag."""
    m = re.search(r'<meta name="domain" content="([^"]+)">', text)
    if m:
        return m.group(1)
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

    # Extrait le scénario le plus probable (pour le badge "Notre scénario")
    best_scenario = get_most_probable_scenario(scenarios)
    kind, pct = best_scenario if best_scenario[0] else (None, None)

    # Impact France : espérance pondérée sur les 3 scénarios, pas juste le plus probable
    esperance = compute_france_esperance(scenarios)
    france_label, france_css_class = label_esperance(esperance)

    return {
        "iso_date": iso_date,
        "title": title,
        "question": question,
        "scenario_kind": kind,
        "scenario_pct": pct,
        "france_esperance": esperance,
        "france_label": france_label,
        "france_css_class": france_css_class,
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
    """Rend une ligne du tableau avec 5 colonnes: Date | Titre | Domaine | Notre scénario | Impact France."""
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

    # Impact France : badge nuancé sur l'espérance pondérée des 3 scénarios
    # (ex. "Plutôt défavorable" si les 2 scénarios les + probables sont dégradés
    # pour la France, même quand le scénario "stable" l'emporte sur le fond)
    france_label = article["france_label"]
    france_css_class = article["france_css_class"]

    if france_label:
        france_html = f'<span class="france-badge {france_css_class}">{france_label}</span>'
    else:
        france_html = "<span class=\"france-badge\">?</span>"

    # Lien EN : lien texte discret, pas un badge encadré
    en_link = f'<a href="en/archives/{article["iso_date"]}.html" title="Read in English" class="lang-link"><span aria-hidden="true">↗</span> EN</a>'

    # data-label sur chaque <td> : utilisé par la vue carte mobile (voir CSS @media)
    # Ordre : Date puis Titre en premier (les 2 repères de nav), puis Domaine, puis les 2 badges
    return f"""    <tr>
      <td class="col-date" data-label="Date">{format_date_display(article["iso_date"])}</td>
      <td class="col-title">
        <span class="title-row">
          <a href="archives/{article["iso_date"]}.html">{html.escape(article["title"])}</a>
          {en_link}
        </span>
      </td>
      <td class="col-domain" data-label="Domaine">{domain_label}</td>
      <td class="col-eval" data-label="Notre scénario">{eval_html}</td>
      <td class="col-france" data-label="Impact France">{france_html}</td>
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
        <th style="width: 9%;">Date</th>
        <th style="width: 40%;">Titre</th>
        <th style="width: 15%;">Domaine</th>
        <th style="width: 18%;">Notre scénario</th>
        <th style="width: 18%;">Impact France</th>
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
