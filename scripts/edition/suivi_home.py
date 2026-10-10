#!/usr/bin/env python3
"""Bloc « Le dernier suivi » de la page d'accueil, juste sous « La dernière édition ».

Demandé le 9 octobre 2026 : le suivi doit être visible sur l'accueil, comme la dernière
édition. Le bloc réutilise la mise en page de la carte « dernière édition »
(`.featured-article*`) : même image, même date en petites capitales, même titre, même
appel à l'action, donc aucune règle CSS nouvelle.

Source : les pages `suivi/*.html` elles-mêmes (rien à tenir à jour à la main). Le suivi
choisi est celui dont la DERNIÈRE version est la plus récente.

Sûreté : `bloc_dernier_suivi()` ne lève jamais d'exception et renvoie "" au moindre
problème (page illisible, image absente…) — l'accueil se publie alors sans le bloc plutôt
que de bloquer l'édition du jour.

Utilisation :
    python3 scripts/edition/suivi_home.py            # met à jour index.html en place
    python3 scripts/edition/suivi_home.py --check    # code 1 si index.html n'est pas à jour
Appelé aussi par build_html.py (assemblage quotidien de l'accueil) et par detection.yml
(après chaque mise à jour d'un suivi).
"""
from __future__ import annotations

import argparse
import html as _html
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUIVI_DIR = ROOT / "suivi"
INDEX_PATH = ROOT / "index.html"

START, END = "<!-- dernier-suivi:start -->", "<!-- dernier-suivi:end -->"

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
MOIS_COURT = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août",
              "sept.", "oct.", "nov.", "déc."]
RUBRIQUES = {
    "international": "International",
    "politique-institutions": "Politique",
    "economie-entreprises": "Économie",
    "sciences-environnement": "Sciences",
    "tech-numerique": "Tech",
    "culture-divertissement": "Culture",
    "sport": "Sport",
}


def _date_fr(texte: str):
    m = re.search(r"(\d{1,2})(?:er)?\s+([a-zéûô]+)\s+(\d{4})", texte or "", re.I)
    if not m or m.group(2).lower() not in MOIS:
        return None
    try:
        return date(int(m.group(3)), MOIS.index(m.group(2).lower()) + 1, int(m.group(1)))
    except ValueError:
        return None


def _debut(texte: str, maxi: int = 260) -> str:
    """Les premières phrases entières, jusqu'à ~maxi caractères ; coupe à une virgule si la
    première phrase est très longue."""
    texte = re.sub(r"\s+", " ", texte or "").strip()
    phrases = re.findall(r"[^.!?]+[.!?]+(?:\s|$)", texte)
    if not phrases:
        return texte
    out = ""
    for p in phrases:
        if out and len(out + p) > maxi:
            break
        out += p
    out = out.strip()
    if len(out) > maxi * 1.4:
        cut = max(out.rfind(", ", 0, maxi), out.rfind(" — ", 0, maxi), out.rfind(" : ", 0, maxi))
        if cut > maxi * 0.5:
            out = re.sub(r"[,:—\s]+$", "", out[:cut]) + "…"
    return out


def _typo(s: str) -> str:
    """Échappe, puis espace insécable avant « ? ! : ; » (comme le reste du site)."""
    return re.sub(r" (?=[?!:;»])", "&nbsp;", _html.escape(s, quote=False))


def lire_suivi(chemin: Path) -> dict | None:
    from bs4 import BeautifulSoup  # importé ici : le module reste importable sans bs4

    soup = BeautifulSoup(chemin.read_text(encoding="utf-8"), "html.parser")
    h1 = soup.find("h1")
    versions = soup.select(".version")
    if not h1 or not versions:
        return None
    derniere = versions[-1]
    d = _date_fr(derniere.select_one(".version-date").get_text(" ", strip=True)) if derniere.select_one(".version-date") else None
    if d is None:
        return None
    mises_a_jour = [v for v in versions if "is-update" in (v.get("class") or [])]
    inner = derniere.select_one(".version-content-inner") or derniere
    fait = ""
    for p in inner.find_all("p"):
        if p.find_parent(class_="mini-scenario") or p.find_parent(class_="conclusion") or "sources-note" in (p.get("class") or []):
            continue
        fait = p.get_text(" ", strip=True)
        if fait:
            break

    image = ""
    img = soup.select_one("figure.article-image img[src]")
    if img:
        src = img["src"]
        image = src[3:] if src.startswith("../") else src
        if not (ROOT / image).is_file():
            image = ""

    rubrique = ""
    origine = soup.select_one("a.origin-link[href]")
    if origine:
        m = re.search(r"archives/(\d{4}-\d{2}-\d{2})\.html", origine["href"])
        edition = ROOT / "archives" / f"{m.group(1)}.html" if m else None
        if edition and edition.is_file():
            mm = re.search(r'<meta name="domain" content="([^"]*)"', edition.read_text(encoding="utf-8"))
            rubrique = RUBRIQUES.get(mm.group(1), "") if mm else ""

    return {
        "slug": chemin.stem,
        "titre": h1.get_text(" ", strip=True),
        "date": d,
        "maj": len(mises_a_jour),
        "fait": fait,
        "image": image,
        "rubrique": rubrique,
    }


def derniers_suivis(n: int = 3, suivi_dir: Path = SUIVI_DIR) -> list[dict]:
    """Les `n` suivis mis à jour le plus récemment (du plus récent au plus ancien)."""
    trouves = []
    for chemin in sorted(suivi_dir.glob("*.html")):
        if chemin.name.startswith("_"):
            continue
        try:
            s = lire_suivi(chemin)
        except Exception:
            s = None
        if s:
            trouves.append(s)
    # Le plus récemment mis à jour ; à égalité, celui qui compte le plus de versions.
    trouves.sort(key=lambda s: (s["date"], s["maj"]), reverse=True)
    return trouves[:n]


def dernier_suivi(suivi_dir: Path = SUIVI_DIR) -> dict | None:
    """Le suivi mis à jour le plus récemment, ou None."""
    liste = derniers_suivis(1, suivi_dir)
    return liste[0] if liste else None


def rendre(s: dict) -> str:
    ligne = _ligne(s)
    image = (f'\n      <div class="featured-article-image-wrap">\n'
             f'        <img class="featured-article-image" src="{_html.escape(s["image"])}" alt="{_html.escape(s["titre"])}">\n'
             f'      </div>') if s["image"] else ""
    question = (f'\n        <p class="featured-article-question">{_typo(_debut(s["fait"]))}</p>') if s["fait"] else ""
    return f"""{START}
<section class="featured-article" id="dernier-suivi">
  <div class="wrap">
    <p class="section-label">Le dernier suivi</p>
    <a href="suivi/{s['slug']}.html" class="featured-article-link">{image}
      <div>
        <span class="featured-article-date">{_html.escape(ligne)}</span>
        <h2 class="featured-article-title">{_typo(s['titre'])}</h2>{question}
        <span class="featured-article-cta">Lire le suivi →</span>
      </div>
    </a>
    <a class="cross-link" href="archives.html?tag=revise">Voir tous les sujets révisés&nbsp;→</a>
  </div>
</section>
{END}"""


def _ligne(s: dict, insecable: bool = False) -> str:
    """« Économie · mis à jour le 9 oct. ». insecable=True : la date reste d'un seul tenant
    (retour à la ligne possible seulement avant elle), pour ne jamais couper « 12 / sept. »."""
    court = f"{s['date'].day} {MOIS_COURT[s['date'].month - 1]}"
    date_txt = f"mis à jour le {court}" if s["maj"] else f"première analyse le {court}"
    rubrique = f"{s['rubrique']} · " if s["rubrique"] else ""
    if not insecable:
        return rubrique + date_txt
    # Deux éléments côte à côte (sans « · » qui pourrait rester seul en bout de ligne) ; la date ne se coupe jamais.
    rub = f"<span>{_html.escape(s['rubrique'])}</span>" if s["rubrique"] else ""
    return rub + f'<span class="nw">{_html.escape(date_txt)}</span>'


def rendre_suivis_edition(suivis: list[dict]) -> str:
    """Bande « Les derniers suivis » de la page Éditions : une carte par suivi, sans image."""
    cartes = "\n".join(
        f"""      <a class="suivi-card" href="suivi/{s['slug']}.html">
        <span class="suivi-card-meta">{_ligne(s, insecable=True)}</span>
        <span class="suivi-card-title">{_typo(s['titre'])}</span>
        <span class="suivi-card-text">{_typo(_debut(s['fait'], 170))}</span>
        <span class="suivi-card-cta">Lire le suivi →</span>
      </a>""" for s in suivis)
    libelle = "Le dernier suivi" if len(suivis) == 1 else "Les derniers suivis"
    return f"""<section class="suivis-recents" id="suivis">
  <div class="wrap">
    <p class="suivis-label">{libelle}</p>
    <div class="suivis-grid">
{cartes}
    </div>
  </div>
</section>"""


def bloc_suivis_edition(n: int = 1) -> str:
    """Bande pour la page Éditions (le dernier suivi seulement : 10 oct. 2026), ou "" au moindre problème (jamais d'exception)."""
    try:
        suivis = derniers_suivis(n)
        return rendre_suivis_edition(suivis) if suivis else ""
    except Exception as e:  # noqa: BLE001
        print(f"[suivi_home] bande ignorée : {e}", file=sys.stderr)
        return ""


def bloc_dernier_suivi() -> str:
    """Bloc HTML, ou "" au moindre problème (jamais d'exception)."""
    try:
        s = dernier_suivi()
        return rendre(s) if s else ""
    except Exception as e:  # noqa: BLE001 — l'accueil ne doit jamais dépendre de ce bloc
        print(f"[suivi_home] bloc ignoré : {e}", file=sys.stderr)
        return ""


def injecter(index_html: str, bloc: str) -> str:
    """Remplace le bloc existant, ou l'insère juste après la carte « La dernière édition »."""
    pattern = re.compile(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n*", re.S)
    sans = pattern.sub("", index_html)
    if not bloc:
        return sans
    m = re.search(r'<section class="featured-article">.*?</section>', sans, re.S)
    if not m:
        return sans
    return sans[:m.end()] + "\n\n" + bloc + "\n" + sans[m.end():]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="ne rien écrire ; code 1 si index.html n'est pas à jour")
    args = ap.parse_args(argv)
    ancien = INDEX_PATH.read_text(encoding="utf-8")
    nouveau = injecter(ancien, bloc_dernier_suivi())
    if nouveau == ancien:
        print("index.html : bloc « Le dernier suivi » déjà à jour")
        return 0
    if args.check:
        print("index.html : bloc « Le dernier suivi » à mettre à jour")
        return 1
    INDEX_PATH.write_text(nouveau, encoding="utf-8")
    print("index.html : bloc « Le dernier suivi » mis à jour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
