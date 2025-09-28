from __future__ import annotations

import click

from doku_gpt.compiler.markdown_compiler import MarkdownCompiler


class CompileMarkdownCommand:
    @staticmethod
    @click.command()
    def execute() -> None:
        MarkdownCompiler().compile()
