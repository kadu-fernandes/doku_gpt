from __future__ import annotations

import re


class LinkLabelSanitizer:
    CLEAN = re.compile(
        r"""
        \[\[
        \s*
        (?P<target>[^|\]]+?(?:\#[^|\]]+)?)
        \s*
        (?:\|
            \s*(?P<label>[^\]]*?)
        )?
        \s*
        \]\]
        """,
        re.VERBOSE,
    )

    @classmethod
    def sanitize(cls, line: str) -> str:
        def repl(match: re.Match) -> str:
            label = match.group("label")
            if label is not None and label.strip() != "":
                return label.strip()
            return ""

        result = cls.CLEAN.sub(repl, line)
        result = re.sub(r"\s{2,}", " ", result).strip()
        return result
