# Journal des notifications push (OneSignal)

Une ligne par tentative d'envoi de la notification push quotidienne (étape
11bis de `docs/routine-prompt.md`), succès ou échec. Sert à vérifier après
coup si l'envoi est bien parti **sans avoir à interroger l'API OneSignal
directement** — ce qu'il a fallu faire le 21 août pour comprendre qu'aucune
notification n'était visible côté OneSignal pour l'édition du jour.

**Cause réelle, identifiée le 22 août (corrigée dans `docs/routine-prompt.md`)** :
le script ciblait `included_segments: ['Subscribed Users']`, un nom de
segment qui n'existe pas dans cette app OneSignal (nomenclature actuelle :
`Active Subscriptions`, etc. — `Subscribed Users` est l'ancien nom de l'API
v1). L'API renvoyait donc un HTTP 200 sans toucher personne
(`errors: ['All included players are not subscribed']`, `id` vide), et le
script loggait à tort un ✅ dès que la requête HTTP réussissait, sans
vérifier ce champ — d'où l'hypothèse initiale erronée d'un abonné
désactivé côté utilisateur, écartée depuis (l'abonnement était et reste
valide, confirmé par un envoi manuel réussi le 22 août).

**Format d'une ligne** : `{AAAA-MM-JJ} — {✅/⚠️/❌} {résultat}`
- ✅ : notification créée côté OneSignal (id renvoyé par l'API).
- ⚠️ : clé API absente dans l'environnement de la routine ce jour-là — étape
  sautée volontairement (voir `docs/routine-prompt.md`, étape 11bis :
  jamais bloquant pour la publication).
- ❌ : la requête a été tentée mais a échoué (réseau, clé invalide, erreur
  OneSignal) — voir le message d'erreur en fin de ligne.

La plus récente en tête.

---
2026-08-22 — ✅ test manuel post-fix, notification créée (id `14681449-6080-4304-bbc5-bbfc73f25690`) — confirme que `included_segments: ['Active Subscriptions']` fonctionne, cause racine réglée
2026-08-22 — ❌ requête acceptée par l'API (HTTP 200) mais aucune notification créée : réponse `{'id': '', 'errors': ['All included players are not subscribed']}` — aucun abonné OneSignal actif à ce jour, id vide
2026-08-21 — ❌ requête acceptée par l'API (HTTP 200) mais aucune notification créée : réponse `{'id': '', 'errors': ['All included players are not subscribed']}` — aucun abonné OneSignal actif à ce jour, id vide
