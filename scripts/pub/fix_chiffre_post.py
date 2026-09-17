#!/usr/bin/env python3
"""
Outil de réparation ponctuel — PAS un script de pipeline régulier.

Régénère EN PLACE (mêmes guid/link/pubDate, jamais un nouvel item) un post
"pub" de catégorie `chiffre` déjà publié, avec le message recalibré par la
version corrigée de `extract_chiffre()` (voir generate_daily_pub.py,
CHIFFRE_MAX_CHARS + garde-fou "message compréhensible seul" — incidents
réels du 16-17 septembre 2026 : image "fusion nucléaire" débordant
complètement du cadre, message du 17 septembre commençant par un pronom
sans antécédent).

Comme le guid/link/pubDate restent identiques, une RSS déjà consommée par
Make.com (dédoublonnée par guid) n'est jamais re-déclenchée — seule
l'image hébergée et le texte du flux changent, visibles pour qui reclique
ou revisite le flux, sans nouveau post social.

Usage :
    OPENROUTER_API_KEY=xxx python3 scripts/pub/fix_chiffre_post.py \\
        --post-date 2026-09-16 --source-date 2026-09-15
"""
import argparse
import os
import re
import sys
from datetime import date

from generate_daily_pub import (
    CHIFFRE_TEMPLATE,
    FEED_PUB,
    EN_FEED_PUB,
    PUB_MESSAGES,
    ROOT,
    build_comments,
    extract_chiffre,
    generate_image,
    html_escape,
    pick_photo,
    translate_fields,
)


def patch_feed_item(feed_path, guid, new_title, new_comments, new_description, new_length):
    text = feed_path.read_text(encoding="utf-8")
    block_re = re.compile(
        r'    <item>\n(?:(?!</item>).)*?<guid isPermaLink="false">' + re.escape(guid) +
        r'</guid>(?:(?!</item>).)*?</item>\n', re.S,
    )
    m = block_re.search(text)
    if not m:
        raise SystemExit(f"item {guid!r} introuvable dans {feed_path}")
    block = m.group(0)
    block = re.sub(r"<title>.*?</title>", f"<title>{html_escape(new_title)}</title>", block, count=1, flags=re.S)
    block = re.sub(r"<comments>.*?</comments>", f"<comments>{html_escape(new_comments)}</comments>", block, count=1, flags=re.S)
    block = re.sub(r'length="\d+"', f'length="{new_length}"', block, count=1)
    block = re.sub(
        r"<description><!\[CDATA\[.*?\]\]></description>",
        f"<description><![CDATA[{new_description}]]></description>",
        block, count=1, flags=re.S,
    )
    text = text[:m.start()] + block + text[m.end():]
    feed_path.write_text(text, encoding="utf-8")


def patch_pub_messages_entry(md_path, entry_id, fields, source_date):
    """Réécrit stat/message/attribution/source ET la note de bas d'entrée
    (« Extrait automatiquement de l'édition du... ») — pas seulement
    stat/message : incident réel du 17 septembre 2026, un changement de
    source_date (électricité -> dollar) laissait attribution/source/note
    encore sur l'ancienne date, incohérent avec le message affiché."""
    text = md_path.read_text(encoding="utf-8")
    # Bloc "- key: value" PLUS la note en italique qui suit (jusqu'à la
    # prochaine entrée "### " ou la fin de fichier) — les deux doivent
    # rester cohérents entre eux.
    block_re = re.compile(
        r"(### " + re.escape(entry_id) + r"\n(?:- [a-z-]+:.*\n)*)(\n\*[^\n]*\*\n)?",
        re.M,
    )
    m = block_re.search(text)
    if not m:
        print(f"[fix] attention : entrée {entry_id!r} introuvable dans {md_path}, "
              f"journal non corrigé (image/flux le sont quand même).", file=sys.stderr)
        return
    fields_block = m.group(1)
    fields_block = re.sub(r"^- stat: .*$", f"- stat: {fields['stat']}", fields_block, count=1, flags=re.M)
    fields_block = re.sub(r"^- message: .*$", f"- message: {fields['message']}", fields_block, count=1, flags=re.M)
    fields_block = re.sub(r"^- attribution: .*$", f"- attribution: {fields['attribution']}", fields_block, count=1, flags=re.M)
    fields_block = re.sub(r"^- source: .*$", f"- source: {fields['source']}", fields_block, count=1, flags=re.M)
    note = (f"\n*Extrait automatiquement de l'édition du {source_date.isoformat()} "
            f"(archives/{source_date.isoformat()}.html) — "
            f"voir docs/ARCHITECTURE.md, script scripts/pub/generate_daily_pub.py.*\n")
    text = text[:m.start()] + fields_block + note + text[m.end():]
    md_path.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post-date", required=True, help="Date du post pub à réparer (AAAA-MM-JJ)")
    ap.add_argument("--source-date", required=True, help="Date de l'édition source d'origine (AAAA-MM-JJ)")
    ap.add_argument("--model", default="deepseek/deepseek-v4-flash")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent.", file=sys.stderr)
        return 1

    post_date = date.fromisoformat(args.post_date)
    source_date = date.fromisoformat(args.source_date)

    result = extract_chiffre(source_date, args.model, api_key)
    if result is None:
        print(f"ERREUR : aucun chiffre exploitable dans l'édition du {source_date} — réparation impossible.", file=sys.stderr)
        return 1
    fields, usage = result
    print(f"Nouveau message ({len(fields['message'])} caractères) : {fields['message']}")

    photo_path, photographer, pexels_url = pick_photo(source_date)

    date_str = post_date.isoformat()
    entry_id = f"chiffre-{date_str}"

    fr_image_path = ROOT / "assets" / "social" / "pub" / f"{date_str}.png"
    fr_length = generate_image(fields, fr_image_path, CHIFFRE_TEMPLATE, photo_path, en=False)
    print(f"Image FR régénérée : {fr_image_path} ({fr_length} octets)")

    comments = build_comments(fields)
    title = re.sub(r"\\n", " ", fields["message"]).replace("**", "").strip()
    description = comments.replace("\n\n", "<br><br>").replace("\n", "<br>") + \
        f"<!-- credit: {photographer} — {pexels_url} -->"
    patch_feed_item(FEED_PUB, f"scenario-pub-{entry_id}-{date_str}", title, comments, description, fr_length)
    print(f"feed-pub.xml : item {entry_id!r} corrigé en place.")

    patch_pub_messages_entry(PUB_MESSAGES, entry_id, fields, source_date)
    print("docs/pub-messages.md : entrée journalisée corrigée.")

    en_fields, usage_en = translate_fields(fields, args.model, api_key)
    en_image_path = ROOT / "en" / "assets" / "social" / "pub" / f"{date_str}.png"
    en_length = generate_image(en_fields, en_image_path, CHIFFRE_TEMPLATE, photo_path, en=True)
    print(f"Image EN régénérée : {en_image_path} ({en_length} octets)")

    en_comments = build_comments(en_fields)
    en_title = re.sub(r"\\n", " ", en_fields["message"]).replace("**", "").strip()
    en_description = en_comments.replace("\n\n", "<br><br>").replace("\n", "<br>") + \
        f"<!-- credit: {photographer} — {pexels_url} -->"
    patch_feed_item(EN_FEED_PUB, f"scenario-pub-en-{entry_id}-{date_str}", en_title, en_comments, en_description, en_length)
    print(f"en/feed-pub.xml : item {entry_id!r} corrigé en place.")

    total_cost = (usage.get("cost") or 0) + (usage_en.get("cost") or 0)
    print(f"\nCoût OpenRouter ≈ {total_cost:.4f} $.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
