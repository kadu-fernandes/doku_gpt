from __future__ import annotations

import os
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.file_matches_pattern_validator import FileMatchesPatternValidator
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.folder_matches_pattern_validator import FolderMatchesPatternValidator
from doku_gpt.validator.path.folder_validator import FolderValidator
from doku_gpt.validator.path.path_is_excluded_file_validator import PathIsExcludedFileValidator
from doku_gpt.validator.path.path_is_excluded_folder_validator import PathIsExcludedFolderValidator
from doku_gpt.validator.path.path_is_not_hidden_validator import PathIsNotHiddenValidator


class Finder(AbstractRootFolder):
    def find_folder_children(self, pattern: str = "*", folder: str | Path | None = None) -> list[Path]:
        base_folder = self.root_folder if folder is None else FolderValidator.validate(folder)

        children: list[Path] = []
        for entry_name in os.listdir(base_folder):
            full_path = Path(base_folder).joinpath(entry_name)

            try:
                full_path = FolderValidator.validate(full_path)
                full_path = PathIsNotHiddenValidator.validate(full_path)
                full_path = PathIsExcludedFolderValidator.validate(
                    folder=full_path, excluded_folders=self.excluded_folders, root_folder=self.root_folder
                )
                full_path = FolderMatchesPatternValidator.validate(folder=full_path, pattern=pattern)
            except InvalidPathError:
                continue

            children.append(full_path)

        return sorted(children)

    def find_folders(self, pattern: str = "*", folder=None) -> list[Path]:
        base_folder = self.root_folder if folder is None else FolderValidator.validate(folder)

        folders_to_return: list[Path] = []

        for found_folder, found_folder_names, _ in os.walk(top=base_folder, followlinks=False):
            base_path = Path(found_folder)

            pruned_folder_names: list[str] = []
            for folder_name in found_folder_names:
                full_path = base_path.joinpath(folder_name)

                try:
                    full_path = FolderValidator.validate(full_path)
                    full_path = PathIsNotHiddenValidator.validate(full_path)
                    full_path = PathIsExcludedFolderValidator.validate(
                        folder=full_path,
                        excluded_folders=self.excluded_folders,
                        root_folder=self.root_folder,
                    )
                    full_path = FolderMatchesPatternValidator.validate(folder=full_path, pattern=pattern)
                except InvalidPathError:
                    continue

                pruned_folder_names.append(folder_name)
                folders_to_return.append(full_path)

            found_folder_names[:] = pruned_folder_names

        return sorted(folders_to_return)

    def find_file_children(self, pattern: str = "*", folder: str | Path | None = None) -> list[Path]:
        base_folder = self.root_folder if folder is None else FolderValidator.validate(folder)

        children: list[Path] = []
        for entry_name in os.listdir(base_folder):
            full_path = Path(base_folder).joinpath(entry_name)

            try:
                full_path = FileValidator.validate(full_path)
                full_path = PathIsNotHiddenValidator.validate(full_path)
                PathIsExcludedFolderValidator.validate(
                    folder=full_path.parent, excluded_folders=self.excluded_folders, root_folder=self.root_folder
                )
                full_path = PathIsExcludedFileValidator.validate(file=full_path, excluded_files=self.excluded_files)
                full_path = FileMatchesPatternValidator.validate(file=full_path, pattern=pattern)
            except InvalidPathError:
                continue

            children.append(full_path)

        return sorted(children)

    def find_files(self, pattern: str = "*") -> list[Path]:
        base_folder = self.root_folder

        files_to_return: list[Path] = []

        files_to_return.extend(self.find_file_children(pattern=pattern, folder=base_folder))

        for subfolder in self.find_folders(pattern="*", folder=base_folder):
            files_to_return.extend(self.find_file_children(pattern=pattern, folder=subfolder))

        return sorted(files_to_return)
