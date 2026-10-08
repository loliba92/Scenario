"""Images de la revue de presse (sources.html) — ajouté le 8 octobre 2026.

Constat : depuis la chaîne de rédaction automatique, le modèle laisse
`revue_de_presse[].image` à null et rien ne le complétait : la revue de presse
s'affichait sans aucune vignette (tous les jours depuis le 24 septembre).
L'étape se fait donc ici, de façon déterministe : on lit la balise
og:image (ou twitter:image) de la page de l'article, comme le décrit
docs/routine-prompt.md. L'image reste un simple lien vers le média d'origine
(jamais téléchargée ni hébergée chez nous).

Jamais bloquant : un site qui bloque les robots (Reuters répond 401), un
délai dépassé ou une page sans image laissent l'article sans vignette —
generate_sources_page.py gère déjà ce cas. Jamais d'image générique à la
place d'une image absente (logos, images par défaut : écartés).
"""

import html
import re
import urllib.request
from urllib.parse import quote, urljoin

USER_AGENT = "Mozilla/5.0 (compatible; ScenarioBot/1.0; +https://lesscenarios.fr)"
_META = re.compile(r"<meta\b[^>]*>", re.I)
_KEY = re.compile(r"""(?:property|name)\s*=\s*["'](og:image(?::secure_url)?|twitter:image(?::src)?)["']""", re.I)
_CONTENT = re.compile(r"""content\s*=\s*["']([^"']+)["']""", re.I)
_GENERIC = re.compile(r"logo|placeholder|default|trading-news|favicon|sprite", re.I)


def extract_og_image(page_html, base_url):
    """Première image og:image/twitter:image exploitable de la page, ou None."""
    for meta in _META.findall(page_html):
        if not _KEY.search(meta):
            continue
        found = _CONTENT.search(meta)
        if not found:
            continue
        url = urljoin(base_url, html.unescape(found.group(1).strip()))
        if url.startswith("http") and not _GENERIC.search(url):
            return url
    return None


def fetch_og_image(url, timeout=15):
    try:
        req = urllib.request.Request(quote(url, safe=":/?&=%#+~@!,;"), headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            page = resp.read(400000).decode("utf-8", "ignore")
    except Exception as exc:  # noqa: BLE001 — jamais bloquant, quelle que soit la cause
        print(f"[press-images] {url[:70]} : pas d'image ({type(exc).__name__})")
        return None
    return extract_og_image(page, url)


def fill_missing_images(articles, fetch=fetch_og_image):
    """Complète `image` pour les articles qui n'en ont pas. Retourne le nombre ajouté."""
    added = 0
    for art in articles:
        if art.get("image") or not art.get("url"):
            continue
        image = fetch(art["url"])
        if image:
            art["image"] = image
            added += 1
    return added
