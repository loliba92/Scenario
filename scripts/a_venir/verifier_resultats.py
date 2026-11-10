#!/usr/bin/env python3
"""Cherche, pour les rendez-vous échus, le résultat réel — puis le soumet à des contrôles stricts (controles.py).

Le modèle (bon marché, avec recherche web) PROPOSE ; un second modèle indépendant confirme le constat ; le code VÉRIFIE
chaque citation, chiffre et date dans les pages sources. Rien n'est publié si un seul contrôle échoue.
Écrit un fichier de propositions (jamais data/a-venir.json lui-même) : appliquer_resultats.py le fusionne.
Usage : OPENROUTER_API_KEY=xxx python3 scripts/a_venir/verifier_resultats.py --sortie patch.json [--dry-run]
"""
import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "edition"))
import controles  # noqa: E402
import generate_a_venir as g  # noqa: E402

RACINE = g.RACINE
MODELE = "deepseek/deepseek-v4-flash"
MODELE_CONFIRMATION = "google/gemini-3.7-flash"   # raisonnement imposé : max_tokens large ci-dessous
MAX_PAR_PASSAGE = 3
MAX_ESSAIS_ECHUS = 10
INTERVALLE_AVANT_ECHEANCE = 7  # jours entre deux recherches pour un rendez-vous pas encore échu
PANNES = ("appel du modèle impossible", "confirmation impossible")
JOURNAL = RACINE / "data" / "a-venir-journal.json"
OUTILS = [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 8}}]


def candidats(rendez_vous, journal, jour):
    """Échus d'abord (essai quotidien, plafonné) ; les autres seulement une fois par semaine."""
    res = []
    for r in rendez_vous:
        if "resultat" in r:
            continue
        j = journal.get(r["id"], {})
        dernier = date.fromisoformat(j["dernier_essai"]) if j.get("dernier_essai") else None
        if date.fromisoformat(r["date"]) < jour:
            if j.get("essais", 0) >= MAX_ESSAIS_ECHUS or dernier == jour:
                continue
            res.append((0, dernier or date.min, r))
        elif dernier is None or (jour - dernier).days >= INTERVALLE_AVANT_ECHEANCE:
            res.append((1, dernier or date.min, r))
    return [r for _, _, r in sorted(res, key=lambda x: (x[0], x[1], x[2]["id"]))][:MAX_PAR_PASSAGE]


def prompt_recherche(r, jour, scenarios):
    sc = "\n".join(f"- {k} : {v[0]}" for k, v in scenarios.items()) or "(non disponibles)"
    return (
        f"Nous sommes le {jour.isoformat()}. Rendez-vous à vérifier : « {r['question']} » "
        f"(responsable : {r['qui']} ; date limite : {r['date']}).\n"
        "Cherche sur le web si la réponse est connue. Réponds UNIQUEMENT par un objet JSON :\n"
        '{"statut": "arrive" | "pas_arrive" | "incertain", "date_reponse": "AAAA-MM-JJ", '
        '"reponse": "une ou deux phrases, au passé, faits datés, sans conditionnel", '
        '"chiffres": [{"libelle": "...", "valeur": "..."}], '
        '"scenario": "favorable" | "stable" | "degrade" | null, '
        '"sources": [{"titre": "...", "url": "https://...", "extrait": "citation EXACTE, mot pour mot, de 40 à 200 caractères, copiée dans la page"}]}\n'
        f"Scénarios de l'édition (choisis celui vers lequel pointe la réponse, ou null si elle ne tranche pas) :\n{sc}\n"
        "Règles : au moins 2 sources de sites différents (presse reconnue ou site officiel) ; chaque extrait doit être recopié tel quel ; "
        "chaque chiffre doit figurer dans une source ; réponds « incertain » au moindre doute, ou si aucune source récente ne le confirme ; "
        "« pas_arrive » seulement si la date limite est dépassée."
    )


def prompt_confirmation(r, jour, prop):
    return (
        f"Nous sommes le {jour.isoformat()}. Vérifie de façon indépendante, avec une recherche web, ce rendez-vous : « {r['question']} » "
        f"(date limite : {r['date']}). Proposition à contrôler : statut = {prop.get('statut')}, réponse = « {prop.get('reponse')} ». "
        'Réponds UNIQUEMENT par un objet JSON : {"statut": "arrive" | "pas_arrive" | "incertain", '
        '"scenario": "favorable" | "stable" | "degrade" | null}. Réponds « incertain » au moindre doute.')


def appel_modele(prompt, modele, cle):
    from generate_daily_edition import call_openrouter
    res, usage = call_openrouter(prompt, modele, cle, temperature=0.1, max_tokens=12000, timeout=220, tools=OUTILS)
    return res, (usage or {}).get("cost") or 0.0


def traiter(r, jour, racine, cle, appel=appel_modele, pages=controles.charger_page):
    """Retourne (resultat|None, motifs, cout)."""
    scen = g.scenarios_edition(racine, r["editions"][0]) if r.get("editions") else {}
    try:
        prop, c1 = appel(prompt_recherche(r, jour, scen), MODELE, cle)
    except Exception as e:  # noqa: BLE001
        return None, [f"appel du modèle impossible : {str(e)[:120]}"], 0.0
    d_ed = date.fromisoformat(r["editions"][0]) if r.get("editions") else None
    ok, motifs, res = controles.verifier(r, prop if isinstance(prop, dict) else {}, jour, d_ed, pages)
    if not ok:
        return None, motifs, c1
    try:
        conf, c2 = appel(prompt_confirmation(r, jour, prop), MODELE_CONFIRMATION, cle)
    except Exception as e:  # noqa: BLE001
        return None, [f"confirmation impossible : {str(e)[:120]}"], c1
    if not isinstance(conf, dict) or conf.get("statut") != res["statut"]:
        return None, ["le second modèle ne confirme pas le constat"], c1 + c2
    if conf.get("scenario") != res["scenario"]:
        res["scenario"] = None   # désaccord sur le scénario : la réponse ne tranche pas
    res["controle"] = {"date": jour.isoformat(), "modeles": [MODELE, MODELE_CONFIRMATION], "sources_verifiees": len(res["sources"])}
    return res, [], c1 + c2


def rapport(lignes, jour, cout, dry):
    L = [f"# Vérification des résultats — {jour.strftime('%d/%m/%Y')}", "",
         f"Modèles : `{MODELE}` (recherche), `{MODELE_CONFIRMATION}` (confirmation) · coût : {cout:.4f} $" + (" · **à vide**" if dry else ""),
         "Un résultat n'est publié que si tous les contrôles passent (citations retrouvées dans les pages, chiffres, dates, "
         "2 sources de domaines différents, confirmation indépendante).", ""]
    if not lignes:
        L.append("Aucun rendez-vous à vérifier aujourd'hui.")
    for rid, question, issue in lignes:
        L.append(f"## {question} (`{rid}`)")
        L.append(issue)
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--rapport", default=str(RACINE / "data" / "a-venir-verification.md"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    jour = date.fromisoformat(a.date) if a.date else g.aujourdhui()
    rv = g.charger()
    journal = json.loads(JOURNAL.read_text(encoding="utf-8")) if JOURNAL.exists() else {}
    cands = candidats(rv, journal, jour)
    cle = os.environ.get("OPENROUTER_API_KEY")
    if cands and not a.dry_run and not cle:
        print("ERREUR : OPENROUTER_API_KEY absent.", file=sys.stderr)
        return 1
    patch, essais, lignes, cout = {}, {}, [], 0.0
    for r in cands:
        if a.dry_run:
            lignes.append((r["id"], r["question"], "À vérifier (à vide, aucun appel)."))
            continue
        res, motifs, c = traiter(r, jour, RACINE, cle)
        cout += c
        if not res and motifs and motifs[0].startswith(PANNES):
            # Panne technique (modèle injoignable, dépendance absente) : pas un essai, on réessaiera au prochain passage.
            lignes.append((r["id"], r["question"], "**Non vérifié (panne technique, nouvel essai au prochain passage)** : " + " ; ".join(motifs)))
            continue
        essais[r["id"]] = {"dernier_essai": jour.isoformat(), "essais": journal.get(r["id"], {}).get("essais", 0) + 1,
                           "motif": "; ".join(motifs)[:400] if motifs else "accepté"}
        if res:
            patch[r["id"]] = res
            lignes.append((r["id"], r["question"], f"**Accepté** : {res['statut']} — {res['reponse']}"))
        else:
            lignes.append((r["id"], r["question"], "**Refusé, reste à vérifier** : " + " ; ".join(motifs)))
    Path(a.sortie).write_text(json.dumps({"resultats": patch, "journal": essais}, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(a.rapport).write_text(rapport(lignes, jour, cout, a.dry_run) + "\n", encoding="utf-8")
    print(rapport(lignes, jour, cout, a.dry_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
