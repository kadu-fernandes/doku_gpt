from __future__ import annotations

import re
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.error.invalid_value_error import InvalidValueError
from doku_gpt.finder.finder import Finder


class NamespaceCompiler(AbstractRootFolder):
    def __init__(
        self,
        namespace_folder: Path,
        gpt_file: Path,
        title: str,
        page: str,
        root_folder: str | Path,
        excluded_folders: list[str] | None = None,
        excluded_files: list[str] | None = None,
    ):
        super().__init__(root_folder=root_folder, excluded_folders=excluded_folders, excluded_files=excluded_files)
        self.namespace_folder = namespace_folder.resolve()
        self.gpt_file = self.root_folder.joinpath(gpt_file)
        self.title = title
        self.page = page

    def compile(self) -> None:
        """
        Create the consolidated GPT file for this namespace:
        - First write the main page content (self.page) as-is.
        - Then append all other .txt files in the namespace (siblings only), separated by one blank line.
        - For non-main pages, demote every DokuWiki header by one level; if a header becomes a single '=', strip the '=' and keep plain text.
        """
        if 0 == len(self.page.strip()) or 0 == len(self.title.strip()):
            raise InvalidValueError("Namespace must provide non-empty 'page' and 'title'.")

        main_file_path = self.namespace_folder.joinpath(f"{self.page}.txt").resolve()
        if not main_file_path.is_file():
            raise InvalidValueError(f"Main page '{main_file_path}' does not exist.")

        finder = Finder(
            root_folder=self.root_folder,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )

        namespace_files = finder.find_file_children("*.txt", folder=self.namespace_folder)
        if 0 == len(namespace_files):
            raise InvalidValueError(f"Namespace '{self.namespace_folder}' has no .txt files.")

        try:
            main_file_resolved = next(p.resolve() for p in namespace_files if p.resolve() == main_file_path)
        except StopIteration:
            raise InvalidValueError(
                f"Main page '{main_file_path}' was not found among namespace files for '{self.namespace_folder}'."
            )

        output_resolved = self.gpt_file.resolve()
        other_files: list[Path] = []
        for file_path in namespace_files:
            file_resolved = file_path.resolve()
            if file_resolved == main_file_resolved:
                continue
            if file_resolved == output_resolved:
                continue
            other_files.append(file_path)

        other_files.sort(key=lambda p: self.__natural_key(p.name))

        parts: list[str] = []
        parts.append(self.__read_text(main_file_resolved))
        for file_path in other_files:
            raw = self.__read_text(file_path.resolve())
            demoted = self.__demote_headers(raw)
            parts.append(demoted)

        self.gpt_file.parent.mkdir(parents=True, exist_ok=True)
        content = ("\n\n").join(s.rstrip("\n") for s in parts) + "\n"
        self.gpt_file.write_text(content, encoding="utf-8")

    def __read_text(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")

    def __demote_headers(self, text: str) -> str:
        """
        Demote DokuWiki headers by one level.
        - '====== Title ======' -> '===== Title ====='
        - '=== Title ===' -> '== Title =='
        - '== Title ==' -> '= Title =' -> becomes 'Title' (strip '=' entirely)
        Keeps non-header lines unchanged.
        """
        pattern = re.compile(
            r"^(?P<prefix>\s*)(?P<eq>=+)\s*(?P<txt>.*?)\s*(?P=eq)(?P<suffix>\s*)$",
            re.MULTILINE,
        )

        def repl(match: re.Match[str]) -> str:
            equals = match.group("eq")
            inner = match.group("txt").strip()
            if 0 == len(inner):
                return ""
            if 1 == len(equals):
                return f"{match.group('prefix')}{inner}{match.group('suffix')}"
            new_eq = equals[:-1]  # demote by one
            return f"{match.group('prefix')}{new_eq} {inner} {new_eq}{match.group('suffix')}"

        return pattern.sub(repl, text)

    def __natural_key(self, text: str) -> list[int | str]:
        normalized = text.casefold()
        tokens = re.findall(r"\d+|[^\d]+", normalized)
        return [int(tok) if tok.isdigit() else tok for tok in tokens]
