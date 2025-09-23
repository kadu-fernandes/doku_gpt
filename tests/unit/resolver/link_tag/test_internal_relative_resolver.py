from __future__ import annotations

from doku_gpt.factory.link_tag_factory import LinkTagFactory
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.resolver.link_tag.internal_relative_resolver import InternalRelativeResolver
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestInternalRelativeResolver(AbstractFakeDokuTest):
    def test_valid(self):
        resolver = InternalRelativeResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "~:three:else"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual(":two:three:else", fixed.core)

    def test_label(self):
        resolver = InternalRelativeResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "~:three:else"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual("Else", fixed.label)

    def test_excerpt(self):
        resolver = InternalRelativeResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "~:three:else"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual("This is something else.", fixed.excerpt)

    def __get_link_tag(self, link_tag: str) -> LinkTag:
        factory = LinkTagFactory(self.tmp_root)
        return factory.get(link_tag)
