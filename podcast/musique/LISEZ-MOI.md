# Thème musical du podcast

Le fichier `ouverture.mp3` (ou `.wav`, `.m4a`) est la musique de tous les épisodes. Actuellement : « Nocturnal Introspection »
(61 s), déposé le 4 octobre 2026. La musique ne s'arrête jamais :

- **Ouverture** : le morceau joue seul (fondu depuis le silence), la voix entre après 10 s pendant que la musique
  redescend.
- **Fond** : sous la voix, la musique reste très légère (7 % du niveau de la voix), à peine perceptible. Le morceau défile
  en continu et se répète sans coupure.
- **Jingles** entre les grandes parties : la musique monte en fondu (9 s), puis redescend sous le début de la partie suivante.
  Chaque jingle tombe sur un passage différent du morceau.
- **Fermeture** : après la phrase finale, la musique monte puis s'éteint en fondu jusqu'à zéro.

Réglages : `NIVEAU_FOND`, `NIVEAU_JINGLE`, `JINGLE_S` dans `scripts/podcast/musique.py`. Sans ce fichier, les épisodes sont sans musique.

Le fichier doit être libre de droits pour cet usage (musique créée par vous, par exemple avec Suno : vérifier que
l'abonnement autorise l'usage commercial).
