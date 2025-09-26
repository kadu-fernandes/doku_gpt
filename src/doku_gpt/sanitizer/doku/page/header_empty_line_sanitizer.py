from __future__ import annotations

import re


class HeaderEmptyLineSanitizer:
    HEADER = re.compile(r"^\s*(?P<eq>=+)\s*(?P<txt>.*?)\s*(?P=eq)\s*$")

    @classmethod
    def sanitize(cls, page: str) -> str:
        content = cls.__strip_blank_edges(page)
        lines = content.split("\n")
        normalized: list[str] = []
        i = 0
        total = len(lines)

        while i < total:
            line = lines[i]

            if cls.HEADER.match(line):
                while normalized and normalized[-1].strip() == "":
                    normalized.pop()
                normalized.append("")
                normalized.append(line.rstrip())

                i += 1
                while i < total and lines[i].strip() == "":
                    i += 1
                normalized.append("")
                continue

            normalized.append(line)
            i += 1

        result = "\n".join(normalized)

        result = re.sub(
            r"^(?P<header>=+\s*.*?\s*=+)\n(?=[^\n])",
            r"\g<header>\n\n",
            result,
            count=1,
            flags=0,
        )

        result = cls.__strip_blank_edges(page=result)

        return result

    @classmethod
    def __strip_blank_edges(cls, page: str, keep_final_newline: bool = True) -> str:
        lines = page.splitlines(keepends=True)
        while lines and lines[0].strip() == "":
            lines.pop(0)
        while lines and lines[-1].strip() == "":
            lines.pop()
        result = "".join(lines)
        if keep_final_newline and result and not result.endswith("\n"):
            result += "\n"
        return result
