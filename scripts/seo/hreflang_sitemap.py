"""Ajoute les liens hreflang (français / anglais) dans sitemap.xml.

Pour chaque page française qui a son équivalent anglais dans le plan (et
inversement), on ajoute sous <loc> deux liens <xhtml:link rel="alternate">
(fr et en) et un lien x-default vers la version française.

Règles :
- une paire n'est écrite que si les deux adresses figurent dans le plan ;
- les pages sans équivalent (archives.html, guide, mentions…) ne changent pas ;
- <lastmod> et le reste du bloc ne bougent pas ;
- idempotent : relancer la fonction ne duplique rien.

Fonction publique : ajouter_hreflang(texte_xml) -> texte_xml.
"""

import re

SITE = "https://lesscenarios.fr"
NS_XHTML = "http://www.w3.org/1999/xhtml"

_LIEN_EXISTANT = re.compile(r"\n[ \t]*<xhtml:link [^\n]*/>(?=\n)")
_LOC = re.compile(r"([ \t]*)<loc>([^<]+)</loc>\n")
_ARCHIVE_FR = re.compile(re.escape(SITE) + r"/archives/(\d{4}-\d{2}-\d{2})\.html")
_ARCHIVE_EN = re.compile(re.escape(SITE) + r"/en/archives/(\d{4}-\d{2}-\d{2})\.html")


def equivalent(loc):
    """Renvoie (fr, en) pour une adresse française ou anglaise, sinon None."""
    if loc in (f"{SITE}/", f"{SITE}/en/"):
        return (f"{SITE}/", f"{SITE}/en/")
    m = _ARCHIVE_FR.fullmatch(loc)
    if m:
        return (loc, f"{SITE}/en/archives/{m.group(1)}.html")
    m = _ARCHIVE_EN.fullmatch(loc)
    if m:
        return (f"{SITE}/archives/{m.group(1)}.html", loc)
    return None


def ajouter_hreflang(xml):
    # 1. retirer les liens déjà présents (idempotence)
    xml = _LIEN_EXISTANT.sub("", xml)

    # 2. adresses réellement listées dans le plan
    listees = set(re.findall(r"<loc>([^<]+)</loc>", xml))
    ajoutes = []

    def ajouter_liens(m):
        indent, loc = m.group(1), m.group(2)
        paire = equivalent(loc)
        if paire is None:
            return m.group(0)
        fr, en = paire
        if fr not in listees or en not in listees:
            return m.group(0)
        ajoutes.append(loc)
        liens = (
            f'{indent}<xhtml:link rel="alternate" hreflang="fr" href="{fr}"/>\n'
            f'{indent}<xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
            f'{indent}<xhtml:link rel="alternate" hreflang="x-default" href="{fr}"/>\n'
        )
        return m.group(0) + liens

    xml = _LOC.sub(ajouter_liens, xml)

    # 3. déclarer l'espace de noms xhtml, seulement si des liens ont été ajoutés
    if ajoutes and "xmlns:xhtml=" not in xml and "<urlset" in xml:
        xml = xml.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            f'        xmlns:xhtml="{NS_XHTML}"',
            1,
        )
    return xml
