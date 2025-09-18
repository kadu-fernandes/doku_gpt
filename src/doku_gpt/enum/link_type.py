from __future__ import annotations

from doku_gpt.enum.abstract_enum import AbstractEnum


class LinkType(AbstractEnum):
    EXTERNAL = "external"
    INTERNAL = "internal"
    INTERNAL_ABSOLUTE = "absolute"
    INTERNAL_PRIOR = "prior"
    INTERNAL_RELATIVE = "relative"
    INTERWIKI = "interwiki"
