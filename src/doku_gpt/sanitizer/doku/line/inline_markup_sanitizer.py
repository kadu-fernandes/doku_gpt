from __future__ import annotations

import re

from doku_gpt.sanitizer.doku.line.bold_sanitizer import BoldSanitizer
from doku_gpt.sanitizer.doku.line.box_sanitizer import BoxSanitizer
from doku_gpt.sanitizer.doku.line.deleted_sanitizer import DeletedSanitizer
from doku_gpt.sanitizer.doku.line.header_sanitizer import HeaderSanitizer
from doku_gpt.sanitizer.doku.line.italic_sanitizer import ItalicSanitizer
from doku_gpt.sanitizer.doku.line.media_sanitizer import MediaSanitizer
from doku_gpt.sanitizer.doku.line.monospace_sanitizer import MonospaceSanitizer
from doku_gpt.sanitizer.doku.line.plugin_sanitizer import PluginSanitizer
from doku_gpt.sanitizer.doku.line.subscript_sanitizer import SubscriptSanitizer
from doku_gpt.sanitizer.doku.line.superscript_sanitizer import SuperscriptSanitizer
from doku_gpt.sanitizer.doku.line.underline_sanitizer import UnderlineSanitizer


class InlineMarkupSanitizer:
    _PIPELINE = (
        BoldSanitizer,
        BoxSanitizer,
        DeletedSanitizer,
        HeaderSanitizer,
        ItalicSanitizer,
        MediaSanitizer,
        MonospaceSanitizer,
        PluginSanitizer,
        SubscriptSanitizer,
        SuperscriptSanitizer,
        UnderlineSanitizer,
    )

    @classmethod
    def sanitize(cls, line: str, normalize_space: bool = False) -> str:
        prev = None
        while prev != line:
            prev = line
            for s in cls._PIPELINE:
                line = s.sanitize(line)
        if normalize_space:
            line = re.sub(r"\s{2,}", " ", line).strip()
        return line
