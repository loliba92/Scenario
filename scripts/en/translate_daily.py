"""
Filet de sécurité pour l'étape 13 de docs/routine-prompt.md (traduction
anglaise de l'édition du jour) — voir l'incident du 11 septembre 2026
dans docs/ARCHITECTURE.md : un sous-agent borné par erreur à l'étape 12
a laissé `en/index.html` bloqué deux jours de suite.

Ce script fait la même chose sans passer par un agent : il appelle
directement l'API OpenRouter pour la traduction, ce qui le rend
indépendant de tout périmètre d'agent mal défini, et le sort entièrement
de la consommation de tokens du compte Claude Code (facturation
séparée, coût de l'ordre de 0,001-0,005 $ par édition avec le modèle
par défaut ci-dessous — voir le comparatif de prix dans la conversation
qui a précédé ce script).

Portée couverte : `en/index.html`, `en/archives/AAAA-MM-JJ.html`, la ligne
"EN" de l'entrée du jour dans `archives.html` (en relançant le script
existant `generate_archives_table.py`, qui vérifie déjà lui-même la
présence du fichier EN sur disque — zéro nouveau code pour ce point),
`sitemap.xml`, `sitemap-news.xml`, l'entrée du jour dans `en/feed.xml`.
Portée NON couverte, à faire séparément :
  - l'image sociale `en/assets/social/...` (nécessite Playwright, pas
    encore ajouté au workflow CI)
  - `en/feed-pub.xml` (posts pub, routine séparée)

Principe non négociable, repris de `docs/routine-en-prompt.md` : traduire,
jamais rerédiger. Le script ne fait que transformer le HTML déjà publié
de `index.html` — aucune recherche, aucun nouveau chiffre.

Garde-fou : si la structure HTML renvoyée par le modèle ne correspond
pas exactement à celle envoyée (balises, attributs, hrefs de glossaire),
le script s'arrête sans rien écrire. Mieux vaut sauter l'anglais du jour
qu'en publier une version cassée — même règle que la routine agent.

Idempotent : si `en/archives/AAAA-MM-JJ.html` existe déjà pour la date
du jour, le script ne fait rien (exit 0). Sans danger de le relancer à
chaque exécution du workflow CI.

Usage :
    export OPENROUTER_API_KEY=sk-or-v1-...
    python3 scripts/en/translate_daily.py [--dry-run] [--model deepseek/deepseek-v4-flash]
"""
import argparse
import copy
import glob
import json
import os
import re
import subprocess
import sys
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-v4-flash"

DAYS_FR_EN = {
    "lundi": "Monday", "mardi": "Tuesday", "mercredi": "Wednesday",
    "jeudi": "Thursday", "vendredi": "Friday", "samedi": "Saturday",
    "dimanche": "Sunday",
}


class TranslationError(Exception):
    pass


# ---------------------------------------------------------------------------
# Mémoire de traduction : construite à partir des paires d'archives FR/EN
# déjà publiées, pour les libellés courts qui reviennent d'une édition à
# l'autre (mot de jauge, étiquette de scénario, registre du bandeau).
# Pas de valeur codée en dur : si un libellé n'a jamais été vu, il part
# dans le lot envoyé au modèle comme le reste du contenu du jour.
# ---------------------------------------------------------------------------
def build_translation_memory(max_pairs=20):
    memory = {}
    fr_archives = sorted(glob.glob(str(REPO_ROOT / "archives" / "????-??-??.html")), reverse=True)
    for fr_path in fr_archives[:max_pairs]:
        date = Path(fr_path).stem
        en_path = REPO_ROOT / "en" / "archives" / f"{date}.html"
        if not en_path.exists():
            continue
        fr_soup = BeautifulSoup(open(fr_path, encoding="utf-8").read(), "html.parser")
        en_soup = BeautifulSoup(open(en_path, encoding="utf-8").read(), "html.parser")
        for selector in [".kind-tag", ".gauge-word"]:
            fr_vals = [e.get_text(strip=True) for e in fr_soup.select(selector)]
            en_vals = [e.get_text(strip=True) for e in en_soup.select(selector)]
            if len(fr_vals) == len(en_vals):
                for fr_v, en_v in zip(fr_vals, en_vals):
                    memory.setdefault(fr_v.lower(), Counter())[en_v] += 1
        fr_eyebrow = fr_soup.select_one(".eyebrow")
        en_eyebrow = en_soup.select_one(".eyebrow")
        if fr_eyebrow and en_eyebrow:
            fr_parts = [p.strip() for p in fr_eyebrow.get_text().split(",")]
            en_parts = [p.strip() for p in en_eyebrow.get_text().split(",")]
            if len(fr_parts) == 2 and len(en_parts) == 2:
                memory.setdefault(fr_parts[1].lower(), Counter())[en_parts[1]] += 1
    return {fr: counter.most_common(1)[0][0] for fr, counter in memory.items()}


# ---------------------------------------------------------------------------
# Extraction des segments à traduire
# ---------------------------------------------------------------------------
def inner_html(tag):
    html = "".join(str(c) for c in tag.contents)
    return rewrite_links_in_fragment(html)


def set_inner_html(tag, html):
    new = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(new.contents):
        tag.append(child)


def collect_segments(soup):
    """Renvoie les segments à traduire, avec les liens internes déjà
    réécrits pour l'arborescence en/ (voir rewrite_citation_link) : le
    modèle a pour consigne de préserver les href tels quels, donc ils
    doivent déjà être corrects avant l'envoi."""
    segments = {}

    title_tag = soup.select_one("title")
    if title_tag:
        segments["title"] = title_tag.string or ""

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        segments["meta_description"] = meta_desc.get("content", "")

    og_image_alt = soup.find("meta", property="og:image:alt")
    if og_image_alt:
        segments["og_image_alt"] = og_image_alt.get("content", "")

    h1 = soup.select_one("h1")
    if h1:
        segments["h1"] = inner_html(h1)

    qtext = soup.select_one(".question-text")
    if qtext:
        segments["question_text"] = inner_html(qtext)

    for i, dek in enumerate(soup.select(".dek")):
        segments[f"dek_{i}"] = inner_html(dek)

    for i, ind in enumerate(soup.select(".indicator")):
        label = ind.select_one(".label")
        value = ind.select_one(".value")
        if label:
            segments[f"indicator_{i}_label"] = inner_html(label)
        if value:
            segments[f"indicator_{i}_value"] = inner_html(value)

    for i, card in enumerate(soup.select(".card")):
        kind = card.get("data-kind", str(i))
        h3 = card.select_one("h3")
        if h3:
            segments[f"card_{kind}_h3"] = inner_html(h3)
        for j, why in enumerate(card.select(".why")):
            segments[f"card_{kind}_why_{j}"] = inner_html(why)

    for i, fl in enumerate(soup.select(".france-line")):
        clone = copy.copy(fl)
        label = clone.select_one(".field-label")
        if label:
            label.decompose()
        segments[f"france_line_{i}"] = inner_html(clone).strip()

    for dt in soup.select(".lexique dt"):
        slug = dt.get("id", "").replace("lex-", "")
        dd = dt.find_next_sibling("dd")
        segments[f"lex_{slug}_dt"] = inner_html(dt)
        if dd:
            segments[f"lex_{slug}_dd"] = inner_html(dd)

    return segments


def collect_feed_segments(date_str):
    """Segments propres à feed.xml, en plus de ceux de collect_segments.

    Beaucoup de champs de l'item feed.xml sont déjà traduits ailleurs
    (titre = h1, comments = question_text, category = titres des cartes)
    — inutile de les renvoyer au modèle une deuxième fois. Seuls les
    paragraphes de <source> qui n'existent nulle part ailleurs sur la
    page (accroche reformulée, faits, scénario le plus probable, signal
    à surveiller, évaluation France) sont de vrais nouveaux segments.

    Renvoie (segments, feed_item) ou (None, None) si feed.xml n'a pas
    encore d'entrée pour cette date (routine FR pas encore passée par
    son étape 8, ou item non trouvé) — dans ce cas l'appelant doit
    sauter la mise à jour du feed sans faire échouer tout le script."""
    feed_path = REPO_ROOT / "feed.xml"
    if not feed_path.exists():
        return None, None
    xml = feed_path.read_text(encoding="utf-8")

    item_match = re.search(r"<item>(.*?)</item>", xml, re.S)
    if not item_match or f"archives/{date_str}.html" not in item_match.group(1):
        return None, None
    item = item_match.group(1)

    def field(tag):
        m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", item, re.S)
        return m.group(1).strip() if m else None

    source_url_match = re.search(r'<source url="([^"]*)">(.*?)</source>', item, re.S)
    if not source_url_match:
        return None, None
    source_text = source_url_match.group(2).strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", source_text) if p.strip()]
    if len(paragraphs) != 5:
        # Format inattendu (routine FR modifiée depuis) — mieux vaut sauter
        # le feed que deviner un découpage faux.
        return None, None

    feed_item = {
        "pub_date": field("pubDate"),
        "enclosure_length": (re.search(r'length="(\d+)"', item) or [None, None])[1],
    }
    segments = {
        "feed_hook": paragraphs[0],
        "feed_facts": paragraphs[1],
        "feed_most_probable": paragraphs[2],
        "feed_signal": paragraphs[3],
        "feed_france_eval": paragraphs[4],
    }
    return segments, feed_item


# ---------------------------------------------------------------------------
# Appel OpenRouter
# ---------------------------------------------------------------------------
def call_openrouter(segments, model, api_key):
    ids = list(segments.keys())
    payload_in = [{"id": k, "html": segments[k]} for k in ids]

    prompt = f"""Tu traduis une édition d'actualité économique du français vers l'anglais,
pour le site Scénario (lesscenarios.fr).

Règles strictes :
- Traduction naturelle, jamais mot à mot ("Concrètement en France" ne se
  traduit pas littéralement, par exemple).
- Chaque segment est un fragment de HTML. Conserve EXACTEMENT les balises,
  attributs, classes, id et href (en particulier les liens
  class="lex-ref" href="#lex-..." qui pointent vers le petit lexique de
  l'article — ne change jamais ce href). Traduis uniquement le texte visible.
- Reformate les unités à l'anglaise si besoin (ex: "725 Md$" -> "$725B",
  "+77 % sur un an" -> "+77% year-on-year").
- Ne résume pas, ne raccourcis pas, n'ajoute aucun commentaire.
- Renvoie un objet JSON unique de la forme {{"translations": [{{"id": "...", "html": "..."}}, ...]}},
  avec exactement les mêmes id, dans le même ordre, un par segment reçu.

Segments à traduire (JSON) :
{json.dumps(payload_in, ensure_ascii=False)}
"""

    body = json.dumps({
        "model": model,
        "max_tokens": 8000,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        # deepseek-v4-flash est un modèle "raisonneur" : sans ce flag, il
        # consomme le budget de tokens en chaîne de pensée cachée avant
        # d'écrire la réponse (vérifié en test : 7912/8000 tokens de
        # "reasoning", contenu tronqué). Traduire ne demande pas de
        # raisonnement caché, donc on le désactive.
        "reasoning": {"enabled": False},
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(OPENROUTER_URL, method="POST", data=body, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())

    if "choices" not in data:
        raise TranslationError(f"réponse OpenRouter sans 'choices' : {data}")

    content = data["choices"][0]["message"]["content"]
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise TranslationError(f"réponse du modèle non-JSON : {e}\n{content[:500]}")

    out = {item["id"]: item["html"] for item in parsed.get("translations", [])}
    missing = set(ids) - set(out.keys())
    if missing:
        raise TranslationError(f"segments manquants dans la réponse : {missing}")

    return out, data.get("usage", {})


# ---------------------------------------------------------------------------
# Validation structurelle : la traduction ne doit pas casser le HTML.
# ---------------------------------------------------------------------------
def structural_signature(html):
    soup = BeautifulSoup(html, "html.parser")
    sig = []
    for tag in soup.find_all(True):
        attrs = tuple(sorted(
            (k, v) for k, v in tag.attrs.items() if k in ("class", "href", "id", "data-france-impact")
        ))
        sig.append((tag.name, attrs))
    return sig


def validate_translations(originals, translations):
    errors = []
    for seg_id, original_html in originals.items():
        translated_html = translations.get(seg_id, "")
        if structural_signature(original_html) != structural_signature(translated_html):
            errors.append(seg_id)
    return errors


# ---------------------------------------------------------------------------
# Rewriting des liens internes FR -> EN (règle générale + cas particuliers)
# ---------------------------------------------------------------------------
def rewrite_link(value):
    if not value or value.startswith(("#", "http://", "https://", "mailto:")):
        return value
    if value.startswith("en/"):
        return value[len("en/"):]
    return f"../{value}"


def rewrite_links_for_en(soup):
    for tag in soup.find_all(["a", "img", "link", "script"]):
        for attr in ("href", "src"):
            if tag.has_attr(attr):
                tag[attr] = rewrite_link(tag[attr])


def rewrite_citation_link(href):
    """Lien vers un article cité dans le texte (ex: 'archives/2026-09-08.html').
    Pointe vers le miroir EN de cet article s'il existe déjà, sinon vers
    l'original FR — jamais un lien mort. C'est la partie mécanique de la
    "cascade vers les articles cités" de docs/routine-en-prompt.md ; la
    décision éditoriale (faut-il ajouter une phrase de contexte) reste
    hors de portée de ce script."""
    m = re.match(r"^archives/(\d{4}-\d{2}-\d{2})\.html$", href)
    if not m:
        return rewrite_link(href)
    date = m.group(1)
    if (REPO_ROOT / "en" / "archives" / f"{date}.html").exists():
        return f"archives/{date}.html"
    return f"../archives/{date}.html"


def rewrite_links_in_fragment(html):
    frag = BeautifulSoup(html, "html.parser")
    for a in frag.find_all("a"):
        if a.has_attr("href"):
            a["href"] = rewrite_citation_link(a["href"])
    return "".join(str(c) for c in frag.contents)


# ---------------------------------------------------------------------------
# Construction de la page EN
# ---------------------------------------------------------------------------
def find_edition_date(soup):
    """Déduit la date de l'édition à traduire depuis index.html.

    Ne JAMAIS lire `.masthead-lang-btn` pour ça : d'après
    docs/routine-prompt.md (étape technique 2, § bouton de bascule de
    langue), ce bouton n'existe pas encore sur index.html au moment où
    ce script tourne — c'est justement cette étape 13 (dont ce script
    est le filet de sécurité) qui l'ajoute rétroactivement, une fois la
    traduction faite. Le lire ici créait une dépendance circulaire :
    le script échouait à chaque exécution du jour (incidents des 11 et
    12 septembre 2026), et ne se mettait à fonctionner qu'après un
    fallback manuel qui posait le bouton en avance. `<link
    rel="canonical">`, lui, pointe déjà vers l'archive du jour dès la
    publication FR (même sur index.html, voir étape 3bis) — source
    fiable et indépendante de ce bouton.
    """
    canonical = soup.find("link", rel="canonical")
    href = canonical.get("href") if canonical else None
    if not href:
        raise TranslationError("<link rel=\"canonical\"> introuvable dans index.html, impossible de déduire la date")
    m = re.search(r"archives/(\d{4}-\d{2}-\d{2})\.html", href)
    if not m:
        raise TranslationError(f"date introuvable dans canonical href={href!r}")
    return m.group(1)


def build_en_soup(fr_soup, date_str, translations, memory):
    soup = copy.copy(fr_soup)

    # D'abord le rewrite générique des liens de chrome statique (nav,
    # masthead, icônes, bannière hebdo...). Les overrides explicites
    # ci-dessous (canonical, OG, bouton de langue) s'appliquent APRÈS,
    # pour ne jamais être re-préfixés par erreur (ex: "../index.html"
    # qui deviendrait "../../index.html" si l'ordre était inversé).
    rewrite_links_for_en(soup)

    def tr(seg_id, fallback_original):
        return translations.get(seg_id, fallback_original)

    def mem_or_llm(text, seg_key):
        return memory.get(text.strip().lower(), translations.get(seg_key, text))

    # <title> / meta description
    if soup.title:
        soup.title.string = tr("title", soup.title.get_text())
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        meta_desc["content"] = tr("meta_description", meta_desc.get("content", ""))

    soup.html["lang"] = "en"

    en_archive_url = f"https://lesscenarios.fr/en/archives/{date_str}.html"
    en_image_url = f"https://lesscenarios.fr/en/assets/social/instagram/{date_str}.png"
    title_text = tr("title", soup.title.get_text() if soup.title else "")
    desc_text = tr("meta_description", meta_desc.get("content", "") if meta_desc else "")

    # hreflang : mêmes URLs absolues que côté FR (déjà correctes, rien à
    # changer). Le canonical, lui, doit pointer vers CETTE page (l'archive EN).
    canonical = soup.find("link", rel="canonical")
    if canonical:
        canonical["href"] = en_archive_url

    # Open Graph / Twitter Card : recopiés depuis title/meta_description déjà
    # traduits, sauf og:url (fixe, pointe vers la home EN — même convention
    # que le reste du site) et og:image/twitter:image (chemin EN, suppose que
    # l'image sociale EN a été régénérée séparément — voir portée non
    # couverte en haut de fichier).
    for prop, value in [
        ("og:locale", "en_US"),
        ("og:url", "https://lesscenarios.fr/en/"),
        ("og:title", title_text),
        ("og:description", desc_text),
        ("og:image", en_image_url),
    ]:
        tag = soup.find("meta", property=prop)
        if tag:
            tag["content"] = value
    og_image_alt = soup.find("meta", property="og:image:alt")
    if og_image_alt:
        og_image_alt["content"] = tr("og_image_alt", og_image_alt.get("content", ""))
    for name, value in [
        ("twitter:title", title_text),
        ("twitter:description", desc_text),
        ("twitter:image", en_image_url),
    ]:
        tag = soup.find("meta", attrs={"name": name})
        if tag:
            tag["content"] = value

    # eyebrow : "Jour, registre"
    eyebrow = soup.select_one(".eyebrow")
    if eyebrow:
        parts = [p.strip() for p in eyebrow.get_text().split(",", 1)]
        day_en = DAYS_FR_EN.get(parts[0].lower(), parts[0])
        register_en = mem_or_llm(parts[1], "eyebrow_register") if len(parts) > 1 else ""
        eyebrow.string = f"{day_en}, {register_en}" if register_en else day_en

    # ligne d'édition : "Édition du 11 septembre 2026 · N°50"
    edition_div = soup.select_one(".edition")
    if edition_div:
        m = re.search(r"N[°º]\s*(\d+)", edition_div.get_text())
        num = m.group(1) if m else "?"
        y, mo, d = date_str.split("-")
        import calendar
        month_en = calendar.month_name[int(mo)]
        edition_div.string = f"Edition of {month_en} {int(d)}, {y} · No. {num}"

    # bouton de langue : pointe vers la page FR du jour
    lang_btn = soup.select_one(".masthead-lang-btn")
    if lang_btn:
        lang_btn["href"] = "../index.html"
        lang_btn["aria-label"] = "Lire en français"
        lang_btn["title"] = "Lire en français"
        lang_btn.string = "FR"

    h1 = soup.select_one("h1")
    if h1:
        set_inner_html(h1, tr("h1", inner_html(h1)))

    qtext = soup.select_one(".question-text")
    if qtext:
        set_inner_html(qtext, tr("question_text", inner_html(qtext)))

    for i, dek in enumerate(soup.select(".dek")):
        set_inner_html(dek, tr(f"dek_{i}", inner_html(dek)))

    for i, ind in enumerate(soup.select(".indicator")):
        label = ind.select_one(".label")
        value = ind.select_one(".value")
        if label:
            set_inner_html(label, tr(f"indicator_{i}_label", inner_html(label)))
        if value:
            set_inner_html(value, tr(f"indicator_{i}_value", inner_html(value)))

    for card in soup.select(".card"):
        kind = card.get("data-kind", "")
        kind_tag = card.select_one(".kind-tag")
        if kind_tag:
            kind_tag.string = mem_or_llm(kind_tag.get_text(), f"card_{kind}_kind_tag")
        gauge_word = card.select_one(".gauge-word")
        if gauge_word:
            gauge_word.string = mem_or_llm(gauge_word.get_text(), f"card_{kind}_gauge_word")
        h3 = card.select_one("h3")
        if h3:
            set_inner_html(h3, tr(f"card_{kind}_h3", inner_html(h3)))
        for j, why in enumerate(card.select(".why")):
            set_inner_html(why, tr(f"card_{kind}_why_{j}", inner_html(why)))

    for i, fl in enumerate(soup.select(".france-line")):
        label = fl.select_one(".field-label")
        label_text = label.get_text() if label else "Concrètement en France"
        translated_body = tr(f"france_line_{i}", "")
        fl.clear()
        new_label = soup.new_tag("span", **{"class": "field-label"})
        new_label.string = "The France angle"
        fl.append(new_label)
        fl.append(BeautifulSoup(translated_body, "html.parser"))

    for dt in soup.select(".lexique dt"):
        slug = dt.get("id", "").replace("lex-", "")
        dd = dt.find_next_sibling("dd")
        set_inner_html(dt, tr(f"lex_{slug}_dt", inner_html(dt)))
        if dd:
            set_inner_html(dd, tr(f"lex_{slug}_dd", inner_html(dd)))

    return soup


# ---------------------------------------------------------------------------
# sitemap.xml / sitemap-news.xml : entrées mécaniques, pas de traduction
# (voir docs/routine-prompt.md étape 7 / docs/routine-en-prompt.md étape
# 6ter pour le format de référence, recopié ici).
# ---------------------------------------------------------------------------
def update_sitemap(date_str):
    path = REPO_ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")

    if f"en/archives/{date_str}.html" in xml:
        return  # déjà fait (script relancé sur une exécution déjà passée ici)

    # <lastmod> de la home EN
    xml, n = re.subn(
        r"(<loc>https://lesscenarios\.fr/en/</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)",
        rf"\g<1>{date_str}\g<2>",
        xml,
    )
    if n != 1:
        raise TranslationError("sitemap.xml : bloc <loc>.../en/</loc> introuvable ou dupliqué")

    new_entry = (
        f"  <url>\n"
        f"    <loc>https://lesscenarios.fr/en/archives/{date_str}.html</loc>\n"
        f"    <lastmod>{date_str}</lastmod>\n"
        f"    <changefreq>never</changefreq>\n"
        f"    <priority>0.6</priority>\n"
        f"  </url>\n"
    )
    # Insérée juste après le bloc de la home EN, avant l'archive EN la plus
    # récente précédente — même ordre reverse-chronologique que le reste
    # du fichier.
    marker = re.search(
        r"<loc>https://lesscenarios\.fr/en/</loc>.*?</url>\n", xml, re.S
    )
    xml = xml[:marker.end()] + new_entry + xml[marker.end():]
    path.write_text(xml, encoding="utf-8")


def get_fr_publication_date_iso(date_str):
    """Lit sitemap-news.xml pour récupérer l'heure de publication ISO 8601
    déjà posée par la routine FR (étape 7bis) sur l'entrée du jour — pas la
    même mise en forme que <pubDate> dans feed.xml (RFC 822), donc pas
    réutilisable telle quelle : on la relit à sa propre source plutôt que
    de la reconvertir à la main, source d'erreurs de fuseau."""
    xml = (REPO_ROOT / "sitemap-news.xml").read_text(encoding="utf-8")
    m = re.search(
        rf"<loc>https://lesscenarios\.fr/archives/{re.escape(date_str)}\.html</loc>.*?"
        rf"<news:publication_date>([^<]+)</news:publication_date>",
        xml, re.S,
    )
    if not m:
        raise TranslationError(f"sitemap-news.xml : entrée fr introuvable pour {date_str}")
    return m.group(1)


def update_sitemap_news(date_str, title_en, pub_date):
    path = REPO_ROOT / "sitemap-news.xml"
    xml = path.read_text(encoding="utf-8")

    if f"en/archives/{date_str}.html" in xml:
        return

    new_entry = (
        f"  <url>\n"
        f"    <loc>https://lesscenarios.fr/en/archives/{date_str}.html</loc>\n"
        f"    <news:news>\n"
        f"      <news:publication>\n"
        f"        <news:name>Scénario</news:name>\n"
        f"        <news:language>en</news:language>\n"
        f"      </news:publication>\n"
        f"      <news:publication_date>{pub_date}</news:publication_date>\n"
        f"      <news:title>{html_escape(title_en)}</news:title>\n"
        f"    </news:news>\n"
        f"  </url>\n"
    )
    xml = xml.replace("</urlset>", new_entry + "</urlset>")

    # Purge : le protocole Google News n'accepte que les articles des
    # dernières 48h, quelle que soit la langue — voir docs/routine-prompt.md
    # étape 7bis. La routine FR ne purge que ses propres entrées fr ; cette
    # étape purge tout le fichier pour ne pas dépendre de l'ordre des deux.
    import datetime
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=48)

    def keep(match):
        pub = match.group(1)
        try:
            dt = datetime.datetime.fromisoformat(pub)
        except ValueError:
            return match.group(0)  # format inattendu, ne pas purger à l'aveugle
        return match.group(0) if dt >= cutoff else ""

    xml = re.sub(
        r"  <url>\s*<loc>.*?</loc>\s*<news:news>.*?<news:publication_date>([^<]+)</news:publication_date>.*?</news:news>\s*</url>\n",
        keep,
        xml,
        flags=re.S,
    )
    path.write_text(xml, encoding="utf-8")


def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------------------------------------------------------------------------
# en/feed.xml : nouvel <item> construit à partir des segments déjà traduits
# (titre, comments, titres de cartes) + des 5 nouveaux segments propres au
# feed (collect_feed_segments). Jamais de suppression d'item existant.
# ---------------------------------------------------------------------------
def build_en_feed_item(date_str, translations, feed_item):
    en_url = f"https://lesscenarios.fr/en/archives/{date_str}.html"
    en_image = f"https://lesscenarios.fr/en/assets/social/instagram/{date_str}.png"
    title = translations.get("h1", "")
    comments = translations.get("question_text", "")

    cat_order = [("favorable", "🟢"), ("stable", "🔵"), ("degrade", "🔴")]
    category_parts = []
    for kind, emoji in cat_order:
        h3 = translations.get(f"card_{kind}_h3")
        if h3:
            category_parts.append(f'{emoji} {h3}')
    category = '","'.join(category_parts)

    # Longueur d'enclosure inconnue tant que l'image sociale EN n'existe
    # pas (portée non couverte par ce script, voir en-tête du fichier) —
    # 0 plutôt qu'une valeur inventée, à corriger quand l'image sera générée.
    length = feed_item.get("enclosure_length") or "0"

    description = (
        f'<img src="{en_image}" alt="{html_escape(title)}" '
        f'style="max-width:100%;width:100%;height:auto;"><br><br>'
        f'The question: {translations.get("question_text", "")}<br><br>'
        f'The facts: {translations.get("feed_facts", "")}<br><br>'
        f'The 3 scenarios:<br>' + '<br>'.join(category_parts) + '<br><br>'
        f'Which one is most likely? 👉 <a href="{en_url}">Read the 3 numbered forecasts on the site</a> — it\'s free (~8 min read).<br><br>'
        f'Want to vote before you know the real probabilities? Join the Telegram channel: <a href="https://t.me/scenario_fr">t.me/scenario_fr</a><br><br>'
        f'A question, a comment? Just reply to this email, we read it.'
    )

    source_paragraphs = [
        translations.get("feed_hook", ""),
        translations.get("feed_facts", ""),
        translations.get("feed_most_probable", ""),
        translations.get("feed_signal", ""),
        translations.get("feed_france_eval", ""),
    ]
    source_text = "\n\n".join(source_paragraphs)

    return (
        f"    <item>\n"
        f"      <title>{html_escape(title)}</title>\n"
        f"      <link>{en_url}</link>\n"
        f"      <guid isPermaLink=\"false\">scenario-en-{date_str}</guid>\n"
        f"      <pubDate>{feed_item['pub_date']}</pubDate>\n"
        f"      <comments>{html_escape(comments)}</comments>\n"
        f"      <category>{category}</category>\n"
        f'      <enclosure url="{en_image}" length="{length}" type="image/png"/>\n'
        f"      <description><![CDATA[{description}]]></description>\n"
        f'      <source url="{en_url}">{source_text}</source>\n'
        f"    </item>\n"
    )


def prepend_feed_item(item_xml):
    path = REPO_ROOT / "en" / "feed.xml"
    xml = path.read_text(encoding="utf-8")
    marker = "<language>en</language>\n"
    if marker not in xml:
        raise TranslationError("en/feed.xml : balise <language>en</language> introuvable")
    xml = xml.replace(marker, marker + item_xml, 1)
    path.write_text(xml, encoding="utf-8")


# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="ne rien écrire, juste rapporter")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY manquant dans l'environnement.", file=sys.stderr)
        return 1

    fr_path = REPO_ROOT / "index.html"
    fr_soup = BeautifulSoup(fr_path.read_text(encoding="utf-8"), "html.parser")

    date_str = find_edition_date(fr_soup)
    en_archive_path = REPO_ROOT / "en" / "archives" / f"{date_str}.html"

    if en_archive_path.exists():
        print(f"en/archives/{date_str}.html existe déjà — rien à faire.")
        return 0

    print(f"Édition du {date_str} pas encore traduite. Traduction via {args.model}...")

    memory = build_translation_memory()
    segments = collect_segments(fr_soup)

    feed_segments, feed_item = collect_feed_segments(date_str)
    if feed_segments:
        segments.update(feed_segments)
    else:
        print("feed.xml : entrée du jour introuvable ou format inattendu — "
              "en/feed.xml ne sera pas mis à jour cette fois.")

    print(f"{len(segments)} segments à traduire.")

    translations, usage = call_openrouter(segments, args.model, api_key)

    errors = validate_translations(segments, translations)
    if errors:
        print("Validation structurelle échouée sur :", errors, file=sys.stderr)
        print("Rien n'est écrit — sauter l'anglais du jour plutôt que publier une version cassée.", file=sys.stderr)
        return 1

    print(f"Traduction validée. Coût de l'appel : {usage.get('cost', '?')} $ "
          f"({usage.get('total_tokens', '?')} tokens).")

    en_soup = build_en_soup(fr_soup, date_str, translations, memory)
    output_html = str(en_soup)

    if args.dry_run:
        print("--dry-run : rien écrit sur disque.")
        print(output_html[:2000])
        return 0

    en_archive_path.parent.mkdir(parents=True, exist_ok=True)
    en_archive_path.write_text(output_html, encoding="utf-8")
    (REPO_ROOT / "en" / "index.html").write_text(output_html, encoding="utf-8")
    print(f"Écrit : en/index.html et en/archives/{date_str}.html")

    # Badge EN dans archives.html : le script existant vérifie déjà lui-même
    # la présence de en/archives/{date}.html sur disque (bug corrigé le 1er
    # septembre 2026, voir le script) — le relancer suffit, aucun nouveau
    # code de notre côté.
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "seo" / "generate_archives_table.py")],
        cwd=REPO_ROOT, check=True,
    )
    print("archives.html régénéré (badge EN inclus).")

    update_sitemap(date_str)
    pub_date_iso = get_fr_publication_date_iso(date_str)
    update_sitemap_news(date_str, translations.get("h1", ""), pub_date_iso)
    print("sitemap.xml et sitemap-news.xml mis à jour.")

    if feed_segments:
        item_xml = build_en_feed_item(date_str, translations, feed_item)
        prepend_feed_item(item_xml)
        print("en/feed.xml mis à jour.")

    print("Reste à faire séparément (pas de traduction, hors de portée de ce "
          "script) : image sociale en/assets/social/ (Playwright, pas encore "
          "dans le workflow CI).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
