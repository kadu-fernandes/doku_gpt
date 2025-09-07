from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.folder_validator import FolderValidator
from doku_gpt.validator.path.not_hidden_validator import NotHiddenValidator


class FinderHelper:

    @staticmethod
    def find_folder_children(
        folder: str | Path,
        pattern: str = "*",
        excluded_folders: list[str] | None = None,
    ) -> list[Path]:
        folder = FolderValidator.validate(folder)
        excluded_folders = FinderHelper.__initialize_excluded_folders(excluded_folders)

        children: list[Path] = []
        for entry_name in os.listdir(folder):
            full_path = Path(folder).joinpath(entry_name)

            try:
                full_path = FolderValidator.validate(full_path)
                NotHiddenValidator.validate(full_path)
            except InvalidPathError:
                continue

            if FinderHelper.__is_excluded_folder(path=full_path, excluded_folders=excluded_folders):
                continue

            if not FinderHelper.__match_pattern_folder(full_path, pattern):
                continue

            children.append(full_path)

        return sorted(children)

    @staticmethod
    def find_folders(folder: str | Path, pattern: str = "*", excluded_folders: list[str] | None = None) -> list[Path]:
        folder = FolderValidator.validate(folder)
        excluded_folders = FinderHelper.__initialize_excluded_folders(excluded_folders)

        folders_to_return: list[Path] = []

        for found_folder, found_folder_names, _ in os.walk(top=folder, followlinks=False):
            base_folder = Path(found_folder)

            pruned_folder_names: list[str] = []
            for folder_name in found_folder_names:
                full_path = base_folder.joinpath(folder_name)

                try:
                    full_path = FolderValidator.validate(full_path)
                    NotHiddenValidator.validate(full_path)
                except InvalidPathError:
                    continue

                if FinderHelper.__is_excluded_folder(path=full_path, excluded_folders=excluded_folders):
                    continue

                pruned_folder_names.append(folder_name)

                if FinderHelper.__match_pattern_folder(full_path, pattern):
                    folders_to_return.append(full_path)

            found_folder_names[:] = pruned_folder_names

        return sorted(folders_to_return)

    @staticmethod
    def find_file_children(
        folder: str | Path,
        pattern: str = "*",
        excluded_files: list[str] | None = None,
    ) -> list[Path]:
        folder = FolderValidator.validate(folder)
        excluded_files = FinderHelper.__initialize_excluded_files(excluded_files)

        children: list[Path] = []
        for entry_name in os.listdir(folder):
            full_path = Path(folder).joinpath(entry_name)

            try:
                full_path = FileValidator.validate(full_path)
                NotHiddenValidator.validate(full_path)
            except InvalidPathError:
                continue

            if FinderHelper.__is_excluded_file(path=full_path, excluded_files=excluded_files):
                continue

            if not FinderHelper.__match_pattern_file(full_path, pattern):
                continue

            children.append(full_path)

        return sorted(children)

    @staticmethod
    def find_files(
        folder: str | Path,
        pattern: str = "*",
        excluded_folders: list[str] | None = None,
        excluded_files: list[str] | None = None,
    ) -> list[Path]:
        folder = FolderValidator.validate(folder)
        excluded_folders = FinderHelper.__initialize_excluded_folders(excluded_folders)
        excluded_files = FinderHelper.__initialize_excluded_files(excluded_files)

        files_to_return: list[Path] = []

        files_to_return.extend(
            FinderHelper.find_file_children(folder=folder, pattern=pattern, excluded_files=excluded_files)
        )

        for subfolder in FinderHelper.find_folders(folder=folder, pattern="*", excluded_folders=excluded_folders):
            files_to_return.extend(
                FinderHelper.find_file_children(folder=subfolder, pattern=pattern, excluded_files=excluded_files)
            )

        return sorted(files_to_return)

    @staticmethod
    def __fetch_folder(path: str | Path) -> Path:
        try:
            return FolderValidator.validate(path)
        except InvalidPathError:
            path = FileValidator.validate(path)
            return path.parent

    @staticmethod
    def __match_pattern_folder(path: str | Path, pattern: str = "*") -> bool:
        path = FinderHelper.__fetch_folder(path=path)
        pattern = (pattern or "*").strip()
        return fnmatch.fnmatch(path.name, pattern)

    @staticmethod
    def __match_pattern_file(path: str | Path, pattern: str = "*") -> bool:
        try:
            path = FileValidator.validate(path)
        except InvalidPathError:
            return False
        return fnmatch.fnmatch(path.name, (pattern or "*").strip())

    @staticmethod
    def __is_excluded_folder(path: str | Path, excluded_folders: list[str] | None = None) -> bool:
        path = FinderHelper.__fetch_folder(path=path)
        excluded_folders = FinderHelper.__initialize_excluded_folders(excluded_folders)
        return path.name in excluded_folders

    @staticmethod
    def __is_excluded_file(path: str | Path, excluded_files: list[str] | None = None) -> bool:
        excluded_files = FinderHelper.__initialize_excluded_files(excluded_files)
        try:
            path = FileValidator.validate(path)
        except InvalidPathError:
            return False
        return path.stem in excluded_files

    @staticmethod
    def __initialize_excluded_folders(excluded_folders: list[str] | None = None) -> list[str]:
        return [] if excluded_folders is None else excluded_folders

    @staticmethod
    def __initialize_excluded_files(excluded_files: list[str] | None = None) -> list[str]:
        return [] if excluded_files is None else excluded_files
