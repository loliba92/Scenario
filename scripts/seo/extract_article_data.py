#!/usr/bin/env python3
"""Extrait les données structurées de toutes les pages d'archives pour reconstruction
automatique d'archives.html.

Ce script parse les fichiers archives/{AAAA-MM-JJ}.html et extrait:
- Titre
- Problématique (question)
- Scénario le plus probable + pourcentage
- Données France Impact
- Domaine thématique (via meta name="domain")

Usage: python3 scripts/seo/extract_article_data.py
"""
import re
import html
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
ARCHIVES_DIR = ROOT / "archives"

# Domaines valides (cf. scripts/seo/generate_theme_pages.py)
DOMAINS = [
    "economie-entreprises",
    "politique-institutions",
    "international",
    "sciences-environnement",
    "tech-numerique",
    "culture-divertissement",
]


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
    """Extrait les scénarios avec leurs pourcentages.
    Retourne une liste de tuples (kind, percentage, title).
    """
    scenarios = []
    # Cherche tous les <article class="card" data-kind="...">
    for card_match in re.finditer(
        r'<article class="card" data-kind="([^"]+)"[^>]*>(.*?)</article>', text, re.DOTALL
    ):
        kind = card_match.group(1)
        card_content = card_match.group(2)

        # Extrait le pourcentage
        pct_m = re.search(r'<div class="gauge-num">(\d+)%</div>', card_content)
        percentage = int(pct_m.group(1)) if pct_m else 0

        # Extrait le titre du scénario (h3 après kind-tag)
        title_m = re.search(r"<h3>([^<]+)</h3>", card_content)
        title = title_m.group(1).strip() if title_m else ""

        scenarios.append((kind, percentage, title))

    return scenarios


def extract_france_impact(text):
    """Extrait la donnée France Impact (texte après 'Concrètement en France')."""
    # Cherche la section france-line et son contenu
    m = re.search(
        r'<div class="france-line">.*?<span class="field-label">Concrètement en France</span>\s*([^<]+)',
        text,
        re.DOTALL,
    )
    if m:
        return html.unescape(m.group(1).strip())
    return None


def extract_domain(text):
    """Extrait le domaine de la meta tag <meta name="domain" content="...">."""
    m = re.search(r'<meta name="domain" content="([^"]+)">', text)
    if m:
        return m.group(1)
    return None


def get_most_probable_scenario(scenarios):
    """Retourne le scénario avec le pourcentage le plus élevé."""
    if not scenarios:
        return None, None, None
    best = max(scenarios, key=lambda x: x[1])
    return best


def parse_article(file_path):
    """Parse un fichier d'article et retourne ses données."""
    text = file_path.read_text(encoding="utf-8")

    iso_date = file_path.stem
    title = extract_title(text)
    question = extract_question(text)
    scenarios = extract_scenarios(text)
    france_impact = extract_france_impact(text)
    domain = extract_domain(text)

    # Récupère le scénario le plus probable
    kind, pct, scenario_title = get_most_probable_scenario(scenarios)

    return {
        "iso_date": iso_date,
        "title": title,
        "question": question,
        "scenario_kind": kind,
        "scenario_pct": pct,
        "scenario_title": scenario_title,
        "all_scenarios": scenarios,
        "france_impact": france_impact,
        "domain": domain if domain in DOMAINS else None,
        "file_path": file_path,
    }


def main():
    """Parse tous les articles et affiche les résultats."""
    articles = []

    # Collecte tous les fichiers archives/{AAAA-MM-JJ}.html
    article_files = sorted(ARCHIVES_DIR.glob("*.html"), reverse=True)

    print(f"Parsing {len(article_files)} articles...")
    print()

    for file_path in article_files:
        data = parse_article(file_path)
        articles.append(data)

        # Affiche un résumé pour chaque article
        status = "✓" if all([data["title"], data["domain"]]) else "⚠"
        domain_str = data["domain"] or "MISSING"
        pct_str = f"{data['scenario_pct']}%" if data["scenario_pct"] else "?"
        print(
            f"{status} {data['iso_date']} | {domain_str:25} | {pct_str:5} | {data['title'][:50]}"
        )

        if not data["domain"]:
            print(f"  ⚠ MISSING domain - add <meta name=\"domain\" content=\"...\">")

    print()
    print(f"Total: {len(articles)} articles")
    missing_domain = sum(1 for a in articles if not a["domain"])
    print(f"Missing domain metadata: {missing_domain}")

    return articles


if __name__ == "__main__":
    main()
