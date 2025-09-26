from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from slugify import slugify

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.error.invalid_value_error import InvalidValueError
from doku_gpt.extractor.doku_page_extractor import DokuPageExtractor
from doku_gpt.finder.finder import Finder


class IndexCompiler(AbstractRootFolder):
    def compile(self) -> list[dict[str, str | Path]]:
        finder = Finder(
            root_folder=self.root_folder,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )
        root_path = Path(self.root_folder).resolve()
        folder_paths: list[Path] = finder.find_folders()

        children_by_parent = self.__index_children_by_parent(folder_paths=folder_paths, root_path=root_path)

        code_by_relative: dict[str, str] = {"": "00"}
        self.__assign_codes(
            parent_relative="", children_by_parent=children_by_parent, code_by_relative=code_by_relative
        )

        index_rows: list[dict[str, str | Path]] = []

        root_code = code_by_relative[""]
        index_rows.append(self.__build_row(folder=root_path, code=root_code))

        for absolute_path in folder_paths:
            relative_path = self.__relative_to_path(absolute_path=absolute_path, root_path=root_path)
            code = code_by_relative[relative_path]
            index_rows.append(self.__build_row(folder=absolute_path.resolve(), code=code))

        index_rows.sort(key=lambda row: self.__natural_key(str(row["index"])))
        return index_rows

    def __index_children_by_parent(self, folder_paths: list[Path], root_path: Path) -> dict[str, list[str]]:
        children_by_parent: dict[str, list[str]] = {}
        for absolute_path in folder_paths:
            relative_path = self.__relative_to_path(absolute_path=absolute_path, root_path=root_path)
            parent_relative = self.__index_parent_of(relative_path=relative_path)
            children_by_parent.setdefault(parent_relative, []).append(relative_path)
        return children_by_parent

    def __assign_codes(
        self,
        parent_relative: str,
        children_by_parent: dict[str, list[str]],
        code_by_relative: dict[str, str],
    ) -> None:
        children: list[str] = children_by_parent.get(parent_relative, [])
        sorted_children = sorted(children, key=lambda child: self.__natural_key(self.__base_name(child)))
        for position, child_relative in enumerate(sorted_children, start=1):
            if 100 == position:
                raise ValueError("A parent cannot have 100 or more direct children with a 2-digit index policy.")
            parent_code = code_by_relative[parent_relative]
            child_code = f"{parent_code}_{position:02d}"
            code_by_relative[child_relative] = child_code
            self.__assign_codes(
                parent_relative=child_relative,
                children_by_parent=children_by_parent,
                code_by_relative=code_by_relative,
            )

    def __relative_to_path(self, absolute_path: Path, root_path: Path) -> str:
        return PurePosixPath(absolute_path.resolve().relative_to(root_path).as_posix()).as_posix()

    def __index_parent_of(self, relative_path: str) -> str:
        relative_posix = PurePosixPath(relative_path)
        if 0 == len(relative_posix.parts) or 1 == len(relative_posix.parts):
            return ""
        return relative_posix.parent.as_posix()

    def __base_name(self, relative_path: str) -> str:
        return PurePosixPath(relative_path).name

    def __natural_key(self, text: str) -> list[int | str]:
        normalized = text.casefold()
        tokens = re.findall(r"\d+|[^\d]+", normalized)
        return [int(token) if token.isdigit() else token for token in tokens]

    def __build_row(self, folder: Path, code: str) -> dict[str, str | Path]:
        page, title = self.__fetch_title(folder)
        if page is None or title is None:
            raise InvalidValueError(f"Namespace '{folder}' has no page with a valid title.")
        slug = slugify(title, separator="_", lowercase=True)
        if 0 == len(slug.strip()):
            raise InvalidValueError(f"Namespace '{folder}' produced an empty slug from title '{title}'.")
        file_path = Path(f"gpt_{code}_{slug}").with_suffix(".txt")
        return {"folder": folder, "file": file_path, "page": page, "title": title, "index": code}

    def __fetch_title(self, folder: Path) -> tuple[str | None, str | None]:
        start_path = folder.joinpath("start.txt").resolve()
        if DokuPageExtractor.file_exists(start_path):
            title = DokuPageExtractor.extract_title(start_path)
            if title is not None:
                return "start", title

        finder = Finder(
            root_folder=self.root_folder,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )
        files = finder.find_file_children("*.txt", folder=folder)
        for file_path in files:
            title = DokuPageExtractor.extract_title(file_path)
            if title is not None:
                return file_path.with_suffix("").name, title

        raise InvalidValueError(f"Namespace '{folder}' has no .txt page with a title.")
