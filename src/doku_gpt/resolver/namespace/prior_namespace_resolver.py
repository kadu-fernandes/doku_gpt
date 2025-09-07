from __future__ import annotations

from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.resolver.namespace.abstract_namespace_resolver import AbstractNamespaceResolver


class PriorNamespaceResolver(AbstractNamespaceResolver):

    def can_resolve(self, namespace: str) -> bool:
        to_resolve = namespace.strip()

        for prefix in AbstractNamespaceResolver._START_ABSOLUTE:
            if to_resolve.startswith(prefix):
                return False

        for prefix in AbstractNamespaceResolver._START_PRIOR:
            if to_resolve.startswith(prefix):
                return True

        for prefix in AbstractNamespaceResolver._START_RELATIVE:
            if to_resolve.startswith(prefix):
                return False

        return False

    def resolve(self, namespace: str) -> str:
        to_resolve = (namespace or "").strip()

        if not self.can_resolve(to_resolve):
            return namespace

        try:
            return self.path_to_absolute_namespace(self._prior_namespace_to_path(namespace))
        except InvalidPathError as ex:
            raise InvalidNamespaceError(f"The given namespace '{namespace}' does not exist!") from ex
