#!/usr/bin/env python3
"""
Régénère les articles avec les optimisations SEO pour Google News.
"""

import json
import re
from pathlib import Path

# Import du module build_html
import sys
sys.path.insert(0, str(Path(__file__).parent / "scripts/edition"))
import build_html

# Dates des articles à régénérer (uniquement celles avec content.json)
DATES = ["2026-09-22", "2026-09-23", "2026-09-24"]

def extract_domain_from_html(html_path):
    """Extrait le domain de l'article existant"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'<meta name="domain" content="([^"]+)"', content)
        return match.group(1) if match else None
    except:
        return None

def load_content(date_str):
    """Charge le contenu JSON pour une date donnée"""
    content_path = Path(f"editorial-previews/{date_str}.content.json")
    if not content_path.exists():
        print(f"  ⚠️  Fichier content non trouvé: {content_path}")
        return None
    try:
        with open(content_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  ⚠️  Erreur lecture content: {e}")
        return None

def build_brief_from_domain(domain):
    """Crée un brief minimal avec le domain nécessaire"""
    return {
        "sujet": {
            "domain": domain,
            "eyebrow": domain.replace("-", " ").title()
        }
    }

def regenerate_article(date_str):
    """Régénère un article avec les nouvelles métadonnées SEO"""
    print(f"\n📝 Régénération: {date_str}")

    # Chemins
    archive_path = Path(f"archives/{date_str}.html")
    if not archive_path.exists():
        print(f"  ✗ Article not found: {archive_path}")
        return False

    # Extraire le domain de l'article existant
    domain = extract_domain_from_html(archive_path)
    if not domain:
        print(f"  ✗ Domain non trouvé dans {date_str}.html")
        return False
    print(f"  ✓ Domain: {domain}")

    # Charger le contenu JSON
    content = load_content(date_str)
    if not content:
        return False

    # Créer le brief
    brief = build_brief_from_domain(domain)

    # Construire la canonical URL
    canonical_url = f"https://lesscenarios.fr/archives/{date_str}.html"

    # Générer le nouvel en-tête avec build_head_dynamic
    try:
        head_dynamic = build_html.build_head_dynamic(
            content,
            brief,
            date_str,
            canonical_url,
            photo=None
        )
        print(f"  ✓ Head dynamique généré")
    except Exception as e:
        print(f"  ✗ Erreur génération head: {e}")
        return False

    # Lire l'article existant
    try:
        with open(archive_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"  ✗ Erreur lecture article: {e}")
        return False

    # Trouver la fin du head dynamique
    # On cherche la première balise link/meta statique (favicon, manifest, etc)
    static_start_patterns = [
        r'<link[^>]*logo\.svg',
        r'<link[^>]*manifest\.webmanifest',
        r'<link[^>]*apple-touch-icon',
    ]

    static_start_pos = None
    for pattern in static_start_patterns:
        match = re.search(pattern, html_content)
        if match:
            static_start_pos = match.start()
            break

    if static_start_pos is None:
        print(f"  ✗ Marqueur de début des tags statiques non trouvé")
        return False

    # Trouver le début du head
    head_start_match = re.search(r'<head>', html_content)
    if not head_start_match:
        print(f"  ✗ <head> non trouvé")
        return False

    head_start_pos = head_start_match.end()

    # Garder le DOCTYPE et l'ouverture du head
    head_prefix = html_content[:head_start_pos] + "\n"

    # Garder les tags statiques et le reste du document
    static_suffix = html_content[static_start_pos:]

    # Nouveau contenu du head
    new_html = head_prefix + head_dynamic + "\n" + static_suffix

    # Sauvegarder l'article régénéré
    try:
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"  ✓ Article régénéré")
        return True
    except Exception as e:
        print(f"  ✗ Erreur sauvegarde: {e}")
        return False

def verify_metadata(date_str):
    """Vérifie que les métadonnées optimisées sont présentes"""
    archive_path = Path(f"archives/{date_str}.html")
    try:
        with open(archive_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        checks = [
            ('robots', r'robots.*index.*follow'),
            ('language', r'language.*fr-FR'),
            ('color-scheme', r'color-scheme.*dark'),
            ('og:url (article)', f'og:url.*archives/{date_str}'),
            ('article:author (Olivier)', r'article:author.*Olivier.*Bertrand'),
            ('article:section', r'article:section'),
            ('twitter:site', r'twitter:site.*scenario_fr'),
        ]

        ok_count = 0
        for name, pattern in checks:
            if re.search(pattern, html_content):
                print(f"    ✓ {name}")
                ok_count += 1
            else:
                print(f"    ✗ {name}")

        return ok_count == len(checks)
    except Exception as e:
        print(f"  ✗ Erreur vérification: {e}")
        return False

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "RÉGÉNÉRATION DES ARTICLES - SEO GOOGLE NEWS" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝")

    success_count = 0

    for date_str in DATES:
        if regenerate_article(date_str):
            print(f"  Vérification des métadonnées:")
            if verify_metadata(date_str):
                success_count += 1
                print(f"  ✓ Article {date_str} optimisé avec succès\n")
            else:
                print(f"  ⚠️  Vérification partielle\n")

    print("═" * 80)
    print(f"✓ Résumé: {success_count}/{len(DATES)} articles régénérés avec succès")
    print("═" * 80)

    if success_count == len(DATES):
        print("\n🎉 Tous les articles ont été régénérés avec les optimisations SEO!")
        print("\nProchaines étapes:")
        print("  1. git diff archives/  (vérifier les changements)")
        print("  2. git add archives/")
        print("  3. git commit -m 'Optimisation SEO: régénérer articles avec métadonnées Google News'")
        print("  4. git push")
        print("  5. Recharger sitemap-news.xml dans Google Search Console")
    else:
        print(f"\n⚠️  {len(DATES) - success_count} article(s) n'ont pas pu être régénérés")

if __name__ == "__main__":
    main()
