from __future__ import annotations

from doku_gpt.factory.link_tag_factory import LinkTagFactory
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestLinkTagFactoryExternal(AbstractFakeDokuTest):
    def test_valid(self) -> None:
        values = self.__get_values()
        factory = self.__get_link_tag_factory()
        link_tag = factory.get(str(values["link_tag"]))
        self.assertIsNotNone(link_tag)
        self.assertTrue(link_tag.is_external)
        self.assertEqual(values["link_tag"], link_tag.link_tag)
        self.assertEqual(values["content"], link_tag.content)

    def __get_values(self) -> dict[str, str | None]:
        core: str = "https://www.youtube.com/watch?v=W2c1HRGB4mE"
        label: str = "3 Disturbing Childhood Memory Horror Stories"
        content: str = f"{core}|{label}"
        link_tag: str = f"[[{content}]]"
        return {
            "core": core,
            "label": label,
            "content": content,
            "link_tag": link_tag,
        }

    def __get_link_tag_factory(self) -> LinkTagFactory:
        return LinkTagFactory(self.tmp_root)
