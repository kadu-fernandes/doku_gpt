from __future__ import annotations

import enum


class NamespaceType(enum.Enum):
    ABSOLUTE = "explicit_absolute"
    ABSOLUTE_IMPLICIT = "implicit_absolute"
    INVALID = "invalid"
    PRIOR = "prior"
    RELATIVE = "explicit_relative"
    RELATIVE_IMPLICIT = "implicit_relative"
