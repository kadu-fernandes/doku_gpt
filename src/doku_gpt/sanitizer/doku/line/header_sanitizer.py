from __future__ import annotations

import re
import unicodedata


class HeaderSanitizer:
    HEADER = re.compile(r"^(?P<open>=+)\s*(?P<text>.*?)\s*(?P<close>=+)\s*$")
    EMOJI = re.compile(r"[\u2600-\u26FF\u2700-\u27BF\U0001F000-\U0001FAFF]+")
    INVISIBLE = re.compile(r"[\u200B-\u200D\u2060\uFE0E\uFE0F\u00AD\u180E\uFEFF]")
    WSP = re.compile(r"[\u00A0\u1680\u2000-\u200A\u202F\u205F\u3000]")

    @classmethod
    def sanitize(cls, line: str) -> str:
        match = cls.HEADER.match(line)
        if not match:
            return line

        text = match.group("text")
        text = unicodedata.normalize("NFKC", text)
        text = cls.INVISIBLE.sub("", text)
        text = cls.WSP.sub(" ", text)
        text = cls.EMOJI.sub("", text)
        text = re.sub(r"\s+", " ", text).strip()

        if text == "":
            return line

        return f"{match.group('open')} {text} {match.group('close')}"
