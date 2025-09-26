from __future__ import annotations

import unittest

from doku_gpt.sanitizer.doku.line.link_label_sanitizer import LinkLabelSanitizer


class TestLinkLabelSanitizer(unittest.TestCase):
    def test_sanitize_first(self) -> None:
        nok = "This is [[https://github.com|Github]] and it' a website."
        ok = "This is Github and it' a website."
        self.assertEqual(ok, LinkLabelSanitizer.sanitize(nok))

    def test_sanitize_second(self) -> None:
        nok = "This is [[https://github.com|]] and it' a website."
        ok = "This is and it' a website."
        self.assertEqual(ok, LinkLabelSanitizer.sanitize(nok))

    def test_sanitize_third(self) -> None:
        nok = "This is [[https://github.com]] and it' a website."
        ok = "This is and it' a website."
        self.assertEqual(ok, LinkLabelSanitizer.sanitize(nok))

    def test_sanitize_fourth(self) -> None:
        nok = "This is [[:some:namespace:page|Page]] and it's a Dokuwiki page."
        ok = "This is Page and it's and it' a Dokuwiki page."
        self.assertEqual(ok, LinkLabelSanitizer.sanitize(nok))

    def test_sanitize_fifth(self) -> None:
        nok = "This is [[:some:namespace:page|]] and it's a Dokuwiki page."
        ok = "This is and it's and it' a Dokuwiki page."
        self.assertEqual(ok, LinkLabelSanitizer.sanitize(nok))

    def test_sanitize_sixth(self) -> None:
        nok = "This is [[:some:namespace:page]] and it's a Dokuwiki page."
        ok = "This is and it's and it' a Dokuwiki page."
        self.assertEqual(ok, LinkLabelSanitizer.sanitize(nok))
