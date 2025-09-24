from __future__ import annotations

from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.sanitizer.root.abstract_root_sanitizer import AbstractRootSanitizer
from doku_gpt.sanitizer.root.line_namespace_sanitizer import LineNamespaceSanitizer


class PageSanitizer(AbstractRootSanitizer):
    def sanitize(self) -> bool:
        adapter = PageAdapter(self.page_path)
        has_sanitized_lines = False
        sanitize_lines = []
        sanitizer: LineNamespaceSanitizer = LineNamespaceSanitizer(
            root_folder=self.root_folder, page_path=self.page_path
        )

        for line in adapter.lines:
            was_sanitized, sanitized = sanitizer.sanitize(line)
            if not has_sanitized_lines and was_sanitized:
                has_sanitized_lines = True
            sanitize_lines.append(sanitized)

        if has_sanitized_lines:
            adapter.lines = sanitize_lines
        return has_sanitized_lines
