    from __future__ import annotations

import re
from typing import List


class LineNamespaceSanitizer:
    # [[path[#anchor][|label]]]
    _LINK_RE = re.compile(r"\[\[(?P<path>[^\]|#]+)(?P<rest>(?:#[^\]|]+)?(?:\|[^\]]*)?)\]\]")

    @classmethod
    def sanitize(cls, line: str) -> None:
        """Find namespaces inside a line, clean them, and return the updated line."""
        namespaces = cls.__extract_namespaces(line)
        for namespace in namespaces:
            sanitized = cls.__sanitize_namespace(namespace)
            cls.__replace_namespace(line, namespace, sanitized)
        return line

    @classmethod
    def __extract_namespaces(cls, line: str) -> List[str]:
        """Return all namespace-like paths found inside [[...]] on this line."""
        out: List[str] = []
        for match in cls._LINK_RE.finditer(line):
            path = match.group("path").strip()
            if cls._is_namespace(path):
                out.append(path)
        return out

    @classmethod
    def __sanitize_namespace(cls, namespace: str) -> str:
        """Sanitize a given namespace."""

    @classmethod
    def __replace_namespace(cls, line: str, old: str, new: str) -> str:
        """Replace an old namespace with a new one in a given line."""
        return line.replace(old, new)