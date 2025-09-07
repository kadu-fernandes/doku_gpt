from __future__ import annotations

from doku_gpt.resolver.namespace.abstract_namespace_resolver import AbstractNamespaceResolver


class RelativeNamespaceResolver(AbstractNamespaceResolver):
    def can_resolve(self, namespace: str) -> bool:
        to_resolve = namespace.strip()

        for prefix in AbstractNamespaceResolver._START_ABSOLUTE:
            if to_resolve.startswith(prefix):
                return False

        for prefix in AbstractNamespaceResolver._START_PRIOR:
            if to_resolve.startswith(prefix):
                return False

        for prefix in AbstractNamespaceResolver._START_RELATIVE:
            if to_resolve.startswith(prefix):
                return True

        return True

    def resolve(self, namespace: str) -> str:
        to_resolve = (namespace or "").strip()

        if not self.can_resolve(to_resolve):
            return namespace

        if self.context is None:
            raise RuntimeError("It's not possible to resolve a relative namespace without a context!")

        to_resolve = self._relative_namespace_to_path(namespace)

        return self.path_to_absolute_namespace(to_resolve)
