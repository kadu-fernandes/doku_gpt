from __future__ import annotations

import unittest

from doku_gpt.extractor.web_page_extractor import WebPageExtractor


class TestisFile(unittest.TestCase):
    def test_can_fetch_valid(self):
        url = "https://www.imdb.com/title/tt0105695"
        self.assertTrue(WebPageExtractor.can_fetch(url))

    def test_url_exists_valid(self):
        url = "https://www.imdb.com/title/tt0105695"
        self.assertTrue(WebPageExtractor.url_exists(url))

    def test_url_exists_invalid(self):
        url = "https://www.imdb.com/title/tt0105695nope"
        self.assertFalse(WebPageExtractor.url_exists(url))

    def test_can_fetch_invalid(self):
        url = "ftp://anonymous:guest@fake-ftp.test/public/data.csv"
        self.assertFalse(WebPageExtractor.can_fetch(url))

    def test_fetch_title_01(self):
        url = "https://www.imdb.com/title/tt0105695"
        self.assertIn(WebPageExtractor.extract_title(url), ["Imperdoável", "Unforgiven"])

    def test_fetch_title_02(self):
        url = "https://www.imdb.com/title/tt0106064"
        self.assertEqual("Power Rangers", WebPageExtractor.extract_title(url))

    def test_fetch_title_03(self):
        url = "https://pt.wikipedia.org/wiki/Jair_Bolsonaro"
        self.assertEqual("Jair Bolsonaro", WebPageExtractor.extract_title(url))

    def test_fetch_title_04(self):
        url = "https://en.wikipedia.org/wiki/Robert_Redford"
        self.assertEqual("Robert Redford", WebPageExtractor.extract_title(url))
