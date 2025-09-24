from __future__ import annotations

import re

from doku_gpt.sanitizer.doku.bold_sanitizer import BoldSanitizer
from doku_gpt.sanitizer.doku.deleted_sanitizer import DeletedSanitizer
from doku_gpt.sanitizer.doku.italic_sanitizer import ItalicSanitizer
from doku_gpt.sanitizer.doku.monospace_sanitizer import MonospaceSanitizer
from doku_gpt.sanitizer.doku.subscript_sanitizer import SubscriptSanitizer
from doku_gpt.sanitizer.doku.superscript_sanitizer import SuperscriptSanitizer
from doku_gpt.sanitizer.doku.underline_sanitizer import UnderlineSanitizer


class InlineMarkupSanitizer:
    _PIPELINE = (
        BoldSanitizer,
        ItalicSanitizer,
        MonospaceSanitizer,
        UnderlineSanitizer,
        SubscriptSanitizer,
        SuperscriptSanitizer,
        DeletedSanitizer,
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
