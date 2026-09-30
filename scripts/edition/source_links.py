"""
Contrôle des liens sources d'un brief — ajouté le 30 septembre 2026, retour
utilisateur : les liens de la source (Reuters, Bloomberg...) du preview du
1er octobre menaient à « We can't find that page ». Cause : le brief de
repli (generate_fallback_brief.py) demande au modèle de remplir lui-même
`sources[].url` et `revue_de_presse[].url`, et rien ne vérifiait qu'une URL
avait réellement été lue — le modèle en composait de plausibles à partir
d'un titre et d'une date (ex. `..._123456789.html`). Le fait « krach de
Wall Street » du même brief ne reposait que sur une de ces sources.

Deux niveaux de contrôle, du plus fiable au plus faible :

1. **Citations de la recherche web** (`cited_urls`) : OpenRouter renvoie,
   avec le server tool `openrouter:web_search`, les URL réellement
   consultées (`message.annotations[].url_citation.url`). Si on en a, une
   URL du brief absente de cette liste est inventée — même si le domaine
   est réel. C'est le seul contrôle qui attrape un faux lien Reuters : ce
   site répond 401 à tout robot, page réelle ou non.
2. **Test HTTP** (repli quand aucune citation n'est disponible) : seuls
   404/410 et un nom de domaine introuvable prouvent qu'un lien est mort.
   401/403/429 (site qui bloque les robots) et les délais dépassés ne
   prouvent rien : le lien est gardé mais l'incertitude est loguée.
"""

import re
import socket
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit

_TRACKING_PARAMS = re.compile(r"^(utm_|fbclid$|gclid$|ref$)", re.I)
_UA = "Mozilla/5.0 (compatible; ScenarioLinkCheck/1.0)"


def normalize_url(url):
    """Forme comparable : sans schéma, `www.`, fragment, slash final ni
    paramètres de suivi — deux écritures de la même page se comparent égales."""
    try:
        parts = urlsplit(url.strip())
    except (ValueError, AttributeError):
        return ""
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    query = "&".join(
        p for p in parts.query.split("&") if p and not _TRACKING_PARAMS.match(p.split("=")[0])
    )
    path = parts.path.rstrip("/")
    return f"{host}{path}" + (f"?{query}" if query else "")


def extract_cited_urls(message):
    """URL des citations `url_citation` d'un message de réponse OpenRouter.
    Ensemble vide si le modèle/le moteur n'en renvoie pas (le contrôle
    bascule alors sur le test HTTP)."""
    urls = set()
    for ann in (message or {}).get("annotations") or []:
        if not isinstance(ann, dict) or ann.get("type") != "url_citation":
            continue
        url = (ann.get("url_citation") or {}).get("url") or ann.get("url")
        if url:
            urls.add(url)
    return urls


def http_status(url, timeout=10):
    """Code HTTP, ou None si le serveur est injoignable pour une raison qui
    ne prouve rien sur la page (délai, réseau). Lève rien : renvoie 'dns'
    si le domaine n'existe pas."""
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.gaierror):
            return "dns"
        return None
    except Exception:  # noqa: BLE001 — jamais bloquant, une incertitude n'est pas un échec
        return None


def _is_dead(status):
    return status in (404, 410, "dns")


def find_bad_urls(urls, cited_urls=None, status_fn=http_status, strict=False):
    """Renvoie {url: raison} pour chaque URL à écarter (dédoublonnées).

    `strict` (sans citations de recherche web, donc test HTTP seul) : un
    lien dont le site refuse les robots (401/403/429) ou ne répond pas est
    lui aussi écarté, car rien ne prouve que la page existe — c'est le cas
    d'un faux lien Reuters/Bloomberg. Hors strict, il est gardé avec un
    avertissement (dernier essai : mieux vaut une source non vérifiée
    qu'aucune édition, voir generate_fallback_brief.py)."""
    cited_norm = {normalize_url(u) for u in (cited_urls or set())}
    bad = {}
    for url in dict.fromkeys(u for u in urls if u):
        if not re.match(r"^https?://", url):
            bad[url] = "URL invalide"
        elif cited_norm:
            if normalize_url(url) not in cited_norm:
                bad[url] = "absente des pages réellement consultées par la recherche web"
        else:
            status = status_fn(url)
            if _is_dead(status):
                bad[url] = f"page introuvable (HTTP {status})" if status != "dns" else "domaine introuvable"
            elif status is None or status in (401, 403, 429) or (isinstance(status, int) and status >= 500):
                if strict:
                    bad[url] = f"non vérifiable (HTTP {status} : accès refusé aux robots ou site injoignable), écarté"
                else:
                    print(f"[source-links] lien non vérifiable (HTTP {status}), GARDÉ : {url}", file=sys.stderr)
    return bad


def sanitize_brief_sources(brief, cited_urls=None, status_fn=http_status, strict=False):
    """Retire du brief (en place) les sources et entrées de revue de presse
    dont l'URL est écartée, ainsi que leurs références dans
    `faits_verifies[].sources`. Renvoie (retirées, erreurs) : `erreurs`
    liste les faits restés sans aucune source vérifiée, à corriger par le
    modèle (retry) plutôt que publiés sans appui."""
    sources = brief.get("sources") or []
    press = brief.get("revue_de_presse") or []
    bad = find_bad_urls([s.get("url") for s in sources] + [p.get("url") for p in press],
                        cited_urls, status_fn, strict)
    if not bad:
        return {}, []

    dropped_ids = {s.get("id") for s in sources if s.get("url") in bad}
    brief["sources"] = [s for s in sources if s.get("url") not in bad]
    brief["revue_de_presse"] = [p for p in press if p.get("url") not in bad]

    errors = []
    for fait in brief.get("faits_verifies") or []:
        refs = fait.get("sources") or []
        fait["sources"] = [r for r in refs if r not in dropped_ids]
        if refs and not fait["sources"]:
            errors.append(
                f"fait « {str(fait.get('affirmation', ''))[:90]} » : aucune de ses sources n'a pu être "
                "vérifiée (URL inventée, absente des résultats de la recherche web, ou page introuvable) "
                "et elles ont été retirées — refaire une recherche pour ce fait et citer l'URL EXACTE d'un "
                "résultat (les sites qui bloquent les robots, comme Reuters ou Bloomberg, ne sont acceptés "
                "que si l'URL figure dans les résultats de recherche), ou retirer le fait"
            )
    for url, reason in bad.items():
        print(f"[source-links] source écartée ({reason}) : {url}", file=sys.stderr)
    return bad, errors
