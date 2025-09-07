from __future__ import annotations

from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.resolver.namespace.abstract_namespace_resolver import AbstractNamespaceResolver


class AbsoluteNamespaceResolver(AbstractNamespaceResolver):

    def can_resolve(self, namespace: str) -> bool:
        to_resolve = namespace.strip()

        for prefix in AbstractNamespaceResolver._START_ABSOLUTE:
            if to_resolve.startswith(prefix):
                return True

        for prefix in AbstractNamespaceResolver._START_PRIOR:
            if to_resolve.startswith(prefix):
                return False

        for prefix in AbstractNamespaceResolver._START_RELATIVE:
            if to_resolve.startswith(prefix):
                return False

        return True

    def resolve(self, namespace: str) -> str:
        to_resolve = (namespace or "").strip()

        if not self.can_resolve(to_resolve):
            return namespace

        to_resolve = AbsoluteNamespaceResolver._resolve_requirements(to_resolve)

        to_resolve_core = self._remove_prefixes(to_resolve)
        to_resolve_core = to_resolve_core.rstrip(":")

        if "" == to_resolve_core:
            raise InvalidNamespaceError("The given namespace resolves to empty after removing prefixes.")
        self._absolute_namespace_to_path(to_resolve_core)

        return ":" + to_resolve_core
