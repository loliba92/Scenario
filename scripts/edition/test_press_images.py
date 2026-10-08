import unittest

import press_images as pi


class PressImagesTest(unittest.TestCase):
    def test_extract_og_image(self):
        page = '<head><meta property="og:image" content="https://x.fr/a.jpg?v=1&amp;p=2"></head>'
        self.assertEqual(pi.extract_og_image(page, "https://x.fr/art"), "https://x.fr/a.jpg?v=1&p=2")

    def test_twitter_et_url_relative(self):
        page = '<meta content="/img/a.jpg" name="twitter:image">'
        self.assertEqual(pi.extract_og_image(page, "https://x.fr/art"), "https://x.fr/img/a.jpg")

    def test_image_generique_ecartee(self):
        page = '<meta property="og:image" content="https://x.fr/bundles/trading-news-1.jpg">'
        self.assertIsNone(pi.extract_og_image(page, "https://x.fr/art"))
        self.assertIsNone(pi.extract_og_image("<html></html>", "https://x.fr/art"))

    def test_fill_missing_images(self):
        arts = [{"url": "https://a", "image": None}, {"url": "https://b", "image": "https://deja.jpg"}, {"url": "https://c", "image": ""}]
        n = pi.fill_missing_images(arts, fetch=lambda u: None if u.endswith("c") else "https://img/" + u[-1])
        self.assertEqual(n, 1)
        self.assertEqual([a["image"] for a in arts], ["https://img/a", "https://deja.jpg", ""])


if __name__ == "__main__":
    unittest.main()
