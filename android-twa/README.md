# Scénario sur le Play Store (TWA)

Wrapper Android minimal autour de `lesscenarios.fr` via Trusted Web
Activity (TWA) — l'app ouvre le site dans un onglet plein écran, sans
UI de navigateur. Le contenu vient toujours du site en direct : pas de
republication nécessaire à chaque édition quotidienne.

`twa-manifest.json` est déjà rempli (nom, couleurs, icône, URL du
manifest). Il ne reste que les étapes qui demandent un compte/une
identité — personne d'autre que toi ne peut les faire.

## Ce qu'il te reste à faire

1. **Créer un compte Google Play Developer** — https://play.google.com/console/signup,
   25 $ US de frais unique, avec ton propre compte Google.
2. **Générer la clé de signature + le build** (`.aab`) — je peux le faire
   ici si tu me dis go, mais lis d'abord le point 3.
3. **Récupérer et sécuriser le keystore** généré à l'étape 2 — c'est la
   clé maîtresse de l'app : si tu la perds, tu ne pourras plus jamais
   publier de mise à jour sous la même app. Il faut la télécharger et la
   garder en lieu sûr (gestionnaire de mots de passe, coffre-fort
   numérique) — jamais dans ce dépôt Git, qui est public.
4. **Ajouter `.well-known/assetlinks.json` sur le site** (`lesscenarios.fr`)
   — fichier public qui prouve à Android que l'app et le site
   t'appartiennent tous les deux. Je m'en charge une fois la clé
   générée (il a besoin de l'empreinte SHA-256 du certificat).
5. **Créer la fiche du Store** : captures d'écran, description courte/longue,
   catégorie, lien vers la politique de confidentialité (on a déjà
   `politique-de-confidentialite.html`, réutilisable tel quel).
6. **Uploader le `.aab` sur la Play Console et soumettre pour revue.**

## Commandes (une fois le compte créé)

```bash
cd android-twa
npx @bubblewrap/cli build
```

Génère le `.aab` signé à partir de `twa-manifest.json`. Nécessite le JDK
et l'Android SDK (Bubblewrap propose de les installer automatiquement
à la première exécution).
