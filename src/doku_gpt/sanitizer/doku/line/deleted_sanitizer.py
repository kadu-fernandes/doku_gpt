from __future__ import annotations

import re


class DeletedSanitizer:
    CLEAN = re.compile(r"<del\b[^>]*>(.*?)</del>", re.IGNORECASE | re.DOTALL)

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.CLEAN.sub(r"\1", line)
