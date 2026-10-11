"""Tests de gsc_sync.py — sans réseau : l'API Google est remplacée par de fausses réponses."""
import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsc_sync as g  # noqa: E402


def _faux_compte():
    """Compte de service factice avec une vraie clé RSA générée pour le test."""
    pem = subprocess.run(["openssl", "genrsa", "2048"], capture_output=True, text=True, check=True).stdout
    return {"client_email": "test@projet.iam.gserviceaccount.com", "private_key": pem,
            "token_uri": "https://oauth2.googleapis.com/token"}


def _b64d(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


class TestJwt(unittest.TestCase):
    def test_signature_valide(self):
        info = _faux_compte()
        jwt = g.build_jwt(info, now=1_700_000_000)
        header, claim, sig = jwt.split(".")
        self.assertEqual(json.loads(_b64d(header)), {"alg": "RS256", "typ": "JWT"})
        c = json.loads(_b64d(claim))
        self.assertEqual(c["iss"], info["client_email"])
        self.assertEqual(c["scope"], g.SCOPE)
        self.assertEqual(c["exp"] - c["iat"], 3600)
        # Vérification cryptographique avec la clé publique.
        with tempfile.TemporaryDirectory() as d:
            priv, pub, sigf = Path(d, "k.pem"), Path(d, "p.pem"), Path(d, "s.bin")
            priv.write_text(info["private_key"])
            subprocess.run(["openssl", "rsa", "-in", str(priv), "-pubout", "-out", str(pub)], capture_output=True, check=True)
            sigf.write_bytes(_b64d(sig))
            res = subprocess.run(["openssl", "dgst", "-sha256", "-verify", str(pub), "-signature", str(sigf)],
                                 input=f"{header}.{claim}".encode(), capture_output=True)
            self.assertEqual(res.returncode, 0, res.stderr)

    def test_cle_illisible(self):
        with self.assertRaises(g.GscError):
            g.build_jwt({"client_email": "a@b", "private_key": "pas une clé"})


class TestDonnees(unittest.TestCase):
    def test_summarize(self):
        by_date = [{"keys": ["2026-10-01"], "clicks": 10, "impressions": 100, "position": 5},
                   {"keys": ["2026-10-02"], "clicks": 30, "impressions": 300, "position": 9}]
        q = [{"keys": ["scénario"], "clicks": 4, "impressions": 40, "ctr": 0.1, "position": 3.456}]
        p = [{"keys": ["https://lesscenarios.fr/"], "clicks": 8, "impressions": 80, "ctr": 0.1, "position": 2}]
        s = g.summarize(by_date, q, p)
        self.assertEqual(s["totaux"]["clicks"], 40)
        self.assertEqual(s["totaux"]["impressions"], 400)
        self.assertEqual(s["totaux"]["ctr"], 0.1)
        self.assertEqual(s["totaux"]["position"], 8.0)   # moyenne pondérée par les impressions
        self.assertEqual(s["requetes"][0], {"requete": "scénario", "clicks": 4, "impressions": 40, "ctr": 0.1, "position": 3.5})
        self.assertEqual(s["pages"][0]["page"], "https://lesscenarios.fr/")

    def test_summarize_vide(self):
        s = g.summarize([], [], [])
        self.assertEqual(s["totaux"], {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0})

    def test_historique_fusion_et_tri(self):
        old = {"2026-10-02": {"clicks": 1}}
        new = g.history_points([{"keys": ["2026-10-01"], "clicks": 5, "impressions": 50, "ctr": 0.1, "position": 4}])
        merged = g.merge_history(old, new)
        self.assertEqual(list(merged), ["2026-10-01", "2026-10-02"])
        self.assertEqual(merged["2026-10-01"]["clicks"], 5)

    def test_inspection(self):
        data = {"inspectionResult": {"indexStatusResult": {"verdict": "PASS", "coverageState": "Submitted and indexed"}}}
        r = g.inspection_row("https://x/", data)
        self.assertEqual((r["verdict"], r["etat"]), ("PASS", "Submitted and indexed"))
        self.assertIsNone(g.inspection_row("https://x/", {})["verdict"])

    def test_pages_a_inspecter(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "archives").mkdir()
            (Path(d) / "en" / "archives").mkdir(parents=True)
            for day in ("2026-10-01", "2026-10-02", "2026-10-03"):
                (Path(d) / "archives" / f"{day}.html").write_text("x")
                (Path(d) / "en" / "archives" / f"{day}.html").write_text("x")
            urls = g.pages_to_inspect(Path(d))
        self.assertIn("https://lesscenarios.fr/", urls)
        self.assertIn("https://lesscenarios.fr/en/", urls)
        self.assertEqual(urls[len(g.KEY_PAGES)], "https://lesscenarios.fr/archives/2026-10-03.html")  # la plus récente d'abord
        self.assertEqual(urls[-3], "https://lesscenarios.fr/en/archives/2026-10-03.html")             # puis les éditions anglaises


class TestExecution(unittest.TestCase):
    def _http_factice(self, sites):
        def fake(method, url, headers=None, body=None, timeout=60):
            if url.endswith("/token"):
                return 200, {"access_token": "jeton"}
            if url.endswith("/sites"):
                return 200, {"siteEntry": [{"siteUrl": s, "permissionLevel": "siteFullUser"} for s in sites]}
            if "searchAnalytics/query" in url:
                dims = json.loads(body)["dimensions"][0]
                return 200, {"rows": [{"keys": ["2026-10-01" if dims == "date" else "x"], "clicks": 2, "impressions": 20, "ctr": 0.1, "position": 6}]}
            if "/sitemaps/" in url:
                return 200, {"lastDownloaded": "2026-10-11T00:00:00Z", "errors": "0", "warnings": "0"}
            if "urlInspection" in url:
                return 200, {"inspectionResult": {"indexStatusResult": {"verdict": "PASS", "coverageState": "Submitted and indexed"}}}
            return 404, {"error": {"message": "inattendu " + url}}
        return fake

    def test_deroule_complet(self):
        info = _faux_compte()
        with tempfile.TemporaryDirectory() as d, \
                mock.patch.object(g, "OUT_DIR", Path(d)), \
                mock.patch.object(g, "_http", self._http_factice([g.DEFAULT_SITE])), \
                mock.patch.object(g, "pages_to_inspect", return_value=["https://lesscenarios.fr/"]):
            self.assertEqual(g.run(info, g.DEFAULT_SITE), 0)
            noms = sorted(p.name for p in Path(d).iterdir())
            self.assertEqual(noms, ["history.json", "indexation.json", "sitemaps.json", "summary.json"])
            summ = json.loads((Path(d) / "summary.json").read_text())
            self.assertEqual(summ["totaux"]["clicks"], 2)
            self.assertEqual(json.loads((Path(d) / "indexation.json").read_text())["pages"][0]["verdict"], "PASS")

    def test_site_absent_explique_la_cause(self):
        info = _faux_compte()
        with mock.patch.object(g, "_http", self._http_factice(["https://autre.fr/"])):
            with self.assertRaises(g.GscError) as cm:
                g.run(info, g.DEFAULT_SITE)
        self.assertIn("compte de service", str(cm.exception))
        self.assertIn("sc-domain:lesscenarios.fr", str(cm.exception))

    def test_check_seul_n_ecrit_rien(self):
        info = _faux_compte()
        with tempfile.TemporaryDirectory() as d, mock.patch.object(g, "OUT_DIR", Path(d)), \
                mock.patch.object(g, "_http", self._http_factice([g.DEFAULT_SITE])):
            self.assertEqual(g.run(info, g.DEFAULT_SITE, check_only=True), 0)
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_refus_google_message_clair(self):
        def fake(method, url, headers=None, body=None, timeout=60):
            return (200, {"access_token": "j"}) if url.endswith("/token") else (403, {"error": {"message": "interdit"}})
        with mock.patch.object(g, "_http", fake):
            with self.assertRaises(g.GscError) as cm:
                g.run(_faux_compte(), g.DEFAULT_SITE)
        self.assertIn("Utilisateurs et autorisations", str(cm.exception))


class TestMain(unittest.TestCase):
    def test_secret_absent_sort_proprement(self):
        with mock.patch.dict(os.environ, {"GSC_SERVICE_ACCOUNT_JSON": ""}):
            self.assertEqual(g.main([]), 0)

    def test_json_invalide(self):
        with mock.patch.dict(os.environ, {"GSC_SERVICE_ACCOUNT_JSON": "{pas du json"}):
            self.assertEqual(g.main([]), 1)

    def test_json_sans_cle(self):
        with mock.patch.dict(os.environ, {"GSC_SERVICE_ACCOUNT_JSON": json.dumps({"client_email": "a@b"})}):
            self.assertEqual(g.main([]), 1)


if __name__ == "__main__":
    unittest.main()
