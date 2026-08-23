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

**Le champ `received` de l'API OneSignal n'est pas fiable pour ce site,
confirmé le 23 août — ne pas s'en servir comme signal d'échec.** L'envoi
du matin (`9236068f...`) affichait `successful: 3, received: 0` ; sur la
base de ce seul chiffre, un test manuel de renvoi a été déclenché pour
diagnostiquer une éventuelle panne d'affichage côté navigateur. Résultat :
l'utilisateur a bien reçu ce second envoi (confirmé en direct), alors que
`received` est resté à 0 pour les deux notifications même après cette
confirmation. Le SDK web ne remonte donc pas cet évènement pour cette
app (pas de callback `on_notification_received` configuré, ou non
supporté pour le web push dans ce plan OneSignal) — `successful`/`failed`
restent les seuls champs à surveiller, `received` est à ignorer.

**Format d'une ligne** : `{AAAA-MM-JJ} — {✅/⚠️/❌} {résultat}`
- ✅ : notification créée côté OneSignal (id renvoyé par l'API).
- ⚠️ : clé API absente dans l'environnement de la routine ce jour-là — étape
  sautée volontairement (voir `docs/routine-prompt.md`, étape 11bis :
  jamais bloquant pour la publication).
- ❌ : la requête a été tentée mais a échoué (réseau, clé invalide, erreur
  OneSignal) — voir le message d'erreur en fin de ligne.

La plus récente en tête.

---
2026-08-23 — ✅ [test manuel diagnostic] notification créée (id `d2b99e61-39b8-4db2-b9bd-dccfd6daa144`) — bien reçue par l'utilisateur (confirmé en direct), malgré `received: 0` côté API (voir note ci-dessus, champ non fiable ici)
2026-08-23 — ✅ notification créée (id `9236068f-d7ea-4868-91e7-0e0fe887ae2d`)
2026-08-22 — ✅ test manuel post-fix, notification créée (id `14681449-6080-4304-bbc5-bbfc73f25690`) — confirme que `included_segments: ['Active Subscriptions']` fonctionne, cause racine réglée
2026-08-22 — ❌ requête acceptée par l'API (HTTP 200) mais aucune notification créée : réponse `{'id': '', 'errors': ['All included players are not subscribed']}` — aucun abonné OneSignal actif à ce jour, id vide
2026-08-21 — ❌ requête acceptée par l'API (HTTP 200) mais aucune notification créée : réponse `{'id': '', 'errors': ['All included players are not subscribed']}` — aucun abonné OneSignal actif à ce jour, id vide
