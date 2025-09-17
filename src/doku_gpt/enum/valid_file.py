from __future__ import annotations

from doku_gpt.enum.abstract_enum import AbstractEnum


class ValidFile(AbstractEnum):
    DOKU_WIKI = "txt"
    MARKDOWN = "md"
    JSON = "json"
