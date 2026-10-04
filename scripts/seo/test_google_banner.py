import shutil
import subprocess
import unittest

import add_google_banner as b
import add_spotify_follow as sp


class TestGoogleBanner(unittest.TestCase):
    def test_balise_apres_pwa_install_idempotente(self):
        for tag in ('<script src="assets/pwa-install.js" defer></script>', '<script defer="" src="../assets/pwa-install.js"></script>'):
            une = b.ajouter("<body>" + tag + "</body>")
            self.assertIn("google-source-banner.js", une)
            self.assertLess(une.index("pwa-install.js"), une.index("google-source-banner.js"))
            self.assertEqual(b.ajouter(une), une)

    def test_prefixe_relatif_conserve(self):
        une = b.ajouter('<script src="../assets/pwa-install.js" defer></script>')
        self.assertIn('src="../assets/google-source-banner.js"', une)

    def test_pages_figees_non_touchees(self):
        noms = {p.relative_to(b.ROOT).as_posix() for p in sp.pages("2026-10-04")}
        self.assertNotIn("archives/2026-10-03.html", noms)
        self.assertIn("archives/2026-10-04.html", noms)

    def test_script_valide(self):
        chemin = b.ROOT / "assets" / "google-source-banner.js"
        texte = chemin.read_text(encoding="utf-8")
        self.assertIn("google.com/preferences/source?q=lesscenarios.fr", texte)
        self.assertIn("localStorage", texte)
        if shutil.which("node"):
            r = subprocess.run(["node", "--check", str(chemin)], capture_output=True)
            self.assertEqual(r.returncode, 0, r.stderr.decode())


if __name__ == "__main__":
    unittest.main()
