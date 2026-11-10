# Page « À venir » : rendez-vous, résultats et contrôles qualité

Page `a-venir.html` + frise de l'accueil. Données : `data/a-venir.json`. Génération : `scripts/a_venir/generate_a_venir.py` (page) et `accueil.py` (frise), rejouées chaque matin par `.github/workflows/signaux.yml`.

## Un rendez-vous
`id`, `date` (date limite), `precision`, `domaine`, `question`, `commentaire`, `qui`, `nature`, `officiel`, `calendrier`, `editions`. Le script refuse un rendez-vous incomplet. Résultat facultatif : `resultat` (statut, date, réponse, chiffres, scénario, sources) ; schéma décrit dans le champ `description` du fichier.

## Résultats : rien n'est publié sans contrôle
Personne ne valide à la main. Chaque matin, pour les rendez-vous échus (3 au plus par passage ; ceux pas encore échus une fois par semaine) :
1. `verifier_resultats.py` : un modèle bon marché avec recherche web PROPOSE un constat, avec des citations exactes.
2. `controles.py` (code, sans modèle) VÉRIFIE, et refuse au moindre échec :
   - statut ferme (pas « incertain ») ; réponse courte, au passé, sans conditionnel ;
   - date de la réponse : jamais dans le futur, jamais avant l'édition ; « ne s'est pas produit » jamais avant la date limite ;
   - au moins 2 sources en https, de domaines différents, hors réseaux sociaux, forums et blogs ; chaque citation retrouvée mot pour mot dans la page ; page qui parle du sujet ;
   - chaque chiffre retrouvé dans une source vérifiée ; scénario valide, sinon « ne tranche pas ».
3. Un second modèle, indépendant, confirme le statut ; désaccord sur le statut = refus ; désaccord sur le scénario = « ne tranche pas ».
4. `appliquer_resultats.py` revalide puis écrit ; ne remplace jamais un résultat existant.

Un refus laisse le rendez-vous « réponse en cours de vérification » et le motif est écrit dans `data/a-venir-verification.md`. Les essais sont comptés dans `data/a-venir-journal.json` (10 au plus par rendez-vous échu, un par jour).

## Tests
`python3 -m unittest scripts/a_venir/test_controles.py scripts/a_venir/test_generate_a_venir.py`
