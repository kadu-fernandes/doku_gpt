from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.file_or_parent_validator import FileOrParentValidator
from doku_gpt.validator.path.path_extension_validator import PathExtensionValidator


class PageAdapter:
    def __init__(self, page_path: str | Path) -> None:
        page_path = FileOrParentValidator.validate(page_path)
        self.page_path = PathExtensionValidator.validate(page_path)

    @property
    def content(self) -> str:
        return self.page_path.read_text(encoding="utf-8")

    @content.setter
    def content(self, content: str) -> None:
        self.page_path.write_text(data=content, encoding="utf-8")

    @property
    def lines(self) -> list[str]:
        lines = self.content.splitlines()
        while lines and lines[-1] == "":
            lines.pop()
        return lines

    @lines.setter
    def lines(self, lines: list[str]) -> None:
        text = "\n".join(lines) + "\n"
        self.page_path.write_text(text, encoding="utf-8")
