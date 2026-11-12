#!/usr/bin/env python3
"""Reprend dans data/a-venir.json chaque échéance à venir de la file de sujets (data/sujets.json).

Un rendez-vous créé ici porte le champ « source » valant « sujets ». Il n'est mis à jour que pour ces champs-là :
un rendez-vous écrit à la main n'est jamais modifié. Un rendez-vous auto-créé dont le sujet a
disparu de la file est retiré, sauf s'il porte déjà un résultat.
Usage : python3 scripts/a_venir/synchro_sujets.py [--date AAAA-MM-JJ]
"""
import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "scripts" / "edition"))
import sujets as sj  # noqa: E402

A_VENIR = RACINE / "data" / "a-venir.json"
SOURCE = "sujets"
DOMAINE = {
    "geopolitique": "Géopolitique", "economie": "Économie", "actualite_francaise": "Politique",
    "sport": "Sport", "sciences": "Technologie", "culture": "Culture",
}
QUI = "Veille de la file des sujets"
NATURE = "Échéance repérée dans la file des sujets"


def sans_pourcent(texte):
    """La page n'affiche pas de « % » (pas de probabilités) : chiffres en « pour cent »."""
    return re.sub(r"(\d) %", r"\1 pour cent", texte).replace("%", " pour cent")


def domaine_de(sec_cle, e, table):
    if sec_cle == "carte_blanche":
        cle = sj.registre_du_sujet(e, table)
        return DOMAINE.get(cle, "Politique")
    return DOMAINE.get(sec_cle, "Politique")


def desires(data, aujourdhui):
    """Un rendez-vous par échéance à venir, d'après la file (tous statuts)."""
    table = sj.charger_registres_tags()
    voulus = {}
    for sec_cle, e in ((s["cle"], x) for s in data["sections"] for x in s["entrees"] if x.get("type") == "sujet"):
        ech = e.get("echeance")
        if not ech or not ech.get("date") or sec_cle == "priorite_absolue":
            continue
        if ech["date"] < aujourdhui.isoformat():
            continue
        voulus[e["id"]] = {
            "id": e["id"],
            "date": ech["date"],
            "precision": "limite",
            "domaine": domaine_de(sec_cle, e, table),
            "question": sans_pourcent(sj.bare(e["titre"])),
            "commentaire": sans_pourcent(ech.get("raison") or "Échéance repérée dans la file des sujets."),
            "editions": [],
            "qui": QUI,
            "nature": NATURE,
            "officiel": False,
            "calendrier": "date_limite",
            "source": SOURCE,
        }
    return voulus


def synchroniser(donnees, voulus, sujets_ids):
    """Met à jour data['rendez_vous'] ; renvoie (ajoutés, mis à jour, retirés)."""
    liste = donnees["rendez_vous"]
    par_id = {r["id"]: r for r in liste}
    ajoutes, maj, retires = 0, 0, []
    for ident, v in voulus.items():
        r = par_id.get(ident)
        if r is None:
            liste.append(v)
            ajoutes += 1
            continue
        if r.get("source") != SOURCE:
            continue  # écrit à la main : jamais modifié
        champs = ("date", "domaine", "question", "commentaire")
        if any(r.get(c) != v[c] for c in champs):
            for c in champs:
                r[c] = v[c]
            maj += 1
    for r in list(liste):
        if r.get("source") == SOURCE and r["id"] not in voulus and "resultat" not in r and r["id"] not in sujets_ids:
            liste.remove(r)
            retires.append(r["id"])
    return ajoutes, maj, retires


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="AAAA-MM-JJ (défaut : aujourd'hui, Paris)")
    a = ap.parse_args(argv)
    aujourdhui = date.fromisoformat(a.date) if a.date else datetime.now(ZoneInfo("Europe/Paris")).date()
    data, _ = sj.load_synced()
    donnees = json.loads(A_VENIR.read_text(encoding="utf-8"))
    voulus = desires(data, aujourdhui)
    sujets_ids = {e["id"] for _, e in sj.sujets(data)}
    ajoutes, maj, retires = synchroniser(donnees, voulus, sujets_ids)
    if ajoutes or maj or retires:
        A_VENIR.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"synchro À venir : {ajoutes} ajouté(s), {maj} mis à jour, {len(retires)} retiré(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
