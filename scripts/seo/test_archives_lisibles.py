"""Toutes les éditions publiées doivent rester lisibles par les générateurs.

Le 17 octobre 2026, la publication du jour a échoué parce que deux éditions
avaient un <title> sans « — Scénario » et que le générateur du tableau des
archives n'y trouvait plus de titre. Ce test lit les vraies pages du dépôt : il
échoue dès qu'une modification (titres, balises, modèle) rend une édition
illisible, avant que la publication du matin ne casse.
"""
import sys
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import extract_article_data as ead
import generate_archives_table as gat

PAGES = sorted(p for p in (RACINE / "archives").glob("2*.html"))


class EditionsLisibles(unittest.TestCase):
    def test_il_y_a_des_editions(self):
        self.assertGreater(len(PAGES), 50)

    def test_titre_present_et_complet(self):
        for page in PAGES:
            texte = page.read_text(encoding="utf-8")
            for module in (gat, ead):
                titre = module.extract_title(texte)
                self.assertTrue(titre, f"{page.name} : titre introuvable ({module.__name__})")
                self.assertFalse(titre.endswith("…"), f"{page.name} : titre coupé")

    def test_generateur_du_tableau_accepte_toutes_les_editions(self):
        for page in PAGES:
            article = gat.parse_article(page)
            self.assertTrue(article["title"], page.name)
            gat.render_table_row(article, featured=False)


if __name__ == "__main__":
    unittest.main()
