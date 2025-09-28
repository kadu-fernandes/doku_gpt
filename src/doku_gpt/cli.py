from __future__ import annotations

import click

from doku_gpt.command.compile_all_command import CompileAllCommand
from doku_gpt.command.compile_doku_command import CompileDokuCommand
from doku_gpt.command.compile_markdown_command import CompileMarkdownCommand
from doku_gpt.command.create_settings_command import CreateSettingsCommand
from doku_gpt.command.list_files_command import ListFilesCommand
from doku_gpt.command.list_folders_command import ListFoldersCommand
from doku_gpt.command.sanitize_namespace_command import SanitizeNamespaceCommand
from doku_gpt.command.update_settings_command import UpdateSettingsCommand


@click.group()
def cli() -> None:
    """DokuGPT CLI entrypoint."""
    pass


@cli.group(help="List commands")
def list_group() -> None:
    pass


@cli.group(help="Sanitize commands")
def sanitize_group() -> None:
    pass


@cli.group(help="Settings commands")
def settings_group() -> None:
    pass


@cli.group(help="Compile commands")
def compile_group() -> None:
    pass


list_group.add_command(ListFoldersCommand.execute, name="folders")
list_group.add_command(ListFilesCommand.execute, name="files")

sanitize_group.add_command(SanitizeNamespaceCommand.execute, name="files")

settings_group.add_command(CreateSettingsCommand.execute, name="create")
settings_group.add_command(UpdateSettingsCommand.execute, name="update")

compile_group.add_command(CompileDokuCommand.execute, name="doku")
compile_group.add_command(CompileMarkdownCommand.execute, name="markdown")
compile_group.add_command(CompileAllCommand.execute, name="all")


def run() -> None:
    cli()


if __name__ == "__main__":
    run()
