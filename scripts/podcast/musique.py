"""Habillage musical du podcast : ouverture, fond discret sous les voix, fermeture.

Musique ORIGINALE synthétisée par ce script (aucun morceau tiers, donc aucun droit à vérifier) :
  - motif de trois notes (ré, fa, la) = les trois scénarios, en montant à l'ouverture, en descendant à la fin ;
  - nappe douce (accords de ré mineur et de si bémol majeur, en alternance) en fond ;
  - le fond s'efface sous les voix (environ -27 dB) et remonte pour la fermeture.
Python standard uniquement (pas de numpy). Demandé le 3 octobre 2026 pour « scénariser » le podcast.
"""
from __future__ import annotations

import math
from array import array

SR = 24000
INTRO_S = 6.0
OUTRO_S = 7.0
BOUCLE_S = 16  # la nappe se répète toutes les 16 s (chaque note fait un nombre entier de cycles)

NIVEAU_OUVERTURE = 0.30   # fond seul (ouverture et fermeture), 1,0 = pleine échelle
NIVEAU_SOUS_VOIX = 0.045  # fond sous les voix
RAMPE_S = 1.2

RE, FA, LA, DO, MI, SIB, SOL = 293.6875, 349.25, 440.0, 523.25, 659.25, 233.0625, 392.0
ACCORD_A = (RE / 2, LA / 2, FA, DO, MI)      # ré mineur neuf, étalé
ACCORD_B = (SIB / 2, FA, LA, RE, SOL)        # si bémol majeur sept, couleur plus claire


def _arrondi(f: float) -> float:
    """Fréquence arrondie à un multiple de 1/16 Hz : la boucle de 16 s se raccorde sans clic."""
    return round(f * BOUCLE_S) / BOUCLE_S


def nappe(duree_s: float, niveau: float) -> array:
    """Fond continu (boucle de 16 s répétée), amplitude maximale `niveau`."""
    n_boucle = SR * BOUCLE_S
    boucle = [0.0] * n_boucle
    for accord, phase in ((ACCORD_A, 0.0), (ACCORD_B, math.pi)):
        freqs = [_arrondi(f) for f in accord]
        for i in range(n_boucle):
            t = i / SR
            gain = 0.5 + 0.5 * math.cos(2 * math.pi * t / BOUCLE_S + phase)
            s = 0.0
            for k, f in enumerate(freqs):
                s += math.sin(2 * math.pi * f * t + k) * (0.55 if k == 0 else 0.30)
                s += math.sin(2 * math.pi * (f + 3 / BOUCLE_S) * t) * 0.10  # léger battement
            boucle[i] += s * gain
    crete = max(abs(x) for x in boucle) or 1.0
    unite = array("f", (x / crete * niveau for x in boucle))
    n = int(SR * duree_s)
    out = array("f")
    while len(out) < n:
        out.extend(unite)
    del out[n:]
    return out


def cloche(freq: float, duree_s: float = 2.4) -> list[float]:
    """Note douce de type cloche : sinus et deux harmoniques, attaque courte, décroissance lente."""
    out = []
    for i in range(int(SR * duree_s)):
        t = i / SR
        env = min(1.0, t / 0.012) * math.exp(-t * 2.1)
        out.append(env * (math.sin(2 * math.pi * freq * t) + 0.32 * math.sin(2 * math.pi * 2 * freq * t)
                          + 0.10 * math.sin(2 * math.pi * 3.01 * freq * t)))
    return out


def motif(notes: tuple[float, ...], ecart_s: float, gain: float, longueur_s: float) -> array:
    piste = array("f", [0.0]) * int(SR * longueur_s)
    for k, f in enumerate(notes):
        debut = int(SR * (0.4 + k * ecart_s))
        for i, x in enumerate(cloche(f)):
            if debut + i < len(piste):
                piste[debut + i] += x * gain
    return piste


def enveloppe_fond(total_s: float) -> list[tuple[float, float]]:
    """Points (instant, niveau) du fond : fort à l'ouverture, discret sous les voix, fort à la fermeture."""
    return [(0.0, NIVEAU_OUVERTURE), (INTRO_S - 1.5, NIVEAU_OUVERTURE),
            (INTRO_S - 1.5 + RAMPE_S, NIVEAU_SOUS_VOIX),
            (total_s - OUTRO_S - RAMPE_S, NIVEAU_SOUS_VOIX), (total_s - OUTRO_S, NIVEAU_OUVERTURE),
            (total_s - 2.5, NIVEAU_OUVERTURE), (total_s, 0.0)]


def _gain(points: list[tuple[float, float]], t: float) -> float:
    for (t0, g0), (t1, g1) in zip(points, points[1:]):
        if t0 <= t <= t1:
            return g0 + (g1 - g0) * ((t - t0) / (t1 - t0) if t1 > t0 else 0.0)
    return points[-1][1]


def habiller(voix_pcm: bytes, intro_s: float = INTRO_S, outro_s: float = OUTRO_S, boost: float = 1.0) -> bytes:
    """PCM 16 bits mono 24 kHz : ouverture musicale, voix avec fond discret, fermeture."""
    voix = array("h")
    voix.frombytes(voix_pcm)
    n_voix = len(voix)
    n_intro, n_outro = int(SR * intro_s), int(SR * outro_s)
    n = n_intro + n_voix + n_outro
    fond = nappe(n / SR, 1.0)
    pts = enveloppe_fond(n / SR)
    piste = array("f", [0.0]) * n
    bloc = 240  # enveloppe interpolée par blocs de 10 ms
    for i0 in range(0, n, bloc):
        g0, g1 = _gain(pts, i0 / SR), _gain(pts, min(n, i0 + bloc) / SR)
        for k in range(min(bloc, n - i0)):
            piste[i0 + k] = fond[i0 + k] * (g0 + (g1 - g0) * k / bloc) * boost
    for i in range(n_voix):
        piste[n_intro + i] += voix[i] / 32768.0
    ouverture = motif((RE * 2, FA * 2, LA * 2), 0.55, 0.20, 5.0)
    fermeture = motif((LA * 2, FA * 2, RE * 2), 0.60, 0.20, outro_s - 0.5)
    for i, x in enumerate(ouverture):
        piste[i] += x
    debut = n - n_outro + int(SR * 0.5)
    for i, x in enumerate(fermeture):
        if debut + i < n:
            piste[debut + i] += x
    return array("h", (max(-32768, min(32767, int(x * 32767))) for x in piste)).tobytes()


# ---------------------------------------------------------------- ouverture chaleureuse en mineur (3 octobre 2026)
# Demande du propriétaire : « une petite musique un peu énergique mais un peu mineure ». Première version rejetée
# (« ça fait exorciste », « plus chaleureux », « arpège mineur ») : cloche aiguë façon « Tubular Bells » et accord de
# mi majeur tendu. Maintenant : piano électrique doux, arpège de la mineur dans le médium, progression la mineur, fa,
# do, sol (mineur mais ouverte, sans tension), nappe chaude, pulsation légère. Aucune cloche, aucun aigu.
BPM = 108
BATTEMENT_S = 60 / BPM
MESURE_S = 4 * BATTEMENT_S
NB_MESURES = 4
OUVERTURE_S = NB_MESURES * MESURE_S      # ≈ 8,9 s
QUEUE_S = 2.2  # résonance de l'accord final, recouverte par le début de la voix
ACCORDS = (  # numéros de notes MIDI : (basse, arpège)
    (33, (57, 60, 64, 67)),  # la mineur 7 : la do mi sol
    (29, (53, 57, 60, 64)),  # fa majeur 7 : fa la do mi
    (36, (55, 60, 64, 67)),  # do majeur : sol do mi sol
    (31, (55, 59, 62, 66)),  # sol majeur : sol si ré fa#, ouvre vers la mineur
)
MELODIE = ((1, 2.5, 76, 1.2), (1, 3.5, 72, 0.9),   # (mesure, temps, note, durée en s) : mi, do
           (2, 0.5, 79, 1.0), (2, 2.0, 76, 1.2),   # sol, mi
           (3, 0.5, 74, 0.9), (3, 2.0, 72, 1.1))   # ré, do


def _hz(midi: int) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def _piano_doux(freq: float, duree_s: float, gain: float) -> list[float]:
    """Piano électrique doux : attaque de 6 ms, harmoniques qui s'éteignent vite, résonance naturelle."""
    n = int(SR * duree_s)
    att = int(SR * 0.006)
    out = []
    for i in range(n):
        t = i / SR
        a = min(1.0, i / att) if att else 1.0
        corps = (math.sin(2 * math.pi * freq * t)
                 + 0.38 * math.sin(4 * math.pi * freq * t) * math.exp(-6.0 * t)
                 + 0.12 * math.sin(6 * math.pi * freq * t) * math.exp(-10.0 * t))
        out.append(gain * a * math.exp(-3.2 * t / max(duree_s, 0.2) * 1.6) * corps)
    return out


def _basse_chaude(freq: float, duree_s: float, gain: float) -> list[float]:
    n = int(SR * duree_s)
    return [gain * math.exp(-4.0 * i / n) * (math.sin(2 * math.pi * freq * i / SR)
            + 0.3 * math.sin(4 * math.pi * freq * i / SR)) for i in range(n)]


def _nappe_chaude(notes: tuple[int, ...], duree_s: float, gain: float) -> list[float]:
    n = int(SR * duree_s)
    montee = int(SR * 0.5)
    descente = int(SR * 0.6)
    out = []
    for i in range(n):
        env = min(1.0, i / montee, (n - i) / descente)
        out.append(gain * env * sum(math.sin(2 * math.pi * _hz(m) * i / SR) for m in notes) / len(notes))
    return out


def _grosse_caisse(gain: float = 0.32) -> list[float]:
    n = int(SR * 0.2)
    out, phase = [], 0.0
    for i in range(n):
        t = i / SR
        phase += 2 * math.pi * (50 + 60 * math.exp(-30 * t)) / SR
        out.append(gain * math.sin(phase) * math.exp(-16 * t))
    return out


def _charleston(graine: int, gain: float = 0.04) -> list[float]:
    n = int(SR * 0.03)
    etat = graine * 2654435761 % 2**32
    out = []
    for i in range(n):
        etat = (etat * 1664525 + 1013904223) % 2**32
        out.append(gain * (etat / 2**31 - 1.0) * math.exp(-5.0 * i / n))
    return out


def _poser(piste: array, debut_s: float, son: list[float]) -> None:
    d = int(debut_s * SR)
    for i, x in enumerate(son):
        if 0 <= d + i < len(piste):
            piste[d + i] += x


def ouverture_energique() -> array:
    """Piste flottante de OUVERTURE_S + QUEUE_S secondes (pas encore normalisée)."""
    n = int(SR * (OUVERTURE_S + QUEUE_S))
    piste = array("f", [0.0]) * n
    caisse = _grosse_caisse()
    for b in range(NB_MESURES * 4):
        t = b * BATTEMENT_S
        if b >= 4 and b % 2 == 0:
            _poser(piste, t, caisse)                       # pulsation légère à partir de la 2e mesure
        _poser(piste, t + BATTEMENT_S / 2, _charleston(b + 7, 0.04 if b >= 4 else 0.02))
    for m, (basse, arpege) in enumerate(ACCORDS):
        t0 = m * MESURE_S
        _poser(piste, t0, _nappe_chaude(tuple(arpege), MESURE_S + 0.3, 0.07))
        for rapport in (0, 1.5, 2.5):                      # basse syncopée
            _poser(piste, t0 + rapport * BATTEMENT_S, _basse_chaude(_hz(basse), 0.6, 0.20))
        ordre = (0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3, 2, 1)  # arpège montant et descendant, croches
        for k, idx in enumerate(ordre):
            fort = 1.0 if k % 4 == 0 else 0.62
            _poser(piste, t0 + k * BATTEMENT_S / 4, _piano_doux(_hz(arpege[idx]), 0.5, 0.11 * fort))
    for mesure, temps, note, duree in MELODIE:
        _poser(piste, mesure * MESURE_S + temps * BATTEMENT_S, _piano_doux(_hz(note), duree + 0.8, 0.12))
    # accord final : la mineur ouvert (la, mi, la, do, mi), sans aigu
    fin = OUVERTURE_S
    _poser(piste, fin, caisse)
    for note, gain in ((45, 0.18), (57, 0.13), (64, 0.11), (69, 0.10), (72, 0.09)):
        _poser(piste, fin, _piano_doux(_hz(note), QUEUE_S + 0.6, gain))
    return piste


def avec_ouverture_energique(voix_pcm: bytes, niveau: float = 0.7) -> bytes:
    """Ouverture énergique, puis la voix qui entre pendant la résonance du dernier accord."""
    voix = array("h")
    voix.frombytes(voix_pcm)
    intro = ouverture_energique()
    crete = max(abs(x) for x in intro) or 1.0
    n_intro = int(SR * OUVERTURE_S)
    n = n_intro + len(voix) + int(SR * 0.5)
    piste = array("f", [0.0]) * n
    for i, x in enumerate(intro):
        if i < n:
            # la résonance baisse franchement quand la voix démarre
            gain = 1.0 if i < n_intro else max(0.0, 1.0 - (i - n_intro) / (SR * QUEUE_S)) ** 1.5 * 0.55
            piste[i] += x / crete * niveau * gain
    for i, x in enumerate(voix):
        piste[n_intro + i] += x / 32768.0
    return array("h", (max(-32768, min(32767, int(x * 32767))) for x in piste)).tobytes()


# ---------------------------------------------------------------- thème fourni par le propriétaire
# La musique synthétisée par ce programme a été rejetée deux fois (3 octobre 2026). Le thème est maintenant un
# fichier du dépôt, podcast/musique/ouverture.mp3 (ou .wav) : tant qu'il n'existe pas, l'épisode est sans musique.
DOSSIER_THEME = None  # défini par narration.py (racine du dépôt)


def trouver_theme(racine) -> "Path | None":
    from pathlib import Path
    for ext in ("mp3", "wav", "m4a"):
        p = Path(racine) / "podcast" / "musique" / f"ouverture.{ext}"
        if p.exists():
            return p
    return None


def decoder_theme(chemin, duree_max_s: float = 12.0) -> bytes:
    """Décode le fichier en PCM 16 bits mono 24 kHz avec ffmpeg (présent sur le serveur de publication).
    Seules les `duree_max_s` premières secondes sont gardées (le thème fourni dure 30 s)."""
    import subprocess
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(chemin), "-t", str(duree_max_s), "-ac", "1", "-ar", str(SR),
                        "-f", "s16le", "-"], capture_output=True, check=True)
    return r.stdout


def _rms(pcm: array) -> float:
    return (sum(x * x for x in pcm) / max(1, len(pcm))) ** 0.5


def melanger_theme(theme_pcm: bytes, voix_pcm: bytes, recouvrement_s: float = 2.0, rapport: float = 1.1,
                   fondu_s: float = 3.0) -> bytes:
    """Le thème joue seul, puis la voix entre `recouvrement_s` avant la fin du thème, qui s'éteint en fondu.
    Le thème est mis au même niveau sonore que la voix (rapport 1,1 : un peu plus fort au début), car un thème
    généré est souvent bien plus fort qu'une voix de synthèse."""
    theme = array("h")
    theme.frombytes(theme_pcm)
    voix = array("h")
    voix.frombytes(voix_pcm)
    n_theme = len(theme)
    gain_theme = rapport * _rms(voix) / (_rms(theme) or 1.0)
    debut_voix = max(0, n_theme - int(SR * recouvrement_s))
    n = max(n_theme, debut_voix + len(voix)) + int(SR * 0.5)
    piste = array("f", [0.0]) * n
    nf = int(SR * fondu_s)
    for i, x in enumerate(theme):
        g = gain_theme
        if i >= n_theme - nf:
            g *= max(0.0, (n_theme - i) / nf)
        piste[i] += x / 32768.0 * g
    for i, x in enumerate(voix):
        piste[debut_voix + i] += x / 32768.0
    crete = max(abs(x) for x in piste) or 1.0
    echelle = min(1.0, 0.95 / crete)  # jamais de saturation
    return array("h", (max(-32768, min(32767, int(x * echelle * 32767))) for x in piste)).tobytes()


# ---------------------------------------------------------------- jingles entre les grandes parties
def jingle_depuis_theme(theme_pcm: bytes, duree_s: float = 2.5, fondu_entree_s: float = 0.08, fondu_sortie_s: float = 1.2) -> bytes:
    """Court extrait du début du thème (2,5 s par défaut), avec un fondu d'entrée bref et un fondu de sortie."""
    theme = array("h")
    theme.frombytes(theme_pcm)
    n = min(len(theme), int(SR * duree_s))
    ne, ns = int(SR * fondu_entree_s), int(SR * fondu_sortie_s)
    out = array("h")
    for i in range(n):
        g = min(1.0, i / ne if ne else 1.0, (n - i) / ns if ns else 1.0)
        out.append(int(theme[i] * g))
    return out.tobytes()


# Départs (en secondes) des extraits du thème utilisés comme jingles : le début, puis des passages différents.
DEPARTS_JINGLES = (0.0, 12.0, 15.0, 18.0, 21.0, 24.0, 26.5)


def jingles_depuis_theme(theme_pcm: bytes, nombre: int, duree_s: float = 3.5) -> list[bytes]:
    """`nombre` jingles, chacun pris à un endroit différent du thème (on reboucle s'il y en a plus que de départs)."""
    theme = array("h")
    theme.frombytes(theme_pcm)
    departs = [d for d in DEPARTS_JINGLES if int(SR * d) < len(theme) - int(SR * 1.5)] or [0.0]
    sortie = []
    for k in range(nombre):
        d = int(SR * departs[k % len(departs)])
        extrait = theme[d:d + int(SR * duree_s)]
        sortie.append(jingle_depuis_theme(extrait.tobytes(), duree_s, 0.15, 1.8))
    return sortie


def assembler_parties(parties_pcm: list[bytes], jingle_pcm, silence_s: float = 0.7,
                      rapport: float = 0.9, recouvrement_s: float = 1.5) -> bytes:
    """Voix des parties mises bout à bout. Entre deux parties, un jingle (au niveau sonore de la voix × rapport) :
    il démarre après un court silence et s'éteint en fondu SOUS le début de la partie suivante, qui entre
    `recouvrement_s` avant la fin du jingle. `jingle_pcm` : un jingle, une liste de jingles (utilisés tour à tour)
    ou None (alors seulement un silence)."""
    voix = array("h")
    for p in parties_pcm:
        voix.frombytes(p)
    blanc = lambda d: array("h", [0]) * int(SR * d)  # noqa: E731
    if not jingle_pcm:
        sortie = array("h")
        for i, p in enumerate(parties_pcm):
            if i:
                sortie.extend(blanc(silence_s))
            a = array("h")
            a.frombytes(p)
            sortie.extend(a)
        return sortie.tobytes()
    liste = [jingle_pcm] if isinstance(jingle_pcm, (bytes, bytearray)) else list(jingle_pcm)
    niveau = rapport * _rms(voix)
    piste = array("f")
    for i, p in enumerate(parties_pcm):
        a = array("h")
        a.frombytes(p)
        debut = len(piste)
        if i:
            j = array("h")
            j.frombytes(liste[(i - 1) % len(liste)])
            gain = niveau / (_rms(j) or 1.0)
            piste.extend(array("f", [0.0]) * int(SR * 0.3))
            debut_j = len(piste)
            piste.extend(array("f", (x * gain for x in j)))
            debut = max(debut_j, len(piste) - int(SR * recouvrement_s))
        if len(piste) < debut + len(a):
            piste.extend(array("f", [0.0]) * (debut + len(a) - len(piste)))
        for k, x in enumerate(a):
            piste[debut + k] += x
    crete = max((abs(x) for x in piste), default=1.0) or 1.0
    echelle = min(1.0, 32000.0 / crete)
    return array("h", (int(x * echelle) for x in piste)).tobytes()
