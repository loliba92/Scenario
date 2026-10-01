#!/usr/bin/env python3
"""Enrichit les dossiers de sujets incomplets de data/sujets.json.

Contexte : à la migration (1er octobre 2026), aucun des 159 sujets n'avait de
« rationnel » ni de mots-clés, et seuls 57 avaient un contexte — les explications
variaient d'un sujet à l'autre. Ce script complète, sujet par sujet, ce qui manque
(contexte, rationnel, mots-clés pour chercher les articles, pistes de sources, point à
vérifier) avec un modèle qui dispose d'une recherche web, pour que TOUS les dossiers
soient aussi clairs que ceux produits par la veille (generate_hot_topics.py).

Règles de sécurité :
- ne remplit QUE les champs absents ; un champ déjà écrit (par vous, par la veille, ou
  repris de l'ancienne note) n'est jamais écrasé ;
- jamais d'invention : chaque fait doit venir du dossier existant ou d'un résultat de
  recherche réel ; une URL n'est gardée que si elle figure parmi les citations de la
  recherche ;
- le modèle dit si le sujet semble DÉPASSÉ (l'actualité a tranché depuis l'ajout) : le
  sujet n'est alors pas retiré, mais l'avertissement est ajouté à « à vérifier » ;
- un lot borné (`--max`, 10 par défaut) : le coût reste prévisible ; les sujets en tête de
  file (les prochains à passer) sont traités d'abord.

Utilisation :
    OPENROUTER_API_KEY=… python scripts/edition/enrich_sujets.py [--max 10] [--registre culture]
                                                                  [--ids id1,id2] [--dry-run]
Workflow : .github/workflows/enrich-sujets.yml (déclenchement manuel).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sujets as sj  # noqa: E402
from generate_daily_edition import GenerationError, call_openrouter  # noqa: E402
from generate_hot_topics import HOT_TOPICS_MODEL, dossier_depuis_reponse  # noqa: E402

MAX_PAR_DEFAUT = 10


def ordre_de_passage(data: dict, cibles: list[tuple[dict, dict]]) -> list[tuple[dict, dict]]:
    """Tête de file d'abord : rang du sujet parmi les sujets éligibles de sa section, puis
    les sujets « à valider »."""
    rang = {}
    for sec in data["sections"]:
        r = 0
        for e in sec["entrees"]:
            if e["type"] == "sujet" and sj.eligible(e):
                rang[e["id"]] = r
                r += 1
    return sorted(cibles, key=lambda c: (rang.get(c[1]["id"], 999), c[0]["cle"]))


def construire_prompt(sec: dict, e: dict, today: date) -> str:
    manque = sj.manquants(e)
    connu = sj.dossier_texte(sec, e)
    return f"""Tu complètes le dossier d'un sujet du backlog du site d'actualité Scénario
(lesscenarios.fr : chaque édition détaille UNE question à issue ouverte en 3 scénarios
chiffrés — favorable / stable / dégradé). Date d'aujourd'hui : {today.isoformat()}.

Le dossier ci-dessous a été écrit il y a plusieurs jours ou semaines et il est INCOMPLET.
Champs à produire (seulement ceux qui manquent, plus 'depasse') : {", ".join(manque) if manque else "aucun"}.

=== DOSSIER ACTUEL ===
{connu}
=== FIN DU DOSSIER ===

Fais une VRAIE recherche web sur ce sujet (utilise les mots-clés s'il y en a, sinon pars du
titre) pour vérifier l'état actuel de l'actualité, puis renvoie un JSON unique avec :

- "depasse" (booléen, obligatoire) : true si l'actualité a déjà tranché la question ou si le
  déclencheur a disparu depuis l'ajout du sujet, false si l'issue est toujours ouverte ;
  "raison" (texte court) si true.
- "contexte" (si absent du dossier ; 3 à 5 phrases, 250 caractères minimum) : CE QUI SE PASSE,
  faits datés, chiffres réels, acteurs. Des FAITS, pas d'opinion ni de prédiction.
- "rationnel" (si absent ; 2 à 4 phrases, 150 caractères minimum) : (1) pourquoi ce sujet
  maintenant, (2) pourquoi l'issue est réellement OUVERTE (forces contraires, incertitude),
  (3) ce qui est en jeu pour un lecteur français. Ne répète pas le contexte.
- "mots_cles" (si absents ; 4 à 8) : requêtes et mots précis pour retrouver les bons articles
  de presse — noms propres, lieux, chiffres clés, termes techniques ; français et, si utile, anglais.
- "question" (seulement si le titre n'est pas déjà une question à issue ouverte précise).
- "a_verifier" (optionnel) : ce qu'il reste à vérifier ou chiffrer avant rédaction.
- "sources" (2 à 4) : [{{"titre":"...","url":"..."}}] avec l'URL EXACTE d'un résultat de ta
  recherche — jamais une URL reconstituée ou inventée.
- "echeance" (optionnel) : {{"date":"AAAA-MM-JJ","raison":"..."}} seulement pour une vraie date butoir.

Règles absolues : n'invente AUCUN fait, chiffre, date ni citation ; chaque affirmation doit venir
du dossier ci-dessus ou d'un résultat de ta recherche. Si tu ne peux pas confirmer un point,
écris-le dans "a_verifier" plutôt que de l'affirmer. Réponds UNIQUEMENT avec le JSON, sans texte
autour ni balise markdown."""


def enrichir_un(sec: dict, e: dict, model: str, api_key: str, today: date):
    """Appelle le modèle et applique le résultat au sujet. Renvoie (champs complétés, coût)."""
    tools = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 6}}]
    resultat, usage = call_openrouter(construire_prompt(sec, e, today), model, api_key,
                                      temperature=0.3, max_tokens=4000, timeout=240, tools=tools)
    return appliquer_resultat(e, resultat, usage.get("cited_urls"), today), usage.get("cost")


def appliquer_resultat(e: dict, resultat: dict, cited_urls, today: date) -> list[str]:
    """Applique une réponse du modèle à un sujet (sans appel réseau : testable seul)."""
    if not isinstance(resultat, dict):
        return []
    champs = dossier_depuis_reponse(resultat, cited_urls)
    faits = sj.enrichir(e, champs, today.isoformat())
    if resultat.get("depasse") is True:
        raison = str(resultat.get("raison") or "l'actualité semble avoir tranché").strip()
        alerte = f"⚠ Peut-être dépassé (enrichissement du {today.isoformat()}) : {raison}"
        e["a_verifier"] = (e["a_verifier"] + " — " if e.get("a_verifier") else "") + alerte
        e["enrichi_le"] = today.isoformat()
        faits.append("a_verifier")
    return faits


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max", type=int, default=MAX_PAR_DEFAUT, help="nombre maximum de sujets traités")
    ap.add_argument("--registre", default=None, help="clé de section (ex. culture) ; défaut : tous")
    ap.add_argument("--ids", default=None, help="identifiants séparés par des virgules")
    ap.add_argument("--model", default=HOT_TOPICS_MODEL)
    ap.add_argument("--dry-run", action="store_true", help="liste les sujets ciblés, sans appel ni écriture")
    args = ap.parse_args(argv)

    try:
        data, action = sj.load_synced()
    except sj.SujetsError as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        return 1
    cibles = sj.incomplets(data)
    if args.registre:
        cibles = [c for c in cibles if c[0]["cle"] == args.registre]
    if args.ids:
        voulus = {i.strip() for i in args.ids.split(",") if i.strip()}
        cibles = [c for c in cibles if c[1]["id"] in voulus]
    cibles = ordre_de_passage(data, cibles)
    print(f"{len(cibles)} sujet(s) à enrichir ; lot de {min(args.max, len(cibles))}.")
    lot = cibles[: args.max]
    if args.dry_run:
        for sec, e in lot:
            print(f"  - {sec['cle']:20s} {e['id'][:60]:60s} manque : {', '.join(sj.manquants(e))}")
        return 0
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERREUR : OPENROUTER_API_KEY absent de l'environnement.", file=sys.stderr)
        return 1

    today = date.today()
    traites, echecs, cout = 0, 0, 0.0
    for sec, e in lot:
        try:
            faits, c = enrichir_un(sec, e, args.model, api_key, today)
        except GenerationError as err:
            echecs += 1
            print(f"  ✗ {e['id'][:60]} : {err}", file=sys.stderr)
            continue
        cout += float(c or 0)
        reste = sj.manquants(e)
        if faits:
            traites += 1
        else:
            echecs += 1
        print(f"  {'✓' if faits and not reste else '·'} {e['id'][:60]} : complété {faits or '—'}"
              + (f" ; manque encore {reste}" if reste else ""))

    if traites or action != "ok":
        sj.save_both(data)
    print(f"\n{traites} sujet(s) enrichi(s), {echecs} sans changement ou en échec (coût OpenRouter ≈ {cout:.3f} $).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
