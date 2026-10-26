"""
Génération automatique de métadonnées SEO optimisées pour chaque édition.

Responsabilités :
  1. Title SEO — incluire les termes clés du domaine + H1
  2. Meta description — 155-160 caractères, avec mots-clés en longue traîne
  3. Keywords — liste des termes pertinents pour le contenu
  4. JSON-LD enrichi — NewsArticle avec keywords + BreadcrumbList
  5. Liens internes — identifier et lier vers glossaire + sources clés

Intégré dans generate_daily_edition.py après rédaction, avant build_html.py.
"""

import json
import re
from datetime import datetime
from typing import Optional


def generate_seo_title(h1: str, domain: str, keywords: list[str]) -> str:
    """
    Génère le titre SEO d'une édition à partir de son h1 court (celui affiché sur la page).

    Règle partagée avec generate_seo_head.py (titre_depuis_h1) : jusqu'à 59 caractères avec la marque,
    jusqu'à 90 sans, jamais de coupure « … » en plein mot au-delà.

    Args:
        h1: Le titre principal affiché sur la page
        domain: Catégorie de l'article (non utilisée pour l'instant)
        keywords: Liste de mots-clés du contenu (non utilisée pour l'instant)

    Returns:
        Titre SEO
    """
    from generate_seo_head import SITE_NAME, _truncate_at_word_boundary, titre_depuis_h1

    du_h1 = titre_depuis_h1(h1)
    if du_h1:
        return du_h1
    return f"{_truncate_at_word_boundary(h1.strip(), 59)} — {SITE_NAME}"


def generate_seo_description(
    h1: str,
    section_title: str,
    question: str,
    keywords: list[str],
    domain: str,
) -> str:
    """
    Génère une meta description optimisée.

    Format : 155-160 caractères
    Stratégie :
      1. Utiliser la question (accroche) si disponible
      2. Ajouter 1-2 mots-clés principaux en contexte
      3. Terminer par domaine (ex: "Analyse et scénarios prospectifs pour 2030")

    Args:
        h1: Titre H1
        section_title: Titre de la section scénarios
        question: La question éditoriale centrale
        keywords: Liste de termes clés
        domain: Domaine (sciences, politique, etc.)

    Returns:
        Meta description (155-160 chars)
    """
    # Commencer par la question si elle est < 100 caractères
    if question and len(question) < 100:
        desc = question
    else:
        # Fallback : résumé du section_title
        desc = section_title[:80]

    # Ajouter contexte de domaine et horizon temporel
    domain_context = {
        "sciences": "Analyse fondée sur données scientifiques.",
        "politique": "Analyse prospective pour 2030.",
        "economie": "Analyse économique et scénarios.",
        "geopolitique": "Enjeux géopolitiques et scénarios prospectifs.",
    }

    context_suffix = domain_context.get(domain, "3 scénarios prospectifs pour 2030.")

    # Assembler description (cible 155-160)
    full_desc = f"{desc} {context_suffix}"

    # Truncate à 160 si nécessaire
    if len(full_desc) > 160:
        full_desc = full_desc[:157] + "..."

    return full_desc


def generate_keywords(
    h1: str,
    domain: str,
    content_snippet: str = "",
) -> list[str]:
    """
    Génère une liste de mots-clés pertinents.

    Extrait :
      - Noms propres du H1 (marques, lieux, personnes)
      - Termes du domaine
      - Variantes longue traîne

    Limite : 10-15 termes
    """
    keywords = set()

    # 1. Extraire noms propres (majuscules en début ou acronymes)
    proper_nouns = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", h1)
    keywords.update(proper_nouns[:5])

    # 2. Ajouter le domaine
    domain_keywords = {
        "sciences": ["santé", "recherche", "innovation", "étude scientifique"],
        "politique": ["élections", "politique", "gouvernement", "débat public"],
        "economie": ["marché", "économie", "prix", "inflation", "investissement"],
        "geopolitique": ["géopolitique", "international", "tensions", "alliances"],
    }
    keywords.update(domain_keywords.get(domain, []))

    # 3. Ajouter termes spécialisés si disponibles
    if content_snippet:
        # Extraire termes entre guillemets
        quoted = re.findall(r'"([^"]+)"', content_snippet)
        keywords.update(quoted[:3])

    # Retourner liste unique, max 15 termes
    return list(keywords)[:15]


def generate_newsarticle_json(
    headline: str,
    description: str,
    image_url: str,
    date_published: str,
    domain: str,
    keywords: list[str],
    author_name: str = "Olivier Bertrand",
) -> str:
    """
    Génère le JSON-LD NewsArticle complet avec keywords.

    Retourne le JSON brut (sera inséré dans <script type="application/ld+json">)
    """

    # Formater date ISO
    try:
        dt = datetime.fromisoformat(date_published.replace("Z", "+00:00"))
        iso_date = dt.isoformat()
    except:
        iso_date = date_published

    # Mapper domaine → section
    section_map = {
        "sciences": "Sciences",
        "politique": "Politique",
        "economie": "Économie",
        "geopolitique": "Géopolitique",
        "sport": "Sport",
    }
    section = section_map.get(domain, "Actualité")

    article = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://lesscenarios.fr/archives/{date_published[:10]}.html",
        },
        "headline": headline,
        "description": description,
        "image": [image_url],
        "datePublished": iso_date,
        "dateModified": iso_date,
        "inLanguage": "fr-FR",
        "keywords": ", ".join(keywords),
        "author": {"@type": "Person", "name": author_name},
        "publisher": {
            "@type": "Organization",
            "name": "Scénario",
            "logo": {
                "@type": "ImageObject",
                "url": "https://lesscenarios.fr/assets/logo-512.png",
                "width": 512,
                "height": 512,
            },
        },
        "articleSection": section,
    }

    return json.dumps(article, ensure_ascii=False, indent=2)


def generate_breadcrumb_json(
    date_str: str,
    article_title: str,
) -> str:
    """
    Génère le JSON-LD BreadcrumbList pour navigation hiérarchique.

    Retourne le JSON brut (sera inséré dans <script type="application/ld+json">)
    """
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Scénario",
                "item": "https://lesscenarios.fr/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Archives",
                "item": "https://lesscenarios.fr/archives.html",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": article_title,
                "item": f"https://lesscenarios.fr/archives/{date_str}.html",
            },
        ],
    }

    return json.dumps(breadcrumb, ensure_ascii=False, indent=2)


def generate_seo_metadata(
    brief: dict,
    domain: str,
    h1_court: Optional[str] = None,
) -> dict:
    """
    Fonction principale : prend le brief éditorial et retourne toutes
    les métadonnées SEO optimisées.

    Args:
        brief: Dictionnaire du brief (structure editorial standard de generate_daily_edition.py)
        domain: Catégorie (sciences, politique, etc.)
        h1_court: h1 affiché sur la page (content["h1"]) : sert de titre SEO s'il existe, sinon le h1 du brief

    Returns:
        dict {
            "title": str,
            "meta_description": str,
            "keywords": list[str],
            "newsarticle_json": str,
            "breadcrumb_json": str,
        }
    """
    # Adapter à la structure réelle du brief de generate_daily_edition.py
    sujet = brief.get("sujet", {})
    h1 = sujet.get("h1", "")
    question = sujet.get("question_posee", "")
    date_str = brief.get("date", "")

    # section_title n'existe pas dans le brief — utiliser h1 comme fallback
    section_title = h1

    # Récupérer un snippet du contenu pour extraction de termes
    # Dans la structure editorial, c'est dans faits_verifies et sources
    faits = brief.get("faits_verifies", [])
    sources = brief.get("sources", [])

    content_parts = [h1, question]
    for fait in faits:
        if isinstance(fait, dict) and fait.get("fait"):
            content_parts.append(fait.get("fait", ""))
    for source in sources:
        if isinstance(source, dict):
            content_parts.append(source.get("summary", ""))

    content = " ".join(content_parts)

    # Générer chaque composant
    title = generate_seo_title(h1_court or h1, domain, [])
    keywords = generate_keywords(h1, domain, content[:500])
    description = generate_seo_description(h1, section_title, question, keywords, domain)

    # JSON-LD
    image_url = f"https://lesscenarios.fr/assets/social/instagram/{date_str}.png"
    newsarticle = generate_newsarticle_json(
        headline=title,
        description=description,
        image_url=image_url,
        date_published=date_str,
        domain=domain,
        keywords=keywords,
    )
    breadcrumb = generate_breadcrumb_json(date_str, h1)

    return {
        "title": title,
        "meta_description": description,
        "keywords": keywords,
        "newsarticle_json": newsarticle,
        "breadcrumb_json": breadcrumb,
    }


if __name__ == "__main__":
    # Test rapide
    test_brief = {
        "title": "Ozempic, Wegovy : révolution médicale ou remède pour les riches ?",
        "question": "Les nouveaux traitements GLP-1 peuvent-ils enrayer l'obésité mondiale ?",
        "section_title": "Nouveaux traitements contre l'obésité : révolution ou privilège ?",
        "date": "2026-09-25",
        "context": "Novo Nordisk, Eli Lilly, semaglutide, tirzepatide, prix, remboursement",
        "facts": "FDA approval, NEJM study, market projections",
    }

    result = generate_seo_metadata(test_brief, "sciences")
    print("=== SEO Metadata ===")
    print(f"Title: {result['title']}")
    print(f"Description: {result['meta_description']}")
    print(f"Keywords: {result['keywords']}")
    print("\n=== NewsArticle JSON ===")
    print(result['newsarticle_json'])
