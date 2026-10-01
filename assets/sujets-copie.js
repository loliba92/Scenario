/*
 * Copie d'un sujet de la file : « Copier le dossier » (texte complet, à coller dans une
 * conversation ou un brief) et « Copier l'identifiant » (à recopier dans sujet.origine_id).
 * Partagé par la page « File de sujets » (file-sujets.js) et par le dashboard
 * (dashboard-sujets.js), pour que les deux produisent exactement le même texte.
 */
(function (root) {
  "use strict";

  var NOMS = { priorite_absolue: "Priorité absolue", carte_blanche: "Carte blanche (mardi)", geopolitique: "Géopolitique (lundi)",
    actualite_francaise: "Actu. française (mercredi)", economie: "Économie & finance (jeudi)", sciences: "Sciences (vendredi)",
    culture: "Culture (samedi)", sport: "Sport (dimanche)" };

  function txt(v) { return (v || "").trim(); }
  function nomSection(sec) { return NOMS[sec.cle] || sec.titre; }

  function dossierTexte(sec, e) {
    var l = ["Identifiant : " + e.id, "Registre : " + nomSection(sec), "Titre : " + e.titre];
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

  // Copie dans le presse-papiers (repli pour les navigateurs sans l'API moderne) puis « Copié ✓ » sur le bouton.
  function copier(texte, bouton) {
    var fait = function () {
      var t = bouton.getAttribute("data-libelle") || bouton.textContent;
      bouton.setAttribute("data-libelle", t);
      bouton.textContent = "Copié ✓";
      setTimeout(function () { bouton.textContent = t; }, 1600);
    };
    if (root.navigator && root.navigator.clipboard && root.navigator.clipboard.writeText) {
      root.navigator.clipboard.writeText(texte).then(fait, function () {});
      return;
    }
    var z = document.createElement("textarea");
    z.value = texte; z.style.position = "fixed"; z.style.opacity = "0";
    document.body.appendChild(z); z.select();
    try { if (document.execCommand("copy")) fait(); } catch (e) {}
    document.body.removeChild(z);
  }

  root.SujetsCopie = { nomSection: nomSection, dossierTexte: dossierTexte, copier: copier };
})(window);
