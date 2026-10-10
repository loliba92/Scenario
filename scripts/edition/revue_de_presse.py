"""Revue de presse automatique : une recherche web dédiée, quand le brief n'en porte aucune.

Cause racine (10 octobre 2026) : les revues de presse des 9 et 10 octobre étaient vides. Le brief de secours
(generate_fallback_brief.py) demande tout dans un seul gros appel ; le modèle économique qui l'écrit (Solar Pro 4)
consacre sa recherche aux faits de l'édition et laisse `revue_de_presse` à `[]`, ce que la règle « jamais bloquant »
autorise. Rien ne relançait la recherche : le jour disparaissait de sources.html sans aucun message.

Ici, un appel court et ciblé, avec la recherche web activée, qui ne demande QUE la revue de presse : 3 à 5 articles
du jour, sur des sujets variés, différents du sujet de l'édition. Chaque lien est contrôlé (source_links) : un lien
absent des pages réellement consultées par la recherche, ou mort, est écarté. Moins de deux articles valables :
aucune revue (jamais de lien inventé pour remplir). Jamais bloquant : toute erreur renvoie [].

Appelé par generate_post_edition.py à la publication, UNIQUEMENT si le brief n'a pas déjà de revue de presse.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime

DOMAINES = ("economie-entreprises", "politique-institutions", "international",
            "sciences-environnement", "tech-numerique", "culture-divertissement")
MODELE_DEFAUT = "upstage/solar-pro4"  # même modèle économique que le brief de repli (recherche web déjà validée)
MIN_ARTICLES, MAX_ARTICLES = 2, 5
_JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def construire_prompt(date_str: str, sujet: str) -> str:
    jour = _JOURS[datetime.strptime(date_str, "%Y-%m-%d").weekday()]
    return f"""Tu prépares la « revue de presse » du site Scénario pour le {jour} {date_str}.

Cherche sur le web 3 à 5 articles de presse publiés le {date_str} (ou la veille au soir) par des médias reconnus
(franceinfo, Le Monde, Les Echos, Le Figaro, France 24, Euronews, Reuters, AFP…), sur des sujets VARIÉS : des
domaines différents les uns des autres, et différents du sujet de l'édition du jour « {sujet or "non précisé"} ».

Règles absolues :
- `url` = l'URL EXACTE d'un résultat renvoyé par ta recherche web, copiée telle quelle. N'écris JAMAIS une URL
  reconstituée à partir d'un titre ou d'un nom de site : un lien inventé est retiré et fait perdre l'article.
- `title` = le titre exact de l'article. `source` = le nom du média.
- `summary` = 1 ou 2 phrases FACTUELLES tirées de l'article (chiffres, noms, dates). Jamais un avis, jamais un scénario.
- `domain` = un seul parmi : {", ".join(DOMAINES)}.
- `lang` = "fr", "en" ou "other". `read_minutes` = durée de lecture estimée (entier, au moins 1).
- Si tu ne trouves pas d'article vérifiable, renvoie moins d'articles ; ne comble jamais avec un article incertain.

Réponds UNIQUEMENT avec un objet JSON, sans texte autour :
{{"revue_de_presse": [{{"title": "", "source": "", "url": "", "lang": "fr", "domain": "", "summary": "", "read_minutes": 1}}]}}
"""


def nettoyer(articles, urls_citees=None, verifier=None) -> list[dict]:
    """Garde les articles complets, au domaine connu, aux liens valables (voir source_links), sans doublon."""
    from source_links import find_bad_urls
    candidats, vus = [], set()
    for a in articles or []:
        if not isinstance(a, dict):
            continue
        url = str(a.get("url") or "").strip()
        titre = str(a.get("title") or "").strip()
        resume = str(a.get("summary") or "").strip()
        if not (re.match(r"^https?://", url) and titre and resume and a.get("domain") in DOMAINES) or url in vus:
            continue
        vus.add(url)
        try:
            minutes = max(1, int(a.get("read_minutes") or 1))
        except (TypeError, ValueError):
            minutes = 1
        candidats.append({"title": titre, "source": str(a.get("source") or "").strip(), "url": url, "image": None,
                          "lang": a.get("lang") if a.get("lang") in ("fr", "en", "other") else "fr",
                          "domain": a["domain"], "summary": resume[:420], "read_minutes": minutes})
    if not candidats:
        return []
    kwargs = {"status_fn": verifier} if verifier else {}
    mauvais = find_bad_urls([c["url"] for c in candidats], urls_citees, strict=False, **kwargs)
    for url, raison in mauvais.items():
        print(f"[revue-de-presse] lien écarté ({raison}) : {url}", file=sys.stderr)
    return [c for c in candidats if c["url"] not in mauvais][:MAX_ARTICLES]


def rechercher(brief: dict, date_str: str, api_key: str, model: str | None = None, appel=None, verifier=None) -> list[dict]:
    """Liste d'articles pour revue_de_presse, ou [] (moins de MIN_ARTICLES valables, ou toute erreur)."""
    try:
        if appel is None:
            from generate_daily_edition import call_openrouter as appel
        modele = model or os.environ.get("REVUE_MODEL") or MODELE_DEFAUT
        sujet = (brief.get("sujet") or {}).get("titre_propose") or ""
        tools = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 8}}]
        reponse, usage = appel(construire_prompt(date_str, sujet), modele, api_key,
                               temperature=0.2, max_tokens=3000, timeout=240, tools=tools)
        articles = nettoyer((reponse or {}).get("revue_de_presse"), (usage or {}).get("cited_urls"), verifier)
        if len(articles) < MIN_ARTICLES:
            print(f"[revue-de-presse] {len(articles)} article(s) valable(s) seulement : aucune revue pour {date_str}", file=sys.stderr)
            return []
        print(f"[revue-de-presse] {len(articles)} article(s) retenu(s) pour {date_str} (modèle {modele}, coût ≈ {(usage or {}).get('cost', '?')} $)", file=sys.stderr)
        return articles
    except Exception as e:  # noqa: BLE001 — jamais bloquant
        print(f"[revue-de-presse] ignorée : {e}", file=sys.stderr)
        return []
