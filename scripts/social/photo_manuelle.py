"""Photo choisie à la main (hors banque Pexels), avec crédit et licence.

Cas d'usage : l'éditeur demande une photo précise (ex. 18 octobre 2026 : Zinedine Zidane, photo sous licence libre
de Wikimedia Commons). La photo est rangée dans le dépôt (assets/social/photos-manuelles/) et décrite dans
editorial-previews/{date}.photo-credits.json avec `"source": "manuelle"` :

    {"source": "manuelle", "local_file": "assets/social/photos-manuelles/2026-10-18-zidane.jpg",
     "photographer": "Oleg Dubyna", "source_label": "Wikimedia Commons", "source_url": "https://commons...",
     "licence": "CC BY-SA 2.0", "licence_url": "https://creativecommons.org/licenses/by-sa/2.0/",
     "focus_x": 0.55, "focus_y": 0.35, "query": "Zinedine Zidane"}

Les recadrages (carré 1080 pour Instagram, large 1600×900 pour l'article) sont faits ici, centrés sur le point
d'intérêt (focus_x, focus_y entre 0 et 1) pour ne jamais couper le visage. Aucun appel réseau.
"""
from pathlib import Path

from PIL import Image


def recadrer(src, dest, w, h, focus_x=0.5, focus_y=0.5):
    """Recadre `src` au format w×h (rapport conservé, puis redimensionné), centré sur (focus_x, focus_y)."""
    with Image.open(src) as im:
        im = im.convert("RGB")
        sw, sh = im.size
        cible = w / h
        if sw / sh > cible:      # image plus large que la cible : on coupe sur les côtés
            cw, ch = int(round(sh * cible)), sh
        else:                    # image plus haute : on coupe en haut et en bas
            cw, ch = sw, int(round(sw / cible))
        left = min(max(int(round(focus_x * sw - cw / 2)), 0), sw - cw)
        top = min(max(int(round(focus_y * sh - ch / 2)), 0), sh - ch)
        out = im.crop((left, top, left + cw, top + ch)).resize((w, h), Image.LANCZOS)
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        out.save(dest, "JPEG", quality=88, optimize=True)


def produire_recadrages(credits, repo_root, dossier_sortie, stem):
    """Écrit {stem}-carre.jpg (1080×1080) et {stem}-large.jpg (1600×900) ; renvoie (chemin_carre, chemin_large)."""
    src = Path(repo_root) / credits["local_file"]
    fx, fy = credits.get("focus_x", 0.5), credits.get("focus_y", 0.4)
    carre = Path(dossier_sortie) / f"{stem}-carre.jpg"
    large = Path(dossier_sortie) / f"{stem}-large.jpg"
    recadrer(src, carre, 1080, 1080, fx, fy)
    recadrer(src, large, 1600, 900, fx, fy)
    return carre, large
