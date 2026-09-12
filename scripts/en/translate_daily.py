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
`sitemap.xml`, `sitemap-news.xml`, l'entrée du jour dans `en/feed.xml`,
l'image sociale `en/assets/social/instagram/AAAA-MM-JJ.png` (ajouté le
12 septembre 2026 — voir generate_en_social_image() : Playwright appelé
directement par ce script, comme generate_archives_table.py juste
au-dessus ; si la génération échoue pour une raison quelconque
(Chromium indisponible sur le runner...), repli automatique sur
l'image générique du site plutôt que de faire échouer toute la
traduction pour ça).
Portée NON couverte, à faire séparément :
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

# Chrome fixe du site (nav, libellés, footer...) — jamais spécifique à
# l'édition du jour, donc jamais envoyé à OpenRouter : une correspondance
# FR -> EN exacte et stable dans le temps. Manquant dans la version
# initiale de ce script (repéré le 12 septembre 2026 : toute la
# navigation/les libellés restaient en français sur les pages EN, seul le
# contenu de l'article lui-même passait par la traduction) — construit à
# partir de en/archives/2026-09-11.html (traduction manuelle de référence,
# avant l'automatisation), voir apply_chrome_translations().
CHROME_TEXT = {
    "Accueil": "Home",
    "Glossaire": "Glossary",
    "Le projet": "About",
    "Nous suivre": "Follow us",
    "Soutenir": "Support us",
    "Scénarios": "Scenarios",
    "L'essentiel": "Key takeaways",
    "Référence": "Reference",
    "Les faits": "The facts",
    "Favorable, stable ou dégradé": "Favorable, stable, or degraded",
    "Pour ceux qui découvrent le sujet": "For those new to the topic",
    "Pour aller plus loin": "To go further",
    "Reste connecté": "Stay connected",
    "La question posée": "The question at hand",
    "Partager :": "Share:",
    "Ce qu'on évalue": "What we're assessing",
    "Comprendre": "Understanding it",
    "Ne rate pas la prochaine édition :": "Don't miss the next edition:",
    "Indicateurs touchés": "Indicators affected",
    "Concrètement en France": "The France angle",
    "Petit lexique": "Quick glossary",
    "Vote avant le résultat, retrouve-nous partout": "Vote before you see the outcome — find us everywhere",
    "Mentions légales": "Legal notice",
    "Politique de confidentialité": "Privacy policy",
    "Voir tous les termes déjà expliqués → Glossaire": "See all terms explained so far → Glossary",
    "En savoir plus sur notre méthode →": "Learn more about our method →",
    "Voir aussi la revue de presse du jour →": "See also today's press roundup →",
    "L'actu, oui. Et après ?": "The news, yes. Then what?",
    "Chaque jour, un sujet qui compte, décortiqué en trois scénarios chiffrés, avec une probabilité pour chacun. Jamais figée : elle évolue si la situation change.":
        "Every day, one story that matters, broken down into three numbered scenarios, each with its own probability. Never fixed — it shifts as the situation changes.",
    "Chaque jour, un sondage sur notre canal Telegram : vote pour le scénario que tu juges le plus probable avant même de découvrir les vraies probabilités ci-dessus.":
        "Every day, a poll on our Telegram channel: vote for the scenario you think is most likely before you even see the real probabilities above.",
    "Retrouve-nous aussi sur tous nos réseaux :": "Find us also across all our channels:",
    "Le récap de la semaine est disponible — les 7 sujets et leur scénario le plus probable.":
        "This week's recap is up — the 7 topics and their most likely scenario.",
    "Lire →": "Read →",
    # aria-label / title (mêmes valeurs, jamais visibles dans le texte de
    # la page mais lues par un lecteur d'écran ou affichées en tooltip)
    "Activer les notifications": "Activate notifications",
    "Imprimer en 1 page": "Print on 1 page",
    "Sujet révisé": "Updated topic",
    "Récap de la semaine": "Weekly recap",
    "Revue de presse": "Press roundup",
    "Accès privé": "Private access",
    "Fermer ce message": "Close this message",
    "Partager sur X": "Share on X",
    "Partager sur Bluesky": "Share on Bluesky",
    "Partager sur Facebook": "Share on Facebook",
    "Partager sur LinkedIn": "Share on LinkedIn",
    "Partager sur WhatsApp": "Share on WhatsApp",
    "Partager sur Telegram": "Share on Telegram",
    "Copier le lien": "Copy link",
    "Sommaire de l'édition": "Edition contents",
    "Voir la définition dans le lexique": "See the definition in the glossary",
}


def apply_chrome_translations(soup):
    """Remplace tout noeud de texte dont le contenu exact correspond à une
    entrée de CHROME_TEXT, sur toute la page — jamais un remplacement
    partiel/en aveugle : seul un noeud dont le texte, une fois dépouillé
    des espaces, est identique mot pour mot à une clé est touché. Un
    contenu déjà traduit par OpenRouter ne risque donc jamais de
    correspondre par erreur (une phrase anglaise ne peut pas être égale à
    une clé française). Couvre aussi bien le texte visible que les
    attributs aria-label/title (mêmes clés, cf. CHROME_TEXT)."""
    for node in soup.find_all(string=True):
        if node.parent and node.parent.name in ("script", "style"):
            continue
        stripped = node.strip()
        if stripped in CHROME_TEXT:
            node.replace_with(CHROME_TEXT[stripped])
    for tag in soup.find_all(attrs={"aria-label": True}):
        if tag["aria-label"] in CHROME_TEXT:
            tag["aria-label"] = CHROME_TEXT[tag["aria-label"]]
    for tag in soup.find_all(attrs={"title": True}):
        if tag["title"] in CHROME_TEXT:
            tag["title"] = CHROME_TEXT[tag["title"]]

    # Cas mixtes : la chaîne à traduire n'est qu'une PARTIE d'un noeud de
    # texte plus large (jamais le noeud entier), donc invisible pour la
    # boucle ci-dessus. Un seul cas connu : le crédit photo en footnote
    # ("Photo d'illustration. {photographe} / ..."), voir
    # docs/routine-prompt.md § Crédit photo.
    credit = soup.select_one(".footer-photo-credit")
    if credit:
        for node in credit.find_all(string=True):
            if "Photo d'illustration." in node:
                node.replace_with(str(node).replace("Photo d'illustration.", "Illustration photo."))


# Script inline qui calcule .pubdate ("Published on ... · ~N min read ·
# Read N times") — exclu par construction de apply_chrome_translations()
# (code JS, pas du texte visible), mais contient plusieurs chaînes FR en
# dur : la regex qui lit la date sur .edition, les libellés, et la locale
# de formatage du compteur de lectures. Repéré le 12 septembre 2026 (même
# signalement utilisateur que les liens cassés) : sans ce correctif,
# .pubdate affichait encore "~6 min de lecture" sur une page par ailleurs
# entièrement en anglais. Remplacements exacts, vérifiés contre le script
# réel d'index.html — jamais une regex approximative sur du code JS.
PUBDATE_SCRIPT_FR_EN = [
    (r"/Édition du\s+(.+?)\s+·/", r"/Edition of\s+(.+?)\s+·/"),
    ('"Publié le " + m[1]', '"Published on " + m[1]'),
    ('"~" + minutes + " min de lecture" : ""', '"~" + minutes + " min read" : ""'),
    (
        'base + " · Lu " + n.toLocaleString("fr-FR") + " fois" : "Lu " + n.toLocaleString("fr-FR") + " fois"',
        'base + " · Read " + n.toLocaleString("en-US") + " times" : "Read " + n.toLocaleString("en-US") + " times"',
    ),
]


def translate_pubdate_script(soup):
    for script in soup.find_all("script"):
        if script.string and "Édition du" in script.string:
            code = script.string
            for old, new in PUBDATE_SCRIPT_FR_EN:
                if old not in code:
                    raise TranslationError(f"translate_pubdate_script : motif introuvable dans le script : {old!r}")
                code = code.replace(old, new)
            script.string = code
            return


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

    # h2.section-title existe à plusieurs endroits de la page (lexique,
    # sources...) mais un seul nous intéresse : celui de section.scenarios,
    # "reformulation courte et pédagogique de la question" (voir
    # docs/routine-prompt.md, étape technique 3) — recyclé tel quel comme
    # "context" de l'image sociale EN (voir generate_en_social_image()).
    section_title = soup.select_one(".scenarios .section-title")
    if section_title:
        segments["section_title"] = inner_html(section_title)

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

    # .comprendre-box (jusqu'à 2/édition) et .list-box (0 ou 1/édition) —
    # composants optionnels du contexte, oubliés lors de la première
    # version de ce script (repéré le 12 septembre 2026 : ces blocs
    # restaient entièrement en français sur la page EN, contrairement à
    # tout le reste de l'article déjà traduit). .comprendre-label et
    # .list-box-rank sont du chrome fixe (voir CHROME_TEXT), jamais des
    # segments à traduire ici.
    for i, cb in enumerate(soup.select(".comprendre-box")):
        lead = cb.select_one(".comprendre-lead")
        text = cb.select_one(".comprendre-text")
        if lead:
            segments[f"comprendre_{i}_lead"] = inner_html(lead)
        if text:
            segments[f"comprendre_{i}_text"] = inner_html(text)

    list_box = soup.select_one(".list-box")
    if list_box:
        label = list_box.select_one(".list-box-label")
        if label:
            segments["list_box_label"] = inner_html(label)
        for j, li in enumerate(list_box.select(".list-box-items > li")):
            title = li.select_one(".list-box-title")
            meta = li.select_one(".list-box-meta")
            if title:
                segments[f"list_box_item_{j}_title"] = inner_html(title)
            if meta:
                segments[f"list_box_item_{j}_meta"] = inner_html(meta)
        foot = list_box.select_one(".list-box-foot")
        if foot:
            segments["list_box_foot"] = inner_html(foot)

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
def call_openrouter(segments, model, api_key, retry_hint=False):
    ids = list(segments.keys())
    payload_in = [{"id": k, "html": segments[k]} for k in ids]

    # `retry_hint` : deuxième passe sur un sous-ensemble de segments déjà
    # rejetés par validate_translations() une première fois (voir main()).
    # Rappel renforcé plutôt qu'un prompt différent — le contenu et la
    # règle de fond ne changent pas, seule l'insistance sur la structure
    # augmente, pour donner une vraie chance au réessai de corriger ce
    # qui a cassé la première fois (balise oubliée, fusionnée, etc.).
    extra_warning = """
ATTENTION — ces segments ont déjà été rejetés une première fois car la
structure HTML renvoyée ne correspondait pas exactement à l'original
(balise manquante, ajoutée, ou attribut altéré) — le cas le plus
fréquent est l'ajout d'une balise <em>/<i> autour d'un titre de
film/série/franchise pour l'italiser à l'anglaise : NE FAIS PAS CELA,
même si c'est l'usage normal en anglais, le titre reste en texte brut.
Avant de répondre, recompte toi-même les balises de chaque segment
(nombre, ordre, nom, attributs class/id/href) et vérifie qu'elles sont
identiques à l'original — seul le texte visible entre les balises doit
changer, aucune balise supplémentaire quelle qu'elle soit.
""" if retry_hint else ""

    prompt = f"""Tu traduis une édition d'actualité économique du français vers l'anglais,
pour le site Scénario (lesscenarios.fr).

Règles strictes :
- Traduction naturelle, jamais mot à mot ("Concrètement en France" ne se
  traduit pas littéralement, par exemple).
- Chaque segment est un fragment de HTML. Conserve EXACTEMENT les balises,
  attributs, classes, id et href (en particulier les liens
  class="lex-ref" href="#lex-..." qui pointent vers le petit lexique de
  l'article — ne change jamais ce href). Traduis uniquement le texte visible.
- N'AJOUTE JAMAIS de balise absente de l'original, quelle qu'elle soit
  (même une balise HTML standard et a priori anodine). En particulier :
  ne mets JAMAIS un titre de film/série/franchise en italique avec
  <em>/<i>, même si c'est l'usage typographique normal en anglais —
  le titre reste en texte brut, exactement comme dans le français
  reçu. La structure de balises (nombre, ordre, imbrication) du
  fragment renvoyé doit être identique à celle reçue, sans exception.
- Reformate les unités à l'anglaise si besoin (ex: "725 Md$" -> "$725B",
  "+77 % sur un an" -> "+77% year-on-year").
- Ne résume pas, ne raccourcis pas, n'ajoute aucun commentaire.
- Renvoie un objet JSON unique de la forme {{"translations": [{{"id": "...", "html": "..."}}, ...]}},
  avec exactement les mêmes id, dans le même ordre, un par segment reçu.
{extra_warning}
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


def dump_validation_failures(attempt, originals, translations, errors):
    """Écrit sur stderr, pour chaque segment rejeté, l'original, la
    traduction reçue et la différence de signature structurelle —
    seule façon de diagnostiquer un échec de validation depuis le log
    CI sans relancer un appel OpenRouter complet (~5-10 min, non
    gratuit) juste pour voir ce qui a cassé. Ajouté après l'incident du
    12 septembre 2026, où le log ne contenait que la liste des id en
    échec, sans aucun moyen de savoir si le modèle avait oublié une
    balise, l'avait dupliquée, ou changé un attribut."""
    print(f"Validation structurelle échouée (essai {attempt}) sur : {errors}", file=sys.stderr)
    for seg_id in errors:
        original = originals.get(seg_id, "")
        translated = translations.get(seg_id, "")
        print(f"--- {seg_id} ---", file=sys.stderr)
        print(f"  original ({len(structural_signature(original))} balises) : {original[:400]!r}", file=sys.stderr)
        print(f"  traduit  ({len(structural_signature(translated))} balises) : {translated[:400]!r}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Rewriting des liens internes FR -> EN (règle générale + cas particuliers)
# ---------------------------------------------------------------------------
def rewrite_link(value, depth=1):
    """`depth` = nombre de niveaux à remonter jusqu'à la racine du site
    depuis le fichier de sortie : 1 pour en/index.html, 2 pour
    en/archives/{date}.html (un dossier de plus). Jamais appliqué aux URL
    absolues (http/https/mailto), aux ancres (#...) ni aux URL
    protocole-relatives (//...) — celles-ci pointent déjà où il faut,
    peu importe la profondeur du fichier qui les contient (bug réel du
    12 septembre 2026 : //gc.zgo.at/count.js devenait ../gc.zgo.at/...,
    lien mort, faute de ce garde-fou)."""
    if not value or value.startswith(("#", "http://", "https://", "mailto:", "//")):
        return value
    if value.startswith("en/"):
        value = value[len("en/"):]
        return ("../" * (depth - 1) + value) if depth > 1 else value
    return "../" * depth + value


def rewrite_links_for_en(soup, depth=1):
    for tag in soup.find_all(["a", "img", "link", "script"]):
        for attr in ("href", "src"):
            if tag.has_attr(attr):
                tag[attr] = rewrite_link(tag[attr], depth)


def rewrite_citation_link(href, depth=1):
    """Lien vers un article cité dans le texte (ex: 'archives/2026-09-08.html').
    Pointe vers le miroir EN de cet article s'il existe déjà, sinon vers
    l'original FR — jamais un lien mort. C'est la partie mécanique de la
    "cascade vers les articles cités" de docs/routine-en-prompt.md ; la
    décision éditoriale (faut-il ajouter une phrase de contexte) reste
    hors de portée de ce script.

    `depth` suit la même convention que rewrite_link, MAIS la forme du
    lien n'est pas un simple "../" de plus entre les deux profondeurs :
    depuis en/archives/{date_str}.html (depth=2), un lien vers un autre
    article EN est un frère dans le même dossier (juste "{date}.html",
    jamais "archives/{date}.html" qui redescendrait dans un sous-dossier
    inexistant) — traité explicitement plutôt que par arithmétique de
    préfixe (bug réel du 12 septembre 2026, voir bump_citation_link())."""
    m = re.match(r"^archives/(\d{4}-\d{2}-\d{2})\.html$", href)
    if not m:
        return rewrite_link(href, depth)
    date = m.group(1)
    en_mirror_exists = (REPO_ROOT / "en" / "archives" / f"{date}.html").exists()
    if depth <= 1:
        return f"archives/{date}.html" if en_mirror_exists else f"../archives/{date}.html"
    # depth == 2 (en/archives/{date_str}.html)
    return f"{date}.html" if en_mirror_exists else f"../../archives/{date}.html"


def bump_citation_link(href):
    """Convertit un lien déjà réécrit par rewrite_citation_link()/
    rewrite_link() pour en/index.html (depth=1) vers sa forme pour
    en/archives/{date_str}.html (depth=2) — utilisé sur le texte déjà
    traduit (translations{}), calculé une seule fois en depth=1 par
    collect_segments() avant même de savoir sur quel fichier il
    atterrira. Voir rewrite_citation_link() pour pourquoi ce n'est pas
    un simple "../" de plus sur un lien de citation vers un autre
    article EN (frère de dossier, pas un "../" de plus)."""
    if not href or href.startswith(("#", "http://", "https://", "mailto:", "//")):
        return href
    m = re.match(r"^archives/(\d{4}-\d{2}-\d{2}\.html)$", href)
    if m:
        return m.group(1)
    m = re.match(r"^\.\./archives/(\d{4}-\d{2}-\d{2}\.html)$", href)
    if m:
        return f"../../archives/{m.group(1)}"
    return f"../{href}"


def bump_fragment_depth(html):
    """Applique bump_citation_link() à tous les <a href> d'un fragment déjà
    traduit — voir build_en_soup(for_archive=True)."""
    frag = BeautifulSoup(html, "html.parser")
    for a in frag.find_all("a"):
        if a.has_attr("href"):
            a["href"] = bump_citation_link(a["href"])
    return "".join(str(c) for c in frag.contents)


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


def build_en_soup(fr_soup, date_str, translations, memory, en_image_url, for_archive=False):
    """for_archive=False construit en/index.html (profondeur 1 : en/) ;
    for_archive=True construit en/archives/{date_str}.html (profondeur 2 :
    en/archives/). Incident du 12 septembre 2026 : les deux étaient
    auparavant construits avec exactement le même HTML (liens calculés une
    seule fois pour la profondeur 1), donc quasiment tous les liens
    relatifs de l'archive (logo, PWA, nav, footer, citations d'articles)
    pointaient un cran trop haut — page cassée en pratique bien qu'elle
    ait l'air normale à l'oeil nu tant qu'on ne clique sur rien."""
    soup = copy.copy(fr_soup)
    depth = 2 if for_archive else 1

    # D'abord le rewrite générique des liens de chrome statique (nav,
    # masthead, icônes, bannière hebdo...). Les overrides explicites
    # ci-dessous (canonical, OG, bouton de langue) s'appliquent APRÈS,
    # pour ne jamais être re-préfixés par erreur (ex: "../index.html"
    # qui deviendrait "../../index.html" si l'ordre était inversé).
    rewrite_links_for_en(soup, depth)
    apply_chrome_translations(soup)
    translate_pubdate_script(soup)

    if for_archive:
        # Les segments déjà traduits (translations{}) ont été calculés une
        # seule fois par collect_segments(), à la profondeur 1 (voir
        # rewrite_citation_link appelé depuis inner_html) — les liens de
        # citation qu'ils contiennent doivent être recalculés pour la
        # profondeur 2 avant d'être insérés ici. Copie locale : ne jamais
        # muter le dict partagé avec build_en_soup(for_archive=False).
        translations = {
            k: (bump_fragment_depth(v) if isinstance(v, str) else v)
            for k, v in translations.items()
        }

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
    title_text = tr("title", soup.title.get_text() if soup.title else "")
    desc_text = tr("meta_description", meta_desc.get("content", "") if meta_desc else "")

    # hreflang : mêmes URLs absolues que côté FR (déjà correctes, rien à
    # changer). Le canonical, lui, doit pointer vers CETTE page (l'archive EN).
    canonical = soup.find("link", rel="canonical")
    if canonical:
        canonical["href"] = en_archive_url

    # Open Graph / Twitter Card : recopiés depuis title/meta_description déjà
    # traduits, sauf og:url (home EN sur en/index.html, archive EN elle-même
    # sur en/archives/{date}.html — même convention que og:url FR, voir
    # docs/routine-prompt.md étape 3bis) et og:image/twitter:image (chemin
    # EN, suppose que l'image sociale EN a été régénérée séparément — voir
    # portée non couverte en haut de fichier).
    og_url = en_archive_url if for_archive else "https://lesscenarios.fr/en/"
    for prop, value in [
        ("og:locale", "en_US"),
        ("og:url", og_url),
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

    # bouton de langue : sur l'archive, vers la page FR de CETTE édition
    # précise (archives/{date}.html) — jamais vers index.html, qui peut
    # déjà afficher une tout autre édition le jour où ce lien est cliqué.
    # Sur l'accueil EN, index.html FR affiche la même édition, donc y
    # pointer reste correct.
    lang_btn = soup.select_one(".masthead-lang-btn")
    if lang_btn:
        lang_btn["href"] = f"../../archives/{date_str}.html" if for_archive else "../index.html"
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

    for i, cb in enumerate(soup.select(".comprendre-box")):
        lead = cb.select_one(".comprendre-lead")
        text = cb.select_one(".comprendre-text")
        if lead:
            set_inner_html(lead, tr(f"comprendre_{i}_lead", inner_html(lead)))
        if text:
            set_inner_html(text, tr(f"comprendre_{i}_text", inner_html(text)))

    list_box = soup.select_one(".list-box")
    if list_box:
        label = list_box.select_one(".list-box-label")
        if label:
            set_inner_html(label, tr("list_box_label", inner_html(label)))
        for j, li in enumerate(list_box.select(".list-box-items > li")):
            title = li.select_one(".list-box-title")
            meta = li.select_one(".list-box-meta")
            if title:
                set_inner_html(title, tr(f"list_box_item_{j}_title", inner_html(title)))
            if meta:
                set_inner_html(meta, tr(f"list_box_item_{j}_meta", inner_html(meta)))
        foot = list_box.select_one(".list-box-foot")
        if foot:
            set_inner_html(foot, tr("list_box_foot", inner_html(foot)))

    # JSON-LD (NewsArticle) : jamais touché jusqu'ici (bug repéré le 12
    # septembre 2026 en même temps que les liens cassés) — la page EN
    # exposait aux moteurs de recherche un headline/description en
    # français et inLanguage=fr-FR sur une page qui prétend être en
    # anglais. author/publisher ne changent jamais (même règle que côté
    # FR, docs/routine-prompt.md étape 3bis) ; image reste l'image
    # générique FR par défaut (og-image-v2.png) si aucune photo EN n'a pu
    # être générée pour cette édition — même repli que og:image plus haut.
    ld_script = soup.find("script", attrs={"type": "application/ld+json"})
    if ld_script and ld_script.string:
        try:
            ld = json.loads(ld_script.string)
        except json.JSONDecodeError:
            ld = None
        if ld:
            ld["mainEntityOfPage"] = {"@type": "WebPage", "@id": og_url}
            ld["headline"] = tr("h1", ld.get("headline", ""))
            ld["description"] = tr("meta_description", ld.get("description", ""))
            ld["image"] = [en_image_url]
            ld["inLanguage"] = "en-US"
            ld_script.string = json.dumps(ld, indent=2, ensure_ascii=False)

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
# Image sociale EN (Instagram 1080x1080) — ajoutée le 12 septembre 2026.
# Portée initialement documentée comme NON couverte par ce script (voir
# historique de ce fichier) : nécessitait Playwright, pas encore dans le
# workflow CI. generate_instagram_image.py rendu portable (chemin Chromium
# du sandbox de dev remplacé par la détection de l'installation locale de
# Playwright, voir ce script) et Playwright+Chromium ajoutés à
# .github/workflows/translate-en.yml — ce script peut donc l'appeler
# lui-même, comme generate_archives_table.py juste au-dessus.
#
# Contrainte : le JSON title/context/scenario[].label utilisé pour l'image
# FR d'origine (/tmp/ig-data.json, voir docs/routine-prompt.md étape
# technique 8) est éphémère et déjà perdu au moment où ce script tourne
# (autre run CI, donc autre conteneur). On reconstruit donc une version
# EN à partir de ce qui est déjà traduit et committé — h1 (title), le
# h2.section-title de section.scenarios (context, exactement la même
# source que la routine FR utilise pour ce champ) et les titres de
# cartes déjà traduits (labels) — plutôt que la reformulation
# spécifiquement calibrée pour l'image que la routine FR écrit à la
# main. Résultat legèrement plus long/moins "punchy" qu'une image FR
# écrite à la main, mais fidèle et jamais un mot-à-mot cassé.
def strip_to_text(html_fragment):
    """Texte brut sans balises, pour les champs du JSON --data de
    generate_instagram_image.py (qui échappe lui-même le HTML reçu —
    lui passer des balises produirait des < > littéraux affichés)."""
    return BeautifulSoup(html_fragment or "", "html.parser").get_text().strip()


# .scenario-row .label des templates instagram-*-en.html est en une seule
# ligne (white-space:nowrap + text-overflow:ellipsis, voir ces fichiers) —
# conçu pour les labels courts que la routine FR écrit à la main
# spécifiquement pour l'image (docs/routine-prompt.md étape technique 8).
# Ici on réutilise le <h3> de carte déjà traduit (voir plus haut) : plus
# long par nature, et l'anglais rallonge encore le texte à sens égal —
# testé en conditions réelles (édition du 12 septembre) : un label de 56
# caractères se coupait déjà en plein mot ("...cut ..."). Tronché nous-
# mêmes sur un espace, avec de vraies points de suspension, plutôt que de
# laisser le CSS couper au pixel près (rendu imprévisible selon la
# largeur réelle des caractères).
SCENARIO_LABEL_MAX_CHARS = 52


def truncate_label(text, max_chars=SCENARIO_LABEL_MAX_CHARS):
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0].rstrip(",;:.")
    return f"{cut}…"


def generate_en_social_image(date_str, translations):
    """Génère en/assets/social/instagram/{date}.png via
    generate_instagram_image.py --lang en. Ne lève jamais d'exception :
    un problème d'environnement CI (Playwright/Chromium indisponible)
    ne doit jamais faire perdre la traduction textuelle déjà validée —
    seule l'image sociale EN reste alors absente pour cette édition,
    signalé sur stdout, jamais silencieux.

    Renvoie (image_url, image_length_bytes) : l'image EN dédiée si la
    génération a réussi, sinon l'image générique par défaut du site
    (même repli que index.html avant qu'une photo Pexels soit retenue,
    voir docs/routine-prompt.md étape technique 3bis) — jamais une URL
    vers un fichier qui n'existe pas.
    """
    fallback_url = "https://lesscenarios.fr/assets/social/og-image-v2.png"
    fallback_path = REPO_ROOT / "assets" / "social" / "og-image-v2.png"
    fallback = (fallback_url, str(fallback_path.stat().st_size) if fallback_path.exists() else "0")

    photo_path = REPO_ROOT / "assets" / "social" / "topic-images" / f"{date_str}.jpg"
    if photo_path.exists():
        template = REPO_ROOT / "scripts" / "social" / "instagram-photo-template-en.html"
        photo_arg = ["--photo", str(photo_path)]
    else:
        template = REPO_ROOT / "scripts" / "social" / "instagram-template-en.html"
        photo_arg = []

    data = {
        "title": strip_to_text(translations.get("h1", "")),
        "context": strip_to_text(translations.get("section_title", "")),
        "scenarios": [
            {"kind": kind, "label": truncate_label(strip_to_text(translations.get(f"card_{kind}_h3", "")))}
            for kind in ("favorable", "stable", "degrade")
        ],
    }
    if not data["title"] or not data["context"] or not all(s["label"] for s in data["scenarios"]):
        print("Image sociale EN : segment(s) manquant(s) (h1/section_title/card_*_h3) — "
              "image générique gardée à la place.", file=sys.stderr)
        return fallback

    output_path = REPO_ROOT / "en" / "assets" / "social" / "instagram" / f"{date_str}.png"
    data_path = output_path.with_suffix(".data.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    try:
        subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "social" / "generate_instagram_image.py"),
             "--data", str(data_path), "--output", str(output_path),
             "--template", str(template), "--lang", "en"] + photo_arg,
            cwd=REPO_ROOT, check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Image sociale EN : génération échouée (image générique gardée à la place) — {e}\n"
              f"stdout: {e.stdout}\nstderr: {e.stderr}", file=sys.stderr)
        return fallback
    finally:
        data_path.unlink(missing_ok=True)

    size = output_path.stat().st_size
    print(f"Image sociale EN générée : {output_path} ({size} octets).")
    return f"https://lesscenarios.fr/en/assets/social/instagram/{date_str}.png", str(size)


# ---------------------------------------------------------------------------
# en/feed.xml : nouvel <item> construit à partir des segments déjà traduits
# (titre, comments, titres de cartes) + des 5 nouveaux segments propres au
# feed (collect_feed_segments). Jamais de suppression d'item existant.
# ---------------------------------------------------------------------------
def build_en_feed_item(date_str, translations, feed_item, en_image, en_image_length):
    en_url = f"https://lesscenarios.fr/en/archives/{date_str}.html"
    title = translations.get("h1", "")
    comments = translations.get("question_text", "")

    cat_order = [("favorable", "🟢"), ("stable", "🔵"), ("degrade", "🔴")]
    category_parts = []
    for kind, emoji in cat_order:
        h3 = translations.get(f"card_{kind}_h3")
        if h3:
            category_parts.append(f'{emoji} {h3}')
    category = '","'.join(category_parts)

    length = en_image_length or "0"

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

    print(f"{len(segments)} segments à traduire.", flush=True)

    translations, usage = call_openrouter(segments, args.model, api_key)
    errors = validate_translations(segments, translations)

    # Un seul réessai, ciblé sur les seuls segments rejetés (voir
    # incident du 12 septembre 2026 : 8/47 segments — surtout des .dek
    # et .why longs, avec plusieurs balises imbriquées — ont échoué la
    # validation structurelle dès le premier essai). Diagnostic
    # toujours imprimé sur stderr avant le réessai, pour rester
    # débogable depuis le seul log CI même si le réessai réussit.
    if errors:
        dump_validation_failures(1, segments, translations, errors)
        print(f"Réessai sur {len(errors)} segment(s)...", flush=True)
        retry_segments = {k: segments[k] for k in errors}
        retry_translations, retry_usage = call_openrouter(retry_segments, args.model, api_key, retry_hint=True)
        retry_errors = validate_translations(retry_segments, retry_translations)
        if retry_errors:
            dump_validation_failures(2, retry_segments, retry_translations, retry_errors)
            print("Rien n'est écrit — sauter l'anglais du jour plutôt que publier une version cassée.", file=sys.stderr)
            return 1
        translations.update(retry_translations)
        usage = {
            "cost": (usage.get("cost") or 0) + (retry_usage.get("cost") or 0),
            "total_tokens": (usage.get("total_tokens") or 0) + (retry_usage.get("total_tokens") or 0),
        }
        print(f"Réessai réussi sur les {len(errors)} segment(s) concerné(s).", flush=True)

    print(f"Traduction validée. Coût de l'appel : {usage.get('cost', '?')} $ "
          f"({usage.get('total_tokens', '?')} tokens).")

    # Image sociale EN : jamais générée en --dry-run (effet de bord réel,
    # appel Playwright + écriture disque) — URL prévisionnelle seulement,
    # pour que le HTML de preview reste représentatif sans rien produire.
    if args.dry_run:
        en_image_url = f"https://lesscenarios.fr/en/assets/social/instagram/{date_str}.png"
        en_image_length = "0"
    else:
        en_image_url, en_image_length = generate_en_social_image(date_str, translations)

    # Deux documents distincts, PAS le même HTML recopié deux fois :
    # en/index.html vit à la profondeur 1 (en/), en/archives/{date}.html à
    # la profondeur 2 (en/archives/) — voir build_en_soup() pour l'incident
    # que ça a causé le 12 septembre 2026 (quasi tous les liens relatifs de
    # l'archive cassés, un cran de "../" manquant).
    index_soup = build_en_soup(fr_soup, date_str, translations, memory, en_image_url, for_archive=False)
    archive_soup = build_en_soup(fr_soup, date_str, translations, memory, en_image_url, for_archive=True)
    index_html = str(index_soup)
    archive_html = str(archive_soup)

    if args.dry_run:
        print("--dry-run : rien écrit sur disque.")
        print(archive_html[:2000])
        return 0

    en_archive_path.parent.mkdir(parents=True, exist_ok=True)
    en_archive_path.write_text(archive_html, encoding="utf-8")
    (REPO_ROOT / "en" / "index.html").write_text(index_html, encoding="utf-8")
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
        item_xml = build_en_feed_item(date_str, translations, feed_item, en_image_url, en_image_length)
        prepend_feed_item(item_xml)
        print("en/feed.xml mis à jour.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
