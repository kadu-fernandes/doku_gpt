from __future__ import annotations

from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.resolver.namespace.absolute_namespace_resolver import AbsoluteNamespaceResolver
from doku_gpt.resolver.namespace.abstract_namespace_resolver import AbstractNamespaceResolver
from doku_gpt.resolver.namespace.prior_namespace_resolver import PriorNamespaceResolver
from doku_gpt.resolver.namespace.relative_namespace_resolver import RelativeNamespaceResolver


class NamespaceResolver(AbstractNamespaceResolver):

    def can_resolve(self, namespace: str) -> bool:
        return True

    def resolve(self, namespace: str) -> str:

        if not self.can_resolve(namespace):
            return namespace

        resolver = AbsoluteNamespaceResolver(root_folder=self.root_folder, context=self.context)
        to_resolve = resolver.resolve(namespace)
        if to_resolve.startswith(":"):
            return to_resolve

        resolver = PriorNamespaceResolver(root_folder=self.root_folder, context=self.context)
        to_resolve = resolver.resolve(namespace)
        if to_resolve.startswith(":"):
            return to_resolve

        resolver = RelativeNamespaceResolver(root_folder=self.root_folder, context=self.context)
        to_resolve = resolver.resolve(namespace)
        if to_resolve.startswith(":"):
            return to_resolve

        raise InvalidNamespaceError(f"It was not possible to resolve the namespace '{namespace}'!")
