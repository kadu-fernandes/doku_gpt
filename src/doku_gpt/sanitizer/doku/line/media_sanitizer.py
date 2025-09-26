from __future__ import annotations

import re


class MediaSanitizer:
    MEDIA = re.compile(r"\{\{\s*[^|}]+(?:\|([^}]*?))?\s*\}\}")

    @classmethod
    def sanitize(cls, line: str) -> str:
        def _repl(match: re.Match) -> str:
            caption = (match.group(1) or "").strip()
            return caption

        return cls.MEDIA.sub(_repl, line)
