from __future__ import annotations

import re


class ImageSanitizer:
    CLEAN = re.compile(
        r"""
        \{\{
        \s*
        (?:https?://[^\|\}\s]+|:?[^|\}\s]+?)
        \.(?:png|jpe?g|gif|webp|svg)
        (?:\?[^\|\}]*)?
        \s*
        (?:\|[^\}]*)?
        \s*
        \}\}
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    @classmethod
    def sanitize(cls, line: str) -> str:
        replaced = cls.CLEAN.sub(" ", line)
        return re.sub(r"\s{2,}", " ", replaced).strip()
