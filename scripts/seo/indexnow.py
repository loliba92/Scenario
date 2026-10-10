#!/usr/bin/env python3
"""Prévient les moteurs compatibles IndexNow (Bing, Yandex, Naver, Seznam…) qu'une édition vient d'être publiée.

Google n'utilise pas IndexNow : pour lui, ce sont le plan du site, les liens internes et les liens externes qui comptent.
Bing, lui, alimente aussi des moteurs de réponse (affirmation de blogs spécialisés, non vérifiée auprès des éditeurs).
La clé est publique par conception : le fichier <clé>.txt à la racine prouve que le site nous appartient.

Annonce l'édition du jour (version française et anglaise, si elle existe) et l'accueil. Jamais bloquant.
Utilisation : python3 scripts/seo/indexnow.py [--dry-run]
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOST = "lesscenarios.fr"
ENDPOINT = "https://api.indexnow.org/IndexNow"
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")
CLE = re.compile(r"^([0-9a-f]{32})\.txt$")


def trouver_cle(racine):
    for p in sorted(racine.glob("*.txt")):
        m = CLE.match(p.name)
        if m and p.read_text(encoding="utf-8").strip() == m.group(1):
            return m.group(1)
    return None


def urls_du_jour(racine):
    editions = sorted(p.name for p in (racine / "archives").glob("*.html") if DATED.match(p.name))
    if not editions:
        return []
    dernier = editions[-1]
    urls = [f"https://{HOST}/", f"https://{HOST}/archives/{dernier}"]
    if (racine / "en" / "archives" / dernier).exists():
        urls.append(f"https://{HOST}/en/archives/{dernier}")
    return urls


def charge(racine):
    cle = trouver_cle(racine)
    if not cle:
        return None
    return {"host": HOST, "key": cle, "keyLocation": f"https://{HOST}/{cle}.txt", "urlList": urls_du_jour(racine)}


def main(argv):
    corps = charge(ROOT)
    if not corps or not corps["urlList"]:
        print("IndexNow : clé ou édition introuvable, rien envoyé.")
        return
    if "--dry-run" in argv:
        print(json.dumps(corps, ensure_ascii=False, indent=2))
        return
    req = urllib.request.Request(ENDPOINT, data=json.dumps(corps).encode("utf-8"),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow : {len(corps['urlList'])} adresse(s) annoncée(s), réponse HTTP {r.status}.")


if __name__ == "__main__":
    main(sys.argv[1:])
