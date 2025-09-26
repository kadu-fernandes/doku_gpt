from __future__ import annotations

import re


class BoldSanitizer:
    CLEAN = re.compile(r"(?<!\*)\*\*((?:[^*]|\*(?!\*))+)\*\*(?!\*)")

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.CLEAN.sub(r"\1", line)
