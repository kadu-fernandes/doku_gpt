from __future__ import annotations

import re


class MonospaceSanitizer:
    CLEAN = re.compile(r"(?<!')''((?:[^']|'(?!'))+)''(?!')", re.DOTALL)

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.CLEAN.sub(r"\1", line)
