import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import indexnow

CLE = "a" * 32


class IndexNowTest(unittest.TestCase):
    def racine(self, avec_cle=True, avec_en=True):
        r = Path(tempfile.mkdtemp())
        (r / "archives").mkdir()
        (r / "en" / "archives").mkdir(parents=True)
        for d in ("2026-10-01", "2026-10-02"):
            (r / "archives" / f"{d}.html").write_text("x")
        if avec_en:
            (r / "en" / "archives" / "2026-10-02.html").write_text("x")
        if avec_cle:
            (r / f"{CLE}.txt").write_text(CLE)
        return r

    def test_payload_has_latest_edition_and_home(self):
        c = indexnow.charge(self.racine())
        self.assertEqual(c["key"], CLE)
        self.assertEqual(c["keyLocation"], f"https://lesscenarios.fr/{CLE}.txt")
        self.assertEqual(c["urlList"], ["https://lesscenarios.fr/", "https://lesscenarios.fr/archives/2026-10-02.html",
                                        "https://lesscenarios.fr/en/archives/2026-10-02.html"])

    def test_no_english_edition_yet(self):
        self.assertEqual(len(indexnow.charge(self.racine(avec_en=False))["urlList"]), 2)

    def test_key_file_must_contain_its_own_name(self):
        r = self.racine(avec_cle=False)
        (r / f"{CLE}.txt").write_text("autre")
        self.assertIsNone(indexnow.charge(r))

    def test_repo_key_is_valid(self):
        self.assertIsNotNone(indexnow.trouver_cle(indexnow.ROOT))


if __name__ == "__main__":
    unittest.main()
