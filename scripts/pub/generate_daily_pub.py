#!/usr/bin/env python3
"""
Génère le post « pub » du jour (manifeste/citation/question, ou chiffre
extrait d'une édition déjà publiée) et son miroir anglais — remplace la
routine Claude Code quotidienne « Scénario — Pub hebdo »
(docs/routine-pub-prompt.md), tâche jugée à 95% mécanique par le prompt
lui-même ("le choix de la catégorie, de l'entrée et de la photo est
entièrement déterministe... ne pas réfléchir dessus" — voir ce fichier,
en-tête) — seule l'extraction du chiffre du jour (catégorie `chiffre`,
5 jours/7 dans la table de rotation actuelle) demande un vrai jugement
éditorial (quelle est l'info la plus importante d'une édition, pas
seulement le chiffre le plus spectaculaire), déléguée à un seul appel
OpenRouter ciblé — jamais une recherche web, jamais un fait inventé (le
message retenu est vérifié verbatim contre le texte source avant d'être
utilisé, voir extract_chiffre()).

Principe non négociable, repris de docs/pub-messages.md : cette routine
pioche dans une liste déjà curée à la main, elle n'invente jamais un
message ni une citation elle-même. Pour `chiffre`, le chiffre et sa
phrase viennent toujours mot pour mot d'une édition déjà publiée et donc
déjà vérifiée par le processus éditorial normal.

**Catégories `futur` (recherche web nécessaire) et `soutien`/`buy me a
coffee` fusionné dans `manifeste` : hors de portée de ce script.**
`futur` est de toute façon dormante dans la table de rotation actuelle
(docs/routine-pub-prompt.md, étape 1, point 2) — si elle est un jour
réactivée sans mécanisme de recherche automatisé, ce script doit
s'arrêter proprement (voir main()) plutôt que de deviner.

**IMPORTANT — conséquence réelle d'une exécution.** `feed-pub.xml` est
lu par un scénario Make.com qui poste automatiquement le nouvel item sur
Telegram/X/LinkedIn/Facebook/Instagram (voir docs/ARCHITECTURE.md). Ce
script n'est PAS branché sur un GitHub Action à ce stade précisément
pour cette raison — contrairement aux autres scripts mécaniques du
dépôt (reads.yml, audience.yml), une exécution ratée ici ne se contente
pas de mal afficher une page interne, elle publie un vrai post public.
Tant qu'il n'a pas été validé en conditions réelles avec l'accord
explicite de l'utilisateur, l'exécuter seulement à la main, jamais via
un cron automatique.

Usage :
    python3 scripts/pub/generate_daily_pub.py --dry-run
    OPENROUTER_API_KEY=xxx python3 scripts/pub/generate_daily_pub.py
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
PUB_MESSAGES = ROOT / "docs" / "pub-messages.md"
FEED_PUB = ROOT / "feed-pub.xml"
EN_FEED_PUB = ROOT / "en" / "feed-pub.xml"
ARCHIVES_DIR = ROOT / "archives"
PARIS = ZoneInfo("Europe/Paris")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-v4-flash"

# Table de rotation — SOURCE UNIQUE : docs/routine-pub-prompt.md, étape 1,
# point 2. Si cette table change là-bas, la reporter ici (docs/pub-
# messages.md § « Règle de rotation » a une copie qui a déjà dérivé une
# fois, ne jamais s'y fier comme référence).
DAY_TO_CATEGORY = {
    6: "manifeste",  # dimanche (Python: lundi=0 .. dimanche=6)
    0: "chiffre",    # lundi
    1: "chiffre",    # mardi
    2: "chiffre",    # mercredi
    3: "chiffre",    # jeudi
    4: "manifeste",  # vendredi
    5: "chiffre",    # samedi
}

# Jour -> registre de l'édition quotidienne (docs/routine-prompt.md,
# étape 1) -> slug de la photo de secours (assets/social/pub-photos/).
DAY_TO_REGISTRE_SLUG = {
    0: "geopolitique",
    1: "carte-blanche",
    2: "actualite-francaise",
    3: "economie-mondiale",
    4: "sciences",
    5: "culture",
    6: "sport",
}

CATEGORY_LINK = {
    "manifeste": "https://lesscenarios.fr/le-projet.html",
    "citation": "https://lesscenarios.fr/",
    "futur": "https://lesscenarios.fr/",
    "question": "https://lesscenarios.fr/contact.html",
    # "chiffre" n'a pas de lien fixe : toujours l'URL de l'édition source.
}

CATEGORY_TEMPLATE = {
    "manifeste": "pub-template-v4-hybride.html",
    "citation": "pub-template-v4-hybride.html",
    "question": "pub-template-v4-hybride.html",
    "chiffre": "pub-template-v5-stat.html",
}


class PubError(Exception):
    pass


# ---------------------------------------------------------------------------
# docs/pub-messages.md : entrées curées à la main, section par catégorie.
# ---------------------------------------------------------------------------
SECTION_HEADINGS = {
    "manifeste": "1. Manifeste — pourquoi Scénario (rotation A)",
    "citation": "2. Citations — le hasard et l'incertitude (rotation B)",
    "question": "3. Questions à la communauté (rotation C)",
    "futur": "4. Grands futurs — inventions et grands risques du siècle (rotation D)",
    "chiffre": "5. Le saviez-vous — un chiffre qui marque (rotation E)",
}

RETIRED_MARKER_RE = re.compile(r"`\[(retiré|déplacé|repliée)[^`]*\]`")
UNVALIDATED_MARKERS = ("[à confirmer]", "[attribution à vérifier]", "[à vérifier]")


def parse_pub_messages_section(md_text, category):
    """Renvoie la liste ordonnée des entrées valides (ni retirées, ni
    marquées non validées) d'une section, chacune {"id", fields...}."""
    heading = SECTION_HEADINGS[category]
    pattern = re.compile(
        r"^## " + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", re.M | re.S,
    )
    m = pattern.search(md_text)
    if not m:
        raise PubError(f"section introuvable dans pub-messages.md : {heading!r}")
    body = m.group(1)

    entries = []
    for entry_m in re.finditer(r"^### (\S+)([^\n]*)\n(.*?)(?=^### |\Z)", body, re.M | re.S):
        entry_id, header_rest, entry_body = entry_m.group(1), entry_m.group(2), entry_m.group(3)
        if RETIRED_MARKER_RE.search(header_rest):
            continue
        if any(marker in entry_body for marker in UNVALIDATED_MARKERS):
            continue
        fields = {}
        for field_m in re.finditer(r"^- ([a-z-]+):\s*(.+)$", entry_body, re.M):
            fields[field_m.group(1)] = field_m.group(2).strip()
        if "eyebrow" not in fields or "message" not in fields:
            continue  # entrée sans contenu structuré (note libre isolée)
        entries.append({"id": entry_id, **fields})
    return entries


def append_chiffre_entry(md_text, entry_id, fields, note):
    """Ajoute une entrée à la fin de la section 5 (journal des chiffres
    déjà utilisés) — jamais réordonné, jamais une entrée existante
    modifiée."""
    heading = SECTION_HEADINGS["chiffre"]
    pattern = re.compile(
        r"(^## " + re.escape(heading) + r"\s*$.*?)(\n(?=^## )|\Z)", re.M | re.S,
    )
    m = pattern.search(md_text)
    if not m:
        raise PubError("section chiffre introuvable pour y journaliser la nouvelle entrée")

    lines = [f"\n### {entry_id}"]
    for key in ("eyebrow", "stat", "message", "attribution", "cta", "source"):
        if fields.get(key):
            lines.append(f"- {key}: {fields[key]}")
    lines.append("")
    lines.append(note)
    lines.append("")
    block = "\n".join(lines)

    insertion_point = m.end(1)
    return md_text[:insertion_point] + block + md_text[insertion_point:]


# ---------------------------------------------------------------------------
# feed-pub.xml : état de la rotation (dernier guid par catégorie) et
# éditions déjà utilisées comme source d'un post `chiffre`.
# ---------------------------------------------------------------------------
def parse_feed_items(xml_text):
    """Renvoie les items dans l'ordre du fichier (le plus récent en
    premier, jamais réordonné) : [{"guid", "category", "entry_id", "link"}]."""
    items = []
    for item_xml in re.findall(r"<item>(.*?)</item>", xml_text, re.S):
        guid_m = re.search(r"<guid[^>]*>([^<]+)</guid>", item_xml)
        link_m = re.search(r"<link>([^<]*)</link>", item_xml)
        if not guid_m:
            continue
        guid = guid_m.group(1)
        cat_m = re.match(r"^scenario-pub-([a-z]+)-", guid)
        if not cat_m:
            continue
        category = cat_m.group(1)
        entry_id = re.sub(r"^scenario-pub-", "", guid)
        entry_id = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", entry_id)
        items.append({
            "guid": guid, "category": category, "entry_id": entry_id,
            "link": link_m.group(1) if link_m else "",
        })
    return items


def pick_rotation_entry(category, valid_entries, feed_items):
    """Entrée suivante dans l'ordre de la section, après la dernière
    publiée dans cette catégorie — retour au début si c'était la
    dernière ; la première de la liste si la catégorie n'a jamais été
    publiée. Voir docs/routine-pub-prompt.md, étape 1, points 3-4."""
    if not valid_entries:
        return None
    ids = [e["id"] for e in valid_entries]
    last_id = next((it["entry_id"] for it in feed_items if it["category"] == category), None)
    if last_id not in ids:
        return valid_entries[0]
    next_index = (ids.index(last_id) + 1) % len(ids)
    return valid_entries[next_index]


def used_chiffre_sources(feed_items):
    """Dates d'édition déjà citées comme source d'un post `chiffre` —
    déduites du <link> (toujours l'URL de l'édition source pour cette
    catégorie, voir docs/routine-pub-prompt.md étape 4)."""
    sources = set()
    for it in feed_items:
        if it["category"] != "chiffre":
            continue
        m = re.search(r"archives/(\d{4}-\d{2}-\d{2})\.html", it["link"])
        if m:
            sources.add(m.group(1))
    return sources


# ---------------------------------------------------------------------------
# Catégorie `chiffre` : candidats extraits d'une édition déjà publiée,
# jamais inventés — voir docstring du module.
# ---------------------------------------------------------------------------
def eligible_chiffre_dates(today, already_used, min_age_hours=24, window_days=30):
    dates = []
    for f in sorted(ARCHIVES_DIR.glob("????-??-??.html"), reverse=True):
        try:
            d = date.fromisoformat(f.stem)
        except ValueError:
            continue
        if d in already_used or (today - d).days > window_days:
            continue
        age_hours = (datetime.now(PARIS) - datetime(d.year, d.month, d.day, 7, 0, tzinfo=PARIS)).total_seconds() / 3600
        if age_hours < min_age_hours:
            continue
        dates.append(d)
    return dates  # déjà du plus récent au plus ancien (glob trié inversé)


def extract_strong_number_sentences(html_text):
    """Repère, dans .dek et .essentiel-text, les phrases contenant un
    <strong> autour d'un chiffre (%, montant, nombre, date marquante) —
    candidats bruts pour la catégorie chiffre, jamais un texte recomposé."""
    candidates = []
    for block_m in re.finditer(
        r'<p class="(?:dek|essentiel-text)">(.*?)</p>', html_text, re.S,
    ):
        block_html = block_m.group(1)
        if not re.search(r"<strong>[^<]*\d[^<]*</strong>", block_html):
            continue
        plain = re.sub(r"<[^>]+>", "", block_html)
        plain = html.unescape(plain).strip()
        if plain:
            candidates.append(plain)
    return candidates


def call_openrouter_json(prompt, model, api_key, timeout=90):
    body = json.dumps({
        "model": model,
        "max_tokens": 1500,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "reasoning": {"enabled": False},
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(OPENROUTER_URL, method="POST", data=body, headers={
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    if "choices" not in data:
        raise PubError(f"réponse OpenRouter sans 'choices' : {data}")
    content = data["choices"][0]["message"]["content"]
    return json.loads(content), data.get("usage", {})


def extract_chiffre(source_date, model, api_key):
    """Choisit, dans l'édition `source_date`, la phrase à chiffre la plus
    importante (pas la plus spectaculaire) et la formate — voir
    docs/routine-pub-prompt.md étape 1 point 7, docs/pub-messages.md § 5.
    Garde-fou non négociable : le message renvoyé doit être un passage
    VERBATIM du texte source (segment continu, jamais recomposé) — vérifié
    après coup, jamais fait confiance au modèle sur ce point précis."""
    archive_path = ARCHIVES_DIR / f"{source_date.isoformat()}.html"
    html_text = archive_path.read_text(encoding="utf-8")
    candidates = extract_strong_number_sentences(html_text)
    if not candidates:
        return None

    title_m = re.search(r"<h1>(.*?)</h1>", html_text, re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", title_m.group(1))) if title_m else ""

    prompt = f"""Tu choisis LE chiffre le plus important d'une édition déjà publiée, pour un
post promotionnel court ("Le saviez-vous").

Titre de l'édition : {title}

Règles strictes :
- Choisis le passage qui porte L'INFORMATION LA PLUS IMPORTANTE de
  l'édition — pas forcément le chiffre le plus spectaculaire. Demande-toi :
  qu'est-ce qu'un lecteur qui n'a lu QUE le titre retiendrait comme message
  principal ?
- Le "message" renvoyé doit être un EXTRAIT LITTÉRAL d'UN SEUL candidat
  ci-dessous (ou de 2-3 phrases CONTIGUËS du même paragraphe) — jamais
  recomposé, jamais reformulé, jamais un mot changé, ajouté ou retiré.
  Tu peux seulement raccourcir en coupant à une frontière naturelle
  (virgule, point-virgule, point) si le passage est trop long.
- Reste sous ~280 caractères au total.
- Vigilance sur les chiffres datés : si un candidat porte un millésime
  passé ("en 2024") ET qu'un autre candidat exprime un point tout aussi
  central sans ce problème, préfère ce dernier. Mais ne sacrifie jamais
  l'exactitude/la pertinence du point clé pour éviter une date.
- "stat" = uniquement le chiffre lui-même (ex. "41,9" ou "725 Md$"),
  extrait tel quel du message, sans unité si le gabarit l'affiche déjà
  séparément (garde l'unité si elle fait partie du sens, ex. "3,1x").
- Si aucun candidat ne convient vraiment (tous secondaires/anecdotiques),
  renvoie {{"ok": false}}.

Candidats (phrases contenant un chiffre en évidence dans l'édition) :
{json.dumps(candidates, ensure_ascii=False, indent=2)}

Renvoie un JSON unique : {{"ok": true, "stat": "...", "message": "..."}}
ou {{"ok": false}}.
"""
    result, usage = call_openrouter_json(prompt, model, api_key)
    if not result.get("ok"):
        return None

    message = result.get("message", "").strip()
    stat = result.get("stat", "").strip()
    if not message or not stat:
        return None

    # Garde-fou anti-invention : le message doit être un sous-segment
    # quasi-littéral du texte source (tolère la ponctuation de coupure
    # ajoutée en fin de segment, jamais un mot substitué au milieu).
    plain_source = " ".join(candidates)
    normalize = lambda s: re.sub(r"\s+", " ", s).strip().rstrip(".,;:")
    if normalize(message) not in normalize(plain_source):
        raise PubError(
            f"extract_chiffre : le message renvoyé n'est pas un extrait littéral du texte source "
            f"— rejeté plutôt que publié. message={message!r}"
        )

    months_fr = ["janvier", "février", "mars", "avril", "mai", "juin",
                 "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    attribution = f"— lesscenarios.fr, {source_date.day} {months_fr[source_date.month - 1]} {source_date.year}"

    return {
        "eyebrow": "LE SAVIEZ-VOUS",
        "stat": stat,
        "message": message,
        "attribution": attribution,
        "cta": "👉 Abonne-toi, un chiffre qui marque chaque jour",
        "source": f"https://lesscenarios.fr/archives/{source_date.isoformat()}.html",
    }, usage


# ---------------------------------------------------------------------------
# Photo — jamais de recherche Pexels en direct ici, uniquement des photos
# déjà validées par un humain (voir docs/routine-pub-prompt.md, étape 2).
# ---------------------------------------------------------------------------
def pick_photo(category, weekday, chiffre_source_date=None):
    """Renvoie (chemin_jpg, photographer, pexels_url)."""
    if category == "chiffre" and chiffre_source_date:
        img = ROOT / "assets" / "social" / "topic-images" / f"{chiffre_source_date.isoformat()}.jpg"
        meta_path = img.with_suffix(".json")
        if img.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            return img, meta.get("photographer", ""), meta.get("pexels_url", "")
        raise PubError(f"pick_photo : image/JSON manquants pour l'édition source {chiffre_source_date}")

    # manifeste/citation/question/futur : image récente déjà validée, en
    # préférant celle qui n'a pas déjà servi à un post feed-pub.xml récent
    # (voir docs/routine-pub-prompt.md, étape 2, point 1) — déduit des
    # commentaires <!-- credit: {photographer} — {pexels_url} --> déjà
    # présents dans le flux, pas d'un champ dédié.
    recent_pexels_urls = set()
    if FEED_PUB.exists():
        recent_xml = FEED_PUB.read_text(encoding="utf-8")
        recent_pexels_urls = set(re.findall(r"<!-- credit: [^—]+ — ([^\s]+) -->", recent_xml)[:14])

    today = datetime.now(PARIS).date()
    fallback = None
    for delta in range(7):
        d = today - timedelta(days=delta)
        img = ROOT / "assets" / "social" / "topic-images" / f"{d.isoformat()}.jpg"
        meta_path = img.with_suffix(".json")
        if not (img.exists() and meta_path.exists()):
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        candidate = (img, meta.get("photographer", ""), meta.get("pexels_url", ""))
        if candidate[2] not in recent_pexels_urls:
            return candidate
        fallback = fallback or candidate  # gardée au cas où toutes ont déjà servi
    if fallback:
        return fallback

    slug = DAY_TO_REGISTRE_SLUG.get(weekday, "geopolitique")
    fallback_img = ROOT / "assets" / "social" / "pub-photos" / f"{slug}.jpg"
    credits = json.loads((ROOT / "assets" / "social" / "pub-photos" / "credits.json").read_text(encoding="utf-8"))
    meta = next((c for c in credits if c.get("file") == f"{slug}.jpg"), {})
    if not fallback_img.exists():
        raise PubError(f"pick_photo : ni image récente ni banque de secours disponible ({slug}.jpg)")
    return fallback_img, meta.get("photographer", ""), meta.get("pexels_url", "")


# ---------------------------------------------------------------------------
# Génération d'image (Playwright, via generate_pub_image.py existant).
# ---------------------------------------------------------------------------
def generate_image(fields, output_path, template_name, photo_path, en=False):
    template = ROOT / "scripts" / "social" / (
        template_name.replace(".html", "-en.html") if en else template_name
    )
    data = {
        "eyebrow": fields.get("eyebrow", ""),
        "message": fields.get("message", ""),
        "attribution": fields.get("attribution", ""),
        "cta": fields.get("cta-image") or fields.get("cta", ""),
    }
    if fields.get("stat"):
        data["stat"] = fields["stat"]
    data_path = output_path.with_suffix(".data.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    try:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "social" / "generate_pub_image.py"),
             "--data", str(data_path), "--output", str(output_path),
             "--template", str(template), "--photo", str(photo_path)],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as e:
        raise PubError(f"generate_pub_image.py a échoué : {e.stdout}\n{e.stderr}")
    finally:
        data_path.unlink(missing_ok=True)
    return output_path.stat().st_size


# ---------------------------------------------------------------------------
# Construction de l'item feed-pub.xml (FR) et de son miroir (EN).
# ---------------------------------------------------------------------------
def html_escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def category_link(category, entry, fields):
    if fields.get("link"):
        return fields["link"]
    if category == "chiffre":
        return fields["source"]
    return CATEGORY_LINK[category]


def build_comments(fields):
    parts = [fields["eyebrow"], fields["message"].replace("\\n", "\n").replace("**", "")]
    if fields.get("attribution"):
        parts.append(fields["attribution"])
    if fields.get("cta"):
        parts.append(fields["cta"])
    return "\n\n".join(parts)


def build_feed_item(category, entry_id, fields, date_str, image_url, image_length,
                     photographer, pexels_url, guid_suffix="", link_override=None):
    now = datetime.now(PARIS)
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S %z")
    title = re.sub(r"\\n", " ", fields["message"]).replace("**", "").strip()
    link = link_override if link_override else category_link(category, entry_id, fields)
    comments = build_comments(fields)
    description = comments.replace("\n\n", "<br><br>").replace("\n", "<br>")
    guid = f"scenario-pub{guid_suffix}-{entry_id}-{date_str}"
    return (
        f"    <item>\n"
        f"      <title>{html_escape(title)}</title>\n"
        f"      <link>{link}</link>\n"
        f"      <guid isPermaLink=\"false\">{guid}</guid>\n"
        f"      <pubDate>{pub_date}</pubDate>\n"
        f"      <comments>{html_escape(comments)}</comments>\n"
        f"      <enclosure url=\"{image_url}\" length=\"{image_length}\" type=\"image/png\"/>\n"
        f"      <description><![CDATA[{description}<!-- credit: {photographer} — {pexels_url} -->]]></description>\n"
        f"    </item>\n"
    )


def insert_item_and_update_build_date(xml_text, item_xml):
    now = datetime.now(PARIS)
    build_date = now.strftime("%a, %d %b %Y %H:%M:%S %z")
    xml_text = re.sub(
        r"<lastBuildDate>.*?</lastBuildDate>",
        f"<lastBuildDate>{build_date}</lastBuildDate>",
        xml_text, count=1,
    )
    xml_text = xml_text.replace("<item>", item_xml.strip() + "\n    <item>", 1)
    # replace() ci-dessus insère AVANT le premier <item> existant tout en
    # gardant la première balise <item> intacte pour la suite du fichier —
    # équivalent à "juste avant le premier item existant".
    return xml_text


def validate_feed_xml(path, expected_new_count):
    tree = ET.parse(path)
    items = tree.getroot().find("channel").findall("item")
    guids = [it.find("guid").text for it in items]
    if len(guids) != len(set(guids)):
        raise PubError(f"validate_feed_xml : guid en double dans {path}")
    if len(items) != expected_new_count:
        raise PubError(f"validate_feed_xml : attendu {expected_new_count} items dans {path}, trouvé {len(items)}")
    return len(items)


# ---------------------------------------------------------------------------
# Traduction des champs pour le miroir EN (docs/routine-en-prompt.md,
# § « Traduction des posts pub ») — un seul appel OpenRouter, jamais une
# nouvelle rédaction.
# ---------------------------------------------------------------------------
def translate_fields(fields, model, api_key):
    keys = [k for k in ("eyebrow", "message", "attribution", "cta", "cta-image") if fields.get(k)]
    payload = {k: fields[k] for k in keys}
    stat_note = ""
    if fields.get("stat"):
        # "stat" doit rester l'EXACTE sous-chaîne utilisée dans le "message"
        # traduit (generate_pub_image.py l'utilise pour repérer où surligner
        # le chiffre dans le message — voir sa docstring) : "1 400" ne
        # matche jamais "$1.4 trillion", il faut donc traduire/reformater
        # "stat" en même temps que "message", jamais le garder tel quel.
        payload["stat"] = fields["stat"]
        keys = keys + ["stat"]
        stat_note = (
            '\n- "stat" doit être réécrit pour être une sous-chaîne EXACTE et '
            'littérale du "message" traduit une fois celui-ci écrit (même '
            'notation numérique, ex. si le message dit "$1.4 trillion", '
            '"stat" doit valoir exactement "$1.4 trillion" ou "1.4 trillion" '
            "selon ce qui apparaît réellement dans le message — jamais la "
            'notation française d\'origine recopiée telle quelle).'
        )
    prompt = f"""Traduis ces champs d'un post promotionnel court, du français vers l'anglais
naturel (jamais mot à mot). Le champ "message" peut contenir des \\n
(sauts de ligne volontaires, à garder aux mêmes endroits sémantiques,
pas nécessairement littéraux) et des **mot** (mise en évidence, à garder
sur le mot équivalent en anglais). N'ajoute aucun commentaire.{stat_note}

Champs (JSON) :
{json.dumps(payload, ensure_ascii=False)}

Renvoie un JSON unique avec exactement les mêmes clés, valeurs traduites.
"""
    result, usage = call_openrouter_json(prompt, model, api_key)
    translated = dict(fields)
    for k in keys:
        if k in result:
            translated[k] = result[k]
    if fields.get("stat") and translated.get("stat") not in translated.get("message", ""):
        raise PubError(
            f"translate_fields : 'stat' traduit ({translated.get('stat')!r}) n'apparaît pas "
            f"littéralement dans 'message' traduit — le surlignage automatique échouerait silencieusement."
        )
    return translated, usage


# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    now = datetime.now(PARIS)
    today = now.date()
    date_str = today.isoformat()
    weekday = today.weekday()
    category = DAY_TO_CATEGORY.get(weekday)
    if category is None or category == "futur":
        print(f"Catégorie du jour ({category}) hors de portée de ce script "
              f"(recherche web nécessaire) — rien à publier.", file=sys.stderr)
        return 1

    print(f"{today.strftime('%A %d %B %Y')} (Paris) -> catégorie : {category}")

    md_text = PUB_MESSAGES.read_text(encoding="utf-8")
    feed_xml = FEED_PUB.read_text(encoding="utf-8")
    feed_items = parse_feed_items(feed_xml)

    chiffre_source_date = None
    usage_total = {"cost": 0.0, "total_tokens": 0}

    if category == "chiffre":
        already_used = used_chiffre_sources(feed_items)
        candidates_dates = eligible_chiffre_dates(today, already_used)
        if not candidates_dates:
            print("Aucune édition éligible pour la catégorie chiffre aujourd'hui.", file=sys.stderr)
            return 1
        fields = None
        for d in candidates_dates:
            result = extract_chiffre(d, args.model, api_key)
            if result is None:
                print(f"  édition du {d} : aucun chiffre exploitable, essai suivant.")
                continue
            fields, usage = result
            for k in ("cost", "total_tokens"):
                usage_total[k] = usage_total.get(k, 0) + (usage.get(k) or 0)
            chiffre_source_date = d
            break
        if fields is None:
            print("Aucune édition candidate n'a de chiffre exploitable.", file=sys.stderr)
            return 1
        entry_id = f"chiffre-{date_str}"
        note = (f"*Extrait automatiquement de l'édition du {chiffre_source_date.isoformat()} "
                f"(archives/{chiffre_source_date.isoformat()}.html) — "
                f"voir docs/ARCHITECTURE.md, script scripts/pub/generate_daily_pub.py.*")
    else:
        entries = parse_pub_messages_section(md_text, category)
        entry = pick_rotation_entry(category, entries, feed_items)
        if entry is None:
            print(f"Aucune entrée valide dans la catégorie {category}.", file=sys.stderr)
            return 1
        fields = entry
        entry_id = entry["id"]
        note = None

    print(f"Entrée retenue : {entry_id}")
    print(f"  eyebrow: {fields.get('eyebrow')}")
    print(f"  message: {fields.get('message')[:120]}")

    photo_path, photographer, pexels_url = pick_photo(category, weekday, chiffre_source_date)
    print(f"Photo : {photo_path.name} ({photographer})")

    if args.dry_run:
        print("--dry-run : aucune image générée, aucun fichier modifié.")
        return 0

    template_name = CATEGORY_TEMPLATE[category]
    fr_image_path = ROOT / "assets" / "social" / "pub" / f"{date_str}.png"
    fr_image_length = generate_image(fields, fr_image_path, template_name, photo_path, en=False)
    fr_image_url = f"https://lesscenarios.fr/assets/social/pub/{date_str}.png"

    link_override = fields["source"] if category == "chiffre" else None
    fr_item_xml = build_feed_item(category, entry_id, fields, date_str, fr_image_url,
                                   fr_image_length, photographer, pexels_url,
                                   link_override=link_override)
    new_feed_xml = insert_item_and_update_build_date(feed_xml, fr_item_xml)
    FEED_PUB.write_text(new_feed_xml, encoding="utf-8")
    validate_feed_xml(FEED_PUB, len(feed_items) + 1)
    print("feed-pub.xml : item ajouté et validé.")

    if category == "chiffre":
        new_md = append_chiffre_entry(md_text, entry_id, fields, note)
        PUB_MESSAGES.write_text(new_md, encoding="utf-8")
        print("docs/pub-messages.md : entrée journalisée.")

    # Miroir EN
    en_fields, usage = translate_fields(fields, args.model, api_key)
    for k in ("cost", "total_tokens"):
        usage_total[k] = usage_total.get(k, 0) + (usage.get(k) or 0)
    en_image_path = ROOT / "en" / "assets" / "social" / "pub" / f"{date_str}.png"
    en_image_length = generate_image(en_fields, en_image_path, template_name, photo_path, en=True)
    en_image_url = f"https://lesscenarios.fr/en/assets/social/pub/{date_str}.png"
    en_feed_items = parse_feed_items(EN_FEED_PUB.read_text(encoding="utf-8")) if EN_FEED_PUB.exists() else []
    en_link = link_override  # la cible n'a presque jamais d'équivalent EN, voir docs/routine-en-prompt.md
    en_item_xml = build_feed_item(category, entry_id, en_fields, date_str, en_image_url,
                                   en_image_length, photographer, pexels_url,
                                   guid_suffix="-en", link_override=en_link)
    en_feed_xml = EN_FEED_PUB.read_text(encoding="utf-8")
    new_en_feed_xml = insert_item_and_update_build_date(en_feed_xml, en_item_xml)
    EN_FEED_PUB.write_text(new_en_feed_xml, encoding="utf-8")
    validate_feed_xml(EN_FEED_PUB, len(en_feed_items) + 1)
    print("en/feed-pub.xml : item ajouté et validé.")

    print(f"\nRésumé : catégorie={category}, entrée={entry_id}, "
          f"photo={photo_path.name} ({photographer} — {pexels_url}), "
          f"coût OpenRouter total ≈ {usage_total.get('cost', '?')} $.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
