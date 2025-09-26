from __future__ import annotations

from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.compiler.index_compiler import IndexCompiler
from doku_gpt.compiler.namespace_compiler import NamespaceCompiler
from doku_gpt.finder.copier import Copier


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
