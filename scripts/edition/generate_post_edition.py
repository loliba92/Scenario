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
     tout juste régénéré à l'étape 6, même bac à sable) ;
  8. docs/sujets-a-suivre.md, section « Journal des sujets publiés » :
     append_journal_entry() ajoute une ligne pour l'édition du jour, en
     tête de liste — seule source dont dépend generate_weekly_recap.py
     pour retrouver les éditions de la semaine (voir append_journal_entry()
     pour l'incident du 21 septembre 2026 qui a motivé cet ajout).

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

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

import build_html
import generate_seo_head
from generate_daily_edition import estimate_word_count, load_brief, normalize_content_markdown

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
# 0. SEO Head injection — génération automatique du <head> optimisé
# ---------------------------------------------------------------------------
# Balises "per-day" du <head> que generate_seo_head() régénère — tout le
# reste (icônes, manifest, apple-*, pwa-install.css, preconnect, fonts,
# <style>...) doit impérativement survivre à l'injection SEO. Même famille
# de prédicats que build_html._PER_DAY_HEAD_PREDICATES, sauf <style> qu'on
# préserve ici au lieu de le gérer séparément.
_SEO_PER_DAY_HEAD_PREDICATES = [
    lambda t: t.name == "meta" and t.get("charset"),
    lambda t: t.name == "meta" and t.get("name") == "viewport",
    lambda t: t.name == "title",
    lambda t: t.name == "link" and t.get("rel") in (["canonical"], ["alternate"]),
    lambda t: t.name == "meta" and t.get("name") in ("description", "robots", "language", "color-scheme", "keywords"),
    lambda t: t.name == "meta" and (t.get("property") or "").startswith(("og:", "article:")),
    lambda t: t.name == "meta" and (t.get("name") or "").startswith("twitter:"),
    lambda t: t.name == "script" and t.get("type") == "application/ld+json",
]


# Formatter bs4 qui préserve l'ordre D'INSERTION des attributs (celui du
# HTML source, puisque html.parser peuple tag.attrs dans l'ordre où il
# rencontre les attributs) et n'auto-ferme jamais les balises vides — au
# lieu du formatter par défaut de bs4, qui trie les attributs par ordre
# alphabétique et ajoute "/>" partout. Sans ça, <meta property="article:
# published_time" content="..."> ressort en <meta content="..."
# property="..."/>, ce qui casse déjà_published_today() (regex plus bas,
# qui attend cet ordre précis) et plusieurs autres regex du dépôt qui lisent
# index.html/archives/*.html en texte brut (generate_archives_table.py,
# extract_article_data.py, generate_suivi_update.py, generate_weekly_recap.py,
# translate_daily.py) — régression découverte en code review le 26 septembre
# 2026, sur la toute première version de cette fonction utilisant bs4.
class _PreserveAttrOrderFormatter(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


_HEAD_FORMATTER = _PreserveAttrOrderFormatter(void_element_close_prefix=None)


def inject_seo_head(html_text, brief):
    """Remplace UNIQUEMENT les balises "per-day" du <head> (title, canonical,
    meta description, og:*, article:*, twitter:*, JSON-LD) par la version SEO
    optimisée générée depuis le brief — sans jamais toucher au reste du
    <head> (icônes, manifest, fonts, pwa-install.css, et surtout le <style>
    du site), ni à un seul octet du <body>.

    Incident du 26 septembre 2026 : cette fonction remplaçait auparavant
    TOUT <head>...</head> par le head SEO généré par generate_seo_head(),
    qui ne contient QUE les balises SEO — perdant silencieusement le
    <style> et tout le head_static (icônes, manifest, fonts), page rendue
    entièrement noire en production. Réécrite une première fois avec bs4
    sur le document ENTIER (régression détectée en review, voir
    _PreserveAttrOrderFormatter ci-dessus), puis une seconde fois pour se
    limiter strictement au texte du <head> : bs4 ne voit jamais le <body>,
    qui est reconcaténé tel quel, byte pour byte.
    """
    try:
        new_head_html = generate_seo_head.generate_seo_head(brief)
    except Exception as e:
        raise PostEditionError(f"Génération du head SEO échouée : {e}")

    match = re.search(r"<head\b[^>]*>.*?</head>", html_text, re.DOTALL | re.IGNORECASE)
    if not match:
        raise PostEditionError("Impossible de trouver <head>...</head> dans le HTML généré")
    head_text = match.group(0)

    head_soup = BeautifulSoup(head_text, "html.parser")
    head = head_soup.select_one("head")
    if head is None:
        raise PostEditionError("Impossible de parser <head> dans le HTML généré")

    had_style = head.select_one("style") is not None
    had_manifest = head.select_one('link[rel="manifest"]') is not None

    for tag in list(head.find_all(recursive=False)):
        if any(pred(tag) for pred in _SEO_PER_DAY_HEAD_PREDICATES):
            tag.decompose()

    new_head_soup = BeautifulSoup(new_head_html, "html.parser")
    new_head_tag = new_head_soup.select_one("head") or new_head_soup
    new_children = list(new_head_tag.find_all(recursive=False))

    first_remaining = next(iter(head.find_all(recursive=False)), None)
    for child in new_children:
        if first_remaining is not None:
            first_remaining.insert_before(child)
        else:
            head.append(child)

    new_head_text = head_soup.decode(formatter=_HEAD_FORMATTER)

    # GARDE-FOU : le <style> et le head_static ne doivent JAMAIS disparaître
    # ici (incident du 26 septembre 2026 — voir docstring ci-dessus).
    if had_style and "<style" not in new_head_text:
        raise PostEditionError(
            "❌ CRITIQUE : inject_seo_head() a fait disparaître le <style> du <head> ! "
            "La page serait entièrement noire. Abandon immédiat."
        )
    if had_manifest and "manifest.webmanifest" not in new_head_text:
        raise PostEditionError(
            "❌ CRITIQUE : inject_seo_head() a fait disparaître le head_static "
            "(manifest.webmanifest) du <head> ! Abandon immédiat."
        )

    return html_text[: match.start()] + new_head_text + html_text[match.end() :]


# ---------------------------------------------------------------------------
# 1. Photo de sujet (Pexels) — sélection automatique
# ---------------------------------------------------------------------------
def select_topic_photo(image_keywords, edition_id, sandbox_root, timeout=25):
    """Retourne un dict de crédits pour le 1er candidat Pexels retenu, ou
    None si aucune photo n'a pu être obtenue — jamais bloquant : l'appelant
    retombe alors sur l'image générique existante (photo=None,
    build_html.py, comportement historique de la Phase 1 rédaction).

    edition_id (jamais date_str seul, chantier multi-éditions/jour du
    28 septembre 2026) : passé tel quel à use_topic_image.py --date, qui
    ne fait QUE s'en servir comme nom de fichier (jamais parsé/validé
    comme une vraie date, vérifié dans use_topic_image.py) — une édition
    à slug (--slug) obtient donc sa propre image
    topic-images/{edition_id}.jpg, jamais celle de l'édition IA du jour.
    Avant ce correctif, les deux auraient partagé le même fichier
    topic-images/{date}.jpg et se seraient silencieusement écrasées l'une
    l'autre — risque réel dès qu'une édition à slug est publiée SANS
    --skip-photo."""
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
            [sys.executable, str(use_script), candidate_path, "--date", edition_id,
             "--credits", str(credits_path), "--repo-root", str(sandbox_root)],
            check=True, capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"[post-edition] use_topic_image.py a échoué : {e}", file=sys.stderr)
        return None

    square_path = sandbox_root / "assets" / "social" / "topic-images" / f"{edition_id}.jpg"
    if not square_path.exists():
        print(f"[post-edition] image carrée attendue introuvable : {square_path}", file=sys.stderr)
        return None
    # Le recadrage large (-wide.jpg) n'est pas toujours produit par
    # use_topic_image.py (nécessite original_url dans credits.json, voir
    # sa docstring) — jamais bloquant, main() retombe alors sur le carré
    # pour l'image visible en tête d'article.
    wide_path = sandbox_root / "assets" / "social" / "topic-images" / f"{edition_id}-wide.jpg"

    return {
        "square_path": square_path,
        "wide_path": wide_path if wide_path.exists() else None,
        "photographer": chosen.get("photographer") or "Photographe non identifié",
        "pexels_url": chosen.get("pexels_url") or "https://www.pexels.com/",
        "query": image_keywords,
    }


def select_topic_photo_from_preview(preview_credits, edition_id, sandbox_root, timeout=25):
    """Télécharge directement la photo Pexels déjà choisie et validée en
    preview (URL connue dans `preview_credits['original_url']`), sans
    refaire de recherche — garantit que l'image publiée est EXACTEMENT
    celle que l'utilisateur a validée en preview, jamais un résultat
    différent d'une recherche Pexels relancée à un autre moment (même
    principe que la réutilisation du content.json du preview pour le
    texte, voir post-edition.yml — incident du 21 septembre 2026).
    Retourne None si le téléchargement échoue — l'appelant retombe alors
    sur select_topic_photo() (nouvelle recherche), jamais bloquant."""
    original_url = preview_credits.get("original_url")
    if not original_url:
        print("[post-edition] preview_credits sans original_url — repli sur une recherche Pexels normale", file=sys.stderr)
        return None

    candidates_dir = sandbox_root / "topic-image-candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(SOCIAL_DIR))
    from fetch_topic_image import download, square_crop_url  # noqa: PLC0415 — import tardif volontaire, voir docstrings des scripts sources

    candidate_path = candidates_dir / "candidate-1.jpg"
    try:
        download(square_crop_url(original_url), str(candidate_path))
    except Exception as e:
        print(f"[post-edition] téléchargement de la photo du preview a échoué : {e}", file=sys.stderr)
        return None

    credits_path = candidates_dir / "credits.json"
    credits_path.write_text(
        json.dumps([{
            "candidate": 1, "source": "pexels", "file": str(candidate_path),
            "photographer": preview_credits.get("photographer"),
            "pexels_url": preview_credits.get("pexels_url"),
            "original_url": original_url,
            "query": preview_credits.get("query"),
        }], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    use_script = SOCIAL_DIR / "use_topic_image.py"
    try:
        subprocess.run(
            [sys.executable, str(use_script), str(candidate_path), "--date", edition_id,
             "--credits", str(credits_path), "--repo-root", str(sandbox_root)],
            check=True, capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"[post-edition] use_topic_image.py a échoué (photo du preview) : {e}", file=sys.stderr)
        return None

    square_path = sandbox_root / "assets" / "social" / "topic-images" / f"{edition_id}.jpg"
    if not square_path.exists():
        print(f"[post-edition] image carrée attendue introuvable : {square_path}", file=sys.stderr)
        return None
    wide_path = sandbox_root / "assets" / "social" / "topic-images" / f"{edition_id}-wide.jpg"

    return {
        "square_path": square_path,
        "wide_path": wide_path if wide_path.exists() else None,
        "photographer": preview_credits.get("photographer") or "Photographe non identifié",
        "pexels_url": preview_credits.get("pexels_url") or "https://www.pexels.com/",
        "query": preview_credits.get("query"),
    }


def select_registry_fallback_photo(registre, edition_id, sandbox_root):
    """Repli sur la photo par défaut du registre (assets/social/pub-
    photos/{registre}.jpg + credits.json) quand Pexels échoue ou ne
    retient rien — jamais l'image générique unique du gabarit tant
    qu'un repli par registre existe (voir docs/routine-prompt.md, étape
    « Image du sujet », point 4 : « ne pas publier sans image »).
    Recadrage LOCAL (Pillow, réutilise square_crop_local/wide_crop_local
    de fetch_topic_image.py/use_topic_image.py) — aucun appel réseau.

    edition_id (jamais date_str seul) : même raison que select_topic_photo()
    — le fichier recadré est écrit sous topic-images/{edition_id}.jpg,
    jamais partagé entre deux éditions du même jour."""
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
    square_path = topic_images_dir / f"{edition_id}.jpg"
    try:
        square_crop_local(str(src_path), str(square_path))
        wide_crop_local(str(src_path), str(topic_images_dir / f"{edition_id}-wide.jpg"))
    except Exception as e:
        print(f"[post-edition] recadrage de la photo de repli échoué : {e}", file=sys.stderr)
        return None

    credit_entry = dict(entry)
    credit_entry["note"] = "banque de secours par registre, pas une photo dédiée au sujet du jour"
    (topic_images_dir / f"{edition_id}.json").write_text(
        json.dumps(credit_entry, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return {
        "square_path": square_path,
        "wide_path": topic_images_dir / f"{edition_id}-wide.jpg",
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
def strip_inline_tags(html_text):
    """Retire les balises inline (<strong>, <span>...) d'un fragment HTML
    simple — utilisé pour <source> ci-dessous, qui doit rester du texte
    brut (voir build_feed_item()), jamais du HTML comme <description>."""
    return re.sub(r"<[^>]+>", "", html_text)


def build_feed_item(content, edition_id, read_minutes, ig_image_url, ig_image_size):
    # edition_id (jamais date_str seul) pour link/guid : deux éditions
    # publiées le même jour (chantier multi-éditions/jour, 28 septembre
    # 2026) partageraient sinon un guid identique — un lecteur RSS traite
    # alors la 2e comme une mise à jour de la 1re plutôt que comme une
    # entrée distincte, et link pointerait vers le mauvais fichier pour
    # l'une des deux (voir build_html.build_archive_entry() pour la
    # convention de nommage "{date}" / "{date}-{slug}").
    h1 = content["h1"]
    link = f"{SITE_URL}/archives/{edition_id}.html"
    guid = f"scenario-{edition_id}"
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

    # <source> : le texte complet de « L'essentiel » (essentiel_box + France
    # Impact), en clair (balises inline retirées) — jamais construit par
    # cette chaîne depuis le 14 septembre 2026, contrairement à l'ancienne
    # routine manuelle. Deux consommateurs en dépendent silencieusement :
    # l'Automation Buttondown RSS-to-email de la newsletter quotidienne
    # (docs/ARCHITECTURE.md, § « Buttondown ») ET
    # scripts/en/translate_daily.py::collect_feed_segments(), qui construit
    # l'entrée en/feed.xml (lue par Make pour la publication sociale EN) à
    # partir de ce même champ — son absence ne fait échouer ni l'un ni
    # l'autre bruyamment (ils se contentent de sauter silencieusement),
    # d'où deux jours (14-15 septembre) sans nouvelle entrée en/feed.xml et
    # potentiellement une newsletter FR incomplète sur la même période.
    # Toujours exactement 5 paragraphes séparés par une ligne vide — même
    # format que l'ancienne routine, voir docs/BACKLOG.md.
    essentiel_plain = [strip_inline_tags(p).strip() for p in content["essentiel_box"]]
    df = content.get("delta_france")
    if df:
        essentiel_plain.append(strip_inline_tags(
            f"Notre évaluation de l'impact pour la France : {df['word']}. {df['text']}"
        ).strip())
    source = ""
    if len(essentiel_plain) == 5:
        source_text = escape_xml("\n\n".join(essentiel_plain))
        source = f'\n      <source url="{link}">{source_text}</source>'

    return (
        "    <item>\n"
        f"      <title>{escape_xml(h1)}</title>\n"
        f"      <link>{link}</link>\n"
        f'      <guid isPermaLink="false">{guid}</guid>\n'
        f"      <pubDate>{pub_date}</pubDate>\n"
        f"      <comments>{escape_xml(question)}</comments>\n"
        f"      <category>{category}</category>"
        f"{enclosure}\n"
        f"      <description><![CDATA[{description}]]></description>"
        f"{source}\n"
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
def update_sitemap_xml(sitemap_text, edition_id, bump_glossaire=False):
    # edition_id (jamais date_str seul) pour <loc> : voir build_feed_item()
    # plus haut, même raison — deux éditions publiées le même jour
    # (chantier multi-éditions/jour, 28 septembre 2026) auraient sinon
    # généré la même <loc>, la 2e silencieusement invisible pour Google
    # (déjà présente en apparence). date_str (les 10 premiers caractères)
    # reste utilisé pour <lastmod>, purement calendaire.
    date_str = edition_id[:10]

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
        f"    <loc>{SITE_URL}/archives/{edition_id}.html</loc>\n"
        f"    <lastmod>{date_str}</lastmod>\n"
        "    <changefreq>never</changefreq>\n"
        "    <priority>0.6</priority>\n"
        "  </url>\n"
    )
    marker = f"<loc>{SITE_URL}/archives.html</loc>"
    idx = text.index(marker)
    insert_at = text.index("</url>", idx) + len("</url>\n")
    return text[:insert_at] + new_entry + text[insert_at:]


def update_sitemap_news_xml(sitemap_news_text, edition_id, title):
    """Ajoute l'entrée du jour et purge tout ce qui a plus de 48h — la
    purge est la règle ici, contrairement à sitemap.xml (voir
    docs/routine-prompt.md, étape technique 7bis). edition_id (jamais
    date_str seul) pour <loc> : même raison que update_sitemap_xml()."""
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
    ET.SubElement(new_url, f"{{{ns['sm']}}}loc").text = f"{SITE_URL}/archives/{edition_id}.html"
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


def _build_glossaire_entry(term, domain_label, edition_id, h1):
    # edition_id (jamais date_str seul) : lien vers l'édition source exacte
    # du terme — voir build_html.build_archive_entry() pour la convention
    # "{date}" (IA) / "{date}-{slug}" (édition supplémentaire du même
    # jour), chantier multi-éditions/jour du 28 septembre 2026. Deux
    # éditions le même jour ont chacune leur propre fichier ; un lien basé
    # sur la seule date pointerait toujours vers la même (mauvaise) archive
    # pour l'une des deux.
    return (
        f'      <div class="lex-entry" id="lex-{term["slug"]}">\n'
        f'        <dt class="lex-term">{html.escape(term["terme"])}</dt>\n'
        f'        <dd class="lex-def">{html.escape(term["definition"])}</dd>\n'
        '        <div class="lex-meta">\n'
        f'          <span class="lex-domain">{html.escape(domain_label)}</span>\n'
        f'          <a class="lex-source" href="archives/{edition_id}.html">Vu dans : {html.escape(h1)} →</a>\n'
        "        </div>\n"
        "      </div>\n"
    )


def update_glossaire_html(glossaire_text, content, brief, edition_id):
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

        new_entry = _build_glossaire_entry(term, domain_label, edition_id, h1)
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
# Liens relatifs de la copie archives/{date}.html — régression réelle du
# 14 septembre 2026, détectée le 15 (retour utilisateur : icône « Revue de
# presse » et son lien morts sur une page d'archive). L'ancienne routine
# manuelle avait une étape dédiée pour ça (docs/routine-prompt.md,
# référence historique, étape technique 5 : « adapter tous les liens
# relatifs d'un niveau ») — perdue au passage à ce script, qui écrivait
# jusqu'ici EXACTEMENT le même HTML sur index.html (racine du dépôt) et
# archives/{date}.html (un niveau plus bas) : tout lien/asset relatif à la
# racine (assets/..., archives.html, glossaire.html, sources.html,
# hebdo/..., index.html, dashboard.html, manifest.webmanifest...) devient
# alors mort sur la copie d'archive. generate_theme_pages.py avait déjà ce
# problème pour ses propres pages (themes/{slug}.html, aussi un niveau
# plus bas) et le corrige avec une liste blanche de noms de pages connus —
# ici on préfère une règle générique (tout préfixer sauf ce qui est
# explicitement absolu/une ancre/un schéma) pour ne jamais dépendre d'une
# liste à tenir à jour à chaque nouvelle page racine.
# ---------------------------------------------------------------------------
_ARCHIVE_LINK_ATTR_RE = re.compile(r'(href|src)="([^"]*)"')
_ARCHIVE_LINK_EXCLUDED_PREFIXES = (
    "http://", "https://", "//", "#", "mailto:", "tel:", "data:", "javascript:",
    "../", "./",  # déjà relatif correctement (ex. le bouton EN, posé par translate_daily.py)
)


def rebase_links_for_archive_copy(html_text):
    """Retourne une copie de html_text avec chaque lien/asset relatif à la
    racine préfixé de "../" — à appliquer UNIQUEMENT à la copie qui va sous
    archives/{date}.html, jamais à celle qui va sur index.html (racine,
    où ces liens sont déjà corrects tels quels)."""
    def repl(m):
        attr, value = m.group(1), m.group(2)
        if value and not value.lower().startswith(_ARCHIVE_LINK_EXCLUDED_PREFIXES):
            return f'{attr}="../{value}"'
        return m.group(0)
    return _ARCHIVE_LINK_ATTR_RE.sub(repl, html_text)


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
    autre exécution n'a pas déjà publié l'édition du jour ») — vérifie
    l'existence du VRAI archives/{date}.html (jamais le bac à sable),
    l'emplacement fixe de l'édition IA quotidienne (voir build_archive_entry()
    et le chantier multi-éditions/jour du 28 septembre 2026 : une édition
    supplémentaire du même jour prend "{date}-{slug}.html", jamais
    "{date}.html" nu — donc cette vérification ne peut jamais être
    faussée par une édition journaliste indépendante publiée le même jour).

    Corrigé le 28 septembre 2026 : la version précédente lisait
    `article:published_time` dans index.html, une balise qui n'existe
    plus depuis la home redesign du 27 septembre (index.html est devenue
    une page de présentation fixe, og:type=website, plus aucune métadonnée
    d'article) — ce garde-fou ne bloquait donc plus RIEN depuis, en
    silence (aucune erreur, juste un `re.search` qui ne trouvait jamais
    rien). Jamais détecté avant faute de double publication réelle depuis
    ce changement — bug resté latent."""
    return (REPO_ROOT / "archives" / f"{date_str}.html").exists()


def promote_to_real_repo(sandbox_root, edition_id):
    """Copie les fichiers déjà générés (et validés) dans le bac à sable
    vers leurs vrais emplacements dans le dépôt — ne génère RIEN
    elle-même, ne fait aucun commit/push (le workflow appelant s'en
    charge). index.html (racine) et archives/{edition_id}.html (copie
    figée, un niveau plus bas) portent le même contenu éditorial mais PAS
    le même HTML octet pour octet depuis le 15 septembre 2026 : leurs
    liens/assets relatifs à la racine diffèrent forcément d'un "../" (voir
    rebase_links_for_archive_copy() plus haut — avant ce correctif, les
    deux fichiers étaient identiques et tout lien relatif était mort sur
    la copie d'archive, régression du 14 septembre 2026).

    edition_id (jamais date_str seul, chantier multi-éditions/jour du
    28 septembre 2026) : "{date}" pour l'édition IA, "{date}-{slug}" pour
    une édition supplémentaire du même jour déclenchée à la main
    (--slug) — voir main()."""
    index_src = sandbox_root / "index.html"
    archive_src = sandbox_root / "archives" / f"{edition_id}.html"
    if not index_src.exists():
        raise PostEditionError(f"--publish : HTML final (racine) introuvable dans le bac à sable : {index_src}")
    if not archive_src.exists():
        raise PostEditionError(f"--publish : HTML final (archive) introuvable dans le bac à sable : {archive_src}")

    # GARDE-FOU final avant promotion vers les vrais fichiers du dépôt
    # (incident du 26 septembre 2026 — voir inject_seo_head()) : dernier
    # filet avant que ces fichiers ne remplacent index.html/archives/*.html
    # en production. Jamais de promotion d'un fichier sans CSS.
    for src_path in (index_src, archive_src):
        src_text = src_path.read_text(encoding="utf-8")
        if "<style" not in src_text or "</style>" not in src_text:
            raise PostEditionError(
                f"❌ CRITIQUE : {src_path} ne contient pas de <style> ! "
                "La page serait entièrement noire en production. --publish annulé, rien n'est écrit."
            )

    (REPO_ROOT / "index.html").write_text(index_src.read_text(encoding="utf-8"), encoding="utf-8")
    real_archive_dir = REPO_ROOT / "archives"
    real_archive_dir.mkdir(parents=True, exist_ok=True)
    (real_archive_dir / f"{edition_id}.html").write_text(archive_src.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[post-edition] --publish : index.html + archives/{edition_id}.html écrits (réels, liens de l'archive réajustés d'un niveau)")

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
        ("assets/social/topic-images", f"{edition_id}*"),
        ("assets/social/instagram", f"{edition_id}.png"),
    ):
        src_dir = sandbox_root / rel_dir
        if not src_dir.exists():
            continue
        dest_dir = REPO_ROOT / rel_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(src_dir.glob(pattern)):
            shutil.copy(f, dest_dir / f.name)
    # Vignette carrée (cartes des pages thèmes, liste d'archives) : tirée de la
    # photo du sujet qui vient d'être copiée. Jamais bloquant.
    square = REPO_ROOT / "assets/social/topic-images" / f"{edition_id}.jpg"
    if square.exists():
        try:
            sys.path.insert(0, str(SOCIAL_DIR))
            from generate_archive_thumbnail import make_square_thumb  # noqa: PLC0415
            make_square_thumb(square, REPO_ROOT / "assets/social/archive-thumbs" / f"{edition_id}.jpg", 144)
        except Exception as e:  # noqa: BLE001
            print(f"[post-edition] vignette non créée : {e}", file=sys.stderr)
    print("[post-edition] --publish : images (topic-images/instagram) écrites (réelles)")


def append_journal_entry(date_str, h1):
    """Ajoute une ligne au « Journal des sujets publiés » de
    docs/sujets-a-suivre.md pour l'édition qui vient d'être publiée — la
    plus récente en tête. scripts/hebdo/generate_weekly_recap.py::week_editions()
    dépend entièrement de cette liste pour retrouver les éditions de la
    semaine.

    Reprend le rôle que jouait l'étape 6bis de l'ancienne routine
    interactive Claude Code (docs/routine-prompt.md), jamais portée dans
    la chaîne automatisée OpenRouter avant ce correctif — conséquence
    réelle constatée le 21 septembre 2026 : generate_weekly_recap.py ne
    trouvait plus aucune édition depuis le 14 septembre 2026, la liste
    s'étant arrêtée net au dernier jour où l'ancienne routine a tourné.

    Idempotent (n'ajoute rien si une ligne pour cette date existe déjà) et
    best-effort, jamais bloquant pour la publication elle-même : une
    section introuvable est un avertissement, pas un échec."""
    path = REPO_ROOT / "docs" / "sujets-a-suivre.md"
    text = path.read_text(encoding="utf-8")
    archive_rel = f"../archives/{date_str}.html"
    if archive_rel in text:
        print(f"[post-edition] sujets-a-suivre.md : entrée du {date_str} déjà présente dans le journal")
        return
    marker = "## Journal des sujets publiés"
    idx = text.find(marker)
    if idx == -1:
        print("[post-edition] sujets-a-suivre.md : section 'Journal des sujets publiés' introuvable "
              "— entrée non ajoutée (non bloquant)")
        return
    year, month, day = date_str.split("-")
    line = f"- {day}.{month}.{year} — [{h1}]({archive_rel})\n"
    # Insère juste avant la 1re ligne "- " déjà présente après le marqueur
    # (après le paragraphe d'intro) — la liste étant triée la plus récente
    # en tête, une nouvelle édition va toujours en haut.
    rest = text[idx:]
    m = re.search(r"^- ", rest, re.M)
    if m:
        insert_at = idx + m.start()
        new_text = text[:insert_at] + line + text[insert_at:]
    else:
        new_text = text.rstrip("\n") + "\n\n" + line
    path.write_text(new_text, encoding="utf-8")
    print(f"[post-edition] sujets-a-suivre.md : entrée journalisée pour {date_str}")


def check_off_priority_topic(brief):
    """Marque « publié » le sujet de la file consommé par l'édition du jour, dans
    `data/sujets.json` (source de vérité) puis régénère `sujets-prioritaires.md`
    (vue lisible) — jamais le bac à sable : ces fichiers n'ont pas d'équivalent
    dedans. Voir scripts/edition/sujets.py et docs/routine-brief-format.md
    § `sujet.origine_id`.

    Remplace l'ancienne consigne « cocher la case toi-même » de la routine
    interactive (`docs/routine-prompt.md` § Étape 0), devenue impossible à
    honorer depuis le 14 septembre 2026 : elle ne publie plus elle-même, elle
    s'arrête après avoir déclenché le pipeline, bien avant la publication réelle.

    Le sujet est retrouvé par son identifiant (`sujet.origine_id`, fiable) ; à
    défaut par le texte (`origine_prioritaire`, titre, h1), en tolérant la puce
    « - [ ] » et le tag final recopiés par erreur (« pop culture » le 26 septembre
    2026, jamais cochée) et un sujet repris de la file sans origine (« Bitcoin »
    le 1er octobre).

    Best-effort, jamais bloquant : introuvable, ou fichiers en conflit, donne un
    simple avertissement — le pire cas est un sujet à marquer à la main (le
    dashboard écarte de toute façon un sujet déjà publié), jamais une
    publication bloquée pour ça."""
    import sujets as sj

    data_path = REPO_ROOT / "data" / "sujets.json"
    md_path = REPO_ROOT / "sujets-prioritaires.md"
    if not data_path.exists():
        print("[post-edition] data/sujets.json introuvable — sujet non marqué (non bloquant)")
        return
    try:
        data, action = sj.load_synced(data_path, md_path)
    except sj.SujetsError as e:
        print(f"[post-edition] file de sujets non mise à jour (non bloquant) : {e}")
        return
    ids = sj.check_off(data, brief)
    if ids or action != "ok":
        sj.save_both(data, data_path, md_path)
    if ids:
        print(f"[post-edition] file de sujets : {len(ids)} sujet(s) marqué(s) publié(s) : {', '.join(ids)}")
    else:
        sujet = brief.get("sujet") or {}
        if sujet.get("origine_id") or sujet.get("origine_prioritaire"):
            print("[post-edition] file de sujets : sujet d'origine introuvable ou déjà publié — "
                  "rien à marquer (non bloquant, probablement reformulé/retiré à la main)")
        else:
            print("[post-edition] file de sujets : aucun sujet de la file ne correspond à cette édition")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, help="chemin du brief JSON (même fichier que la rédaction)")
    parser.add_argument("--content", default=None,
                         help="chemin du {date}.content.json produit par generate_daily_edition.py — "
                              "requis sauf avec --recheck-priority-only")
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
    parser.add_argument(
        "--recheck-priority-only", action="store_true",
        help="Ne fait QUE check_off_priority_topic() sur le VRAI sujets-prioritaires.md (jamais le "
             "bac à sable) puis s'arrête — aucun appel Pexels/OpenRouter, aucune écriture des autres "
             "fichiers réels. Sert à rejouer cette seule étape, bon marché et idempotente, dans une "
             "boucle de retry après un pull frais (voir .github/workflows/post-edition.yml) — jamais "
             "besoin de refaire tourner tout le pipeline coûteux juste pour cette case à cocher.",
    )
    parser.add_argument(
        "--slug", default=None,
        help="Publie une édition SUPPLÉMENTAIRE le même jour (chantier multi-éditions/jour, "
             "28 septembre 2026 — contributions de journalistes indépendants, en plus de l'édition IA "
             "quotidienne) plutôt que l'édition IA elle-même : archives/{date}-{slug}.html au lieu de "
             "archives/{date}.html nu. Minuscules/chiffres/tirets uniquement. Absent par défaut : "
             "comportement inchangé, publie toujours l'édition IA du jour (archives/{date}.html).",
    )
    args = parser.parse_args()

    brief = load_brief(args.brief)
    date_str = brief["date"]
    if args.slug:
        if not re.fullmatch(r"[a-z0-9-]+", args.slug):
            raise PostEditionError(f"--slug {args.slug!r} : minuscules/chiffres/tirets uniquement (voir build_html._ARCHIVE_DATE_RE)")
        edition_id = f"{date_str}-{args.slug}"
    else:
        edition_id = date_str
    print(f"[post-edition] brief chargé : {args.brief} (date {date_str}, edition_id {edition_id})")

    if args.recheck_priority_only:
        check_off_priority_topic(brief)
        return

    # already_published_today() vérifie toujours l'emplacement fixe de
    # l'édition IA (archives/{date}.html nu) — jamais celui d'une édition
    # à slug : deux éditions supplémentaires différentes le même jour ne
    # doivent jamais se bloquer l'une l'autre. Avec --slug, seule une
    # RÉPÉTITION du même edition_id est bloquée (rejouer exactement la
    # même commande par erreur), pas une nouvelle édition IA du jour.
    already = (
        (REPO_ROOT / "archives" / f"{edition_id}.html").exists() if args.slug
        else already_published_today(date_str)
    )
    if args.publish and already:
        print(f"[post-edition] --publish : archives/{edition_id}.html existe déjà — "
              "édition déjà publiée, on s'arrête proprement sans rien republier.")
        return

    if not args.content:
        raise PostEditionError("--content requis (sauf avec --recheck-priority-only)")
    content_path = Path(args.content)
    if not content_path.exists():
        raise PostEditionError(f"content.json introuvable : {content_path} — lancer generate_daily_edition.py d'abord")
    content = normalize_content_markdown(json.loads(content_path.read_text(encoding="utf-8")))

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
        # Priorité à la photo déjà choisie et validée en preview (voir
        # daily-preview.yml) — retélécharge EXACTEMENT cette même image
        # au lieu de relancer une recherche Pexels qui pourrait retourner
        # un candidat différent (incident du 21 septembre 2026).
        preview_credits_path = REPO_ROOT / "editorial-previews" / f"{date_str}.photo-credits.json"
        photo_from_preview = False
        if preview_credits_path.exists():
            preview_credits = json.loads(preview_credits_path.read_text(encoding="utf-8"))
            photo_credits = select_topic_photo_from_preview(preview_credits, edition_id, sandbox_root)
            photo_from_preview = photo_credits is not None
            if not photo_credits:
                print("[post-edition] échec de reprise de la photo du preview — repli sur une nouvelle recherche Pexels", file=sys.stderr)
                photo_credits = select_topic_photo(image_keywords, edition_id, sandbox_root)
        else:
            photo_credits = select_topic_photo(image_keywords, edition_id, sandbox_root)
        if photo_credits:
            origin = "reprise du preview déjà validé" if photo_from_preview else "nouvelle recherche Pexels"
            print(f"[post-edition] photo retenue ({origin}, requête « {photo_credits['query']} », {photo_credits['photographer']})")
        else:
            photo_credits = select_registry_fallback_photo(brief["registre"], edition_id, sandbox_root)
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

    # 2. HTML final (photo incluse) — DEUX copies distinctes, jamais
    # identiques : index.html (racine, liens tels quels) et
    # archives/{date}.html (un niveau plus bas, liens réajustés — voir
    # rebase_links_for_archive_copy() ci-dessus).
    index_html_path = REPO_ROOT / "index.html"
    shell = build_html.extract_shell(index_html_path.read_text(encoding="utf-8"))
    html_text, edition_number = build_html.assemble_index_html(shell, content, brief, date_str, photo=photo)

    # 2bis. SEO Head injection — remplace le <head> par un head optimisé
    # généré déterministiquement à partir du brief (title, og:*, twitter:*,
    # Schema.org BreadcrumbList/WebSite/NewsArticle/Organization).
    html_text = inject_seo_head(html_text, brief)
    print(f"[post-edition] <head> SEO optimisé injecté (title, og:*, twitter:*, Schema.org)")

    # GARDE-FOU final, juste avant écriture sur disque : dernier filet avant
    # que le HTML ne parte vers le bac à sable puis --publish (incident du
    # 26 septembre 2026 — voir inject_seo_head()). Attrape toute régression
    # future, peu importe l'étape du pipeline qui l'introduirait.
    if "<style" not in html_text or "</style>" not in html_text:
        raise PostEditionError(
            "❌ CRITIQUE : le HTML final (juste avant écriture) ne contient plus de <style> ! "
            "La page serait entièrement noire. Abandon immédiat, rien n'est écrit."
        )

    # La home est une page fixe de présentation (jamais le contenu d'un
    # article) : voir assemble_home_page() pour le motif SEO — conflit de
    # canonical home/archive détecté via Search Console le 27 septembre
    # 2026 (0 archive indexée alors que la home, elle, l'était). Une home
    # qui ne republie plus jamais le contenu d'un article élimine ce
    # conflit à la racine. L'archive seule garde le contenu intégral,
    # comme avant. today_entry : l'archive du jour n'existe pas encore
    # sur REPO_ROOT à ce stade (encore dans le bac à sable), donc
    # get_latest_archives() ne peut pas la trouver elle-même.
    today_image_path = sandbox_root / "assets" / "social" / "topic-images" / f"{edition_id}.jpg"
    today_entry = {
        "edition_id": edition_id,
        "date_str": date_str,
        "title": content["h1"],
        "image_url": (
            f"assets/social/topic-images/{edition_id}.jpg" if today_image_path.exists()
            else "assets/social/og-image-v2.png"
        ),
        # Même transformation que build_html.py (section_name, tête SEO de
        # l'archive) — jamais DOMAIN_LABELS ci-dessus : ce badge doit rester
        # identique à ce que get_latest_archives() relira demain depuis le
        # <meta property="article:section"> réellement écrit dans le
        # fichier, sinon le libellé changerait de forme du jour au
        # lendemain pour la même édition.
        "domain": brief["sujet"]["domain"].replace("-", " ").title(),
        # Même troncature que generate_seo_head._build_description() (la
        # meta description) — cohérence avec ce que build_archive_entry()
        # relira demain depuis le <meta name="description"> réellement
        # écrit dans le fichier.
        "question": generate_seo_head._truncate_at_word_boundary(brief["sujet"]["question_posee"], 160),
    }
    home_html = build_html.assemble_home_page(shell, date_str, edition_number, REPO_ROOT,
                                               today_entry=today_entry, theme_link_base="themes/")
    if "<style" not in home_html or "</style>" not in home_html:
        raise PostEditionError(
            "❌ CRITIQUE : le HTML de la home ne contient plus de <style> ! "
            "La page serait entièrement noire. Abandon immédiat, rien n'est écrit."
        )

    index_out = sandbox_root / "index.html"
    index_out.write_text(home_html, encoding="utf-8")
    archive_dir = sandbox_root / "archives"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{edition_id}.html"
    archive_path.write_text(rebase_links_for_archive_copy(html_text), encoding="utf-8")
    print(f"[post-edition] HTML final (édition N°{edition_number}) écrit : {index_out} (racine, résumé) et {archive_path} (archive, contenu complet, liens réajustés d'un niveau)")

    # 3. Image Instagram
    ig_image_path = generate_instagram_image(content, edition_id, sandbox_root, photo)
    ig_image_size = ig_image_path.stat().st_size
    ig_image_url = f"{SITE_URL}/assets/social/instagram/{edition_id}.png"
    print(f"[post-edition] image Instagram écrite : {ig_image_path} ({ig_image_size} octets)")

    # 4. feed.xml
    word_count = estimate_word_count(content)
    read_minutes = max(1, round(word_count / 200))
    feed_item = build_feed_item(content, edition_id, read_minutes, ig_image_url, ig_image_size)
    feed_text = (REPO_ROOT / "feed.xml").read_text(encoding="utf-8")
    new_feed_text = update_feed_xml(feed_text, feed_item)
    ET.fromstring(new_feed_text)  # valide la syntaxe XML avant écriture — échoue fort sinon
    feed_out = sandbox_root / "feed.xml"
    feed_out.write_text(new_feed_text, encoding="utf-8")
    print(f"[post-edition] feed.xml (avec nouvel item, {read_minutes} min de lecture) écrit : {feed_out}")

    # 4bis. glossaire.html — voir docs/routine-prompt.md, étape 6ter
    glossaire_text = (REPO_ROOT / "glossaire.html").read_text(encoding="utf-8")
    new_glossaire_text, added_terms = update_glossaire_html(glossaire_text, content, brief, edition_id)
    glossaire_out = sandbox_root / "glossaire.html"
    glossaire_out.write_text(new_glossaire_text, encoding="utf-8")
    if added_terms:
        print(f"[post-edition] glossaire.html : {len(added_terms)} nouveau(x) terme(s) ajouté(s) — {', '.join(added_terms)}")
    else:
        print("[post-edition] glossaire.html : aucun nouveau terme (tous déjà présents)")

    # 5. sitemap.xml / sitemap-news.xml
    sitemap_text = (REPO_ROOT / "sitemap.xml").read_text(encoding="utf-8")
    new_sitemap_text = update_sitemap_xml(sitemap_text, edition_id, bump_glossaire=bool(added_terms))
    ET.fromstring(new_sitemap_text)
    sitemap_out = sandbox_root / "sitemap.xml"
    sitemap_out.write_text(new_sitemap_text, encoding="utf-8")
    print(f"[post-edition] sitemap.xml écrit : {sitemap_out}")

    sitemap_news_text = (REPO_ROOT / "sitemap-news.xml").read_text(encoding="utf-8")
    new_sitemap_news_text = update_sitemap_news_xml(sitemap_news_text, edition_id, content["h1"])
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
    # edition_id (jamais date_str) : bug réel trouvé le 28 septembre 2026
    # en testant --slug — cette copie renommait TOUJOURS le fichier en
    # "{date_str}.html" nu, écrasant silencieusement dans le miroir la
    # copie de l'édition IA réelle du jour (déjà présente via le
    # copytree juste au-dessus) avec le contenu de l'édition à slug, sous
    # le nom de l'AUTRE édition. archives.html régénéré à partir de ce
    # miroir n'aurait alors jamais eu de ligne pour l'édition à slug, et
    # la ligne de l'édition IA aurait porté le titre de l'édition à slug.
    shutil.copy(archive_path, mirror_root / "archives" / f"{edition_id}.html")

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
        promote_to_real_repo(sandbox_root, edition_id)
        # date_str (jamais edition_id) : append_journal_entry() est
        # idempotent PAR JOUR (voir sa docstring) — une édition
        # supplémentaire du même jour (--slug) n'y ajoute donc pas sa
        # propre ligne pour l'instant, elle resterait absente du récap
        # hebdomadaire (generate_weekly_recap.py::week_editions() lit ce
        # même journal). Question ouverte, comme update_sources_log()
        # plus haut : faut-il une ligne par édition ou une ligne agrégée
        # par jour ? Pas tranché ici.
        append_journal_entry(date_str, content["h1"])
        # check_off_priority_topic() n'est PAS appelé ici : sujets-prioritaires.md
        # est volontairement exclu du commit de cette étape (voir
        # .github/workflows/post-edition.yml, étape "Committer et pousser") pour
        # éviter un conflit avec hot-topics.yml. L'appeler ici modifierait le
        # fichier réel sans le committer, laissant une modification non indexée
        # qui fait échouer le `git pull --rebase` juste après (incident du
        # 21 septembre 2026). La case est cochée uniquement par l'étape dédiée
        # du workflow (--recheck-priority-only), qui repart d'un fetch frais.
        print("[post-edition] --publish : fichiers réels écrits — commit/push restent à faire par le workflow appelant.")
    else:
        print("[post-edition] AUCUN commit, AUCUN push effectué — Phase 1 prototype (workflow_dispatch uniquement).")


if __name__ == "__main__":
    try:
        main()
    except PostEditionError as e:
        print(f"[post-edition] ERREUR : {e}", file=sys.stderr)
        sys.exit(1)
