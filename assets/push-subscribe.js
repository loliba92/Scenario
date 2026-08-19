/*
 * Démo — abonnement aux notifications push (Web Push standard, aucun
 * service tiers). Clé PUBLIQUE VAPID uniquement ici, c'est son rôle
 * (la clé privée ne sert qu'à l'envoi, jamais côté client/repo).
 * Étape de test manuelle : affiche l'abonnement généré dans un champ
 * copiable, à envoyer pour recevoir une notification de test tant
 * qu'aucun backend d'envoi automatique n'est en place.
 */
(function () {
  "use strict";

  var VAPID_PUBLIC_KEY =
    "BDj8lj4KyXLvjpfSdNKjijGrLB5Hr013hc9H4k9DBgE7mkrmjrPmc3R09WmOFJ7vuGaLeHKPstpFFFR9OSEx3Ak";

  function urlBase64ToUint8Array(base64String) {
    var padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    var base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
    var rawData = window.atob(base64);
    var outputArray = new Uint8Array(rawData.length);
    for (var i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  if (!("serviceWorker" in navigator) || !("PushManager" in window)) return;

  var btn = document.getElementById("push-subscribe-btn");
  var output = document.getElementById("push-subscribe-output");
  if (!btn) return;

  if (Notification.permission === "granted") {
    btn.textContent = "Notifications déjà activées";
    btn.disabled = true;
  }

  btn.addEventListener("click", function () {
    btn.disabled = true;
    btn.textContent = "Activation…";

    navigator.serviceWorker.ready
      .then(function (registration) {
        return registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
        });
      })
      .then(function (subscription) {
        btn.textContent = "Notifications activées ✓";
        if (output) {
          output.style.display = "block";
          output.value = JSON.stringify(subscription);
          output.focus();
          output.select();
        }
      })
      .catch(function (err) {
        btn.disabled = false;
        btn.textContent = "Activer les notifications";
        if (output) {
          output.style.display = "block";
          output.value = "Erreur : " + (err && err.message ? err.message : String(err));
        }
      });
  });
})();
