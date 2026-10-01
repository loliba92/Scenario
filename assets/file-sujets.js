/*
 * Page « File de sujets » (file-sujets.html) — lecture seule de data/sujets.json.
 *
 * Même porte d'accès que dashboard.html (clé en mémoire locale) : sans elle, la page
 * renvoie vers le tableau de bord. La page lit data/sujets.json ; la seule écriture est le
 * boutons d'un sujet — « Valider » (sujet « à valider »), « Passer en priorité absolue »,
 * « Retirer de la priorité » : ils déclenchent le workflow valider-sujets.yml par l'API GitHub, avec un jeton personnel saisi une fois et gardé dans ce navigateur
 * seulement. Pour le reste, on édite data/sujets.json (ou sujets-prioritaires.md, qui est
 * synchronisé) ; pour compléter les dossiers incomplets, on lance le workflow
 * « Enrichir les dossiers de sujets ».
 *
 * La règle « dossier complet » est la même que scripts/edition/sujets.py (manquants()).
 */
(function () {
  "use strict";

  // ---- porte d'accès (copie de dashboard.html : même hash, même clé) ----
  var HASH = "a9d52f2653bec32bf7f3b688832f285b663ae56d4ee30acb3d57122725bcfad3";
  var STORAGE_KEY = "scenario-dash-auth";
  var ok = false;
  try { ok = localStorage.getItem(STORAGE_KEY) === HASH; } catch (e) { ok = false; }
  var verrou = document.getElementById("verrou");
  var app = document.getElementById("app");
  if (!ok) { verrou.hidden = false; return; }
  app.hidden = false;

  // ---- règle de complétude (miroir de sujets.py) ----
  var MIN_CONTEXTE = 80, MIN_RATIONNEL = 60, MIN_MOTS_CLES = 3;
  function txt(v) { return (v || "").trim(); }
  function manquants(e) {
    var m = [];
    if (!(txt(e.question) || txt(e.titre).slice(-1) === "?")) m.push("question");
    if (txt(e.contexte).length < MIN_CONTEXTE) m.push("contexte");
    if (txt(e.rationnel).length < MIN_RATIONNEL) m.push("rationnel");
    if ((e.mots_cles || []).filter(function (k) { return txt(k); }).length < MIN_MOTS_CLES) m.push("mots-clés");
    return m;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  // Espace insécable avant « ? ! : ; » : le signe ne passe pas seul à la ligne.
  function typo(s) { return esc(s).replace(/ (?=[?!:;»])/g, "&nbsp;"); }
  var MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."];
  function fmtDate(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    return m ? (+m[3]) + " " + MOIS[+m[2] - 1] + " " + m[1] : "";
  }
  function plur(n, mot) { return n + " " + mot + (n > 1 ? "s" : ""); }

  var NOMS = { priorite_absolue: "Priorité absolue", carte_blanche: "Carte blanche (mardi)", geopolitique: "Géopolitique (lundi)",
    actualite_francaise: "Actu. française (mercredi)", economie: "Économie & finance (jeudi)", sciences: "Sciences (vendredi)",
    culture: "Culture (samedi)", sport: "Sport (dimanche)" };
  function nomSection(sec) { return NOMS[sec.cle] || sec.titre; }

  // ---- validation par bouton (workflow valider-sujets.yml) ----
  var DEPOT = "loliba92/Scenario", WORKFLOW = "valider-sujets.yml", BRANCHE = "main";
  var JETON_KEY = "scenario-gh-token";          // jeton personnel, gardé dans ce navigateur seulement
  var ATTENTE_KEY = "scenario-sujets-valides";  // validations envoyées mais pas encore publiées sur le site
  var ATTENTE_MS = 20 * 60 * 1000;
  function lire(cle) { try { return localStorage.getItem(cle); } catch (e) { return null; } }
  function ecrire(cle, v) { try { if (v == null) localStorage.removeItem(cle); else localStorage.setItem(cle, v); } catch (e) {} }
  function enAttente() {   // { id: {a: action, t: instant} }
    var m = {}, maintenant = Date.now();
    try { m = JSON.parse(lire(ATTENTE_KEY) || "{}") || {}; } catch (e) { m = {}; }
    Object.keys(m).forEach(function (id) { if (!m[id] || maintenant - m[id].t > ATTENTE_MS) delete m[id]; });
    return m;
  }
  function noterAttente(id, action) { var m = enAttente(); m[id] = { a: action, t: Date.now() }; ecrire(ATTENTE_KEY, JSON.stringify(m)); }
  function message(texte, erreur) {
    var z = document.getElementById("action-statut");
    z.textContent = texte; z.className = "action-statut" + (erreur ? " erreur" : ""); z.hidden = !texte;
  }
  function demanderJeton() {
    var j = window.prompt("Pour valider un sujet depuis cette page, collez un jeton GitHub personnel (une seule fois ; il reste dans ce navigateur).\n\n" +
      "Créez-le sur github.com > Settings > Developer settings > Fine-grained tokens : dépôt " + DEPOT +
      " uniquement, droit « Actions : Read and write », rien d'autre.");
    j = (j || "").trim();
    if (j) ecrire(JETON_KEY, j);
    majPied();
    return j;
  }
  function majPied() { document.getElementById("jeton-zone").hidden = !lire(JETON_KEY); }

  var TEXTES = {
    valider: { envoi: "Envoi de la validation…", ok: "Sujet validé." },
    prioriser: { envoi: "Envoi : passage en priorité absolue…", ok: "Sujet passé en priorité absolue : il sera traité avant tout le reste." },
    deprioriser: { envoi: "Envoi : retrait de la priorité…", ok: "Sujet retiré de la priorité : il retrouve la tête de son registre." }
  };
  var CONFIRMATION = {
    prioriser: "Passer ce sujet en priorité absolue ?\n\nIl sera traité en premier, quel que soit le registre du jour, avant tous les autres sujets."
  };

  function agir(action, id, bouton) {
    if (CONFIRMATION[action] && !window.confirm(CONFIRMATION[action])) return;
    var jeton = lire(JETON_KEY) || demanderJeton();
    if (!jeton) { message("Action annulée : aucun jeton enregistré.", true); return; }
    bouton.disabled = true;
    message(TEXTES[action].envoi);
    fetch("https://api.github.com/repos/" + DEPOT + "/actions/workflows/" + WORKFLOW + "/dispatches", {
      method: "POST",
      headers: { "Accept": "application/vnd.github+json", "Authorization": "Bearer " + jeton, "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json" },
      body: JSON.stringify({ ref: BRANCHE, inputs: { action: action, ids: id } })
    }).then(function (r) {
      if (r.status === 204) {
        var s = sujets.filter(function (x) { return x.e.id === id; })[0];
        if (s) appliquer(s, action);
        noterAttente(id, action);
        message(TEXTES[action].ok + " L'enregistrement dans la file prend une à deux minutes ; le site est mis à jour ensuite.");
        rendreResume(); filtrer();
        return;
      }
      bouton.disabled = false;
      if (r.status === 401) { ecrire(JETON_KEY, null); majPied(); message("Jeton refusé (expiré ou incorrect) : il a été effacé, recliquez pour en saisir un nouveau.", true); }
      else if (r.status === 403 || r.status === 404) message("Accès refusé : le jeton doit couvrir le dépôt " + DEPOT + " avec le droit « Actions : Read and write ».", true);
      else message("GitHub a répondu " + r.status + " : action non envoyée.", true);
    }).catch(function () {
      bouton.disabled = false;
      message("Réseau indisponible : action non envoyée.", true);
    });
  }

  // Sujet d'une section vers une autre, en tête (même règle que sujets.py : _mettre_en_tete).
  function deplacer(s, cible) {
    var i = sujets.indexOf(s);
    sujets.splice(i, 1);
    var pos = sujets.findIndex(function (x) { return x.sec === cible; });
    if (pos < 0) pos = sujets.length;
    s.sec = cible;
    sujets.splice(pos, 0, s);
  }
  function sectionOrigine(id) {   // « economie-… » -> economie ; « actualite-francaise-… » -> actualite_francaise
    return sections.filter(function (sec) {
      return sec.cle !== "priorite_absolue" && id.indexOf(sec.cle.replace(/_/g, "-") + "-") === 0;
    })[0] || null;
  }
  function appliquer(s, action) {   // mêmes effets que sujets.py, sans attendre la publication du site
    if (action === "valider") s.e.validation = "valide";
    if (action === "prioriser" && s.sec.cle !== "priorite_absolue" && s.e.statut === "a_traiter") {
      s.e.validation = "valide";
      deplacer(s, sections.filter(function (x) { return x.cle === "priorite_absolue"; })[0]);
    }
    if (action === "deprioriser" && s.sec.cle === "priorite_absolue" && s.e.statut === "a_traiter") {
      var o = sectionOrigine(s.e.id);
      if (o) deplacer(s, o);
    }
    recalculerProchain();
  }

  var sujets = [];          // {e, sec, prochain, manque}
  var sections = [];
  var engine = null;

  function recalculerProchain() {
    sections.forEach(function (sec) {
      var premier = true;
      sujets.forEach(function (s) {
        if (s.sec !== sec) return;
        s.prochain = false;
        if (premier && s.e.statut === "a_traiter" && s.e.validation === "valide") { s.prochain = true; premier = false; }
      });
    });
  }

  function preparer(data) {
    sections = data.sections;
    sections.forEach(function (sec) {
      sec.entrees.forEach(function (e) {
        if (e.type !== "sujet") return;
        sujets.push({ e: e, sec: sec, prochain: false, manque: manquants(e) });
      });
    });
    // Actions envoyées il y a peu : le site publié peut ne pas encore les contenir.
    var attente = enAttente();
    sujets.slice().forEach(function (s) { if (attente[s.e.id]) appliquer(s, attente[s.e.id].a); });
    recalculerProchain();
    var core = window.GlossarySearchCore;
    if (core) {
      engine = core.createEngine(sujets.map(function (s) {
        return { term: s.e.titre, def: [s.e.question, s.e.contexte, s.e.rationnel, (s.e.mots_cles || []).join(" ")].filter(Boolean).join(" "), domains: [s.sec.cle] };
      }));
    }
  }

  // ---- résumé ----
  function rendreResume() {
    var aTraiter = sujets.filter(function (s) { return s.e.statut === "a_traiter"; });
    var complets = aTraiter.filter(function (s) { return !s.manque.length; });
    var aValider = aTraiter.filter(function (s) { return s.e.validation === "a_valider"; });
    var publies = sujets.filter(function (s) { return s.e.statut === "publie"; });
    document.getElementById("stats").innerHTML =
      '<div class="stat"><b>' + aTraiter.length + "</b><span>à traiter</span></div>" +
      '<div class="stat"><b>' + complets.length + "</b><span>dossiers complets</span></div>" +
      '<div class="stat"><b>' + aValider.length + "</b><span>à valider 🔍</span></div>" +
      '<div class="stat"><b>' + publies.length + "</b><span>publiés</span></div>";
    var pct = aTraiter.length ? Math.round(100 * complets.length / aTraiter.length) : 100;
    document.getElementById("barre").style.width = pct + "%";
    document.getElementById("barre-note").textContent =
      complets.length + " sujet(s) à traiter sur " + aTraiter.length + " ont un dossier complet (" + pct + " %). " +
      (aTraiter.length - complets.length ? "Les autres attendent d'être enrichis." : "Tout est prêt.");

    var lignes = ['<tr><th>Registre</th><th>À traiter</th><th>Complets</th><th>À valider</th><th>Publiés</th><th>Dernier</th></tr>'];
    sections.forEach(function (sec) {
      var s = sujets.filter(function (x) { return x.sec === sec; });
      var at = s.filter(function (x) { return x.e.statut === "a_traiter"; });
      var pub = s.filter(function (x) { return x.e.statut === "publie"; });
      var dernier = pub.map(function (x) { return x.e.edition || ""; }).sort().pop() || "";
      var cplt = at.filter(function (x) { return !x.manque.length; }).length;
      var tension = at.filter(function (x) { return x.e.validation === "valide"; }).length <= 2 && sec.cle !== "priorite_absolue";
      lignes.push("<tr><td>" + esc(nomSection(sec)) + "</td><td" + (tension ? ' class="bad"' : "") + ">" + at.length + "</td><td>" + cplt +
        "</td><td>" + at.filter(function (x) { return x.e.validation === "a_valider"; }).length + "</td><td>" + pub.length +
        "</td><td>" + esc(dernier ? fmtDate(dernier) : "—") + "</td></tr>");
    });
    document.getElementById("registres").innerHTML = lignes.join("");

    var sel = document.getElementById("f-registre");
    sel.innerHTML = '<option value="">Tous les registres</option>' + sections.map(function (sec) {
      return '<option value="' + esc(sec.cle) + '">' + esc(nomSection(sec)) + "</option>";
    }).join("");
  }

  // ---- carte d'un sujet ----
  function champ(titre, contenu, manquant) {
    return '<div class="f"><h3>' + titre + "</h3>" +
      (contenu ? contenu : '<p class="vide">' + (manquant || "Non renseigné") + "</p>") + "</div>";
  }

  function dossierTexte(s) {
    var e = s.e, l = ["Identifiant : " + e.id, "Registre : " + nomSection(s.sec), "Titre : " + e.titre];
    if (txt(e.question) && txt(e.question) !== e.titre) l.push("Question : " + e.question);
    if (txt(e.contexte)) l.push("Contexte : " + e.contexte);
    if (txt(e.rationnel)) l.push("Rationnel : " + e.rationnel);
    if (txt(e.angle)) l.push("Angle : " + e.angle);
    if (txt(e.a_verifier)) l.push("À vérifier : " + e.a_verifier);
    if ((e.mots_cles || []).length) l.push("Mots-clés : " + e.mots_cles.join(" ; "));
    if (e.scenarios) l.push("Scénarios (brouillon) : favorable = " + e.scenarios.favorable + " ; stable = " + e.scenarios.stable + " ; dégradé = " + e.scenarios.degrade);
    if ((e.sources || []).length) l.push("Sources : " + e.sources.map(function (x) { return x.titre + (x.url ? " <" + x.url + ">" : ""); }).join(" ; "));
    return l.join("\n");
  }

  function carte(s) {
    var e = s.e;
    var badges = '<span class="badge">' + esc(nomSection(s.sec)) + "</span>";
    if (s.prochain) badges += '<span class="badge next">Prochain</span>';
    if (e.validation === "a_valider") badges += '<span class="badge warn">🔍 À valider</span>';
    if (e.statut === "publie") badges += '<span class="badge ok">Publié' + (e.edition ? " le " + esc(fmtDate(e.edition)) : "") + "</span>";
    if (s.manque.length && e.statut === "a_traiter") badges += '<span class="badge inc">Incomplet · ' + esc(s.manque.join(", ")) + "</span>";

    var corps = "";
    if (txt(e.question) && txt(e.question) !== e.titre) corps += champ("Question à issue ouverte", "<p>" + esc(e.question) + "</p>");
    corps += champ("Contexte — ce qui se passe", txt(e.contexte) ? "<p>" + esc(e.contexte) + "</p>" : "");
    corps += champ("Rationnel — pourquoi ce sujet, pourquoi l'issue est ouverte", txt(e.rationnel) ? "<p>" + esc(e.rationnel) + "</p>" : "");
    if (txt(e.angle)) corps += champ("Angle", "<p>" + esc(e.angle) + "</p>");
    if (txt(e.a_verifier)) corps += champ("À vérifier avant rédaction", "<p>" + esc(e.a_verifier) + "</p>");
    corps += champ("Mots-clés pour chercher les articles", (e.mots_cles || []).length ?
      '<div class="chips">' + e.mots_cles.map(function (k) {
        return '<a class="chip" target="_blank" rel="noopener" href="https://news.google.com/search?hl=fr&gl=FR&ceid=FR:fr&q=' + encodeURIComponent(k) + '">' + esc(k) + "</a>";
      }).join("") + "</div>" : "");
    if (e.scenarios) {
      corps += champ("Scénarios (brouillon)", '<div class="scen">' +
        '<div class="favorable"><b>Favorable</b>' + esc(e.scenarios.favorable) + "</div>" +
        '<div class="stable"><b>Stable</b>' + esc(e.scenarios.stable) + "</div>" +
        '<div class="degrade"><b>Dégradé</b>' + esc(e.scenarios.degrade) + "</div></div>");
    }
    if (e.echeance) corps += champ("Échéance", "<p>" + esc(fmtDate(e.echeance.date) || e.echeance.date) + (e.echeance.raison ? " — " + esc(e.echeance.raison) : "") + "</p>");
    if ((e.sources || []).length) {
      corps += champ("Pistes de sources", "<p>" + e.sources.map(function (x) {
        return x.url ? '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.titre) + "</a>" : esc(x.titre);
      }).join("<br>") + "</p>");
    }
    if (txt(e.note)) corps += champ("Note éditoriale (historique)", '<p class="note">' + esc(e.note) + "</p>");

    var meta = "<code>" + esc(e.id) + "</code>" +
      (e.tag ? " · " + esc(e.tag) : "") +
      (e.origine ? " · origine : " + esc(e.origine) : "") +
      (e.ajoute_le ? " · ajouté le " + esc(fmtDate(e.ajoute_le)) : "") +
      (e.enrichi_le ? " · enrichi le " + esc(fmtDate(e.enrichi_le)) : "");

    return '<details class="sj" data-id="' + esc(e.id) + '"><summary><div class="badges">' + badges + '</div><div class="titre">' + typo(e.titre) +
      '</div></summary><div class="corps">' + corps +
      '<div class="meta">' + meta + '<div class="actions">' +
      (e.validation === "a_valider" && e.statut === "a_traiter" ? '<button type="button" class="btn btn-valider" data-action="valider" data-id="' + esc(e.id) + '">✓ Valider ce sujet</button>' : "") +
      (e.statut === "a_traiter" && s.sec.cle !== "priorite_absolue" ? '<button type="button" class="btn btn-prio" data-action="prioriser" data-id="' + esc(e.id) + '">🔥 Passer en priorité absolue</button>' : "") +
      (e.statut === "a_traiter" && s.sec.cle === "priorite_absolue" && sectionOrigine(e.id) ? '<button type="button" class="btn" data-action="deprioriser" data-id="' + esc(e.id) + '">Retirer de la priorité</button>' : "") +
      '<button type="button" class="btn" data-copier="' + esc(e.id) + '">Copier le dossier</button>' +
      '<button type="button" class="btn" data-copier-id="' + esc(e.id) + '">Copier l\'identifiant</button></div></div></div></details>';
  }

  // ---- liste filtrée ----
  function filtrer() {
    var q = document.getElementById("q").value.trim();
    var reg = document.getElementById("f-registre").value;
    var st = document.getElementById("f-statut").value;
    var dos = document.getElementById("f-dossier").value;

    var liste = sujets.filter(function (s) {
      if (reg && s.sec.cle !== reg) return false;
      if (st !== "tous" && s.e.statut !== st) return false;
      if (dos === "incomplet" && !s.manque.length) return false;
      if (dos === "complet" && s.manque.length) return false;
      if (dos === "a_valider" && s.e.validation !== "a_valider") return false;
      return true;
    });

    var ordonne = liste;
    if (q && engine) {
      var res = engine.search(q, { flat: true, minRelated: 9 });
      var rang = {};
      res.direct.forEach(function (x, i) { rang[x.i] = i; });
      ordonne = liste.filter(function (s) { return rang[sujets.indexOf(s)] !== undefined; })
        .sort(function (a, b) { return rang[sujets.indexOf(a)] - rang[sujets.indexOf(b)]; });
    }

    document.getElementById("compte").textContent = plur(ordonne.length, "sujet") +
      (q ? " pour « " + q + " »" : "");
    var zone = document.getElementById("liste");
    if (!ordonne.length) { zone.innerHTML = '<p class="vide-liste">Aucun sujet ne correspond.</p>'; return; }

    var html = "", dernier = null;
    ordonne.forEach(function (s) {
      if (!q && s.sec !== dernier) { html += '<h2 class="groupe">' + esc(nomSection(s.sec)) + "</h2>"; dernier = s.sec; }
      html += carte(s);
    });
    zone.innerHTML = html;
  }

  // ---- actions ----
  document.addEventListener("click", function (ev) {
    var v = ev.target.closest("[data-action]");
    if (v) { agir(v.getAttribute("data-action"), v.getAttribute("data-id"), v); return; }
    if (ev.target.closest("#oublier-jeton")) { ecrire(JETON_KEY, null); majPied(); message("Jeton effacé de ce navigateur."); return; }
    var b = ev.target.closest("[data-copier],[data-copier-id]");
    if (!b) return;
    var id = b.getAttribute("data-copier") || b.getAttribute("data-copier-id");
    var s = sujets.filter(function (x) { return x.e.id === id; })[0];
    if (!s) return;
    var texte = b.hasAttribute("data-copier") ? dossierTexte(s) : id;
    var fait = function () { var t = b.textContent; b.textContent = "Copié ✓"; setTimeout(function () { b.textContent = t; }, 1600); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(texte).then(fait, function () {});
  });

  var minuteur = null;
  ["f-registre", "f-statut", "f-dossier"].forEach(function (id) { document.getElementById(id).addEventListener("change", filtrer); });
  document.getElementById("q").addEventListener("input", function () { clearTimeout(minuteur); minuteur = setTimeout(filtrer, 150); });

  majPied();
  fetch("data/sujets.json?v=" + Date.now()).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function (data) {
    preparer(data);
    rendreResume();
    filtrer();
  }).catch(function () {
    document.getElementById("compte").textContent = "Impossible de charger data/sujets.json.";
  });
})();
