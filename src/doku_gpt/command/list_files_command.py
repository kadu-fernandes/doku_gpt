from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from doku_gpt.command.abstract_finder_command import AbstractFinderCommand


class ListFilesCommand(AbstractFinderCommand):
    @staticmethod
    @click.command()
    @click.argument(
        "root_folder",
        type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    )
    @click.option(
        "-p",
        "--pattern",
        type=str,
        default="*",
        help="Pattern to filter the files (ex: '*.txt'). The default is '*'.",
    )
    @click.option(
        "-o",
        "--excluded-folders",
        "excluded_folders",
        multiple=True,
        help="the name of a folder part you want to exclude (use more than once if you need multiple folders).",
    )
    @click.option(
        "-i",
        "--excluded-files",
        "excluded_files",
        multiple=True,
        help="the name of a files part you want to exclude (use more than once if you need multiple folders).",
    )
    @staticmethod
    def execute(
        root_folder: Path,
        excluded_folders: tuple[str, ...],
        excluded_files: tuple[str, ...],
        pattern: str = "*",
    ) -> None:
        finder = ListFilesCommand._create_finder(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )

        files = finder.find_files(pattern)

        table = Table()
        table.add_column("#", justify="right", style="cyan")
        table.add_column("File", style="green")

        for index, folder in enumerate(files, start=1):
            table.add_row(str(index), str(folder))

        Console().print(table)
