from __future__ import annotations

import unittest

from doku_gpt.sanitizer.doku.line.line_break_sanitizer import LinebreakSanitizer


class TestLineBreakSanitizer(unittest.TestCase):
    TO_SANITIZE = "This \\\\ was a line break!"

    def test_sanitize(self) -> None:
        self.assertEqual("This was a line break!", LinebreakSanitizer.sanitize(self.TO_SANITIZE))
