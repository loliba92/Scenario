/*
 * Bandeau discret « Scénario dans vos sources Google » — partagé par les pages vivantes et les éditions du jour (4 octobre 2026).
 * Apparaît quelques secondes après l'ouverture du site, puis revient de temps en temps : 21 jours après une fermeture, 1 an après un
 * clic sur « Ajouter ». Le souvenir tient dans le navigateur du lecteur (localStorage, aucune donnée envoyée) ; sans localStorage le
 * bandeau s'affiche simplement à chaque visite. Lien officiel de Google (« Preferred sources ») : les articles de Scénario remontent
 * alors plus souvent dans « À la une ». N'apparaît pas pendant l'installation de l'application, ni sur les pages légales ou de confirmation.
 * Langue : document.documentElement.lang (« fr » ou « en »), comme pwa-install.js.
 */
(function () {
  "use strict";

  var LANG = (document.documentElement.lang || "fr").slice(0, 2) === "en" ? "en" : "fr";
  var STRINGS = {
    fr: { label: "Ajouter Scénario à vos sources Google", text: "Scénario dans vos actualités Google ?", add: "Ajouter", close: "Fermer" },
    en: { label: "Add Scénario to your Google sources", text: "Scénario in your Google news?", add: "Add", close: "Close" },
  };
  var T = STRINGS[LANG];
  var GOOGLE_URL = "https://google.com/preferences/source?q=lesscenarios.fr";
  var STORAGE_KEY = "scenario-google-source-until";
  var CLOSED_DAYS = 21;
  var ADDED_DAYS = 365;
  var SHOW_DELAY_MS = 7000;
  var RETRY_MS = 15000;
  var MAX_RETRIES = 3;
  var SKIP_PAGES = /(confirmez-votre-email|bienvenue|mentions-legales|politique-de-confidentialite|cookies)(\.html)?$/;
  var DAY_MS = 24 * 60 * 60 * 1000;
  var bannerEl = null;

  function hidden() {
    try {
      var until = localStorage.getItem(STORAGE_KEY);
      return !!until && Date.now() < Number(until);
    } catch (e) {
      return false;
    }
  }

  function remember(days) {
    try {
      localStorage.setItem(STORAGE_KEY, String(Date.now() + days * DAY_MS));
    } catch (e) {}
  }

  function isStandalone() {
    return (
      (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) ||
      window.navigator.standalone === true
    );
  }

  function addStyle() {
    var css =
      ".gs-banner{position:fixed;left:12px;right:12px;margin:0 auto;bottom:16px;z-index:8000;display:flex;align-items:center;gap:10px;" +
      "width:max-content;max-width:min(440px,calc(100vw - 24px));box-sizing:border-box;padding:9px 10px 9px 14px;" +
      "background:var(--surface,#1a212b);border:1px solid var(--hairline,#2c3644);border-radius:12px;" +
      "box-shadow:0 8px 28px rgba(0,0,0,.35);color:var(--paper,#e9e6dc);font-size:.84rem;line-height:1.3;" +
      "opacity:0;transform:translateY(10px);transition:opacity .3s ease,transform .3s ease}" +
      ".gs-banner.is-visible{opacity:1;transform:translateY(0)}" +
      "html.has-bottom-nav .gs-banner{bottom:calc(84px + env(safe-area-inset-bottom,0px))}" +
      ".gs-banner svg{flex:none;width:15px;height:15px;color:var(--gold,#c9a24a)}" +
      ".gs-banner .gs-text{flex:1;min-width:0}" +
      ".gs-banner .gs-add{flex:none;padding:5px 12px;border:1px solid var(--gold,#c9a24a);border-radius:100px;" +
      "color:var(--gold,#c9a24a);text-decoration:none;font-size:.78rem;white-space:nowrap}" +
      ".gs-banner .gs-add:hover{background:var(--gold,#c9a24a);color:var(--ink,#0f141a)}" +
      ".gs-banner .gs-close{flex:none;width:26px;height:26px;border:0;border-radius:50%;background:none;" +
      "color:var(--paper-dim,#b4b2a6);font-size:1.1rem;line-height:1;cursor:pointer}" +
      ".gs-banner .gs-close:hover{color:var(--paper,#e9e6dc)}" +
      "@media (prefers-reduced-motion:reduce){.gs-banner{transition:none}}" +
      "@media print{.gs-banner{display:none!important}}";
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);
  }

  function hide() {
    if (!bannerEl) return;
    var el = bannerEl;
    bannerEl = null;
    el.classList.remove("is-visible");
    setTimeout(function () {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 350);
  }

  function show() {
    addStyle();
    var el = document.createElement("aside");
    el.className = "gs-banner";
    el.setAttribute("aria-label", T.label);
    el.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" ' +
      'stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5l2.5 5.4 5.9.7-4.4 4 1.2 5.8L12 16.5l-5.2 2.9 1.2-5.8-4.4-4 5.9-.7z"/></svg>' +
      '<span class="gs-text"></span>' +
      '<a class="gs-add" target="_blank" rel="noopener noreferrer"></a>' +
      '<button type="button" class="gs-close"></button>';
    el.querySelector(".gs-text").textContent = T.text;
    var add = el.querySelector(".gs-add");
    add.textContent = T.add;
    add.href = GOOGLE_URL;
    add.setAttribute("aria-label", T.label);
    var close = el.querySelector(".gs-close");
    close.textContent = "×";
    close.setAttribute("aria-label", T.close);
    add.addEventListener("click", function () {
      remember(ADDED_DAYS);
      hide();
    });
    close.addEventListener("click", function () {
      remember(CLOSED_DAYS);
      hide();
    });
    document.addEventListener("keydown", function onKey(e) {
      if (e.key === "Escape" && bannerEl) {
        remember(CLOSED_DAYS);
        hide();
        document.removeEventListener("keydown", onKey);
      }
    });
    document.body.appendChild(el);
    bannerEl = el;
    setTimeout(function () {
      el.classList.add("is-visible");
    }, 60);
  }

  function tryShow(attempt) {
    // Une seule invitation à la fois : si le bandeau d'installation de l'application est affiché, on réessaie plus tard.
    if (document.querySelector(".pwa-install-banner.is-visible")) {
      if (attempt < MAX_RETRIES) setTimeout(function () { tryShow(attempt + 1); }, RETRY_MS);
      return;
    }
    show();
  }

  function init() {
    if (SKIP_PAGES.test(window.location.pathname) || isStandalone() || hidden()) return;
    setTimeout(function () { tryShow(0); }, SHOW_DELAY_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
