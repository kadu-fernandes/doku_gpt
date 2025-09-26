from __future__ import annotations

import re


class HeaderSanitizer:
    HEADER = re.compile(r"^(?P<open>=+)\s*(?P<text>.*?)\s*(?P<close>=+)\s*$")

    EMOJI = re.compile(r"[\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001FAFF]+")

    @classmethod
    def sanitize(cls, line: str) -> str:
        match = cls.HEADER.match(line)
        if not match:
            return line

        text = match.group("text")
        text = cls.EMOJI.sub("", text)
        text = re.sub(r"\s+", " ", text).strip()

        return f"{match.group('open')} {text} {match.group('close')}"
