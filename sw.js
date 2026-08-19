/*
 * Service worker minimal — sert uniquement à rendre le site installable
 * (critère PWA) et à donner un filet de secours hors-ligne.
 * Stratégie "réseau d'abord" : tant que la connexion fonctionne, tout
 * vient du réseau comme d'habitude (le site est mis à jour plusieurs
 * fois par jour, jamais question de servir une version en cache par
 * défaut). Le cache ne sert que si le réseau échoue.
 *
 * Fusionné avec le service worker de OneSignal (notifications push) —
 * importScripts en premier, comme demandé par leur doc : partage ce
 * fichier plutôt que d'avoir deux service workers qui se disputent le
 * même scope. Voir OneSignal.init({ serviceWorkerPath: "sw.js" }) côté
 * page.
 */
importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");

const CACHE_NAME = "scenario-shell-v1";
const SHELL_ASSETS = [
  "/",
  "/index.html",
  "/assets/logo.svg",
  "/assets/icon-192.png",
  "/assets/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(SHELL_ASSETS))
      .catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy)).catch(() => {});
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});

/* ---------- Notifications push ---------- */

self.addEventListener("push", (event) => {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (e) {
    data = { title: "Scénario", body: event.data ? event.data.text() : "" };
  }

  const title = data.title || "Scénario";
  const options = {
    body: data.body || "",
    icon: "/assets/icon-192.png",
    badge: "/assets/icon-192.png",
    data: { url: data.url || "/" },
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || "/";
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((windowClients) => {
      for (const client of windowClients) {
        if (client.url === url && "focus" in client) return client.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow(url);
    })
  );
});
