from __future__ import annotations

import re


class UnderlineSanitizer:
    CLEAN = re.compile(r"(?<!_)__((?:[^_]|_(?!_))+)__(?!_)", re.DOTALL)

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.CLEAN.sub(r"\1", line)
