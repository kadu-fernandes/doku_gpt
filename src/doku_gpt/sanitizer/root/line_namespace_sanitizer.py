from __future__ import annotations

import copy
import re
from typing import List

from doku_gpt.enum.link_type import LinkType
from doku_gpt.factory.link_tag_factory import LinkTagFactory
from doku_gpt.resolver.link_tag.external_resolver import ExternalResolver
from doku_gpt.resolver.link_tag.internal_absolute_resolver import InternalAbsoluteResolver
from doku_gpt.resolver.link_tag.internal_implicit_resolver import InternalImplicitResolver
from doku_gpt.resolver.link_tag.internal_prior_resolver import InternalPriorResolver
from doku_gpt.resolver.link_tag.internal_relative_resolver import InternalRelativeResolver
from doku_gpt.resolver.link_tag.interwiki_resolver import InterwikiResolver
from doku_gpt.sanitizer.root.abstract_root_sanitizer import AbstractRootSanitizer


class LineNamespaceSanitizer(AbstractRootSanitizer):
    _LINK_RE = re.compile(r"(?P<token>\[\[(?P<path>[^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]*)?\]\])")

    def sanitize(self, line: str) -> tuple[bool, str]:
        """Find link_tags inside a line, clean them, and return the updated line."""
        to_sanitize = str(line)
        namespaces = self.__extract_link_tags(to_sanitize)
        for namespace in namespaces:
            sanitized = self.__sanitize_link_tag(namespace)
            to_sanitize = self.__replace_link_tag(to_sanitize, namespace, sanitized)
        return line != to_sanitize, to_sanitize

    def __extract_link_tags(self, line: str) -> List[str]:
        """Return all link_tags-like paths found inside [[...]] on this line."""
        return [path.strip() for path, _ in self._LINK_RE.findall(line)]

    def __sanitize_link_tag(self, link_tag: str) -> str:
        """Sanitize a given link_tag."""
        factory = LinkTagFactory(root_folder=self.root_folder)
        tag = factory.get(link_tag)
        resolved_tag = copy.copy(tag)

        if resolved_tag.is_external:
            external_resolver = ExternalResolver(root_folder=self.root_folder)
            result, resolved_tag = external_resolver.resolve(resolved_tag)
            if result is True:
                return resolved_tag.link_tag
            return tag.link_tag

        if resolved_tag.is_interwiki:
            interwiki_resolver = InterwikiResolver(root_folder=self.root_folder)
            result, resolved_tag = interwiki_resolver.resolve(resolved_tag)
            if result is True:
                return resolved_tag.link_tag
            return tag.link_tag

        if LinkType.INTERNAL_ABSOLUTE == resolved_tag.link_type:
            absolute_resolver = InternalAbsoluteResolver(root_folder=self.root_folder, context=self.page_path)
            result, resolved_tag = absolute_resolver.resolve(resolved_tag)
            if result is True:
                return resolved_tag.link_tag
            return tag.link_tag

        if LinkType.INTERNAL_PRIOR == resolved_tag.link_type:
            prior_resolver = InternalPriorResolver(root_folder=self.root_folder, context=self.page_path)
            result, resolved_tag = prior_resolver.resolve(resolved_tag)
            if result is True:
                return resolved_tag.link_tag
            return tag.link_tag

        if LinkType.INTERNAL_RELATIVE == resolved_tag.link_type:
            relative_resolver = InternalRelativeResolver(root_folder=self.root_folder, context=self.page_path)
            result, resolved_tag = relative_resolver.resolve(resolved_tag)
            if result is True:
                return resolved_tag.link_tag
            return tag.link_tag

        implicit_resolver = InternalImplicitResolver(root_folder=self.root_folder, context=self.page_path)
        result, resolved_tag = implicit_resolver.resolve(resolved_tag)
        if result is True:
            return resolved_tag.link_tag
        return tag.link_tag

    def __replace_link_tag(self, line: str, old: str, new: str) -> str:
        """Replace an old link_tag with a new one in a given line."""

        if new.startswith("["):
            old = old.lstrip("[").rstrip("]").strip()
            old = f"[[{old}]]"
        return line.replace(old, new)
