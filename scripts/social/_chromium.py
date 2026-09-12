"""
Chemin Chromium partagé par les scripts de génération d'image (Playwright).

`/opt/pw-browsers/chromium` est le navigateur pré-installé du sandbox de
développement (PLAYWRIGHT_BROWSERS_PATH de cet environnement) — n'existe
pas sur un runner GitHub Actions, qui installe son propre Chromium à
l'emplacement par défaut de Playwright (`playwright install chromium`,
voir les workflows sous .github/workflows/). Ce chemin n'est donc utilisé
que s'il existe réellement ; sinon Playwright retrouve tout seul le
navigateur qu'il a installé lui-même — voir chromium_launch_kwargs().

Introduit le 12 septembre 2026 en même temps que la première utilisation
CI (generate_instagram_image.py, --lang en) ; les autres scripts de
génération d'image (generate_pub_image.py, generate_suivi_image.py)
avaient le même chemin en dur, corrigés dans la foulée pour rester
utilisables sur un runner.
"""
from pathlib import Path

_SANDBOX_CHROMIUM = "/opt/pw-browsers/chromium"


def chromium_launch_kwargs():
    """kwargs à passer à `playwright.chromium.launch(**kwargs)` : force le
    chemin du sandbox de dev s'il existe, sinon laisse Playwright choisir
    (comportement par défaut, celui qu'un runner CI doit utiliser)."""
    return {"executable_path": _SANDBOX_CHROMIUM} if Path(_SANDBOX_CHROMIUM).exists() else {}
