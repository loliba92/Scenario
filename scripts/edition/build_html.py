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
JOURS_FR = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


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
_PER_DAY_HEAD_PREDICATES = [
    lambda t: t.name == "title",
    lambda t: t.name == "link" and t.get("rel") == ["canonical"],
    lambda t: t.name == "link" and t.get("rel") == ["alternate"],
    lambda t: t.name == "meta" and t.get("name") == "description",
    lambda t: t.name == "meta" and t.get("name") == "domain",
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
    intro_banner = soup.select_one("#intro-banner")
    footer = soup.select_one("footer")
    for name, tag in [
        ("header.masthead", masthead), ("nav.topnav", topnav),
        ("#weekly-banner", weekly_banner), ("#intro-banner", intro_banner),
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

    return {
        "head_static": "\n".join(head_static_tags),
        "style_block": str(style_tag),
        "masthead_html": str(masthead),
        "topnav_html": str(topnav),
        "weekly_banner_html": str(weekly_banner),
        "intro_banner_html": str(intro_banner),
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
    ld_json = (
        "{\n"
        '  "@context": "https://schema.org",\n'
        '  "@type": "NewsArticle",\n'
        '  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://lesscenarios.fr/" },\n'
        f'  "headline": {content["h1"]!r},\n'
        f'  "description": {description!r},\n'
        f'  "image": ["{og_image}"],\n'
        f'  "datePublished": "{published}",\n'
        f'  "dateModified": "{published}",\n'
        '  "inLanguage": "fr-FR",\n'
        '  "author": { "@type": "Organization", "name": "Scénario", "url": "https://lesscenarios.fr/le-projet.html", "sameAs": ["https://www.linkedin.com/company/136694258/"] },\n'
        '  "publisher": {\n'
        '    "@type": "Organization",\n'
        '    "name": "Scénario",\n'
        '    "logo": { "@type": "ImageObject", "url": "https://lesscenarios.fr/assets/logo-512.png", "width": 512, "height": 512 }\n'
        "  }\n"
        "}"
    ).replace("'", "&#39;")
    return f"""<title>{title}</title>
<link rel="canonical" href="{canonical_url}">
<link rel="alternate" hreflang="fr" href="{canonical_url}">
<link rel="alternate" hreflang="x-default" href="{canonical_url}">
<meta name="description" content="{description}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Scénario">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="https://lesscenarios.fr/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="{og_image_width}">
<meta property="og:image:height" content="{og_image_height}">
<meta property="og:image:alt" content="{og_image_alt}">
<meta property="article:author" content="Scénario">
<meta name="domain" content="{domain}">
<meta property="article:published_time" content="{published}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">
{ld_json}
</script>"""


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
    path = f"M {x_pos(points[0]['annee'])} {y_pos(points[0]['valeur'])}"
    for i in range(1, len(points)):
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


def build_hero(content, date_str, photo=None, graphique_dc_chart=None):
    jour, date_longue = format_date_fr(date_str)
    dek_blocks = []
    for i, dek_html in enumerate(content["dek"]):
        dek_blocks.append(f'<p class="dek">{_unwrap_own_tag(dek_html, "p", "dek")}</p>')
        for box in content.get("comprendre_box") or []:
            if box.get("apres_dek_index") == i:
                dek_blocks.append(_comprendre_box_html(box))
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
        <h1>{content['h1']}</h1>
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
    </p>

    <nav class="toc" aria-label="Sommaire de l'édition">
      <a href="#scenarios">Scénarios</a>
      <a href="#essentiel">L'essentiel</a>
      <a href="#lexique">Référence</a>
    </nav>

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
    </div>
    <div class="share-row" style="margin-top:14px">
      <button type="button" id="onesignal-subscribe-btn" class="onesignal-subscribe-btn btn-outline"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 10.5a6 6 0 0 1 12 0c0 3.2 1 4.7 1.5 5.3H4.5C5 15.2 6 13.7 6 10.5Z"/><path d="M10.3 18.5a1.8 1.8 0 0 0 3.4 0"/></svg> <span class="btn-label">Activer les notifications</span></button>
      <a class="btn-outline" href="https://buymeacoffee.com/scenario" target="_blank" rel="noopener noreferrer">☕ Nous offrir un café</a>
    </div>
  </div>
</section>"""


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
            month_name = MOIS_FR[month - 1][:4]  # "sept.", "juil.", etc.
            if month_name.endswith("e"):
                formatted_date = f"{day} {month_name.rstrip('e')}."
            else:
                formatted_date = f"{day} {month_name}."
        except Exception:
            formatted_date = article_date

        article_html = f'''      <li><a href="archives/{article_date}.html" class="related-articles-item">
        <img class="related-articles-image" src="assets/social/topic-images/{article_date}.jpg" alt="{title}">
        <div class="related-articles-content">
          <span class="related-articles-date">{formatted_date}</span>
          <span class="related-articles-title">{title}</span>
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
    hero = build_hero(content, date_str, photo=photo, graphique_dc_chart=brief.get("graphique_dc_chart"))
    related_articles = build_related_articles(brief)
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

    return f"""<!DOCTYPE html>
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

{shell['intro_banner_html']}

{hero}

{related_articles}

{scenarios}

{lexique}

{sources}

{_SHARE_BLOCK}

{footer_html}

{shell['scripts_tail_html']}
</body>
</html>
""", edition_number
