from __future__ import annotations

import unittest

from doku_gpt.enum.link_type import LinkType
from doku_gpt.model.link_tag import LinkTag


class TestLinkTagInterwiki(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.__link_type: LinkType = LinkType.INTERWIKI
        self.__target_prefix: str = "imdb"
        self.__target_suffix: str = "tt0105695"
        self.__target_fragment: str = "top_rated_movies"
        self.__target_query: str = "ref_=tt_ov_in_4"
        self.__resolved: str = "https://www.imdb.com/title/tt0105695?ref_=tt_ov_in_4#top_rated_movies"
        self.__label: str = "Unforgiven"
        self.__core: str = "imdb>tt0105695"
        self.__core_full: str = f"{self.__core}?{self.__target_query}#{self.__target_fragment}"
        self.__content: str = f"{self.__core_full}|{self.__label}"
        self.__path: str | None = None
        self.__url: str | None = "https://www.imdb.com/title/tt0105695?ref_=tt_ov_in_4#top_rated_movies"

    def test_is_external(self):
        link_tag = self.__valid_link_tag()
        self.assertFalse(link_tag.is_external)

    def test_is_internal(self):
        link_tag = self.__valid_link_tag()
        self.assertFalse(link_tag.is_internal)

    def test_is_interwiki(self):
        link_tag = self.__valid_link_tag()
        self.assertTrue(link_tag.is_interwiki)

    def test_core(self):
        link_tag = self.__valid_link_tag()
        self.assertEqual(self.__core_full, link_tag.core)

    def test_content(self):
        link_tag = self.__valid_link_tag()
        self.assertEqual(self.__content, link_tag.content)

    def test_link_tag(self):
        link_tag = self.__valid_link_tag()
        self.assertEqual(f"[[{self.__content}]]", link_tag.link_tag)

    def test_path(self):
        link_tag = self.__valid_link_tag()
        self.assertIsNone(link_tag.path)

    def test_url(self):
        link_tag = self.__valid_link_tag()
        self.assertEqual(self.__url, link_tag.url)

    def test_core_only_core(self):
        link_tag = self.__valid_link_tag_only_core()
        self.assertEqual(self.__core, link_tag.core)

    def test_content_only_core(self):
        link_tag = self.__valid_link_tag_only_core()
        self.assertEqual(self.__core, link_tag.content)

    def test_link_tag_only_core(self):
        link_tag = self.__valid_link_tag_only_core()
        self.assertEqual(f"[[{self.__core}]]", link_tag.link_tag)

    def test_core_only_query(self):
        link_tag = self.__valid_link_tag_only_query()
        self.assertEqual(f"{self.__core}?{self.__target_query}", link_tag.core)

    def test_content_only_query(self):
        link_tag = self.__valid_link_tag_only_query()
        self.assertEqual(f"{self.__core}?{self.__target_query}", link_tag.content)

    def test_link_tag_only_query(self):
        link_tag = self.__valid_link_tag_only_query()
        self.assertEqual(f"[[{self.__core}?{self.__target_query}]]", link_tag.link_tag)

    def test_core_only_fragment(self):
        link_tag = self.__valid_link_tag_only_fragment()
        self.assertEqual(f"{self.__core}#{self.__target_fragment}", link_tag.core)

    def test_content_only_fragment(self):
        link_tag = self.__valid_link_tag_only_fragment()
        self.assertEqual(f"{self.__core}#{self.__target_fragment}", link_tag.content)

    def test_link_tag_only_fragment(self):
        link_tag = self.__valid_link_tag_only_fragment()
        self.assertEqual(f"[[{self.__core}#{self.__target_fragment}]]", link_tag.link_tag)

    def __valid_link_tag(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_suffix=self.__target_suffix,
            target_fragment=self.__target_fragment,
            target_query=self.__target_query,
            label=self.__label,
            resolved=self.__resolved,
        )
        return link_tag

    def __valid_link_tag_only_core(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type, target_prefix=self.__target_prefix, target_suffix=self.__target_suffix
        )
        return link_tag

    def __valid_link_tag_only_query(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_suffix=self.__target_suffix,
            target_query=self.__target_query,
        )
        return link_tag

    def __valid_link_tag_only_fragment(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_suffix=self.__target_suffix,
            target_fragment=self.__target_fragment,
        )
        return link_tag
