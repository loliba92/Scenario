/*
 * Bandeau "Installer l'application" — partagé par toutes les pages.
 * Chrome/Android/Edge : capte beforeinstallprompt et affiche un bouton
 * "Installer" personnalisé. iOS Safari : n'a pas d'API d'installation
 * programmatique, on affiche juste l'astuce "Partager → Sur l'écran
 * d'accueil". Ne s'affiche jamais si déjà installé, et se souvient
 * d'un refus pendant DISMISS_DAYS jours (localStorage).
 *
 * Bilingue depuis le 29 août (retour utilisateur : "le popup en
 * français, possible de mettre en anglais aussi ?") — un seul script
 * partagé par les pages FR et EN, la langue du texte suit
 * `document.documentElement.lang` (déjà correct sur chaque page,
 * "fr"/"en") plutôt qu'un second fichier dupliqué à maintenir.
 */
(function () {
  "use strict";

  var LANG = (document.documentElement.lang || "fr").slice(0, 2) === "en" ? "en" : "fr";
  var STRINGS = {
    fr: {
      dialogLabel: "Installer l'application Scénario",
      title: "Installer Scénario",
      iosText: 'Appuyez sur <strong>Partager</strong> puis <strong>Sur l’écran d’accueil</strong>.',
      text: "Accédez à l’édition du jour en un geste, depuis votre écran d’accueil.",
      install: "Installer",
      dismiss: "Fermer",
    },
    en: {
      dialogLabel: "Install the Scénario app",
      title: "Install Scénario",
      iosText: 'Tap <strong>Share</strong> then <strong>Add to Home Screen</strong>.',
      text: "Get to the day's edition in one tap, from your home screen.",
      install: "Install",
      dismiss: "Close",
    },
  };
  var T = STRINGS[LANG];

  var THIS_SCRIPT = document.currentScript;
  var SCRIPT_SRC = THIS_SCRIPT ? THIS_SCRIPT.getAttribute("src") || "" : "";
  var BASE_PREFIX = SCRIPT_SRC.replace(/assets\/pwa-install\.js.*$/, "");

  // Clé versionnée (v2) : invalide les anciens flags posés par le bug
  // où une installation était aussi enregistrée comme un refus de 14
  // jours (voir appinstalled plus bas) — sans ça, quiconque a déjà
  // installé puis désinstallé resterait bloqué jusqu'à expiration.
  var STORAGE_KEY = "scenario-install-dismissed-until-v2";
  var DISMISS_DAYS = 14;
  var SHOW_DELAY_MS = 4000;

  function isStandalone() {
    return (
      (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) ||
      window.navigator.standalone === true
    );
  }

  function isDismissed() {
    try {
      var until = localStorage.getItem(STORAGE_KEY);
      return !!until && Date.now() < Number(until);
    } catch (e) {
      return false;
    }
  }

  function rememberDismissal() {
    try {
      localStorage.setItem(STORAGE_KEY, String(Date.now() + DISMISS_DAYS * 24 * 60 * 60 * 1000));
    } catch (e) {}
  }

  function isIos() {
    var ua = window.navigator.userAgent;
    if (/iphone|ipad|ipod/i.test(ua) && !window.MSStream) return true;
    // iPadOS masque son user agent en "Macintosh" par défaut depuis la
    // version 13 (option système "Demander la version pour ordinateur",
    // activée d'office sur iPad, suivie aussi par Chrome/Firefox iOS) :
    // la regex ci-dessus ne matche alors plus rien. Repli recommandé par
    // Apple — un "Mac" tactile n'existe pas, donc un Mac qui répond au
    // toucher est forcément un iPad.
    return (
      /macintosh/i.test(ua) &&
      "ontouchend" in document &&
      navigator.maxTouchPoints > 1
    );
  }

  var deferredPrompt = null;
  var bannerEl = null;

  function buildBanner(kind) {
    var el = document.createElement("div");
    el.className = "pwa-install-banner";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", T.dialogLabel);

    var body = document.createElement("div");
    body.className = "pwa-install-body";

    var title = document.createElement("p");
    title.className = "pwa-install-title";
    title.textContent = T.title;
    body.appendChild(title);

    var text = document.createElement("p");
    text.className = "pwa-install-text";
    if (kind === "ios") {
      text.innerHTML = T.iosText;
    } else {
      text.textContent = T.text;
    }
    body.appendChild(text);

    var icon = document.createElement("img");
    icon.className = "pwa-install-icon";
    icon.src = BASE_PREFIX + "assets/icon-192.png";
    icon.alt = "";
    icon.width = 40;
    icon.height = 40;

    var actions = document.createElement("div");
    actions.className = "pwa-install-actions";

    if (kind !== "ios") {
      var installBtn = document.createElement("button");
      installBtn.type = "button";
      installBtn.className = "pwa-install-btn";
      installBtn.textContent = T.install;
      installBtn.addEventListener("click", function () {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        deferredPrompt.userChoice
          .catch(function () {})
          .then(function () {
            deferredPrompt = null;
            hideBanner();
          });
      });
      actions.appendChild(installBtn);
    }

    var dismissBtn = document.createElement("button");
    dismissBtn.type = "button";
    dismissBtn.className = "pwa-install-dismiss";
    dismissBtn.setAttribute("aria-label", T.dismiss);
    dismissBtn.innerHTML = "&times;";
    dismissBtn.addEventListener("click", function () {
      rememberDismissal();
      hideBanner();
    });
    actions.appendChild(dismissBtn);

    el.appendChild(icon);
    el.appendChild(body);
    el.appendChild(actions);
    return el;
  }

  function showBanner(kind) {
    if (bannerEl || isStandalone() || isDismissed()) return;
    bannerEl = buildBanner(kind);
    document.body.appendChild(bannerEl);
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        if (bannerEl) bannerEl.classList.add("is-visible");
      });
    });
  }

  function hideBanner() {
    if (!bannerEl) return;
    var el = bannerEl;
    bannerEl = null;
    el.classList.remove("is-visible");
    setTimeout(function () {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 350);
  }

  function init() {
    if (isStandalone() || isDismissed()) return;

    // [CORRIGÉ le 30 août 2026, retour utilisateur : bandeau jamais vu
    // dans Chrome sur iPad.] Restait limité à Safari (via isIosSafari(),
    // qui excluait explicitement CriOS/FxiOS/EdgiOS) : Chrome/Firefox/
    // Edge sur iOS tombaient alors dans la branche beforeinstallprompt
    // plus bas, un événement que WebKit ne déclenche jamais — ni dans
    // Safari, ni dans aucun autre navigateur iOS, tous obligatoirement
    // bâtis sur WebKit. Résultat : aucun bandeau du tout hors Safari. Le
    // geste "Partager → Sur l'écran d'accueil" est proposé par la
    // feuille de partage système (UIActivityViewController), disponible
    // depuis n'importe quel navigateur iOS, pas seulement Safari — donc
    // montrer ces instructions dès qu'on est sur iOS/iPadOS, quel que
    // soit le navigateur.
    if (isIos()) {
      setTimeout(function () {
        showBanner("ios");
      }, SHOW_DELAY_MS);
      return;
    }

    window.addEventListener("beforeinstallprompt", function (event) {
      event.preventDefault();
      deferredPrompt = event;
      setTimeout(function () {
        showBanner("chromium");
      }, SHOW_DELAY_MS);
    });

    window.addEventListener("appinstalled", function () {
      // Pas de rememberDismissal() ici : isStandalone() suffit déjà à
      // masquer le bandeau tant que l'app est installée. Un dismiss de
      // 14 jours resterait actif après une désinstallation et
      // empêcherait le bandeau de revenir.
      hideBanner();
    });
  }

  init();

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register(BASE_PREFIX + "OneSignalSDKWorker.js", { scope: BASE_PREFIX || "/" }).catch(function () {});
    });
  }
})();
