from __future__ import annotations

import shutil
from pathlib import Path

from slugify import slugify

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.compiler.namespace_compiler import NamespaceCompiler
from doku_gpt.finder.copier import Copier
from doku_gpt.finder.finder import Finder
from doku_gpt.sanitizer.doku.line.inline_markup_sanitizer import InlineMarkupSanitizer
from doku_gpt.sanitizer.doku.link_tag_sanitizer import LinkTagSanitizer


class DokuCompiler(AbstractRootFolder):
    COMPILE_DESTINATION = Path("/tmp/doku_gpt_prepare")

    def compile(self) -> None:
        copier = Copier(
            root_folder=self.root_folder,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )
        copier.copy(destination=self.COMPILE_DESTINATION)

        finder = Finder(
            root_folder=self.COMPILE_DESTINATION,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )
        top_level_folders = finder.find_folder_children(pattern="*", folder=self.COMPILE_DESTINATION)

        for folder in top_level_folders:
            slug = slugify(folder.name, separator="_", lowercase=True)
            gpt_file = Path(f"gpt_{slug}.txt")

            # Mantém a assinatura “oficial” do NamespaceCompiler que tens em uso
            namespace_compiler = NamespaceCompiler(
                namespace_folder=folder,
                gpt_file=gpt_file,
                title=folder.name,
                page="start",
                root_folder=self.COMPILE_DESTINATION,
                excluded_folders=self.excluded_folders,
                excluded_files=self.excluded_files,
            )
            namespace_compiler.compile()

        self._sanitize()
        self._final_cleanup()

    def _sanitize(self) -> None:
        finder = Finder(root_folder=self.COMPILE_DESTINATION)
        files = finder.find_file_children("*.txt")
        sanitizer = LinkTagSanitizer(self.COMPILE_DESTINATION)
        for file in files:
            adapter = PageAdapter(file)
            lines = adapter.lines
            sanitized_lines: list[str] = []
            for line in lines:
                sanitized_line = InlineMarkupSanitizer.sanitize(line)
                sanitized_lines.append(sanitized_line)
            adapter.lines = sanitized_lines
            adapter.content = sanitizer.sanitize(adapter.content)

    def _final_cleanup(self) -> None:
        root_path = self.COMPILE_DESTINATION.resolve()
        for child in root_path.iterdir():
            if child.is_file():
                if not (child.name.startswith("gpt_") and child.suffix == ".txt"):
                    try:
                        child.unlink()
                    except OSError:
                        # Se algum ficheiro estiver bloqueado, passa; na próxima corrida cai.
                        pass
                continue

            if child.is_dir():
                # Remove a pasta inteira com tudo lá dentro; só os gpt_*.txt ficam na raiz.
                try:
                    shutil.rmtree(child)
                except OSError:
                    # Se não conseguir remover por algum motivo do sistema, ignora silenciosamente.
                    pass
