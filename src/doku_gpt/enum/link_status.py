from __future__ import annotations

from doku_gpt.enum.abstract_enum import AbstractEnum


class LinkStatus(AbstractEnum):
    VALID = "valid"
    INVALID = "invalid"
    NOT_VALIDATED = "not_validated"
