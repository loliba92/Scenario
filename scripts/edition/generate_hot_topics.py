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
`🔍` (voir format_entry()) — docs/routine-prompt.md § Étape 0 l'ignore
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
import html
import json
import os
import re
import sys
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


def titles_in_section(md_text, heading):
    """Titres déjà en file (coché ou non) dans UNE section — sert d'anti-
    doublon minimal donné au modèle. Pas les commentaires HTML (trop
    lourd pour le prompt), juste la ligne visible."""
    pattern = re.compile(
        r"^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", re.M | re.S,
    )
    m = pattern.search(md_text)
    if not m:
        raise HotTopicsError(f"section introuvable dans sujets-prioritaires.md : {heading!r}")
    titles = re.findall(r"^- \[[ x]\] (.+)$", m.group(1), re.M)
    return [t.strip() for t in titles]


def parse_existing_titles(md_text):
    """Même chose que titles_in_section(), pour chacun des 6 registres."""
    return {key: titles_in_section(md_text, heading) for key, heading in REGISTRE_HEADINGS.items()}


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
        "Pour chaque sujet retenu :",
        "- 'accroche' : la question complète telle qu'elle apparaîtra dans le fichier "
        "(même style que les exemples existants, percutante mais précise).",
        "- 'tag' : 1-3 mots-clés courts entre crochets, ex. 'géopolitique & Arctique'.",
        "- 'contexte' : un paragraphe dense avec faits datés, chiffres réels, et "
        "2-4 sources (nom + URL réelle, jamais inventée) — même niveau de détail "
        "que les entrées déjà présentes (déclencheur, contexte de fond, ce qui reste "
        "à vérifier avant rédaction).",
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
        '{"geopolitique": [{"accroche":"...", "tag":"...", "contexte":"...", '
        '"urgence":"normal", "scenarios":{"favorable":"...","stable":"...","degrade":"..."}}], '
        '"actualite_francaise": [...], "economie": [...], "sciences": [...], '
        '"culture": [...], "sport": [...]} — liste vide pour un registre sans rien de solide.',
    ]
    return "\n".join(lines)


def format_entry(entry, today, origin_label=None):
    accroche = entry["accroche"].strip()
    tag = entry.get("tag", "").strip()
    contexte = entry.get("contexte", "").strip()
    scenarios = entry.get("scenarios") or {}
    # Préfixe 🔍 : marque une proposition automatique pas encore validée par
    # l'utilisateur — docs/routine-prompt.md § Étape 0 l'ignore explicitement
    # tant qu'il n'est pas retiré à la main. Sans ce marqueur, l'entrée était
    # indiscernable d'un sujet déjà validé et pouvait être piochée par
    # l'auto-sélection dès son tour suivant, sans jamais passer par la revue
    # humaine que ce script est censé préparer (voir incident du 19 septembre
    # 2026, docs/ARCHITECTURE.md).
    title_line = f"- [ ] 🔍 {accroche}"
    if tag:
        title_line += f" [{tag}]"
    comment_parts = [f"Ajouté automatiquement le {today.isoformat()} (recherche OpenRouter, "
                      "voir scripts/edition/generate_hot_topics.py) — à valider avant de "
                      "passer en priorité."]
    if origin_label:
        comment_parts.append(f"Repéré en veille sur le registre {origin_label}, "
                              "remonté ici pour son urgence.")
    if contexte:
        comment_parts.append(contexte)
    if scenarios:
        comment_parts.append(
            "→ 3 scénarios (brouillon) : favorable = {favorable} ; stable = {stable} ; "
            "dégradé = {degrade}".format(
                favorable=scenarios.get("favorable", "?"),
                stable=scenarios.get("stable", "?"),
                degrade=scenarios.get("degrade", "?"),
            )
        )
    comment = "  <!-- " + " ".join(comment_parts) + " -->\n"
    return title_line + "\n" + comment


def insert_entries(md_text, heading, entries, today):
    """`entries` : liste de (entry, origin_label) — origin_label est None
    pour un ajout normal (registre = section cible), ou le libellé du
    registre d'origine quand l'entrée est remontée en Carte blanche/
    Priorité absolue.

    Insère EN HAUT de la section (juste après l'en-tête et son
    commentaire d'intro, avant le premier sujet déjà en file) — voir la
    justification dans le docstring du module. Si la section est
    entièrement vide (aucun sujet), retombe en fin de section, ce qui
    revient au même point d'insertion."""
    if not entries:
        return md_text
    pattern = re.compile(r"^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", re.M | re.S)
    m = pattern.search(md_text)
    if not m:
        raise HotTopicsError(f"section introuvable pour insertion : {heading!r}")
    section_body = m.group(1)
    first_entry = re.search(r"^- \[[ x]\] ", section_body, re.M)
    insertion_point = m.start(1) + first_entry.start() if first_entry else m.end(1)
    block = "".join(format_entry(e, today, origin_label) for e, origin_label in entries)
    return md_text[:insertion_point] + block + md_text[insertion_point:]


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

    shown = history[:10]
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
    ap.add_argument("--model", default=HOT_TOPICS_MODEL)
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    today = date.today()
    md_text = SUJETS_PRIORITAIRES.read_text(encoding="utf-8")
    existing = parse_existing_titles(md_text)
    priorite_absolue_titles = titles_in_section(md_text, PRIORITE_ABSOLUE_HEADING)
    carte_blanche_titles = titles_in_section(md_text, CARTE_BLANCHE_HEADING)
    recent = recent_journal_titles(today)

    prompt = build_prompt(existing, priorite_absolue_titles, carte_blanche_titles, recent, today)
    tools = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 8}}]
    try:
        content, usage = call_openrouter(
            prompt, args.model, api_key, temperature=0.4, max_tokens=6000, timeout=180, tools=tools,
        )
    except GenerationError as e:
        print(f"ERREUR OpenRouter : {e}", file=sys.stderr)
        return 1

    # call_openrouter() renvoie déjà le contenu parsé (un dict, pas une
    # chaîne JSON) — le JSON invalide est géré en interne (InvalidModelJSON,
    # sous-classe de GenerationError, déjà catchée ci-dessus).
    result = content

    total = 0
    added_records = []
    entries_by_heading = {}
    priorite_absolue_count = 0
    carte_blanche_count = 0
    for key, heading in REGISTRE_HEADINGS.items():
        entries = (result.get(key) or [])[:MAX_PER_REGISTRE]
        entries = [e for e in entries if e.get("accroche") and e.get("contexte")]
        if not entries:
            continue
        print(f"{key} : {len(entries)} sujet(s) proposé(s)")
        total += len(entries)
        for e in entries:
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
                entries_by_heading.setdefault(target_heading, []).append((e, origin_label))
                added_records.append({
                    "date": today.isoformat(),
                    "registre": REGISTRE_LABELS[key],
                    "section": section_label,
                    "accroche": e["accroche"].strip(),
                    "tag": (e.get("tag") or "").strip(),
                })

    if args.dry_run:
        print(f"\n--dry-run : {total} sujet(s) au total, rien écrit.")
        return 0

    if total == 0:
        print("Aucun sujet retenu ce passage-ci — fichier inchangé.")
        return 0

    for target_heading, heading_entries in entries_by_heading.items():
        md_text = insert_entries(md_text, target_heading, heading_entries, today)

    SUJETS_PRIORITAIRES.write_text(md_text, encoding="utf-8")
    write_run_summary(added_records, today)
    history = update_hot_topics_history(added_records)
    update_dashboard_card(today, history)
    print(f"\n{total} sujet(s) ajouté(s) à sujets-prioritaires.md "
          f"(coût OpenRouter ≈ {usage.get('cost', '?')} $).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
