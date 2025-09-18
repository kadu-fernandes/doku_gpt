from __future__ import annotations

import unittest

from doku_gpt.enum.link_type import LinkType
from doku_gpt.model.link_tag import LinkTag


class TestLinkTagInterwiki(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.__link_type: LinkType = LinkType.EXTERNAL
        self.__target_prefix: str = "https://babylonbee.com/news/after-antifa-designated-a-terrorist-organization-trump-orders-drone-strikes-on-portland"
        self.__target_fragment: str = "previous"
        self.__target_query: str = "some=thing"
        self.__resolved: str = "https://babylonbee.com/news/after-antifa-designated-a-terrorist-organization-trump-orders-drone-strikes-on-portland?some=thing#previous"
        self.__label: str = "After Antifa Designated A Terrorist Organization, Trump Orders Drone Strikes On Portland"
        self.__core: str = "https://babylonbee.com/news/after-antifa-designated-a-terrorist-organization-trump-orders-drone-strikes-on-portland"
        self.__core_full: str = f"{self.__core}?{self.__target_query}#{self.__target_fragment}"
        self.__content: str = f"{self.__core_full}|{self.__label}"
        self.__path: str | None = None
        self.__url: str | None = (
            "https://babylonbee.com/news/after-antifa-designated-a-terrorist-organization-trump-orders-drone-strikes-on-portland?some=thing#previous"
        )

    def test_is_external(self):
        link_tag = self.__valid_link_tag()
        self.assertTrue(link_tag.is_external)

    def test_is_internal(self):
        link_tag = self.__valid_link_tag()
        self.assertFalse(link_tag.is_internal)

    def test_is_interwiki(self):
        link_tag = self.__valid_link_tag()
        self.assertFalse(link_tag.is_interwiki)

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
            target_fragment=self.__target_fragment,
            target_query=self.__target_query,
            label=self.__label,
            resolved=self.__resolved,
        )
        return link_tag

    def __valid_link_tag_only_core(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(link_type=self.__link_type, target_prefix=self.__target_prefix)
        return link_tag

    def __valid_link_tag_only_query(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_query=self.__target_query,
        )
        return link_tag

    def __valid_link_tag_only_fragment(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_fragment=self.__target_fragment,
        )
        return link_tag
