from __future__ import annotations

from pathlib import Path

import click

from doku_gpt.finder.finder import Finder


class AbstractFinderCommand:
    @staticmethod
    def common_options(func):
        func = click.argument(
            "root_folder",
            type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
            metavar="ROOT_FOLDER",
        )(func)

        func = click.option(
            "-p",
            "--pattern",
            default="*",
            type=str,
            show_default=True,
            help="Pattern to filter the files (ex: '*.txt').",
        )(func)

        func = click.option(
            "-v",
            "--verbose",
            is_flag=True,
            default=False,
            show_default=True,
            help="Shows output.",
        )(func)

        func = click.option(
            "-o",
            "--excluded-folder",
            "excluded_folders",
            multiple=True,
            help="Exclude folders by name (use multiple times for more).",
        )(func)

        func = click.option(
            "-i",
            "--excluded-file",
            "excluded_files",
            multiple=True,
            help="Exclude files by name (use multiple times for more).",
        )(func)
        return func

    @staticmethod
    def _create_finder(root_folder: Path, excluded_folders: tuple[str, ...], excluded_files: tuple[str, ...]) -> Finder:
        default_excluded_folders, default_excluded_files = AbstractFinderCommand._handle_excluded(
            excluded_folders=excluded_folders, excluded_files=excluded_files
        )

        return Finder(
            root_folder=root_folder, excluded_folders=default_excluded_folders, excluded_files=default_excluded_files
        )

    @staticmethod
    def _handle_excluded(
        excluded_folders: tuple[str, ...], excluded_files: tuple[str, ...]
    ) -> tuple[list[str], list[str]]:
        default_excluded_folders: list[str] = ["playground", "wiki", "old_content"]
        default_excluded_folders.extend(excluded_folders)
        default_excluded_folders = sorted(default_excluded_folders)

        default_excluded_files: list[str] = ["sidebar"]
        default_excluded_files.extend(excluded_files)
        default_excluded_files = sorted(default_excluded_files)

        return default_excluded_folders, default_excluded_files
