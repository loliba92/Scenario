#!/usr/bin/env python3
"""File d'attente éditoriale : source de vérité structurée + vue Markdown.

`data/sujets.json` est la source de vérité de la file de sujets.
`sujets-prioritaires.md` en est la VUE lisible, générée par ce module : elle garde
exactement le format que les anciens lecteurs attendent (dashboard, brief de
secours, routine), si bien qu'ils n'ont pas eu à changer.

Pourquoi : jusqu'ici tout reposait sur du texte libre. Le lien entre une édition
publiée et sa ligne était une phrase recopiée ; un seul caractère de différence
(puce, tag final) et la case n'était jamais cochée, le sujet revenait en tête de
file et risquait d'être republié (« pop culture » le 26/09, « Bitcoin » le 01/10).
Chaque sujet a maintenant un identifiant stable (`id`) ; une édition publiée le
cite (`sujet.origine_id` dans le brief) et le statut se met à jour par
identifiant, sans correspondance de texte.

Qui écrit quoi : les scripts (cochage après publication, veille) passent par ce
module. Un humain peut modifier SOIT le JSON, SOIT le Markdown : `load_synced()`
détecte lequel a changé depuis la dernière génération (empreinte
`meta.md_sha256`) et reprend la modification dans l'autre. Si les deux ont changé
en même temps, il refuse et le dit (jamais de modification perdue en silence).

Utilisation en ligne de commande :
    python scripts/edition/sujets.py check     # vérifie la cohérence (CI)
    python scripts/edition/sujets.py sync      # reprend une modification manuelle
    python scripts/edition/sujets.py stats     # suivi par registre
    python scripts/edition/sujets.py import    # Markdown -> JSON (migration initiale)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "sujets.json"
MD_PATH = ROOT / "sujets-prioritaires.md"
ARCHIVES_DIR = ROOT / "archives"
BRIEFS_DIR = ROOT / "editorial-briefs"

VERSION = 1
STATUTS = ("a_traiter", "publie")
VALIDATIONS = ("valide", "a_valider")
MARQUE_A_VALIDER = "🔍"

BANNER = (
    "<!-- FICHIER GÉNÉRÉ depuis data/sujets.json (source de vérité) par "
    "scripts/edition/sujets.py — ne pas réécrire les identifiants. Vous pouvez "
    "modifier ce fichier OU data/sujets.json : la modification est reprise dans "
    "l'autre au prochain passage (python scripts/edition/sujets.py sync). -->"
)

# Titre de section (début) -> clé stable. Mêmes clés que generate_hot_topics.REGISTRE_HEADINGS.
_CLES = (
    ("🔥 Priorité absolue", "priorite_absolue"),
    ("Mardi — carte blanche", "carte_blanche"),
    ("Géopolitique", "geopolitique"),
    ("Sport", "sport"),
    ("Actualité & politique française", "actualite_francaise"),
    ("Sciences", "sciences"),
    ("Culture", "culture"),
    ("Économie & finance mondiale", "economie"),
)
_JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
_MOIS = {m: i + 1 for i, m in enumerate(
    ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
     "septembre", "octobre", "novembre", "décembre"])}

_ITEM_RE = re.compile(r"^- \[([ xX])\] (.*)$")


class SujetsError(Exception):
    pass


class SujetsConflict(SujetsError):
    """Le JSON et le Markdown ont tous deux changé depuis la dernière génération."""


# --------------------------------------------------------------------------- utilitaires
def deburr(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", deburr(s)).strip()


def slugify(s: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", deburr(s)).strip("-")
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit("-", 1)[0] or slug[:max_len]
    return slug or "sujet"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bare(raw: str | None) -> str:
    """Texte d'un sujet sans puce « - [ ] », sans 🔍 et sans tag final [..]."""
    t = re.sub(r"^\s*-\s*\[[ xX]\]\s*", "", raw or "").strip()
    t = re.sub(r"^" + MARQUE_A_VALIDER + r"\s*", "", t)
    return re.sub(r"\s*\[[^\]\n]*\]\s*$", "", t).strip()


def _cle_pour(titre: str) -> str:
    for debut, cle in _CLES:
        if titre.startswith(debut):
            return cle
    return slugify(titre).replace("-", "_")


def _jour_pour(titre: str):
    m = re.search(r"—\s*(" + "|".join(_JOURS) + r")\b", titre, re.I)
    return m.group(1).lower() if m else None


def _date_ajout(note: str | None):
    if not note:
        return None
    m = re.search(r"[Aa]jouté(?: automatiquement)? le (\d{4}-\d{2}-\d{2})", note)
    if m:
        return m.group(1)
    m = re.search(r"[Aa]jouté(?: automatiquement)? le (\d{1,2})(?:er)? (" + "|".join(_MOIS) + r") (\d{4})", note)
    if m:
        return f"{m.group(3)}-{_MOIS[m.group(2)]:02d}-{int(m.group(1)):02d}"
    return None


# --------------------------------------------------------------------------- Markdown -> données
def _lire_commentaire(lignes: list[str], i: int):
    """Lit un commentaire HTML (une ou plusieurs lignes) commençant à lignes[i].
    Renvoie (texte intérieur, index de la ligne suivante)."""
    buf = []
    j = i
    while j < len(lignes):
        buf.append(lignes[j])
        if "-->" in lignes[j]:
            break
        j += 1
    else:
        raise SujetsError(f"commentaire HTML jamais fermé (ligne {i + 1})")
    brut = "\n".join(buf)
    interieur = brut[brut.index("<!--") + 4: brut.rindex("-->")]
    texte = "\n".join(l.strip() for l in interieur.strip().split("\n")).strip()
    return texte, j + 1


def parse_md(text: str, precedent: dict | None = None) -> dict:
    """Markdown -> données. Les identifiants lus dans les `<!-- id: .. -->` sont
    conservés ; un sujet sans identifiant en reçoit un, en réutilisant celui du
    sujet précédent de même texte (métadonnées reprises) s'il existe."""
    lignes = text.split("\n")
    # En-tête : tout ce qui précède la première section, sans la bannière.
    premier = next((n for n, l in enumerate(lignes) if l.startswith("## ")), None)
    if premier is None:
        raise SujetsError("aucune section « ## » trouvée")
    entete = "\n".join(lignes[:premier]).strip()
    entete = re.sub(r"^<!-- FICHIER GÉNÉRÉ.*?-->\s*", "", entete, flags=re.S).strip()

    anciens = {}
    if precedent:
        for s in precedent.get("sections", []):
            for e in s["entrees"]:
                if e["type"] == "sujet":
                    anciens.setdefault((s["cle"], norm(e["texte"])), e)

    sections = []
    ids_pris: set[str] = set()
    i = premier
    while i < len(lignes):
        titre = lignes[i][3:].strip()
        sec = {"cle": _cle_pour(titre), "titre": titre, "jour": _jour_pour(titre), "entrees": []}
        i += 1
        dernier = None            # dernier sujet, pour lui rattacher ses notes
        collant = False           # la ligne précédente faisait partie de ce sujet
        while i < len(lignes) and not lignes[i].startswith("## "):
            l = lignes[i]
            m = _ITEM_RE.match(l)
            if m:
                rest = m.group(2).rstrip()
                valid = "valide"
                if rest.startswith(MARQUE_A_VALIDER):
                    valid = "a_valider"
                    rest = rest[len(MARQUE_A_VALIDER):].lstrip()
                tag = None
                mt = re.search(r" \[([^\]\n]*)\]$", rest)
                if mt:
                    tag = mt.group(1).strip() or None
                    rest = rest[:mt.start()].rstrip()
                dernier = {
                    "type": "sujet", "id": None, "texte": rest, "tag": tag,
                    "statut": "publie" if m.group(1) in "xX" else "a_traiter",
                    "validation": valid, "note": None,
                    "ajoute_le": None, "publie_le": None, "edition": None,
                }
                sec["entrees"].append(dernier)
                collant = True
                i += 1
                continue
            if l.strip() == "":
                collant = False
                i += 1
                continue
            if l.lstrip().startswith("<!--"):
                texte, i = _lire_commentaire(lignes, i)
                if dernier is not None and collant and l.startswith((" ", "\t")):
                    mid = re.match(r"^id:\s*(\S+)\s*$", texte)
                    if mid:
                        dernier["id"] = mid.group(1)
                    else:
                        dernier["note"] = texte if not dernier["note"] else dernier["note"] + "\n" + texte
                else:
                    sec["entrees"].append({"type": "commentaire", "texte": texte})
                    dernier, collant = None, False
                continue
            raise SujetsError(
                f"ligne inattendue dans la section « {titre} » (ligne {i + 1}) : {l[:80]!r}")
        sections.append(sec)

    # Identifiant « volé » : une ligne insérée à la main entre un sujet et son
    # commentaire `id:` fait rattacher cet identifiant au mauvais sujet. Si le texte
    # d'origine de cet identifiant existe toujours ailleurs dans le fichier, l'identifiant
    # n'est pas à lui ; on l'écarte (le texte retrouve le sien, l'autre en reçoit un neuf).
    # Si l'ancien texte a disparu, c'est une simple correction du texte : on garde l'id.
    textes_md = {(sec["cle"], norm(e["texte"])) for sec in sections for e in sec["entrees"] if e["type"] == "sujet"}
    par_id = {}
    if precedent:
        for ps in precedent.get("sections", []):
            for pe in ps["entrees"]:
                if pe["type"] == "sujet":
                    par_id[pe["id"]] = (ps["cle"], pe)
    for sec in sections:
        for e in sec["entrees"]:
            if e["type"] == "sujet" and e["id"] in par_id:
                pcle, pe = par_id[e["id"]]
                if norm(pe["texte"]) != norm(e["texte"]) and (pcle, norm(pe["texte"])) in textes_md:
                    e["id"] = None

    # Identifiants et métadonnées
    for sec in sections:
        for e in sec["entrees"]:
            if e["type"] != "sujet":
                continue
            ancien = anciens.get((sec["cle"], norm(e["texte"])))
            if ancien is None and e["id"] in par_id:     # texte corrigé, identifiant conservé
                ancien = par_id[e["id"]][1]
            if ancien:                                   # reprise des métadonnées
                for k in ("ajoute_le", "publie_le", "edition"):
                    if e[k] is None:
                        e[k] = ancien.get(k)
                if e["id"] is None:
                    e["id"] = ancien["id"]
            if e["ajoute_le"] is None:
                e["ajoute_le"] = _date_ajout(e["note"])
    for sec in sections:
        for e in sec["entrees"]:
            if e["type"] != "sujet":
                continue
            base = e["id"] or f"{sec['cle'].replace('_', '-')}-{slugify(e['texte'], 48)}"
            ident, n = base, 2
            while ident in ids_pris:
                ident, n = f"{base}-{n}", n + 1
            e["id"] = ident
            ids_pris.add(ident)

    return {"version": VERSION, "meta": {"md_sha256": ""}, "preambule": entete, "sections": sections}


# --------------------------------------------------------------------------- données -> Markdown
def _commentaire(texte: str, indent: str) -> str:
    lignes = texte.split("\n")
    if len(lignes) == 1:
        return f"{indent}<!-- {texte} -->"
    cont = indent + "     "
    return f"{indent}<!-- {lignes[0]}\n" + "\n".join(cont + l for l in lignes[1:]) + " -->"


def render_md(data: dict) -> str:
    out = [BANNER, "", data["preambule"].rstrip()]
    for sec in data["sections"]:
        out += ["", "", f"## {sec['titre']}"]
        for e in sec["entrees"]:
            if e["type"] == "commentaire":
                out.append(_commentaire(e["texte"], ""))
                continue
            case = "x" if e["statut"] == "publie" else " "
            marque = f"{MARQUE_A_VALIDER} " if e["validation"] == "a_valider" else ""
            tag = f" [{e['tag']}]" if e.get("tag") else ""
            out.append(f"- [{case}] {marque}{e['texte']}{tag}")
            out.append(f"  <!-- id: {e['id']} -->")
            if e.get("note"):
                out.append(_commentaire(e["note"], "  "))
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- fichiers et synchronisation
def sujets(data: dict):
    for sec in data["sections"]:
        for e in sec["entrees"]:
            if e["type"] == "sujet":
                yield sec, e


def _dump(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def save_both(data: dict, data_path: Path = DATA_PATH, md_path: Path = MD_PATH) -> None:
    md = render_md(data)
    data["meta"]["md_sha256"] = sha(md)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(_dump(data), encoding="utf-8")
    md_path.write_text(md, encoding="utf-8")


def load_synced(data_path: Path = DATA_PATH, md_path: Path = MD_PATH):
    """Charge les données en reprenant une éventuelle modification manuelle.
    Renvoie (données, action) avec action dans {"ok", "md_repris", "json_repris"}.
    Ne passe jamais à l'écriture : c'est à l'appelant de faire save_both()."""
    if not data_path.exists():
        raise SujetsError(f"{data_path} introuvable — lancer `sujets.py import` (migration initiale)")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    if not md_path.exists():
        return data, "json_repris"
    md = md_path.read_text(encoding="utf-8")
    ref = data.get("meta", {}).get("md_sha256", "")
    md_change = sha(md) != ref
    json_change = sha(render_md(data)) != ref
    if md_change and json_change:
        raise SujetsConflict(
            "data/sujets.json et sujets-prioritaires.md ont été modifiés tous les deux depuis "
            "la dernière génération : conservez une seule des deux modifications (par exemple "
            "`git checkout origin/main -- sujets-prioritaires.md`) puis relancez.")
    if md_change:
        return parse_md(md, data), "md_repris"
    if json_change:
        return data, "json_repris"
    return data, "ok"


# --------------------------------------------------------------------------- cochage et ajout
def check_off(data: dict, brief: dict, publie_le: str | None = None) -> list[str]:
    """Marque « publié » le(s) sujet(s) consommé(s) par l'édition décrite par `brief`.
    D'abord par `sujet.origine_id` (fiable), sinon par le texte (origine_prioritaire,
    titre, h1 : égalité ou début de texte). Toutes les occurrences, car la veille
    ajoute parfois le même sujet dans deux sections. Renvoie les identifiants cochés."""
    sujet = brief.get("sujet") or {}
    jour = publie_le or brief.get("date")
    cochés: list[str] = []

    def marquer(e):
        e["statut"] = "publie"
        e["publie_le"] = jour
        e["edition"] = jour
        cochés.append(e["id"])

    # Identifiant recopié tel quel, éventuellement avec « id: » ou les balises du commentaire.
    ident = re.sub(r"^(?:<!--)?\s*id:\s*|\s*(?:-->)?\s*$", "", (sujet.get("origine_id") or "").strip()).strip()
    if ident:
        for _, e in sujets(data):
            if e["id"] == ident and e["statut"] == "a_traiter":
                marquer(e)
        if cochés:
            return cochés

    candidats = []
    for raw, mini in ((sujet.get("origine_prioritaire"), 1), (sujet.get("titre_propose"), 25), (sujet.get("h1"), 25)):
        c = norm(bare(raw))
        if c and len(c) >= mini and c not in candidats:
            candidats.append(c)
    for c in candidats:
        for _, e in sujets(data):
            if e["statut"] != "a_traiter":
                continue
            t = norm(e["texte"])
            if t == c or t.startswith(c + " "):
                marquer(e)
        if cochés:
            return cochés
    return cochés


def ajouter(data: dict, cle: str, texte: str, tag: str | None = None, note: str | None = None,
            ajoute_le: str | None = None, validation: str = "a_valider") -> dict:
    """Ajoute un sujet EN HAUT de la section `cle` (avant le premier sujet déjà en
    file, après le commentaire d'introduction), comme le faisait la veille."""
    sec = next((s for s in data["sections"] if s["cle"] == cle), None)
    if sec is None:
        raise SujetsError(f"section inconnue : {cle!r}")
    pris = {e["id"] for _, e in sujets(data)}
    base = f"{cle.replace('_', '-')}-{slugify(bare(texte), 48)}"
    ident, n = base, 2
    while ident in pris:
        ident, n = f"{base}-{n}", n + 1
    e = {"type": "sujet", "id": ident, "texte": bare(texte), "tag": tag or None, "statut": "a_traiter",
         "validation": validation, "note": note, "ajoute_le": ajoute_le or date.today().isoformat(),
         "publie_le": None, "edition": None}
    pos = next((k for k, x in enumerate(sec["entrees"]) if x["type"] == "sujet"), len(sec["entrees"]))
    sec["entrees"].insert(pos, e)
    return e


# --------------------------------------------------------------------------- éditions publiées
def editions_publiees(archives_dir: Path = ARCHIVES_DIR, briefs_dir: Path = BRIEFS_DIR) -> dict[str, set[str]]:
    """date -> {titres normalisés} (titre de l'archive + titre/h1 du brief), pour les
    éditions réellement publiées (une archive existe)."""
    res: dict[str, set[str]] = {}
    for f in sorted(archives_dir.glob("2026-*.html")):
        date_ed = f.stem[:10]
        titres = res.setdefault(date_ed, set())
        txt = f.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'<meta property="og:title" content="([^"]*)"', txt)
        if m:
            t = re.sub(r" — Scénario$", "", m.group(1))
            t = t.replace("&#x27;", "'").replace("&amp;", "&").replace("&quot;", '"')
            titres.add(norm(t))
        bf = briefs_dir / f"{date_ed}.json"
        if bf.exists():
            try:
                s = json.loads(bf.read_text(encoding="utf-8")).get("sujet", {})
            except ValueError:
                s = {}
            for k in ("titre_propose", "h1"):
                if s.get(k):
                    titres.add(norm(s[k]))
            if s.get("origine_prioritaire"):          # texte de la ligne d'origine, tel que noté par le brief
                titres.add(norm(bare(s["origine_prioritaire"])))
    return {d: {t for t in ts if len(t) >= 20} for d, ts in res.items()}


def edition_du_sujet(texte: str, editions: dict[str, set[str]]):
    n = norm(texte)
    for d, titres in editions.items():
        if any(n == t or n.startswith(t + " ") for t in titres):
            return d
    return None


def relier_editions(data: dict, editions: dict[str, set[str]]) -> int:
    """Renseigne `publie_le` / `edition` des sujets publiés dont l'édition se retrouve
    par le titre. Renvoie le nombre de sujets reliés. Sans effet sur les autres."""
    n = 0
    for _, e in sujets(data):
        if e["statut"] == "publie" and not e["edition"]:
            d = edition_du_sujet(e["texte"], editions)
            if d:
                e["publie_le"] = e["edition"] = d
                n += 1
    return n


# --------------------------------------------------------------------------- vérifications
def desynchronisation(data: dict, md_text: str):
    """None si le JSON et la vue sont d'accord ; "md" ou "json" si l'un des deux a été
    modifié à la main (se répare tout seul : `sync` reprend la modification dans
    l'autre) ; "conflit" si les deux ont changé (à arbitrer par un humain)."""
    ref = data.get("meta", {}).get("md_sha256", "")
    md_change = sha(md_text) != ref
    json_change = sha(render_md(data)) != ref
    if md_change and json_change:
        return "conflit"
    return "md" if md_change else "json" if json_change else None


def verifier(data: dict, md_text: str | None = None, editions: dict | None = None,
             briefs_dir: Path = BRIEFS_DIR) -> list[str]:
    pb: list[str] = []
    ids: set[str] = set()
    cles: set[str] = set()
    for sec in data.get("sections", []):
        if sec["cle"] in cles:
            pb.append(f"section en double : {sec['cle']}")
        cles.add(sec["cle"])
        for e in sec["entrees"]:
            if e["type"] == "commentaire":
                continue
            if e["type"] != "sujet":
                pb.append(f"{sec['cle']} : type inconnu {e['type']!r}")
                continue
            if not e["id"] or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", e["id"]):
                pb.append(f"identifiant invalide : {e['id']!r}")
            if e["id"] in ids:
                pb.append(f"identifiant en double : {e['id']}")
            ids.add(e["id"])
            if e["statut"] not in STATUTS:
                pb.append(f"{e['id']} : statut invalide {e['statut']!r}")
            if e["validation"] not in VALIDATIONS:
                pb.append(f"{e['id']} : validation invalide {e['validation']!r}")
            if not e["texte"].strip():
                pb.append(f"{e['id']} : texte vide")
            if e["statut"] == "publie" and e["edition"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["edition"]):
                pb.append(f"{e['id']} : date de publication invalide {e['edition']!r}")
    if md_text is not None and desynchronisation(data, md_text) == "conflit":
        pb.append("sujets-prioritaires.md ET data/sujets.json ont changé tous les deux depuis la "
                  "dernière génération (conflit) : en garder un seul des deux, puis relancer "
                  "`python scripts/edition/sujets.py sync`")
    if editions is not None:
        for sec, e in sujets(data):
            if e["statut"] == "a_traiter":
                d = edition_du_sujet(e["texte"], editions)
                if d:
                    pb.append(f"{e['id']} : encore « à traiter » alors qu'une édition du {d} porte ce titre "
                              "(case oubliée ? risque de republication)")
    # Les briefs doivent citer des identifiants qui existent.
    if briefs_dir.exists():
        for bf in sorted(briefs_dir.glob("2026-*.json")):
            try:
                oid = (json.loads(bf.read_text(encoding="utf-8")).get("sujet") or {}).get("origine_id")
            except ValueError:
                continue
            if oid and oid not in ids:
                pb.append(f"{bf.name} : origine_id {oid!r} absent du fichier de sujets")
    return pb


# --------------------------------------------------------------------------- suivi
def stats(data: dict) -> list[dict]:
    lignes = []
    for sec in data["sections"]:
        s = [e for e in sec["entrees"] if e["type"] == "sujet"]
        pub = [e for e in s if e["statut"] == "publie"]
        att = [e for e in s if e["statut"] == "a_traiter"]
        valides = [e for e in att if e["validation"] == "valide"]
        dernier = max((e["edition"] for e in pub if e["edition"]), default=None)
        lignes.append({"cle": sec["cle"], "titre": sec["titre"], "total": len(s), "publies": len(pub),
                       "a_traiter": len(att), "a_valider": len(att) - len(valides),
                       "disponibles": len(valides), "derniere_publication": dernier})
    return lignes


# --------------------------------------------------------------------------- ligne de commande
def _main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("commande", choices=["check", "sync", "stats", "import"])
    args = ap.parse_args(argv)

    if args.commande == "import":
        data = parse_md(MD_PATH.read_text(encoding="utf-8"))
        n = relier_editions(data, editions_publiees())
        save_both(data)
        print(f"import : {sum(1 for _ in sujets(data))} sujets, {n} reliés à une édition → {DATA_PATH.relative_to(ROOT)}")
        return 0

    if args.commande == "sync":
        try:
            data, action = load_synced()
        except SujetsError as e:
            print(f"ERREUR : {e}", file=sys.stderr)
            return 1
        if action != "ok":
            save_both(data)
        print(f"sync : {action}")
        return 0

    if args.commande == "stats":
        data, _ = load_synced()
        print(f"{'registre':32s} {'total':>5s} {'publiés':>8s} {'à traiter':>10s} {'dont à valider':>15s} {'dernière publi.':>16s}")
        for l in stats(data):
            print(f"{l['cle']:32s} {l['total']:5d} {l['publies']:8d} {l['a_traiter']:10d} {l['a_valider']:15d} {str(l['derniere_publication'] or '-'):>16s}")
        return 0

    # check
    try:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"ERREUR : data/sujets.json illisible ({e})", file=sys.stderr)
        return 1
    md = MD_PATH.read_text(encoding="utf-8") if MD_PATH.exists() else ""
    pb = verifier(data, md, editions_publiees())
    ds = desynchronisation(data, md)
    if ds == "md":
        print("::warning::sujets-prioritaires.md modifié à la main : la modification sera reprise dans data/sujets.json (sync)")
    elif ds == "json":
        print("::warning::data/sujets.json modifié à la main : sujets-prioritaires.md sera régénéré (sync)")
    for p in pb:
        print(f"::error::{p}")
    print(f"check : {sum(1 for _ in sujets(data))} sujets, {len(pb)} problème(s)")
    return 1 if pb else 0


if __name__ == "__main__":
    sys.exit(_main())
