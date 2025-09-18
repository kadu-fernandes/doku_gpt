from __future__ import annotations

import re
from typing import List


class LineNamespaceSanitizer:
    # [[path[#anchor][|label]]]
    _LINK_RE = re.compile(r"\[\[(?P<path>[^\]|#]+)(?P<rest>(?:#[^\]|]+)?(?:\|[^\]]*)?)\]\]")

    @classmethod
    def sanitize(cls, line: str) -> tuple[bool, str]:
        """Find namespaces inside a line, clean them, and return the updated line."""
        to_sanitize = str(line)
        namespaces = cls.__extract_namespaces(to_sanitize)
        for namespace in namespaces:
            sanitized = cls.__sanitize_namespace(namespace)
            cls.__replace_namespace(to_sanitize, namespace, sanitized)
        return line != to_sanitize, to_sanitize

    @classmethod
    def __extract_namespaces(cls, line: str) -> List[str]:
        """Return all namespace-like paths found inside [[...]] on this line."""
        return [path.strip() for path, _ in cls._LINK_RE.findall(line)]

    @classmethod
    def __sanitize_namespace(cls, namespace: str) -> str:
        """Sanitize a given namespace."""
        return namespace

    @classmethod
    def __replace_namespace(cls, line: str, old: str, new: str) -> str:
        """Replace an old namespace with a new one in a given line."""
        return line.replace(old, new)
