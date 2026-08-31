#!/usr/bin/env python3
"""Ajoute les balises <meta name="domain"> à tous les fichiers articles.

Ce script:
1. Lit map_domains.py pour obtenir le mapping domaine de chaque article
2. Pour chaque article, ajoute <meta name="domain" content="...">
   après la ligne <meta name="description" content="...">
"""
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[2]
ARCHIVES_DIR = ROOT / "archives"
ARCHIVES_HTML = ROOT / "archives.html"

# Mapping entre tags thématiques et domaines
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
    article_tags = {}
    for entry_match in re.finditer(
        r'<a class="entry-title" href="archives/(\d{4}-\d{2}-\d{2})\.html">([^<]+)</a>.*?<div class="entry-tags">(.*?)</div>',
        text,
        re.DOTALL,
    ):
        iso_date = entry_match.group(1)
        tags_html = entry_match.group(3)
        theme_tags = re.findall(r'class="tag theme"[^>]*data-tag="([^"]+)"', tags_html)
        article_tags[iso_date] = theme_tags
    return article_tags


def map_article_domain(theme_tags):
    """Mappe une liste de tags thématiques à un domaine."""
    if not theme_tags:
        return None
    domains = []
    for tag in theme_tags:
        domain = TAG_TO_DOMAIN.get(tag)
        if domain:
            domains.append(domain)
    if not domains:
        return None
    counts = Counter(domains)
    return counts.most_common(1)[0][0]


def add_domain_to_article(file_path, domain):
    """Ajoute le meta tag domain à un fichier article."""
    text = file_path.read_text(encoding="utf-8")

    # Cherche la ligne <meta name="description" content="...">
    # et ajoute la meta domain juste après
    pattern = (
        r'(<meta name="description" content="[^"]*">\n)'
    )
    replacement = rf'\1<meta name="domain" content="{domain}">\n'

    # Vérifie que la meta domain n'existe pas déjà
    if re.search(r'<meta name="domain"', text):
        return False, "Domain meta tag already exists"

    new_text = re.sub(pattern, replacement, text)

    if new_text == text:
        return False, "Could not find description meta tag to insert after"

    # Écrit le fichier modifié
    file_path.write_text(new_text, encoding="utf-8")
    return True, "Added"


def main():
    """Ajoute les meta domain tags à tous les articles."""
    article_tags = extract_article_tags()

    added = 0
    skipped = 0

    print(f"Ajout des meta domain tags à {len(article_tags)} articles...")
    print()

    for iso_date in sorted(article_tags.keys(), reverse=True):
        tags = article_tags[iso_date]
        domain = map_article_domain(tags)

        if not domain:
            print(f"⚠ {iso_date} → SKIP (no domain mapped)")
            skipped += 1
            continue

        file_path = ARCHIVES_DIR / f"{iso_date}.html"
        if not file_path.exists():
            print(f"✗ {iso_date} → FILE NOT FOUND")
            skipped += 1
            continue

        success, message = add_domain_to_article(file_path, domain)
        if success:
            print(f"✓ {iso_date} → {domain:30} {message}")
            added += 1
        else:
            print(f"✗ {iso_date} → {domain:30} {message}")
            skipped += 1

    print()
    print(f"✓ Added to {added} articles")
    print(f"⚠ Skipped {skipped} articles")


if __name__ == "__main__":
    main()
