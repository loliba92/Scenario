/*
 * Page « Recherche » : cherche dans toutes les éditions ET dans le glossaire.
 *
 * Les données ne sont pas dupliquées : à l'ouverture, la page lit archives.html
 * (une ligne par édition : titre, question, domaine, date) et glossaire.html
 * (un bloc par terme) et les passe au moteur de recherche du glossaire
 * (assets/glossary-search.js : mots multiples, accents, pluriels, fautes de
 * frappe, familles de mots, termes connexes). Une nouvelle édition ou un nouveau
 * terme est donc trouvable dès qu'il est publié, sans rien régénérer ici.
 */
(function () {
  "use strict";

  var core = window.GlossarySearchCore;
  var input = document.getElementById("site-search-input");
  var hints = document.getElementById("site-search-hints");
  var status = document.getElementById("site-search-status");
  var out = document.getElementById("site-search-results");
  if (!core || !input || !out) return;

  var SHOWN = 12;           // résultats directs montrés avant « Voir la suite »
  var MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."];
  var EXAMPLES = ["inflation", "retraite", "bitcoin", "climat", "OTAN", "intelligence artificielle"];

  var MATIERES = [
    ["economie-entreprises", "Économie & entreprises"], ["politique-institutions", "Politique & institutions"],
    ["international", "International"], ["sciences-environnement", "Sciences & environnement"],
    ["tech-numerique", "Tech & numérique"], ["culture-divertissement", "Culture & divertissement"], ["sport", "Sport"]
  ];
  var matiere = "";  // slug de la matière choisie, "" = toutes
  var chips = document.getElementById("site-search-matieres");

  var editions = [], terms = [];
  var edEngine = null, glEngine = null;
  var expanded = { ed: false, gl: false };
  var baseStatus = "";

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function fetchDoc(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(url + " " + r.status);
      return r.text();
    }).then(function (t) { return new DOMParser().parseFromString(t, "text/html"); });
  }

  // Domaines hors des 6 thèmes officiels : archives.html affiche alors le nom technique brut.
  var DOMAIN_ALIAS = { "economie-mondiale": "Économie", "sciences": "Sciences", "sport": "Sport" };
  function prettyDomain(d) {
    if (DOMAIN_ALIAS[d]) return DOMAIN_ALIAS[d];
    return /^[a-z-]+$/.test(d) ? d.charAt(0).toUpperCase() + d.slice(1).replace(/-/g, " ") : d;
  }

  function loadEditions(doc) {
    var rows = doc.querySelectorAll("tr[data-date]");
    Array.prototype.forEach.call(rows, function (tr) {
      var a = tr.querySelector(".col-title a");
      if (!a) return;
      var dom = tr.querySelector(".col-domain");
      editions.push({
        title: a.textContent.replace(/\s+/g, " ").trim(),
        question: (a.getAttribute("title") || "").replace(/^[^\p{L}\p{N}«"'(]+/u, "").trim(),
        href: a.getAttribute("href"),
        domain: dom ? prettyDomain(dom.textContent.replace(/\s+/g, " ").trim()) : "",
        slug: tr.getAttribute("data-domain") || "",
        date: tr.getAttribute("data-date") || ""
      });
    });
  }

  function loadTerms(doc) {
    var list = doc.querySelectorAll(".lex-entry");
    Array.prototype.forEach.call(list, function (e) {
      var t = e.querySelector(".lex-term"), d = e.querySelector(".lex-def");
      if (!t || !d) return;
      var dom = e.querySelector(".lex-domain");
      terms.push({
        term: t.textContent.replace(/\s+/g, " ").trim(),
        def: d.textContent.replace(/\s+/g, " ").trim(),
        id: e.getAttribute("id") || "",
        domain: dom ? prettyDomain(dom.textContent.replace(/\s+/g, " ").trim()) : ""
      });
    });
  }

  function fmtDate(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
    return m ? (+m[3]) + " " + MONTHS[+m[2] - 1] + " " + m[1] : "";
  }

  function editionItem(e, related) {
    var meta = [fmtDate(e.date), e.domain].filter(Boolean).join(" · ");
    return '<li class="sr-item' + (related ? " is-related" : "") + '"><a href="' + esc(e.href) + '">' +
      '<span class="sr-meta">' + esc(meta) + "</span>" +
      '<span class="sr-item-title">' + esc(e.title) + "</span>" +
      (e.question ? '<span class="sr-item-text">' + esc(e.question) + "</span>" : "") + "</a></li>";
  }

  function termItem(t, related) {
    return '<li class="sr-item' + (related ? " is-related" : "") + '"><a href="glossaire.html#' + esc(t.id) + '">' +
      '<span class="sr-meta">Glossaire' + (t.domain ? " · " + esc(t.domain) : "") + "</span>" +
      '<span class="sr-item-title">' + esc(t.term) + "</span>" +
      '<span class="sr-item-text">' + esc(t.def) + "</span></a></li>";
  }

  function plural(n, w) { return n + " " + w + (n > 1 ? "s" : ""); }

  // Une section (éditions ou glossaire) : résultats directs, puis « sur le même sujet ».
  function section(key, title, res, data, render) {
    if (!res.direct.length && !res.related.length) return "";
    var all = expanded[key];
    var direct = all ? res.direct : res.direct.slice(0, SHOWN);
    var html = '<section class="sr-section"><h2 class="sr-title">' + title + " (" + res.direct.length + ")</h2>";
    if (direct.length) {
      html += '<ul class="sr-list">' + direct.map(function (x) { return render(data[x.i], false); }).join("") + "</ul>";
      if (res.direct.length > SHOWN && !all) {
        html += '<button type="button" class="sr-more" data-more="' + key + '">Voir les ' + (res.direct.length - SHOWN) + " autres</button>";
      }
    } else {
      html += '<p class="sr-sub">Aucun résultat exact dans cette partie.</p>';
    }
    if (res.related.length) {
      html += '<p class="sr-sub">Sur le même sujet</p><ul class="sr-list">' +
        res.related.map(function (x) { return render(data[x.i], true); }).join("") + "</ul>";
    }
    return html + "</section>";
  }

  function drawChips() {
    if (!chips) return;
    chips.innerHTML = '<button type="button" data-m=""' + (matiere ? "" : ' class="is-active"') + ">Toutes</button>" +
      MATIERES.map(function (m) {
        return '<button type="button" data-m="' + m[0] + '"' + (matiere === m[0] ? ' class="is-active"' : "") + ">" + esc(m[1]) + "</button>";
      }).join("");
  }

  function keep(list) {
    return matiere ? list.filter(function (x) { return editions[x.i].slug === matiere; }) : list;
  }

  function render() {
    var q = input.value.trim();
    if (!edEngine || !glEngine) return;
    try {
      var qs = [];
      if (q) qs.push("q=" + encodeURIComponent(q));
      if (matiere) qs.push("matiere=" + matiere);
      history.replaceState(null, "", qs.length ? "?" + qs.join("&") : location.pathname);
    } catch (e) { /* aperçu / navigation privée */ }
    drawChips();
    if (!q) {
      out.innerHTML = "";
      status.textContent = baseStatus;
      hints.hidden = false;
      return;
    }
    hints.hidden = true;
    var ed = edEngine.search(q, { flat: true, minRelated: 0.14 }), gl = glEngine.search(q);
    if (matiere) {
      // Une matière choisie : seulement ses éditions (le glossaire n'a pas de matière comparable).
      ed = { direct: keep(ed.direct), related: keep(ed.related) };
      gl = { direct: [], related: [] };
    }
    var n = ed.direct.length + gl.direct.length;
    var rel = ed.related.length + gl.related.length;
    if (!n && !rel) {
      out.innerHTML = "";
      status.textContent = "Aucun résultat pour « " + q + " »" + (matiere ? " dans cette matière. Essayez « Toutes »." : ". Essayez un mot plus court ou un synonyme.");
      return;
    }
    status.textContent = (n ? plural(n, "résultat") : "Aucun résultat exact") +
      (rel ? " · " + plural(rel, "sujet") + " voisin" + (rel > 1 ? "s" : "") : "");
    out.innerHTML = section("ed", "Éditions", ed, editions, editionItem) +
      section("gl", "Termes du glossaire", gl, terms, termItem);
  }

  if (chips) chips.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    matiere = b.getAttribute("data-m") || "";
    expanded.ed = false;
    render();
  });

  out.addEventListener("click", function (e) {
    var b = e.target.closest("[data-more]");
    if (!b) return;
    expanded[b.getAttribute("data-more")] = true;
    render();
  });

  var timer = null;
  input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(render, 120); });

  hints.innerHTML = EXAMPLES.map(function (w) { return '<button type="button">' + esc(w) + "</button>"; }).join("");
  hints.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    input.value = b.textContent;
    render();
    input.focus();
  });

  Promise.all([fetchDoc("archives.html"), fetchDoc("glossaire.html")]).then(function (docs) {
    loadEditions(docs[0]);
    loadTerms(docs[1]);
    edEngine = core.createEngine(editions.map(function (e) { return { term: e.title, def: e.question, domains: [e.domain] }; }));
    glEngine = core.createEngine(terms.map(function (t) { return { term: t.term, def: t.def, domains: [t.domain] }; }));
    var params = new URLSearchParams(location.search), q0 = params.get("q"), m0 = params.get("matiere") || "";
    if (q0) input.value = q0;
    if (MATIERES.some(function (m) { return m[0] === m0; })) matiere = m0;
    baseStatus = plural(editions.length, "édition") + " et " + plural(terms.length, "terme") + " à explorer.";
    render();
    if (!q0 && !matiere) input.focus();
  }).catch(function () {
    status.textContent = "Impossible de charger les données pour le moment. Réessayez dans quelques instants.";
  });
})();
