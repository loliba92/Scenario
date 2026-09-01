#!/usr/bin/env python3
"""Génère les pages thématiques statiques (`themes/{slug}.html`) à partir des
entrées d'`archives.html`, pour le maillage interne SEO.

Chaque page liste tous les articles qui portent au moins un tag thématique
d'un "domaine" (regroupement défini dans `docs/tags.md` §2, même table que
`themeDomains` dans le JS d'`archives.html` — gardée synchronisée à la main
avec DOMAINS ci-dessous).

Usage : python3 scripts/seo/generate_theme_pages.py
Idempotent — peut être relancé à chaque nouvelle édition pour que les pages
thématiques restent à jour (nouvel article taggé → réapparaît automatiquement
dans la bonne page au prochain run).
"""
import re
import html
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[2]
ARCHIVES_HTML = ROOT / "archives.html"
GLOSSAIRE_HTML = ROOT / "glossaire.html"
THEMES_DIR = ROOT / "themes"
SITE_URL = "https://lesscenarios.fr"
TODAY = date.today().isoformat()

# Même table que `themeDomains` dans archives.html (script inline, section
# "Domaines des tags thématiques") — à tenir manuellement synchronisée si
# cette table change là-bas. Domaines trop pauvres en articles (< 3) exclus
# volontairement pour éviter le "thin content" (voir docs/BACKLOG.md, audit
# SEO du 31 août).
DOMAINS = [
    {"slug": "economie-entreprises", "label": "Économie & entreprises",
     "tags": ["economie", "entreprises", "emploi"]},
    {"slug": "politique-institutions", "label": "Politique & institutions",
     "tags": ["politique", "justice"]},
    {"slug": "international", "label": "International",
     "tags": ["diplomatie", "defense", "immigration"]},
    {"slug": "sciences-environnement", "label": "Sciences & environnement",
     "tags": ["energie", "climat", "sante", "espace"]},
    {"slug": "tech-numerique", "label": "Tech & numérique",
     "tags": ["intelligence-artificielle", "numerique"]},
    {"slug": "culture-divertissement", "label": "Culture & divertissement",
     "tags": ["cinema", "musique", "jeux-video", "litterature", "medias"]},
]

# [CORRIGÉ le 1er septembre 2026] archives.html n'est plus une liste de
# <li class="entry"> avec des boutons .tag (ancien format, avant la
# restructuration en tableau de generate_archives_table.py) — c'est
# désormais un <table class="archives-table"> où chaque article est une
# seule <tr data-domain="{slug}" ...>, avec un domaine unique déjà résolu
# (plus de jeu de tags à recouper). Regex mises à jour en conséquence ;
# la notion de "registre" (jour/thème type "Lundi géopolitique") a
# disparu de ce tableau, elle n'est donc plus affichée sur ces pages.
ENTRY_RE = re.compile(r'<tr data-domain="([a-z-]*)"[^>]*>(.*?)</tr>', re.DOTALL)
TITLE_RE = re.compile(r'<a href="archives/(\d{4}-\d{2}-\d{2})\.html"[^>]*>([^<]+)</a>')


def parse_entries():
    text = ARCHIVES_HTML.read_text(encoding="utf-8")
    entries = []
    for domain_slug, block in ENTRY_RE.findall(text):
        title_m = TITLE_RE.search(block)
        if not domain_slug or not title_m:
            continue  # pas de domaine assigné, ou bloc non-article
        iso_date, title = title_m.groups()
        display_date = f"{iso_date[8:10]}.{iso_date[5:7]}.{iso_date[0:4]}"
        entries.append({
            "iso_date": iso_date,
            "display_date": display_date,
            "title": html.unescape(title),
            "href": f"archives/{iso_date}.html",
            "registre": None,
            "domain_slug": domain_slug,
        })
    return entries


def extract_block(text, start_marker, end_marker, include_end=True):
    start = text.index(start_marker)
    end = text.index(end_marker, start) + (len(end_marker) if include_end else 0)
    return text[start:end]


def build_shared_pieces():
    text = GLOSSAIRE_HTML.read_text(encoding="utf-8")
    style_block = extract_block(text, "<style>", "</style>")
    masthead_nav = extract_block(text, '<header class="masthead">', "</nav>")
    follow_footer = extract_block(text, '<section class="follow-block" id="nous-suivre">', "</footer>")
    tail_scripts = extract_block(
        text,
        '<script data-goatcounter="https://scenario.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>',
        "</html>",
    )
    return style_block, masthead_nav, follow_footer, tail_scripts


THEME_LIST_CSS = """
  /* ---- Liste d'articles par page de thème (scripts/seo/generate_theme_pages.py) ---- */
  .theme-list{ margin: 0; padding: 0; list-style: none; }
  .theme-entry{
    display: flex;
    align-items: baseline;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid var(--hairline);
  }
  .theme-entry:first-child{ padding-top: 0; }
  .theme-entry-date{
    font-family: "JetBrains Mono", monospace;
    font-size: 0.72rem;
    color: var(--paper-dim);
    white-space: nowrap;
    flex-shrink: 0;
  }
  .theme-entry-title{
    font-family: "Fraunces", serif;
    font-weight: 600;
    font-size: 1.02rem;
    color: var(--paper);
    text-decoration: none;
  }
  .theme-entry-title:hover{ text-decoration: underline; text-decoration-color: var(--gold); }
  .theme-registre{
    font-family: "JetBrains Mono", monospace;
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 100px;
    padding: 2px 9px;
    white-space: nowrap;
    border: 1px solid var(--gold);
    color: var(--gold);
    flex-shrink: 0;
  }
"""


def render_page(domain, entries, style_block, masthead_nav, follow_footer, tail_scripts):
    count = len(entries)
    title = f"{domain['label']} — Scénario"
    description = (
        f"Toutes les éditions de Scénario sur le thème {domain['label'].lower()} : "
        f"{count} articles, chacun avec 3 scénarios chiffrés (favorable, stable, dégradé)."
    )
    url = f"{SITE_URL}/themes/{domain['slug']}.html"

    items_html = "\n".join(
        f'''      <li class="theme-entry">
        <span class="theme-entry-date">{e["display_date"]}</span>
        <a class="theme-entry-title" href="../{e["href"]}">{html.escape(e["title"])}</a>
        {f'<span class="theme-registre">{html.escape(e["registre"])}</span>' if e["registre"] else ""}
      </li>'''
        for e in entries
    )

    json_ld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": {html.escape(title)!r},
  "description": {html.escape(description)!r},
  "url": {url!r},
  "isPartOf": {{ "@type": "WebSite", "name": "Scénario", "url": "{SITE_URL}/" }}
}}
</script>'''.replace("'", '"')

    # THEME_LIST_CSS doit vivre À L'INTÉRIEUR de la balise <style> copiée de
    # glossaire.html, jamais après — sinon le HTML5 parser sort ce texte du
    # <head> (mode "in head", anything else) et l'affiche comme texte brut en
    # haut du <body> (bug constaté le 31 août sur les 6 pages générées).
    style_block = style_block.replace("</style>", THEME_LIST_CSS + "</style>")

    head = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="../assets/logo.svg">
<link rel="manifest" href="../manifest.webmanifest">
<meta name="theme-color" content="#10151c">
<link rel="apple-touch-icon" href="../assets/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Scénario">
<link rel="stylesheet" href="../assets/pwa-install.css">
<meta name="description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Scénario">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE_URL}/assets/social/og-image-v2.png">
<meta property="og:image:width" content="2508">
<meta property="og:image:height" content="1412">
<meta property="og:image:alt" content="Scénario — trois scénarios chiffrés pour chaque actualité : favorable, stable, dégradé.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/assets/social/og-image-v2.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
{style_block}
{json_ld}
</head>
"""

    # Les liens du masthead/nav pointent vers la racine (index.html, archives.html…)
    # depuis glossaire.html (profondeur 0) ; themes/ est un cran plus profond, donc
    # préfixer chaque lien relatif de "../" comme le fait déjà archives/{date}.html.
    masthead_nav_rel = re.sub(
        r'href="(index\.html|archives\.html|glossaire\.html|le-projet\.html|newsletter\.html|contact\.html)',
        r'href="../\1',
        masthead_nav,
    )
    masthead_nav_rel = masthead_nav_rel.replace('src="assets/logo.svg"', 'src="../assets/logo.svg"')
    # La page thème courante n'est pas dans le nav (voir docs/strategie-anglais.md
    # précédent pour guide-pedagogique.html) : retire l'aria-current="page" hérité
    # du lien Glossaire.
    masthead_nav_rel = masthead_nav_rel.replace(' aria-current="page"', "")

    follow_footer_rel = re.sub(
        r'href="(mentions-legales\.html|politique-de-confidentialite\.html)"',
        r'href="../\1"',
        follow_footer,
    )

    tail_scripts_rel = tail_scripts.replace(
        'src="assets/pwa-install.js"', 'src="../assets/pwa-install.js"'
    ).replace(
        'serviceWorkerPath: "OneSignalSDKWorker.js"', 'serviceWorkerPath: "../OneSignalSDKWorker.js"'
    )

    body = f"""<body>

{masthead_nav_rel}

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Thème</p>
    <h1>{domain['label']}</h1>
    <p class="dek">{count} édition{"s" if count != 1 else ""} de Scénario sur ce thème, classées de la plus récente à la plus ancienne — chacune avec 3 scénarios chiffrés.</p>
  </div>
</section>

<section class="listing">
  <div class="wrap">
    <ul class="theme-list">
{items_html}
    </ul>
    <p style="margin-top:28px"><a class="theme-entry-title" href="../archives.html" style="font-size:0.85rem">← Retour à toutes les archives</a></p>
  </div>
</section>

{follow_footer_rel}

{tail_scripts_rel}
"""
    return head + body


def main():
    entries = parse_entries()
    style_block, masthead_nav, follow_footer, tail_scripts = build_shared_pieces()
    THEMES_DIR.mkdir(exist_ok=True)

    summary = []
    for domain in DOMAINS:
        matched = [e for e in entries if e["domain_slug"] == domain["slug"]]
        matched.sort(key=lambda e: e["iso_date"], reverse=True)
        page = render_page(domain, matched, style_block, masthead_nav, follow_footer, tail_scripts)
        out_path = THEMES_DIR / f"{domain['slug']}.html"
        out_path.write_text(page, encoding="utf-8")
        summary.append((domain["slug"], domain["label"], len(matched)))
        print(f"→ themes/{domain['slug']}.html : {len(matched)} articles")

    return summary


if __name__ == "__main__":
    main()
