/*
 * Recherche du glossaire.
 *
 * Fonctionne entièrement dans le navigateur, sans service extérieur :
 *  1. Résultats directs : tous les mots saisis doivent être trouvés (dans le
 *     terme ou sa définition), sans tenir compte des accents, des majuscules,
 *     des pluriels ni d'une faute de frappe. Le terme compte plus que la
 *     définition, et le classement met en premier les meilleures réponses.
 *  2. Termes connexes : à partir des meilleurs résultats, on cherche les
 *     autres termes du glossaire qui parlent de la même chose (vocabulaire
 *     commun dans les définitions, termes qui se citent entre eux).
 *
 * Le calcul se fait à l'ouverture de la page sur la liste telle qu'elle est ;
 * un nouveau terme ajouté au glossaire est donc pris en compte sans rien
 * modifier ici. Le noyau (createEngine) ne touche pas au DOM pour pouvoir
 * être testé seul.
 */
(function (root) {
  "use strict";

  var STOPWORDS = {};
  ("le la les un une des de du d l au aux et ou en a y ce cet cette ces se sa son ses leur leurs " +
   "qui que quoi dont ne pas plus par pour sur sous dans avec sans est sont etre ete fait faire " +
   "peut peuvent comme mais si il elle ils elles on nous vous entre tout tous toute toutes " +
   "aussi ainsi tres afin lors vers chez non oui the of and").split(" ").forEach(function (w) { STOPWORDS[w] = 1; });

  var SUFFIXES = ["issements", "issement", "ations", "ation", "ements", "ement", "ances", "ance",
    "ences", "ence", "ites", "ite", "iques", "ique", "ismes", "isme", "istes", "iste", "euses",
    "euse", "eurs", "eur", "ives", "ive", "ifs", "if", "ables", "able", "ions", "ion", "aux",
    "ales", "ale", "als", "al", "es", "s", "x", "e"];

  function deburr(s) {
    return String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  // Racine approximative : suffisant pour rapprocher pluriels et dérivés courants.
  function stem(w) {
    if (w.length <= 4) return w;
    for (var i = 0; i < SUFFIXES.length; i++) {
      var suf = SUFFIXES[i];
      if (w.length - suf.length >= 5 && w.slice(-suf.length) === suf) return w.slice(0, -suf.length);
    }
    return w;
  }

  function tokens(text, keepStop) {
    var out = [];
    var parts = deburr(text).match(/[a-z0-9]+/g) || [];
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      if (!keepStop && (STOPWORDS[p] || (p.length < 2 && !/\d/.test(p)))) continue;
      out.push(stem(p));
    }
    return out;
  }


  // Familles de mots voisins : chercher l'un fait aussi trouver les autres
  // (avec un poids plus faible qu'une correspondance exacte). À compléter au fil
  // du temps : une ligne = une famille, mots simples, sans accent obligatoire.
  var FAMILIES = [
    "sante medical medecin hopital soin maladie medicament sanitaire patient pharmaceutique",
    "taux interet credit emprunt obligation dette",
    "banque bancaire monetaire monnaie devise dollar fed bce",
    "inflation prix indexation stagflation pouvoir achat",
    "retraite pension cotisation repartition vieillesse",
    "chomage emploi travail salaire licenciement salarie social",
    "impot taxe fiscal fiscalite fiscale prelevement patrimoine",
    "energie petrole gaz nucleaire electricite carbone baril",
    "climat carbone canicule rechauffement environnement ecologique",
    "spatial lune lunaire orbite fusee satellite station cosmos",
    "guerre conflit armee militaire defense securite otan blocus",
    "cinema film salle streaming studio diffusion",
    "intelligence artificielle numerique algorithme donnees technologie",
    "justice tribunal cour loi juridique proces",
    "election vote electoral scrutin parlement assemblee",
    "sport football fifa championnat club",
    "bourse action marche investisseur speculative capitalisation",
    "commerce tarif tarifaire douane echange exportation",
    "deficit budget depense public etat",
    "europe europeen union schengen"
  ];
  var SYN_W = 0.6; // poids d'un mot de la même famille
  var SYN = {};
  FAMILIES.forEach(function (line) {
    var ws = line.split(" ").map(function (w) { return stem(w); });
    ws.forEach(function (a) {
      SYN[a] = SYN[a] || {};
      ws.forEach(function (b) { if (b !== a) SYN[a][b] = 1; });
    });
  });

  // Le texte saisi commence-t-il un mot ? (« sante » ne doit pas être trouvé dans « glissante »)
  function wordStart(text, q) {
    var at = -1;
    while ((at = text.indexOf(q, at + 1)) !== -1) {
      if (at === 0 || !/[a-z0-9]/.test(text.charAt(at - 1))) return true;
    }
    return false;
  }

  function levenshtein(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var prev = [], cur = [], i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      var rowMin = i;
      for (j = 1; j <= b.length; j++) {
        var cost = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
        if (cur[j] < rowMin) rowMin = cur[j];
      }
      if (rowMin > max) return max + 1;
      prev = cur;
    }
    return prev[b.length];
  }

  /**
   * items : [{ term, def, domains }]  (dans l'ordre d'origine)
   * renvoie { search(query, opts) → { direct:[{i,score}], related:[{i,score}], partial } }
   */
  function createEngine(items) {
    var N = items.length;
    var docs = [];
    var index = {};      // racine → [{ i, inTerm, inDef }]
    var df = {};         // racine → nombre de termes qui la contiennent

    items.forEach(function (it, i) {
      var termStems = tokens(it.term);
      var defStems = tokens(it.def);
      var tf = {}; // racine → poids brut
      var seen = {};
      termStems.forEach(function (s) { tf[s] = (tf[s] || 0) + 3; seen[s] = seen[s] || { t: 0, d: 0 }; seen[s].t++; });
      defStems.forEach(function (s) { tf[s] = (tf[s] || 0) + 1; seen[s] = seen[s] || { t: 0, d: 0 }; seen[s].d++; });
      Object.keys(seen).forEach(function (s) {
        (index[s] = index[s] || []).push({ i: i, t: seen[s].t, d: seen[s].d });
        df[s] = (df[s] || 0) + 1;
      });

      // Formes du terme pour détecter les renvois d'un terme à l'autre :
      // « Taux directeur (BCE) » → « taux directeur » et « bce ».
      var keys = [];
      var main = it.term.replace(/\(.*?\)/g, " ");
      var inParen = (it.term.match(/\((.*?)\)/) || [])[1];
      [main, inParen].forEach(function (k) {
        if (!k) return;
        var t = tokens(k).join(" ");
        if (t.length >= 4) keys.push(t);
      });

      docs.push({
        tf: tf,
        termText: deburr(it.term),
        fullText: deburr(it.term + " " + it.def),
        termStems: termStems,
        keys: keys,
        defString: " " + defStems.join(" ") + " ",
        domains: it.domains || []
      });
    });

    var vocab = Object.keys(index);

    function idf(s) { return Math.log(1 + N / (df[s] || 1)); }

    // Pour chaque mot saisi : quelles racines du glossaire correspondent, et avec quel poids.
    function expand(qStem, isLast) {
      var out = {};
      if (index[qStem]) out[qStem] = 1;
      if (SYN[qStem]) Object.keys(SYN[qStem]).forEach(function (v) { if (index[v] && !out[v]) out[v] = SYN_W; });
      var minPrefix = qStem.length >= 3;
      var maxDist = qStem.length >= 8 ? 2 : qStem.length >= 5 ? 1 : 0;
      for (var k = 0; k < vocab.length; k++) {
        var v = vocab[k];
        if (out[v] === 1) continue;
        if (minPrefix && (v.indexOf(qStem) === 0 || (qStem.length >= 5 && qStem.indexOf(v) === 0 && v.length >= 4))) {
          out[v] = Math.max(out[v] || 0, 0.85);
        } else if (maxDist && Math.abs(v.length - qStem.length) <= maxDist && levenshtein(v, qStem, maxDist) <= maxDist) {
          out[v] = Math.max(out[v] || 0, 0.55);
        }
      }
      return out;
    }

    function vectorOf(i) {
      var tf = docs[i].tf, vec = {}, norm = 0;
      Object.keys(tf).forEach(function (s) {
        var w = (1 + Math.log(tf[s])) * idf(s);
        vec[s] = w; norm += w * w;
      });
      norm = Math.sqrt(norm) || 1;
      Object.keys(vec).forEach(function (s) { vec[s] /= norm; });
      return vec;
    }

    var vecCache = {};
    function vec(i) { return vecCache[i] || (vecCache[i] = vectorOf(i)); }

    function scoreDirect(query, requireAll) {
      var qRaw = deburr(query.trim());
      var qToks = tokens(query);
      var scores = {};
      var matchedCount = {};
      var termHit = {};

      if (qToks.length) {
        qToks.forEach(function (qs, n) {
          var exp = expand(qs, n === qToks.length - 1);
          var hitThis = {};
          Object.keys(exp).forEach(function (s) {
            var w = exp[s];
            index[s].forEach(function (p) {
              var sc = 0;
              if (p.t) sc += 14 * w;
              if (p.d) sc += w * idf(s);
              if (p.t && w !== SYN_W) termHit[p.i] = true;
              if (!hitThis[p.i] || hitThis[p.i] < sc) hitThis[p.i] = sc;
            });
          });
          Object.keys(hitThis).forEach(function (i) {
            scores[i] = (scores[i] || 0) + hitThis[i];
            matchedCount[i] = (matchedCount[i] || 0) + 1;
          });
        });
      }

      // Ancien comportement conservé : le texte saisi tel quel dans le terme ou la définition.
      if (qRaw.length >= 2) {
        for (var i = 0; i < N; i++) {
          if (wordStart(docs[i].fullText, qRaw)) {
            scores[i] = (scores[i] || 0) + 1;
            matchedCount[i] = Math.max(matchedCount[i] || 0, qToks.length || 1);
          }
        }
      }

      var need = requireAll ? Math.max(qToks.length, 1) : 1;
      var res = [];
      Object.keys(scores).forEach(function (k) {
        var i = +k;
        if (matchedCount[i] < need) return;
        var s = scores[i];
        var t = docs[i].termText;
        if (qRaw && t === qRaw) s += 40;
        else if (qRaw && t.indexOf(qRaw) === 0) s += 20;
        else if (qRaw && wordStart(t, qRaw)) s += 10;
        if (qRaw && wordStart(t, qRaw)) termHit[i] = true;
        res.push({ i: i, score: s, term: !!termHit[i] });
      });
      res.sort(function (a, b) { return b.score - a.score || a.i - b.i; });
      return res;
    }

    function related(pool, all, opts) {
      var top = pool.length ? pool[0].score : 0;
      var seeds = pool.filter(function (d) { return d.score >= top * 0.6; }).slice(0, 3);
      if (!seeds.length) return [];
      var seedSet = {};
      all.forEach(function (d) { seedSet[d.i] = 1; });

      var centroid = {};
      seeds.forEach(function (sd, r) {
        var w = 1 / (1 + r * 0.6);
        var v = vec(sd.i);
        Object.keys(v).forEach(function (s) { centroid[s] = (centroid[s] || 0) + v[s] * w; });
      });
      var cnorm = 0;
      Object.keys(centroid).forEach(function (s) { cnorm += centroid[s] * centroid[s]; });
      cnorm = Math.sqrt(cnorm) || 1;

      var sim = {};
      Object.keys(centroid).forEach(function (s) {
        (index[s] || []).forEach(function (p) {
          if (seedSet[p.i]) return;
          sim[p.i] = (sim[p.i] || 0) + (centroid[s] / cnorm) * (vec(p.i)[s] || 0);
        });
      });

      var out = [];
      Object.keys(sim).forEach(function (k) {
        var i = +k, s = sim[i];
        // Renvois explicites : le candidat cite un terme trouvé, ou l'inverse.
        var link = 0;
        seeds.forEach(function (sd) {
          docs[sd.i].keys.forEach(function (key) { if (docs[i].defString.indexOf(" " + key + " ") !== -1) link = 1; });
          docs[i].keys.forEach(function (key) { if (docs[sd.i].defString.indexOf(" " + key + " ") !== -1) link = 1; });
        });
        s += link * 0.2;
        if (docs[i].domains.some(function (d) { return docs[seeds[0].i].domains.indexOf(d) !== -1; })) s += 0.03;
        if (s >= (opts.minRelated || 0.22)) out.push({ i: i, score: s, link: !!link });
      });
      // Les termes cités par un résultat (ou qui le citent) sont connexes même avec peu de mots communs.
      for (var i = 0; i < N; i++) {
        if (seedSet[i] || sim[i] !== undefined) continue;
        var linked = false;
        seeds.forEach(function (sd) {
          docs[sd.i].keys.forEach(function (key) { if (docs[i].defString.indexOf(" " + key + " ") !== -1) linked = true; });
          docs[i].keys.forEach(function (key) { if (docs[sd.i].defString.indexOf(" " + key + " ") !== -1) linked = true; });
        });
        if (linked) out.push({ i: i, score: 0.15, link: true });
      }
      out.sort(function (a, b) { return b.score - a.score || a.i - b.i; });
      return out.slice(0, opts.maxRelated || 8);
    }

    return {
      search: function (query, opts) {
        opts = opts || {};
        var q = (query || "").trim();
        if (!q) return { direct: [], related: [], partial: false };
        var all = scoreDirect(q, true);
        var partial = false;
        if (!all.length && tokens(q).length > 1) {
          all = scoreDirect(q, false);
          partial = all.length > 0;
        }
        // Niveau 1 : le mot est dans le nom du terme. Niveau 2 : le mot n'apparaît que
        // dans des définitions ; ces termes parlent du sujet sans porter ce nom.
        var direct = all.filter(function (x) { return x.term; });
        var mentions = all.filter(function (x) { return !x.term; });
        var seeds = direct.length ? direct : mentions;
        var extra = related(seeds, all, opts);
        // Les termes qui ne font que citer le mot : on coupe la longue traîne de faibles correspondances.
        var floor = mentions.length ? Math.max(3, mentions[0].score * 0.4) : 0;
        var rel = mentions.filter(function (x) { return x.score >= floor; }).slice(0, opts.maxMentions || 10);
        var taken = {};
        rel.forEach(function (x) { taken[x.i] = 1; });
        extra.forEach(function (x) { if (!taken[x.i]) rel.push(x); });
        return { direct: direct, related: rel, partial: partial, onlyRelated: !direct.length && rel.length > 0 };
      }
    };
  }

  var core = { createEngine: createEngine, deburr: deburr, stem: stem, tokens: tokens };
  if (typeof module !== "undefined" && module.exports) { module.exports = core; return; }
  root.GlossarySearchCore = core;

  // ---------------------------------------------------------------- interface
  function start() {
    var list = document.getElementById("lex-list");
    var input = document.getElementById("glossary-search");
    var chips = document.getElementById("domain-filters");
    var noResult = document.getElementById("no-result");
    if (!list || !input || !chips) return;

    var style = document.createElement("style");
    style.textContent =
      ".lex-related-title{margin:28px 0 6px;padding-top:14px;border-top:1px solid var(--hairline);" +
      "font-family:'JetBrains Mono',monospace;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--gold)}" +
      ".lex-related-title small{display:block;margin-top:4px;text-transform:none;letter-spacing:0;color:var(--paper-dim);font-size:.78rem}" +
      ".lex-entry.is-related{opacity:.92;border-left:2px solid var(--hairline);padding-left:14px}" +
      ".lex-status{margin:10px 0 0;font-size:.82rem;color:var(--paper-dim)}" +
      ".lex-status:empty{display:none}" +
      // Téléphone : les domaines tiennent sur une ligne qu'on fait glisser, pour que les résultats restent visibles.
      "@media (max-width:720px){.domain-filters{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;" +
      "margin-right:-24px;padding-right:24px;padding-bottom:4px}.domain-filters::-webkit-scrollbar{display:none}" +
      ".domain-filters .filter-chip{flex-shrink:0;white-space:nowrap}}";
    document.head.appendChild(style);

    var entries = Array.prototype.slice.call(list.querySelectorAll(".lex-entry"));
    var domainOrder = [], seen = {};
    var items = entries.map(function (entry) {
      var domains = [];
      entry.querySelectorAll(".lex-domain").forEach(function (el) {
        var d = el.textContent.trim();
        domains.push(d);
        if (!seen[d]) { seen[d] = 1; domainOrder.push(d); }
      });
      entry._domains = domains;
      return { term: entry.querySelector(".lex-term").textContent, def: entry.querySelector(".lex-def").textContent, domains: domains };
    });
    domainOrder.sort();
    var engine = createEngine(items);

    var active = "all";
    function makeChip(val, label) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "filter-chip"; b.dataset.filter = val; b.textContent = label;
      b.addEventListener("click", function () {
        active = val;
        chips.querySelectorAll(".filter-chip").forEach(function (c) { c.classList.toggle("is-active", c.dataset.filter === val); });
        apply();
      });
      chips.appendChild(b);
      return b;
    }
    makeChip("all", "Tous").classList.add("is-active");
    domainOrder.forEach(function (d) { makeChip(d, d); });

    var status = document.createElement("p");
    status.className = "lex-status"; status.setAttribute("aria-live", "polite");
    list.parentNode.insertBefore(status, list);

    var relatedTitle = document.createElement("div");
    relatedTitle.className = "lex-related-title";
    relatedTitle.setAttribute("role", "heading"); relatedTitle.setAttribute("aria-level", "2");
    function setRelatedTitle(onlyRelated) {
      relatedTitle.innerHTML = onlyRelated
        ? "Aucun terme ne porte ce nom<small>Voici ceux qui en parlent ou qui sont sur le même sujet.</small>"
        : "Termes connexes<small>Ils citent ce mot ou parlent du même sujet.</small>";
    }

    function plural(n, w) { return n + " " + w + (n > 1 ? "s" : ""); }

    function apply() {
      var q = input.value.trim();
      var okDomain = function (i) { return active === "all" || entries[i]._domains.indexOf(active) !== -1; };

      if (relatedTitle.parentNode) relatedTitle.parentNode.removeChild(relatedTitle);
      entries.forEach(function (e) { e.classList.remove("is-related"); });

      if (!q) {
        // Retour à l'ordre alphabétique d'origine, filtré par domaine.
        entries.forEach(function (e, i) { list.appendChild(e); e.classList.toggle("is-hidden", !okDomain(i)); });
        status.textContent = "";
        noResult.classList.remove("is-shown");
        return;
      }

      var r = engine.search(q);
      var direct = r.direct.filter(function (x) { return okDomain(x.i); });
      var rel = r.related.filter(function (x) { return okDomain(x.i); });

      var shown = {};
      direct.forEach(function (x) { shown[x.i] = 1; });
      rel.forEach(function (x) { shown[x.i] = 1; });
      entries.forEach(function (e, i) { e.classList.toggle("is-hidden", !shown[i]); });

      direct.forEach(function (x) { list.appendChild(entries[x.i]); });
      if (rel.length) {
        setRelatedTitle(!direct.length);
        list.appendChild(relatedTitle);
        rel.forEach(function (x) { entries[x.i].classList.add("is-related"); list.appendChild(entries[x.i]); });
      }

      var msg = direct.length ? plural(direct.length, "résultat") : "Aucun résultat exact";
      if (r.partial) msg += " (aucun terme ne contient tous les mots)";
      if (rel.length) msg += " · " + plural(rel.length, "terme") + " connexe" + (rel.length > 1 ? "s" : "");
      status.textContent = direct.length || rel.length ? msg : "";
      noResult.classList.toggle("is-shown", !direct.length && !rel.length);
    }

    input.addEventListener("input", apply);
    apply();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})(typeof window !== "undefined" ? window : this);
