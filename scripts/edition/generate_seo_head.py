"""
Génère automatiquement le <head> SEO optimisé à partir du brief éditorial.

Intégré à generate_post_edition.py, après génération de l'édition, avant d'écrire index.html.
Prend le brief JSON (editorial-briefs/{date}.json) et produit un <head> complet :
  - <title>, meta description, canonical, hreflang
  - Open Graph (og:*), Twitter Cards (twitter:*)
  - Schema.org : NewsArticle, Organization, WebSite, BreadcrumbList
  - Article metadata (author, dates, section, domain)

Tout hardcodé (règles + données du brief) — aucun modèle AI.
"""
import json
import html
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BRIEFS_DIR = REPO_ROOT / "editorial-briefs"
AUTHOR = "Olivier Bertrand"
SITE_NAME = "Scénario"
SITE_URL = "https://lesscenarios.fr"
SOCIAL_TWITTER = "@scenario_fr"
LOGO_URL = f"{SITE_URL}/assets/logo-512.png"
LOCALE_FR = "fr_FR"
DOMAIN_MAPPING = {
    "economie-mondiale": "Économie Mondiale",
    "sciences": "Sciences",
    "sciences-environnement": "Sciences & Environnement",
    "geopolitique": "Géopolitique",
    "tech": "Technologie",
    "sante": "Santé",
}

_JOURS_FR = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def _normalize_domain(domain: str) -> str:
    """Maps technical domain to display section name."""
    return DOMAIN_MAPPING.get(domain, domain.replace("-", " ").title())


def _escape_json_string(s: str) -> str:
    """Échappe les caractères spéciaux JSON (guillemets, backslash, etc.)."""
    return json.dumps(s)[1:-1]  # json.dumps() ajoute les guillemets, on les retire


def _build_title(brief: Dict[str, Any]) -> str:
    """Title: titre_propose + " — Scénario"."""
    titre = brief.get("sujet", {}).get("titre_propose", "Scénario")
    return f"{titre} — {SITE_NAME}" if titre else SITE_NAME


def _build_description(brief: Dict[str, Any]) -> str:
    """Meta description: question_posee (max 160 chars)."""
    question = brief.get("sujet", {}).get("question_posee", "")
    if len(question) > 160:
        question = question[:157] + "…"
    return question


def _build_h1(brief: Dict[str, Any]) -> str:
    """H1 for schema: h1 from brief."""
    return brief.get("sujet", {}).get("h1", "")


def _build_canonical_url(date: str) -> str:
    """Canonical URL: archive du jour."""
    return f"{SITE_URL}/archives/{date}.html"


def _build_social_image_url(date: str) -> str:
    """Social image: assets/social/instagram/{date}.png."""
    return f"{SITE_URL}/assets/social/instagram/{date}.png"


def _build_og_tags(brief: Dict[str, Any], date: str) -> str:
    """Open Graph tags."""
    canonical = _build_canonical_url(date)
    title = _build_title(brief)
    description = _build_description(brief)
    image_url = _build_social_image_url(date)
    h1 = _build_h1(brief)

    tags = [
        f'<meta property="og:type" content="article">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:locale" content="{LOCALE_FR}">',
        f'<meta property="og:url" content="{canonical}">',
        f'<meta property="og:title" content="{html.escape(title)}">',
        f'<meta property="og:description" content="{html.escape(description)}">',
        f'<meta property="og:image" content="{image_url}">',
        f'<meta property="og:image:width" content="1080">',
        f'<meta property="og:image:height" content="1080">',
        f'<meta property="og:image:alt" content="Photo d\'illustration — {html.escape(h1)}">',
        f'<meta property="og:image:type" content="image/png">',
    ]
    return "\n".join(tags)


def _build_article_tags(brief: Dict[str, Any], date: str) -> str:
    """Article-specific meta tags (author, timestamps, section)."""
    domain = brief.get("domain", brief.get("registre", ""))
    section = _normalize_domain(domain)
    dt = datetime.strptime(date, "%Y-%m-%d")
    iso_time = dt.isoformat() + "+02:00"

    tags = [
        f'<meta property="article:author" content="{AUTHOR}">',
        f'<meta property="article:published_time" content="{iso_time}">',
        f'<meta property="article:modified_time" content="{iso_time}">',
        f'<meta property="article:section" content="{section}">',
        f'<meta name="domain" content="{domain}">',
    ]
    return "\n".join(tags)


def _build_twitter_tags(brief: Dict[str, Any]) -> str:
    """Twitter Card tags."""
    title = _build_title(brief)
    description = _build_description(brief)
    image_url = _build_social_image_url(brief.get("date", ""))

    tags = [
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:site" content="{SOCIAL_TWITTER}">',
        f'<meta name="twitter:title" content="{html.escape(title)}">',
        f'<meta name="twitter:description" content="{html.escape(description)}">',
        f'<meta name="twitter:image" content="{image_url}">',
    ]
    return "\n".join(tags)


def _build_newsarticle_schema(brief: Dict[str, Any], date: str) -> str:
    """Schema.org NewsArticle (JSON-LD)."""
    title = _build_title(brief)
    h1 = _build_h1(brief)
    description = _build_description(brief)
    canonical = _build_canonical_url(date)
    image_url = _build_social_image_url(date)
    dt = datetime.strptime(date, "%Y-%m-%d")
    iso_time = dt.isoformat() + "+02:00"
    domain = brief.get("domain", brief.get("registre", ""))
    section = _normalize_domain(domain)

    schema = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "headline": h1,
        "description": description,
        "image": [image_url],
        "datePublished": iso_time,
        "dateModified": iso_time,
        "inLanguage": "fr-FR",
        "author": {"@type": "Person", "name": AUTHOR},
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "logo": {"@type": "ImageObject", "url": LOGO_URL, "width": 512, "height": 512},
        },
        "articleSection": section,
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def _build_organization_schema() -> str:
    """Schema.org Organization (JSON-LD)."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": SITE_URL,
        "logo": LOGO_URL,
        "description": "Chaque jour, les trois scénarios de demain : un à court terme, un à moyen terme, un à long terme.",
        "sameAs": [
            "https://www.linkedin.com/company/136694258/",
            "https://www.facebook.com/share/1LuiQ1cAmt/",
        ],
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def _build_website_schema() -> str:
    """Schema.org WebSite (JSON-LD) — pour SearchAction (search box) optionnel."""
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL,
        "description": "Les trois scénarios du jour : court, moyen et long terme.",
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def _build_breadcrumblist_schema(date: str, brief: Dict[str, Any]) -> str:
    """Schema.org BreadcrumbList (JSON-LD)."""
    domain = brief.get("domain", brief.get("registre", ""))
    section = _normalize_domain(domain)
    dt = datetime.strptime(date, "%Y-%m-%d")
    jour_fr = _JOURS_FR[dt.weekday()]

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Accueil",
                "item": SITE_URL,
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Archives",
                "item": f"{SITE_URL}/archives",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": section,
                "item": f"{SITE_URL}/archives?domain={domain}",
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": f"{date} ({jour_fr})",
                "item": _build_canonical_url(date),
            },
        ],
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def generate_seo_head(brief_dict: Dict[str, Any]) -> str:
    """
    Génère le <head> HTML complet avec tous les tags SEO.

    Args:
        brief_dict: Brief JSON parsé (from editorial-briefs/{date}.json)

    Returns:
        String du <head> completo, incluant <head> et </head>
    """
    date = brief_dict.get("date", "")
    if not date:
        raise ValueError("Brief must contain 'date' field")

    canonical = _build_canonical_url(date)
    title = _build_title(brief_dict)
    description = _build_description(brief_dict)

    # Validations rapides
    if not description:
        raise ValueError("Brief must contain sujet.question_posee for meta description")
    if len(description) > 160:
        description = description[:157] + "…"

    head_parts = [
        "<head>",
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{html.escape(title)}</title>",
        f'<link rel="canonical" href="{canonical}">',
        f'<link rel="alternate" hreflang="fr" href="{canonical}">',
        f'<link rel="alternate" hreflang="en" href="{SITE_URL}/en/archives/{date}.html">',
        f'<link rel="alternate" hreflang="x-default" href="{canonical}">',
        f'<meta name="description" content="{html.escape(description)}">',
        '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">',
        '<meta name="language" content="fr-FR">',
        '<meta name="color-scheme" content="dark">',
        _build_og_tags(brief_dict, date),
        _build_article_tags(brief_dict, date),
        _build_twitter_tags(brief_dict),
        f'<script type="application/ld+json">\n{_build_newsarticle_schema(brief_dict, date)}\n</script>',
        f'<script type="application/ld+json">\n{_build_organization_schema()}\n</script>',
        f'<script type="application/ld+json">\n{_build_website_schema()}\n</script>',
        f'<script type="application/ld+json">\n{_build_breadcrumblist_schema(date, brief_dict)}\n</script>',
        "</head>",
    ]

    return "\n".join(head_parts)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate SEO <head> from brief JSON")
    parser.add_argument("--date", required=True, help="Date du brief (AAAA-MM-JJ)")
    parser.add_argument("--output", help="Fichier de sortie (défaut: stdout)")
    args = parser.parse_args()

    brief_path = BRIEFS_DIR / f"{args.date}.json"
    if not brief_path.exists():
        raise FileNotFoundError(f"Brief not found: {brief_path}")

    brief_dict = json.loads(brief_path.read_text(encoding="utf-8"))
    head_html = generate_seo_head(brief_dict)

    if args.output:
        Path(args.output).write_text(head_html + "\n", encoding="utf-8")
        print(f"SEO <head> written to {args.output}")
    else:
        print(head_html)


if __name__ == "__main__":
    main()
