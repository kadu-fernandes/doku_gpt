from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from doku_gpt.command.abstract_finder_command import AbstractFinderCommand


class ListFoldersCommand(AbstractFinderCommand):
    @staticmethod
    @click.command()
    @AbstractFinderCommand.common_options  # <-- usa aqui
    def execute(
        root_folder: Path,
        pattern: str,
        excluded_folders: tuple[str, ...],
        excluded_files: tuple[str, ...],  # fica disponível mesmo se não usares
    ) -> None:
        finder = ListFoldersCommand._create_finder(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )
        folders = finder.find_folders(pattern)

        table = Table()
        table.add_column("#", justify="right", style="cyan")
        table.add_column("Folder", style="green")

        for index, folder in enumerate(folders, start=1):
            table.add_row(str(index), str(folder))

        Console().print(table)
