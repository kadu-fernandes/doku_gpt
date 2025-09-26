from __future__ import annotations

import re


class BoxSanitizer:
    OPEN = re.compile(r"<box\b[^>|]*\|([^>]*)>", flags=re.IGNORECASE)
    CLOSE = re.compile(r"</box\s*>", flags=re.IGNORECASE)

    @classmethod
    def sanitize(cls, line: str) -> str:
        line = cls.OPEN.sub(r"\1", line)
        line = cls.CLOSE.sub("", line)
        return line
