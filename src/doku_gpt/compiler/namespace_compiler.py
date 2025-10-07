from __future__ import annotations

import re
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.error.invalid_value_error import InvalidValueError
from doku_gpt.finder.finder import Finder
from doku_gpt.sanitizer.doku.header_sanitizer import HeaderSanitizer


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
        Build one consolidated GPT file for the current top-level namespace:
        - Collect all .txt files recursively under this namespace folder.
        - For each file, rebuild the header using HeaderSanitizer.
        - Concatenate everything in natural order, separated by blank lines.
        """
        if 0 == len(self.page.strip()) or 0 == len(self.title.strip()):
            raise InvalidValueError("Namespace must provide non-empty 'page' and 'title'.")

        finder = Finder(
            root_folder=self.root_folder,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )

        namespace_files = finder.find_files("*.txt")
        namespace_files = [f for f in namespace_files if f.is_relative_to(self.namespace_folder)]

        if 0 == len(namespace_files):
            raise InvalidValueError(f"Namespace '{self.namespace_folder}' has no .txt files.")

        namespace_files.sort(key=lambda p: self.__natural_key(str(p.relative_to(self.namespace_folder))))

        sanitizer = HeaderSanitizer()
        parts: list[str] = []

        for file_path in namespace_files:
            raw_text = self.__read_text(file_path)
            lines = raw_text.splitlines()
            if 0 == len(lines):
                continue

            new_header = sanitizer.sanitize(self.root_folder, file_path)
            lines[0] = new_header
            parts.append("\n".join(lines).rstrip("\n"))

        self.gpt_file.parent.mkdir(parents=True, exist_ok=True)
        content = ("\n\n").join(parts) + "\n"
        self.gpt_file.write_text(content, encoding="utf-8")

        self.__cleanup_namespace_artifacts()

    def __cleanup_namespace_artifacts(self) -> None:
        """
        Remove non-gpt files directly under the current namespace folder.
        Keep only files named 'gpt_*.txt' and prune empty folders upwards.
        """
        for child in list(self.namespace_folder.iterdir()):
            if child.is_file():
                if not self.__is_gpt_output_file(child):
                    child.unlink(missing_ok=True)
                continue
            if child.is_dir():
                self.__remove_dir_if_empty(child)

        self.__remove_dir_if_empty(self.namespace_folder)

        current = self.namespace_folder.parent
        while current != self.root_folder and current.is_dir():
            if self.__dir_is_empty(current):
                try:
                    current.rmdir()
                except OSError:
                    break
                current = current.parent
                continue
            break

    def __is_gpt_output_file(self, file_path: Path) -> bool:
        return file_path.is_file() and file_path.name.startswith("gpt_") and file_path.suffix == ".txt"

    def __dir_is_empty(self, folder: Path) -> bool:
        try:
            next(folder.iterdir())
            return False
        except StopIteration:
            return True

    def __remove_dir_if_empty(self, folder: Path) -> None:
        if self.__dir_is_empty(folder):
            try:
                if folder.resolve() != self.root_folder.resolve():
                    folder.rmdir()
            except OSError:
                pass

    def __read_text(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")

    def __natural_key(self, text: str) -> list[int | str]:
        normalized = text.casefold()
        tokens = re.findall(r"\d+|[^\d]+", normalized)
        return [int(tok) if tok.isdigit() else tok for tok in tokens]
