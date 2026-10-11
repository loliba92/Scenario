#!/usr/bin/env python3
"""Synchronise Google Search Console vers le dépôt (données de visibilité réelles).

Pourquoi : la liaison SEOmatic ne fonctionnait pas (11 octobre 2026). Ce script interroge directement
l'API officielle de Search Console avec un « compte de service » Google, sans dépendance externe
(Python standard + la commande `openssl`, présente sur les machines GitHub Actions).

Ce qu'il écrit, dans `data/gsc/` :
  - `summary.json`     : 28 derniers jours — totaux, meilleures requêtes, meilleures pages.
  - `history.json`     : un point par jour (clics, impressions, CTR, position), cumulé.
  - `indexation.json`  : état d'indexation Google d'un échantillon de pages (accueil, pages clés, dernières éditions).
  - `sitemaps.json`    : état des plans du site déclarés (envoyés, erreurs, avertissements).
Il envoie aussi les plans du site à Google (idempotent), pour qu'il relise les pages modifiées.

Secrets / variables (GitHub → Settings → Secrets and variables → Actions) :
  GSC_SERVICE_ACCOUNT_JSON  (secret)   contenu du fichier JSON du compte de service
  GSC_SITE                  (variable) `sc-domain:lesscenarios.fr` (défaut) ou `https://lesscenarios.fr/`
Voir docs/gsc-installation.md.

Utilisation :
  python3 scripts/seo/gsc_sync.py            # appelle l'API et écrit data/gsc/
  python3 scripts/seo/gsc_sync.py --check    # vérifie seulement l'accès (jeton + liste des sites)

Codes de sortie : 0 = ok ou secret absent (rien à faire) ; 1 = erreur à corriger (message explicite).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "gsc"
SITE_URL_PUBLIC = "https://lesscenarios.fr"
DEFAULT_SITE = "sc-domain:lesscenarios.fr"
SCOPE = "https://www.googleapis.com/auth/webmasters"  # lecture + envoi des plans du site
TOKEN_URL_DEFAULT = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/webmasters/v3"
INSPECT_API = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

SITEMAPS = ("sitemap.xml", "sitemap-news.xml")
KEY_PAGES = ("", "archives.html", "guide-pedagogique.html", "le-projet.html", "sources.html", "glossaire.html")
LAST_EDITIONS = 20          # pages d'éditions inspectées (quota Google : 2000 par jour, on en utilise ~30)
DATA_LAG_DAYS = 3           # Search Console publie ses chiffres avec ~2-3 jours de retard
WINDOW_DAYS = 28
ROW_LIMIT = 100


class GscError(RuntimeError):
    """Erreur claire, avec une piste de correction pour le propriétaire."""


# ------------------------------------------------------------------ authentification
def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def build_jwt(info: dict, now: int | None = None) -> str:
    """Jeton signé RS256 (méthode officielle des comptes de service Google), signé via openssl."""
    now = int(now if now is not None else time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    claim = {
        "iss": info["client_email"],
        "scope": SCOPE,
        "aud": info.get("token_uri", TOKEN_URL_DEFAULT),
        "iat": now,
        "exp": now + 3600,
    }
    signing_input = _b64url(json.dumps(header, separators=(",", ":")).encode()) + "." + \
        _b64url(json.dumps(claim, separators=(",", ":")).encode())
    with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as fh:
        fh.write(info["private_key"])
        key_path = fh.name
    try:
        os.chmod(key_path, 0o600)
        res = subprocess.run(["openssl", "dgst", "-sha256", "-sign", key_path],
                             input=signing_input.encode(), capture_output=True)
    finally:
        os.unlink(key_path)
    if res.returncode != 0:
        raise GscError("Signature impossible : la clé privée du compte de service est illisible. "
                       "Vérifiez que le secret GSC_SERVICE_ACCOUNT_JSON contient le fichier JSON complet, tel que téléchargé.")
    return signing_input + "." + _b64url(res.stdout)


def _http(method: str, url: str, headers: dict | None = None, body: bytes | None = None, timeout: int = 60) -> tuple[int, dict]:
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8") or "{}"
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as err:
        raw = err.read().decode("utf-8", "replace")
        try:
            return err.code, json.loads(raw)
        except ValueError:
            return err.code, {"error": {"message": raw[:300]}}


def get_token(info: dict) -> str:
    form = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": build_jwt(info),
    }).encode()
    status, data = _http("POST", info.get("token_uri", TOKEN_URL_DEFAULT),
                         {"Content-Type": "application/x-www-form-urlencoded"}, form)
    if status != 200 or "access_token" not in data:
        detail = data.get("error_description") or data.get("error") or data
        raise GscError(f"Google refuse le compte de service ({status}) : {detail}. "
                       "Vérifiez que l'API « Google Search Console API » est activée dans le projet Google Cloud.")
    return data["access_token"]


def api(token: str, method: str, url: str, payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    status, data = _http(method, url, headers, body)
    if status in (401, 403):
        msg = (data.get("error") or {}).get("message", "")
        raise GscError(f"Accès refusé par Search Console ({status}) : {msg}. Le plus souvent, l'adresse e-mail du compte de service "
                       "n'a pas été ajoutée comme utilisateur du site (Search Console → Paramètres → Utilisateurs et autorisations), "
                       "ou GSC_SITE ne correspond pas au type de propriété (domaine ou préfixe d'URL).")
    if status >= 400:
        raise GscError(f"Erreur API ({status}) sur {url.split('?')[0]} : {(data.get('error') or {}).get('message', data)}")
    return data


# ------------------------------------------------------------------ traitement des données
def summarize(rows_total: list[dict], rows_query: list[dict], rows_page: list[dict]) -> dict:
    """Met en forme les réponses de l'API (fonction pure, testée)."""
    def tot(rows):
        clicks = sum(r.get("clicks", 0) for r in rows)
        imp = sum(r.get("impressions", 0) for r in rows)
        pos = (sum(r.get("position", 0) * r.get("impressions", 0) for r in rows) / imp) if imp else 0
        return {"clicks": int(clicks), "impressions": int(imp),
                "ctr": round(clicks / imp, 4) if imp else 0, "position": round(pos, 1)}

    def rows(rs, key):
        return [{key: r["keys"][0], "clicks": int(r.get("clicks", 0)), "impressions": int(r.get("impressions", 0)),
                 "ctr": round(r.get("ctr", 0), 4), "position": round(r.get("position", 0), 1)} for r in rs]

    return {"totaux": tot(rows_total), "requetes": rows(rows_query, "requete"), "pages": rows(rows_page, "page")}


def history_points(rows_by_date: list[dict]) -> dict[str, dict]:
    return {r["keys"][0]: {"clicks": int(r.get("clicks", 0)), "impressions": int(r.get("impressions", 0)),
                           "ctr": round(r.get("ctr", 0), 4), "position": round(r.get("position", 0), 1)}
            for r in rows_by_date}


def merge_history(old: dict, new_points: dict[str, dict]) -> dict:
    merged = dict(old or {})
    merged.update(new_points)
    return dict(sorted(merged.items()))


def pages_to_inspect(root: Path = ROOT) -> list[str]:
    urls = [f"{SITE_URL_PUBLIC}/{p}" for p in KEY_PAGES]
    editions = sorted((root / "archives").glob("2026-*.html"), reverse=True)[:LAST_EDITIONS]
    urls += [f"{SITE_URL_PUBLIC}/archives/{e.name}" for e in editions]
    return urls


def inspection_row(url: str, data: dict) -> dict:
    res = (data.get("inspectionResult") or {}).get("indexStatusResult") or {}
    return {"url": url, "verdict": res.get("verdict"), "etat": res.get("coverageState"),
            "derniere_exploration": res.get("lastCrawlTime"), "canonique_google": res.get("googleCanonical"),
            "canonique_declaree": res.get("userCanonical"), "robots": res.get("robotsTxtState"),
            "indexation": res.get("indexingState")}


# ------------------------------------------------------------------ exécution
def query(token: str, site: str, start: date, end: date, dimensions: list[str], limit: int) -> list[dict]:
    url = f"{API}/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query"
    payload = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dimensions,
               "rowLimit": limit, "dataState": "final"}
    return api(token, "POST", url, payload).get("rows", [])


def write_json(name: str, data) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(info: dict, site: str, check_only: bool = False) -> int:
    token = get_token(info)
    sites = api(token, "GET", f"{API}/sites").get("siteEntry", [])
    known = {s["siteUrl"]: s.get("permissionLevel") for s in sites}
    print(f"Sites visibles par le compte de service : {known or 'aucun'}")
    if site not in known:
        raise GscError(f"Le site « {site} » n'apparaît pas parmi les sites du compte de service ({list(known) or 'aucun'}). "
                       "Ajoutez l'e-mail du compte de service comme utilisateur dans Search Console, "
                       "ou corrigez la variable GSC_SITE (sc-domain:lesscenarios.fr pour une propriété « domaine », "
                       "https://lesscenarios.fr/ pour une propriété « préfixe d'URL »).")
    if check_only:
        print(f"OK : accès en {known[site]} à {site}.")
        return 0

    end = date.today() - timedelta(days=DATA_LAG_DAYS)
    start = end - timedelta(days=WINDOW_DAYS - 1)
    by_date = query(token, site, start, end, ["date"], WINDOW_DAYS + 5)
    by_query = query(token, site, start, end, ["query"], ROW_LIMIT)
    by_page = query(token, site, start, end, ["page"], ROW_LIMIT)

    summary = summarize(by_date, by_query, by_page)
    summary.update({"site": site, "periode": {"debut": start.isoformat(), "fin": end.isoformat()},
                    "mis_a_jour": date.today().isoformat()})
    write_json("summary.json", summary)

    hist_path = OUT_DIR / "history.json"
    old = json.loads(hist_path.read_text(encoding="utf-8")) if hist_path.exists() else {}
    write_json("history.json", merge_history(old, history_points(by_date)))

    # Plans du site : envoi (idempotent) puis lecture de leur état.
    sm_state = []
    for sm in SITEMAPS:
        feed = f"{SITE_URL_PUBLIC}/{sm}"
        sm_url = f"{API}/sites/{urllib.parse.quote(site, safe='')}/sitemaps/{urllib.parse.quote(feed, safe='')}"
        try:
            api(token, "PUT", sm_url)
            info_sm = api(token, "GET", sm_url)
            sm_state.append({"plan": feed, "derniere_lecture": info_sm.get("lastDownloaded"),
                             "erreurs": info_sm.get("errors"), "avertissements": info_sm.get("warnings"),
                             "contenus": info_sm.get("contents")})
        except GscError as err:
            sm_state.append({"plan": feed, "erreur": str(err)[:300]})
    write_json("sitemaps.json", {"mis_a_jour": date.today().isoformat(), "plans": sm_state})

    # Indexation : un échantillon de pages.
    rows = []
    for url in pages_to_inspect():
        try:
            data = api(token, "POST", INSPECT_API, {"inspectionUrl": url, "siteUrl": site, "languageCode": "fr"})
            rows.append(inspection_row(url, data))
        except GscError as err:
            rows.append({"url": url, "erreur": str(err)[:200]})
    write_json("indexation.json", {"mis_a_jour": date.today().isoformat(), "pages": rows})

    t = summary["totaux"]
    indexees = sum(1 for r in rows if r.get("verdict") == "PASS")
    print(f"OK : {t['clicks']} clics, {t['impressions']} impressions (28 j) ; {indexees}/{len(rows)} pages inspectées indexées.")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="vérifie seulement l'accès (jeton + sites)")
    args = ap.parse_args(argv)

    raw = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        print("GSC_SERVICE_ACCOUNT_JSON absent : rien à faire (voir docs/gsc-installation.md).")
        return 0
    site = os.environ.get("GSC_SITE", "").strip() or DEFAULT_SITE
    try:
        info = json.loads(raw)
        for k in ("client_email", "private_key"):
            if not info.get(k):
                raise GscError(f"Le secret GSC_SERVICE_ACCOUNT_JSON ne contient pas « {k} » : collez le fichier JSON complet.")
        return run(info, site, args.check)
    except ValueError:
        print("::error::GSC_SERVICE_ACCOUNT_JSON n'est pas un JSON valide : collez le contenu complet du fichier téléchargé.")
        return 1
    except GscError as err:
        print(f"::error::{err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
