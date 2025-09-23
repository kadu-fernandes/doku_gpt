from __future__ import annotations

from doku_gpt.factory.link_tag_factory import LinkTagFactory
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.resolver.link_tag.internal_implicit_resolver import InternalImplicitResolver
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestInternalImplicitResolver(AbstractFakeDokuTest):
    def test_absolute_valid(self):
        resolver = InternalImplicitResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "two:three:else"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual(":two:three:else", fixed.core)

    def test_absolute_label(self):
        resolver = InternalImplicitResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "two:three:else"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual("Else", fixed.label)

    def test_absolute_excerpt(self):
        resolver = InternalImplicitResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "two:three:else"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual("This is something else.", fixed.excerpt)

    def test_relative_valid(self):
        resolver = InternalImplicitResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "start"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual(":two:start", fixed.core)

    def test_relative_label(self):
        resolver = InternalImplicitResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "start"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual("Start", fixed.label)

    def test_relative_excerpt(self):
        resolver = InternalImplicitResolver(root_folder=self.tmp_root, context=self.folder_valid)
        namespace = "start"
        link_tag = self.__get_link_tag(namespace)
        status, fixed = resolver.resolve(link_tag)
        self.assertTrue(status)
        self.assertEqual(
            "* [[end|End]] * [[~else]] * [[.else]] * [[.:else]] - [[..:start|Start]] - [[..:end]] - [[..:one:start|Start]] - [[..:one:end|Start]] - [[:one:else|Else]] - [[one:else|Else]]",
            fixed.excerpt,
        )

    def __get_link_tag(self, link_tag: str) -> LinkTag:
        factory = LinkTagFactory(self.tmp_root)
        return factory.get(link_tag)
