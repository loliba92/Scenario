"""
Construction déterministe du HTML d'une édition à partir du contenu
éditorial produit par le modèle de rédaction et du gabarit de la dernière
édition publiée (`index.html`).

Principe (voir docs/routine-redaction-prompt.md) : le modèle ne voit et ne
produit jamais le `<style>`, le header/nav/footer/scripts — uniquement le
contenu éditorial (JSON). Ce module réinjecte ce contenu dans le gabarit
existant, recopié tel quel pour tout ce qui ne change jamais d'une édition
à l'autre — même principe que la règle « recopier le `<style>`
intégralement » de `docs/routine-prompt.md` (étape technique 2), mais
appliqué ici par du code déterministe plutôt que rappelé dans un prompt :
aucun risque qu'une classe CSS disparaisse silencieusement un jour où elle
n'est pas utilisée (voir l'incident `.dek-list` documenté dans
`docs/ARCHITECTURE.md`).

Limites connues, assumées pour la Phase 1 (prototype, voir
`.github/workflows/edition.yml`) :
  - pas de sélection/téléchargement de photo de sujet (pipeline Pexels,
    `scripts/social/fetch_topic_image.py`) — image de repli générique,
    jamais un faux crédit photo inventé ;
  - pas de mise à jour de `archives.html`/`sources.html`/`themes/*.html`/
    `sitemap.xml`/`feed.xml` — hors périmètre de ce prototype (génération +
    validation + artifact uniquement, voir le cahier des charges validé) ;
  - pas de liens croisés vers des suivis actifs/archives passées — cette
    décision reste dans la partie recherche (brief), jamais improvisée ici.
Ces limites sont un choix explicite du prototype, pas un oubli — à traiter
séparément si la Phase 1 est validée.
"""
import re
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup

MOIS_FR = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]
# Abréviations françaises usuelles (même table que assets/site-search.js).
# Ne pas dériver de MOIS_FR[:4] : « octobre » donnait « octo. », « avril »
# « avri. », « mars » « mars. » (point abusif sur un mois non abrégé).
MOIS_FR_ABBR = [
    "janv.", "févr.", "mars", "avr.", "mai", "juin",
    "juil.", "août", "sept.", "oct.", "nov.", "déc.",
]
JOURS_FR = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS_EN_ABBR = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def _unwrap_own_tag(html, tag, cls):
    """Défense contre un modèle qui renvoie déjà la balise que ce module
    ajoute lui-même autour du contenu (ex. `dek` contenant
    `<p class="dek">...</p>` en plus du wrapper posé par build_hero()) —
    trouvé en conditions réelles le 14 septembre 2026 : un imbriquement
    `<p class="dek"><p class="dek">texte</p></p>` invalide faisait compter
    chaque paragraphe deux fois par le sélecteur CSS `.dek` de la
    validation de longueur, gonflant artificiellement le nombre de mots
    mesuré d'environ 2× (aucun rapport avec la vraie longueur affichée).
    Ne retire le wrapper que s'il encadre exactement tout le texte —
    jamais un retrait partiel qui pourrait mutiler un contenu légitime."""
    stripped = html.strip()
    m = re.match(rf'^<{tag}\s+class="{re.escape(cls)}"\s*>(.*)</{tag}>$', stripped, re.S)
    return m.group(1).strip() if m else html

# Balises <head> propres au jour — tout le reste de <head> est recopié tel
# quel depuis le gabarit (icônes, manifest, apple-*, pwa-install.css,
# preconnect, fonts, <style>...). Autant de prédicats que de familles de
# balises per-day à exclure de la recopie brute.
#
# meta charset/viewport/robots/language/color-scheme : bug réel trouvé le
# 28 septembre 2026 (retour utilisateur, dupliquées 5x sur index.html et
# 6x sur en/index.html en prod) — ces 5 balises sont TOUJOURS réémises
# telles quelles par le template englobant (<meta charset>/<meta
# name="viewport"> en dur dans assemble_index_html()/assemble_home_page())
# et par head_dynamic (build_head_dynamic()/build_home_head() : robots/
# language/color-scheme). Absentes d'_is_per_day, elles étaient donc AUSSI
# recopiées dans head_static à chaque extract_shell() — une régénération
# de index.html à partir de lui-même (cas normal : la home ET le pipeline
# quotidien extraient le shell depuis le VRAI index.html) en ajoutait une
# copie de plus à chaque fois, sans jamais en retirer. Jamais "per-day" au
# sens propre (elles ne varient pas d'une édition à l'autre) mais doivent
# être exclues de head_static pour la même raison technique : déjà
# garanties par ailleurs, jamais à recopier depuis le gabarit source.
_PER_DAY_HEAD_PREDICATES = [
    lambda t: t.name == "title",
    lambda t: t.name == "link" and t.get("rel") == ["canonical"],
    lambda t: t.name == "link" and t.get("rel") == ["alternate"],
    lambda t: t.name == "meta" and t.get("charset") is not None,
    lambda t: t.name == "meta" and t.get("name") == "viewport",
    lambda t: t.name == "meta" and t.get("name") == "description",
    lambda t: t.name == "meta" and t.get("name") == "domain",
    lambda t: t.name == "meta" and t.get("name") == "robots",
    lambda t: t.name == "meta" and t.get("name") == "language",
    lambda t: t.name == "meta" and t.get("name") == "color-scheme",
    lambda t: t.name == "meta" and (t.get("property") or "").startswith("og:"),
    lambda t: t.name == "meta" and (t.get("property") or "").startswith("article:"),
    lambda t: t.name == "meta" and (t.get("name") or "").startswith("twitter:"),
    lambda t: t.name == "script" and t.get("type") == "application/ld+json",
    lambda t: t.name == "style",  # géré séparément (style_block)
]


class ShellError(Exception):
    """Le gabarit source (index.html) ne contient pas un repère attendu —
    jamais un résultat partiel silencieux, toujours une erreur explicite."""


def _is_per_day(tag):
    return any(pred(tag) for pred in _PER_DAY_HEAD_PREDICATES)


def extract_shell(index_html_text):
    """Extrait du HTML de la dernière édition publiée tout ce qui ne
    change jamais d'une édition à l'autre. Retourne un dict de fragments
    HTML bruts (str) + l'entête d'édition courante (numéro)."""
    soup = BeautifulSoup(index_html_text, "html.parser")

    head = soup.select_one("head")
    if head is None:
        raise ShellError("aucun <head> dans le gabarit source")
    head_static_tags = [str(t) for t in head.find_all(recursive=False) if not _is_per_day(t)]

    style_tag = soup.select_one("style")
    if style_tag is None:
        raise ShellError("aucun <style> dans le gabarit source")

    masthead = soup.select_one("header.masthead")
    topnav = soup.select_one("nav.topnav")
    weekly_banner = soup.select_one("#weekly-banner")
    footer = soup.select_one("footer")
    for name, tag in [
        ("header.masthead", masthead), ("nav.topnav", topnav),
        ("#weekly-banner", weekly_banner),
        ("footer", footer),
    ]:
        if tag is None:
            raise ShellError(f"repère de gabarit introuvable : {name}")

    scripts_tail = "\n\n".join(str(s) for s in footer.find_next_siblings("script"))

    edition_div = masthead.select_one(".edition")
    m = re.search(r"N°(\d+)", edition_div.get_text()) if edition_div else None
    if not m:
        raise ShellError("numéro d'édition introuvable dans .edition")
    edition_number = int(m.group(1))

    legal_links = footer.select_one(".legal-links")
    if legal_links is None:
        raise ShellError("repère de gabarit introuvable : .legal-links")

    style_block_str = str(style_tag)
    # GARDE-FOU : s'assurer que la balise <style> n'est jamais vide ou cassée
    # (incident du 26 septembre 2026 : style_block cassé → page entièrement noire).
    # "<style" (préfixe, pas "<style>" exact) : ne doit jamais dépendre de
    # l'absence d'attribut sur la balise (ex. <style media="screen">).
    if not style_block_str or "<style" not in style_block_str or "</style>" not in style_block_str:
        raise ShellError(
            f"Balise <style> invalide dans le gabarit source : {len(style_block_str)} chars, "
            f"contient '<style' : {('<style' in style_block_str)}, "
            f"contient '</style>' : {('</style>' in style_block_str)}"
        )

    return {
        "head_static": "\n".join(head_static_tags),
        "style_block": style_block_str,
        "masthead_html": str(masthead),
        "topnav_html": str(topnav),
        "weekly_banner_html": str(weekly_banner),
        "legal_links_html": str(legal_links),
        "scripts_tail_html": scripts_tail,
        "edition_number": edition_number,
    }


def format_date_fr(date_str):
    """'2026-09-20' -> ('samedi', '20 septembre 2026')"""
    d = date.fromisoformat(date_str)
    jour = JOURS_FR[d.weekday()]
    return jour, f"{d.day} {MOIS_FR[d.month - 1]} {d.year}"


def build_head_dynamic(content, brief, date_str, canonical_url, photo=None):
    meta = content["meta"]
    title = meta["title"]
    description = meta["meta_description"]
    # photo (voir generate_post_edition.py) : dict {"og_image_url", "hero_image_url", "alt", ...}
    # si une photo de sujet a été retenue — sinon repli générique inchangé
    # (comportement historique de la Phase 1 rédaction, voir docstring de
    # ce module). og_image_alt vient de meta['og_image_alt'] (rédigé par
    # le modèle) dans les deux cas quand photo est absent ; avec une
    # photo réelle, on utilise la description factuelle de la photo elle-
    # même (photo['alt']), pas celle imaginée par le modèle pour une
    # image générique.
    if photo:
        og_image = photo["og_image_url"]
        og_image_width, og_image_height = "1080", "1080"
        og_image_alt = photo["alt"]
    else:
        og_image = "https://lesscenarios.fr/assets/social/og-image-v2.png"
        og_image_width, og_image_height = "2508", "1412"
        og_image_alt = meta["og_image_alt"]
    published = f"{date_str}T07:15:00+02:00"
    domain = brief["sujet"]["domain"]
    section_name = domain.replace("-", " ").title()
    en_canonical_url = canonical_url.replace("/archives/", "/en/archives/")

    # Utiliser le JSON-LD optimisé généré par seo_optimizer si disponible,
    # sinon générer le JSON-LD de base (comportement historique Phase 1)
    if "seo_newsarticle_json" in meta:
        ld_json = meta["seo_newsarticle_json"]
    else:
        # Fallback : génération manuelle (ancien comportement)
        ld_json = (
            "{\n"
            '  "@context": "https://schema.org",\n'
            '  "@type": "NewsArticle",\n'
            f'  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{canonical_url}" }},\n'
            f'  "headline": {content["h1"]!r},\n'
            f'  "description": {description!r},\n'
            f'  "image": ["{og_image}"],\n'
            f'  "datePublished": "{published}",\n'
            f'  "dateModified": "{published}",\n'
            '  "inLanguage": "fr-FR",\n'
            '  "author": { "@type": "Person", "name": "Olivier Bertrand", "url": "https://www.facebook.com/share/1LuiQ1cAmt/" },\n'
            '  "publisher": {\n'
            '    "@type": "Organization",\n'
            '    "name": "Scénario",\n'
            '    "logo": { "@type": "ImageObject", "url": "https://lesscenarios.fr/assets/logo-512.png", "width": 512, "height": 512 }\n'
            "  }\n"
            "}"
        ).replace("'", "&#39;")

    # Keywords meta tag (si disponible depuis seo_optimizer)
    keywords_meta = ""
    if "keywords" in meta and meta["keywords"]:
        keywords_str = ", ".join(meta["keywords"]) if isinstance(meta["keywords"], list) else meta["keywords"]
        keywords_meta = f'<meta name="keywords" content="{keywords_str}">\n'

    # BreadcrumbList JSON-LD (si disponible depuis seo_optimizer)
    breadcrumb_script = ""
    if "seo_breadcrumb_json" in meta:
        breadcrumb_script = f'<script type="application/ld+json">\n{meta["seo_breadcrumb_json"]}\n</script>\n'

    return f"""<title>{title}</title>
<link rel="canonical" href="{canonical_url}">
<link rel="alternate" hreflang="fr" href="{canonical_url}">
<link rel="alternate" hreflang="en" href="{en_canonical_url}">
<link rel="alternate" hreflang="x-default" href="{canonical_url}">
<meta name="description" content="{description}">
{keywords_meta}<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="language" content="fr-FR">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Scénario">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="{og_image_width}">
<meta property="og:image:height" content="{og_image_height}">
<meta property="og:image:alt" content="{og_image_alt}">
<meta property="og:image:type" content="image/png">
<meta property="article:author" content="Olivier Bertrand">
<meta property="article:published_time" content="{published}">
<meta property="article:modified_time" content="{published}">
<meta property="article:section" content="{section_name}">
<meta name="domain" content="{domain}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@scenario_fr">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">
{ld_json}
</script>
{breadcrumb_script}"""


def build_masthead(masthead_shell_html, date_str, edition_number):
    jour, date_longue = format_date_fr(date_str)
    new_edition_div = f'<div class="edition">Édition du {date_longue} · N°{edition_number}</div>'
    return re.sub(r'<div class="edition">.*?</div>', new_edition_div, masthead_shell_html, count=1)


def _kpi_indicator_html(ind):
    return (
        '<div class="indicator">\n'
        f'  <span class="label">{ind["label"]}</span>\n'
        f'  <span class="value">{ind["value"]} <span class="delta">{ind["delta"]}</span></span>\n'
        "</div>"
    )


def _comprendre_box_html(box):
    return (
        '<div class="comprendre-box">\n'
        '  <span class="comprendre-label">Comprendre</span>\n'
        f'  <p class="comprendre-lead">{box["lead"]}</p>\n'
        f'  <p class="comprendre-text">{box["text"]}</p>\n'
        "</div>"
    )


# ---------------------------------------------------------------------------
# .dc-chart-box — graphique en escalier pour série historique longue
# (docs/routine-prompt.md, § « Graphique en escalier »). Jusqu'au 15
# septembre 2026, ce composant n'existait QUE via un <script> JS écrit à la
# main par la routine manuelle pour chaque édition qui l'utilisait (voir
# archives/2026-08-21.html/2026-08-24.html, gardées comme référence
# historique) — jamais porté dans la chaîne automatisée
# (generate_daily_edition.py/build_html.py), ce que le brief du
# 14 septembre notait déjà explicitement : « Le prototype Phase 1 ne gère
# de toute façon pas encore ce composant. » Rendu ici SERVEUR (Python,
# SVG statique) plutôt qu'un <script> JS comme l'original — même rendu
# visuel (mêmes classes CSS déjà dans le gabarit), mais déterministe et
# sans dépendre de l'exécution JS côté client. brief["graphique_dc_chart"]["serie"]
# porte toutes les décisions éditoriales (unités, graduations, années
# affichées, points notables) — voir docs/routine-brief-format.md, ce
# script ne fait plus que du calcul géométrique.
# ---------------------------------------------------------------------------
_DC_CHART_W, _DC_CHART_H = 700, 240
_DC_CHART_PAD_L, _DC_CHART_PAD_R, _DC_CHART_PAD_T, _DC_CHART_PAD_B = 40, 12, 14, 30


def _dc_chart_svg_inner(serie):
    points = serie["points"]
    years = [p["annee"] for p in points]
    min_year, max_year = years[0], years[-1]
    plot_w = _DC_CHART_W - _DC_CHART_PAD_L - _DC_CHART_PAD_R
    plot_h = _DC_CHART_H - _DC_CHART_PAD_T - _DC_CHART_PAD_B
    y_max = serie["y_max"]

    def x_pos(year):
        if max_year == min_year:
            return _DC_CHART_PAD_L
        return round(_DC_CHART_PAD_L + (year - min_year) / (max_year - min_year) * plot_w, 2)

    def y_pos(value):
        return round(_DC_CHART_PAD_T + (1 - value / y_max) * plot_h, 2)

    parts = []

    for gl in serie.get("y_gridlines") or []:
        ly = y_pos(gl["valeur"])
        parts.append(
            f'<line x1="{_DC_CHART_PAD_L}" x2="{_DC_CHART_W - _DC_CHART_PAD_R}" y1="{ly}" y2="{ly}" class="dc-gridline"/>'
        )
        parts.append(
            f'<text x="{_DC_CHART_PAD_L - 8}" y="{ly + 3}" class="dc-axis-label" text-anchor="end">{gl["label"]}</text>'
        )

    for yr in serie.get("x_axis_years") or []:
        parts.append(
            f'<text x="{x_pos(yr)}" y="{_DC_CHART_H - _DC_CHART_PAD_B + 16}" class="dc-axis-label" '
            f'text-anchor="middle">{yr}</text>'
        )
    axis_y = _DC_CHART_H - _DC_CHART_PAD_B
    parts.append(f'<line x1="{_DC_CHART_PAD_L}" x2="{_DC_CHART_W - _DC_CHART_PAD_R}" y1="{axis_y}" y2="{axis_y}" class="dc-axis"/>')

    # Chemin en escalier : la valeur tient jusqu'au point suivant, jamais
    # d'interpolation continue entre deux points (même logique que
    # l'original) — pour chaque point i>0, deux segments : horizontal
    # jusqu'à la nouvelle année (à l'ancienne valeur), puis vertical vers
    # la nouvelle valeur.
    # style "ligne" : segments droits, pour un cours qui évolue en continu
    # (actif financier) — l'escalier y suggérerait un prix constant.
    path = f"M {x_pos(points[0]['annee'])} {y_pos(points[0]['valeur'])}"
    for i in range(1, len(points)):
        if serie.get("style") != "ligne":
            path += f" L {x_pos(points[i]['annee'])} {y_pos(points[i - 1]['valeur'])}"
        path += f" L {x_pos(points[i]['annee'])} {y_pos(points[i]['valeur'])}"
    parts.append(f'<path d="{path}" class="dc-line"/>')

    for p in points:
        is_last = bool(p.get("last"))
        cx, cy = x_pos(p["annee"]), y_pos(p["valeur"])
        r = 5 if is_last else 3
        cls = "dc-dot is-highlight" if is_last else "dc-dot"
        tooltip = p.get("tooltip", "")
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}"><title>{tooltip}</title></circle>')
        if p.get("peak"):
            parts.append(
                f'<text x="{cx}" y="{cy - 10}" class="dc-point-label is-favorable" '
                f'text-anchor="middle">{p.get("peak_label", "")}</text>'
            )
        if is_last:
            parts.append(
                f'<text x="{cx}" y="{cy - 28}" class="dc-point-label is-degrade" '
                f'text-anchor="end">{p.get("last_label", "")}</text>'
            )

    return "\n      ".join(parts)


def _dc_chart_box_html(serie):
    svg_inner = _dc_chart_svg_inner(serie)
    return f"""<div class="dc-chart-box">
      <span class="dc-chart-label">Repère historique</span>
      <p class="dc-chart-lead">{serie["lead"]}</p>
      <svg id="dc-svg" viewBox="0 0 {_DC_CHART_W} {_DC_CHART_H}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="{serie["aria_label"]}">
      {svg_inner}
      </svg>
      <p class="dc-chart-caption">{serie["caption"]}</p>
    </div>"""


# ---------------------------------------------------------------------------
# Graphique « Les chiffres du sujet » (barres) — ajouté le 4 octobre 2026.
# Le graphique en escalier (.dc-chart-box, ci-dessus) exige une longue série historique publique : presque jamais
# réunie, donc plus aucun graphique dans les éditions. Ce second graphique compare 3 à 6 chiffres RÉELS déjà présents
# dans les faits vérifiés du brief (brief["graphique_chiffres"]["barres"]) — jamais inventés. Même habillage que
# .dc-chart-box, rendu serveur en SVG statique.
# ---------------------------------------------------------------------------
_BARRES_W = 700
_BARRES_PAD_R = 170
_BARRES_ROW_H = 58


def _barres_valides(b):
    """Garde-fou : un graphique douteux est omis, jamais publié à moitié (ni erreur, ni page cassée)."""
    try:
        vals = b["valeurs"]
        if not (3 <= len(vals) <= 6):
            return False
        if not all(str(v.get("label", "")).strip() for v in vals):
            return False
        nums = [float(v["valeur"]) for v in vals]
        if any(n < 0 for n in nums) or max(nums) <= 0:
            return False
        return all(str(b.get(k, "")).strip() for k in ("lead", "caption", "aria_label"))
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


def _nombre_fr(x):
    texte = f"{x:.2f}".rstrip("0").rstrip(".")
    return texte.replace(".", ",")


def _barres_box_html(b):
    vals = b["valeurs"]
    nums = [float(v["valeur"]) for v in vals]
    vmax = max(nums)
    unite = str(b.get("unite", "")).strip()
    plot_w = _BARRES_W - _BARRES_PAD_R
    h = 8 + _BARRES_ROW_H * len(vals)
    parts = []
    for i, (v, n) in enumerate(zip(vals, nums)):
        top = 8 + i * _BARRES_ROW_H
        largeur = max(2.0, round(n / vmax * plot_w, 1))
        cls = "dc-bar is-highlight" if v.get("mis_en_avant") else "dc-bar"
        affichage = str(v.get("affichage") or (_nombre_fr(n) + (f" {unite}" if unite else "")))
        parts.append(f'<text x="0" y="{top + 16}" class="dc-bar-label">{v["label"]}</text>')
        parts.append(f'<rect x="0" y="{top + 24}" width="{largeur}" height="20" rx="3" class="{cls}"/>')
        parts.append(f'<text x="{round(largeur + 10, 1)}" y="{top + 40}" class="dc-bar-value">{affichage}</text>')
    svg_inner = "\n      ".join(parts)
    return f"""<div class="dc-chart-box">
      <span class="dc-chart-label">Les chiffres</span>
      <p class="dc-chart-lead">{b["lead"]}</p>
      <svg viewBox="0 0 {_BARRES_W} {h}" preserveAspectRatio="xMinYMid meet" role="img" aria-label="{b["aria_label"]}">
      {svg_inner}
      </svg>
      <p class="dc-chart-caption">{b["caption"]}</p>
    </div>"""


# ---------------------------------------------------------------------------
# Rappel d'un article précédent dans « Les faits » — ajouté le 4 octobre 2026 (retour de l'éditeur : plus aucune
# référence à nos articles précédents dans le texte). Construit mécaniquement à partir de articles_connexes du
# brief (3 articles choisis pour leur lien thématique), formule impersonnelle, jamais adressée au lecteur.
# ---------------------------------------------------------------------------
def _rappels_depuis_connexes(brief, maximum=2):
    rappels = []
    for a in (brief.get("articles_connexes") or [])[:maximum]:
        iso, titre = a.get("date", ""), a.get("titre", "")
        try:
            d = date.fromisoformat(iso)
        except ValueError:
            continue
        if not titre:
            continue
        rappels.append({"date": iso, "jour": f"{d.day} {MOIS_FR[d.month - 1]}", "titre": titre})
    return rappels


def _rappel_edition_html(r):
    return (
        '<p class="rappel-edition"><span class="rappel-edition-label">Déjà abordé sur Scénario</span> '
        f'<a href="archives/{r["date"]}.html">{fr_typo(r["titre"])}</a> '
        f'<span class="rappel-edition-date">({r["jour"]})</span></p>'
    )


def _list_box_html(lb):
    items = "\n".join(
        '<li>\n'
        f'  <span class="list-box-rank">{it["rank"]}</span>\n'
        '  <span class="list-box-body">\n'
        f'    <span class="list-box-title">{it["title"]}</span>\n'
        f'    <span class="list-box-meta">{it["meta"]}</span>\n'
        "  </span>\n"
        "</li>"
        for it in lb["items"]
    )
    foot = f'<p class="list-box-foot">{lb["foot"]}</p>' if lb.get("foot") else ""
    return (
        '<div class="list-box">\n'
        f'  <span class="list-box-label">{lb["label"]}</span>\n'
        f'  <ul class="list-box-items">\n{items}\n  </ul>\n'
        f"  {foot}\n"
        "</div>"
    )


def build_hero(content, date_str, photo=None, graphique_dc_chart=None, theme_link_html="", graphique_chiffres=None, rappels=None):
    jour, date_longue = format_date_fr(date_str)
    dek_blocks = []
    for i, dek_html in enumerate(content["dek"]):
        dek_blocks.append(f'<p class="dek">{_unwrap_own_tag(dek_html, "p", "dek")}</p>')
        for box in content.get("comprendre_box") or []:
            if box.get("apres_dek_index") == i:
                dek_blocks.append(_comprendre_box_html(box))
        # un rappel d'article précédent après le 2e paragraphe, un autre après le 4e (si le texte est assez long)
        for k, r in enumerate(rappels or []):
            if i == 1 + 2 * k and i < len(content["dek"]) - 1:
                dek_blocks.append(_rappel_edition_html(r))
    dek_html_full = "\n\n".join(dek_blocks)

    list_box_html = _list_box_html(content["list_box"]) if content.get("list_box") else ""
    indicators_html = "\n".join(_kpi_indicator_html(ind) for ind in content["indicators"])

    # .dc-chart-box (voir la note au-dessus de _dc_chart_box_html()) —
    # optionnel, jamais forcé : présent seulement si la recherche a
    # explicitement décidé "oui" ET fourni une série exploitable (voir
    # docs/routine-brief-format.md). "serie" reste `null` la plupart des
    # éditions, jamais une erreur.
    dc_chart_html = ""
    if graphique_dc_chart and graphique_dc_chart.get("decision") == "oui" and graphique_dc_chart.get("serie"):
        dc_chart_html = "\n\n    " + _dc_chart_box_html(graphique_dc_chart["serie"])
    elif graphique_chiffres and graphique_chiffres.get("decision") == "oui" and _barres_valides(graphique_chiffres.get("barres") or {}):
        # repli : à défaut de longue série historique, les chiffres réels du sujet (voir _barres_box_html)
        dc_chart_html = "\n\n    " + _barres_box_html(graphique_chiffres["barres"])

    # photo (voir generate_post_edition.py) : dict {"hero_image_url", "alt"}
    # si une photo de sujet a été retenue — sinon repli générique inchangé
    # (comportement historique de la Phase 1 rédaction). Volontairement
    # PAS og_image_url ici : og_image_url pointe vers le PNG Instagram
    # composé (titre + scénarios incrustés, pour les prévisualisations
    # sociales, voir build_head_dynamic()) — jamais la bonne image pour
    # l'<img> visible en tête d'article, qui doit montrer la photo brute
    # (voir docs/routine-prompt.md, étape « Image du sujet », structure
    # exacte de .article-image-photo). Bug réel trouvé le 14 septembre
    # 2026 : les deux étaient confondues, provoquant une superposition
    # visuelle (titre du PNG composé sous le vrai h1 de la page).
    if photo:
        hero_image = photo["hero_image_url"]
        image_alt = photo["alt"]
    else:
        hero_image = "https://lesscenarios.fr/assets/social/og-image-v2.png"
        image_alt = content['meta']['og_image_alt']

    return f"""<section class="hero" id="contexte">
  <figure class="article-image">
    <div class="article-image-photo-wrap">
      <img class="article-image-photo" src="{hero_image}" alt="{image_alt}">
      <div class="article-image-scrim"></div>
      <div class="article-image-masthead">
        <img class="article-image-logo" src="assets/logo.svg" alt="">
        <span class="article-image-wordmark">Scéna<span>rio</span></span>
      </div>
      <div class="article-image-overlay wrap">
        <p class="eyebrow">{jour.capitalize()}, {content.get('eyebrow_suffix', '')}</p>
        <h1>{fr_typo(content['h1'])}</h1>
        <p class="question-text">{content['question_text']}</p>
        <p class="pubdate">Publié le {date_longue}</p>
      </div>
    </div>
  </figure>
  <div class="wrap">
    <p class="share-inline">
      <span class="share-inline-label">Partager :</span>
      <a href="#" id="share-x" aria-label="Partager sur X" title="Partager sur X"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M5 5L19 19M19 5L5 19"/></svg></a>
      <a href="#" id="share-bluesky" aria-label="Partager sur Bluesky" title="Partager sur Bluesky"><svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3.468 1.948C5.303 3.325 7.276 6.118 8 7.616c.725-1.498 2.698-4.29 4.532-5.668C13.855.955 16 .186 16 2.632c0 .489-.28 4.105-.444 4.692-.572 2.04-2.653 2.561-4.504 2.246 3.236.551 4.06 2.375 2.281 4.2-3.376 3.464-4.852-.87-5.23-1.98-.07-.204-.103-.3-.103-.218 0-.081-.033.014-.102.218-.379 1.11-1.855 5.444-5.231 1.98-1.778-1.825-.955-3.65 2.28-4.2-1.85.315-3.932-.205-4.503-2.246C.28 6.737 0 3.12 0 2.632 0 .186 2.145.955 3.468 1.948"/></svg></a>
      <a href="#" id="share-facebook" aria-label="Partager sur Facebook" title="Partager sur Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15 4h-2a4 4 0 0 0-4 4v3H7v4h2v7h4v-7h2.6l.4-4H13V8a1 1 0 0 1 1-1h2V4z"/></svg></a>
      <a href="#" id="share-linkedin" aria-label="Partager sur LinkedIn" title="Partager sur LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="6" cy="6" r="2"/><rect x="4.5" y="10" width="3" height="9"/><path d="M11 10h3v1.5c.7-1 1.8-1.8 3.3-1.8 2.6 0 4.2 1.7 4.2 5.1V19h-3v-3.7c0-1.6-.6-2.6-1.9-2.6-1 0-1.6.7-1.9 1.4-.1.3-.1.6-.1 1V19h-3V10z"/></svg></a>
      <a href="#" id="share-whatsapp" aria-label="Partager sur WhatsApp" title="Partager sur WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.4L3 21l4.8-1.2A9 9 0 1 0 12 3zm4.7 12.4c-.2.6-1.2 1.1-1.7 1.2-.4.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.6-2.7-1.2-4.4-3.9-4.6-4.1-.1-.2-1.1-1.4-1.1-2.7 0-1.3.7-1.9.9-2.1.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.4.2.5.7 1.7.8 1.8.1.1.1.3 0 .5-.1.2-.1.3-.3.5-.1.2-.3.4-.4.5-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.5 1.5.3.1.5.1.6-.1.2-.2.7-.8.9-1.1.2-.3.4-.2.6-.1.2.1 1.5.7 1.7.8.2.1.4.2.5.3.1.2.1.7-.1 1.3z"/></svg></a>
      <a href="#" id="share-telegram" aria-label="Partager sur Telegram" title="Partager sur Telegram"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2 12l19-9-7 19-3-7-6-3z"/></svg></a>
      <button type="button" id="share-copy" aria-label="Copier le lien" title="Copier le lien"><svg class="share-icon-link" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M10 14a5 5 0 0 0 7.5.5l2-2a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7.5-.5l-2 2a5 5 0 0 0 7 7l1-1"/></svg><svg class="share-icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg></button>
      <a href="https://google.com/preferences/source?q=lesscenarios.fr" id="share-google" target="_blank" rel="noopener noreferrer" aria-label="Ajouter Scénario à vos sources Google" title="Ajouter Scénario à vos sources Google"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5l2.5 5.4 5.9.7-4.4 4 1.2 5.8L12 16.5l-5.2 2.9 1.2-5.8-4.4-4 5.9-.7z"/></svg></a>
    </p>

    <nav class="toc" aria-label="Sommaire de l'édition">
      <a href="#scenarios">Scénarios</a>
      <a href="#essentiel">L'essentiel</a>
      <a href="#lexique">Référence</a>
    </nav>
{theme_link_html}
    <p class="section-label">Les faits</p>

    {dek_html_full}

    {list_box_html}

    <div class="indicator-strip">
      {indicators_html}
    </div>
{dc_chart_html}

  </div>
</section>"""


def _card_html(kind, label, data):
    indicateurs_li = "\n".join(
        '<li>\n'
        f'  <span class="field-name">{ind["field_name"]}</span>\n'
        f'  <span class="evo-current">{ind["evo_current"]}</span> <span class="evo-arrow is-{ind["evo_arrow"]}">'
        + {"up": "↑", "down": "↓", "flat": "→"}[ind["evo_arrow"]]
        + f'</span> <span class="evo-prev">{ind["evo_prev"]}</span>\n'
        "</li>"
        for ind in data["indicateurs_touches"]
    )
    why_html = "\n".join(f'<p class="why">{_unwrap_own_tag(w, "p", "why")}</p>' for w in data["why"])
    arrow_char = "↑" if data["france_impact"] == "favorable" else "↓"
    arrow_cls = "is-up" if data["france_impact"] == "favorable" else "is-down"
    france_word = "favorable" if data["france_impact"] == "favorable" else "défavorable"
    return f"""<article class="card" data-kind="{kind}">
  <div class="card-head">
  <span class="kind-tag">{label}</span>
  <div class="gauge">
    <svg viewBox="0 0 108 64">
      <path class="gauge-track" d="M9,58 A45,45 0 0,1 99,58"/>
      <path class="gauge-value" data-pct="{data['pct']}" d="M9,58 A45,45 0 0,1 99,58"/>
    </svg>
    <div class="gauge-num">{data['pct']}%</div>
  </div>
  <div class="gauge-word">{data['gauge_word']}</div>
  <h3>{data['h3']}</h3>
  </div>
  <div class="card-body">
  {why_html}
  <hr class="divider">
  <div class="field">
    <span class="field-label">Indicateurs touchés</span>
    <ul>
      {indicateurs_li}
    </ul>
  </div>
  <div class="france-line" data-france-impact="{data['france_impact']}">
    <span class="field-label">Concrètement en France</span>
    {data['france_line']} <span class="evo-arrow {arrow_cls}">{arrow_char}</span> Plutôt {france_word} pour la France.
  </div>
  </div>
</article>"""


def build_scenarios(content):
    labels = {"favorable": "Favorable", "stable": "Stable", "degrade": "Dégradé"}
    branches = "\n".join(
        f'<li data-kind="{kind}"><span class="stakes-tag">{labels[kind]}</span>{content["stakes_branches"][kind]}</li>'
        for kind in ("favorable", "stable", "degrade")
    )
    cards = "\n\n".join(
        _card_html(kind, labels[kind], content["cards"][kind])
        for kind in ("favorable", "stable", "degrade")
    )
    essentiel_paras = "\n".join(f'<p class="essentiel-text">{p}</p>' for p in content["essentiel_box"])
    df = content["delta_france"]
    # phrase_a_retenir — ajouté le 19 septembre 2026, remplace l'ancienne
    # extraction a posteriori du "chiffre" pub (voir docs/ARCHITECTURE.md) :
    # cette même phrase, affichée ici, est reprise mot pour mot par
    # scripts/pub/generate_daily_pub.py pour le post du jour — jamais
    # reformulée entre les deux. phrase_a_retenir_stat est mis en évidence
    # (1re occurrence seulement, pour ne pas doubler si le chiffre apparaît
    # deux fois dans la phrase) plutôt que redemandé au modèle en HTML.
    retenir_text = content["phrase_a_retenir"]
    retenir_stat = content.get("phrase_a_retenir_stat") or ""
    if retenir_stat and retenir_stat in retenir_text:
        retenir_text = retenir_text.replace(retenir_stat, f"<strong>{retenir_stat}</strong>", 1)
    return f"""<section class="scenarios" id="scenarios">
  <div class="wrap">
    <p class="section-label">Favorable, stable ou dégradé</p>
    <h2 class="section-title">{content['section_title']}</h2>

    <div class="stakes-box">
      <span class="stakes-label">Ce qu'on évalue</span>
      <ul class="stakes-branches">
        {branches}
      </ul>
    </div>

    <div class="cards">

      {cards}

    </div>

    <p class="indicators-note">Ordres de grandeur indicatifs pour les 3 scénarios ci-dessus, estimés avec l'information disponible à la publication et réévalués si la situation change — jamais des prévisions garanties. <a href="le-projet.html">En savoir plus sur notre méthode →</a></p>

    <div class="essentiel-box" id="essentiel">
      <span class="essentiel-label">L'essentiel</span>
      {essentiel_paras}
      <div class="delta-france" data-kind="{df['kind']}">
        <div class="delta-gauge">
          <svg viewBox="0 0 108 64">
            <defs>
              <linearGradient id="deltaGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:var(--degrade)"/>
                <stop offset="50%" style="stop-color:var(--stable)"/>
                <stop offset="100%" style="stop-color:var(--favorable)"/>
              </linearGradient>
            </defs>
            <path class="delta-gauge-track" d="M9,58 A45,45 0 0,1 99,58" stroke="url(#deltaGrad)"/>
            <circle class="delta-gauge-marker" data-score="{df['score']:.2f}" cx="54" cy="13" r="5"/>
          </svg>
          <div class="delta-gauge-word">{df['word'].capitalize()}</div>
        </div>
        <p class="essentiel-text delta-text"><svg class="delta-flag" viewBox="0 0 21 15" width="16" height="11" aria-hidden="true"><rect x="0" y="0" width="7" height="15" fill="#2a4d8f"/><rect x="7" y="0" width="7" height="15" fill="#ece7da"/><rect x="14" y="0" width="7" height="15" fill="#bd6248"/></svg> <strong>Notre évaluation de l'impact pour la France : <span class="delta-word">{df['word']}</span>.</strong> {df['text']}</p>
      </div>
    </div>

    <div class="retenir-box" id="retenir" data-stat="{retenir_stat}">
      <span class="retenir-label">Si tu devais retenir 1 chose</span>
      <p class="retenir-text">{retenir_text}</p>
    </div>

    <div class="follow-inline">
      <p class="follow-inline-text">Ne rate pas la prochaine édition :</p>
      <div class="follow-inline-actions">
        <button type="button" class="onesignal-subscribe-btn btn-outline"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 10.5a6 6 0 0 1 12 0c0 3.2 1 4.7 1.5 5.3H4.5C5 15.2 6 13.7 6 10.5Z"/><path d="M10.3 18.5a1.8 1.8 0 0 0 3.4 0"/></svg> <span class="btn-label">Activer les notifications</span></button>
        <a class="btn-outline" href="newsletter.html"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="1.5"/><path d="M4.5 7 12 12.5 19.5 7"/></svg> Newsletter</a>
      </div>
    </div>

  </div>
</section>"""


def build_lexique(content):
    entries = "\n".join(
        f'<dt id="lex-{term["slug"]}">{term["terme"]}</dt>\n<dd>{term["definition"]}</dd>'
        for term in content["lexique"]
    )
    return f"""<section class="lexique" id="lexique">
  <div class="wrap">
    <p class="section-label">Pour ceux qui découvrent le sujet</p>
    <h2 class="section-title">Petit lexique</h2>
    <dl class="glossary">
      {entries}
    </dl>
    <a class="cross-link" href="glossaire.html">Voir tous les termes déjà expliqués → Glossaire</a>
  </div>
</section>"""


def build_sources(content, date_str):
    links = "\n".join(f"<li>{s}</li>" for s in content["sources_html"])
    return f"""<section class="sources" id="sources">
  <div class="wrap">
    <p class="section-label">Pour aller plus loin</p>
    <h2 class="section-title">Sources</h2>
    <ul class="sources-list">
      {links}
    </ul>
    <p style="margin-top:16px"><a href="sources.html#{date_str}" style="color:var(--gold);text-decoration:none">Voir aussi la revue de presse du jour →</a></p>
  </div>
</section>"""


_SHARE_BLOCK = """<section class="share-block" id="nous-suivre">
  <div class="wrap">
    <p class="section-label">Reste connecté</p>
    <h2 class="section-title">Vote avant le résultat, retrouve-nous partout</h2>
    <p>Chaque jour, un sondage sur notre canal Telegram : vote pour le scénario que tu juges le plus probable avant même de découvrir les vraies probabilités ci-dessus.</p>
    <p>Retrouve-nous aussi sur tous nos réseaux :</p>
    <div class="share-row">
      <a class="follow-btn" href="https://x.com/scenario_fr" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="4" x2="20" y2="20"></line><line x1="20" y1="4" x2="4" y2="20"></line></svg> X</a>
      <a class="follow-btn" href="https://bsky.app/profile/scenario-actu.bsky.social" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M3.468 1.948C5.303 3.325 7.276 6.118 8 7.616c.725-1.498 2.698-4.29 4.532-5.668C13.855.955 16 .186 16 2.632c0 .489-.28 4.105-.444 4.692-.572 2.04-2.653 2.561-4.504 2.246 3.236.551 4.06 2.375 2.281 4.2-3.376 3.464-4.852-.87-5.23-1.98-.07-.204-.103-.3-.103-.218 0-.081-.033.014-.102.218-.379 1.11-1.855 5.444-5.231 1.98-1.778-1.825-.955-3.65 2.28-4.2-1.85.315-3.932-.205-4.503-2.246C.28 6.737 0 3.12 0 2.632 0 .186 2.145.955 3.468 1.948"></path></svg> Bluesky</a>
      <a class="follow-btn" href="https://www.linkedin.com/company/136694258/" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="4" fill="none" stroke="currentColor" stroke-width="1.6"></rect><circle cx="7.7" cy="7.6" r="1.3" fill="currentColor"></circle><line x1="7.7" y1="10.6" x2="7.7" y2="17.3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"></line><path d="M11.6 17.3v-4.2c0-1.5 1-2.4 2.3-2.4s2.3.9 2.3 2.4v4.2M11.6 10.6v.1" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg> LinkedIn</a>
      <a class="follow-btn" href="https://www.facebook.com/share/1DZVhe3KtR/" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><rect x="1" y="1" width="22" height="22" rx="6" fill="#000" stroke="currentColor" stroke-width="1"></rect><rect x="10.3" y="9.5" width="2.4" height="9" fill="#fff"></rect><rect x="10.3" y="6" width="4.7" height="2.6" rx="1" fill="#fff"></rect><rect x="7.8" y="11.6" width="6.5" height="2" fill="#fff"></rect></svg> Facebook</a>
      <a class="follow-btn" href="https://www.instagram.com/scenarios.actu/" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg> Instagram</a>
      <a class="follow-btn" href="https://t.me/scenario_fr" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M2 12l19-9-7 19-3-7-6-3z"/></svg> Telegram</a>
      <a class="follow-btn" href="https://open.spotify.com/show/1eycE00I2egdNO50oqeDFQ" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><path d="M6.8 9.4c3.6-1 7.4-.7 10.6 1"></path><path d="M7.4 12.6c3-.8 6-.5 8.6.9"></path><path d="M8 15.6c2.4-.6 4.7-.4 6.6.7"></path></svg> Spotify</a>
      <a class="follow-btn" href="https://google.com/preferences/source?q=lesscenarios.fr" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"></path></svg> Source préférée Google</a>
    </div>
    <div class="share-row" style="margin-top:14px">
      <button type="button" id="onesignal-subscribe-btn" class="onesignal-subscribe-btn btn-outline"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 10.5a6 6 0 0 1 12 0c0 3.2 1 4.7 1.5 5.3H4.5C5 15.2 6 13.7 6 10.5Z"/><path d="M10.3 18.5a1.8 1.8 0 0 0 3.4 0"/></svg> <span class="btn-label">Activer les notifications</span></button>
      <a class="btn-outline" href="https://buymeacoffee.com/scenario" target="_blank" rel="noopener noreferrer">☕ Nous offrir un café</a>
    </div>
  </div>
</section>"""


# Bandeau d'intro affiché une seule fois par visiteur (localStorage,
# voir le <script> qui le pilote dans scripts_tail_html), sur les pages
# article/archive uniquement — jamais sur la home depuis la home redesign
# du 27 septembre 2026 : son texte y fait doublon avec le hero fixe qui
# introduit déjà le principe du site (retour utilisateur du 28 septembre
# 2026). Constante plutôt qu'un fragment extrait de shell (comme
# _SHARE_BLOCK ci-dessus) : depuis que la home ne le republie plus,
# extract_shell() ne peut plus compter sur sa présence dans index.html
# pour le retrouver.
_INTRO_BANNER_HTML = """<div class="intro-banner" hidden="" id="intro-banner">
<div class="wrap intro-banner-inner">
<button aria-label="Fermer ce message" class="intro-banner-close" id="intro-banner-close" type="button">
<svg aria-hidden="true" fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-width="2" viewbox="0 0 24 24" width="16"><path d="M5 5L19 19M19 5L5 19"></path></svg>
</button>
<div class="intro-banner-body">
<img alt="" aria-hidden="true" class="intro-banner-icon" src="assets/logo.svg"/>
<div>
<p class="intro-banner-lead">L'actu, oui. Et après ?</p>
<p class="intro-banner-text">Chaque jour, un sujet qui compte, décortiqué en trois scénarios chiffrés, avec une probabilité pour chacun. Jamais figée : elle évolue si la situation change.</p>
</div>
</div>
</div>
</div>"""


def build_related_articles(brief, repo_root=None):
    """Génère la section des articles connexes à partir des données du brief.
    Utilise le titre exact du brief (champ 'titre' des articles_connexes).
    Retourne une chaîne HTML ou vide si pas d'articles connexes."""
    articles = brief.get("articles_connexes", [])
    if not articles or len(articles) == 0:
        return ""

    articles_html = []
    for article in articles:
        article_date = article.get("date", "")
        if not article_date:
            continue

        # Utiliser le titre exact du brief
        title = article.get("titre", "Article")

        # Formater la date (YYYY-MM-DD -> "DD mois.")
        try:
            date_parts = article_date.split("-")
            day = int(date_parts[2])
            month = int(date_parts[1])
            formatted_date = f"{day} {MOIS_FR_ABBR[month - 1]}"
        except Exception:
            formatted_date = article_date

        article_html = f'''      <li><a href="archives/{article_date}.html" class="related-articles-item">
        <img class="related-articles-image" src="assets/social/topic-images/{article_date}.jpg" alt="{title}">
        <div class="related-articles-content">
          <span class="related-articles-date">{formatted_date}</span>
          <span class="related-articles-title">{fr_typo(title)}</span>
        </div>
      </a></li>'''
        articles_html.append(article_html)

    if not articles_html:
        return ""

    return f'''<section class="related-articles">
  <div class="wrap">
    <p class="section-label">À approfondir</p>
    <h2 class="section-title">Articles connexes</h2>
    <ul class="related-articles-list">
{(chr(10)).join(articles_html)}
    </ul>
  </div>
</section>'''


def build_theme_more(brief, date_str, repo_root=None):
    """Bloc « Plus sur cette matière » en bas de l'édition (après les sources) :
    les 2 éditions les plus récentes de la même matière + lien vers
    themes/{slug}.html. Ajouté le 4 octobre 2026 : les pages thèmes n'étaient
    reliées que depuis les archives. Lit archives.html (une ligne par édition,
    la plus récente en premier). Vide si le domaine n'a pas de page thème
    (ex. sport) ou s'il n'y a aucune autre édition — jamais de lien cassé."""
    slug = (brief.get("sujet") or {}).get("domain")
    label = THEME_SLUG_LABELS.get(slug)
    if not label:
        return ""
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
    try:
        text = (root / "archives.html").read_text(encoding="utf-8")
    except OSError:
        return ""
    cards = []
    for m in re.finditer(r'<tr data-domain="([a-z-]*)"[^>]*>(.*?)</tr>', text, re.S):
        if m.group(1) != slug:
            continue
        a = re.search(r'<a href="archives/(\d{4}-\d{2}-\d{2})\.html"[^>]*>([^<]+)</a>', m.group(2))
        if not a or a.group(1) >= date_str:
            continue
        d, title = a.groups()
        cards.append(f'''      <li><a href="archives/{d}.html" class="related-articles-item">
        <img class="related-articles-image" src="assets/social/topic-images/{d}.jpg" alt="">
        <div class="related-articles-content">
          <span class="related-articles-date">{int(d[8:10])} {MOIS_FR_ABBR[int(d[5:7]) - 1]}</span>
          <span class="related-articles-title">{fr_typo(title)}</span>
        </div>
      </a></li>''')
        if len(cards) == 2:
            break
    if not cards:
        return ""
    label_html = label.replace("&", "&amp;")
    return f'''<section class="related-articles theme-more">
  <div class="wrap">
    <p class="section-label">Plus sur cette matière</p>
    <h2 class="section-title">{label_html}</h2>
    <ul class="related-articles-list">
{chr(10).join(cards)}
    </ul>
    <a class="cross-link" href="themes/{slug}.html">Toutes les éditions «&nbsp;{label_html}&nbsp;»&nbsp;→</a>
  </div>
</section>'''


# Élargie le 28 septembre 2026 (chantier multi-éditions/jour, retour
# utilisateur) : reconnaît aussi archives/{date}-{slug}.html, pour les
# éditions supplémentaires publiées le même jour (contributions
# journalistes indépendants, en plus de l'édition IA quotidienne qui
# garde elle "{date}.html" nu, sans suffixe — zéro changement sur les URLs
# déjà indexées). Groupe 1 : la date seule (formatage/tri) ; le nom de
# fichier entier (sans ".html") sert d'identifiant unique d'édition
# ("edition_id", voir build_archive_entry()) — jamais juste la date, qui
# ne distingue plus deux éditions du même jour.
_ARCHIVE_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-[a-z0-9-]+)?\.html$")


def extract_og_title(text, fallback=None):
    """Extrait le contenu de <meta property="og:title" content="..."> peu
    importe l'ordre des attributs : les archives FR sont écrites par
    templating Python simple (property avant content, toujours), mais les
    archives EN passent par un round-trip BeautifulSoup
    (scripts/en/translate_daily.py build_en_soup()), qui réordonne les
    attributs alphabétiquement (content avant property) — la balise
    entière est matchée d'abord, content en extrait ensuite, peu importe
    l'ordre. Retire le suffixe " — Scénario" s'il est présent. Retourne
    `fallback` si la balise est introuvable.

    og:title est plafonné à 60 caractères pour le SEO (« … » en fin de
    coupe) : s'il est tronqué, on prend le <h1> de la page, qui porte le
    titre complet (bug du 2 octobre 2026 sur les cartes de en/index.html)."""
    tag_m = re.search(r'<meta[^>]*\bproperty="og:title"[^>]*/?>', text)
    content_m = re.search(r'\bcontent="([^"]*)"', tag_m.group(0)) if tag_m else None
    if not content_m:
        return fallback
    title = content_m.group(1).rsplit(" — Scénario", 1)[0]
    if title.endswith("…"):
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
        if h1:
            full = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
            if full:
                return full
    return title


def extract_article_domain(text):
    """Extrait le contenu de <meta property="article:section" content="...">
    (déjà en Title Case côté FR, ex. "Sport", "Economie Mondiale") — même
    tolérance à l'ordre des attributs qu'extract_og_title(). None si absent
    (pages sans domaine, ex. le-projet.html s'il était scanné par erreur)."""
    tag_m = re.search(r'<meta[^>]*\bproperty="article:section"[^>]*/?>', text)
    content_m = re.search(r'\bcontent="([^"]*)"', tag_m.group(0)) if tag_m else None
    return content_m.group(1) if content_m else None


def extract_meta_description(text):
    """Extrait le contenu de <meta name="description" content="..."> — la
    question_posee du brief (voir generate_seo_head.py _build_description()),
    déjà tronquée à 160 caractères et échappée HTML. Même tolérance à
    l'ordre des attributs qu'extract_og_title(). None si absent."""
    tag_m = re.search(r'<meta[^>]*\bname="description"[^>]*/?>', text)
    content_m = re.search(r'\bcontent="([^"]*)"', tag_m.group(0)) if tag_m else None
    return content_m.group(1) if content_m else None


def build_archive_entry(repo_root, edition_id, path, image_path_prefix="", domain_translator=None):
    """Construit une entrée {"edition_id", "date_str", "title", "image_url",
    "domain", "question"} pour UN fichier d'archive déjà connu — factorisé hors de
    get_latest_archives() pour être aussi utilisable sur une archive qui
    vient d'être écrite mais n'est pas encore visible pour un scan "avant
    aujourd'hui" (voir scripts/en/translate_daily.py build_en_index_page() :
    l'archive EN du jour existe déjà sur disque à ce stade du pipeline,
    mais get_latest_archives(before_date_str=date_str) l'exclurait quand
    même, la comparaison étant strictement "<").

    edition_id : nom du fichier sans ".html" — "{date}" pour l'édition IA
    du jour, "{date}-{slug}" pour une édition supplémentaire du même jour
    (chantier multi-éditions/jour, 28 septembre 2026). Sert de clé pour le
    lien (archives/{edition_id}.html) ET pour l'image associée
    (topic-images/{edition_id}.jpg) — jamais la seule date, qui ne
    distingue plus deux éditions publiées le même jour. `date_str` (les 10
    premiers caractères, toujours "AAAA-MM-JJ" par construction) reste
    utilisé pour tout ce qui est purement calendaire (titre de repli,
    formatage d'affichage) : c'est la date de PUBLICATION qu'on affiche,
    peu importe combien d'éditions ce jour-là.

    domain_translator (optionnel) : fonction str -> str appliquée au
    domaine extrait — jamais traduit côté FR (déjà dans la bonne langue),
    utilisé côté EN (voir scripts/en/translate_daily.py DOMAIN_FR_EN) car
    article:section n'est pas retraduit par build_en_soup(), donc les
    pages en/archives/*.html le portent encore tel quel en français."""
    date_str = edition_id[:10]
    text = path.read_text(encoding="utf-8")
    title = extract_og_title(text, fallback=date_str)
    domain = extract_article_domain(text)
    if domain and domain_translator:
        domain = domain_translator(domain)
    question = extract_meta_description(text)
    image_path = Path(repo_root) / "assets" / "social" / "topic-images" / f"{edition_id}.jpg"
    image_url = (
        f"{image_path_prefix}assets/social/topic-images/{edition_id}.jpg" if image_path.exists()
        else f"{image_path_prefix}assets/social/og-image-v2.png"
    )
    return {"edition_id": edition_id, "date_str": date_str, "title": title, "image_url": image_url,
            "domain": domain, "question": question}


def get_latest_archives(repo_root, before_date_str, count=4, archives_dir="archives",
                         image_path_prefix="", domain_translator=None):
    """Scanne {archives_dir}/*.html (jamais .../fragments/) et retourne les
    `count` éditions les plus récentes strictement antérieures à
    before_date_str, triées de la plus récente à la plus ancienne. Chaque
    entrée : {"edition_id", "date_str", "title", "image_url", "domain"}.
    Le tri par nom de fichier suffit (préfixe YYYY-MM-DD, donc l'ordre
    alphabétique est l'ordre chronologique) — aucun besoin de parser les
    dates. Depuis le 28 septembre 2026 (multi-éditions/jour), plusieurs
    fichiers peuvent partager le même préfixe de date
    ("{date}.html"/"{date}-{slug}.html") : le tri secondaire se fait alors
    sur le nom de fichier entier, sans prétendre à un ordre chronologique
    réel entre deux éditions du même jour (aucun horodatage dans le nom de
    fichier par construction) — seulement un ordre déterministe.

    archives_dir : "archives" (défaut, FR) ou "en/archives" (home EN, voir
    scripts/en/translate_daily.py build_en_index_page()) — les traductions
    déjà faites, jamais un nouvel appel LLM pour construire une home EN.
    image_path_prefix : "" pour la home FR (assets/... est déjà relatif à
    la racine) ; "../" pour la home EN (en/index.html est un niveau plus
    bas) — les photos de sujet sont partagées entre les deux langues, seul
    le chemin relatif change."""
    archives_path = Path(repo_root) / archives_dir
    dated_files = []
    for f in archives_path.glob("*.html"):
        m = _ARCHIVE_DATE_RE.match(f.name)
        if m and m.group(1) < before_date_str:
            dated_files.append((m.group(1), f.stem, f))
    dated_files.sort(key=lambda t: (t[0], t[1]), reverse=True)

    entries = []
    for date_str, edition_id, f in dated_files[:count]:
        entries.append(build_archive_entry(repo_root, edition_id, f, image_path_prefix, domain_translator))
    return entries


def get_today_editions(repo_root, date_str, archives_dir="archives", image_path_prefix="", domain_translator=None):
    """Scanne {archives_dir}/*.html et retourne TOUTES les éditions déjà
    écrites sur le disque pour `date_str` précisément (jamais avant, jamais
    après) — contrairement à get_latest_archives() (avant date_str,
    strictement). Chantier multi-éditions/jour, 28 septembre 2026 : sert à
    distinguer, sur la home, l'édition IA du jour (featured) des éditions
    supplémentaires publiées le même jour (contributions journalistes —
    section "Aussi aujourd'hui", voir assemble_home_page()). Triées avec
    l'édition IA (edition_id == date_str, sans suffixe) en premier si elle
    existe, les autres ensuite par edition_id — un ordre déterministe,
    jamais une vraie chronologie intra-jour (aucun horodatage dans le nom
    de fichier par construction, voir get_latest_archives())."""
    archives_path = Path(repo_root) / archives_dir
    same_day = []
    for f in archives_path.glob(f"{date_str}*.html"):
        m = _ARCHIVE_DATE_RE.match(f.name)
        if m and m.group(1) == date_str:
            same_day.append(f.stem)
    same_day.sort(key=lambda edition_id: (edition_id != date_str, edition_id))
    return [
        build_archive_entry(repo_root, edition_id, archives_path / f"{edition_id}.html",
                             image_path_prefix, domain_translator)
        for edition_id in same_day
    ]


def _format_date_short(date_str, lang="fr"):
    """'2026-09-20' -> '20 sept.' (fr) ou 'Sep 20' (en) — même format court
    que build_related_articles() côté FR. lang="en" : bug repéré le
    28 septembre 2026, en/index.html affichait encore "27 sept." sur ses
    cartes — cette chaîne varie chaque jour donc apply_chrome_translations()
    (correspondance FR -> EN exacte et stable) ne peut jamais la traduire."""
    d = date.fromisoformat(date_str)
    if lang == "en":
        return f"{MOIS_EN_ABBR[d.month - 1]} {d.day}"
    return f"{d.day} {MOIS_FR_ABBR[d.month - 1]}"


def build_home_cards(articles, lang="fr", section_id="dernieres-editions",
                      section_label="Les éditions précédentes",
                      section_title="Dernières éditions",
                      cross_link_html='<a class="cross-link" href="archives.html">Voir toutes les archives →</a>'):
    """Cartes vers un groupe d'éditions, même gabarit visuel que
    build_related_articles() (classes .related-articles-*, CSS déjà présent
    dans le style_block du gabarit — aucun nouveau CSS à ajouter). Domaine
    affiché avant la date (ex. "Sport · 27 sept.") pour orienter le
    lecteur sans qu'il ait à lire le titre en entier — demandé par
    l'utilisateur le 28 septembre 2026. lang="en" : passé à
    _format_date_short() (voir son docstring — une date ne peut jamais être
    traduite par apply_chrome_translations, table FR -> EN exacte et
    figée).

    section_id/label/title/cross_link_html (optionnels) : réutilisée telle
    quelle pour le bloc "Aussi aujourd'hui" (chantier multi-éditions/jour,
    28 septembre 2026 — voir assemble_home_page()), pas seulement pour les
    éditions précédentes — d'où ces paramètres plutôt que du texte en dur.
    cross_link_html="" pour "Aussi aujourd'hui" : pas de page dédiée aux
    éditions du jour, contrairement à archives.html pour l'historique."""
    if not articles:
        return ""
    items = "\n".join(
        f'''      <li><a href="archives/{a.get("edition_id", a["date_str"])}.html" class="related-articles-item">
        <img class="related-articles-image" src="{a["image_url"]}" alt="{a["title"]}">
        <div class="related-articles-content">
          <span class="related-articles-date">{(display_domain(a["domain"]) + " · ") if a.get("domain") else ""}{_format_date_short(a["date_str"], lang)}</span>
          <span class="related-articles-title">{fr_typo(a["title"], lang)}</span>
        </div>
      </a></li>'''
        for a in articles
    )
    return f'''<section class="related-articles" id="{section_id}">
  <div class="wrap">
    <p class="section-label">{section_label}</p>
    <h2 class="section-title">{section_title}</h2>
    <ul class="related-articles-list">
{items}
    </ul>
    {cross_link_html}
  </div>
</section>'''


def fr_typo(text, lang="fr"):
    """Typographie française pour un titre affiché : espace insécable avant
    « ? ! : ; » et à l'intérieur des guillemets « », pour qu'un signe de
    ponctuation ne passe jamais seul à la ligne sur mobile (retour utilisateur
    du 1er octobre 2026 : « Bitcoin : le sacre institutionnel / ? »). Texte
    affiché seulement (jamais un attribut alt/title ni un champ structuré), et
    jamais en anglais, où la ponctuation se colle au mot."""
    if lang != "fr" or not text:
        return text
    text = re.sub(r"(?<=\S) (?=[?!:;»])", "&nbsp;", text)
    return re.sub(r"(?<=«) ", "&nbsp;", text)


# Libellé AFFICHÉ (badge des cartes, ligne de date, lien « Voir tous les
# sujets ») pour les domaines dont le texte brut d'article:section est
# disgracieux : sans accent, sur deux mots, donc coupé en fin de ligne sur
# mobile (retour utilisateur du 1er octobre 2026 : « Economie Mondiale »).
# Affichage seulement : DOMAIN_THEME_SLUGS et la traduction EN restent
# clés sur la valeur brute, jamais sur ce libellé.
DOMAIN_DISPLAY = {
    "Economie Mondiale": "Économie",
}


def display_domain(domain):
    return DOMAIN_DISPLAY.get(domain, domain)


# Correspondance domaine (article:section, texte libre — voir
# extract_article_domain()) -> slug de themes/{slug}.html. Best-effort,
# volontairement incomplète : "Sport" (valeur réellement observée dans
# les archives le 28 septembre 2026) n'a AUCUNE page thème correspondante
# parmi les 6 officielles (docs/tags.md) — build_featured_article() omet
# alors simplement le lien plutôt que d'en fabriquer un cassé. Signalé à
# l'utilisateur : incohérence de fond entre le domaine réellement produit
# par le brief et la taxonomie à 6 thèmes, pas une évidence technique à
# corriger ici en silence.
DOMAIN_THEME_SLUGS = {
    "Culture": "culture-divertissement",
    "Economie Mondiale": "economie-entreprises",
    "International": "international",
    "Politique Institutions": "politique-institutions",
    "Sciences": "sciences-environnement",
    "Tech Numerique": "tech-numerique",
    "Sport": "sport",
}

# Même 6 pages thèmes que DOMAIN_THEME_SLUGS ci-dessus, mais keyée sur le
# slug BRUT du domaine (brief["sujet"]["domain"], ex.
# "economie-entreprises") plutôt que sur un libellé Title Case observé
# dans un <meta> déjà rendu — utilisée par assemble_index_html() (page
# article elle-même), qui a accès au brief d'origine, contrairement à
# build_featured_article()/DOMAIN_THEME_SLUGS (page home, qui ne voit
# qu'une archive déjà écrite). Même table que DOMAIN_LABELS dans
# generate_post_edition.py/generate_seo_head.py (à tenir manuellement
# synchronisée, même convention documentée là-bas) : les 6 slugs
# officiels de docs/tags.md avec leur libellé humain. Un domaine produit
# hors de ces 6 (dérive constatée, ex. "sport") ne matche simplement pas
# ici — lien omis, jamais cassé, même logique que DOMAIN_THEME_SLUGS.
THEME_SLUG_LABELS = {
    "economie-entreprises": "Économie & entreprises",
    "politique-institutions": "Politique & institutions",
    "international": "International",
    "sciences-environnement": "Sciences & environnement",
    "tech-numerique": "Tech & numérique",
    "culture-divertissement": "Culture & divertissement",
    "sport": "Sport",
}


def build_featured_article(article, lang="fr", theme_link_base=None):
    """Met en avant la toute dernière édition (grande image + titre) juste
    sous le hero de présentation, séparément des 4 éditions suivantes
    (build_home_cards) — demandé pour donner du poids visuel au contenu le
    plus récent sur une home devenue une page de présentation fixe.
    lang="en" : voir build_home_cards().

    theme_link_base (optionnel, ex. "themes/") : si fourni ET que le
    domaine de l'article a une correspondance dans DOMAIN_THEME_SLUGS,
    ajoute un lien "Voir tous les sujets {domaine} →" sous la carte
    (jamais DANS .featured-article-link : un <a> ne peut pas en contenir
    un autre, ce lien est donc un élément frère, hors du lien principal).
    None côté EN (aucune page themes/*.html en anglais pour l'instant,
    27 septembre 2026 — voir le chantier correspondant)."""
    domain_link_html = ""
    if theme_link_base and article.get("domain"):
        slug = DOMAIN_THEME_SLUGS.get(article["domain"])
        if slug:
            domain_link_html = f'\n    <a class="cross-link" href="{theme_link_base}{slug}.html">Voir tous les sujets «&nbsp;{display_domain(article["domain"])}&nbsp;»&nbsp;→</a>'
    question_html = (
        f'\n        <p class="featured-article-question">{article["question"]}</p>'
        if article.get("question") else ""
    )
    return f'''<section class="featured-article">
  <div class="wrap">
    <p class="section-label">La dernière édition</p>
    <a href="archives/{article.get("edition_id", article["date_str"])}.html" class="featured-article-link">
      <div class="featured-article-image-wrap">
        <img class="featured-article-image" src="{article["image_url"]}" alt="{article["title"]}">
      </div>
      <div>
        <span class="featured-article-date">{(display_domain(article["domain"]) + " · ") if article.get("domain") else ""}{_format_date_short(article["date_str"], lang)}</span>
        <h2 class="featured-article-title">{fr_typo(article["title"], lang)}</h2>{question_html}
        <span class="featured-article-cta">Lire l'édition →</span>
      </div>
    </a>{domain_link_html}
  </div>
</section>'''


MATIERE_ICONS = {
    "economie-entreprises": '<path d="M4 19V5"/><path d="M4 19h16"/><path d="m7 15 4-4 3 3 5-6"/>',
    "politique-institutions": '<path d="M3 9 12 4l9 5"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20h18"/>',
    "international": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.5 2.5 3.5 5.5 3.5 8.5s-1 6-3.5 8.5c-2.5-2.5-3.5-5.5-3.5-8.5s1-6 3.5-8.5Z"/>',
    "sciences-environnement": '<path d="M9 3h6"/><path d="M10 3v6L5 18a1.5 1.5 0 0 0 1.3 2.2h11.4A1.5 1.5 0 0 0 19 18l-5-9V3"/><path d="M7.5 14h9"/>',
    "tech-numerique": '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    "culture-divertissement": '<rect x="3.5" y="5" width="17" height="14" rx="2"/><path d="m10 9.5 5 2.5-5 2.5Z"/>',
    "sport": '<path d="M8 4h8v5a4 4 0 0 1-8 0Z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4"/><path d="M12 13v4M8.5 20h7M10 17h4"/>',
}


MATIERE_SHORT = {"economie-entreprises": "Économie", "politique-institutions": "Politique", "international": "International", "sciences-environnement": "Sciences", "tech-numerique": "Tech", "culture-divertissement": "Culture", "sport": "Sport"}


def build_matieres_section():
    """Rangée de pastilles « Par matière » sous le hero de l'accueil : seul
    chemin visible vers themes/*.html (avant, elles n'étaient reliées que
    depuis les archives). FR uniquement : pas de pages thèmes en anglais.
    L'ancre #matieres est aussi la cible du lien « Matières » du menu."""
    icons = MATIERE_ICONS
    chips = "\n".join(
        f'      <li><a class="matiere-tile" href="themes/{slug}.html" title="{label.replace("&", "&amp;")}"><svg viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'{icons[slug]}</svg>{MATIERE_SHORT[slug]}</a></li>'
        for slug, label in THEME_SLUG_LABELS.items()
    )
    return f"""

<section class="matieres" id="matieres" aria-label="Parcourir par matière">
  <div class="wrap">
    <p class="section-label">Par matière</p>
    <ul class="matiere-tiles">
{chips}
    </ul>
  </div>
</section>"""


def build_home_hero():
    """Hero fixe de la page d'accueil — ne dépend d'aucune édition, ne
    change jamais d'un jour à l'autre. Texte repris de le-projet.html pour
    rester cohérent avec le ton déjà établi ailleurs sur le site. Logo à
    côté du titre (.hero-brand, CSS dans le style_block du gabarit) : le
    texte seul en h1 n'engageait pas assez la marque sur la première chose
    vue en arrivant sur le site. Classe .hero--home (CSS dans le style_block
    du gabarit) : padding-top propre à ce hero sans image de fond, jamais
    appliqué au hero d'article (voir la règle CSS pour le motif)."""
    return """<section class="hero hero--home" id="contexte">
  <div class="wrap">
    <p class="eyebrow">Chaque jour, un sujet, trois scénarios</p>
    <h1>Comprendre l'actualité, c'est en mesurer les <span>conséquences</span></h1>
    <p class="dek">Chaque jour, Scénario prend un sujet clé et en détaille trois évolutions possibles, chacune avec une probabilité chiffrée.</p>
    <ul class="hero-scenarios" aria-label="Les trois scénarios de chaque édition">
      <li class="is-favorable">Favorable</li>
      <li class="is-stable">Stable</li>
      <li class="is-degrade">Dégradé</li>
    </ul>
    <a class="hero-cta" href="le-projet.html">Découvrir le projet <span aria-hidden="true">→</span></a>
  </div>
</section>""" + build_matieres_section()


def build_home_head(date_str, edition_number):
    """Head SEO de la page d'accueil — fixe et générique (site web de
    présentation), jamais celui d'un article : og:type=website (pas
    "article"), canonical vers la racine elle-même (jamais une archive,
    précisément pour éviter le conflit de canonical corrigé le 27 septembre
    2026 — voir build_home_cards() et le commit associé), JSON-LD
    WebSite + Organization seulement (pas de NewsArticle : cette page ne
    porte plus le contenu d'un article, BreadcrumbList non plus, une home
    n'a pas de fil d'ariane)."""
    title = "Scénario — chaque jour, les trois scénarios de demain"
    description = "Chaque jour, un sujet d'actualité clé et ses trois scénarios chiffrés : favorable, stable, dégradé."
    return f"""<title>{title}</title>
<link rel="canonical" href="https://lesscenarios.fr/">
<meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="language" content="fr-FR">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Scénario">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="https://lesscenarios.fr/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://lesscenarios.fr/assets/social/og-image-v2.png">
<meta property="og:image:width" content="2508">
<meta property="og:image:height" content="1412">
<meta property="og:image:alt" content="Scénario — trois scénarios chiffrés pour chaque actualité : favorable, stable, dégradé.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@scenario_fr">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://lesscenarios.fr/assets/social/og-image-v2.png">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Scénario",
  "url": "https://lesscenarios.fr",
  "logo": "https://lesscenarios.fr/assets/logo-512.png",
  "description": "Chaque jour, les trois scénarios de demain : un à court terme, un à moyen terme, un à long terme.",
  "sameAs": [
    "https://www.linkedin.com/company/136694258/",
    "https://www.facebook.com/share/1LuiQ1cAmt/"
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Scénario",
  "url": "https://lesscenarios.fr",
  "description": "Les trois scénarios du jour : court, moyen et long terme."
}}
</script>"""


def assemble_home_page(shell, date_str, edition_number, repo_root, today_entry=None,
                        lang="fr", head_builder=None, hero_html=None,
                        archives_dir="archives", image_path_prefix="",
                        domain_translator=None, theme_link_base=None):
    """Assemble la page d'accueil FIXE : head/hero génériques (jamais liés à
    une édition précise), la dernière édition mise en avant (grande carte),
    les 6 éditions suivantes en cartes plus petites (grille à 3 colonnes,
    donc deux lignes complètes), bloc "reste connecté", footer. Remplace
    l'ancien comportement (copie intégrale de l'article du
    jour) — voir le commit du 27 septembre 2026 : Google indexait la home à
    la place de l'archive faute d'une vraie séparation de contenu ; une home
    qui ne republie plus jamais un contenu d'article élimine ce conflit à la
    racine plutôt que de le réduire.

    today_entry (optionnel) : {"date_str", "title", "image_url"} pour
    l'édition du jour même. Son archive n'existe pas encore sur le disque
    scanné par get_latest_archives() à ce stade du pipeline (elle est
    encore dans le bac à sable, pas promue vers repo_root) — sans cet
    argument, seules les éditions déjà publiées apparaissent.

    Paramètres pour la variante EN (voir scripts/en/translate_daily.py
    build_en_index_page()) : lang="en", head_builder=build_home_head_en,
    hero_html=build_home_hero_en(), archives_dir="en/archives",
    image_path_prefix="../" — jamais un nouvel appel LLM, seulement des
    traductions déjà faites (en/archives/*.html) et du texte fixe.

    domain_translator (optionnel) : voir build_archive_entry() — propagé
    à get_latest_archives() pour traduire le badge domaine des cartes
    (article:section n'est jamais retraduit dans en/archives/*.html).

    theme_link_base (optionnel, ex. "themes/") : propagé à
    build_featured_article() — voir DOMAIN_THEME_SLUGS et son docstring.
    None côté EN (pas de pages themes/*.html en anglais).

    Depuis le 28 septembre 2026 (multi-éditions/jour, décision
    utilisateur) : la home distingue maintenant 3 groupes — l'édition mise
    en avant (featured, toujours l'édition IA du jour si elle existe),
    "Aussi aujourd'hui" (les AUTRES éditions du même jour, ex. contributions
    de journalistes indépendants — affiché seulement s'il y en a), puis
    "Dernières éditions" (les jours précédents, inchangé). Voir
    get_today_editions() pour la distinction avec get_latest_archives()
    (strictement avant date_str).

    _INTRO_BANNER_HTML volontairement absent du HTML produit ici
    (contrairement à la page article, voir plus bas dans ce fichier) :
    son texte ("Chaque jour, un sujet qui compte, décortiqué en trois
    scénarios chiffrés...") fait doublon avec le hero fixe juste en
    dessous depuis la home redesign — retour utilisateur du 28 septembre
    2026. Le bandeau reste affiché tel quel sur les pages article/archive,
    où rien d'autre n'introduit le principe du site à un visiteur qui
    atterrit directement dessus."""
    head_dynamic = (head_builder or build_home_head)(date_str, edition_number)
    masthead = build_masthead(shell["masthead_html"], date_str, edition_number)
    hero = hero_html if hero_html is not None else build_home_hero()

    # Éditions déjà écrites sur le disque pour CE jour précisément (jamais
    # avant) — distinct de `previous` plus bas (strictement avant date_str).
    today_on_disk = get_today_editions(repo_root, date_str, archives_dir=archives_dir,
                                        image_path_prefix=image_path_prefix,
                                        domain_translator=domain_translator)
    # today_entry (l'édition en cours, pas encore promue vers repo_root à ce
    # stade du pipeline — voir son docstring) remplace toute entrée de même
    # edition_id déjà trouvée sur disque (dédoublonnage), puis rejoint le
    # tas commun — jamais insérée directement en position 0 : today_entry
    # peut être l'édition IA (generate_post_edition.py, cas normal) OU une
    # édition à slug déclenchée à la main (--slug, chantier
    # multi-éditions/jour du 28 septembre 2026) construisant SA PROPRE
    # édition ce jour-là alors que l'édition IA du jour est déjà sur disque
    # — dans ce 2e cas, today_entry ne doit surtout PAS prendre la place de
    # mise en avant. Le tri qui suit tranche uniformément dans les deux cas.
    today_all = list(today_on_disk)
    if today_entry:
        today_all = [e for e in today_all if e.get("edition_id") != today_entry.get("edition_id", date_str)]
        today_all.append(today_entry)
    # Toujours l'édition IA (edition_id == date_str, SANS suffixe) en
    # position 0 si elle existe dans le tas (sur disque ou via today_entry),
    # peu importe l'ordre d'arrivée ou quel run a fourni today_entry —
    # jamais une édition à slug, même si c'est elle que CE run est en train
    # de construire. Repli (aucune édition edition_id == date_str du tout,
    # cas rare) : la 1re édition du jour trouvée, peu importe laquelle.
    # `other_today` : les éditions du jour restantes (contributions
    # journalistes etc.), affichées dans leur propre section.
    today_all.sort(key=lambda e: (e.get("edition_id", date_str) != date_str, e.get("edition_id", date_str)))
    featured_entry = today_all[0] if today_all else None
    other_today = today_all[1:]

    # 7 au total pour les précédentes : la plus récente en avant (featured)
    # + les 6 suivantes en cartes — jamais la même édition dans les deux
    # blocs. 6 plutôt que 4 : la grille de cartes est fixée à 3 colonnes
    # (voir le CSS .related-articles-list), donc 6 remplit deux lignes
    # complètes là où 4 laissait une ligne à moitié vide.
    previous = get_latest_archives(repo_root, before_date_str=date_str,
                                    count=6 if featured_entry else 7,
                                    archives_dir=archives_dir, image_path_prefix=image_path_prefix,
                                    domain_translator=domain_translator)
    if not featured_entry and previous:
        # Aucune édition pour date_str du tout (cas théorique seulement,
        # jamais rencontré tant que l'IA publie chaque jour) : repli sur la
        # plus récente des éditions précédentes, comme avant ce chantier.
        featured_entry, previous = previous[0], previous[1:]

    featured = build_featured_article(featured_entry, lang, theme_link_base=theme_link_base) if featured_entry else ""
    also_today = build_home_cards(
        other_today, lang, section_id="aussi-aujourdhui",
        section_label="Le même jour", section_title="Aussi aujourd'hui",
        cross_link_html="",
    ) if other_today else ""
    cards = build_home_cards(previous[:6], lang)

    footer_html = f'<footer>\n  <div class="wrap">\n    <div class="footer-bottom">\n      {shell["legal_links_html"]}\n    </div>\n  </div>\n</footer>'

    html_result = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{head_dynamic}
{shell['head_static']}
{shell['style_block']}
</head>
<body>

{masthead}

{shell['topnav_html']}

{shell['weekly_banner_html']}

{featured}

{hero}

{also_today}

{cards}

{_SHARE_BLOCK}

{footer_html}

{shell['scripts_tail_html']}
</body>
</html>
"""
    if "<style" not in html_result or "</style>" not in html_result:
        raise ShellError(
            "❌ CRITIQUE : le CSS n'a pas été injecté dans le HTML de la home ! "
            "La page serait entièrement noire. Abandon immédiat."
        )
    return html_result


def assemble_index_html(shell, content, brief, date_str, photo=None):
    """Assemble le document complet. Ne fait AUCUN appel réseau, AUCUNE
    écriture disque — retourne uniquement la chaîne HTML finale, à valider
    par le code appelant avant toute écriture.

    `photo` (optionnel, voir generate_post_edition.py) : dict
    {"og_image_url", "hero_image_url", "alt", "photographer", "pexels_url"}
    si une photo de sujet réelle a été retenue — sinon (défaut) comportement historique
    de la Phase 1 rédaction : image générique, aucun crédit photo."""
    canonical_url = f"https://lesscenarios.fr/archives/{date_str}.html"
    edition_number = shell["edition_number"] + 1
    content = dict(content)
    content["eyebrow_suffix"] = brief["sujet"]["eyebrow"].split(", ", 1)[-1] if ", " in brief["sujet"]["eyebrow"] else brief["registre"]

    head_dynamic = build_head_dynamic(content, brief, date_str, canonical_url, photo=photo)
    masthead = build_masthead(shell["masthead_html"], date_str, edition_number)
    # Pas de lien « Voir tous les sujets « Domaine » → » dans le hero de l'article : ajouté le 28 septembre 2026,
    # retiré le 4 octobre 2026 à la demande de l'éditeur (placé juste avant « Les faits », il n'avait pas de sens).
    # Le lien reste sous la carte mise en avant de la page d'accueil (build_featured_article).
    theme_link_html = ""
    hero = build_hero(content, date_str, photo=photo, graphique_dc_chart=brief.get("graphique_dc_chart"),
                       theme_link_html=theme_link_html, graphique_chiffres=brief.get("graphique_chiffres"),
                       rappels=_rappels_depuis_connexes(brief))
    related_articles = build_related_articles(brief)
    theme_more = build_theme_more(brief, date_str)
    scenarios = build_scenarios(content)
    lexique = build_lexique(content)
    sources = build_sources(content, date_str)

    # Crédit photo — uniquement si une photo réelle a été retenue (jamais
    # un crédit inventé sur l'image générique). Voir docs/routine-prompt.md,
    # étape technique « Image du sujet », `.footer-photo-credit`.
    photo_credit_html = ""
    if photo:
        photo_credit_html = (
            '\n    <p class="footer-photo-credit"><svg viewBox="0 0 24 24" width="14" height="14" '
            'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><path d="M4 8.5a1.5 1.5 0 0 1 1.5-1.5h2l1-1.5h7l1 '
            '1.5h2A1.5 1.5 0 0 1 20 8.5v9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 17.5Z"/>'
            '<circle cx="12" cy="12.5" r="3.2"/></svg> Photo d\'illustration. '
            f'{photo["photographer"]} / <a href="{photo["pexels_url"]}" target="_blank" '
            'rel="noopener noreferrer">Pexels ↗</a></p>'
        )

    footer_html = f'<footer>\n  <div class="wrap">{photo_credit_html}\n    <div class="footer-bottom">\n      {shell["legal_links_html"]}\n    </div>\n  </div>\n</footer>'

    html_result = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{head_dynamic}
{shell['head_static']}
{shell['style_block']}
</head>
<body>

{masthead}

{shell['topnav_html']}

{shell['weekly_banner_html']}

{_INTRO_BANNER_HTML}

{hero}

{related_articles}

{scenarios}

{lexique}

{sources}

{theme_more}

{_SHARE_BLOCK}

{footer_html}

{shell['scripts_tail_html']}
</body>
</html>
"""

    # GARDE-FOU : s'assurer que le CSS a bien été injecté dans le HTML généré
    # (incident du 26 septembre 2026). "<style" en préfixe, pas "<style>"
    # exact — ne doit jamais dépendre de l'absence d'attribut sur la balise.
    if "<style" not in html_result or "</style>" not in html_result:
        raise ShellError(
            "❌ CRITIQUE : le CSS n'a pas été injecté dans le HTML généré ! "
            "La page serait entièrement noire. Abandon immédiat."
        )

    return html_result, edition_number
