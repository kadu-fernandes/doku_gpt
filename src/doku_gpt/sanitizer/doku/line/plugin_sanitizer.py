from __future__ import annotations

import re


class PluginSanitizer:
    PLUGIN = re.compile(r"~~[A-Z][A-Z0-9_]*(?:>[^~]+)?~~")

    @classmethod
    def sanitize(cls, line: str) -> str:
        return cls.PLUGIN.sub("", line)
