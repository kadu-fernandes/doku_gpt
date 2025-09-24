from __future__ import annotations

import re


class LinebreakSanitizer:
    """DokuWiki forced line break: '\\\\' → single space"""

    CLEAN = re.compile(r"\s*\\{2}\s*")

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.CLEAN.sub(" ", line)
