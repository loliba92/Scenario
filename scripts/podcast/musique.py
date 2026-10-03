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


# ---------------------------------------------------------------- ouverture énergique en mineur (4 octobre 2026)
# Demande du propriétaire : « une petite musique un peu énergique mais un peu mineure au début ». La nappe
# douce ci-dessus ne lui plaisait pas ; ici : pulsation, basse, arpège, cloche. La mesure dure 2 s (120 battements
# par minute), 4 mesures : la mineur, fa, do, mi (mi majeur = tension), puis accord final de la mineur.
BPM = 120
BATTEMENT_S = 60 / BPM
OUVERTURE_S = 8.0
QUEUE_S = 2.0  # résonance de l'accord final, recouverte par le début de la voix
ACCORDS = (  # numéros de notes MIDI : (basse, arpège)
    (33, (57, 60, 64, 69)),  # la mineur
    (29, (53, 57, 60, 65)),  # fa majeur
    (36, (55, 60, 64, 67)),  # do majeur
    (40, (52, 56, 59, 64)),  # mi majeur
)
MELODIE = ((2.0 * 2 + 1.5, 76, 0.9), (2.0 * 2 + 2.5, 74, 0.6), (2.0 * 2 + 3.0, 72, 1.0),
           (2.0 * 3 + 0.5, 71, 0.8), (2.0 * 3 + 1.5, 68, 0.8), (2.0 * 3 + 3.0, 71, 0.6))  # (temps en battements, note, durée)


def _hz(midi: int) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def _pincee(freq: float, duree_s: float, gain: float, brillance: float = 0.5) -> list[float]:
    n = int(SR * duree_s)
    return [gain * math.exp(-5.0 * i / n) * (math.sin(2 * math.pi * freq * i / SR)
            + brillance * math.sin(4 * math.pi * freq * i / SR) * math.exp(-9.0 * i / n)
            + 0.25 * brillance * math.sin(6 * math.pi * freq * i / SR) * math.exp(-14.0 * i / n)) for i in range(n)]


def _grosse_caisse(gain: float = 0.55) -> list[float]:
    n = int(SR * 0.22)
    out, phase = [], 0.0
    for i in range(n):
        t = i / SR
        phase += 2 * math.pi * (45 + 85 * math.exp(-28 * t)) / SR
        out.append(gain * math.sin(phase) * math.exp(-14 * t))
    return out


def _charleston(graine: int, gain: float = 0.10) -> list[float]:
    n = int(SR * 0.04)
    etat = graine * 2654435761 % 2**32
    out = []
    for i in range(n):
        etat = (etat * 1664525 + 1013904223) % 2**32
        out.append(gain * (etat / 2**31 - 1.0) * math.exp(-60 * i / n * 3))
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
    for b in range(int(OUVERTURE_S / BATTEMENT_S)):
        t = b * BATTEMENT_S
        _poser(piste, t, caisse if b >= 2 else [x * 0.6 for x in caisse])  # la caisse entre en douceur
        _poser(piste, t + BATTEMENT_S / 2, _charleston(b + 7, 0.10 if b >= 4 else 0.05))
    for m, (basse, arpege) in enumerate(ACCORDS):
        t0 = m * 4 * BATTEMENT_S
        for k, rapport in enumerate((0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5)):  # croches de basse
            note = basse + (12 if k in (3, 6) else 0)
            _poser(piste, t0 + rapport * BATTEMENT_S, _pincee(_hz(note), 0.45, 0.20, 0.35))
        ordre = (0, 1, 2, 3, 2, 1, 2, 3, 0, 1, 2, 3, 2, 1, 3, 2)  # doubles croches d'arpège
        for k, idx in enumerate(ordre):
            fort = 1.0 if k % 4 == 0 else 0.6
            _poser(piste, t0 + k * BATTEMENT_S / 4, _pincee(_hz(arpege[idx] + 12), 0.30, 0.075 * fort, 0.7))
    for temps, note, duree in MELODIE:
        _poser(piste, temps * BATTEMENT_S, cloche(_hz(note + 12), 2.4 * duree))
    # accord final de la mineur sur le temps 8,0 s
    fin = OUVERTURE_S
    _poser(piste, fin, caisse)
    for note, gain in ((45, 0.22), (57, 0.16), (60, 0.14), (64, 0.14), (69, 0.12)):
        _poser(piste, fin, _pincee(_hz(note), QUEUE_S + 0.6, gain, 0.45))
    _poser(piste, fin, cloche(_hz(93), 2.6))
    return piste


def avec_ouverture_energique(voix_pcm: bytes, niveau: float = 0.55) -> bytes:
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
