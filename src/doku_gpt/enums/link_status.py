from __future__ import annotations

import enum


class LinkStatus(enum.Enum):
    VALID = "valid"
    INVALID = "invalid"
    NOT_VALIDATED = "not_validated"
