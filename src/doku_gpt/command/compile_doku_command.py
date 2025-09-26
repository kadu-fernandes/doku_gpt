from __future__ import annotations

from pathlib import Path

import click

from doku_gpt.command.abstract_finder_command import AbstractFinderCommand
from doku_gpt.compiler.doku_compiler import DokuCompiler


class CompileDokuCommand(AbstractFinderCommand):
    @staticmethod
    @click.command()
    @AbstractFinderCommand.common_options
    def execute(
        root_folder: Path,
        excluded_folders: tuple[str, ...],
        excluded_files: tuple[str, ...],
        pattern: str = "*",
        verbose: bool = False,
    ) -> None:
        CompileDokuCommand.__copy(
            root_folder=root_folder, excluded_folders=excluded_folders, excluded_files=excluded_files
        )

    @staticmethod
    def __copy(
        root_folder: Path,
        excluded_folders: tuple[str, ...],
        excluded_files: tuple[str, ...],
    ) -> None:
        default_excluded_folders, default_excluded_files = AbstractFinderCommand._handle_excluded(
            excluded_folders=excluded_folders, excluded_files=excluded_files
        )

        compiler = DokuCompiler(
            root_folder=root_folder,
            excluded_folders=default_excluded_folders,
            excluded_files=default_excluded_files,
        )

        compiler.compile()
