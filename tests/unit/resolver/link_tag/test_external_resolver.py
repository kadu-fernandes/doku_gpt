from __future__ import annotations

from doku_gpt.factory.link_tag_factory import LinkTagFactory
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.resolver.link_tag.external_resolver import ExternalResolver
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestExternalResolver(AbstractFakeDokuTest):
    def test_can_resolve(self):
        resolver = ExternalResolver(self.tmp_root)
        link_tag = self.__get_link_tag()
        self.assertTrue(resolver.can_resolve(link_tag))

    def test_can_resolve_invalid(self):
        resolver = ExternalResolver(self.tmp_root)
        link_tag = self.__get_link_tag("[[some:namespace:page]]")
        self.assertFalse(resolver.can_resolve(link_tag))

    def test_values(self):
        resolver = ExternalResolver(self.tmp_root)
        link_tag = self.__get_link_tag()
        self.assertIsNone(link_tag.label)
        self.assertIsNone(link_tag.resolved)
        _, resolved = resolver.resolve(link_tag)
        self.assertEqual("Power Rangers", resolved.label)
        self.assertEqual("https://www.imdb.com/title/tt0106064", resolved.resolved)

    def __get_link_tag(self, link_tag: str = "[[https://www.imdb.com/title/tt0106064]]") -> LinkTag:
        factory = LinkTagFactory(self.tmp_root)
        return factory.get(link_tag)
