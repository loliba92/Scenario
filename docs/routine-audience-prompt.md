# Prompt de la routine « Scénario — Audience »

Ce fichier est la copie de référence du prompt envoyé par la routine "audience"
(Claude Code Remote, trigger **« Scénario — Audience »**, cron **hebdomadaire**).
Créée le 21 août à la demande de l'utilisateur, pour maintenir à jour le
graphique de croissance de l'audience sur `le-projet.html` (section
`#audience`, composant `.dc-chart-box` réutilisé en variante "favorable").

**Objectif** : montrer que l'audience grandit, avec de vrais chiffres —
cohérent avec l'identité du site ("on chiffre plutôt qu'on affirme"). Voir
`docs/ARCHITECTURE.md`, section "Mesure d'audience", pour l'historique complet
de la décision (pourquoi Search Console a été écarté, pourquoi le calcul se
limite aux éditions et pas au trafic total du site).

**Le token API GoatCounter (lecture seule) n'est jamais dans ce fichier ni
ailleurs dans le dépôt** — le dépôt est public (servi tel quel par GitHub
Pages), un secret commité y resterait visible pour toujours dans l'historique
git. Le token est fourni uniquement dans le prompt du trigger lui-même
(configuration privée côté Claude Code Remote, `job_config`, jamais
synchronisée vers GitHub). **Si le token doit être régénéré** (rotation,
fuite suspectée) : mettre à jour uniquement le trigger via `update_trigger`,
jamais un fichier de ce dépôt.

**La cible du push est toujours `main`, sans exception** — même règle que les
autres routines Scénario, même si l'environnement d'exécution assigne une
autre branche de session par défaut.

## Étape 1 — Récupérer les données

Appeler l'API GoatCounter, `GET https://scenario.goatcounter.com/api/v0/stats/hits`,
avec :
- `start=2026-07-29` — date du tout premier hit enregistré sur le site
  (constante connue, jamais à redécouvrir dynamiquement).
- `end` = **demain**, pas aujourd'hui — vérifié empiriquement le 21 août :
  `end` égal à la date du jour omettait les hits du jour lui-même dans la
  réponse ; `end` = date du jour + 2 jours les incluait de façon fiable.
  Utiliser `end` = date du jour (Paris) + 2 jours pour rester marge.
- `limit=200` — largement suffisant, le site a moins de 100 chemins trackés
  au 21 août.

En-tête `Authorization: Bearer {token}` (fourni dans le prompt du trigger,
voir ci-dessus) et `Content-Type: application/json`.

## Étape 2 — Agréger

Parmi les chemins retournés (`hits[].path`), **ne garder que ceux qui
correspondent à `^/archives/(\d{4}-\d{2}-\d{2})\.html(\?.*)?$`** — regrouper
les variantes avec query string (ex. `?trk=feed_main-feed-card_...`, ajoutée
par certains liens entrants) avec le chemin propre du même article, jamais
les compter comme un article à part. Ignorer tous les autres chemins (page
d'accueil `/` et `/index.html`, `archives.html`, `le-projet.html`, `contact.html`,
`newsletter.html`, `suivi/*`, `hebdo/*`...) — **seules les éditions
quotidiennes comptent pour ce graphique**, même périmètre que le compteur de
lecture par article (voir `docs/ARCHITECTURE.md`).

Pour chaque chemin retenu, sommer par jour calendaire (`stats[].day` /
`stats[].daily` dans la réponse) — additionner tous les articles ensemble
pour obtenir un total de lectures d'éditions par jour, tous articles
confondus, pas un total par article. Construire ensuite le **cumul** : somme
courante jour après jour, du plus ancien au plus récent, en incluant les
jours à 0 (ex. le tout premier jour du site) pour que la courbe démarre
proprement à zéro.

## Étape 3 — Mettre à jour `le-projet.html`

Dans le `<script>` situé juste après le script de suivi GoatCounter
(`data-goatcounter=...`) et juste avant `assets/pwa-install.js` :

- Remplacer le tableau `data` (paires `[date ISO, cumul]`) par la nouvelle
  série complète.
- Remplacer `xLabels` par une sélection de ~5 dates réparties sur toute la
  période — toujours la première et la dernière date de la série, 3
  intermédiaires à peu près régulièrement espacées. Ne jamais afficher tous
  les jours sur l'axe X, ça surcharge (même règle que le graphique de
  l'Horloge de l'Apocalypse, voir `docs/routine-prompt.md`).
- `yMax` : palier rond immédiatement au-dessus du dernier cumul (ex. 200 pour
  un cumul de 181, 250 pour un cumul de 210...).

Mettre à jour aussi le texte autour du graphique, dans la section
`#audience` :
- Le chiffre en gras du paragraphe d'intro : "**{N} lectures d'éditions
  cumulées** depuis le lancement, au {date la plus récente}".
- `.dc-chart-lead` : "Nombre total de lectures d'éditions depuis le
  lancement, du {date début} au {date fin}."
- Le `aria-label` du `<svg id="audience-svg">` : reprendre le point de départ
  et le point d'arrivée exacts de la série.
- Le label du dernier point sur le graphique (`{N} au {date}`, jamais
  "aujourd'hui" — ce chiffre n'est mis à jour qu'une fois par semaine, pas en
  direct, donc jamais présenté comme temps réel).

**Ne jamais changer le CSS, la structure HTML de la section, ni son
emplacement sur la page** (juste avant `#nous-suivre`) — seules les données
et le texte qui en dépend changent d'une exécution à l'autre.

## Étape 4 — Vérification et publication

Vérifier la syntaxe du `<script>` modifié (`node --check`) avant de committer.
Une vérification visuelle (Playwright, `executablePath:
'/opt/pw-browsers/chromium'`, capture de la section `#audience`) est
recommandée à chaque passage — le composant ne change pas de structure d'une
semaine à l'autre, mais une régression silencieuse (chevauchement de labels
sur une série qui s'accélère, par exemple) resterait invisible sans capture.

`git add le-projet.html`, commit avec un message clair (`[audience] mise à
jour du {date} — {N} lectures cumulées`), `git push origin main` directement
— jamais sur une autre branche.

## Étape 5 — Résumé final

Toujours terminer par : le nouveau total cumulé, la date de la donnée la plus
récente, et le delta depuis la dernière mise à jour connue (comparer au
dernier total committé si visible dans l'historique git, sinon simplement
donner le nouveau total).
