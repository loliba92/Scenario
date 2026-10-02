#!/usr/bin/env python3
"""
Alimente automatiquement `sujets-prioritaires.md` avec des sujets
"chauds" (actualité récente, falsifiable en 3 scénarios) — demandé le
17 septembre 2026 : « le fichier sujets prioritaires est aujourd'hui
quasi manuel, j'aimerais que tu l'alimentes régulièrement [...] tu peux
les mettre dans les domaines respectifs et je vérifierai si ça mérite de
les passer en prioritaire ».

Comportement par défaut : ce script écrit **en haut** de la section de
CHAQUE registre (Géopolitique/lundi, Économie/jeudi, etc.), juste après
l'en-tête et son commentaire d'intro, avant tous les sujets déjà en
file. Choix explicite du 18 septembre 2026 (retour utilisateur) :
certains registres accumulent 30+ sujets non cochés, consommés un par
semaine — un ajout en bas y attendrait ~30 semaines (~7-8 mois) avant
d'être traité, largement le temps qu'un sujet "chaud" (actualité de la
semaine) devienne périmé. En haut, il est le premier choisi au prochain
passage de son registre. MAX_PER_REGISTRE (2) sert de facto de "sujet
principal + sujet de secours" pour ce prochain passage.

**Marqueur 🔍, ajouté le 19 septembre 2026 (correctif root cause).** Être
premier dans la file ne suffisait pas à garantir la revue humaine promise
ci-dessus ("je vérifierai si ça mérite de les passer en prioritaire") :
rien n'empêchait Étape 0 de piocher une proposition non revue dès son tour
suivant, parfois le lendemain (cas réel du 19 septembre 2026, voir
docs/ARCHITECTURE.md — un sujet ajouté la veille a été retenu tel quel,
sans validation). Chaque entrée écrite par ce script est désormais préfixée
`🔍` (voir build_note() et sujets.ajouter()) — docs/routine-prompt.md § Étape 0 l'ignore
explicitement tant qu'un humain ne l'a pas retiré à la main.

Deux échappatoires supplémentaires, pour un sujet encore plus urgent que
"la semaine prochaine" — le modèle choisit via le champ 'urgence' de sa
réponse (voir build_prompt()), mais les plafonds MAX_CARTE_BLANCHE /
MAX_PRIORITE_ABSOLUE sont appliqués en dur dans main(), quoi que le
modèle renvoie :
- 'carte_blanche' : va dans « Mardi — carte blanche », traité sans
  attendre le tour normal du registre (utile si le prochain mardi
  arrive avant le prochain jour du registre d'origine).
- 'priorite_absolue' : va dans « 🔥 Priorité absolue », passe avant
  tout, quel que soit le jour — réservé à l'actualité en cours de
  rupture, plafonné à 1 par passage.

Un seul appel OpenRouter avec le server tool `openrouter:web_search`
(même mécanique que `generate_fallback_brief.py`) — le modèle cherche
lui-même l'actualité récente par registre, avec le contexte des sujets
déjà en file (anti-doublon) et des dernières éditions publiées.

Garde-fous repris de docs/routine-prompt.md (Étape 0bis, anti-doublon) :
- Jamais un sujet déjà traité récemment (30 derniers jours) ou déjà en
  file (coché ou non).
- La « règle d'or » du fichier s'applique : une vraie question à 3
  issues chiffrables, jamais un simple résumé d'actualité.
- Zéro sujet plutôt qu'un sujet artificiel juste pour remplir — un
  registre sans rien de vraiment chaud cette semaine reste vide.

Usage :
    OPENROUTER_API_KEY=xxx python3 scripts/edition/generate_hot_topics.py
"""
import argparse
import difflib
import html
import json
import os
import re
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_daily_edition import GenerationError, call_openrouter  # noqa: E402

# Passé de DEFAULT_MODEL (anthropic/claude-sonnet-5) à DeepSeek le
# 18 septembre 2026 : repérage de sujets chauds = tri/priorisation,
# pas de rédaction fine — finance le passage d'Opus sur la recherche
# quotidienne (voir generate_fallback_brief.py).
HOT_TOPICS_MODEL = "deepseek/deepseek-v4-flash"

ROOT = Path(__file__).resolve().parents[2]
SUJETS_PRIORITAIRES = ROOT / "sujets-prioritaires.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sujets as sj  # noqa: E402  (file de sujets structurée, voir scripts/edition/sujets.py)
SUJETS_A_SUIVRE = ROOT / "docs" / "sujets-a-suivre.md"
ARCHIVES_DIR = ROOT / "archives"
DASHBOARD = ROOT / "dashboard.html"
HOT_TOPICS_HISTORY = ROOT / "assets" / "data" / "hot-topics-history.json"
# Jamais committé (voir .gitignore) — lu par hot-topics.yml juste après ce
# script pour construire le corps de l'issue GitHub récapitulative.
RUN_SUMMARY = ROOT / "hot-topics-run-summary.md"

MAX_PER_REGISTRE = 2
JOURNAL_WINDOW_DAYS = 45
HISTORY_MAX_ENTRIES = 30
# Anti-doublon code, ajouté le 19 septembre 2026 (renfort demandé par
# l'utilisateur) — voir is_near_duplicate() plus bas pour le pourquoi :
# la consigne de prompt seule (« NE JAMAIS proposer un doublon ») a laissé
# passer plusieurs quasi-doublons en pratique (ex. « Carburants à prix
# record »/« Carburants à 3 € le litre »/« Carburants à 3 euros le
# litre » — même événement, trois runs différents ; « Les Houthis
# prennent le contrôle de Bab el-Mandeb » proposé mot pour mot identique
# deux fois dans un même run, une fois redirigé en carte blanche). Seuil
# calibré empiriquement sur ces cas réels (0.88-1.0 pour les vrais
# doublons) vs. des sujets proches mais distincts du même thème (0.29-0.44,
# ex. Taïwan vs. guerre commerciale USA-Chine) — large marge de sécurité.
DUPLICATE_SIMILARITY_THRESHOLD = 0.6
# Plafonds appliqués en dur dans main(), indépendamment de ce que le
# modèle renvoie dans 'urgence' — un sujet en trop est rétrogradé d'un
# cran (priorite_absolue -> carte_blanche -> normal) plutôt que perdu.
MAX_PRIORITE_ABSOLUE = 1
MAX_CARTE_BLANCHE = 2

PRIORITE_ABSOLUE_HEADING = "## 🔥 Priorité absolue (n'importe quel jour, avant tout le reste)"
PRIORITE_ABSOLUE_LABEL = "🔥 Priorité absolue"
CARTE_BLANCHE_HEADING = "## Mardi — carte blanche aux lecteurs (tous registres au choix)"
CARTE_BLANCHE_LABEL = "Carte blanche"

# clé du registre (utilisée par le modèle dans sa réponse) -> titre EXACT
# de la section dans sujets-prioritaires.md.
REGISTRE_HEADINGS = {
    "geopolitique": "## Géopolitique — lundi",
    "actualite_francaise": "## Actualité & politique française — mercredi",
    "economie": "## Économie & finance mondiale — jeudi",
    "sciences": "## Sciences — vendredi (climat & écologie, espace, IA, médecine, énergie…)",
    "culture": "## Culture — samedi",
    "sport": "## Sport — dimanche",
}

# Même clé -> libellé court affiché dans l'issue récapitulative et la
# carte "Derniers sujets identifiés" du dashboard (texte brut, jamais
# HTML-échappé ici — l'échappement se fait au moment d'écrire dans
# dashboard.html, voir update_dashboard_card()).
REGISTRE_LABELS = {
    "geopolitique": "Géopolitique",
    "actualite_francaise": "Actu. française",
    "economie": "Économie & finance",
    "sciences": "Sciences",
    "culture": "Culture",
    "sport": "Sport",
}

MONTHS_FULL = ["janvier", "février", "mars", "avril", "mai", "juin",
               "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def fmt_date_fr(d):
    return f"{d.day} {MONTHS_FULL[d.month - 1]} {d.year}"


class HotTopicsError(Exception):
    pass


def _normalize_title(text):
    """Minuscules, accents retirés, ponctuation réduite à des espaces —
    pour comparer deux titres sur leur contenu réel, pas leur mise en
    forme (« 3 € » vs « 3 euros », majuscule de début de phrase...)."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def find_near_duplicate(candidate_title, known_titles):
    """Renvoie le titre de `known_titles` le plus proche de
    `candidate_title` s'il dépasse DUPLICATE_SIMILARITY_THRESHOLD, sinon
    None. Backstop CODE à la consigne de prompt (« NE JAMAIS proposer un
    doublon, même reformulé ») — celle-ci seule a laissé passer plusieurs
    quasi-doublons en pratique, voir le commentaire sur
    DUPLICATE_SIMILARITY_THRESHOLD. Comparaison en O(n) sur `known_titles`,
    jamais un souci de perf ici (quelques dizaines de titres tout au
    plus)."""
    candidate_norm = _normalize_title(candidate_title)
    for known in known_titles:
        known_norm = _normalize_title(known)
        ratio = difflib.SequenceMatcher(None, candidate_norm, known_norm).ratio()
        if ratio >= DUPLICATE_SIMILARITY_THRESHOLD:
            return known
    return None


def titles_in_section(data, heading):
    """Titres déjà en file (publié ou non) dans UNE section — sert d'anti-
    doublon minimal donné au modèle. Même représentation qu'avant la file
    structurée : texte, tag final entre crochets, marque 🔍 si non validé. Pas
    les notes (trop lourdes pour le prompt)."""
    titre = heading[3:].strip()
    sec = next((x for x in data["sections"] if x["titre"] == titre), None)
    if sec is None:
        raise HotTopicsError(f"section introuvable dans data/sujets.json : {heading!r}")
    out = []
    for e in sec["entrees"]:
        if e["type"] != "sujet":
            continue
        t = e["titre"] + (f" [{e['tag']}]" if e.get("tag") else "")
        out.append((f"{sj.MARQUE_A_VALIDER} " if e["validation"] == "a_valider" else "") + t)
    return out


def parse_existing_titles(data):
    """Même chose que titles_in_section(), pour chacun des 6 registres."""
    return {key: titles_in_section(data, heading) for key, heading in REGISTRE_HEADINGS.items()}


def recent_journal_titles(today):
    """Titres des éditions publiées dans les JOURNAL_WINDOW_DAYS derniers
    jours (docs/sujets-a-suivre.md) — anti-doublon avec l'actu déjà
    traitée, pas seulement avec la file d'attente."""
    if not SUJETS_A_SUIVRE.exists():
        return []
    text = SUJETS_A_SUIVRE.read_text(encoding="utf-8")
    titles = []
    for m in re.finditer(
        r"^- (\d{2})\.(\d{2})\.(\d{4}) — \[(.+?)\]\(\.\./archives/(\d{4}-\d{2}-\d{2})\.html\)",
        text, re.M,
    ):
        d = date.fromisoformat(m.group(5))
        if (today - d).days <= JOURNAL_WINDOW_DAYS:
            titles.append(m.group(4).strip())
    return titles


def build_prompt(existing_by_registre, priorite_absolue_titles, carte_blanche_titles, recent_titles, today):
    lines = [
        "Tu alimentes le backlog de sujets du site d'actualité Scénario "
        "(lesscenarios.fr, chaque édition détaille une question à 3 issues "
        "chiffrées : favorable/stable/dégradé). Les sujets doivent être "
        "ANCRÉS DANS L'ACTUALITÉ RÉELLE ET RÉCENTE (dernières 1-2 semaines) — "
        "jamais un thème générique/intemporel sans déclencheur daté.",
        "",
        "Fais une VRAIE recherche web SÉPARÉE pour CHACUN des 6 registres "
        "ci-dessous, pas une seule passe superficielle qui couvre 2-3 "
        "registres et laisse les autres vides par défaut. Creuse chaque "
        "registre pour de vrai avant de conclure qu'il n'y a rien — "
        "renvoyer zéro sujet pour un registre doit rester l'exception, "
        "après une recherche sérieuse, jamais le résultat d'une recherche "
        "trop rapide. Jusqu'à "
        f"{MAX_PER_REGISTRE} sujets vraiment chauds par registre.",
        "",
        "Règle d'or, non négociable : chaque sujet doit être une "
        "PROBLÉMATIQUE À ISSUE OUVERTE, tranchable en 3 scénarios chiffrés "
        "(favorable/stable/dégradé) — jamais un simple résumé d'actualité "
        "ou une thèse déjà conclue. Mais jamais non plus un sujet artificiel "
        "juste pour remplir une case vide : une vraie actualité chaude "
        "d'abord, la reformulation en 3 scénarios ensuite.",
        "",
        "Barre d'importance, tout aussi non négociable : un sujet doit avoir "
        "une VRAIE conséquence structurelle (économique, politique, "
        "scientifique, sociétale, institutionnelle) — jamais un sujet dont "
        "l'intérêt tient surtout au buzz ou à l'émoi qu'il suscite (polémique "
        "de personnalité, célébrité, réseaux sociaux) sans enjeu de fond "
        "vérifiable. Test simple : si le sujet disparaissait des radars dans "
        "un mois sans laisser de trace réelle (aucun changement de politique, "
        "de marché, de rapport de force, de connaissance...), ce n'est pas "
        "un sujet chaud au sens de ce backlog, même s'il fait beaucoup parler "
        "cette semaine.",
        "",
        "Scénario est un site FRANÇAIS, lu par des lecteurs français : à "
        "candidats comparables dans un même registre, préférer celui qui a "
        "une vraie portée ou un lien concret pour un lecteur français (pas "
        "besoin d'un sujet franco-français — un sujet mondial avec un enjeu "
        "réel convient très bien) plutôt qu'un sujet purement anecdotique à "
        "l'étranger, sans résonance ni conséquence réelle côté France.",
        "",
        "Registres à couvrir, un par un, sans en sauter aucun : "
        "geopolitique, actualite_francaise, economie, sciences, culture, sport.",
        "",
        "Sujets déjà en file (NE JAMAIS proposer un doublon, même reformulé) :",
    ]
    for key in REGISTRE_HEADINGS:
        titles = existing_by_registre.get(key, [])
        lines.append(f"- {key} : " + ("; ".join(titles) if titles else "(vide)"))
    special_titles = priorite_absolue_titles + carte_blanche_titles
    lines.append(
        "- déjà en 🔥 Priorité absolue ou Carte blanche : "
        + ("; ".join(special_titles) if special_titles else "(vide)")
    )
    if recent_titles:
        lines.append("")
        lines.append(f"Sujets déjà publiés dans les {JOURNAL_WINDOW_DAYS} derniers jours "
                      "(éviter aussi, même angle proche) :")
        lines.append("; ".join(recent_titles))
    lines += [
        "",
        f"Date d'aujourd'hui : {today.isoformat()}.",
        "",
        "Pour chaque sujet retenu, renvoie un DOSSIER COMPLET et HOMOGÈNE — mêmes "
        "champs, même niveau de détail pour tous, jamais un champ bâclé ou laissé "
        "vide. Ce dossier servira directement à produire l'édition (il guidera la "
        "recherche d'articles), il doit donc être clair pour quelqu'un qui n'a PAS "
        "suivi l'actualité :",
        "- 'accroche' (obligatoire) : le titre du sujet, une QUESTION claire comprise du premier "
        "coup par quelqu'un qui n'a pas suivi l'actualité, qui sert aussi de base au titre "
        "de l'édition (donc lisible et bien référencé) : 60 à 110 caractères (120 au "
        "maximum) ; le sujet réel (nom propre, pays, objet) dans les premiers mots, tel "
        "qu'un lecteur le chercherait ; une seule idée, des mots simples ; pas d'acronyme "
        "inconnu du grand public, pas de métaphore, pas d'enchaînement de plusieurs "
        "propositions ni plus d'un deux-points.",
        "- 'question' (optionnel) : la problématique à issue ouverte, en UNE phrase "
        "précise, seulement si elle diffère de l'accroche (sinon omets-la).",
        "- 'tag' : 1-3 mots-clés courts, ex. 'géopolitique & Arctique'.",
        "- 'contexte' (obligatoire, 3 à 5 phrases, 250 caractères minimum) : CE QUI SE "
        "PASSE — le déclencheur daté (jour, mois), les faits établis, les chiffres "
        "réels, les acteurs. Des FAITS, pas d'opinion ni de prédiction.",
        "- 'rationnel' (obligatoire, 2 à 4 phrases, 150 caractères minimum) : LA PROBLÉMATIQUE "
        "que l'édition traitera. Commence par « La question : » suivi de la question à issue "
        "ouverte posée avec précision (ce qu'on cherche à trancher, avec l'horizon si utile). "
        "Puis : pourquoi l'issue est réellement OUVERTE (les forces ou hypothèses en présence, "
        "ce qui ferait pencher vers un scénario favorable, stable ou dégradé). Enfin, l'enjeu "
        "concret pour un lecteur français. INTERDIT de qualifier le sujet (« brûlant », « chaud », "
        "« crucial », « incontournable », « d'actualité ») ou de justifier son intérêt médiatique : "
        "seule compte la problématique. Ne répète pas le contexte.",
        "- 'mots_cles' (obligatoire, 4 à 8) : requêtes et mots précis pour retrouver "
        "les bons articles de presse — noms propres, lieux, chiffres clés, termes "
        "techniques ; en français et, quand c'est utile, en anglais.",
        "- 'sources' (2 à 4) : liste de {\"titre\":\"...\", \"url\":\"...\"} avec l'URL EXACTE "
        "d'un résultat de ta recherche web — jamais une URL reconstituée ou inventée.",
        "- 'a_verifier' (optionnel) : ce qu'il reste à vérifier ou chiffrer avant rédaction.",
        "- 'echeance' (optionnel) : {\"date\":\"AAAA-MM-JJ\",\"raison\":\"...\"} SEULEMENT s'il "
        "existe une vraie date butoir (vote, sommet, échéance légale) qui change l'intérêt "
        "du sujet.",
        "- 'scenarios' : un brouillon des 3 issues (favorable/stable/dégradé), "
        "2-3 phrases chacune.",
        "- 'urgence' (optionnel, 'normal' par défaut — l'immense majorité des cas) : "
        "'normal' = actualité chaude sur 1-2 semaines, attend son tour normal dans la "
        "file de son registre ; "
        "'carte_blanche' = sujet vraiment chaud qui ne doit PAS attendre son tour "
        "(la file d'un registre peut prendre plusieurs semaines à se vider) — sera "
        "inséré dans la file du mardi 'carte blanche', traité en priorité ce jour-là. "
        "À réserver aux sujets qui perdraient leur intérêt à attendre, pas à tout ce "
        "qui te semble intéressant ; "
        "'priorite_absolue' = actualité en cours de bascule/rupture (déclencheur des "
        "dernières 24-72h), qui serait probablement déjà obsolète ou tranchée dans une "
        "semaine — passe avant TOUT, quel que soit le jour. Réserve ce niveau à "
        "l'exception absolue (au plus un sujet sur tout ce que tu renvoies) : en cas "
        "de doute entre 'carte_blanche' et 'priorite_absolue', choisis 'carte_blanche'.",
        "",
        "Renvoie un JSON unique : "
        '{"geopolitique": [{"accroche":"...", "question":"...", "tag":"...", "contexte":"...", '
        '"rationnel":"...", "mots_cles":["..."], "sources":[{"titre":"...","url":"..."}], '
        '"a_verifier":"...", "echeance":{"date":"AAAA-MM-JJ","raison":"..."}, '
        '"urgence":"normal", "scenarios":{"favorable":"...","stable":"...","degrade":"..."}}], '
        '"actualite_francaise": [...], "economie": [...], "sciences": [...], '
        '"culture": [...], "sport": [...]} — liste vide pour un registre sans rien de solide.',
    ]
    return "\n".join(lines)


def build_note(entry, today, origin_label=None):
    """Note de MÉTHODE d'une proposition automatique : d'où elle vient. Tout le fond
    (contexte, rationnel, mots-clés, scénarios, sources) a ses propres champs dans le
    dossier — la note n'en contient plus."""
    parts = [f"Ajouté automatiquement le {today.isoformat()} (recherche OpenRouter, "
             "voir scripts/edition/generate_hot_topics.py) — à valider avant de "
             "passer en priorité."]
    if origin_label:
        parts.append(f"Repéré en veille sur le registre {origin_label}, "
                     "remonté ici pour son urgence.")
    return " ".join(parts)


def _texte_ou_none(v):
    v = (v or "").strip() if isinstance(v, str) else ""
    return v or None


def dossier_depuis_reponse(entry, cited_urls=None):
    """Champs du dossier (format de sujets.py) à partir d'une proposition du modèle,
    nettoyés et validés. Les sources n'ont une URL que si elle figure parmi les
    citations réelles de la recherche (`cited_urls`), jamais une URL reconstituée."""
    cited = set(cited_urls or [])
    mots = []
    for k in entry.get("mots_cles") or []:
        k = str(k).strip()
        if k and k.lower() not in {m.lower() for m in mots}:
            mots.append(k)
    sc = entry.get("scenarios") or {}
    scenarios = ({"favorable": str(sc["favorable"]).strip(), "stable": str(sc["stable"]).strip(),
                  "degrade": str(sc["degrade"]).strip()}
                 if all(isinstance(sc.get(k), str) and sc[k].strip() for k in ("favorable", "stable", "degrade")) else None)
    ec = entry.get("echeance")
    echeance = ({"date": ec["date"], "raison": str(ec.get("raison") or "").strip()}
                if isinstance(ec, dict) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(ec.get("date", ""))) else None)
    sources = []
    for src in entry.get("sources") or []:
        if not isinstance(src, dict) or not str(src.get("titre") or "").strip():
            continue
        url = str(src.get("url") or "").strip()
        sources.append({"titre": str(src["titre"]).strip(), "url": url if url in cited else None})
    return {
        "question": _texte_ou_none(entry.get("question")),
        "contexte": _texte_ou_none(entry.get("contexte")),
        "rationnel": _texte_ou_none(entry.get("rationnel")),
        "angle": _texte_ou_none(entry.get("angle")),
        "a_verifier": _texte_ou_none(entry.get("a_verifier")),
        "mots_cles": mots, "scenarios": scenarios, "echeance": echeance, "sources": sources,
    }


def insert_entries(data, heading, entries, today):
    """`entries` : liste de (entry, origin_label) — origin_label est None
    pour un ajout normal (registre = section cible), ou le libellé du
    registre d'origine quand l'entrée est remontée en Carte blanche/
    Priorité absolue.

    Ajoute EN HAUT de la section (avant le premier sujet déjà en file, après
    son commentaire d'intro), dans l'ordre reçu — voir la justification dans le
    docstring du module. Chaque ajout est « à valider » (🔍 dans la vue
    Markdown) : docs/routine-prompt.md § Étape 0 l'ignore tant qu'un humain ne
    l'a pas validé (incident du 19 septembre 2026, docs/ARCHITECTURE.md)."""
    if not entries:
        return []
    titre = heading[3:].strip()
    sec = next((x for x in data["sections"] if x["titre"] == titre), None)
    if sec is None:
        raise HotTopicsError(f"section introuvable pour insertion : {heading!r}")
    # On insère un à un en tête de section : dans l'ordre inverse pour garder l'ordre reçu.
    ajoutes = []
    for e, origin_label in reversed(entries):
        champs = dossier_depuis_reponse(e, e.get("_cited_urls"))
        ajoutes.append(sj.ajouter(data, sec["cle"], e["accroche"].strip(), tag=(e.get("tag") or "").strip() or None,
                                  validation="a_valider", origine="veille", ajoute_le=today.isoformat(),
                                  note=build_note(e, today, origin_label), **champs)["id"])
    return ajoutes


# Nombre de sujets DÉJÀ en file mais incomplets que chaque passage de la veille complète, en
# plus de ses propres ajouts : le retard (aucun rationnel ni mots-clés à la migration du
# 1er octobre 2026) se résorbe seul, sans lancer le workflow d'enrichissement à la main.
ENRICH_RETARD_PAR_PASSAGE = 4


def enrichir_apres_ajout(data, ids_nouveaux, api_key, model, today, retard=ENRICH_RETARD_PAR_PASSAGE):
    """Enrichit (recherche web, voir enrich_sujets.py) d'abord les dossiers INCOMPLETS qui
    viennent d'être ajoutés, puis `retard` sujets incomplets déjà en file (tête de file d'abord).
    Jamais bloquant : un échec d'appel laisse le sujet tel quel. Renvoie le nombre enrichi."""
    import enrich_sujets as en  # import tardif : enrich_sujets importe ce module
    nouveaux = [(sec, e) for sec, e in sj.sujets(data) if e["id"] in set(ids_nouveaux) and not sj.est_complet(e)]
    anciens = [c for c in sj.incomplets(data) if c[1]["id"] not in set(ids_nouveaux)]
    cibles = nouveaux + en.ordre_de_passage(data, anciens)[:max(retard, 0)]
    fait = 0
    for sec, e in cibles:
        try:
            champs, _ = en.enrichir_un(sec, e, model, api_key, today)
        except Exception as err:  # noqa: BLE001 — jamais bloquer la veille pour l'enrichissement
            print(f"  ✗ enrichissement de {e['id'][:60]} : {err}", file=sys.stderr)
            continue
        if champs:
            fait += 1
        print(f"  {'✓' if champs else '·'} enrichi {e['id'][:60]} : {champs or '—'}")
    return fait


def write_run_summary(records, today):
    """Corps de l'issue GitHub récapitulative — lu par hot-topics.yml juste
    après ce script. Groupé par SECTION CIBLE (où le sujet a été inséré),
    Priorité absolue et Carte blanche en tête — c'est l'info qui compte
    pour savoir quoi regarder en premier, pas le registre d'origine."""
    lines = [
        f"Sujets ajoutés automatiquement à `sujets-prioritaires.md` le {today.isoformat()} "
        "par la routine de veille (voir `scripts/edition/generate_hot_topics.py`) — "
        "à valider avant de passer en priorité.",
        "",
    ]
    by_section = {}
    for r in records:
        by_section.setdefault(r["section"], []).append(r)
    order = [PRIORITE_ABSOLUE_LABEL, CARTE_BLANCHE_LABEL] + list(REGISTRE_LABELS.values())
    for section in sorted(by_section, key=lambda s: order.index(s) if s in order else len(order)):
        items = by_section[section]
        lines.append(f"### {section}")
        for it in items:
            tag = f" [{it['tag']}]" if it["tag"] else ""
            origin = f" (repéré en veille {it['registre']})" if it["registre"] != section else ""
            lines.append(f"- {it['accroche']}{tag}{origin}")
        lines.append("")
    RUN_SUMMARY.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_hot_topics_history(new_records):
    """Historique des sujets ajoutés (plus récent en tête), plafonné à
    HISTORY_MAX_ENTRIES — alimente la carte "Derniers sujets identifiés"
    du dashboard. Même principe que update_openrouter_history() dans
    scripts/seo/update_audience.py."""
    if HOT_TOPICS_HISTORY.exists():
        history = json.loads(HOT_TOPICS_HISTORY.read_text(encoding="utf-8"))
    else:
        history = []
    history = new_records + history
    history = history[:HISTORY_MAX_ENTRIES]
    HOT_TOPICS_HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HOT_TOPICS_HISTORY.write_text(
        json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    return history


def update_dashboard_card(today, history):
    """Régénère la carte "Derniers sujets identifiés" de dashboard.html
    (mêmes marqueurs HTML que ceux posés dans le fichier), même principe
    de templating direct que update_dashboard() dans
    scripts/seo/update_audience.py — pas d'attente du prochain passage
    d'audience.yml, la mise à jour est immédiate."""
    text = DASHBOARD.read_text(encoding="utf-8")

    date_pattern = re.compile(r"(<!-- HOT-TOPICS:DATE_START -->).*?(<!-- HOT-TOPICS:DATE_END -->)", re.S)
    if not date_pattern.search(text):
        raise HotTopicsError("dashboard.html : marqueur HOT-TOPICS:DATE introuvable")
    text = date_pattern.sub(lambda m: m.group(1) + fmt_date_fr(today) + m.group(2), text)

    # Un même sujet peut figurer plusieurs fois dans l'historique (passages successifs) :
    # on n'affiche chaque accroche qu'une fois, la plus récente d'abord.
    shown, vus = [], set()
    for r in history:
        cle = re.sub(r"\W+", " ", r["accroche"].lower()).strip()
        if cle in vus:
            continue
        vus.add(cle)
        shown.append(r)
        if len(shown) == 10:
            break
    if shown:
        items = "\n".join(
            f'        <li><span class="agenda-later-tag">{html.escape(r.get("section", r["registre"]), quote=False)}</span>'
            f'{html.escape(r["accroche"], quote=False)} '
            f'<span class="agenda-later-empty">({date.fromisoformat(r["date"]).strftime("%d/%m")})</span></li>'
            for r in shown
        )
    else:
        items = ('        <li><span class="agenda-later-empty">aucun sujet identifié pour '
                  "l'instant — prochain passage mardi ou vendredi.</span></li>")

    list_pattern = re.compile(r"(<!-- HOT-TOPICS:LIST_START -->).*?(<!-- HOT-TOPICS:LIST_END -->)", re.S)
    if not list_pattern.search(text):
        raise HotTopicsError("dashboard.html : marqueur HOT-TOPICS:LIST introuvable")
    text = list_pattern.sub(lambda m: m.group(1) + "\n" + items + "\n        " + m.group(2), text)

    DASHBOARD.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-enrich", action="store_true", help="n'enrichit pas les dossiers incomplets après l'ajout")
    ap.add_argument("--enrich-retard", type=int, default=ENRICH_RETARD_PAR_PASSAGE,
                    help="nombre de sujets incomplets déjà en file complétés à chaque passage")
    ap.add_argument("--model", default=HOT_TOPICS_MODEL)
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    today = date.today()
    try:
        data, sync_action = sj.load_synced()
    except sj.SujetsError as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        return 1
    if sync_action != "ok":
        print(f"[sujets] modification manuelle reprise ({sync_action})")
    existing = parse_existing_titles(data)
    priorite_absolue_titles = titles_in_section(data, PRIORITE_ABSOLUE_HEADING)
    carte_blanche_titles = titles_in_section(data, CARTE_BLANCHE_HEADING)
    recent = recent_journal_titles(today)

    prompt = build_prompt(existing, priorite_absolue_titles, carte_blanche_titles, recent, today)
    tools = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 8}}]
    try:
        content, usage = call_openrouter(
            prompt, args.model, api_key, temperature=0.4, max_tokens=12000, timeout=240, tools=tools,
        )
    except GenerationError as e:
        print(f"ERREUR OpenRouter : {e}", file=sys.stderr)
        return 1

    # call_openrouter() renvoie déjà le contenu parsé (un dict, pas une
    # chaîne JSON) — le JSON invalide est géré en interne (InvalidModelJSON,
    # sous-classe de GenerationError, déjà catchée ci-dessus).
    result = content

    # Bassin de titres connus pour l'anti-doublon CODE (find_near_duplicate),
    # backstop à la consigne de prompt — voir DUPLICATE_SIMILARITY_THRESHOLD.
    # Grossit au fil de la boucle avec chaque entrée acceptée, pour attraper
    # aussi les doublons DANS la même réponse du modèle (constaté en
    # pratique : le même fait proposé deux fois dans un seul run, avec une
    # 'urgence' différente sur chaque copie — passait entre les mailles
    # d'un filtre qui n'aurait comparé qu'au fichier déjà sur disque).
    known_titles = (
        [t for titles in existing.values() for t in titles]
        + priorite_absolue_titles + carte_blanche_titles + recent
    )

    total = 0
    skipped_duplicates = 0
    added_records = []
    entries_by_heading = {}
    priorite_absolue_count = 0
    carte_blanche_count = 0
    for key, heading in REGISTRE_HEADINGS.items():
        entries = (result.get(key) or [])[:MAX_PER_REGISTRE]
        # Le contexte et le rationnel sont obligatoires : sans eux le sujet n'est pas
        # exploitable (ni compréhensible) pour produire le brief. Un dossier sans mots-clés
        # entre quand même, signalé « incomplet » (le workflow d'enrichissement le complétera).
        avant = len(entries)
        entries = [e for e in entries if e.get("accroche")
                   and len(str(e.get("contexte") or "").strip()) >= sj.MIN_CONTEXTE
                   and len(str(e.get("rationnel") or "").strip()) >= sj.MIN_RATIONNEL]
        if avant - len(entries):
            print(f"{key} : {avant - len(entries)} proposition(s) écartée(s) — contexte ou rationnel manquant/trop court")
        if not entries:
            continue
        print(f"{key} : {len(entries)} sujet(s) proposé(s)")
        for e in entries:
            dup = find_near_duplicate(e["accroche"], known_titles)
            if dup:
                skipped_duplicates += 1
                print(f"  - (doublon écarté) {e['accroche'][:100]!r} ~ déjà en file : {dup[:100]!r}")
                continue
            known_titles.append(e["accroche"])
            total += 1

            urgence = (e.get("urgence") or "normal").strip()
            if urgence not in ("normal", "carte_blanche", "priorite_absolue"):
                urgence = "normal"
            # Plafonds appliqués en dur, quoi que le modèle renvoie — une
            # urgence en trop est rétrogradée d'un cran plutôt que perdue.
            if urgence == "priorite_absolue" and priorite_absolue_count >= MAX_PRIORITE_ABSOLUE:
                urgence = "carte_blanche"
            if urgence == "carte_blanche" and carte_blanche_count >= MAX_CARTE_BLANCHE:
                urgence = "normal"

            if urgence == "priorite_absolue":
                target_heading, section_label = PRIORITE_ABSOLUE_HEADING, PRIORITE_ABSOLUE_LABEL
                priorite_absolue_count += 1
            elif urgence == "carte_blanche":
                target_heading, section_label = CARTE_BLANCHE_HEADING, CARTE_BLANCHE_LABEL
                carte_blanche_count += 1
            else:
                target_heading, section_label = heading, REGISTRE_LABELS[key]

            redirected = target_heading != heading
            suffix = f"  → {section_label}" if redirected else ""
            print(f"  - {e['accroche'][:100]}{suffix}")

            if not args.dry_run:
                origin_label = REGISTRE_LABELS[key] if redirected else None
                e["_cited_urls"] = usage.get("cited_urls") or []
                entries_by_heading.setdefault(target_heading, []).append((e, origin_label))
                added_records.append({
                    "date": today.isoformat(),
                    "registre": REGISTRE_LABELS[key],
                    "section": section_label,
                    "accroche": e["accroche"].strip(),
                    "tag": (e.get("tag") or "").strip(),
                })

    dup_suffix = f" ({skipped_duplicates} doublon(s) écarté(s))" if skipped_duplicates else ""

    if args.dry_run:
        print(f"\n--dry-run : {total} sujet(s) au total{dup_suffix}, rien écrit.")
        return 0

    if total == 0:
        print(f"Aucun sujet retenu ce passage-ci{dup_suffix} — fichier inchangé.")
        return 0

    ids_ajoutes = []
    for target_heading, heading_entries in entries_by_heading.items():
        ids_ajoutes += insert_entries(data, target_heading, heading_entries, today)

    sj.save_both(data)          # les ajouts sont d'abord mis à l'abri
    if not args.no_enrich:
        print("\nEnrichissement des dossiers incomplets :")
        if enrichir_apres_ajout(data, ids_ajoutes, api_key, args.model, today, args.enrich_retard):
            sj.save_both(data)
    write_run_summary(added_records, today)
    history = update_hot_topics_history(added_records)
    update_dashboard_card(today, history)
    print(f"\n{total} sujet(s) ajouté(s) à la file de sujets{dup_suffix} "
          f"(coût OpenRouter ≈ {usage.get('cost', '?')} $).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
