#!/usr/bin/env python3
"""Génère une nouvelle archives.html avec tableau auto-construit à partir des données d'articles.

Ce script remplace le manuel archives.html par un tableau structuré:
  Date | Titre | Problématique | Évaluation | France Impact | Domaine

Idempotent — peut être relancé après chaque nouvel article pour mettre à jour le tableau.
"""
import re
import html
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
ARCHIVES_DIR = ROOT / "archives"
SUIVI_DIR = ROOT / "suivi"
GLOSSAIRE_HTML = ROOT / "glossaire.html"
ARCHIVES_HTML = ROOT / "archives.html"
SITE_URL = "https://lesscenarios.fr"
TODAY = datetime.now().isoformat()

FRENCH_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9,
    "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}

# Domaine labels
DOMAIN_LABELS = {
    "economie-entreprises": "Économie & entreprises",
    "politique-institutions": "Politique & institutions",
    "international": "International",
    "sciences-environnement": "Sciences & environnement",
    "tech-numerique": "Tech & numérique",
    "culture-divertissement": "Culture & divertissement",
}

# CSS pour le tableau
ARCHIVES_TABLE_CSS = """
  /* ---- Hero avec photo de fond (archives.html uniquement — .archives-hero
     s'ajoute à .hero partagé, ne modifie pas .hero lui-même donc n'affecte
     aucune autre page). Photo forêt déjà utilisée en générique réseaux
     sociaux (assets/social/pub-photos/, crédit Nikola Tomašić/Pexels),
     dégradé sombre par-dessus pour garder le texte lisible et coller au
     thème sombre du site plutôt que de le rompre. */
  .hero.archives-hero {
    position: relative;
    padding: 96px 0 60px;
    background:
      linear-gradient(180deg, rgba(16,21,28,0.55) 0%, rgba(16,21,28,0.82) 65%, var(--ink) 100%),
      url('assets/social/pub-photos/generique-foret.jpg') center 35% / cover no-repeat;
  }

  .hero.archives-hero .eyebrow,
  .hero.archives-hero h1,
  .hero.archives-hero .dek {
    position: relative;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
  }

  @media (max-width: 600px) {
    .hero.archives-hero {
      padding: 64px 0 44px;
    }
  }

  /* ---- Archives table (scripts/seo/generate_archives_table.py) ---- */
  .archives-table {
    width: 100%;
    max-width: 1200px;
    margin: 32px auto;
    border-collapse: collapse;
    table-layout: fixed;
    font-size: 0.90rem;
    line-height: 1.6;
    background: var(--surface);
    border: 1px solid var(--hairline);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .archives-table thead {
    background: linear-gradient(135deg, var(--surface-2) 0%, var(--surface) 100%);
    border-bottom: 2px solid var(--gold);
  }

  .archives-table th {
    padding: 14px 12px;
    text-align: center;
    font-weight: 700;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.70rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--gold);
  }

  .archives-table th:first-child,
  .archives-table th:nth-child(2),
  .archives-table th:nth-child(3) {
    text-align: left;
  }

  .archives-table tbody tr {
    border-bottom: 1px solid var(--hairline);
    transition: background 0.2s ease;
  }

  .archives-table tbody tr:last-child {
    border-bottom: none;
  }

  .archives-table tbody tr:hover {
    background: var(--surface-2);
  }

  .archives-table td {
    padding: 12px;
    vertical-align: middle;
  }

  .archives-table .col-date {
    font-family: "JetBrains Mono", monospace;
    white-space: nowrap;
    flex-shrink: 0;
    letter-spacing: 0.02em;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    line-height: 1.3;
  }

  .archives-table .date-day {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--paper);
  }

  .archives-table .date-year {
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--paper-dim);
  }

  .archives-table .col-domain {
    font-size: 0.72rem;
    font-family: "JetBrains Mono", monospace;
    font-weight: 600;
    white-space: normal;
    line-height: 1.35;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    text-align: center;
  }

  /* Chaque domaine renvoie vers sa page thématique (themes/{slug}.html) —
     maillage interne : 39 liens contextuels vers les 6 pages, en plus du
     menu déroulant "Archives" du nav (site-wide, mais générique). */
  .archives-table .col-domain a {
    color: var(--paper-dim);
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .archives-table .col-domain a:hover {
    color: var(--gold);
    text-decoration: underline;
  }

  .archives-table .col-title {
    overflow-wrap: break-word;
  }

  /* Titre + lien EN alignés dans un même flex row, TOUJOURS sur une seule
     ligne (nowrap) : EN reste collé au titre au lieu de passer dessous.
     Le titre rétrécit (flex-shrink + min-width:0) pour laisser la place à
     EN plutôt que de le pousser en dessous (le titre a besoin de
     display:-webkit-box pour son clamp 2 lignes, donc on isole ça sur le <a>
     et on gère l'alignement au niveau du wrapper) */
  .archives-table .title-row {
    display: flex;
    align-items: baseline;
    gap: 8px;
    flex-wrap: nowrap;
  }

  .archives-table .col-title a:first-child {
    color: var(--gold);
    text-decoration: none;
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: 0.95rem;
    transition: color 0.2s ease;
    /* Pas de troncage : le titre s'affiche en entier, sur autant de lignes
       que nécessaire. EN reste aligné sur la 1ère ligne (align-items:baseline
       sur .title-row) même quand le titre en fait plusieurs. */
    flex: 1 1 auto;
    min-width: 0;
  }

  .archives-table .col-title a:first-child:hover {
    color: var(--paper);
    text-decoration: underline;
  }

  /* Lien EN : simple texte discret + petite flèche, pas un badge encadré */
  .archives-table .lang-link {
    display: inline-flex;
    align-items: baseline;
    gap: 2px;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.65rem;
    color: var(--paper-dim);
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 0.04em;
    flex-shrink: 0;
    align-self: flex-start;
    transition: color 0.2s ease;
  }

  .archives-table .lang-link:hover {
    color: var(--gold);
    text-decoration: underline;
  }

  /* Badge "Révisé" : sujet mis à jour après publication (voir extract_revised
     dans le script — meta name="revised-on" côté article). Pas d'emoji (règle
     du site), contour or discret pour se distinguer sans crier. */
  .archives-table .revised-badge {
    display: inline-flex;
    align-items: center;
    flex-shrink: 0;
    align-self: flex-start;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--gold);
    border: 1px solid var(--gold);
    border-radius: 3px;
    padding: 2px 6px;
    text-decoration: none;
    cursor: default;
    transition: background 0.2s ease, color 0.2s ease;
  }

  /* Version lien (suivi dédié existant) : cliquable, hover fond or */
  a.revised-badge {
    cursor: pointer;
  }

  a.revised-badge:hover {
    background: var(--gold);
    color: var(--ink);
  }

  .archives-table .col-eval {
    text-align: center;
  }

  .archives-table .eval-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.68rem;
    font-family: "JetBrains Mono", monospace;
    white-space: nowrap;
  }

  /* Notre scénario : badge fond plein (donnée principale du site) */
  .archives-table .eval-badge.eval-favorable {
    background: #5e9c78;
    color: #10151c;
    border: 1px solid #5e9c78;
  }

  .archives-table .eval-badge.eval-stable {
    background: #6f8fae;
    color: #10151c;
    border: 1px solid #6f8fae;
  }

  .archives-table .eval-badge.eval-degrade {
    background: #bd6248;
    color: #10151c;
    border: 1px solid #bd6248;
  }

  .archives-table .eval-label {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .archives-table .eval-pct {
    font-weight: 700;
    font-size: 0.68rem;
  }

  .archives-table .col-france {
    text-align: center;
  }

  /* Impact France : jauge à 7 segments (3 rouges dégradé | 1 bleu neutre |
     3 verts favorable, dans cet ordre gauche→droite) plutôt qu'un label texte
     — reflète l'espérance pondérée des 3 scénarios (voir FRANCE_ESPERANCE_SCALE
     et FRANCE_SCALE_SEGMENTS). Le segment qui correspond au niveau actuel est
     en surbrillance, les 6 autres restent atténués : un repère de position +
     couleur immédiat, le label complet reste dispo au survol (title=). */
  .archives-table .france-scale {
    display: inline-flex;
    gap: 2px;
    align-items: center;
    cursor: default;
  }

  /* Lectures : chiffre cumulé depuis le lancement, écrit dans
     assets/data/reads.json toutes les heures par un GitHub Action
     (.github/workflows/reads.yml — plus par une routine Claude Code depuis
     le 3 septembre, voir docs/routine-audience-prompt.md étape 3ter). JS
     ci-dessous, jamais de valeur écrite en dur ici — cette colonne part
     toujours à "—" tant que le JS n'a pas chargé le JSON. Badge 🔥 posé sur
     le titre de la ligne qui a le plus de lectures, ajouté par le même
     script. Barre : signal visuel "gros/petit" au premier coup d'œil, sans
     avoir à comparer les chiffres entre eux — largeur relative au maximum
     du tableau, calculée aussi côté JS (voir reads_script, aucune valeur
     de largeur écrite ici). */
  .archives-table .col-reads {
    text-align: center;
  }

  .reads-value {
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .reads-num {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.78rem;
    color: var(--paper-dim);
    min-width: 1.6em;
    text-align: right;
  }

  .reads-bar {
    display: inline-block;
    width: 44px;
    height: 4px;
    border-radius: 2px;
    background: var(--hairline);
    overflow: hidden;
    flex: none;
  }

  .reads-bar-fill {
    display: block;
    height: 100%;
    width: 0%;
    border-radius: 2px;
    background: var(--gold);
  }

  .reads-top-badge {
    margin-left: 6px;
    font-size: 0.82em;
  }

  .archives-table .france-scale .seg {
    width: 9px;
    height: 16px;
    border-radius: 2px;
    opacity: 0.25;
    transition: opacity 0.2s ease, transform 0.2s ease;
  }

  .archives-table .france-scale .seg.esp-degrade,
  .archives-table .france-scale .seg.esp-degrade-fort,
  .archives-table .france-scale .seg.esp-degrade-extreme {
    background: #bd6248;
  }

  .archives-table .france-scale .seg.esp-neutre {
    background: #6f8fae;
  }

  .archives-table .france-scale .seg.esp-favorable,
  .archives-table .france-scale .seg.esp-favorable-fort,
  .archives-table .france-scale .seg.esp-favorable-extreme {
    background: #5e9c78;
  }

  .archives-table .france-scale .seg.active {
    opacity: 1;
    transform: scaleY(1.2);
  }

  /* Donnée manquante (pas de scénario/jugement extrait) — distinct visuellement
     de "Neutre" (une vraie valeur calculée), gris discret plutôt qu'une couleur
     de jugement qui laisserait croire à une évaluation qui n'a pas eu lieu. */
  .archives-table .badge-na {
    background: transparent;
    color: var(--paper-dim);
    border: 1.5px dashed var(--hairline);
  }

  @media (max-width: 1200px) and (min-width: 769px) {
    .archives-table {
      font-size: 0.85rem;
    }
    .archives-table th,
    .archives-table td {
      padding: 10px 10px;
    }
  }

  /* ---- Mobile (<768px) : vue carte empilée ----
     Une table à 5 colonnes ne tient pas sur un écran de téléphone : on bascule
     chaque ligne en carte verticale (titre en haut, méta, puis les 2 badges
     en ligne label/valeur). thead est masqué, l'ordre est piloté par `order`. */
  @media (max-width: 768px) {
    .archives-table {
      max-width: 100%;
      margin: 20px auto;
      box-shadow: none;
      font-size: 0.85rem;
    }

    .archives-table thead {
      display: none;
    }

    .archives-table,
    .archives-table tbody {
      display: block;
      width: 100%;
    }

    .archives-table tr {
      display: flex;
      flex-direction: column;
      padding: 16px;
      border-bottom: 1px solid var(--hairline);
    }

    .archives-table tr:last-child {
      border-bottom: none;
    }

    .archives-table td {
      padding: 0;
      border: none;
      text-align: left;
    }

    .archives-table .col-title {
      order: 1;
      padding-bottom: 8px;
    }

    .archives-table .col-date {
      order: 2;
      text-align: left;
      flex-direction: row;
      align-items: baseline;
      gap: 4px;
    }

    /* Sur mobile, jour et année sur la même ligne : la hiérarchie de taille
       desktop (gros jour blanc / petite année grise) ne lit plus comme une
       seule date une fois posée côte à côte au lieu d'empilée — on uniformise. */
    .archives-table .date-day,
    .archives-table .date-year {
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--paper-dim);
    }

    .archives-table .col-domain {
      order: 3;
      text-align: left;
      font-size: 0.68rem;
      margin-bottom: 10px;
    }

    .archives-table .col-eval,
    .archives-table .col-france,
    .archives-table .col-reads {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-top: 1px solid var(--hairline);
      text-align: left;
    }

    .archives-table .col-eval { order: 4; }
    .archives-table .col-france { order: 5; }
    .archives-table .col-reads { order: 6; }

    .archives-table .col-eval::before,
    .archives-table .col-france::before,
    .archives-table .col-reads::before {
      content: attr(data-label);
      font-family: "JetBrains Mono", monospace;
      font-size: 0.62rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--paper-dim);
    }
  }

  @media (max-width: 480px) {
    .archives-table {
      margin: 16px auto;
    }
    .archives-table tr {
      padding: 14px;
    }
    .archives-table .col-title a:first-child {
      font-size: 0.88rem;
    }
  }

  /* ---- Filtres (Domaine / Notre scénario / Impact France) ----
     Réutilise .filter-row / .filter-row-label / .domain-filters / .filter-chip
     / .is-active, déjà stylés dans le <style> partagé de glossaire.html —
     rien à redéfinir, juste le conteneur des 3 lignes + le masquage filtré. */
  .archives-filters {
    max-width: 1200px;
    margin: 0 auto 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  /* Le tableau (desktop) comme les cartes (mobile, tr en display:flex)
     doivent tous deux disparaître complètement quand filtrés */
  .archives-table tbody tr.is-hidden {
    display: none !important;
  }

  /* ---- Légende sous le tableau : explique chaque colonne ---- */
  .archives-legend {
    max-width: 1200px;
    margin: 20px auto 0;
    padding: 18px 22px;
    background: var(--surface);
    border: 1px solid var(--hairline);
    border-radius: 8px;
  }

  .archives-legend-title {
    margin: 0 0 12px;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--gold);
  }

  .archives-legend dl {
    margin: 0;
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: 8px 16px;
  }

  .archives-legend dt {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--paper);
    white-space: nowrap;
  }

  .archives-legend dd {
    margin: 0;
    font-size: 0.82rem;
    color: var(--paper-dim);
    line-height: 1.5;
  }

  .archives-legend dd a {
    color: var(--gold);
  }

  @media (max-width: 600px) {
    .archives-legend {
      padding: 16px;
    }
    .archives-legend dl {
      grid-template-columns: 1fr;
      gap: 2px 0;
    }
    .archives-legend dt {
      margin-top: 10px;
    }
    .archives-legend dt:first-child {
      margin-top: 0;
    }
  }
"""


def extract_title(text):
    """Extrait le titre de la balise <title>."""
    m = re.search(r"<title>([^<]+) — Scénario</title>", text)
    return html.unescape(m.group(1)) if m else None


def extract_question(text):
    """Extrait la problématique du bloc .question-text."""
    m = re.search(r'<p class="question-text">([^<]+)</p>', text)
    if m:
        return html.unescape(m.group(1))
    return None


def _extract_card_judgment(card_content):
    """Extrait le jugement France Impact (favorable/stable/degrade) d'UN card de scénario.

    Lit d'abord l'attribut data-france-impact="..." posé sur la div .france-line
    dans le HTML source (articles récents) — plus robuste que de parser le texte,
    où "favorable" est un sous-mot de "défavorable". Pour les articles plus anciens
    qui n'ont pas cet attribut, retombe sur un parsing du jugement en toutes lettres
    ("Plutôt favorable" / "Neutre" / "Plutôt défavorable"), en testant "défavorable"
    avant "favorable" pour éviter le piège du sous-mot.
    """
    # 1) Attribut data-france-impact (articles récents, fiable)
    attr_m = re.search(r'<div class="france-line" data-france-impact="([^"]+)"', card_content)
    if attr_m:
        return attr_m.group(1)  # "favorable" | "stable" | "degrade"

    # 2) Fallback texte (articles anciens sans l'attribut)
    france_m = re.search(
        r'<div class="france-line"[^>]*>.*?<span class="field-label">Concrètement en France</span>\s*(.*?)</div>',
        card_content,
        re.DOTALL,
    )
    if not france_m:
        return None
    france_text = re.sub(r'<[^>]+>', '', france_m.group(1)).lower()
    if "défavorable" in france_text:
        return "degrade"
    if "favorable" in france_text:
        return "favorable"
    return "stable"  # "Neutre pour la France" et autres formulations stables


def extract_scenarios(text):
    """Extrait les 3 scénarios avec leur pourcentage et leur jugement France Impact respectif.

    Important : le jugement France Impact d'un card est indépendant de son "kind"
    (ex. le scénario "stable" peut très bien avoir un impact France jugé "degrade") —
    c'est justement ce qui permet de calculer une espérance pondérée plus bas.
    """
    scenarios = []
    for card_match in re.finditer(
        r'<article class="card" data-kind="([^"]+)"[^>]*>(.*?)</article>', text, re.DOTALL
    ):
        kind = card_match.group(1)
        card_content = card_match.group(2)

        pct_m = re.search(r'<div class="gauge-num">(\d+)%</div>', card_content)
        percentage = int(pct_m.group(1)) if pct_m else 0

        judgment = _extract_card_judgment(card_content)

        scenarios.append((kind, percentage, judgment))

    return scenarios


# Valeur numérique de chaque jugement pour le calcul de l'espérance pondérée
_JUDGMENT_VALUE = {"favorable": 1, "stable": 0, "degrade": -1}


def compute_france_esperance(scenarios):
    """Calcule l'espérance (valeur pondérée par les probabilités) de l'impact France.

    Chacun des 3 scénarios a un pourcentage (probabilité) et un jugement France Impact
    propre (favorable=+1, stable=0, degrade=-1). L'espérance = Σ(pct_i/100 × valeur_i),
    un score continu dans [-1, 1] — plus fidèle que de ne retenir que le jugement du
    seul scénario le plus probable, qui ignore les deux autres.
    """
    if not scenarios:
        return None
    return sum(
        (pct / 100) * _JUDGMENT_VALUE.get(judgment, 0)
        for _kind, pct, judgment in scenarios
        if judgment is not None
    )


# Barème officiel de l'espérance France Impact — SOURCE UNIQUE, documentée
# dans docs/routine-prompt.md (garder les deux synchronisés si ce barème change).
# Seuils décroissants ; le premier seuil <= value l'emporte.
FRANCE_ESPERANCE_SCALE = [
    (0.8, "Très favorable", "esp-favorable-extreme"),
    (0.4, "Assez favorable", "esp-favorable-fort"),
    (0.15, "Plutôt favorable", "esp-favorable"),
    (-0.15, "Neutre", "esp-neutre"),
    (-0.4, "Plutôt défavorable", "esp-degrade"),
    (-0.8, "Assez défavorable", "esp-degrade-fort"),
    (float("-inf"), "Très défavorable", "esp-degrade-extreme"),
]


# Ordre d'affichage de la jauge à 7 segments (gauche = pire, droite = mieux),
# dérivé de FRANCE_ESPERANCE_SCALE mais dans l'autre sens (celle-ci va du
# meilleur seuil au pire). 3 rouges (dégradé) | 1 bleu (neutre) | 3 verts (favorable).
FRANCE_SCALE_SEGMENTS = list(reversed([css_class for _t, _l, css_class in FRANCE_ESPERANCE_SCALE]))


def render_france_scale(css_class, label):
    """Rend la jauge à 7 segments pour Impact France : le segment qui correspond
    au niveau actuel est en surbrillance, les 6 autres restent atténués — un
    repère visuel immédiat (position + couleur) plutôt qu'un label à lire.
    """
    if not css_class:
        segs = "".join(f'<span class="seg {c}"></span>' for c in FRANCE_SCALE_SEGMENTS)
        return f'<span class="france-scale" title="Non évalué" aria-label="Impact France : non évalué">{segs}</span>'

    segs = "".join(
        f'<span class="seg {c}{" active" if c == css_class else ""}"></span>'
        for c in FRANCE_SCALE_SEGMENTS
    )
    return f'<span class="france-scale" title="{label}" aria-label="Impact France : {label}">{segs}</span>'


def label_esperance(value):
    """Mappe l'espérance (float dans [-1, 1]) à un label nuancé + une classe CSS.

    Applique FRANCE_ESPERANCE_SCALE (7 niveaux symétriques : très / assez /
    plutôt / neutre / plutôt / assez / très — même vocabulaire que les
    mots-repères de probabilité des scénarios, étape 5 de la routine).
    """
    if value is None:
        return None, None
    for threshold, label, css_class in FRANCE_ESPERANCE_SCALE:
        if value >= threshold:
            return label, css_class
    return None, None  # inatteignable : le dernier seuil est -inf


def extract_domain(text):
    """Extrait le domaine de la meta tag."""
    m = re.search(r'<meta name="domain" content="([^"]+)">', text)
    if m:
        return m.group(1)
    return None


def extract_revised(text):
    """Extrait la date de révision de la meta tag, si le sujet a été révisé après publication.

    Convention : <meta name="revised-on" content="AAAA-MM-JJ"> dans le <head>
    de l'archive concernée — posée par la routine de détection/révision au
    moment où elle met à jour un article déjà publié (voir docs/routine-prompt.md).
    Alimente le filtre "Sujet révisé" du nav (lien historique vers
    archives.html?tag=revise, cassé depuis la restructuration du 9 septembre
    tant que ce champ n'est pas relu ici).
    """
    m = re.search(r'<meta name="revised-on" content="([^"]+)">', text)
    if m:
        return m.group(1)
    return None


def parse_french_date(text):
    """Convertit '21 août 2026' ou '1er août 2026' en 'AAAA-MM-JJ'. None si non reconnu."""
    m = re.match(r"(\d{1,2})(?:er)?\s+(\S+)\s+(\d{4})", text.strip(), re.IGNORECASE)
    if not m:
        return None
    day, month_name, year = m.groups()
    month = FRENCH_MONTHS.get(month_name.lower())
    if not month:
        return None
    return f"{year}-{month:02d}-{int(day):02d}"


def build_suivi_mapping():
    """Scanne suivi/*.html (hors _gabarit) et retourne {AAAA-MM-JJ origine: Path du suivi}.

    Le lien de retour (.origin-link vers archives/{date}.html) posé sur chaque
    page de suivi sert d'index inverse — aucun fichier séparé à maintenir.
    """
    mapping = {}
    if not SUIVI_DIR.exists():
        return mapping
    for f in SUIVI_DIR.glob("*.html"):
        if f.stem == "_gabarit":
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(r'class="origin-link" href="\.\./archives/(\d{4}-\d{2}-\d{2})\.html"', text)
        if m:
            mapping[m.group(1)] = f
    return mapping


def extract_latest_suivi_version(suivi_path):
    """Extrait la dernière version d'une page de suivi : date de mise à jour +
    pourcentage courant de chacun des 3 scénarios (kind -> pct).

    "Chaque mise à jour s'ajoute à la précédente, rien n'est réécrit" (convention
    du site, voir docs/routine-detection-prompt.md) : le dernier bloc .version du
    fichier est donc toujours le plus récent, par construction — pas besoin de
    comparer des dates pour le savoir, juste prendre le dernier.
    """
    text = suivi_path.read_text(encoding="utf-8")
    # (?:\s+[^"]*)? évite de matcher class="version-head"/"version-content"/etc. —
    # seul class="version" ou class="version is-update" doit compter comme un bloc
    blocks = re.split(r'<div class="version(?:\s+[^"]*)?">', text)
    if len(blocks) < 2:
        return None, {}
    last_block = blocks[-1]

    date_m = re.search(r'<span class="version-date">([^<]+)</span>', last_block)
    version_date = parse_french_date(date_m.group(1)) if date_m else None

    pcts = {}
    for card_m in re.finditer(
        r'<div class="mini-scenario" data-kind="([^"]+)">(.*?)</div>', last_block, re.DOTALL
    ):
        kind, card_content = card_m.groups()
        # V1+ (mise à jour) : <span class="evo-current">45%</span>
        pct_m = re.search(r'<span class="evo-current">(\d+)%</span>', card_content)
        if not pct_m:
            # V0 (jamais mise à jour, cas où le fichier n'a qu'une version) :
            # <span class="mini-scenario-pct">25%</span>
            pct_m = re.search(r'<span class="mini-scenario-pct">(\d+)%</span>', card_content)
        if pct_m:
            pcts[kind] = int(pct_m.group(1))

    return version_date, pcts


def get_most_probable_scenario(scenarios):
    """Retourne le scénario avec le pourcentage le plus élevé."""
    if not scenarios:
        return (None, None, None)
    best = max(scenarios, key=lambda x: x[1])
    return best[:2]  # Retourne juste (kind, pct), pas france_impact


def parse_article(file_path, suivi_mapping=None):
    """Parse un fichier d'article.

    Si un suivi actif existe pour cette date (suivi_mapping), les pourcentages
    des 3 scénarios sont remplacés par ceux de la DERNIÈRE version du suivi —
    le tableau doit refléter la dernière évaluation d'un sujet mis à jour, pas
    les chiffres figés de l'édition d'origine. Le jugement France Impact de
    chaque scénario (favorable/stable/degrade), lui, reste celui de l'édition
    d'origine : les pages de suivi ne le réestiment pas (voir extract_latest_suivi_version).
    """
    text = file_path.read_text(encoding="utf-8")

    iso_date = file_path.stem
    title = extract_title(text)
    question = extract_question(text)
    scenarios = extract_scenarios(text)
    domain = extract_domain(text)
    revised_on = extract_revised(text)

    suivi_path = (suivi_mapping or {}).get(iso_date)
    if suivi_path:
        suivi_date, updated_pcts = extract_latest_suivi_version(suivi_path)
        if updated_pcts:
            scenarios = [
                (kind, updated_pcts.get(kind, pct), judgment)
                for kind, pct, judgment in scenarios
            ]
        # La date de suivi prime sur un meta revised-on posé à la main : c'est
        # elle qui reflète la vraie dernière mise à jour des chiffres affichés.
        if suivi_date:
            revised_on = suivi_date

    # Extrait le scénario le plus probable (pour le badge "Notre scénario") —
    # sur les pourcentages à jour (suivi appliqué ci-dessus le cas échéant)
    best_scenario = get_most_probable_scenario(scenarios)
    kind, pct = best_scenario if best_scenario[0] else (None, None)

    # Impact France : espérance pondérée sur les 3 scénarios (pondération à jour,
    # jugement d'origine), pas juste le plus probable
    esperance = compute_france_esperance(scenarios)
    france_label, france_css_class = label_esperance(esperance)
    # Groupe large (favorable/neutre/degrade) pour le filtre — les 7 niveaux fins
    # restent affichés sur le badge, mais 7 chips de filtre serait illisible
    if france_css_class and france_css_class.startswith("esp-favorable"):
        france_group = "favorable"
    elif france_css_class and france_css_class.startswith("esp-degrade"):
        france_group = "degrade"
    elif france_css_class == "esp-neutre":
        france_group = "neutre"
    else:
        france_group = None

    return {
        "iso_date": iso_date,
        "title": title,
        "question": question,
        "scenario_kind": kind,
        "scenario_pct": pct,
        "france_esperance": esperance,
        "france_label": france_label,
        "france_css_class": france_css_class,
        "france_group": france_group,
        "domain": domain,
        "revised_on": revised_on,
        "suivi_slug": suivi_path.stem if suivi_path else None,
    }


def format_date_display(iso_date):
    """Convertit AAAA-MM-JJ en JJ.MM sur une ligne, AAAA en dessous (2 spans)."""
    parts = iso_date.split("-")
    return f'<span class="date-day">{parts[2]}.{parts[1]}</span><span class="date-year">{parts[0]}</span>'


def format_date_display_plain(iso_date):
    """Convertit AAAA-MM-JJ en JJ.MM.AAAA, texte brut (pour un attribut title=)."""
    parts = iso_date.split("-")
    return f"{parts[2]}.{parts[1]}.{parts[0]}"


def get_scenario_label(kind):
    """Retourne le label lisible du scénario."""
    labels = {
        "favorable": "Favorable",
        "stable": "Stable",
        "degrade": "Dégradé",
    }
    return labels.get(kind, kind)


def render_table_row(article):
    """Rend une ligne du tableau avec 5 colonnes: Date | Titre | Domaine | Notre scénario | Impact France."""
    domain_label = DOMAIN_LABELS.get(article["domain"], article["domain"])

    # Notre scénario : badge de couleur + % SEULEMENT (pas de texte du scénario)
    kind = article["scenario_kind"]
    pct = article["scenario_pct"]

    if kind and pct:
        scenario_label = get_scenario_label(kind)
        # Badge de couleur avec SEULEMENT le label et le pourcentage
        eval_html = f'''<span class="eval-badge eval-{kind}" data-kind="{kind}">
      <span class="eval-label">{scenario_label}</span>
      <span class="eval-pct">{pct}%</span>
    </span>'''
    else:
        eval_html = '<span class="eval-badge badge-na">Non évalué</span>'

    # Impact France : jauge à 7 segments plutôt qu'un label texte (ex. "Plutôt
    # défavorable" si les 2 scénarios les + probables sont dégradés pour la
    # France, même quand le scénario "stable" l'emporte sur le fond) — voir
    # render_france_scale(). Le label reste dispo au survol (title=/aria-label=).
    france_html = render_france_scale(article["france_css_class"], article["france_label"])

    # Lien EN : lien texte discret, pas un badge encadré — uniquement si la
    # traduction existe vraiment sur disque (bug corrigé le 1er septembre 2026 :
    # le lien était généré inconditionnellement, y compris vers des pages
    # en/archives/AAAA-MM-JJ.html inexistantes pour les éditions non traduites).
    en_archive_path = ROOT / "en" / "archives" / f'{article["iso_date"]}.html'
    en_link = (
        f'<a href="en/archives/{article["iso_date"]}.html" title="Read in English" class="lang-link"><span aria-hidden="true">↗</span> EN</a>'
        if en_archive_path.exists() else ""
    )

    # Badge "Révisé" : discret, pas d'emoji (règle du site) — visible directement
    # sur la ligne, sans attendre que le lecteur clique le filtre "Sujet révisé".
    # Lien vers la page de suivi quand elle existe (donnée à jour du tableau) ;
    # sinon simple indicateur (révision signalée à la main, sans suivi dédié).
    revised_on = article["revised_on"]
    revised_title = f"Sujet révisé le {format_date_display_plain(revised_on)}" if revised_on else ""
    if article["suivi_slug"]:
        revised_badge = f'<a href="suivi/{article["suivi_slug"]}.html" class="revised-badge" title="{revised_title} — voir le suivi">Révisé</a>'
    elif revised_on:
        revised_badge = f'<span class="revised-badge" title="{revised_title}">Révisé</span>'
    else:
        revised_badge = ""

    # Tooltip natif au survol du titre = la problématique de l'édition
    question_attr = f' title="{html.escape(article["question"])}"' if article["question"] else ""

    # data-domain/scenario/france/revised : lus par le JS de filtre (voir render_page)
    # data-date : lu par le JS de lectures (voir reads_script) pour associer chaque
    # ligne à sa clé dans assets/data/reads.json, sans reparser le lien/l'affichage.
    # data-label sur chaque <td> : utilisé par la vue carte mobile (voir CSS @media)
    # Ordre : Date puis Titre en premier (les 2 repères de nav), puis Domaine, puis les 2 badges
    return f"""    <tr data-domain="{article["domain"] or ''}" data-scenario="{kind or ''}" data-france="{article["france_group"] or ''}" data-revised="{'true' if revised_on else 'false'}" data-date="{article["iso_date"]}">
      <td class="col-date" data-label="Date">{format_date_display(article["iso_date"])}</td>
      <td class="col-title">
        <span class="title-row">
          <a href="archives/{article["iso_date"]}.html"{question_attr}>{html.escape(article["title"])}</a>
          {revised_badge}
          {en_link}
        </span>
      </td>
      <td class="col-domain" data-label="Domaine">{f'<a href="themes/{article["domain"]}.html">{domain_label}</a>' if article["domain"] else domain_label}</td>
      <td class="col-eval" data-label="Notre scénario">{eval_html}</td>
      <td class="col-france" data-label="Impact France">{france_html}</td>
      <td class="col-reads" data-label="Lectures">
        <span class="reads-value">
          <span class="reads-num">—</span>
          <span class="reads-bar"><span class="reads-bar-fill"></span></span>
        </span>
      </td>
    </tr>"""


def extract_block(text, start_marker, end_marker, include_end=True):
    """Extrait un bloc HTML."""
    start = text.index(start_marker)
    end = text.index(end_marker, start) + (len(end_marker) if include_end else 0)
    return text[start:end]


def fix_nav_active_link(masthead_nav):
    """Déplace aria-current="page" du lien "Glossaire" (actif dans glossaire.html,
    la page source du gabarit) vers le lien "Archives" (la page qu'on génère).
    Sans ça, le nav copié tel quel affiche "Glossaire" en doré sur archives.html.
    """
    masthead_nav = masthead_nav.replace('<a href="glossaire.html" aria-current="page">', '<a href="glossaire.html">')
    masthead_nav = masthead_nav.replace('<a href="archives.html">', '<a href="archives.html" aria-current="page">')
    return masthead_nav


def build_shared_pieces():
    """Extrait les blocs réutilisables de glossaire.html."""
    text = GLOSSAIRE_HTML.read_text(encoding="utf-8")
    style_block = extract_block(text, "<style>", "</style>")
    masthead_nav = extract_block(text, '<header class="masthead">', "</nav>")
    masthead_nav = fix_nav_active_link(masthead_nav)
    follow_footer = extract_block(text, '<section class="follow-block" id="nous-suivre">', "</footer>")
    tail_scripts = extract_block(
        text,
        '<script data-goatcounter="https://scenario.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>',
        "</html>",
    )
    return style_block, masthead_nav, follow_footer, tail_scripts


def render_page(articles, style_block, masthead_nav, follow_footer, tail_scripts):
    """Rend la page archives.html complète."""
    title = "Archives — Scénario"
    description = f"Archives complètes de Scénario : {len(articles)} éditions avec chacune 3 scénarios chiffrés (favorable, stable, dégradé)."
    url = f"{SITE_URL}/archives.html"

    # Liens vers les 6 pages thématiques, réutilisés dans la légende (maillage
    # interne — en plus des 39 liens contextuels posés sur chaque cellule Domaine)
    theme_links_html = ", ".join(
        f'<a href="themes/{slug}.html">{label}</a>' for slug, label in DOMAIN_LABELS.items()
    )

    # Rend le tableau
    rows_html = "\n".join(render_table_row(article) for article in articles)
    table_html = f"""  <table class="archives-table" id="archives-table">
    <thead>
      <tr>
        <th style="width: 9%;">Date</th>
        <th style="width: 34%;">Titre</th>
        <th style="width: 13%;">Domaine</th>
        <th style="width: 16%;">Notre scénario</th>
        <th style="width: 16%;">Impact France</th>
        <th style="width: 12%;">Lectures</th>
      </tr>
    </thead>
    <tbody>
{rows_html}
    </tbody>
  </table>"""

    # Filtres (Domaine / Notre scénario / Impact France) : chips générées côté
    # Python à partir des valeurs réellement présentes dans les articles, pas
    # d'une liste figée — un chip pour un domaine sans aucune édition n'a pas
    # d'intérêt. Le filtrage lui-même est un petit JS vanilla (voir plus bas),
    # même pattern que le filtre de glossaire.html (.filter-chip/.is-active).
    scenario_labels = {"favorable": "Favorable", "stable": "Stable", "degrade": "Dégradé"}
    # Labels volontairement différents de "Notre scénario" (favorable/stable/dégradé)
    # pour éviter l'ambiguïté : ici on filtre un effet (positif/neutre/négatif),
    # pas un scénario — même si les valeurs data-filter internes restent identiques.
    france_group_labels = {"favorable": "Positif", "neutre": "Neutre", "degrade": "Négatif"}

    def chip_group(group_id, label, values_present, value_labels, ordered_values):
        chips = ['<button type="button" class="filter-chip is-active" data-filter="all">Tous</button>']
        for v in ordered_values:
            if v in values_present:
                chips.append(
                    f'<button type="button" class="filter-chip" data-filter="{v}">{value_labels[v]}</button>'
                )
        return f'''      <div class="filter-row">
        <span class="filter-row-label">{label}</span>
        <div class="domain-filters" id="{group_id}" data-field="{group_id.replace('-filters', '')}">
{"".join(chips)}
        </div>
      </div>'''

    domains_present = {a["domain"] for a in articles if a["domain"]}
    scenarios_present = {a["scenario_kind"] for a in articles if a["scenario_kind"]}
    france_groups_present = {a["france_group"] for a in articles if a["france_group"]}
    revised_present = {"true"} if any(a["revised_on"] for a in articles) else set()

    # Chip "Révisé" seulement si au moins une édition l'est (sinon chip inutile,
    # rien à filtrer) — binaire, pas de valeurs multiples comme les 3 autres.
    revised_filter_html = (
        chip_group("revised-filters", "Révisé", revised_present, {"true": "Révisé uniquement"}, ["true"])
        if revised_present else ""
    )

    filters_html = f"""    <div class="archives-filters">
{chip_group("domain-filters", "Domaine", domains_present, DOMAIN_LABELS, list(DOMAIN_LABELS.keys()))}
{chip_group("scenario-filters", "Notre scénario", scenarios_present, scenario_labels, ["favorable", "stable", "degrade"])}
{chip_group("france-filters", "Impact France", france_groups_present, france_group_labels, ["favorable", "neutre", "degrade"])}
{revised_filter_html}
      <p class="no-result" id="archives-no-result">Aucune édition ne correspond à ces filtres.</p>
    </div>"""

    filters_script = """<script>
  (function(){
    var table = document.getElementById('archives-table');
    if(!table){ return; }
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
    var noResult = document.getElementById('archives-no-result');
    var active = { domain: 'all', scenario: 'all', france: 'all', revised: 'all' };

    ['domain-filters', 'scenario-filters', 'france-filters', 'revised-filters'].forEach(function(groupId){
      var box = document.getElementById(groupId);
      if(!box){ return; }
      var field = box.dataset.field;
      box.querySelectorAll('.filter-chip').forEach(function(chip){
        chip.addEventListener('click', function(){
          active[field] = chip.dataset.filter;
          box.querySelectorAll('.filter-chip').forEach(function(c){
            c.classList.toggle('is-active', c === chip);
          });
          apply();
        });
      });
    });

    // Chip "Révisé" pré-activée si on arrive via ?tag=revise (lien historique
    // du nav .masthead-right) — même filtre, juste 2 points d'entrée.
    if(new URLSearchParams(window.location.search).get('tag') === 'revise'){
      var revisedBox = document.getElementById('revised-filters');
      if(revisedBox){
        var revisedChip = revisedBox.querySelector('[data-filter="true"]');
        if(revisedChip){
          active.revised = 'true';
          revisedBox.querySelectorAll('.filter-chip').forEach(function(c){
            c.classList.toggle('is-active', c === revisedChip);
          });
        }
      }
    }

    function apply(){
      var visible = 0;
      rows.forEach(function(row){
        var show = (active.domain === 'all' || row.dataset.domain === active.domain)
          && (active.scenario === 'all' || row.dataset.scenario === active.scenario)
          && (active.france === 'all' || row.dataset.france === active.france)
          && (active.revised === 'all' || row.dataset.revised === active.revised);
        row.classList.toggle('is-hidden', !show);
        if(show){ visible++; }
      });
      if(noResult){ noResult.classList.toggle('is-shown', visible === 0); }
    }

    apply();
  })();
</script>"""

    # Lectures : chargées côté client depuis assets/data/reads.json plutôt
    # qu'injectées ici en dur — ce fichier est régénéré chaque semaine par ce
    # script (domaines/tags), pendant que reads.json est régénéré toutes les
    # heures par un GitHub Action (.github/workflows/reads.yml, zéro session
    # Claude Code — voir docs/routine-audience-prompt.md étape 3ter pour
    # l'historique). Les deux ne se marchent jamais dessus : celui-ci ne
    # connaît jamais le nombre de lectures, seulement où aller le chercher au
    # chargement de la page. Absence du fichier ou erreur réseau : la
    # colonne reste "—", jamais bloquant.
    #
    # Barre "gros/petit" (ajoutée le 3 septembre, retour utilisateur : "met
    # un petit truc visuel pour montrer si gros petit lecture") : largeur en
    # % du maximum de lectures observé sur CETTE page (pas une échelle
    # absolue figée à l'avance — se réajuste naturellement à mesure que le
    # site grandit). Largeur plancher à 4% pour qu'un petit chiffre non nul
    # reste visible, jamais un vrai 0% qui se confondrait avec "pas de
    # donnée" (la colonne "—" gère déjà ce cas séparément).
    reads_script = """<script>
  (function(){
    var table = document.getElementById('archives-table');
    if(!table){ return; }
    fetch('assets/data/reads.json').then(function(res){
      return res.ok ? res.json() : {};
    }).then(function(reads){
      var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
      var known = rows.map(function(row){ return reads[row.dataset.date]; })
        .filter(function(n){ return typeof n === 'number'; });
      var max = known.length ? Math.max.apply(null, known) : 0;
      var bestRow = null, bestCount = -1;
      rows.forEach(function(row){
        var count = reads[row.dataset.date];
        if(typeof count !== 'number'){ return; }
        var numEl = row.querySelector('.reads-num');
        var fillEl = row.querySelector('.reads-bar-fill');
        if(numEl){ numEl.textContent = count; }
        if(fillEl && max > 0){
          fillEl.style.width = Math.max(4, Math.round(count / max * 100)) + '%';
        }
        if(count > bestCount){ bestCount = count; bestRow = row; }
      });
      if(bestRow && bestCount > 0){
        var link = bestRow.querySelector('.col-title a');
        if(link){
          var badge = document.createElement('span');
          badge.className = 'reads-top-badge';
          badge.title = "L'édition la plus lue";
          badge.textContent = '🔥';
          link.insertAdjacentElement('afterend', badge);
        }
      }
    }).catch(function(){ /* colonne déjà à "—" par défaut, rien à faire */ });
  })();
</script>"""

    json_ld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": {html.escape(title)!r},
  "description": {html.escape(description)!r},
  "url": {url!r},
  "isPartOf": {{ "@type": "WebSite", "name": "Scénario", "url": "{SITE_URL}/" }}
}}
</script>'''.replace("'", '"')

    # Injecte le CSS dans le style block
    style_block = style_block.replace("</style>", ARCHIVES_TABLE_CSS + "</style>")

    head = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="assets/logo.svg">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#10151c">
<link rel="apple-touch-icon" href="assets/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Scénario">
<link rel="stylesheet" href="assets/pwa-install.css">
<meta name="description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Scénario">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE_URL}/assets/social/og-image-v2.png">
<meta property="og:image:width" content="2508">
<meta property="og:image:height" content="1412">
<meta property="og:image:alt" content="Scénario — trois scénarios chiffrés pour chaque actualité : favorable, stable, dégradé.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/assets/social/og-image-v2.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
{style_block}
{json_ld}
</head>
"""

    body = f"""<body>

{masthead_nav}

<section class="hero archives-hero">
  <div class="wrap">
    <p class="eyebrow">Archives</p>
    <h1>Toutes les éditions</h1>
    <p class="dek">Nos précédentes éditions de Scénario — chacune analyse un sujet d'actualité avec 3 scénarios chiffrés : favorable, stable, dégradé. Cliquez sur le titre pour voir l'analyse complète.</p>
  </div>
</section>

<section class="listing">
  <div class="wrap">
{filters_html}
{table_html}
    <div class="archives-legend">
      <p class="archives-legend-title">Comment lire ce tableau</p>
      <dl>
        <dt>Date</dt>
        <dd>Date de publication de l'édition.</dd>
        <dt>Titre</dt>
        <dd>Cliquez pour lire l'analyse complète (lien <strong>↗ EN</strong> pour la version anglaise).</dd>
        <dt>Domaine</dt>
        <dd>Catégorie thématique de l'édition (cliquez sur le domaine dans le tableau), l'une des 6 : {theme_links_html}.</dd>
        <dt>Notre scénario</dt>
        <dd>Le plus probable des 3 scénarios de l'édition, avec son pourcentage de probabilité — <strong>favorable</strong> : la problématique se résout plutôt bien ; <strong>stable</strong> : la situation reste proche des conditions actuelles ; <strong>dégradé</strong> : la problématique s'aggrave nettement.</dd>
        <dt>Impact France</dt>
        <dd>Effet attendu pour la France, calculé sur les <strong>3</strong> scénarios pondérés par leur probabilité — pas seulement le plus probable (2 scénarios secondaires peuvent faire pencher la balance). La jauge va du dégradé (rouge, gauche) au favorable (vert, droite) ; le segment en surbrillance indique le niveau — survolez-le pour voir le détail.</dd>
        <dt>Lectures</dt>
        <dd>Nombre de lectures cumulées depuis la publication de l'édition, mis à jour chaque heure — la barre donne un repère visuel rapide (relative au maximum du tableau). 🔥 signale l'édition la plus lue du moment.</dd>
      </dl>
    </div>
    <p style="margin-top:28px"><a href="index.html" style="color:var(--gold);text-decoration:none">← Retour à l'accueil</a></p>
  </div>
</section>

{follow_footer}

{filters_script}

{reads_script}

{tail_scripts}
"""
    return head + body


def main():
    """Génère archives.html."""
    print(f"Parsing {len(list(ARCHIVES_DIR.glob('*.html')))} articles...")

    suivi_mapping = build_suivi_mapping()
    if suivi_mapping:
        print(f"✓ {len(suivi_mapping)} suivi actif(s) trouvé(s) : {', '.join(sorted(suivi_mapping))}")

    articles = []
    for file_path in sorted(ARCHIVES_DIR.glob("*.html"), reverse=True):
        data = parse_article(file_path, suivi_mapping)
        articles.append(data)

    print(f"✓ Parsed {len(articles)} articles")

    # Charge les blocs réutilisables
    style_block, masthead_nav, follow_footer, tail_scripts = build_shared_pieces()

    # Génère la page
    page = render_page(articles, style_block, masthead_nav, follow_footer, tail_scripts)

    # Écrit le fichier
    ARCHIVES_HTML.write_text(page, encoding="utf-8")
    print(f"✓ Generated {ARCHIVES_HTML.name}")


if __name__ == "__main__":
    main()
