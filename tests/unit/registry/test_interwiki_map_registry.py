from __future__ import annotations

import unittest

from doku_gpt.error.invalid_interwiki_error import InvalidInterwikiError
from doku_gpt.registry.interwiki_map_registry import InterwikiMapRegistry


class TestInterwikiMapRegistry(unittest.TestCase):
    def test_returns_copy(self) -> None:
        original_map = InterwikiMapRegistry.get_map()
        modified_map = InterwikiMapRegistry.get_map()
        modified_map["wp"] = "CHANGED"
        self.assertNotEqual(original_map["wp"], modified_map["wp"])


class TestExists(unittest.TestCase):
    def test_exists_true_false(self) -> None:
        self.assertTrue(InterwikiMapRegistry.exists("wp"))
        self.assertTrue(InterwikiMapRegistry.exists("WP"))
        self.assertFalse(InterwikiMapRegistry.exists(" unknown "))


class TestGet(unittest.TestCase):
    def test_resolves_with_path(self) -> None:
        interwiki_id = "C++/Guide & Tips"
        url = InterwikiMapRegistry.get("wp", interwiki_id)
        self.assertTrue(url.startswith("https://en.wikipedia.org/wiki/"))
        self.assertEqual(url, "https://en.wikipedia.org/wiki/C++/Guide & Tips")

    def test_uses_quote_plus_for_query_templates(self) -> None:
        interwiki_id = "python tips & tricks"
        url = InterwikiMapRegistry.get("google", interwiki_id)
        self.assertTrue(url.startswith("https://www.google.com/search?q="))
        self.assertEqual(url, "https://www.google.com/search?q=python tips & tricks")

    def test_requires_existing_prefix(self) -> None:
        with self.assertRaises(InvalidInterwikiError):
            InterwikiMapRegistry.get("nope", "something")

    def test_requires_id_when_placeholder_present(self) -> None:
        with self.assertRaises(InvalidInterwikiError):
            InterwikiMapRegistry.get("wp", None)
        with self.assertRaises(InvalidInterwikiError):
            InterwikiMapRegistry.get("wp", "")

    def test_simple_knowns(self) -> None:
        imdb_url = InterwikiMapRegistry.get("imdb", "tt0105695")
        self.assertEqual(imdb_url, "https://www.imdb.com/title/tt0105695")
        php_url = InterwikiMapRegistry.get("phpfn", "str_replace")
        self.assertEqual(php_url, "https://www.php.net/str_replace")


class TestGetByTarget(unittest.TestCase):
    def test_resolves_target(self) -> None:
        url = InterwikiMapRegistry.get_by_target("wp>Python_(programming_language)")
        self.assertEqual(url, "https://en.wikipedia.org/wiki/Python_(programming_language)")

    def test_invalid_target_raises(self) -> None:
        for invalid in ["", "wponly", "wp>", ">id", "wp>a>b", "  >  "]:
            with self.assertRaises(InvalidInterwikiError):
                InterwikiMapRegistry.get_by_target(invalid)


class TestSplitInterwiki(unittest.TestCase):
    def test_valid(self) -> None:
        prefix, interwiki_id = InterwikiMapRegistry.split_interwiki("wp>Some_Page")
        self.assertEqual(prefix, "wp")
        self.assertEqual(interwiki_id, "Some_Page")

    def test_invalid(self) -> None:
        for invalid in ["", "wponly", "wp>", ">id", "wp>a>b", "  >  "]:
            with self.assertRaises(InvalidInterwikiError):
                InterwikiMapRegistry.split_interwiki(invalid)
