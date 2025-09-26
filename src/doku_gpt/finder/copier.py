from __future__ import annotations

import shutil
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.finder.finder import Finder, InvalidPathError
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.folder_validator import FolderValidator


class Copier(AbstractRootFolder):
    def copy_file(self, origin: str | Path, destination: str | Path) -> Path:
        origin_path = FileValidator.validate(origin)
        destination_path = Path(destination)

        if destination_path.exists() and destination_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            target_path = destination_path / origin_path.name
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            target_path = destination_path

        shutil.copy2(src=origin_path, dst=target_path)
        return target_path

    def copy(self, destination: str | Path, origin: str | Path | None = None, pattern: str = "*.txt") -> Path:
        if origin is None:
            origin = self.root_folder

        try:
            origin_file = FileValidator.validate(origin)
            return self.copy_file(origin=origin_file, destination=destination)
        except InvalidPathError:
            origin_folder = FolderValidator.validate(origin)

        destination_folder = self.__remove_dir_and_recreate(destination)

        source_files: list[Path] = self.__finder(root_folder=origin_folder).find_files(pattern)
        origin_folder_resolved = origin_folder.resolve()

        for source_path in source_files:
            source_resolved = source_path.resolve()
            try:
                relative_path = source_resolved.relative_to(origin_folder_resolved)
            except ValueError:
                continue

            target_path = destination_folder.joinpath(relative_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src=source_resolved, dst=target_path)

        return destination_folder

    def __remove_dir_and_recreate(self, path: str | Path) -> Path:
        path_obj = Path(path).resolve(strict=False)
        if path_obj.exists():
            if path_obj.is_dir():
                shutil.rmtree(path_obj)
            else:
                path_obj.unlink()
        path_obj.mkdir(parents=True, exist_ok=True)
        return path_obj

    def __finder(self, root_folder: Path | None = None) -> Finder:
        root = self.root_folder if root_folder is None else root_folder
        return Finder(
            root_folder=root,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )
