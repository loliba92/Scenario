#!/usr/bin/env python3
"""Aligne l'affichage des pages de suivi (suivi/*.html) sur celui des éditions.

Constat (9 octobre 2026) : une page de suivi n'indiquait nulle part sa dernière mise à
jour, cachait « ce qui a changé » derrière un bouton, n'avait pas la ligne de repère du
bandeau des éditions, et son graphique devenait illisible sur téléphone (étiquettes de
6 px, pourcentages finaux superposés).

Ce script ajoute, de façon idempotente (repérée par des marqueurs, donc relançable sans
doublon) et SANS toucher aux zones que `scripts/detection/generate_suivi_update.py`
réécrit (`<h1>`, `evoData`, section `timeline`) :
  - une ligne de repère sous le logo : « Suivi · mis à jour le … · Vn » ;
  - une section « Où en est-on ? » : date de première analyse, nombre de mises à jour,
    liens « Dans ce suivi », et le bloc « Ce qui a changé » (faits, scénarios, conclusion
    de la dernière version) ;
  - des correctifs du graphique (pourcentages qui ne se chevauchent plus, étiquettes
    lisibles sur téléphone) ;
  - le tout alimenté par le contenu de la page elle-même (aucun changement du générateur).

Usage :
    python3 scripts/seo/align_suivi_design.py          # applique à suivi/*.html
    python3 scripts/seo/align_suivi_design.py --check  # code 1 si une page n'est pas à jour
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUIVI_DIR = ROOT / "suivi"

CSS_START, CSS_END = "/* suivi-statut:css:start */", "/* suivi-statut:css:end */"
HTML_START, HTML_END = "<!-- suivi-statut:html:start -->", "<!-- suivi-statut:html:end -->"
JS_START, JS_END = "<!-- suivi-statut:js:start -->", "<!-- suivi-statut:js:end -->"

CSS = f"""  {CSS_START}
  .brand .edition{{
    font-family: "JetBrains Mono", monospace; font-size: 0.74rem; color: var(--paper-dim);
    text-transform: uppercase; letter-spacing: 0.08em;
  }}
  .hero .eyebrow{{
    display: inline-block; margin: 0 0 18px; padding: 5px 12px;
    background: var(--surface); border-left: 3px solid var(--gold); letter-spacing: 0.12em;
  }}
  section.suivi-statut{{ padding: 28px 0 8px; }}
  .suivi-meta{{
    font-family: "JetBrains Mono", monospace; font-size: 0.8rem; color: var(--paper-dim);
    margin: 0 0 18px;
  }}
  .suivi-jump{{
    display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 22px;
    padding: 14px 0; margin: 0 0 24px;
    border-top: 1px solid var(--hairline); border-bottom: 1px solid var(--hairline);
  }}
  .suivi-jump-label{{
    font-family: "JetBrains Mono", monospace; font-size: 0.7rem; text-transform: uppercase;
    letter-spacing: 0.14em; color: var(--paper-dim);
  }}
  .suivi-jump a{{
    font-family: "Fraunces", serif; font-size: 1.05rem; color: var(--paper); text-decoration: none;
    white-space: nowrap;
  }}
  .suivi-jump a:hover{{ color: var(--gold); }}
  .suivi-jump a span{{ color: var(--gold); }}
  .suivi-changes{{
    background: var(--surface); border: 1px solid var(--hairline); border-radius: 14px;
    padding: 22px 24px; margin: 0 0 8px;
  }}
  .suivi-changes-label{{
    display: block; font-family: "JetBrains Mono", monospace; font-size: 0.74rem;
    text-transform: uppercase; letter-spacing: 0.14em; color: var(--gold); margin: 0 0 10px;
  }}
  .suivi-changes h2{{
    font-family: "Fraunces", serif; font-weight: 600; font-size: 1.3rem; line-height: 1.25;
    margin: 0 0 10px;
  }}
  .suivi-changes p{{ margin: 0 0 14px; color: var(--paper-dim); }}
  .suivi-chips{{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 0 0 16px; }}
  .suivi-chip{{
    border: 1px solid var(--hairline); border-radius: 10px; padding: 10px 12px; background: var(--ink, transparent);
  }}
  .suivi-chip-title{{ font-size: 0.86rem; line-height: 1.3; margin: 0 0 6px; color: var(--paper); }}
  .suivi-chip-pct{{ font-family: "Fraunces", serif; font-weight: 700; font-size: 1.35rem; margin: 0; }}
  .suivi-chip-pct small{{
    font-family: "JetBrains Mono", monospace; font-weight: 400; font-size: 0.7rem; color: var(--paper-dim);
  }}
  .suivi-chip[data-kind="favorable"] .suivi-chip-pct{{ color: var(--favorable); }}
  .suivi-chip[data-kind="stable"] .suivi-chip-pct{{ color: var(--stable); }}
  .suivi-chip[data-kind="degrade"] .suivi-chip-pct{{ color: var(--degrade); }}
  .suivi-changes .suivi-conclusion{{ color: var(--paper); margin: 0 0 12px; }}
  .suivi-changes a.suivi-more{{
    font-family: "JetBrains Mono", monospace; font-size: 0.82rem; color: var(--gold);
    text-decoration: none; border-bottom: 1px dotted var(--gold); padding-bottom: 1px;
  }}
  section.evolution, section.timeline{{ scroll-margin-top: 12px; }}
  section.suivi-statut, .suivi-changes{{ scroll-margin-top: 12px; }}
  @media (max-width: 640px){{
    .suivi-chips{{ grid-template-columns: 1fr; gap: 8px; }}
    .suivi-chip{{ display: flex; justify-content: space-between; align-items: center; gap: 12px; }}
    .suivi-chip-title, .suivi-chip-pct{{ margin: 0; }}
    .suivi-chip-pct{{ white-space: nowrap; text-align: right; }}
    .suivi-changes{{ padding: 18px 16px; }}
    .evo-axis-label{{ font-size: 17px; }}
    .evo-pct-label{{ font-size: 22px; }}
  }}
  {CSS_END}
"""

HTML = f"""{HTML_START}
<section class="suivi-statut" id="suivi-statut">
  <div class="wrap">
    <p class="suivi-meta" id="suivi-meta">Suivi d'un sujet</p>
    <nav class="suivi-jump" aria-label="Dans ce suivi">
      <span class="suivi-jump-label">Dans ce suivi</span>
      <a href="#ce-qui-a-change">Ce qui a changé <span aria-hidden="true">↓</span></a>
      <a href="#evolution">L'évolution <span aria-hidden="true">↓</span></a>
      <a href="#historique">L'historique <span aria-hidden="true">↓</span></a>
    </nav>
    <div class="suivi-changes" id="ce-qui-a-change"></div>
  </div>
</section>
{HTML_END}
"""

JS = f"""{JS_START}
<script>
  // Alimenté par le contenu de la page (versions, dates, scénarios) : rien à mettre à jour
  // à la main quand une nouvelle version est ajoutée. Voir scripts/seo/align_suivi_design.py.
  (function(){{
    function txt(n){{ return n ? n.textContent.replace(/\\s+/g, ' ').trim() : ''; }}
    function esc(s){{ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }}
    var evo = document.querySelector('section.evolution'), tl = document.querySelector('section.timeline');
    if(evo && !evo.id) evo.id = 'evolution';
    if(tl && !tl.id) tl.id = 'historique';

    var versions = Array.prototype.slice.call(document.querySelectorAll('.version'));
    var first = versions[0], last = versions[versions.length - 1];
    var dFirst = first ? txt(first.querySelector('.version-date')) : '';
    var dLast = last ? txt(last.querySelector('.version-date')) : '';
    var updates = versions.filter(function(v){{ return v.classList.contains('is-update'); }});
    var n = updates.length;

    var line = document.getElementById('suivi-ligne');
    // Date abrégée (« 10 sept. 2026 ») pour tenir sur une seule ligne sur téléphone.
    var ABR = {{janvier:'janv.', 'février':'févr.', juillet:'juil.', septembre:'sept.', octobre:'oct.', novembre:'nov.', 'décembre':'déc.'}};
    function court(d){{ return d.replace(/[a-zéûô]+/i, function(m){{ return ABR[m.toLowerCase()] || m; }}); }}
    if(line) line.textContent = n ? 'Suivi · mis à jour le ' + court(dLast) : 'Suivi · première analyse' + (dFirst ? ' le ' + court(dFirst) : '');
    var meta = document.getElementById('suivi-meta');
    if(meta){{
      meta.textContent = (dFirst ? 'Première analyse le ' + dFirst + ' · ' : '') +
        (n ? n + (n > 1 ? ' mises à jour' : ' mise à jour') + ' · dernière le ' + dLast : 'aucune mise à jour pour l’instant');
    }}

    // Les premières phrases entières, jusqu'à ~max caractères (jamais de coupure en plein mot).
    function debut(s, max){{
      var ph = s.match(/[^.!?]+[.!?]+(\\s|$)/g);
      if(!ph) return s;
      var out = '';
      for(var i = 0; i < ph.length; i++){{
        if(out && (out + ph[i]).length > max) break;
        out += ph[i];
      }}
      out = out.trim();
      if(out.length > max * 1.4){{
        // Première phrase très longue : on coupe à la dernière virgule ou tiret avant la limite.
        var cut = Math.max(out.lastIndexOf(', ', max), out.lastIndexOf(' — ', max), out.lastIndexOf(' : ', max));
        if(cut > max * 0.5) out = out.slice(0, cut).replace(/[,:—\\s]+$/, '') + '…';
      }}
      return out;
    }}
    var box = document.getElementById('ce-qui-a-change');
    if(box){{
      if(!n){{
        box.innerHTML = '<span class="suivi-changes-label">Ce qui a changé</span>' +
          '<p class="suivi-conclusion">Rien pour l’instant : cette page présente la première analyse. Dès qu’un fait nouveau déplace les scénarios, il apparaît ici, avec ce qui a changé.</p>' +
          '<a class="suivi-more" href="#historique">Voir la première analyse ↓</a>';
      }} else {{
        var inner = last.querySelector('.version-content-inner') || last;
        var tag = txt(last.querySelector('.version-tag')).split('—')[0].trim();
        var title = txt(inner.querySelector('.version-title'));
        var fact = '';
        Array.prototype.some.call(inner.querySelectorAll('p'), function(p){{
          if(p.closest('.mini-scenario') || p.closest('.conclusion') || p.classList.contains('sources-note')) return false;
          fact = txt(p); return !!fact;
        }});
        var conc = txt(inner.querySelector('.conclusion p'));
        var chips = Array.prototype.map.call(inner.querySelectorAll('.mini-scenario'), function(s){{
          var arrow = s.querySelector('.evo-arrow');
          return '<div class="suivi-chip" data-kind="' + esc(s.getAttribute('data-kind') || '') + '">' +
            '<p class="suivi-chip-title">' + esc(txt(s.querySelector('.mini-scenario-title'))) + '</p>' +
            '<p class="suivi-chip-pct">' + esc(txt(s.querySelector('.evo-current'))) + ' ' + esc(txt(arrow)) +
            ' <small>' + esc(txt(s.querySelector('.evo-prev'))) + '</small></p></div>';
        }}).join('');
        box.innerHTML = '<span class="suivi-changes-label">Dernière mise à jour · ' + esc(dLast) + ' · ' + esc(tag) + '</span>' +
          (title ? '<h2>' + esc(title) + '</h2>' : '') +
          (fact ? '<p>' + esc(debut(fact, 330)) + '</p>' : '') +
          (chips ? '<div class="suivi-chips">' + chips + '</div>' : '') +
          (conc ? '<p class="suivi-conclusion"><strong>En clair :</strong> ' + esc(debut(conc, 220)) + '</p>' : '') +
          '<a class="suivi-more" href="#historique">Lire le détail et les sources ↓</a>';
      }}
    }}

    // Graphique : de la marge à droite pour les pourcentages finaux, et pas de chevauchement.
    var svg = document.getElementById('evo-svg');
    if(svg){{
      svg.setAttribute('viewBox', '0 0 650 210');
      // Téléphone : axe vertical sans le signe %, pour tenir dans la marge (les valeurs finales le portent).
      if(window.matchMedia('(max-width: 640px)').matches){{
        Array.prototype.forEach.call(svg.querySelectorAll('.evo-axis-label[text-anchor="end"]'), function(l){{
          l.textContent = l.textContent.replace('%', '');
        }});
        svg.setAttribute('viewBox', '-6 0 656 210');
      }}
      var labels = Array.prototype.slice.call(svg.querySelectorAll('.evo-pct-label'));
      if(labels.length){{
        var fs = parseFloat(getComputedStyle(labels[0]).fontSize) || 15;
        var gap = fs * 1.3;
        labels.sort(function(a, b){{ return parseFloat(a.getAttribute('y')) - parseFloat(b.getAttribute('y')); }});
        for(var i = 1; i < labels.length; i++){{
          var prev = parseFloat(labels[i - 1].getAttribute('y')), cur = parseFloat(labels[i].getAttribute('y'));
          if(cur - prev < gap) labels[i].setAttribute('y', prev + gap);
        }}
        // Sans empiéter sur la ligne des V0, V1… : si le dernier descend trop bas, on remonte l'ensemble.
        var bas = parseFloat(labels[labels.length - 1].getAttribute('y')), limite = 176;
        if(bas > limite){{
          labels.forEach(function(l){{ l.setAttribute('y', parseFloat(l.getAttribute('y')) - (bas - limite)); }});
        }}
      }}
    }}
  }})();
</script>
{JS_END}
"""

EDITION_LINE = '        <div class="edition" id="suivi-ligne">Suivi d\'un sujet</div>\n'


def _strip(text: str, start: str, end: str) -> str:
    return re.sub(r"[ \t]*" + re.escape(start) + r".*?" + re.escape(end) + r"\n?", "", text, flags=re.S)


def apply(text: str) -> str:
    text = _strip(text, CSS_START, CSS_END)
    text = _strip(text, HTML_START, HTML_END)
    text = _strip(text, JS_START, JS_END)

    # CSS : dans l'unique bloc <style>, juste avant sa fermeture.
    text = text.replace("</style>", CSS + "</style>", 1)

    # Ligne de repère sous le logo (même classe visuelle que « Édition du … » des éditions).
    if 'id="suivi-ligne"' not in text:
        text, k = re.subn(r'(<div class="brand-row">.*?</div>\n)(\s*</div>\s*</div>\s*</header>)',
                          lambda m: m.group(1) + EDITION_LINE + m.group(2), text, count=1, flags=re.S)
        if not k:
            raise ValueError("masthead introuvable")

    # Section « Où en est-on ? » : entre l'en-tête (hero) et le graphique.
    marker = '<section class="evolution">'
    if marker not in text:
        raise ValueError("section evolution introuvable")
    text = text.replace(marker, HTML + marker, 1)

    # Script : en fin de page.
    if "</body>" not in text:
        raise ValueError("</body> introuvable")
    text = text.replace("</body>", JS + "</body>", 1)
    return text


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="ne rien écrire ; code 1 si une page n'est pas à jour")
    args = ap.parse_args(argv)
    retard = []
    for path in sorted(SUIVI_DIR.glob("*.html")):
        old = path.read_text(encoding="utf-8")
        new = apply(old)
        if new != old:
            retard.append(path.name)
            if not args.check:
                path.write_text(new, encoding="utf-8")
    print(f"{'À mettre à jour' if args.check else 'Mis à jour'} : {len(retard)} page(s)" + (f" — {', '.join(retard)}" if retard else ""))
    return 1 if (args.check and retard) else 0


if __name__ == "__main__":
    sys.exit(main())
