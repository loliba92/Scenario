#!/usr/bin/env python3
"""
Génère le post « pub » du jour (catégorie `chiffre`, unique désormais) et
son miroir anglais — remplace la routine Claude Code quotidienne
« Scénario — Pub hebdo » (docs/routine-pub-prompt.md), tâche jugée à 95%
mécanique par le prompt lui-même ("le choix de la catégorie, de l'entrée
et de la photo est entièrement déterministe... ne pas réfléchir dessus" —
voir ce fichier, en-tête).

**Mécanisme depuis le 19 septembre 2026 (retour utilisateur — remplace
extract_chiffre()/bank_chiffre.py/get_chiffre_for_date(), retirés le même
jour).** Ce script ne juge et n'extrait plus rien lui-même : il se
contente de LIRE la phrase `phrase_a_retenir` (et son `phrase_a_retenir_stat`)
déjà écrite à la rédaction de l'édition **du jour même**, directement
dans le HTML publié (voir `read_phrase_a_retenir()`) — zéro appel
OpenRouter, zéro jugement éditorial ici, zéro recherche dans les archives
passées. L'ancien mécanisme balayait jusqu'à 30 jours d'éditions
antérieures non utilisées pour y extraire a posteriori un chiffre — un
vrai incident réel le 19 septembre 2026 : deux posts consécutifs retombés
sur le même vieux candidat, un 3e sur une édition vieille de 3 jours,
hors contexte. Voir docs/ARCHITECTURE.md pour l'incident complet.

Principe non négociable, repris de docs/pub-messages.md : cette routine
n'invente jamais un message elle-même — le chiffre et sa phrase viennent
toujours mot pour mot de l'édition du jour, déjà vérifiée par le
processus éditorial normal (voir docs/routine-redaction-prompt.md
§ phrase_a_retenir).

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
from datetime import datetime
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

# Catégorie unique désormais — "chiffre" toujours, tous les jours.
# Simplifié le 17 septembre 2026 (retour utilisateur : « pas facile à
# comprendre [...] on peut dégager manifeste/citation, on peut simplifier
# ici ») : "manifeste"/"citation"/"question"/"futur" ne tournaient de
# toute façon presque jamais (seul "manifeste" était réellement actif,
# dimanche/vendredi) et forçaient à lire deux mécaniques différentes
# (rotation dans docs/pub-messages.md vs extraction verbatim) pour
# comprendre ce script. Les entrées manifeste/citation/question restent
# dans docs/pub-messages.md (contenu curaté, jamais supprimé), juste
# plus jamais lues par ce script — réactivables en réintroduisant une
# table de rotation si besoin un jour.
CHIFFRE_TEMPLATE = "pub-template-v5-stat.html"


class PubError(Exception):
    pass


# Plafond dur sur la longueur du message "chiffre" — le gabarit
# pub-template-v5-stat.html ancre .content en bas du cadre (bottom:0) et le
# laisse grandir VERS LE HAUT sans limite de hauteur ni scroll (voir ce
# fichier) : un message trop long déborde par le haut de l'image 1080x1080,
# clippé par overflow:hidden et chevauchant le masthead. Incident réel du
# 16 septembre 2026 (sujet fusion nucléaire, message ~650 caractères,
# image totalement illisible).
# Depuis le 19 septembre 2026, la vérification PRINCIPALE se fait en amont,
# à la rédaction (generate_daily_edition.py, PHRASE_A_RETENIR_MAX_CHARS) —
# même valeur, jamais désynchronisée volontairement. Gardé ici comme
# 2e filet dans read_phrase_a_retenir(), au cas où une édition publiée
# avant ce garde-fou (ou modifiée à la main) contournerait la vérification
# de rédaction.
CHIFFRE_MAX_CHARS = 280


# ---------------------------------------------------------------------------
# docs/pub-messages.md : journal des chiffres déjà utilisés (seule section
# encore lue par ce script — voir commentaire sur CHIFFRE_TEMPLATE plus
# haut pour les sections manifeste/citation/question, jamais supprimées
# mais plus jamais lues).
# ---------------------------------------------------------------------------
CHIFFRE_SECTION_HEADING = "5. Le saviez-vous — un chiffre qui marque (rotation E)"


def append_chiffre_entry(md_text, entry_id, fields, note):
    """Ajoute une entrée à la fin de la section 5 (journal des chiffres
    déjà utilisés) — jamais réordonné, jamais une entrée existante
    modifiée."""
    heading = CHIFFRE_SECTION_HEADING
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


# ---------------------------------------------------------------------------
# Catégorie `chiffre` : lecture directe de la phrase déjà écrite et
# vérifiée à la rédaction — voir docstring du module. Remplace le 19
# septembre 2026 toute la chaîne extract_chiffre()/bank_chiffre.py/
# get_chiffre_for_date() (recherche a posteriori dans jusqu'à 30 jours
# d'archives passées) : incident réel constaté le même jour, deux posts
# consécutifs retombés sur le même vieux candidat (aucun chiffre neuf
# trouvé entre-temps) puis un 3e retombé sur une édition vieille de 3
# jours, hors contexte. `phrase_a_retenir`/`phrase_a_retenir_stat` sont
# désormais écrits UNE FOIS, à la rédaction (voir
# docs/routine-redaction-prompt.md), avec tout le contexte de l'article —
# ce script ne fait plus que les relire tels quels dans le HTML déjà
# publié de l'édition du jour, jamais une édition plus ancienne.
# ---------------------------------------------------------------------------
def read_phrase_a_retenir(source_date):
    """Lit `.retenir-box`/`.retenir-text`/`data-stat` dans
    archives/{source_date}.html — aucun appel réseau, aucun jugement
    éditorial ici, juste une lecture. Renvoie (fields, usage) avec un coût
    nul, ou lève PubError si l'édition n'a pas (encore) cet encart —
    jamais un repli silencieux vers une autre date."""
    archive_path = ARCHIVES_DIR / f"{source_date.isoformat()}.html"
    if not archive_path.exists():
        raise PubError(f"édition du jour introuvable : {archive_path} — rien à publier")
    html_text = archive_path.read_text(encoding="utf-8")

    box_m = re.search(
        r'<div class="retenir-box"[^>]*\bdata-stat="([^"]*)"[^>]*>.*?'
        r'<p class="retenir-text">(.*?)</p>',
        html_text, re.S,
    )
    if not box_m:
        raise PubError(
            f"aucun .retenir-box trouvé dans {archive_path} — édition publiée avant le "
            "19 septembre 2026 (phrase_a_retenir), ou gabarit cassé. Jamais de repli vers "
            "une édition plus ancienne : corriger l'édition du jour, pas contourner."
        )
    stat = html.unescape(box_m.group(1)).strip()
    message = html.unescape(re.sub(r"<[^>]+>", "", box_m.group(2))).strip()
    if not message or not stat:
        raise PubError(f"retenir-box vide/incomplet dans {archive_path} (stat={stat!r}, message={message!r})")
    if len(message) > CHIFFRE_MAX_CHARS:
        raise PubError(
            f"phrase_a_retenir de {archive_path} fait {len(message)} caractères "
            f"(max {CHIFFRE_MAX_CHARS}) — devrait avoir été refusé à la rédaction "
            "(voir generate_daily_edition.py, PHRASE_A_RETENIR_MAX_CHARS), jamais publié tel quel."
        )
    if stat not in message:
        raise PubError(
            f"phrase_a_retenir_stat ({stat!r}) n'apparaît pas mot pour mot dans phrase_a_retenir "
            f"({message!r}) dans {archive_path} — devrait avoir été refusé à la rédaction."
        )

    months_fr = ["janvier", "février", "mars", "avril", "mai", "juin",
                 "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    attribution = f"— lesscenarios.fr, {source_date.day} {months_fr[source_date.month - 1]} {source_date.year}"

    fields = {
        "eyebrow": "LE SAVIEZ-VOUS",
        "stat": stat,
        "message": message,
        "attribution": attribution,
        "cta": "👉 Abonne-toi, un chiffre qui marque chaque jour",
        "source": f"https://lesscenarios.fr/archives/{source_date.isoformat()}.html",
    }
    return fields, {"cost": 0.0, "total_tokens": 0}


# ---------------------------------------------------------------------------
# Photo — toujours celle de l'édition source (assets/social/topic-images/
# {date}.jpg), jamais une recherche Pexels en direct ici.
# ---------------------------------------------------------------------------
def pick_photo(chiffre_source_date):
    """Renvoie (chemin_jpg, photographer, pexels_url)."""
    img = ROOT / "assets" / "social" / "topic-images" / f"{chiffre_source_date.isoformat()}.jpg"
    meta_path = img.with_suffix(".json")
    if img.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return img, meta.get("photographer", ""), meta.get("pexels_url", "")
    raise PubError(f"pick_photo : image/JSON manquants pour l'édition source {chiffre_source_date}")


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


def build_comments(fields):
    parts = [fields["eyebrow"], fields["message"].replace("\\n", "\n").replace("**", "")]
    if fields.get("attribution"):
        parts.append(fields["attribution"])
    if fields.get("cta"):
        parts.append(fields["cta"])
    return "\n\n".join(parts)


def build_feed_item(entry_id, fields, date_str, image_url, image_length,
                     photographer, pexels_url, guid_suffix=""):
    now = datetime.now(PARIS)
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S %z")
    title = re.sub(r"\\n", " ", fields["message"]).replace("**", "").strip()
    link = fields["source"]
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

    print(f"{today.strftime('%A %d %B %Y')} (Paris) -> catégorie : chiffre (unique), édition du jour")

    md_text = PUB_MESSAGES.read_text(encoding="utf-8")
    feed_xml = FEED_PUB.read_text(encoding="utf-8")
    feed_items = parse_feed_items(feed_xml)

    usage_total = {"cost": 0.0, "total_tokens": 0}

    # Toujours l'édition du jour, jamais une recherche parmi d'anciennes
    # éditions — voir read_phrase_a_retenir() et docs/ARCHITECTURE.md.
    chiffre_source_date = today
    fields, usage = read_phrase_a_retenir(chiffre_source_date)
    for k in ("cost", "total_tokens"):
        usage_total[k] = usage_total.get(k, 0) + (usage.get(k) or 0)
    entry_id = f"chiffre-{date_str}"
    note = (f"*Phrase à retenir de l'édition du {chiffre_source_date.isoformat()} "
            f"(archives/{chiffre_source_date.isoformat()}.html), reprise mot pour mot — "
            f"voir docs/ARCHITECTURE.md, script scripts/pub/generate_daily_pub.py.*")

    print(f"Entrée retenue : {entry_id}")
    print(f"  eyebrow: {fields.get('eyebrow')}")
    print(f"  message: {fields.get('message')[:120]}")

    photo_path, photographer, pexels_url = pick_photo(chiffre_source_date)
    print(f"Photo : {photo_path.name} ({photographer})")

    if args.dry_run:
        print("--dry-run : aucune image générée, aucun fichier modifié.")
        return 0

    fr_image_path = ROOT / "assets" / "social" / "pub" / f"{date_str}.png"
    fr_image_length = generate_image(fields, fr_image_path, CHIFFRE_TEMPLATE, photo_path, en=False)
    fr_image_url = f"https://lesscenarios.fr/assets/social/pub/{date_str}.png"

    fr_item_xml = build_feed_item(entry_id, fields, date_str, fr_image_url,
                                   fr_image_length, photographer, pexels_url)
    new_feed_xml = insert_item_and_update_build_date(feed_xml, fr_item_xml)
    FEED_PUB.write_text(new_feed_xml, encoding="utf-8")
    validate_feed_xml(FEED_PUB, len(feed_items) + 1)
    print("feed-pub.xml : item ajouté et validé.")

    new_md = append_chiffre_entry(md_text, entry_id, fields, note)
    PUB_MESSAGES.write_text(new_md, encoding="utf-8")
    print("docs/pub-messages.md : entrée journalisée.")

    # Miroir EN
    en_fields, usage = translate_fields(fields, args.model, api_key)
    for k in ("cost", "total_tokens"):
        usage_total[k] = usage_total.get(k, 0) + (usage.get(k) or 0)
    en_image_path = ROOT / "en" / "assets" / "social" / "pub" / f"{date_str}.png"
    en_image_length = generate_image(en_fields, en_image_path, CHIFFRE_TEMPLATE, photo_path, en=True)
    en_image_url = f"https://lesscenarios.fr/en/assets/social/pub/{date_str}.png"
    en_feed_items = parse_feed_items(EN_FEED_PUB.read_text(encoding="utf-8")) if EN_FEED_PUB.exists() else []
    en_item_xml = build_feed_item(entry_id, en_fields, date_str, en_image_url,
                                   en_image_length, photographer, pexels_url, guid_suffix="-en")
    en_feed_xml = EN_FEED_PUB.read_text(encoding="utf-8")
    new_en_feed_xml = insert_item_and_update_build_date(en_feed_xml, en_item_xml)
    EN_FEED_PUB.write_text(new_en_feed_xml, encoding="utf-8")
    validate_feed_xml(EN_FEED_PUB, len(en_feed_items) + 1)
    print("en/feed-pub.xml : item ajouté et validé.")

    print(f"\nRésumé : entrée={entry_id}, "
          f"photo={photo_path.name} ({photographer} — {pexels_url}), "
          f"coût OpenRouter total ≈ {usage_total.get('cost', '?')} $.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
