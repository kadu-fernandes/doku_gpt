from __future__ import annotations

import unittest

from doku_gpt.sanitizer.doku.subscript_sanitizer import SubscriptSanitizer


class TestSubscriptSanitizer(unittest.TestCase):
    TO_SANITIZE = "DokuWiki supports **bold**, //italic//, __underlined__ and ''monospaced'' texts. But, of course you can **__//''combine''//__** all these. You can use <sub>subscript</sub>, <sup>superscript</sup>, and <del>deleted</del> as well."
    LINE = "DokuWiki supports **bold**, //italic//, __underlined__ and ''monospaced'' texts. But, of course you can **__//''combine''//__** all these. You can use subscript, <sup>superscript</sup>, and <del>deleted</del> as well."

    def test_sanitize(self) -> None:
        self.assertEqual(self.LINE, SubscriptSanitizer.sanitize(self.TO_SANITIZE))
