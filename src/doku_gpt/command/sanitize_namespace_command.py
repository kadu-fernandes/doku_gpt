from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from doku_gpt.command.abstract_finder_command import AbstractFinderCommand
from doku_gpt.sanitizer.root.page_sanitizer import PageSanitizer


class SanitizeNamespaceCommand(AbstractFinderCommand):
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
        finder = SanitizeNamespaceCommand._create_finder(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )

        files = finder.find_files(pattern)
        for file in files:
            sanitizer = PageSanitizer(root_folder=root_folder, page_path=file)
            was_sanitized = sanitizer.sanitize()
            if was_sanitized and verbose:
                Console().print(f"Sanitized: {file}")
