/*
 * Barre de navigation du bas — mobile uniquement (≤ 720 px).
 *
 * Partagée par toutes les pages (comme pwa-install.js) : le script injecte
 * lui-même son CSS et son HTML, donc il n'y a rien d'autre à recopier dans
 * les gabarits que la balise <script>. Les liens sont calculés à partir de
 * l'adresse de ce fichier, ce qui fonctionne aussi bien depuis la racine
 * que depuis archives/, hebdo/ ou en/.
 *
 * 4 onglets directs (Accueil, Archives, Glossaire, Le projet) + « Plus »
 * qui ouvre un petit panneau avec les autres liens du menu du haut.
 * Sur mobile, le menu du haut est masqué pour éviter un double menu ;
 * sur ordinateur, rien ne change.
 */
(function () {
  "use strict";

  if (document.getElementById("bottom-nav")) return;

  var script = document.currentScript;
  if (!script) {
    var all = document.getElementsByTagName("script");
    for (var i = 0; i < all.length; i++) {
      if ((all[i].getAttribute("src") || "").indexOf("bottom-nav.js") !== -1) script = all[i];
    }
  }
  var src = script ? script.getAttribute("src") || "" : "";
  var root = src.replace(/assets\/bottom-nav\.js.*$/, "");

  var LANG = (document.documentElement.lang || "fr").slice(0, 2) === "en" ? "en" : "fr";
  var T = LANG === "en"
    ? { nav: "Main navigation", home: "Home", archives: "Archives", glossary: "Glossary", project: "The project",
        more: "More", newsletter: "Newsletter", contact: "Contact", follow: "Follow us", support: "Support us",
        close: "Close" }
    : { nav: "Navigation principale", home: "Accueil", archives: "Archives", glossary: "Glossaire", project: "Le projet",
        more: "Plus", newsletter: "Newsletter", contact: "Contact", follow: "Nous suivre", support: "Soutenir",
        close: "Fermer" };

  function svg(paths) {
    return '<svg aria-hidden="true" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" ' +
           'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + paths + "</svg>";
  }

  // Mêmes pictogrammes que le menu du haut, pour rester cohérent.
  var ICONS = {
    home: svg('<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h3v-6h4v6h3a1 1 0 0 0 1-1v-9"/>'),
    archives: svg('<rect x="4" y="4.5" width="16" height="4" rx="1"/><path d="M5 8.5v9.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8.5"/><line x1="10" y1="13" x2="14" y2="13"/>'),
    glossary: svg('<path d="M12 6.5c-1.6-1.2-3.7-1.7-6-1.7v13c2.3 0 4.4.5 6 1.7 1.6-1.2 3.7-1.7 6-1.7v-13c-2.3 0-4.4.5-6 1.7Z"/><line x1="12" y1="6.5" x2="12" y2="19.5"/>'),
    project: svg('<path d="m12 3 8 4.5-8 4.5-8-4.5Z"/><path d="m4 12 8 4.5 8-4.5"/><path d="m4 16.5 8 4.5 8-4.5"/>'),
    more: svg('<circle cx="5.5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="18.5" cy="12" r="1.3"/>'),
    newsletter: svg('<rect x="3.5" y="5.5" width="17" height="13" rx="1.5"/><path d="M4.5 7 12 12.5 19.5 7"/>'),
    contact: svg('<path d="M4 6.5A1.5 1.5 0 0 1 5.5 5h13A1.5 1.5 0 0 1 20 6.5v8a1.5 1.5 0 0 1-1.5 1.5H10l-4 3.5V16H5.5A1.5 1.5 0 0 1 4 14.5Z"/>'),
    follow: svg('<path d="M6 10.5a6 6 0 0 1 12 0c0 3.2 1 4.7 1.5 5.3H4.5C5 15.2 6 13.7 6 10.5Z"/><path d="M10.3 18.5a1.8 1.8 0 0 0 3.4 0"/>'),
    support: svg('<path d="M5 9h11v6a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4Z"/><path d="M16 10.5h1.5a2 2 0 0 1 0 4H16"/><path d="M8.5 4.5c-.6.7-.6 1.3 0 2M12 4.5c-.6.7-.6 1.3 0 2"/>')
  };

  // Page courante → onglet actif.
  var path = location.pathname.replace(/\/+$/, "");
  var file = path.split("/").pop() || "index.html";
  if (file.indexOf(".") === -1) file += ".html";
  var inArchives = /\/archives\//.test(path) || file === "archives.html";
  var active = "";
  if (file === "index.html" && !inArchives && !/\/(hebdo|themes|suivi)\//.test(path)) active = "home";
  else if (inArchives || /\/(hebdo|themes|suivi)\//.test(path)) active = "archives";
  else if (file === "glossaire.html") active = "glossary";
  else if (file === "le-projet.html") active = "project";
  else if (file === "newsletter.html" || file === "contact.html") active = "more";

  var tabs = [
    { id: "home", href: root + "index.html", label: T.home },
    { id: "archives", href: root + "archives.html", label: T.archives },
    { id: "glossary", href: root + "glossaire.html", label: T.glossary },
    { id: "project", href: root + "le-projet.html", label: T.project }
  ];
  var more = [
    { id: "newsletter", href: root + "newsletter.html", label: T.newsletter },
    { id: "contact", href: root + "contact.html", label: T.contact },
    { id: "follow", href: root + "index.html#nous-suivre", label: T.follow },
    { id: "support", href: "https://buymeacoffee.com/scenario", label: T.support, external: true, gold: true }
  ];

  var css =
    "#bottom-nav,#bottom-nav-sheet,#bottom-nav-backdrop{display:none}" +
    "@media (max-width:720px){" +
    "html.has-bottom-nav nav.topnav{display:none}" +
    "html.has-bottom-nav body{padding-bottom:calc(68px + env(safe-area-inset-bottom,0px))}" +
    "#bottom-nav{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:9000;" +
    "background:#1a212b;border-top:1px solid #2c3644;" +
    "padding:0 4px env(safe-area-inset-bottom,0px);font-family:'JetBrains Mono',monospace}" +
    "#bottom-nav a,#bottom-nav button{flex:1 1 0;min-width:0;height:62px;display:flex;flex-direction:column;" +
    "align-items:center;justify-content:center;gap:4px;position:relative;background:none;border:0;margin:0;" +
    "padding:0;color:#a9a89c;text-decoration:none;font:inherit;cursor:pointer;" +
    "-webkit-tap-highlight-color:transparent}" +
    "#bottom-nav .bn-label{font-size:.62rem;letter-spacing:.04em;text-transform:uppercase;line-height:1;" +
    "max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}" +
    "#bottom-nav a:active,#bottom-nav button:active{color:#ece7da}" +
    "#bottom-nav [aria-current='page'],#bottom-nav button[aria-expanded='true']{color:#cf9d4c}" +
    "#bottom-nav [aria-current='page']::before,#bottom-nav button.is-active::before{content:'';position:absolute;" +
    "top:0;left:28%;right:28%;height:2px;border-radius:0 0 2px 2px;background:#cf9d4c}" +
    "#bottom-nav-backdrop{position:fixed;inset:0;z-index:8990;background:rgba(0,0,0,.45)}" +
    "#bottom-nav-backdrop.is-open{display:block}" +
    "#bottom-nav-sheet{position:fixed;left:12px;right:12px;z-index:8995;" +
    "bottom:calc(72px + env(safe-area-inset-bottom,0px));background:#1a212b;border:1px solid #2c3644;" +
    "border-top:3px solid #cf9d4c;border-radius:12px;padding:6px;box-shadow:0 10px 30px rgba(0,0,0,.5);" +
    "font-family:'JetBrains Mono',monospace}" +
    "#bottom-nav-sheet.is-open{display:block}" +
    "#bottom-nav-sheet a{display:flex;align-items:center;gap:14px;padding:14px 12px;border-radius:8px;" +
    "color:#ece7da;text-decoration:none;font-size:.82rem;letter-spacing:.06em;text-transform:uppercase}" +
    "#bottom-nav-sheet a+a{border-top:1px solid #2c3644;border-radius:0}" +
    "#bottom-nav-sheet a:active{background:#212a35}" +
    "#bottom-nav-sheet a.is-gold{color:#cf9d4c}" +
    "#bottom-nav-sheet a[aria-current='page']{color:#cf9d4c}" +
    // Le bandeau « Installer l'application » ne doit pas passer sous la barre.
    "html.has-bottom-nav .pwa-install-banner{margin-bottom:calc(68px + env(safe-area-inset-bottom,0px))}" +
    "}" +
    "@media print{#bottom-nav,#bottom-nav-sheet,#bottom-nav-backdrop{display:none!important}}";

  var style = document.createElement("style");
  style.id = "bottom-nav-style";
  style.textContent = css;
  document.head.appendChild(style);

  function tabHtml(t) {
    return '<a href="' + t.href + '"' + (active === t.id ? ' aria-current="page"' : "") + ">" +
           ICONS[t.id] + '<span class="bn-label">' + t.label + "</span></a>";
  }

  var nav = document.createElement("nav");
  nav.id = "bottom-nav";
  nav.setAttribute("aria-label", T.nav);
  nav.innerHTML =
    tabs.map(tabHtml).join("") +
    '<button type="button" id="bottom-nav-more" aria-haspopup="true" aria-expanded="false" aria-controls="bottom-nav-sheet"' +
    (active === "more" ? ' class="is-active"' : "") + ">" +
    ICONS.more + '<span class="bn-label">' + T.more + "</span></button>";

  var sheet = document.createElement("div");
  sheet.id = "bottom-nav-sheet";
  sheet.innerHTML = more.map(function (m) {
    var cur = active === "more" && m.href.indexOf(file) !== -1 && file !== "index.html";
    return '<a href="' + m.href + '"' + (m.gold ? ' class="is-gold"' : "") + (cur ? ' aria-current="page"' : "") +
           (m.external ? ' target="_blank" rel="noopener noreferrer"' : "") + ">" +
           ICONS[m.id] + "<span>" + m.label + "</span></a>";
  }).join("");

  var backdrop = document.createElement("div");
  backdrop.id = "bottom-nav-backdrop";

  function setOpen(open) {
    sheet.classList.toggle("is-open", open);
    backdrop.classList.toggle("is-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  document.body.appendChild(backdrop);
  document.body.appendChild(sheet);
  document.body.appendChild(nav);
  document.documentElement.classList.add("has-bottom-nav");

  var btn = document.getElementById("bottom-nav-more");
  btn.addEventListener("click", function () { setOpen(!sheet.classList.contains("is-open")); });
  backdrop.addEventListener("click", function () { setOpen(false); });
  sheet.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
  window.addEventListener("pageshow", function () { setOpen(false); });
})();
