from __future__ import annotations

import click

from doku_gpt.command.list_files_command import ListFilesCommand
from doku_gpt.command.list_folders_command import ListFoldersCommand


@click.group()
def cli() -> None:
    """DokuGPT CLI entrypoint."""
    pass


@cli.group(help="List commands")
def list_group() -> None:
    pass


list_group.add_command(ListFoldersCommand.execute, name="folders")
list_group.add_command(ListFilesCommand.execute, name="files")


def run() -> None:
    cli()


if __name__ == "__main__":
    run()
