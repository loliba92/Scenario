"""Aucun « **gras** » Markdown ne doit atteindre la page, d'où qu'il vienne (modèle de rédaction ou brief).

Le 17 octobre 2026, le preview du lendemain a échoué : un « ** » venu d'un champ non nettoyé a fait refuser le
HTML assemblé, et l'édition n'avait plus de preview.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_daily_edition as gde


class GrasMarkdown(unittest.TestCase):
    def test_html_texte_converti(self):
        html = '<p>Un chiffre de <b>1</b> et **84 %** du total</p><script>let x = 2**3;</script><style>/** c */</style>'
        out = gde.convert_markdown_bold_in_html(html)
        self.assertIn("<strong>84 %</strong>", out)
        self.assertIn("2**3", out)       # script intact
        self.assertIn("/** c */", out)   # style intact

    def test_etoiles_separees_par_une_balise(self):
        """« mot*<a class="lex-ref">*</a> » s'affiche « mot** » : les deux étoiles sont dans des blocs différents."""
        from bs4 import BeautifulSoup
        for html in (
            '<p>un soft power*<a class="lex-ref" href="#lex-x">*</a> ici</p>',
            '<p>un terme <em>mot*</em><a class="lex-ref" href="#lex-x">*</a></p>',
            '<p><strong>Titre*</strong>*<sup>1</sup></p>',
        ):
            visible = BeautifulSoup(gde.convert_markdown_bold_in_html(html), "html.parser").get_text()
            self.assertNotIn("**", visible, html)
            self.assertEqual(visible.count("*"), 1, html)  # l'étoile du renvoi au lexique est conservée

    def test_renvoi_au_lexique_seul_inchange(self):
        html = '<p>un soft power<a class="lex-ref" href="#lex-x">*</a> ici</p>'
        self.assertEqual(gde.convert_markdown_bold_in_html(html), html)

    def test_paire_mal_formee_supprimee(self):
        out = gde.convert_markdown_bold_in_html("<p>mot ** isolé</p>")
        self.assertNotIn("**", out)

    def test_html_sans_astérisque_inchange(self):
        html = "<p>rien à faire</p>"
        self.assertEqual(gde.convert_markdown_bold_in_html(html), html)

    def test_brief_nettoye_au_chargement(self):
        racine = Path(__file__).resolve().parents[2] / "editorial-briefs"
        brief = json.loads(sorted(racine.glob("2026-10-1[0-9].json"))[-1].read_text(encoding="utf-8"))
        brief["sujet"]["h1"] = "Le **pass Sport** survivra-t-il ?"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(brief, f)
        charge = gde.load_brief(f.name)
        self.assertEqual(charge["sujet"]["h1"], "Le pass Sport survivra-t-il ?")


if __name__ == "__main__":
    unittest.main()
