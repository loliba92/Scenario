#!/usr/bin/env python3
"""File d'attente éditoriale : source de vérité structurée + vue Markdown.

`data/sujets.json` est la source de vérité de la file de sujets (format v2).
`sujets-prioritaires.md` en est la VUE lisible, générée par ce module, au format que
la routine du matin lit encore.

Pourquoi : jusqu'ici tout reposait sur du texte libre. Le lien entre une édition
publiée et sa ligne était une phrase recopiée ; un seul caractère de différence et la
case n'était jamais cochée, le sujet revenait en tête de file et risquait d'être
republié (« pop culture » le 26/09, « Bitcoin » le 01/10). Et les explications
variaient d'un sujet à l'autre : tantôt un paragraphe, tantôt rien.

Un sujet est maintenant un DOSSIER homogène, pensé pour nourrir la production du brief :

    id            identifiant stable ; le brief le cite (`sujet.origine_id`)
    titre         l'accroche, la question telle qu'elle s'affiche
    question      la problématique précise à issue ouverte (par défaut : le titre)
    contexte      ce qui se passe, faits datés et chiffrés           (OBLIGATOIRE)
    rationnel     pourquoi ce sujet, pourquoi maintenant, pourquoi
                  l'issue est ouverte, ce qui est en jeu             (OBLIGATOIRE)
    mots_cles     mots et requêtes pour chercher les articles        (OBLIGATOIRE, 3+)
    angle, a_verifier, scenarios (brouillon), echeance, sources, origine, note
    statut, validation, ajoute_le, publie_le, edition, enrichi_le

Qui écrit quoi : les scripts (veille, enrichissement, cochage après publication) passent
par ce module. Un humain peut modifier SOIT le JSON, SOIT le Markdown : `load_synced()`
détecte lequel a changé depuis la dernière génération (empreinte `meta.md_sha256`) et
reprend la modification dans l'autre. Les deux changés en même temps : il refuse et le
dit (jamais de modification perdue en silence).

Utilisation en ligne de commande :
    python scripts/edition/sujets.py check              # cohérence (CI)
    python scripts/edition/sujets.py sync               # reprend une modification manuelle
    python scripts/edition/sujets.py stats              # suivi par registre, complétude
    python scripts/edition/sujets.py incomplets         # sujets à enrichir
    python scripts/edition/sujets.py prochain [--registre culture] [--json]   # dossier du sujet du jour
    python scripts/edition/sujets.py timbrer editorial-briefs/AAAA-MM-JJ.json # inscrit le point de départ dans un brief
    python scripts/edition/sujets.py import             # Markdown -> JSON (migration)
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

VERSION = 2
STATUTS = ("a_traiter", "publie")
VALIDATIONS = ("valide", "a_valider")
ORIGINES = ("veille", "utilisateur")
MARQUE_A_VALIDER = "🔍"

# Un dossier est « complet » quand ces trois champs sont renseignés (et assez fournis).
MIN_CONTEXTE = 80
MIN_RATIONNEL = 60
MIN_MOTS_CLES = 3

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
# Jour de la semaine (0 = lundi) -> section traitée ce jour-là.
REGISTRE_DU_JOUR = {0: "geopolitique", 1: "carte_blanche", 2: "actualite_francaise",
                    3: "economie", 4: "sciences", 5: "culture", 6: "sport"}
_JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
_MOIS = {m: i + 1 for i, m in enumerate(
    ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
     "septembre", "octobre", "novembre", "décembre"])}

_ITEM_RE = re.compile(r"^- \[([ xX])\] (.*)$")

# Étiquette (dans la vue Markdown) -> champ. L'ordre est celui d'écriture.
_ETIQUETTES = (
    ("id", "id"), ("question", "question"), ("contexte", "contexte"), ("rationnel", "rationnel"),
    ("angle", "angle"), ("à vérifier", "a_verifier"), ("mots-clés", "mots_cles"),
    ("scénarios (brouillon)", "scenarios"), ("échéance", "echeance"), ("sources", "sources"),
    ("origine", "origine"), ("enrichi", "enrichi_le"), ("note", "note"),
)
_ETIQ_RE = re.compile(
    r"^(" + "|".join(re.escape(e) for e, _ in _ETIQUETTES) + r")\s*:\s*(.*)$", re.S)
_CHAMP_DE = {e: c for e, c in _ETIQUETTES}
_CHAMPS_TEXTE = ("id", "note", "question", "contexte", "rationnel", "angle", "a_verifier", "origine", "enrichi_le")


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


def sujet_vide(**kw) -> dict:
    """Un sujet avec tous les champs du format v2."""
    e = {
        "type": "sujet", "id": None, "titre": "", "question": None, "tag": None,
        "statut": "a_traiter", "validation": "valide",
        "contexte": None, "rationnel": None, "angle": None, "a_verifier": None,
        "mots_cles": [], "scenarios": None, "echeance": None, "sources": [],
        "origine": None, "note": None,
        "ajoute_le": None, "publie_le": None, "edition": None, "enrichi_le": None,
    }
    e.update(kw)
    return e


def _texte(v) -> str:
    return (v or "").strip()


# --------------------------------------------------------------------------- complétude
def manquants(e: dict) -> list[str]:
    """Champs obligatoires absents ou trop maigres d'un dossier."""
    m = []
    if not (_texte(e.get("question")) or _texte(e.get("titre")).endswith("?")):
        m.append("question")
    if len(_texte(e.get("contexte"))) < MIN_CONTEXTE:
        m.append("contexte")
    if len(_texte(e.get("rationnel"))) < MIN_RATIONNEL:
        m.append("rationnel")
    if len([k for k in e.get("mots_cles") or [] if _texte(k)]) < MIN_MOTS_CLES:
        m.append("mots_cles")
    return m


def est_complet(e: dict) -> bool:
    return not manquants(e)


# --------------------------------------------------------------------------- extraction depuis l'ancien format
# Les anciennes notes sont de la prose libre qui contient des segments étiquetés.
_SEG_RE = re.compile(
    r"(?<![\wéèàç])(Problématique(?: à vérifier et sourcer avant rédaction)?|→\s*3 scénarios(?: \(brouillon\))?|"
    r"Sources?|Angle(?: retenu| éditorial)?|À vérifier(?:\s*/\s*(?:chiffrer|sourcer)|\s+et\s+(?:chiffrer|sourcer))*(?: avant rédaction)?|Contexte)\s*:\s*",
    re.I)
_SCEN_RE = re.compile(
    r"favorable\s*=\s*(.*?)\s*;\s*stable\s*=\s*(.*?)\s*;\s*d[ée]grad[ée]\s*=\s*(.*)$", re.S | re.I)


def _nettoyer(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip(" \t\n—-;,.").strip()


_URL_RE = re.compile(r"https?://[^\s;,<>)\]]+")


_META_VEILLE_RE = re.compile(
    r"^\s*Ajouté automatiquement le [\d-]+ \(recherche OpenRouter[^)]*\)\s*—\s*(?:à valider avant de passer en priorité|validé)\.\s*"
    r"(?:Repéré en veille sur le registre [^,]+, remonté ici pour son urgence\.\s*)?")


def _decouper_sources(seg: str) -> list[dict]:
    """« Le Monde (17.09) https://… ; L'Express (18.09) » -> une source par élément, avec son
    lien séparé quand il y en a un (les liens des anciennes notes ont été écrits à la main ou
    par la recherche d'alors : ils sont repris tels quels)."""
    out = []
    for part in re.split(r"\s*;\s*|\n", seg):
        part = part.strip()
        if not part:
            continue
        m = _URL_RE.search(part)
        titre = _nettoyer((part[:m.start()] + part[m.end():]) if m else part)
        out.append({"titre": titre or (m.group(0) if m else part), "url": m.group(0) if m else None})
    return out


def _maj(t: str) -> str:
    """Majuscule à la première lettre (les segments extraits d'une phrase commencent parfois par une minuscule)."""
    for i, c in enumerate(t):
        if c.isalpha():
            return t[:i] + c.upper() + t[i + 1:]
    return t


def structurer_ancien(e: dict) -> dict:
    """Répartit les ANCIENNES données d'un sujet (ligne du fichier + note libre) dans les
    champs du format v2. Rien n'est inventé : chaque phrase est rangée à sa place ou
    laissée dans `note`. Sans effet sur les champs déjà renseignés."""
    note = e.get("note") or ""
    # 1. explication collée à la ligne, après le « ? » : contexte
    m = re.match(r"^(.*?\?)(?:\s+(.*))?$", e["titre"], re.S)
    if m and m.group(2) and m.group(2).strip():
        e["titre"] = m.group(1).strip()
        if not _texte(e["contexte"]):
            e["contexte"] = m.group(2).strip()
    # 2. segments étiquetés de la note
    marques = list(_SEG_RE.finditer(note))
    reste = note[:marques[0].start()] if marques else note
    for i, mk in enumerate(marques):
        fin = marques[i + 1].start() if i + 1 < len(marques) else len(note)
        seg = _nettoyer(note[mk.end():fin])
        lab = deburr(mk.group(1))
        if not seg:
            continue
        if lab.startswith("probl") or lab.startswith("contexte"):
            e["contexte"] = seg if not _texte(e["contexte"]) else e["contexte"] + " " + seg
        elif "scenarios" in lab:
            ms = _SCEN_RE.search(seg)
            if ms and not e["scenarios"]:
                e["scenarios"] = {"favorable": _nettoyer(ms.group(1)), "stable": _nettoyer(ms.group(2)),
                                  "degrade": _nettoyer(ms.group(3))}
            else:
                reste += f" → 3 scénarios : {seg}"
        elif lab.startswith("source"):
            if not e["sources"]:
                e["sources"] = _decouper_sources(seg)
        elif lab.startswith("angle"):
            if not _texte(e["angle"]):
                e["angle"] = seg
        elif lab.startswith("a verifier"):
            if not _texte(e["a_verifier"]):
                e["a_verifier"] = seg
    # Sujets ajoutés par l'ancienne veille : deux phrases de méthode, puis le contenu sans
    # étiquette. Les phrases de méthode restent dans la note, le contenu devient le contexte.
    mv = _META_VEILLE_RE.match(reste)
    if mv:
        contenu = _nettoyer(reste[mv.end():])
        reste = reste[:mv.end()]
        if contenu and not _texte(e["contexte"]):
            e["contexte"] = contenu
    for champ in ("contexte", "angle", "a_verifier"):
        if _texte(e[champ]):
            e[champ] = _maj(e[champ])
    e["note"] = _nettoyer(reste) or None
    # 3. provenance et échéance, quand la note les dit clairement
    if not e["origine"]:
        if re.search(r"[Aa]jouté automatiquement", note):
            e["origine"] = "veille"
        elif re.search(r"suggestion utilisateur|retour utilisateur|id[ée]es? de l'utilisateur|favori #", note):
            e["origine"] = "utilisateur"
    if not e["echeance"]:
        me = re.search(r"à traiter (?:le )?(?:" + "|".join(_JOURS) + r") (\d{1,2}) (" + "|".join(_MOIS) + r")", note, re.I)
        if me:
            annee = (e.get("ajoute_le") or _date_ajout(note) or "2026")[:4]
            e["echeance"] = {"date": f"{annee}-{_MOIS[me.group(2).lower()]:02d}-{int(me.group(1)):02d}",
                             "raison": "jour de traitement indiqué dans la note d'origine"}
    return e


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


def _valeur(champ: str, brut: str):
    brut = brut.strip()
    if champ == "mots_cles":
        return [k.strip() for k in re.split(r"\s*;\s*", brut) if k.strip()]
    if champ == "scenarios":
        ms = _SCEN_RE.search(brut)
        return ({"favorable": ms.group(1).strip(), "stable": ms.group(2).strip(), "degrade": ms.group(3).strip()}
                if ms else None)
    if champ == "echeance":
        m = re.match(r"^(\d{4}-\d{2}-\d{2})(?:\s*—\s*(.*))?$", brut, re.S)
        return {"date": m.group(1), "raison": (m.group(2) or "").strip()} if m else None
    if champ == "sources":
        out = []
        for part in re.split(r"\s*;\s*", brut):
            if not part.strip():
                continue
            mu = re.match(r"^(.*?)\s*<(https?://[^>\s]+)>\s*$", part.strip(), re.S)
            out.append({"titre": mu.group(1).strip(), "url": mu.group(2)} if mu else {"titre": part.strip(), "url": None})
        return out
    return brut or None


def parse_md(text: str, precedent: dict | None = None) -> dict:
    """Markdown -> données. Les identifiants lus dans les `<!-- id: .. -->` sont
    conservés ; un sujet sans identifiant en reçoit un, en réutilisant celui du
    sujet précédent de même titre (métadonnées reprises) s'il existe. Les commentaires
    étiquetés (`contexte:`, `mots-clés:`…) remplissent les champs du dossier ; un
    commentaire sans étiquette est une ancienne note libre, rangée par
    `structurer_ancien()`."""
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
                    anciens.setdefault((s["cle"], norm(e["titre"])), e)

    sections = []
    i = premier
    while i < len(lignes):
        titre = lignes[i][3:].strip()
        sec = {"cle": _cle_pour(titre), "titre": titre, "jour": _jour_pour(titre), "entrees": []}
        i += 1
        dernier = None            # dernier sujet, pour lui rattacher ses commentaires
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
                dernier = sujet_vide(titre=rest, tag=tag, validation=valid,
                                     statut="publie" if m.group(1) in "xX" else "a_traiter")
                dernier["_etiquete"] = False
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
                    me = _ETIQ_RE.match(texte)
                    if me:
                        champ = _CHAMP_DE[me.group(1)]
                        dernier["_etiquete"] = dernier["_etiquete"] or champ != "id"
                        dernier[champ] = ((me.group(2).strip() or None) if champ in _CHAMPS_TEXTE
                                          else _valeur(champ, me.group(2)))
                    else:  # ancienne note libre
                        dernier["note"] = texte if not dernier["note"] else dernier["note"] + "\n" + texte
                else:
                    sec["entrees"].append({"type": "commentaire", "texte": texte})
                    dernier, collant = None, False
                continue
            raise SujetsError(
                f"ligne inattendue dans la section « {titre} » (ligne {i + 1}) : {l[:80]!r}")
        sections.append(sec)

    # Identifiant « volé » : une ligne insérée à la main entre un sujet et son
    # commentaire `id:` fait rattacher cet identifiant au mauvais sujet. Si le titre
    # d'origine de cet identifiant existe toujours ailleurs dans le fichier, l'identifiant
    # n'est pas à lui ; on l'écarte (le titre retrouve le sien, l'autre en reçoit un neuf).
    # Si l'ancien titre a disparu, c'est une simple correction du texte : on garde l'id.
    textes_md = {(sec["cle"], norm(e["titre"])) for sec in sections for e in sec["entrees"] if e["type"] == "sujet"}
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
                if norm(pe["titre"]) != norm(e["titre"]) and (pcle, norm(pe["titre"])) in textes_md:
                    e["id"] = None

    ids_pris: set[str] = set()
    for sec in sections:
        for e in sec["entrees"]:
            if e["type"] != "sujet":
                continue
            if not e.pop("_etiquete"):            # ancien format : ranger la ligne et la note libre
                structurer_ancien(e)
            ancien = anciens.get((sec["cle"], norm(e["titre"])))
            if ancien is None and e["id"] in par_id:     # texte corrigé, identifiant conservé
                ancien = par_id[e["id"]][1]
            if ancien:                                   # reprise des métadonnées absentes de la vue
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
            base = e["id"] or f"{sec['cle'].replace('_', '-')}-{slugify(e['titre'], 48)}"
            ident, n = base, 2
            while ident in ids_pris:
                ident, n = f"{base}-{n}", n + 1
            e["id"] = ident
            ids_pris.add(ident)

    return {"version": VERSION, "meta": {"md_sha256": ""}, "preambule": entete, "sections": sections}


# --------------------------------------------------------------------------- données -> Markdown
def _commentaire(texte: str, indent: str) -> str:
    texte = texte.replace("-->", "‑‑>")
    lignes = texte.split("\n")
    if len(lignes) == 1:
        return f"{indent}<!-- {texte} -->"
    cont = indent + "     "
    return f"{indent}<!-- {lignes[0]}\n" + "\n".join(cont + l for l in lignes[1:]) + " -->"


def _serialiser(champ: str, v) -> str | None:
    if champ == "mots_cles":
        return " ; ".join(v) if v else None
    if champ == "scenarios":
        return (f"favorable = {v['favorable']} ; stable = {v['stable']} ; dégradé = {v['degrade']}" if v else None)
    if champ == "echeance":
        return (f"{v['date']} — {v['raison']}" if v and v.get("raison") else (v["date"] if v else None))
    if champ == "sources":
        return " ; ".join((s["titre"] + (f" <{s['url']}>" if s.get("url") else "")) for s in v) if v else None
    return _texte(v) or None


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
            out.append(f"- [{case}] {marque}{e['titre']}{tag}")
            for etiq, champ in _ETIQUETTES:
                v = e["id"] if champ == "id" else _serialiser(champ, e.get(champ))
                if v:
                    out.append(_commentaire(f"{etiq}: {v}", "  "))
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
    data["version"] = VERSION
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
    if data.get("version") != VERSION:
        raise SujetsError(f"{data_path} est au format v{data.get('version')} : v{VERSION} attendu")
    if not md_path.exists():
        return data, "json_repris"
    md = md_path.read_text(encoding="utf-8")
    ds = desynchronisation(data, md)
    if ds == "conflit":
        raise SujetsConflict(
            "data/sujets.json et sujets-prioritaires.md ont été modifiés tous les deux depuis "
            "la dernière génération : conservez une seule des deux modifications (par exemple "
            "`git checkout origin/main -- sujets-prioritaires.md`) puis relancez.")
    if ds == "md":
        return parse_md(md, data), "md_repris"
    if ds == "json":
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
            for t in (norm(e["titre"]), norm(e.get("question") or "")):
                if t and (t == c or t.startswith(c + " ")):
                    marquer(e)
                    break
        if cochés:
            return cochés
    return cochés


def ajouter(data: dict, cle: str, titre: str, tag: str | None = None, validation: str = "a_valider",
            **champs) -> dict:
    """Ajoute un sujet EN HAUT de la section `cle` (avant le premier sujet déjà en
    file, après le commentaire d'introduction), comme le faisait la veille. `champs` :
    question, contexte, rationnel, angle, a_verifier, mots_cles, scenarios, echeance,
    sources, origine, note, ajoute_le."""
    sec = next((s for s in data["sections"] if s["cle"] == cle), None)
    if sec is None:
        raise SujetsError(f"section inconnue : {cle!r}")
    inconnus = set(champs) - set(sujet_vide())
    if inconnus:
        raise SujetsError(f"champs inconnus : {sorted(inconnus)}")
    pris = {e["id"] for _, e in sujets(data)}
    base = f"{cle.replace('_', '-')}-{slugify(bare(titre), 48)}"
    ident, n = base, 2
    while ident in pris:
        ident, n = f"{base}-{n}", n + 1
    champs.setdefault("ajoute_le", date.today().isoformat())
    e = sujet_vide(id=ident, titre=bare(titre), tag=tag or None, validation=validation, **champs)
    pos = next((k for k, x in enumerate(sec["entrees"]) if x["type"] == "sujet"), len(sec["entrees"]))
    sec["entrees"].insert(pos, e)
    return e


def enrichir(e: dict, champs: dict, jour: str | None = None) -> list[str]:
    """Complète les champs ABSENTS d'un sujet (jamais d'écrasement d'un champ déjà
    renseigné). Renvoie la liste des champs complétés."""
    faits = []
    for k, v in champs.items():
        if k in ("id", "type", "titre", "statut", "validation", "enrichi_le") or k not in e:
            continue
        actuel = e.get(k)
        if k == "mots_cles" and isinstance(v, list):
            # Moins de mots-clés qu'il n'en faut : on COMPLÈTE sans jamais retirer ceux qui existent.
            if len([m for m in (actuel or []) if _texte(m)]) < MIN_MOTS_CLES:
                connus = {m.lower() for m in (actuel or [])}
                ajout = [m for m in v if isinstance(m, str) and m.strip() and m.lower() not in connus]
                if ajout:
                    e[k] = list(actuel or []) + ajout
                    faits.append(k)
            continue
        vide = (not actuel) if not isinstance(actuel, str) else not actuel.strip()
        if vide and v:
            e[k] = v
            faits.append(k)
    if faits:
        e["enrichi_le"] = jour or date.today().isoformat()
    return faits


def valider(data: dict, ids: list[str]) -> tuple[list[str], list[str]]:
    """Passe des sujets « à valider » en « valide » (ils deviennent éligibles au brief du jour).
    Renvoie (ids validés, ids inconnus). Un sujet déjà validé ne change pas."""
    par_id = {e["id"]: e for _, e in sujets(data)}
    faits, inconnus = [], []
    for i in ids:
        e = par_id.get(i)
        if e is None:
            inconnus.append(i)
        elif e["validation"] != "valide":
            e["validation"] = "valide"
            faits.append(i)
    return faits, inconnus


def _retirer(data: dict, ident: str):
    """Sort le sujet `ident` de sa section et le renvoie avec cette section ; (None, None) si absent."""
    for sec in data["sections"]:
        for k, x in enumerate(sec["entrees"]):
            if x["type"] == "sujet" and x["id"] == ident:
                return sec["entrees"].pop(k), sec
    return None, None


def _mettre_en_tete(sec: dict, e: dict) -> None:
    """Insère `e` avant le premier sujet de `sec` (après le commentaire d'introduction)."""
    pos = next((k for k, x in enumerate(sec["entrees"]) if x["type"] == "sujet"), len(sec["entrees"]))
    sec["entrees"].insert(pos, e)


def section_d_origine(data: dict, ident: str) -> dict | None:
    """Section dans laquelle le sujet a été créé, d'après le préfixe de son identifiant
    (« economie-… » -> economie, « actualite-francaise-… » -> actualite_francaise)."""
    return next((s for s in data["sections"]
                 if s["cle"] != "priorite_absolue" and ident.startswith(s["cle"].replace("_", "-") + "-")), None)


def prioriser(data: dict, ids: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Passe des sujets « à traiter » en tête de « 🔥 Priorité absolue » : ils sont traités avant
    tout le reste, quel que soit le registre du jour, et sont validés du même coup.
    Renvoie (ids déplacés, ids inconnus, ids ignorés : déjà en priorité ou déjà publiés)."""
    cible = next(s for s in data["sections"] if s["cle"] == "priorite_absolue")
    par_id = {e["id"]: (sec, e) for sec, e in sujets(data)}
    faits, inconnus, ignores = [], [], []
    for i in ids:
        if i not in par_id:
            inconnus.append(i)
            continue
        sec, e = par_id[i]
        if sec["cle"] == "priorite_absolue" or e["statut"] != "a_traiter":
            ignores.append(i)
            continue
        _retirer(data, i)
        e["validation"] = "valide"
        _mettre_en_tete(cible, e)
        faits.append(i)
    return faits, inconnus, ignores


def deprioriser(data: dict, ids: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Remet en tête de leur registre d'origine des sujets passés en priorité absolue (annule
    `prioriser`). Le registre se déduit du préfixe de l'identifiant ; sans préfixe reconnu, le
    sujet est ignoré. Renvoie (ids déplacés, ids inconnus, ids ignorés)."""
    par_id = {e["id"]: (sec, e) for sec, e in sujets(data)}
    faits, inconnus, ignores = [], [], []
    for i in ids:
        if i not in par_id:
            inconnus.append(i)
            continue
        sec, e = par_id[i]
        origine = section_d_origine(data, i)
        if sec["cle"] != "priorite_absolue" or e["statut"] != "a_traiter" or origine is None:
            ignores.append(i)
            continue
        _retirer(data, i)
        _mettre_en_tete(origine, e)
        faits.append(i)
    return faits, inconnus, ignores


# --------------------------------------------------------------------------- sujet du jour et dossier
def eligible(e: dict) -> bool:
    return e["statut"] == "a_traiter" and e["validation"] == "valide"


def sujet_du_jour(data: dict, registre: str | None = None, jour: date | None = None):
    """(section, sujet) que la routine doit traiter : d'abord le premier sujet éligible de
    « Priorité absolue », sinon le premier éligible de la section du registre du jour
    (`registre`, ou celle du jour de la semaine). None si rien n'est éligible."""
    if registre is None:
        registre = REGISTRE_DU_JOUR[(jour or date.today()).weekday()]
    for cle in ("priorite_absolue", registre):
        sec = next((s for s in data["sections"] if s["cle"] == cle), None)
        if sec:
            for e in sec["entrees"]:
                if e["type"] == "sujet" and eligible(e):
                    return sec, e
    return None


def dossier_texte(sec: dict, e: dict) -> str:
    """Le dossier d'un sujet, en texte clair, prêt à être donné à un modèle ou lu par un
    humain. Les faits du contexte sont des PISTES à vérifier, jamais des faits établis."""
    q = _texte(e.get("question")) or e["titre"]
    out = [f"Identifiant (à recopier dans sujet.origine_id) : {e['id']}",
           f"Registre : {sec['titre']}",
           f"Titre : {e['titre']}"]
    if _texte(e.get("question")) and _texte(e["question"]) != e["titre"]:
        out.append(f"Question à issue ouverte : {q}")
    for etiq, champ in (("Contexte (à vérifier)", "contexte"),
                        ("Problématique (la question que l'édition cherche à trancher, pourquoi l'issue est ouverte)", "rationnel"),
                        ("Angle", "angle"), ("À vérifier / chiffrer avant rédaction", "a_verifier")):
        if _texte(e.get(champ)):
            out.append(f"{etiq} : {_texte(e[champ])}")
    if e.get("mots_cles"):
        out.append("Mots-clés pour chercher les articles : " + " ; ".join(e["mots_cles"]))
    if e.get("scenarios"):
        s = e["scenarios"]
        out.append(f"Scénarios (brouillon, à refaire sur des faits vérifiés) : favorable = {s['favorable']} ; "
                   f"stable = {s['stable']} ; dégradé = {s['degrade']}")
    if e.get("echeance"):
        out.append(f"Échéance : {_serialiser('echeance', e['echeance'])}")
    if e.get("sources"):
        out.append("Pistes de sources : " + _serialiser("sources", e["sources"]))
    if _texte(e.get("note")):
        out.append(f"Note éditoriale : {_texte(e['note'])}")
    m = manquants(e)
    if m:
        out.append("Dossier incomplet (à compenser par ta propre recherche) : " + ", ".join(m))
    return "\n".join(out)


def dossier_json(sec: dict, e: dict) -> dict:
    """Le dossier d'un sujet en JSON : le POINT DE DÉPART donné à la construction du brief.
    Mêmes champs que le fichier de sujets (sans les champs de suivi interne), plus le
    registre et la liste de ce qui manque. Le contexte, les scénarios et les sources y sont
    des PISTES à vérifier, jamais des faits établis."""
    return {
        "id": e["id"], "registre": sec["cle"], "titre": e["titre"],
        "question": _texte(e.get("question")) or e["titre"],
        "contexte": e.get("contexte"), "rationnel": e.get("rationnel"),
        "mots_cles": list(e.get("mots_cles") or []),
        "angle": e.get("angle"), "a_verifier": e.get("a_verifier"),
        "scenarios_brouillon": e.get("scenarios"), "echeance": e.get("echeance"),
        "sources_pistes": list(e.get("sources") or []), "tag": e.get("tag"),
        "origine": e.get("origine"), "note_editoriale": e.get("note"),
        "dossier_incomplet": manquants(e),
    }


def trouver(data: dict, ident: str):
    """(section, sujet) d'après son identifiant, ou None."""
    ident = re.sub(r"^(?:<!--)?\s*id:\s*|\s*(?:-->)?\s*$", "", (ident or "").strip()).strip()
    for sec, e in sujets(data):
        if e["id"] == ident:
            return sec, e
    return None


def timbrer_brief(brief: dict, data: dict) -> str | None:
    """Inscrit dans le brief le dossier du sujet cité par `sujet.origine_id`, comme POINT DE
    DÉPART (`sujet.point_de_depart`) : le brief porte ainsi, noir sur blanc, ce dont il est
    parti (traçabilité, relecture). N'ajoute rien si le brief ne cite aucun sujet de la file.
    Renvoie l'identifiant, ou None. Idempotent (le dossier est remplacé par sa version à jour)."""
    sujet = brief.get("sujet")
    if not isinstance(sujet, dict):
        return None
    trouve = trouver(data, sujet.get("origine_id") or "")
    if not trouve:
        return None
    sec, e = trouve
    sujet["origine_id"] = e["id"]
    sujet["point_de_depart"] = dossier_json(sec, e)
    return e["id"]


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


def edition_du_sujet(titre: str, editions: dict[str, set[str]]):
    n = norm(titre)
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
            d = edition_du_sujet(e["titre"], editions) or (
                edition_du_sujet(e["question"], editions) if e.get("question") else None)
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
    if data.get("version") != VERSION:
        pb.append(f"version {data.get('version')!r} : v{VERSION} attendu")
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
            if not _texte(e.get("titre")):
                pb.append(f"{e['id']} : titre vide")
            if e.get("origine") not in (None, *ORIGINES):
                pb.append(f"{e['id']} : origine invalide {e['origine']!r}")
            if not isinstance(e.get("mots_cles"), list) or any(not isinstance(k, str) for k in e.get("mots_cles", [])):
                pb.append(f"{e['id']} : mots_cles doit être une liste de textes")
            sc = e.get("scenarios")
            if sc is not None and (not isinstance(sc, dict) or set(sc) != {"favorable", "stable", "degrade"}):
                pb.append(f"{e['id']} : scenarios doit avoir favorable, stable, degrade")
            if not isinstance(e.get("sources"), list) or any(not isinstance(s, dict) or "titre" not in s for s in e.get("sources", [])):
                pb.append(f"{e['id']} : sources doit être une liste de {{titre, url}}")
            ec = e.get("echeance")
            if ec is not None and (not isinstance(ec, dict) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(ec.get("date", "")))):
                pb.append(f"{e['id']} : echeance invalide {ec!r}")
            if e["statut"] == "publie" and e["edition"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["edition"]):
                pb.append(f"{e['id']} : date de publication invalide {e['edition']!r}")
    if md_text is not None and desynchronisation(data, md_text) == "conflit":
        pb.append("sujets-prioritaires.md ET data/sujets.json ont changé tous les deux depuis la "
                  "dernière génération (conflit) : en garder un seul des deux, puis relancer "
                  "`python scripts/edition/sujets.py sync`")
    if editions is not None:
        for sec, e in sujets(data):
            if e["statut"] == "a_traiter":
                d = edition_du_sujet(e["titre"], editions)
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
                       "disponibles": len(valides), "complets": sum(1 for e in att if est_complet(e)),
                       "derniere_publication": dernier})
    return lignes


def incomplets(data: dict, seulement_a_traiter: bool = True) -> list[tuple[dict, dict]]:
    """(section, sujet) à enrichir, dans l'ordre de passage (tête de file d'abord)."""
    out = []
    for sec, e in sujets(data):
        if seulement_a_traiter and e["statut"] != "a_traiter":
            continue
        if not est_complet(e):
            out.append((sec, e))
    return out


# --------------------------------------------------------------------------- ligne de commande
def _main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("commande", choices=["check", "sync", "stats", "import", "incomplets", "prochain", "timbrer", "valider", "prioriser", "deprioriser"])
    ap.add_argument("brief", nargs="*", default=[],
                    help="timbrer : chemin du brief (editorial-briefs/AAAA-MM-JJ.json) ; valider / prioriser / deprioriser : identifiants (séparés par des espaces ou des virgules)")
    ap.add_argument("--json", action="store_true", help="prochain : affiche le dossier en JSON (point de départ du brief)")
    ap.add_argument("--registre", default=None, help="prochain : registre (clé de section) ; défaut = registre du jour")
    ap.add_argument("--force", action="store_true", help="import : écrase un data/sujets.json existant (perd ses modifications)")
    args = ap.parse_args(argv)

    if args.commande == "import":
        if DATA_PATH.exists() and not args.force:
            print(f"ERREUR : {DATA_PATH.relative_to(ROOT)} existe déjà — `import` est la migration initiale et "
                  "écraserait toutes les modifications faites depuis. Utiliser `sync` pour reprendre une "
                  "modification manuelle, ou --force pour écraser volontairement.", file=sys.stderr)
            return 1
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
        print(f"{'registre':22s} {'total':>5s} {'publiés':>8s} {'à traiter':>10s} {'à valider':>10s} {'complets':>9s} {'dernière publi.':>16s}")
        for l in stats(data):
            print(f"{l['cle']:22s} {l['total']:5d} {l['publies']:8d} {l['a_traiter']:10d} {l['a_valider']:10d} {l['complets']:9d} {str(l['derniere_publication'] or '-'):>16s}")
        return 0

    if args.commande == "incomplets":
        data, _ = load_synced()
        for sec, e in incomplets(data):
            print(f"{sec['cle']:20s} {e['id'][:60]:60s} manque : {', '.join(manquants(e))}")
        return 0

    if args.commande == "prochain":
        data, _ = load_synced()
        r = sujet_du_jour(data, args.registre)
        if not r:
            print("(aucun sujet éligible : auto-sélection normale)")
            return 0
        print(json.dumps(dossier_json(*r), ensure_ascii=False, indent=2) if args.json else dossier_texte(*r))
        return 0

    if args.commande == "valider":
        ids = [i.strip() for a in args.brief for i in a.split(",") if i.strip()]
        if not ids:
            print("ERREUR : valider demande au moins un identifiant", file=sys.stderr)
            return 1
        data, _ = load_synced()
        faits, inconnus = valider(data, ids)
        for i in inconnus:
            print(f"::warning::valider : identifiant inconnu {i!r}")
        if faits:
            save_both(data)
        print(f"valider : {len(faits)} validé(s), {len(ids) - len(faits) - len(inconnus)} déjà validé(s), {len(inconnus)} inconnu(s)")
        return 1 if inconnus and not faits and len(inconnus) == len(ids) else 0

    if args.commande in ("prioriser", "deprioriser"):
        ids = [i.strip() for a in args.brief for i in a.split(",") if i.strip()]
        if not ids:
            print(f"ERREUR : {args.commande} demande au moins un identifiant", file=sys.stderr)
            return 1
        data, _ = load_synced()
        faits, inconnus, ignores = (prioriser if args.commande == "prioriser" else deprioriser)(data, ids)
        for i in inconnus:
            print(f"::warning::{args.commande} : identifiant inconnu {i!r}")
        for i in ignores:
            print(f"::warning::{args.commande} : {i!r} ignoré (déjà dans cet état, déjà publié, ou registre d'origine introuvable)")
        if faits:
            save_both(data)
        print(f"{args.commande} : {len(faits)} déplacé(s), {len(ignores)} ignoré(s), {len(inconnus)} inconnu(s)")
        return 0

    if args.commande == "timbrer":
        if not args.brief:
            print("ERREUR : timbrer demande le chemin du brief", file=sys.stderr)
            return 1
        data, _ = load_synced()
        chemin = Path(args.brief[0])
        brief = json.loads(chemin.read_text(encoding="utf-8"))
        ident = timbrer_brief(brief, data)
        if not ident:
            print("timbrer : le brief ne cite aucun sujet de la file (sujet.origine_id) — rien à inscrire")
            return 0
        chemin.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"timbrer : dossier de {ident} inscrit dans {chemin} (sujet.point_de_depart)")
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
    n_inc = len(incomplets(data))
    if n_inc:
        print(f"::notice::{n_inc} sujet(s) à traiter ont un dossier incomplet (contexte, rationnel ou mots-clés) : "
              "voir `sujets.py incomplets` ou le workflow d'enrichissement")
    print(f"check : {sum(1 for _ in sujets(data))} sujets, {len(pb)} problème(s)")
    return 1 if pb else 0


if __name__ == "__main__":
    sys.exit(_main())
