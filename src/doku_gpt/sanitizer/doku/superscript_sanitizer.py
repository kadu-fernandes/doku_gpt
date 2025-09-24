from __future__ import annotations

import re


class SuperscriptSanitizer:
    CLEAN = re.compile(r"<sup\b[^>]*>(.*?)</sup>", re.IGNORECASE | re.DOTALL)

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.CLEAN.sub(r"\1", line)
