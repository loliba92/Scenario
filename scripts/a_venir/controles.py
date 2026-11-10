"""Contrôles qualité d'un résultat proposé pour un rendez-vous. Aucun modèle ici : uniquement du code.

Un résultat n'est publié que si TOUS les contrôles passent. Sinon le rendez-vous reste « réponse en cours de vérification ».
Principe : le modèle propose, le code vérifie dans les pages sources elles-mêmes (citations, chiffres, dates, domaines).
"""
import html as _html
import re
import unicodedata
import urllib.request
from datetime import date
from urllib.parse import urlparse

DOMAINES_REFUSES = {
    "facebook.com", "x.com", "twitter.com", "instagram.com", "tiktok.com", "reddit.com", "youtube.com", "youtu.be",
    "linkedin.com", "medium.com", "substack.com", "blogspot.com", "wordpress.com", "quora.com", "pinterest.com",
    "t.me", "telegram.org", "wikipedia.org",
}
MIN_SOURCES = 2          # sources vérifiées, de domaines différents
MIN_EXTRAIT = 40         # caractères minimum d'une citation
MAX_REPONSE = 300
MAX_PAGE = 1_500_000
MOTS_VAGUES = re.compile(r"\b(devrait|pourrait|pourraient|serait|semble|probablement|peut-être|aurait|auraient)\b", re.I)
VERTS = {"arrive", "pas_arrive"}


def normaliser(t):
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode()
    t = t.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9%]+", " ", t).strip()


def domaine(url):
    h = (urlparse(url).hostname or "").lower()
    parts = h.split(".")
    if len(parts) >= 3 and parts[-2] in {"co", "com", "org", "gouv"} and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def charger_page(url, delai=15):
    """Texte d'une page web (HTML sans balises), ou None. Client simple, délai court, taille bornée."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ScenarioVerif/1.0)"})
        with urllib.request.urlopen(req, timeout=delai) as r:
            if r.status != 200 or "html" not in (r.headers.get("Content-Type") or "text/html"):
                return None
            brut = r.read(MAX_PAGE).decode(r.headers.get_content_charset() or "utf-8", errors="ignore")
    except Exception:  # noqa: BLE001 — une page inaccessible n'est jamais une preuve
        return None
    brut = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", brut, flags=re.S | re.I)
    return _html.unescape(re.sub(r"<[^>]+>", " ", brut))


def chiffres_dans(texte_normalise, valeur):
    """Tous les nombres de `valeur` (ex. « 0,5 million » → 0 5) doivent figurer dans le texte."""
    nombres = re.findall(r"\d+", normaliser(valeur))
    return bool(nombres) and all(re.search(rf"(?<!\d){n}(?!\d)", texte_normalise) for n in nombres)


def verifier(r, prop, aujourdhui, date_edition, pages):
    """Retourne (ok, motifs, resultat). `pages` : fonction url -> texte|None. `prop` : proposition du modèle."""
    motifs = []
    statut = prop.get("statut")
    if statut not in VERTS:
        return False, [f"statut « {statut} » : pas de réponse ferme"], None

    # C1 — dates
    try:
        d = date.fromisoformat(prop.get("date_reponse") or "")
    except ValueError:
        return False, ["date de la réponse absente ou illisible"], None
    limite = date.fromisoformat(r["date"])
    if d > aujourdhui:
        motifs.append("date de la réponse dans le futur")
    if date_edition and d < date_edition:
        motifs.append("date de la réponse antérieure à l'édition")
    if statut == "pas_arrive" and aujourdhui <= limite:
        motifs.append("« ne s'est pas produit » refusé avant la date limite")

    # C2 — texte de la réponse
    rep = str(prop.get("reponse", "")).strip()
    if not rep or len(rep) > MAX_REPONSE:
        motifs.append("réponse vide ou trop longue")
    if MOTS_VAGUES.search(rep):
        motifs.append("réponse au conditionnel ou hésitante : un fait doit être affirmé par les sources")

    # C3 — sources : citation retrouvée mot pour mot dans la page, domaines distincts et acceptables
    verifiees, vus, textes = [], set(), []
    for s in prop.get("sources") or []:
        url, ex = str(s.get("url", "")), str(s.get("extrait", "")).strip()
        dom = domaine(url)
        if not url.startswith("https://") or dom in DOMAINES_REFUSES or dom in vus:
            continue
        if len(ex) < MIN_EXTRAIT:
            continue
        page = pages(url)
        if not page:
            continue
        n = normaliser(page)
        if normaliser(ex) not in n:
            continue
        # la source doit parler du sujet : au moins 2 mots significatifs de la question dans la citation ou la page
        mots = {m for m in normaliser(r["question"]).split() if len(m) > 4}
        if len(mots & set(n.split())) < 2:
            continue
        vus.add(dom)
        textes.append(n)
        verifiees.append({"titre": str(s.get("titre") or dom).strip(), "url": url})
    if len(verifiees) < MIN_SOURCES:
        motifs.append(f"{len(verifiees)} source(s) vérifiée(s) sur {MIN_SOURCES} exigées "
                      "(citation introuvable dans la page, domaine répété, refusé ou page inaccessible)")

    # C4 — chiffres : chaque nombre doit figurer dans au moins une source vérifiée
    chiffres = []
    for c in prop.get("chiffres") or []:
        lib, val = str(c.get("libelle", "")).strip(), str(c.get("valeur", "")).strip()
        if not lib or not val:
            motifs.append("chiffre incomplet")
        elif not any(chiffres_dans(tx, val) for tx in textes):
            motifs.append(f"chiffre « {val} » introuvable dans les sources")
        else:
            chiffres.append({"libelle": lib, "valeur": val})

    # C5 — scénario : doit exister ; sinon la réponse ne tranche pas
    sc = prop.get("scenario")
    if sc not in ("favorable", "stable", "degrade"):
        sc = None

    if motifs:
        return False, motifs, None
    resultat = {"statut": statut, "date": (limite if statut == "pas_arrive" else d).isoformat(), "reponse": rep,
                "scenario": sc, "sources": verifiees}
    if chiffres:
        resultat["chiffres"] = chiffres
    return True, [], resultat
