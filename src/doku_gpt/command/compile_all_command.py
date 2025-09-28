from __future__ import annotations

import time
from pathlib import Path

import click
from rich.console import Console

from doku_gpt.command.abstract_finder_command import AbstractFinderCommand
from doku_gpt.compiler.doku_compiler import DokuCompiler
from doku_gpt.compiler.markdown_compiler import MarkdownCompiler
from doku_gpt.sanitizer.root.page_sanitizer import PageSanitizer


class CompileAllCommand(AbstractFinderCommand):
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
        console = Console()

        console.print(f"[bold]Sanitizing[/bold] {root_folder}")
        t0 = time.perf_counter()
        CompileAllCommand.__sanitize(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
            pattern=pattern,
            verbose=verbose,
            console=console,
        )
        console.print(f"[green]Sanitize phase took {time.perf_counter() - t0:.2f} seconds[/green]")

        console.print(f"[bold]Compiling Doku[/bold] {root_folder}")
        t1 = time.perf_counter()
        CompileAllCommand.__compile_doku(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )
        console.print(f"[green]Doku compile phase took {time.perf_counter() - t1:.2f} seconds[/green]")

        console.print(f"[bold]Compiling Markdown[/bold] {root_folder}")
        t2 = time.perf_counter()
        CompileAllCommand.__compile_markdown(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )
        console.print(f"[green]Markdown compile phase took {time.perf_counter() - t2:.2f} seconds[/green]")

        console.print(f"[bold]GPT files available in[/bold] {DokuCompiler.COMPILE_DESTINATION}")

    @staticmethod
    def __sanitize(
        root_folder: Path,
        excluded_folders: tuple[str, ...],
        excluded_files: tuple[str, ...],
        pattern: str,
        verbose: bool,
        console: Console,
    ) -> None:
        finder = CompileAllCommand._create_finder(
            root_folder=root_folder,
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )
        files = finder.find_files(pattern)
        for file_path in files:
            sanitizer = PageSanitizer(root_folder=root_folder, page_path=file_path)
            was_sanitized = sanitizer.sanitize()
            if was_sanitized and verbose:
                console.print(f"[blue]Sanitized:[/blue] {file_path}")

    @staticmethod
    def __compile_doku(
        root_folder: Path,
        excluded_folders: tuple[str, ...],
        excluded_files: tuple[str, ...],
    ) -> None:
        default_excluded_folders, default_excluded_files = AbstractFinderCommand._handle_excluded(
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )
        compiler = DokuCompiler(
            root_folder=root_folder,
            excluded_folders=default_excluded_folders,
            excluded_files=default_excluded_files,
        )
        compiler.compile()

    @staticmethod
    def __compile_markdown(
        root_folder: Path,
        excluded_folders: tuple[str, ...],
        excluded_files: tuple[str, ...],
    ) -> None:
        default_excluded_folders, default_excluded_files = AbstractFinderCommand._handle_excluded(
            excluded_folders=excluded_folders,
            excluded_files=excluded_files,
        )
        compiler = MarkdownCompiler()
        compiler.compile()
