from __future__ import annotations

from pathlib import Path
from shutil import copy2, copytree, rmtree

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.helper.finder_helper import FinderHelper
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.folder_validator import FolderValidator
from doku_gpt.validator.path.not_child_validator import NotChildValidator
from doku_gpt.validator.path.not_hidden_validator import NotHiddenValidator


class FileSystemHelper:
    @staticmethod
    def simple_copy_folder(source: Path | str, destination: Path | str) -> None:
        source = FolderValidator.validate(source)

        try:
            destination = FolderValidator.validate(destination)
            rmtree(destination)
        except InvalidPathError:
            FolderValidator.validate(destination.parent)

        copytree(src=source, dst=destination)

    @staticmethod
    def copy_file(source: Path | str, destination: Path | str, extension: str | None = None) -> None:
        source = FileValidator.validate(source)
        copy_to = destination
        if extension is not None:
            copy_to = destination.with_suffix(extension)

        try:
            copy_to = FileValidator.validate(copy_to)
            copy_to.unlink()
        except InvalidPathError:
            pass

        copy2(src=source, dst=copy_to)

    @staticmethod
    def copy_folder(
        source: Path | str,
        destination: Path | str,
        file_pattern: str = "*",
        excluded_folders: list[str] | None = None,
        excluded_files: list[str] | None = None,
    ) -> None:
        source_path = FolderValidator.validate(source)
        destination_path = Path(destination)

        FileSystemHelper.__ensure_destination_parent(destination_path)
        NotChildValidator.validate(parent=source_path, other=destination_path)

        try:
            existing_destination = FolderValidator.validate(destination_path)
            rmtree(existing_destination)
        except InvalidPathError:
            pass

        excluded_folders = [] if excluded_folders is None else excluded_folders
        excluded_files = [] if excluded_files is None else excluded_files

        allowed_subfolders = FinderHelper.find_folders(
            folder=source_path,
            pattern="*",
            excluded_folders=excluded_folders,
        )

        folders_to_create: list[Path] = [source_path, *allowed_subfolders]

        for folder_path in folders_to_create:
            relative_path = folder_path.relative_to(source_path)
            target_folder = destination_path.joinpath(relative_path)
            target_folder.mkdir(parents=True, exist_ok=True)

            NotHiddenValidator.validate(folder_path)

            files_in_folder = FinderHelper.find_file_children(
                folder=folder_path,
                pattern=file_pattern,
                excluded_files=excluded_files,
            )

            for file_path in files_in_folder:
                valid_file = FileValidator.validate(file_path)
                NotHiddenValidator.validate(valid_file)

                relative_file_parent = valid_file.parent.relative_to(source_path)
                destination_file = destination_path.joinpath(relative_file_parent, valid_file.name)

                copy2(src=valid_file, dst=destination_file)

    @staticmethod
    def __ensure_destination_parent(destination_path: Path) -> None:
        parent = destination_path.parent
        FolderValidator.validate(parent)
