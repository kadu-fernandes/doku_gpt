from __future__ import annotations

from doku_gpt.enum.link_type import LinkType
from doku_gpt.error.invalid_value_error import InvalidValueError
from doku_gpt.model.link_tag import LinkTag
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestLinkTagInternalPrior(AbstractFakeDokuTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.__link_type: LinkType = LinkType.INTERNAL_PRIOR
        self.__target_prefix: str = "..some:prior:page"
        self.__target_fragment: str = "a_subtitle"
        self.__target_query: str = "some=thing"  # no leading '?'
        self.__resolved_value: str = "../some/prior/page.txt"
        self.__label_value: str = "This is a page from parent!"
        self.__core_base: str = "..some:prior:page"
        self.__core_full: str = f"{self.__core_base}?{self.__target_query}#{self.__target_fragment}"
        self.__content_full: str = f"{self.__core_full}|{self.__label_value}"
        self.__url_value: str | None = None

    def test_is_external(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        self.assertFalse(link_tag.is_external)

    def test_is_internal(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        self.assertTrue(link_tag.is_internal)

    def test_is_interwiki(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        self.assertFalse(link_tag.is_interwiki)

    def test_core_with_query_and_fragment(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        self.assertEqual(self.__core_full, link_tag.core)

    def test_content_with_label(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        self.assertEqual(self.__content_full, link_tag.content)

    def test_link_tag_bracketed(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        self.assertEqual(f"[[{self.__content_full}]]", link_tag.link_tag)

    def test_path_raises_for_non_absolute_internal_when_resolved_present(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        with self.assertRaises(InvalidValueError):
            _ = link_tag.path

    def test_path_is_none_when_resolved_is_none(self) -> None:
        link_tag = self.__create_link_tag_only_core()
        self.assertIsNone(link_tag.path)

    def test_url_is_none_for_internal_prior(self) -> None:
        link_tag = self.__create_valid_link_tag_with_all_fields()
        self.assertEqual(self.__url_value, link_tag.url)

    def test_core_only_base(self) -> None:
        link_tag = self.__create_link_tag_only_core()
        self.assertEqual(self.__core_base, link_tag.core)

    def test_content_only_base(self) -> None:
        link_tag = self.__create_link_tag_only_core()
        self.assertEqual(self.__core_base, link_tag.content)

    def test_link_tag_only_base(self) -> None:
        link_tag = self.__create_link_tag_only_core()
        self.assertEqual(f"[[{self.__core_base}]]", link_tag.link_tag)

    def test_core_with_only_query(self) -> None:
        link_tag = self.__create_link_tag_only_query()
        self.assertEqual(f"{self.__core_base}?{self.__target_query}", link_tag.core)

    def test_content_with_only_query(self) -> None:
        link_tag = self.__create_link_tag_only_query()
        self.assertEqual(f"{self.__core_base}?{self.__target_query}", link_tag.content)

    def test_link_tag_with_only_query(self) -> None:
        link_tag = self.__create_link_tag_only_query()
        self.assertEqual(f"[[{self.__core_base}?{self.__target_query}]]", link_tag.link_tag)

    def test_core_with_only_fragment(self) -> None:
        link_tag = self.__create_link_tag_only_fragment()
        self.assertEqual(f"{self.__core_base}#{self.__target_fragment}", link_tag.core)

    def test_content_with_only_fragment(self) -> None:
        link_tag = self.__create_link_tag_only_fragment()
        self.assertEqual(f"{self.__core_base}#{self.__target_fragment}", link_tag.content)

    def test_link_tag_with_only_fragment(self) -> None:
        link_tag = self.__create_link_tag_only_fragment()
        self.assertEqual(f"[[{self.__core_base}#{self.__target_fragment}]]", link_tag.link_tag)

    def __create_valid_link_tag_with_all_fields(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_fragment=self.__target_fragment,
            target_query=self.__target_query,
            label=self.__label_value,
            resolved=self.__resolved_value,
        )
        link_tag.attach_root(self.tmp_root)
        return link_tag

    def __create_link_tag_only_core(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
        )
        return link_tag

    def __create_link_tag_only_query(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_query=self.__target_query,
        )
        return link_tag

    def __create_link_tag_only_fragment(self) -> LinkTag:
        link_tag: LinkTag = LinkTag(
            link_type=self.__link_type,
            target_prefix=self.__target_prefix,
            target_fragment=self.__target_fragment,
        )
        return link_tag
