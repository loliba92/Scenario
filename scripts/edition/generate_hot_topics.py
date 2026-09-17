#!/usr/bin/env python3
"""
Alimente automatiquement `sujets-prioritaires.md` avec des sujets
"chauds" (actualité récente, falsifiable en 3 scénarios) — demandé le
17 septembre 2026 : « le fichier sujets prioritaires est aujourd'hui
quasi manuel, j'aimerais que tu l'alimentes régulièrement [...] tu peux
les mettre dans les domaines respectifs et je vérifierai si ça mérite de
les passer en prioritaire ».

Principe non négociable : ce script écrit dans les sections **par
registre** (Géopolitique/lundi, Économie/jeudi, etc.), jamais dans
« 🔥 Priorité absolue » — cette section reste une décision humaine (voir
le nom de la section elle-même : ça passe avant tout, quel que soit le
jour). Les nouvelles entrées vont toujours **en bas** de leur section
(ordre = ordre de priorité, un ajout automatique ne double jamais un
sujet déjà en file).

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
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_daily_edition import DEFAULT_MODEL, GenerationError, call_openrouter  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SUJETS_PRIORITAIRES = ROOT / "sujets-prioritaires.md"
SUJETS_A_SUIVRE = ROOT / "docs" / "sujets-a-suivre.md"
ARCHIVES_DIR = ROOT / "archives"

MAX_PER_REGISTRE = 2
JOURNAL_WINDOW_DAYS = 45

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


class HotTopicsError(Exception):
    pass


def parse_existing_titles(md_text):
    """Titres déjà en file (coché ou non), par registre — sert d'anti-
    doublon minimal donné au modèle. Pas les commentaires HTML (trop
    lourd pour le prompt), juste la ligne visible."""
    sections = {}
    for key, heading in REGISTRE_HEADINGS.items():
        pattern = re.compile(
            r"^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", re.M | re.S,
        )
        m = pattern.search(md_text)
        if not m:
            raise HotTopicsError(f"section introuvable dans sujets-prioritaires.md : {heading!r}")
        titles = re.findall(r"^- \[[ x]\] (.+)$", m.group(1), re.M)
        sections[key] = [t.strip() for t in titles]
    return sections


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


def build_prompt(existing_by_registre, recent_titles, today):
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
        "Registres à couvrir, un par un, sans en sauter aucun : "
        "geopolitique, actualite_francaise, economie, sciences, culture, sport.",
        "",
        "Sujets déjà en file (NE JAMAIS proposer un doublon, même reformulé) :",
    ]
    for key in REGISTRE_HEADINGS:
        titles = existing_by_registre.get(key, [])
        lines.append(f"- {key} : " + ("; ".join(titles) if titles else "(vide)"))
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
        "",
        "Renvoie un JSON unique : "
        '{"geopolitique": [{"accroche":"...", "tag":"...", "contexte":"...", '
        '"scenarios":{"favorable":"...","stable":"...","degrade":"..."}}], '
        '"actualite_francaise": [...], "economie": [...], "sciences": [...], '
        '"culture": [...], "sport": [...]} — liste vide pour un registre sans rien de solide.',
    ]
    return "\n".join(lines)


def format_entry(entry, today):
    accroche = entry["accroche"].strip()
    tag = entry.get("tag", "").strip()
    contexte = entry.get("contexte", "").strip()
    scenarios = entry.get("scenarios") or {}
    title_line = f"- [ ] {accroche}"
    if tag:
        title_line += f" [{tag}]"
    comment_parts = [f"Ajouté automatiquement le {today.isoformat()} (recherche OpenRouter, "
                      "voir scripts/edition/generate_hot_topics.py) — à valider avant de "
                      "passer en priorité."]
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
    if not entries:
        return md_text
    pattern = re.compile(r"(^" + re.escape(heading) + r"\s*$.*?)(\n(?=^## )|\Z)", re.M | re.S)
    m = pattern.search(md_text)
    if not m:
        raise HotTopicsError(f"section introuvable pour insertion : {heading!r}")
    block = "".join(format_entry(e, today) for e in entries)
    insertion_point = m.end(1)
    return md_text[:insertion_point] + block + md_text[insertion_point:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    today = date.today()
    md_text = SUJETS_PRIORITAIRES.read_text(encoding="utf-8")
    existing = parse_existing_titles(md_text)
    recent = recent_journal_titles(today)

    prompt = build_prompt(existing, recent, today)
    tools = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 8}}]
    try:
        content, usage = call_openrouter(
            prompt, args.model, api_key, temperature=0.4, max_tokens=6000, timeout=180, tools=tools,
        )
    except GenerationError as e:
        print(f"ERREUR OpenRouter : {e}", file=sys.stderr)
        return 1

    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"ERREUR : réponse non-JSON : {e}\n{content[:1500]}", file=sys.stderr)
        return 1

    total = 0
    for key, heading in REGISTRE_HEADINGS.items():
        entries = (result.get(key) or [])[:MAX_PER_REGISTRE]
        entries = [e for e in entries if e.get("accroche") and e.get("contexte")]
        if not entries:
            continue
        print(f"{key} : {len(entries)} sujet(s) proposé(s)")
        for e in entries:
            print(f"  - {e['accroche'][:100]}")
        total += len(entries)
        if not args.dry_run:
            md_text = insert_entries(md_text, heading, entries, today)

    if args.dry_run:
        print(f"\n--dry-run : {total} sujet(s) au total, rien écrit.")
        return 0

    if total == 0:
        print("Aucun sujet retenu ce passage-ci — fichier inchangé.")
        return 0

    SUJETS_PRIORITAIRES.write_text(md_text, encoding="utf-8")
    print(f"\n{total} sujet(s) ajouté(s) à sujets-prioritaires.md "
          f"(coût OpenRouter ≈ {usage.get('cost', '?')} $).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
