/* Bouton « Écouter » en tête d'une édition.

   Amélioration progressive : le HTML de l'édition n'est pas modifié. Si un épisode audio existe pour la date
   de l'édition (liste data/podcast-episodes.json, tenue à jour par le workflow « Podcast — épisode du jour »),
   un bouton s'affiche au-dessus du sommaire ; un clic ouvre un lecteur. Sans épisode, sans JavaScript ou si la liste
   est introuvable, rien ne change.
   Respect de la vie privée : le fichier audio (hébergé sur GitHub) n'est demandé qu'au clic, jamais au chargement
   de la page. La voix est une voix de synthèse : la page le dit à côté du lecteur.
   Demandé le 3 octobre 2026. */
(function () {
  "use strict";
  var script = document.currentScript;
  if (!script || !window.fetch) return;
  var base = (script.getAttribute("src") || "").replace(/assets\/edition-audio\.js.*$/, "");
  var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
  var meta = document.querySelector('meta[property="article:published_time"]');
  var date = meta && (meta.getAttribute("content") || "").slice(0, 10);
  if (!date) {
    var m = location.pathname.match(/(\d{4}-\d{2}-\d{2})\.html/);
    date = m && m[1];
  }
  var toc = document.querySelector("nav.toc");
  if (!date || !toc) return;

  var css = [
    "@media screen{",
    ".ea{margin:0 0 18px}",
    ".ea-btn{display:inline-flex;align-items:center;gap:11px;padding:10px 18px 10px 14px;background:transparent;color:var(--paper,#e6e1d4);border:1px solid var(--gold,#cf9d4c);border-radius:999px;font-family:'Fraunces',Georgia,serif;font-size:1.02rem;font-weight:500;line-height:1.2;cursor:pointer;transition:background .15s,color .15s}",
    ".ea-btn:hover,.ea-btn[aria-expanded='true']{background:var(--gold,#cf9d4c);color:var(--ink,#10151c)}",
    ".ea-btn:focus-visible{outline:2px solid var(--gold,#cf9d4c);outline-offset:3px}",
    ".ea-btn svg{flex:none}",
    ".ea-dur{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.72rem;letter-spacing:.06em;opacity:.8}",
    ".ea-panel{margin-top:12px;max-width:520px}",
    ".ea-panel audio{display:block;width:100%}",
    ".ea-note{margin:8px 0 0;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--paper-dim,#b4b2a6)}",
    "}",
    "@media print{.ea{display:none}}"
  ].join("");

  function duree(s) {
    s = Math.round(Number(s) || 0);
    if (!s) return "";
    return Math.floor(s / 60) + " min" + (s % 60 ? " " + (s % 60 < 10 ? "0" : "") + (s % 60) + " s" : "");
  }

  function build(ep) {
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    var wrap = document.createElement("div");
    wrap.className = "ea";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "ea-btn";
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", "ea-panel");
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.2"/><rect x="17" y="14" width="4" height="6" rx="1.2"/></svg>';
    var label = document.createElement("span");
    label.textContent = isEn ? "Listen (audio in French)" : "Écouter l'édition";
    btn.appendChild(label);
    var d = duree(ep.duree);
    if (d) {
      var dur = document.createElement("span");
      dur.className = "ea-dur";
      dur.textContent = d;
      btn.appendChild(dur);
    }
    var panel = document.createElement("div");
    panel.className = "ea-panel";
    panel.id = "ea-panel";
    panel.hidden = true;
    wrap.appendChild(btn);
    wrap.appendChild(panel);

    var audio = null;
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      if (open) {
        btn.setAttribute("aria-expanded", "false");
        panel.hidden = true;
        if (audio) audio.pause();
        return;
      }
      btn.setAttribute("aria-expanded", "true");
      panel.hidden = false;
      if (!audio) {
        audio = document.createElement("audio");
        audio.controls = true;
        audio.preload = "auto";
        audio.setAttribute("aria-label", isEn ? "Audio version of this edition (French)" : "Version audio de cette édition");
        audio.src = ep.url;  /* première requête vers le fichier : au clic seulement */
        var note = document.createElement("p");
        note.className = "ea-note";
        note.textContent = isEn ? "Synthetic voice (AI). Text drawn from this edition." : "Voix de synthèse (IA). Texte tiré de cette édition.";
        panel.appendChild(audio);
        panel.appendChild(note);
      }
      var p = audio.play();
      if (p && p.catch) p.catch(function () { /* le lecteur reste affiché : l'utilisateur peut lancer la lecture */ });
    });
    toc.parentNode.insertBefore(wrap, toc);
  }

  fetch(base + "data/podcast-episodes.json", { cache: "no-cache" })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (list) {
      if (!Array.isArray(list)) return;
      for (var i = 0; i < list.length; i++) {
        if (list[i] && list[i].date === date && /^https:\/\//.test(list[i].url || "")) { build(list[i]); return; }
      }
    })
    .catch(function () { /* pas de bouton, la page reste comme avant */ });
})();
