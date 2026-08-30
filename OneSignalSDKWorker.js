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
 * même scope.
 *
 * Nom de fichier imposé par OneSignal (OneSignalSDKWorker.js, pas
 * sw.js) : `serviceWorkerPath` dans OneSignal.init() ne suffisait pas
 * à lui seul à faire pointer leur SDK ailleurs — repéré le 19 août via
 * une erreur 404 sur OneSignalSDKWorker.js malgré la config custom,
 * probablement figé côté dashboard par l'assistant "Typical site".
 * Plus simple d'aligner le nom de fichier que de creuser plus loin.
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

/* ---------- Notifications push ----------
 * [CORRIGÉ le 30 août 2026, retour utilisateur : "je reçois bien la
 * notification avec le titre mais j'en reçois 1 autre vide".] Ce
 * fichier a longtemps défini son propre gestionnaire `push` en plus de
 * l'`importScripts` OneSignal ci-dessus — hors `addEventListener`
 * s'empile, il ne remplace jamais un listener existant : les DEUX
 * gestionnaires tournaient à chaque notification. Celui d'OneSignal
 * (dans OneSignalSDK.sw.js) décode correctement leur charge utile
 * propriétaire et affiche la vraie notification (titre + texte). Le
 * nôtre, plus bas, tentait de reparser la même charge utile en JSON
 * simple `{title, body, url}` — un format qui ne correspond pas à
 * celui d'OneSignal — retombait donc sur ses valeurs par défaut
 * ("Scénario", corps vide) et affichait une seconde notification,
 * creuse, à chaque envoi. Supprimé : OneSignal gère déjà `push` et
 * `notificationclick` (ouverture/focus de l'URL de la notif) tout
 * seul via l'`importScripts` plus haut, rien à dupliquer ici. */
