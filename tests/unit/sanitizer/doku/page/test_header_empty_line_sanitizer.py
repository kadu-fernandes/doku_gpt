import unittest

from doku_gpt.sanitizer.doku.page.header_empty_line_sanitizer import HeaderEmptyLineSanitizer


class TestHeaderEmptyLineSanitizer(unittest.TestCase):
    def test_sanitize(self) -> None:
        self.assertEqual(self.__ok(), HeaderEmptyLineSanitizer.sanitize(self.__nok()))

    def __nok(self) -> str:
        return "\n\n\n\n\n======= First Header ======\n\n\n\n\n"
        +"Some text.\n"
        +"===== Second Header =====\n\n"
        +"Some text.\n\n\n\n\n"
        +"==== Third Header ====\n\n\n\n\n"
        +"Some text.\n"
        +"==== Fourth Header ====\n"
        +"Some text.\n\n"
        +"Some text.\n"
        +"=== Fifth Header ===\n"
        +"Some text.\n\n\n\n\n"

    def __ok(self) -> str:
        return "======= First Header ======\n"
        +"Some text.\n\n"
        +"===== Second Header =====\n\n"
        +"Some text.\n\n"
        +"==== Third Header ====\n\n"
        +"Some text.\n\n"
        +"==== Fourth Header ====\n\n"
        +"Some text.\n\n"
        +"Some text.\n\n"
        +"=== Fifth Header ===\n\n"
        +"Some text.\n"
