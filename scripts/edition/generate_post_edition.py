#!/usr/bin/env python3
"""
Post-édition (Phase 1 prototype) : à partir du contenu déjà rédigé et
validé par generate_daily_edition.py (fichier `{date}.content.json`),
produit tout ce qui manquait encore pour une vraie publication — voir
docs/BACKLOG.md § « Chaîne rédaction OpenRouter » :
  1. photo de sujet (Pexels) — sélection AUTOMATIQUE du 1er candidat,
     sans revue humaine (décision assumée le 14 septembre 2026, voir
     docs/routine-brief-format.md § image_keywords — changement de
     comportement volontaire par rapport à fetch_topic_image.py, qui
     documente une sélection humaine par défaut) ;
  2. HTML final réassemblé avec cette photo (build_html.assemble_index_html,
     paramètre `photo`) ;
  3. image Instagram (scripts/social/generate_instagram_image.py) ;
  4. feed.xml (nouvel <item>) ;
  4bis. glossaire.html : report mécanique des nouveaux termes du lexique
     du jour (voir docs/routine-prompt.md, étape 6ter) — un terme déjà
     présent n'est jamais modifié, un nouveau terme est inséré à la
     bonne place alphabétique ;
  5. sitemap.xml (nouvelle entrée archive, <lastmod> de glossaire.html
     mis à jour seulement si 4bis a ajouté un terme) et sitemap-news.xml
     (purge >48h) ;
  6. archives.html (scripts/seo/generate_archives_table.py, réutilisé tel
     quel — nécessite que l'archive du jour existe réellement sur disque,
     voir --sandbox-root) ;
  7. themes/{slug}.html, les 6 pages thématiques SEO (scripts/seo/
     generate_theme_pages.py, réutilisé tel quel — lit archives.html
     tout juste régénéré à l'étape 6, même bac à sable).

Photo — deux niveaux de repli si Pexels échoue ou si image_keywords est
absent : 1) photo par défaut du registre (assets/social/pub-photos/
{registre}.jpg, recadrage LOCAL via Pillow, jamais un appel réseau) ;
2) seulement si ce repli échoue aussi (registre inconnu, fichier
manquant) : image générique unique du gabarit (comportement historique
de build_html.py, photo=None). Jamais bloquant à aucun des deux niveaux.

Limites Phase 1, assumées (voir docs/BACKLOG.md) :
  - `<comments>`/le 1er bloc de la Description reprennent question_text
    seul, sans « accroche » distincte (jamais définie précisément dans
    le brief actuel) ;
  - pas de en/feed.xml ni sitemap EN (traduction gérée séparément par
    translate-en.yml, hors périmètre ici).

Par défaut (`--publish` absent) : AUCUN commit, AUCUN push — tout
s'écrit sous --sandbox-root, jamais dans les vrais fichiers du dépôt.

`--publish` (Phase 2, ajouté le 14 septembre 2026, activé sur décision
explicite de l'utilisateur — voir docs/BACKLOG.md) : une fois tout
généré et validé dans le bac à sable EXACTEMENT comme en Phase 1
(aucun changement de logique de génération), promote_to_real_repo()
copie les fichiers finaux vers leurs vrais emplacements (index.html,
archives/{date}.html, feed.xml, sitemap.xml, sitemap-news.xml,
glossaire.html, archives.html, themes/*.html, assets/social/...) — le
commit + push reste effectué par le workflow appelant
(.github/workflows/post-edition.yml), jamais par ce script lui-même.
Garde-fou repris de docs/routine-prompt.md (« vérifier qu'une autre
exécution n'a pas déjà publié l'édition du jour ») : si le vrai
index.html porte déjà la date du brief, --publish s'arrête proprement
sans rien écrire de plus, jamais une double publication.

Usage:
    export PEXELS_API_KEY=sk-...
    python3 generate_post_edition.py \\
        --brief ../../editorial-briefs/2026-09-14.json \\
        --content ../../_prototype-out/2026-09-14.content.json \\
        --sandbox-root ../../_prototype-out/post-edition

    # Sans clé Pexels/sans réseau, pour tester la mécanique (feed/sitemap/
    # archives) sans dépendre d'un appel externe :
    python3 generate_post_edition.py --brief ... --content ... --skip-photo
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape as escape_xml

import build_html
from generate_daily_edition import estimate_word_count, load_brief

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOCIAL_DIR = REPO_ROOT / "scripts" / "social"
SEO_DIR = REPO_ROOT / "scripts" / "seo"
SITE_URL = "https://lesscenarios.fr"
CARD_ORDER = ("favorable", "stable", "degrade")
# Même table que docs/tags.md §2 / DOMAIN_LABELS de generate_archives_table.py
# et generate_theme_pages.py — dupliquée ici volontairement (même
# convention que ces deux scripts : « à tenir manuellement synchronisée »,
# pas d'import croisé entre scripts/seo et scripts/edition).
DOMAIN_LABELS = {
    "economie-entreprises": "Économie & entreprises",
    "politique-institutions": "Politique & institutions",
    "international": "International",
    "sciences-environnement": "Sciences & environnement",
    "tech-numerique": "Tech & numérique",
    "culture-divertissement": "Culture & divertissement",
}
CARD_EMOJI = {"favorable": "🟢", "stable": "🔵", "degrade": "🔴"}
# Approximation Europe/Paris (CEST, UTC+2) — même limite que le reste du
# prototype (pas de dépendance à une base tz système), acceptable pour un
# <pubDate>/<news:publication_date> de test, jamais utilisé tel quel en
# production réelle sans vérifier le décalage hiver/été.
PARIS_TZ = timezone(timedelta(hours=2))


class PostEditionError(Exception):
    pass


# ---------------------------------------------------------------------------
# 1. Photo de sujet (Pexels) — sélection automatique
# ---------------------------------------------------------------------------
def select_topic_photo(image_keywords, date_str, sandbox_root, timeout=25):
    """Retourne un dict de crédits pour le 1er candidat Pexels retenu, ou
    None si aucune photo n'a pu être obtenue — jamais bloquant : l'appelant
    retombe alors sur l'image générique existante (photo=None,
    build_html.py, comportement historique de la Phase 1 rédaction)."""
    if not image_keywords:
        print("[post-edition] image_keywords absent du brief — pas de recherche de photo", file=sys.stderr)
        return None

    candidates_dir = sandbox_root / "topic-image-candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    fetch_script = SOCIAL_DIR / "fetch_topic_image.py"

    try:
        subprocess.run(
            [sys.executable, str(fetch_script), image_keywords, "--count", "5", "--out", str(candidates_dir)],
            check=True, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.CalledProcessError as e:
        print(f"[post-edition] fetch_topic_image.py a échoué (code {e.returncode}) : "
              f"{(e.stderr or '')[-500:]}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"[post-edition] fetch_topic_image.py : délai dépassé ({timeout}s)", file=sys.stderr)
        return None

    credits_path = candidates_dir / "credits.json"
    if not credits_path.exists():
        print("[post-edition] aucun credits.json produit — aucun candidat", file=sys.stderr)
        return None
    with open(credits_path, encoding="utf-8") as f:
        credits = json.load(f)
    if not credits:
        print("[post-edition] credits.json vide — aucun candidat exploitable", file=sys.stderr)
        return None

    # Sélection automatique du 1er candidat — voir docstring module.
    chosen = credits[0]
    candidate_path = chosen.get("file")
    if not candidate_path or not os.path.isfile(candidate_path):
        print(f"[post-edition] candidat retenu introuvable sur disque : {candidate_path!r}", file=sys.stderr)
        return None

    use_script = SOCIAL_DIR / "use_topic_image.py"
    try:
        subprocess.run(
            [sys.executable, str(use_script), candidate_path, "--date", date_str,
             "--credits", str(credits_path), "--repo-root", str(sandbox_root)],
            check=True, capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"[post-edition] use_topic_image.py a échoué : {e}", file=sys.stderr)
        return None

    square_path = sandbox_root / "assets" / "social" / "topic-images" / f"{date_str}.jpg"
    if not square_path.exists():
        print(f"[post-edition] image carrée attendue introuvable : {square_path}", file=sys.stderr)
        return None
    # Le recadrage large (-wide.jpg) n'est pas toujours produit par
    # use_topic_image.py (nécessite original_url dans credits.json, voir
    # sa docstring) — jamais bloquant, main() retombe alors sur le carré
    # pour l'image visible en tête d'article.
    wide_path = sandbox_root / "assets" / "social" / "topic-images" / f"{date_str}-wide.jpg"

    return {
        "square_path": square_path,
        "wide_path": wide_path if wide_path.exists() else None,
        "photographer": chosen.get("photographer") or "Photographe non identifié",
        "pexels_url": chosen.get("pexels_url") or "https://www.pexels.com/",
        "query": image_keywords,
    }


def select_registry_fallback_photo(registre, date_str, sandbox_root):
    """Repli sur la photo par défaut du registre (assets/social/pub-
    photos/{registre}.jpg + credits.json) quand Pexels échoue ou ne
    retient rien — jamais l'image générique unique du gabarit tant
    qu'un repli par registre existe (voir docs/routine-prompt.md, étape
    « Image du sujet », point 4 : « ne pas publier sans image »).
    Recadrage LOCAL (Pillow, réutilise square_crop_local/wide_crop_local
    de fetch_topic_image.py/use_topic_image.py) — aucun appel réseau."""
    pub_photos_dir = REPO_ROOT / "assets" / "social" / "pub-photos"
    credits_path = pub_photos_dir / "credits.json"
    if not credits_path.exists():
        return None
    with open(credits_path, encoding="utf-8") as f:
        all_credits = json.load(f)
    entry = next((c for c in all_credits if c.get("file") == f"{registre}.jpg"), None)
    if not entry:
        print(f"[post-edition] aucune photo de repli connue pour le registre {registre!r}", file=sys.stderr)
        return None
    src_path = pub_photos_dir / f"{registre}.jpg"
    if not src_path.exists():
        print(f"[post-edition] photo de repli introuvable sur disque : {src_path}", file=sys.stderr)
        return None

    sys.path.insert(0, str(SOCIAL_DIR))
    from fetch_topic_image import square_crop_local  # noqa: PLC0415 — import tardif volontaire, voir docstrings des scripts sources
    from use_topic_image import wide_crop_local  # noqa: PLC0415

    topic_images_dir = sandbox_root / "assets" / "social" / "topic-images"
    topic_images_dir.mkdir(parents=True, exist_ok=True)
    square_path = topic_images_dir / f"{date_str}.jpg"
    try:
        square_crop_local(str(src_path), str(square_path))
        wide_crop_local(str(src_path), str(topic_images_dir / f"{date_str}-wide.jpg"))
    except Exception as e:
        print(f"[post-edition] recadrage de la photo de repli échoué : {e}", file=sys.stderr)
        return None

    credit_entry = dict(entry)
    credit_entry["note"] = "banque de secours par registre, pas une photo dédiée au sujet du jour"
    (topic_images_dir / f"{date_str}.json").write_text(
        json.dumps(credit_entry, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return {
        "square_path": square_path,
        "wide_path": topic_images_dir / f"{date_str}-wide.jpg",
        "photographer": entry.get("photographer") or "Photographe non identifié",
        "pexels_url": entry.get("pexels_url") or entry.get("source_url") or "https://www.pexels.com/",
        "query": f"repli registre {registre}",
    }


# ---------------------------------------------------------------------------
# 2. Image Instagram
# ---------------------------------------------------------------------------
def generate_instagram_image(content, date_str, sandbox_root, photo):
    """Reconstruit /tmp/ig-data.json à la volée et appelle
    generate_instagram_image.py. Structure simplifiée le 14 septembre
    2026 (retour utilisateur, image réelle relue) : titre + question
    posée, plus de bloc listant les 3 scénarios — leurs libellés (repris
    tels quels des titres de cartes du site, simplification Phase 1
    assumée) étaient systématiquement tronqués par le CSS une seule
    ligne du template (`text-overflow: ellipsis`), illisible. Voir
    scripts/social/generate_instagram_image.py pour le détail du
    changement de gabarit."""
    ig_data = {
        "title": content["h1"],
        "context": content["question_text"],
    }
    data_path = sandbox_root / "ig-data.json"
    data_path.write_text(json.dumps(ig_data, ensure_ascii=False, indent=2), encoding="utf-8")

    out_dir = sandbox_root / "assets" / "social" / "instagram"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{date_str}.png"

    cmd = [
        sys.executable, str(SOCIAL_DIR / "generate_instagram_image.py"),
        "--data", str(data_path), "--output", str(output_path),
    ]
    if photo:
        cmd += ["--template", str(SOCIAL_DIR / "instagram-photo-template.html"),
                "--photo", str(photo["square_path"])]
    else:
        cmd += ["--template", str(SOCIAL_DIR / "instagram-template.html")]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise PostEditionError(f"generate_instagram_image.py a échoué : {result.stderr[-1000:]}")
    if not output_path.exists():
        raise PostEditionError(f"generate_instagram_image.py n'a produit aucun fichier : {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# 3. feed.xml
# ---------------------------------------------------------------------------
def build_feed_item(content, date_str, read_minutes, ig_image_url, ig_image_size):
    h1 = content["h1"]
    link = f"{SITE_URL}/archives/{date_str}.html"
    guid = f"scenario-{date_str}"
    pub_date = datetime.now(PARIS_TZ).strftime("%a, %d %b %Y %H:%M:%S %z")
    question = content["question_text"]
    if len(content.get("essentiel_box") or []) < 2:
        raise PostEditionError("essentiel_box : moins de 2 paragraphes, impossible d'extraire le Contexte")
    contexte = content["essentiel_box"][1]
    card_titles = {k: content["cards"][k]["h3"] for k in CARD_ORDER}

    category = ",".join(f'"{CARD_EMOJI[k]} {card_titles[k]}"' for k in CARD_ORDER)
    scenarios_lines = "<br>".join(f"{CARD_EMOJI[k]} {card_titles[k]}" for k in CARD_ORDER)

    description = (
        f'<img src="{ig_image_url}" alt="{escape_xml(h1)}" style="max-width:100%;width:100%;height:auto;"><br><br>'
        f"La question posée : {question}<br><br>"
        f"Les faits : {contexte}<br><br>"
        f"Les 3 scénarios :<br>{scenarios_lines}<br><br>"
        f'Lequel est le plus probable ? 👉 <a href="{link}">Lire les 3 prévisions chiffrées sur le site</a> '
        f"— c'est gratuit (~{read_minutes} min de lecture).<br><br>"
        'Envie de voter avant de connaître les vraies probabilités ? Rejoins le canal Telegram : '
        '<a href="https://t.me/scenario_fr">t.me/scenario_fr</a><br><br>'
        "Une question, une remarque ? Réponds directement à cet email, on te lit."
    )

    enclosure = f'\n  <enclosure url="{ig_image_url}" length="{ig_image_size}" type="image/png"/>' if ig_image_url else ""

    return (
        "    <item>\n"
        f"      <title>{escape_xml(h1)}</title>\n"
        f"      <link>{link}</link>\n"
        f'      <guid isPermaLink="false">{guid}</guid>\n'
        f"      <pubDate>{pub_date}</pubDate>\n"
        f"      <comments>{escape_xml(question)}</comments>\n"
        f"      <category>{category}</category>"
        f"{enclosure}\n"
        f"      <description><![CDATA[{description}]]></description>\n"
        "    </item>"
    )


def update_feed_xml(feed_text, item_xml):
    # Bug réel du 14 septembre 2026, premier vrai run --publish : l'ancien
    # marker "<channel>" insérait le nouvel item JUSTE APRÈS <channel>,
    # repoussant les métadonnées de la chaîne (title/link/description/
    # language) APRÈS ce nouvel item — donc entre le nouvel item et l'ancien
    # premier item, plutôt qu'avant les deux comme dans un flux RSS normal.
    # Flux toujours valide en pratique (Make/la plupart des lecteurs RSS
    # trouvent les balises par nom, pas par position), mais structure
    # trompeuse à la lecture et non conforme à l'ordre conventionnel.
    # Corrigé : insérer juste avant le premier <item> existant, jamais
    # juste après <channel> — les métadonnées de chaîne restent toujours
    # en tête, avant tout item.
    marker = "\n    <item>"
    idx = feed_text.index(marker)
    insert_at = idx + 1  # juste après le \n, avant l'indentation du <item>
    return feed_text[:insert_at] + item_xml + "\n" + feed_text[insert_at:]


# ---------------------------------------------------------------------------
# 4. sitemap.xml / sitemap-news.xml
# ---------------------------------------------------------------------------
def update_sitemap_xml(sitemap_text, date_str, bump_glossaire=False):
    def bump_lastmod(text, loc):
        pattern = re.compile(
            rf'(<loc>{re.escape(loc)}</loc>\s*<lastmod>)\d{{4}}-\d{{2}}-\d{{2}}(</lastmod>)'
        )
        new_text, n = pattern.subn(rf"\g<1>{date_str}\g<2>", text, count=1)
        if n != 1:
            raise PostEditionError(f"sitemap.xml : <lastmod> introuvable/ambigu pour {loc} ({n} correspondance(s))")
        return new_text

    text = bump_lastmod(sitemap_text, f"{SITE_URL}/")
    text = bump_lastmod(text, f"{SITE_URL}/archives.html")
    # Uniquement si 6ter (voir update_glossaire_html()) a réellement
    # ajouté un terme — voir docs/routine-prompt.md, étape 7.
    if bump_glossaire:
        text = bump_lastmod(text, f"{SITE_URL}/glossaire.html")

    new_entry = (
        "  <url>\n"
        f"    <loc>{SITE_URL}/archives/{date_str}.html</loc>\n"
        f"    <lastmod>{date_str}</lastmod>\n"
        "    <changefreq>never</changefreq>\n"
        "    <priority>0.6</priority>\n"
        "  </url>\n"
    )
    marker = f"<loc>{SITE_URL}/archives.html</loc>"
    idx = text.index(marker)
    insert_at = text.index("</url>", idx) + len("</url>\n")
    return text[:insert_at] + new_entry + text[insert_at:]


def update_sitemap_news_xml(sitemap_news_text, date_str, title):
    """Ajoute l'entrée du jour et purge tout ce qui a plus de 48h — la
    purge est la règle ici, contrairement à sitemap.xml (voir
    docs/routine-prompt.md, étape technique 7bis)."""
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
          "news": "http://www.google.com/schemas/sitemap-news/0.9"}
    ET.register_namespace("", ns["sm"])
    ET.register_namespace("news", ns["news"])
    root = ET.fromstring(sitemap_news_text)

    now = datetime.now(PARIS_TZ)
    cutoff = now - timedelta(hours=48)
    for url_el in list(root.findall("sm:url", ns)):
        pub_el = url_el.find("news:news/news:publication_date", ns)
        if pub_el is None or pub_el.text is None:
            continue
        try:
            pub_dt = datetime.fromisoformat(pub_el.text)
        except ValueError:
            continue
        if pub_dt < cutoff:
            root.remove(url_el)

    new_url = ET.SubElement(root, f"{{{ns['sm']}}}url")
    ET.SubElement(new_url, f"{{{ns['sm']}}}loc").text = f"{SITE_URL}/archives/{date_str}.html"
    news_el = ET.SubElement(new_url, f"{{{ns['news']}}}news")
    pub_el = ET.SubElement(news_el, f"{{{ns['news']}}}publication")
    ET.SubElement(pub_el, f"{{{ns['news']}}}name").text = "Scénario"
    ET.SubElement(pub_el, f"{{{ns['news']}}}language").text = "fr"
    ET.SubElement(news_el, f"{{{ns['news']}}}publication_date").text = now.isoformat(timespec="seconds")
    ET.SubElement(news_el, f"{{{ns['news']}}}title").text = title

    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode")


# ---------------------------------------------------------------------------
# 5bis. glossaire.html — retour utilisateur du 14 septembre 2026 : la
# Phase 1 ne le mettait pas à jour, le glossaire restait figé au fil des
# éditions de test. Voir docs/routine-prompt.md, étape 6ter (« purement
# mécanique »).
# ---------------------------------------------------------------------------
_GLOSSAIRE_ENTRY_RE = re.compile(
    r'<div class="lex-entry" id="(lex-[a-z0-9-]+)">\s*'
    r'<dt class="lex-term">(.*?)</dt>\s*'
    r'<dd class="lex-def">.*?</dd>\s*'
    r'<div class="lex-meta">.*?</div>\s*'
    r'</div>',
    re.S,
)


def _normalize_for_sort(text):
    """Tri alphabétique insensible accents/majuscules, voir
    docs/routine-prompt.md étape 6ter."""
    stripped_tags = re.sub(r"<[^>]+>", "", text)
    normalized = unicodedata.normalize("NFKD", stripped_tags)
    return "".join(c for c in normalized if not unicodedata.combining(c)).lower().strip()


def _build_glossaire_entry(term, domain_label, date_str, h1):
    return (
        f'      <div class="lex-entry" id="lex-{term["slug"]}">\n'
        f'        <dt class="lex-term">{html.escape(term["terme"])}</dt>\n'
        f'        <dd class="lex-def">{html.escape(term["definition"])}</dd>\n'
        '        <div class="lex-meta">\n'
        f'          <span class="lex-domain">{html.escape(domain_label)}</span>\n'
        f'          <a class="lex-source" href="archives/{date_str}.html">Vu dans : {html.escape(h1)} →</a>\n'
        "        </div>\n"
        "      </div>\n"
    )


def update_glossaire_html(glossaire_text, content, brief, date_str):
    """Reporte chaque terme du lexique du jour dans glossaire.html — un
    terme déjà présent n'est jamais modifié (garde son 1er lien source),
    un nouveau terme est inséré à la bonne place alphabétique. Édition
    SURGICALE par texte, jamais un aller-retour BeautifulSoup sur tout
    le fichier (2000+ lignes) qui risquerait de reformatter en silence
    des parties sans rapport — même principe que extract_block() dans
    generate_archives_table.py/generate_theme_pages.py. Retourne
    (nouveau_texte, liste des termes effectivement ajoutés)."""
    list_start_marker = '<dl class="lex-list" id="lex-list">'
    list_end_marker = "</dl>"
    if list_start_marker not in glossaire_text:
        raise PostEditionError(f'glossaire.html : marqueur {list_start_marker!r} introuvable')
    start = glossaire_text.index(list_start_marker) + len(list_start_marker)
    end = glossaire_text.index(list_end_marker, start)

    domain_label = DOMAIN_LABELS.get(brief["sujet"]["domain"], brief["sujet"]["domain"])
    h1 = content["h1"]
    text = glossaire_text
    added = []

    for term in content.get("lexique") or []:
        slug = term.get("slug")
        if not slug:
            continue
        entry_id = f"lex-{slug}"
        if f'id="{entry_id}"' in text[start:end]:
            continue  # déjà présent : jamais modifié, garde son 1er lien source

        new_entry = _build_glossaire_entry(term, domain_label, date_str, h1)
        new_key = _normalize_for_sort(term["terme"])

        insert_at = None
        for m in _GLOSSAIRE_ENTRY_RE.finditer(text[start:end]):
            if _normalize_for_sort(m.group(2)) > new_key:
                insert_at = start + m.start()
                break
        if insert_at is None:
            insert_at = end  # dernier alphabétiquement (ou liste vide)

        text = text[:insert_at] + new_entry + text[insert_at:]
        end += len(new_entry)
        added.append(term["terme"])

    return text, added


# ---------------------------------------------------------------------------
# sources-log.json / sources.html — « revue de presse » (docs/routine-prompt.md,
# étape 3) : automatisée le 14 septembre 2026, sur décision explicite de
# l'utilisateur, pour ne plus dépendre d'une étape manuelle de la routine
# CCR régulièrement sautée (3 jours d'écart réels constatés avant ce
# changement). Source : brief["revue_de_presse"] (voir
# docs/routine-brief-format.md) — PAS brief["sources"], qui sert à un
# usage distinct (les sources citées par faits_verifies[], presque
# toujours sur le sujet du jour) : la revue de presse porte au contraire
# des articles croisés au passage, pas forcément liés au sujet du jour,
# gardés pour leur intérêt factuel propre. Mêmes champs que sources-log.json
# à un près (l'"id" du brief, purement interne à faits_verifies[].sources,
# n'existe pas dans revue_de_presse).
# ---------------------------------------------------------------------------
_SOURCES_LOG_ARTICLE_FIELDS = ("title", "source", "url", "image", "lang", "domain", "summary", "read_minutes")


def build_sources_log_entry(brief):
    """brief["revue_de_presse"][] -> entrée sources-log.json du jour (mêmes
    champs). N'invente jamais de champ manquant : reprend la liste telle
    quelle, comme la routine manuelle le faisait pour sources-log.json."""
    articles = []
    for src in brief.get("revue_de_presse") or []:
        articles.append({k: src.get(k) for k in _SOURCES_LOG_ARTICLE_FIELDS})
    return {"date": brief["date"], "articles": articles}


def update_sources_log(sources_log_text, entry):
    """Insère l'entrée du jour dans sources-log.json (ordre du plus récent
    au plus ancien, comme sources.html.py trie déjà lui-même — voir
    render_page() : sorted(..., reverse=True) — mais l'ordre du JSON source
    reste explicite pour rester lisible en diff). Idempotent : si une entrée
    pour cette date existe déjà (relance après une exécution déjà publiée
    aujourd'hui, ou double déclenchement du pipeline), elle est REMPLACÉE
    par la nouvelle plutôt que dupliquée — jamais deux <section id="{date}">
    identiques sur sources.html. Retourne (nouveau_texte, ajoutée: bool)."""
    data = json.loads(sources_log_text)
    days = data.get("days", [])
    existing_idx = next((i for i, d in enumerate(days) if d.get("date") == entry["date"]), None)
    if existing_idx is not None:
        days[existing_idx] = entry
        added = False
    else:
        days.insert(0, entry)
        added = True
    data["days"] = days
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n", added


# ---------------------------------------------------------------------------
# Publication réelle (--publish uniquement, Phase 2)
# ---------------------------------------------------------------------------
def already_published_today(date_str):
    """Garde-fou repris de docs/routine-prompt.md (« vérifier qu'une
    autre exécution n'a pas déjà publié l'édition du jour ») — lit le
    VRAI index.html (jamais le bac à sable) et compare la date de
    `article:published_time` à celle du brief. Jamais bloquant si le
    fichier ou la balise est absent (nouveau dépôt/gabarit inhabituel) :
    on suppose alors qu'il n'y a rien à protéger."""
    index_path = REPO_ROOT / "index.html"
    if not index_path.exists():
        return False
    text = index_path.read_text(encoding="utf-8")
    m = re.search(r'<meta property="article:published_time" content="(\d{4}-\d{2}-\d{2})', text)
    return bool(m) and m.group(1) == date_str


def promote_to_real_repo(sandbox_root, date_str):
    """Copie les fichiers déjà générés (et validés) dans le bac à sable
    vers leurs vrais emplacements dans le dépôt — ne génère RIEN
    elle-même, ne fait aucun commit/push (le workflow appelant s'en
    charge). Le HTML de l'archive du jour devient à la fois le nouveau
    index.html (l'édition du jour) ET archives/{date}.html (copie
    figée) — même contenu, comme le veut docs/routine-prompt.md, étape
    6 (« index.html = toujours l'édition du jour uniquement »)."""
    archive_src = sandbox_root / "archives" / f"{date_str}.html"
    if not archive_src.exists():
        raise PostEditionError(f"--publish : HTML final introuvable dans le bac à sable : {archive_src}")
    html_text = archive_src.read_text(encoding="utf-8")

    (REPO_ROOT / "index.html").write_text(html_text, encoding="utf-8")
    real_archive_dir = REPO_ROOT / "archives"
    real_archive_dir.mkdir(parents=True, exist_ok=True)
    (real_archive_dir / f"{date_str}.html").write_text(html_text, encoding="utf-8")
    print(f"[post-edition] --publish : index.html + archives/{date_str}.html écrits (réels)")

    for rel in ("feed.xml", "sitemap.xml", "sitemap-news.xml", "glossaire.html", "archives.html"):
        src = sandbox_root / rel
        if not src.exists():
            raise PostEditionError(f"--publish : {rel} introuvable dans le bac à sable : {src}")
        (REPO_ROOT / rel).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print("[post-edition] --publish : feed.xml, sitemap.xml, sitemap-news.xml, glossaire.html, archives.html écrits (réels)")

    # sources-log.json / sources.html — jamais bloquant si absents du bac à
    # sable (brief["sources"] vide un jour donné, cas non observé en
    # pratique mais pas exclu par le schéma — voir docs/routine-brief-format.md
    # « sources : au moins 1 élément » : cette règle est déjà vérifiée en
    # amont par generate_daily_edition.py, donc en pratique toujours présents).
    for rel in ("sources-log.json", "sources.html"):
        src = sandbox_root / rel
        if src.exists():
            (REPO_ROOT / rel).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    if (sandbox_root / "sources-log.json").exists():
        print("[post-edition] --publish : sources-log.json, sources.html écrits (réels)")

    themes_src = sandbox_root / "themes"
    if themes_src.exists():
        real_themes_dir = REPO_ROOT / "themes"
        real_themes_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(themes_src.glob("*.html")):
            shutil.copy(f, real_themes_dir / f.name)
        print(f"[post-edition] --publish : {len(list(themes_src.glob('*.html')))} page(s) thématique(s) écrite(s) (réelles)")

    for rel_dir, pattern in (
        ("assets/social/topic-images", f"{date_str}*"),
        ("assets/social/instagram", f"{date_str}.png"),
    ):
        src_dir = sandbox_root / rel_dir
        if not src_dir.exists():
            continue
        dest_dir = REPO_ROOT / rel_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(src_dir.glob(pattern)):
            shutil.copy(f, dest_dir / f.name)
    print("[post-edition] --publish : images (topic-images/instagram) écrites (réelles)")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, help="chemin du brief JSON (même fichier que la rédaction)")
    parser.add_argument("--content", required=True, help="chemin du {date}.content.json produit par generate_daily_edition.py")
    parser.add_argument("--sandbox-root", default=None,
                         help="racine bac à sable pour toutes les écritures (défaut : _prototype-out/post-edition/{date}) — "
                              "jamais le dépôt réel")
    parser.add_argument("--skip-photo", action="store_true", help="n'appelle pas Pexels (test mécanique sans réseau)")
    parser.add_argument(
        "--publish", action="store_true",
        help="Phase 2 : écrit les vrais fichiers du dépôt (index.html, archives/, feed.xml, "
             "sitemap*.xml, glossaire.html, themes/*.html, images) en plus du bac à sable — "
             "jamais de commit/push depuis ce script, voir .github/workflows/post-edition.yml. "
             "Absent par défaut : comportement Phase 1 inchangé.",
    )
    args = parser.parse_args()

    brief = load_brief(args.brief)
    date_str = brief["date"]
    print(f"[post-edition] brief chargé : {args.brief} (date {date_str})")

    if args.publish and already_published_today(date_str):
        print(f"[post-edition] --publish : index.html porte déjà la date {date_str} — "
              "édition déjà publiée, on s'arrête proprement sans rien republier.")
        return

    content_path = Path(args.content)
    if not content_path.exists():
        raise PostEditionError(f"content.json introuvable : {content_path} — lancer generate_daily_edition.py d'abord")
    content = json.loads(content_path.read_text(encoding="utf-8"))

    sandbox_root = Path(args.sandbox_root) if args.sandbox_root else REPO_ROOT / "_prototype-out" / "post-edition" / date_str
    sandbox_root.mkdir(parents=True, exist_ok=True)
    print(f"[post-edition] bac à sable : {sandbox_root}")

    # 1. Photo — Pexels (sujet du jour) puis, à défaut, repli par registre
    # (assets/social/pub-photos/{registre}.jpg) — jamais directement
    # l'image générique unique du gabarit tant qu'un repli par registre
    # existe (voir docs/routine-prompt.md, étape « Image du sujet »,
    # point 4 : « ne pas publier sans image »).
    photo = None
    photo_credits = None
    if args.skip_photo:
        print("[post-edition] --skip-photo : pas d'appel Pexels, image générique conservée")
    else:
        image_keywords = brief.get("sujet", {}).get("image_keywords")
        photo_credits = select_topic_photo(image_keywords, date_str, sandbox_root)
        if photo_credits:
            print(f"[post-edition] photo Pexels retenue (requête « {photo_credits['query']} », {photo_credits['photographer']})")
        else:
            photo_credits = select_registry_fallback_photo(brief["registre"], date_str, sandbox_root)
            if photo_credits:
                print(f"[post-edition] repli sur la photo par défaut du registre {brief['registre']!r} "
                      f"({photo_credits['photographer']}) — pas une photo dédiée au sujet du jour")
            else:
                print("[post-edition] aucune photo retenue (ni Pexels ni repli registre) — image générique conservée")

    if photo_credits:
        # Deux URLs distinctes, jamais confondues (bug réel trouvé le 14
        # septembre 2026 en relisant le rendu réel de la page : les deux
        # pointaient vers la même image composée, créant une superposition
        # visuelle titre-sur-titre) — voir docs/routine-prompt.md, étape
        # « Image du sujet » : og_image_url (meta og:image/twitter:image/
        # JSON-LD, prévisualisation sociale) pointe vers le PNG Instagram
        # composé (titre + scénarios incrustés) ; hero_image_url (l'<img>
        # visible en tête d'article) pointe vers la photo BRUTE recadrée
        # (topic-images/{date}-wide.jpg), jamais l'image composée. Repli
        # sur le carré si le recadrage large n'a pas pu être produit
        # (voir select_topic_photo()).
        wide_path = photo_credits.get("wide_path")
        hero_filename = f"{date_str}-wide.jpg" if wide_path else f"{date_str}.jpg"
        photo = {
            "og_image_url": f"{SITE_URL}/assets/social/instagram/{date_str}.png",
            "hero_image_url": f"{SITE_URL}/assets/social/topic-images/{hero_filename}",
            "alt": f"Photo d'illustration — {content['h1']}",
            "photographer": photo_credits["photographer"],
            "pexels_url": photo_credits["pexels_url"],
            "square_path": photo_credits["square_path"],
        }

    # 2. HTML final (photo incluse)
    index_html_path = REPO_ROOT / "index.html"
    shell = build_html.extract_shell(index_html_path.read_text(encoding="utf-8"))
    html_text, edition_number = build_html.assemble_index_html(shell, content, brief, date_str, photo=photo)
    archive_dir = sandbox_root / "archives"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{date_str}.html"
    archive_path.write_text(html_text, encoding="utf-8")
    print(f"[post-edition] HTML final (édition N°{edition_number}) écrit : {archive_path}")

    # 3. Image Instagram
    ig_image_path = generate_instagram_image(content, date_str, sandbox_root, photo)
    ig_image_size = ig_image_path.stat().st_size
    ig_image_url = f"{SITE_URL}/assets/social/instagram/{date_str}.png"
    print(f"[post-edition] image Instagram écrite : {ig_image_path} ({ig_image_size} octets)")

    # 4. feed.xml
    word_count = estimate_word_count(content)
    read_minutes = max(1, round(word_count / 200))
    feed_item = build_feed_item(content, date_str, read_minutes, ig_image_url, ig_image_size)
    feed_text = (REPO_ROOT / "feed.xml").read_text(encoding="utf-8")
    new_feed_text = update_feed_xml(feed_text, feed_item)
    ET.fromstring(new_feed_text)  # valide la syntaxe XML avant écriture — échoue fort sinon
    feed_out = sandbox_root / "feed.xml"
    feed_out.write_text(new_feed_text, encoding="utf-8")
    print(f"[post-edition] feed.xml (avec nouvel item, {read_minutes} min de lecture) écrit : {feed_out}")

    # 4bis. glossaire.html — voir docs/routine-prompt.md, étape 6ter
    glossaire_text = (REPO_ROOT / "glossaire.html").read_text(encoding="utf-8")
    new_glossaire_text, added_terms = update_glossaire_html(glossaire_text, content, brief, date_str)
    glossaire_out = sandbox_root / "glossaire.html"
    glossaire_out.write_text(new_glossaire_text, encoding="utf-8")
    if added_terms:
        print(f"[post-edition] glossaire.html : {len(added_terms)} nouveau(x) terme(s) ajouté(s) — {', '.join(added_terms)}")
    else:
        print("[post-edition] glossaire.html : aucun nouveau terme (tous déjà présents)")

    # 5. sitemap.xml / sitemap-news.xml
    sitemap_text = (REPO_ROOT / "sitemap.xml").read_text(encoding="utf-8")
    new_sitemap_text = update_sitemap_xml(sitemap_text, date_str, bump_glossaire=bool(added_terms))
    ET.fromstring(new_sitemap_text)
    sitemap_out = sandbox_root / "sitemap.xml"
    sitemap_out.write_text(new_sitemap_text, encoding="utf-8")
    print(f"[post-edition] sitemap.xml écrit : {sitemap_out}")

    sitemap_news_text = (REPO_ROOT / "sitemap-news.xml").read_text(encoding="utf-8")
    new_sitemap_news_text = update_sitemap_news_xml(sitemap_news_text, date_str, content["h1"])
    ET.fromstring(new_sitemap_news_text)
    sitemap_news_out = sandbox_root / "sitemap-news.xml"
    sitemap_news_out.write_text(new_sitemap_news_text, encoding="utf-8")
    print(f"[post-edition] sitemap-news.xml écrit : {sitemap_news_out}")

    # 6. archives.html — generate_archives_table.py calcule sa racine à
    # partir de son PROPRE __file__ (Path(__file__).resolve().parents[2]),
    # jamais du cwd : l'appeler tel quel toucherait le vrai archives.html
    # du dépôt. Ruse plutôt que fork du script (jamais dupliquer sa
    # logique) : on reproduit sous le bac à sable la portion d'arborescence
    # qu'il lit (archives/, suivi/, hebdo/, glossaire.html) ET on copie le
    # script lui-même au même chemin relatif (scripts/seo/...) — son
    # __file__ résout alors naturellement sur le bac à sable, jamais sur
    # le vrai dépôt.
    mirror_root = sandbox_root / "repo-mirror"
    if mirror_root.exists():
        shutil.rmtree(mirror_root)
    shutil.copytree(REPO_ROOT / "archives", mirror_root / "archives")
    if (REPO_ROOT / "suivi").exists():
        shutil.copytree(REPO_ROOT / "suivi", mirror_root / "suivi")
    if (REPO_ROOT / "hebdo").exists():
        shutil.copytree(REPO_ROOT / "hebdo", mirror_root / "hebdo")
    shutil.copy(REPO_ROOT / "glossaire.html", mirror_root / "glossaire.html")
    shutil.copy(archive_path, mirror_root / "archives" / f"{date_str}.html")

    # Bug réel du 14 septembre 2026 (signalé par l'utilisateur : badge EN
    # disparu sur archives.html, y compris pour des éditions déjà traduites
    # les jours précédents) : generate_archives_table.py lit lui-même
    # en/archives/{date}.html sur disque pour décider d'ajouter le badge
    # EN — mais ce dossier n'était jamais recopié dans ce miroir, donc le
    # script y voyait TOUJOURS aucune traduction et régénérait
    # archives.html avec zéro badge, quelle que soit la date. Ce fichier
    # sans badges était ensuite promu tel quel vers le vrai dépôt via
    # --publish, effaçant les 20 badges déjà présents. Corrigé en
    # recopiant aussi en/archives/ dans le miroir.
    if (REPO_ROOT / "en" / "archives").exists():
        shutil.copytree(REPO_ROOT / "en" / "archives", mirror_root / "en" / "archives")

    mirrored_script_dir = mirror_root / "scripts" / "seo"
    mirrored_script_dir.mkdir(parents=True, exist_ok=True)
    mirrored_script = mirrored_script_dir / "generate_archives_table.py"
    shutil.copy(SEO_DIR / "generate_archives_table.py", mirrored_script)

    result = subprocess.run(
        [sys.executable, str(mirrored_script)],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise PostEditionError(f"generate_archives_table.py a échoué : {result.stderr[-1000:]}")
    generated = mirror_root / "archives.html"
    if not generated.exists():
        raise PostEditionError(f"generate_archives_table.py n'a pas produit {generated}")
    archives_html_out = sandbox_root / "archives.html"
    archives_html_out.write_text(generated.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[post-edition] archives.html régénéré : {archives_html_out}")

    # 7. Pages thématiques (SEO, maillage interne) — generate_theme_pages.py
    # lit archives.html (déjà régénéré ci-dessus, dans le même mirror_root)
    # + glossaire.html (déjà copié) et écrit themes/{slug}.html pour les 6
    # domaines. Même ruse __file__ que generate_archives_table.py — même
    # mirror_root, donc rien à recopier de plus.
    mirrored_theme_script = mirrored_script_dir / "generate_theme_pages.py"
    shutil.copy(SEO_DIR / "generate_theme_pages.py", mirrored_theme_script)
    result = subprocess.run(
        [sys.executable, str(mirrored_theme_script)],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise PostEditionError(f"generate_theme_pages.py a échoué : {result.stderr[-1000:]}")
    mirrored_themes_dir = mirror_root / "themes"
    if not mirrored_themes_dir.exists():
        raise PostEditionError(f"generate_theme_pages.py n'a produit aucun fichier sous {mirrored_themes_dir}")
    themes_out = sandbox_root / "themes"
    if themes_out.exists():
        shutil.rmtree(themes_out)
    shutil.copytree(mirrored_themes_dir, themes_out)
    n_themes = len(list(themes_out.glob("*.html")))
    print(f"[post-edition] {n_themes} page(s) thématique(s) régénérée(s) : {themes_out}")

    # 8. sources-log.json / sources.html — « revue de presse », automatisée
    # le 14 septembre 2026 (voir commentaire au-dessus de build_sources_log_entry()
    # plus haut dans ce fichier). Jamais bloquant : brief["revue_de_presse"]
    # vide/absent -> aucun jour ajouté (comme le faisait la routine
    # manuelle), ni sources-log.json ni sources.html ne sont même écrits
    # dans le bac à sable — promote_to_real_repo() ne touche alors pas ces
    # deux fichiers du tout.
    if brief.get("revue_de_presse"):
        # Même mirror_root que les étapes 6-7 : il a déjà glossaire.html,
        # le 2e fichier lu par generate_sources_page.py — rien de plus à
        # recopier pour cette dépendance.
        sources_entry = build_sources_log_entry(brief)
        sources_log_text = (REPO_ROOT / "sources-log.json").read_text(encoding="utf-8")
        new_sources_log_text, sources_added = update_sources_log(sources_log_text, sources_entry)
        json.loads(new_sources_log_text)  # valide la syntaxe JSON avant écriture — échoue fort sinon
        sources_log_out = sandbox_root / "sources-log.json"
        sources_log_out.write_text(new_sources_log_text, encoding="utf-8")
        (mirror_root / "sources-log.json").write_text(new_sources_log_text, encoding="utf-8")
        if sources_added:
            print(f"[post-edition] sources-log.json : {len(sources_entry['articles'])} article(s) ajouté(s) pour {date_str}")
        else:
            print(f"[post-edition] sources-log.json : entrée du {date_str} déjà présente — remplacée (relance idempotente)")

        mirrored_sources_script = mirrored_script_dir / "generate_sources_page.py"
        shutil.copy(SEO_DIR / "generate_sources_page.py", mirrored_sources_script)
        result = subprocess.run(
            [sys.executable, str(mirrored_sources_script)],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            raise PostEditionError(f"generate_sources_page.py a échoué : {result.stderr[-1000:]}")
        generated_sources_html = mirror_root / "sources.html"
        if not generated_sources_html.exists():
            raise PostEditionError(f"generate_sources_page.py n'a pas produit {generated_sources_html}")
        sources_html_out = sandbox_root / "sources.html"
        sources_html_out.write_text(generated_sources_html.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[post-edition] sources.html régénéré : {sources_html_out}")
    else:
        print("[post-edition] revue_de_presse : absente/vide dans le brief — aucun jour ajouté (comme avant, jamais forcé)")

    print(f"[post-edition] terminé — {word_count} mots, {read_minutes} min de lecture.")

    if args.publish:
        promote_to_real_repo(sandbox_root, date_str)
        print("[post-edition] --publish : fichiers réels écrits — commit/push restent à faire par le workflow appelant.")
    else:
        print("[post-edition] AUCUN commit, AUCUN push effectué — Phase 1 prototype (workflow_dispatch uniquement).")


if __name__ == "__main__":
    try:
        main()
    except PostEditionError as e:
        print(f"[post-edition] ERREUR : {e}", file=sys.stderr)
        sys.exit(1)
