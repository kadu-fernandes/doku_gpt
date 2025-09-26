from __future__ import annotations

from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder


class namespace_compiler(AbstractRootFolder):
    def __init__(
        self,
        namespace_folder: Path,
        index: str,
        root_folder: str | Path,
        excluded_folders: list[str] | None = None,
        excluded_files: list[str] | None = None,
    ):
        super().__init__(root_folder=root_folder, excluded_folders=excluded_folders, excluded_files=excluded_files)
        self.namespace_folder: Path = namespace_folder
        self.index: str = index

    def compile(self):
        pass
