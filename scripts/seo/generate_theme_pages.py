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
    # Ajouté le 4 octobre 2026 : les éditions du dimanche ont le domaine « sport »
    # (3 articles à l'ajout, seuil anti thin-content atteint).
    {"slug": "sport", "label": "Sport", "tags": ["sport"]},
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
# Groupe 1 élargi le 28 septembre 2026 (chantier multi-éditions/jour) pour
# capturer "{date}-{slug}.html" en plus de "{date}.html" nu : sans le
# suffixe optionnel, une édition supplémentaire publiée le même jour que
# l'édition IA (voir build_html._ARCHIVE_DATE_RE, même convention) ne
# matchait jamais cette regex — l'entrée entière disparaissait
# silencieusement des pages themes/*.html (title_m à None -> skip plus
# bas), pas d'erreur, juste une édition jamais listée. La variable
# `iso_date` ci-dessous reste utilisable telle quelle même avec un suffixe
# : display_date la découpe par position fixe (les 10 premiers
# caractères sont toujours AAAA-MM-JJ), et href en a besoin en entier
# pour pointer vers le bon fichier.
TITLE_RE = re.compile(r'<a href="archives/(\d{4}-\d{2}-\d{2}(?:-[a-z0-9-]+)?)\.html"([^>]*)>([^<]+)</a>')
QUESTION_RE = re.compile(r'title="([^"]*)"')
KIND_RE = re.compile(r'<span class="eval-badge[^"]*" data-kind="([a-z]+)"')
LABEL_RE = re.compile(r'<span class="eval-label">([^<]+)</span>')
FRANCE_RE = re.compile(r'<span class="france-scale" title="([^"]*)"')


def parse_entries():
    text = ARCHIVES_HTML.read_text(encoding="utf-8")
    entries = []
    for domain_slug, block in ENTRY_RE.findall(text):
        title_m = TITLE_RE.search(block)
        if not domain_slug or not title_m:
            continue  # pas de domaine assigné, ou bloc non-article
        iso_date, attrs, title = title_m.groups()
        question = QUESTION_RE.search(attrs)
        kind = KIND_RE.search(block)
        label = LABEL_RE.search(block)
        france = FRANCE_RE.search(block)
        display_date = f"{iso_date[8:10]}.{iso_date[5:7]}.{iso_date[0:4]}"
        entries.append({
            "iso_date": iso_date,
            "display_date": display_date,
            "title": html.unescape(title),
            "href": f"archives/{iso_date}.html",
            "registre": None,
            "question": html.unescape(question.group(1)) if question else "",
            "kind": kind.group(1) if kind else "",
            "label": html.unescape(label.group(1)) if label else "",
            "france": html.unescape(france.group(1)) if france else "",
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
    # Le <footer> de glossaire.html porte une légende propre à cette page
    # ("Ce glossaire est alimenté au fil des éditions...") — ne jamais la
    # reprendre telle quelle sur une page qui réutilise ce bloc partagé
    # (même bug que generate_archives_table.py, corrigé le 5 septembre 2026
    # là-bas mais jamais porté ici : cette légende fuyait sur les 6 pages
    # themes/*.html, trouvé en code review le 26 septembre 2026).
    follow_footer = re.sub(r'\s*<p class="caveat">.*?</p>\n?', '\n', follow_footer, count=1, flags=re.S)
    tail_scripts = extract_block(
        text,
        '<script data-goatcounter="https://scenario.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>',
        "</html>",
    )
    return style_block, masthead_nav, follow_footer, tail_scripts


THEME_LIST_CSS = """
  /* ---- Pages de thème : sélecteur, édition à la une, cartes (scripts/seo/generate_theme_pages.py) ---- */
  .theme-chips{ display:flex; flex-wrap:wrap; gap:8px; margin: 22px 0 0; padding:0; list-style:none; }
  .theme-chip{
    font-family:"JetBrains Mono", monospace; font-size:0.72rem; letter-spacing:0.03em;
    padding:7px 13px; border-radius:100px; border:1px solid var(--hairline);
    color:var(--paper-dim); text-decoration:none; white-space:nowrap;
  }
  .theme-chip:hover{ border-color:var(--gold); color:var(--paper); }
  .theme-chip[aria-current="page"]{ background:var(--gold); border-color:var(--gold); color:var(--ink); font-weight:700; }
  .theme-chip .n{ opacity:0.6; margin-left:4px; }

  .theme-featured{
    display:block; text-decoration:none; color:inherit;
    background:var(--surface); border:1px solid var(--hairline); border-left:3px solid var(--gold);
    border-radius:10px; padding:22px 24px; margin-bottom:34px;
    transition:border-color .15s, transform .15s;
  }
  .theme-featured:hover{ border-color:var(--gold); transform:translateY(-1px); }
  .theme-featured .kicker{ font-family:"JetBrains Mono", monospace; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; color:var(--gold); }
  .theme-featured h2{ font-family:"Fraunces", serif; font-weight:600; font-size:1.45rem; line-height:1.25; margin:8px 0 10px; color:var(--paper); }
  .theme-featured .q{ color:var(--paper-dim); font-size:0.95rem; line-height:1.55; margin:0 0 14px; }
  .theme-featured .go{ font-size:0.85rem; color:var(--gold); }

  .theme-grid{ display:grid; grid-template-columns:repeat(auto-fill, minmax(290px, 1fr)); gap:14px; margin:0; padding:0; list-style:none; }
  .theme-card{
    display:flex; gap:14px; align-items:flex-start; text-decoration:none; color:inherit;
    background:var(--surface); border:1px solid var(--hairline); border-radius:10px; padding:12px;
    height:100%; transition:border-color .15s, transform .15s;
  }
  .theme-card:hover{ border-color:var(--gold); transform:translateY(-1px); }
  .theme-thumb{ width:72px; height:72px; border-radius:7px; background:var(--surface-2); object-fit:cover; flex-shrink:0; }
  .theme-card-body{ min-width:0; }
  .theme-card-date{ font-family:"JetBrains Mono", monospace; font-size:0.68rem; color:var(--paper-dim); }
  .theme-card-title{ font-family:"Fraunces", serif; font-weight:600; font-size:1rem; line-height:1.3; color:var(--paper); margin:3px 0 8px; }
  .theme-card:hover .theme-card-title{ text-decoration:underline; text-decoration-color:var(--gold); }
  .theme-tags{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }
  .theme-badge{
    font-family:"JetBrains Mono", monospace; font-size:0.64rem; text-transform:uppercase; letter-spacing:0.05em;
    padding:2px 8px; border-radius:100px; border:1px solid var(--hairline); color:var(--paper-dim);
  }
  .theme-badge::before{ content:""; display:inline-block; width:6px; height:6px; border-radius:50%; margin-right:6px; background:currentColor; vertical-align:middle; }
  .theme-badge.favorable{ color:var(--favorable); border-color:var(--favorable); }
  .theme-badge.stable{ color:var(--stable); border-color:var(--stable); }
  .theme-badge.degrade{ color:var(--degrade); border-color:var(--degrade); }
  .theme-france{ font-size:0.72rem; color:var(--paper-dim); }
  .theme-section-title{ font-family:"JetBrains Mono", monospace; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; color:var(--paper-dim); margin:0 0 14px; }
  @media (max-width: 480px){
    .theme-featured{ padding:18px; }
    .theme-featured h2{ font-size:1.2rem; }
    .theme-chips{ flex-wrap:nowrap; overflow-x:auto; margin-right:-20px; padding-right:20px; scrollbar-width:none; }
    .theme-chips::-webkit-scrollbar{ display:none; }
  }
"""


def render_page(domain, entries, style_block, masthead_nav, follow_footer, tail_scripts, counts=None):
    count = len(entries)
    counts = counts or {}
    title = f"{domain['label']} — Scénario"
    description = (
        f"Toutes les éditions de Scénario sur le thème {domain['label'].lower()} : "
        f"{count} articles, chacun avec 3 scénarios chiffrés (favorable, stable, dégradé)."
    )
    url = f"{SITE_URL}/themes/{domain['slug']}.html"

    def chip(d):
        current = ' aria-current="page"' if d["slug"] == domain["slug"] else ""
        return (f'      <li><a class="theme-chip" href="{d["slug"]}.html"{current}>'
                f'{html.escape(d["label"])}<span class="n">{counts.get(d["slug"], 0)}</span></a></li>')

    chips_html = "\n".join(chip(d) for d in DOMAINS)

    def thumb(e):
        # Les miniatures vivent dans assets/social/archive-thumbs ; le script
        # tourne parfois dans un miroir sans images, donc on ne teste pas leur
        # présence : onerror masque l'<img> (en gardant sa place) si le fichier manque.
        return (f'<img class="theme-thumb" src="../assets/social/archive-thumbs/{e["iso_date"][:10]}.jpg" '
                f'alt="" width="72" height="72" loading="lazy" onerror="this.style.visibility=\x27hidden\x27">')

    def badges(e):
        out = []
        if e["kind"] in ("favorable", "stable", "degrade") and e["label"]:
            out.append(f'<span class="theme-badge {e["kind"]}" title="Notre scénario">{html.escape(e["label"])}</span>')
        if e["france"]:
            out.append(f'<span class="theme-france">France : {html.escape(e["france"].lower())}</span>')
        return "".join(out)

    featured_html = ""
    rest = entries
    if entries:
        f = entries[0]
        rest = entries[1:]
        # Certaines éditions reprennent la question telle quelle en titre : inutile de la répéter.
        redite = f["question"].strip(" ?").lower() == f["title"].strip(" ?").lower()
        q = f'\n    <p class="q">{html.escape(f["question"])}</p>' if f["question"] and not redite else ""
        featured_html = f'''    <a class="theme-featured" href="../{f["href"]}">
    <span class="kicker">Dernière édition · {f["display_date"]}</span>
    <h2>{html.escape(f["title"])}</h2>{q}
    <div class="theme-tags">{badges(f)}</div>
    <span class="go">Lire l'édition →</span>
    </a>'''

    items_html = "\n".join(
        f'''      <li><a class="theme-card" href="../{e["href"]}">
        {thumb(e)}
        <div class="theme-card-body">
          <div class="theme-card-date">{e["display_date"]}</div>
          <div class="theme-card-title">{html.escape(e["title"])}</div>
          <div class="theme-tags">{badges(e)}</div>
        </div>
      </a></li>'''
        for e in rest
    )
    earlier_html = (
        f'''    <h2 class="theme-section-title">Les éditions précédentes</h2>
    <ul class="theme-grid">
{items_html}
    </ul>''' if rest else ""
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
        'src="assets/bottom-nav.js"', 'src="../assets/bottom-nav.js"'
    ).replace(
        'src="assets/google-source-banner.js"', 'src="../assets/google-source-banner.js"'
    ).replace(
        'serviceWorkerPath: "OneSignalSDKWorker.js"', 'serviceWorkerPath: "../OneSignalSDKWorker.js"'
    )

    body = f"""<body>

{masthead_nav_rel}

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Thème</p>
    <h1>{domain['label']}</h1>
    <p class="dek">{count} édition{"s" if count != 1 else ""} sur ce thème, chacune avec trois scénarios chiffrés.</p>
    <ul class="theme-chips" aria-label="Changer de thème">
{chips_html}
    </ul>
  </div>
</section>

<section class="listing">
  <div class="wrap">
{featured_html}
{earlier_html}
    <p style="margin-top:28px"><a class="theme-chip" href="../archives.html">← Toutes les archives</a></p>
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

    counts = {d["slug"]: sum(1 for e in entries if e["domain_slug"] == d["slug"]) for d in DOMAINS}
    summary = []
    for domain in DOMAINS:
        matched = [e for e in entries if e["domain_slug"] == domain["slug"]]
        matched.sort(key=lambda e: e["iso_date"], reverse=True)
        page = render_page(domain, matched, style_block, masthead_nav, follow_footer, tail_scripts, counts)
        out_path = THEMES_DIR / f"{domain['slug']}.html"
        out_path.write_text(page, encoding="utf-8")
        summary.append((domain["slug"], domain["label"], len(matched)))
        print(f"→ themes/{domain['slug']}.html : {len(matched)} articles")

    return summary


if __name__ == "__main__":
    main()
