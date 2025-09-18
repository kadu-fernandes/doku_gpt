from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from doku_gpt.command.abstract_finder_command import AbstractFinderCommand
from doku_gpt.sanitizer.root_page_sanitizer import RootPageSanitizer


class SanitizeNamespaceCommand(AbstractFinderCommand):
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
        finder = SanitizeNamespaceCommand._create_finder(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )

        files = finder.find_files(pattern)
        for file in files:
            sanitizer = RootPageSanitizer(file)
            was_sanitized = sanitizer.sanitize()
            if was_sanitized:
                Console.print(f"Sanitized: {file}")
