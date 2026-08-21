# Journal des notifications push (OneSignal)

Une ligne par tentative d'envoi de la notification push quotidienne (étape
11bis de `docs/routine-prompt.md`), succès ou échec. Sert à vérifier après
coup si l'envoi est bien parti **sans avoir à interroger l'API OneSignal
directement** — ce qu'il a fallu faire le 21 août pour comprendre qu'aucune
notification n'était visible côté OneSignal pour l'édition du jour (la
cause s'est révélée être les notifications désactivées côté utilisateur,
pas un bug de la routine — mais rien dans le dépôt ne permettait de le
vérifier sans requêter l'API directement, d'où ce journal).

**Format d'une ligne** : `{AAAA-MM-JJ} — {✅/⚠️/❌} {résultat}`
- ✅ : notification créée côté OneSignal (id renvoyé par l'API).
- ⚠️ : clé API absente dans l'environnement de la routine ce jour-là — étape
  sautée volontairement (voir `docs/routine-prompt.md`, étape 11bis :
  jamais bloquant pour la publication).
- ❌ : la requête a été tentée mais a échoué (réseau, clé invalide, erreur
  OneSignal) — voir le message d'erreur en fin de ligne.

La plus récente en tête.

---
2026-08-21 — ❌ requête acceptée par l'API (HTTP 200) mais aucune notification créée : réponse `{'id': '', 'errors': ['All included players are not subscribed']}` — aucun abonné OneSignal actif à ce jour, id vide
