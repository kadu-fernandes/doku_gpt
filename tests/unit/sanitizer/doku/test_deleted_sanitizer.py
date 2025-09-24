from __future__ import annotations

import unittest

from doku_gpt.sanitizer.doku.deleted_sanitizer import DeletedSanitizer


class TestDeletedSanitizer(unittest.TestCase):
    TO_SANITIZE = "DokuWiki supports **bold**, //italic//, __underlined__ and ''monospaced'' texts. But, of course you can **__//''combine''//__** all these. You can use <sub>subscript</sub>, <sup>superscript</sup>, and <del>deleted</del> as well."
    LINE = "DokuWiki supports **bold**, //italic//, __underlined__ and ''monospaced'' texts. But, of course you can **__//''combine''//__** all these. You can use <sub>subscript</sub>, <sup>superscript</sup>, and deleted as well."

    def test_sanitize(self) -> None:
        self.assertEqual(self.LINE, DeletedSanitizer.sanitize(self.TO_SANITIZE))
