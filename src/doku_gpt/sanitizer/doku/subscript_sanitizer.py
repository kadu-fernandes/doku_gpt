from __future__ import annotations

import re


class SubscriptSanitizer:
    CLEAN = re.compile(r"<sub\b[^>]*>(.*?)</sub>", re.IGNORECASE | re.DOTALL)

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.CLEAN.sub(r"\1", line)
