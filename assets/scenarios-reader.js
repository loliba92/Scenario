/* Lecture des scénarios : un scénario à la fois, trois onglets (Favorable / Stable / Dégradé).

   Amélioration progressive : le HTML des éditions n'est pas modifié. Sans JavaScript, à l'impression
   et pour les moteurs de recherche, les trois scénarios restent affichés en entier, comme avant.
   Avec JavaScript (écran), la section #scenarios devient :
     - une bande d'onglets (probabilité de chaque scénario) ;
     - le scénario choisi, avec un fond teinté de sa couleur (vert, bleu ou orange) ;
     - un lien « Scénario suivant » pour enchaîner sans remonter ;
     - sur téléphone : onglets collés en haut, glisser le doigt pour changer, analyse longue repliée.
   Retours du propriétaire (3 octobre 2026) : lecture en colonnes étroites pénible sur ordinateur
   (descendre, remonter, redescendre), page de 10 écrans sur téléphone, « trop d'encadrés » : ici du
   texte sur fond teinté, sans cartes ni jauges. */
(function () {
  "use strict";
  var section = document.querySelector("section.scenarios");
  if (!section) return;
  var cards = Array.prototype.slice.call(section.querySelectorAll(".cards > article.card"));
  if (cards.length < 2) return;

  var EN = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
  var T = EN
    ? { tabs: "The three scenarios", more: "Read the full analysis", less: "Hide the analysis", next: "Next scenario: ", first: "Back to the first scenario", prob: "probability" }
    : { tabs: "Les trois scénarios", more: "Lire l'analyse complète", less: "Masquer l'analyse", next: "Scénario suivant : ", first: "Revoir le premier scénario", prob: "de probabilité" };

  /* ---------- Style (injecté ici : une seule source pour toutes les éditions) ---------- */
  var css = [
    "@media screen{",
    ".scenarios.sr-on .stakes-box{display:none}",
    ".sr-tabs{display:grid;grid-template-columns:repeat(" + cards.length + ",minmax(0,1fr));gap:2px;margin:6px 0 0}",
    ".sr-tab{--c:var(--stable,#7c9bb8);--t:#1e2732;appearance:none;background:transparent;border:0;border-bottom:3px solid transparent;border-radius:10px 10px 0 0;color:var(--paper-dim,#b4b2a6);text-align:left;font:inherit;cursor:pointer;padding:12px 16px 12px;display:flex;flex-direction:column;gap:2px;min-width:0}",
    ".sr-tab[data-kind=favorable]{--c:var(--favorable,#6aa584);--t:#1c292a}",
    ".sr-tab[data-kind=degrade]{--c:var(--degrade,#c47257);--t:#2a2123}",
    ".sr-tab .sr-k{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase}",
    ".sr-tab .sr-p{font-family:'JetBrains Mono',ui-monospace,monospace;font-weight:500;font-size:1.7rem;line-height:1.15;color:var(--paper,#e6e1d4);font-variant-numeric:tabular-nums}",
    ".sr-tab .sr-p small{font-size:.85rem;color:var(--paper-dim,#b4b2a6)}",
    ".sr-tab .sr-s{font-size:.86rem;line-height:1.4;color:var(--paper-dim,#b4b2a6);margin-top:4px}",
    ".sr-tab:hover .sr-k{color:var(--c)}",
    ".sr-tab[aria-selected=true]{background:var(--t);background:color-mix(in srgb,var(--c) 15%,var(--ink,#10151c));border-bottom-color:var(--c)}",
    ".sr-tab[aria-selected=true] .sr-k{color:var(--c)}",
    ".sr-tab:not([aria-selected=true]) .sr-p{color:var(--paper-dim,#b4b2a6)}",
    ".sr-tab:focus-visible,.sr-next:focus-visible,.sr-more:focus-visible{outline:2px solid var(--gold,#cf9d4c);outline-offset:2px}",
    /* le fond suit le scénario choisi */
    ".scenarios.sr-on .cards{display:block;position:relative}",
    ".scenarios.sr-on .card{--t:#1e2732;display:none;background:var(--t);background:color-mix(in srgb,var(--accent) 15%,var(--ink,#10151c));border:0;border-radius:0 0 10px 10px;padding:30px 32px 24px;gap:0;animation:sr-in .22s ease-out}",
    ".scenarios.sr-on .card[data-kind=favorable]{--t:#1c292a}",
    ".scenarios.sr-on .card[data-kind=degrade]{--t:#2a2123}",
    ".scenarios.sr-on .card.sr-current{display:block}",
    "@keyframes sr-in{from{opacity:0}to{opacity:1}}",
    "@media (prefers-reduced-motion:reduce){.scenarios.sr-on .card{animation:none}}",
    ".scenarios.sr-on .card-head{width:auto;align-items:flex-start;text-align:left;gap:0}",
    ".scenarios.sr-on .card-head .kind-tag,.scenarios.sr-on .card-head .gauge,.scenarios.sr-on .card-head .gauge-word{display:none}",
    ".scenarios.sr-on .card-head h3{text-align:left;justify-content:flex-start;min-height:0;margin:0 0 14px;font-size:clamp(1.25rem,2.2vw,1.55rem);line-height:1.3;text-wrap:balance}",
    ".scenarios.sr-on .card-body{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);column-gap:56px;gap:0 56px}",
    ".sr-main{min-width:0}",
    ".sr-aside{min-width:0;border-left:1px solid rgba(236,231,218,.16);padding-left:32px;display:flex;flex-direction:column;gap:26px}",
    ".scenarios.sr-on .card .why{font-size:1.06rem;line-height:1.75;color:var(--paper-dim,#b4b2a6);max-width:62ch;margin:0}",
    ".scenarios.sr-on .card .sr-more ~ .why{margin-top:16px;padding-top:0;border-top:0}",
    ".scenarios.sr-on .sr-aside .france-line{background:none;border:0;border-radius:0;padding:0;margin:0}",
    ".scenarios.sr-on .sr-aside .france-line .field-label{display:block;margin-bottom:8px}",
    ".scenarios.sr-on .sr-aside .field li{padding-left:0;margin:0 0 14px}",
    ".scenarios.sr-on .sr-aside .field li::before{display:none}",
    ".scenarios.sr-on .card .why .sr-lead{display:block;font-size:1.14rem;line-height:1.65;color:var(--paper,#e6e1d4);margin-bottom:8px}",
    ".scenarios.sr-on .card .divider{display:none}",
    ".scenarios.sr-on .card .field{margin:0}",
    ".sr-next-wrap{margin-top:40px;padding-top:18px;border-top:1px solid rgba(236,231,218,.16)}",
    ".sr-next{font-family:'Fraunces',Georgia,serif;font-weight:500;font-size:.98rem;background:none;border:0;border-bottom:1px solid var(--gold,#cf9d4c);color:var(--paper,#e6e1d4);padding:6px 0;cursor:pointer}",
    ".sr-more{display:none;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.85rem;background:none;border:0;border-bottom:1px solid rgba(236,231,218,.3);color:var(--paper,#e6e1d4);padding:4px 0;cursor:pointer;margin:10px 0 0}",
    "@media (max-width:820px){",
    ".sr-tabs{position:sticky;top:var(--sr-top,0px);z-index:20;background:var(--ink,#10151c);margin-inline:-16px;padding-inline:16px;border-bottom:1px solid rgba(236,231,218,.12)}",
    ".sr-tab{padding:9px 8px 9px;border-radius:0}",
    ".sr-tab .sr-s{display:none}",
    ".sr-tab .sr-p{font-size:1.3rem}",
    ".scenarios.sr-on .card{padding:22px 16px 20px;margin-inline:-16px;border-radius:0}",
    ".scenarios.sr-on .card-body{display:block}",
    ".sr-aside{border-left:0;padding-left:0;margin-top:28px;padding-top:22px;border-top:1px solid rgba(236,231,218,.16)}",
    ".sr-more{display:inline-block}",
    ".scenarios.sr-on .card:not(.sr-open) .sr-rest,.scenarios.sr-on .card:not(.sr-open) .sr-more ~ .why{display:none}",
    ".scenarios.sr-on .card .why .sr-lead{display:inline}",
    "}",
    "}"
  ].join("\n");
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);

  /* ---------- Données lues dans le HTML existant ---------- */
  function txt(el) { return el ? el.textContent.replace(/\s+/g, " ").trim() : ""; }
  var stakes = {};
  Array.prototype.forEach.call(section.querySelectorAll(".stakes-branches li"), function (li) {
    var tag = li.querySelector(".stakes-tag");
    stakes[li.getAttribute("data-kind")] = txt(li).replace(txt(tag), "").trim();
  });

  /* ---------- Phrase d'accroche : première phrase du premier paragraphe ---------- */
  function splitLead(p) {
    var text = p.textContent;
    var m = /^[\s\S]{40,}?[.!?](?=\s|$)/.exec(text);
    if (!m || m[0].length >= text.length - 20) return;
    var limit = m[0].length, count = 0, node = null, offset = 0;
    var walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT, null);
    while (walker.nextNode()) {
      var n = walker.currentNode, len = n.nodeValue.length;
      if (count + len >= limit) { node = n; offset = limit - count; break; }
      count += len;
    }
    if (!node) return;
    try {
      var r = document.createRange();
      r.setStart(p, 0);
      r.setEnd(node, offset);
      var lead = document.createElement("span");
      lead.className = "sr-lead";
      lead.appendChild(r.extractContents());
      var rest = document.createElement("span");
      rest.className = "sr-rest";
      while (p.firstChild) rest.appendChild(p.firstChild);
      p.appendChild(lead);
      p.appendChild(document.createTextNode(" "));
      p.appendChild(rest);
    } catch (e) { /* mise en page sans accroche : le texte reste entier */ }
  }

  /* ---------- Construction ---------- */
  var tabs = document.createElement("div");
  tabs.className = "sr-tabs";
  tabs.setAttribute("role", "tablist");
  tabs.setAttribute("aria-label", T.tabs);
  var infos = cards.map(function (card, i) {
    var kind = card.getAttribute("data-kind") || "stable";
    var tag = txt(card.querySelector(".kind-tag"));
    var numEl = card.querySelector(".gauge-num");
    var pct = numEl ? txt(numEl).replace(/\s*%/, "") : "";
    card.id = card.id || "scenario-" + kind;
    card.setAttribute("role", "tabpanel");
    card.setAttribute("aria-labelledby", "sr-tab-" + kind);

    var body = card.querySelector(".card-body");
    if (body) {
      var main = document.createElement("div"); main.className = "sr-main";
      var aside = document.createElement("div"); aside.className = "sr-aside";
      Array.prototype.slice.call(body.children).forEach(function (el) {
        if (el.matches(".field,.france-line")) aside.appendChild(el); else main.appendChild(el);
      });
      body.appendChild(main);
      body.appendChild(aside);
      var firstWhy = main.querySelector(".why");
      if (firstWhy) {
        splitLead(firstWhy);
        var more = document.createElement("button");
        more.type = "button"; more.className = "sr-more"; more.textContent = T.more; more.setAttribute("aria-expanded", "false");
        more.addEventListener("click", function () {
          var open = card.classList.toggle("sr-open");
          more.textContent = open ? T.less : T.more;
          more.setAttribute("aria-expanded", open ? "true" : "false");
        });
        firstWhy.parentNode.insertBefore(more, firstWhy.nextSibling);
      }
      var wrap = document.createElement("div"); wrap.className = "sr-next-wrap";
      var next = document.createElement("button"); next.type = "button"; next.className = "sr-next";
      next.setAttribute("data-i", i);
      wrap.appendChild(next); body.appendChild(wrap);
    }

    var tab = document.createElement("button");
    tab.type = "button"; tab.className = "sr-tab"; tab.id = "sr-tab-" + kind;
    tab.setAttribute("role", "tab"); tab.setAttribute("aria-controls", card.id); tab.setAttribute("data-kind", kind);
    tab.setAttribute("aria-label", tag + (pct ? ", " + pct + " % " + T.prob : ""));
    tab.innerHTML = '<span class="sr-k"></span><span class="sr-p"></span>' + (stakes[kind] ? '<span class="sr-s"></span>' : "");
    tab.querySelector(".sr-k").textContent = tag;
    tab.querySelector(".sr-p").innerHTML = (pct || "–") + "<small> %</small>";
    if (stakes[kind]) tab.querySelector(".sr-s").textContent = stakes[kind];
    tabs.appendChild(tab);
    return { card: card, tab: tab, tag: tag };
  });
  var cardsBox = section.querySelector(".cards");
  cardsBox.parentNode.insertBefore(tabs, cardsBox);
  section.classList.add("sr-on");

  var current = 0;
  function stickyTop() {
    var m = document.querySelector("header.masthead");
    var top = m && getComputedStyle(m).position === "sticky" ? m.offsetHeight : 0;
    section.style.setProperty("--sr-top", top + "px");
  }
  function show(i, scrollToTabs) {
    current = (i + infos.length) % infos.length;
    infos.forEach(function (o, j) {
      var on = j === current;
      o.card.classList.toggle("sr-current", on);
      o.tab.setAttribute("aria-selected", on ? "true" : "false");
      o.tab.tabIndex = on ? 0 : -1;
      var nb = o.card.querySelector(".sr-next");
      if (nb) {
        var nxt = infos[(j + 1) % infos.length];
        nb.textContent = j === infos.length - 1 ? T.first + " →" : T.next + nxt.tag.toLowerCase() + " →";
      }
    });
    if (scrollToTabs) {
      var r = tabs.getBoundingClientRect(), top = parseInt(section.style.getPropertyValue("--sr-top"), 10) || 0;
      if (r.top < top + 1 || r.top > window.innerHeight * 0.6) {
        window.scrollTo({ top: window.pageYOffset + r.top - top - 8, behavior: "smooth" });
      }
    }
  }
  tabs.addEventListener("click", function (e) {
    var b = e.target.closest(".sr-tab");
    if (b) show(infos.map(function (o) { return o.tab; }).indexOf(b));
  });
  tabs.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
      e.preventDefault();
      show(current + (e.key === "ArrowRight" ? 1 : -1));
      infos[current].tab.focus();
    }
  });
  cardsBox.addEventListener("click", function (e) {
    var n = e.target.closest(".sr-next");
    if (n) show(current + 1, true);
  });
  var x0 = null, y0 = null;
  cardsBox.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
  cardsBox.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    x0 = null;
    if (Math.abs(dx) > 70 && Math.abs(dx) > Math.abs(dy) * 1.6) show(current + (dx < 0 ? 1 : -1), true);
  });
  window.addEventListener("resize", stickyTop);
  stickyTop();

  var start = 0;
  if (location.hash) {
    infos.forEach(function (o, j) { if ("#" + o.card.id === location.hash) start = j; });
  }
  show(start);
})();
