#!/usr/bin/env python3
"""Génère sources.html — la revue de presse — à partir de sources-log.json.

Une seule page qui grandit (comme feed.xml), jamais un fichier par jour :
sources-log.json est une liste de jours, chacun avec ses articles croisés
pendant la recherche éditoriale (docs/routine-prompt.md, étape 3) — jamais
liés au sujet du jour lui-même, jamais d'avis dessus, juste ce que dit
l'article. Chaque jour devient une <section id="{date}"> sur cette page
unique, ce qui permet un lien direct depuis une édition
(sources.html#2026-09-04) sans jamais créer de fichier séparé.

Économie de tokens : cette étape est entièrement déterministe (lecture du
JSON + petit script), aucun jugement éditorial requis — la routine n'a
jamais à relire toute la page, seulement à ajouter un jour au JSON et
relancer ce script. Même logique que generate_archives_table.py.

Idempotent — peut être relancé après chaque ajout au JSON.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES_LOG = ROOT / "sources-log.json"
GLOSSAIRE_HTML = ROOT / "glossaire.html"
SOURCES_HTML = ROOT / "sources.html"
SITE_URL = "https://lesscenarios.fr"

# Même liste fermée que docs/tags.md — dupliquée ici plutôt qu'importée
# (chaque script scripts/seo/*.py reste autonome, même convention que
# generate_archives_table.py).
DOMAIN_LABELS = {
    "economie-entreprises": "Économie & entreprises",
    "politique-institutions": "Politique & institutions",
    "international": "International",
    "sciences-environnement": "Sciences & environnement",
    "tech-numerique": "Tech & numérique",
    "culture-divertissement": "Culture & divertissement",
}

LANG_LABELS = {"fr": "Français", "en": "English", "other": "Autres"}

FRENCH_MONTHS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]
FRENCH_DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def format_date_long(iso_date):
    """AAAA-MM-JJ -> "vendredi 4 septembre 2026"."""
    from datetime import date
    y, m, d = (int(p) for p in iso_date.split("-"))
    dt = date(y, m, d)
    return f"{FRENCH_DAYS[dt.weekday()]} {d} {FRENCH_MONTHS[m - 1]} {y}"


def format_date_short(iso_date):
    """AAAA-MM-JJ -> "04.09.2026" (même format que .lang-link/dates archives)."""
    y, m, d = iso_date.split("-")
    return f"{d}.{m}.{y}"


# ---------------------------------------------------------------------------
# CSS propre à cette page — palette/typo identiques au reste du site (voir
# --ink/--gold/etc déjà posés dans le style_block partagé, extrait plus bas
# de glossaire.html), rien de nouveau inventé ici.
# ---------------------------------------------------------------------------
SOURCES_PAGE_CSS = """
  /* ---- Revue de presse (scripts/seo/generate_sources_page.py) ---- */
  .sources-toolbar{ display:flex; flex-direction:column; gap:14px; margin: 0 0 28px; }
  .sources-search{
    width:100%; max-width:480px; background: var(--surface-2); border:1px solid var(--hairline);
    color: var(--paper); border-radius:6px; padding:10px 14px; font-size:0.92rem; font-family: inherit;
  }
  .sources-search:focus{ outline: 2px solid var(--gold); border-color: var(--gold); }
  .sources-filter-row{ display:flex; flex-wrap:wrap; align-items:center; gap:8px; }
  .sources-filter-label{
    font-family:"JetBrains Mono",monospace; font-size:0.68rem; text-transform:uppercase;
    letter-spacing:0.06em; color: var(--paper-dim); margin-right:2px;
  }
  .sources-day{ margin: 0 0 8px; }
  .sources-day-label{
    display:block; font-family:"JetBrains Mono",monospace; font-size:0.8rem; text-transform:uppercase;
    letter-spacing:0.08em; color: var(--paper-dim); padding: 22px 4px 4px; scroll-margin-top: 90px;
  }
  .sources-row{
    display:flex; gap:20px; padding:18px 4px; border-bottom:1px solid var(--hairline);
  }
  .sources-row.is-hidden{ display:none; }
  .sources-photo{
    background-color: var(--surface-2);
    background-image: repeating-linear-gradient(135deg, rgba(207,157,76,0.05) 0px, rgba(207,157,76,0.05) 1px, transparent 1px, transparent 14px);
    border-radius:6px; flex: 0 0 140px; width:140px; height:104px;
  }
  .sources-content{ display:flex; flex-direction:column; gap:6px; flex:1; min-width:0; }
  .sources-domain{
    font-family:"JetBrains Mono",monospace; font-size:0.68rem; text-transform:uppercase;
    letter-spacing:0.06em; color: var(--gold);
  }
  .sources-title{ font-size:1.02rem; font-weight:600; color: var(--paper); line-height:1.35; margin:0; }
  .sources-title a{ color: inherit; text-decoration:none; }
  .sources-title a:hover{ text-decoration:underline; }
  .sources-meta{ font-family:"JetBrains Mono",monospace; font-size:0.74rem; color: var(--paper-dim); }
  .sources-summary{ margin:2px 0 4px; color: var(--paper-dim); font-size:0.9rem; }
  .sources-readlink{ font-family:"JetBrains Mono",monospace; font-size:0.8rem; color: var(--gold); text-decoration:none; }
  .sources-readlink:hover{ text-decoration:underline; }
  .sources-empty{ color: var(--paper-dim); font-size:0.95rem; padding: 24px 4px; }
  .sources-empty.is-hidden{ display:none; }
  .sources-next{ text-align:center; padding-top:24px; }
  .sources-next span{ font-family:"JetBrains Mono",monospace; font-size:0.78rem; color: var(--paper-dim); }
  @media (max-width: 560px){
    .sources-row{ flex-direction:column; }
    .sources-photo{ width:100%; height:160px; }
  }
"""


def render_row(day_date, article):
    domain = article.get("domain", "")
    domain_label = DOMAIN_LABELS.get(domain, domain)
    lang = article.get("lang", "other")
    lang_label = {"fr": "FR", "en": "EN", "other": "—"}.get(lang, "—")
    title = html.escape(article["title"])
    source = html.escape(article["source"])
    url = html.escape(article["url"])
    summary = html.escape(article.get("summary", ""))
    read_minutes = article.get("read_minutes")
    read_str = f" · {read_minutes} min" if read_minutes else ""
    search_blob = html.escape(f"{article['title']} {article['source']} {article.get('summary', '')}".lower())

    return f"""      <div class="sources-row" data-domain="{domain}" data-lang="{lang}" data-search="{search_blob}">
        <div class="sources-photo" aria-hidden="true"></div>
        <div class="sources-content">
          <span class="sources-domain">{domain_label}</span>
          <p class="sources-title"><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></p>
          <span class="sources-meta">{source} · {format_date_short(day_date)}{read_str} · <span title="{LANG_LABELS.get(lang, 'Autre langue')}">{lang_label}</span></span>
          <p class="sources-summary">{summary}</p>
          <a href="{url}" target="_blank" rel="noopener noreferrer" class="sources-readlink">Lire l'article ↗</a>
        </div>
      </div>"""


def render_day(day):
    rows = "\n".join(render_row(day["date"], a) for a in day.get("articles", []))
    return f"""    <div class="sources-day" id="{day['date']}">
      <span class="sources-day-label">{format_date_long(day['date'])}</span>
{rows}
    </div>"""


def chip_group(field, label, values_present, value_labels, ordered_values):
    if not values_present:
        return ""
    chips = ['<button type="button" class="filter-chip is-active" data-filter="all">Tous</button>']
    for v in ordered_values:
        if v in values_present:
            chips.append(f'<button type="button" class="filter-chip" data-filter="{v}">{value_labels[v]}</button>')
    return f"""      <div class="sources-filter-row">
        <span class="sources-filter-label">{label}</span>
        <div class="domain-filters" id="{field}-filters" data-field="{field}">
{"".join(chips)}
        </div>
      </div>"""


FILTER_SCRIPT = """<script>
  (function(){
    var rows = Array.prototype.slice.call(document.querySelectorAll('.sources-row'));
    var days = Array.prototype.slice.call(document.querySelectorAll('.sources-day'));
    var noResult = document.getElementById('sources-no-result');
    var searchInput = document.getElementById('sources-search');
    var active = { domain: 'all', lang: 'all', q: '' };

    ['domain-filters', 'lang-filters'].forEach(function(groupId){
      var box = document.getElementById(groupId);
      if(!box){ return; }
      var field = box.dataset.field;
      box.querySelectorAll('.filter-chip').forEach(function(chip){
        chip.addEventListener('click', function(){
          active[field] = chip.dataset.filter;
          box.querySelectorAll('.filter-chip').forEach(function(c){
            c.classList.toggle('is-active', c === chip);
          });
          apply();
        });
      });
    });

    if(searchInput){
      searchInput.addEventListener('input', function(){
        active.q = searchInput.value.trim().toLowerCase();
        apply();
      });
    }

    function apply(){
      var visible = 0;
      rows.forEach(function(row){
        var show = (active.domain === 'all' || row.dataset.domain === active.domain)
          && (active.lang === 'all' || row.dataset.lang === active.lang)
          && (active.q === '' || row.dataset.search.indexOf(active.q) !== -1);
        row.classList.toggle('is-hidden', !show);
        if(show){ visible++; }
      });
      // Un jour sans aucune ligne visible (filtré à vide) disparaît lui aussi,
      // sinon l'en-tête de date resterait affiché au-dessus de rien.
      days.forEach(function(day){
        var anyVisible = Array.prototype.slice.call(day.querySelectorAll('.sources-row'))
          .some(function(r){ return !r.classList.contains('is-hidden'); });
        day.classList.toggle('is-hidden', !anyVisible);
      });
      if(noResult){ noResult.classList.toggle('is-hidden', visible !== 0); }
    }

    apply();
  })();
</script>"""


def extract_block(text, start_marker, end_marker, include_end=True):
    start = text.index(start_marker)
    end = text.index(end_marker, start) + (len(end_marker) if include_end else 0)
    return text[start:end]


def build_shared_pieces():
    """Extrait les blocs réutilisables de glossaire.html — même source que
    generate_archives_table.py, pour que les deux pages restent en phase."""
    text = GLOSSAIRE_HTML.read_text(encoding="utf-8")
    style_block = extract_block(text, "<style>", "</style>")
    masthead_nav = extract_block(text, '<header class="masthead">', "</nav>")
    masthead_nav = masthead_nav.replace('<a href="glossaire.html" aria-current="page">', '<a href="glossaire.html">')
    follow_footer = extract_block(text, '<section class="follow-block" id="nous-suivre">', "</footer>")
    tail_scripts = extract_block(
        text,
        '<script data-goatcounter="https://scenario.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>',
        "</html>",
    )
    return style_block, masthead_nav, follow_footer, tail_scripts


def render_page(days, style_block, masthead_nav, follow_footer, tail_scripts):
    title = "Revue de presse — Scénario"
    description = "Les articles croisés pendant la recherche éditoriale de Scénario, jour après jour — factuel, sans avis, en plus des sources déjà citées dans chaque édition."
    url = f"{SITE_URL}/sources.html"

    all_articles = [a for day in days for a in day.get("articles", [])]
    domains_present = {a.get("domain") for a in all_articles if a.get("domain")}
    langs_present = {a.get("lang") for a in all_articles if a.get("lang")}

    filters_html = ""
    if all_articles:
        filters_html = f"""    <div class="sources-toolbar">
      <input type="text" id="sources-search" class="sources-search" placeholder="Rechercher un article, une source, un mot-clé…">
{chip_group("domain", "Domaine", domains_present, DOMAIN_LABELS, list(DOMAIN_LABELS.keys()))}
{chip_group("lang", "Langue", langs_present, LANG_LABELS, ["fr", "en", "other"])}
    </div>"""

    days_sorted = sorted(days, key=lambda d: d["date"], reverse=True)
    days_html = "\n".join(render_day(d) for d in days_sorted)

    empty_state = (
        '<p class="sources-empty">Rien pour l\'instant — la revue de presse s\'enrichit d\'un jour à l\'autre, revenez bientôt.</p>'
        if not all_articles else
        '<p class="sources-empty is-hidden" id="sources-no-result">Aucun article ne correspond à ces filtres.</p>'
    )

    style_block = style_block.replace("</style>", SOURCES_PAGE_CSS + "</style>")

    head = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="assets/logo.svg">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#10151c">
<link rel="apple-touch-icon" href="assets/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Scénario">
<link rel="stylesheet" href="assets/pwa-install.css">
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
</head>
"""

    body = f"""<body>

{masthead_nav}

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Revue de presse</p>
    <h1>Ce qu'on a lu</h1>
    <p class="dek">Les articles croisés pendant la recherche du jour, en plus des sources déjà citées dans l'édition — jamais un avis dessus, juste ce que les autres racontent.</p>
  </div>
</section>

<section class="listing">
  <div class="wrap">
{filters_html}
{empty_state if not all_articles else ""}
{days_html}
{empty_state if all_articles else ""}
    <div class="sources-next"><span>Prochaine revue de presse demain, 7h</span></div>
    <p style="margin-top:28px"><a href="index.html" style="color:var(--gold);text-decoration:none">← Retour à l'accueil</a></p>
  </div>
</section>

{follow_footer}

{FILTER_SCRIPT}

{tail_scripts}
"""
    return head + body


def main():
    data = json.loads(SOURCES_LOG.read_text(encoding="utf-8"))
    days = data.get("days", [])
    total_articles = sum(len(d.get("articles", [])) for d in days)
    print(f"Lu {len(days)} jour(s), {total_articles} article(s) au total.")

    style_block, masthead_nav, follow_footer, tail_scripts = build_shared_pieces()
    page = render_page(days, style_block, masthead_nav, follow_footer, tail_scripts)

    SOURCES_HTML.write_text(page, encoding="utf-8")
    print(f"✓ Generated {SOURCES_HTML.name}")


if __name__ == "__main__":
    main()
