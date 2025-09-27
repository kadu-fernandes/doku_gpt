from __future__ import annotations

from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.compiler.index_compiler import IndexCompiler
from doku_gpt.compiler.namespace_compiler import NamespaceCompiler
from doku_gpt.finder.copier import Copier
from doku_gpt.finder.finder import Finder
from doku_gpt.sanitizer.doku.line.inline_markup_sanitizer import InlineMarkupSanitizer
from doku_gpt.sanitizer.doku.link_tag_sanitizer import LinkTagSanitizer


class DokuCompiler(AbstractRootFolder):
    COMPILE_DESTINATION = Path("/tmp/doku_gpt_prepare")

    def compile(self) -> None:
        copier = Copier(
            root_folder=self.root_folder, excluded_folders=self.excluded_folders, excluded_files=self.excluded_files
        )
        copier.copy(destination=self.COMPILE_DESTINATION)

        indexer = IndexCompiler(
            root_folder=self.COMPILE_DESTINATION,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )
        index = indexer.compile()
        for item in index:
            namespace_compiler = NamespaceCompiler(
                namespace_folder=Path(item["folder"]),
                gpt_file=Path(item["file"]),
                title=str(item["title"]),
                page=str(item["page"]),
                root_folder=self.COMPILE_DESTINATION,
                excluded_folders=self.excluded_folders,
                excluded_files=self.excluded_files,
            )
            namespace_compiler.compile()
            self._sanitize()

    def _sanitize(self) -> None:
        finder = Finder(root_folder=self.COMPILE_DESTINATION)
        files = finder.find_file_children("*.txt")
        sanitizer = LinkTagSanitizer(self.root_folder)
        for file in files:
            adapter = PageAdapter(file)
            lines = adapter.lines
            sanitized_lines: list[str] = []
            for line in lines:
                sanitized_line = InlineMarkupSanitizer.sanitize(line)
                sanitized_lines.append(sanitized_line)
            adapter.lines = sanitized_lines
            adapter.content = sanitizer.sanitize(adapter.content)
