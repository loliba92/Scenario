#!/usr/bin/env python3
"""Crée un mapping domaine pour les 39 articles basé sur leurs tags thématiques
dans archives.html.

Ce script lit archives.html, extrait les tags theme pour chaque article,
puis propose un domaine basé sur les domaines définis dans generate_theme_pages.py.
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
ARCHIVES_HTML = ROOT / "archives.html"
ARCHIVES_DIR = ROOT / "archives"

# Mapping entre tags thématiques et domaines
# (cf. generate_theme_pages.py)
TAG_TO_DOMAIN = {
    # Économie & entreprises
    "economie": "economie-entreprises",
    "entreprises": "economie-entreprises",
    "emploi": "economie-entreprises",
    # Politique & institutions
    "politique": "politique-institutions",
    "justice": "politique-institutions",
    # International
    "diplomatie": "international",
    "defense": "international",
    "immigration": "international",
    # Sciences & environnement
    "energie": "sciences-environnement",
    "climat": "sciences-environnement",
    "sante": "sciences-environnement",
    "espace": "sciences-environnement",
    # Tech & numérique
    "intelligence-artificielle": "tech-numerique",
    "numerique": "tech-numerique",
    # Culture & divertissement
    "cinema": "culture-divertissement",
    "musique": "culture-divertissement",
    "jeux-video": "culture-divertissement",
    "litterature": "culture-divertissement",
    "medias": "culture-divertissement",
}


def extract_article_tags():
    """Extrait les tags thématiques pour chaque article d'archives.html."""
    text = ARCHIVES_HTML.read_text(encoding="utf-8")

    # Cherche chaque <li class="entry">
    article_tags = {}

    for entry_match in re.finditer(
        r'<a class="entry-title" href="archives/(\d{4}-\d{2}-\d{2})\.html">([^<]+)</a>.*?<div class="entry-tags">(.*?)</div>',
        text,
        re.DOTALL,
    ):
        iso_date = entry_match.group(1)
        tags_html = entry_match.group(3)

        # Extrait tous les theme tags (ceux avec class="tag theme")
        theme_tags = re.findall(r'class="tag theme"[^>]*data-tag="([^"]+)"', tags_html)

        article_tags[iso_date] = theme_tags

    return article_tags


def map_article_domain(theme_tags):
    """Mappe une liste de tags thématiques à un domaine.
    Retourne le domaine le plus approprié ou None.
    """
    if not theme_tags:
        return None

    # Mappe chaque tag à son domaine
    domains = []
    for tag in theme_tags:
        domain = TAG_TO_DOMAIN.get(tag)
        if domain:
            domains.append(domain)

    if not domains:
        return None

    # Retourne le domaine le plus fréquent, ou le premier si égalité
    from collections import Counter
    counts = Counter(domains)
    return counts.most_common(1)[0][0]


def main():
    """Crée et affiche le mapping domaine pour chaque article."""
    article_tags = extract_article_tags()

    print(f"Mapping {len(article_tags)} articles aux domaines...")
    print()

    mapping = {}
    domain_groups = defaultdict(list)

    for iso_date in sorted(article_tags.keys(), reverse=True):
        tags = article_tags[iso_date]
        domain = map_article_domain(tags)
        mapping[iso_date] = domain

        if domain:
            domain_groups[domain].append(iso_date)
            print(f"✓ {iso_date} → {domain:30} tags: {', '.join(tags)}")
        else:
            domain_groups["UNMATCHED"].append(iso_date)
            print(f"⚠ {iso_date} → UNMATCHED                    tags: {', '.join(tags)}")

    print()
    print("Résumé par domaine:")
    for domain in sorted(domain_groups.keys()):
        count = len(domain_groups[domain])
        print(f"  {domain:30} {count:2} articles")

    return mapping, article_tags


if __name__ == "__main__":
    main()
