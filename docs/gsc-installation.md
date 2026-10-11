# Connecter Google Search Console au dépôt (une seule fois)

**But** : recevoir chaque jour, automatiquement, les chiffres réels de Google (visites depuis Google, requêtes, pages, indexation) dans `data/gsc/`, lisibles ensuite par Claude à chaque session. **Coût : gratuit** (API Google et GitHub Actions dans leurs quotas).

Principe : on crée un « compte de service », une sorte de robot avec sa propre adresse e-mail, qu'on invite dans Search Console comme un utilisateur de plus. Le workflow `gsc.yml` s'en sert pour lire les données.

Durée : environ 10 minutes. Quatre étapes, à faire sur ordinateur.

## Étape 1 — Créer le compte de service (Google Cloud)

1. Ouvrez https://console.cloud.google.com avec le compte Google qui possède le site dans Search Console.
2. En haut, **Sélectionner un projet → Nouveau projet**. Nom : `scenario-seo`. Créez-le, puis sélectionnez-le.
3. Menu **API et services → Bibliothèque**. Cherchez **« Google Search Console API »**, ouvrez-la, cliquez **Activer**.
4. Menu **IAM et administration → Comptes de service → Créer un compte de service**. Nom : `scenario-gsc`. Cliquez **Créer et continuer**, ne donnez **aucun rôle**, puis **OK**.
5. Cliquez sur le compte créé, onglet **Clés → Ajouter une clé → Créer une clé → JSON → Créer**. Un fichier `.json` se télécharge : **c'est un mot de passe, ne le partagez à personne**.
6. Notez l'adresse du compte, de la forme `scenario-gsc@scenario-seo.iam.gserviceaccount.com`.

> Si le bouton de création de clé est grisé, une règle d'organisation Google la bloque ; dites-le-moi, il existe une autre voie.

## Étape 2 — Inviter le compte de service dans Search Console

1. Ouvrez https://search.google.com/search-console, choisissez la propriété `lesscenarios.fr`.
2. **Paramètres → Utilisateurs et autorisations → Ajouter un utilisateur**.
3. Collez l'adresse du compte de service. Autorisation : **Complète** (nécessaire pour envoyer les plans du site ; « Limitée » suffit si vous ne voulez que la lecture).

## Étape 3 — Donner la clé à GitHub

1. Sur GitHub, dépôt `loliba92/Scenario` → **Settings → Secrets and variables → Actions**.
2. Onglet **Secrets → New repository secret**. Nom : `GSC_SERVICE_ACCOUNT_JSON`. Valeur : ouvrez le fichier `.json` avec un éditeur de texte, **copiez tout son contenu**, collez-le. Enregistrez.
3. Seulement si votre propriété Search Console est de type **« préfixe d'URL »** (et non « domaine ») : onglet **Variables → New repository variable**, nom `GSC_SITE`, valeur `https://lesscenarios.fr/`. Sinon, ne faites rien (défaut : `sc-domain:lesscenarios.fr`).
4. Supprimez ensuite le fichier `.json` de votre ordinateur.

## Étape 4 — Tester

1. Dépôt → onglet **Actions → Sync Search Console → Run workflow**.
2. Attendez la fin (1 à 2 minutes). Coche verte : un commit `[gsc] mise à jour automatique…` apparaît avec les fichiers de `data/gsc/`. Croix rouge : ouvrez l'exécution, le message d'erreur dit quoi corriger (le plus souvent l'étape 2 ou le type de propriété).
3. Dites-moi « c'est fait » : je lis les journaux du workflow et les fichiers, et je corrige le script au besoin.

## Ce que contient `data/gsc/`

| Fichier | Contenu |
|---|---|
| `summary.json` | 28 derniers jours : clics, impressions, CTR, position moyenne, meilleures requêtes et pages |
| `history.json` | un point par jour, cumulé dans le temps |
| `indexation.json` | état d'indexation Google des pages clés et des 20 dernières éditions |
| `sitemaps.json` | état des plans du site (dernière lecture par Google, erreurs, avertissements) |

Le workflow renvoie aussi `sitemap.xml` et `sitemap-news.xml` à Google chaque jour : cela accélère la relecture des pages modifiées.

## Bon à savoir
- Les chiffres de Google ont **environ 3 jours de retard**.
- **Confidentialité** : les fichiers de `data/gsc/` sont enregistrés dans le dépôt. Si le dépôt est public, ces statistiques (requêtes, pages) le sont aussi ; elles ne contiennent aucune donnée personnelle. Si vous ne le souhaitez pas, dites-le-moi : on les enregistrera ailleurs.
- Un site récent ou peu visité aura peu de requêtes : les fichiers seront alors courts, c'est normal.
- Pour arrêter : supprimez le secret `GSC_SERVICE_ACCOUNT_JSON` (le workflow s'arrête sans erreur) ou désactivez le workflow dans l'onglet Actions. Pour révoquer l'accès : retirez l'utilisateur dans Search Console.
- Le script n'utilise que la bibliothèque standard de Python et la commande `openssl` : aucune installation, aucune dépendance à surveiller.
