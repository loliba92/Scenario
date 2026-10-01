/*
 * Dashboard : ajoute « Copier le dossier » et « Copier l'identifiant » sous chaque sujet de la
 * file (agenda, « Ensuite », « Derniers sujets identifiés »). Les blocs HTML sont produits par
 * scripts/seo/update_audience.py et generate_hot_topics.py, avec l'identifiant du sujet dans
 * data-sujet-id ; le dossier lui-même est lu dans data/sujets.json à l'ouverture de la page.
 */
(function () {
  "use strict";
  var cibles = document.querySelectorAll("[data-sujet-id]");
  if (!cibles.length || !window.SujetsCopie) return;

  function bouton(libelle, texte) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "copy-btn"; b.textContent = libelle;
    b.addEventListener("click", function (ev) { ev.preventDefault(); window.SujetsCopie.copier(texte, b); });
    return b;
  }

  fetch("data/sujets.json?v=" + Date.now()).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function (data) {
    var index = {};
    data.sections.forEach(function (sec) {
      sec.entrees.forEach(function (e) { if (e.type === "sujet") index[e.id] = { sec: sec, e: e }; });
    });
    Array.prototype.forEach.call(cibles, function (el) {
      var s = index[el.getAttribute("data-sujet-id")];
      if (!s) return;
      var barre = document.createElement("div");
      barre.className = "copy-bar";
      barre.appendChild(bouton("Copier le dossier", window.SujetsCopie.dossierTexte(s.sec, s.e)));
      barre.appendChild(bouton("Copier l'identifiant", s.e.id));
      el.appendChild(barre);
    });
  }).catch(function () { /* sans le fichier, le dashboard reste lisible, sans boutons */ });
})();
