from __future__ import annotations

import re


class WikipediaTitleNormalizer:
    _REGEX_WIKIPEDIA_001 = r"(\s*\- Wikipedia.*)$"
    _REGEX_WIKIPEDIA_002 = r"(\s*\– Wikipédia.*)$"

    @staticmethod
    def normalize(title: str) -> str:
        normalized_title = re.sub(WikipediaTitleNormalizer._REGEX_WIKIPEDIA_001, "", title)
        return re.sub(WikipediaTitleNormalizer._REGEX_WIKIPEDIA_002, "", normalized_title)
