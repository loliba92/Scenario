"""Contrôle de fidélité de la voix : ce qui est lu doit être EXACTEMENT le texte fourni.

Incident du 10 octobre 2026 : le moteur vocal (Gemini) n'a pas lu le texte du dépôt. Pour le deuxième et le troisième
scénario il a inventé d'autres phrases (« la valeur se crée dans la transaction NFT » : aucun NFT dans l'édition),
puis les a répétées deux fois. L'audio faisait 1 855 mots au lieu de 1 226 (11 min 25 au lieu d'environ 8). Le seul
contrôle existant ne vérifiait que les 12 premières secondes.

Désormais chaque partie lue est transcrite (Gemini, comme le contrôle du début) puis comparée mot à mot au texte :
- similarité (difflib) d'au moins SIMILARITE_MIN : une transcription correcte donne environ 0,95, un passage inventé
  ou répété moins de 0,3 (mesuré sur l'épisode fautif) ;
- nombre de mots entendus compris entre RAPPORT_MIN et RAPPORT_MAX fois le nombre attendu.
Une partie infidèle est relue (jusqu'à ESSAIS fois) ; si aucune lecture n'est fidèle, l'épisode n'est pas publié.
Un contrôle impossible (service de transcription indisponible) n'empêche pas l'épisode mais est signalé.
"""
from __future__ import annotations

import base64
import difflib
import json
import re
import subprocess
import unicodedata
import urllib.request

SIMILARITE_MIN = 0.85
RAPPORT_MIN, RAPPORT_MAX = 0.85, 1.15
ESSAIS = 3
SAMPLE_RATE = 24000


def mots(texte: str) -> list[str]:
    sans = "".join(c for c in unicodedata.normalize("NFD", texte.lower()) if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", sans)


def comparer(attendu: str, entendu: str) -> dict:
    a, e = mots(attendu), mots(entendu)
    if not a:
        return {"similarite": 1.0 if not e else 0.0, "rapport": 1.0 if not e else float("inf"), "attendus": 0, "entendus": len(e)}
    sim = difflib.SequenceMatcher(None, a, e, autojunk=False).ratio()
    return {"similarite": sim, "rapport": len(e) / len(a), "attendus": len(a), "entendus": len(e)}


def conforme(resultat: dict) -> bool:
    return resultat["similarite"] >= SIMILARITE_MIN and RAPPORT_MIN <= resultat["rapport"] <= RAPPORT_MAX


def _wav_16k(pcm: bytes) -> bytes:
    """PCM 24 kHz -> WAV 16 kHz mono (plus léger à envoyer)."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "s16le", "-ar", str(SAMPLE_RATE), "-ac", "1", "-i", "-",
                        "-ar", "16000", "-ac", "1", "-f", "wav", "-"], input=pcm, capture_output=True, check=True)
    return r.stdout


def transcrire(pcm: bytes, cle: str) -> tuple[str | None, str]:
    """(transcription, détail) ; (None, erreur) si la transcription a échoué."""
    import generate_podcast as gp
    corps = json.dumps({"contents": [{"parts": [
        {"text": "Transcris mot à mot, en français, tout ce qui est dit dans cet audio, sans rien corriger, résumer ni ajouter, "
                 "et sans rien omettre, même si des passages se répètent. Réponds uniquement par la transcription."},
        {"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(_wav_16k(pcm)).decode()}}]}],
        "generationConfig": {"temperature": 0}}).encode()
    erreurs = []
    try:
        candidats = gp._modeles_transcription(cle)[:3]
    except Exception as e:  # noqa: BLE001
        return None, f"liste des modèles : {type(e).__name__}: {e}"
    for modele in candidats:
        req = urllib.request.Request(gp.GEMINI_URL.format(model=modele), data=corps, method="POST",
                                     headers={"Content-Type": "application/json", "x-goog-api-key": cle})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                rep = json.loads(r.read())
            return rep["candidates"][0]["content"]["parts"][0]["text"].strip(), modele
        except Exception as e:  # noqa: BLE001
            erreurs.append(f"{modele} : {type(e).__name__}: {e}")
    return None, " ; ".join(erreurs) or "aucun modèle de transcription disponible"


def controler(pcm: bytes, texte: str, cle: str, transcrire_fn=None) -> tuple[bool | None, dict, str]:
    """(conforme | None si contrôle impossible, mesures, détail)."""
    transcription, detail = (transcrire_fn or transcrire)(pcm, cle)
    if transcription is None:
        return None, {}, detail
    mesures = comparer(texte, transcription)
    return conforme(mesures), mesures, transcription
