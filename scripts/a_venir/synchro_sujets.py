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
FERMES = RACINE / "data" / "echeances-fermes.json"  # échéances à date ferme, par identifiant de sujet
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


MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def titre_evenement(ech):
    """Titre de la carte : l'intitulé de l'événement et sa date. Jamais le titre du sujet,
    qui est un titre d'article ou d'édition."""
    d = date.fromisoformat(ech["date"])
    return sans_pourcent(f"{ech['evenement'].rstrip('.')} : {d.day} {MOIS[d.month - 1]} {d.year}")


def domaine_de(sec_cle, e, table):
    if sec_cle == "carte_blanche":
        cle = sj.registre_du_sujet(e, table)
        return DOMAINE.get(cle, "Politique")
    return DOMAINE.get(sec_cle, "Politique")


def desires(data, aujourdhui, fermes=None):
    """Un rendez-vous par événement à date ferme à venir. Plusieurs sujets sur le même événement
    (même intitulé, même date) forment une seule carte, rattachée à toutes leurs éditions."""
    if fermes is None:
        fermes = json.loads(FERMES.read_text(encoding="utf-8")) if FERMES.exists() else {}
    table = sj.charger_registres_tags()
    voulus = {}
    for sec_cle, e in ((s["cle"], x) for s in data["sections"] for x in s["entrees"] if x.get("type") == "sujet"):
        fixe = fermes.get(e["id"])
        ech = dict(e.get("echeance") or {}, **(fixe or {}))
        if not fixe or not ech.get("date") or sec_cle == "priorite_absolue":
            continue
        if ech["date"] < aujourdhui.isoformat():
            continue
        cle = (ech["evenement"], ech["date"])
        ident = "evt-" + sj.slugify(ech["evenement"], 50) + "-" + ech["date"]
        r = voulus.get(ident)
        if r is None:
            r = voulus[ident] = {
                "id": ident,
                "date": ech["date"],
                "precision": ech["precision"],
                "domaine": domaine_de(sec_cle, e, table),
                "question": titre_evenement(ech),
                "commentaire": sans_pourcent(ech["nature"].rstrip(".") + "."),
                "editions": [],
                "qui": ech["qui"],
                "nature": ech["nature"],
                "officiel": bool(ech["officiel"]),
                "calendrier": ech["calendrier"],
                "source": SOURCE,
            }
        if e.get("edition") and e["edition"] not in r["editions"]:
            r["editions"].append(e["edition"])
            r["editions"].sort()
    return voulus


def synchroniser(donnees, voulus, sujets_ids):
    """Met à jour data['rendez_vous'] ; renvoie (ajoutés, mis à jour, retirés)."""
    liste = donnees["rendez_vous"]
    par_id = {r["id"]: r for r in liste}
    ajoutes, maj, retires = 0, 0, []
    champs = ("date", "precision", "domaine", "question", "commentaire", "editions", "qui", "nature", "officiel", "calendrier")
    for ident, v in voulus.items():
        r = par_id.get(ident)
        if r is None:
            liste.append(v)
            ajoutes += 1
            continue
        if r.get("source") != SOURCE:
            continue  # écrit à la main : jamais modifié
        if any(r.get(c) != v[c] for c in champs):
            for c in champs:
                r[c] = v[c]
            maj += 1
    for r in list(liste):
        if r.get("source") == SOURCE and r["id"] not in voulus and "resultat" not in r:
            liste.remove(r)
            retires.append(r["id"])
    return ajoutes, maj, retires


CHAMPS_FIXES = ("evenement", "precision", "qui", "nature", "officiel", "calendrier")
PRECISIONS = {"jour", "limite", "fin_mois", "mois", "fin_annee"}
CALENDRIERS = {"date_fixee", "date_limite", "periode_annoncee", "non_programme"}


def valider_fixe(champs):
    """Renvoie les champs « fermes » normalisés, ou None si un champ manque ou est douteux.
    Règle : une échéance n'est ferme que si toutes les informations sont claires."""
    if not isinstance(champs, dict) or champs.get("ferme") is not True:
        return None
    if any(not str(champs.get(c, "")).strip() for c in ("evenement", "qui", "nature")):
        return None
    if champs.get("precision") not in PRECISIONS or champs.get("calendrier") not in CALENDRIERS:
        return None
    if not isinstance(champs.get("officiel"), bool):
        return None
    return {"ferme": True, **{c: champs[c] for c in CHAMPS_FIXES}}


def enregistrer_fixe(ident, champs):
    """Écrit (ou remplace) les champs fermes d'un sujet dans data/echeances-fermes.json."""
    fermes = json.loads(FERMES.read_text(encoding="utf-8")) if FERMES.exists() else {}
    fermes[ident] = champs
    FERMES.write_text(json.dumps(dict(sorted(fermes.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
