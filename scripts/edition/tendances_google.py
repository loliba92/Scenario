"""Recherches en hausse sur Google en France (flux public Google Trends).

Sert à orienter la veille des sujets prioritaires vers ce que les gens cherchent
réellement en ce moment. Lecture seule, sans clé. En cas de panne ou de flux
vide, renvoie une liste vide : la veille fonctionne alors comme avant.

Le flux donne seulement des expressions et un trafic approximatif. Il ne dit
pas si un sujet a un enjeu : ce tri reste à la charge de la veille, qui applique
déjà sa « barre d'importance ».
"""

import urllib.request
import xml.etree.ElementTree as ET

FLUX_URL = "https://trends.google.fr/trending/rss?geo=FR"
NS = {"ht": "https://trends.google.com/trending/rss"}
MAX_TENDANCES = 10


def parser_flux(xml_text):
    """Renvoie [{'titre': str, 'trafic': str}] depuis le XML du flux (sans erreur si vide)."""
    racine = ET.fromstring(xml_text)
    out = []
    for item in racine.iter("item"):
        titre = (item.findtext("title") or "").strip()
        if not titre:
            continue
        trafic = (item.findtext("ht:approx_traffic", namespaces=NS) or "").strip()
        out.append({"titre": titre, "trafic": trafic})
    return out[:MAX_TENDANCES]


def lire_tendances(url=FLUX_URL, timeout=15):
    """Renvoie la liste des tendances, ou [] si le flux est indisponible."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return parser_flux(r.read())
    except Exception as e:  # réseau, XML invalide : on n'arrête pas la veille
        print(f"[tendances] flux Google indisponible, veille sans cette aide : {e}")
        return []


def bloc_prompt(tendances):
    """Paragraphe ajouté au prompt de la veille (chaîne vide si rien à ajouter)."""
    if not tendances:
        return ""
    lignes = [
        "Recherches actuellement en hausse sur Google en France (indicatif, "
        "flux Google Trends du jour) :",
    ]
    for t in tendances:
        suffixe = f" ({t['trafic']} recherches)" if t["trafic"] else ""
        lignes.append(f"- {t['titre']}{suffixe}")
    lignes.append(
        "Si, à enjeu structurel égal, une de ces recherches correspond à un sujet "
        "réel de la veille, préfère-la : c'est ce que les lecteurs cherchent. "
        "Ne retiens jamais un sujet seulement parce qu'il est recherché : la barre "
        "d'importance reste la règle (pas de célébrité, de jeu ou de polémique sans "
        "enjeu de fond)."
    )
    return "\n".join(lignes)
