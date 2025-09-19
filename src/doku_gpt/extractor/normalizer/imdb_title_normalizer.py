from __future__ import annotations

import re


class ImdbTitleNormalizer:
    _REGEX_IMDB_001 = r"\s*\(\d{4}\)\s*⭐.*$"
    _REGEX_IMDB_002 = r"\s*\(.*?\)\s*⭐.*$"

    @staticmethod
    def normalize(title: str) -> str:
        normalized_title = re.sub(ImdbTitleNormalizer._REGEX_IMDB_001, "", title)
        return re.sub(ImdbTitleNormalizer._REGEX_IMDB_002, "", normalized_title)
