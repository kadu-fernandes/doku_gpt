from __future__ import annotations

import copy

from doku_gpt.enum.link_type import LinkType
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.resolver.link_tag.abstract_namespace_resolver import AbstractNamespaceResolver
from doku_gpt.resolver.link_tag.external_resolver import ExternalResolver
from doku_gpt.resolver.link_tag.internal_absolute_resolver import InternalAbsoluteResolver
from doku_gpt.resolver.link_tag.internal_implicit_resolver import InternalImplicitResolver
from doku_gpt.resolver.link_tag.internal_prior_resolver import InternalPriorResolver
from doku_gpt.resolver.link_tag.internal_relative_resolver import InternalRelativeResolver
from doku_gpt.resolver.link_tag.interwiki_resolver import InterwikiResolver


class Resolver(AbstractNamespaceResolver):
    def can_resolve(self, link_tag: LinkTag) -> bool:
        return True

    def resolve(self, link_tag: LinkTag) -> tuple[bool, LinkTag]:
        resolved_tag = copy.copy(link_tag)

        if resolved_tag.is_interwiki:
            interwiki_resolver = InterwikiResolver(root_folder=self.root_folder)
            result, resolved_tag = interwiki_resolver.resolve(resolved_tag)
            return (True, resolved_tag) if result is True else (False, link_tag)

        if resolved_tag.is_external:
            external_resolver = ExternalResolver(root_folder=self.root_folder)
            result, resolved_tag = external_resolver.resolve(resolved_tag)
            return (True, resolved_tag) if result is True else (False, link_tag)

        if LinkType.INTERNAL_ABSOLUTE == resolved_tag.link_type:
            absolute_resolver = InternalAbsoluteResolver(root_folder=self.root_folder, context=self.context)
            result, resolved_tag = absolute_resolver.resolve(resolved_tag)
            return (True, resolved_tag) if result is True else (False, link_tag)

        if LinkType.INTERNAL_PRIOR == resolved_tag.link_type:
            prior_resolver = InternalPriorResolver(root_folder=self.root_folder, context=self.context)
            result, resolved_tag = prior_resolver.resolve(resolved_tag)
            return (True, resolved_tag) if result is True else (False, link_tag)

        if LinkType.INTERNAL_RELATIVE == resolved_tag.link_type:
            relative_resolver = InternalRelativeResolver(root_folder=self.root_folder, context=self.context)
            result, resolved_tag = relative_resolver.resolve(resolved_tag)
            return (True, resolved_tag) if result is True else (False, link_tag)

        # Fallback: implicit
        implicit_resolver = InternalImplicitResolver(root_folder=self.root_folder, context=self.context)
        result, resolved_tag = implicit_resolver.resolve(resolved_tag)
        return (True, resolved_tag) if result is True else (False, link_tag)
