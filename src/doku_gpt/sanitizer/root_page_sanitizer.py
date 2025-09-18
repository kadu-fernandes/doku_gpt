from __future__ import annotations

from pathlib import Path

from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.sanitizer.line_namespace_sanitizer import LineNamespaceSanitizer
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.path_extension_validator import PathExtensionValidator


class RootPageSanitizer:
    def __init__(self, page_path: str | Path) -> None:
        page_path = FileValidator.validate(page_path)
        self.page_path = PathExtensionValidator.validate(page_path)

    def sanitize(self) -> bool:
        adapter = PageAdapter(self.page_path)
        has_sanitized_lines = False
        sanitize_lines = []
        for line in adapter.lines:
            was_sanitized, sanitized = LineNamespaceSanitizer.sanitize(line)
            if not has_sanitized_lines and was_sanitized:
                has_sanitized_lines = True
            sanitize_lines.append(sanitized)

        if has_sanitized_lines:
            adapter.lines = sanitize_lines
        return has_sanitized_lines
