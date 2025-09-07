from __future__ import annotations

import enum


class LinkType(enum.Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    INTERWIKI = "interwiki"
